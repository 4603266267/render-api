import hmac
import hashlib
import time
import os
from fastapi.responses import FileResponse
from fastapi import Query
from pydantic import BaseModel, Field

DOWNLOAD_SECRET = os.getenv("DOWNLOAD_SECRET", "dev-secret")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

FILE_TTL_SECONDS = int(os.getenv("FILE_TTL_SECONDS", "21600"))  # 6 часа

def cleanup_old_outputs():
    now = time.time()

    for file_path in OUTPUT_DIR.glob("*.webp"):
        try:
            age = now - file_path.stat().st_mtime

            if age > FILE_TTL_SECONDS:
                file_path.unlink()
        except Exception:
            pass

def sign_download(filename, expires):
    message = f"{filename}:{expires}".encode()
    return hmac.new(
        DOWNLOAD_SECRET.encode(),
        message,
        hashlib.sha256
    ).hexdigest()

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pathlib import Path
import subprocess
import tempfile
import uuid
import re

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
FILE_TTL_SECONDS = int(os.getenv("FILE_TTL_SECONDS", "21600"))

ALLOWED_TEMPLATES = {"colorful-birthday","bright-gerbera"}

TEXT_RE = re.compile(r"^[\w\s.,!?;:'\"()\-–—&]+$", re.UNICODE)

class Fields(BaseModel):
    recp: str = Field(max_length=80)
    wish: str = Field(max_length=400)
    from_: str = Field(alias="from", max_length=80)
    dat: str = Field(max_length=40)

class RenderRequest(BaseModel):
    template: str
    fields: Fields

def clean_text(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n").strip()

    if not value:
        raise HTTPException(status_code=400, detail="Empty text field")

    if not TEXT_RE.match(value):
        raise HTTPException(status_code=400, detail="Unsupported characters")

    return value

@app.get("/download/{filename}")
def download_file(
    filename: str,
    expires: int = Query(...),
    token: str = Query(...)
):
    if not filename.endswith(".webp"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    if int(time.time() * 1000) > expires:
        raise HTTPException(status_code=403, detail="Download expired")

    expected = sign_download(filename, expires)

    if token != expected:
        raise HTTPException(status_code=403, detail="Invalid download token")

    file_path = (OUTPUT_DIR / filename).resolve()

    if not str(file_path).startswith(str(OUTPUT_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid path")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="image/webp"
    )

@app.post("/render")
def render(req: RenderRequest):
    cleanup_old_outputs()

    if req.template not in ALLOWED_TEMPLATES:
        raise HTTPException(status_code=400, detail="Invalid template")

    template_dir = TEMPLATES_DIR / req.template
    render_script = template_dir / "render.sh"

    if not render_script.exists():
        raise HTTPException(status_code=500, detail="Render script missing")

    fields = {
        "recp": clean_text(req.fields.recp),
        "wish": clean_text(req.fields.wish),
        "from": clean_text(req.fields.from_),
        "dat": clean_text(req.fields.dat),
    }

    job_id = uuid.uuid4().hex
    output_file = OUTPUT_DIR / f"{job_id}.webp"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)

        for name, text in fields.items():
            (tmp_dir / f"{name}.txt").write_text(text, encoding="utf-8")

        result = subprocess.run(
            [
                "bash",
                "./render.sh",
                str(tmp_dir).replace("\\", "/"),
                str(output_file).replace("\\", "/")
            ],
            shell=False,
            cwd=str(template_dir),
            timeout=30,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=result.stderr
            )

        expires = int(time.time() * 1000) + (6 * 60 * 60 * 1000)
        token = sign_download(output_file.name, expires)

        download_url = (
            f"{BASE_URL}/download/{output_file.name}"
            f"?expires={expires}&token={token}"
        )

        return {
            "ok": True,
            "file": f"/output/{output_file.name}",
            "download_url": download_url
        }
// server.js
import path from "path";
import fs from "fs";
import express from "express";

const app = express();

const OUTPUT_DIR = path.resolve("output");

app.get("/download/:filename", (req, res) => {
  const filename = req.params.filename;

  // allow only safe .webp filenames
  if (!/^[a-zA-Z0-9._-]+\.webp$/.test(filename)) {
    return res.status(400).json({
      ok: false,
      error: "Invalid filename"
    });
  }

  const filePath = path.join(OUTPUT_DIR, filename);
  const resolvedPath = path.resolve(filePath);

  // prevent path traversal
  if (!resolvedPath.startsWith(OUTPUT_DIR + path.sep)) {
    return res.status(403).json({
      ok: false,
      error: "Forbidden path"
    });
  }

  if (!fs.existsSync(resolvedPath)) {
    return res.status(404).json({
      ok: false,
      error: "File not found"
    });
  }

  res.setHeader("Content-Type", "image/webp");
  res.setHeader(
    "Content-Disposition",
    `attachment; filename="${filename}"`
  );

  return res.download(resolvedPath, filename);
});
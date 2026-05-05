FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    imagemagick \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i '/pattern="@\*"/ s|^|<!-- |; /pattern="@\*"/ s|$| -->|' /etc/ImageMagick-7/policy.xml

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/output

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
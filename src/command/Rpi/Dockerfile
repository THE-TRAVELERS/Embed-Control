FROM python:3.11-slim-bookworm

WORKDIR /app

ENV TERM=xterm

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    python3-picamera2 --no-install-recommends

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

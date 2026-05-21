# Multi-architecture: linux/amd64, linux/arm64
FROM python:3.11-slim

RUN groupadd -r appuser && useradd -r -g appuser -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN chown -R appuser:appuser /app

ARG APP_VERSION=1.0.0
ENV APP_VERSION=${APP_VERSION} \
    FAULT_DELAY_MS=0 \
    FAULT_ERROR_RATE=0.0

EXPOSE 8080
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

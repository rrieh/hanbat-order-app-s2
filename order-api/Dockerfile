# Multi-architecture: linux/amd64, linux/arm64 (Mac M칩 로컬 테스트 포함)
FROM python:3.11-slim

# 보안: non-root 사용자
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

WORKDIR /app

# 레이어 캐시 최적화: 의존성 먼저
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN chown -R appuser:appuser /app

ARG APP_VERSION=1.0.0
ENV APP_VERSION=${APP_VERSION} \
    PAYMENT_API_URL=http://payment-api:8080

EXPOSE 8080
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

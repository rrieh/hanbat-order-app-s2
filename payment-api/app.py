"""
payment-api · 한밭푸드 결제 서비스 (시즌 2)

Phase 1 장애 재현용:
  FAULT_DELAY_MS  : 응답 지연(ms). 기본값 0 (정상). 예) 8000 → 8초 지연
  FAULT_ERROR_RATE: 에러 주입률 0.0~1.0. 기본값 0.0 (에러 없음). 예) 0.5 → 50% 확률로 503 반환
"""

import asyncio
import os
import random
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="payment-api", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Fault injection 설정 (Phase 1 장애 재현 핵심)
# ---------------------------------------------------------------------------
FAULT_DELAY_MS: int = int(os.getenv("FAULT_DELAY_MS", "0"))
FAULT_ERROR_RATE: float = float(os.getenv("FAULT_ERROR_RATE", "0.0"))

# ---------------------------------------------------------------------------
# 샘플 결제 데이터
# ---------------------------------------------------------------------------
PAYMENTS: dict[str, dict] = {
    "ORD-001": {"order_id": "ORD-001", "amount": 32000, "method": "신용카드", "status": "승인완료", "pg_txn_id": "PG-20250401-001"},
    "ORD-002": {"order_id": "ORD-002", "amount": 15500, "method": "카카오페이", "status": "승인완료", "pg_txn_id": "PG-20250401-002"},
    "ORD-003": {"order_id": "ORD-003", "amount": 58000, "method": "신용카드", "status": "승인완료", "pg_txn_id": "PG-20250402-001"},
    "ORD-004": {"order_id": "ORD-004", "amount": 4500,  "method": "네이버페이", "status": "승인완료", "pg_txn_id": "PG-20250402-002"},
    "ORD-005": {"order_id": "ORD-005", "amount": 12000, "method": "신용카드", "status": "승인완료", "pg_txn_id": "PG-20250403-001"},
}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "payment-api"}


@app.get("/api/payments/{order_id}")
async def get_payment(order_id: str):
    """
    결제 정보 조회 API

    Phase 1 실습 포인트:
      - FAULT_DELAY_MS=8000 으로 배포 → order-api 스레드 포화 현상 재현
      - FAULT_ERROR_RATE=0.5 으로 배포  → order-api 에러 전파 재현
    """
    start = time.monotonic()

    # -----------------------------------------------------------------------
    # [FAULT INJECTION] 응답 지연 — Phase 1 장애 재현 핵심
    # FAULT_DELAY_MS 환경변수로 외부 PG사 응답 지연 시뮬레이션
    # -----------------------------------------------------------------------
    if FAULT_DELAY_MS > 0:
        await asyncio.sleep(FAULT_DELAY_MS / 1000)

    # -----------------------------------------------------------------------
    # [FAULT INJECTION] 에러율 주입 — 간헐적 결제 실패 시뮬레이션
    # FAULT_ERROR_RATE 환경변수: 0.0(정상) ~ 1.0(항상 에러)
    # -----------------------------------------------------------------------
    if FAULT_ERROR_RATE > 0.0 and random.random() < FAULT_ERROR_RATE:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "PG_GATEWAY_UNAVAILABLE",
                "message": "외부 PG사 응답 없음 (시뮬레이션)",
                "order_id": order_id,
            },
        )

    payment = PAYMENTS.get(order_id)
    if not payment:
        raise HTTPException(
            status_code=404,
            detail={"error": "PAYMENT_NOT_FOUND", "order_id": order_id},
        )

    elapsed_ms = int((time.monotonic() - start) * 1000)
    return {**payment, "response_time_ms": elapsed_ms}

# 한밭푸드 주문 조회 시스템 S2

> **Composable Architecture 운영 자동화 및 고도화** 강의 실습 레포지터리
> 강사: 김누리 (Skilleat, @feeltechedu)

---

## 배경

시즌 1에서 Azure Container Apps로 이관을 완료한 한밭푸드 주문 조회 시스템.
그로부터 1년 후, **지난 목요일 오후 2시** — 결제 API 응답 지연이 주문 조회 API 전체 장애로 번졌습니다.
44분간의 침묵 끝에 CTO가 세 가지 숙제를 내렸습니다.

| Phase | 주제 | 핵심 기술 |
|-------|------|----------|
| 1–2 | 장애 전파 차단 | Timeout · Retry · Circuit Breaker |
| 3–4 | 사람 손 덜 가는 배포 | GitHub Actions · ArgoCD (GitOps) |
| 5–6 | AI Agent 운영 자동화 | Azure OpenAI · Tool Calling |

---

## 서비스 구조

```
브라우저 → order-web (nginx)
                ↓
           order-api (FastAPI)
                ↓
          payment-api (FastAPI)   ← 여기가 느려지면 위로 전파됨
```

---

## 로컬 실행 (Docker Compose)

```bash
# 정상 동작 확인
docker compose up --build
# 브라우저 → http://localhost:8080

# Phase 1 장애 재현: FAULT_DELAY_MS 를 8000으로 변경 후
docker compose up --build
```

`docker-compose.yml` 의 `FAULT_DELAY_MS` / `FAULT_ERROR_RATE` 값을 바꿔서 장애를 재현할 수 있습니다.

---

## 환경변수 레퍼런스

### payment-api

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `FAULT_DELAY_MS` | `0` | 응답 지연(ms). `8000` = 8초 지연 |
| `FAULT_ERROR_RATE` | `0.0` | 에러 주입률 (0.0 ~ 1.0). `0.5` = 50% 확률 503 |

### order-api

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `PAYMENT_API_URL` | `http://payment-api:8080` | payment-api 주소 |

---

## 실습 가이드 사이트

👉 https://skilleat-labs.github.io/composable-ops-labs/

---

Copyright © 2026 Skilleat · 본 자료는 교육 목적으로만 사용 가능

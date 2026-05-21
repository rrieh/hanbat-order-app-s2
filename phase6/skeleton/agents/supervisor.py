"""
Phase 6 · Supervisor Agent
Log / Metrics / Event Agent 를 조율하여 종합 장애 보고서를 생성한다.

TODO: 전체 orchestrate() 함수를 구현하세요.
  힌트:
    1. 세 Agent 를 순서대로(또는 병렬로) 호출
    2. 각 결과를 합쳐 최종 요약 프롬프트 구성
    3. AzureOpenAI 로 종합 보고서 생성
    4. 심각도 / 근본 원인 / 권장 조치 세 파트로 구성 권장
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "<AZURE_OPENAI_ENDPOINT>"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", "<AZURE_OPENAI_API_KEY>"),
    api_version="2024-02-01",
)
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")


def orchestrate(target_deployment: str = "order-api") -> str:
    """
    TODO: 하위 Agent 결과를 취합해 종합 장애 보고서를 반환하세요.

    단계:
      1. log_agent.analyze_logs(target_deployment)
      2. metrics_agent.analyze_metrics()
      3. event_agent.analyze_events()
      4. 세 결과를 LLM 에 넘겨 최종 보고서 생성

    반환 예시 (Markdown 형식):
      ## 장애 분석 보고서
      ### 심각도: CRITICAL
      ### 근본 원인: payment-api 응답 지연 → order-api 스레드 포화
      ### 권장 조치: Circuit Breaker 적용 및 payment-api FAULT_DELAY_MS 확인
    """
    # TODO: 여기에 구현하세요
    raise NotImplementedError("orchestrate() 를 구현하세요!")

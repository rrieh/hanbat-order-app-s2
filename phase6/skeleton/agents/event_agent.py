"""
Phase 6 · Event Agent
쿠버네티스 이벤트를 분석하여 장애 징후를 반환한다.

TODO: analyze_events() 함수를 구현하세요.
  힌트:
    1. kubectl_events() 로 이벤트 수집
    2. Warning 이벤트에 집중하여 LLM 분석
    3. 타임라인(언제 무슨 일이 발생했는지) 형식으로 요약 권장
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openai import AzureOpenAI
from tools.kubectl_events import kubectl_events

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "<AZURE_OPENAI_ENDPOINT>"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", "<AZURE_OPENAI_API_KEY>"),
    api_version="2024-02-01",
)
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")


def analyze_events() -> str:
    """
    TODO: kubectl get events 결과를 LLM 으로 분석하고 요약을 반환하세요.

    반환 예시:
      "[3분 전] order-api Readiness probe 실패 → [2분 전] 컨테이너 재시작 반복"
    """
    # TODO: 여기에 구현하세요
    raise NotImplementedError("analyze_events() 를 구현하세요!")

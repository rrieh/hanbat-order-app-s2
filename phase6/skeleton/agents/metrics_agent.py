"""
Phase 6 · Metrics Agent
Pod CPU/메모리 사용량을 분석하여 병목 징후를 반환한다.

TODO: analyze_metrics() 함수를 구현하세요.
  힌트:
    1. kubectl_top_pods() 로 메트릭 수집
    2. AzureOpenAI 로 분석 → 한국어 요약 반환
    3. log_agent.py 의 analyze_logs() 를 참고하세요
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openai import AzureOpenAI
from tools.kubectl_top import kubectl_top_pods

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "<AZURE_OPENAI_ENDPOINT>"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", "<AZURE_OPENAI_API_KEY>"),
    api_version="2024-02-01",
)
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")


def analyze_metrics() -> str:
    """
    TODO: kubectl top pods 결과를 LLM 으로 분석하고 요약을 반환하세요.

    반환 예시:
      "order-api CPU 사용률 450m (limit 500m) — 포화 임박. 스케일 아웃 권장."
    """
    # TODO: 여기에 구현하세요
    raise NotImplementedError("analyze_metrics() 를 구현하세요!")

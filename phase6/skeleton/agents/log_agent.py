"""
Phase 6 · Log Agent
Pod 로그를 수집·분석하여 이상 징후 요약을 반환한다.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openai import AzureOpenAI
from tools.kubectl_logs import kubectl_logs

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "<AZURE_OPENAI_ENDPOINT>"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", "<AZURE_OPENAI_API_KEY>"),
    api_version="2024-02-01",
)
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")


def analyze_logs(deployment: str) -> str:
    """지정 Deployment 의 로그를 LLM 으로 분석하고 요약 반환."""
    logs = kubectl_logs(deployment)
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 쿠버네티스 운영 전문가입니다. "
                    "다음 Pod 로그에서 에러, 경고, 이상 패턴을 찾아 한국어로 요약하세요. "
                    "심각도(CRITICAL/WARNING/INFO)와 원인을 명시하세요."
                ),
            },
            {"role": "user", "content": f"[{deployment} 로그]\n{logs}"},
        ],
    )
    return response.choices[0].message.content

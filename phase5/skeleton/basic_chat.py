"""
Phase 5 · 스켈레톤 1: Azure OpenAI 기본 호출

실습 목표:
  - Azure OpenAI 엔드포인트에 연결하고 간단한 질의응답을 수행한다
  - gpt-4o-mini 모델의 응답 구조를 이해한다

환경변수 (강사 제공):
  AZURE_OPENAI_ENDPOINT   예) https://xxxxx.openai.azure.com/
  AZURE_OPENAI_API_KEY    강사 제공 키
  AZURE_OPENAI_DEPLOYMENT 배포 이름 (예: gpt-4o-mini)
"""

import os
from openai import AzureOpenAI

# ---------------------------------------------------------------------------
# TODO 1: 환경변수에서 설정 읽기
# ---------------------------------------------------------------------------
endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT", "<AZURE_OPENAI_ENDPOINT>")
api_key    = os.getenv("AZURE_OPENAI_API_KEY",   "<AZURE_OPENAI_API_KEY>")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

# ---------------------------------------------------------------------------
# TODO 2: AzureOpenAI 클라이언트 초기화
# ---------------------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-01",
)


def chat(user_message: str) -> str:
    """단일 메시지를 보내고 응답 텍스트를 반환한다."""
    # TODO 3: client.chat.completions.create() 호출
    #   - model: deployment
    #   - messages: [{"role": "user", "content": user_message}]
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "당신은 한밭푸드 운영팀을 돕는 AI 어시스턴트입니다."},
            {"role": "user",   "content": user_message},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print("=== Azure OpenAI 기본 연결 테스트 ===")
    answer = chat("안녕하세요. 간단히 자기소개를 해주세요.")
    print(answer)

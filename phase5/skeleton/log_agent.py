"""
Phase 5 · 스켈레톤 2: Tool Calling 로그 분석 Agent

실습 목표:
  - Tool(Function) Calling 패턴을 이해한다
  - LLM 이 스스로 도구를 선택하고 결과를 해석하는 흐름을 체험한다
  - kubectl logs 를 도구로 노출하여 장애 원인을 분석하게 한다

흐름:
  사용자 질문 → LLM (어떤 도구 쓸지 결정) → 도구 실행 → 결과 반환 → LLM (최종 답변)
"""

import json
import os
import subprocess
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "<AZURE_OPENAI_ENDPOINT>"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", "<AZURE_OPENAI_API_KEY>"),
    api_version="2024-02-01",
)
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
NAMESPACE  = os.getenv("K8S_NAMESPACE", "hanbat-<본인_GitHub_사용자명>")

# ---------------------------------------------------------------------------
# Tool 정의 — LLM 에 노출할 함수 스펙
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_pod_logs",
            "description": "지정한 서비스의 최근 Pod 로그를 조회한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "서비스 이름. 예: order-api, payment-api, order-web",
                    },
                    "tail_lines": {
                        "type": "integer",
                        "description": "가져올 로그 줄 수. 기본값 50",
                        "default": 50,
                    },
                },
                "required": ["service_name"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Tool 구현
# ---------------------------------------------------------------------------
def get_pod_logs(service_name: str, tail_lines: int = 50) -> str:
    """kubectl logs 로 Pod 로그를 가져온다."""
    # TODO: 실제 클러스터 연결 후 주석 해제
    # cmd = [
    #     "kubectl", "logs",
    #     f"deployment/{service_name}",
    #     "-n", NAMESPACE,
    #     f"--tail={tail_lines}",
    # ]
    # result = subprocess.run(cmd, capture_output=True, text=True)
    # return result.stdout or result.stderr

    # 로컬 실습용 더미 로그 (클러스터 없을 때)
    dummy_logs = {
        "order-api": (
            "INFO:     Started server process\n"
            "INFO:     Uvicorn running on http://0.0.0.0:8080\n"
            "ERROR:    httpx.ReadTimeout: timed out waiting for payment-api response\n"
            "ERROR:    httpx.ReadTimeout: timed out waiting for payment-api response\n"
            "WARNING:  Thread pool exhausted: 50/50 workers busy\n"
        ),
        "payment-api": (
            "INFO:     Started server process\n"
            "INFO:     GET /api/payments/ORD-001  → sleeping 8000ms (FAULT_DELAY_MS)\n"
            "INFO:     GET /api/payments/ORD-002  → sleeping 8000ms (FAULT_DELAY_MS)\n"
        ),
    }
    return dummy_logs.get(service_name, f"[{service_name}] 로그 없음")


def dispatch_tool(name: str, arguments: str) -> str:
    """LLM 이 선택한 도구를 실행하고 결과 문자열을 반환한다."""
    args = json.loads(arguments)
    if name == "get_pod_logs":
        return get_pod_logs(**args)
    return f"알 수 없는 도구: {name}"


# ---------------------------------------------------------------------------
# Agent 루프
# ---------------------------------------------------------------------------
def run_agent(user_question: str) -> str:
    """
    ReAct 패턴: Think → Act(Tool) → Observe → Answer
    최대 3턴 동안 도구 호출을 허용한다.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "당신은 한밭푸드 운영팀의 AI 에이전트입니다. "
                "장애 분석을 위해 필요하다면 get_pod_logs 도구를 사용하세요. "
                "분석 결과는 한국어로 간결하게 답변하세요."
            ),
        },
        {"role": "user", "content": user_question},
    ]

    for turn in range(3):  # 최대 3턴
        response = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        msg = response.choices[0].message

        # 도구 호출이 없으면 최종 답변
        if not msg.tool_calls:
            return msg.content

        # 도구 실행
        messages.append(msg)
        for tool_call in msg.tool_calls:
            result = dispatch_tool(tool_call.function.name, tool_call.function.arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    # 루프 초과 시 마지막 응답 반환
    return response.choices[0].message.content or "분석 완료 (최대 턴 도달)"


if __name__ == "__main__":
    print("=== 로그 분석 Agent ===")
    answer = run_agent("order-api 에서 왜 에러가 발생하고 있는지 로그를 보고 분석해줘.")
    print(answer)

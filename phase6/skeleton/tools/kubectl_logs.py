"""
Tool: kubectl logs
Pod 로그를 조회하여 문자열로 반환한다.
"""
import os
import subprocess


NAMESPACE = os.getenv("K8S_NAMESPACE", "hanbat-<본인_GitHub_사용자명>")


def kubectl_logs(deployment: str, tail: int = 100) -> str:
    """
    kubectl logs deployment/<deployment> -n <namespace> --tail=<tail>
    클러스터 연결이 없을 때는 더미 데이터 반환.
    """
    try:
        result = subprocess.run(
            ["kubectl", "logs", f"deployment/{deployment}", "-n", NAMESPACE, f"--tail={tail}"],
            capture_output=True, text=True, timeout=10,
        )
        return result.stdout or result.stderr or "(로그 없음)"
    except FileNotFoundError:
        return f"[STUB] {deployment} 로그 (kubectl 없음 — 로컬 스텁 반환)\nERROR: timeout calling payment-api"
    except subprocess.TimeoutExpired:
        return "(kubectl 명령 타임아웃)"

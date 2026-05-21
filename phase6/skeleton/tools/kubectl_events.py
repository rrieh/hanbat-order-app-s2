"""
Tool: kubectl get events
네임스페이스의 최근 이벤트를 조회하여 문자열로 반환한다.
"""
import os
import subprocess


NAMESPACE = os.getenv("K8S_NAMESPACE", "hanbat-<본인_GitHub_사용자명>")


def kubectl_events() -> str:
    """
    kubectl get events -n <namespace> --sort-by='.lastTimestamp'
    """
    try:
        result = subprocess.run(
            ["kubectl", "get", "events", "-n", NAMESPACE, "--sort-by=.lastTimestamp"],
            capture_output=True, text=True, timeout=10,
        )
        return result.stdout or result.stderr or "(이벤트 없음)"
    except FileNotFoundError:
        return (
            "[STUB] kubectl get events (로컬 스텁)\n"
            "LAST SEEN   TYPE      REASON              OBJECT                    MESSAGE\n"
            "2m          Warning   BackOff             pod/order-api-xxx         Back-off restarting failed container\n"
            "3m          Warning   Unhealthy           pod/order-api-xxx         Readiness probe failed: HTTP probe failed\n"
        )
    except subprocess.TimeoutExpired:
        return "(kubectl events 타임아웃)"

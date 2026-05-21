"""
Tool: kubectl top pods
Pod CPU/메모리 사용량을 조회하여 문자열로 반환한다.
"""
import os
import subprocess


NAMESPACE = os.getenv("K8S_NAMESPACE", "hanbat-<본인_GitHub_사용자명>")


def kubectl_top_pods() -> str:
    """
    kubectl top pods -n <namespace>
    """
    try:
        result = subprocess.run(
            ["kubectl", "top", "pods", "-n", NAMESPACE],
            capture_output=True, text=True, timeout=10,
        )
        return result.stdout or result.stderr or "(메트릭 없음)"
    except FileNotFoundError:
        return (
            "[STUB] kubectl top pods (로컬 스텁)\n"
            "NAME                          CPU(cores)   MEMORY(bytes)\n"
            "order-api-6d9f7b8c9-xk2lp    450m         198Mi\n"
            "payment-api-5c8b7d6f4-mn3qr  12m           64Mi\n"
            "order-web-7f9c6b5d3-pq4rs    5m            32Mi\n"
        )
    except subprocess.TimeoutExpired:
        return "(kubectl top 타임아웃)"

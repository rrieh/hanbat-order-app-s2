"""
Phase 6 · 미니 프로젝트 진입점

사용법:
  python main.py
  python main.py --deployment payment-api

TODO: metrics_agent, event_agent, supervisor 구현 후
      주석 처리된 전체 실행 코드를 활성화하세요.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from agents.log_agent import analyze_logs


def main():
    parser = argparse.ArgumentParser(description="한밭푸드 장애 분석 Agent")
    parser.add_argument("--deployment", default="order-api", help="분석할 Deployment 이름")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  한밭푸드 장애 분석 Agent — 대상: {args.deployment}")
    print(f"{'='*60}\n")

    # Phase 6 Step 1: 로그 분석 (log_agent 완성 후 동작)
    print("[ 1/3 ] 로그 분석 중...")
    log_report = analyze_logs(args.deployment)
    print(log_report)

    # TODO Phase 6 Step 2: 메트릭 분석 (metrics_agent 구현 후 주석 해제)
    # from agents.metrics_agent import analyze_metrics
    # print("\n[ 2/3 ] 메트릭 분석 중...")
    # metrics_report = analyze_metrics()
    # print(metrics_report)

    # TODO Phase 6 Step 3: 이벤트 분석 (event_agent 구현 후 주석 해제)
    # from agents.event_agent import analyze_events
    # print("\n[ 3/3 ] 이벤트 분석 중...")
    # event_report = analyze_events()
    # print(event_report)

    # TODO Phase 6 Step 4: 종합 보고서 (supervisor 구현 후 주석 해제)
    # from agents.supervisor import orchestrate
    # print("\n[ 종합 보고서 생성 중... ]")
    # report = orchestrate(args.deployment)
    # print(report)


if __name__ == "__main__":
    main()

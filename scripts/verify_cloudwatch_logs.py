from __future__ import annotations

import sys
import time

import boto3


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/verify_cloudwatch_logs.py <log-group-name>")
        return 2

    log_group = sys.argv[1]
    logs = boto3.client("logs")
    end_time = int(time.time() * 1000)
    start_time = end_time - 30 * 60 * 1000

    response = logs.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        limit=10,
    )
    events = response.get("events", [])
    if not events:
        print(f"No recent CloudWatch log events found in {log_group}.")
        return 1

    print(f"Found {len(events)} recent CloudWatch log event(s) in {log_group}.")
    for event in events[:3]:
        print(event.get("message", "").strip()[:300])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

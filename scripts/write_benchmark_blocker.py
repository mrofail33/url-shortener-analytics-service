from __future__ import annotations

import json
import subprocess
from pathlib import Path


def main() -> int:
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        docker_stdout = result.stdout.strip()
        docker_stderr = result.stderr.strip()
        docker_returncode = result.returncode
    except Exception as exc:
        docker_stdout = ""
        docker_stderr = f"{type(exc).__name__}: {exc}"
        docker_returncode = None

    summary = {
        "benchmark_date": "2026-09-23",
        "status": "blocked",
        "blocked_components": ["PostgreSQL", "Redis"],
        "reason": "Docker engine was not running, so docker-compose services required for the real redirect benchmark were unavailable.",
        "attempted_benchmark": "scripts/benchmark_redirects.py requires the repo's real PostgreSQL and Redis services.",
        "docker_ps_returncode": docker_returncode,
        "docker_ps_stdout": docker_stdout,
        "docker_ps_stderr": docker_stderr,
        "metrics_not_reported": [
            "average redirect latency",
            "successful request rate",
            "Redis cache hit rate",
            "cached vs uncached database behavior",
        ],
    }
    output = Path("docs/benchmark-results/redirect_benchmark_blocked_2026-09-23.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

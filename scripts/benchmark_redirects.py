from __future__ import annotations

import argparse
import json
import os
import statistics
import time
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/url_shortener")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("BASE_URL", "http://testserver")

from fastapi.testclient import TestClient
from redis import Redis
from sqlalchemy import event, text

from app.db.base import Base
from app.db.session import engine
from app.main import app


def percentile(values: list[float], pct: float) -> float:
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * pct))
    return ordered[index]


def run_phase(client: TestClient, redis_client: Redis, short_code: str, requests: int, force_uncached: bool):
    latencies = []
    successes = 0
    cache_hits = 0
    query_count = 0
    short_url_selects = 0

    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        nonlocal query_count, short_url_selects
        query_count += 1
        if "short_urls" in statement.lower() and statement.lstrip().lower().startswith("select"):
            short_url_selects += 1

    event.listen(engine, "before_cursor_execute", before_cursor_execute)
    try:
        for _ in range(requests):
            key = f"url:{short_code}"
            if force_uncached:
                redis_client.delete(key)
            was_cached = redis_client.exists(key) == 1
            started = time.perf_counter()
            response = client.get(f"/{short_code}", follow_redirects=False)
            latencies.append((time.perf_counter() - started) * 1000)
            if response.status_code == 307:
                successes += 1
            if was_cached:
                cache_hits += 1
    finally:
        event.remove(engine, "before_cursor_execute", before_cursor_execute)

    return {
        "requests": requests,
        "successful_requests": successes,
        "successful_request_rate": successes / requests,
        "cache_hits": cache_hits,
        "cache_hit_rate": cache_hits / requests,
        "average_latency_ms": statistics.mean(latencies),
        "median_latency_ms": statistics.median(latencies),
        "p95_latency_ms": percentile(latencies, 0.95),
        "total_db_statements": query_count,
        "short_url_selects": short_url_selects,
        "avg_db_statements_per_redirect": query_count / requests,
        "avg_short_url_selects_per_redirect": short_url_selects / requests,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark cached and uncached redirect paths.")
    parser.add_argument("--requests-per-phase", type=int, default=500)
    parser.add_argument("--output", default="docs/benchmark-results/redirect_benchmark_2026-09-23.json")
    args = parser.parse_args()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    redis_client = Redis.from_url(os.environ["REDIS_URL"], decode_responses=True)
    redis_client.flushdb()

    client = TestClient(app)
    create_response = client.post("/api/urls", json={"original_url": "https://example.com/benchmark"})
    create_response.raise_for_status()
    short_code = create_response.json()["short_code"]

    uncached = run_phase(client, redis_client, short_code, args.requests_per_phase, force_uncached=True)
    redis_client.delete(f"url:{short_code}")
    client.get(f"/{short_code}", follow_redirects=False)
    cached = run_phase(client, redis_client, short_code, args.requests_per_phase, force_uncached=False)

    summary = {
        "benchmark_date": "2026-09-23",
        "database": "PostgreSQL via docker-compose",
        "cache": "Redis via docker-compose",
        "total_redirect_requests": args.requests_per_phase * 2,
        "short_code": short_code,
        "uncached_phase": uncached,
        "cached_phase": cached,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

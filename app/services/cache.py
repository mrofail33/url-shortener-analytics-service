import json
from typing import Any

from redis import Redis
from redis.exceptions import RedisError

from app.core.config import get_settings


settings = get_settings()


def get_redis_client() -> Redis:
    return Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=0.2,
        socket_timeout=0.2,
    )


def get_cached_url(short_code: str) -> dict[str, Any] | None:
    try:
        cached = get_redis_client().get(f"url:{short_code}")
    except RedisError:
        return None

    if not cached:
        return None

    return json.loads(cached)


def set_cached_url(short_code: str, url_data: dict[str, Any]) -> None:
    try:
        get_redis_client().setex(
            f"url:{short_code}",
            settings.redis_ttl_seconds,
            json.dumps(url_data),
        )
    except RedisError:
        # Redis improves performance, but the API should still work if cache is unavailable.
        return

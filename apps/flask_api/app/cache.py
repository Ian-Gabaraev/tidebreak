"""Redis caching helpers for API responses."""

import json
import logging
from typing import Any

import redis

logger = logging.getLogger(__name__)


class CacheClient:
    def __init__(self, redis_url: str, default_ttl: int = 300) -> None:
        self.default_ttl = default_ttl
        self.client = None

        try:
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Redis unavailable, continuing without cache: %s", exc)
            self.client = None

    def get_json(self, key: str) -> Any | None:
        if self.client is None:
            return None

        payload = self.client.get(key)
        if not payload:
            return None

        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return None

    def set_json(self, key: str, value: Any, ttl: int | None = None) -> None:
        if self.client is None:
            return

        expiry = ttl if ttl is not None else self.default_ttl
        self.client.setex(key, expiry, json.dumps(value))

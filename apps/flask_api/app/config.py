"""Runtime configuration for Flask API service."""

import os


class Config:
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    SQLITE_PATH = os.getenv("SQLITE_PATH", "./apps/flask_api/data/tidebreak_api.db")

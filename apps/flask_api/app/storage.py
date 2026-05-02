"""SQLite persistence for request logs."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class SQLiteStorage:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS request_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country_code TEXT NOT NULL,
                    article_count INTEGER NOT NULL,
                    from_cache INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                )
                """)
            conn.commit()

    def log_request(self, country_code: str, article_count: int, from_cache: bool) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO request_log (country_code, article_count, from_cache, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    country_code,
                    article_count,
                    1 if from_cache else 0,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()

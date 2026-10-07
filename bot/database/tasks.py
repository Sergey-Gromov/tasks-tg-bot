"""SQLite входит в Python — отдельный сервер базы данных не нужен."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class Database:
    def __init__(self, path: Path):
        self.path = path

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    user TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    def add_task(self, text: str, user: str) -> int:
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with sqlite3.connect(self.path) as connection:
            # Параметры защищают запрос от кавычек и SQL в тексте задачи.
            cursor = connection.execute(
                "INSERT INTO tasks (text, user, created_at) VALUES (?, ?, ?)",
                (text, user, created_at),
            )
            return cursor.lastrowid

    def list_tasks(self) -> list[sqlite3.Row]:
        with sqlite3.connect(self.path) as connection:
            connection.row_factory = sqlite3.Row
            return connection.execute(
                "SELECT id, text, user, created_at FROM tasks ORDER BY id"
            ).fetchall()

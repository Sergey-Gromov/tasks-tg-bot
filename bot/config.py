"""Настройки читаются из .env и переменных окружения."""

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    token: str
    database_path: Path
    proxy_url: str | None = None


def load_config() -> Config:
    load_dotenv(PROJECT_ROOT / ".env")
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token or token == "your_bot_token_here":
        raise ValueError("Укажите BOT_TOKEN в файле .env (токен от @BotFather).")
    path = Path(os.getenv("DATABASE_PATH", "data/tasks.db"))
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    proxy_url = os.getenv("TELEGRAM_PROXY_URL", "").strip() or None
    if proxy_url:
        try:
            parsed = urlsplit(proxy_url)
            valid = (
                parsed.scheme in {"socks5", "socks4", "http"}
                and parsed.hostname and parsed.port
                and parsed.path in {"", "/"}
                and not parsed.query and not parsed.fragment
            )
        except ValueError:
            valid = False
        if not valid:
            raise ValueError(
                "TELEGRAM_PROXY_URL должен быть адресом локального прокси, "
                "например socks5://127.0.0.1:10808. Ссылка vless:// не подходит."
            )
    return Config(token=token, database_path=path, proxy_url=proxy_url)

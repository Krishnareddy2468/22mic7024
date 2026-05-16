import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def env_value(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()

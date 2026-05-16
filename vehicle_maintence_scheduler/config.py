import os

from dotenv import load_dotenv

load_dotenv()


def env_value(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()

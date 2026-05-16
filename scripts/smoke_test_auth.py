#!/usr/bin/env python3
"""Verify POST /auth returns access_token. Run after register + .env filled."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from logging_middleware.client import get_token


def main() -> int:
    try:
        token = get_token()
    except Exception:
        print("FAIL: get_token() failed (check stderr and .env)", file=sys.stderr)
        return 1

    if not token:
        print("FAIL: empty access token", file=sys.stderr)
        return 1

    print(f"OK: access_token={token[:12]}... (truncated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

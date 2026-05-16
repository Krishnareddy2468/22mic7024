#!/usr/bin/env python3
"""Verify Log() returns 200 with logID. Run from repo root after filling .env."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from logging_middleware import Log


def main() -> int:
    result = Log(
        "backend",
        "info",
        "utils",
        "smoke test: logging_middleware ready",
    )
    if not result:
        print("FAIL: Log() returned None (check stderr and .env)", file=sys.stderr)
        return 1

    log_id = result.get("logID") or result.get("logId")
    if not log_id:
        print(f"FAIL: response missing logID: {result}", file=sys.stderr)
        return 1

    print(f"OK: logID={log_id}")
    print(f"response: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

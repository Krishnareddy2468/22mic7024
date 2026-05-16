#!/usr/bin/env python3
"""One-time POST /register. Prints clientID and clientSecret for .env."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from logging_middleware.client import register


def main() -> int:
    try:
        data = register()
    except Exception:
        print(
            "FAIL: register failed (check stderr, .env, and that you have not "
            "already registered this roll number)",
            file=sys.stderr,
        )
        return 1

    client_id = data.get("clientID") or data.get("clientId")
    client_secret = data.get("clientSecret")
    if not client_id or not client_secret:
        print(f"FAIL: unexpected response: {data}", file=sys.stderr)
        return 1

    print("OK: registration succeeded")
    print(f"EVAL_CLIENT_ID={client_id}")
    print(f"EVAL_CLIENT_SECRET={client_secret}")
    print("\nAdd the two lines above to your .env, then run:")
    print("  python scripts/smoke_test_log.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

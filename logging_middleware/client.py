import os
import sys
import time
from typing import Any, Optional

import httpx

from .constants import REQUEST_TIMEOUT_SEC, get_base_url

_token: Optional[str] = None
_token_expires_at: float = 0.0


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _register_payload() -> dict[str, str]:
    return {
        "email": required_env("EVAL_EMAIL"),
        "name": required_env("EVAL_NAME"),
        "mobileNo": required_env("EVAL_MOBILE"),
        "githubUsername": required_env("EVAL_GITHUB_USERNAME"),
        "rollNo": required_env("EVAL_ROLL_NO"),
        "accessCode": required_env("EVAL_ACCESS_CODE"),
    }


def _auth_payload() -> dict[str, str]:
    return {
        "email": required_env("EVAL_EMAIL"),
        "name": required_env("EVAL_NAME"),
        "rollNo": required_env("EVAL_ROLL_NO"),
        "accessCode": required_env("EVAL_ACCESS_CODE"),
        "clientID": required_env("EVAL_CLIENT_ID"),
        "clientSecret": required_env("EVAL_CLIENT_SECRET"),
    }


def register() -> dict:
    url = f"{get_base_url()}/register"
    try:
        response = httpx.post(
            url,
            json=_register_payload(),
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT_SEC,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        _log_local(f"register failed: {exc}")
        if isinstance(exc, httpx.HTTPStatusError):
            _log_local(f"response body: {exc.response.text[:500]}")
        raise


def _parse_expires_at(expires_in: Any) -> float:
    try:
        raw = float(expires_in)
    except (TypeError, ValueError):
        return time.time() + 3600

    if raw > 1_000_000_000:
        return raw
    return time.time() + max(raw, 60)


def get_token(force_refresh: bool = False) -> str:
    global _token, _token_expires_at

    if not force_refresh and _token and time.time() < (_token_expires_at - 30):
        return _token

    url = f"{get_base_url()}/auth"
    try:
        response = httpx.post(
            url,
            json=_auth_payload(),
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT_SEC,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        _log_local(f"auth failed: {exc}")
        raise

    token = data.get("access_token") or data.get("accessToken")
    if not token:
        _log_local(f"auth response missing access_token: {data}")
        raise ValueError("auth response missing access_token")

    _token = token
    _token_expires_at = _parse_expires_at(data.get("expires_in", 3600))
    return _token


def post_log(payload: dict[str, str]) -> Optional[dict]:
    try:
        token = get_token()
    except Exception:
        return None

    url = f"{get_base_url()}/logs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        response = httpx.post(
            url,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SEC,
        )
        if response.status_code == 401:
            token = get_token(force_refresh=True)
            headers["Authorization"] = f"Bearer {token}"
            response = httpx.post(
                url,
                json=payload,
                headers=headers,
                timeout=REQUEST_TIMEOUT_SEC,
            )
        if response.status_code not in (200, 201):
            _log_local(f"log POST {response.status_code}: {response.text[:500]}")
            return None
        return response.json()
    except Exception as exc:
        _log_local(f"log POST failed: {exc}")
        return None


def _log_local(message: str) -> None:
    print(f"[logging_middleware] {message}", file=sys.stderr)

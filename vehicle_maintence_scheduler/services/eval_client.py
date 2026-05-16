import httpx
from logging_middleware import Log
from logging_middleware.client import get_token
from logging_middleware.constants import REQUEST_TIMEOUT_SEC, get_base_url


def _headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {get_token()}"}


def _get(path: str) -> dict:
    url = f"{get_base_url()}{path}"
    try:
        response = httpx.get(
            url,
            headers=_headers(),
            timeout=REQUEST_TIMEOUT_SEC,
        )
        if response.status_code == 401:
            get_token(force_refresh=True)
            response = httpx.get(
                url,
                headers=_headers(),
                timeout=REQUEST_TIMEOUT_SEC,
            )
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException:
        Log("backend", "error", "handler", f"{path} timeout after {REQUEST_TIMEOUT_SEC}s")
        raise
    except httpx.HTTPStatusError as exc:
        Log("backend", "error", "handler", f"{path} returned {exc.response.status_code}")
        raise
    except Exception as exc:
        Log("backend", "error", "handler", f"{path} failed: {exc}")
        raise


def fetch_depots() -> list[dict]:
    data = _get("/depots")
    depots = data.get("depots", [])
    Log("backend", "info", "service", f"depots API returned {len(depots)} depots")
    return depots


def fetch_vehicles() -> list[dict]:
    data = _get("/vehicles")
    vehicles = data.get("vehicles", [])
    Log("backend", "info", "service", f"vehicles API returned {len(vehicles)} tasks")
    return vehicles

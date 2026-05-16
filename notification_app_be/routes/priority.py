from fastapi import APIRouter, HTTPException, Query
from logging_middleware import Log

from services.eval_client import fetch_notifications
from services.priority_inbox import format_notification, top_notifications

router = APIRouter(tags=["notifications"])


@router.get("/notifications/priority")
def get_priority_notifications(n: int = Query(default=10, ge=1, le=50)):
    Log("backend", "info", "route", f"building priority notification list, limit={n}")
    try:
        notifications = fetch_notifications()
    except Exception as exc:
        Log("backend", "error", "route", f"notification fetch failed: {exc}")
        raise HTTPException(status_code=502, detail="evaluation notifications API unavailable") from exc

    top = top_notifications(notifications, n=n)
    Log(
        "backend",
        "info",
        "service",
        f"priority inbox selected {len(top)} of {len(notifications)} notifications",
    )
    return {
        "limit": n,
        "totalFetched": len(notifications),
        "notifications": [format_notification(item) for item in top],
    }

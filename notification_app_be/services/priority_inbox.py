import heapq
from datetime import datetime

TYPE_WEIGHT = {"Placement": 3, "Result": 2, "Event": 1}


def _field(notification: dict, *keys: str, default: str = "") -> str:
    for key in keys:
        if key in notification and notification[key] is not None:
            return str(notification[key])
    return default


def parse_timestamp(raw: str) -> datetime:
    text = raw.strip()
    supported_formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S.%f",
    )

    for fmt in supported_formats:
        try:
            return datetime.strptime(text.replace("Z", ""), fmt.replace("Z", ""))
        except ValueError:
            continue
    return datetime.min


def score(notification: dict) -> tuple[int, datetime]:
    notification_type = _field(notification, "Type", "type", default="Event")
    priority = TYPE_WEIGHT.get(notification_type, 0)
    created_at = parse_timestamp(_field(notification, "Timestamp", "timestamp", "createdAt"))
    return (priority, created_at)


def is_unread(notification: dict) -> bool:
    for key in ("isRead", "is_read", "IsRead", "read"):
        if key in notification:
            return not bool(notification[key])
    return True


def _heap_entry(notification: dict) -> tuple[tuple[int, datetime], str, dict]:
    return (score(notification), _field(notification, "ID", "id"), notification)


def top_notifications(notifications: list[dict], n: int = 10) -> list[dict]:
    unread = [item for item in notifications if is_unread(item)]
    limit = max(1, n)
    heap: list[tuple[tuple[int, datetime], str, dict]] = []

    for notification in unread:
        entry = _heap_entry(notification)
        if len(heap) < limit:
            heapq.heappush(heap, entry)
        elif entry > heap[0]:
            heapq.heapreplace(heap, entry)

    ranked = sorted(heap, key=lambda item: (item[0][0], item[0][1]), reverse=True)
    return [item[2] for item in ranked]


def format_notification(notification: dict) -> dict:
    return {
        "id": _field(notification, "ID", "id"),
        "type": _field(notification, "Type", "type"),
        "message": _field(notification, "Message", "message"),
        "timestamp": _field(notification, "Timestamp", "timestamp", "createdAt"),
    }

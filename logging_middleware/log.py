from typing import Optional

from .client import _log_local, post_log
from .constants import LEVELS, PACKAGES, STACKS


def _invalid_value(field: str, value: str, allowed: frozenset[str]) -> Optional[str]:
    normalized = value.strip().lower()
    if normalized not in allowed:
        allowed_values = ", ".join(sorted(allowed))
        return f"invalid {field} '{value}'; allowed: {allowed_values}"
    return None


def Log(stack: str, level: str, package: str, message: str) -> Optional[dict]:
    for error in (
        _invalid_value("stack", stack, STACKS),
        _invalid_value("level", level, LEVELS),
        _invalid_value("package", package, PACKAGES),
    ):
        if error:
            _log_local(error)
            return None

    if not message or not str(message).strip():
        _log_local("message must be non-empty")
        return None

    payload = {
        "stack": stack.strip().lower(),
        "level": level.strip().lower(),
        "package": package.strip().lower(),
        "message": str(message).strip(),
    }
    return post_log(payload)

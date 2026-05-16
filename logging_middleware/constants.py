import os

DEFAULT_BASE_URL = "http://4.224.186.213/evaluation-service"
REQUEST_TIMEOUT_SEC = 5.0


def get_base_url() -> str:
    return os.getenv("EVAL_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


STACKS = frozenset({"backend", "frontend"})
LEVELS = frozenset({"debug", "info", "warn", "error", "fatal"})
PACKAGES = frozenset(
    {
        "auth",
        "cache",
        "config",
        "controller",
        "cron_job",
        "db",
        "domain",
        "handler",
        "middleware",
        "repository",
        "route",
        "service",
        "utils",
    }
)

# 22MIC7024

Backend assessment for Afford Medical Tech.

## What's inside

Two FastAPI services and a shared logging package.

**Notification Priority Inbox** (port 8000)
- `GET /notifications/priority?n=10` — top n notifications sorted by priority
- `GET /health`

**Vehicle Maintenance Scheduler** (port 8001)
- `GET /schedule` — schedules for all depots
- `GET /depots/{depot_id}/schedule` — schedule for a single depot
- `GET /health`

**Logging Middleware** — `pip install -e ./logging_middleware` gives you `Log(stack, level, package, message)` to push logs to the evaluation service. Both services use it.

## Running locally

Detailed steps are in [LOCAL_SETUP.md](LOCAL_SETUP.md).

```bash
cp .env.example .env
pip install -e ./logging_middleware
python scripts/register.py
python scripts/smoke_test_auth.py
python scripts/smoke_test_log.py

# start notification app
cd notification_app_be && uvicorn main:app --reload --port 8000

# start vehicle scheduler
cd vehicle_maintence_scheduler && uvicorn main:app --reload --port 8001
```



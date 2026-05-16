# 22MIC7024

Backend assessment submission for Afford Medical Tech pre-test.

## Project Overview

This repository contains two FastAPI microservices with a shared logging middleware:

| Service | Port | Description |
|---------|------|-------------|
| **Notification Priority Inbox** | 8000 | Fetches notifications from the evaluation API and returns the top priority items sorted by weight |
| **Vehicle Maintenance Scheduler** | 8001 | Generates optimal maintenance schedules for vehicle depots using a knapsack-based approach |

### Notification Priority Inbox

- `GET /notifications/priority?n=10` — Returns the top *n* priority notifications, sorted by priority weight
- `GET /health` — Health check

### Vehicle Maintenance Scheduler

- `GET /schedule` — Returns maintenance schedules for all depots
- `GET /depots/{depot_id}/schedule` — Returns the maintenance schedule for a specific depot
- `GET /health` — Health check

### Logging Middleware

A reusable Python package (`logging_middleware`) that provides a `Log()` helper to send structured log entries to the evaluation service. Used across both microservices at route, service, and repository boundaries.

## Quick Start

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for full setup instructions.

```bash
# 1. Create .env from template and fill in credentials
cp .env.example .env

# 2. Install logging middleware
pip install -e ./logging_middleware

# 3. Register with evaluation service (one-time)
python scripts/register.py          # copy clientID/secret into .env

# 4. Verify auth and logging work
python scripts/smoke_test_auth.py
python scripts/smoke_test_log.py

# 5. Start the services
cd notification_app_be && uvicorn main:app --reload --port 8000
cd vehicle_maintence_scheduler && uvicorn main:app --reload --port 8001
```



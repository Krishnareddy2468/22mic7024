# Local setup (pre-test)

Use a **public GitHub repo named exactly your roll number** (no personal name or “Affordmed” in the repo name, README, or commits).

## 1. Python environment

```bash
cd /path/to/<rollNo>
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ./logging_middleware
pip install httpx python-dotenv
```

Alternative without editable install:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 2. Evaluation credentials (register once)

1. Copy `.env.example` to `.env` at the repo root.
2. Fill `EVAL_EMAIL`, `EVAL_NAME`, `EVAL_MOBILE`, `EVAL_GITHUB_USERNAME`, `EVAL_ROLL_NO`, and `EVAL_ACCESS_CODE` in `.env`.
3. Register (choose one):

**Option A — script**

```bash
python scripts/register.py
```

Copy the printed `EVAL_CLIENT_ID` and `EVAL_CLIENT_SECRET` into `.env`.

**Option B — Postman or Insomnia**

Send **one** registration request:

| Field | Value |
|-------|--------|
| Method | `POST` |
| URL | `http://4.224.186.213/evaluation-service/register` |
| Body (JSON) | `email`, `name`, `mobileNo`, `githubUsername`, `rollNo`, `accessCode` |

4. Copy `clientID` and `clientSecret` from the response into `.env` as `EVAL_CLIENT_ID` and `EVAL_CLIENT_SECRET`.

Never commit `.env`.

## 3. Smoke-test auth and logging

From the repo root with `.venv` active and `.env` filled:

```bash
python scripts/smoke_test_auth.py
python scripts/smoke_test_log.py
```

Expected output includes `OK: logID=...` and HTTP 200 JSON with `logID` and `message`.

If it fails, check stderr for `[logging_middleware]` messages (auth, validation, or network).

## 4. Run FastAPI stubs

**Notification app**

```bash
cd notification_app_be
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e ../logging_middleware
uvicorn main:app --reload --port 8000
```

**Vehicle scheduler** (separate terminal)

```bash
cd vehicle_maintence_scheduler
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e ../logging_middleware
uvicorn main:app --reload --port 8001
```

Health checks: `GET http://127.0.0.1:8000/health` and `GET http://127.0.0.1:8001/health`.

## 5. Postman / Insomnia notes

- **Evaluation service** (setup only): `register`, `auth`, `logs` on `http://4.224.186.213/evaluation-service/...`. Use these to obtain credentials and verify `Log()`; they are not your assessment screenshots.
- **Your apps** (test day): capture screenshots of requests to **your** FastAPI URLs—request body, response body, and response time—for each question folder.
- Suggested collection folders:
  - `Evaluation` — register (once), auth (manual check), logs (manual check)
  - `notification_app_be` — your routes as you build them
  - `vehicle_maintence_scheduler` — your routes as you build them
- For `/logs`, set header `Authorization: Bearer <access_token>` and body:

```json
{
  "stack": "backend",
  "level": "info",
  "package": "route",
  "message": "POST /example registered"
}
```

Enums must be lowercase. Backend `package` values include: `cache`, `controller`, `cron_job`, `db`, `domain`, `handler`, `repository`, `route`, `service`, plus `auth`, `config`, `middleware`, `utils`.

## 6. Using `Log()` in apps

```python
from logging_middleware import Log

Log("backend", "info", "route", "POST /vehicles registered")
```

Call at route, service, and repository boundaries with specific messages.

## 7. Test-day reminder

Implement assessment logic **without AI** during the live test. Push to `main` only when done; submit the Google form after logging works end-to-end.

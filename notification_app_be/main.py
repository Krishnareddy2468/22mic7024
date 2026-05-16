from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from logging_middleware import Log

from routes.priority import router as priority_router

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

app = FastAPI(title="Notification Priority Inbox")
app.include_router(priority_router)


@app.on_event("startup")
async def startup():
    Log("backend", "info", "config", "notification_app_be started")


@app.get("/health")
def health():
    return {"status": "ok"}

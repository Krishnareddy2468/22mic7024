from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from logging_middleware import Log

from routes.schedule import router as schedule_router

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

app = FastAPI(title="Vehicle Maintenance Scheduler")
app.include_router(schedule_router)


@app.on_event("startup")
async def startup():
    Log("backend", "info", "config", "vehicle_maintence_scheduler started")


@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import APIRouter, HTTPException
from logging_middleware import Log

from services.schedule_service import build_all_schedules, build_schedule_for_depot

router = APIRouter(tags=["schedule"])


@router.get("/schedule")
def get_all_schedules():
    Log("backend", "info", "route", "building schedules for all depots")
    schedules = build_all_schedules()
    Log("backend", "info", "route", f"built schedules for {len(schedules)} depots")
    return {"schedules": schedules}


@router.get("/depots/{depot_id}/schedule")
def get_depot_schedule(depot_id: int):
    Log("backend", "info", "route", f"building schedule for depot {depot_id}")
    try:
        schedule = build_schedule_for_depot(depot_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    Log("backend", "info", "route", f"built schedule for depot {depot_id}")
    return schedule

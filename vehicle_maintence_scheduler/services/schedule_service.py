from logging_middleware import Log

from .eval_client import fetch_depots, fetch_vehicles
from .knapsack import pick_tasks


def build_depot_schedule(depot: dict, tasks: list[dict]) -> dict:
    depot_id = depot["ID"]
    hours_available = int(depot["MechanicHours"])

    selected_tasks, used_hours, total_impact = pick_tasks(tasks, hours_available)

    Log(
        "backend",
        "info",
        "service",
        f"depot {depot_id}: selected {len(selected_tasks)} tasks, total impact {total_impact}",
    )

    if hours_available > used_hours:
        Log(
            "backend",
            "warn",
            "service",
            f"depot {depot_id}: {hours_available - used_hours} mechanic-hours unused",
        )

    return {
        "depotId": depot_id,
        "mechanicHours": hours_available,
        "selectedTasks": selected_tasks,
        "totalDuration": used_hours,
        "totalImpact": total_impact,
    }


def build_all_schedules() -> list[dict]:
    depots = fetch_depots()
    tasks = fetch_vehicles()
    return [build_depot_schedule(depot, tasks) for depot in depots]


def build_schedule_for_depot(depot_id: int) -> dict:
    depots = fetch_depots()
    depot = next((d for d in depots if d["ID"] == depot_id), None)
    if depot is None:
        Log("backend", "error", "handler", f"unknown depotId={depot_id}")
        raise ValueError(f"depot {depot_id} not found")

    tasks = fetch_vehicles()
    return build_depot_schedule(depot, tasks)

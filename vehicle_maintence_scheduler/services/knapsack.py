def pick_tasks(tasks: list[dict], capacity: int) -> tuple[list[str], int, int]:
    if not tasks or capacity <= 0:
        return [], 0, 0

    task_count = len(tasks)
    best_impact = [[0] * (capacity + 1) for _ in range(task_count + 1)]

    for row, task in enumerate(tasks, start=1):
        duration = int(task["Duration"])
        impact = int(task["Impact"])

        for hours in range(capacity + 1):
            best_impact[row][hours] = best_impact[row - 1][hours]
            if duration <= hours:
                with_task = best_impact[row - 1][hours - duration] + impact
                best_impact[row][hours] = max(best_impact[row][hours], with_task)

    selected: list[str] = []
    total_duration = 0
    total_impact = 0
    hours_left = capacity

    for row in range(task_count, 0, -1):
        if best_impact[row][hours_left] != best_impact[row - 1][hours_left]:
            task = tasks[row - 1]
            selected.append(task["TaskID"])
            total_duration += int(task["Duration"])
            total_impact += int(task["Impact"])
            hours_left -= int(task["Duration"])

    selected.reverse()
    return selected, total_duration, total_impact

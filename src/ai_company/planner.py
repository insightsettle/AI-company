"""Deterministic, read-only task planning. Never executes tasks or calls model providers."""
from decimal import Decimal
from .store import TaskStore


def build_dry_run_plan(store: TaskStore, project_id: str | None = None) -> dict:
    """Summarize ready tasks and their prerequisites without reserving budget or changing state."""
    listed = store.list_tasks(project_id)
    by_id = {item["id"]: store.get_task(item["id"]) for item in listed}
    ready = []
    skipped = []
    total_estimate = Decimal("0.00")
    model_estimate = Decimal("0.00")

    for task_id, task in by_id.items():
        if task["status"] != "ready":
            continue
        unmet = []
        for dep_id in task["dependencies"]:
            dep = store.get_task(dep_id)
            if dep is None or dep["status"] != "done":
                unmet.append(dep_id)
        if unmet:
            skipped.append({"task_id": task_id, "reason": "dependencies_incomplete", "dependencies": unmet})
            continue
        total = Decimal(task["estimated_total_cost"])
        model = Decimal(task["estimated_model_cost"])
        requires_approval = task["permission_tier"] >= 2
        ready.append({
            "task_id": task_id,
            "project_id": task["project_id"],
            "title": task["title"],
            "permission_tier": task["permission_tier"],
            "estimated_total_cost": str(total),
            "estimated_model_cost": str(model),
            "requires_explicit_approval": requires_approval,
            "execution_enabled": False,
        })
        total_estimate += total
        model_estimate += model

    return {
        "mode": "dry_run",
        "read_only": True,
        "provider_calls_enabled": False,
        "tasks_considered": len(listed),
        "eligible_ready_tasks": ready,
        "skipped_tasks": skipped,
        "eligible_estimated_total_cost": str(total_estimate.quantize(Decimal("0.01"))),
        "eligible_estimated_model_cost": str(model_estimate.quantize(Decimal("0.01"))),
        "note": "Planning only. No task was claimed, no budget was reserved, and no external action was performed.",
    }

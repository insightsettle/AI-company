from ai_company.models import Task
from ai_company.planner import build_dry_run_plan
from ai_company.store import TaskStore


def add_ready(store, task_id, tier=0, total="0.10", model="0.05"):
    store.add_task(Task(id=task_id, project_id="insight", title=task_id,
                        acceptance_criteria=("Evidence linked",), permission_tier=tier,
                        estimated_total_cost=total, estimated_model_cost=model))
    store.transition_task(task_id, "ready", "validated")


def test_dry_run_plan_is_read_only_and_marks_approval_tasks(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    add_ready(store, "research", tier=0)
    add_ready(store, "publish", tier=2, total="0.20", model="0.10")

    before = [(x["id"], x["status"]) for x in store.list_tasks()]
    plan = build_dry_run_plan(store, "insight")
    after = [(x["id"], x["status"]) for x in store.list_tasks()]

    assert before == after
    assert plan["mode"] == "dry_run"
    assert plan["provider_calls_enabled"] is False
    assert len(plan["eligible_ready_tasks"]) == 2
    assert next(t for t in plan["eligible_ready_tasks"] if t["task_id"] == "publish")["requires_explicit_approval"] is True
    assert plan["eligible_estimated_total_cost"] == "0.30"


def test_dry_run_plan_skips_tasks_with_unmet_dependencies(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    store.add_task(Task(id="parent", project_id="insight", title="parent",
                        acceptance_criteria=("Evidence linked",)))
    store.add_task(Task(id="child", project_id="insight", title="child",
                        acceptance_criteria=("Evidence linked",), dependencies=("parent",)))
    # A valid task can only become ready after its dependency is done; planner still
    # independently reports only eligible ready tasks from persisted state.
    store.transition_task("parent", "ready", "validated")
    plan = build_dry_run_plan(store, "insight")
    assert [t["task_id"] for t in plan["eligible_ready_tasks"]] == ["parent"]
    assert plan["provider_calls_enabled"] is False

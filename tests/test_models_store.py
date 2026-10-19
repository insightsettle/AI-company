import pytest
from ai_company.models import Task
from ai_company.store import TaskStore


def sample_task(task_id="t-001"):
    return Task(id=task_id, project_id="insight", title="Audit a requirement", acceptance_criteria=("Evidence is linked",), permission_tier=0)


def test_task_requires_acceptance_criteria():
    task = Task(id="t", project_id="p", title="x", acceptance_criteria=())
    with pytest.raises(ValueError):
        task.validate()


def test_task_cannot_depend_on_itself():
    task = Task(id="t", project_id="p", title="x", acceptance_criteria=("done",), dependencies=("t",))
    with pytest.raises(ValueError):
        task.validate()


def test_store_persists_task_and_audit_event(tmp_path):
    db = tmp_path / "state.sqlite3"
    store = TaskStore(db)
    store.add_task(sample_task())
    restarted = TaskStore(db)
    assert restarted.get_task("t-001")["project_id"] == "insight"
    assert restarted.audit_events("t-001")[0]["event_type"] == "task_created"


def test_duplicate_task_id_is_rejected(tmp_path):
    store = TaskStore(tmp_path / "state.sqlite3")
    store.add_task(sample_task())
    with pytest.raises(Exception):
        store.add_task(sample_task())

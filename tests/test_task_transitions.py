import pytest
from ai_company.models import Task
from ai_company.store import TaskStore


def make_task(task_id, dependencies=()):
    return Task(id=task_id, project_id="insight", title=task_id,
                acceptance_criteria=("Evidence recorded",), dependencies=tuple(dependencies))


def test_cannot_mark_task_done_without_qa_evidence(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    store.add_task(make_task("task-1"))
    store.transition_task("task-1", "ready", "criteria clarified")
    store.transition_task("task-1", "reserved", "budget reserved")
    store.transition_task("task-1", "running", "worker started")
    store.transition_task("task-1", "needs_qa", "output saved")
    with pytest.raises(ValueError, match="QA evidence"):
        store.transition_task("task-1", "done", "agent says complete")


def test_done_requires_qa_stage_and_evidence(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    store.add_task(make_task("task-1"))
    with pytest.raises(ValueError, match="Transition not allowed"):
        store.transition_task("task-1", "done", "skip verification", qa_evidence="test report")
    store.transition_task("task-1", "ready", "ready for work")
    store.transition_task("task-1", "reserved", "budget reserved")
    store.transition_task("task-1", "running", "started")
    store.transition_task("task-1", "needs_qa", "artifact saved")
    store.transition_task("task-1", "done", "QA passed", qa_evidence="tests/test_task_transitions.py passed")
    assert store.get_task("task-1")["status"] == "done"
    assert store.audit_events("task-1")[-1]["event_type"] == "status_transition"


def test_ready_task_waits_for_dependencies(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    store.add_task(make_task("parent"))
    store.add_task(make_task("child", dependencies=("parent",)))
    with pytest.raises(ValueError, match="Dependency is not complete"):
        store.transition_task("child", "ready", "attempt before dependency")


def test_transition_rejects_unknown_task(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    with pytest.raises(KeyError):
        store.transition_task("missing", "ready", "no such task")

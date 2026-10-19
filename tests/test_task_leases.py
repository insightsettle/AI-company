from datetime import datetime, timedelta, timezone

import pytest

from ai_company.models import Task
from ai_company.store import TaskStore


def task(task_id, dependencies=(), project="insight"):
    return Task(id=task_id, project_id=project, title=task_id,
                acceptance_criteria=("Output is reviewed",), dependencies=tuple(dependencies))


def make_ready(store, task_id):
    store.transition_task(task_id, "ready", "validated for scheduling")


def test_claim_is_atomic_and_second_worker_cannot_claim_same_task(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    store.add_task(task("one"))
    make_ready(store, "one")

    claim = store.claim_ready_task("worker-a")
    assert claim and claim["task_id"] == "one"
    assert store.claim_ready_task("worker-b") is None
    assert store.get_task("one")["status"] == "reserved"


def test_only_lease_owner_can_start_task(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    store.add_task(task("one"))
    make_ready(store, "one")
    store.claim_ready_task("worker-a")

    with pytest.raises(ValueError, match="valid active lease"):
        store.start_claimed_task("one", "worker-b")

    store.start_claimed_task("one", "worker-a")
    assert store.get_task("one")["status"] == "running"


def test_expired_reservation_returns_to_ready_and_can_be_reclaimed(tmp_path, monkeypatch):
    store = TaskStore(tmp_path / "tasks.db")
    store.add_task(task("one"))
    make_ready(store, "one")
    start = datetime(2026, 10, 19, 10, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(store, "_utc_now", lambda: start)
    first = store.claim_ready_task("worker-a", lease_seconds=30)
    assert first

    monkeypatch.setattr(store, "_utc_now", lambda: start + timedelta(seconds=31))
    second = store.claim_ready_task("worker-b", lease_seconds=30)
    assert second and second["task_id"] == "one"
    events = [event["event_type"] for event in store.audit_events("one")]
    assert "lease_expired" in events
    assert "task_claimed" in events


def test_lease_renewal_requires_owner_and_live_reservation(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    store.add_task(task("one"))
    make_ready(store, "one")
    store.claim_ready_task("worker-a")

    with pytest.raises(ValueError, match="active lease"):
        store.renew_task_lease("one", "worker-b")
    assert store.renew_task_lease("one", "worker-a")


def test_scheduler_does_not_claim_task_with_incomplete_dependency(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    store.add_task(task("parent"))
    store.add_task(task("child", dependencies=("parent",)))
    make_ready(store, "parent")

    claim = store.claim_ready_task("worker-a")
    assert claim and claim["task_id"] == "parent"
    assert store.claim_ready_task("worker-b") is None
    assert store.get_task("child")["status"] == "backlog"

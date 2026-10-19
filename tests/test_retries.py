import pytest

from ai_company.models import Task
from ai_company.store import TaskStore


def make_task(store):
    store.add_task(Task(id="retry-me", project_id="insight", title="Retry me",
                        acceptance_criteria=("Evidence recorded",)))
    store.transition_task("retry-me", "ready", "ready")
    store.transition_task("retry-me", "reserved", "budget reserved")


def fail_one_attempt(store):
    store.transition_task("retry-me", "running", "worker started")
    store.transition_task("retry-me", "failed", "temporary failure")


def test_failed_task_retries_until_three_attempts_then_stops(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    make_task(store)

    fail_one_attempt(store)
    assert store.get_task("retry-me")["attempt_count"] == 1
    assert store.retry_failed_task("retry-me", "retry after transient error") is True
    assert store.get_task("retry-me")["status"] == "ready"

    store.transition_task("retry-me", "reserved", "budget reserved again")
    fail_one_attempt(store)
    assert store.get_task("retry-me")["attempt_count"] == 2
    assert store.retry_failed_task("retry-me", "second retry") is True

    store.transition_task("retry-me", "reserved", "budget reserved again")
    fail_one_attempt(store)
    assert store.get_task("retry-me")["attempt_count"] == 3
    assert store.retry_failed_task("retry-me", "retry limit reached") is False
    assert store.get_task("retry-me")["status"] == "failed"
    assert store.audit_events("retry-me")[-1]["event_type"] == "retry_exhausted"


def test_retry_only_accepts_failed_tasks_and_maximum_is_three(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")
    make_task(store)
    with pytest.raises(ValueError, match="Only failed tasks"):
        store.retry_failed_task("retry-me", "not failed")
    with pytest.raises(ValueError, match="between 1 and 3"):
        store.retry_failed_task("retry-me", "too many", max_attempts=4)

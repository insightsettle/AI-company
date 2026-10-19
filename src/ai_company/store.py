"""SQLite-backed starter store for task persistence and an append-only audit log."""
import json
import sqlite3
from pathlib import Path
from .models import Task

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL, title TEXT NOT NULL,
  acceptance_criteria_json TEXT NOT NULL, status TEXT NOT NULL,
  permission_tier INTEGER NOT NULL, estimated_total_cost TEXT NOT NULL,
  estimated_model_cost TEXT NOT NULL, dependencies_json TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS audit_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL, event_type TEXT NOT NULL, detail_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_tasks_project_status ON tasks(project_id, status);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_events(entity_type, entity_id, id);
"""

class TaskStore:
    def __init__(self, database_path: str | Path):
        self.database_path = str(database_path)
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    def _connect(self):
        conn = sqlite3.connect(self.database_path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def add_task(self, task: Task) -> None:
        task.validate()
        with self._connect() as conn:
            conn.execute("INSERT INTO tasks (id, project_id, title, acceptance_criteria_json, status, permission_tier, estimated_total_cost, estimated_model_cost, dependencies_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (task.id, task.project_id, task.title, json.dumps(task.acceptance_criteria), task.status, task.permission_tier, task.estimated_total_cost, task.estimated_model_cost, json.dumps(task.dependencies)))
            conn.execute("INSERT INTO audit_events (entity_type, entity_id, event_type, detail_json) VALUES (?, ?, ?, ?)",
                ("task", task.id, "task_created", json.dumps({"project_id": task.project_id, "status": task.status})))

    def get_task(self, task_id: str) -> dict | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return None
        result = dict(row)
        result["acceptance_criteria"] = json.loads(result.pop("acceptance_criteria_json"))
        result["dependencies"] = json.loads(result.pop("dependencies_json"))
        return result

    def list_tasks(self, project_id: str | None = None) -> list[dict]:
        query = "SELECT id, project_id, title, status, permission_tier, updated_at FROM tasks"
        params: tuple = ()
        if project_id:
            query += " WHERE project_id = ?"
            params = (project_id,)
        query += " ORDER BY updated_at, id"
        with self._connect() as conn:
            return [dict(row) for row in conn.execute(query, params).fetchall()]

    def audit_events(self, entity_id: str) -> list[dict]:
        with self._connect() as conn:
            return [dict(row) for row in conn.execute("SELECT * FROM audit_events WHERE entity_id = ? ORDER BY id", (entity_id,)).fetchall()]

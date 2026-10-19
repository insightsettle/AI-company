"""Small typed records shared by the orchestration foundation."""
from dataclasses import dataclass, field
from typing import Literal

TaskStatus = Literal["backlog", "ready", "reserved", "running", "needs_qa", "done", "blocked", "awaiting_approval", "failed", "cancelled"]
VALID_STATUSES = {"backlog", "ready", "reserved", "running", "needs_qa", "done", "blocked", "awaiting_approval", "failed", "cancelled"}

@dataclass(frozen=True)
class Task:
    id: str
    project_id: str
    title: str
    acceptance_criteria: tuple[str, ...]
    status: TaskStatus = "backlog"
    permission_tier: int = 0
    estimated_total_cost: str = "0.00"
    estimated_model_cost: str = "0.00"
    dependencies: tuple[str, ...] = field(default_factory=tuple)

    def validate(self) -> None:
        if not self.id.strip() or not self.project_id.strip() or not self.title.strip():
            raise ValueError("Task id, project_id, and title are required")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"Unsupported task status: {self.status}")
        if not 0 <= self.permission_tier <= 3:
            raise ValueError("permission_tier must be between 0 and 3")
        if not self.acceptance_criteria:
            raise ValueError("At least one acceptance criterion is required")
        if self.id in self.dependencies:
            raise ValueError("A task cannot depend on itself")

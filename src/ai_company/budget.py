"""Deterministic budget guardrails. This module never calls an LLM provider."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class BudgetPolicy:
    monthly_total_cap: Decimal = Decimal("50.00")
    monthly_model_cap: Decimal = Decimal("15.00")
    total_stop_at: Decimal = Decimal("45.00")
    model_review_at: Decimal = Decimal("7.50")
    model_pause_low_priority_at: Decimal = Decimal("10.50")
    model_stop_at: Decimal = Decimal("13.50")
    daily_model_target: Decimal = Decimal("0.50")
    max_task_estimate: Decimal = Decimal("0.50")


@dataclass(frozen=True)
class BudgetSnapshot:
    total_spent: Decimal = Decimal("0.00")
    model_spent: Decimal = Decimal("0.00")
    model_spent_today: Decimal = Decimal("0.00")
    reserved_total: Decimal = Decimal("0.00")
    reserved_model: Decimal = Decimal("0.00")


@dataclass(frozen=True)
class BudgetDecision:
    allowed: bool
    reason: str


def can_start_task(policy: BudgetPolicy, snapshot: BudgetSnapshot, estimated_total: Decimal,
                   estimated_model: Decimal, priority: str = "normal") -> BudgetDecision:
    """Fail-closed preflight check; caller must atomically reserve funds before execution."""
    values = (estimated_total, estimated_model, snapshot.total_spent, snapshot.model_spent,
              snapshot.model_spent_today, snapshot.reserved_total, snapshot.reserved_model)
    if any(v < 0 for v in values):
        return BudgetDecision(False, "Negative costs are invalid")
    if estimated_model > estimated_total:
        return BudgetDecision(False, "Model estimate cannot exceed total estimate")
    if estimated_model > policy.max_task_estimate:
        return BudgetDecision(False, "Task estimate exceeds configured per-task ceiling")
    if snapshot.total_spent + snapshot.reserved_total + estimated_total > policy.total_stop_at:
        return BudgetDecision(False, "Total spend stop threshold would be exceeded")
    if snapshot.model_spent + snapshot.reserved_model + estimated_model > policy.model_stop_at:
        return BudgetDecision(False, "Model spend stop threshold would be exceeded")
    if snapshot.model_spent_today + estimated_model > policy.daily_model_target:
        return BudgetDecision(False, "Daily model spend target would be exceeded")
    if priority.lower() in {"low", "low-priority"} and snapshot.model_spent >= policy.model_pause_low_priority_at:
        return BudgetDecision(False, "Low-priority work paused by model-spend policy")
    if snapshot.total_spent + snapshot.reserved_total + estimated_total > policy.monthly_total_cap:
        return BudgetDecision(False, "Monthly total cap would be exceeded")
    if snapshot.model_spent + snapshot.reserved_model + estimated_model > policy.monthly_model_cap:
        return BudgetDecision(False, "Monthly model cap would be exceeded")
    return BudgetDecision(True, "Preflight passed; reserve cost atomically before running")

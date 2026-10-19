from decimal import Decimal
from ai_company.budget import BudgetPolicy, BudgetSnapshot, can_start_task


def test_allows_small_task_under_limits():
    decision = can_start_task(BudgetPolicy(), BudgetSnapshot(), Decimal("0.03"), Decimal("0.02"))
    assert decision.allowed


def test_blocks_total_stop_threshold():
    snapshot = BudgetSnapshot(total_spent=Decimal("44.99"))
    decision = can_start_task(BudgetPolicy(), snapshot, Decimal("0.02"), Decimal("0.01"))
    assert not decision.allowed
    assert "Total spend" in decision.reason


def test_blocks_model_spend_stop_threshold():
    snapshot = BudgetSnapshot(model_spent=Decimal("13.49"))
    decision = can_start_task(BudgetPolicy(), snapshot, Decimal("0.02"), Decimal("0.02"))
    assert not decision.allowed
    assert "Model spend" in decision.reason


def test_blocks_estimate_above_per_task_cap():
    decision = can_start_task(BudgetPolicy(), BudgetSnapshot(), Decimal("0.80"), Decimal("0.60"))
    assert not decision.allowed


def test_blocks_negative_estimates():
    decision = can_start_task(BudgetPolicy(), BudgetSnapshot(), Decimal("-0.01"), Decimal("0.00"))
    assert not decision.allowed

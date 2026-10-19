from decimal import Decimal
import pytest
from ai_company.ledger import BudgetLedger
from ai_company.budget import BudgetPolicy


def test_reservation_counts_against_remaining_budget(tmp_path):
    ledger = BudgetLedger(tmp_path / "budget.sqlite3", BudgetPolicy(daily_model_target=Decimal("15.00"), max_task_estimate=Decimal("15.00")))
    first = ledger.reserve("r1", "2026-10", "30.00", "10.00", day_key="2026-10-19")
    second = ledger.reserve("r2", "2026-10", "16.00", "1.00")
    assert first.allowed
    assert not second.allowed


def test_settle_converts_reservation_to_actual_spend(tmp_path):
    ledger = BudgetLedger(tmp_path / "budget.sqlite3")
    assert ledger.reserve("r1", "2026-10", "0.10", "0.05").allowed
    ledger.settle("r1", "0.08", "0.04")
    summary = ledger.summary("2026-10")
    assert summary["actual_total"] == "0.08"
    assert summary["reserved_total"] == "0.00"


def test_release_frees_reserved_amount(tmp_path):
    ledger = BudgetLedger(tmp_path / "budget.sqlite3", BudgetPolicy(daily_model_target=Decimal("15.00")))
    assert ledger.reserve("r1", "2026-10", "40.00", "10.00", day_key="2026-10-19").allowed
    ledger.release("r1")
    assert ledger.summary("2026-10")["reserved_total"] == "0.00"
    assert ledger.reserve("r2", "2026-10", "40.00", "10.00", day_key="2026-10-19").allowed


def test_duplicate_reservation_id_is_rejected(tmp_path):
    ledger = BudgetLedger(tmp_path / "budget.sqlite3")
    assert ledger.reserve("same", "2026-10", "0.10", "0.05").allowed
    assert not ledger.reserve("same", "2026-10", "0.10", "0.05").allowed


def test_rejects_invalid_actual_cost(tmp_path):
    ledger = BudgetLedger(tmp_path / "budget.sqlite3")
    ledger.reserve("r1", "2026-10", "0.10", "0.05")
    with pytest.raises(ValueError):
        ledger.settle("r1", "0.01", "0.02")


def test_custom_model_cap_blocks_reservation(tmp_path):
    policy = BudgetPolicy(model_stop_at=Decimal("0.10"))
    ledger = BudgetLedger(tmp_path / "budget.sqlite3", policy)
    result = ledger.reserve("r1", "2026-10", "0.50", "0.11")
    assert not result.allowed


def test_daily_model_target_counts_reserved_and_actual_spend(tmp_path):
    ledger = BudgetLedger(tmp_path / "budget.sqlite3", BudgetPolicy(daily_model_target=Decimal("0.50")))
    assert ledger.reserve("r1", "2026-10", "0.30", "0.30", day_key="2026-10-19").allowed
    blocked = ledger.reserve("r2", "2026-10", "0.20", "0.21", day_key="2026-10-19")
    assert not blocked.allowed
    assert "Daily model spend target" in blocked.reason
    assert ledger.reserve("r3", "2026-10", "0.30", "0.30", day_key="2026-10-20").allowed


def test_daily_model_target_uses_actual_after_settlement(tmp_path):
    ledger = BudgetLedger(tmp_path / "budget.sqlite3", BudgetPolicy(daily_model_target=Decimal("0.50")))
    assert ledger.reserve("r1", "2026-10", "0.40", "0.40", day_key="2026-10-19").allowed
    ledger.settle("r1", "0.20", "0.20")
    assert ledger.reserve("r2", "2026-10", "0.30", "0.30", day_key="2026-10-19").allowed


def test_day_key_must_match_month(tmp_path):
    ledger = BudgetLedger(tmp_path / "budget.sqlite3")
    with pytest.raises(ValueError):
        ledger.reserve("r1", "2026-10", "0.10", "0.05", day_key="2026-11-01")

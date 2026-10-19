import json
from ai_company.cli import main


def test_status_explicitly_disables_unimplemented_runtime(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr("sys.argv", ["ai-company", "--db", str(tmp_path / "state.db"), "status"])
    assert main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["model_calls_enabled"] is False
    assert payload["autonomous_scheduler_enabled"] is False


def test_budget_command_shows_monthly_summary(monkeypatch, capsys, tmp_path):
    db = str(tmp_path / "state.db")
    monkeypatch.setattr("sys.argv", ["ai-company", "--db", db, "budget", "--month", "2026-10"])
    assert main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["month_key"] == "2026-10"
    assert payload["actual_model"] == "0.00"
    assert payload["reserved_model"] == "0.00"

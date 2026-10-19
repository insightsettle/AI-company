import json
from ai_company.cli import main


def test_status_explicitly_disables_unimplemented_runtime(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr("sys.argv", ["ai-company", "--db", str(tmp_path / "state.db"), "status"])
    assert main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["model_calls_enabled"] is False
    assert payload["autonomous_scheduler_enabled"] is False

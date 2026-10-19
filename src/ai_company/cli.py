"""CLI for checking repository configuration and local task state."""
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from .store import TaskStore
from .ledger import BudgetLedger


def main() -> int:
    parser = argparse.ArgumentParser(prog="ai-company")
    parser.add_argument("--db", default=os.environ.get("AI_COMPANY_DB", "data/ai-company.sqlite3"), help="SQLite database path")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Show local store status")
    listing = sub.add_parser("tasks", help="List tasks")
    listing.add_argument("--project", default=None)
    budget = sub.add_parser("budget", help="Show local budget ledger summary")
    budget.add_argument("--month", default=datetime.now(timezone.utc).strftime("%Y-%m"), help="UTC month in YYYY-MM format")
    args = parser.parse_args()
    store = TaskStore(Path(args.db))
    if args.command == "budget":
        print(json.dumps(BudgetLedger(Path(args.db)).summary(args.month), indent=2))
        return 0
    if args.command == "status":
        print(json.dumps({"service": "ai-company", "database_initialized": True, "model_calls_enabled": False, "autonomous_scheduler_enabled": False, "deployment_status": "not_deployed"}, indent=2))
        return 0
    print(json.dumps(store.list_tasks(args.project), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

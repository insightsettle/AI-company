"""Atomic SQLite budget reservations and usage ledger.

This is local persistence, not provider billing enforcement. Configure provider-side caps too.
"""
import sqlite3
from datetime import datetime, timezone, date
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from .budget import BudgetPolicy


@dataclass(frozen=True)
class Reservation:
    reservation_id: str
    allowed: bool
    reason: str


class BudgetLedger:
    def __init__(self, database_path: str | Path, policy: BudgetPolicy | None = None):
        self.database_path = str(database_path)
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self.policy = policy or BudgetPolicy()
        with self._connect() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS budget_reservations (
              reservation_id TEXT PRIMARY KEY, month_key TEXT NOT NULL,
              day_key TEXT NOT NULL DEFAULT '', estimated_total TEXT NOT NULL, estimated_model TEXT NOT NULL,
              status TEXT NOT NULL CHECK(status IN ('reserved','settled','released')),
              actual_total TEXT, actual_model TEXT,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
              settled_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_budget_month_status ON budget_reservations(month_key, status);
            CREATE TABLE IF NOT EXISTS budget_events (
              id INTEGER PRIMARY KEY AUTOINCREMENT, month_key TEXT NOT NULL,
              event_type TEXT NOT NULL, reservation_id TEXT NOT NULL,
              detail TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """)

    def _connect(self):
        conn = sqlite3.connect(self.database_path, timeout=10, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout = 10000")
        return conn

    @staticmethod
    def _money(value: Decimal | str | float) -> Decimal:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0:
            raise ValueError("Costs must be finite and non-negative")
        return amount.quantize(Decimal("0.01"))

    def _totals(self, conn, month_key: str):
        rows = conn.execute("SELECT status, estimated_total, estimated_model, actual_total, actual_model FROM budget_reservations WHERE month_key=?", (month_key,)).fetchall()
        total_spent = model_spent = reserved_total = reserved_model = Decimal("0.00")
        for row in rows:
            if row["status"] == "reserved":
                reserved_total += Decimal(row["estimated_total"])
                reserved_model += Decimal(row["estimated_model"])
            elif row["status"] == "settled":
                total_spent += Decimal(row["actual_total"] or "0.00")
                model_spent += Decimal(row["actual_model"] or "0.00")
        return total_spent, model_spent, reserved_total, reserved_model

    def _daily_model_totals(self, conn, day_key: str) -> tuple[Decimal, Decimal]:
        rows = conn.execute(
            "SELECT status, estimated_model, actual_model FROM budget_reservations WHERE day_key=?",
            (day_key,),
        ).fetchall()
        spent = reserved = Decimal("0.00")
        for row in rows:
            if row["status"] == "reserved":
                reserved += Decimal(row["estimated_model"])
            elif row["status"] == "settled":
                spent += Decimal(row["actual_model"] or "0.00")
        return spent, reserved

    def reserve(self, reservation_id: str, month_key: str, estimated_total: Decimal | str | float,
                estimated_model: Decimal | str | float, day_key: str | None = None) -> Reservation:
        if not reservation_id.strip() or not month_key.strip():
            raise ValueError("reservation_id and month_key are required")
        day_key = day_key or datetime.now(timezone.utc).date().isoformat()
        try:
            parsed_day = date.fromisoformat(day_key)
        except (TypeError, ValueError) as exc:
            raise ValueError("day_key must be an ISO date (YYYY-MM-DD)") from exc
        if parsed_day.strftime("%Y-%m") != month_key:
            raise ValueError("day_key month must match month_key")
        total, model = self._money(estimated_total), self._money(estimated_model)
        if model > total:
            return Reservation(reservation_id, False, "Model estimate cannot exceed total estimate")
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            existing = conn.execute("SELECT status FROM budget_reservations WHERE reservation_id=?", (reservation_id,)).fetchone()
            if existing:
                conn.execute("ROLLBACK")
                return Reservation(reservation_id, False, "Reservation ID already exists; use a new idempotency key")
            spent_total, spent_model, held_total, held_model = self._totals(conn, month_key)
            daily_spent, daily_held = self._daily_model_totals(conn, day_key)
            p = self.policy
            if spent_total + held_total + total > p.total_stop_at:
                reason = "Total spend stop threshold would be exceeded"
            elif spent_model + held_model + model > p.model_stop_at:
                reason = "Model spend stop threshold would be exceeded"
            elif daily_spent + daily_held + model > p.daily_model_target:
                reason = "Daily model spend target would be exceeded"
            elif spent_total + held_total + total > p.monthly_total_cap:
                reason = "Monthly total cap would be exceeded"
            elif spent_model + held_model + model > p.monthly_model_cap:
                reason = "Monthly model cap would be exceeded"
            elif model > p.max_task_estimate:
                reason = "Task estimate exceeds configured per-task ceiling"
            else:
                reason = ""
            if reason:
                conn.execute("ROLLBACK")
                return Reservation(reservation_id, False, reason)
            conn.execute("INSERT INTO budget_reservations(reservation_id,month_key,day_key,estimated_total,estimated_model,status) VALUES(?,?,?,?,?, 'reserved')", (reservation_id, month_key, day_key, str(total), str(model)))
            conn.execute("INSERT INTO budget_events(month_key,event_type,reservation_id,detail) VALUES(?,?,?,?)", (month_key, "reserved", reservation_id, f"estimated_total={total};estimated_model={model}"))
            conn.execute("COMMIT")
            return Reservation(reservation_id, True, "Cost reserved; execution may proceed only after permission checks")
        except Exception:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def settle(self, reservation_id: str, actual_total: Decimal | str | float,
               actual_model: Decimal | str | float) -> None:
        total, model = self._money(actual_total), self._money(actual_model)
        if model > total:
            raise ValueError("Actual model cost cannot exceed actual total cost")
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT month_key,status FROM budget_reservations WHERE reservation_id=?", (reservation_id,)).fetchone()
            if not row:
                raise KeyError("Unknown reservation")
            if row["status"] != "reserved":
                raise ValueError("Only a reserved item can be settled")
            conn.execute("UPDATE budget_reservations SET status='settled',actual_total=?,actual_model=?,settled_at=CURRENT_TIMESTAMP WHERE reservation_id=?", (str(total), str(model), reservation_id))
            conn.execute("INSERT INTO budget_events(month_key,event_type,reservation_id,detail) VALUES(?,?,?,?)", (row["month_key"], "settled", reservation_id, f"actual_total={total};actual_model={model}"))
            conn.execute("COMMIT")
        except Exception:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def release(self, reservation_id: str, reason: str = "cancelled before execution") -> None:
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT month_key,status FROM budget_reservations WHERE reservation_id=?", (reservation_id,)).fetchone()
            if not row:
                raise KeyError("Unknown reservation")
            if row["status"] != "reserved":
                raise ValueError("Only a reserved item can be released")
            conn.execute("UPDATE budget_reservations SET status='released',settled_at=CURRENT_TIMESTAMP WHERE reservation_id=?", (reservation_id,))
            conn.execute("INSERT INTO budget_events(month_key,event_type,reservation_id,detail) VALUES(?,?,?,?)", (row["month_key"], "released", reservation_id, reason[:500]))
            conn.execute("COMMIT")
        except Exception:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def summary(self, month_key: str) -> dict[str, str]:
        with self._connect() as conn:
            spent_total, spent_model, held_total, held_model = self._totals(conn, month_key)
        return {"month_key": month_key, "actual_total": str(spent_total), "actual_model": str(spent_model),
                "reserved_total": str(held_total), "reserved_model": str(held_model),
                "internal_total_stop_at": str(self.policy.total_stop_at),
                "internal_model_stop_at": str(self.policy.model_stop_at)}

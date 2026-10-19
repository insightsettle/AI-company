# Implementation Status

Updated: 2026-10-19

## Present in repository

- Project, budget, architecture, operating, and security documentation.
- Python package skeleton and CLI for local status/task listing.
- Deterministic budget preflight checks.
- SQLite task persistence and task-creation audit events.
- Atomic SQLite budget reservations, settlement, release, monthly summaries, and reservation event records.
- Daily model-spend target enforced atomically across reserved estimates and settled actual costs, with UTC date attribution and migration/backfill for existing ledger databases.
- Validated task state transitions, dependency gating before a task becomes ready, and audit events for state changes.
- Completion gate: a task can only move from `needs_qa` to `done` when QA evidence is supplied.
- Unit tests for budget limits, task validation, persistence, ledger reservation/settlement/release/idempotency, safe CLI status, task transitions, dependencies, and QA evidence.
- GitHub Actions workflow for push, pull request, manual, and weekday scheduled test runs. It has read-only repository permissions and does not call AI providers.

## Not implemented yet

- Provider invoice reconciliation and comparison of internal usage against actual provider invoices.
- Safe task claiming/leases for multiple workers and full orchestration loop.
- Provider adapters, model routing, credentials, rate limits, and model selection by current price/quality.
- Cloud database, hosted orchestrator, durable queue, dashboard, and notifications.
- Source ingestion from separate chats, Drive, Lovable, and other user projects.
- Runtime deployment and proof that jobs execute while the desktop is closed.

## Validation status

Files have been committed to GitHub. The CI workflow has been authored, but its test run has not yet been observed here. Do not describe the tests as passing until GitHub Actions reports success. The CLI explicitly reports that model calls and autonomous scheduling are disabled.

## Next engineering milestones

1. Observe the first CI run and fix any failing tests.
2. Add provider-cost reconciliation and tests against real provider invoice exports.
3. Implement safe task claiming, retries, and a dry-run planner without model providers.
4. Select hosting and database after verifying current free-tier limits and budget.
5. Add a provider adapter only after budget reservation, secret handling, and logging are tested.

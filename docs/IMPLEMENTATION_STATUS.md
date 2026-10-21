# Implementation Status

Updated: 2026-10-21

## Repository and project isolation

- Active project registry is intentionally empty by user request.
- Prior projects have been excluded; do not re-import their scope or artifacts.
- A separate Saudi-first fintech research charter exists at `projects/saudi-fintech-venture/PROJECT_CHARTER.md`.
- The charter is a planning document only. Project execution is blocked until AI Company verification gates are evidenced.

## Present in repository

- Project, budget, architecture, operating, and security documentation.
- Python package skeleton and CLI for local status, task listing, and monthly budget-ledger summary (`ai-company budget --month YYYY-MM`).
- Deterministic budget preflight checks.
- SQLite task persistence and task-creation audit events.
- Atomic SQLite budget reservations, settlement, release, monthly summaries, and reservation event records.
- Daily model-spend target enforced atomically across reserved estimates and settled actual costs, with UTC date attribution and migration/backfill for existing ledger databases.
- Validated task state transitions, dependency gating before a task becomes ready, and audit events for state changes.
- Atomic ready-task claiming with worker-owned expiring leases, stale-reservation recovery, lease renewal, and lease-owner validation before starting work.
- Bounded task retry tracking: each start increments an attempt counter; failed tasks can be requeued up to three attempts, after which retry is denied and audited.
- Read-only dry-run planner and `ai-company plan` CLI command; it reports estimated cost and approval requirements without claiming tasks, reserving funds, calling providers, or executing external actions.
- Completion gate: a task can only move from `needs_qa` to `done` when QA evidence is supplied.
- Unit tests covering budget limits, task validation, persistence, ledger operations, CLI planning, task transitions, leases, retries, dependencies, and QA evidence.
- GitHub Actions workflow for push, pull request, manual, and weekday scheduled test runs. It has read-only repository permissions and does not call AI providers.

## Not implemented or not proven

- Successful GitHub Actions run for the current code has not been observed/confirmed.
- Provider invoice reconciliation and comparison of internal usage against actual provider invoices.
- Full orchestration loop and safe recovery for workers that fail after a task enters `running`.
- End-to-end concurrency tests against multiple processes.
- Provider adapters, model routing, credentials, rate limits, and model selection by current price/quality.
- Cloud database, hosted orchestrator, durable queue, dashboard, and notifications.
- Runtime deployment and proof that jobs execute while the desktop is closed.

## Mandatory start gate

No project execution beyond bounded research/documentation until there is dated evidence for all of the following:
1. CI test suite passes on the current commit.
2. Security and repository review is completed.
3. CLI smoke tests and budget/ledger/task/lease/retry/dependency/QA tests pass.
4. Concurrency and crash recovery are tested; no unsafe blind replay of side-effecting tasks.
5. Cloud persistence, scheduled execution, restart recovery and work continuing while Claude is closed are demonstrated in a non-production environment.
6. Provider routing, secret handling and actual-cost reconciliation are tested with mocks.
7. USD 50 total monthly and USD 15 model/API monthly limits are enforced; provider-side billing controls are configured where available.
8. Independent QA publishes commit IDs, workflow links, test commands, pass/fail results, known gaps and residual risks.

A test file or workflow definition is not proof of passing tests. Do not claim a component is working until its behavior has been observed.

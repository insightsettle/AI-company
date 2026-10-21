# AI Company

Budget-controlled AI project orchestration foundation.

## Current status

AI Company is **not yet verified as operational**. It is not deployed and autonomous jobs have not been proven to run. The CI workflow exists, but a successful test run has not yet been confirmed. Do not begin project execution until the verification gate is satisfied.

## Project isolation

The active project registry is intentionally empty. All previously registered projects have been excluded at the user's request. Do not restore or import prior project scopes, files, or task lists.

A new, separate Saudi-first fintech research charter is stored at [projects/saudi-fintech-venture/PROJECT_CHARTER.md](projects/saudi-fintech-venture/PROJECT_CHARTER.md). It is a brief and research plan only, not authorization to start execution. Research/documentation must remain bounded until the verification gate passes.

## Budget guardrails

- Total internal monthly cap: USD 50.
- Model/API internal monthly cap: USD 15.
- Stop low-priority work at thresholds defined in configuration.
- Never place API keys, tokens, passwords, or private credentials in Git.
- Require explicit user approval for live trading, financial transactions, paid purchases, production deployments, customer contact, and destructive actions.
- Internal limits do not replace provider-side billing caps or invoice reconciliation.

## Planned roles (not running agents)

- CEO / Planner: priorities and outcomes.
- COO / Orchestrator: task queue, dependencies, blockers, schedules.
- Engineer: bounded implementation tasks.
- QA / Auditor: independent verification and evidence.

## Verification gate

Before any project execution, independently verify:
1. GitHub Actions tests pass on the current commit.
2. Budget ledger, task transitions, leases, retries, dependencies and QA gates pass tests.
3. Concurrency and safe crash recovery are tested.
4. Secret handling and provider-cost reconciliation are tested with mocks.
5. Cloud persistence and unattended scheduled execution are demonstrated in a non-production environment.
6. Independent QA records commit/run links, results, gaps and residual risks.

If a gate is not evidenced, stop and report it. Never claim tests pass based on the existence of test files.

## Security

- No secrets or customer data in Git.
- Default to read-only, dry-run and synthetic data.
- No external financial actions, paid subscriptions, production deployment or regulated activity without explicit approval and regulatory review.

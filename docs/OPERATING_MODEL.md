# Operating Model

## Task record
Every task should include: stable ID, project ID, source requirements, objective, acceptance criteria, priority, dependencies, permission tier, estimated cost, assigned role/model, status, retry count, artifacts, QA evidence, actual usage/cost, timestamps, and blocker reason.

## Status lifecycle

`backlog -> ready -> reserved -> running -> needs_qa -> done`

Alternative outcomes: `blocked`, `awaiting_approval`, `failed`, `cancelled`. Only QA with linked evidence can mark a task done. A task cannot be marked done merely because an agent says it finished.

## Workflow

1. Discover candidate work from approved sources.
2. Select the highest-priority task whose dependencies are satisfied.
3. Validate task permissions and reserve estimated cost.
4. Assign a role and choose a model based on verified capability and price.
5. Execute with bounded steps and tools.
6. Store the output, logs, and source references.
7. Run independent acceptance checks.
8. If checks fail, allow up to three bounded repair attempts; then block and report.
9. Update project status only from verified evidence.
10. Notify the user about material blockers, approval requests, risk, or budget thresholds.

## Project-specific constraints

- **Insight:** preserve C01-C11 identifiers and reconcile every requirement to source documents, implementation, and test evidence.
- **Qarar:** focus on product quality, discoverability, and organic growth; no paid campaigns without explicit approval.
- **Trading research:** research, backtesting, and paper trading only by default. No live orders or account changes without explicit, task-specific approval.
- **Other projects:** do not register or change them until their source material and goals are verified.
- Do not include the retired Value project unless reactivated by the user.

## Reporting
A daily or scheduled report should distinguish completed work, proposed work, blockers, QA results, spend estimates, actual spend, and approvals needed. Never report a percentage complete without a defined denominator and evidence.
# AI Company

Budget-controlled autonomous AI project management system.

## Status

Foundation repository only. It is not deployed and no autonomous jobs are running yet.

## Budget guardrails

- Total internal monthly cap: USD 50.
- Model/API internal monthly cap: USD 15.
- Stop low-priority work at thresholds defined in configuration.
- Never place API keys, tokens, passwords, or private credentials in Git.
- Require explicit user approval for live trading, financial transactions, paid purchases, production deployments, and destructive actions.

## Initial roles

- CEO / Planner: priorities and outcomes.
- COO / Orchestrator: task queue, dependencies, blockers, schedules.
- Engineer: bounded implementation tasks.
- QA / Auditor: independent verification and evidence.

These are planned roles, not running agents yet.

## Initial project registry

- Insight: escrow / trusted-intermediary fintech concept. C01-C11 progress must be verified against source artifacts before marking anything complete.
- Qarar: digital financial products store, product quality, SEO, and organic growth.
- Trading research: strategy research, backtesting, paper trading, and reports only until explicitly authorized otherwise.
- Other projects: register only after inspecting available sources.

Do not include the retired Value project unless the user explicitly reactivates it.

## Planned documents

- docs/ARCHITECTURE.md
- docs/BUDGET_AND_GUARDRAILS.md
- docs/OPERATING_MODEL.md
- config/projects.example.json
- config/budget.example.json
- SECURITY.md

## Important

This is a foundation, not a deployed autonomous company. Cloud hosting, persistent database, provider API keys, integrations, scheduling, and tests still need to be configured and verified.

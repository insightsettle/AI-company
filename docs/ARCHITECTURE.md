# Proposed Architecture

## Goal
Build a persistent cloud service that coordinates project work and runs scheduled tasks even when Claude Desktop is closed. This document describes a plan, not a deployed system.

## Components

1. **Project registry** — canonical project IDs, goals, source locations, requirements, owners, statuses, and evidence links.
2. **Task queue** — prioritized tasks with dependencies, approval requirements, retry limits, deadlines, and estimated cost.
3. **Orchestrator** — claims eligible tasks, selects an agent/model, checks permissions and budget, runs work, and records outcomes.
4. **Model router** — provider-neutral adapter that selects an approved model based on task type, quality, and current verified pricing.
5. **Persistent database** — tasks, decisions, usage records, artifacts, approvals, and audit events.
6. **Independent QA** — checks acceptance criteria and evidence before a task can be marked complete.
7. **Scheduler and notifications** — triggers bounded work and reports material blockers, approvals, failures, and budget thresholds.
8. **Dashboard** — project status, work queue, recent changes, approvals, and spending.

## Execution lifecycle

`discover -> prioritize -> budget reservation -> permission check -> assign -> execute -> save evidence -> independent QA -> update registry -> schedule next task`

A failed QA check returns the task to a bounded repair cycle. After the configured retry limit, the task is blocked and reported.

## Deployment principles

- Prefer managed/serverless services and free tiers during the pilot.
- Verify scheduled jobs run while the user's desktop is offline.
- Use database migrations, backups, health checks, and structured logs.
- Keep provider credentials in a secret manager or encrypted environment configuration.
- Do not enable unattended production changes or live financial actions in the first release.

## Initial roles

- **CEO / Planner:** chooses outcomes and resolves priority conflicts.
- **COO / Orchestrator:** coordinates queue, dependencies, blockers, and schedules.
- **Engineer:** implements bounded changes in isolated branches.
- **QA / Auditor:** independently validates outputs and tests.

These are logical roles until execution infrastructure is deployed.

## Project reconciliation

Import project material only from sources the user has authorized. Preserve identifiers such as Insight C01-C11. Never infer completion from a past estimate; require current artifacts and test evidence. Exclude the retired Value project unless the user reactivates it.
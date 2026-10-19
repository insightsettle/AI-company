# Budget and Guardrails

## Monthly internal caps

- Total company spend: **USD 50**.
- Model/API spend: **USD 15**.
- Use free tiers where practical. The remaining amount is an unallocated reserve, not permission to spend automatically.
- These are internal operating limits; provider billing delays or untracked third-party charges can prevent a mathematically perfect real-time guarantee. Configure native billing controls wherever offered and reconcile actual invoices.

## Model-spend alerts and stops

- At USD 7.50: review usage and model routing.
- At USD 10.50: pause low-priority tasks.
- At USD 13.50: stop new model calls and retain a cushion.
- Do not automatically top up credits.

## Per-task controls

Initial proposed targets (to be validated during testing):

- Simple task: USD 0.02 maximum estimated model cost.
- Standard task: USD 0.10 maximum estimated model cost.
- Complex task: USD 0.50 maximum estimated model cost and explicit approval if exceeded.
- Internal daily model-spend target: USD 0.50.
- Maximum automatic repair retries: 3.

Before each model call, reserve estimated cost atomically. The SQLite ledger enforces the configured daily model-spend target against both unsettled reservations and settled actual usage for that UTC date. A reservation must supply a matching `YYYY-MM` month and ISO `YYYY-MM-DD` day (the day defaults to the current UTC date). This is an internal guardrail, not a substitute for provider billing limits. If the budget reservation fails, do not call the provider. Record estimates and actual usage separately, and reconcile provider invoices.

## Permission tiers

- **Tier 0 — read-only:** inspect approved sources, research, summarize, draft plans.
- **Tier 1 — reversible workspace changes:** create draft files or isolated branches and run tests.
- **Tier 2 — external or costly actions:** require explicit approval before spending money, publishing, changing production, or making binding commitments.
- **Tier 3 — high-impact financial actions:** live trading, money transfers, purchases, and irreversible/destructive actions remain disabled unless the user explicitly authorizes the specific action and safeguards are implemented.

## Stop conditions

Stop new work when any of these occurs: total internal spend reaches USD 45; model spend reaches USD 13.50; cost accounting is unavailable; provider spend cannot be estimated; repeated failures exceed the retry limit; credentials may be exposed; or a task requires unapproved permissions. Do not exceed the hard internal ceiling of USD 50 by launching more tasks.

## Model routing

Choose the least expensive approved model that meets the quality requirement. Verify provider pricing at implementation time. Use deterministic code for arithmetic and budget accounting; do not delegate budget enforcement solely to an LLM.
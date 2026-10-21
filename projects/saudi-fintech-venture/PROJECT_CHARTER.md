# Standalone Fintech Venture — Saudi Arabia First

**Status:** RESEARCH BRIEF ONLY — NOT APPROVED TO START EXECUTION  
**Prepared:** 2026-10-21  
**Working rule:** This venture is separate from all previous projects. Do not import, resume, or use the scope, files, assumptions, or task lists of Insight, Qarar, Trading Research, or any other prior project. The AI Company project registry is intentionally empty.

## 1. Mission

Research, validate, and recommend one original, commercially viable fintech opportunity for Saudi Arabia first, with GCC expansion considered only after evidence supports it. Use Claude as the dedicated working environment for this venture, with this document as its project charter and source of truth. AI Company is an orchestration tool, not the product being built.

The objective is not to chase a trend. Find a specific, costly, recurring financial problem; validate the problem with credible evidence and prospective customers; assess regulatory feasibility; then recommend a lean prototype and measurable go/no-go criteria.

## 2. Mandatory start gate — do not bypass

**No project execution, product build, provider API calls, paid services, production deployment, customer onboarding, movement of money, or external commitments until all of the following are evidenced:**

1. AI Company test suite has run in GitHub Actions and reports success for the current commit.
2. Repository health/security review is completed; any critical/high severity defects are fixed or explicitly blocked.
3. CLI smoke tests pass; budget reservation, settlement, release, monthly cap, daily target, idempotency, task leases, retries, dependency gating, and QA completion gate have test evidence.
4. Concurrency and crash/recovery behavior have been tested. A task stuck in `running` must not be blindly replayed if it could cause external side effects.
5. Actual cloud persistence, scheduled execution, restart recovery, and work continuing while Claude is closed are demonstrated in a non-production environment. Documentation alone is not evidence.
6. Model/provider routing, secrets handling, cost estimation and actual-cost reconciliation are tested with mock providers first. No API keys in Git.
7. Budget controls are verified: USD 50/month total internal ceiling; USD 15/month model/API ceiling. Set provider-side billing alerts/caps where available. If provider caps cannot be guaranteed, do not enable paid calls.
8. Independent QA signs off with a dated evidence report listing commands, commits, run links, pass/fail results, known gaps, and residual risks.

If any gate fails or cannot be tested, stop at research/documentation and report the blocker. Never claim a test passed without its result. The current repository has not yet demonstrated successful CI, cloud hosting, provider integration, or unattended execution; these must be verified rather than assumed.

## 3. Research scope and current signals (as of 2026-10-21)

Use primary sources first: SAMA, Saudi Open Banking Framework, Ministry of Commerce, Monsha'at, ZATCA, Saudi Data & AI Authority, CMA when applicable, and official regulators in Bahrain, UAE, and other GCC markets. Use industry reports and interviews as secondary evidence. Clearly label dated facts, estimates, assumptions, and hypotheses. Do not treat a trend report as proof of demand.

### Evidence signals to investigate

- **Saudi open banking is moving toward commercial operation.** SAMA announced the start of licensing fintech companies for open banking services on 26 March 2026, after the regulatory sandbox phase. Its September 2026 Open Banking Forum discussed Payment Initiation Services and expanding open banking use by businesses. Potential implications include consent-based financial dashboards, cash-flow insights, reconciliation, and SME financial workflows. Regulatory permission and partner access are essential; do not assume an unlicensed startup can access bank APIs.
- **Digital payments are mature enough to support adjacent workflows.** SAMA reported that electronic payments accounted for 85% of Saudi retail payments in 2025, up from 79% in 2024. This supports investigation of reconciliation, treasury visibility, fraud controls, and payment operations—not a generic “another wallet” idea.
- **SME financing, factoring, and receivables remain relevant areas to test.** SAMA announced four new sandbox fintechs in February 2025, including P2P lending and MSME factoring. Competition and licensing complexity must be mapped; these announcements do not prove that any specific gap remains open.
- **Cross-border B2B payment friction is a hypothesis worth validating.** A 2026 regional industry survey reports settlement delays and unclear transfer costs among surveyed SMEs. Treat its sample and commercial perspective critically; verify with Saudi importers/exporters and their finance teams before using figures in an investor case.
- **AI-native financial operations may create efficiencies, but require controls.** Investigate invoice data extraction, transaction matching, cash-flow forecasting, Arabic-first finance copilots, and compliance workflow assistance. Avoid autonomous financial advice or payment execution in the initial product.

### Starting source list

1. SAMA — Open banking licensing announcement, 26 March 2026: https://www.sama.gov.sa/en-US/MediaCenter/News/Pages/news-1135.aspx
2. SAMA — Open Banking Framework and Open Banking Lab: https://www.openbanking.sama.gov.sa/index-en.html
3. SAMA — Open Banking Forum, 17 September 2026: https://sama.gov.sa/en-US/MediaCenter/News/pages/news-1171.aspx
4. SAMA — E-payments accounted for 85% of retail payments in 2025, announcement listed 12 April 2026: https://sama.gov.sa/en-US/MediaCenter/News/pages/allnews.aspx?PageFirstRow=25&Paged=TRUE&View=e89bae7e-2d45-471c-bfac-824a22711046&p_ID=1409&p_SAMAPublishingDate=20260429+12%3A30%3A00&p_SortBehavior=0
5. SAMA — Fintech sandbox companies including P2P lending and MSME factoring, 11 February 2025: https://sama.gov.sa/en-US/MediaCenter/News/pages/news-1073.aspx
6. Gulf News — GCC fintech trends and funding, 12 May 2026 (secondary analysis): https://gulfnews.com/business/analysis/how-fintech-across-gcc-is-growing-up-1.500537845
7. ARP Digital — GCC SME cross-border payments report, 22 May 2026 (commercial research; independently validate): https://www.arpdigital.io/en/resources/news-insights/gcc-sme-cross-border-payments-2026
8. Reuters — Circle's international expansion and stablecoin developments, 16 October 2026 (context only; not a recommendation to issue/use stablecoins): https://www.reuters.com/technology/stablecoin-issuer-circle-push-into-40-new-markets-ceo-says-2026-10-16/

Refresh all sources when work begins; record publication date and access date. Do not treat stablecoins, lending, remittance, custody, escrow, payment initiation, or handling customer funds as permissible without written regulatory analysis.

## 4. Opportunity hypotheses to score, not pre-select

Score each opportunity 1–5 on pain severity, frequency, willingness to pay, access to buyers, time to MVP, differentiation, regulatory burden (reverse score), capital intensity (reverse score), data/integration access, and GCC scalability. Attach evidence and confidence to each score.

### A. SME cash-flow and bank-reconciliation workspace
- **Problem hypothesis:** Saudi SMEs reconcile bank transactions, invoices, receivables and payables across disconnected systems; owners lack a timely cash position.
- **Potential solution:** Arabic-first cash position, bank-feed imports or consent-based open-banking connection where authorized, invoice matching, alerts, and a 13-week cash forecast.
- **Potential customer/payer:** finance managers, accountants, SME owners, accounting firms.
- **Business model to test:** monthly SaaS tier per entity or accountant-managed portfolio.
- **Risks:** existing accounting software, integration access, sensitive financial data, forecast trust, PDPL and cybersecurity obligations.
- **MVP boundary:** start with customer-uploaded CSV/Excel and read-only reports; no bank credentials, payment initiation, or money movement.

### B. Accounts-receivable follow-up and invoice-to-cash assistant
- **Problem hypothesis:** SMEs lose time tracking invoices, payment promises, overdue receivables and disputes.
- **Potential solution:** invoice aging, Arabic/English reminders approved by the user, dispute notes, payment matching, and collection analytics.
- **Payer:** B2B suppliers and finance teams.
- **MVP boundary:** upload invoices/CSV and generate drafts/reports; do not send messages automatically without approval.
- **Risks:** crowded accounting/ERP market, invoice-data quality, integration effort.

### C. SME financing-readiness and receivables-finance workflow
- **Problem hypothesis:** smaller businesses struggle to assemble reliable cash-flow, invoice and financial data for lenders.
- **Potential solution:** consent-based financial data pack, document checklist, cash-flow explanation and lender-ready reporting; refer only to appropriately licensed providers.
- **Revenue hypothesis:** B2B SaaS or disclosed referral arrangements where legally permitted.
- **Risks:** lending/credit intermediation regulation, conflicts of interest, credit decisions, data privacy. Do not lend or underwrite in MVP.

### D. Cross-border B2B payment visibility and cost comparison
- **Problem hypothesis:** Saudi importers/exporters face uncertain fees, slow settlement, compliance requests and poor payment-status visibility on specific corridors.
- **Potential solution:** payment workflow tracker, document readiness checklist, transparent fee/FX comparison using public or partner-supplied quotes, status and exception management.
- **Payer:** importers, exporters, wholesalers and finance teams.
- **MVP boundary:** workflow and comparison only; no remittance, FX execution, custody, or payment routing without authorized partners and regulatory review.
- **Risks:** strong incumbent banks, partner dependence, compliance, sanctions screening and corridor-specific restrictions.

### E. Arabic-first finance operations copilot
- **Problem hypothesis:** small finance teams repeatedly perform time-consuming invoice extraction, reconciliation, monthly close checklists and variance explanations.
- **Potential solution:** AI assistant that cites source rows/documents, flags uncertainty, keeps an audit trail, and requires human approval for accounting entries or outbound actions.
- **Payer:** SMEs, outsourced accountants, finance consultancies.
- **MVP boundary:** user-uploaded synthetic/sample data first; no autonomous journal posting or bank actions.
- **Risks:** hallucinations, confidential data exposure, accounting correctness and crowded AI tooling.

## 5. Required research work before recommending one idea

1. Build a dated source register covering global fintech changes and Saudi/GCC regulatory updates from the last 12 months, prioritizing the latest 90 days.
2. Map Saudi licensing perimeter and applicable obligations for every shortlisted model: SAMA, CMA, PDPL, AML/CFT, cybersecurity, outsourcing, consumer protection, and any other relevant authority. Cite primary documents and mark questions requiring a Saudi lawyer or regulator.
3. Map at least 10 competitors/alternatives per finalist, including banks, fintechs, accounting platforms and manual workflows; identify pricing where public and never invent prices.
4. Define 3–5 customer segments and conduct at least 10–15 discovery interviews before claiming product-market fit. Do not fabricate interviews, quotes, TAM, or willingness-to-pay.
5. Quantify the problem with transparent bottom-up calculations and ranges. Separate sourced inputs from assumptions.
6. Test demand using a landing-page/waitlist or concierge prototype only after the start gate; no paid ads unless separately approved.
7. Create an opportunity scorecard and recommend one primary idea plus one backup. Include why other ideas were rejected.
8. Produce a 90-day validation roadmap, lean MVP scope, costs within the USD 50 total monthly / USD 15 model budget until explicitly revised, measurable milestones, kill criteria, and regulatory questions.
9. Include Sharia considerations where relevant, without presenting an unqualified legal or religious conclusion.
10. Deliver the final recommendation in Arabic, with an English technical brief if needed.

## 6. Team / AI employee design

Do not create or pay for new external services or human contractors without explicit approval. After the start gate, AI Company may assign bounded, auditable roles:

- Research Lead: source register and global/Saudi trend monitoring.
- Saudi Regulatory Analyst: regulator-first perimeter map; flags items for professional advice.
- Customer Discovery Lead: interview guide, interview notes and evidence ledger; never fabricate responses.
- Product Strategist: opportunity scorecard, value proposition, MVP and go/no-go metrics.
- Competitor Analyst: competitor matrix with citations and dated prices.
- Engineer: prototype only after approval; synthetic data first.
- Independent QA / Red Team: challenge assumptions, reproduce calculations, check citations, test security and privacy.
- Finance & Budget Controller: reserve before spend, reconcile actuals, halt at caps.

Each task must have an owner, input sources, deliverable, deadline, estimated cost, permission tier, acceptance criteria, and independent QA. The Research Lead cannot approve its own conclusions. Agents must not receive broader permissions than their task needs.

## 7. Permissions and non-negotiable safety

- Default to read-only research, mock data, dry-run and local prototypes.
- No handling or custody of customer funds; no escrow, lending, payment initiation, FX execution, investment recommendations, or regulated activities without a documented licensing path and qualified advice.
- No production deployment, customer data ingestion, contacting prospects, sending emails, signing contracts, paid subscriptions, or external commitments without explicit user approval.
- Never place secrets or personal customer data in GitHub, prompts, or logs.
- Keep a source ledger, decision log, audit trail and change history.
- Any budget cap, permission or scope change must be explicitly approved by the user.
- If evidence is weak, say so; do not claim guaranteed success.

## 8. Deliverables

1. Current global fintech developments report with dates and citations.
2. Saudi/GCC problem and opportunity map.
3. Regulatory perimeter and unresolved legal questions.
4. Competitor matrix and evidence ledger.
5. Opportunity scorecard with confidence ratings.
6. Primary recommendation and backup, with problem solved and buyer/payer clearly defined.
7. Customer interview plan and validation metrics.
8. Lean MVP specification and 90-day roadmap.
9. Cost/budget plan and explicit kill criteria.
10. Independent QA report.

## 9. Claude kickoff prompt

You are the dedicated research team for a **new, standalone fintech venture focused first on Saudi Arabia**. Treat this file as the project charter. Do not import or resume any prior project. Begin with source-based research and a regulatory-first opportunity analysis only. Refresh the dated sources, search for developments from the last 12 months (especially the latest 90 days), cite primary sources, compare the opportunity hypotheses, and produce the deliverables above in Arabic.

**Critical stop condition:** Before doing any project execution beyond research/documentation, request and inspect AI Company's independent test evidence. If GitHub Actions success, security review, budget enforcement, persistence, unattended scheduling, and safe recovery are not proven, report the exact gaps and stop. Never state that AI Company is operational or tests pass without evidence. Do not use paid APIs or external services, contact people, build/deploy production software, or move money without explicit approval. Keep initial monthly limits at USD 50 total and USD 15 for models/API.

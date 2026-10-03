---
description: One tested Decimal/calendar implementation produces explainable financial and replacement results.
---

# Objective
One tested Decimal/calendar implementation produces explainable financial and replacement results.

Scope status: PROPOSED, unexecuted. Trace: FR-011, FR-014, FR-018, FR-019, SC-003, SC-008, AR-003.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f002c -> [f002d, f003a] -> f004a`; full dependency graph is in docs/tasks.md.
- Prerequisites: f002c and f001b delivered within their stated acceptance limits.
- Approval gate: Finance/display settings. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: May run alongside f002d after f002c and both approval gates. Own src/services and unit tests only. f002d owns views/browser tests. Neither edits shared conftest or root files during this window. Otherwise serialize.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f003-report-financial-reporting.md, f003-status-financial-reporting.md, and one f003 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/services/`.
- Allowed secondary folders/files: tests/unit/test_finance.py; tests/unit/test_display.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Compute the current installation anchor or purchase fallback. Derive each anniversary from the original current service day with month-end clamping, including leap years. Completed months are zero before service and capped at positive life.
2. Use Decimal precision 28 and ROUND_HALF_UP. Compute cost × capped_months / life and cost minus depreciation. Resolve active override pair before source pair. Return decimal strings. Do not round intermediate values.
3. Compute replacement by anchor plus useful-life months. Classify overdue, today, future days 1–90 inclusive, and Later. Sum separate overdue/today/future spending proxies through the inclusive twelve-calendar-month endpoint.
4. Validate all five positive finite dated FX rates with USD=1. Convert USD-per-source-unit. Group local totals by effective currency, sum each distinct asset once, and quantize only display: JPY zero places, others two.
5. Use injected explicit reporting dates/clock/config for independent tests. Invalid FX produces approved diagnostics without fabricated/partial totals. Financial date never changes operational data or chooses a different rate table.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. USD 1200 on July 14/15 yields 500/700 and 600/600. Original-day month-end, leap-year, before-service, and life-cap examples match the spec.
2. Day 90/day 91 and twelve-calendar-month endpoint/+1 distinguish categories/windows. Effective cost is the spending proxy, without book-value subtraction.
3. 0.004+0.004 displays as USD 0.01 after aggregation. HKD800 at isolated rate0.125 gives USD100. Invalid/missing rates fail honestly; local currencies remain separate.
4. Required scenario references: AC-US05-001, AC-US05-002, AC-US05-003, AC-US05-004, AC-US05-005, AC-US05-006, AC-US05-007, AC-US05-008, AC-US05-009, AC-US05-010, AC-US05-011, AC-US05-012, AC-US05-013. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/unit/test_finance.py tests/unit/test_display.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Pure calculations add no UI. f003b/f003c and f007a own I/B/M financial integration evidence.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

---
description: Actual imported, edited, overridden, and maintained records drive consistent scoped financial reports.
---

# Objective
Actual imported, edited, overridden, and maintained records drive consistent scoped financial reports.

Scope status: PROPOSED, unexecuted. Trace: FR-006, FR-011, FR-014, FR-018, FR-019, SC-003, SC-005, SC-008, AR-003.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f003a + f004c + f005c + f006c -> f003b`; full dependency graph is in docs/tasks.md.
- Prerequisites: f003a, f004c, f005c, f006c delivered within their stated acceptance limits.
- Approval gate: Previously approved Finance/display settings scope; renewed review for consequential deviations. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f003-report-financial-reporting.md, f003-status-financial-reporting.md, and one f003 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `tests/`.
- Allowed secondary folders/files: src/services financial/reporting adapters only; src/views thin finance response wiring only.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Complete independent integration methods for US-05 and currency/date US-02 cases using real store/service/HTTP boundaries. Verify current edited anchors, applied invoices, override reset/clearing, and grouped totals.
2. Verify overview/room financial payloads use the same scoped unique asset set and f003a calculation functions. Do not duplicate rules in SQL or browser code.
3. Test complete/absent/invalid configuration under approved P-03. Preserve operational reads and assumptions access while withholding invalid totals.
4. Exercise explicit asset-linked critical flags separately from replacement date categories. Multiple tickets/invoices cannot duplicate acquisition/book/spending amounts.
5. Repair only financial adapters/response wiring exposed by these checks. Changes to unrelated mutations/schema/layout require a separately scoped job.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. All U/I financial methods in verification-plan.md pass with independent starting states and unchanged-record assertions.
2. Reporting-date, currency, invoice, override/reset, and maintenance inputs compose without duplicate totals or condition inference.
3. Failures identify configuration and omit invalid totals. Record actual evidence, including omissions; no full-series completion until f003c browser methods pass.
4. Required scenario references: AC-US05-001, AC-US05-002, AC-US05-003, AC-US05-004, AC-US05-005, AC-US05-006, AC-US05-007, AC-US05-008, AC-US05-009, AC-US05-010, AC-US05-011, AC-US05-012, AC-US05-013, AC-US02-006, AC-US02-008, AC-US02-018, AC-US02-019, AC-US03-012, AC-US04-016. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/unit/test_finance.py tests/unit/test_display.py tests/integration/test_records.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Final visible reporting follows in f003c. Do not claim B/M results from integration assertions.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

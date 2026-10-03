---
description: Supporting financial reports and assumptions explain real scoped calculations and independent display settings.
---

# Objective
Supporting financial reports and assumptions explain real scoped calculations and independent display settings.

Scope status: PROPOSED, unexecuted. Trace: FR-011, FR-014, FR-017, FR-018, UX-004, UX-014, UX-019, SC-003, SC-008, AR-003.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f003b -> f003c`; full dependency graph is in docs/tasks.md.
- Prerequisites: f003b delivered within their stated acceptance limits.
- Approval gate: Finance/display settings. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f003-report-financial-reporting.md, f003-status-financial-reporting.md, and one f003 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/views/`.
- Allowed secondary folders/files: tests/browser/test_journeys.py; tests/browser/test_ui.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Complete Overview financial/replacement sections after operational content. Show source/current/effective pairs, service anchor/fallback, depreciation/book values, replacement dates/categories, separate proxy horizons, and explicit critical-link flags.
2. Provide custom Financial reporting date and Reset to today. Retain tab date on navigation/reload and initialize new sessions from server Hong Kong today. Label operational date and timestamps/offsets separately.
3. Wire upper-right USD/Local transaction currency controls through shared independent persistent preferences. Display server results without recomputing finances. Offer English and only delivered reviewed stretch sets.
4. Complete the entire UX-019 read-only assumptions inventory using approved rules and loaded configuration. Show fixed FX date/disclaimer/rates/owners, invalid configuration, prototype limits, and AR-002 gap before imports too.
5. Implement all US-05/US-02 financial B methods and IX-UX-014/019. Complete unchanged source/user text and preference tests, including separate reporting/operational clocks.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Scoped reports and local/USD display match service values, approved labels, numeric rounding, and independent preference/date behavior.
2. Missing FX shows corrective diagnostics without partial/fabricated totals; operational views and assumptions stay usable.
3. Installed-Chrome and automated browser checks show accessible custom-date/currency controls, complete assumptions, honest limits, and no source/history mutation from display changes.
4. Required scenario references: AC-US05-001, AC-US05-002, AC-US05-003, AC-US05-004, AC-US05-005, AC-US05-006, AC-US05-007, AC-US05-008, AC-US05-009, AC-US05-010, AC-US05-011, AC-US05-012, AC-US05-013, AC-US02-006, AC-US02-008, AC-US02-016, AC-US02-017, AC-US02-018, AC-US02-019, AC-US03-012, AC-UX-004, AC-UX-014, AC-UX-019, AC-DEMO-003. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/browser/test_journeys.py tests/browser/test_ui.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Run mapped B/M financial/display methods and IX-UX-014/019 in Windows installed Chrome. Record linguistic review separately if any stretch set is delivered.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

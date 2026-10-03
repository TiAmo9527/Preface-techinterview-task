---
description: Users independently preview, review, confirm, and inspect honest import outcomes.
---

# Objective
Users independently preview, review, confirm, and inspect honest import outcomes.

Scope status: PROPOSED, unexecuted. Trace: FR-002–FR-005, FR-015, UX-007, UX-008, UX-013, SC-002, AR-001, AR-002.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f002c -> f002d`; full dependency graph is in docs/tasks.md.
- Prerequisites: f002c delivered within their stated acceptance limits.
- Approval gate: Imports. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: May run alongside f003a after f002c and both approval gates. Own src/views and browser tests only. f003a owns services/unit tests. Neither edits shared conftest or root files during this window. Otherwise serialize.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f002-report-reviewed-imports.md, f002-status-reviewed-imports.md, and one f002 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/views/`.
- Allowed secondary folders/files: tests/browser/test_journeys.py; tests/browser/test_ui.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Implement Assets/Invoices selection, one file upload, prerequisite guidance, proposed counts, blocker/warning diagnostics, source coordinates, six-field before/after changes, and explicit override-clearing effects.
2. Invalidate the browser preview when file/workflow changes. Disable confirmation for blockers and during submission. Keep warnings visible and allow warning-only confirmation.
3. Handle stale preview by renewed review and a separate confirmation action. Preserve file/workflow/summary/diagnostics after failure and keep the same command identity for an unchanged retry. Show actual counts only after success.
4. Cancel saves nothing. Refetch affected server data after successful import/receipt replay. Use shared request/state/English/feedback primitives without another rule implementation.
5. Add browser methods for every US-01 row marked B in verification-plan.md and IX-UX-007/008. Test full two-tab preview-reset and committed retry through the actual routes.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Invalid Assets on empty state and invalid Invoices on independently seeded baseline show blockers and zero saved effects.
2. Valid baseline and invoice imports are separate reviewed actions with actual 4/12/36 and 36/36 results. Headers-only, warning, cancelled, stale, failed, and retry states follow mapped outcomes.
3. Installed-Chrome review confirms labelled diagnostics, pending controls, keyboard feedback, and retained correction input. No paired upload/PDF workflow appears.
4. Required scenario references: AC-US01-001, AC-US01-002, AC-US01-008, AC-US01-019, AC-US01-020, AC-US01-021, AC-US01-022, AC-UX-007, AC-UX-008, AC-UX-013, AC-INFRA-005, AC-INFRA-007, AC-INFRA-008. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/browser/test_journeys.py tests/browser/test_ui.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Run B/M import methods and IX-UX-007/008/013 with real endpoints in Windows installed Chrome.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

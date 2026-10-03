---
description: Managers edit existing assets and understand their source, effective values, and histories.
---

# Objective
Managers edit existing assets and understand their source, effective values, and histories.

Scope status: PROPOSED, unexecuted. Trace: FR-010, FR-015, FR-019, UX-010, UX-011, SC-003, SC-004, AR-002, AR-003.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f006b -> f006c`; full dependency graph is in docs/tasks.md.
- Prerequisites: f006b delivered within their stated acceptance limits.
- Approval gate: Assets/overrides. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f006-report-asset-accountability.md, f006-status-asset-accountability.md, and one f006 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/views/`.
- Allowed secondary folders/files: tests/browser/test_journeys.py; tests/browser/test_ui.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Add nested room-card operational editors with permitted fields and read-only identities/category/calculated results. Show purchase fallback clearly. Create no Add asset action.
2. Add separate Apply financial override and Reset to source forms with paired values, reason, recorder, source identification, and before/after history. Explain unchanged operational fields during reset.
3. Render baseline/invoice evidence/provenance, historical-only items, applied updates/references, and override history. Label source/current/effective values distinctly.
4. Protect dirty forms across room/filter/navigation/card changes. Preserve failure/stale input and provide explicit Review latest. Refresh real room/overview/financial results after successful saved commands.
5. Execute all US-03 B methods and IX-UX-010/011 with independently prepared records and real routes. Preserve AR-002 manual-creation disclosure and unconfirmed interpretation.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Permitted edits, paired override, source reset, histories, and source/current/effective labels match actual server state and survive restart.
2. Cancelled/invalid/failed/stale commands show no success and preserve required saved state/input. Applied versus historical invoices have the approved effects.
3. Installed-Chrome/keyboard/narrow-card evidence passes mapped checks. Manual asset creation remains explicitly unmet under AR-002.
4. Required scenario references: AC-US03-001, AC-US03-002, AC-US03-003, AC-US03-004, AC-US03-005, AC-US03-006, AC-US03-007, AC-US03-008, AC-US03-009, AC-US03-010, AC-US03-011, AC-US03-012, AC-UX-010, AC-UX-011, AC-UX-013, AC-UX-016, AC-UX-017, AC-INFRA-001, AC-INFRA-008. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/browser/test_journeys.py tests/browser/test_ui.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Run asset B/M methods and IX-UX-010/011, including dirty/failure states and actual history offsets, in Windows installed Chrome.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

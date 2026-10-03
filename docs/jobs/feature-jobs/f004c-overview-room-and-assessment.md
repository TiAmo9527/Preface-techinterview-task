---
description: Managers can filter, select rooms, inspect context, and save or clear independent observations.
---

# Objective
Managers can filter, select rooms, inspect context, and save or clear independent observations.

Scope status: PROPOSED, unexecuted. Trace: FR-006–FR-009, FR-015, FR-016, UX-002–UX-005, UX-009, SC-004, SC-005, AR-004.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f004b -> f004c`; full dependency graph is in docs/tasks.md.
- Prerequisites: f004b delivered within their stated acceptance limits.
- Approval gate: Observations/reporting. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f004-report-room-understanding.md, f004-status-room-understanding.md, and one f004 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/views/`.
- Allowed secondary folders/files: tests/browser/test_journeys.py; tests/browser/test_ui.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Render approved Overview order and shared filters. Clear incompatible children and close excluded selected cards through dirty protection. Search room/property labels case-insensitively as view-only, with separate scope/search-empty feedback.
2. Build default schematic property-grouped Map and equivalent List using deterministic label/identity order. Preserve representation/search/selection and return scroll context. Label three observations and unresolved counts separately.
3. Render bordered desktop room card and approved narrow overlay. Keep headings/Close/actions reachable, focus correctly, protect dirty forms, and reject obsolete room responses using shared sequencing.
4. Add inline observation forms, separate confirmed Clear, required metadata feedback, and distinct recorded/unassessed Unknown. Refetch server counts/room only after saves. Retain drafts on failure.
5. Expose the Log fault handoff boundary with origin context and room preselection for f005c. Do not show a functioning ticket save until its real service/routes exist. Asset editing belongs to f006c.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Every Map/List/ticket link shows correct independent room context and consistent counts. Search never changes reporting scope/totals.
2. Observation Save/Clear/cancel/invalid/failure/restart cases pass B methods. Late A response cannot replace B. No maintenance inference changes condition.
3. IX-UX-002/003/004/005/009 and relevant shared UX checks pass for delivered room surfaces. Log fault save/return acceptance remains pending f005c.
4. Required scenario references: AC-US02-001, AC-US02-002, AC-US02-003, AC-US02-004, AC-US02-005, AC-US02-006, AC-US02-007, AC-US02-008, AC-US02-009, AC-US02-010, AC-US02-011, AC-US02-012, AC-US02-013, AC-US02-014, AC-US02-015, AC-UX-002, AC-UX-003, AC-UX-004, AC-UX-005, AC-UX-009, AC-UX-013, AC-UX-016, AC-UX-017, AC-INFRA-003. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/browser/test_journeys.py tests/browser/test_ui.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Run mapped room B/M methods and IX-UX-002/003/004/005/009, including widths/focus/dirty forms, in Windows installed Chrome.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

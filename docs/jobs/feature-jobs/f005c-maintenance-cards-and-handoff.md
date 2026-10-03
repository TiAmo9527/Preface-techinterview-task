---
description: Managers log faults, assign owners, progress work, and inspect history from both approved entry points.
---

# Objective
Managers log faults, assign owners, progress work, and inspect history from both approved entry points.

Scope status: PROPOSED, unexecuted. Trace: FR-012, FR-013, FR-015, UX-005, UX-006, UX-012, SC-004, AR-005.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f005b -> f005c`; full dependency graph is in docs/tasks.md.
- Prerequisites: f005b delivered within their stated acceptance limits.
- Approval gate: Maintenance. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f005-report-accountable-maintenance.md, f005-status-accountable-maintenance.md, and one f005 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/views/`.
- Allowed secondary folders/files: tests/browser/test_journeys.py; tests/browser/test_ui.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Implement Maintenance default unresolved view, resolved view, ordered rows, room links, explicit Unassigned/No target date/Room only, and on-demand right-side create/edit cards with approved narrow overlay.
2. Create forms for existing room and optional same-room asset, description, severity, owner/target, and typed recorder. Room-card Log fault preselects room, leaves asset unselected, focuses description, and retains origin context.
3. Cancel returns to the originating room card with scope/search/representation/selection/scroll intact and no ticket. Save displays the new ticket in Maintenance; Overview refreshes when returning.
4. Use Save/Cancel for unresolved fields, Start work/Resolve actions, owner prerequisite guidance, and resolution-note input. Fixed links/generated fields remain read-only. Resolved tickets expose history only.
5. Disable duplicate pending commands, retain failed/stale drafts, use Review latest, and show chronological history. Complete mapped B/M methods and IX-UX-005/006/012/013/018 using real endpoints.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Both creation entries persist one valid Open ticket with separate recorder/owner. Cancel creates nothing and preserves complete return context.
2. Ownerless start, blank note/recorder, invalid association/stale/failed save, and duplicate retry follow expected feedback/state. Valid progress resolves read-only with history.
3. Room counts refresh and observations/replacement remain independent. Installed-Chrome keyboard/overlay/handoff checks pass with actual evidence.
4. Required scenario references: AC-US04-001, AC-US04-004, AC-US04-006, AC-US04-008, AC-US04-009, AC-US04-010, AC-US04-011, AC-US04-012, AC-UX-005, AC-UX-006, AC-UX-012, AC-UX-013, AC-UX-016, AC-UX-017, AC-UX-018, AC-INFRA-001, AC-INFRA-002, AC-INFRA-008, AC-INFRA-009. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/browser/test_journeys.py tests/browser/test_ui.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Run maintenance B/M methods and IX-UX-005/006/012/013/018 in Windows installed Chrome, including assistive-technology evidence when required.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

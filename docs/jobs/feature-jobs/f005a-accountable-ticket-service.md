---
description: Manual tickets have accountable owners, fixed links, forward progression, and atomic history.
---

# Objective
Manual tickets have accountable owners, fixed links, forward progression, and atomic history.

Scope status: PROPOSED, unexecuted. Trace: FR-012, FR-013, FR-015, FR-016, SC-004, SC-005, AR-005.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f004c -> f005a`; full dependency graph is in docs/tasks.md.
- Prerequisites: f004c delivered within their stated acceptance limits.
- Approval gate: Maintenance. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f005-report-accountable-maintenance.md, f005-status-accountable-maintenance.md, and one f005 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/services/`.
- Allowed secondary folders/files: src/db ticket/history query adapters; tests/unit/test_maintenance.py; tests/integration/test_records.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Create exactly one Open ticket for a valid existing room, optional same-room asset, description, severity, optional owner/target, and required typed recorder. Generate IDs/actual timestamps. Recorder is separate from configured owner.
2. Edit unresolved description/severity/owner/target through shared coordinator. Keep room/asset fixed. Open permits owner removal; In progress requires owner but permits reassignment.
3. Allow only Open -> In progress -> Resolved. Start requires saved owner. Resolve requires note, typed recorder, actual resolution time, and becomes immutable. Reject skips, reopening, deletion, and resolved editing.
4. Write one chronological before/after event per command, including simultaneous edits, resulting version, recorder, and actual instant. Entity/history/receipt commit together and survive restart.
5. Use f004a scope/order/critical-link projection. Keep observations, source/effective asset values, and replacement dates unchanged by ticket commands. Test duplicate/lost-response retry after restart, stale versions, busy/failure rollback.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. All US-04 U/I cases pass independently with fixed association/owner/status/recorder rules and required history.
2. Repeated creation returns one ticket/CREATE event; changed payload conflicts. No failed/stale command writes ticket/history/receipt.
3. Only explicit linked Critical unresolved tickets flag assets. Sort/missing-information/resolved separation and unchanged observations/finance match expectations.
4. Required scenario references: AC-US04-001, AC-US04-002, AC-US04-003, AC-US04-004, AC-US04-005, AC-US04-006, AC-US04-007, AC-US04-008, AC-US04-009, AC-US04-010, AC-US04-011, AC-US04-012, AC-US04-013, AC-US04-014, AC-US04-015, AC-US04-016, AC-INFRA-001, AC-INFRA-002, AC-INFRA-008, AC-INFRA-009. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/unit/test_maintenance.py tests/integration/test_records.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Services add no rendered controls. f005b/f005c verify real route/browser behavior.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

---
description: Thin maintenance routes expose only valid creation, editing, and progression commands.
---

# Objective
Thin maintenance routes expose only valid creation, editing, and progression commands.

Scope status: PROPOSED, unexecuted. Trace: FR-012, FR-013, FR-015, SC-004, AR-005.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: Medium

# Execution Order
- DAG: `f005a -> f005b`; full dependency graph is in docs/tasks.md.
- Prerequisites: f005a delivered within their stated acceptance limits.
- Approval gate: Maintenance. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f005-report-accountable-maintenance.md, f005-status-accountable-maintenance.md, and one f005 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/views/`.
- Allowed secondary folders/files: tests/integration/test_records.py; app.py route registration only.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Wire the existing maintenance list/detail/create/patch/start/resolve endpoints to f005a services and frozen models. Expose fixed links, versions, separate resolved views, and ordered history.
2. Reject unexpected room/asset/status/timestamp changes and missing recorders at HTTP boundaries. Keep Start separate from Save owner and Resolve separate from general editing.
3. Return approved errors/no-store headers, generation, latest stale record, and saved response receipts. Verify restart retry through actual HTTP requests.
4. Keep visual layout and shared state/CSS unchanged. Add no unrestricted status endpoint or ticket deletion/reopen route.
5. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
6. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Independent maintenance I methods pass through HTTP, including recorder, same-room link, fixed associations, transitions, history, and resolved immutability.
2. Stale/busy/failed/repeated requests match shared mutation contracts and preserve all unchanged-state obligations.
3. Non-visual route wiring is reviewable without changing existing room/import presentation.
4. Required scenario references: AC-US04-001, AC-US04-002, AC-US04-003, AC-US04-004, AC-US04-005, AC-US04-006, AC-US04-007, AC-US04-008, AC-US04-009, AC-US04-010, AC-US04-011, AC-US04-012, AC-US04-013, AC-US04-014, AC-US04-015, AC-US04-016, AC-INFRA-001, AC-INFRA-002, AC-INFRA-008, AC-INFRA-009. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/integration/test_records.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Browser form verification is assigned to f005c.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

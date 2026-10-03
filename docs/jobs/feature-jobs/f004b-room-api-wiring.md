---
description: Thin room/overview and observation endpoints expose one consistent reporting contract.
---

# Objective
Thin room/overview and observation endpoints expose one consistent reporting contract.

Scope status: PROPOSED, unexecuted. Trace: FR-006–FR-009, FR-015, FR-016, SC-004, SC-005, AR-004.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: Medium

# Execution Order
- DAG: `f004a -> f004b`; full dependency graph is in docs/tasks.md.
- Prerequisites: f004a delivered within their stated acceptance limits.
- Approval gate: Observations/reporting. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f004-report-room-understanding.md, f004-status-room-understanding.md, and one f004 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/views/`.
- Allowed secondary folders/files: tests/integration/test_records.py; app.py route registration only.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Wire existing GET /api/overview, GET /api/rooms/{room_id}, observation PUT, and observation Clear POST to f004a services with f001b contracts. No SQL/domain rules belong in routes.
2. Validate scope/date/currency inputs and generation before missing-record checks. Return generation/version and no-store headers. Use approved P-03 invalid-finance response without blocking valid operational payloads.
3. Exercise real HTTP requests against isolated on-disk stores. Check extra/protected fields, stale generation/version, structured diagnostics, and failed writes.
4. Keep visual modules/shared CSS unchanged in this non-visual job. Freeze response integration before f004c renders the room journey.
5. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
6. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. API scope/room payloads match independent expected records and counts, and valid Save/Clear refresh saved versions.
2. Invalid/failed/stale commands return approved error shapes without partial rows/history/receipt. Current persisted state remains inspectable.
3. Real HTTP integration passes applicable US-02 I methods. Browser presentation still awaits f004c.
4. Required scenario references: AC-US02-001, AC-US02-002, AC-US02-003, AC-US02-004, AC-US02-005, AC-US02-006, AC-US02-007, AC-US02-008, AC-US02-009, AC-US02-010, AC-US02-011, AC-US02-012, AC-US02-013, AC-US02-014, AC-US02-015, AC-INFRA-001, AC-INFRA-008. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/integration/test_records.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Non-visual route wiring. Browser methods are explicitly assigned to f004c.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

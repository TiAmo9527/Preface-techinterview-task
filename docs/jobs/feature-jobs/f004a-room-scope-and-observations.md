---
description: Shared scoped room reads and valid latest observations remain consistent and durable.
---

# Objective
Shared scoped room reads and valid latest observations remain consistent and durable.

Scope status: PROPOSED, unexecuted. Trace: FR-006–FR-009, FR-015, FR-016, SC-004, SC-005, AR-004.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f002d + f003a -> f004a`; full dependency graph is in docs/tasks.md.
- Prerequisites: f002d, f003a delivered within their stated acceptance limits.
- Approval gate: Observations/reporting. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f004-report-room-understanding.md, f004-status-room-understanding.md, and one f004 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/services/`.
- Allowed secondary folders/files: src/db scoped reads/observation query adapters; tests/integration/test_records.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Implement one scope resolver for location/property/room relationships. Build distinct property/room/asset counts, ticket counts, and system/state observation counts from the same snapshot. Do not multiply assets through joins.
2. Return room property context, exactly three assets/observations, and separate unresolved/resolved tickets with versions/generation. Use f003a for supporting finance, not a new calculation path.
3. Implement latest-observation Save/Clear through shared validators/coordinator. Recorded states including UNKNOWN require date/recorder; Clear removes all metadata. Preserve immutable baseline and create no observation history.
4. Define reusable unresolved ordering and explicit critical asset-link projection used later by maintenance. Use actual Hong Kong date, severity then overdue group then opening time. Room-only faults infer no asset flag.
5. Return honest zero/empty results and preserve independently prepared operations/evidence/history when reporting date changes. Cross-property access remains within fixed identities/import-only master data.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Independent scope/count cases exclude unrelated rooms consistently and never duplicate asset money with multiple invoices/tickets.
2. Healthy/recorded Unknown/unassessed Unknown, invalid metadata, Clear, cancellation/failure, restart, and baseline-repeat cases match mapped outcomes.
3. Observations and maintenance remain independent. Data reads change nothing; failed/stale observation commands roll back and expose no success.
4. Required scenario references: AC-US02-001, AC-US02-002, AC-US02-003, AC-US02-004, AC-US02-005, AC-US02-006, AC-US02-007, AC-US02-008, AC-US02-009, AC-US02-010, AC-US02-011, AC-US02-012, AC-US02-013, AC-US02-014, AC-US02-015, AC-US04-014, AC-US04-015, AC-US04-016, AC-INFRA-001. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/integration/test_records.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: No new browser rendering. f004b/f004c verify endpoint and B/M outcomes.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

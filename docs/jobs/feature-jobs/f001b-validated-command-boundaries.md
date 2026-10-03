---
description: Stable validated service contracts and one atomic command boundary for all later feature jobs.
---

# Objective
Stable validated service contracts and one atomic command boundary for all later feature jobs.

Scope status at authoring: PROPOSED, unexecuted. Current execution is recorded in the [f001 status](../feature-job-reports/f001-status-local-runtime.md). Trace: FR-003, FR-010, FR-012, FR-015, FR-016, FR-019, SC-002, SC-004, SC-008.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f001a -> f001b`; full dependency graph is in docs/tasks.md.
- Prerequisites: f001a delivered within their stated acceptance limits.
- Approval gate: Submit and receive approval for the scoped Persistence/reset, Imports, and Finance/display settings pseudocode before implementing each affected algorithm. P-03/P-04 were approved on 2026-10-03.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f001-report-local-runtime.md, f001-status-local-runtime.md, and one f001 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/services/`.
- Allowed secondary folders/files: tests/unit/test_import.py; tests/unit/test_display.py; tests/integration/test_records.py; src/db query adapters only.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Define Pydantic request/response shapes for existing technical-design.md section 5 endpoints. Reject extra fields and protected identity/cost/status fields. Preserve canonical enums, optional nulls, decimal strings, generation and expected versions. Implement no feature mutations yet.
2. Implement reusable text, identity-parent, date, decimal, positive-whole-month, observation metadata, and enum validators from data-contracts.md. Reject booleans, non-finite amounts, timed/ambiguous dates, numeric source IDs, malformed region/parent links, and incomplete assessment metadata.
3. Implement one caller-owned command coordinator: generation check, durable receipt lookup, operation/normalized-payload comparison, then version/prerequisite checks. Mutations, histories, resulting versions, and response receipt share one transaction.
4. Implement structured errors and status mapping for invalid input, missing records, stale store/record/preview, submission conflict, busy store, and save failure. Expose latest saved representations without discarding drafts at the service boundary.
5. Implement approved local owner/FX configuration and Hong Kong operational clock boundary. Freeze P-03 finance diagnostic shape before f004b endpoints. Hash canonical normalized command payloads deterministically and test equality without invented timestamps.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Identical committed retries replay their saved response before version checks, including after reopening the store. Changed operation/payload under the same submission ID conflicts.
2. Stale generation/version, failed write/history/receipt, and busy lock create no partial mutation. Boundary contracts serialize decimals as strings and reject unexpected fields.
3. Independent parser-value/config cases exercise shared validators. Full feature acceptance remains with downstream jobs; this foundation does not establish all scenario outcomes.
4. Required scenario references: AC-US01-006, AC-US01-007, AC-US02-010, AC-US05-009, AC-INFRA-001, AC-INFRA-002, AC-INFRA-008, AC-INFRA-009. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/unit/test_import.py tests/unit/test_display.py tests/integration/test_records.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: No visible UI changes. Browser error/retry presentation is verified by f001c and consuming feature UI jobs.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

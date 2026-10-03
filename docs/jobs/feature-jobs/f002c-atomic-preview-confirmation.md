---
description: Reviewed imports commit evidence, records, changes, histories, and receipts atomically.
---

# Objective
Reviewed imports commit evidence, records, changes, histories, and receipts atomically.

Scope status: PROPOSED, unexecuted. Trace: FR-001–FR-005, FR-015, FR-019, SC-001, SC-002, SC-004, AR-001, AR-002.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f002b + f001c -> f002c`; full dependency graph is in docs/tasks.md.
- Prerequisites: f002b, f001c delivered within their stated acceptance limits.
- Approval gate: Imports and approved Persistence/reset registry invalidation scope. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f002-report-reviewed-imports.md, f002-status-reviewed-imports.md, and one f002 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/services/`.
- Allowed secondary folders/files: src/db import write/read adapters; src/views thin import routes; tests/integration/test_import.py; tests/integration/test_runtime.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Create a thread-safe process preview registry with opaque UUIDs, thirty-minute TTL, at most twenty entries, normalized rows, generation, workflow, filename, and reviewed plan. Parse each workbook only once.
2. Implement existing preview/confirm endpoints. Confirmation accepts no replacement rows. Check generation then durable receipt before preview/version prerequisites. Re-read saved state inside BEGIN IMMEDIATE and run the same planner.
3. Return STALE_PREVIEW with renewed preview ID/summary when meaningful effects differ. Require renewed explicit confirmation. Reject expired/restarted/evicted previews and any blockers without domain writes.
4. Write all approved entity/evidence/update/override-history/reference/version changes and response receipt together. Preserve baselines, source coordinates, unchanged observations/tickets, and original provenance on skips.
5. Create upload records only for newly committed evidence/entities. Successful no-op confirmations return zero effects without upload/domain history, with a retry receipt only. Return actual counts after commit.
6. Connect generation-selective preview eviction to f001c reset. Test registry/confirmation/reset races, response-loss retry after expiry/restart, lock timeout, and failure between entity/history/receipt writes.
7. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
8. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Valid supplied files produce actual approved counts on independently prepared stores. Invalid files produce no domain/evidence/history changes.
2. Stale/expired previews require renewed review. A committed retry after process restart returns the receipt without replay; changed submission payload conflicts.
3. Half-written failure and busy lock preserve saved state and report no success. Reset invalidates old previews while preserving concurrently created new-generation previews.
4. Required scenario references: AC-US01-001, AC-US01-002, AC-US01-003, AC-US01-004, AC-US01-005, AC-US01-006, AC-US01-007, AC-US01-008, AC-US01-009, AC-US01-010, AC-US01-011, AC-US01-012, AC-US01-013, AC-US01-014, AC-US01-015, AC-US01-016, AC-US01-017, AC-US01-018, AC-US01-019, AC-US01-020, AC-US01-021, AC-US01-022, AC-US01-023, AC-US01-024, AC-US01-025, AC-INFRA-005, AC-INFRA-007, AC-INFRA-008. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/integration/test_import.py tests/integration/test_runtime.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: No finished upload page in this job. f002d executes mapped B/M review, retry, and cancellation methods.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

---
description: Existing assets accept permitted edits and accountable paired overrides while preserving evidence.
---

# Objective
Existing assets accept permitted edits and accountable paired overrides while preserving evidence.

Scope status: PROPOSED, unexecuted. Trace: FR-010, FR-015, FR-019, SC-003, SC-004, AR-002, AR-003.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f005c -> f006a`; full dependency graph is in docs/tasks.md.
- Prerequisites: f005c delivered within their stated acceptance limits.
- Approval gate: Assets/overrides. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f006-report-asset-accountability.md, f006-status-asset-accountability.md, and one f006 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/services/`.
- Allowed secondary folders/files: src/db asset/evidence/history query adapters; tests/integration/test_records.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Edit only operational name, purchase/installation dates, and useful life using shared validation/version/generation/receipt rules. Keep asset/room/category and calculated outputs fixed/read-only.
2. Set a complete non-negative cost/supported-currency pair with reason and typed recorder. Save immutable SET_OVERRIDE history, before/after/effective state, and actual timestamp atomically.
3. Reset with reason/recorder to latest applied invoice pair or baseline fallback. Clear active override and preserve RESET_TO_SOURCE history. Do not restore names/dates/observations.
4. Return preserved baseline, accepted invoice items/provenance, applied before/after history/references, and override history. Distinguish source, current operational, and effective values; historical-only items are not update events.
5. Verify composition with f002c: applied newer snapshots clear overrides with linked system history, while older/equivalent/repeat evidence preserves them. Keep ordinary source evidence immutable and normal restart durable.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. All US-03 I methods pass for fixed categories/fields, valid edits, incomplete pairs, reset sources, history, and display independence.
2. Invalid/cancelled/failed/stale commands preserve previous records/history/receipts; duplicate committed retries do not append another event.
3. Independent applied/older/equivalent/repeat invoice cases preserve approved before/after attribution and unchanged identities/observations/tickets.
4. Required scenario references: AC-US03-001, AC-US03-002, AC-US03-003, AC-US03-004, AC-US03-005, AC-US03-006, AC-US03-007, AC-US03-008, AC-US03-009, AC-US03-010, AC-US03-011, AC-US03-012, AC-US01-014, AC-US01-015, AC-US01-018, AC-INFRA-001, AC-INFRA-008. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/integration/test_records.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: No new visual editor. f006b/f006c own HTTP/browser verification.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

---
description: Thin asset endpoints enforce permitted fields and expose accountable evidence.
---

# Objective
Thin asset endpoints enforce permitted fields and expose accountable evidence.

Scope status: PROPOSED, unexecuted. Trace: FR-010, FR-015, FR-019, SC-003, SC-004, AR-002, AR-003.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: Medium

# Execution Order
- DAG: `f006a -> f006b`; full dependency graph is in docs/tasks.md.
- Prerequisites: f006a delivered within their stated acceptance limits.
- Approval gate: Assets/overrides. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f006-report-asset-accountability.md, f006-status-asset-accountability.md, and one f006 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/views/`.
- Allowed secondary folders/files: tests/integration/test_records.py; app.py route registration only.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Wire existing asset PATCH, override POST, reset-to-source POST, and evidence GET contracts to f006a services.
2. Reject protected fields and extra request keys. Keep financial override separate from operational edit. Preserve generation/version, decimal strings, attribution, structured errors, and no-store reads.
3. Verify HTTP edit/reset/override/evidence outcomes with independent on-disk state and the real command coordinator. Include lost-response retries after restart and stale-record responses.
4. Keep visual room/editor layout unchanged. Introduce no manual asset creation, identity/category move, evidence edit, or configuration edit endpoint.
5. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
6. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. All US-03 integration outcomes remain correct through real HTTP contracts, including untouched baselines/items/history.
2. Invalid/failed/stale commands report approved feedback with no state changes. Receipt replay returns the original result without added history.
3. Evidence is inspectable without a write or loss of historical-only items/provenance.
4. Required scenario references: AC-US03-001, AC-US03-002, AC-US03-003, AC-US03-004, AC-US03-005, AC-US03-006, AC-US03-007, AC-US03-008, AC-US03-009, AC-US03-010, AC-US03-011, AC-US03-012, AC-INFRA-001, AC-INFRA-008. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/integration/test_records.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Browser editing/evidence presentation belongs to f006c.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

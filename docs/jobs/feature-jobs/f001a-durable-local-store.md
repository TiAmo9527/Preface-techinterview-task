---
description: A reproducible local store that initializes safely, survives restart, and rolls back atomic writes.
---

# Objective
A reproducible local store that initializes safely, survives restart, and rolls back atomic writes.

Scope status at authoring: PROPOSED, unexecuted. Current execution is recorded in the [f001 status](../feature-job-reports/f001-status-local-runtime.md). Trace: FR-001, FR-015, SC-001, SC-004, SC-008, AR-002.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `PLAN/ADAPTATION APPROVAL -> f001a`; full dependency graph is in docs/tasks.md.
- Prerequisites: No implementation predecessor. Review the plan/adaptations first.
- Approval gate: Submit Persistence/reset pseudocode and wait for Alex's actual algorithm approval in docs/pseudocode-review.md. Plan, P-01/P-02, and S-01–S-03 were approved on 2026-10-03.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f001-report-local-runtime.md, f001-status-local-runtime.md, and one f001 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/db/`.
- Allowed secondary folders/files: app.py; requirements.lock; requirements-dev.lock; pyproject.toml; tests/integration/test_runtime.py; tests/conftest.py; README.md and docs/demo.md only for actual runtime instructions.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Implement the version-1 logical schema from technical-design.md section 2. Preserve text IDs, decimal strings, ISO dates, UTC instants, foreign keys, category uniqueness, paired overrides, immutable evidence, and history relationships.
2. Use one sqlite3 helper with foreign_keys=ON, five-second busy timeout, isolation_level=None, check_same_thread=True, and explicit BEGIN IMMEDIATE. Reads spanning multiple queries use a short snapshot transaction. Nested services share the connection.
3. Initialize through one migration transaction. Block unsupported newer schema versions. Preserve supported existing stores. Resolve production runtime/app.sqlite3 from the repository root, including launches from another directory.
4. Implement app.py --init-db and a test-only application/store seam under approved P-01. Pin and test the runtime/development dependencies from the technical design, including P-02 support when required. Keep serving/shell integration for f001c.
5. Establish independent on-disk test stores and clock/config fixtures in tests/conftest.py. Failure injection must roll back after an initial write. Automated tests never touch the demo store.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Clean Python 3.12.5 initialization creates an empty supported store. Alex approved this runtime substitution after feasibility checks on 2026-10-03. A second initialization preserves generation and independently prepared records.
2. Foreign-key/uniqueness/override constraints reject invalid state. Injected migration/write failure rolls back fully. A held write lock produces the approved timeout outcome.
3. Restart/reopen retains domain records, evidence, histories, versions, and receipts. Record actual environment/package versions. Browser startup acceptance waits for f001c.
4. Required scenario references: AC-DEMO-002, AC-DEMO-005, AC-INFRA-008. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification: Use the pinned .venv Python and pytest for tests/integration/test_runtime.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Browser checks are deferred to f001c because this job creates no rendered UI.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

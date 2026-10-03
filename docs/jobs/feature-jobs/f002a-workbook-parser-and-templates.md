---
description: Supported workbooks normalize into immutable rows with actionable source diagnostics.
---

# Objective
Supported workbooks normalize into immutable rows with actionable source diagnostics.

Scope status: PROPOSED, unexecuted. Trace: FR-001–FR-004, FR-009, FR-016, SC-001, SC-002, AR-001.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f001b -> f001c -> f002a`; full dependency graph is in docs/tasks.md.
- Prerequisites: f001c and its f001b contracts delivered within their stated acceptance limits. Serialize shared service edits with f001c.
- Approval gate: Imports. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f002-report-reviewed-imports.md, f002-status-reviewed-imports.md, and one f002 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/services/`.
- Allowed secondary folders/files: tests/unit/test_import.py; sample_data/spreadsheets blank Assets/Invoices templates only.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Read one required sheet with openpyxl data_only=False. Validate exact 26/12 header sets in any order, single sheet, format/readability, formulas, merges, and missing/duplicate/unexpected headers.
2. Normalize each row using f001b validators. Ignore fully empty rows, validate partial rows, preserve leading-zero text identities and all coordinates, and retain raw offending information for diagnostics.
3. Validate all three observation groups independently. Distinguish unassessed UNKNOWN from recorded UNKNOWN and enforce conditional date/recorder requirements. Do not infer Healthy or create history.
4. Produce immutable normalized rows and diagnostics. Create no database writes or saved raw workbook. Separate blockers from missing-installation, zero-cost, and missing-supplier warnings.
5. During later authorized execution only, create two headers-only blank templates using the approved schemas. Keep supplied workbooks byte-identical. Boundary variants are generated in temporary test paths.
6. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
7. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Saved blank templates have one required sheet, exact headers, and no source rows/formulas/merges. Supplied fixture hashes remain unchanged.
2. Independent structure/type/date/identity/assessment cases produce field/source coordinates. Equivalent decimal/date forms normalize equally and unsupported forms block.
3. Valid supplied files parse without missing-value/zero-cost warnings. Invalid files retain offending rows for review. Parser results establish no committed records.
4. Required scenario references: AC-US01-006, AC-US01-007, AC-US01-008, AC-US01-009, AC-US01-022, AC-US02-009, AC-US02-014. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/unit/test_import.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: No browser surface is added. f002d verifies these diagnostics through real upload endpoints.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

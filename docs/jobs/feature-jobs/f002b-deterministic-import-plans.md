---
description: One deterministic planner applies approved baseline identity and invoice precedence rules.
---

# Objective
One deterministic planner applies approved baseline identity and invoice precedence rules.

Scope status: PROPOSED, unexecuted. Trace: FR-001–FR-005, FR-015, FR-019, SC-001, SC-002, SC-004, AR-001, AR-002.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f002a -> f002b`; full dependency graph is in docs/tasks.md.
- Prerequisites: f002a delivered within their stated acceptance limits.
- Approval gate: Imports. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f002-report-reviewed-imports.md, f002-status-reviewed-imports.md, and one f002 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/services/`.
- Allowed secondary folders/files: src/db import snapshot read adapters; tests/unit/test_import.py; tests/integration/test_import.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Implement plan_import(normalized_rows, saved_state) without writes. Group repeated property/room values, retain contributing coordinates, enforce all three categories, exact parents, property-local room labels, occupied categories, and preserved baseline equality.
2. Skip identical existing asset/item identities using preserved source fields. Block changed identities and any upload duplicate, including identical rows. New rooms may join an unchanged existing property only as complete category sets.
3. Resolve every invoice room/category target. Validate historical rows too. Across stored/incoming evidence, find maximum invoice_date and compare all normalized six-field snapshots there.
4. Block different controlling snapshots. Retain equivalent distinct item identities deterministically. Apply first controlling invoice regardless of baseline purchase date; thereafter apply only a strictly newer date, even for equivalent values.
5. Plan all six-field replacement and blank-installation clearing, source-pair changes, override clearing with linked system history, evidence/references, versions, and before/after values. Older/equal historical-only items and repeats preserve edits/overrides.
6. Return entity inserts, new evidence items, distinct asset updates, historical-only items, skips, warnings/blockers, and all reviewed effects. Exclude generated IDs/commit times from deterministic equality. Include before-values and override effects.
7. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
8. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Independent cases cover baseline disagreement/category/identity blockers and invoice order, ties, older differences, subsets, first/newer equal snapshots, and repeats after edits.
2. The same normalized input/state gives equivalent plans regardless of upload row order. Different meaningful saved state changes the reviewed plan.
3. Blocked plans have no writable effects. Valid supplied baseline predicts 4 properties/12 rooms/36 assets; invoices predict 36 items/36 distinct updates.
4. Required scenario references: AC-US01-001, AC-US01-002, AC-US01-003, AC-US01-004, AC-US01-005, AC-US01-006, AC-US01-007, AC-US01-008, AC-US01-009, AC-US01-010, AC-US01-011, AC-US01-012, AC-US01-013, AC-US01-014, AC-US01-015, AC-US01-016, AC-US01-017, AC-US01-018, AC-US01-019, AC-US01-020, AC-US01-021, AC-US01-022, AC-US01-023, AC-US01-024, AC-US01-025. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/unit/test_import.py tests/integration/test_import.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: No new UI. f002c/f002d must verify actual commits and browser review; planner assertions alone do not pass B methods.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

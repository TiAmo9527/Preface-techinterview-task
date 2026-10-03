---
description: The local web shell starts reproducibly and can confirm a safe empty-store reset.
---

# Objective
The local web shell starts reproducibly and can confirm a safe empty-store reset.

Scope status: PROPOSED, unexecuted. Trace: FR-015, FR-017, FR-018, UX-001, UX-013, UX-015–UX-019, SC-004, SC-008, AR-002.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f001b -> f001c`; full dependency graph is in docs/tasks.md.
- Prerequisites: f001b delivered within their stated acceptance limits.
- Approval gate: Persistence/reset and scoped Finance/display settings browser-state approval. Submit applicable pseudocode and wait for Alex's actual approval in docs/pseudocode-review.md.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f001-report-local-runtime.md, f001-status-local-runtime.md, and one f001 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `src/views/`.
- Allowed secondary folders/files: app.py serving integration; src/services reset/config operations; src/db reset queries; tests/integration/test_runtime.py; tests/browser/test_runtime.py; tests/browser/test_ui.py; tests/conftest.py.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Export the FastAPI app and serve local assets through one Uvicorn worker on 127.0.0.1:8000, without reload. Implement GET /api/config and POST /api/reset with existing contracts. Add no external runtime integration.
2. Create one browser state module and one request helper. Use hash navigation for Overview, Maintenance, Import, and Debugging - Assumptions. Own drafts, request sequences, loaded versions/generation, and dirty-form Continue editing/Discard behavior here.
3. Store independent language/currency preferences in localStorage. Store tab navigation/filter/search/representation/selection/reporting context in sessionStorage. Initialize new sessions from server Hong Kong today. Preserve reload dates and guard new-tab context cloning.
4. Create mandatory English dictionary/fallback, approved shared layout/controls/feedback, and read-only assumptions shell. Establish 16px type, 8px rhythm, palette, semantic labels, responsive card/overlay/focus primitives, with no prohibited effects.
5. Reset with confirm=true and current generation through the shared write helper. Delete in approved FK order, change generation atomically, retain schema/configuration/file/preferences, and evict only old-generation previews through a registry hook consumed by f002c.
6. After reset, open empty Overview and today's reporting context. Reject old drafts on focus/request and before writes. Preserve invalid other-tab drafts until discard. No repeated old-generation reset can delete a newly imported portfolio.
7. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
8. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. python app.py serves a working empty shell in installed Windows Chrome. --init-db remains non-destructive. Record actual Python/package/Windows/Chrome/build versions.
2. Cancel and injected halfway reset failure preserve all rows and generation. Confirmed reset clears prepared domain state atomically and preserves preferences/configuration.
3. Two-tab stale drafts, lost reset responses, dirty navigation, late reads, keyboard/focus, and width/breakpoint checks match mapped cases. Full preview-reset race is repeated when f002c exists.
4. Required scenario references: AC-DEMO-001, AC-DEMO-002, AC-DEMO-005, AC-INFRA-003, AC-INFRA-004, AC-INFRA-005, AC-INFRA-006, AC-US02-016, AC-US02-017, AC-US02-019, AC-UX-001, AC-UX-013, AC-UX-015, AC-UX-016, AC-UX-017, AC-UX-019. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/integration/test_runtime.py tests/browser/test_runtime.py tests/browser/test_ui.py. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Run mapped B/M methods and IX-UX-001/013/015/016/017/019 in Windows installed Chrome for the implemented shell/reset surfaces.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

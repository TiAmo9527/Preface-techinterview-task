---
description: Required scenarios and interactions have truthful evidence on one integrated build.
---

# Objective
Required scenarios and interactions have truthful evidence on one integrated build.

Scope status: PROPOSED, unexecuted. Trace: SC-001–SC-005, SC-007, SC-008, AR-001–AR-005, AR-007, UX-001–UX-019; all 118 scenarios and nineteen IX companions are required here.
Read [task order/coverage](../../tasks.md), [planning adaptations](../../implementation-planning-review.md), and applicable AGENTS.md files.
Use [product](../../product-spec.md), [design](../../technical-design.md), [contracts](../../data-contracts.md), and [UI requirements](../../ui-ux-spec.md).
[Acceptance](../../acceptance-scenarios.md) and [verification](../../verification-plan.md) govern outcomes and methods.

# Recommended Reasoning Effort
- GPT-6.1 Sol reasoning effort: High

# Execution Order
- DAG: `f003c -> f007a`; full dependency graph is in docs/tasks.md.
- Prerequisites: f003c delivered within their stated acceptance limits.
- Approval gate: All affected behavior groups must already have recorded approval. Verification adds no application behavior or new pseudocode gate.
- Parallelization: Serialized on the default delivery path. Primary-folder, query-adapter, route-registration, shared test-file, and reporting hotspots prevent concurrent feature edits. Optional disjoint foundations are defined only in docs/tasks.md.
- Execution tracking: execution skill later maintains docs/jobs/feature-job-reports/f007-report-demo-readiness.md, f007-status-demo-readiness.md, and one f007 row in feature-job-reports/job-status.md. No artifacts are created during authoring.

# Folder Ownership
- Primary folder: `tests/`.
- Allowed secondary folders/files: docs/demo.md; README.md; docs/assessment-requirements.md evidence references only; docs/ui-ux-spec.md evidence references only.
- Modify only this job's named behavior surfaces within those folders. Secondary access is serialized, not blanket ownership of adjacent domains.

# Required
1. Inventory all 118 scenarios and nineteen IX companions from verification-plan.md. Run every applicable U/I/B/M method with independent setup and declared build/environment. Conditional omissions apply only to undelivered stretch translations.
2. Run the complete unit/integration/browser commands from demo.md on isolated production-helper stores. Repeat cross-feature reset/preview/stale/receipt/late-read/atomic-history cases on the integrated build.
3. Review Windows installed Chrome manually at 1440/1024/768/360 and both sides of 1200/600 breakpoints. Exercise keyboard/assistive-technology feedback, long errors, overlays, dirty forms, and every shared feedback state.
4. Record startup from clean Python 3.11, missing/supported/unsupported store, working-directory independence, normal restart, session/preferences, and confirmed/cancelled/failed/two-tab reset.
5. Keep actual evidence under runtime/verification/<build>/<scenario-or-check-id>. Link assessed results from series reporting and governing evidence ledgers without duplicate execution status tables.
6. Report any defect under its owning feature job or a later writing-skill bugfix specification. This verification job cannot widen scope into production fixes. Re-run only affected regressions after fixes.
7. Add or update the named mapped tests while implementing behavior. Use independent setups and actual production helpers. Read [fixture scope](../../sample-data-plan.md) and [runtime procedures](../../demo.md) where applicable.
8. Report actual checks and remaining limitations through the execution skill's consolidated series artifacts. Link local scenario evidence; do not turn docs/tasks.md into a status ledger.

# Must Not Touch
- Out-of-scope src/db, src/services, src/views, tests, root configuration, and documentation surfaces beyond Folder Ownership.
- sample/2026-10-03 workbook bytes, source identities, and inspection sidecars. Preserve fictional-only and local-only delivery.
- Settled product/input/UX/schema policies, AR-002 disclosure, other jobs' behavior, or external sharing/deployment.
- Global state/request/configuration/transaction rules beyond explicitly allowed integration. Consequential deviations require renewed approval.
- Per-subjob reports or planning-time execution report/status/master files. Execution artifacts are owned by the execution skill.

# Acceptance Criteria
1. Every applicable scenario/method and IX subcase has PASS/FAIL/NOT RUN with actual expected/observed values, independent setup, build/date, and environment references.
2. Chromium and installed-Chrome evidence are distinct. Application readiness is claimed only when required checks pass; failures/omissions remain visible.
3. Supplied fixture hashes and fictional/confidential boundaries remain intact. No runtime store/evidence or assessment PDF is committed/published.
4. Required scenario references: AC-UX-015, AC-UX-016, AC-UX-017, AC-UX-018, AC-DEMO-001, AC-DEMO-002, AC-DEMO-005, AC-INFRA-001, AC-INFRA-002, AC-INFRA-003, AC-INFRA-004, AC-INFRA-005, AC-INFRA-006, AC-INFRA-007, AC-INFRA-008, AC-INFRA-009. Run the corresponding methods from verification-plan.md for the implemented surface. Downstream deferred methods remain NOT RUN until their named job executes.
5. Automated verification (planned, not yet available): Use the pinned .venv Python and pytest for tests/unit tests/integration tests/browser. Run browser files with --browser chromium when applicable. Use targeted compileall for changed Python surfaces after S-03 approval.
6. Browser/manual verification: Run every mapped M method and IX companion in Windows installed Chrome. Evidence completeness is an audit obligation, not a passing claim.
7. Record build/date, method, independent setup, expected/actual outcome, status, and environment. State lint/typecheck/tests/count results or their approved S-03 absence. Passing fixture/document checks do not establish application acceptance.

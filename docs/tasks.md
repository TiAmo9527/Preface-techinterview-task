# Implementation work-plan index

Version: 0.6. Revised: 2026-10-03. Target delivery: 2026-10-05.
Status: APPROVED dependency plan. Alex approved the plan and adaptations on 2026-10-03. Execution progress is owned by the [series status artifacts](jobs/feature-job-reports/job-status.md).

This is the sole index for planned order, dependencies, and requirement coverage.
[Delivery approach](plan.md) defines context. [Planning review](implementation-planning-review.md) records readiness and proposals.
Governing specifications retain authority. Job scope and plan approval never bypass [pseudocode approval](pseudocode-review.md).

## Delivery priorities and gates

The current app prints a title. All six behavior groups have NOT SUBMITTED pseudocode.
Required English, local startup, reviewed imports, room understanding, and accountable maintenance take priority.
Asset edits/overrides and financial/replacement reports remain required. Their later position is sequencing, not deferral.
Keep a final verification/rehearsal session. Translations, optional date presets, regeneration, and publication are outside the critical path.
If time expires, disclose required omissions. Do not reduce policies or mark unverified work complete.

Before f001a: present Persistence/reset pseudocode and wait for explicit algorithm approval.
The plan and P-01–P-05/S-01–S-03 adaptations were approved by Alex on 2026-10-03.
f001b also needs scoped Imports and Finance/display settings reviews for shared validators/configuration.
f001c needs the browser-state/display scope approved. Later jobs require their full affected algorithm scopes.
Record each algorithm approval's actual response, scope, date, and document versions in pseudocode-review.md.

## Dependency graph and ownership

Required DAG:

```text
f001a -> f001b -> f001c -> f002a -> f002b -> f002c -> [f002d, f003a] -> f004a -> f004b -> f004c -> f005a -> f005b -> f005c -> f006a -> f006b -> f006c -> f003b -> f003c -> f007a -> f007b
```

Default delivery order follows the rows below. f003a may follow f002d when only one agent executes.
Parallelization: Only f002d and f003a may run concurrently after f002c and their approval gates.
They own disjoint src/views versus src/services surfaces, browser versus unit tests, and different series artifacts.
Neither may edit shared conftest, root files, or the other's surface during that parallel window.
All other jobs serialize because of folder ownership, query adapters, route registration, shared state/CSS, or shared test files.
Parallel eligibility is not a request to spawn agents during this planning pass.

No artificial shared/server/ui folders are introduced.
The contract-first sequence is f001b -> services -> thin endpoints -> visible UI -> integrated evidence.
Tests accompany each behavior job. f007 audits integrated coverage instead of postponing all testing.

| Job | End-to-end contribution / detailed specification | Exact implementation prerequisites | Primary ownership |
|---|---|---|---|
| f001a | [durable local store](jobs/feature-jobs/f001a-durable-local-store.md) | Plan/adaptation review and pseudocode gate | src/db/ |
| f001b | [validated command boundaries](jobs/feature-jobs/f001b-validated-command-boundaries.md) | f001a | src/services/ |
| f001c | [browser shell and reset](jobs/feature-jobs/f001c-browser-shell-and-reset.md) | f001b | src/views/ |
| f002a | [workbook parser and templates](jobs/feature-jobs/f002a-workbook-parser-and-templates.md) | f001c (and its f001b contract prerequisite) | src/services/ |
| f002b | [deterministic import plans](jobs/feature-jobs/f002b-deterministic-import-plans.md) | f002a | src/services/ |
| f002c | [atomic preview confirmation](jobs/feature-jobs/f002c-atomic-preview-confirmation.md) | f002b, f001c | src/services/ |
| f002d | [reviewed import browser flow](jobs/feature-jobs/f002d-reviewed-import-browser-flow.md) | f002c | src/views/ |
| f003a | [calendar and money calculations](jobs/feature-jobs/f003a-calendar-and-money-calculations.md) | f002c | src/services/ |
| f004a | [room scope and observations](jobs/feature-jobs/f004a-room-scope-and-observations.md) | f002d, f003a | src/services/ |
| f004b | [room api wiring](jobs/feature-jobs/f004b-room-api-wiring.md) | f004a | src/views/ |
| f004c | [overview room and assessment](jobs/feature-jobs/f004c-overview-room-and-assessment.md) | f004b | src/views/ |
| f005a | [accountable ticket service](jobs/feature-jobs/f005a-accountable-ticket-service.md) | f004c | src/services/ |
| f005b | [maintenance api wiring](jobs/feature-jobs/f005b-maintenance-api-wiring.md) | f005a | src/views/ |
| f005c | [maintenance cards and handoff](jobs/feature-jobs/f005c-maintenance-cards-and-handoff.md) | f005b | src/views/ |
| f006a | [asset edits overrides and evidence](jobs/feature-jobs/f006a-asset-edits-overrides-and-evidence.md) | f005c | src/services/ |
| f006b | [asset api wiring](jobs/feature-jobs/f006b-asset-api-wiring.md) | f006a | src/views/ |
| f006c | [asset edit and evidence cards](jobs/feature-jobs/f006c-asset-edit-and-evidence-cards.md) | f006b | src/views/ |
| f003b | [financial integration regressions](jobs/feature-jobs/f003b-financial-integration-regressions.md) | f003a, f004c, f005c, f006c | tests/ |
| f003c | [financial display and assumptions](jobs/feature-jobs/f003c-financial-display-and-assumptions.md) | f003b | src/views/ |
| f007a | [integrated readiness verification](jobs/feature-jobs/f007a-integrated-readiness-verification.md) | f003c | tests/ |
| f007b | [timed demo handoff](jobs/feature-jobs/f007b-timed-demo-handoff.md) | f007a | docs/ |

The tables describe planned dependencies, not actual progress.
Feature series contain three or four jobs, except the two-job final handoff.
No bugfix series is invented before an actual defect is found.

## Requirement and scenario coverage

Ranges include every existing ID between endpoints. Verification-plan.md retains each scenario's exact methods and evidence groups.
Jobs inherit mapped U/I/B/M obligations for their implemented surfaces. Deferred methods remain NOT RUN until the named downstream job.
f007a audits every applicable method for all 118 scenarios and all nineteen IX companions.

| Requirements / scenarios | Implementing jobs | Evidence obligation |
|---|---|---|
| FR-001–FR-005, FR-015, FR-019; SC-001/002; AR-001/002; AC-US01-001–025 | f001a/b infrastructure; f002a–d | E-IMPORT. Parser/planner, actual atomic commit, and browser review are separate evidence. |
| FR-006–FR-009, FR-016; SC-004/005; AR-004; AC-US02-001–015 | f004a–c, f002 for baseline/repeats | E-ROOM/E-UI. Shared scope, distinct counts, card context, metadata, independence, failure/restart. |
| FR-011, FR-017/018; SC-003/008; AC-US02-016–019 | f001b/c, f003a–c | E-ROOM/E-UI/E-FINANCE. English, conditional fallback, separate preferences/dates, grouped local/USD. |
| FR-010/019; SC-003/004; AR-002/003; AC-US03-001–012 | f006a–c, f002c invoice composition, f003 calculations | E-ASSET/E-FINANCE. Fixed records, edits, overrides/source reset, preserved evidence/history, AR-002 gap. |
| FR-012/013; SC-004/005; AR-005; AC-US04-001–016 | f005a–c, f004a scoped ordering/flags | E-MAINT. Recorder versus owner, same-room links, forward progression, chronology, resolved immutability. |
| FR-011/014/018/019; SC-003/008; AR-003; AC-US05-001–013 | f003a–c, f004 scoped composition | E-FINANCE. Calendar/Decimal boundaries, complete FX, unique assets, independent flags/horizons. |
| UX-001/013/015/016/017; AC-UX-001/013/015/016/017 and matching IX | f001c foundations, consuming views, f007a full review | E-UI. Shell/state, dirty forms, feedback, styling, responsive/keyboard/assistive checks. |
| UX-002–005/009; AC-UX-002–005/009 and matching IX | f004c; f005c completes Log fault return | E-ROOM/E-UI. Search stays view-only, equivalent representations, complete return context. |
| UX-006/012; AC-UX-006/012 and matching IX | f005c | E-MAINT/E-UI. Cards, both entries, cancellation, prerequisites, history. |
| UX-007/008; AC-UX-007/008 and matching IX | f002d | E-IMPORT/E-UI. File/workflow invalidation, stale renewed review, pending/retry presentation. |
| UX-010/011; AC-UX-010/011 and matching IX | f006c | E-ASSET/E-UI. Inline editors/evidence, reset source and unchanged operational fields. |
| UX-014/019; AC-UX-014/019 and matching IX | f003c, f001c reset/config foundation | E-FINANCE/E-UI. Actual assumptions/configuration and independent display/date controls. |
| UX-018; AC-UX-018; IX-UX-018 | f005c/f006c/f003c integration; f007a/b | E-STARTUP/E-UI. Full journey refresh, context, restart, and truthful readiness. |
| FR-015; AC-INFRA-001 | f001b, f006b/c, f005b/c | Stale-record I/B evidence for assets and tickets; explicit Review latest. |
| FR-012/015; AC-INFRA-002/009 | f005a–c | Durable duplicate-create replay, changed-payload conflict, typed recorder on all manual actions. |
| FR-008/009; AC-INFRA-003 | f001c request primitive; f004c actual room reads | Reverse response-order B evidence. |
| FR-015/018; AC-INFRA-004–006 | f001a/c, f002c/d, f007a | Reset cancel/rollback, other tabs, old reset retry preserving newly imported records. |
| FR-003/005/015; AC-INFRA-007 | f002c/d | Expiry/eviction/restart and committed retry after preview loss. |
| FR-015/019; AC-INFRA-008 | f001a/b, f002c/d, f005a–c, f006a–c | Busy lock and half-written entity/history/receipt rollback, including retained UI input. |
| SC-006/007; AR-006; AC-DEMO-001–005 | f001 runtime foundation, f007a/b | E-STARTUP/E-DEMO. Clean startup, reset/restart/session, explicit dates, measured <=12-minute walkthrough. |
| AR-007/008 | f007a/b | E-CONFIDENTIAL. Fictional/internal-only review. Sharing is optional and separately authorized. |
| CL-01–CL-28 | Governing product checklist and all jobs above | Preserve documentation coverage. Checklist completion never substitutes for application evidence. |

FR-001–FR-019, SC-001–SC-008, AR-001–AR-008, US-01–US-05, UX-001–UX-019, and CL-01–CL-28 remain unchanged.
AR-002 manual creation remains unmet; its maintenance reinterpretation remains unconfirmed by the assessor.

## Designated execution tracking

These filenames are planned references, deliberately absent until execution begins.
Execution reads job-specification-execution and later creates/maintains exactly one report/status pair per series.
The feature master is `docs/jobs/feature-job-reports/job-status.md`, with one series row, never per-subjob summaries.
The bugfix master is `docs/jobs/bugfix-job-reports/job-status.md` only if later bugfix execution needs it.
The writing skill creates none of these artifacts. Progress belongs to series status files, not this index.

| Series outcome | Planned report file under docs/jobs/feature-job-reports/ | Planned status file under the same folder |
|---|---|---|
| f001: local runtime | f001-report-local-runtime.md | f001-status-local-runtime.md |
| f002: reviewed imports | f002-report-reviewed-imports.md | f002-status-reviewed-imports.md |
| f003: financial reporting | f003-report-financial-reporting.md | f003-status-financial-reporting.md |
| f004: room understanding | f004-report-room-understanding.md | f004-status-room-understanding.md |
| f005: accountable maintenance | f005-report-accountable-maintenance.md | f005-status-accountable-maintenance.md |
| f006: asset accountability | f006-report-asset-accountability.md | f006-status-asset-accountability.md |
| f007: demo readiness | f007-report-demo-readiness.md | f007-status-demo-readiness.md |

## Completed documentation history

The v0.5 completed-documentation checklist follows unchanged.
Its evidence is in [the historical specification review](spec-review.md).
The bounded dependency plan above supersedes the old unsequenced implementation inventory.

- [x] Preserve stable product and assessment identifiers and the explicit AR-002 gap.
- [x] Document independent Assets/Invoices workflows and preserved source/history boundaries.
- [x] Preserve the combined valid/invalid sample instructions without generating files.
- [x] Preserve UI choices and record approval of the existing proposals.
- [x] Name the room manager and the primary maintenance decision.
- [x] Document starts, entry points, priorities, actions, outcomes, and independent journey setups.
- [x] Preserve 109 linked scenarios and add nine infrastructure scenarios with requirement and evidence references.
- [x] Define shared domain terms and required/optional entity information.
- [x] Record current owner confirmation dated 2026-10-03 without proving older dates.
- [x] Define Windows-laptop Chrome context and actual-version evidence.
- [x] Define shared-store reset, retained preferences, stale drafts, and normal restart behavior.
- [x] Add the 28-item product checklist with defining sections and acceptance references.
- [x] Apply the supplied controlled-English writing guidance and record documentation checks.
- [x] Approve exact input contracts and local technical design.
- [x] Define governing documents, pseudocode approvals, and verification mapping.
- [x] Inventory the existing dated fixtures without altering workbooks.

## Original unsequenced inventory retained for traceability

These v0.5 bullets preserve scope/history. They are not independently maintained execution status.
Each behavior is assigned above. Actual progress is read from the designated series status files.

### Implementation and fixtures inventory

- Implement approved technical details within the presentation/business/persistence boundaries.
- Implement and verify the approved clean-startup and reset procedures.
- Create two blank templates. Validate the supplied valid/invalid fixture basis and its inventory.
- Verify saved samples and separate boundary fixtures.
- Implement independent import preview, diagnostics, explicit confirmation, and atomic writes.
- Implement identities, category completeness, baseline equality, provenance, and invoice targets.
- Implement invoice precedence, controlling-date conflicts, equivalent ties, historical-only items, and skips.
- Implement asset editing, invoice updates, override clearing, paired overrides, source reset, and history.
- Implement observations with metadata and Clear to Unknown.
- Implement maintenance owners, transitions, history, fixed links, and resolved immutability.
- Implement filters, counts, room links, empty results, and unique-asset totals.
- Implement Overview, Maintenance, Import, and Debugging - Assumptions.
- Implement Map/List, right-side cards, inline editors, and Log fault navigation.
- Implement confirmed styling, keyboard access, accessible feedback, and responsive widths.
- Implement financial rules, complete fixed FX, dates, and replacement proxies.
- Implement mandatory English and independent persistent language/currency choices.
- Implement confirmed shared-store reset with preserved preferences and invalidated drafts/previews.
- Deliver stretch translation sets if feasible with English fallback.

### Verification and assessment inventory

- Record E-IMPORT for required import scenarios.
- Record E-ROOM for filters, observations, room context, and independent faults.
- Record E-ASSET for permitted edits, overrides, source evidence, histories, and the AR-002 gap.
- Record E-MAINT for valid progression, ownership, rejected actions, and history.
- Record E-FINANCE for numerical examples, boundaries, complete FX, and spending proxies.
- Record E-UI for confirmed interface checks, preferences, languages, keyboard access, and responsive behavior.
- Record actual Windows and Chrome versions with each applicable build/date.
- Resolve translation review with Alex and disclose unreviewed sets.
- Record E-STARTUP for clean web startup, normal restart, and shared-store reset behavior.
- Record E-DEMO for a timed rehearsal and required disclosures.
- Review fictional data, confidentiality, and unmet requirements.
- Prepare controlled sharing only after a separate owner decision.

All application evidence remains NOT RUN. Supplied fixture structure has prior inspected evidence only.
This planning revision creates specifications and instructions. It implements no application behavior or generated fixtures.

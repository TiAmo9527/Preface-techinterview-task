# Verification plan and scenario mapping

Version: 1.0

Approved: 2026-10-03. Status: Verification design ready. All application checks NOT RUN.

Use [acceptance scenarios](acceptance-scenarios.md), [UI requirements](ui-ux-spec.md), and [technical design](technical-design.md).
The required ledger fields are in [assessment evidence](assessment-requirements.md#5-evidence-ledger).

## 1. Methods and independent setups

| Code | Method | Future implementation location and setup |
|---|---|---|
| U | pytest unit cases | tests/unit/test_import.py, test_finance.py, test_maintenance.py, or test_display.py. Use independently prepared values/clock. |
| I | pytest service/database/API integration | tests/integration/test_import.py, test_records.py, or test_runtime.py. Use a temporary on-disk SQLite store with production helpers. |
| B | Playwright Chromium browser cases | tests/browser/test_journeys.py, test_ui.py, or test_runtime.py. Start one isolated local server per test context. |
| M | Manual Windows/installed-Chrome check | Required widths, actual versions, keyboard/focus, layout, language review, or timed rehearsal as applicable. |

Use test_<scenario_id_lowercase_with_underscores> as each automated scenario's entry name.
Case tables use parameterized cases named by input/boundary. One scenario can require multiple methods and cases.
Do not reuse another scenario execution as setup. Seed independent state through fixture helpers or the service boundary.
Test helpers exercise real transaction helpers. Use temporary files, not a shared :memory: connection with different thread behavior.
Use the supplied valid/invalid workbooks for demonstration-import coverage. Generate separate boundary data only in isolated tests.
Use explicit clocks for finance and transition assertions. Record actual time only in manual presentation evidence.
Failure checks inject a failure after an initial write and before history/receipt completion.
Inspect domain rows, histories, receipts, and generation before/after. Check every unchanged-state obligation.
Application restart checks close/reopen actual connections and restart the local process for browser checks.
Browser tests intercept delayed responses to verify request-order safeguards.

The table below assigns every scenario to methods and its evidence groups.
US-01/02/03/04 use their source-defined Given setup. US-05 uses explicit dates/amounts/configuration.
UX cases use prepared page states. DEMO cases use independent runtime setups. INFRA cases use their stated races/failures.
Manual evidence is required for installed Chrome even when Chromium automation passes.

## 2. Scenario-to-check matrix

All rows are NOT RUN. U/I/B/M identify planned checks, not existing tests.

| Scenario and expected behavior | Methods | Evidence groups |
|---|---|---|
| [AC-US01-001: Baseline without invoices](acceptance-scenarios.md#ac-us01-001) | U, I, B | E-IMPORT |
| [AC-US01-002: Independent invoice subset](acceptance-scenarios.md#ac-us01-002) | U, I, B | E-IMPORT |
| [AC-US01-003: Unknown or ambiguous targets](acceptance-scenarios.md#ac-us01-003) | U, I | E-IMPORT |
| [AC-US01-004: Baseline integrity blockers](acceptance-scenarios.md#ac-us01-004) | U, I | E-IMPORT |
| [AC-US01-005: Occupied category and changed baselines](acceptance-scenarios.md#ac-us01-005) | U, I | E-IMPORT |
| [AC-US01-006: Invalid row values](acceptance-scenarios.md#ac-us01-006) | U, I | E-IMPORT |
| [AC-US01-007: File and header failures](acceptance-scenarios.md#ac-us01-007) | U, I | E-IMPORT |
| [AC-US01-008: Warning-only success](acceptance-scenarios.md#ac-us01-008) | U, I, B | E-IMPORT |
| [AC-US01-009: Preview and diagnostics](acceptance-scenarios.md#ac-us01-009) | U, I | E-IMPORT |
| [AC-US01-010: Newest date independent of order](acceptance-scenarios.md#ac-us01-010) | U, I | E-IMPORT |
| [AC-US01-011: Historical-only older items](acceptance-scenarios.md#ac-us01-011) | U, I | E-IMPORT |
| [AC-US01-012: Controlling-date conflict](acceptance-scenarios.md#ac-us01-012) | U, I | E-IMPORT |
| [AC-US01-013: Equivalent controlling-date evidence](acceptance-scenarios.md#ac-us01-013) | U, I | E-IMPORT |
| [AC-US01-014: Identical baseline repeat after edits](acceptance-scenarios.md#ac-us01-014) | U, I | E-IMPORT |
| [AC-US01-015: Identical invoice repeat after edits](acceptance-scenarios.md#ac-us01-015) | U, I | E-IMPORT |
| [AC-US01-016: Changed source identity](acceptance-scenarios.md#ac-us01-016) | U, I | E-IMPORT |
| [AC-US01-017: Duplicate identity inside upload](acceptance-scenarios.md#ac-us01-017) | U, I | E-IMPORT |
| [AC-US01-018: Applied invoice replaces edits](acceptance-scenarios.md#ac-us01-018) | U, I | E-IMPORT |
| [AC-US01-019: Blank installation clears previous date](acceptance-scenarios.md#ac-us01-019) | U, I, B | E-IMPORT |
| [AC-US01-020: Commit failure rolls back all effects](acceptance-scenarios.md#ac-us01-020) | U, I, B | E-IMPORT |
| [AC-US01-021: Changed stale preview](acceptance-scenarios.md#ac-us01-021) | U, I, B | E-IMPORT |
| [AC-US01-022: Cancellation and no-op inputs](acceptance-scenarios.md#ac-us01-022) | U, I, B | E-IMPORT |
| [AC-US01-023: First invoice and equal-value newer invoice](acceptance-scenarios.md#ac-us01-023) | U, I | E-IMPORT |
| [AC-US01-024: Different older snapshots](acceptance-scenarios.md#ac-us01-024) | U, I | E-IMPORT |
| [AC-US01-025: Provenance and new rooms](acceptance-scenarios.md#ac-us01-025) | U, I | E-IMPORT |
| [AC-US02-001: Consistent reporting scope](acceptance-scenarios.md#ac-us02-001) | I, B | E-ROOM, E-UI |
| [AC-US02-002: Incompatible child filters](acceptance-scenarios.md#ac-us02-002) | I, B | E-ROOM, E-UI |
| [AC-US02-003: Empty results](acceptance-scenarios.md#ac-us02-003) | I, B | E-ROOM, E-UI |
| [AC-US02-004: Operational ordering and count units](acceptance-scenarios.md#ac-us02-004) | I, B | E-ROOM, E-UI |
| [AC-US02-005: Room context through every link](acceptance-scenarios.md#ac-us02-005) | I, B | E-ROOM, E-UI |
| [AC-US02-006: No financial duplication](acceptance-scenarios.md#ac-us02-006) | I, B | E-ROOM, E-UI |
| [AC-US02-007: Cross-property access and edit boundary](acceptance-scenarios.md#ac-us02-007) | I, B | E-ROOM, E-UI |
| [AC-US02-008: Reporting date does not change operations](acceptance-scenarios.md#ac-us02-008) | I, B | E-ROOM, E-UI |
| [AC-US02-009: Unknown does not mean Healthy](acceptance-scenarios.md#ac-us02-009) | I, B | E-ROOM, E-UI |
| [AC-US02-010: Recorded assessment metadata](acceptance-scenarios.md#ac-us02-010) | I, B | E-ROOM, E-UI |
| [AC-US02-011: Record Healthy](acceptance-scenarios.md#ac-us02-011) | I, B | E-ROOM, E-UI |
| [AC-US02-012: Clear assessment](acceptance-scenarios.md#ac-us02-012) | I, B | E-ROOM, E-UI |
| [AC-US02-013: Observations and tickets are independent](acceptance-scenarios.md#ac-us02-013) | I, B | E-ROOM, E-UI |
| [AC-US02-014: Invalid imported assessment and baseline repeat](acceptance-scenarios.md#ac-us02-014) | I, B | E-ROOM, E-UI |
| [AC-US02-015: Observation cancellation and failure](acceptance-scenarios.md#ac-us02-015) | I, B | E-ROOM, E-UI |
| [AC-US02-016: Defaults and persistent independent preferences](acceptance-scenarios.md#ac-us02-016) | I, B, M | E-ROOM, E-UI |
| [AC-US02-017: English and conditional translations](acceptance-scenarios.md#ac-us02-017) | I, B, M | E-ROOM, E-UI |
| [AC-US02-018: Local and USD display](acceptance-scenarios.md#ac-us02-018) | I, B, M | E-ROOM, E-UI |
| [AC-US02-019: Session financial date](acceptance-scenarios.md#ac-us02-019) | I, B, M | E-ROOM, E-UI |
| [AC-US03-001: Three fixed category records](acceptance-scenarios.md#ac-us03-001) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-002: Permitted fields and read-only results](acceptance-scenarios.md#ac-us03-002) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-003: Invalid, cancelled, and failed edits](acceptance-scenarios.md#ac-us03-003) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-004: Saved edits and normal restart](acceptance-scenarios.md#ac-us03-004) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-005: Inspect source and histories](acceptance-scenarios.md#ac-us03-005) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-006: Set paired financial override](acceptance-scenarios.md#ac-us03-006) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-007: Reject incomplete override](acceptance-scenarios.md#ac-us03-007) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-008: Reset to latest applied invoice](acceptance-scenarios.md#ac-us03-008) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-009: Reset to baseline before invoices](acceptance-scenarios.md#ac-us03-009) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-010: Invalid or failed override reset](acceptance-scenarios.md#ac-us03-010) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-011: Applied and historical invoice effects](acceptance-scenarios.md#ac-us03-011) | I, B | E-ASSET, E-FINANCE |
| [AC-US03-012: Display settings do not edit assets](acceptance-scenarios.md#ac-us03-012) | I, B | E-ASSET, E-FINANCE |
| [AC-US04-001: Create Open ticket](acceptance-scenarios.md#ac-us04-001) | U, I, B | E-MAINT |
| [AC-US04-002: Same-room asset link](acceptance-scenarios.md#ac-us04-002) | U, I | E-MAINT |
| [AC-US04-003: Fixed ticket associations](acceptance-scenarios.md#ac-us04-003) | U, I | E-MAINT |
| [AC-US04-004: Start work with owner](acceptance-scenarios.md#ac-us04-004) | U, I, B | E-MAINT |
| [AC-US04-005: Reject ownerless start](acceptance-scenarios.md#ac-us04-005) | U, I | E-MAINT |
| [AC-US04-006: Resolve with note](acceptance-scenarios.md#ac-us04-006) | U, I, B | E-MAINT |
| [AC-US04-007: Reject empty resolution note](acceptance-scenarios.md#ac-us04-007) | U, I | E-MAINT |
| [AC-US04-008: Disallowed transitions and deletion](acceptance-scenarios.md#ac-us04-008) | U, I, B | E-MAINT |
| [AC-US04-009: Owner removal and reassignment](acceptance-scenarios.md#ac-us04-009) | U, I, B | E-MAINT |
| [AC-US04-010: Unresolved edits and chronology](acceptance-scenarios.md#ac-us04-010) | U, I, B | E-MAINT |
| [AC-US04-011: Cancellation and persistence failure](acceptance-scenarios.md#ac-us04-011) | U, I, B | E-MAINT |
| [AC-US04-012: Resolved ticket is read-only](acceptance-scenarios.md#ac-us04-012) | U, I, B | E-MAINT |
| [AC-US04-013: Resolution does not alter observations or replacement](acceptance-scenarios.md#ac-us04-013) | U, I | E-MAINT |
| [AC-US04-014: Priority and actual overdue date](acceptance-scenarios.md#ac-us04-014) | U, I | E-MAINT |
| [AC-US04-015: Separate resolved records and missing information](acceptance-scenarios.md#ac-us04-015) | U, I | E-MAINT |
| [AC-US04-016: Explicit critical asset flags](acceptance-scenarios.md#ac-us04-016) | U, I | E-MAINT |
| [AC-US05-001: Whole completed months](acceptance-scenarios.md#ac-us05-001) | U | E-FINANCE |
| [AC-US05-002: Month-end original-day anniversaries](acceptance-scenarios.md#ac-us05-002) | U | E-FINANCE |
| [AC-US05-003: Leap-year boundaries](acceptance-scenarios.md#ac-us05-003) | U | E-FINANCE |
| [AC-US05-004: Before service and useful-life cap](acceptance-scenarios.md#ac-us05-004) | U | E-FINANCE |
| [AC-US05-005: Installation fallback and current edited anchor](acceptance-scenarios.md#ac-us05-005) | U, I, B | E-FINANCE |
| [AC-US05-006: Replacement date and urgency](acceptance-scenarios.md#ac-us05-006) | U, I, B | E-FINANCE |
| [AC-US05-007: Future-window boundaries](acceptance-scenarios.md#ac-us05-007) | U | E-FINANCE |
| [AC-US05-008: FX direction and fixed date](acceptance-scenarios.md#ac-us05-008) | U, I, B | E-FINANCE |
| [AC-US05-009: Missing or invalid FX configuration](acceptance-scenarios.md#ac-us05-009) | U, I, B | E-FINANCE |
| [AC-US05-010: Effective-cost spending proxy](acceptance-scenarios.md#ac-us05-010) | U, I, B | E-FINANCE |
| [AC-US05-011: Separate horizons and shared filters](acceptance-scenarios.md#ac-us05-011) | U, I, B | E-FINANCE |
| [AC-US05-012: Planning labels and independent flags](acceptance-scenarios.md#ac-us05-012) | U, I, B | E-FINANCE |
| [AC-US05-013: Unrounded aggregation and local display](acceptance-scenarios.md#ac-us05-013) | U, I, B | E-FINANCE |
| [AC-UX-001: Navigation and header controls](acceptance-scenarios.md#ac-ux-001) | B, M | E-UI |
| [AC-UX-002: Search does not change reporting scope](acceptance-scenarios.md#ac-ux-002) | B, M | E-ROOM, E-UI |
| [AC-UX-003: Schematic Map and equivalent List](acceptance-scenarios.md#ac-ux-003) | B, M | E-ROOM, E-UI |
| [AC-UX-004: Operational overview precedes finance](acceptance-scenarios.md#ac-ux-004) | B, M | E-UI |
| [AC-UX-005: Room card selection and Log fault](acceptance-scenarios.md#ac-ux-005) | B, M | E-MAINT, E-ROOM, E-UI |
| [AC-UX-006: Maintenance entry points](acceptance-scenarios.md#ac-ux-006) | B, M | E-MAINT, E-UI |
| [AC-UX-007: Independent import presentation](acceptance-scenarios.md#ac-ux-007) | B, M | E-IMPORT, E-UI |
| [AC-UX-008: Stale preview requires renewed confirmation](acceptance-scenarios.md#ac-ux-008) | B, M | E-IMPORT, E-UI |
| [AC-UX-009: Inline observation editor](acceptance-scenarios.md#ac-ux-009) | B, M | E-ROOM, E-UI |
| [AC-UX-010: Inline asset editor and evidence](acceptance-scenarios.md#ac-ux-010) | B, M | E-ASSET, E-UI |
| [AC-UX-011: Override and reset information](acceptance-scenarios.md#ac-ux-011) | B, M | E-ASSET, E-UI |
| [AC-UX-012: Inline maintenance editor](acceptance-scenarios.md#ac-ux-012) | B, M | E-MAINT, E-UI |
| [AC-UX-013: Empty and write-feedback states](acceptance-scenarios.md#ac-ux-013) | B, M | E-UI |
| [AC-UX-014: Display and date boundaries](acceptance-scenarios.md#ac-ux-014) | B, M | E-FINANCE, E-UI |
| [AC-UX-015: Confirmed visual styling](acceptance-scenarios.md#ac-ux-015) | B, M | E-UI |
| [AC-UX-016: Required browser and responsive widths](acceptance-scenarios.md#ac-ux-016) | B, M | E-UI |
| [AC-UX-017: Keyboard and accessible feedback](acceptance-scenarios.md#ac-ux-017) | B, M | E-UI |
| [AC-UX-018: Integrated refresh and persistence](acceptance-scenarios.md#ac-ux-018) | B, M | E-STARTUP, E-UI |
| [AC-UX-019: Complete assumptions inventory](acceptance-scenarios.md#ac-ux-019) | B, M | E-FINANCE, E-UI |
| [AC-DEMO-001: Reset starts an empty rehearsal](acceptance-scenarios.md#ac-demo-001) | I, B, M | E-DEMO, E-STARTUP |
| [AC-DEMO-002: Restart retains selected rehearsal](acceptance-scenarios.md#ac-demo-002) | I, B, M | E-DEMO, E-STARTUP |
| [AC-DEMO-003: Explicit financial example dates](acceptance-scenarios.md#ac-demo-003) | M | E-DEMO, E-STARTUP |
| [AC-DEMO-004: Timed walkthrough and disclosures](acceptance-scenarios.md#ac-demo-004) | M | E-DEMO, E-STARTUP |
| [AC-DEMO-005: Clean startup evidence](acceptance-scenarios.md#ac-demo-005) | I, B, M | E-DEMO, E-STARTUP |
| [AC-INFRA-001: Stale record saves](acceptance-scenarios.md#ac-infra-001) | I, B | E-ASSET, E-MAINT |
| [AC-INFRA-002: Duplicate maintenance submission](acceptance-scenarios.md#ac-infra-002) | I, B | E-MAINT |
| [AC-INFRA-003: Obsolete browser response](acceptance-scenarios.md#ac-infra-003) | B | E-ROOM, E-UI |
| [AC-INFRA-004: Reset cancellation and rollback](acceptance-scenarios.md#ac-infra-004) | I, B | E-STARTUP |
| [AC-INFRA-005: Reset invalidates other tabs](acceptance-scenarios.md#ac-infra-005) | I, B | E-STARTUP, E-UI |
| [AC-INFRA-006: Reset response-loss retry](acceptance-scenarios.md#ac-infra-006) | I | E-STARTUP |
| [AC-INFRA-007: Preview lifetime and confirmation retry](acceptance-scenarios.md#ac-infra-007) | I, B | E-IMPORT, E-STARTUP |
| [AC-INFRA-008: Database busy and atomic history](acceptance-scenarios.md#ac-infra-008) | I, B | E-ASSET, E-IMPORT, E-MAINT |
| [AC-INFRA-009: Required maintenance recorder](acceptance-scenarios.md#ac-infra-009) | I, B | E-MAINT |

## 3. Approved interaction companion checks

The existing UI proposal checks are now required. Each IX check is executed alongside its linked acceptance scenario.
Record subcase results under that scenario's evidence directory. Every IX check requires browser automation and manual Chrome review.

| Check | Required interaction cases | Companion scenario |
|---|---|---|
| IX-UX-001 | Active navigation, retained filters/reporting date, dirty-form Continue/Discard | AC-UX-001 |
| IX-UX-002 | Substring/case search, search versus scope empty states, Clear search | AC-UX-002 |
| IX-UX-003 | Deterministic ordering and retained search/selection across Map/List | AC-UX-003 |
| IX-UX-004 | Operational ordering, labelled counts, unique-asset finance | AC-UX-004 |
| IX-UX-005 | Card close/switch/exclusion protection, focus and complete Log fault return context | AC-UX-005 |
| IX-UX-006 | Add maintenance record card, room/asset choices, cancellation, typed recorder, duplicate submission | AC-UX-006 |
| IX-UX-007 | Workflow/file changes invalidate preview, prerequisites, blockers versus warnings | AC-UX-007 |
| IX-UX-008 | Pending controls, retained failure input, renewed stale-preview review | AC-UX-008 |
| IX-UX-009 | Clear confirmation, recorded versus unassessed UNKNOWN | AC-UX-009 |
| IX-UX-010 | Source/current/effective labels, installation fallback, historical-only evidence | AC-UX-010 |
| IX-UX-011 | Financial override/reset labels, source identification, unchanged operational fields | AC-UX-011 |
| IX-UX-012 | Card fields, prerequisite messages, Start/Resolve actions, resolution note | AC-UX-012 |
| IX-UX-013 | First-use, empty, loading, invalid, warning, saving, success, persistence failure | AC-UX-013 |
| IX-UX-014 | Delivered language options, date labels/control, offsets, FX/disclaimer | AC-UX-014 |
| IX-UX-015 | 16px base, 8px spacing, blue action contrast, separate neutral clearing actions | AC-UX-015 |
| IX-UX-016 | 1200px/600px breakpoints, 200px navigation/400px card, wrapping/scrolling | AC-UX-016 |
| IX-UX-017 | Error announcements/focus, trigger restoration, overlay trap, Escape dirty protection | AC-UX-017 |
| IX-UX-018 | Refreshed data, return context, restarted records/preferences, session boundaries | AC-UX-018 |
| IX-UX-019 | Read-only assumptions before imports/invalid FX, loaded owners/rates, reset dialog | AC-UX-019 |

Check responsive behavior at 1440px, 1024px, 768px, and 360px, plus both sides of approved breakpoints.
Use long fictional labels and validation errors. Check keyboard operation without hover or color dependence.
For each delivered stretch language, check dictionary coverage, English fallback, unchanged source text, and Alex's review status.
Undelivered stretch languages are conditional omissions, not fabricated passing results.

## 4. Evidence, commands, and completion

Use [runtime test commands](demo.md#6-local-runtime-procedures) after implementation.
Save local evidence in runtime/verification/<build>/<scenario-or-check-id>/.
Each record includes scenario/case ID, governing requirements, method, independent setup, expected/actual outcomes, and PASS/FAIL/NOT RUN.
Include build revision, local modification state, date, Python/package versions, database reference, and relevant browser/Windows versions.
Attach assertion output or screenshots when they substantiate the result. Preserve failures and omissions.
Use actual installed-Chrome results for E-UI/E-STARTUP/E-DEMO. Do not relabel Chromium screenshots as installed Chrome.

Minimum infrastructure coverage includes half-written rollback, stale edits, response-loss retries, late reads, reset races, preview expiry, and restart.
Application readiness requires every applicable scenario and IX subcase to have actual evidence.
The twelve-minute rehearsal requires measured elapsed time and explicit AR-002/translation limitations.
Documentation readiness only requires complete mappings, approved interfaces, and consistent instructions.
No application test files or passing application results exist in this documentation revision.

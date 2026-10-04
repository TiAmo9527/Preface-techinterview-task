# F002 reviewed imports execution report

Updated: 2026-10-04. Series status: **implemented** within the approved scope and Alex's narrowed verification scope.
[Series status](f002-status-reviewed-imports.md). [Planned order and coverage](../../tasks.md).

## Approval and scope

Alex selected **"Approve IM-01–IM-04 (Recommended)"** on 2026-10-03 and then requested
implementation of the F002A plan. [Recorded algorithms and approval](../../pseudocode-review.md#f002-imports-submission--im-01im-04).
Algorithm approval covers F002A–D. The original execution delivered F002A;
Alex explicitly requested F002B, F002C and F002D implementation on 2026-10-04. This report now covers **F002A–D**.
Alex authorized pushing F002A–D and creating a GitHub PR, then requested "skip chrome computer use test".
F001C and its F001B contract prerequisite were delivered within their foundation limits.
F002 recommends High reasoning effort. The active setting is not exposed, so comparison is unverified;
the execution skill explicitly permits proceeding in this case. Approved S-03 governs Python checks.

## Execution log

### 2026-10-03–04 — F002A workbook parser and templates

- Implemented [workbook parser](../../../src/services/workbooks.py) with shared approved schema constants,
  frozen row/cell/result structures, detached normalized-value copies, and the existing diagnostic contract.
  It reads workbook bytes once in memory with `data_only=False`, closes the workbook, and accesses no store.
- Enforced sole workflow sheet, exact headers in any order, supported/readable XLSX, formulas/merges,
  required values, enums, identity grammar/parents/region, dates/order, costs, useful lives and Excel error cells.
  Preserved nonempty invalid rows, offending values/types and field-to-cell coordinates.
  Independent failures remain visible. Fully empty rows are ignored; partial rows are validated.
- Normalized each assessment independently through F001B helpers. Recorded UNKNOWN retains metadata;
  absent assessments become unassessed UNKNOWN without metadata. No Healthy state or history is inferred.
  Missing installation, explicit zero cost and missing invoice supplier produce warnings on otherwise valid rows.
- Created headers-only [Assets template](../../../sample_data/spreadsheets/templates/Assets.xlsx) and
  [Invoices template](../../../sample_data/spreadsheets/templates/Invoices.xlsx). Both have one required sheet,
  exact 26/12 headers, no source rows, formulas or merges. All four supplied workbook SHA-256 hashes match inventory.
- Extended [mapped tests](../../../tests/unit/test_import.py). Targeted run: **204 passed** in 2.90s.
  Final unit/integration regression: **465 passed**, 0 failures, 1 upstream Starlette/AnyIO warning, 28.20s.
  Scoped parser/store boundary checks use production temporary on-disk stores, with empty and independently populated
  state, and prove byte-identical database/generation preservation and no saved workbook. These do not claim HTTP import acceptance.
- Targeted compileall and pip check passed. Lint/typecheck/count: **NOT RUN**, approved S-03; no configured equivalents.
  Browser/manual checks: **NOT RUN in this execution**; F002A adds no browser surface. Existing F001 evidence is historical.
  [Final test output](../../../runtime/verification/3e2eac2-f002a/tests.txt),
  [JUnit](../../../runtime/verification/3e2eac2-f002a/tests.xml),
  [environment, commands and hashes](../../../runtime/verification/3e2eac2-f002a/environment.json).
- Build: `3e2eac2` plus this uncommitted F002A change set; Python 3.12.5 on Windows.
  Documentation links/anchors and whitespace are verified in the
  [local documentation audit](../../../runtime/verification/3e2eac2-f002a/documentation-audit.json).
  Tests ran on 2026-10-03; final reporting completed on 2026-10-04 in Asia/Hong_Kong.

F002A is **implemented within its parser/template acceptance limits**.
Supplied valid files each normalize 36 rows without warnings.
Supplied invalid Assets rows deliberately parse: their assessment disagreements and category conflicts belong to F002B.
Invalid Invoices retains all 38 source rows and reports unsupported category/currency, impossible date,
installation ordering and invalid life. Unknown targets, duplicate identities and controlling-date conflicts belong to F002B.
No preview, confirmation, saved import counts, observation persistence, or browser behavior is claimed.

## Scenario evidence and acceptance limits

Each linked record contains build/date, environment, independent setup, expected/actual outcomes,
assertion references and explicit deferred methods. Parser checks live in the authorized unit file;
the scoped I checks there exercise the production parser alongside isolated production stores.

| Scenario | Passing F002A surface | Deferred acceptance |
|---|---|---|
| [AC-US01-006](../../../runtime/verification/3e2eac2-f002a/AC-US01-006/result.json) | U value/identity/date validation, source diagnostics; scoped I unchanged-store boundary | Preview/confirmation/HTTP behavior in F002B/C. |
| [AC-US01-007](../../../runtime/verification/3e2eac2-f002a/AC-US01-007/result.json) | U file/header/sheet/formula/merge failures; scoped I unchanged-store boundary | Actual upload/confirmation routes in F002C. |
| [AC-US01-008](../../../runtime/verification/3e2eac2-f002a/AC-US01-008/result.json) | U warnings and retained absent/zero values; scoped I no writes | Atomic confirmation, calculated fallback and browser review in later jobs. |
| [AC-US01-009](../../../runtime/verification/3e2eac2-f002a/AC-US01-009/result.json) | U immutable values/coordinates/diagnostics; scoped I no writes | Reviewed effects/counts/override clearing in F002B/C. |
| [AC-US01-022](../../../runtime/verification/3e2eac2-f002a/AC-US01-022/result.json) | U headers-only/empty/partial cases; scoped I no writes | Cancellation and committed no-op receipt in F002C/D. |
| [AC-US02-009](../../../runtime/verification/3e2eac2-f002a/AC-US02-009/result.json) | U recorded/unassessed UNKNOWN and independent groups; scoped I no writes | Saved observations and room browser presentation in F002C/F004. |
| [AC-US02-014](../../../runtime/verification/3e2eac2-f002a/AC-US02-014/result.json) | U invalid imported metadata; scoped I no writes | Baseline repeat preserving manager edits, import commit and browser in F002B/C/D/F004. |

## Project status and remaining work

F001 and F002A–D are complete within their scoped acceptance limits and Alex's narrowed verification scope.
F003–F007 remain unimplemented. Installed-Chrome computer-use review is explicitly omitted, not passed.
F002 is **4/4 jobs = 100%**. Project spec-driven milestone completion is **7/21 jobs = 33.3%**.
Only fully implemented jobs count, with equal weighting; this is not an effort estimate or full product acceptance.
The next delivery job is F003A: calendar and money calculations. Its behavior-group pseudocode requires separate approval.
AR-002 manual asset creation remains unmet; assessor acceptance of the maintenance reinterpretation is unconfirmed.

## 2026-10-04 — F002B deterministic import plans

- Implemented [read-only planner](../../../src/services/imports.py) and
  [snapshot read adapter](../../../src/db/import_queries.py). IM-02 approval already covers this algorithm;
  Alex's current request authorizes this job. Active reasoning effort is unavailable, so its comparison remains unverified.
- Plans consume the immutable parser result and one caller-owned saved-state snapshot. Baselines group repeated
  property/room values, retain all contributing cell coordinates, enforce complete new rooms and property-local labels,
  compare preserved evidence, skip identical identities, and block changed/duplicate identities or occupied categories.
- Invoices resolve every valid normalized row, including historical targets; carry all parser diagnostics;
  compare six-field snapshots at the maximum stored/incoming date; retain equivalent references in identity order;
  apply the first controlling invoice regardless of baseline purchase date and later strictly newer dates even with equal values.
  Skips and historical-only items preserve operational edits and overrides.
- Reviewed effects include entity inserts, new evidence, distinct updates, historical-only items, skips, warnings/blockers,
  all six before/after fields, source/effective/override states, previous/new references, expected/resulting versions,
  and system-attributed CLEAR_ON_INVOICE history linked symbolically to its planned update.
  F002C allocates actual event/upload IDs and commit timestamps. Blocked plans contain no writable effects.
  Canonical immutable plans compare all reviewed effects; returned dictionaries are detached.
- Added independent planner cases in [unit checks](../../../tests/unit/test_import.py) and
  [snapshot integration checks](../../../tests/integration/test_import.py). Covered source repeats after edits,
  old/equal/new dates, equivalent/conflicting ties, both separate upload orders, incomplete/new rooms,
  invalid historical rows, meaningful saved-state changes and row permutation.
  Snapshot tests use production transactions and isolated on-disk stores and compare every table and generation before/after.
  Fixture insertion is test setup, not execution of an import commit.
- Supplied baseline predicts **4 properties / 12 rooms / 36 assets**; supplied invoices predict
  **36 evidence items / 36 distinct updates**. Both invalid files block without writable effects.
  All four supplied workbook hashes match the inventory.
- Final unit/integration regression: **528 passed**, 0 failures, 1 upstream Starlette/AnyIO deprecation warning.
  [Test output](../../../runtime/verification/3e2eac2-f002b/tests.txt),
  [JUnit assertions](../../../runtime/verification/3e2eac2-f002b/tests.xml),
  [environment/commands/hashes](../../../runtime/verification/3e2eac2-f002b/environment.json),
  [documentation audit](../../../runtime/verification/3e2eac2-f002b/documentation-audit.json).
  Targeted compileall, pip check and whitespace checks passed.
  Lint/typecheck/count: **NOT RUN** under approved S-03; no configured equivalents.
  Browser/manual methods: **NOT RUN** for this job, which adds no UI.
- Build `3e2eac2` plus preserved F002A and new F002B uncommitted changes; Python 3.12.5 on Windows.
  No root configuration, schema, route, browser, supplied workbook or existing approval-policy changes.

F002B is **implemented within its planner/snapshot acceptance limits**. Full US-01 acceptance remains open:
actual writes, rollback, preview races, histories/receipts, cancellation, API confirmation and browser review are F002C/D.
Financial recalculation/display remain later jobs. No saved-import or browser-success claim is made here.

Planner evidence for AC-US01-001–019 and 021–025 is recorded under
[the local evidence directory](../../../runtime/verification/3e2eac2-f002b), one result.json per scenario.
Each record includes independent setup, expected/actual result, assertion references, build/environment and deferred methods.
[AC-US01-020](../../../runtime/verification/3e2eac2-f002b/AC-US01-020/result.json) is **NOT RUN**:
commit-failure injection requires F002C. AC-US01-021 passes only meaningful-plan comparison;
its stale-preview API/reconfirmation behavior remains NOT RUN. AC-US01-022 passes only empty/no-op planning;
cancellation and successful no-op receipts remain NOT RUN.

## 2026-10-04 — F002C atomic preview confirmation

- Alex requested F002C implementation. Existing IM-03 and PR-05 approvals cover the algorithm and reset integration.
  No consequential deviation was required. Active reasoning effort is not exposed; comparison remains unverified.
- Added [preview/confirmation service](../../../src/services/previews.py): immutable entries, opaque UUIDs,
  a locked process registry, thirty-minute expiry and twenty-entry FIFO capacity. Workbooks parse once.
  Preview plans against a read snapshot without saved records or raw workbook storage.
- Confirmation uses the existing validated command coordinator and caller-owned BEGIN IMMEDIATE.
  Generation and durable receipt precede registry prerequisites. Re-planning compares all meaningful effects.
  Changed effects return STALE_PREVIEW with a new review; blockers and unavailable previews save nothing.
  Retries return the committed response even after expiry, eviction, store reopening, or a separate Python process restart.
- Extended [query adapter](../../../src/db/import_queries.py) to save entity inserts, observations, preserved baselines,
  source coordinates, invoice items, all six current fields, versions, before/after update references, and linked
  SYSTEM override-clearing histories. The coordinator saves the response receipt in the same transaction.
  Counts use actual entity/evidence/update writes. Skips preserve original evidence and operational state;
  no-op confirmations save only their retry receipt, without upload or domain history.
- Added strict multipart preview and JSON confirmation endpoints in [thin routes](../../../src/views/routes.py).
  Duplicate/extra multipart fields and replacement confirmation rows are rejected. Existing structured errors
  and no-store headers apply. Route registration connects generation-selective registry eviction to the reset hook.
- Extended [integration checks](../../../tests/integration/test_import.py) with independent on-disk stores and real helpers.
  Verified supplied baseline **4 properties / 12 rooms / 36 assets**, invoice **36 items / 36 distinct updates**,
  blocked uploads, warnings, precedence/ties, skips after edits, provenance/new rooms, blank installation,
  override history, stale renewed review, cancellation boundary and receipt-only no-ops.
  Injected failures at baseline, invoice-history, override-history and receipt writes all rolled back.
  A five-second busy lock preserved state and allowed explicit retry. Concurrent confirmations replay one receipt;
  preview/confirmation/reset schedules and delayed cleanup preserve new-generation previews.
- Final unit/integration suite: **576 passed**, 0 failures, 1 upstream Starlette/AnyIO deprecation warning, 46.30s.
  [Test output](../../../runtime/verification/3e2eac2-f002c/tests.txt),
  [JUnit](../../../runtime/verification/3e2eac2-f002c/tests.xml),
  [environment/commands/hashes](../../../runtime/verification/3e2eac2-f002c/environment.json),
  [documentation audit](../../../runtime/verification/3e2eac2-f002c/documentation-audit.json).
  Targeted compileall, pip check, supplied hashes and whitespace checks passed.
  Lint/typecheck/count: **NOT RUN**, approved S-03; this Python stack has no configured equivalents.
- Build `3e2eac2` plus preserved F002A/B and F002C uncommitted changes; Python 3.12.5 on Windows.
  No schema, root configuration, browser module, or supplied workbook changes. Evidence remains ignored local runtime data.

F002C is **implemented within its service/database/API acceptance limits**.
Per-scenario records for AC-US01-001–025 and AC-INFRA-005/007/008 are under
[local F002C evidence](../../../runtime/verification/3e2eac2-f002c).
Each names independent setup, expected/actual results, executed assertions and remaining methods.
Browser/manual review, full two-tab UI behavior, financial recalculation/display, observation editing,
maintenance actions and evidence presentation remain NOT RUN for their downstream jobs.
Cancellation is verified as an abandoned review causing no saved writes; its actual browser controls are F002D.
AR-002 manual asset creation remains unmet and assessor acceptance of its maintenance reinterpretation remains unconfirmed.

## 2026-10-04 — F002D reviewed import browser flow

- Implemented [Import presentation](../../../src/views/static/imports.js) through existing production preview/confirmation routes.
  The shared state/request/English/shell modules own review state, upload transport, feedback and navigation integration.
  Views display server effects without implementing validation, precedence, persistence or financial calculations.
- Assets and Invoices remain independent single-workbook actions. The selected workflow/file and prerequisite guidance remain visible.
  Reviews separate proposed counts from actual committed counts, distinguish blockers/warnings and expose source coordinates and offending values.
  Invoice review shows all six before/after fields and explicit active-override clearing with linked history.
- File/workflow changes and cancellation invalidate the review. Blockers disable confirmation; warnings permit it.
  Confirmation disables duplicate/pending controls and guards navigation until its result is known.
  Stale results display the replacement review and require a separate confirmation with a new command identity.
  Rollback, busy-store and unknown-response failures retain file, workflow, summary, diagnostics and unchanged retry identity.
  A committed retry replays the receipt after preview expiry/eviction or an actual server-process restart.
- Successful commits and receipt replays refetch the existing server-rendered portfolio snapshot through the shared request helper.
  Saved counts are never inferred from proposed effects. Refresh failure preserves the confirmed result and offers a read-only retry.
  The current summary is hidden until refreshed. Full operational/financial endpoints and source-evidence cards remain later jobs.
- Added [journey checks](../../../tests/browser/test_journeys.py) and extended [UI checks](../../../tests/browser/test_ui.py).
  Every US-01 B method is covered, plus IX-UX-007/008/013 and AC-INFRA-005/007/008.
  Independent isolated stores and actual routes cover invalid supplied uploads, 4/12/36 baseline, two-target and 36/36 invoices,
  warnings, blank installation/override clearing, four rollback stages, headers/empty-row no-ops, cancel, stale review,
  two-tab reset, five-second write lock, response loss and actual process restart.
  Browser checks also cover loading/obsolete responses, pending controls, refresh retry, keyboard feedback and eight required widths.
- An initial selector-label failure was corrected with an explicit accessible name.
  An initial 360px overflow failed and was corrected by allowing the file control's flex container to shrink.
  The final full browser suite passed: **66 passed**, 0 failures, 1 upstream deprecation warning, 77.08s.
  Final unit/integration regressions: **576 passed**, 0 failures, 1 upstream deprecation warning, 47.65s.
  Total: **642 passing automated cases** across the two required commands.
- [Final browser assertions](../../../runtime/verification/3e2eac2-f002d/all-browser.xml),
  [unit/integration assertions](../../../runtime/verification/3e2eac2-f002d/regression.xml),
  [environment/commands/hashes](../../../runtime/verification/3e2eac2-f002d/environment.json),
  [documentation audit](../../../runtime/verification/3e2eac2-f002d/documentation-audit.json).
  Thirteen local scenario directories retain independent setup, expected/actual outcome, assertion names and explicit downstream omissions.
  Targeted compileall, pip check, blank templates, four supplied workbook hashes and whitespace checks passed.
  Lint/typecheck/count: **NOT RUN**, approved S-03; no configured equivalents.
- Installed-Chrome computer-use review: **NOT RUN at Alex's explicit request**, "skip chrome computer use test" on 2026-10-04.
  The attempted native selection timed out before application input; the browser connector reported Chrome unavailable.
  Chromium automation is not relabelled as installed-Chrome or manual evidence.
  Financial recalculation/display, source-evidence cards, remaining room/maintenance/asset workflows and final integrated acceptance remain downstream.
- Verified source tree: `3e2eac2` plus preserved F002A–C and new F002D changes, Python 3.12.5, Chromium 140.0.7339.16 on Windows.
  The new `codex/f002-reviewed-imports` branch starts from tree-equivalent `origin/main` (`b288475`) for the authorized F002A–D PR.
  No supplied workbook/sidecar, schema, dependency or root-configuration changes. Generated runtime evidence stays uncommitted.

F002D is **implemented within Alex's explicitly narrowed verification scope**.
This completes all four F002 delivery jobs; it does not claim full product or external assessment acceptance.
AR-002's missing manual asset creation and unconfirmed maintenance reinterpretation remain disclosed.

| F002D browser evidence | Passing implemented surface |
|---|---|
| [AC-US01-001](../../../runtime/verification/3e2eac2-f002d/AC-US01-001/result.json), [AC-US01-002](../../../runtime/verification/3e2eac2-f002d/AC-US01-002/result.json) | Independent baseline/invoice actions and actual counts. |
| [AC-US01-008](../../../runtime/verification/3e2eac2-f002d/AC-US01-008/result.json), [AC-US01-019](../../../runtime/verification/3e2eac2-f002d/AC-US01-019/result.json) | Warning confirmation, six-field changes, blank installation and override history. |
| [AC-US01-020](../../../runtime/verification/3e2eac2-f002d/AC-US01-020/result.json), [AC-US01-021](../../../runtime/verification/3e2eac2-f002d/AC-US01-021/result.json), [AC-US01-022](../../../runtime/verification/3e2eac2-f002d/AC-US01-022/result.json) | Rollback/retry, renewed stale review, cancellation and no-op uploads. |
| [AC-UX-007 / IX-UX-007](../../../runtime/verification/3e2eac2-f002d/AC-UX-007/result.json), [AC-UX-008 / IX-UX-008](../../../runtime/verification/3e2eac2-f002d/AC-UX-008/result.json), [AC-UX-013 / IX-UX-013](../../../runtime/verification/3e2eac2-f002d/AC-UX-013/result.json) | Blocked/invalidated review, pending controls, retained input, feedback, keyboard and responsive presentation. |
| [AC-INFRA-005](../../../runtime/verification/3e2eac2-f002d/AC-INFRA-005/result.json), [AC-INFRA-007](../../../runtime/verification/3e2eac2-f002d/AC-INFRA-007/result.json), [AC-INFRA-008](../../../runtime/verification/3e2eac2-f002d/AC-INFRA-008/result.json) | Two-tab reset, expiry/eviction, committed retry/process restart and database busy. |

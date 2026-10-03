# Pseudocode approval record

Version: 1.4

Date: 2026-10-03

Status: Persistence/reset PR-01–PR-06 APPROVED by Alex on 2026-10-03.
F001B FB-01–FB-03 and F001C FC-01–FC-03 foundations are also APPROVED. All later algorithms retain their separate gates.

Use [technical design](technical-design.md), [verification mapping](verification-plan.md), and [agent instructions](../AGENTS.md).
The instruction to adjust documentation does not authorize application coding past this gate.

## Required submission

For one behavior group, record its document versions, inputs, outputs, and acceptance/check IDs.
Present ordered pseudocode with validation, transaction ownership, before/after state, failure outcomes, and retry behavior.
State any departure from the approved design. Record Alex's actual response and approval date.
An unanswered request is pending. An approval applies only to its recorded group and algorithm scope.

## Group ledger

| Group | Algorithm scope | Status | Owner approval/evidence |
|---|---|---|---|
| Persistence/reset | [f001 PR-01–PR-06](#f001-persistencereset-submission): initialization, transactions, constraints, receipts, versions, generation, atomic reset and browser invalidation | APPROVED | Alex approved 2026-10-03: "approve pseudocode - directly work on the feature job as needed". |
| Imports | FB-01/FB-02 shared validators/contracts only; parsing/planning/confirmation remain unapproved | FOUNDATION APPROVED | Alex selected "Approve scoped pseudocode (Recommended)" on 2026-10-03. See FB-01–FB-03 below. |
| Observations/reporting | Shared scope, independent observations, distinct counts, room reads | NOT SUBMITTED | None |
| Assets/overrides | Operational edits, source/effective values, override/reset history | NOT SUBMITTED | None |
| Maintenance | Creation card, recorder, owners, progression, immutable resolution, retries | NOT SUBMITTED | None |
| Finance/display settings | FB-02/FB-03 contracts/configuration/clock/diagnostics; FC-01–FC-03 browser preferences, sessions, dictionaries and shell | FOUNDATION APPROVED | Alex approved FC-01–FC-03 on 2026-10-03. Calculations and consuming feature views remain unapproved. |

This is an approval ledger, not the deferred implementation task plan.

## f001 Persistence/reset submission

Submission date: 2026-10-03. Approved by Alex on 2026-10-03. See the decision record below.
Application status at submission: NOT RUN. Subsequent execution evidence belongs in the f001 series artifacts.

Alex selected Persistence/reset only during the review conversation.
The subsequent instruction, "PLEASE IMPLEMENT THIS PLAN", authorizes recording this pending submission.
The requested plan explicitly retains the algorithm approval gate and excludes installation and job execution.
That recording instruction was not approval of PR-01–PR-06.
Alex subsequently approved the pseudocode and authorized feature-job execution through the response recorded below.

### Governing documents and scope

| Authority | Version / approved adaptation |
|---|---|
| [Product](product-spec.md), [contracts](data-contracts.md), [sample plan](sample-data-plan.md) | v0.5 each |
| [Assessment obligations](assessment-requirements.md), [demo/runtime procedures](demo.md) | v0.5 each |
| [Technical design](technical-design.md), [verification mapping](verification-plan.md) | v1.0 each at submission. Technical design v1.1 records the runtime amendment below. |
| [UI requirements](ui-ux-spec.md) | v0.4 |
| [Acceptance scenarios](acceptance-scenarios.md), [glossary](glossary.md) | v0.2 each |
| [Task order and coverage](tasks.md) | v0.6 |
| [Planning adaptations](implementation-planning-review.md) | P-01–P-05 and S-01–S-03 approved by Alex on 2026-10-03 |

Read root and scoped AGENTS.md files for docs, jobs, persistence, services, views, and tests.
Read all three f001 jobs, governing documents, adjacent foundations, and both job-specification skills.
The documentation skill was not used.

| Job | Submitted Persistence/reset surface | Separate approval still required |
|---|---|---|
| [f001a](jobs/feature-jobs/f001a-durable-local-store.md) | Initialization, schema constraints, connections, transactions, isolated-store seam | No other behavior group for this surface. Installation/execution was subsequently authorized by the recorded response. |
| [f001b](jobs/feature-jobs/f001b-validated-command-boundaries.md) | Command coordination, payload hashing, receipts, versions, structured persistence errors | Imports validators/contracts and Finance/display configuration/diagnostics |
| [f001c](jobs/feature-jobs/f001c-browser-shell-and-reset.md) | Generation-guarded reset, preview-eviction hook, reset presentation, obsolete-draft/read protection | Finance/display browser-state scope, including preferences, session/new-tab dates, and dictionaries |

Keep the serialized f001a -> f001b -> f001c dependency order.
This submission does not approve whole jobs or other behavior groups.
Full domain mutations remain with their consuming jobs and approvals.

Apply P-01 and P-04 through injectable test seams and the approved persistence/service/view ownership.
Apply P-02 by verifying multipart/timezone support on the approved runtime during implementation.
The runtime amendment below supersedes the submitted Python 3.11 target.
Apply P-03 by preserving operational reads during invalid finance configuration.
Its diagnostic contract requires the separate Finance/display review.
Apply P-05 by treating technical-design section 2 as the schema authority despite the stale product sentence.

Apply S-01–S-03: GPT-6.1 Sol guidance only, existing folders, and Python verification.
All three f001 jobs recommend High reasoning effort.
The active effort is not exposed. Its comparison is unverified.
No consequential departure from the approved design is proposed.

AR-002 manual asset creation remains unmet.
Assessor acceptance of the maintenance reinterpretation remains unconfirmed.

### Local prerequisite evidence

These are read-only observations from this review session, not application acceptance.
Interpreter, scaffold, absent files, and execution artifacts were rechecked before recording.

| Prerequisite | Observed result |
|---|---|
| Repository | HEAD 4cdd533. Working tree was clean before documentation edits. |
| Application/store/tests | Title-printing scaffold. No database implementation, domain store, or application tests. |
| Target interpreter | Python 3.11 absent from the launcher's registered interpreters. |
| Available interpreter | Python 3.12.5 at D:\Python\python.exe. SQLite 3.45.3. |
| Project environment | No .venv, requirements.lock, or requirements-dev.lock. |
| Global packages | FastAPI 0.124.4, Uvicorn 0.33.0, Pydantic 2.12.5, openpyxl 3.1.5, HTTPX 0.28.1. |
| Installation support | python-multipart 0.0.26 and tzdata 2025.2 present globally. Asia/Hong_Kong works on Python 3.12. |
| Test packages | pytest, pytest-playwright, and Playwright absent from that interpreter. |
| Platform/browser | Windows 11 build 26200. Installed Chrome 154.0.8037.93. |
| Local serving | No listener observed on port 8000. |
| Supplied fixtures | All four workbook SHA-256 hashes match the supplied inventory. |
| Initial planning audit | Three f001 job formats, 30 local job links, and 24 scenario mappings checked without failures. |
| Execution artifacts | f001 report/status and feature master status absent, as expected before execution. |

Global packages do not establish a tested Python 3.11 environment or approved dependency pins.
No package or browser installation ran.
The initial audit predates this record. Post-edit results belong in the planning review.

### Algorithms submitted for approval

PR-01–PR-06 are local submission labels, not new requirement or acceptance IDs.
Inputs from separately gated contracts are consumed here without approving their normalization algorithms.

#### PR-01: Initialize and reopen the durable store — f001a

Inputs: Launcher mode, repository root, approved migration version 1.
Tests inject an isolated path, clock, and configuration.
Outputs: Supported empty or preserved store, or actionable startup failure.
Rules: Resolve production runtime/app.sqlite3 from the repository root. Startup never seeds or resets records.

```text
Resolve the fixed production path from app.py's repository location.
Accept an alternate store path only through the test application seam.
Open a configured connection through PR-02.
BEGIN IMMEDIATE.

Inspect existing tables and store_metadata.
IF the database is empty:
    Execute version-1 migration statements on this connection.
    Create the exact logical schema from technical-design section 2.
    Insert singleton metadata with schema_version=1 and a new UUID generation.
ELSE IF metadata identifies supported version 1:
    Verify the required schema exists.
    Preserve all rows, versions, receipts, and generation.
ELSE:
    Reject unsupported, malformed, or unversioned existing stores.
    Do not repair, reseed, or replace them automatically.

Validate the resulting schema and foreign-key integrity.
COMMIT.
Close the connection.

IF --init-db:
    Report initialization and exit.
ELSE:
    Continue startup through the approved application factory.
    f001c serves one worker on 127.0.0.1:8000 without reload.
```

Execute migration statements without implicit intermediate commits.
Preserve text identities, decimal strings, ISO dates, UTC instants, canonical enums, and required text.
Preserve foreign keys with ON DELETE RESTRICT, uniqueness, paired overrides, observation metadata constraints, ticket constraints, and history relationships.
Services validate calendar/decimal values, identifier parents, complete room categories, and same-room ticket links.
Immutable evidence has no ordinary update/delete command path.

State changes: A fresh store gains its complete schema and generation in one transaction.
A supported existing store retains its saved state.
Failures/retries: Migration, validation, or commit failure rolls back schema changes and metadata. Startup stops.
Retrying initialization does not duplicate data or change an existing generation.
Mapping: AC-DEMO-002, AC-DEMO-005, AC-INFRA-008. Browser startup remains deferred until f001c.

#### PR-02: Own connections and transaction boundaries — f001a/f001b

Inputs: Store path, read/write operation, caller-owned callback.
Outputs: Committed result, consistent read snapshot, or structured failure.

```text
Create the connection inside the synchronous operation that uses it.
Set isolation_level=None and check_same_thread=True.
Enable foreign_keys and verify enforcement.
Set the busy timeout to five seconds.
Retain the default DELETE journal mode.

FOR a write:
    BEGIN IMMEDIATE.
    Pass the connection to all nested services and query adapters.
    Execute the caller's operation.
    COMMIT before exposing success.

FOR a read spanning multiple queries:
    BEGIN a short read transaction.
    Read metadata and related representations from one snapshot.
    Finish the read transaction promptly.

ON any failure before successful commit:
    ROLLBACK if a transaction remains active.

ALWAYS close the connection in its owning operation.
```

Nested services neither open competing connections nor begin or commit independent transactions.
Use parameterized SQL.
State changes: A write commits its complete unit of work. Reads change no domain state.
Failures/retries: Lock timeout returns 503 STORE_BUSY. Persistence failure returns 500 SAVE_FAILED after rollback.
Expose no raw SQLite exception. Perform no automatic write retry.
Mapping: AC-INFRA-008 and the rollback foundation for AC-INFRA-004.

#### PR-03: Coordinate commands, versions, and durable receipts — f001b

Inputs: Validated normalized command, operation identity, target identities, generation_id, UUID submission_id, and applicable expected versions.
Outputs: Original receipt response, newly committed response, or structured rejection.
Contract normalization and domain validators require their separate approvals. This algorithm consumes their output.

```text
Reject malformed envelopes and unexpected/protected fields.
Canonicalize the normalized payload as sorted-key UTF-8 JSON.
Include target identities, expected versions, and supplied command fields.
Preserve omission versus explicit null where their meanings differ.
Exclude server-generated timestamps and IDs from the payload hash.
Keep generation/submission identity in the receipt key.
Calculate a deterministic SHA-256 payload hash.

Enter PR-02's write transaction.
Read the current generation.
IF request generation differs:
    Reject as STALE_STORE before receipt, record, or preview lookup.

Look up receipt by generation and submission ID.
IF a receipt exists:
    IF operation or payload hash differs:
        Reject as SUBMISSION_CONFLICT.
    ELSE:
        End this transaction and return the original saved response.
        Replay no effects.

Load required records and prerequisites.
IF a record is missing:
    Reject with the mapped missing-record error.
IF an expected version differs:
    Reject as STALE_RECORD with the latest saved representation.

Execute the approved mutation callback using this connection.
Write its required histories and references.
Initialize created record versions at 1.
Increment each successfully mutated record's version.
Build the resulting response with generation and saved versions.
Insert the response receipt in the same transaction.
COMMIT.
Return success only after commit.
```

Receipt lookup precedes version and preview checks.
A committed retry remains valid after response loss, preview expiry, or process restart.
Generation validation still precedes receipt replay.
State changes: Mutation, histories, resulting versions, and receipt commit together.
Failures/retries: Rejections and write failures follow PR-02's rollback path.
No partial mutation or receipt remains after failure.
An unchanged user retry retains its ID and payload. Changed drafts use a new submission ID.

STALE_RECORD preserves the draft and exposes the latest saved representation.
Explicit Review latest invalidates the old expected version.
The user confirms intended fields against the latest record before creating a new command.

Error interface: {code, message_key, details, generation_id}.
Use 422 for invalid/domain input, 404 for missing records, and 409 for stale/conflicting submissions.
Use 503 for busy stores and 500 for rolled-back persistence failures.
Mapping: AC-INFRA-001, AC-INFRA-002, AC-INFRA-008.
Actual asset/ticket/import behavior and recorder checks remain downstream obligations.

#### PR-04: Atomically reset the shared store — f001c

Inputs: POST /api/reset with current generation_id and strict confirm=true.
Outputs: New generation and committed empty-store counts, or structured failure.
Reset uses its separate contract. It has no submission receipt.

```text
Reject absent/false confirmation, invalid generation, or extra fields.
Enter PR-02's write transaction.
Read the current generation.
IF the supplied generation differs:
    Reject as STALE_STORE without deleting anything.

Remember the old generation.
Delete tables in this exact order:
    command_receipts
    override_history
    invoice_update_refs
    invoice_updates
    maintenance_history
    maintenance_tickets
    invoice_items
    baseline_coordinates
    uploads
    observations
    asset_baselines
    assets
    rooms
    properties

Generate a fresh UUID distinct from the old generation.
Update only store_metadata.generation_id.
Compute empty-store counts within this transaction.
COMMIT.

Invoke PR-05 with the old generation.
Return the new generation and committed counts.
```

State changes: Clear all domain records, evidence, histories, and receipts, and replace generation atomically.
Retain schema version, database file, static configuration, and browser language/currency preferences.
Reset is the sole approved destructive exception to evidence/history preservation.
Failures/retries: Any deletion, metadata update, or commit failure restores all previous rows and generation.
Busy/failure responses preserve retry input.
A lost-response retry retains the original generation.
If reset committed, that retry returns STALE_STORE and cannot delete a subsequently imported portfolio.
Never silently substitute the latest generation and resend reset.
Mapping: AC-DEMO-001, AC-INFRA-004, AC-INFRA-005, AC-INFRA-006.

#### PR-05: Invalidate previews by generation after commit — f001c/f002c hook

Inputs: Successfully committed reset's old generation and registered preview-eviction hook.
Outputs: Removal of matching preview entries without removing new-generation entries.

```text
Run the hook only after reset commits.
Acquire the preview registry's own lock.
Remove entries whose generation equals the old generation.
Keep every other generation's entries.
Release the lock.
```

f001c establishes the hook seam. f002c supplies the actual registry and full race tests.
Do not implement workbook parsing or preview planning in f001.
State changes: Evict old-generation process entries only after database commit.
Database generation checks remain authoritative.
Old previews cannot commit if cleanup is delayed or an old preview appears during a race.
Failures/retries: Cleanup cannot undo a committed reset or produce a false rollback claim.
Record cleanup failure locally while generation guards continue blocking obsolete confirmations.
Mapping: AC-INFRA-005.
Full preview lifecycle and receipt replay verification remains with f002c under AC-INFRA-007.

#### PR-06: Present reset and invalidate browser context — f001c

Inputs: Current generation, loaded drafts/versions, request sequences, configuration date, and explicit user actions.
Outputs: Cancelled reset, pending/error state, confirmed empty Overview, or invalid retained drafts.

```text
Route reset through the shared state module and request helper.
IF a form is dirty:
    Offer Continue editing or Discard changes.
    Continue editing cancels the attempted transition.
    Discard permits opening reset confirmation.

Explain deletion of all shared records, evidence, and histories.
Offer Cancel and Reset data.
Cancel sends no command.

On explicit Reset data:
    Capture the current generation.
    Disable duplicate submission.
    Send one reset request with confirm=true.
    Perform no automatic write retry.

On confirmed success:
    Adopt the returned generation.
    Invalidate outstanding reads from the previous context.
    Clear initiating-tab drafts, previews, selection, and reporting context.
    Open empty Overview.
    Initialize reporting date from the server's Hong Kong today.
    Preserve independent language/currency preferences.

On confirmed rollback/busy failure:
    Show failure and retain retry input.
    Do not announce success.

On transport failure with an unknown outcome:
    Explain that the result is unconfirmed.
    Re-read configuration.
    Keep any retry bound to the originally submitted generation.

On another tab's focus, request, and before writes:
    Check current generation.
    If changed, invalidate obsolete reads and previews.
    Preserve old draft text visibly until explicit discard.
    Disable saving that obsolete draft.
    Explain the shared-store reset.

Accept read results/errors only for the active request sequence and context.
```

Browser checks supplement server guards.
An intervening reset cannot bypass the server's transactional generation comparison.
State changes: Confirmed reset clears initiating-tab context. Other tabs retain invalid drafts until discard.
Ordinary successful commands refresh affected saved representations.
Browser code never invents saved counts, histories, or versions.
Failures/retries: Preserve input on known failure. Distinguish unknown transport outcomes from confirmed rollback.
Never retry a write automatically or retarget an old reset to the new generation.

General preference persistence, session/new-tab dates, translation fallback, configuration validation, and finance diagnostics retain their separate Finance/display approval.
Repeat full room-response sequencing when room reads exist.
Mapping: AC-INFRA-003, AC-INFRA-004, AC-INFRA-005, AC-INFRA-006, AC-DEMO-001, AC-DEMO-002.
Also map AC-UX-001/013/017/019 and their IX companions.

### Planned verification and deferred evidence

At submission, all application checks were NOT RUN. Current foundation results and deferred checks are recorded in the [f001 report](jobs/feature-job-reports/f001-report-local-runtime.md).
U/I/B/M retain their definitions from verification-plan.md.

| Coverage | Required methods and mapped IDs | Completion limit |
|---|---|---|
| Store/init/restart | I/B/M: AC-DEMO-002, AC-DEMO-005 | I foundation after implementation. B/M startup waits for f001c. Full journeys remain downstream. |
| Coordinator/version/receipt | I/B: AC-INFRA-001, AC-INFRA-002, AC-INFRA-008 | I foundations in f001. Actual feature B checks remain downstream. |
| Reset/cancel/rollback | I/B: AC-INFRA-004, AC-INFRA-005. I: AC-INFRA-006. I/B/M: AC-DEMO-001 | Real registry race repeated in f002c. |
| Browser sequencing | B: AC-INFRA-003 | Primitive checks in f001c. Repeat real room reads in f004c. |
| Shell/reset interaction | B/M: AC-UX-001, AC-UX-013, AC-UX-015, AC-UX-016, AC-UX-017, AC-UX-019 | Shell/reset surfaces only. Missing feature subcases stay NOT RUN. |
| Interaction companions | B/M: IX-UX-001, IX-UX-013, IX-UX-015, IX-UX-016, IX-UX-017, IX-UX-019 | Companion cases retain consuming-view obligations. |
| Separately gated foundations | U/I: AC-US01-006, AC-US01-007. I/B: AC-US02-010, AC-INFRA-009 | Imports/observations/maintenance rules are not approved here. |
| Separately gated configuration/display | U/I/B: AC-US05-009. I/B/M: AC-US02-016, AC-US02-017, AC-US02-019 | Requires Finance/display review and applicable downstream integration. |
| Preview lifetime/retry | I/B: AC-INFRA-007 | f002c supplies real registry/confirmation evidence. |

Prepare each test independently in a temporary on-disk store using production helpers.
Automated checks never reset runtime/app.sqlite3.
Use test_<scenario_id_lowercase_with_underscores> entry names.
Include these cases:

1. Empty initialization, repeated initialization, foreign-directory launch, unsupported schema, and migration rollback.
2. Constraint rejection and multi-query snapshot consistency.
3. Receipt replay after reopen and changed-operation/payload conflicts.
4. Generation validation before receipt, record, version, or preview lookup.
5. Failures after initial writes and before history/receipt completion.
6. Reset failure during deletion, with all previous rows and generation restored.
7. Locks exceeding five seconds, with unchanged rows, histories, versions, receipts, and generation.
8. Cancelled reset, successful deletion, retained preferences/configuration, obsolete-tab drafts, and lost-response retries.
9. Generation-selective cleanup with a concurrently present new-generation preview entry.

During later execution, use pinned Python/pytest and mapped browser commands from demo.md.
Use targeted compileall as syntax verification, not lint or typechecking.
Lint/typecheck/count remain NOT RUN because configured equivalents are absent under approved S-03.
Application tests, compileall, browser/manual checks, startup, and rehearsal were not run during this documentation task.

Record manual installed-Chrome checks separately from automated Chromium.
Check 1440px, 1024px, 768px, and 360px, plus both sides of 1200px/600px breakpoints.
Defer absent feature-card and workflow subcases explicitly.
Evidence records require build/date, environment, independent setup, expected/actual results, status, and concrete omissions.
Keep generated evidence under ignored runtime/verification.

### Approval decision record

| Field | Current record |
|---|---|
| Submitted algorithm scope | PR-01–PR-06, Persistence/reset portions of f001a/f001b/f001c |
| Alex's scope selection | Persistence/reset only (Recommended), selected in the review conversation |
| Recording authorization | 2026-10-03: "PLEASE IMPLEMENT THIS PLAN", with the pending-approval boundary retained |
| Algorithm approval response | Alex: "approve pseudocode - directly work on the feature job as needed" |
| Algorithm approval date | 2026-10-03 |
| Approved algorithm scope | PR-01–PR-06, Persistence/reset portions of f001a/f001b/f001c, against the governing versions listed above |
| Other groups | All remain NOT SUBMITTED |
| Installation/job authorization | Alex's later response authorizes the feature job and its necessary dependencies. Other behavior-group gates remain. |

Runtime amendment approved by Alex on 2026-10-03:
"evaluate if we can use the current version of python as feasibility check, if can, ignore python 3.11".
Python 3.12.5 passes the dependency and SQLite feasibility checks recorded in the f001 series report.
Use Python 3.12.5 for delivery and P-02 checks. Python 3.11 is no longer a prerequisite.
This changes the interpreter target only. The approved algorithms, schema, and other group gates remain.

The approval is recorded before application changes.
Its scope is limited to the listed algorithms and governing document versions.
Request renewed approval for consequential deviations.
Keep ordinary choices within the approved design under the existing scope.

No f001 execution report/status/master artifacts existed at submission. Execution now maintains the designated series artifacts.
Task dependencies and coverage remain owned by tasks.md.
Post-edit documentation checks are recorded in implementation-planning-review.md.

## F001B shared boundary approval — FB-01–FB-03

Submitted and approved: 2026-10-03, before the remaining F001B implementation.
Alex's actual selection: **"Approve scoped pseudocode (Recommended)"**.
Execution authorization: Alex subsequently supplied **"PLEASE IMPLEMENT THIS PLAN"** with the complete F001B plan.

Authority: product/contracts/sample plan/assessment v0.5; technical design v1.1;
verification v1.0; UI v0.4; acceptance/glossary v0.2; task index v0.6;
approved P-01–P-05 and S-01–S-03. Python 3.12.5 remains the delivery runtime.
The job recommends High; the active effort is unavailable and its comparison is unverified.

Approved scope: shared request/response declarations, normalization, command preparation,
local owner/FX configuration, operational clock, and the P-03 diagnostic envelope.
No departure from the approved design. Workbook parsing/planning/confirmation, feature
mutations, financial calculations, routes, reset execution, and browser state remain
with their downstream jobs and approval gates. Declaring their contracts does not approve their algorithms.

```text
FB-01 — Shared input normalization
Inputs: JSON fields/workbook values, field name, optional source coordinates.
Outputs: canonical values or structured field diagnostics.
Reject unknown/protected fields per endpoint. Trim outer whitespace; preserve text
case, internal whitespace, and leading zeros. Reject numeric source identities.
Validate identity grammar, exact parent prefixes, and region/location agreement.
Normalize enums. Accept ISO/date-only Excel dates; reject ambiguous/timed values.
Normalize finite non-negative amounts to equal decimal strings without rounding;
reject booleans/non-finite/invalid syntax. Require positive integral month counts.
Reject installation before purchase when both dates are available.
Normalize observations independently: all absent or UNKNOWN without metadata is
unassessed UNKNOWN; recorded states require status/date/recorder; reject incomplete
or note-only metadata. Invalid values return INVALID_INPUT/422 with field/source
details. Normalization changes no saved state.

FB-02 — Typed endpoint boundaries
Inputs: technical-design section 5 requests and saved response representations.
Outputs: strict Pydantic models and normalized commands.
Require canonical generation/submission UUIDs and positive expected edit versions.
Reject unexpected and endpoint-protected identity/cost/status/timestamp fields.
PATCH omission preserves fields; explicit null clears only nullable fields.
Require recorder/reason/resolution text where specified. Preserve decimal strings,
ISO dates, canonical enums, nulls, and omission-versus-null command hashing.
Cross-field PATCH checks use merged saved values inside downstream transactions.
Use PR-03 unchanged: generation, receipt replay/conflict, versions/prerequisites,
atomic mutation/history/version/receipt, commit, response. No feature callbacks here.
Preserve existing errors/latest saved stale-record values and caller drafts.

FB-03 — Configuration and operational clock
Inputs: versioned local owner/FX data and injected aware clock.
Outputs: validated configuration, Hong Kong date/time, UTC persisted instants,
or configuration diagnostics. Use approved owners, five rates dated 2026-10-03,
fictional disclaimer, and delivered English. Validate unique identities/currencies,
complete rates, positive finite values, valid FX date, USD=1. Reject naive clocks.
Derive operational today in Asia/Hong_Kong independently of financial reporting date.
Finance envelope: status VALID or INVALID_CONFIGURATION, diagnostics list,
typed results or null on invalid configuration. Preserve operational/config reads.
Never fabricate partial totals or change source values on configuration failure.
```

Acceptance/check mapping: AC-US01-006/007, AC-US02-010, AC-US05-009,
AC-INFRA-001/002/008/009. F001B verifies foundation portions only; parser, feature,
HTTP and browser portions remain NOT RUN until their owning jobs execute.
State/transactions: validation/config/clock helpers write nothing; command writes
retain the single caller-owned PR-03 transaction and rollback/retry ordering.
Verification: named import/display unit cases and record integration cases, independent
temporary stores/values/aware clocks, F001A regressions, targeted compileall.
Record actual execution/evidence in the single F001 report/status and master row.

## F001C browser/display submission — FC-01–FC-03

Submitted and approved: 2026-10-03. Status: **APPROVED** before browser implementation.
Alex's actual response: **"Approve FC-01–FC-03 and implement F001C"**.
This submission completes only F001C's scoped Finance/display browser foundation.
PR-04–PR-06 remain approved. Financial calculations and later feature forms retain their gates.
Authority versions: product/contracts/sample plan/assessment/demo v0.5; design v1.1;
UI v0.4; acceptance/glossary v0.2; verification v1.0; tasks v0.6; approved P-01–P-05/S-01–S-03.
There is no proposed policy or architecture deviation. Active reasoning effort is unavailable.

```text
FC-01 — Browser context and preferences
Inputs: GET /api/config; browser storage; current hash; explicit preference/date actions.
Outputs: one tab context, independent preferences, labelled operational/reporting dates.
Validate stored values before use. Default to English/USD. Offer delivered dictionaries only.
Persist language and currency separately in localStorage; neither changes the other.
Render interface keys through the English dictionary with English fallback.
Never translate source/user text or calculate financial amounts in the browser.
Store navigation, filters, search, Map/List, selection, return/scroll context and date in sessionStorage.
Use a tab identity and live-tab ownership handshake to reject cloned session context.
A fresh tab starts Overview with the server's Hong Kong today, even with copied storage.
Reload/same-tab navigation retains valid context and reporting date.
Custom date validates an ISO calendar date. Reset to today rereads server configuration.
Preference/date changes write no database state, evidence, history or command receipt.
Unavailable storage uses in-memory state and visible persistence feedback.
Configuration/network failure shows Retry and no invented date, generation or totals.
Invalid FX preserves config/assumptions access and displays existing diagnostics.

FC-02 — Shared state and request integration
Inputs: route actions, loaded versions/generation, drafts, request results/errors, tab focus.
Outputs: current-route rendering, retained drafts, guarded transitions and sequenced results.
Own drafts and request sequences in one state module; use one request helper.
Before navigation/closure/reset, offer Continue editing or Discard changes for dirty drafts.
Continue cancels transition; Discard clears the draft and completes the requested transition.
Hash destinations are Overview, Maintenance, Import and Debugging - Assumptions.
Keep reporting/filter/search/representation context; destination changes close selection/card.
On focus/request and before writes, reread generation through configuration.
Changed generation invalidates pending reads/previews and marks old drafts unsavable.
Keep obsolete draft text until explicit discard. Never replace its generation/version silently.
Accept results/errors only for the active request sequence and captured context.
Writes use captured generation and draft versions; disable duplicates and never auto-retry.
Retain unchanged command ID/payload for explicit retry; edited drafts need a fresh ID.
PR-06 reset uses captured generation without receipts, including unknown-outcome retries.
Known rollback retains retry input. Unknown outcome rereads config and announces uncertainty.
Confirmed reset clears initiating-tab context and opens Overview with server today.
State writes are browser-only. Server mutations still use PR-02/PR-04 transactions.

FC-03 — Shell and assumptions
Inputs: config/diagnostics, approved rules, active route, feedback and explicit dialog actions.
Outputs: local English shell, read-only assumptions, accessible reset and dirty dialogs.
Use 16px system type, 8px spacing, beige/white/neutral panels and blue primary actions.
Use semantic labels/headings, live feedback, visible focus and text status meanings.
At 1200px use 200px navigation and a reusable roughly 400px card primitive.
Below 1200px use top navigation and bounded overlays; at <=600px stack fields/full-width overlays.
Focus dialog/card headings; restore trigger focus on close. Trap modal/overlay focus only.
Escape follows dirty protection. beforeunload uses the standard browser prompt.
Show baseline initialization guidance; downstream workflow shells disclose availability honestly.
Display approved assumptions/source references, actual owners/rates/date/disclaimer and AR-002 gap.
Never fabricate portfolio counts or report values before their server endpoints exist.
Reset confirmation explains shared record/evidence/history deletion; Cancel sends no write.
Use PR-04 exact deletion order and post-commit generation-selective PR-05 eviction hook.
Hook failure logs locally and cannot claim that committed reset rolled back.
```

Validation/check mapping: AC-US02-016/017/019; AC-UX-001/013/015/016/017/019 and their IX companions;
AC-DEMO-001/002/005; AC-INFRA-003/004/005/006. Use isolated production API/browser helpers.
Check reload/new-tab storage cloning, preferences, dirty drafts, reverse reads, reset failures,
unknown reset outcome, stale-tab writes, keyboard/focus and all specified widths/breakpoints.
Record Chromium and installed Windows Chrome separately. Missing consuming feature subcases
and the F002C preview race remain NOT RUN. Approval covers only the recorded scope.

# f001 local runtime execution report

Updated: 2026-10-03. Series status: **implemented**.
Verified build: `62c1f78` plus F001C implementation changes. Git history identifies the release commit. [Detailed status](f001-status-local-runtime.md).

Execution follows the [recorded Persistence/reset approval](../../pseudocode-review.md#approval-decision-record) and approved P-01–P-05 / S-01–S-03 adaptations.
Python 3.12.5 is the approved tested runtime; Python 3.11 is no longer required. SQLite is 3.45.3 on Windows 11 build 26200.
All f001 jobs recommend GPT-6.1 Sol High. Active reasoning effort is not exposed; the comparison is unverified.

## Execution log

### 2026-10-03 — f001a: persistence foundation

- Implemented version-1 schema, immutable evidence guards, caller-owned transactions, five-second busy timeout, read snapshots, and atomic migration. Initialization preserves supported stores and blocks unsupported or damaged stores.
- Added repository-relative `--init-db`, an injectable application/store/clock/configuration seam, isolated test fixtures, and exact dependency pins: 17 runtime packages and 36 runtime/development packages.
- Key surfaces: [store helper](../../../src/db/store.py), [schema](../../../src/db/schema.py), [launcher](../../../app.py), [runtime tests](../../../tests/integration/test_runtime.py), [fixtures](../../../tests/conftest.py), [runtime lock](../../../requirements.lock), [development lock](../../../requirements-dev.lock). README and demo initialization instructions were updated.
- Verification: **58 integration cases passed**. Manual non-destructive initialization from the repository and another directory retained the same path, schema, and generation. Browser startup remains assigned to f001c.

### 2026-10-03 — f001b: approved PR-03 portion

- Implemented canonical envelopes/payload hashing, generation checks before lookup, durable receipt replay before version/prerequisite checks, stale-version responses, and structured error/status mapping. Mutations, histories, versions, and receipts use one transaction; success is returned after commit.
- Key surfaces: [command coordinator](../../../src/services/commands.py), [service errors](../../../src/services/errors.py), [receipt queries](../../../src/db/command_queries.py), [coordinator tests](../../../tests/integration/test_records.py).
- Verification: **44 integration cases passed**, including response-loss replay after reopening, submission conflicts, concurrent duplicates, malformed input, lock timeout, and mutation/history/receipt/commit rollback.
- Remaining: endpoint-specific contracts, domain validators, owner/FX configuration, Hong Kong operational clock boundary, and P-03 diagnostics. Test mutation callbacks prepare independent fixture effects; production feature mutations are not implemented. Domain callbacks own version changes and histories on the supplied connection.

Setup history: uv provisioning/resolution failed with certificate/path errors; the declined Python 3.11 download was not retried. Standard pip installed pinned dependencies into an isolated `.venv`. No browser binaries were installed.

### 2026-10-03 — f001b: complete approved shared boundary foundations

- Recorded Alex's actual FB-01–FB-03 approval and implementation authorization before coding. Approval covers shared declarations/validators, local configuration, operational clock, and P-03 diagnostics only; all later mutation/calculation/parser/browser algorithms retain their gates.
- Added strict Pydantic request/response contracts for all 18 section-5 endpoints, field/source diagnostics, endpoint-owned command operation/allowlists, and response validation before effects/history/receipt commit. PATCH omission preserves values; explicit null clears nullable fields. Cross-field asset PATCH validation uses merged saved values on the caller's transaction boundary.
- Added shared text, exact source identity/parent/region, calendar, finite decimal, whole-month, enum, date-order, and observation metadata validators. Amount normalization is exact without context rounding; financial wire contracts separate unrounded strings from supplied formatted strings, preserving display trailing places.
- Added copied versioned fictional owner/FX configuration, owner selection validation, complete unique positive finite dated FX checks with USD=1, and an injected aware-clock boundary for Hong Kong today/offset and UTC instants. Invalid FX returns diagnostic/null financial results while configuration (including invalid settings), operational records, and stored source values remain readable and unchanged.
- Key surfaces: [contracts](../../../src/services/contracts.py), [validators](../../../src/services/validators.py), [configuration](../../../src/services/configuration.py), [clock](../../../src/services/clock.py), named import/display unit tests and record integration tests. Existing PR-03 ordering/transactions and original fixture bytes were preserved. App wiring remains F001C and consuming jobs.
- Latest verification: **346 passed**, 0 failed, 1 upstream Starlette/AnyIO warning, 18.65s. This includes 101 import-value cases, 128 display/contract/configuration cases, 59 record-boundary cases, and 58 F001A regressions. Targeted compileall and pip check passed; all four supplied workbook hashes match the inventory. Evidence: [output](../../../runtime/verification/4cdd533-f001b-completion/tests.txt), [JUnit](../../../runtime/verification/4cdd533-f001b-completion/tests.xml), [environment/commands](../../../runtime/verification/4cdd533-f001b-completion/environment.json).
- Initial unit iteration: 219 passed / 2 failed because PATCH round-trip test serialization included omitted fields as explicit nulls. Corrected the tests to use the approved `exclude_unset` serialization; subsequent implementation checks passed. No passing result is claimed for file/header parsing, feature mutations, actual HTTP endpoints, browser/manual, or end-to-end scenarios.

F001B is **implemented within its stated foundation acceptance limits**. F001 is still in progress.
Milestone completion is 2/3 F001 jobs (66.7%) and 2/21 project jobs (9.5%), counting only fully implemented jobs equally. This is not an effort estimate or full product-acceptance percentage.

### 2026-10-03 — f001c: browser shell and reset, partial acceptance

- Recorded Alex's actual response, "Approve FC-01–FC-03 and implement F001C", before browser coding. Implemented approved PR-04–PR-06 and the scoped display/browser foundation without changing product policies or dependencies.
- `python app.py` now serves one localhost Uvicorn worker, without reload. Added the typed configuration/reset endpoints, no-store responses, safe structured errors and a server-derived shell snapshot. Reset uses the existing transaction helper, exact FK deletion order and atomic generation replacement. Registry eviction runs only after commit and logs cleanup failure without falsely claiming rollback.
- Added the four hash destinations, mandatory English/fallback, read-only assumptions with actual configuration and AR-002 disclosure, preferences, tab-local context/date, cloned-tab protection, draft/version ownership and request sequencing. Reset retains preferences, clears initiating context, rejects obsolete drafts, and keeps unknown-outcome retry bound to its original generation. Added approved styling, focus/feedback, dirty dialogs and reusable responsive card primitives. Downstream workflows are explicitly unavailable.
- Key surfaces: [launcher](../../../app.py), [thin routes](../../../src/views/routes.py), [runtime service](../../../src/services/runtime.py), [reset queries](../../../src/db/reset_queries.py), [shell](../../../src/views/static/shell.js), [state](../../../src/views/static/state.js), [request helper](../../../src/views/static/request.js), [dictionary](../../../src/views/static/i18n.js), [runtime browser tests](../../../tests/browser/test_runtime.py), [UI browser tests](../../../tests/browser/test_ui.py).
- Final verification: **393 passed**, 0 failed, 1 upstream warning, 60.67s: 362 unit/integration and 31 Chromium browser cases. All eight widths/breakpoints passed. Coverage includes cancel, halfway/metadata/commit rollback, busy HTTP/retry, post-commit selective cleanup, stale tabs, lost reset responses, reverse results/errors, persistent-profile restart, actual isolated server-process restart, session cloning, dates, unavailable storage and keyboard/focus. [Output](../../../runtime/verification/62c1f78-f001c/tests.txt), [JUnit](../../../runtime/verification/62c1f78-f001c/tests.xml), [environment/commands](../../../runtime/verification/62c1f78-f001c/environment.json).
- An earlier 28-case suite also passed through installed Windows Chrome 154.0.8037.93 automation, 45.23s. Final added cases ran in Chromium 140.0.7339.16. This does not establish manual acceptance. The actual production launcher, foreign-directory initialization, unchanged demo state and all four workbook inventory hashes passed. [Startup evidence](../../../runtime/verification/62c1f78-f001c/startup.json). Compileall and pip check passed; lint/typecheck/count remain NOT RUN under approved S-03.
- Preserved failed attempts: Chromium cache initially required sandbox approval; verified download initially failed TLS. Exported Windows-trusted public roots locally and successfully retried with TLS verification enabled. The first combined run found duplicate test-module names; the allowed conftest importlib hook fixed collection. A later busy-reset test held the lock before startup; corrected setup to acquire it after startup. Failure output remains in the local evidence folder.
- Required manual Windows Chrome/assistive review is **NOT RUN**. Computer Use stopped because it could not determine the current browser URL confidently enough to enforce policy. No further desktop input was issued. F001C remains **partial**, rather than receiving completion credit. Automated keyboard/semantic checks do not claim screen-reader results.
- Documentation links/anchors, all sixteen F001C scenario references, consolidated status/percentage and whitespace passed the [local audit](../../../runtime/verification/62c1f78-f001c/documentation-audit.json). Planned dependencies, job specifications, schema, dependencies and supplied workbook bytes remain unchanged.

The spec-driven milestone remains **2/3 F001 jobs (66.7%)** and **2/21 project jobs (9.5%)**.
Partial jobs receive no credit. Full product acceptance and the AR-002 interpretation remain unresolved.

### 2026-10-03 — f001c: owner confirmation and demo guide

- Alex confirmed the remaining scoped F001C checks through the response **"all check passes."** This follows the explicit manual Chrome, layout, keyboard/focus and assistive-review checklist in this conversation. F001C is implemented within its foundation acceptance limits. No new agent manual run, device details, screenshots or screen-reader output are invented. The earlier tool stop remains historical evidence.
- Updated the [root README](../../../README.md) with ASD-STE100-style instructions for a first-time Windows user. It covers Python/project download, one-time setup, each-session startup, empty-store reset, available features, stop/restart and common failures. It clearly identifies downstream workflows as unavailable.
- Updated the single series status and master row. F001 is **3/3 jobs, 100%**. Project milestone completion is **3/21 jobs, 14.3%**, with equal job weighting. Later feature acceptance, the timed rehearsal and AR-002 assessor interpretation remain pending.
- Verification uses the existing **393-test PASS** because this follow-up changes documentation only. Local links, command paths, direct code counts, 20/25-word statement limits and whitespace passed the [release audit](../../../runtime/verification/62c1f78-f001c/release-documentation-audit.json). Formal ASD-STE100 dictionary compliance remains unverified; the supplied linter is unavailable. Owner confirmation is separate from automated assertion evidence and prior local scenario records.

## Verification evidence

The original 102-case foundation and F001B runs remain historical evidence below. The F001C entry above and scenario table below own current results.
Tests use independent temporary on-disk stores, production persistence helpers, and explicit clocks. Automated checks never write or reset the demonstration store.

| Check | Recorded result | Evidence / limitation |
|---|---|---|
| Combined pytest | **102 passed**, 0 failed, 1 warning, 17.65s | [Output](../../../runtime/verification/4cdd533-f001/foundation-tests.txt), [JUnit](../../../runtime/verification/4cdd533-f001/foundation-tests.xml). |
| F001B completion + F001A regressions | **346 passed**, 0 failed, 1 warning, 18.65s | [Output](../../../runtime/verification/4cdd533-f001b-completion/tests.txt), [JUnit](../../../runtime/verification/4cdd533-f001b-completion/tests.xml). |
| F001B targeted compileall / pip check / fixture hashes | **PASS** | [Environment, exact commands and four workbook hashes](../../../runtime/verification/4cdd533-f001b-completion/environment.json). |
| Targeted compileall | **PASS**, exit 0 | [Environment and command](../../../runtime/verification/4cdd533-f001b/environment.json). Syntax check only. |
| pip check / imports / P-02 multipart and timezone | **PASS** | [Environment](../../../runtime/verification/4cdd533-f001a/environment.json), [installed versions](../../../runtime/verification/4cdd533-f001a/package-versions.json). |
| Manual initialization/reinitialization | **PASS** | [Initial launch](../../../runtime/verification/4cdd533-f001a/init-db.txt), [other-directory launch](../../../runtime/verification/4cdd533-f001a/init-other-directory.txt). |
| Documentation / pins / fixtures | **PASS** at implementation | [Audit](../../../runtime/verification/4cdd533-f001/final-audit.json); four workbook hashes preserved. |
| Lint / typecheck / count | **NOT RUN** | No configured equivalents; approved S-03. |
| Chromium / installed Chrome / responsive / linguistic / rehearsal | **NOT RUN** | Shell and workflows are not delivered. Chrome 154.0.8037.93 was a prerequisite observation only. |

The single warning is an upstream Starlette TestClient/AnyIO deprecation.

| Scenario | Passing foundation evidence | Remaining acceptance |
|---|---|---|
| AC-DEMO-002 | [Store durability](../../../runtime/verification/4cdd533-f001a/AC-DEMO-002/result.json) | Completed-workflow and browser/process restart. |
| AC-DEMO-005 | [Initialization/lifespan/CLI](../../../runtime/verification/4cdd533-f001a/AC-DEMO-005/result.json) | Working shell and second-host setup. |
| AC-INFRA-001 | [Stale-version coordination](../../../runtime/verification/4cdd533-f001b/AC-INFRA-001/result.json) | Actual asset/ticket services and browser review. |
| AC-INFRA-002 | [Durable receipt replay](../../../runtime/verification/4cdd533-f001b/AC-INFRA-002/result.json) | Maintenance creation service, CREATE event, and card. |
| AC-INFRA-008 | [Store atomicity](../../../runtime/verification/4cdd533-f001a/AC-INFRA-008/result.json), [command atomicity](../../../runtime/verification/4cdd533-f001b/AC-INFRA-008/result.json) | Consuming feature HTTP/browser failures. |

Foundation PASS does not complete a full scenario. The remaining acceptance checks above are NOT RUN.

### F001B completion scenario evidence

Each linked record states build/date, method, independent setup, expected/actual results, environment, and explicit completion limits. Tests use actual normalization/contracts/transaction helpers; fixture callbacks do not implement production feature mutations.

| Scenario | Current scoped evidence | Deferred methods/surfaces |
|---|---|---|
| AC-US01-006 | [PASS — U/I shared value validation and unchanged-store boundary](../../../runtime/verification/4cdd533-f001b-completion/AC-US01-006/result.json) | Actual workbook/preview/confirmation in F002. |
| AC-US01-007 | [NOT RUN — parser absent](../../../runtime/verification/4cdd533-f001b-completion/AC-US01-007/result.json); import boundary shape checks passed separately | File/readability/header/sheet/formula/merged-cell U/I methods in F002A. |
| AC-US02-010 | [PASS — U/I metadata rejection and unchanged saved observations](../../../runtime/verification/4cdd533-f001b-completion/AC-US02-010/result.json) | Actual observation save and HTTP/B presentation in F004. |
| AC-US05-009 | [PASS — U/I invalid FX, null finance, readable config, preserved source state](../../../runtime/verification/4cdd533-f001b-completion/AC-US05-009/result.json) | Calculation/reporting integration and browser in F003/F004. |
| AC-INFRA-001 | [PASS — I typed stale command/latest saved values](../../../runtime/verification/4cdd533-f001b-completion/AC-INFRA-001/result.json) | Actual asset/ticket services and browser Review latest. |
| AC-INFRA-002 | [PASS — I typed durable replay after reopen](../../../runtime/verification/4cdd533-f001b-completion/AC-INFRA-002/result.json) | Actual ticket creation, CREATE history and card. |
| AC-INFRA-008 | [PASS — I busy/atomic response/history/receipt failures](../../../runtime/verification/4cdd533-f001b-completion/AC-INFRA-008/result.json) | Consuming HTTP/B failure/input presentation. |
| AC-INFRA-009 | [PASS — U/I recorder contracts for four actions with no writes](../../../runtime/verification/4cdd533-f001b-completion/AC-INFRA-009/result.json) | Actual maintenance actions/attributed histories/HTTP/B in F005. |

## Remaining scope

F001B foundations are complete following the scoped FB-01–FB-03 approval.
F001C is implemented under the FC-01–FC-03 approval and Alex's later confirmation that all remaining scoped checks passed.
The full preview-registry race repeats in F002C. Actual room-read sequencing repeats in F004C.
Imports, observations/reporting, maintenance, assets/overrides and financial calculations/views remain undelivered. [Task order](../../tasks.md) retains dependency ownership.
AR-002 manual asset creation remains unmet; assessor acceptance of the maintenance reinterpretation is unconfirmed.
The current release is prepared for Alex's authorized GitHub push and pull request.

### F001C scenario evidence and acceptance limits

Each record includes build/date, environment, independent setup, expected/actual outcome, assertions and concrete omissions.
The table below preserves the agent-run results before Alex's later completion confirmation.
Its M omissions are historical. The owner confirmation closes scoped F001C manual checks only.
Downstream methods remain deferred. Existing local JSON records are not rewritten to fabricate new agent evidence.

| Scenario / companion | Scoped evidence | Remaining methods/surfaces |
|---|---|---|
| AC-DEMO-001 | [Reset/empty shell](../../../runtime/verification/62c1f78-f001c/AC-DEMO-001/result.json) | M and full import/rehearsal journey. |
| AC-DEMO-002 | [Lifecycle/process restart](../../../runtime/verification/62c1f78-f001c/AC-DEMO-002/result.json) | M and completed consuming workflows. |
| AC-DEMO-005 | [Lifespan/launcher](../../../runtime/verification/62c1f78-f001c/AC-DEMO-005/result.json) | M and second-host clean installation. |
| AC-INFRA-003 | [Late results/errors](../../../runtime/verification/62c1f78-f001c/AC-INFRA-003/result.json) | Actual room A/B reads in F004C. |
| AC-INFRA-004 | [Cancel/rollback/busy/retry](../../../runtime/verification/62c1f78-f001c/AC-INFRA-004/result.json) | Implemented reset surface I/B passed. |
| AC-INFRA-005 | [Old drafts/selective hook](../../../runtime/verification/62c1f78-f001c/AC-INFRA-005/result.json) | F002C actual preview/reset race. |
| AC-INFRA-006 | [Lost response/old retry](../../../runtime/verification/62c1f78-f001c/AC-INFRA-006/result.json) | Portfolio prepared independently through SQL; importer remains downstream. |
| AC-US02-016 | [Independent persistent preferences](../../../runtime/verification/62c1f78-f001c/AC-US02-016/result.json) | M. |
| AC-US02-017 | [English/fallback](../../../runtime/verification/62c1f78-f001c/AC-US02-017/result.json) | M; translations not delivered, linguistic review conditional. |
| AC-US02-019 | [Session/date/cloning](../../../runtime/verification/62c1f78-f001c/AC-US02-019/result.json) | M. |
| AC-UX-001 / IX-UX-001 | [Navigation/dirty context](../../../runtime/verification/62c1f78-f001c/AC-UX-001/result.json) | M and actual feature forms. |
| AC-UX-013 / IX-UX-013 | [Feedback/storage/pending](../../../runtime/verification/62c1f78-f001c/AC-UX-013/result.json) | M; downstream filter/upload/field-error states. |
| AC-UX-015 / IX-UX-015 | [Shell styling](../../../runtime/verification/62c1f78-f001c/AC-UX-015/result.json) | M and consuming feature UI. |
| AC-UX-016 / IX-UX-016 | [Eight widths/card primitive](../../../runtime/verification/62c1f78-f001c/AC-UX-016/result.json) | M and actual room/Log fault forms. |
| AC-UX-017 / IX-UX-017 | [Keyboard/focus/dirty Escape](../../../runtime/verification/62c1f78-f001c/AC-UX-017/result.json) | M, screen reader, actual room controls. |
| AC-UX-019 / IX-UX-019 | [Read-only assumptions/config](../../../runtime/verification/62c1f78-f001c/AC-UX-019/result.json) | M and financial calculation integration in F003C. |

# Approved local technical design

Version: 1.0

Approved: 2026-10-03 by Alex through the planning answers and instruction to proceed.

Status: Implementation guidance ready. Application implementation and verification: NOT RUN.

[Product behavior](product-spec.md), [input contracts](data-contracts.md), and [UI requirements](ui-ux-spec.md) govern this design.
[Verification](verification-plan.md) defines completion evidence. [Runtime procedures](demo.md#6-local-runtime-procedures) define future commands.

## 1. Stack, ownership, and trade-offs

Use one local FastAPI application, one Uvicorn worker, and one SQLite file.
Bind to 127.0.0.1:8000. The browser communicates with this application through same-origin JSON endpoints.
Operation requires no external API, key, hosting account, database server, font CDN, or translation service.
Initial installation requires package access. Later operation uses installed packages and local assets.

| Component | Selected implementation | Responsibility |
|---|---|---|
| Entry point | app.py exports a FastAPI app and a local command-line launcher | Startup and command argument handling. |
| Presentation | src/views contains HTML, CSS, JavaScript modules, and thin route handlers | Render server results and submit typed commands. |
| Services | src/services contains synchronous Python functions | Validation, import planning, calculations, and permitted transitions. |
| Persistence | src/db uses Python sqlite3 | Parameterized queries, connection settings, transactions, schema version, and histories. |
| Boundaries | Pydantic request/response models | Validate JSON shape. Domain services own business rules. |
| Workbooks | openpyxl with data_only=False | Read types, formulas, sheets, headers, rows, and merged cells. |
| Local serving | Uvicorn, one worker | Serve the application and local assets. |
| Verification | pytest, HTTPX, pytest-playwright | Unit, service/database/API, and browser checks. |

Alex owns scope, pseudocode approvals, and linguistic review. The implementing agent owns code, checks, and accurate evidence.
Exact dependency versions must be recorded in a tested lock file during implementation. Do not use broad untested upgrades for delivery.
Target Python 3.11. Use standard synchronous handlers for workbook and SQLite operations.
Create, use, and close each connection in the same synchronous operation. Keep check_same_thread=True.

SQLite avoids a separate service and supports the required local transactions.
Its single-writer limit fits the prototype. Multiple browser tabs are supported through locks and stale-write checks.
Plain browser modules avoid a frontend build pipeline. Explicit state ownership compensates for the absence of framework state management.
JSON endpoints are internal interfaces, not an external integration or a public API compatibility promise.
One process is required because preview storage is process-local. Concurrent processes and network hosting are outside this delivery.

Use no ORM, connection pool, background job queue, live push connection, derived-result cache, or generic event-sourcing framework.
Keep the default SQLite DELETE journal mode. Add complexity only after evidence and renewed design approval.

## 2. Data representation and schema

Store IDs and enums as canonical text. Store calendar dates as ISO YYYY-MM-DD strings.
Store actual instants as UTC ISO strings with Z. Display their Asia/Hong_Kong offset explicitly.
Use UUID text for generated upload, event, ticket, submission, and store-generation identities.
Whole-month lives and versions are integers. Versions start at 1 and increase after each successful record mutation.

Store amounts as canonical decimal strings. Parse and calculate with Decimal in services.
Use Decimal precision 28 with ROUND_HALF_UP. Do not quantize intermediate results or totals for display.
Quantize only displayed values: JPY to zero places and other local currencies/USD to two places.
Return decimal strings through JSON. Browser code displays these strings and never recomputes financial values.
Database numeric SUM over stored money is prohibited because SQLite coercion can lose decimal precision.

The following logical schema fixes ownership and relationships. SQL migrations implement these columns and constraints.
Snapshot JSON contains exactly the six fields defined in the input contract. JSON is canonical UTF-8 with sorted keys.
History JSON is an immutable event snapshot. It contains values needed to explain the action, not a replay engine.

| Table | Key and stored information | Relationships and constraints |
|---|---|---|
| store_metadata | Singleton key 1, schema_version, generation_id | Schema version starts at 1. Generation changes only on reset. |
| properties | property_id, property_name, location, city | Immutable property baseline. Valid location CHECK. |
| rooms | room_id, property_id, room_number, baseline_assessments_json | Immutable room baseline. FK property. UNIQUE(property_id, room_number). |
| assets | asset_id, room_id, facility_type, asset_name, purchase_date, installation_date, useful_life_months, applied_invoice_date, source_cost, source_currency, override_cost, override_currency, version | FK room. UNIQUE(room_id, facility_type). Three-category CHECK. Positive life CHECK. Override pair both NULL or both present. Supported-currency CHECKs. |
| asset_baselines | asset_id, snapshot_json | One immutable baseline per asset. FK asset. |
| observations | room_id, system, status, observed_on, recorder, note, version | Composite primary key. FK room. Three-system/status CHECKs. Recorded metadata required. Unassessed UNKNOWN has no metadata. |
| uploads | upload_id, workflow, filename, imported_at | ASSETS/INVOICES CHECK. Created only when an import commits new evidence/entities. |
| baseline_coordinates | upload_id, row_number, sheet, property_id, room_id, asset_id | Primary key(upload_id, row_number). FKs to all referenced entities/upload. One accepted baseline row preserves all three contributing identities. |
| invoice_items | invoice_id, line_id, asset_id, room_id, facility_type, snapshot_json, invoice_date, supplier_name, upload_id, sheet, row_number | Composite primary key. FKs asset/room/upload. Immutable normalized source values and provenance. |
| invoice_updates | event_id, asset_id, invoice_date, before_json, after_json, upload_id, happened_at | FKs asset/upload. Includes operational fields, source pairs, overrides, effective pairs, and previous applied date. |
| invoice_update_refs | event_id, role, invoice_id, line_id | Primary key across four columns. FKs event and invoice item. BEFORE/AFTER role CHECK. |
| override_history | event_id, asset_id, action, before_json, after_json, reason, recorder, happened_at, invoice_update_id | FKs asset and optional invoice update. SET_OVERRIDE/RESET_TO_SOURCE/CLEAR_ON_INVOICE CHECK. |
| maintenance_tickets | ticket_id, room_id, asset_id, description, severity, status, owner_id, target_date, opened_at, updated_at, resolved_at, resolution_note, version | FK room and optional asset. Enum CHECKs. IN_PROGRESS/RESOLVED require owner. RESOLVED requires note/time. |
| maintenance_history | event_id, ticket_id, action, before_json, after_json, recorder, happened_at, resulting_version | FK ticket. UNIQUE(ticket_id, resulting_version). CREATE/EDIT/START/RESOLVE CHECK. |
| command_receipts | generation_id, submission_id, operation, payload_hash, response_json | Primary key(generation_id, submission_id). Recorded with a successful mutation for safe response-loss retries. |

Use NOT NULL for required fields and CHECK(trim(value) <> '') for required text.
Use parameterized SQL. All foreign keys use ON DELETE RESTRICT.
Services validate decimal grammar, calendar validity, identifier parents, category completeness, and ticket same-room links before writing.
Check these cross-record rules inside the write transaction. Do not weaken them to fit a supplied fixture.
Return source evidence from baselines/invoice items. Return current operational fields from assets.
Resolve effective values through the override/source rule. Derive financial outputs and aggregates on request.
Read equivalent current invoice references from immutable items at the applied date. Later historical-only evidence does not rewrite applied events.
Preserve all contributing baseline coordinates. Skips leave original provenance untouched.

Owners are fixed configuration identities owner-alex, owner-mei, and owner-sam.
Their fictional labels are Alex Chan, Mei Wong, and Sam Lee. They are not authenticated accounts.
Use one versioned local configuration module for owners and FX. Use local language dictionaries for interface text.
FX as_of_date is 2026-10-03. Rates are HKD 0.128, SGD 0.74, GBP 1.25, JPY 0.0067, USD 1.
Validate the full five-rate configuration before complete financial reporting. Display its fictional disclaimer.

## 3. Connections, commands, and reset

One connection helper sets PRAGMA foreign_keys=ON and a five-second busy timeout before opening transactions.
Use sqlite3 isolation_level=None and explicit BEGIN IMMEDIATE for writes. Each transaction helper commits, rolls back, and closes explicitly.
Read-only requests use a short read transaction when multiple queries must describe the same snapshot.
Acquire the connection inside the synchronous operation, not in a separate dependency thread.
Nested service calls share the caller's connection. They neither open another transaction nor commit independently.
Schema initialization runs before serving, using one versioned migration transaction. A newer unsupported schema blocks startup.
Starting an existing version-1 store never reseeds or resets it. The database path resolves relative to the repository root.

Each record/import mutation receives generation_id and a UUID submission_id. Reset uses its separate generation-guarded contract.
Inside the transaction, check the generation first. Then check for an existing command receipt.
An identical operation/payload returns the original response without replay. Reused IDs with different content return SUBMISSION_CONFLICT.
Otherwise check record versions and business prerequisites, write the mutation/history, and save its response receipt atomically.
Receipt matching precedes version checks so a committed command remains retryable after its first response was lost.
Buttons are disabled during submission. This presentation safeguard supplements durable receipts.
Failed transactions create no receipt. Retry uses the same ID and same payload until the user changes the draft.
No automatic retries apply to writes. A lock timeout returns STORE_BUSY and preserves input.

Update records using their expected version. A mismatch returns STALE_RECORD with the latest saved representation.
The browser preserves the unsaved draft and offers Review latest. Review invalidates its old expected version.
After explicit review, the user re-enters/confirms the intended fields against the latest record and submits a new command.

Reset receives confirm=true and the current generation_id. It uses the same write transaction helper.
Delete command_receipts, override_history, invoice_update_refs, invoice_updates, maintenance_history, and maintenance_tickets first.
Then delete invoice_items, baseline_coordinates, uploads, observations, asset_baselines, assets, rooms, and properties.
Generate a new generation_id in the same transaction. Retain schema version, database file, and static configuration.
Rollback preserves all previous data if any deletion fails. Commit invalidates old drafts and previews across all tabs.
Evict previews from the old generation after commit. Keep new-generation previews created concurrently after reset.
Every confirmation checks generation, so reset races cannot bypass invalidation.
A repeated reset request with the old generation fails as STALE_STORE and never resets a newly imported portfolio.
Reset intentionally removes preserved evidence/history. This is the sole approved destructive demonstration exception.

## 4. Import planning and confirmation

Parse each uploaded workbook once with data_only=False. Capture normalized immutable rows and all source diagnostics.
Use one plan_import(rows, saved_state) service for preview and confirmation. It validates every row and computes deterministic effects.
Its result includes diagnostics, source identities/targets, inserts, updates, histories, skips, warnings, and before/after field changes.
Deterministic comparison excludes generated IDs and actual commit timestamps. It includes all reviewed effects and before-values.

Preview creates no database records. Return an opaque UUID preview_id tied to workflow, generation, normalized rows, and reviewed plan.
Keep a thread-safe process registry with a thirty-minute lifetime and at most twenty previews.
Expired/evicted/restarted previews require upload and review again. File/workflow changes invalidate the browser's prior preview.
Store no raw workbook on disk. Preserve filename/coordinates in the parsed representation.

Confirmation supplies preview_id, generation_id, and submission_id. Accept no replacement rows from the browser.
Acquire the write transaction, check generation/receipt, then load the preview and reread saved state.
Recompute the plan using the same normalized rows and service. Blockers produce no writes.
Different outcomes return STALE_PREVIEW and a renewed preview_id/summary. Require another explicit confirmation.
Equivalent outcomes commit all entities, evidence, asset updates, override clearing, and histories together.
Rechecks do not reparse the workbook or duplicate parser rules.
No-op confirmations return successful zero-effect counts without an upload/evidence/history record. Their retry receipt is infrastructure metadata only.
Post-commit responses report actual effects. Receipt lookup supports retry even if the preview has since expired or the app restarted.

## 5. Internal endpoint contracts

All endpoints use /api except the HTML/static routes. All domain responses include generation_id.
Dates use ISO strings, IDs/enums use canonical text, optional values use null, and decimal amounts use strings.
Unexpected request fields are rejected. Return structured errors, not raw exception messages.

Mutation envelope: generation_id, submission_id, expected_version when editing, plus the fields specified below.
Successful mutations return the saved record/result and its new version. UI refresh happens only after this response or verified receipt replay.

| Method and path | Request contract | Response contract |
|---|---|---|
| GET /api/config | None | Operational date/time, timezone, FX values/date/disclaimer, owners, delivered languages, schema version, generation. |
| GET /api/overview | Optional location/property_id/room_id, financial_date, currency_mode | Scope, distinct counts, room summaries, ordered unresolved tickets, finance/replacement results, diagnostics. Missing financial_date uses Hong Kong today. |
| GET /api/rooms/{room_id} | financial_date and currency_mode | Property/room, three observations/assets, separate unresolved/resolved tickets, versions, financial results. |
| GET /api/assets/{asset_id}/evidence | None | Baseline, invoice items/provenance, applied updates, override history, source/current/effective values. |
| PUT /api/rooms/{room_id}/observations/{system} | Envelope, status, observed_on, recorder, note | Saved latest observation. No observation history. |
| POST /api/rooms/{room_id}/observations/{system}/clear | Envelope | Unassessed UNKNOWN without metadata. |
| PATCH /api/assets/{asset_id} | Envelope, asset_name, purchase_date, installation_date, useful_life_months | Saved operational asset. Identity/category/cost fields excluded. |
| POST /api/assets/{asset_id}/override | Envelope, cost, currency, reason, recorder | Saved asset/effective pair and history reference. |
| POST /api/assets/{asset_id}/reset-to-source | Envelope, reason, recorder | Saved asset/source pair and history reference. |
| GET /api/maintenance | Optional location/property_id/room_id, view=UNRESOLVED or RESOLVED | Ordered tickets, versions, fixed links, explicit missing-information labels. |
| GET /api/maintenance/{ticket_id} | None | Ticket and ordered before/after history. |
| POST /api/maintenance | Envelope, room_id, asset_id, description, severity, owner_id, target_date, recorder | Open ticket, generated timestamps/ID, CREATE history. |
| PATCH /api/maintenance/{ticket_id} | Envelope, description, severity, owner_id, target_date, recorder | Saved unresolved ticket and EDIT history. Room/asset links excluded. |
| POST /api/maintenance/{ticket_id}/start | Envelope, recorder | In-progress ticket/history. Owner must already be set or saved first. |
| POST /api/maintenance/{ticket_id}/resolve | Envelope, resolution_note, recorder | Resolved ticket/history with actual resolution time. |
| POST /api/imports/preview | Multipart file and workflow=ASSETS or INVOICES | preview_id, counts, diagnostics, proposed asset changes/override clearing, expiry, generation. |
| POST /api/imports/confirm | generation_id, submission_id, preview_id | Actual counts and upload reference if evidence was written. |
| POST /api/reset | generation_id, confirm=true | New generation and empty-store counts. |

Errors use {code, message_key, details, generation_id}. Field diagnostics additionally contain coordinates, severity, identity, and reason.
Use 422 for invalid input/domain rules, 404 for missing records, and 409 for stale records/store/previews or submission conflicts.
Use 503 STORE_BUSY for lock timeout. Use 500 SAVE_FAILED for persistence failure after rollback.
PREVIEW_EXPIRED uses 409. STALE_PREVIEW details include its replacement preview for renewed review.
A request that supplies an obsolete generation returns STALE_STORE before record lookup.
Use no-store cache headers for domain/config responses. Static assets may use normal local caching with build-versioned URLs.

## 6. Browser state and UI safeguards

Use one state module and one request helper. Route/form modules use these shared boundaries.
Store language/currency independently in localStorage. Store navigation/filter/search/representation/selection/reporting date in sessionStorage.
The session is one browser tab until closure. Reload/navigation retains its reporting date. A newly opened session starts at Hong Kong today.
Initialize its date from /api/config, not the browser timezone. Reset starts a fresh reporting context in the initiating tab.
Browser preferences never enter the domain database or create overrides.

Use hash navigation for the four destinations, so refresh requires no server route fallback.
Keep record versions and generation with each loaded draft. Check generation on tab focus and before writes.
An obsolete-store draft remains visible as invalid input until discarded. It cannot recreate reset records.
On confirmed local reset, clear local drafts/context and open empty Overview. Other tabs show a reset notification on next focus/request.

Dirty forms offer Continue editing and Discard changes before navigation, room changes, card closure, or reset confirmation.
Browser tab closure uses the standard beforeunload prompt when possible. Do not claim custom browser-close wording.
Successful mutations refetch affected server representations. Do not optimistically invent saved counts or histories.
Preserve input on validation, stale-version, busy-store, or persistence failure.
Abort obsolete reads or reject responses by request sequence. A late room-A response cannot replace the selected room-B card.
Server-side services calculate all financial values. Views use formatted strings and semantic status labels.

English keys live in one local dictionary. Delivered dictionaries use the same keys with English fallback.
Offer en initially. Offer zh-Hant, zh-Hans, or ja only when their sets are delivered.
Translation tests verify keys/fallback. Alex's linguistic review remains separate submission evidence.

## 7. Sources and limits

The design uses [synchronous FastAPI handlers](https://fastapi.tiangolo.com/async/) and [Python SQLite connection rules](https://docs.python.org/3.11/library/sqlite3.html).
SQLite [foreign-key enforcement](https://www.sqlite.org/foreignkeys.html) requires explicit activation on each connection.
These references support design feasibility. They do not establish application test results.
Hosted deployment was considered and then excluded by Alex's final all-local instruction.

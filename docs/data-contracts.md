# Data contracts: Hotel asset-management prototype

Version: 0.2

Revised: 2026-10-02

Status: Explicit technical contract proposals for the approved product policies; not a database schema or claim of implementation

The [product specification](spec.md) governs behaviour. These layouts make its supported-input boundary explicit. Exact column spellings, parsing/normalisation details, technical history fields, and manual reset-baseline representation below are proposals for implementation review, not independently owner-approved policies.

## 1. Batch and workbook boundary

Upload all four separate .xlsx files in one batch. Recommended template filenames and required sheet names:

| Template filename | Sole table sheet | Identity |
|---|---|---|
| Properties.xlsx | Properties | property_id |
| Rooms.xlsx | Rooms | room_id |
| Assets.xlsx | Assets | asset_id |
| InvoiceLines.xlsx | InvoiceLines | invoice_id + line_id |

Each workbook contains exactly its one prescribed sheet. Row 1 contains the specified headers; data starts at Excel row 2. All defined headers must be present, including optional-value columns; order may vary. A headers-only table is allowed. Filenames can vary and do not determine identity. No .xls/.csv, multi-sheet-workbook path, arbitrary layouts, or PDF import. Fictional PDFs are evidence supplied alongside the structured data.

Proposed structural rules: reject missing/duplicate/unexpected headers, extra sheets, formulas, merged table cells, and unusable identifier columns with diagnostics. Ignore fully empty rows; validate partially populated rows normally. Translate none of the source headers/enums.

## 2. Common types and canonical values

| Type | Proposed representation and validation |
|---|---|
| ID | Non-empty text; trim outer whitespace; preserve case and leading zeros. Format ID cells as Text; reject numeric IDs rather than guess a lost zero. |
| Text | Unicode text with outer whitespace trimmed; preserve case and internal whitespace. Required text cannot be blank. |
| Optional text | Blank/whitespace-only → absent. |
| Calendar date | Valid Excel date cell with no time component, or ISO YYYY-MM-DD text; reject ambiguous locale strings and impossible dates. Interpret as calendar dates, not UTC instants. |
| Decimal amount | Finite non-negative decimal; numeric Excel cell or canonical decimal text without currency symbols/grouping separators. Reject booleans, NaN/infinity, and negative values; preserve calculation precision. |
| Whole months | Positive integer; reject zero, negatives, and fractional values. |
| Currency | HKD, SGD, GBP, JPY, USD; trim and uppercase. |
| Location | HONG_KONG, SINGAPORE, LONDON, JAPAN; trim and uppercase. |
| Facility type | LIGHTING, WATER_SUPPLY, AIR_CONDITIONING, OTHER; trim and uppercase. |
| Condition | HEALTHY, ATTENTION_NEEDED, CRITICAL, UNKNOWN; trim and uppercase. |

Enum values are stored independently of translated labels. Source text is never automatically translated. Equivalent dates/decimal values compare equal after parsing; display formatting must not change equality.

All monetary calculations and aggregation use decimal precision before display rounding. Proposed native display: JPY zero decimals, other supported currencies two; USD display is two decimals as required by the spec. Retain unrounded stored values.

## 3. Properties table

| Column | Type | Required value | Meaning |
|---|---|---|---|
| property_id | ID | Yes | Unique property identity |
| property_name | Text | Yes | Fictional hotel name |
| location | Location | Yes | Portfolio filter location |
| city | Text | Yes | Named city; Japanese fixture is Tokyo |

Property master data are created through valid imports only. Changed existing source content conflicts; no property-editing forms or import-based updates.

## 4. Rooms table

| Column | Type | Required value | Meaning |
|---|---|---|---|
| room_id | ID | Yes | Portfolio-unique room identity |
| property_id | ID | Yes | Existing or valid same-batch property |
| room_number | Text | Yes | Unique within that property; preserve text formatting |
| lighting_status | Condition | Conditional | Latest lighting assessment |
| lighting_observed_on | Calendar date | Conditional | Lighting assessment date |
| lighting_recorder | Text | Conditional | Lighting assessor |
| lighting_note | Optional text | No | Lighting assessment note |
| water_supply_status | Condition | Conditional | Latest water assessment |
| water_supply_observed_on | Calendar date | Conditional | Water assessment date |
| water_supply_recorder | Text | Conditional | Water assessor |
| water_supply_note | Optional text | No | Water assessment note |
| air_conditioning_status | Condition | Conditional | Latest air-conditioning assessment |
| air_conditioning_observed_on | Calendar date | Conditional | Air-conditioning assessment date |
| air_conditioning_recorder | Text | Conditional | Air-conditioning assessor |
| air_conditioning_note | Optional text | No | Air-conditioning assessment note |

Apply the following independently to each observation group:

- All four values absent: initialise unassessed UNKNOWN.
- UNKNOWN with absent date, recorder, and note: unassessed UNKNOWN.
- A recorded assessment, including recorded UNKNOWN, requires status, date, and recorder; note is optional.
- Non-UNKNOWN without date/recorder, metadata without status, one missing required metadata field, invalid status/date, or note-only unassessed data is a blocking row error.
- Imported observations never come from invoices. Manager edits affect the current observation, not the preserved imported Rooms baseline.
- An identical Rooms re-import skips that record without restoring an observation later edited/cleared by a manager. Changed imported observation content conflicts like other meaningful room source fields.

Recorded observations are latest-state records, not observation histories. Room master fields remain fixed in the UI; observation edits are permitted.

## 5. InvoiceLines table

| Column | Type | Required value | Meaning |
|---|---|---|---|
| invoice_id | ID | Yes | Invoice identity |
| line_id | ID | Yes | Line identity within invoice |
| description | Text | Yes | Individually tracked purchased item |
| acquisition_cost | Decimal amount | Yes | Original source line cost |
| currency | Currency | Yes | Original source currency |
| invoice_date | Calendar date | No | Optional invoice evidence date |
| supplier_name | Optional text | No | Optional fictional supplier |
| invoice_file | Optional text | No | Optional reference to accompanying fictional invoice |

Composite identity is (invoice_id, line_id). Every imported asset references one line; at most one asset may reference that line across existing and incoming records. Unlinked invoice lines may remain source records. There is no quantity/bundle/allocation field or allocation logic.

Invoice cost/currency are immutable source evidence. Zero cost is allowed with a warning. Missing optional supplier details warn. invoice_file is an evidence reference, not permission to read arbitrary files or run OCR; changing only a filename does not create a source-content conflict.

## 6. Assets table

| Column | Type | Required value | Meaning |
|---|---|---|---|
| asset_id | ID | Yes | Unique imported asset identity |
| room_id | ID | Yes | Existing or valid same-batch room |
| asset_name | Text | Yes | Item name |
| facility_type | Facility type | Yes | Facility category |
| purchase_date | Calendar date | Yes | Acquisition/service fallback date |
| installation_date | Calendar date | No | Must be on/after purchase; omission warns |
| useful_life_months | Whole months | Yes | Positive service life |
| invoice_id | ID | Yes | Linked invoice identity |
| line_id | ID | Yes | Linked invoice line identity |

Cost/currency are intentionally obtained from InvoiceLines, not duplicated in the Assets template. Extra cost/currency columns are outside this proposed layout; the importer must not silently choose between conflicting sources.

No derived financial columns, overrides, or ticket fields are imported. Every imported asset must have complete room/property/invoice dependencies. Reject a line already linked to a different existing asset.

## 7. Provenance, comparison, and atomic outcome

Preserve a source baseline for each imported entity, separate from editable operational state. Retain import/batch reference, source filename, sheet, Excel row number, and actual import timestamp. An asset also retains invoice/line identities and source invoice cost/currency.

Meaningful comparison fields:

| Entity | Fields compared after normalisation |
|---|---|
| Property | All declared table values |
| Room | Master fields and supplied/defaulted observation values |
| Invoice line | All declared table values except invoice_file |
| Asset | All declared table values; linked invoice content compares as its own entity |

Ignore upload filename, workbook bytes/style, sheet row position, ingestion timestamps, derived results, operational edits, and override history in identity comparison. Missing observation status and unassessed UNKNOWN normalise to the same logical state; absent optional values normalise consistently.

- Detect upload duplicates after ID normalisation, even if duplicate rows are otherwise identical.
- Existing same ID + same source content: planned skip, not duplicate insertion.
- Existing same ID + changed meaningful source content: blocking conflict, even if incoming values match current operational edits.
- Incoming identity matching a manually created asset: no imported baseline exists, so treat as a conflict rather than adopting or overwriting it.
- Resolve links through valid batch records or existing preserved records. Report dependencies on invalid/missing records.
- Check uniqueness/links across the complete batch and existing records before confirmation. Recheck commit-time integrity so a stale preview cannot bypass the rules.
- Any blocker prevents all operational writes. After a valid explicit confirmation, insert new records together and skip identical existing records; roll back on failure.

Diagnostics contain severity, entity/table, file, sheet, row, field, offending identity/value where useful, and an actionable reason. Coordinates are absent only when unavailable, such as an unreadable file. Preview counts are proposed; committed counts are actual. Never show proposed insertion counts as successful writes for a blocked batch.

## 8. Operational asset values and override history

Logical operational interface:

| Field/group | Behaviour |
|---|---|
| asset_id, room_id, invoice_id/line_id | Fixed after creation; imported IDs supplied, manual asset IDs generated |
| asset_name, facility_type, purchase_date, installation_date, useful_life_months | Editable with source-type/date validation |
| origin | IMPORTED or MANUAL; display manual origin as Manually entered |
| source_cost, source_currency | Preserved invoice values for imports |
| override_cost, override_currency | Both active together or both absent |
| override_reason, recorder, changed_at | Required on override and reset |
| effective_cost/currency | Active override pair, else preserved baseline pair; derived/read-only |
| depreciation, remaining_value, replacement_date | Derived/read-only under the spec |

For manual creation require cost and currency; no invoice link is necessary. Proposed representation: preserve the initially entered cost/currency as the manual reset baseline, applying later corrections through the same paired override/history mechanism. This proposal prevents a reset from fabricating invoice evidence; it is not independently owner-approved.

Proposed persistent override entry: history ID, asset ID, action (SET_OVERRIDE or RESET_TO_SOURCE), before/after effective cost/currency and override state, reason, self-declared recorder name, actual timestamp. Preserve previous entries after resets. A self-declared recorder is attribution, not authenticated identity.

Reset restores source invoice values for imported assets. Calculations and replacement proxies always use effective values. Changing display language/currency cannot create an override.

## 9. Maintenance and latest observation interfaces

These are operational records, not additional source-file import paths.

Maintenance fields: generated ticket ID; fixed room ID and optional same-room asset ID; non-empty description; severity LOW/MEDIUM/CRITICAL; optional owner while OPEN; canonical status OPEN/IN_PROGRESS/RESOLVED; actual opened/updated timestamps; optional calendar target date; resolution note and actual resolved timestamp when RESOLVED.

Use a short fictional owner list with stable owner IDs and display names. Its names/size are sample configuration, not permission roles. Proposed history entry: ticket/history ID, actual change timestamp, changed field, before/after value, and recorder attribution. Persist description/severity/target/owner/status changes, including simultaneous changes as one ordered event with changed fields. Display ties deterministically without implying an additional business priority.

Clearing owner is allowed only in OPEN. Owner is required in IN_PROGRESS. No status skipping/reopening/deletion; RESOLVED is read-only. A same-room asset link is validated on creation and fixed thereafter. Resolution timestamps use the actual clock, not the financial reporting date.

Latest observations use the same condition/date/recorder/note contract as Rooms imports. Clear sets unassessed UNKNOWN and removes metadata. Mark Healthy requires assessment metadata. No observation history or automatic maintenance-to-condition mapping.

## 10. Fixed configuration and display

Proposed FX configuration fields: as_of_date, fictional disclaimer, and currency→usd_per_unit. Exactly the supported five currencies must have positive finite rates; USD must equal 1. Validate completeness, uniqueness, positivity, and date before financial reporting. This document defines configuration shape, not fabricated rate values.

Missing/invalid FX configuration requires correction; no partial USD portfolio totals, zero substitutions, or silently excluded assets. No live lookup. Language is unrelated to rates.

Proposed language identifiers: en, zh-Hant, zh-Hans, ja. English is mandatory; other sets are stretch. Labels/messages/assumption text use translation keys with English fallback. Stored enums, filenames/headers, names, notes, and descriptions remain independent of translation.

Display preference: USD or LOCAL_TRANSACTION. English/USD are initial defaults; persist later selections across browser restarts on the same device. LOCAL_TRANSACTION uses effective asset currency and groups mixed totals by currency. Preferences do not modify stored money.

Operational dates/timestamps use Asia/Hong_Kong with explicit offsets for instants. Financial reporting is a separate session calendar-date control, initially today and retained for the session until changed/reset. The selected financial date never advances the operational clock.

## 11. Verification obligations

Verify parsing/normalisation with equivalent decimal/date representations, leading-zero text IDs, duplicate/conflicting IDs, and filename/row-independent repeats. Verify complete-batch no-write/rollback, existing invoice-link collisions, and repeat import after asset or observation editing.

Verify source/override isolation, reset history, same-room tickets, owner/status integrity, latest observation metadata, fixed FX completeness, translation boundaries, grouped currency totals, and date separation. Map results to SC-001–005, SC-007–008 and [assessment evidence](assessment-requirements.md).

No application tests or contract execution have occurred; these are required future checks.

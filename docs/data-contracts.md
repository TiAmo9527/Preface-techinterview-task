# Data contracts: Hotel asset-management prototype

Version: 0.3

Revised: 2026-10-03

Status: Documented contracts for the owner-approved baseline/invoice-update model; application and workbook generation pending

The [product specification](spec.md) governs behaviour. The two-workbook workflow and update policies are owner-approved; exact parsing, identifier grammar and technical history representations below are implementation proposals. This document defines logical interfaces, not a database schema or evidence of working validation.

## 1. Upload and workbook boundary

Two workbook types are supported, uploaded and confirmed independently:

| Recommended filename | Sole sheet | Purpose | Row identity |
|---|---|---|---|
| Assets.xlsx | Assets | Initialise properties, rooms and their three asset records | asset_id |
| Invoices.xlsx | Invoices | Update assets already recorded in rooms | invoice_id + line_id |

Load a valid Assets baseline before an invoice upload. Never require both workbooks in one upload. Invoice uploads may target a subset of existing rooms/assets; they cannot create rooms or assets. Baseline values are usable for finance without invoices. Headers-only sheets are allowed as no-op uploads.

Each workbook has exactly one prescribed sheet. Row 1 contains all defined headers, including optional-value columns; data starts at row 2. Header order may vary. Filenames do not determine identity. Reject missing/duplicate/unexpected headers, extra sheets, formulas, merged table cells, unsupported .xls/.csv formats and unreadable files. Ignore fully empty rows; validate partially populated rows normally. No PDF import or attachment requirement; workbook content and provenance are the source evidence.

## 2. Common types and identifiers

| Type | Proposed representation and validation |
|---|---|
| ID | Non-empty text; trim outer whitespace; preserve case and leading zeros. Reject numeric ID cells rather than guessing lost zeros. |
| Text | Unicode text; trim outer whitespace and preserve internal whitespace/case. Required text cannot be blank. |
| Optional text | Blank/whitespace-only means absent. |
| Calendar date | Valid Excel date cell without a time, or ISO YYYY-MM-DD text; reject impossible dates and ambiguous locale strings. Calendar dates are not UTC instants. |
| Decimal amount | Finite non-negative decimal, as numeric Excel cell or canonical decimal text without currency/grouping symbols; reject booleans, NaN/infinity and negatives. |
| Whole months | Positive integer; reject booleans, zero, negative and fractional values. |
| Currency | HKD, SGD, GBP, JPY, USD; trim and uppercase. |
| Location | HONG_KONG, SINGAPORE, LONDON, JAPAN; trim and uppercase. |
| Facility type | LIGHTING, WATER_SUPPLY, AIR_CONDITIONING only; trim and uppercase. |
| Condition | HEALTHY, ATTENTION_NEEDED, CRITICAL, UNKNOWN; trim and uppercase. |

Region codes map HK → HONG_KONG, SG → SINGAPORE, LDN → LONDON, JP → JAPAN. Proposed ID grammar: optional S<digits>- namespace, region code, -P<at least two digits> for a property; append -R<at least three digits> for a room; append -A<at least three digits> for an asset. Examples: HK-P01, HK-P01-R001, HK-P01-R001-A001; seeded examples prefix every linked ID with S20261002-. Use uppercase codes. Invoice/line IDs are non-empty text and do not need this location grammar.

Validate that property_id's region agrees with location, room_id has the exact property_id prefix, and asset_id has the exact room_id prefix, including namespace. Asset suffixes do not encode editable names or dates. room_number is a text display label, unique within its property; it need not equal the internal room-code suffix. Relationships use exact identifiers, never guessed names.

Equivalent parsed dates/decimals compare equal. Source text and enums are independent of translated UI labels. Calculations/aggregation use unrounded decimal values; proposed display is JPY zero decimals, other supported currencies two, and USD two decimals.

## 3. Assets baseline sheet

Exact recommended header order:

```text
property_id, property_name, location, city, room_id, room_number,
lighting_status, lighting_observed_on, lighting_recorder, lighting_note,
water_supply_status, water_supply_observed_on, water_supply_recorder, water_supply_note,
air_conditioning_status, air_conditioning_observed_on, air_conditioning_recorder, air_conditioning_note,
asset_id, asset_name, facility_type, purchase_date, installation_date,
useful_life_months, acquisition_cost, currency
```

| Columns | Type | Required value | Meaning |
|---|---|---|---|
| property_id, room_id, asset_id | ID | Yes | Stable property, room and asset-record identities |
| property_name, city, room_number | Text | Yes | Fictional property/city and room label |
| location | Location | Yes | Portfolio location |
| lighting_status, water_supply_status, air_conditioning_status | Condition | Conditional | Latest independent room-system assessments |
| lighting_observed_on, water_supply_observed_on, air_conditioning_observed_on | Calendar date | Conditional | Assessment dates |
| lighting_recorder, water_supply_recorder, air_conditioning_recorder | Text | Conditional | Assessment recorders |
| lighting_note, water_supply_note, air_conditioning_note | Optional text | No | Assessment notes |
| asset_name | Text | Yes | Initial asset name |
| facility_type | Facility type | Yes | One of the room's three fixed categories |
| purchase_date | Calendar date | Yes | Initial acquisition/service fallback date |
| installation_date | Calendar date | No | On/after purchase; omission warns and uses purchase fallback |
| useful_life_months | Whole months | Yes | Initial useful life |
| acquisition_cost | Decimal amount | Yes | Initial acquisition cost; zero warns |
| currency | Currency | Yes | Initial transaction currency |

Each room has exactly three records: one LIGHTING, one WATER_SUPPLY and one AIR_CONDITIONING. No empty-room rows, extra categories or multiple records in a category. Validate completeness against the union of existing records and incoming valid baseline rows. Existing rooms are already complete; a different incoming asset identity occupying an existing room/category blocks the upload.

Derive property and room records from baseline rows. Repeated property IDs and room IDs are expected. All normalised property values for a property must agree; all normalised room labels, property associations and three assessment groups for a room must agree. Retain contributing coordinates and report disagreements without choosing the first row silently. Count each property/room once. Asset IDs are unique within the upload even if duplicate rows are identical.

Property and room master data are import-only. New rooms may be added to an existing property when property baseline values agree, and the new room has all three asset rows. Changed source fields of an existing entity conflict. Identical baseline re-imports compare with preserved original baselines and never restore values changed by invoices, asset edits or assessment edits.

## 4. Latest room assessments

Apply independently to each four-field assessment group, then compare repeated groups after normalisation:

- All values absent, or UNKNOWN with absent date/recorder/note: initialise unassessed UNKNOWN.
- A recorded assessment, including recorded UNKNOWN, requires status, valid date and recorder; note is optional.
- Metadata without status, missing required assessment metadata, invalid status/date or note-only unassessed data blocks the upload.

Missing status and unassessed UNKNOWN normalise to the same logical state. Assessment edits affect current observations, not the original baseline. Observations are latest-state records without observation history. Invoice uploads never supply or change them; an invoice is not evidence of a healthy condition.

## 5. Invoices update sheet

Exact recommended header order:

```text
invoice_id, line_id, room_id, facility_type, asset_name, purchase_date,
installation_date, useful_life_months, acquisition_cost, currency,
invoice_date, supplier_name
```

| Column | Type | Required value | Meaning |
|---|---|---|---|
| invoice_id | ID | Yes | Invoice identity; may repeat for different items |
| line_id | ID | Yes | Item identity within invoice |
| room_id | ID | Yes | Existing room; includes property and region |
| facility_type | Facility type | Yes | Identifies exactly one existing asset in that room |
| asset_name | Text | Yes | Purchased-item description and replacement asset name |
| purchase_date | Calendar date | Yes | Replacement purchase date |
| installation_date | Calendar date | No | Replacement installation date; on/after purchase |
| useful_life_months | Whole months | Yes | Replacement useful life |
| acquisition_cost | Decimal amount | Yes | Replacement acquisition cost; zero warns |
| currency | Currency | Yes | Replacement source currency |
| invoice_date | Calendar date | Yes | Determines invoice update precedence |
| supplier_name | Optional text | No | Fictional supplier; omission warns |

Resolve (room_id, facility_type) to one stable existing asset_id and retain that resolved target with the invoice item. Unknown rooms or missing/ambiguous targets block the upload. Every invoice item has a target; no unlinked rows or bundle/quantity allocation. A line cannot target multiple assets, but many distinct invoice items may target the same asset over time. asset_name serves as description; there are no separate description or invoice_file headers.

An invoice is a full replacement snapshot of six fields: asset_name, purchase_date, installation_date, useful_life_months, acquisition_cost and currency. A blank optional installation date explicitly clears the previous date and enables purchase-date fallback; it is not a partial patch. Asset ID, room, category, observations and tickets stay fixed. Updates represent purchases/replacements, not accumulated repair expenses.

## 6. Invoice precedence and repeat uploads

1. Validate every uploaded row, including older evidence. Detect duplicate (invoice_id, line_id) identities inside the upload, including identical duplicates. Existing identical invoice items skip; changed content under an existing identity is a blocker.
2. Group accepted existing and valid incoming invoice items by resolved asset. Determine the maximum invoice_date per target; upload time, file order and purchase date do not determine precedence.
3. Compare the six-field normalised replacement snapshots at that maximum date. Different snapshots block the entire upload. Equal snapshots with distinct item identities may coexist as equivalent evidence. Retain all equivalent evidence references in deterministic invoice_id/line_id order; do not arbitrarily discard one.
4. With no prior applied invoice, apply the maximum-date snapshot. Otherwise apply only when the incoming controlling date is strictly newer. The first accepted invoice is eligible regardless of the initial baseline purchase date.
5. Older new items and new equal-date/equal-snapshot evidence are stored as historical-only records; they do not replay updates, clear overrides or disturb manual edits. A strictly newer snapshot applies even when its values equal the previous invoice values.

An identical re-upload of an older invoice still skips by identity. Conflicting snapshots at dates below the controlling maximum remain historical evidence; the same-date ambiguity blocker concerns the controlling maximum date. Required-field/type/target errors always block, regardless of precedence.

When applying a snapshot, replace all six current asset fields and clear an active paired financial override. Preserve the prior values and override state in invoice-update history; append a linked CLEAR_ON_INVOICE override-history entry when an override is cleared. Recalculate depreciation, book value and replacement outputs from the newly effective fields. Clearing an override here has a system-generated reason referencing the invoice update, not a fabricated manager attribution.

## 7. Provenance, comparison and atomic outcome

Keep original property/room/asset baselines immutable and separate from current operational values. Preserve every accepted invoice item, resolved asset target, import/upload reference, filename, sheet, Excel row and actual import timestamp. Property/room baselines retain all contributing row coordinates. Skipped uploads must not rewrite original source evidence.

| Record | Meaningful comparison fields |
|---|---|
| Property baseline | property_id, property_name, location, city |
| Room baseline | room_id, property_id, room_number and normalised assessment groups |
| Asset baseline | asset_id, room_id, asset_name, facility_type, purchase_date, installation_date, useful_life_months, acquisition_cost, currency |
| Invoice item | All twelve declared input values |

Ignore filename, bytes/styles, row position, timestamps, derived results, operational edits and override history for source equality. No import updates existing baseline or invoice-item identities; new invoice-item identities can update current assets under section 6.

Proposed invoice-update history: event ID, asset ID, controlling invoice date, equivalent invoice-item references, previous applied source references, before/after six-field current values, before/after source cost/currency, before/after override/effective values, upload reference and actual timestamp. Historical-only items remain in the evidence ledger without a false asset-update event. History and source references must survive restart.

Preview performs no operational writes. Recheck all integrity/precedence rules at confirmation, rejecting a stale preview that would change the confirmed result. Commit source evidence, new baseline entities, asset updates and linked histories together or roll everything back. Any blocker prevents all changes, including historical-only evidence inserts.

Diagnostics include severity, entity, file, sheet, row, field, offending identity/value and actionable reason; omit coordinates only when unavailable. Preview separately reports proposed baseline property/room/asset inserts, asset updates, new invoice items, historical-only items, source skips, warnings and blockers. Asset-update counts are distinct assets, not invoice-row counts. Equivalent top-date evidence is counted as source items but never duplicated in asset or financial totals. Post-commit counts are actual; blocked/failed uploads never show successful writes.

## 8. Operational asset values and override history

| Field/group | Behaviour |
|---|---|
| asset_id, room_id, facility_type | Fixed; no manual creation, category changes or relocation |
| asset_name, purchase_date, installation_date, useful_life_months | Editable with source-type/date validation; a newly applied invoice replaces them |
| baseline_cost, baseline_currency | Preserved Assets values |
| source_cost, source_currency | Latest applied invoice values, else baseline pair |
| applied_invoice_date/references | Read-only; absent before an invoice is applied |
| override_cost, override_currency | Both active together or both absent |
| override_reason, recorder, changed_at | Required for manager override/reset |
| effective_cost/currency | Active override pair, else source pair; read-only |
| depreciation, remaining_value, replacement_date | Derived/read-only |

Proposed override-history entry: history ID, asset ID, SET_OVERRIDE / RESET_TO_SOURCE / CLEAR_ON_INVOICE action, before/after effective/source values and override state, reason, manager recorder or linked invoice-update attribution, actual timestamp. Preserve entries after reset or invoice clearing. Self-declared manager names are attribution, not authenticated identity.

Reset restores the latest applied invoice cost/currency, falling back to baseline values when no invoice is applied; it does not replay source dates/names or clear assessment edits. It requires a reason and appends history. Historical-only and skipped invoices leave active overrides intact. Display language/currency changes never create overrides.

## 9. Maintenance and latest observation interfaces

These are operational records, not additional source-file import paths.

Maintenance fields: generated ticket ID; fixed room ID and optional same-room asset ID; non-empty description; severity LOW/MEDIUM/CRITICAL; optional owner while OPEN; canonical status OPEN/IN_PROGRESS/RESOLVED; actual opened/updated timestamps; optional calendar target date; resolution note and actual resolved timestamp when RESOLVED.

Use a short fictional owner list with stable owner IDs and display names. Its names/size are sample configuration, not permission roles. Proposed history entry: ticket/history ID, actual change timestamp, changed field, before/after value, and recorder attribution. Persist description/severity/target/owner/status changes, including simultaneous changes as one ordered event with changed fields. Display ties deterministically without implying an additional business priority.

Clearing owner is allowed only in OPEN. Owner is required in IN_PROGRESS. No status skipping/reopening/deletion; RESOLVED is read-only. A same-room asset link is validated on creation and fixed thereafter. Resolution timestamps use the actual clock, not the financial reporting date.

Latest observations use the same condition/date/recorder/note contract as Assets baseline imports. Clear sets unassessed UNKNOWN and removes metadata. Mark Healthy requires assessment metadata. No observation history or automatic maintenance-to-condition mapping.

## 10. Fixed configuration and display

Proposed FX configuration fields: as_of_date, fictional disclaimer, and currency→usd_per_unit. Exactly the supported five currencies must have positive finite rates; USD must equal 1. Validate completeness, uniqueness, positivity, and date before financial reporting. This document defines configuration shape, not fabricated rate values.

Missing/invalid FX configuration requires correction; no partial USD portfolio totals, zero substitutions, or silently excluded assets. No live lookup. Language is unrelated to rates.

Proposed language identifiers: en, zh-Hant, zh-Hans, ja. English is mandatory; other sets are stretch. Labels/messages/assumption text use translation keys with English fallback. Stored enums, filenames/headers, names, notes, and descriptions remain independent of translation.

Display preference: USD or LOCAL_TRANSACTION. English/USD are initial defaults; persist later selections across browser restarts on the same device. LOCAL_TRANSACTION uses effective asset currency and groups mixed totals by currency. Preferences do not modify stored money.

Operational dates/timestamps use Asia/Hong_Kong with explicit offsets for instants. Financial reporting is a separate session calendar-date control, initially today and retained for the session until changed/reset. The selected financial date never advances the operational clock.

## 11. Verification obligations

Verify parsing/normalisation with equivalent decimal/date representations, leading-zero text IDs, duplicate/conflicting IDs, and filename/row-independent repeats. Verify complete-upload no-write/rollback, baseline-only initialisation, category completeness, repeated room/property consistency, invoice-only subset updates, unknown targets, maximum-date selection, equal-date conflicts/equivalent evidence, older historical-only items, source identity skips/conflicts, and repeats after invoice/asset/observation edits.

Verify invoice replacement and override clearing/history, recalculation, baseline/latest-invoice reset fallback, source/override isolation, reset history, same-room tickets, owner/status integrity, latest observation metadata, fixed FX completeness, translation boundaries, grouped currency totals, and date separation. Map results to SC-001–005, SC-007–008 and [assessment evidence](assessment-requirements.md).

No application tests or contract execution have occurred; these are required future checks.

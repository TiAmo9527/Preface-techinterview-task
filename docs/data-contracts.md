# Data contracts: Hotel asset-management prototype

Version: 0.4

Revised: 2026-10-03

Status: Documented logical interfaces. Application validation and workbook generation: NOT RUN.

[Product specification v0.4](product-spec.md) defines behavior. The owner-approved model uses independent baseline and invoice uploads.
Exact headers, parsing, identifier grammar, configuration representation, and technical history representation remain implementation proposals.
This document selects no database columns or storage types. Use the [shared glossary](glossary.md) for domain meaning.

## 1. Upload and workbook boundary

| Recommended filename | Sole sheet | Purpose | Row identity |
|---|---|---|---|
| Assets.xlsx | Assets | Initialize properties, rooms, and their three asset records. | asset_id |
| Invoices.xlsx | Invoices | Update existing room/category asset records. | invoice_id + line_id |

Import a valid baseline before invoice updates. Do not require both workbooks in one upload.
Invoices can target a subset of existing assets. They cannot create property, room, or asset identities.
Baseline financial values require no invoices. Headers-only uploads contain no new rows.

Proposed workbook structure:

- Each file contains its required single sheet.
- Row 1 contains all headers, including optional-value columns.
- Data starts at row 2. Header order can vary.
- Missing, duplicate, or unexpected headers block validation.
- Extra sheets, formulas, and merged table cells block validation.
- Unsupported .xls/.csv formats and unreadable files block validation.
- Fully empty rows are ignored. Partial rows use normal validation.

Filenames do not establish identity. There is no PDF import or attachment requirement.
Workbook information and provenance supply source evidence.

## 2. Common types and identifiers

| Type | Proposed representation and validation |
|---|---|
| ID | Non-empty text. Trim outer whitespace. Preserve case and leading zeros. Reject numeric identity cells. |
| Text | Unicode text. Trim outer whitespace. Preserve internal whitespace and case. Required text cannot be blank. |
| Optional text | Blank or whitespace-only values mean absent. |
| Calendar date | Excel date without time, or ISO YYYY-MM-DD text. Reject impossible dates and ambiguous locale strings. Not a UTC instant. |
| Decimal amount | Finite non-negative numeric decimal or canonical decimal text without currency/grouping symbols. Reject booleans, NaN, infinity, and negatives. |
| Whole months | Positive integer. Reject booleans, zero, negatives, and fractions. |
| Currency | HKD, SGD, GBP, JPY, USD. Trim and uppercase. |
| Location | HONG_KONG, SINGAPORE, LONDON, JAPAN. Trim and uppercase. |
| Facility type | LIGHTING, WATER_SUPPLY, AIR_CONDITIONING. Trim and uppercase. |
| Condition | HEALTHY, ATTENTION_NEEDED, CRITICAL, UNKNOWN. Trim and uppercase. |

Region mappings:

| Region | Location |
|---|---|
| HK | HONG_KONG |
| SG | SINGAPORE |
| LDN | LONDON |
| JP | JAPAN |

Proposed identity grammar:

1. Use an optional S<digits>- namespace.
2. Use the uppercase region code.
3. Add -P and at least two digits for a property.
4. Add -R and at least three digits for a room.
5. Add -A and at least three digits for an asset.

Examples are HK-P01, HK-P01-R001, and HK-P01-R001-A001.
Seeded examples use the S20261002- prefix throughout linked identities.
Invoice/line identities require non-empty text without the location grammar.

Property region must agree with location. Room identity must use the exact property prefix.
Asset identity must use the exact room prefix, including namespace. Asset suffixes do not derive category, name, or dates.
Room numbers are unique text labels within a property. They need not equal the internal room suffix.

Use exact identities for relationships. Do not guess relationships from names.

Equivalent parsed dates and decimals compare equal. UI translation does not change source text or enums.
Use unrounded calculations and aggregates. Proposed local display uses zero decimals for JPY and two for other supported currencies.
USD display uses two decimals under the product policy.

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
| property_id, room_id, asset_id | ID | Yes | Stable record identities. |
| property_name, city, room_number | Text | Yes | Fictional property/city and property-local room label. |
| location | Location | Yes | Portfolio location. |
| lighting_status, water_supply_status, air_conditioning_status | Condition | Conditional | Latest independent room-system assessments. |
| lighting_observed_on, water_supply_observed_on, air_conditioning_observed_on | Calendar date | Conditional | Assessment dates. |
| lighting_recorder, water_supply_recorder, air_conditioning_recorder | Text | Conditional | Assessment recorders. |
| lighting_note, water_supply_note, air_conditioning_note | Optional text | No | Assessment notes. |
| asset_name | Text | Yes | Initial asset name. |
| facility_type | Facility type | Yes | One fixed category for this room. |
| purchase_date | Calendar date | Yes | Initial acquisition and service fallback date. |
| installation_date | Calendar date | No | On/after purchase. Absence warns and uses purchase fallback. |
| useful_life_months | Whole months | Yes | Initial useful life. |
| acquisition_cost | Decimal amount | Yes | Initial acquisition cost. Explicit zero warns. |
| currency | Currency | Yes | Initial transaction currency. |

Each room requires one LIGHTING, one WATER_SUPPLY, and one AIR_CONDITIONING record.
Empty-room rows, extra categories, and multiple records per category are invalid.
Check completeness against existing records and incoming valid baseline rows.
Existing rooms are already complete. Another asset identity occupying their category blocks the upload.

Derive property and room records from baseline rows. Repeated property and room identities are expected.
Normalized property information must agree for each property. Room labels, parent property, and three assessment groups must agree for each room.
Retain contributing coordinates. Report disagreements without choosing the first row.

Count properties and rooms once. Duplicate asset identities inside one upload block even when rows match.

Property and room master data are import-only. New rooms can join an existing property with matching property baseline values.
The new room still requires three categories. Changed source information for existing entities conflicts.
Identical baseline repeats compare preserved evidence, not current operational edits.
They do not restore invoice values, asset edits, or manager assessments.

## 4. Latest room assessments

Normalize each four-field group independently. Compare repeated groups after normalization.

- All absent values initialize unassessed UNKNOWN.
- UNKNOWN without date, recorder, or note initializes unassessed UNKNOWN.
- Recorded assessments require status, valid date, and recorder, including recorded UNKNOWN.
- Notes remain optional for recorded assessments.
- Metadata without status blocks validation.
- Missing required metadata, invalid status/date, or note-only unassessed information blocks validation.

Absent status and unassessed UNKNOWN represent the same state.
Manager edits change current observations, not baseline evidence. Observations have no history.
Invoices do not supply observations. A purchase does not prove Healthy condition.

## 5. Invoices update sheet

Exact recommended header order:

```text
invoice_id, line_id, room_id, facility_type, asset_name, purchase_date,
installation_date, useful_life_months, acquisition_cost, currency,
invoice_date, supplier_name
```

| Column | Type | Required value | Meaning |
|---|---|---|---|
| invoice_id | ID | Yes | Invoice identity. Can repeat for different items. |
| line_id | ID | Yes | Item identity within the invoice. |
| room_id | ID | Yes | Existing room, including property and region. |
| facility_type | Facility type | Yes | One existing asset target in that room. |
| asset_name | Text | Yes | Purchased-item description and replacement name. |
| purchase_date | Calendar date | Yes | Replacement purchase date. |
| installation_date | Calendar date | No | Replacement installation date, on/after purchase. |
| useful_life_months | Whole months | Yes | Replacement useful life. |
| acquisition_cost | Decimal amount | Yes | Replacement acquisition cost. Explicit zero warns. |
| currency | Currency | Yes | Replacement source currency. |
| invoice_date | Calendar date | Yes | Update precedence date. |
| supplier_name | Optional text | No | Fictional supplier. Absence warns. |

Resolve room_id plus facility_type to one existing asset_id. Retain that target in accepted evidence.
Unknown, absent, or ambiguous targets block the whole upload. Every invoice item requires one target.
There is no unlinked evidence, quantity allocation, or bundle allocation.

Many distinct items can target the same record over time. One item cannot target multiple records.
asset_name is also the description. There are no separate description or invoice_file columns.

Each item supplies all six snapshot fields. Blank installation clears the old date and enables purchase fallback.
It does not mean “retain the previous date”. Identity, room, category, observations, and tickets stay fixed.
Invoice items represent purchases/replacements, not accumulated repair expenses.

## 6. Invoice precedence and repeats

1. Validate every row, including older evidence.
2. Reject duplicate invoice_id/line_id pairs inside the upload, including identical duplicates.
3. Skip existing identical items.
4. Block changed evidence under an existing item identity.
5. Group stored and valid incoming evidence by resolved target.
6. Find the maximum invoice_date per target.
7. Compare normalized six-field snapshots at that date.
8. Block different controlling snapshots.
9. Retain equivalent distinct identities as evidence.
10. Apply the controlling snapshot if no invoice was applied previously.
11. Otherwise apply only a strictly newer controlling date.

Upload time, row order, and purchase date do not set precedence.
The first invoice applies regardless of baseline purchase date. A strictly newer date applies even when snapshot values match.
Keep equivalent references in deterministic invoice_id/line_id order. Do not discard equivalent evidence arbitrarily.

Older new items and equivalent equal-date items remain historical-only. They do not replay updates or clear overrides.
Differences below the maximum date do not control current values. Required-field, type, and target errors always block.
An identical older re-upload still skips by identity.

Applied invoices replace six current fields and clear active overrides.
Preserve previous fields and override state in update history. Link CLEAR_ON_INVOICE override history when clearing occurs.
Use a system-generated reason linked to the update, not fabricated manager attribution.
Recalculate financial and replacement results from the effective fields.

## 7. Provenance, comparisons, and atomic outcome

Preserve immutable property, room, and asset baselines separately from current values.
Accepted invoice provenance includes resolved target, upload reference, filename, sheet, row, and actual import timestamp.
Property/room baselines retain all contributing coordinates. Skips do not rewrite original provenance.

| Record | Meaningful comparison fields |
|---|---|
| Property baseline | property_id, property_name, location, city |
| Room baseline | room_id, property_id, room_number, normalized assessment groups |
| Asset baseline | asset_id, room_id, asset_name, facility_type, purchase_date, installation_date, useful_life_months, acquisition_cost, currency |
| Invoice item | All twelve declared input values |

Ignore filename, file bytes/styles, row position, timestamps, calculated results, operational edits, and override history for source equality.
Imports never update existing baseline or invoice-item identities. New item identities can update current assets under precedence rules.

Proposed invoice-update history includes:

- Event identity and asset identity.
- Controlling invoice date and all equivalent item references.
- Previous applied source references.
- Before/after six-field operational values.
- Before/after source values, override state, and effective values.
- Upload reference and actual timestamp.

Historical-only items have no false applied-update event. Evidence references and histories survive normal restart.

Preview saves nothing. Confirmation rechecks integrity and precedence.
Changed outcomes require renewed review and confirmation. Commit evidence, entities, updates, and histories atomically.
Failure preserves previous saved state. Any blocker prevents every write, including historical-only evidence.

Diagnostics include severity, entity, file, sheet, row, field, offending identity/value, and actionable reason.
Omit unavailable coordinates only. Preview separates entity inserts, distinct asset updates, new items, historical-only items, skips, warnings, and blockers.
Equivalent controlling items count as evidence, not duplicated assets. Post-commit counts report actual successful effects.
Blocked or failed uploads display no successful writes.

## 8. Operational values and override history

| Field/group | Behavior |
|---|---|
| asset_id, room_id, facility_type | Fixed. No manual creation, category changes, or relocation. |
| asset_name, purchase_date, installation_date, useful_life_months | Editable with validation. Applied invoices replace them. |
| baseline_cost, baseline_currency | Preserved Assets values. |
| source_cost, source_currency | Latest applied invoice pair, otherwise baseline pair. |
| applied_invoice_date/references | Read-only. Absent before the first applied invoice. |
| override_cost, override_currency | Both active or both absent. |
| override_reason, recorder, changed_at | Required for manager override/reset. |
| effective_cost/currency | Active override pair, otherwise source values. Read-only result. |
| depreciation, remaining_value, replacement_date | Calculated and read-only. |

Proposed override-history entries include identity, asset, action, before/after values, override state, reason, attribution, and actual timestamp.
Actions are SET_OVERRIDE, RESET_TO_SOURCE, and CLEAR_ON_INVOICE.
Use manager attribution for manual actions and linked invoice attribution for system clearing.
Preserve entries after reset or clearing. Self-declared recorders do not prove authenticated identity.

Reset restores latest applied invoice values or baseline fallback. Reset requires reason/recorder and appends history.
It does not restore source names/dates or clear observations. Historical-only items and skips preserve overrides.
Display settings do not create overrides.

## 9. Maintenance and observation interfaces

These records have no extra source-file import path.

Maintenance requires ticket identity, room, non-empty description, LOW/MEDIUM/CRITICAL severity, status, and actual opened/updated timestamps.
Status values are OPEN, IN_PROGRESS, and RESOLVED.
Asset link and target date are optional. Owner is optional only while OPEN.
RESOLVED requires a note and actual resolution timestamp. Validate same-room links at creation.

Room/asset links remain fixed. IN_PROGRESS requires an owner and blocks owner removal.
Reassignment remains permitted while unresolved. No skipping, reopening, deletion, or resolved edits apply.

Use stable owner identities and display names from a short fictional configuration list.
Names and list size are sample configuration, not permission roles.
Proposed history stores event identity, actual timestamp, changed fields, before/after values, and recorder attribution.
Simultaneous changes form one ordered event. Display ties deterministically without adding business priority.

Observations use the baseline condition/date/recorder/note contract. Clear returns unassessed UNKNOWN without metadata.
Healthy requires assessment metadata. No observation history or automatic maintenance-to-condition mapping exists.

## 10. Fixed configuration, display, and local state

Proposed FX representation uses as_of_date, a fictional disclaimer, and currency→usd_per_unit.
Exactly five supported currencies require positive finite rates. USD must equal 1.
Check completeness, uniqueness, positivity, and date before reporting. Numerical application rates remain unselected.

Missing configuration blocks complete reporting without zero substitutions or omitted assets. No live lookup applies.
The configured FX date is independent of financial reporting date and language.

Proposed language identifiers are en, zh-Hant, zh-Hans, and ja.
English is mandatory. Other sets remain stretch. Missing translation keys use English.
Stored enums, filenames, headers, names, notes, and descriptions stay unchanged.

Display modes are USD and LOCAL_TRANSACTION. First use defaults to English/USD.
Later choices persist independently across browser restarts on the same device.
Local mode uses effective currency with separate currency totals. Preferences do not change stored money.

Operational dates and timestamps use Asia/Hong_Kong. Display explicit offsets for actual instants under the proposed display contract.
Financial reporting uses a separate session date, initially today. It never advances the operational clock.

Normal restart preserves the selected store's records, source evidence, and histories.
Each rehearsal selects a new isolated empty store. Normal data and browser preferences remain unchanged.
Another rehearsal selects another store. No destructive reset button is required.
Selection mechanisms and storage representation remain technical-planning work.

## 11. Verification obligations

Required domain checks are in [acceptance scenarios](acceptance-scenarios.md). All application results remain NOT RUN.

Proposed parser checks must cover:

- Equivalent decimal/date representations.
- Leading-zero text identities and rejected numeric identity cells.
- Malformed identity prefixes and inconsistent region/parent links.
- Duplicate headers, extra sheets, formulas, merged cells, and unsupported formats.
- Missing-value normalization and filename/row-independent source comparisons.
- Rejected booleans, non-finite numbers, ambiguous date text, and date cells containing time.

Exact parsing checks do not imply owner approval of every technical proposal.
Map actual domain results to SC-001–SC-005, SC-007, SC-008, and [assessment evidence](assessment-requirements.md#5-evidence-ledger).
No contract execution or application tests occurred.

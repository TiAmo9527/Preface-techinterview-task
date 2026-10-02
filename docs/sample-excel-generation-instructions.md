# AI instructions: Generate baseline and invoice-update Excel samples

Version: 0.3

Revised: 2026-10-03

Use this as one self-contained AI prompt. Generate both valid and invalid samples in the same invocation. This document is instructions only; no workbooks or application validation have been executed. In this repository, [data contracts](data-contracts.md) and [sample-data plan](sample-data-plan.md) govern the same model; report any discrepancy before generating incompatible files.

## 1. Request, outputs and defaults

Generate exactly four .xlsx files and one external generation-summary.md:

```text
<run>/valid/Assets.xlsx
<run>/valid/Invoices.xlsx
<run>/invalid/Assets.xlsx
<run>/invalid/Invoices.xlsx
<run>/generation-summary.md
```

Each example contains the same two workbook types. The product first imports an Assets baseline, then independently uploads Invoices to update existing room/category records. Do not describe these as a required paired upload or four-file product import. Invalid generation is mandatory, not opt-in. Generate no extra workbook variants, PDFs, attachment links, FX configurations, maintenance imports, code edits, dependency installations, commits or publication.

| Parameter | Default |
|---|---|
| Seed | 20261002 |
| Financial reference date | 2026-10-02 |
| Properties | 4: Hong Kong, Singapore, London, Tokyo (Japan) |
| Rooms per property | 3 |
| Assets per room | Exactly 3: one LIGHTING, one WATER_SUPPLY, one AIR_CONDITIONING; not configurable |
| Valid invoice items | One update per asset: 36 with default room count |
| Mode | Both fully populated valid and deliberately invalid examples |
| Run root | sample_data/spreadsheets/generated/seed-20261002 |

State selected parameters/output directory before generation and record them in the manifest. Use one seeded random generator, deterministic iteration and fixed reserved cases so the same parameters produce logically identical records. Different seeds use different ID namespaces. Use a new seed for independent datasets with changed parameters; changed content under existing IDs intentionally conflicts. Keep existing artifacts intact by selecting a fresh run suffix if necessary. The reference date anchors financial examples, not the operational clock.

## 2. Exact schemas and common rules

Each workbook has exactly one sheet. Row 1 contains the following exact headers in order; data starts at row 2. All headers remain present, including optional-value columns. No titles, totals, formulas, merged cells, hidden helper columns, charts, extra sheets or calculated financial columns. Freeze the header row, enable filters and size columns legibly. Put disclaimers and explanations in the manifest.

### Assets.xlsx / Assets — 26 columns

```text
property_id, property_name, location, city, room_id, room_number,
lighting_status, lighting_observed_on, lighting_recorder, lighting_note,
water_supply_status, water_supply_observed_on, water_supply_recorder, water_supply_note,
air_conditioning_status, air_conditioning_observed_on, air_conditioning_recorder, air_conditioning_note,
asset_id, asset_name, facility_type, purchase_date, installation_date,
useful_life_months, acquisition_cost, currency
```

All property/room/asset master values are required except installation_date. Each room assessment group is conditionally required: a recorded status, including UNKNOWN, needs observed_on and recorder; note is optional. All four values blank or UNKNOWN alone means unassessed UNKNOWN. Metadata without status or partial required metadata is invalid. In the fully populated valid example, populate every assessment field and installation_date, including all optional notes.

Repeat the same property/room/assessment values for each of the room's three asset rows. Exactly one row per category per room is required. Reject empty rooms, fourth categories, duplicate categories and inconsistent repeated values. Baseline cost/currency are supplied here; invoice links are absent.

### Invoices.xlsx / Invoices — 12 columns

```text
invoice_id, line_id, room_id, facility_type, asset_name, purchase_date,
installation_date, useful_life_months, acquisition_cost, currency,
invoice_date, supplier_name
```

All values except installation_date and supplier_name are required. Populate those optional fields in the valid example too. asset_name is also the invoice-item description; do not add description or invoice_file columns. Each row targets an existing baseline (room_id, facility_type) pair. invoice_id may repeat for different items, but (invoice_id, line_id) must be unique. There is no asset creation, room creation, quantity, bundle allocation or cumulative repair cost.

### Types, enums and IDs

- IDs/room numbers are text cells preserving leading zeros. Required text must be non-empty. Trim outer whitespace; preserve source-text case/internal whitespace.
- Dates are ISO YYYY-MM-DD text or actual Excel date cells without times. No ambiguous locale strings or impossible dates. Installation must be on/after purchase.
- Costs are finite non-negative numeric decimals without currency/grouping symbols; lives are positive whole numbers. Reject boolean numeric inputs.
- Locations: HONG_KONG, SINGAPORE, LONDON, JAPAN. Region codes: HK, SG, LDN, JP respectively. Cities for this fixture: Hong Kong, Singapore, London, Tokyo.
- Categories: LIGHTING, WATER_SUPPLY, AIR_CONDITIONING only. Conditions: HEALTHY, ATTENTION_NEEDED, CRITICAL, UNKNOWN. Currencies: HKD, SGD, GBP, JPY, USD. Use canonical English enums.
- Generated IDs use S<seed>-<region>-P01 for a property; append -R001 for room and -A001 for asset. Property codes have at least two digits; room/asset codes at least three. For example S20261002-HK-P01-R001-A001. Allocate A001/A002/A003 to the three categories in the order above; the product's ID grammar does not derive category from suffix.
- A room_id starts with its exact property_id; asset_id starts with its exact room_id. Namespace/region must agree throughout. room_number is a unique text label per property. Use deterministic invoice IDs such as S20261002-INV-HK-001 and text line IDs such as 001.

## 3. Construct the fully populated valid pair

1. Generate four clearly fictional hotel names, three rooms per property and the three required asset records per room. Repeat room assessments consistently. Include all four condition states, representing UNKNOWN with complete recorded metadata. All 26 fields of every baseline row must be populated correctly.
2. Use positive costs, positive integer lives, valid purchase/installation dates and fictional recorder/note text. Use location's usual currency for most rows and include at least one USD transaction; all five supported currencies appear in the valid baseline.
3. Build a distinct invoice item for every target. Reuse invoice IDs where appropriate, preserving unique item IDs. Supply all 12 fields, including fictional suppliers. Change each target's name, dates, useful life and cost visibly; change currency on at least one target while keeping all five supported currencies represented. Reserve financial cases before randomising other values.
4. Use invoice_date at/before the reference date and no earlier than its purchase_date for these coherent samples. Product validation does not impose a new invoice/purchase ordering rule. The valid pair contains one item per target, so every invoice applies without date ties. Invoices may cover only a subset in the product, but this full demonstration covers all 36.
5. Verify initial finance is usable from baseline alone, then compute expected source/effective fields after invoices. All room/property IDs, asset IDs/categories and observations stay unchanged. Invoice-date precedence is independent of service-date depreciation.

The valid pair must have no blank cells, unsupported values, unresolved links or missing-value/zero-cost warnings. Do not put unassessed UNKNOWN, missing installation, omitted suppliers or zero costs in this example; those belong to separate future warning tests. No real names/data or researched-market-price claims.

## 4. Financial cases and expected results

Reserve cases in the updated invoice snapshots, and record the matching baseline values and target IDs in the manifest:

- USD 1,200, installed 2026-01-15, life 12 months: reporting 2026-07-14 gives depreciation USD 500 and remaining USD 700; 2026-07-15 gives USD 600 each. Use different baseline values so the update is visible.
- Service 2026-01-31: month anniversaries 2026-02-28 and 2026-03-31.
- Service 2024-01-31: month anniversaries 2024-02-29 and 2024-03-31.
- Replacement overdue, due on the reference date, within 90 days and beyond the 12-calendar-month window. Choose positive lives/dates giving those outcomes and keep purchase no later than installation.
- At least one baseline before-service case, useful-life cap and zero remaining-value case at the reference date; retain corresponding before/after calculations.

Policy: installation date is the service anchor, otherwise purchase date. Straight-line depreciation uses whole completed months and zero residual. Derive each anniversary from the original service day, clamping to the destination month's last day; cap completed months at life. Depreciation = cost × completed months / life; remaining = cost − depreciation. Replacement = original service date + life months with the same clamping. Use unrounded decimals until display. For USD examples no FX assumptions are needed; do not invent FX configuration outputs.

Expected updated fields and calculated results belong in the manifest, never imported columns. Calculating expected results is fixture verification, not evidence that the product passes tests.

## 5. Construct the invalid pair in the same invocation

Copy the in-memory valid datasets, then deliberately alter selected fields/rows. Preserve the valid outputs unchanged. Record every deliberate error and expected dependent diagnostic; use distinct targets for unrelated defects.

| File | Deliberate defect | Expected validation |
|---|---|---|
| invalid/Assets.xlsx | Change a repeated assessment note on just one row of a room | Inconsistent room baseline blocks entire upload |
| invalid/Assets.xlsx | Change one AIR_CONDITIONING category to LIGHTING while retaining distinct asset IDs | Duplicate lighting and missing air-conditioning block entire upload |
| invalid/Invoices.xlsx | Replace one room_id with a well-formed absent room | Unknown target blocks entire upload |
| invalid/Invoices.xlsx | Set one facility_type to OTHER | Unsupported category blocks entire upload |
| invalid/Invoices.xlsx | Set one currency to EUR | Unsupported currency blocks entire upload |
| invalid/Invoices.xlsx | Set one purchase_date to 2026-02-30 | Impossible date blocks entire upload |
| invalid/Invoices.xlsx | Set another installation_date before purchase_date | Date-order error blocks entire upload |
| invalid/Invoices.xlsx | Set one useful_life_months to 0 | Invalid life blocks entire upload |
| invalid/Invoices.xlsx | Append an exact duplicate of a previously unaltered item row | Duplicate invoice_id/line_id within upload blocks even when identical |
| invalid/Invoices.xlsx | Append another item for a different unaltered target, using a fresh invoice_id/line_id, equal invoice_date and a different positive cost | Conflicting snapshots at that target's maximum invoice date block entire upload |

Default counts: invalid Assets stays at 36 rows; invalid Invoices has 38 rows after the two deliberate additions. Report actual counts if room-count parameters differ. Added duplicate/tie rows are deliberate defects, not unexpected generator mistakes. Ensure the tie's date equals that target's maximum. Do not introduce extra defects through shared mutable objects.

Prerequisites: validate invalid Assets against an empty database. Validate invalid Invoices after committing valid Assets and before valid Invoices. The former must create no records; the latter must change no assets and insert no invoice evidence/history. Valid surrounding rows are not independently importable from a blocked upload. Product execution is pending unless an actual implemented importer is available and exercised.

## 6. Product update semantics to explain in the manifest

- A confirmed invoice applies the full six-field snapshot: name, purchase date, installation date, life, cost and currency. Blank installation clears it; it never means retain the old date.
- Maximum invoice_date controls each existing asset across stored and incoming items. Older new items are historical-only. Different snapshots at the controlling maximum date block; equal snapshots with distinct identities coexist as evidence without replaying an already applied update.
- With no applied invoice the first accepted snapshot applies, irrespective of baseline purchase date. A strictly newer invoice replaces manual edits to these fields and clears active paired financial overrides, preserving before/after and override history. Older/equal-date evidence leaves edits/overrides intact.
- Baseline re-imports and identical invoice-item re-imports skip by preserved source equality; modified content under an existing source identity conflicts. They never restore prior operational values. Filename, order and formatting do not determine equality.
- Reset restores the latest applied invoice cost/currency, or baseline values if there is no applied invoice. Identity, room, category, observations and tickets remain fixed. Finance recalculates after applied updates.
- Uploads are independently previewed/confirmed and atomic: any blocker prevents all source/evidence/asset/history writes. Preview counts are proposed; actual counts require successful commit.

Do not generate extra workbooks to demonstrate history ordering, manual edits, missing optional values or rollback. Describe those as future product acceptance scenarios, with prerequisite state and expected outcome.

## 7. Saved-file verification and delivery

Reopen all four saved files and verify:

1. Exact file/sheet layout, exact 26/12 headers, text ID cells, numeric costs/lives and valid-source date cell types; no forbidden formulas/merges/extra sheets.
2. Valid baseline counts: 4 properties, 12 rooms, 36 unique assets and exactly one of each category per room; every field populated and all repeated room/property values consistent.
3. Valid invoice count 36, unique composite IDs, existing targets, positive costs/lives, supported currencies and complete valid dates/suppliers. Apply snapshots in an independent in-memory model to confirm the 36 expected updates and unchanged room/identity/assessment values.
4. Baseline and invoice examples both cover all four locations/five currencies; financial case results and before/after mappings match the manifest.
5. Invalid files retain every declared defect, intended additions and correct surrounding data. Cross-check the mutation list against a valid/invalid comparison, allowing documented dependency diagnostics.
6. Manifest includes seed, parameters, reference date, actual row counts, fictional disclaimer, schemas, case mappings, before/after update values, invalid coordinates/prerequisites/expected blockers and actual verification methods/results.

Deliver links to the four workbooks and manifest. Separate saved-file/static verification from application validation. Report any failed/unavailable check honestly; do not claim the product rejected files unless it was executed. Correct unintended generation defects before delivery. If generation cannot run, preserve the instructions and disclose the limitation without invented links or passing results.

## 8. Copyable invocation

> Follow docs/sample-excel-generation-instructions.md to generate one combined fictional sample set with both valid and invalid Assets.xlsx and Invoices.xlsx. Use seed 20261002 and financial reference date 2026-10-02, four properties and three rooms per property. Include exactly the three fixed assets in every room, fully populate the valid files, demonstrate invoice-driven updates, verify all four saved workbooks and provide the generation manifest. Generate no extra workbook variants or PDFs.

For larger sets, change rooms per property while retaining the four locations and exactly three asset records per room. Both valid and invalid generation always remain required.

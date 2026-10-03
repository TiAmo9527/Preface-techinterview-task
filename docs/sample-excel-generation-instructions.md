# AI instructions: Generate baseline and invoice-update Excel samples

Version: 0.5

Revised: 2026-10-03

Use this document as one self-contained generation prompt. This document creates no workbooks by itself.
Existing supplied files are inventoried in [fixture evidence](../sample/2026-10-03/fixture-inventory.md).
Future regeneration and application validation remain NOT RUN.
[Contracts](data-contracts.md) and [sample scope](sample-data-plan.md) define the same model.
Report discrepancies before generating incompatible files. Use the [shared glossary](glossary.md).

Exact parsing contracts are approved. Existing sample/2026-10-03 files are the default input basis.
This generation procedure applies only to a later explicit regeneration request. Preserve those existing files.

## 1. Request, outputs, and defaults

Generate exactly four .xlsx files and one external manifest:

```text
<run>/valid/Assets.xlsx
<run>/valid/Invoices.xlsx
<run>/invalid/Assets.xlsx
<run>/invalid/Invoices.xlsx
<run>/generation-summary.md
```

Generate both valid and invalid examples in one invocation. Invalid generation is mandatory.
Each example contains the two workbook types. Product uploads remain independent.
The product imports Assets first, then Invoices for existing room/category records.
Do not describe a required paired or four-file upload.

Do not generate extra workbook variants, PDFs, attachment links, FX files, or maintenance imports.
Do not edit application code, install dependencies, commit files, or publish artifacts.

| Parameter | Default |
|---|---|
| Seed | 20261002 |
| Financial reference date | 2026-10-02 |
| Properties | Hong Kong, Singapore, London, Tokyo in Japan. Four total. |
| Rooms per property | 3 |
| Assets per room | Exactly one LIGHTING, one WATER_SUPPLY, one AIR_CONDITIONING. Not configurable. |
| Valid invoice items | One per asset. Thirty-six with default room count. |
| Mode | Fully populated valid and deliberately invalid examples together. |
| Run root | sample_data/spreadsheets/generated/seed-20261002 |

State the chosen parameters and output directory before generation. Record them in the manifest.
Use one seeded generator, deterministic iteration, and reserved financial cases.
The same parameters must produce logically identical records. Different seeds require different identity namespaces.

Use a new seed when independent dataset parameters change. Changed content under existing identities intentionally conflicts.
Choose a fresh run suffix when artifacts exist. Keep existing artifacts intact.
The reference date controls financial examples, not the operational clock.

## 2. Exact example schemas and common rules

Each file contains one sheet. Row 1 contains the following exact headers in the stated order.
Data starts at row 2. Include headers for optional values.
Do not include titles, totals, formulas, merged cells, hidden helpers, charts, extra sheets, or calculated financial columns.

Freeze row 1. Enable filters. Set readable column widths.
Place disclaimers and explanations in the manifest.
Header order is fixed for these examples. The approved product parser permits other orders.

### Assets.xlsx / Assets: 26 columns

```text
property_id, property_name, location, city, room_id, room_number,
lighting_status, lighting_observed_on, lighting_recorder, lighting_note,
water_supply_status, water_supply_observed_on, water_supply_recorder, water_supply_note,
air_conditioning_status, air_conditioning_observed_on, air_conditioning_recorder, air_conditioning_note,
asset_id, asset_name, facility_type, purchase_date, installation_date,
useful_life_months, acquisition_cost, currency
```

All master values require information except installation_date.
Recorded observations require status, date, and recorder, including UNKNOWN. The note is optional.
All absent values, or UNKNOWN alone, mean unassessed UNKNOWN.
Metadata without status and missing required metadata are invalid.
The valid example supplies every assessment field, note, and installation date.

Repeat the same property, room, and assessment information across each room's three asset rows.
Require one record per category. Empty rooms, fourth categories, duplicate categories, and repeated-value disagreements are invalid.
Baseline cost/currency belong here. No invoice links are required.

### Invoices.xlsx / Invoices: 12 columns

```text
invoice_id, line_id, room_id, facility_type, asset_name, purchase_date,
installation_date, useful_life_months, acquisition_cost, currency,
invoice_date, supplier_name
```

All values require information except installation_date and supplier_name.
Populate those optional values in the valid example. asset_name also supplies the purchased-item description.
Do not add description or invoice_file columns.
Each item targets an existing baseline room/category pair.

invoice_id can repeat across different items. invoice_id plus line_id must remain unique.
There is no asset creation, room creation, quantity allocation, or cumulative repair cost.

### Types, enums, and identities

- Store identities and room numbers as text cells with leading zeros preserved.
- Require non-empty text where required.
- Trim outer whitespace and preserve source case/internal whitespace.
- Use ISO YYYY-MM-DD text or Excel date cells without times.
- Reject ambiguous locale strings and impossible dates.
- Keep installation on or after purchase.
- Use finite non-negative numeric decimals for costs without currency/grouping symbols.
- Use positive whole numbers for useful life.
- Reject boolean numeric values.

| Kind | Allowed values |
|---|---|
| Location | HONG_KONG, SINGAPORE, LONDON, JAPAN |
| Region | HK, SG, LDN, JP, matching the locations above |
| Fixture city | Hong Kong, Singapore, London, Tokyo |
| Category | LIGHTING, WATER_SUPPLY, AIR_CONDITIONING |
| Condition | HEALTHY, ATTENTION_NEEDED, CRITICAL, UNKNOWN |
| Currency | HKD, SGD, GBP, JPY, USD |

Use S<seed>-<region>-P01 for property identities. Add -R001 for rooms and -A001 for assets.
Property codes require at least two digits. Room and asset codes require at least three digits.
Example: S20261002-HK-P01-R001-A001.
Allocate A001, A002, and A003 to the three categories in the stated order.

The product grammar does not derive category from the suffix.

Room identities require the exact property prefix. Asset identities require the exact room prefix.
Namespace and region must agree. room_number is a unique text label within the property.
Use deterministic invoice identities such as S20261002-INV-HK-001. Use text line identities such as 001.

## 3. Construct the fully populated valid pair

1. Generate four clearly fictional property names.
2. Generate three rooms per property with three required category records each.
3. Repeat room assessments consistently.
4. Include all four condition states with complete recorded metadata, including UNKNOWN.
5. Populate every baseline field correctly.
6. Use positive costs, positive integer lives, valid dates, and fictional notes/recorders.
7. Use each location's usual currency for most records.
8. Include USD transactions and all five currencies.
9. Reserve financial cases before randomizing other values.
10. Generate a distinct invoice item for every target.
11. Reuse invoice identities only with unique line identities.
12. Populate all invoice fields, including supplier and installation.
13. Change each target's name, dates, useful life, and cost visibly.
14. Change currency on at least one target.
15. Retain all five currencies in the updated snapshots.
16. Use invoice dates no later than the reference date and no earlier than purchase for these coherent examples.
17. Check baseline finance without invoices.
18. Calculate expected current and effective values after invoices.
19. Check unchanged property, room, asset identities, categories, and observations.

The product does not impose invoice/purchase date ordering. That ordering is a fixture coherence choice only.
One invoice per target avoids date ties in this valid pair.
The product permits subsets, but these examples update all thirty-six assets.
Do not include blanks, zero costs, unassessed UNKNOWN, missing suppliers, unsupported values, or unresolved links in the valid pair.
Separate future fixtures cover warnings and missing information.

Do not use real names or claim researched market prices.

## 4. Financial cases and expected results

Reserve updated snapshots for these cases. Record corresponding baseline values and target identities in the manifest.

| Case | Expected result |
|---|---|
| USD 1,200, service 2026-01-15, life twelve months, reporting 2026-07-14 | Depreciation USD 500. Book value USD 700. |
| Same asset, reporting 2026-07-15 | Depreciation USD 600. Book value USD 600. |
| Service 2026-01-31 | Anniversaries 2026-02-28 and 2026-03-31. |
| Service 2024-01-31 | Anniversaries 2024-02-29 and 2024-03-31. |
| Replacement before, on, within ninety days, and beyond twelve months from the reference date | Correct overdue, due-today, due-soon, and excluded-future-window outcomes. |

Use different baseline values to make updates visible.
Include baseline before-service, life-cap, and zero-book-value cases. Retain their before/after calculations.
Keep purchase no later than installation.

Calculation rules:

1. Use installation as service anchor, or purchase when installation is absent.
2. Use straight-line depreciation with zero residual and whole completed months.
3. Derive anniversaries from the original service day.
4. Clamp to each destination month's last day when necessary.
5. Cap completed months at useful life.
6. Calculate depreciation as cost × capped months ÷ useful-life months.
7. Calculate book value as cost minus depreciation.
8. Calculate replacement as service anchor plus useful-life months with the same clamping.
9. Keep unrounded decimal results until display.

USD examples require no invented FX assumptions. Do not generate FX configuration outputs.
Put expected fields and calculations in the manifest, not source columns.
Fixture calculations do not establish passing application tests.

## 5. Construct the invalid pair

Copy the in-memory valid records. Keep valid outputs unchanged.
Mutate distinct targets for unrelated defects. Record each error and expected dependent diagnostic.

| File | Deliberate defect | Expected blocker |
|---|---|---|
| invalid/Assets.xlsx | Change one repeated assessment note for one room row. | Inconsistent room baseline. |
| invalid/Assets.xlsx | Change AIR_CONDITIONING to LIGHTING while preserving distinct asset identities. | Duplicate Lighting and missing Air conditioning. |
| invalid/Invoices.xlsx | Set a well-formed but absent room identity. | Unknown target. |
| invalid/Invoices.xlsx | Set facility_type to OTHER. | Unsupported category. |
| invalid/Invoices.xlsx | Set currency to EUR. | Unsupported currency. |
| invalid/Invoices.xlsx | Set purchase_date to 2026-02-30. | Impossible date. |
| invalid/Invoices.xlsx | Set another installation date before purchase. | Invalid date order. |
| invalid/Invoices.xlsx | Set useful_life_months to 0. | Invalid useful life. |
| invalid/Invoices.xlsx | Append an exact duplicate of an otherwise unaltered item. | Duplicate invoice/line identity. |
| invalid/Invoices.xlsx | Append a fresh item identity at another target's maximum date with different positive cost. | Different controlling-date snapshot. |

Default invalid counts are thirty-six Assets rows and thirty-eight Invoices rows.
Report actual counts for other room parameters. Extra rows represent deliberate defects, not generator mistakes.
The equal-date conflict must use the target's maximum date. Avoid extra unintended errors from shared mutable records.

Application-validation prerequisites:

1. Use an empty isolated store for invalid Assets.
2. Expect no property, room, asset, or observation writes.
3. Use a valid baseline without applied valid invoices for invalid Invoices.
4. Expect no invoice evidence, asset update, override change, or history writes.

Valid surrounding rows cannot commit from a blocked upload. Application execution remains pending unless an implemented importer actually runs.

## 6. Explain update semantics in the manifest

- Applied invoices replace all six snapshot fields.
- Blank installation clears the old date and uses purchase fallback.
- Maximum invoice_date controls source updates across stored and incoming items.
- Older new items remain historical-only.
- Different controlling-date snapshots block the whole upload.
- Equivalent tied identities remain evidence without replaying an applied update.
- The first invoice applies regardless of baseline purchase date.
- Strictly newer invoices replace manual edits and clear active overrides with before/after history.
- Older and equivalent equal-date items preserve manual edits and overrides.
- Identical baseline/invoice repeats skip by preserved source equality.
- Changed evidence under an existing identity conflicts.
- Filename, row order, and formatting do not set source equality.
- Reset restores latest applied invoice values or baseline fallback.
- Identity, room, category, observations, and tickets stay fixed.
- Applied updates recalculate financial and replacement outputs.
- Preview counts are proposed. Actual counts require a successful atomic commit.

Describe extra ordering, warning, repeat, cancellation, stale-preview, and rollback cases as future acceptance checks.
Do not generate extra workbooks for those cases. Give each future case its own prerequisite state.
Shared-store rehearsal reset follows [the demo](demo.md). Isolated test stores remain required for independent checks. Fixture reference dates do not change the operational clock.

## 7. Saved-file checks and delivery

Reopen all four saved files.

1. Check filenames, single sheets, exact 26/12 headers, and text identity cells.
2. Check numeric costs/lives and supported date cell representations.
3. Check that formulas, merges, helper columns, and extra sheets are absent.
4. Check four properties, twelve rooms, thirty-six unique baseline assets, and three categories per room.
5. Check complete valid fields and consistent repeated property/room information.
6. Check thirty-six unique valid invoice items with existing targets.
7. Check supported currencies, positive costs/lives, and complete valid dates/suppliers.
8. Apply snapshots in an independent in-memory model.
9. Check thirty-six expected updates and unchanged identities, categories, rooms, and observations.
10. Check four locations and five currencies in each valid file.
11. Check financial cases and before/after mappings against the manifest.
12. Compare valid/invalid records against every declared mutation and added row.
13. Check intended dependency diagnostics without extra defects.
14. Record seed, parameters, reference date, counts, schemas, fictional disclaimer, and case mappings in the manifest.
15. Record source coordinates, invalid values, prerequisites, expected blockers, methods, and actual check results.
16. Correct unintended generation defects before delivery.
17. Deliver links to all four files and the manifest.

Separate saved-file checks from application validation.
Report failed or unavailable checks. Do not claim product rejection unless the importer actually ran.
If generation cannot run, preserve the instructions. Do not invent output links or passing results.

## 8. Copyable invocation

1. Follow docs/sample-excel-generation-instructions.md.
2. Generate one combined fictional valid/invalid Assets and Invoices sample set.
3. Use seed 20261002 and financial reference date 2026-10-02.
4. Use four properties and three rooms per property.
5. Include exactly three fixed categories in each room.
6. Populate every valid field.
7. Demonstrate invoice updates.
8. Check all four saved workbooks.
9. Provide the generation manifest.
10. Do not generate extra workbook variants or PDFs.

For larger examples, change rooms per property only. Keep four locations and three categories.
Both valid and invalid generation remain required.

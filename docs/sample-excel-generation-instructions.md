# AI instructions: Generate fictional hotel Excel samples

Use this document when asking an AI to generate random, import-ready hotel sample workbooks. It is a generation prompt, not application code or an import-format change. This document alone does not execute generation.

If working in this repository, first read [data contracts](data-contracts.md) and [sample-data plan](sample-data-plan.md). Their current layouts are technical proposals; this prompt targets that documented layout without declaring it newly approved. If these instructions disagree with newer contracts, report the discrepancy before generating incompatible files. When using this prompt outside the repository, the schema reference below makes it self-contained.

## 1. Request and parameters

Generate four separate Excel workbooks containing fictional property, room, asset, and invoice-line source tables. Randomise names, values, and ordinary dates while preserving relationships and required scenario coverage.

Use these defaults unless the requester supplies alternatives:

| Parameter | Default |
|---|---|
| Random seed | 20261002 |
| Financial reference date | 2026-10-02 |
| Properties | 4: Hong Kong, Singapore, London, Tokyo (Japan) |
| Rooms per property | 3 |
| Assets per room | 3: one lighting, one water-supply, one air-conditioning |
| Invoice lines | One distinct line for each asset: 36 lines by default |
| Mode | Valid samples only; invalid batches are opt-in |
| Output directory | sample_data/spreadsheets/generated/seed-20261002/valid, adjusting the seed segment as needed |

The reference date is a fixture-generation anchor, not permission to change the application's operational clock. Produce logically identical records for the same seed and parameters. Use a seeded random generator for all random choices. A different seed uses a different ID namespace so independent sample sets do not accidentally collide on import.

Use a new seed when changing parameters for an independent sample set. Reusing existing IDs with changed source values intentionally creates import conflicts.

Create the four .xlsx files and a generation-summary.md manifest outside the workbooks. Keep existing files intact: if the output directory contains earlier artifacts, choose a new run directory and report it. Generate spreadsheets only; invoice PDFs, FX configuration, maintenance imports, application edits, dependency installation, commits, and publication require a separate request. Set invoice_file blank when no accompanying invoice exists.

Completion: state the selected seed, reference date, output directory, and mode before generation; retain them in the manifest.

## 2. Construct the linked records

1. Create four fictional hotel names, one per required location. Use Tokyo as the Japanese city. Explicitly identify names as fictional in the manifest and property names.
2. Generate portfolio-unique text IDs, for example S20261002-P-HK, S20261002-R-HK-001, and S20261002-A-HK-001-LIGHT. Preserve leading zeros. Room numbers are text and unique within each property.
3. Create the configured number of rooms/assets (default: three rooms per property and three assets per room). Preserve at least one lighting, water-supply, and air-conditioning asset in every room. Every room references a property in Properties; every asset references a room in Rooms.
4. Generate a distinct invoice line per asset. Multiple lines may share an invoice_id, but each invoice_id + line_id pair is unique. Each asset references exactly one line, and no line is shared by assets.
5. Put acquisition_cost and currency in InvoiceLines only. Use fictional item/supplier names and the same item description consistently across invoice and asset evidence. Generate non-negative finite costs and positive whole-month useful lives. Label random costs as fictional nominal amounts, not researched market prices.
6. Use HKD for most Hong Kong items, SGD for Singapore, GBP for London, and JPY for Tokyo; include at least one USD transaction so all five supported currencies are represented. This is fixture variety, not a rule requiring hotel currency to match location.
7. Use calendar dates, with installation on/after purchase when present. Reserve required date-boundary examples first, then randomise remaining past purchase dates and reasonable installation delays. Missing installation triggers a purchase-date fallback warning.
8. Generate latest room-system observations independently of invoices. Recorded assessments require status, observed_on, and a fictional recorder. Optional notes may be blank. Unassessed UNKNOWN has blank date, recorder, and note.

Completion: every asset resolves asset → room → property and asset → invoice line; all identities and invoice links are unique before writing files.

## 3. Required valid-sample coverage

Reserve records for these cases; randomisation must not remove them:

- All four condition states somewhere in the room observations: HEALTHY, ATTENTION_NEEDED, CRITICAL, UNKNOWN.
- At least one unassessed UNKNOWN, one recorded UNKNOWN with metadata, and one group whose four observation values are blank and therefore default to UNKNOWN.
- At least one missing installation date, one zero-cost line, and one omitted optional supplier. These are valid cases/warnings, not blocking errors.
- Replacement overdue, due today, within 90 days, and beyond the 12-month horizon relative to the reference date. Choose an in-service date and whole-month life that produce each required date exactly; ensure purchase is no later than service.
- An asset costing USD 1,200 with in-service date 2026-01-15 and useful life 12 months. The manifest records the policy examples: on 2026-07-14, depreciation USD 500 and remaining USD 700; on 2026-07-15, USD 600 each.
- An in-service date of 2026-01-31: anniversaries 2026-02-28 and 2026-03-31.
- An in-service date of 2024-01-31: anniversaries 2024-02-29 and 2024-03-31.

Record the case-to-asset/room mapping in the manifest. Derived financial values belong in that explanatory manifest, not imported columns. The examples express required policy outcomes; they are not evidence that the application calculates correctly.

## 4. Exact workbook schema reference

Write exactly one sheet per workbook. Row 1 is the header; data begins at row 2. Retain optional columns even when their values are blank. Use these headers in this order.

### Properties.xlsx / Properties

```text
property_id, property_name, location, city
```

All values required. location uses HONG_KONG, SINGAPORE, LONDON, JAPAN. city uses Hong Kong, Singapore, London, Tokyo for the default fixture.

### Rooms.xlsx / Rooms

```text
room_id, property_id, room_number,
lighting_status, lighting_observed_on, lighting_recorder, lighting_note,
water_supply_status, water_supply_observed_on, water_supply_recorder, water_supply_note,
air_conditioning_status, air_conditioning_observed_on, air_conditioning_recorder, air_conditioning_note
```

room_id, property_id, room_number required. Observation values follow section 2. Allowed states: HEALTHY, ATTENTION_NEEDED, CRITICAL, UNKNOWN. A supplied assessment date without a status/recorder, or a non-UNKNOWN state without metadata, is invalid. Blank means an empty cell, not the strings null, None, N/A, or Unknown.

### Assets.xlsx / Assets

```text
asset_id, room_id, asset_name, facility_type, purchase_date,
installation_date, useful_life_months, invoice_id, line_id
```

All values except installation_date required. Allowed facility types: LIGHTING, WATER_SUPPLY, AIR_CONDITIONING, OTHER. The default fixture uses the first three. useful_life_months is a positive integer. Cost, currency, depreciation, book value, override, ticket, and provenance columns are absent from this source table.

### InvoiceLines.xlsx / InvoiceLines

```text
invoice_id, line_id, description, acquisition_cost, currency,
invoice_date, supplier_name, invoice_file
```

The first five values are required; the final three are optional. Allowed currency values: HKD, SGD, GBP, JPY, USD. Costs are numeric decimals with no currency symbols or thousands separators. invoice_file is blank unless the named fictional invoice is actually supplied; no invented attachment links.

### Workbook presentation and cell types

- Use actual .xlsx files, with text IDs/room numbers, numeric costs/lives, and ISO YYYY-MM-DD date text or valid Excel date cells without times.
- Use exactly the source headers and canonical English enum values regardless of interface language.
- Freeze the header row, enable filters, and size columns for legibility without changing the schema.
- Keep data plain: no formula cells, merged cells, title/disclaimer rows, totals, charts, extra columns, or additional report/summary sheets. Put the fictional-data disclaimer in the manifest instead.

Completion: reopen all four saved workbooks and verify sheet names, exact headers, cell types, and row counts against the in-memory records.

## 5. Optional deliberately invalid batches

Run this branch only when the requester asks for invalid import examples. Preserve the valid set. Create a complete four-file copy per case under sample_data/invalid/generated/seed-<seed>/<case>; retain all four files except in a case deliberately testing a missing file.

Change one rule per case where possible:

| Case | Deliberate change | Expected result |
|---|---|---|
| unknown-room | One asset references an absent room_id | Whole batch blocked |
| duplicate-id | Duplicate one asset_id inside Assets | Whole batch blocked |
| shared-invoice-line | Two distinct assets reference one line | Whole batch blocked |
| unsupported-currency | One invoice line has EUR | Whole batch blocked |
| invalid-installation | One installation date precedes purchase | Whole batch blocked |
| invalid-life | One useful_life_months becomes zero | Whole batch blocked |
| incomplete-observation | HEALTHY is supplied without recorder/date | Whole batch blocked |
| missing-header | Remove one required column | Whole batch blocked |
| changed-existing-source | Change one source value after the valid baseline is imported | Whole batch blocked on that existing ID |

For each case record file, sheet, Excel row, field, deliberate error, prerequisite state, and expected result in a manifest. Valid rows in an invalid batch must not be described as importable separately. Conflicting-existing-source tests require the valid baseline first; they are not standalone invalid data on an empty database.

For repeat-import examples, copy/rename the valid workbooks without changing meaningful field values; expected result after baseline import is skipped identical records. Do not regenerate random values under the same IDs to simulate an identical repeat.

## 6. Verify and deliver

After saving, reload files and check:

1. Exactly four supported workbooks with the sole required sheet and complete headers.
2. Default counts: 4 properties, 12 rooms, 36 assets, 36 unique invoice lines.
3. Required values, text identity/room-number cells, enum sets, valid dates, non-negative costs, and positive integer lives.
4. Unique IDs/composite line IDs, room-number uniqueness, complete property/room links, and one-to-one asset/line linkage.
5. Installation not before purchase and valid conditional observation metadata.
6. Presence of every coverage case and expected date/value examples in the manifest.
7. Optional invalid copies contain their declared defect, without unintended additional defects wherever possible.

Deliver links to all workbooks plus the manifest. Report actual checks, counts, seed, reference date, scenario mappings, warnings, and remaining limitations. Correct generation defects before delivering the valid set. If spreadsheet creation or verification cannot run, disclose that limitation and preserve the instructions rather than present invented file links or passing checks.

## 7. Copyable invocation

> Follow docs/sample-excel-generation-instructions.md to generate the valid four-file fictional hotel sample set. Use seed 20261002 and financial reference date 2026-10-02. Verify the saved workbooks and provide file links and the generation manifest. Generate no invalid batches unless requested.

For a larger random sample, specify rooms per property and assets per room explicitly; retain four locations and at least one of each required facility per room. For isolated failure examples, append: "Also generate the optional invalid-batch cases, each separate from the valid set."

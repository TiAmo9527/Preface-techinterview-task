# Sample-data and import-template plan

Version: 0.4

Revised: 2026-10-03

Owner: Alex

Status: Owner-approved fixture scope. Generation and application validation: NOT RUN.

Use the [product specification](product-spec.md), [contracts](data-contracts.md), and [shared glossary](glossary.md).
Owner confirmation dated 2026-10-03 preserves the fixture decisions. It does not approve every technical parsing proposal.

## 1. Dataset scope

Use four fictional properties in Hong Kong, Singapore, London, and Tokyo, Japan.
Use three rooms per property, twelve rooms total. Use thirty-six assets, one per required category in each room.
Three categories are universal product constraints. The four-property fixture size is not a capacity limit.

Assets supplies complete baseline values without invoices. Invoices supplies replacement snapshots for existing room/category records.
There is no manual asset creation, fourth category, empty-room import, or quantity allocation.
Asset identities remain stable through replacements. Invoices leave observations and maintenance links unchanged.
Managers can edit permitted fields and apply financial overrides.

All names, suppliers, recorders, identities, and amounts are fictional. Do not use real customer or hotel data.

## 2. Templates and combined generation

[Generation instructions](sample-excel-generation-instructions.md) define one invocation with both valid and invalid examples.

| File in each example | Sole sheet | Row meaning |
|---|---|---|
| Assets.xlsx | Assets | One baseline asset with repeated property, room, and assessment information. |
| Invoices.xlsx | Invoices | One invoice item with an existing target and full replacement snapshot. |

Generate four sample files across valid/invalid folders and one external manifest.
Product uploads remain independent. A folder containing both files does not require paired uploads.
Later blank templates use the same headers without rows.
No formulas, calculated financial columns, totals, merged cells, extra sheets, or explanation columns belong in sources.
Canonical headers and enums remain independent of UI language.

Default future root: sample_data/spreadsheets/generated/seed-20261002.
Use valid and invalid subfolders with generation-summary.md at the root.
Use a fresh suffix when that root exists. Do not overwrite artifacts.
Supplied fictional fixtures belong in sample_data. Imported local state belongs in ignored runtime.

Do not generate PDFs, attachment fields, or FX configuration files.

## 3. Fully populated valid pair

Assets contains thirty-six rows, four properties, and twelve rooms. Every one of its 26 fields is populated correctly.
Repeat room assessments consistently. Include all four condition states with recorded metadata, including UNKNOWN.
Supply optional notes and installation dates. Use positive costs, valid dates, supported currencies, and positive whole useful lives.

The valid pair produces no missing-value or zero-cost warnings.

Invoices contains thirty-six rows, one per target. Populate all twelve fields, including supplier and installation date.
Use unique item identities. Change names, dates, useful lives, and costs visibly.
Change supported currency on at least one target. Retain all four locations and five currencies in both valid files.

The manifest records baseline and updated fields with expected calculated results.
Expected invoice result: thirty-six stored items and thirty-six distinct asset updates.
Invoice dates control ordering. Purchase/installation dates control service calculations.
Amounts are not researched prices. Actual fixed FX configuration remains separate future work.

## 4. Invalid pair and prerequisites

Copy valid records before introducing deliberate defects. Preserve valid outputs.
Record source coordinates, original/invalid values, prerequisites, expected blockers, and dependent diagnostics.

| File | Deliberate defects | Independent prerequisite | Expected product result |
|---|---|---|---|
| invalid/Assets.xlsx | Repeated assessment disagreement and duplicate category with a missing category. | Empty isolated store. | Reject the whole upload without entity or observation writes. |
| invalid/Invoices.xlsx | Unknown room, unsupported category/currency, duplicate identity, impossible dates, installation-before-purchase, invalid life, and controlling-date conflict. | Valid baseline without applied valid invoices. | Reject the whole upload without evidence, asset, or history changes. |

Purchase before installation is valid. Installation before purchase is the date-order defect.
Use distinct targets for unrelated errors. Add deliberate duplicate and conflicting rows when required.
Manifest counts must match actual files. The equal-date conflict must occur at the controlling maximum date.

Changed-existing-source conflicts are not standalone empty-store defects.

## 5. Separate acceptance coverage

Do not introduce blanks or warnings into the fully populated valid pair.
Define separate future fixtures for:

- Baseline-only initialization, invoice subsets, unknown targets, completeness, and repeated-value consistency.
- Identical/changed source identities and repeats after manager edits.
- Newest-date ordering, older evidence, conflicting controlling ties, and equivalent ties.
- Applied replacement, override clearing, source reset, and unchanged observations/tickets.
- Missing installation, explicit zero cost, missing supplier, and unassessed UNKNOWN.
- Invalid assessment metadata, cancellation, stale previews, and persistence failure.
- Before-service, month-end, leap-year, useful-life cap, and replacement endpoints.
- Unique-asset financial totals despite multiple invoices or tickets.
- Normal restart and isolated rehearsal stores with retained browser preferences.

Use [acceptance scenarios](acceptance-scenarios.md) for independent starting states and required outcomes.
Create operational fixtures through later application actions or isolated tests. Do not add import workbook types.
Use [the demo](demo.md) for rehearsal. Disclose AR-002's manual-creation gap.

## 6. Evidence status

Generation, saved-file checks, and application validation remain NOT RUN.
Expected calculations are fixture checks, not passing application tests.
Record actual generation results separately from SC/AR application evidence.
The reference date controls financial examples only. It does not change the actual operational clock.

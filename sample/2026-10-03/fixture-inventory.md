# Supplied fixture inventory

Inspected: 2026-10-03. Status: Read-only saved-file structure and difference checks completed. Application validation: NOT RUN.

Alex selected this existing folder as the input basis. Preserve the workbooks and S20261002- identities.
The folder date identifies the supplied collection, not a proven generator execution date.
Original generation provenance is unverified. No workbooks were generated or modified in this revision.

## File evidence

All files have the required sole sheet, no formulas, no merged cells, and text identity cells.
Each inspection sidecar's full table values match the actual workbook after calendar-date normalization.
Headers match the approved Assets 26-column and Invoices twelve-column interfaces.

| File | Sole sheet | Data rows | Columns | SHA-256 |
|---|---|---|---|---|
| [invalid/Assets.xlsx](invalid/Assets.xlsx) | Assets | 36 | 26 | caf81d1c37cec01be4715a1498193049dca64c93967d4fb0e36a262e527c3aad |
| [invalid/Invoices.xlsx](invalid/Invoices.xlsx) | Invoices | 38 | 12 | 7b933802f6e7382e1138801e3a707a56d3a89564981cfbcf9bc5a6ce3b24b72d |
| [valid/Assets.xlsx](valid/Assets.xlsx) | Assets | 36 | 26 | 16862ba1ec2b12cf07d24459c9f024d15b705dd7cd44b91970cef8e9a79a2647 |
| [valid/Invoices.xlsx](valid/Invoices.xlsx) | Invoices | 36 | 12 | 1bae2192e28d52e66304af07c9d15a602df0d2d9c0aa76f124eedef45164edb7 |

## Expected import outcomes and prerequisites

| Input | Independent prerequisite | Expected application outcome |
|---|---|---|
| valid/Assets.xlsx | Empty test/demo store | Four properties, twelve rooms, thirty-six assets and consistent assessments. No missing-value/zero-cost warnings. |
| valid/Invoices.xlsx | Its valid Assets baseline, no previous invoices | Thirty-six stored items, thirty-six distinct asset updates, preserved baselines, and linked update history. |
| invalid/Assets.xlsx | Empty isolated test store | All baseline writes rejected. Counts remain zero. |
| invalid/Invoices.xlsx | Its valid Assets baseline, no previous invoices | All evidence, asset, and history writes rejected. Baseline state remains intact. |

The valid files contain all five supported currencies and no blank cells.
Sources carry no calculated finance columns. Application calculations remain unverified.
For the live demonstration, reset establishes empty state. Automated checks use separate temporary stores.

## Deliberate invalid differences

| File | Coordinates | Actual defect | Expected diagnostic |
|---|---|---|---|
| invalid/Assets.xlsx | J2 versus J3/J4 | Different lighting note for the same room | Inconsistent repeated room assessment, with all contributing coordinates. |
| invalid/Assets.xlsx | U7 versus U5/U6 | AIR_CONDITIONING changed to LIGHTING | Duplicate LIGHTING category and missing AIR_CONDITIONING in that room. |
| invalid/Invoices.xlsx | C2 | Unknown room S20261002-HK-P01-R999 | Unknown invoice target. |
| invalid/Invoices.xlsx | D3 | Unsupported OTHER | Unsupported category and unresolved target. |
| invalid/Invoices.xlsx | J4 | Unsupported EUR | Unsupported currency. |
| invalid/Invoices.xlsx | F5 | Impossible 2026-02-30 date | Invalid calendar date. |
| invalid/Invoices.xlsx | G6 versus F6 | Installation 2025-09-24 before purchase 2025-09-25 | Invalid installation ordering. |
| invalid/Invoices.xlsx | H7 | Zero useful_life_months | Useful life must be a positive whole month count. |
| invalid/Invoices.xlsx | A38:B38 versus A8:B8 | Identical appended invoice/line identity | Duplicate identity within the upload, even when values match. |
| invalid/Invoices.xlsx | A39:L39 versus A9:L9; I39 versus I9 | Distinct invoice identity, equal controlling invoice date 2025-06-26, costs 1305.5 versus 1205.5 | Different six-field snapshots at the maximum date for the target. |

Comparison found eight changed original cells and two appended invoice rows, with no other table-value differences.
The duplicate and tied-conflict checks are independent blockers. Dependent diagnostics must not hide the original source errors.
Row numbers above are worksheet coordinates, including the header row.

## Evidence limits

These are actual structural/difference observations and expected domain diagnostics.
They are not PASS results for application imports, persistence, depreciation, or browser behavior.
Use [sample scope](../../docs/sample-data-plan.md), [contracts](../../docs/data-contracts.md), and [verification mapping](../../docs/verification-plan.md).
Correct this inventory if a future authorized fixture change alters a hash, coordinate, count, or prerequisite.

# Sample-data and import-template plan

Version: 0.2

Revised: 2026-10-02

Owner: Alex

Status: Approved fixture scope; proposed layouts/cases; no workbooks, PDFs, or datasets generated

## 1. Approved scope

Four fictional properties: one in Hong Kong, Singapore, London, and Tokyo (Japan). Three rooms per property: twelve rooms total. At least one lighting, water-supply, and air-conditioning asset per room: minimum thirty-six individually tracked assets.

Include fictional invoices with structured invoice lines and one asset per linked line. Managers can later create manual assets without invoice links; do not represent those as imported invoice-backed assets.

Property/supplier/person names, identifiers, dates, costs, owner names, and exact fixed FX rates remain fixture authoring work. Use no real hotel/customer records. Four-location coverage is AR-001; the exact size is owner-approved demonstration scope, not a product record limit.

## 2. Proposed Excel templates

Future blank templates use the layouts in [data contracts](data-contracts.md); this phase documents them only.

For later generation of random sample workbooks or isolated invalid batches, use [AI sample-generation instructions](sample-excel-generation-instructions.md), which define the generation steps and completion checks.

| Future template | Sole sheet | Column groups | Authoring guidance |
|---|---|---|---|
| Properties.xlsx | Properties | property_id, property_name, location, city | One fictional hotel per required location; Japan city Tokyo |
| Rooms.xlsx | Rooms | room_id, property_id, room_number; three system status/date/recorder/note groups | Text IDs/numbers; include assessed and unassessed conditions |
| Assets.xlsx | Assets | asset_id, room_id, asset_name, facility_type, purchase_date, installation_date, useful_life_months, invoice_id, line_id | Cost/currency derive from linked invoice line; omit derived/override fields |
| InvoiceLines.xlsx | InvoiceLines | invoice_id, line_id, description, acquisition_cost, currency, invoice_date, supplier_name, invoice_file | Unique line identity; no bundle/quantity allocation |

All four files are uploaded together. Preserve all template headers, including optional-value columns. Use prescribed canonical English enum values regardless of UI language. Dates use valid Excel dates or ISO YYYY-MM-DD; IDs use Text to retain zeros.

Future template instructions should explain required/optional values, enum choices, invoice linking, zero-cost/install-date warnings, assessed Unknown versus unassessed Unknown, and whole-batch rejection. Templates do not promise arbitrary spreadsheet compatibility.

No online spreadsheet references were used. Browse later only to resolve a concrete contract/design question, and record any reference plus its limited role; a reference never broadens supported inputs automatically.

## 3. Fictional invoice evidence

Plan readable fictional invoices corresponding to structured lines, clearly labelled as fictional. Every imported asset resolves its line cost/currency and traceable invoice identity. Provide no OCR claim. Do not generate invoice PDFs in this documentation phase.

Keep source fixtures in sample_data/spreadsheets and sample_data/invoices, with deliberate invalid fixtures in sample_data/invalid. Local imported/runtime state belongs in runtime and must not be committed. Respect the repository's supplied-development-fixture boundary.

## 4. Valid-case coverage

| Planned case | Purpose and expected behaviour | Trace |
|---|---|---|
| Complete four-location batch | All links valid; all new records commit together after confirmation | US-01, SC-001/002, AR-001 |
| All supported currencies | Complete fixed fictional FX table including USD rate 1 | FR-011/018, SC-003 |
| Assessed Healthy/Attention needed/Critical and assessed Unknown | Metadata retained and condition counts meaningful | FR-009/016 |
| Missing observations and optional installation | Unknown default and visible purchase-date fallback warning | FR-009/011 |
| Zero cost / missing optional supplier | Non-blocking warnings; no fabricated values | US-01/03 |
| Renamed/reordered identical files | Records skip based on meaningful normalised values | FR-005 |
| Re-import after manager asset/observation edits | Preserved source baseline skips; operational edits survive | US-01/03 |
| Manual asset plus paired override/reset | Generated ID, origin label, effective values and history | FR-010/019 |
| Same asset with several tickets | Distinct ticket counts without duplicated financial sums | FR-007/008 |
| Critical room-only versus asset-linked fault | Room issue visible; asset flag only through linkage | US-02/05 |
| Healthy observation with an unresolved fault | Assessment and ticket remain independent | FR-009/016 |

Maintenance examples are created through the application later or isolated test fixtures, not an unapproved fifth import file.

## 5. Deliberately invalid batches and test fixtures

Plan separate altered copies, changing one rule at a time where practical:

- Missing required file/sheet/header; unsupported format/layout.
- Duplicate upload ID or composite invoice-line identity.
- Unknown property/room/invoice link and two assets linked to one line, including an existing link collision.
- Changed meaningful source content for an existing ID.
- Invalid date, installation before purchase, negative cost, unsupported currency, zero/fractional life.
- Invalid observation state, incomplete date/recorder, or orphan metadata.
- A mixed-validity batch: confirmation blocked and every new record remains absent.
- Persistence-failure injection: valid confirmed batch rolls back entirely.
- Incomplete/invalid FX configuration: financial reporting blocked, no partial totals.

Verification should distinguish file/row/conflict blockers from warnings. Invalid sources remain inspectable with coordinates; they never enter operational records.

## 6. Date and presentation fixture coverage

Include dates that allow demonstrations of before-service, ordinary month anniversaries, 31 January month-end, leap-year February, useful-life cap, and replacement overdue/today/90-day/12-month boundaries. Financial-date changes never create maintenance events or alter actual overdue indicators.

Do not freeze the operational clock to match the walkthrough. Before rehearsal, choose financial reporting presets that expose the prepared asset cases. Derive operational ticket target dates from the actual date for a later fictional test fixture.

Use [the existing demo plan](demo.md) for sequence and evidence; do not create a duplicate demo-plan file. English is mandatory; stretch translations require completeness/fallback checks, with linguistic review still deferred. This plan is coverage intent, not test evidence.

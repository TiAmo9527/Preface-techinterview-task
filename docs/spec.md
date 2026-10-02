# Product specification: Hotel asset-management prototype

Status: Revised draft; owner-approved policies recorded below

Owner: Alex

Created: 2026-10-01

Revised: 2026-10-02

Target delivery: 2026-10-05

Version: 0.2

This document defines product behaviour. Approval of the policies in section 15 does not claim client approval, implemented features, or verified application behaviour. Technical contract proposals are identified in [data contracts](data-contracts.md). Architecture and implementation tasks belong in [the delivery plan](plan.md) and [task checklist](tasks.md).

[Assessment requirements](assessment-requirements.md) record external obligations separately. Any contradiction between those obligations and product decisions requires explicit resolution by Alex; neither document silently overrides the other.

## 1. Problem and intended outcome

The fictional hotel portfolio maintains room and asset information across separate spreadsheets and invoices. Managers lack one view connecting facilities, recorded condition, asset details, and maintenance ownership.

The primary outcome is: **Managers can understand a room's facilities and take accountable maintenance action.**

Data consolidation establishes trust. Financial values and replacement information support management decisions and remain secondary.

The primary journey is:

Import and validate source data → review maintenance and condition → inspect a room → assess condition or edit an asset → log or update maintenance.

Users can then review book values and replacement planning. This is a decision-support prototype, not a production hotel-management or accounting-compliance product.

## 2. Users

### Executive

Needs portfolio filters, clearly labelled condition and ticket counts, prioritised maintenance, room drill-downs, acquisition/book values, and secondary replacement visibility.

### Room manager

Needs to inspect and edit assets and room-system assessments across any existing fictional property; log faults, assign owners, and update progress; and distinguish recorded condition from tickets.

### Data-maintenance user

Needs to upload prescribed source tables together, preview diagnostics before saving, establish trustworthy links, and inspect source provenance and conflicts.

These are user perspectives, not permission roles. Authentication and property-level access enforcement are excluded. Property and room master data are import-only; cross-property access does not permit forms to create/edit that master data.

## 3. Product scope

Required capabilities:

- A working web application with the observable workflows below.
- Linked property, room, asset, and invoice-line records from four prescribed Excel files.
- Whole-batch preview/validation, explicit confirmation, atomic commit, and exception reporting.
- Maintenance-first dashboard with location, property, and room filters and room drill-downs.
- Asset creation with generated IDs, permitted asset editing, and explicit financial overrides.
- Separate editable lighting, water-supply, and air-conditioning observations.
- Manual fault logging, owner assignment, progress, and persistent change history.
- Financial calculations, effective transaction-currency/USD display, and secondary replacement planning.
- English interface as mandatory scope. Traditional Chinese, Simplified Chinese, and Japanese are stretch translation sets with English fallback.
- Persistent display preferences, actionable validation, integrity, durable local saves, and reproducible startup.

Assessment coverage and presentation fixtures are defined in [assessment requirements](assessment-requirements.md) and [sample-data plan](sample-data-plan.md), not product-size limits.

Exclusions:

- Arbitrary PDF OCR, arbitrary spreadsheet compatibility, multi-sheet-workbook imports, live FX, sensors, and live-system integrations.
- Authentication/authorisation, real customer/hotel data, and AI features inside the application.
- Import-based updates, property/room editing forms, asset relocation or invoice relinking after creation.
- Bundled purchases or quantity allocation, procurement/payments/orders, and production accounting compliance.
- Automated condition inference, observation history, ticket reopening/deletion/stage skipping, and resolved-ticket editing.

Fictional data only. Confidential assessment materials must not be published. Presentation and optional sharing obligations live in the assessment document.

## 4. Source data, identity, and evidence

The supported input boundary is four separate .xlsx files uploaded as one batch, with one prescribed table sheet each: Properties, Rooms, Assets, and InvoiceLines. All four are required; headers-only tables can represent no new rows. The [data contracts](data-contracts.md) explicitly define fields, canonical values, observation metadata, supported dates, normalisation, and comparison rules.

- Property IDs are unique; room IDs are portfolio-unique; room numbers are unique within their property.
- Asset IDs identify individual items. The system generates a unique ID for a manually created asset.
- Invoice ID plus line ID identifies a line. Every imported asset must link to one valid line; a line must not link to multiple assets, including existing records.
- Relationships use identifiers, never guessed names.
- Imported records retain original source values and file/sheet/row provenance. Imported asset cost/currency originate from the linked invoice line.
- Manually created assets may have no invoice link and are labelled "Manually entered".
- Manager edits replace operational values without rewriting source evidence. Identical repeat imports compare against the preserved source baseline and leave edits intact.
- Changed meaningful source content is a blocking conflict. Filenames, file bytes, and row position do not determine record identity.

Fictional invoices accompany structured invoice lines; invoice PDFs are not an import/OCR path.

## 5. User journeys and acceptance scenarios

Acceptance scenarios describe required verification, not completed tests.

### US-01: Consolidate source records

Priority: Required

As a data-maintenance user, I want to preview all four source files so that a trusted batch can be consolidated without hiding errors.

Journey: select files → preview links/counts/diagnostics → correct blocking errors → confirm a valid batch → inspect actual inserted/skipped counts and provenance.

Acceptance scenarios:

- A valid linked batch writes nothing during preview; confirmation inserts its new records together and reports actual counts.
- An unknown room, missing invoice link, duplicate ID, shared invoice line, invalid observation, or conflicting existing source ID blocks the entire batch, including otherwise valid rows.
- Diagnostics identify file, sheet, row, field, and reason where applicable.
- Missing/unsupported files or unusable columns block confirmation. Correcting and revalidating is required.
- Non-blocking warnings remain visible; a valid warning-only batch can be confirmed.
- An identical existing source record is skipped even if its filename/row changes or its operational asset/observation has been edited.
- A changed existing source baseline conflicts; import never resets operational edits or invoice evidence.
- A commit failure rolls back all new records from the batch and never displays success.

Independent verification compares operational state before preview, after a blocked batch, after a successful confirmation, after repeat import, and after an injected commit failure.

### US-02: Inspect portfolio and room context

Priority: Required

As a manager or executive, I want condition and maintenance results with room context.

Acceptance scenarios:

- One filter scope applies to every metric, table, and replacement result. Changing a parent filter clears incompatible child selections.
- Empty results show an empty state and no stale records.
- The dashboard presents labelled entity/ticket/observation counts and a prioritised unresolved-ticket table before secondary finance and replacement sections.
- Each operational table row drills down to its room, which shows property, three observations, assets, and unresolved/resolved tickets.
- Two tickets for one asset count as two tickets without duplicating asset acquisition value.
- A critical room-only ticket remains visible without flagging all room assets as critically faulty.
- Managers can select any imported property; property/room editing forms are absent.
- Changing the financial reporting date does not change observations, ticket timestamps, or operational overdue ordering.
- A recorded satisfactory assessment saves as Healthy with date/recorder; missing metadata blocks it. Clear removes metadata and returns to Unknown, including after restart.
- Invalid imported observation metadata blocks the whole batch; identical Rooms re-imports do not undo a manager's latest assessment.
- With no saved preference, the interface starts in English/USD. Changing language leaves the currency preference independent; both selected preferences survive browser restart.
- A delivered translation set localises interface text and falls back to English for missing keys without translating stored names, notes, descriptions, IDs, or enums.
- Local mode groups a mixed-currency portfolio into labelled currency totals; USD mode uses the complete configured rate table. Neither mode alters source or override values.

Observation editing is additionally covered by FR-016 and section 9; language/currency behaviour by FR-017–018 and section 13.

### US-03: Maintain asset records

Priority: Required

As a room manager, I want the asset register to reflect current acquisition and service information while retaining source evidence.

Acceptance scenarios:

- Creating a valid manual asset generates a unique ID, places it in its selected room, and labels it Manually entered; no invoice link is required.
- After creation, ID, room association, and invoice linkage remain fixed. Name, facility type, purchase/installation dates, and useful life can be edited.
- Invalid cost/currency, dates, useful life, or relationships block saving with field feedback.
- A paired cost/currency override requires a reason; its history retains before/after values, recorder, and actual timestamp.
- An override changes depreciation, book value, and replacement spending proxies without changing original invoice evidence.
- Reset to source requires a reason, restores the preserved cost/currency pair, and appends history.
- Cancelled/invalid/failed writes leave stored values unchanged. Successful saves survive restart and refresh room/dashboard results.

### US-04: Manage maintenance

Priority: Required

As a room manager, I want faults to have clear ownership and progress.

Acceptance scenarios:

- A new ticket starts Open and may already have an owner. A linked asset must belong to the ticket's room.
- Room/asset associations cannot change after creation.
- Open → In progress requires an owner; In progress → Resolved requires a non-empty resolution note and a recorded resolution timestamp.
- Direct Open → Resolved, reopening, and deletion are disallowed.
- Owner removal is permitted in Open but blocked in In progress; reassignment remains possible while unresolved.
- Unresolved description, severity, target date, owner, and status edits persist with chronological history. Resolved tickets are read-only.
- Unresolved rows sort by severity, then overdue target date, then oldest opening timestamp; resolved tickets appear separately.
- Resolution never changes a room observation or an expected replacement date.

### US-05: Review replacement needs

Priority: Required; secondary presentation

As an executive, I want explainable replacement dates and separate spending proxies.

Acceptance scenarios:

- Replacement dates before/on/after the financial reporting date classify as overdue/due today/future.
- Due soon is strictly after the reporting date through reporting date + 90 days inclusive.
- The 12-month future window excludes overdue/due-today and includes its calendar-month endpoint.
- Overdue, due-today, and future-window spending have separate totals and follow the selected filters.
- Spending uses effective acquisition cost, including overrides, through the fixed FX table; it does not subtract book value.
- An asset's critical unresolved flag requires an explicitly linked ticket; room-only faults remain separate.
- Labels identify an acquisition-cost proxy, not a quotation, inflation allowance, installation-labour estimate, or failure prediction.

## 6. Functional requirements

FR-001: Preserve valid property-room-asset relationships and unique invoice-line linkage.

FR-002: Preview and validate all four source files before explicit confirmation.

FR-003: Distinguish blocking file/row/conflict errors from non-blocking warnings; any blocker prevents the entire batch commit.

FR-004: Keep invalid/conflicting source rows inspectable in diagnostics without creating operational records.

FR-005: Skip identical source records, block changed source IDs and upload duplicates, and never overwrite through import.

FR-006: Filter portfolio outputs by location, property, and room.

FR-007: Show property/room/asset counts; unresolved/critical unresolved ticket counts; observation counts by system/state; prioritised unresolved tickets; acquisition/book values; and secondary replacement counts/proxies. Label units explicitly.

FR-008: Use one consistent filter scope for all outputs, clear incompatible filters, and avoid stale empty results.

FR-009: Show each room's three separate observations, including unassessed Unknown.

FR-010: Generate IDs for manual assets and allow permitted edits; identifiers/associations remain fixed and derived values remain read-only.

FR-011: Display the financial reporting date, calculation assumptions, FX date/disclaimer, and separate current operational date.

FR-012: Create faults, assign owners, and use Open → In progress → Resolved with required transition fields and fixed associations.

FR-013: Persist chronological history of saved unresolved-ticket field changes; resolved tickets are immutable.

FR-014: Provide secondary replacement dates, urgency flags, and separately labelled overdue/due-today/future effective-cost proxies.

FR-015: Persist successful saves and atomic valid imports; cancelled, blocked, invalid, or failed operations must not alter operational records.

FR-016: Edit or clear latest observations, validate assessment metadata, and never infer condition from tickets.

FR-017: Provide English and switchable stretch translation sets for interface text, retaining canonical data values and English fallback.

FR-018: Provide an independent USD/effective-transaction-currency display preference, grouped mixed-currency totals, and persistent language/currency selections.

FR-019: Preserve invoice/source cost evidence and record paired operational overrides/resets with reason and persistent history.

FR-001–015 retain their v0.1 identities; wording is revised. FR-016–019 are additions.

## 7. Import policies

Preview and validation never write operational records. Require all four files. Validate the complete relationship graph against valid batch records and preserved existing records.

Blocking file errors include unsupported/unreadable files, missing tables/headers, or structurally unusable identifiers. Blocking row errors include missing required fields, duplicates, unknown relationships, invalid dates/observations, unsupported currencies, negative costs, non-positive useful life, multiple links to one invoice line, and changed source-ID conflicts.

An error in any file/row blocks every new record in that batch. Do not offer an import-valid-rows action. Warnings include absent installation date (purchase fallback), zero cost, optional supplier omission, and identical existing records to skip.

Preview reports proposed inserts/skips, blockers, warnings, and dependency errors, with diagnostic coordinates. Only a blocker-free batch can be explicitly confirmed. Commit all its new records together or none. Report actual committed/skipped counts after success. File changes require new validation and confirmation. Detailed comparison and provenance rules are in [data contracts](data-contracts.md).

## 8. Asset and financial rules

An asset requires ID, room, name, facility type, purchase date, cost/currency, and positive whole-month useful life. For imports, invoice lines supply cost/currency; manual creation requires those fields and a generated ID.

Facility types: Lighting, Water supply, Air conditioning, Other. Cost is non-negative; zero cost warns. Installation is optional and cannot precede purchase.

### Source, operational, and effective values

Preserve original imported asset fields and invoice cost/currency. Managers edit permitted operational fields. A financial override is a cost/currency pair with required reason, recorder name, timestamp, and persistent before/after history. Calculations use the override pair when active, otherwise the source pair. Reset restores the preserved pair and retains history. Manual records retain their initial entered cost/currency as the reset baseline; this technical representation is a proposal in the contracts, not a newly asserted owner policy.

### In-service and financial reporting dates

Installation is the in-service date; visibly use purchase date when absent. Use one explicit financial reporting date throughout financial and replacement results.

Use current operational purchase/installation dates when deriving the in-service anchor. "Original date" in the anniversary rule means that anchor before month clamping, not an immutable imported date that ignores manager edits.

Timezone: Asia/Hong_Kong. A fresh session defaults financial reporting to the actual current date; keep the selected date for that session until changed/reset. This control does not advance the clock, change source data, generate faults, modify observations/timestamps, or reconstruct historical portfolio snapshots. Operational sections show current recorded state; maintenance overdue uses the actual current Hong Kong date independently.

### Depreciation

Straight-line, zero residual, whole completed service months; none before service. Derive every month anniversary from the original in-service date and clamp to the destination month's last day when necessary. Cap completed months at useful life.

Accumulated depreciation = effective acquisition cost × completed months ÷ useful-life months.

Remaining book value = effective acquisition cost − accumulated depreciation.

Use unrounded values for calculations/aggregation; depreciation cannot exceed cost and remaining value cannot be negative.

Examples:

- USD 1,200, service 2026-01-15, useful life 12 months: on 2026-07-14, five months gives USD 500 depreciation and USD 700 remaining; on 2026-07-15, six months gives USD 600 each.
- Service 2026-01-31: first anniversary 2026-02-28, second 2026-03-31. On 2026-03-30 only one month is complete.
- Service 2024-01-31: first anniversary 2024-02-29, second 2024-03-31.
- Service 2024-02-29 with 12-month life: replacement 2025-02-28. Before service, depreciation is zero; at/beyond useful life, remaining value is zero.

Expected replacement = original in-service date + useful-life months using the same anniversary convention. This is a planning assumption, not a predicted failure.

### Currency

Supported currencies only: HKD, SGD, GBP, JPY, USD. Use one complete dated fixed fictional table; rates mean USD per one source unit, and USD = 1.

USD amount = effective transaction-currency amount × rate.

Validate completeness and rate integrity before financial reporting. A missing/invalid configured rate is a configuration failure requiring correction, not a normal partial-USD reporting workflow. Never replace missing rates with zero, omit affected amounts, or present an incomplete portfolio total. Source values remain preserved.

Display the FX date and "Fictional fixed rates — not live market rates". USD display rounds to two decimals after calculation/aggregation. Local means effective transaction currency: group totals by currency, never combine unlike currencies into one local amount. Display mode never changes stored currency or rates.

## 9. Condition and maintenance rules

### Latest room-system observations

Separate Lighting, Water supply, and Air conditioning. States:

- Healthy: recorded satisfactory assessment.
- Attention needed: recorded non-critical concern.
- Critical: recorded serious issue.
- Unknown: no assessment, or an explicitly recorded assessment that could not establish condition.

Unassessed Unknown can lack date/recorder. Every recorded assessment, including a recorded Unknown, requires observation date and recorder; note is optional. Missing imported observations default Unknown. Rooms-table observation fields and blocking validation are specified in the contracts.

Managers may edit the latest assessment across properties. Clear assessment removes its date/recorder/note and returns to unassessed Unknown. Mark Healthy records satisfactory condition and requires metadata. Keep no observation history. Maintenance never automatically changes condition; a Healthy room can still show unresolved faults.

### Maintenance

Ticket fields include ID, room, optional asset, description, Low/Medium/Critical severity, optional owner while Open, status, opened/updated timestamps, optional target date, and resolution note/timestamp when resolved. Use a short fictional owner list.

Allowed transitions: Open → In progress → Resolved. Entering In progress requires an owner; removing that owner is prohibited, but reassignment is allowed. Resolution requires a note and recorded actual timestamp. No skipping, reopening, deletion, or resolved edits.

Unresolved description/severity/target-date/owner/status changes retain persistent chronological before/after history. Ticket room/asset links remain fixed; linked assets must belong to the room.

Unresolved sorting: Critical before Medium before Low; within severity, overdue target dates before others; then oldest opened timestamp. A target date is overdue only when before the actual current operational date. Display owner or "Unassigned", target date or its absence, and separate resolved tickets.

Room-only critical faults are room issues. Only explicit asset linkage flags an asset as having a critical unresolved fault; never infer assets from room/facility type.

## 10. Dashboard and replacement planning

Condition and ticket-count cards lead, followed by the prioritised unresolved-ticket table with room links. Finance and secondary replacement sections follow; resolved records are separately accessible.

Counts have distinct units:

- Properties, rooms, and assets count unique entities in scope.
- Unresolved tickets are Open/In progress; critical unresolved tickets are that subset with Critical severity.
- Observation counts group each room's three systems by system/state, including unassessed Unknown.
- Ticket, affected-room, asset, and observation counts must not be presented as interchangeable.
- Sum asset values once per unique asset, independent of joined ticket rows.

All results share filters. Condition/maintenance reflect current records; only finance/replacement use the financial reporting date.

Replacement categories: overdue before that date, due today equal to it, due soon strictly after through +90 days inclusive, later beyond 90 days. Future spending window: strictly after reporting date through +12 calendar months inclusive. Separate overdue/due-today/future totals; overlapping categorisation must not duplicate assets within a total.

Use effective acquisition-cost proxies, with currency display/rates from section 8. Do not subtract book value or claim inflation, installation labour, quotations, or predicted failures. Show explicit critical asset-link flags separately from dates.

## 11. Key entities and contracts

Property; Room; individually tracked Asset; Invoice line; latest Facility observation; Maintenance ticket; Maintenance history; Financial override history; preserved Source baseline/provenance; Import result.

Their field contracts and comparison boundaries are defined in [data contracts](data-contracts.md). These are logical interfaces, not a chosen database schema or architecture.

## 12. Failure and edge cases

- Never guess source links or report success for a failed write.
- Blocked imports create no operational records; a failed commit leaves no new batch records.
- Operational edits survive identical source re-imports; source changes conflict.
- Duplicate invoice linkage must also be checked against existing assets.
- Missing observation information never implies Healthy.
- Healthy observations and unresolved faults may coexist.
- Test pre-service, life-cap, month-end, and leap-year calculations.
- Missing FX configuration prevents complete financial reporting; no fabricated totals.
- Keep ticket room/asset integrity, owner requirements, fixed associations, history, and resolved immutability.
- Cancelled edits, empty filters, and failed saves must not expose stale/successful-looking state.
- Financial reporting-date changes must not affect operational overdue indicators.
- Translation/currency preferences must not modify identifiers, source values, or user-entered text.

## 13. Quality and interface requirements

Persist local operational records and histories across normal restart. Supply actionable field/coordinate diagnostics and a startup process reproducible in a clean local environment. No live provider is required for core workflows. Confidential materials and real data must not enter published artifacts.

Interface sets: English (base), Traditional Chinese, Simplified Chinese, Japanese. Translate labels, navigation, validation, status labels, and explanations/assumptions. Do not automatically translate names, notes, descriptions, IDs, source headers, or stored enums. Missing translated text falls back to English. English is mandatory; the other sets are stretch. Translation verification is deferred; completeness checks do not establish linguistic accuracy.

English and USD are initial defaults when no preference exists. Later language/currency choices persist across browser restarts on that device and remain independent. Hosted storage, if later provided, must disclose durability/reset limits accurately.

## 14. Measurable completion criteria

SC-001: Every committed asset has a valid room/property and, if imported, a valid unique invoice-line link. Four-location evidence from v0.1 maps to AR-001 in the assessment document.

SC-002: Verify clean commit, blocked mixed-validity batch, duplicate/conflicting IDs, repeat imports after edits, and rollback. This supersedes v0.1 valid-subset import acceptance.

SC-003: Verify numerical examples, month-end/leap boundaries, effective-cost overrides, FX completeness, and replacement-window boundaries.

SC-004: Verify asset creation/edit/override/reset, observation assessment/clear, and maintenance progression/history; successful records survive restart.

SC-005: Verify consistent filters, counting units, drill-downs, empty states, and no financial duplication.

SC-006: Relocated to AR-006; this ID is retained as a traceability marker, not an additional product criterion.

SC-007: Record evidence for all required product acceptance scenarios before submission; disclose unmet criteria. Assessment evidence is tracked separately.

SC-008: Verify mandatory English UI, translation boundary/fallback for delivered stretch sets, grouped local/USD values, persistent preferences, and financial/operational date independence.

## 15. Decision and approval record

The following are owner-approved prototype policies, approved by Alex on 2026-10-02. They are not client requirements or claims of implemented/tested behaviour.

| Decision | Selected policy | Rationale | Affected requirements |
|---|---|---|---|
| D-001 | Room understanding and accountable maintenance first; finance/replacement secondary | Reflect primary management outcome | US-02–05, FR-007, FR-014 |
| D-002 | Four separate prescribed Excel files, atomic confirmed import, warnings visible | Trustworthy consolidation | US-01, FR-002–004, FR-015 |
| D-003 | Normalised preserved source comparison, identical skip, changed source conflict; no import updates | Preserve edits and evidence | US-01, FR-005 |
| D-004 | One asset per invoice line; imported links required; no allocation | Traceable individual purchases | FR-001, FR-019 |
| D-005 | Paired operational override/reset with reason/history; effective-cost calculations/proxies | Correct management values without rewriting evidence | US-03/05, FR-019 |
| D-006 | Cross-property asset/observation/ticket access; master data import-only; generated manual asset IDs; fixed associations | Define edit boundary without permissions | FR-001, FR-010, FR-016 |
| D-007 | Separate latest observations in Rooms; assessed metadata required; Clear → Unknown; recorded satisfactory → Healthy | Keep assessment meaning explicit | FR-009, FR-016 |
| D-008 | Three forward-only statuses; owner required in progress; resolved read-only; unresolved edits/history and agreed sorting | Accountable work | US-04, FR-012–013 |
| D-009 | Complete fixed fictional five-currency FX table, USD rate 1 | Reproducible reporting | FR-011, FR-018 |
| D-010 | Effective transaction-currency local mode, grouped totals; independent persistent defaults English/USD | Understandable display | FR-017–018 |
| D-011 | Asia/Hong_Kong actual operational date; separate session financial date | Avoid historical/simulation claims | FR-011, FR-014 |
| D-012 | Installation/purchase fallback; whole original-date anniversaries; zero residual; capped straight-line | Explainable valuation | FR-011, SC-003 |
| D-013 | 90-day category and 12-month future window; overdue/due-today totals separate | Explicit spending horizon | US-05, FR-014 |
| D-014 | Four interface sets; English mandatory, others stretch; English fallback | Bound translation scope | FR-017 |
| D-015 | Four properties, twelve rooms, minimum thirty-six assets; Tokyo in Japan | Manageable assessment fixture | Sample-data plan, AR-001 |

Approval date is 2026-10-02 for each row; evidence is Alex's decisions and confirmation in this planning conversation.

Superseded: valid-subset imports, Assigned as a status, operational partial-FX reporting, and source-only replacement proxies. These map respectively to D-002, D-008, D-009, and D-005. Observation independence and depreciation remain retained policies.

Unresolved/deferred: translation verification (owner: Alex; revisit before submission). Exact template schemas, normalisation details, manual cost baseline representation, and technical history fields are documented implementation proposals in the contracts; do not label them independently owner-approved. This revised text remains available for owner review.

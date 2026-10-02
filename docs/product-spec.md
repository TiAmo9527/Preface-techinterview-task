# Product specification: Hotel asset-management prototype

Status: Revised draft; owner-approved policies recorded below

Owner: Alex

Created: 2026-10-01

Revised: 2026-10-03

Target delivery: 2026-10-05

Version: 0.3

This document defines product behaviour. Approval of the policies in section 15 does not claim client approval, implemented features, or verified application behaviour. Technical contract proposals are identified in [data contracts](data-contracts.md). Architecture and implementation tasks belong in [the delivery plan](plan.md) and [task checklist](tasks.md).

The complementary [UI/UX specification](ui-ux-spec.md) records existing interface requirements, Alex's confirmed layout/styling choices, and proposed interaction details. It does not change the v0.3 product requirements or approval record below; implementation and UI verification remain pending.

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

Needs to initialise the portfolio from Assets, upload invoice updates independently, preview changes/diagnostics before saving, and inspect source evidence, conflicts and update history.

These are user perspectives, not permission roles. Authentication and property-level access enforcement are excluded. Property and room master data are import-only; cross-property access does not permit forms to create/edit that master data.

## 3. Product scope

Required capabilities:

- A working web application with the observable workflows below.
- Two prescribed workbook types: Assets baseline initialisation and independent Invoices updates to existing assets. Every room has exactly one lighting, one water-supply and one air-conditioning record.
- Whole-batch preview/validation, explicit confirmation, atomic commit, and exception reporting.
- Maintenance-first dashboard with location, property, and room filters and room drill-downs.
- Asset viewing, permitted editing, invoice-driven replacement fields/history and explicit financial overrides; identity, room and category stay fixed.
- Separate editable lighting, water-supply, and air-conditioning observations.
- Manual fault logging, owner assignment, progress, and persistent change history.
- Financial calculations, effective transaction-currency/USD display, and secondary replacement planning.
- English interface as mandatory scope. Traditional Chinese, Simplified Chinese, and Japanese are stretch translation sets with English fallback.
- Persistent display preferences, actionable validation, integrity, durable local saves, and reproducible startup.

Assessment coverage and presentation fixtures are defined in [assessment requirements](assessment-requirements.md) and [sample-data plan](sample-data-plan.md), not product-size limits.

Exclusions:

- Arbitrary PDF OCR, arbitrary spreadsheet compatibility, multi-sheet-workbook imports, live FX, sensors, and live-system integrations.
- Authentication/authorisation, real customer/hotel data, and AI features inside the application.
- Manual asset creation, baseline-based updates to existing records, property/room editing forms, asset relocation/category changes and editing accepted invoice-item evidence.
- Bundled purchases or quantity allocation, procurement/payments/orders, and production accounting compliance.
- Automated condition inference, observation history, ticket reopening/deletion/stage skipping, and resolved-ticket editing.

Fictional data only. Confidential assessment materials must not be published. Presentation and optional sharing obligations live in the assessment document.

## 4. Source data, identity, and evidence

The supported input boundary is two .xlsx workbook types, uploaded independently: Assets.xlsx / Assets establishes the baseline; Invoices.xlsx / Invoices updates recorded assets. Filenames are recommended, sheet names are required, and each file has one prescribed sheet. Headers-only sheets represent no new rows. [Data contracts](data-contracts.md) defines exact fields, types, identifier grammar, comparisons and precedence.

- Baseline rows contain complete initial asset values, including cost/currency, and repeated property/room/assessment details. No invoice link is required to initialise or report finance.
- Every room has exactly three records, one per supported category. Repeated property/room values must agree; duplicate asset IDs, missing/duplicate categories or occupied-category collisions block the upload. No empty-room or fourth-category import.
- Property IDs and room IDs encode region/property/room; asset IDs include their room prefix. Text IDs preserve leading zeros. Room numbers are unique within their property.
- An invoice item is identified by invoice_id plus line_id and matches one existing asset via (room_id, facility_type). Many invoice items can update one asset over time; one item cannot target multiple assets.
- Invoice updates replace name, purchase/installation dates, useful life, cost and currency. Blank optional installation clears it. Asset identity, room, category, assessments and tickets remain unchanged.
- The maximum invoice_date per asset controls current invoice-sourced values. Older new items are historical evidence; conflicting snapshots at the controlling maximum date block the upload. Equal-date equivalent evidence does not replay a current update.
- Preserve original baselines, accepted invoice items, source coordinates/timestamps and invoice-update/override history independently of editable operational state.
- Identical baseline/invoice re-imports skip without restoring previous values; changed content under an existing source identity conflicts. Newly identified invoice items can update current records according to date precedence.

Workbook content and provenance are source evidence. There is no invoice_file column, accompanying PDF requirement or OCR import path. Manual asset creation is excluded, leaving the assessment's add-asset obligation unmet; this owner-selected gap must be disclosed under AR-002.

## 5. User journeys and acceptance scenarios

Acceptance scenarios describe required verification, not completed tests.

### US-01: Initialise and update source records

Priority: Required

As a data-maintenance user, I want to establish a trusted baseline and then update existing room assets from invoices while retaining previous evidence.

Journey: select Assets or Invoices workflow → preview proposed inserts/updates/history-only records/skips/diagnostics → correct blockers → confirm → inspect actual results and provenance.

Acceptance scenarios:

- A valid Assets-only upload creates linked properties, rooms and their three assets together; initial finance works without invoices.
- An Invoices-only upload targets existing room/category records, including a subset of rooms. It creates no room/asset identities.
- Unknown targets, inconsistent repeated baseline values, missing/duplicate categories, duplicate source identities, invalid dates/observations/types or changed-source conflicts block every change in the upload.
- Preview writes nothing and shows before/after invoice field changes and override clearing. Diagnostics identify file, sheet, row, field and actionable reason.
- Missing/unsupported files or unusable columns block confirmation; only the selected workflow's one workbook is required. Warning-only valid uploads can be confirmed.
- Newest invoice_date wins across existing and incoming items regardless of row/upload order. Older valid items are stored without asset updates. Different snapshots at the controlling newest date block; equivalent tied evidence is retained without duplicating/replaying an update.
- Identical baseline/invoice repeats skip after invoice, asset, override or assessment edits. Changed source content under an existing identity conflicts rather than silently modifying evidence.
- A newly applied invoice replaces manual edits to its six fields and clears an active financial override with linked histories. Historical-only/equal-date evidence leaves edits and overrides intact.
- A commit failure rolls back baseline records, invoice evidence, asset changes and histories together; failed/blocked uploads never display successful writes. Confirmation rechecks integrity and precedence against a stale preview.

Independent verification compares state before preview, after blocked/failed uploads, after confirmed baseline, after invoice updates, after older/equal-date evidence and after repeats. Fixture verification alone is not product acceptance evidence.

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
- Invalid imported observation metadata blocks the whole batch; identical Assets baseline re-imports do not undo a manager's latest assessment.
- With no saved preference, the interface starts in English/USD. Changing language leaves the currency preference independent; both selected preferences survive browser restart.
- A delivered translation set localises interface text and falls back to English for missing keys without translating stored names, notes, descriptions, IDs, or enums.
- Local mode groups a mixed-currency portfolio into labelled currency totals; USD mode uses the complete configured rate table. Neither mode alters source or override values.

Observation editing is additionally covered by FR-016 and section 9; language/currency behaviour by FR-017–018 and section 13.

### US-03: View and edit asset records

Priority: Required

As a room manager, I want to view/edit the three room asset records while retaining their baseline and invoice evidence.

Acceptance scenarios:

- View each room's lighting, water-supply and air-conditioning records; there is no manual asset-creation action.
- Asset ID, room and category remain fixed. Name, purchase/installation dates and useful life are editable; cost/currency corrections use paired overrides.
- Invalid fields block saving with feedback. Cancelled/failed writes leave state unchanged; successful saves survive restart and refresh financial/room/dashboard results.
- Inspect original baseline, all invoice items and applied update history, including previous operational fields and override state.
- A paired cost/currency override requires reason/recorder and records before/after values and actual timestamp; it changes calculations without changing source evidence.
- Reset requires a reason and restores latest applied invoice cost/currency, or baseline values before invoices, while retaining history. Reset does not restore source names/dates or room observations.
- A newly applied invoice replaces its six current fields, clears active overrides and recalculates finance/replacement values. Older or identical invoice uploads do not undo manager edits.

Manual creation is deliberately excluded. This does not satisfy the external add-asset obligation; preserve that gap in assessment evidence rather than claiming full AR-002 compliance.

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

FR-001: Preserve property-room-asset relationships, exactly one asset per required room/category, and a single existing target per invoice item.

FR-002: Preview and validate one Assets baseline or one Invoices update workbook independently before explicit confirmation.

FR-003: Distinguish blocking file/row/conflict errors from non-blocking warnings; any blocker prevents the entire batch commit.

FR-004: Keep invalid/conflicting source rows inspectable in diagnostics without creating operational records.

FR-005: Preserve source identities, skip identical repeats, block changed source IDs/upload duplicates, and apply new invoice snapshots by maximum invoice_date with controlling-date conflict checks.

FR-006: Filter portfolio outputs by location, property, and room.

FR-007: Show property/room/asset counts; unresolved/critical unresolved ticket counts; observation counts by system/state; prioritised unresolved tickets; acquisition/book values; and secondary replacement counts/proxies. Label units explicitly.

FR-008: Use one consistent filter scope for all outputs, clear incompatible filters, and avoid stale empty results.

FR-009: Show each room's three separate observations, including unassessed Unknown.

FR-010: View/edit existing asset records without manual creation; identity, room and category remain fixed and derived values read-only.

FR-011: Display the financial reporting date, calculation assumptions, FX date/disclaimer, and separate current operational date.

FR-012: Create faults, assign owners, and use Open → In progress → Resolved with required transition fields and fixed associations.

FR-013: Persist chronological history of saved unresolved-ticket field changes; resolved tickets are immutable.

FR-014: Provide secondary replacement dates, urgency flags, and separately labelled overdue/due-today/future effective-cost proxies.

FR-015: Persist successful saves and atomic valid imports; cancelled, blocked, invalid, or failed operations must not alter operational records.

FR-016: Edit or clear latest observations, validate assessment metadata, and never infer condition from tickets.

FR-017: Provide English and switchable stretch translation sets for interface text, retaining canonical data values and English fallback.

FR-018: Provide an independent USD/effective-transaction-currency display preference, grouped mixed-currency totals, and persistent language/currency selections.

FR-019: Preserve baselines/invoice evidence and invoice-update history; record paired overrides/resets, clear active overrides on applied invoices, and reset cost/currency to latest invoice or baseline fallback.

FR-001–015 retain their v0.1 identities; FR-016–019 were added in v0.2. v0.3 revises source/update/asset policies without renumbering requirements.

## 7. Import policies

Preview and validation never write operational records. Assets initialisation and Invoices updates are independent single-workbook workflows. Baseline imports create complete new rooms; invoice imports resolve existing targets only. Validate all rows and dependencies before confirmation, including historical invoice items.

Blocking errors include unreadable/unsupported files, invalid headers/IDs/types/dates, inconsistent repeated property/room values, missing/duplicate room categories, unknown invoice targets, duplicate source identities, changed source content and conflicting snapshots at a target's maximum invoice date. Any blocker prevents all operational and evidence/history writes; do not offer import-valid-rows. Warnings include missing installation date, zero cost and missing optional supplier. Fully populated valid examples omit these warning cases.

For each target, use maximum invoice_date across accepted existing and incoming items. If there is no applied invoice, apply the first accepted controlling snapshot regardless of baseline purchase date. Subsequently apply only strictly newer dates. Older new items and equal-date/equal-snapshot evidence are historical-only. Same maximum date with different six-field snapshots blocks the upload; conflicts at older dates do not choose current state. Compare source snapshots rather than manager-edited operational values.

Existing identical invoice identities skip; changed values under the same identity conflict. A newly applied invoice replaces all six current fields, clears active overrides and records histories; blanks in optional installation clear previous values. Asset identity/category/room, assessments and maintenance stay unchanged. Equivalent newest evidence references are retained without duplicating asset values.

Preview distinguishes proposed baseline entity inserts, new invoice items, distinct asset updates, historical-only items, skips, blockers and warnings. Show invoice before/after values and override effects. Only a blocker-free upload can be confirmed. Revalidate stale previews; commit evidence, records, updates and histories together or roll everything back. Report actual results only after success. Detailed precedence/comparison/provenance rules are in [data contracts](data-contracts.md).

## 8. Asset and financial rules

Assets supplies each record's initial ID, room, category, name, purchase/installation dates, positive whole-month useful life and cost/currency. Supported types are Lighting, Water supply and Air conditioning only; exactly one of each per room. There is no manual creation or category/room/ID editing. Invoice updates supply a full replacement snapshot of name, purchase/installation dates, life, cost and currency for an existing target.

Cost is non-negative; zero warns. Installation is optional, cannot precede purchase and falls back to purchase when absent. Invoice_date is required for precedence and is independent of the service-date financial calculation; no extra invoice/purchase ordering constraint is imposed by the product.

### Source, operational, and effective values

Preserve the original baseline and every accepted invoice snapshot. Source cost/currency means latest applied invoice values, or baseline values when there is no applied invoice. Current dates/name/life can differ after manager edits until a newer invoice replaces them.

A financial override is a cost/currency pair with required reason, recorder, actual timestamp and persistent before/after history. Calculations use active override values, otherwise the source pair. Reset restores that latest source pair, retaining history; it does not reset names/dates. Applied invoices clear active overrides with linked system-attributed history and before/after state. Historical-only and skipped invoice items do not clear them. Manual reset-baseline/origin handling is removed.

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

Unassessed Unknown can lack date/recorder. Every recorded assessment, including a recorded Unknown, requires observation date and recorder; note is optional. Missing imported observations default Unknown. Assets baseline observation fields and blocking validation are specified in the contracts.

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

Property; Room; stable room/category Asset record; Invoice item; Invoice update history; latest Facility observation; Maintenance ticket; Maintenance history; Financial override history; preserved Source baseline/provenance; Import result.

Their field contracts and comparison boundaries are defined in [data contracts](data-contracts.md). These are logical interfaces, not a chosen database schema or architecture.

## 12. Failure and edge cases

- Never guess source links or report success for a failed write.
- Blocked uploads write no operational/evidence/history records; failed commits roll back inserts and existing-asset updates.
- Edits survive identical baseline/invoice repeats and historical-only invoices; newly applied invoices intentionally replace their six fields and clear overrides. Changed evidence under an existing identity conflicts.
- Validate existing room/category targets and exact three-category completeness; one invoice item has one target, while multiple items may reference that target over time.
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

SC-001: Every committed room has exactly one asset record in each required category, each linked to its property/room. Every invoice item resolves to one existing target; initial assets need no invoice. Four-location evidence from v0.1 maps to AR-001.

SC-002: Verify independent baseline/invoice commits, subset updates, mixed-validity rejection, duplicates/changed-source conflicts, date precedence/equal-date conflicts, historical-only evidence, repeats after edits, stale previews and rollback. Atomic uploads retain the superseding v0.2 policy over v0.1 valid-subset imports.

SC-003: Verify numerical examples, month-end/leap boundaries, effective-cost overrides, FX completeness, and replacement-window boundaries.

SC-004: Verify asset viewing/editing, invoice replacement/override clearing/history, latest-invoice/baseline reset fallback, observation assessment/clear and maintenance progression/history; successful records survive restart. Manual creation is excluded and the AR-002 gap disclosed.

SC-005: Verify consistent filters, counting units, drill-downs, empty states, and no financial duplication.

SC-006: Relocated to AR-006; this ID is retained as a traceability marker, not an additional product criterion.

SC-007: Record evidence for all required product acceptance scenarios before submission; disclose unmet criteria. Assessment evidence is tracked separately.

SC-008: Verify mandatory English UI, translation boundary/fallback for delivered stretch sets, grouped local/USD values, persistent preferences, and financial/operational date independence.

## 15. Decision and approval record

The following are owner-approved prototype policies, approved by Alex on 2026-10-02. They are not client requirements or claims of implemented/tested behaviour.

| Decision | Selected policy | Rationale | Affected requirements |
|---|---|---|---|
| D-001 | Room understanding and accountable maintenance first; finance/replacement secondary | Reflect primary management outcome | US-02–05, FR-007, FR-014 |
| D-002 | Two workbook types with independent atomic confirmed uploads: Assets baseline then Invoices updates; warnings visible | Trustworthy initialisation and updates | US-01, FR-002–004, FR-015 |
| D-003 | Preserve normalised baseline/invoice identities; identical skip and changed-identity conflict; new invoices update current records by newest invoice_date | Preserve evidence while allowing accountable updates | US-01, FR-005 |
| D-004 | Each invoice item targets one existing room/category asset; many items over time; baseline has independent cost/currency; no allocation | Traceable update evidence | FR-001, FR-019 |
| D-005 | Paired override/reset/history; applied invoices clear overrides; reset to latest invoice or baseline fallback; effective-cost calculations | Correct values while preserving each source | US-03/05, FR-019 |
| D-006 | Cross-property record viewing/editing; master data import-only; no manual asset creation; identity/room/category fixed | Define edit boundary and disclose AR-002 add-asset gap | FR-001, FR-010, FR-016 |
| D-007 | Latest observations repeated consistently in Assets baseline; invoices do not change them; assessed metadata required; Clear → Unknown | Keep assessments independent from purchase updates | FR-009, FR-016 |
| D-008 | Three forward-only statuses; owner required in progress; resolved read-only; unresolved edits/history and agreed sorting | Accountable work | US-04, FR-012–013 |
| D-009 | Complete fixed fictional five-currency FX table, USD rate 1 | Reproducible reporting | FR-011, FR-018 |
| D-010 | Effective transaction-currency local mode, grouped totals; independent persistent defaults English/USD | Understandable display | FR-017–018 |
| D-011 | Asia/Hong_Kong actual operational date; separate session financial date | Avoid historical/simulation claims | FR-011, FR-014 |
| D-012 | Installation/purchase fallback; whole original-date anniversaries; zero residual; capped straight-line | Explainable valuation | FR-011, SC-003 |
| D-013 | 90-day category and 12-month future window; overdue/due-today totals separate | Explicit spending horizon | US-05, FR-014 |
| D-014 | Four interface sets; English mandatory, others stretch; English fallback | Bound translation scope | FR-017 |
| D-015 | Four properties, twelve rooms, exactly thirty-six assets; three universal categories; one AI invocation generates fully populated valid and deliberately invalid pairs | Manageable reproducible update fixtures | Sample-data plan, AR-001 |
| D-016 | Invoice full snapshots; newest-date control; historical-only older items; controlling-date conflicts blocked; applied updates replace edits and retain histories | Explainable current values and repeat safety | US-01/03, FR-005/019, SC-002/004 |

Approval date is 2026-10-02. D-002–007 and D-015 are revised, and D-016 added, by Alex's explicit approval of the v0.3 implementation plan. Other policy rows retain earlier approval. This is owner approval, not client acceptance or application evidence.

Superseded in v0.3: four-file paired imports, prohibition of all import-driven current-value updates, mandatory invoice links on initial assets, fixed single invoice linkage over an asset's lifetime, generated manual asset creation, separate Rooms source workbook, OTHER category/minimum-only three-asset coverage, and opt-in invalid generation. Earlier superseded policies remain: valid-subset imports, Assigned status, partial-FX reporting and source-only replacement proxies. Observation independence, atomic writes and depreciation remain retained.

Unresolved/deferred: translation verification (owner: Alex; revisit before submission). Exact header spellings, parsing/identifier grammar and technical history representations remain implementation proposals in the contracts. The owner-approved removal of manual asset creation leaves AR-002's add-asset obligation unmet and must be disclosed; do not rewrite that external obligation to imply compliance.

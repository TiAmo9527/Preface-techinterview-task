# Product specification: Hotel asset-management prototype

Status: Documented requirements with owner-approved policies. Application verification: NOT RUN.

Owner: Alex

Created: 2026-10-01

Revised: 2026-10-03

Target delivery: 2026-10-05

Version: 0.4

This document defines product behavior. Owner approval does not establish client acceptance or implemented behavior.

[Data contracts](data-contracts.md) contain proposed technical interfaces. Database columns, storage types, and architecture remain technical-planning work.

[UI/UX requirements](ui-ux-spec.md) distinguish Inherited, Confirmed, and Proposed details. [Assessment requirements](assessment-requirements.md) preserve external obligations.

Alex must resolve contradictions between product decisions and external obligations. Neither document silently changes the other.

Use the [shared glossary](glossary.md) for domain terms. [Acceptance scenarios](acceptance-scenarios.md) define independent Given/When/Then checks.

## 1. Problem and intended outcome

The fictional hotel portfolio stores room and asset information in spreadsheets and invoice records.
The room manager needs connected room information and accountable maintenance actions.

**Primary user:** Room manager.

**Primary decision:** Determine the required maintenance action and assign its ticket owner.

The primary outcome is room understanding with accountable maintenance action. Finance and replacement planning support this outcome.

The demonstration sequence is:

1. Preview and confirm source imports.
2. Review observations and unresolved tickets.
3. Select a room.
4. Assess condition or edit an asset record.
5. Log a fault or update maintenance.
6. Review supporting financial and replacement results.

The [demo](demo.md) defines the proposed 12-minute sequence. This is a decision-support prototype, not a production accounting product.

## 2. Users

### Room manager

The room manager is the primary user. This user reviews rooms, edits permitted asset information, assesses condition, and manages maintenance.
This user can work across all imported fictional properties.

### Executive

The executive is a supporting user. This user reviews portfolio priorities, room context, book values, and replacement spending proxies.

### Data-maintenance user

The data-maintenance user is a supporting user. This user establishes the baseline and uploads independent invoice updates.
This user inspects diagnostics, source evidence, conflicts, and update history.

These perspectives are not permission roles. Authentication and property-level access enforcement remain excluded.
Property and room master data are import-only. Cross-property access does not permit master-data editing forms.

## 3. Product scope

Required capabilities:

- A working web application for the required journeys.
- Independent Assets baseline and Invoices update uploads.
- Exactly one asset record per room in each of the three categories.
- Preview, validation, explicit confirmation, atomic commit, and diagnostics.
- An operational overview with shared location, property, and room filters.
- Room selection with asset records, observations, and maintenance tickets.
- Permitted asset editing with paired financial overrides and persistent histories.
- Invoice updates with preserved source evidence and update history.
- Separate editable Lighting, Water supply, and Air conditioning observations.
- Manual fault logging, ticket ownership, progress, and history.
- Financial calculations, USD/local display, and supporting replacement planning.
- Mandatory English interface text.
- Independent persistent language/currency preferences and durable local saves.
- A reproducible startup process and isolated rehearsal data stores.

Stretch capabilities:

- Traditional Chinese interface text.
- Simplified Chinese interface text.
- Japanese interface text.

Delivered stretch sets require English fallback. Translation review remains pending.

Excluded capabilities:

- Arbitrary PDF OCR, arbitrary spreadsheets, and multi-sheet imports.
- Live FX, sensors, and live-system integrations.
- Authentication, property-level authorization, real customer data, and application AI features.
- Manual asset creation and baseline updates to existing records.
- Property/room editing forms and asset relocation, category changes, or identity changes.
- Editing accepted invoice evidence.
- Bundled purchases, quantity allocation, procurement, payments, or orders.
- Production accounting compliance.
- Automatic condition inference and observation history.
- Ticket reopening, deletion, stage skipping, or resolved-ticket editing.

Use fictional data only. Do not publish confidential assessment materials.
The four-property sample is demonstration coverage, not a product capacity limit.
Manual asset creation remains an unmet part of AR-002.

## 4. Source data, identity, and evidence

Assets.xlsx has the Assets sheet. Invoices.xlsx has the Invoices sheet.
Filenames are recommendations. Each supported workbook contains its required single sheet.
Headers-only sheets contain no new rows.

Assets supplies complete initial asset values with repeated property, room, and observation information.
Baseline finance requires no invoice link. Each room requires exactly three asset records with distinct required categories.

Property and room identities contain their region and parent information. Asset identities contain their room prefix.
Text identities preserve leading zeros. Room numbers are unique within a property.

An invoice item uses invoice_id plus line_id as its identity. Its room/category pair selects one existing asset record.
Many invoice items can target that record over time. One item cannot target multiple asset records.

Each invoice snapshot replaces six fields:

1. Asset name.
2. Purchase date.
3. Installation date.
4. Useful life.
5. Acquisition cost.
6. Currency.

Blank installation clears the previous date. Identity, room, category, observations, and tickets remain unchanged.

The maximum invoice_date controls source updates. Older new items remain historical-only evidence.
Different snapshots at the controlling maximum date block the upload. Equivalent tied evidence does not replay an update.

Preserve original baselines, accepted invoice items, provenance, invoice-update history, and override history.
Identical source repeats skip without restoring previous operational values. Changed evidence under an existing source identity conflicts.

Workbook information and provenance are source evidence. There is no invoice_file field, PDF attachment requirement, or OCR path.

## 5. User journeys and acceptance scenarios

All required scenarios are in [acceptance scenarios](acceptance-scenarios.md). Every scenario states its own prerequisite information.
Prepare that information independently. Do not require an earlier scenario to establish it.
Fixture checks do not establish product acceptance.

### US-01: Initialise and update source records

Actor: Data-maintenance user.

Priority: Required.

Starting state: Empty portfolio for baseline import. Invoice updates require independently prepared existing room/category targets.

Entry point: Import, with Assets or Invoices selected.

Actions:

1. Select the workbook.
2. Inspect preview counts, field changes, override effects, and diagnostics.
3. Correct blockers.
4. Confirm the reviewed upload.
5. Inspect actual results and provenance.

Successful outcome: Atomic saved changes with accurate counts and inspectable source evidence.

Independent setup: Prepare an empty store or the stated baseline, invoices, manager edits, and overrides for that scenario.

Coverage: [US-01 scenarios](acceptance-scenarios.md#us-01). Blocked, cancelled, or failed imports preserve the previous saved state.

### US-02: Inspect portfolio and room context

Actor: Room manager. The executive can use the same review journey.

Priority: Required.

Starting state: An independently prepared portfolio with the observations, tickets, currencies, and preferences required by the scenario.

Entry point: Overview.

Actions:

1. Select location, property, or room filters.
2. Review labelled counts and unresolved tickets.
3. Select a room from Map, List, or a ticket link.
4. Inspect its observations, asset records, and tickets.
5. Save or clear an observation when required.

Successful outcome: Consistent filtered results, accurate room context, and persistent valid observation changes.

Independent setup: Prepare the required portfolio directly. Use an empty portfolio for first-use and empty-state checks.

Coverage: [US-02 scenarios](acceptance-scenarios.md#us-02). Invalid, cancelled, or failed observation saves preserve the previous assessment.

### US-03: View and edit asset records

Actor: Room manager.

Priority: Required.

Starting state: An existing asset record with defined baseline, invoice evidence, current operational values, and override state.

Entry point: The room card's asset editor or evidence section.

Actions:

1. Inspect the asset record and its source evidence.
2. Edit permitted operational fields or the paired financial override.
3. Correct validation errors.
4. Save the change or reset financial values to source values.
5. Inspect refreshed results and retained history.

Successful outcome: Valid persistent changes without identity changes or source-evidence changes.

Independent setup: Prepare the specific asset, applied invoice state, manual edits, and override required by the scenario.

Coverage: [US-03 scenarios](acceptance-scenarios.md#us-03). Manual asset creation remains excluded and does not satisfy AR-002.

### US-04: Manage maintenance

Actor: Room manager.

Priority: Required.

Starting state: An existing room and optional same-room asset. Transition checks use an independently prepared ticket in the stated status.

Entry point: Maintenance or the room card's Log fault action.

Actions:

1. Save a valid fault as Open.
2. Assign a ticket owner.
3. Start work as In progress.
4. Resolve the ticket with a resolution note.
5. Inspect its history and resolved read-only state.

Successful outcome: Accountable maintenance progress with valid associations, required ownership, actual timestamps, and persistent history.

Independent setup: Prepare the room and ticket status directly for each transition, rejection, or history check.

Coverage: [US-04 scenarios](acceptance-scenarios.md#us-04). Ticket changes do not update observations or replacement dates.

### US-05: Review replacement needs

Actor: Executive. This journey supports the room manager's primary decision.

Priority: Required. Presentation priority: Secondary.

Starting state: Independently prepared asset records, valid fixed FX configuration, and an explicit financial reporting date.

Entry point: Overview's financial and replacement sections.

Actions:

1. Select the reporting scope.
2. Select the financial reporting date.
3. Inspect book values and replacement categories.
4. Compare separate spending proxies.
5. Inspect assumptions and explicit critical asset links.

Successful outcome: Correct, explainable categories and spending proxies for the selected scope and date.

Independent setup: Prepare boundary dates and effective values directly. Prepare invalid FX configuration separately for failure checks.

Coverage: [US-05 scenarios](acceptance-scenarios.md#us-05). Reporting changes do not change operational records or source evidence.

## 6. Functional requirements

FR-001: Preserve property, room, asset, and invoice relationships. Each room has one asset record per required category.

FR-002: Preview one Assets or Invoices workbook before explicit confirmation.

FR-003: Distinguish blockers from warnings. Any blocker prevents the whole upload commit.

FR-004: Keep rejected source rows inspectable in diagnostics without operational records.

FR-005: Preserve source identities. Skip identical repeats. Block changed identities, upload duplicates, and conflicting controlling-date snapshots.
Apply eligible invoice snapshots by maximum invoice_date.

FR-006: Filter portfolio outputs by location, property, and room.

FR-007: Label entity counts, ticket counts, and observation counts separately. Present unresolved tickets before supporting financial and replacement results.

FR-008: Use one filter scope for all outputs. Clear incompatible child filters. Avoid stale empty results.

FR-009: Display three separate room-system observations, including unassessed Unknown.

FR-010: Permit existing asset editing only. Keep identity, room, category, and calculated outputs read-only.

FR-011: Display the financial reporting date, operational date, calculation assumptions, and FX date/disclaimer.

FR-012: Create faults and assign ticket owners. Enforce Open → In progress → Resolved with fixed associations and required fields.

FR-013: Preserve chronological unresolved-ticket history. Keep resolved tickets read-only.

FR-014: Display replacement dates, urgency categories, and separate overdue, due-today, and future spending proxies.

FR-015: Persist successful saves and atomic imports. Cancelled, blocked, invalid, or failed operations preserve saved records.

FR-016: Edit or clear latest observations with required metadata. Do not infer condition from maintenance.

FR-017: Provide English interface text. Delivered stretch translations require English fallback and unchanged stored information.

FR-018: Provide USD/local display with grouped local totals and independent persistent preferences.

FR-019: Preserve source evidence and invoice-update history. Record paired overrides and resets.
Clear active overrides on applied invoices. Reset to the latest applied invoice pair or baseline fallback.

FR-001–FR-015 retain their v0.1 identities. FR-016–FR-019 first appeared in v0.2.
Later revisions preserve these identifiers.

## 7. Import rules

Preview and validation save no records, evidence, or histories. Assets and Invoices are independent single-workbook workflows.
Baseline import creates complete new rooms. Invoice import resolves existing targets only.
Validate every row, including historical invoice evidence.

Blockers include:

- Missing, unreadable, or unsupported files and invalid headers.
- Invalid identities, types, dates, observations, or repeated property/room information.
- Missing or duplicate categories and occupied room/category combinations.
- Unknown invoice targets and duplicate source identities.
- Changed evidence under an existing identity.
- Different snapshots at the controlling maximum invoice date.

Any blocker rejects the whole upload. Rejected rows remain visible in diagnostics.
Valid surrounding rows do not commit separately. Partial import is excluded.

Missing installation dates, zero cost, and absent optional suppliers produce warnings. Warning-only valid uploads can proceed after confirmation.
The fully populated valid demonstration examples contain no such warnings.

Use the maximum invoice_date across stored and incoming evidence for each asset record.
The first controlling invoice applies regardless of baseline purchase date. Later applied invoices require a strictly newer date.
Older and equivalent equal-date items remain historical-only. Older-date snapshot differences do not select current values.
Compare source snapshots, not manager-edited operational values.

Applied invoices replace all six fields and clear active overrides with linked history.
Historical-only items and skips preserve manual edits and overrides.

Preview distinguishes entity inserts, new invoice items, distinct asset updates, historical-only items, skips, warnings, and blockers.
Display before/after fields and override effects. Diagnostics identify file, sheet, row, field, and actionable reason when available.

Recheck integrity and precedence at confirmation. Changed preview effects require refreshed review and renewed confirmation.
Commit records, evidence, updates, and histories together. Failure preserves the previous saved state.
Display actual committed counts only after success.

## 8. Asset and financial rules

Assets supplies initial identities, names, categories, dates, useful life, cost, and currency.
Useful life is a positive whole number of months. Cost is non-negative. Zero cost produces a warning.
Installation is optional and cannot precede purchase. Missing installation uses purchase as the service anchor.

Invoice_date controls precedence independently of service dates. The product imposes no invoice/purchase date-order constraint.

### Source, operational, and effective values

Preserve baseline and invoice snapshots. Source values use the latest applied invoice pair, or the baseline pair before invoices.
Manager edits can change current operational names, dates, and useful life until a newer invoice replaces them.

An override requires a cost/currency pair, reason, recorder, actual timestamp, and before/after history.
Calculations use effective financial values. Reset restores source values and retains history.
Reset does not restore names, dates, or observations. Applied invoices clear overrides with system attribution and linked history.
Historical-only items and skips do not clear overrides.

### In-service and financial reporting dates

The current installation date is the service anchor. Display purchase-date fallback when installation is absent.
The original date in anniversary calculations means the current service anchor before clamping.
It does not mean an immutable imported date.

Use one financial reporting date for financial and replacement results. A new session starts with actual Hong Kong today.
Retain the selected date for that session until the user changes or resets it.
The control does not advance the operational clock or reconstruct historical portfolio state.
It does not change source evidence, observations, faults, or timestamps.
Operational overdue checks use the actual current Asia/Hong_Kong date.

### Depreciation

Use straight-line depreciation, zero residual, and whole completed service months. Before service, completed months equal zero.
Derive each anniversary from the original service day. Clamp to the destination month's last day when necessary.
Cap completed months at useful life.

Accumulated depreciation = effective acquisition cost × capped completed months ÷ useful-life months.

Remaining book value = effective acquisition cost − accumulated depreciation.

Calculate and aggregate unrounded values. Depreciation cannot exceed cost. Book value cannot be negative.

| Service anchor | Life | Reporting date | Required result |
|---|---|---|---|
| 2026-01-15, USD 1,200 | 12 months | 2026-07-14 | Five months. Depreciation USD 500. Book value USD 700. |
| 2026-01-15, USD 1,200 | 12 months | 2026-07-15 | Six months. Depreciation USD 600. Book value USD 600. |
| 2026-01-31 | Positive life | 2026-03-30 | First anniversary 2026-02-28. Second anniversary 2026-03-31. One completed month. |
| 2024-01-31 | Positive life | 2024-03-31 | Anniversaries 2024-02-29 and 2024-03-31. Two completed months. |
| 2024-02-29 | 12 months | 2025-02-28 | Replacement due. Book value zero. |

Expected replacement = service anchor + useful-life months, using the same anniversary convention.
This date is a planning assumption, not a predicted failure.

### Currency

Supported currencies are HKD, SGD, GBP, JPY, and USD. Use one complete, dated, fixed fictional FX table.
Each rate means USD per one source-currency unit. USD equals 1.

USD amount = effective transaction-currency amount × configured rate.

Validate rate completeness and integrity before financial reporting. Missing or invalid configuration requires correction.
Do not substitute zero, omit affected amounts, or display incomplete portfolio totals.
Preserve source values when configuration fails. No live rates apply.

Display the configured FX date and “Fictional fixed rates — not live market rates”.
The FX date identifies the fixed table. Changing the financial reporting date does not select another rate date.
Round USD to two decimals after calculation and aggregation.
Local mode groups totals by effective transaction currency. Never combine unlike local currencies into one amount.

Display settings do not change stored currencies or rates.

## 9. Condition and maintenance rules

### Latest room-system observations

Lighting, Water supply, and Air conditioning have separate observations.

| State | Meaning |
|---|---|
| Healthy | Recorded satisfactory assessment. |
| Attention needed | Recorded non-critical concern. |
| Critical | Recorded serious issue. |
| Unknown | No assessment, or an assessment that could not establish condition. |

Unassessed Unknown requires no date or recorder. Every recorded assessment requires a date and recorder, including recorded Unknown.
The note is optional. Missing imported observations initialize as Unknown.
Managers may assess rooms across properties. Clear removes the date, recorder, and note.

Clear returns the observation to unassessed Unknown. No observation history exists.
Maintenance never changes condition automatically. Healthy observations can coexist with unresolved tickets.

### Maintenance

A ticket requires identity, room, description, severity, status, and actual opened/updated timestamps.
The asset link and target date are optional. The asset must belong to the room.
Owner is optional while Open. Use a short fictional owner list.

Allowed transitions are Open → In progress → Resolved.
In progress requires a ticket owner. Owner removal is blocked in that status, but reassignment is allowed.
Resolution requires a non-empty note and actual timestamp. Resolved tickets are read-only.
Stage skipping, reopening, and deletion are excluded.

Room and asset links remain fixed after creation. Saved unresolved changes retain chronological before/after history.
These changes include description, severity, target date, owner, and status.

Sort unresolved tickets by:

1. Severity: Critical, Medium, then Low.
2. Overdue target dates before other target dates within that severity.
3. Oldest opening timestamp within that group.

Overdue means a target date before the actual operational date. Show Unassigned when no owner exists.
Show target-date absence explicitly. Present resolved tickets separately.

Only an explicit asset link creates a critical unresolved asset flag. Room-only critical faults do not flag all room assets.

## 10. Dashboard and replacement planning

Overview orders shared filters, labelled operational counts, central room view, unresolved maintenance, then finance and replacement results.
Resolved tickets remain separately accessible.

Count unique properties, rooms, and asset records. Count unresolved tickets in Open or In progress.
Count critical unresolved tickets as the Critical subset. Group observations by system and state, including unassessed Unknown.
Do not interchange ticket, room, asset, or observation counts. Sum each asset's value once, independent of ticket or invoice joins.

All outputs use the same reporting filters. Condition and maintenance show current records.
Only finance and replacement use the financial reporting date.

| Replacement category | Rule |
|---|---|
| Overdue | Replacement date before the financial reporting date. |
| Due today | Replacement date equal to the financial reporting date. |
| Due soon | Replacement date after reporting date through reporting date + 90 days, inclusive. |
| Later | Replacement date beyond reporting date + 90 days. |

The future spending window excludes overdue and due-today records. It includes dates through reporting date + 12 calendar months.
Use the month-clamping convention for the calendar-month endpoint.
Separate overdue, due-today, and future totals. Do not duplicate an asset within a total.

Use effective acquisition-cost spending proxies with configured FX/display rules. Do not subtract book value.
These proxies exclude quotations, inflation, installation labor, and failure predictions.
Display critical asset-link flags separately from date categories. They do not infer condition or automatically change replacement dates.

## 11. Data meaning and relationships

The [glossary](glossary.md) supplies the shared definitions. The following table states required relationships and information.

| Entity | Identity and relationship | Required information | Optional information |
|---|---|---|---|
| Property | Stable property identity. Contains rooms in one location. | Identity, name, location, city. | None in the baseline interface. |
| Room | Stable room identity. Belongs to one property. | Identity, parent property, unique property-local room label, three category records. | Assessment metadata when unassessed. |
| Asset record | Stable asset identity. Belongs to one room/category combination. | Identity, room, category, name, purchase date, useful life, acquisition cost, currency. | Installation date and active financial override. |
| Invoice item | Invoice identity plus line identity. Resolves to one existing room/category asset. | Both identities, target, full snapshot, invoice date, provenance. | Installation date and supplier. |
| Observation | One latest assessment per room/system. Independent of tickets and purchases. | State. Recorded states also require date and recorder. | Note. Unassessed Unknown has no metadata. |
| Maintenance ticket | Generated ticket identity. Belongs to one room. | Description, severity, status, actual timestamps. In progress also requires owner. Resolved also requires note/timestamp. | Same-room asset, target date, owner while Open. |

Asset identity represents the room/category record, not a newly identified physical unit after every purchase.
Ticket links therefore continue through replacements. An invoice does not prove fault resolution or satisfactory condition.
The manager resolves tickets and records observations separately.

Imported provenance includes upload reference, filename, sheet, row, and actual timestamp.
Property and room baselines retain all contributing coordinates. Source comparisons ignore filenames, formatting, row order, and operational edits.

Histories preserve invoice updates, financial overrides, and maintenance changes. Observations keep only the latest state.
Import results distinguish proposed counts from actual committed counts.
Financial results are calculated, not imported financial-result fields.

Missing costs block import. Explicit zero costs warn. Missing observations remain Unknown, not Healthy.
Missing installation uses the stated fallback. Missing FX configuration blocks complete financial reporting, not a zero-value substitute.

Logical interfaces remain in [data contracts](data-contracts.md). Exact database columns and storage types remain deferred.

## 12. Failure and edge cases

Required [acceptance scenarios](acceptance-scenarios.md) cover these cases:

- Invalid source links, identity conflicts, category completeness, and repeated baseline disagreements.
- Atomic rejection, commit failure, cancellation, stale previews, and accurate success feedback.
- Identical repeats after edits and historical-only invoice preservation.
- New invoice replacement of operational edits and active overrides.
- Unknown observations, required assessment metadata, and independent faults.
- Before-service, month-end, leap-year, useful-life cap, and replacement boundaries.
- Missing FX configuration without fabricated totals.
- Owner requirements, fixed ticket associations, history, and resolved immutability.
- Empty filters without stale results and unique-asset financial totals.
- Language/currency independence and unchanged source/user text.
- Normal restart persistence and isolated rehearsals.

## 13. Quality and experience requirements

### Device and browser

Required context: Windows laptop with Chrome. Record the actual Windows version, Chrome version, build, and date during testing.
Existing responsive checks cover 1440px, 1024px, 768px, and 360px widths.
These widths do not add mandatory alternative browsers. Keyboard and accessible feedback requirements remain required.

### Language, currency, and editing

English is mandatory. Traditional Chinese, Simplified Chinese, and Japanese remain stretch.
Translate interface labels, navigation, validation, status labels, and assumptions for delivered sets.
Do not translate names, notes, descriptions, identities, source headers, or stored enums automatically.
Missing translations use English. Translation completeness does not establish linguistic accuracy.

With no saved preference, use English and USD. Later selections persist across browser restarts on that device.
Language and currency preferences remain independent. Reporting date remains a session setting.
Section 2 defines access. Sections 8–9 define edit boundaries without authentication.

### Persistence and demonstration isolation

Successful local records, source evidence, and histories survive normal restart in the selected data store.
Each rehearsal selects a new isolated demo data store. It starts without imported records, observations, tickets, overrides, or histories.
Normal saved data and browser preferences remain unchanged. Restarting the same rehearsal retains its saved state.

Another rehearsal uses another empty store. No destructive reset button is required.
Each new session defaults the financial reporting date to actual Hong Kong today.
The demonstrator selects financial example dates explicitly.

Store selection and startup mechanisms remain technical-planning details. Do not invent a working command or control before implementation.
Document and check a reproducible clean-environment startup later. Disclose any future hosted durability or reset limits accurately.
Core workflows require no live provider. Do not publish real data or confidential materials.

### Writing policy

Apply the supplied ASD-STE100 guidance. Use Strict mode for procedures, acceptance scenarios, message examples, and verification instructions.
Use STE-flavored mode for descriptions. This policy does not claim official dictionary compliance.

- Limit instruction sentences to 20 words.
- Limit descriptive sentences to 25 words.
- Write one instruction per sentence.
- Use active voice and simple tenses.
- Avoid semicolons, phrasal verbs, unnecessary nominalizations, and marketing adjectives.
- Limit paragraphs to one topic and six sentences.
- Use lists for sequences with three or more steps.
- Use the shared glossary consistently.
- Preserve facts, conditions, scope, numbers, and uncertainty.

Check these rules manually. The supplied linter is unavailable locally.
Record necessary precision exceptions in [the review record](spec-review.md).

## 14. Measurable completion criteria

SC-001: Every committed room has exactly three linked category records. Each invoice item resolves to one existing asset.
Initial assets require no invoice. AR-001 owns four-location fixture coverage.

SC-002: Check independent uploads, subsets, blockers, conflicts, precedence, historical-only items, repeats, stale previews, and atomic rollback.
Atomic uploads retain the v0.2 policy that superseded v0.1 partial imports.

SC-003: Check numerical examples, calendar boundaries, effective overrides, complete FX configuration, and replacement endpoints.

SC-004: Check permitted asset editing, invoice updates, overrides, source reset, observations, maintenance, histories, and normal restart persistence.
Disclose the excluded manual creation part of AR-002.

SC-005: Check consistent filters, distinct count units, room selection, empty states, and unique-asset financial totals.

SC-006: Retain this identifier as a traceability marker. AR-006 owns its presentation obligation.

SC-007: Record evidence for every required scenario before submission. Disclose unmet criteria.
Documentation coverage does not mean application acceptance.

SC-008: Check mandatory English, delivered translation boundaries, local/USD results, persistent preferences, separate dates, and rehearsal isolation.

The documentation revision requires all 28 checklist rows and complete required scenario coverage.
Application completion requires actual evidence under these SC and AR identifiers.

## 15. Decision and approval record

Alex reconfirmed D-001–D-016 and the existing Confirmed UI choices on 2026-10-03.
Source: Alex's answers to Q1–Q4 in this specification-readiness planning conversation, followed by the implementation request.
This confirmation leaves Proposed details pending. It is owner approval, not client acceptance or execution evidence.

| Decision | Selected policy | Rationale | Trace |
|---|---|---|---|
| D-001 | Room understanding and accountable maintenance first. Finance/replacement remain secondary. | Primary management outcome. | US-02–US-05, FR-007, FR-014 |
| D-002 | Independent atomic confirmed Assets and Invoices uploads with visible warnings. | Trusted initialization and updates. | US-01, FR-002–FR-004, FR-015 |
| D-003 | Preserve source identities. Skip identical repeats. Block changed identities. Apply new invoices by newest date. | Evidence and accountable updates. | US-01, FR-005 |
| D-004 | One existing room/category target per invoice item. Many items over time. Baseline finance is independent. No allocation. | Traceable purchases. | FR-001, FR-019 |
| D-005 | Paired override/reset/history. Applied invoices clear overrides. Reset restores latest invoice values or baseline values. | Accountable corrections. | US-03, US-05, FR-019 |
| D-006 | Cross-property editing within boundaries. Master data is import-only. No manual asset creation or identity changes. | Explicit edit scope and AR-002 gap. | FR-001, FR-010, FR-016 |
| D-007 | Consistent baseline observations. Assessed metadata is required. Clear returns Unknown. Invoices do not change observations. | Independent condition assessment. | FR-009, FR-016 |
| D-008 | Three forward-only statuses. Required owner in progress. Resolved read-only. Persistent history and defined sorting. | Accountable work. | US-04, FR-012, FR-013 |
| D-009 | Complete fixed fictional five-currency FX table. USD equals 1. | Reproducible reporting. | FR-011, FR-018 |
| D-010 | Grouped local totals and independent persistent language/currency choices. Initial defaults are English/USD. | Clear display. | FR-017, FR-018 |
| D-011 | Actual Asia/Hong_Kong operational date with separate session financial reporting date. | No historical-state claim. | FR-011, FR-014 |
| D-012 | Installation/purchase fallback, original-day anniversaries, zero residual, and capped straight-line depreciation. | Explainable valuation. | FR-011, SC-003 |
| D-013 | 90-day category and 12-month future window. Separate overdue/due-today totals. | Explicit spending horizon. | US-05, FR-014 |
| D-014 | English mandatory. Traditional Chinese, Simplified Chinese, and Japanese stretch. English fallback. | Bounded translation scope. | FR-017 |
| D-015 | Four properties, twelve rooms, thirty-six assets. One invocation produces fully populated valid and deliberately invalid pairs. | Reproducible fixtures. | AR-001, sample-data plan |
| D-016 | Full invoice snapshots and newest-date control. Older items remain evidence. Applied updates replace edits and retain history. | Clear current values. | US-01, US-03, FR-005, FR-019, SC-002, SC-004 |
| D-017 | Room manager primary. Executives and data-maintenance users support the maintenance decision. | Clear audience. | US-01–US-05, section 1 |
| D-018 | Windows laptop with Chrome required. Record the actual browser version during tests. | Defined walkthrough context. | Section 13, E-UI, E-DEMO |
| D-019 | New isolated store per rehearsal. Preserve normal saved data and browser preferences. No destructive reset button required. | Repeatable demonstrations. | FR-015, SC-004, SC-008, E-STARTUP, E-DEMO |

Historical record: v0.3 recorded approval on 2026-10-02.
It recorded revised D-002–D-007 and D-015, plus new D-016, from the approved v0.3 implementation plan.
Other rows retained earlier recorded approval. The current confirmation does not independently prove those older dates.

The v0.3 superseded policies remain superseded:

- Four-file paired imports and separate Rooms workbooks.
- Mandatory initial invoice links and single lifetime invoice linkage.
- Prohibition of all invoice-driven current-value updates.
- Generated manual asset creation, OTHER category, and minimum-only category coverage.
- Opt-in invalid sample generation.

Earlier superseded policies include valid-subset imports, Assigned status, partial FX reporting, and source-only spending proxies.
Retained policies include independent observations, atomic writes, and depreciation rules.

Deferred work includes translation review by Alex before submission.
Exact header spellings, parsing, identifier grammar, and technical history representations remain proposals in the contracts.
The owner-approved exclusion of manual creation does not remove the external AR-002 obligation.

## 16. Checklist coverage

Each row is Specified. This status describes documentation only. Application scenarios remain NOT RUN.

| ID | Checklist item | Defining section | Acceptance or authority coverage |
|---|---|---|---|
| CL-01 | Main user and primary decision | [Purpose](#1-problem-and-intended-outcome) | [Room review](acceptance-scenarios.md#us-02), [Maintenance](acceptance-scenarios.md#us-04), D-017 |
| CL-02 | End-to-end demonstration | [Purpose](#1-problem-and-intended-outcome), [Demo](demo.md#1-rehearsal-state) | [Demo scenarios](acceptance-scenarios.md#demo) |
| CL-03 | Required, optional, excluded capabilities | [Scope](#3-product-scope) | [Asset boundaries](acceptance-scenarios.md#ac-us03-001), [Languages](acceptance-scenarios.md#ac-us02-017) |
| CL-04 | Prototype limits | [Scope](#3-product-scope), [Demo disclosures](demo.md#4-explanation-and-disclosure) | [Assumptions](acceptance-scenarios.md#ac-ux-019) |
| CL-05 | Correct owner-approval labels | [Approval record](#15-decision-and-approval-record), [UI authority](ui-ux-spec.md#1-authority-and-context) | Q4 dated 2026-10-03. [Documentation review](spec-review.md) |
| CL-06 | Journey starts and successful outcomes | [Journeys](#5-user-journeys-and-acceptance-scenarios) | [Independent setups](acceptance-scenarios.md#verification-method) |
| CL-07 | Journey priorities and independent checks | [Journeys](#5-user-journeys-and-acceptance-scenarios) | [Verification method](acceptance-scenarios.md#verification-method) |
| CL-08 | Concrete Given/When/Then outcomes | [Journeys](#5-user-journeys-and-acceptance-scenarios) | [Required scenarios](acceptance-scenarios.md) |
| CL-09 | Invalid, empty, and failure cases | [Failures](#12-failure-and-edge-cases) | [Import](acceptance-scenarios.md#us-01), [Room](acceptance-scenarios.md#us-02), [Writes](acceptance-scenarios.md#ac-ux-013) |
| CL-10 | Measurable completion | [Completion](#14-measurable-completion-criteria) | SC-001–SC-008, [Evidence ledger](assessment-requirements.md#5-evidence-ledger) |
| CL-11 | Depreciation timing and fallback | [Finance](#8-asset-and-financial-rules) | [Financial scenarios](acceptance-scenarios.md#us-05) |
| CL-12 | Reporting and replacement dates | [Finance](#8-asset-and-financial-rules), [Replacement](#10-dashboard-and-replacement-planning) | [Financial scenarios](acceptance-scenarios.md#us-05) |
| CL-13 | FX direction, date, and missing rates | [Currency](#currency) | [FX checks](acceptance-scenarios.md#ac-us05-008) |
| CL-14 | Import warnings, rejection, conflict, and partial import | [Import](#7-import-rules) | [Import scenarios](acceptance-scenarios.md#us-01) |
| CL-15 | Observations and maintenance relationship | [Condition](#9-condition-and-maintenance-rules) | [Independent conditions](acceptance-scenarios.md#ac-us02-013), [Resolution](acceptance-scenarios.md#ac-us04-013) |
| CL-16 | Maintenance transitions and required information | [Maintenance](#maintenance) | [Maintenance scenarios](acceptance-scenarios.md#us-04) |
| CL-17 | Replacement priorities and spending proxies | [Replacement](#10-dashboard-and-replacement-planning) | [Replacement scenarios](acceptance-scenarios.md#us-05) |
| CL-18 | Entity meanings | [Data meaning](#11-data-meaning-and-relationships), [Glossary](glossary.md) | [Asset identity](acceptance-scenarios.md#ac-us03-001), [Invoice](acceptance-scenarios.md#ac-us01-002) |
| CL-19 | Identity and relationship rules | [Sources](#4-source-data-identity-and-evidence) | [Import integrity](acceptance-scenarios.md#us-01), [Ticket links](acceptance-scenarios.md#ac-us04-002) |
| CL-20 | Required and optional information | [Data meaning](#11-data-meaning-and-relationships) | [Warnings](acceptance-scenarios.md#ac-us01-008), [Assessment metadata](acceptance-scenarios.md#ac-us02-010) |
| CL-21 | Imported provenance | [Data meaning](#11-data-meaning-and-relationships) | [Source history](acceptance-scenarios.md#ac-us03-005) |
| CL-22 | Stored and calculated information | [Finance](#8-asset-and-financial-rules), [Data meaning](#11-data-meaning-and-relationships) | [Read-only results](acceptance-scenarios.md#ac-us03-002), [FX](acceptance-scenarios.md#ac-us05-008) |
| CL-23 | Unknown does not mean zero or Healthy | [Data meaning](#11-data-meaning-and-relationships) | [Unknown](acceptance-scenarios.md#ac-us02-009), [Missing FX](acceptance-scenarios.md#ac-us05-009) |
| CL-24 | Primary device and browser | [Experience](#13-quality-and-experience-requirements) | [Browser checks](acceptance-scenarios.md#ac-ux-016), [Demo record](acceptance-scenarios.md#ac-demo-004) |
| CL-25 | Explicit language scope | [Scope](#3-product-scope), [Experience](#13-quality-and-experience-requirements) | [Language checks](acceptance-scenarios.md#ac-us02-017) |
| CL-26 | Language, currency, and date effects | [Experience](#13-quality-and-experience-requirements) | [Preferences](acceptance-scenarios.md#ac-us02-016), [Date independence](acceptance-scenarios.md#ac-us02-008) |
| CL-27 | Edit permissions and scope | [Users](#2-users), [Asset rules](#8-asset-and-financial-rules) | [Cross-property edits](acceptance-scenarios.md#ac-us02-007), [Fixed identity](acceptance-scenarios.md#ac-us03-002) |
| CL-28 | Persistence, demonstration, and reset | [Experience](#13-quality-and-experience-requirements), [Demo](demo.md#1-rehearsal-state) | [Demo isolation](acceptance-scenarios.md#ac-demo-001), [Restart](acceptance-scenarios.md#ac-demo-002) |

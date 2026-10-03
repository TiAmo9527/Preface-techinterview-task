# Required acceptance scenarios

Version: 0.2

Revised: 2026-10-03

Status: Required verification defined. Every application scenario is NOT RUN.

Authority: [Product specification v0.5](product-spec.md). Domain terms use the [shared glossary](glossary.md).

These scenarios describe required behavior. They do not report executed tests.
Delivered stretch translations have conditional acceptance. Previously proposed interactions are approved in [UI/UX requirements](ui-ux-spec.md) and mapped in [verification](verification-plan.md).

## Verification method

1. Select one scenario or one listed case.
2. Prepare its Given state independently in an isolated test store.
3. Record the previous saved records, source evidence, histories, preferences, and operational clock when relevant.
4. Execute its When action.
5. Check every Then result and unchanged-state requirement.
6. Record method, build/date, expected result, actual result, and PASS, FAIL, or NOT RUN.

Do not execute another scenario as a prerequisite. Repeated cases require independent prepared states.
Numeric FX examples are isolated test inputs, not chosen application rates.
The four-property baseline is demonstration coverage, not a capacity limit.

Every scenario maps to its journey, functional requirements, completion criteria, assessment obligations, and evidence group.
SC-007 applies to every required scenario's evidence record. AR-007 requires fictional data throughout.
Use [the assessment ledger](assessment-requirements.md#5-evidence-ledger) for actual evidence.

<a id="us-01"></a>

## US-01

<a id="ac-us01-001"></a>

### AC-US01-001: Baseline without invoices

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an empty store and a valid baseline with four properties, twelve rooms, and thirty-six assets.

**When** the data-maintenance user confirms Assets without Invoices.

**Then** the upload saves four properties, twelve rooms, and thirty-six linked assets. Each room has three distinct categories. Baseline finance works with valid FX configuration. Source provenance remains inspectable.

<a id="ac-us01-002"></a>

### AC-US01-002: Independent invoice subset

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains existing complete rooms and a valid invoice upload targeting two asset records.

**When** the user confirms Invoices without an Assets workbook.

**Then** two invoice items update the two targets. No property, room, or asset identity is created. Untargeted records remain unchanged.

<a id="ac-us01-003"></a>

### AC-US01-003: Unknown or ambiguous targets

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an existing baseline and an invoice row with an unknown room, absent category target, or ambiguous target.

**When** the user previews the upload.

**Then** the row has an actionable blocker. Confirmation cannot save any rows. Existing records, evidence, and histories remain unchanged.

<a id="ac-us01-004"></a>

### AC-US01-004: Baseline integrity blockers

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an empty store and a baseline containing one defect from the case table.

**When** the user previews the baseline.

**Then** the upload reports the defect and blocks all writes. No property, room, asset, observation, or source evidence is created.

Run each case independently:

| Defect | Expected blocker |
|---|---|
| Duplicate asset identity, including identical rows | Duplicate source identity. |
| Two Lighting records in one room | Duplicate category and missing category. |
| Missing Air conditioning record | Incomplete room. |
| Unsupported fourth category | Unsupported category. |
| Different property names for one property identity | Inconsistent property baseline. |
| Different room labels or assessments for one room identity | Inconsistent room baseline. |
| Region/parent identity mismatch | Invalid relationship. |
| Duplicate room number within one property | Invalid room identity relationship. |

<a id="ac-us01-005"></a>

### AC-US01-005: Occupied category and changed baselines

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an existing complete room and preserved property, room, and asset baselines.

**When** the user previews changed baseline evidence or a new asset identity occupying an existing category.

**Then** the upload reports a conflict. Existing baseline and operational information remain unchanged. Valid surrounding rows do not commit.

<a id="ac-us01-006"></a>

### AC-US01-006: Invalid row values

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an existing target or empty baseline store and an upload containing one invalid required value.

**When** the user previews the upload.

**Then** the upload reports field and coordinate diagnostics. Every row remains uncommitted.

Run each defect independently:

- Missing required cost, currency, purchase date, name, or identity.
- Negative or non-finite cost.
- Unsupported currency, category, condition, or location.
- Zero, negative, or fractional useful life.
- Impossible date or installation before purchase.
- Recorded assessment without a date or recorder.
- Assessment metadata without a status.

Exact parsing examples are approved in the data contracts.

<a id="ac-us01-007"></a>

### AC-US01-007: File and header failures

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains a selected import workflow and a missing, unreadable, unsupported, or structurally invalid workbook.

**When** the user attempts preview or confirmation.

**Then** the interface reports an actionable blocker. No successful writes appear. Saved state remains unchanged.

Exact header, sheet, formula, and format parsing rules are approved in [data contracts](data-contracts.md).

<a id="ac-us01-008"></a>

### AC-US01-008: Warning-only success

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains valid source rows with absent installation, explicit zero cost, or an absent optional invoice supplier.

**When** the user previews the upload and confirms it.

**Then** warnings remain visible during review. The valid upload commits atomically. Missing installation uses purchase-date fallback. Explicit zero remains zero.

<a id="ac-us01-009"></a>

### AC-US01-009: Preview and diagnostics

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains existing targets with manual edits and active overrides, plus a valid newer invoice upload.

**When** the user previews the upload.

**Then** six-field before/after changes and override clearing appear. Counts distinguish records, evidence, updates, history-only items, skips, warnings, and blockers. Preview saves nothing.

Diagnostics identify file, sheet, row, field, offending information, and actionable reason when available. Distinct asset updates do not equal invoice-row counts.

<a id="ac-us01-010"></a>

### AC-US01-010: Newest date independent of order

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains one target and distinct valid invoice snapshots dated 2026-09-01 and 2026-10-01.

**When** the user uploads the rows in either order or separate upload orders.

**Then** the 2026-10-01 snapshot controls current source values. Both items remain evidence. Upload time and row order do not select current values.

<a id="ac-us01-011"></a>

### AC-US01-011: Historical-only older items

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an applied 2026-10-01 invoice, subsequent manager edits, and an active override.

**When** the user confirms a new valid invoice item dated 2026-09-01.

**Then** the item becomes historical-only evidence. Current operational values and the override remain unchanged. No applied-update event appears.

<a id="ac-us01-012"></a>

### AC-US01-012: Controlling-date conflict

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains one target with stored or incoming snapshots at its maximum invoice date.

**When** the user previews another distinct item at that date with a different six-field snapshot.

**Then** the entire upload is blocked. Valid surrounding evidence, records, and histories remain uncommitted.

<a id="ac-us01-013"></a>

### AC-US01-013: Equivalent controlling-date evidence

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an applied snapshot, subsequent manager edits, and an active override.

**When** the user confirms a distinct invoice identity with the same maximum date and equivalent snapshot.

**Then** the new evidence is retained without replaying the update. Manager edits and overrides remain unchanged. Asset values are not duplicated.

<a id="ac-us01-014"></a>

### AC-US01-014: Identical baseline repeat after edits

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains a preserved baseline followed by invoices, asset edits, overrides, and changed observations.

**When** the user confirms an identical baseline repeat.

**Then** existing source identities skip. The upload restores no previous values. Operational records, original provenance, and histories remain unchanged.

<a id="ac-us01-015"></a>

### AC-US01-015: Identical invoice repeat after edits

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains accepted invoice evidence followed by manager edits, overrides, and observation changes.

**When** the user confirms an identical invoice-item repeat.

**Then** the existing item skips, including an older item. No operational values, original provenance, or histories change.

<a id="ac-us01-016"></a>

### AC-US01-016: Changed source identity

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an accepted invoice item or asset baseline with preserved source values.

**When** the user previews changed source values under that existing identity.

**Then** the upload reports a source conflict. No evidence rewrite or operational update occurs.

<a id="ac-us01-017"></a>

### AC-US01-017: Duplicate identity inside upload

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an otherwise valid upload with the same asset identity or invoice-item identity twice.

**When** the user previews the upload.

**Then** the whole upload is blocked even when duplicate rows are identical. No rows commit.

<a id="ac-us01-018"></a>

### AC-US01-018: Applied invoice replaces edits

Trace: US-01 | FR-005, FR-015, FR-019 | SC-002, SC-004 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an existing target with manually edited snapshot fields and an active paired financial override.

**When** the user confirms a strictly newer controlling invoice.

**Then** all six fields take the new snapshot values. The override clears with linked system-attributed history. Before/after values and evidence remain inspectable. Identity, room, category, observations, and tickets remain unchanged.

<a id="ac-us01-019"></a>

### AC-US01-019: Blank installation clears previous date

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains an existing asset with an installation date and an eligible newer invoice with blank installation.

**When** the user confirms that invoice.

**Then** the installation date becomes absent. Purchase-date fallback controls financial results. Source evidence and previous values remain in history.

<a id="ac-us01-020"></a>

### AC-US01-020: Commit failure rolls back all effects

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains a valid upload with inserts, invoice evidence, asset updates, and override/history changes.

**When** persistence fails during confirmation.

**Then** the previous saved state remains intact. No partial records, evidence, or histories remain. The interface reports failure instead of successful counts.

<a id="ac-us01-021"></a>

### AC-US01-021: Changed stale preview

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains a valid preview followed by a saved change that alters its proposed result.

**When** the user attempts confirmation using the old preview.

**Then** no upload changes commit from the old confirmation. Refreshed review and renewed confirmation are required. Current saved state remains intact.

<a id="ac-us01-022"></a>

### AC-US01-022: Cancellation and no-op inputs

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains a valid preview, a headers-only workbook, or a workbook with fully empty rows.

**When** the user cancels the preview or confirms an otherwise valid no-op upload.

**Then** cancellation saves nothing. A no-op upload reports zero new rows. Existing records and original source evidence remain unchanged.

Run cancellation and each no-op input as independent cases. Partially populated rows use normal validation.

<a id="ac-us01-023"></a>

### AC-US01-023: First invoice and equal-value newer invoice

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains a baseline without an applied invoice, or an applied invoice followed by a strictly newer equivalent snapshot.

**When** the user confirms the eligible controlling invoice.

**Then** the snapshot applies. Baseline purchase date does not block the first invoice. A newer date applies despite equal snapshot values.

Run both starting states independently. Applied updates replace subsequent edits and clear active overrides under the normal history rules.

<a id="ac-us01-024"></a>

### AC-US01-024: Different older snapshots

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains a target with a controlling 2026-10-01 snapshot and distinct valid older items sharing 2026-09-01.

**When** the user confirms the older items with different snapshots.

**Then** both items remain historical-only evidence. Their disagreement does not control current values. Required-field and target errors would still block.

<a id="ac-us01-025"></a>

### AC-US01-025: Provenance and new rooms

Trace: US-01 | FR-001, FR-002, FR-003, FR-005, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-IMPORT.

**Given** the setup contains a preserved property baseline and a valid new room with all three categories.

**When** the user confirms its Assets rows.

**Then** one room and three assets are created under the existing property. Baseline and contributing source coordinates remain inspectable. Unrelated records stay unchanged.

<a id="us-02"></a>

## US-02

<a id="ac-us02-001"></a>

### AC-US02-001: Consistent reporting scope

Trace: US-02 | FR-006, FR-007, FR-008, FR-009 | SC-005 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains two locations with independently prepared properties, rooms, tickets, observations, and asset values.

**When** the manager selects a location, property, or room filter.

**Then** every count, operational table, financial result, and replacement result uses the same scope. Saved records remain unchanged.

<a id="ac-us02-002"></a>

### AC-US02-002: Incompatible child filters

Trace: US-02 | FR-006, FR-007, FR-008, FR-009 | SC-005 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains selected location, property, and room filters.

**When** the manager changes a parent to exclude its selected child.

**Then** incompatible child selections clear. Every scoped output refreshes. No stale room card or table shows excluded records.

<a id="ac-us02-003"></a>

### AC-US02-003: Empty results

Trace: US-02 | FR-006, FR-007, FR-008, FR-009 | SC-005 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains an empty portfolio or selected filters with no matching records.

**When** the manager opens or changes Overview.

**Then** the interface shows the appropriate empty state. Counts reflect no matching entities. No stale rows or values appear.

<a id="ac-us02-004"></a>

### AC-US02-004: Operational ordering and count units

Trace: US-02 | FR-006, FR-007, FR-008, FR-009 | SC-005 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains rooms with three observations and both unresolved and resolved tickets.

**When** the manager opens Overview.

**Then** operational counts and the central room view precede unresolved maintenance. Finance and replacement follow. Each count labels its entity or ticket unit. Observations group by system and state.

<a id="ac-us02-005"></a>

### AC-US02-005: Room context through every link

Trace: US-02 | FR-006, FR-007, FR-008, FR-009 | SC-005 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains an existing room with three assets, three observations, and unresolved/resolved tickets.

**When** the manager selects its Map tile, List row, or operational ticket link.

**Then** the same room context appears. Property, assets, observations, and separate ticket groups match the selected room. Selection saves no data.

<a id="ac-us02-006"></a>

### AC-US02-006: No financial duplication

Trace: US-02 | FR-006, FR-007, FR-008, FR-009 | SC-005 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains one asset valued at USD 1,200 with two linked unresolved tickets and multiple invoice evidence items.

**When** the manager reviews the scope with valid FX configuration.

**Then** the interface counts two tickets and one asset. Acquisition value includes USD 1,200 once. Observations remain separate counts.

<a id="ac-us02-007"></a>

### AC-US02-007: Cross-property access and edit boundary

Trace: US-02 | FR-001, FR-010, FR-016 | SC-004, SC-005 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains two imported fictional properties and their complete rooms.

**When** the manager selects either property and saves a valid permitted observation or asset edit.

**Then** the selected record changes. Property and room master-data forms remain absent. Identity and category remain fixed.

<a id="ac-us02-008"></a>

### AC-US02-008: Reporting date does not change operations

Trace: US-02 | FR-011, FR-014 | SC-003, SC-008 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains current observations, ticket timestamps, and operational overdue ordering.

**When** the manager changes the financial reporting date.

**Then** financial and replacement results refresh. Observations, source evidence, tickets, timestamps, and operational overdue ordering remain unchanged.

<a id="ac-us02-009"></a>

### AC-US02-009: Unknown does not mean Healthy

Trace: US-02 | FR-009, FR-016 | SC-001, SC-004 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains a valid baseline with blank observation groups or UNKNOWN without metadata.

**When** the user confirms the baseline and inspects its room.

**Then** each missing assessment is unassessed Unknown. No date, recorder, or note exists. No Healthy state is inferred.

<a id="ac-us02-010"></a>

### AC-US02-010: Recorded assessment metadata

Trace: US-02 | FR-009, FR-016 | SC-004 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains an existing room observation and a draft recorded state, including recorded Unknown.

**When** the manager saves without a date or recorder.

**Then** field feedback blocks the save. The previous observation remains unchanged. Missing metadata never becomes a satisfactory assessment.

<a id="ac-us02-011"></a>

### AC-US02-011: Record Healthy

Trace: US-02 | FR-009, FR-016 | SC-004 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains an existing room observation and a valid date and recorder.

**When** the manager saves a Healthy assessment.

**Then** Healthy, date, recorder, and any note persist. Room and dashboard results refresh. Baseline evidence and tickets remain unchanged.

<a id="ac-us02-012"></a>

### AC-US02-012: Clear assessment

Trace: US-02 | FR-009, FR-015, FR-016 | SC-004 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains a recorded observation with date, recorder, and note.

**When** the manager clears the assessment and restarts normally.

**Then** unassessed Unknown persists without date, recorder, or note. No observation history appears. Baseline evidence and tickets remain unchanged.

<a id="ac-us02-013"></a>

### AC-US02-013: Observations and tickets are independent

Trace: US-02 | FR-009, FR-012, FR-014, FR-016 | SC-004, SC-005 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains a Healthy observation with unresolved maintenance, including a room-only Critical ticket.

**When** the manager reviews the room or changes a ticket.

**Then** Healthy can remain visible with unresolved faults. The room-only fault remains visible. No asset receives an inferred critical flag. Ticket changes do not update observations.

<a id="ac-us02-014"></a>

### AC-US02-014: Invalid imported assessment and baseline repeat

Trace: US-02 | FR-003, FR-005, FR-016 | SC-002, SC-004 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains an empty store with invalid observation metadata, or a saved baseline followed by a manager assessment edit.

**When** the user previews the invalid baseline or confirms an identical baseline repeat.

**Then** invalid metadata blocks all baseline writes. Identical repeats preserve the latest manager assessment.

Run each starting state independently.

<a id="ac-us02-015"></a>

### AC-US02-015: Observation cancellation and failure

Trace: US-02 | FR-015, FR-016 | SC-004 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains an existing observation and a changed draft.

**When** the manager cancels, or persistence fails during Save.

**Then** the previous saved assessment remains unchanged. Cancel creates no history. Failed Save reports failure and preserves the draft for correction.

<a id="ac-us02-016"></a>

### AC-US02-016: Defaults and persistent independent preferences

Trace: US-02 | FR-017, FR-018 | SC-008 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains no saved preferences, or independently prepared delivered-language and currency selections.

**When** the user starts the interface, changes one preference, or restarts the browser.

**Then** first use starts in English/USD. Changing one preference leaves the other unchanged. Saved selections survive browser restart. Stored asset values remain unchanged.

Run first use, each preference change, and browser restart independently.

<a id="ac-us02-017"></a>

### AC-US02-017: English and conditional translations

Trace: US-02 | FR-017 | SC-008 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains mandatory English interface text and any delivered stretch translation set with one missing key.

**When** the user selects each delivered language and reviews interface text.

**Then** labels, navigation, validation, status labels, and assumptions use the selected set. Missing keys use English. Stored names, notes, descriptions, identities, headers, and enums remain unchanged.

Traditional Chinese, Simplified Chinese, and Japanese remain stretch. Apply translation checks only to delivered sets. Completeness does not prove linguistic accuracy.

<a id="ac-us02-018"></a>

### AC-US02-018: Local and USD display

Trace: US-02 | FR-011, FR-018 | SC-003, SC-008 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains assets in HKD, SGD, GBP, JPY, and USD with effective values and complete fixed FX configuration.

**When** the user switches Currency between local and USD.

**Then** local totals remain separate by currency. USD totals use configured rates. Source values and active overrides remain unchanged.

<a id="ac-us02-019"></a>

### AC-US02-019: Session financial date

Trace: US-02 | FR-011, FR-015, FR-018 | SC-004, SC-008 | AR-004 | E-ROOM, E-UI.

**Given** the setup contains an existing session with a selected financial reporting date and saved preferences.

**When** the user navigates within the session, then starts a new session.

**Then** navigation retains the session date. The new session uses actual Hong Kong today. Browser preferences and saved records remain unchanged.

<a id="us-03"></a>

## US-03

<a id="ac-us03-001"></a>

### AC-US03-001: Three fixed category records

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains an imported room with its three asset records and a later purchase snapshot.

**When** the manager inspects the room before or after an applied invoice.

**Then** Lighting, Water supply, and Air conditioning remain the three stable records. No Add asset action exists. Invoice replacement creates no new asset identity. AR-002 manual creation remains unmet.

<a id="ac-us03-002"></a>

### AC-US03-002: Permitted fields and read-only results

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains an existing asset with calculated financial results.

**When** the manager opens its editor.

**Then** name, purchase/installation dates, and useful life are editable. Identity, room, category, and calculated results remain read-only. Cost/currency changes use the separate paired override.

<a id="ac-us03-003"></a>

### AC-US03-003: Invalid, cancelled, and failed edits

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains an existing asset and a draft edit.

**When** the manager saves invalid input, cancels, or encounters persistence failure.

**Then** invalid input produces field feedback. Each unsuccessful operation preserves saved values and histories. Failed Save reports no success.

Run invalid dates, installation before purchase, invalid life, cancellation, and failure independently.

<a id="ac-us03-004"></a>

### AC-US03-004: Saved edits and normal restart

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains a baseline asset and valid changed name, dates, and useful life.

**When** the manager saves and restarts normally.

**Then** the operational edits persist. Room, financial, dashboard, and replacement results refresh. Source evidence and fixed identity remain unchanged.

<a id="ac-us03-005"></a>

### AC-US03-005: Inspect source and histories

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains a preserved baseline, accepted invoices, historical-only items, an applied update, and override history.

**When** the manager opens the asset evidence sections.

**Then** all evidence and provenance remain inspectable. Applied history shows previous operational fields and override state. Historical-only items are not false update events. Inspection changes no values.

<a id="ac-us03-006"></a>

### AC-US03-006: Set paired financial override

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains an asset with source values and a complete override pair, reason, and recorder.

**When** the manager saves the override.

**Then** effective values use the override. History records before/after values and actual timestamp. Financial and replacement results refresh. Baseline and invoice evidence remain unchanged.

<a id="ac-us03-007"></a>

### AC-US03-007: Reject incomplete override

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains an asset with an override draft missing cost, currency, reason, or recorder.

**When** the manager attempts Save.

**Then** field feedback blocks the save. Effective values and history remain unchanged.

Run each missing field independently.

<a id="ac-us03-008"></a>

### AC-US03-008: Reset to latest applied invoice

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains an asset with a baseline, applied invoice, active override, and a reset reason and recorder.

**When** the manager resets financial values.

**Then** effective values return to the latest applied invoice pair. History retains the previous override and records the reset. Names, dates, observations, and source evidence remain unchanged.

<a id="ac-us03-009"></a>

### AC-US03-009: Reset to baseline before invoices

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains an asset without applied invoices, with an active override and a reset reason and recorder.

**When** the manager resets financial values.

**Then** effective values return to the baseline pair. Reset history persists. Names, dates, observations, and baseline evidence remain unchanged.

<a id="ac-us03-010"></a>

### AC-US03-010: Invalid or failed override reset

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains an active override and a reset draft without required attribution, or a valid draft with persistence failure.

**When** the manager attempts reset.

**Then** the reset fails with feedback. Effective values and histories remain unchanged.

Run missing reason, missing recorder, and persistence failure independently.

<a id="ac-us03-011"></a>

### AC-US03-011: Applied and historical invoice effects

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains manually edited fields and an active override after an applied invoice.

**When** the user confirms a strictly newer invoice, older evidence, equivalent same-date evidence, or an identical repeat.

**Then** a newer invoice replaces six fields and clears the override with history. The other cases preserve edits and overrides.

Run each invoice case independently. Source evidence remains preserved in every successful case.

<a id="ac-us03-012"></a>

### AC-US03-012: Display settings do not edit assets

Trace: US-03 | FR-010, FR-015, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-ASSET, E-FINANCE.

**Given** the setup contains an asset with an active override and stored source values.

**When** the user changes Language, Currency, or financial reporting date.

**Then** no source values, override values, or histories change. Only the applicable interface or calculated display changes.

<a id="us-04"></a>

## US-04

<a id="ac-us04-001"></a>

### AC-US04-001: Create Open ticket

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an existing room and a valid fault description and severity.

**When** the manager saves a new fault with or without an owner.

**Then** exactly one Open ticket persists with actual opened/updated timestamps. The optional owner and target date persist when supplied. No observation changes.

<a id="ac-us04-002"></a>

### AC-US04-002: Same-room asset link

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains two existing rooms and their asset records.

**When** the manager attempts a ticket link to an asset from another room.

**Then** validation blocks creation. No ticket or history is saved. A valid same-room link or room-only fault remains permitted.

<a id="ac-us04-003"></a>

### AC-US04-003: Fixed ticket associations

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an independently prepared unresolved ticket linked to a room and optional asset.

**When** the manager attempts to change its room or asset association.

**Then** the association change is unavailable or rejected. Existing ticket information and history remain unchanged.

<a id="ac-us04-004"></a>

### AC-US04-004: Start work with owner

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an Open ticket with an assigned owner.

**When** the manager starts work.

**Then** status becomes In progress. Actual change time and before/after history persist. Room, asset link, and observations remain unchanged.

<a id="ac-us04-005"></a>

### AC-US04-005: Reject ownerless start

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an Open ticket without an owner.

**When** the manager attempts In progress.

**Then** the interface identifies the required owner. Status remains Open. No successful transition or history appears.

<a id="ac-us04-006"></a>

### AC-US04-006: Resolve with note

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an In progress ticket with an owner and a non-empty resolution note.

**When** the manager resolves the ticket.

**Then** status becomes Resolved. The actual resolution timestamp, note, and history persist. The ticket becomes read-only.

<a id="ac-us04-007"></a>

### AC-US04-007: Reject empty resolution note

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an In progress ticket with an owner and a blank resolution note.

**When** the manager attempts resolution.

**Then** validation blocks resolution. Status and existing histories remain unchanged.

<a id="ac-us04-008"></a>

### AC-US04-008: Disallowed transitions and deletion

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an Open or Resolved ticket prepared for the tested action.

**When** the manager attempts Open → Resolved, reopening, or deletion.

**Then** the action is unavailable or rejected. Saved records and histories remain unchanged.

Run each disallowed action independently.

<a id="ac-us04-009"></a>

### AC-US04-009: Owner removal and reassignment

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an unresolved ticket with an owner in Open or In progress.

**When** the manager removes or reassigns its owner.

**Then** Open permits owner removal. In progress blocks owner removal. Both unresolved statuses permit reassignment with history.

Run each status/action combination independently.

<a id="ac-us04-010"></a>

### AC-US04-010: Unresolved edits and chronology

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an Open or In progress ticket with existing history.

**When** the manager saves description, severity, target date, owner, or an allowed status change.

**Then** valid changes persist with chronological before/after history and actual timestamps. History survives normal restart. Fixed links remain unchanged.

Run each field independently. Check simultaneous saved changes as one ordered event under the approved history representation.

<a id="ac-us04-011"></a>

### AC-US04-011: Cancellation and persistence failure

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an unresolved ticket with a changed draft, or a valid new fault draft.

**When** the manager cancels or persistence fails during Save.

**Then** existing saved state remains unchanged. New drafts create no ticket. Failure reports no success and retains the draft.

Run new-ticket and existing-ticket cases independently.

<a id="ac-us04-012"></a>

### AC-US04-012: Resolved ticket is read-only

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains a Resolved ticket with resolution information and history.

**When** the manager attempts to change any ticket field.

**Then** editing is unavailable or rejected. Ticket information and histories remain unchanged.

<a id="ac-us04-013"></a>

### AC-US04-013: Resolution does not alter observations or replacement

Trace: US-04 | FR-009, FR-012, FR-013, FR-014, FR-016 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains an In progress ticket, a manual observation, and a calculated replacement date.

**When** the manager resolves the ticket with a valid note.

**Then** only the ticket and maintenance history change. Observation and expected replacement date remain unchanged.

<a id="ac-us04-014"></a>

### AC-US04-014: Priority and actual overdue date

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains tickets with different severities, target dates, and opening timestamps.

**When** the manager reviews unresolved tickets.

**Then** Critical precedes Medium and Low. Within severity, overdue targets precede others. Oldest opening time orders each group. Only dates before actual Hong Kong today are overdue.

Prepare yesterday, today, future, and absent targets. Changing financial reporting date must preserve this ordering.

<a id="ac-us04-015"></a>

### AC-US04-015: Separate resolved records and missing information

Trace: US-04 | FR-012, FR-013, FR-015 | SC-004 | AR-005 | E-MAINT.

**Given** the setup contains unresolved tickets without owner/target and resolved tickets with resolution metadata.

**When** the manager reviews maintenance.

**Then** unresolved rows show Unassigned and target-date absence explicitly. Resolved tickets appear separately with read-only history. No missing owner becomes an assumed assignment.

<a id="ac-us04-016"></a>

### AC-US04-016: Explicit critical asset flags

Trace: US-04 | FR-007, FR-012, FR-014, FR-016 | SC-004, SC-005 | AR-005 | E-MAINT.

**Given** the setup contains a room-only Critical ticket and an explicitly asset-linked Critical ticket.

**When** the manager reviews room and replacement results.

**Then** the room-only ticket flags no assets. Only the explicitly linked asset has the critical unresolved flag. Observation states remain unchanged.

<a id="us-05"></a>

## US-05

<a id="ac-us05-001"></a>

### AC-US05-001: Whole completed months

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains USD 1,200 effective cost, service 2026-01-15, and useful life twelve months.

**When** the user reports at 2026-07-14 or 2026-07-15.

**Then** July 14 gives depreciation USD 500 and book value USD 700. July 15 gives USD 600 for both. Stored values remain unchanged.

Run each reporting date independently.

<a id="ac-us05-002"></a>

### AC-US05-002: Month-end original-day anniversaries

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains a service anchor of 2026-01-31 and useful life twelve months.

**When** the user reports at 2026-02-28, 2026-03-30, or 2026-03-31.

**Then** completed months are one, one, and two respectively. Anniversaries use February 28 and March 31. The service anchor remains January 31.

Run each reporting date independently.

<a id="ac-us05-003"></a>

### AC-US05-003: Leap-year boundaries

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains service 2024-01-31, or service 2024-02-29 with twelve-month life.

**When** the user calculates anniversaries and replacement.

**Then** January service anniversaries are 2024-02-29 and 2024-03-31. February service replacement is 2025-02-28.

Run each service anchor independently.

<a id="ac-us05-004"></a>

### AC-US05-004: Before service and useful-life cap

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains a positive effective cost and positive useful life.

**When** the user reports before service, at life completion, or after life completion.

**Then** before service, depreciation is zero. At or after life completion, depreciation equals cost and book value is zero. Results never exceed those bounds.

Run each reporting boundary independently.

<a id="ac-us05-005"></a>

### AC-US05-005: Installation fallback and current edited anchor

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains an asset with absent installation, or a valid manager-edited installation date.

**When** the user reviews financial and replacement results.

**Then** absent installation visibly uses purchase date. Edited installation uses the current date, not immutable source evidence. Source evidence remains unchanged.

Run missing installation and edited installation independently.

<a id="ac-us05-006"></a>

### AC-US05-006: Replacement date and urgency

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains independently prepared assets due before, on, and after reporting date R.

**When** the user reviews replacement categories.

**Then** dates before R are overdue. Dates equal to R are due today. Dates after R are future. Replacement uses the service anchor plus useful-life months.

<a id="ac-us05-007"></a>

### AC-US05-007: Future-window boundaries

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains assets due at R, R + 1 day, R + 90 days, and the twelve-calendar-month endpoint.

**When** the user reports at R.

**Then** due soon excludes R and includes days 1 through 90. The future spending window excludes R and includes its calendar-month endpoint.

Also prepare dates one day after each endpoint. Day 91 is Later. Dates after the twelve-month endpoint are excluded. Check month-end and leap-year clamping independently.

<a id="ac-us05-008"></a>

### AC-US05-008: FX direction and fixed date

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains complete dated fictional rates, including HKD rate 0.125 and USD rate 1.

**When** the user reports HKD 800 and changes financial reporting date.

**Then** HKD 800 displays as USD 100. The configured FX date and disclaimer remain visible. Changing reporting date does not select another rate table. Source and override values remain unchanged.

The numeric rate is an isolated test input. It does not select application or market rates.

<a id="ac-us05-009"></a>

### AC-US05-009: Missing or invalid FX configuration

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains one missing rate, absent FX date, duplicate currency, invalid finite/positive rate, or USD rate other than 1.

**When** the user requests financial reporting.

**Then** configuration feedback requires correction. No incomplete portfolio total, zero substitute, or omitted affected amount appears. Source values remain unchanged.

Run each configuration defect independently. Also check wholly absent configuration.

<a id="ac-us05-010"></a>

### AC-US05-010: Effective-cost spending proxy

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains an asset with source cost USD 1,200, active override USD 900, and book value USD 300.

**When** the user reviews its replacement spending proxy.

**Then** the proxy is USD 900. It does not subtract book value. Reset or an applied invoice recalculates from the effective pair.

<a id="ac-us05-011"></a>

### AC-US05-011: Separate horizons and shared filters

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains assets in two properties, with overdue, due-today, and future-window replacement dates.

**When** the user selects one property and reviews spending.

**Then** only that property contributes. Overdue, due-today, and future totals remain separate. Each asset contributes once within each applicable total.

<a id="ac-us05-012"></a>

### AC-US05-012: Planning labels and independent flags

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains an overdue asset, a future asset with an explicit Critical ticket, and a room-only Critical ticket.

**When** the user reviews replacement information.

**Then** labels identify planning dates and acquisition-cost proxies. Explicit critical flags remain separate from date categories. Room-only faults infer no asset flag.

The interface claims no quotation, inflation allowance, installation labor estimate, predicted failure, or production accounting compliance.

<a id="ac-us05-013"></a>

### AC-US05-013: Unrounded aggregation and local display

Trace: US-05 | FR-011, FR-014, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-FINANCE.

**Given** the setup contains two USD assets valued at 0.004 each, plus assets in different local currencies.

**When** the user aggregates in USD or selects local mode.

**Then** the USD aggregate rounds 0.008 to 0.01 after aggregation. Local totals remain separated by currency. Stored source amounts remain unchanged.

The rounding example is an isolated test input. It does not change the warning-free demonstration fixtures.

<a id="confirmed-ui"></a>

## Confirmed UI requirements

<a id="ac-ux-001"></a>

### AC-UX-001: Navigation and header controls

Trace: See journey trace below | FR-017, FR-018 | SC-008 | AR-002 | E-UI.

**Given** the setup contains the application shell in the required browser.

**When** the manager opens each primary destination.

**Then** Overview, Maintenance, Import, and Debugging - Assumptions remain accessible. Labelled Language/Currency controls occupy the upper-right header. Keyboard access remains available.

Trace journey: US-02. Trace interface: UX-001.

<a id="ac-ux-002"></a>

### AC-UX-002: Search does not change reporting scope

Trace: See journey trace below | FR-006, FR-008 | SC-005 | AR-004 | E-UI, E-ROOM.

**Given** the setup contains room labels, property names, and a selected reporting scope.

**When** the manager searches rooms or property names.

**Then** visible room results match the search. Shared reporting scope and totals remain unchanged. No search result creates or edits records.

Trace journey: US-02. Trace interface: UX-002.

<a id="ac-ux-003"></a>

### AC-UX-003: Schematic Map and equivalent List

Trace: See journey trace below | FR-007, FR-009 | SC-005 | AR-004 | E-UI, E-ROOM.

**Given** the setup contains a prepared portfolio with Unknown and Healthy observations plus unresolved faults.

**When** the manager switches between Map and List.

**Then** Map is the default representation. Each room appears once with three observations and unresolved count. Both representations show equivalent room information. No physical position or combined condition is inferred.

Trace journey: US-02. Trace interface: UX-003.

<a id="ac-ux-004"></a>

### AC-UX-004: Operational overview precedes finance

Trace: See journey trace below | FR-007, FR-011, FR-014 | SC-003, SC-005 | AR-003, AR-004 | E-UI.

**Given** the setup contains a portfolio with observations, tickets, and financial values.

**When** the manager reviews Overview.

**Then** filters and labelled counts precede the room view. Unresolved maintenance follows that view. Finance/replacement follow operational content. Ticket links open the matching room.

Trace journey: US-02, US-05. Trace interface: UX-004.

<a id="ac-ux-005"></a>

### AC-UX-005: Room card selection and Log fault

Trace: See journey trace below | FR-009, FR-012, FR-015 | SC-004, SC-005 | AR-004, AR-005 | E-UI, E-ROOM, E-MAINT.

**Given** the setup contains two rooms visible in Map or List with a selected filter and scroll position.

**When** the manager selects each room, closes its card, or chooses Log fault.

**Then** the bordered desktop card shows the selected room. Closing retains filters, view mode, and central scroll. Log fault opens Maintenance for that room. Navigation alone saves no ticket.

Trace journey: US-02, US-04. Trace interface: UX-005.

Run selection, closing, and Log fault independently. Approved dirty-form and return details are required companion interaction checks.

<a id="ac-ux-006"></a>

### AC-UX-006: Maintenance entry points

Trace: See journey trace below | FR-012, FR-013, FR-015 | SC-004, SC-005 | AR-005 | E-UI, E-MAINT.

**Given** the setup contains an existing room and a valid new fault draft.

**When** the manager saves through Maintenance or the room-card handoff.

**Then** the on-demand creation card saves one Open ticket with a required typed recorder. Cancel saves nothing. The room-card handoff preselects its room. Ownership/progression follow required rules. Resolved tickets remain separate.

Trace journey: US-04. Trace interface: UX-006.

<a id="ac-ux-007"></a>

### AC-UX-007: Independent import presentation

Trace: See journey trace below | FR-001, FR-002, FR-003, FR-004, FR-015 | SC-001, SC-002 | AR-001, AR-002 | E-UI, E-IMPORT.

**Given** the setup contains an empty store for Assets, or prepared targets for Invoices.

**When** the user opens the selected import workflow.

**Then** upload, preview, explicit confirmation, and actual results remain distinct. Diagnostics and effects use the required count units. No paired upload or PDF path appears.

Trace journey: US-01. Trace interface: UX-007.

<a id="ac-ux-008"></a>

### AC-UX-008: Stale preview requires renewed confirmation

Trace: See journey trace below | FR-003, FR-005, FR-015 | SC-002 | AR-002 | E-UI, E-IMPORT.

**Given** the setup contains a reviewed preview whose effects change before confirmation.

**When** the user attempts confirmation.

**Then** the old confirmation saves no upload changes. Refreshed review and renewed confirmation are required. Failed commits display no successful counts.

Trace journey: US-01. Trace interface: UX-008.

<a id="ac-ux-009"></a>

### AC-UX-009: Inline observation editor

Trace: See journey trace below | FR-009, FR-016 | SC-004 | AR-004 | E-UI, E-ROOM.

**Given** the setup contains a room observation with optional note.

**When** the manager opens the editor.

**Then** state, date, recorder, note, Save, Cancel, and Clear remain accessible. Recorded states require date/recorder. Clear returns unassessed Unknown without history.

Trace journey: US-02. Trace interface: UX-009.

<a id="ac-ux-010"></a>

### AC-UX-010: Inline asset editor and evidence

Trace: See journey trace below | FR-010, FR-011, FR-019 | SC-003, SC-004 | AR-002, AR-003 | E-UI, E-ASSET.

**Given** the setup contains a room with three fixed assets and preserved source/history information.

**When** the manager opens an asset editor.

**Then** permitted fields and evidence are accessible within the room card. Identity and calculated values are read-only. Overrides use a separate paired form. No Add asset action appears.

Trace journey: US-03. Trace interface: UX-010.

<a id="ac-ux-011"></a>

### AC-UX-011: Override and reset information

Trace: See journey trace below | FR-019 | SC-003, SC-004 | AR-003 | E-UI, E-ASSET.

**Given** the setup contains an active override and known source values.

**When** the manager opens override or reset controls.

**Then** the paired override form requires reason and recorder. Reset displays the source values it restores. Successful reset retains history.

Trace journey: US-03. Trace interface: UX-011.

<a id="ac-ux-012"></a>

### AC-UX-012: Inline maintenance editor

Trace: See journey trace below | FR-012, FR-013 | SC-004 | AR-005 | E-UI, E-MAINT.

**Given** the setup contains an unresolved ticket or independently prepared Resolved ticket.

**When** the manager opens its editor.

**Then** unresolved editing uses the maintenance-card pattern with permitted fields, typed recorder, and progression. Fixed associations stay read-only. Resolved information/history remain read-only. Narrow layouts use the approved overlay.

Trace journey: US-04. Trace interface: UX-012.

<a id="ac-ux-013"></a>

### AC-UX-013: Empty and write-feedback states

Trace: See journey trace below | FR-003, FR-008, FR-015 | SC-002, SC-004, SC-005 | AR-002 | E-UI.

**Given** the setup contains a prepared first-use, filtered-empty, loading, invalid, warning-only, saving, success, or persistence-failure state.

**When** the user enters that state.

**Then** the interface names the state accurately. Only confirmed persistence produces success. Failed saves retain input. Empty results contain no stale records.

Trace journey: US-01, US-02, US-03. Trace interface: UX-013.

Run each state independently. Loading uses static feedback under the no-animation policy.

<a id="ac-ux-014"></a>

### AC-UX-014: Display and date boundaries

Trace: See journey trace below | FR-011, FR-014, FR-017, FR-018 | SC-003, SC-008 | AR-003, AR-004 | E-UI, E-FINANCE.

**Given** the setup contains prepared preferences, valid FX configuration, and current operational records.

**When** the user changes Language, Currency, or financial reporting date.

**Then** only the applicable interface or calculated display changes. Saved preferences persist independently. Current operational date remains explicit. Source information and ticket timestamps remain unchanged.

Trace journey: US-02, US-05. Trace interface: UX-014.

<a id="ac-ux-015"></a>

### AC-UX-015: Confirmed visual styling

Trace: See journey trace below | FR-007 | SC-005, SC-008 | AR-002 | E-UI.

**Given** the setup contains all essential views with normal, empty, invalid, and pending states.

**When** the reviewer inspects the interface in color and greyscale.

**Then** black/grey/white, pale beige, white panels, and bright blue primary actions match the confirmed palette. Labels and statuses remain readable. No shadows, gradients, fading, or animations appear.

Trace journey: US-02. Trace interface: UX-015.

<a id="ac-ux-016"></a>

### AC-UX-016: Required browser and responsive widths

Trace: See journey trace below | FR-009, FR-012, FR-017, FR-018 | SC-005, SC-008 | AR-002 | E-UI.

**Given** the setup contains a Windows laptop with Chrome and prepared long names and validation messages.

**When** the reviewer checks 1440px, 1024px, 768px, and 360px widths with room details open and closed.

**Then** navigation, header controls, Close, Log fault, and form actions remain reachable. Narrow layouts use stacked content and an explicit-close overlay. No unintended page overflow appears.

Trace journey: US-02, US-04. Trace interface: UX-016.

Record the actual Windows version, Chrome version, build, and test date. Numeric breakpoint choices are approved in UX-016.

<a id="ac-ux-017"></a>

### AC-UX-017: Keyboard and accessible feedback

Trace: See journey trace below | FR-009, FR-010, FR-012, FR-015 | SC-004, SC-005, SC-008 | AR-002 | E-UI.

**Given** the setup contains required-browser views with room selection, editing, and validation states.

**When** the reviewer uses keyboard-only navigation and checks accessible feedback.

**Then** inputs have labels and visible focus. Room selection and closing remain keyboard usable. Status meaning and feedback require neither hover nor color.

Trace journey: US-02, US-03, US-04. Trace interface: UX-017.

Specific focus destinations, Escape behavior, and overlay focus trapping are approved in UX-017. Record assistive-technology results without claiming unperformed checks.

<a id="ac-ux-018"></a>

### AC-UX-018: Integrated refresh and persistence

Trace: See journey trace below | FR-005, FR-015, FR-018, FR-019 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-UI, E-STARTUP.

**Given** the setup contains saved room, asset, ticket, and preference information plus a valid invoice update.

**When** the user applies the update and restarts normally.

**Then** affected room and financial results refresh. Saved records, evidence, histories, and preferences survive restart. The new session financial date is today. Undelivered behavior remains disclosed.

Trace journey: US-01, US-02, US-03, US-04, US-05. Trace interface: UX-018.

<a id="ac-ux-019"></a>

### AC-UX-019: Complete assumptions inventory

Trace: See journey trace below | FR-011, FR-014, FR-017, FR-018, FR-019 | SC-003, SC-008 | AR-003 | E-UI, E-FINANCE.

**Given** the setup contains complete, absent, or invalid FX configuration and any imported portfolio state.

**When** the user opens Debugging - Assumptions.

**Then** the UX-019 inventory matches product rules and actual configuration. Missing configuration is explicit. Rates are never fabricated. Opening the page changes no records or preferences.

Trace journey: US-03, US-05. Trace interface: UX-019.

Run each configuration state independently. Check USD rate integrity, numeric examples, unchanged rates across display settings, keyboard access, and narrow layouts. Approved technical details reference the governing technical design.

<a id="demo"></a>

## Demo

<a id="ac-demo-001"></a>

### AC-DEMO-001: Reset starts an empty rehearsal

Trace: See journey trace below | FR-015, FR-017, FR-018 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-STARTUP, E-DEMO.

**Given** the shared local store contains imported records, evidence, observations, tickets, overrides, and histories, plus saved browser preferences.

**When** the demonstrator confirms Reset data on Debugging - Assumptions.

**Then** the store is empty and its generation changes. Configuration and browser preferences remain. Old drafts/previews cannot save. Overview opens empty with today's financial reporting date.

Trace journeys: US-01, US-02, US-03, US-04, US-05.

<a id="ac-demo-002"></a>

### AC-DEMO-002: Restart retains selected rehearsal

Trace: See journey trace below | FR-015, FR-017, FR-018 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-STARTUP, E-DEMO.

**Given** the setup contains a selected rehearsal store with saved records, evidence, overrides, and histories.

**When** the demonstrator restarts the application with that store.

**Then** its saved state remains intact. Browser preferences persist. A newly opened browser-tab session uses actual Hong Kong today for financial reporting. Startup neither resets nor reseeds the store.

Trace journeys: US-01, US-02, US-03, US-04, US-05.

<a id="ac-demo-003"></a>

### AC-DEMO-003: Explicit financial example dates

Trace: See journey trace below | FR-015, FR-017, FR-018 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-STARTUP, E-DEMO.

**Given** the setup contains a new rehearsal session and prepared financial examples.

**When** the demonstrator selects 2026-07-14 or 2026-07-15 explicitly.

**Then** financial examples use the selected date. Operational date, ticket timestamps, and observations remain unchanged. No preset control is required.

Trace journeys: US-01, US-02, US-03, US-04, US-05.

<a id="ac-demo-004"></a>

### AC-DEMO-004: Timed walkthrough and disclosures

Trace: See journey trace below | FR-015, FR-017, FR-018 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-STARTUP, E-DEMO.

**Given** the setup contains an implemented build with recorded verification results and a shared demo store reset to empty.

**When** the demonstrator completes the planned walkthrough on a Windows laptop with Chrome.

**Then** the record includes elapsed time, build/date, actual browser version, completed steps, omissions, and evidence references. Completion requires at most twelve minutes. Missing manual creation and other unmet criteria remain disclosed.

Trace journeys: US-01, US-02, US-03, US-04, US-05.

<a id="ac-demo-005"></a>

### AC-DEMO-005: Clean startup evidence

Trace: See journey trace below | FR-015, FR-017, FR-018 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-STARTUP, E-DEMO.

**Given** the setup contains a clean local environment with the later documented application startup procedure.

**When** the reviewer executes that procedure.

**Then** the web application starts reproducibly. The record states environment, build/date, expected result, actual result, and status. A title-printing scaffold does not pass.

Trace journeys: US-01, US-02, US-03, US-04, US-05.



<a id="infrastructure"></a>

## Infrastructure

<a id="ac-infra-001"></a>

### AC-INFRA-001: Stale record saves

Trace: US-03, US-04 | FR-010, FR-012, FR-015 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-ASSET, E-MAINT.

**Given** Two tabs hold the same asset or unresolved-ticket version.

**When** One tab saves, then the other submits its previous version.

**Then** The second save returns STALE_RECORD without writes/history. Its draft and latest saved values remain available for explicit review.

<a id="ac-infra-002"></a>

### AC-INFRA-002: Duplicate maintenance submission

Trace: US-04 | FR-012, FR-015 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-MAINT.

**Given** A valid creation card has one submission ID and generation.

**When** The same creation request is submitted twice, including a lost-response retry after restart.

**Then** Exactly one Open ticket and one CREATE event exist. Both requests return the original result. Changed payload under the same ID conflicts.

<a id="ac-infra-003"></a>

### AC-INFRA-003: Obsolete browser response

Trace: US-02 | FR-008, FR-009 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-ROOM, E-UI.

**Given** Room A and room B reads can complete in reverse order.

**When** The user selects A, then B, and A responds last.

**Then** The card still displays B. Old errors/results cannot replace its current context.

<a id="ac-infra-004"></a>

### AC-INFRA-004: Reset cancellation and rollback

Trace: US-01, US-04 | FR-015 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-STARTUP.

**Given** The store contains baselines, invoices, observations, maintenance, overrides, receipts, and histories.

**When** The user cancels reset, or confirms with an injected failure halfway through deletion.

**Then** All saved records and generation remain unchanged. Cancellation performs no command. Failure reports no success and leaves reset retry available.

<a id="ac-infra-005"></a>

### AC-INFRA-005: Reset invalidates other tabs

Trace: US-01, US-03, US-04 | FR-005, FR-015, FR-018 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-STARTUP, E-UI.

**Given** Another tab has unsaved edits and an import preview from the current generation.

**When** Reset commits, then the other tab submits its old draft or confirmation.

**Then** STALE_STORE prevents every write. On focus/request, the other tab identifies its old draft as invalid and requires discard. Preferences remain.

<a id="ac-infra-006"></a>

### AC-INFRA-006: Reset response-loss retry

Trace: US-01 | FR-015 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-STARTUP.

**Given** Reset succeeded and a new-generation baseline was then imported.

**When** The previous reset request is retried with its old generation.

**Then** The retry returns STALE_STORE and preserves the newly imported portfolio.

<a id="ac-infra-007"></a>

### AC-INFRA-007: Preview lifetime and confirmation retry

Trace: US-01 | FR-003, FR-005, FR-015 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-IMPORT, E-STARTUP.

**Given** An unconfirmed preview expires or the process restarts. Separately, a confirmed import has a durable receipt.

**When** The old unconfirmed preview is submitted, or the identical committed command is retried after restart.

**Then** Expired/missing preview requires renewed upload/review with no domain writes. A committed retry returns its receipt without replaying effects.

<a id="ac-infra-008"></a>

### AC-INFRA-008: Database busy and atomic history

Trace: US-01, US-03, US-04 | FR-015, FR-019 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-IMPORT, E-MAINT, E-ASSET.

**Given** A write lock exceeds five seconds. Separately, a save fails after its entity write but before its history/receipt.

**When** The user confirms an import or saves a valid maintenance/override change.

**Then** Lock timeout returns STORE_BUSY and preserves input. Injected failure rolls back entity, history, and receipt together. No success is displayed.

<a id="ac-infra-009"></a>

### AC-INFRA-009: Required maintenance recorder

Trace: US-04 | FR-012, FR-013 | SC-004, SC-007, SC-008 | AR-002, AR-006 | E-MAINT.

**Given** Creation, editing, start, and resolve drafts have valid business prerequisites.

**When** The user submits each action with a blank recorder, then with a non-empty typed recorder.

**Then** Blank recorders block all writes. Valid actions record their self-declared recorder separately from the assigned owner.

Application status for every scenario: **NOT RUN**. Documentation checks do not change this status.

# UI/UX specification: Hotel asset-management prototype

Version: 0.3

Created / revised: 2026-10-03

Owner: Alex

Target delivery: 2026-10-05

Status: Requirements defined. Proposed interactions remain pending. Application verification: NOT RUN.

This document complements [product specification v0.4](product-spec.md). [Data contracts](data-contracts.md) contain proposed technical interfaces.
[Assessment requirements](assessment-requirements.md) preserve external obligations. Use the [shared glossary](glossary.md) for terms.

## 1. Authority and context

- **Inherited:** A requirement already defined by the product specification.
- **Confirmed:** A layout or styling choice that Alex confirmed.
- **Proposed:** A supporting detail without owner approval.

Alex reconfirmed the existing Confirmed choices on 2026-10-03 in this specification-readiness planning conversation.
The implementation request approves documentation changes, not all Proposed details. Owner approval does not establish client acceptance or passing tests.

Required context: Windows laptop with Chrome. Record the actual Windows version, Chrome version, build, and test date.
Retain responsive checks at 1440px, 1024px, 768px, and 360px. Other browsers are not additional mandatory targets.

The application remains a title-printing scaffold. No UI, screenshot, fixture, or application result exists.
Manual asset creation remains excluded and leaves part of AR-002 unmet.
No property/room forms, observation history, authentication, geographic coordinates, or floor-plan data are added.
Framework, APIs, database design, deployment, and detailed wireframes remain outside this revision.

## 2. Styling and layout

The desktop shell has left navigation and a flexible central workspace. A selected room opens a bordered right-side card.
Overview offers schematic Map and List representations. The map groups rooms by property, not physical room position.
Maintenance, Import, and Debugging - Assumptions replace the central workspace.
Language and Currency controls occupy the upper-right header on every page.

Use black, grey, and white as the main palette. Use a pale beige background and white panels.
Use bright blue for primary actions. Use neutral outlines or text for secondary actions.
Use a system sans-serif font. Keep text readable, spacing consistent, borders restrained, and numeric columns aligned.

Do not use shadows, gradients, fading, or animated transitions.

Status text or icons distinguish Healthy, Attention needed, Critical, and Unknown. Meaning must not depend on color.
On narrow screens, navigation becomes compact and content stacks. Room details use an overlay with an explicit Close action.
Wide tables scroll inside labelled containers. Controls remain usable at 360px.

Numeric layout and font defaults remain Proposed under UX-015 and UX-016.

## 3. Essential views

| View | Required purpose |
|---|---|
| Overview | Shared filters, operational counts, central room view, unresolved maintenance, then supporting reports. |
| Map | Clickable rooms grouped by property. Each room shows three observations and unresolved-ticket count. |
| List | The same room context and observations, with room-selection actions. |
| Room card | Property/room context, three assets, three observations, separate ticket groups, nested editors, and Log fault. |
| Maintenance | Fault logging, ownership, progress, unresolved/resolved views, room links, and inline editors. |
| Import | Independent workflow selection, upload, preview, explicit confirmation, diagnostics, and actual results. |
| Debugging - Assumptions | Product rules, calculation assumptions, actual configuration, and identified technical proposals. |

Editors remain nested views, not extra primary destinations. Financial and replacement results remain supporting Overview sections.
Source/history inspection belongs with the selected asset or ticket.

## 4. Requirements and proposal checks

Required Given/When/Then checks are in [confirmed UI acceptance](acceptance-scenarios.md#confirmed-ui).
They cover only Inherited and Confirmed behavior. Proposed checks below remain pending design choices.
All application checks are NOT RUN.

### UX-001: Application shell and navigation

**Confirmed:** Left navigation contains Overview, Maintenance, Import, and Debugging - Assumptions.
Labelled Language/Currency controls occupy the upper-right header on every page.

**Inherited:** US-02, FR-017, FR-018, SC-008.

**Proposed:** Overview is the initial destination. Text and outline identify the active destination.
Navigation retains filters and session reporting date. Destination changes close the room card.
Unsaved forms require explicit discard or continued editing before navigation.

Proposal check: Check active navigation, retained context, and explicit handling of unsaved forms.

Required check: [AC-UX-001](acceptance-scenarios.md#ac-ux-001).

### UX-002: Shared filters and room search

**Inherited:** US-02, FR-006, FR-008, SC-005. Shared filters apply to every reporting output.
Parent changes clear incompatible children. Empty scope shows no stale records.

**Confirmed:** Search room labels and property names without changing reporting scope.

**Proposed:** Search uses case-insensitive substrings and narrows visible rooms only.
Use the label “Search rooms (view only)”. Retain search between Map and List.
Keep totals and portfolio maintenance unaffected by search.

Proposal check: Compare Map/List search results. Check separate search-empty and filter-empty feedback.
Clear search must restore visible rooms without changing reporting filters.

Required checks: [AC-UX-002](acceptance-scenarios.md#ac-ux-002) and [US-02](acceptance-scenarios.md#us-02).

### UX-003: Central Map/List overview

**Confirmed:** Map is the default. Label both controls and expose the current representation.
Use “Schematic room map” for property-grouped tiles. Do not imply physical positions or floors.

**Inherited:** US-02, FR-009. Each representation shows the same three observations and unresolved-ticket count.

**Proposed:** Retain the representation for the session. Sort properties and room labels consistently, using identities for ties.
Retain selected room and search across representation changes.

Proposal check: Check retained scope, search, selection, and totals across Map/List changes.

Required check: [AC-UX-003](acceptance-scenarios.md#ac-ux-003).

### UX-004: Operational summaries and supporting reports

**Confirmed:** Overview orders filters, labelled counts, central rooms, unresolved maintenance, then finance/replacement.
Observation counts distinguish system/state. Entity and ticket counts name their units.
Every maintenance row links to its room. Finance counts each asset value once.

**Inherited:** US-02, US-05, FR-007, FR-011, FR-014, SC-003, SC-005, SC-008.

Required checks: [AC-UX-004](acceptance-scenarios.md#ac-ux-004) and [unique counts](acceptance-scenarios.md#ac-us02-006).

### UX-005: Right-side room card and return context

**Confirmed:** Selecting a room in Map or List opens a bordered card on the right.
The desktop central workspace narrows. Another room selection updates the card.
Closing retains filters, representation, and central scroll position. Log fault opens Maintenance for that room.

**Inherited:** US-02, US-03, US-04, FR-009, FR-010, FR-016.
The card shows property, observations, assets, separate ticket groups, nested editors, and source/history evidence.

**Proposed:** Keep the heading and Close action visible. Retain selected room across Map/List changes.
Protect unsaved forms before switching rooms or closing. Close excluded room cards after filter changes with the same protection.

Proposed Log fault details:

- Display the preselected room clearly.
- Leave the optional asset unselected initially.
- Focus the description field.
- Protect unsaved forms before navigation.
- Retain filters, representation, search, room selection, and scroll for return.
- Cancel the draft without saving a ticket.
- Return Cancel to the originating card.
- After Save, display the new ticket in Maintenance.
- Refresh counts when returning to Overview.

Opening a draft alone does not persist a ticket under FR-015.

Proposal check: Check unsaved-form protection, selected-room retention, excluded-card closure, and complete return context.

Required check: [AC-UX-005](acceptance-scenarios.md#ac-ux-005).

### UX-006: Maintenance destination

**Confirmed:** Maintenance supports fault logging, ownership, and progress.
It has unresolved/resolved views and room links using the same card.
The room-card action opens a room-preselected fault form.

**Inherited:** US-04, FR-012, FR-013, SC-004, SC-005. Required sorting uses actual operational date.

**Proposed:** Start with unresolved tickets. Show owner, target, room, asset link, severity, and status.
Use “Unassigned”, “No target date”, and “Room only” where appropriate.
Maintenance's Log fault action uses the same inline creation form.
The form selects an existing room and optional same-room asset.
Creation exposes description, severity, optional owner, and optional target date.

Proposal check: Check both form entries, field presentation, cancelled drafts, and prevention of duplicate submissions.

Required checks: [AC-UX-006](acceptance-scenarios.md#ac-ux-006) and [maintenance scenarios](acceptance-scenarios.md#us-04).

### UX-007: Import workflow and diagnostics

**Confirmed:** Select one workflow, upload, inspect preview, confirm, then inspect actual results.
Show source coordinates when available, actionable reasons, blockers, warnings, and distinct counts.
Invoice previews show six-field changes and override clearing. Do not add paired uploads or PDF paths.

**Inherited:** US-01, FR-001–FR-005, FR-015, FR-019, SC-001, SC-002.

**Proposed:** Keep the selected file/workflow visible throughout review. Hide or disable confirmation when blockers exist.
Explain that warnings permit confirmation and blockers reject the whole upload.
Explain invoice prerequisites before baseline creation. File/workflow changes invalidate the previous preview.

Proposal check: Check workflow changes, cancelled previews, and visible confirmation availability.

Required check: [AC-UX-007](acceptance-scenarios.md#ac-ux-007).

### UX-008: Import confirmation and results

**Confirmed:** Changed stale previews require refreshed review and renewed confirmation.

**Inherited:** US-01, FR-003, FR-005, FR-015, SC-002.

**Proposed:** Prevent duplicate submissions while confirming. Retain the reviewed summary.
Retain upload and diagnostics after failure for retry. Refresh affected views only after a successful commit.

Proposal check: Check pending submission controls and retry presentation.

Required checks: [AC-UX-008](acceptance-scenarios.md#ac-ux-008) and [rollback](acceptance-scenarios.md#ac-us01-020).

### UX-009: Observation editor

**Confirmed:** Inline forms expose state, date, recorder, note, Save, Cancel, and Clear.
Recorded states require date/recorder, including recorded Unknown. Clear removes metadata and returns unassessed Unknown.
No observation history is added.

**Inherited:** US-02, FR-009, FR-016, SC-004, SC-005.

**Proposed:** Separate Clear from Save. Explain Clear before explicit confirmation.
Distinguish “Unknown — not assessed” from recorded Unknown with metadata.

Proposal check: Check distinct Unknown presentation and explicit Clear confirmation.

Required check: [AC-UX-009](acceptance-scenarios.md#ac-ux-009).

### UX-010: Asset editor and source evidence

**Confirmed:** Nested inline editors expose name, purchase/installation dates, and useful life.
Identity, room, category, and calculated results are read-only. Cost/currency corrections use a separate paired override form.
Evidence sections show original baseline, invoices, provenance, and applied before/after history. No Add asset action exists.

**Inherited:** US-03, FR-010, FR-011, FR-019, SC-003, SC-004.

**Proposed:** Label source, current operational, and effective values separately.
Explain purchase fallback. Separate historical-only evidence from applied-update events.

Proposal check: Check source/current/effective labels and evidence presentation.

Required check: [AC-UX-010](acceptance-scenarios.md#ac-ux-010).

### UX-011: Financial override and reset

**Confirmed:** The paired override form requires reason and recorder. Reset displays the source values and retains history.

**Inherited:** US-03, FR-019, SC-003, SC-004. Reset requires reason/recorder under the operational contract.

**Proposed:** Use “Apply financial override” and “Reset to source”. Identify the latest applied invoice or baseline as reset source.
Show current/source/effective pairs. Explain that reset does not restore names, dates, or observations.

Proposal check: Check action labels and explicit reset-source explanation.

Required check: [AC-UX-011](acceptance-scenarios.md#ac-ux-011).

### UX-012: Ticket editor and history

**Confirmed:** Inline forms expose description, severity, owner, target date, and permitted progression.
Associations remain fixed after creation. Owner and resolution-note requirements apply.
Resolved tickets remain read-only with chronological history.

**Inherited:** US-04, FR-012, FR-013, SC-004.

**Proposed:** Use “Start work” and “Resolve”, not an unrestricted status selector.
Explain unavailable actions beside prerequisites. Show the resolution note with Resolve.
Keep Save/Cancel for editable fields. Owner removal follows the existing Open-only rule.

Proposal check: Check action wording, prerequisites, and resolution-note presentation.

Required check: [AC-UX-012](acceptance-scenarios.md#ac-ux-012).

### UX-013: Empty, loading, and write-feedback states

**Confirmed:** Define first-use, filtered-empty, loading, validation failure, blocked upload, warning-only preview, saving, success, and persistence failure.
Failed saves retain input. Success requires confirmed persistence.

**Inherited:** US-01–US-03, FR-003, FR-008, FR-015, SC-002, SC-004, SC-005.

**Proposed:** Use these presentations:

| State | Proposed presentation |
|---|---|
| No imported data | Explain baseline initialization and offer Import Assets. Show honest zero counts. |
| Filter/search empty | Explain the cause. Offer Clear filters or Clear room search. |
| Loading | Show static text or progress, not stale information as current. |
| Invalid/blocked | Show field errors and a summary. Preserve input for correction. |
| Warning-only | Keep warnings visible and explain confirmation availability. |
| Saving | Show static pending feedback. Prevent duplicate submissions. |
| Success | Announce after persistence. Refresh affected information. |
| Persistence failure | Explain that nothing saved. Retain the draft/upload for retry. |

Proposal check: Check presentation and accessible feedback for every state.

Required check: [AC-UX-013](acceptance-scenarios.md#ac-ux-013).

### UX-014: Language, currency, and date boundaries

**Confirmed:** Upper-right controls, English/USD defaults, independent persistent preferences, conditional translations, and English fallback apply.
Local totals remain grouped. Source/user text stays unchanged. Financial and operational dates have separate labels.

**Inherited:** US-02, US-05, FR-011, FR-014, FR-017, FR-018, SC-003, SC-008.

**Proposed:** Offer only delivered language sets. Label modes “USD” and “Local transaction currency”.
Place the session reporting date at the start of supporting financial sections.
Offer custom date and Reset to today. Show timezone offsets with actual history timestamps.
Demo presets remain optional proposals.

Display the fixed FX date and fictional-rate disclaimer. Invalid configuration requires correction without partial or fabricated totals.
Label spending as acquisition-cost proxies and replacement dates as planning assumptions.

Proposal check: Check control labels, date placement, and actual timestamp presentation.

Required check: [AC-UX-014](acceptance-scenarios.md#ac-ux-014).

### UX-015: Styling and primary actions

**Confirmed:** Apply the palette, typography, spacing, borders, numeric alignment, and prohibited effects in section 2.

**Proposed:** Use a 16px base font and an 8px spacing rhythm.
Use readable white text on blue primary buttons. Keep clearing actions separate from Save with explicit neutral wording.

Proposal check: Check numeric styling defaults and clearing-action placement.

Required check: [AC-UX-015](acceptance-scenarios.md#ac-ux-015).

### UX-016: Desktop and narrow layouts

**Confirmed:** The desktop card narrows central space. Narrow layouts use compact navigation, stacked forms, and an explicit-close overlay.
Usability extends to 360px.

**Proposed:** At 1200px and above, use 200px left navigation and an approximately 400px right card.
Below 1200px, use compact top navigation and a bounded overlay.
At 600px and below, use a full-width overlay and stacked fields.
Keep card heading, Close, and Log fault reachable. Scroll wide tables inside labelled containers.
Header controls may wrap at narrow widths without disappearing. Overlay Log fault honors the proposed unsaved-form protection.

Proposal check: Check proposed breakpoints and control wrapping with long names and errors.

Required check: [AC-UX-016](acceptance-scenarios.md#ac-ux-016).

### UX-017: Keyboard, focus, and feedback

**Confirmed:** Inputs have labels and visible focus. Statuses include text. Room selection and closing support keyboard use.
Feedback remains accessible. No action requires hover or color interpretation.

**Proposed:** Use semantic headings, controls, tables, and labels. Expose selected and expanded states.
Announce results and associate errors with inputs. Focus the first invalid field.
Opening cards focuses their heading. Close restores trigger focus or a suitable heading.
Only narrow overlays trap focus and deactivate background content. Escape uses the proposed unsaved-form protection.
Desktop cards permit access to the central workspace.

Proposal check: Check focus destinations, announcements, Escape, and overlay focus boundaries with assistive technology.

Required check: [AC-UX-017](acceptance-scenarios.md#ac-ux-017).

### UX-018: Integrated journey and persistence

**Confirmed:** Map/List, room context, maintenance navigation, cancellation, import states, keyboard access, responsive layouts, and display boundaries require verification.

**Inherited:** US-01–US-05, SC-002–SC-005, SC-008, AR-002, AR-004–AR-006.
New isolated rehearsal stores follow D-019. Normal restart retains successful state in the selected store.
Browser preferences remain independent of store selection. A new session reporting date starts at actual Hong Kong today.

**Proposed:** Use the integrated sequence in [the demo](demo.md). Preserve proposed complete return context between Overview and Maintenance.

Proposal check: Check complete return context and sequence timing.

Required checks: [AC-UX-018](acceptance-scenarios.md#ac-ux-018) and [demo scenarios](acceptance-scenarios.md#demo).

### UX-019: Debugging - Assumptions

**Confirmed:** This navigation page lists all assumptions, including depreciation math and FX rates.

**Inherited:** Product sections 3–4, 7–10, 13, and 15. US-03, US-05, FR-011, FR-014, FR-017–FR-019, SC-003, SC-008.

**Proposed:** Use read-only sections with source references. Separate approved rules, loaded configuration, and technical/display proposals.
Allow access before imports and during invalid financial configuration. Do not add editable configuration or application logs.

Required inventory:

| Group | Content |
|---|---|
| Service anchor and clock | Current installation or purchase fallback. Actual Hong Kong operational date and separate session reporting date. No historical portfolio reconstruction. |
| Depreciation | Straight-line, zero residual, whole completed months, original-day clamping, and life cap. Formulae and all product numerical/calendar examples. |
| Effective values | Override pair, latest applied invoice pair, or baseline pair. Edited operational values continue until a newer applied invoice. Reset/history boundaries. |
| Replacement | Service anchor plus life. Overdue/today/90-day categories and twelve-month endpoint. Separate spending proxies without book-value subtraction or price predictions. |
| FX | Actual HKD, SGD, GBP, JPY, and USD rates. USD per source unit. USD equals 1. Fixed date and fictional disclaimer. |
| Missing configuration | Not configured or explicit invalid-rate diagnostics. No fabricated rates or incomplete financial totals. |
| Money and aggregation | Unrounded calculation/aggregation and two-decimal USD display. Grouped local totals and unique-asset valuation. JPY display precision remains Proposed. |
| Import model | Independent prescribed workbooks, exactly three categories, preview without writes, blockers, warnings, confirmed atomic commit, and stale-preview recheck. |
| Invoice precedence | Maximum invoice date, historical-only evidence, controlling-date conflicts, equivalent ties, identical skips, changed-source conflicts, and applied update history. |
| Conditions and links | Independent latest observations, Unknown meanings, required metadata, Clear, no observation history, and explicit ticket links. Schematic map limits. |
| Maintenance | Fictional owners, attribution limits, required owner in progress, forward-only statuses, resolution note/time, fixed links, sorting, and history. |
| Languages | English mandatory, other named sets stretch, fallback, unchanged stored text, independent persistent preferences, and pending linguistic review. |
| Prototype and persistence | Fictional sample coverage, exclusions, AR-002 gap, normal restart, isolated rehearsal stores, and any future hosting limits. |
| Technical proposals | Proposed parsing, identifiers, history representation, local precision, and layout defaults. |

Show the loaded fictional owner configuration when available. Show Not configured otherwise.
Changing Currency does not change displayed source-to-USD rates. Update this inventory when source rules or actual configuration change.
Presentation must use the same calculation rules as services. Do not maintain a conflicting calculation model in views.

Proposal check: Check read-only grouping, source references, and access before imports or during configuration failure.

Required check: [AC-UX-019](acceptance-scenarios.md#ac-ux-019).

## 5. Verification and evidence status

| Coverage | Evidence groups | Status |
|---|---|---|
| UX-001–UX-005 | E-ROOM, E-UI | NOT RUN |
| UX-006, UX-012 | E-MAINT, E-ROOM, E-UI | NOT RUN |
| UX-007–UX-008 | E-IMPORT, E-UI | NOT RUN |
| UX-009–UX-011 | E-ROOM, E-ASSET, E-FINANCE, E-UI | NOT RUN |
| UX-013–UX-017 | E-UI and applicable workflow group | NOT RUN. Linguistic review pending. |
| UX-018 | E-DEMO, E-STARTUP, workflow groups | NOT RUN |
| UX-019 | E-UI, E-FINANCE | NOT RUN |

Record actual method, environment, build/date, expected result, actual result, and status in [the evidence ledger](assessment-requirements.md#5-evidence-ledger).
Documentation checks establish link, identifier, writing, and requirement consistency only.
They do not establish application, accessibility, startup, fixture, or rehearsal results.

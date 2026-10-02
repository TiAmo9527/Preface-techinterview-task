# UI/UX specification: Hotel asset-management prototype

Version: 0.2

Created / revised: 2026-10-03

Owner: Alex

Target delivery: 2026-10-05

Status: **Proposed; not implemented or verified**

This is a complementary interface specification for the [product specification v0.3](product-spec.md). It records existing requirements, user-confirmed design choices and proposed interaction details. The [data contracts](data-contracts.md) govern the existing input/logical interfaces; [assessment requirements](assessment-requirements.md) preserve external obligations and pending evidence.

## 1. Review findings, authority and boundaries

Existing UI/UX requirements are present in US-01–05, FR-006–010/012–018, product sections 7–10/13 and SC-002/004/005/008: independent import preview/confirmation, maintenance-first presentation, shared filters, room drill-down, permitted edits, actionable feedback, empty states, language/currency preferences and separate financial/operational dates. The [demo](demo.md) also proposes financial date presets; the contracts specify display and diagnostic boundaries.

Missing detail included screen organization, Map/List behavior, room-detail presentation, visual styling, keyboard/focus handling, responsive layout and explicit interaction states. There is no implemented UI to assess: app.py only prints a title.

Each UX group distinguishes these origins:

- **Inherited:** behavior already required by the referenced US/FR/SC IDs. Product rules remain authoritative; do not silently change them through interface choices.
- **Confirmed:** layout/styling choices Alex confirmed on 2026-10-03 and included in the requested documentation plan. This confirmation is not client approval or execution evidence.
- **Proposed:** supporting interaction details and defaults below. Writing them down does not establish owner approval of every detail.

This document does not alter the product's v0.3 approval record. Preserve AR-002's unmet manual asset-creation obligation: no Add asset action is introduced. No property/room editing, observation history, ticket deletion/reopening, authentication, geographic coordinates or floor-plan data is added. Framework, APIs, schemas, fixtures, deployment, screenshots, detailed wireframes and a full design-token system remain outside this revision.

## 2. Brief styling and layout

The desktop shell has a left navigation bar, a flexible central workspace and a bordered right-side room card when a room is selected. Overview's central workspace switches between a schematic room map and a list. The map groups clickable rooms by property; it represents logical grouping, never physical room placement. Maintenance, Import and Debugging - Assumptions replace the central workspace with their respective functions. Two labelled dropdowns, Language and Currency, sit in the upper-right header on every page. The Overview room card includes a bright primary "Log fault" button that opens Maintenance with a new fault form for that room.

Use black, grey and white as the main spectrum, a pale beige page background and white panels. Bright blue identifies primary actions; secondary actions use neutral outlines or text. Use a system sans-serif font, readable dark text, consistent spacing, restrained borders and aligned numeric columns. No shadows, gradients, fading effects or animated transitions. Status text/icons distinguish Healthy, Attention needed, Critical and Unknown without relying on color.

On narrow screens, navigation becomes compact, panels/forms stack and room details use an overlay with an explicit Close action. Wide tables scroll inside labelled containers; page content and primary controls remain usable down to 360px. Proposed numeric layout defaults are specified under UX-015/016 rather than a full visual system.

## 3. Essential screens and views

| Screen or view | Purpose and essential content |
|---|---|
| Overview | Shared location/property/room filters; labelled operational counts; central Map/List room view; prioritized unresolved maintenance; secondary financial and replacement sections. |
| Room map | Clickable room tiles grouped by property, labelled "Schematic room map"; each tile shows room label, three separately labelled observations and unresolved ticket count. |
| Room list | Property/room identity, the same three observations and ticket count, and room-selection action. Search room labels or property names without changing shared reporting scope. |
| Room detail card | Room/property context, three observations, three fixed assets and separate unresolved/resolved tickets; nested editors and source/history sections; "Log fault" opens a new item form on Maintenance for this room. |
| Maintenance | Let managers log faults, assign an owner and update maintenance progress. Show the shared-scope unresolved list in product priority order, separate resolved view, room links opening the same room card, and inline fault creation/editing. |
| Import | Independent Assets or Invoices selection, upload, validation/preview, explicit confirmation and actual result; diagnostics, distinct counts, before/after invoice values and override effects. |
| Debugging - Assumptions | Read-only listing of all product/calculation assumptions and relevant configuration, including depreciation math, effective-cost rules, replacement windows, actual configured fictional FX rates/date, operational clock and prototype limits. Distinguish approved rules, configuration and proposals. |

Observation, asset and ticket editors are nested views, not extra primary navigation destinations. Financial reporting and replacement remain supporting sections in Overview; source/history inspection belongs with the selected asset or ticket.

## 4. Requirements and future acceptance checks

All checks below are **NOT RUN**. They specify later application verification, not documentation test results. See section 5 for evidence mapping.

### UX-001: Application shell and navigation

**Confirmed:** Left navigation contains Overview, Maintenance, Import and Debugging - Assumptions. Two labelled dropdowns, Language and Currency, occupy the upper-right header on every page. **Inherited:** US-02; FR-017/018. **Proposed:** Overview is the initial destination. Show the active destination in text and outline/emphasis. Keep shared filters and session financial date when navigating; close the room card on destination changes. If an editor has unsaved changes, require explicit discard or continued editing before leaving.

**Acceptance:** Navigate among all four functions using pointer and keyboard. The active function is clear, both upper-right dropdowns stay accessible, saved filter/date context survives, and leaving a dirty editor does not silently discard entries.

### UX-002: Shared filters and room-search scope

**Inherited:** US-02; FR-006/008; SC-005. Location → property → room filters apply consistently to operational counts, maintenance and financial/replacement outputs. Changing a parent clears incompatible children; empty scope shows no stale records. **Confirmed:** Search room labels/property names without changing shared reporting scope. **Proposed:** Case-insensitive substring search narrows only visible room tiles/list rows; label it "Search rooms (view only)". It does not alter totals or the portfolio maintenance table. Carry the search between Map/List modes.

**Acceptance:** Changing location clears incompatible property/room selections and updates all scoped outputs. Search gives equivalent Map/List room sets while totals remain unchanged; distinguish search-empty from filter-empty states. Clear search restores all rooms in the selected scope.

### UX-003: Central Map/List overview

**Confirmed:** Default to Map; provide clearly labelled Map/List controls with the current choice exposed. Use room tiles grouped by property under "Schematic room map"; no physical placement is implied. **Inherited:** US-02; FR-009. Both modes show the same three individual observations and unresolved ticket count. **Proposed:** Keep the selected mode for the session. Group properties and order room labels consistently in both modes, using IDs to break equal-label ties. Do not infer floors or combine three observations into an invented room condition.

**Acceptance:** Switching modes changes representation without changing scope, search, totals or selected room. Each room appears once. Unknown is visible, and a Healthy observation can coexist with unresolved maintenance.

### UX-004: Operational summaries and supporting reports

**Inherited:** US-02/05; FR-007/011/014; SC-003/005/008. **Confirmed:** Overview orders shared filters, labelled operational counts, central room view, prioritized unresolved maintenance, then finance/replacement. Observation summaries distinguish system/state; entity and ticket counts name their units. Every maintenance row links to its room. Finance sums each asset once, independently of ticket rows; local totals remain grouped by currency.

**Acceptance:** Two tickets on one asset count as two tickets without doubling its value. A room-only critical ticket does not mark all its assets critical. Financial/replacement sections follow operational content and use the same reporting filters.

### UX-005: Right-side room card and return context

**Confirmed:** Clicking a room in either mode opens a bordered card on the right and narrows the desktop central workspace. Another room selection updates the card. Closing preserves filters, view mode and central scroll position. **Inherited:** US-02/03/04; FR-009/010/016. The card contains room/property context, three observations, three assets and separate unresolved/resolved tickets, with nested inline editors/evidence. **Proposed:** Show a persistent heading and Close action; preserve the room selection through Map/List switching. Prevent silent loss of dirty forms before switching rooms or closing. Close the card if a filter change excludes its room, subject to the same dirty-form guard.

**Confirmed:** The Overview room card has a "Log fault" button leading to Maintenance and its new fault form. **Proposed:** Preselect and clearly display the selected room; leave the optional asset unselected so this starts as a room-only fault unless the manager explicitly links one of that room's three assets. Focus the description field, apply the existing dirty-form guard before navigation and retain Overview's filters, Map/List choice, search, selected room and scroll position for return. Navigation opens an unsaved draft, not a persisted ticket; only a valid Save creates the new Open item. Cancel creates nothing and returns to the originating Overview room card. After Save, show the created item in Maintenance; returning to Overview refreshes counts and retains context.

**Acceptance:** Select two rooms in succession and verify all details update together. Close and return to the unchanged central view. Filter out the selected room and verify no out-of-scope card remains. Unsaved edits require an explicit choice before dismissal. From either Map or List, Log fault opens Maintenance for the correct room; navigation/Cancel creates no ticket, valid Save creates exactly one Open item, and return restores the originating card/context with refreshed counts.

### UX-006: Maintenance destination

**Confirmed:** Maintenance lets managers log faults, assign an owner and update maintenance progress. It is a primary left-navigation function, with unresolved/resolved views and room links using the same card. The Overview room-card Log fault action navigates here with the room preselected. **Inherited:** US-04; FR-012/013; SC-004/005. Unresolved tickets sort Critical → Medium → Low, then overdue target dates, then oldest opening timestamp. Overdue uses the actual Hong Kong date, not financial reporting date. **Proposed:** Start with unresolved tickets; show owner or "Unassigned", target date or "No target date", room, linked asset or "Room only", severity and status. Maintenance's own "Log fault" button opens an inline form selecting an existing room and optional same-room asset; the room-card entry uses the same form. Include description, severity, optional owner and optional target date at creation. Managers assign/reassign owners while unresolved and use Start work/Resolve to update progress under UX-012. New items start Open, and only Save persists them.

**Acceptance:** Both entry points create Open tickets with valid associations after Save. Assign an owner, progress Open → In progress → Resolved with a resolution note, and inspect persistent history. Cancelled/invalid drafts create nothing; duplicate submission is prevented. Room links show the corresponding room card. Resolved tickets appear separately and remain read-only. Shared filter changes update the list without stale rows.

### UX-007: Import workflow and diagnostics

**Inherited:** US-01; FR-001–005/015/019; SC-001/002. **Confirmed:** Select Assets baseline or Invoices update → upload → validate/preview → confirm → actual result. Show file/sheet/row/field diagnostics when available, actionable reasons, separate blockers/warnings, baseline entity inserts, distinct asset updates, invoice items, historical-only items and skips. Invoice preview shows six-field before/after values and override-clearing effects. No paired upload, PDF attachment or extra source type is introduced.

**Proposed:** Show selected workflow and file throughout review; hide or disable confirmation until preview is blocker-free. Explain that any blocker prevents the entire batch. Permit confirmation with visible non-blocking warnings. Before an initial baseline, explain that Invoices requires existing room/category targets. Selecting another file or workflow invalidates the previous preview; cancelling abandons it without writes.

**Acceptance:** Preview invalid Assets on empty state and invalid Invoices after valid baseline; both show coordinates and no writes. Valid baseline works without invoices. A warning-only valid upload can be confirmed, and historical-only/skipped items never appear as asset updates.

### UX-008: Import confirmation, stale previews and results

**Inherited:** US-01; FR-003/005/015; SC-002. **Confirmed:** Changed stale previews require refreshed review and renewed confirmation. **Proposed:** While confirming, prevent duplicate submission and retain the reviewed summary. If revalidation changes the proposed outcome, stop before committing and show the refreshed preview or new blockers. Display actual committed counts only after successful atomic persistence. On failure, show rollback/failure feedback and retain the upload/diagnostics for retry; do not display success or partial-commit counts.

**Acceptance:** A stale preview with changed effects cannot commit using earlier consent. Failed commits leave evidence, assets and histories unchanged. Successful imports refresh all affected views. No-op identical repeats report skips without replaying edits.

### UX-009: Observation editor

**Inherited:** US-02; FR-009/016; SC-004/005. **Confirmed:** Inline state/date/recorder/note form with Save/Cancel and Clear assessment. Recorded states, including recorded Unknown, require date/recorder. Clear removes metadata and returns to unassessed Unknown; no observation history is added. **Proposed:** Separate Clear from ordinary Save and explain its effect before explicit confirmation. Distinguish "Unknown — not assessed" from recorded Unknown with its metadata.

**Acceptance:** Missing required metadata blocks saving. Cancel leaves the observation unchanged. Clear persists unassessed Unknown after restart. Changing a ticket never automatically changes an observation.

### UX-010: Asset editor and source evidence

**Inherited:** US-03; FR-010/011/019; SC-003/004. **Confirmed:** Nested inline editor exposes name, purchase/installation dates and useful life; ID, room/category and derived values are read-only. Cost/currency corrections use the separate paired override form. Source/history sections show original baseline, invoice items/provenance and applied before/after update history. No Add asset action exists.

**Proposed:** Label source, current operational and effective financial values distinctly; explain purchase-date fallback when installation is absent. Keep historical-only invoice evidence separate from applied-update events.

**Acceptance:** Invalid date/life input blocks saving; Cancel changes nothing. Exactly three fixed assets remain visible. Newer applied invoices replace six fields and clear overrides; older/equal-date evidence and identical repeats preserve operational edits. Histories and successful saves survive restart.

### UX-011: Financial override and reset

**Inherited:** US-03; FR-019; SC-003/004. **Confirmed:** Paired cost/currency form requires reason and recorder; reset exposes the source values it restores and retains history. **Proposed:** Label actions "Apply financial override" and "Reset to source". Identify whether the reset source is the latest applied invoice or baseline. Show current/source/effective pairs and explain that reset does not restore name/dates or observations. Require reason/recorder in the reset form as well as the override form.

**Acceptance:** Incomplete pairs or missing attribution block saving. Reset restores the correct source pair and appends history. Failed writes change neither effective values nor history. Display currency changes never create overrides.

### UX-012: Ticket editor, progression and history

**Inherited:** US-04; FR-012/013; SC-004. **Confirmed:** Inline ticket forms expose description, severity, owner, target date and permitted progression; associations become fixed after creation. Open → In progress requires an owner; In progress → Resolved requires a resolution note and actual timestamp. Resolved tickets are read-only with chronological history.

**Proposed:** Use explicit "Start work" and "Resolve" actions instead of an unrestricted status selector. Explain unavailable actions beside their prerequisites. Allow owner removal only in Open, with reassignment while unresolved. Keep Save/Cancel available for editable fields; resolution note appears with the Resolve action.

**Acceptance:** Ownerless start, owner removal in progress, empty-note resolution, stage skipping, reopening, deletion and resolved editing are unavailable or rejected. Allowed edits retain before/after history; failed/cancelled edits leave records unchanged.

### UX-013: Empty, loading and write-feedback states

**Inherited:** US-01–03; FR-003/008/015; SC-002/004/005. **Confirmed:** Define first-use/no-data, filtered-empty, loading, validation failure, blocked upload, warning-only preview, saving, success and persistence failure; failed saves retain entered values, and success requires confirmed persistence. **Proposed:**

| State | Required presentation/action |
|---|---|
| No imported data | Explain baseline initialization and provide "Import Assets"; show honest zero counts. |
| Filter/search empty | Explain the cause and offer Clear filters or Clear room search; no stale rows. |
| Loading | Static text/progress indicator; no animated shimmer or old data presented as current. |
| Invalid form / blocked upload | Inline field/coordinate errors plus summary; preserve input and offer correction. |
| Warning-only preview | Keep warnings visible and explain that confirmation is allowed. |
| Saving / confirming | Static pending feedback; disable duplicate submissions until the result is known. |
| Success | Announce only after persistence, then refresh affected data. |
| Persistence failure | Explain nothing was saved, retain form/upload for retry, and keep prior saved state. |

**Acceptance:** Exercise each state, including a forced write failure. No success-looking state appears before persistence; errors are accessible without relying on transient notifications.

### UX-014: Language, currency and date boundaries

**Inherited:** US-02/05; FR-011/014/017/018; SC-003/008. **Confirmed:** Upper-right Language and Currency dropdowns on every page; English/USD initial defaults; independent persistent preferences; conditional stretch translation sets with English fallback; grouped local totals; unchanged source/user text; explicit financial versus operational date labels.

**Proposed:** Offer only delivered language sets. Label currency choices "USD" and "Local transaction currency". Put the session financial reporting date at the start of financial/replacement sections, defaulting to actual Hong Kong today, with a custom date and Reset to today. Show current operational date by maintenance summaries and offset/timezone with actual history timestamps. Existing demo presets remain optional proposals, not required controls.

Always show the fixed FX date and "Fictional fixed rates — not live market rates" with financial results. Missing/invalid FX configuration requires correction and blocks complete reporting; never show partial or fabricated USD totals. Label replacement spending as an acquisition-cost proxy and dates as planning assumptions, not quotations or predicted failures.

**Acceptance:** Both labelled dropdowns appear in the upper-right header on Overview, Maintenance, Import and Debugging - Assumptions and are keyboard usable. Language/currency selections independently survive browser restart without modifying stored data. Changing financial date alters only financial/replacement outputs, not current observations, ticket timestamps or operational overdue order. Verify local grouping, fallback and invalid-FX feedback.

### UX-015: Monochrome styling and bright actions

**Confirmed:** Black/grey/white spectrum, pale beige background, white panels, bright blue primary actions, dark readable text, restrained borders, aligned numeric columns and consistent spacing. No shadows, gradients, fading or animated transitions. **Proposed:** Use a 16px base system font and a simple 8px spacing rhythm, with larger page headings and comfortable control padding. Primary buttons use white text on a blue that provides readable contrast; secondary buttons remain neutral. Destructive/clearing actions use explicit wording and neutral outlined treatment, separate from Save.

**Acceptance:** Inspect all essential views and states for the agreed palette, readable labels, numeric alignment and absence of prohibited effects. Status meanings and active navigation remain clear in greyscale.

### UX-016: Responsive desktop and narrow layouts

**Confirmed:** Desktop central workspace narrows when the right card opens; narrow screens use compact navigation, stacked content/forms and an explicit-close room overlay; usability extends to 360px. **Proposed:** At 1200px and above, use a 200px left navigation and approximately 400px right card with the remainder for the central workspace. Below 1200px, move navigation to a compact top row and use a viewport-bounded room overlay instead of squeezing three columns. At 600px and below, make the room overlay full-width and stack form fields. Keep the room heading/Close action visible while its content scrolls; horizontally scroll wide tables inside labelled containers, never the entire page.

Keep Language and Currency dropdowns right-aligned in the header; at narrow widths they may wrap onto a second header row without truncating labels or disappearing. In the room overlay, keep Log fault reachable and close the overlay when it navigates to Maintenance, honoring the same unsaved-change guard.

**Acceptance:** Check 1440px, 1024px, 768px and 360px widths with the card open/closed, long names and validation messages. Navigation, both header dropdowns, Close, Log fault and primary form actions remain reachable; panel content scrolls without clipping and no unintended page overflow occurs.

### UX-017: Keyboard, focus and accessible feedback

**Confirmed:** Labelled inputs, visible keyboard focus, text accompanying status indicators, keyboard room selection/closing and accessible feedback. **Proposed:** Use semantic headings, buttons, tables and form labels. Expose Map/List selection and inline-section expansion states. Announce loading/save/error results and associate field errors with inputs; focus the first invalid field after failed validation. On opening a card, move focus to its heading; Close returns focus to the room trigger or a sensible view heading if the trigger is gone. Trap focus only in the narrow overlay, make background content inactive there, and let Escape invoke the same close/dirty-form guard. Desktop cards permit keyboard access to the central workspace.

**Acceptance:** Complete navigation, room selection, editing, validation correction and close/return using only the keyboard. Check labels, selected/expanded states and result announcements with an assistive-technology review. No action requires hover or color interpretation.

### UX-018: Integrated scope and return journey

**Inherited:** US-01–05; SC-002–005/008; AR-002/004/005/006. **Confirmed:** Map/List consistency, room-card context, maintenance navigation, cancellation/failure, import states, keyboard/narrow layouts and display boundaries all require future verification. **Proposed:** Rehearse Import baseline → Overview filter → Map/List → room card → observation/asset edit → room-card Log fault → Maintenance owner assignment/progression → financial review → Debugging - Assumptions, maintaining honest evidence and the existing 12-minute target in the demo.

**Acceptance:** Applied invoice updates refresh visible room/financial data; historical-only evidence does not overwrite edits. Closing cards or returning from Maintenance preserves the relevant context. Restart retains successful records/history and language/currency preferences; fresh-session financial date resets to today. Disclose AR-002's missing manual creation and any undelivered/unverified UI behavior.

### UX-019: Debugging - Assumptions page

**Confirmed:** Add a left-navigation page named "Debugging - Assumptions" listing all assumptions used, including depreciation math and FX rates. **Inherited:** Product sections 3–4/7–10/13/15; US-03/05; FR-011/014/017–019; SC-003/008; data contracts. **Proposed:** Use read-only sections with concise explanations and source references. Separate approved product rules, actual loaded configuration, and proposed technical/display defaults. The page remains available before imports and when financial configuration is invalid. It documents the calculation model and prototype policies, rather than application logs or an editable configuration form.

The complete assumption inventory is:

| Group | Required content |
|---|---|
| Service anchor and clock | Current operational installation date, falling back to purchase date; Asia/Hong_Kong actual operational clock; session financial date initially today. Changing financial date does not reconstruct historical records or change tickets/observations. |
| Depreciation | Straight-line, zero residual, whole completed months; derive each anniversary from the original service day and clamp to the destination month's last day. Before service, completed months = 0; cap months at useful life. Depreciation = effective cost × capped completed months ÷ useful-life months; book value = effective cost − depreciation. Retain unrounded decimal calculations/aggregations. Include the USD 1,200 / 12-month example and month-end/leap-year examples from product section 8. |
| Effective values and overrides | Active paired cost/currency override, otherwise latest applied invoice source pair, otherwise baseline pair. Current edited dates/name/life apply until a newer invoice replaces its six fields. Reset restores only source cost/currency; preserve before/after history. |
| Replacement planning | Service anchor + useful-life months with the same month clamping. Overdue is before reporting date, due today is equal, due soon is strictly after through +90 days inclusive. The future spending window is strictly after through +12 calendar months inclusive. Separate overdue/today/future totals; acquisition-cost proxy, no book-value subtraction, quotations, inflation, installation-labor estimate or failure prediction. |
| FX configuration | Show the actual configured HKD, SGD, GBP, JPY and USD rate table, with USD per one source unit, USD = 1, configuration date and "Fictional fixed rates — not live market rates". Conversion = effective transaction amount × configured rate. Do not invent numerical rates: before configuration exists show "Not configured"; missing/invalid values show explicit diagnostics and blocked financial-reporting status. Rates remain visible in their source-to-USD direction regardless of Currency dropdown choice. |
| Money display and aggregation | USD rounds to two decimals after calculation/aggregation; mixed local totals are grouped by effective currency. Proposed contract display: JPY zero decimals, other supported currencies two, clearly identified as a proposal. Each asset is valued once regardless of tickets or invoice-evidence joins. |
| Baseline/import model | Prescribed single-sheet Assets and Invoices uploads independently; exactly one lighting, water-supply and air-conditioning asset per room. Baseline creates complete rooms; invoices update existing room/category targets. Preview writes nothing; any blocker rejects the whole batch; confirmation revalidates and commits atomically. Warnings are non-blocking. |
| Invoice ordering and evidence | Maximum invoice_date controls current source values; older items remain evidence. Conflicting controlling-date snapshots block; equivalent ties do not replay updates. Identical identities skip; changed source content conflicts. Newly applied snapshots replace six fields and clear overrides with history; source evidence remains preserved. |
| Conditions and asset links | Three independent latest observations; missing assessment is Unknown, recorded assessments need date/recorder, Clear removes metadata, and no observation history exists. Faults do not infer condition; only explicit same-room asset links flag an asset. The schematic map is not a physical floor plan. |
| Maintenance | Manual fault logging, fictional owner list/self-declared attribution, optional owner in Open and required owner in progress. Forward-only Open → In progress → Resolved; resolution note and actual timestamp required. Associations fixed, unresolved edits have history, resolved tickets are read-only. Priority is severity, overdue target date, oldest opened timestamp. |
| Language and preferences | English mandatory; Traditional Chinese, Simplified Chinese and Japanese conditional stretch sets with English fallback. Stored IDs/enums/headers/names/notes remain unchanged; English/USD defaults, independent device-persistent language/currency choices. Translation linguistic review remains pending. |
| Prototype/data boundaries | Fictional data only; four properties/twelve rooms/thirty-six assets describe sample coverage, not product capacity. No manual asset creation (AR-002 gap), master-data forms, live FX/OCR/sensors/integrations, authentication or production accounting compliance. Operational records/history require local restart persistence; actual storage details are pending and any future hosted reset/durability limits require accurate disclosure. |

List proposed parsing/identifier, history-representation and display details separately with references to the data contracts; identify them as proposals rather than claiming they are implemented. Show the loaded fictional owner configuration when available and "Not configured" otherwise. Future changes to assumptions/configuration must update this inventory alongside their source and the actual calculation services; presentation logic must not maintain a conflicting calculation model.

**Acceptance:** Every inventory group is present and its rule/status matches product/contracts and actual loaded configuration. Check complete, absent and invalid FX configuration, including USD rate integrity; never show fabricated rates. Numeric examples match the financial rules, changing display currency does not change configured rates, and opening the page changes no data/preferences by itself. Verify access before imports, keyboard/narrow-screen operation and labelled upper-right dropdowns; keep all application checks NOT RUN until exercised.

## 5. Verification and evidence status

| UX coverage | Existing evidence groups / criteria | Status |
|---|---|---|
| UX-001–005 | E-ROOM/E-UI; US-02; SC-005/008 | NOT RUN |
| UX-006/012 | E-MAINT/E-ROOM; US-04; SC-004/005 | NOT RUN |
| UX-007/008 | E-IMPORT; US-01; SC-001/002 | NOT RUN |
| UX-009–011 | E-ROOM/E-ASSET/E-FINANCE; US-02/03; SC-003/004 | NOT RUN |
| UX-013–017 | E-UI and relevant workflow group; SC-002/004/005/008 | NOT RUN; linguistic review deferred |
| UX-018 | E-DEMO/E-STARTUP and workflow groups; AR-006; SC-004/007 | NOT RUN |
| UX-019 | E-UI/E-FINANCE; FR-011/014/017–019; SC-003/008 | NOT RUN |

During later implementation, record method, build/date, expected/actual outcome and PASS/FAIL/NOT RUN under the existing [evidence ledger](assessment-requirements.md). Include pending or failed accessibility/responsive checks rather than treating documentation as proof. The [delivery plan](plan.md), [task checklist](tasks.md) and [demo](demo.md) carry this future work.

For this documentation revision, verify local Markdown links, renamed-file references, stable/unique UX IDs and consistency with product/contracts. Such checks establish documentation integrity only. Application verification, fixture generation, startup/restart evidence and rehearsal remain pending.

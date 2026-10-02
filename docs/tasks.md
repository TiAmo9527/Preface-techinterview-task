# Task checklist

Version: 0.3

Revised: 2026-10-03

Target delivery: 2026-10-05

This checklist follows [the plan](plan.md). Completed documentation is not application evidence.

## Documentation revision

- [x] Revise specification to v0.3 with retained IDs, exactly three room/category records, baseline/invoice updates and revised owner decisions.
- [x] Preserve assessment obligations/legacy SC mappings and explicitly disclose AR-002's manual asset-creation gap.
- [x] Document two independent workbook contracts, source baselines, invoice precedence and operational/history boundaries.
- [x] Document fully populated valid and deliberate invalid pairs generated together, with coordinates/prerequisites, without generating files.
- [x] Expand existing demo and align plan/README.
- [x] Rename the product specification and add a linked [UI/UX specification](ui-ux-spec.md), distinguishing inherited requirements, confirmed design choices and proposed details.
- [x] Revise UI/UX specification to v0.2 with room-card Log fault handoff, maintenance owner/progress behavior, upper-right dropdowns and the Debugging - Assumptions page inventory.
- [ ] Obtain review of exact technical contract proposals before implementation reliance.

## Future implementation and fixtures

- [ ] Select implementation details separately, respecting views/services/db boundaries.
- [ ] Create blank Assets/Invoices templates and one combined four-location valid/invalid sample run with manifest; verify saved files and expected updates.
- [ ] Create deliberate invalid batches and boundary test fixtures.
- [ ] Implement independent baseline/invoice preview/confirmation with before/after effects, category completeness/repeated-value checks, atomic writes and detailed diagnostics.
- [ ] Preserve baselines/invoice items/provenance; verify source repeat/conflict rules, target integrity, subset updates, newest-date selection, tied conflicts/equivalent evidence and historical-only records.
- [ ] Implement viewing/editing of existing assets, invoice replacement/override clearing/history, paired overrides and latest-invoice/baseline reset fallback; exclude manual creation.
- [ ] Implement room observations with required metadata and Clear → Unknown.
- [ ] Implement maintenance ownership, permitted edits, ordering, transitions/history and resolved immutability.
- [ ] Implement dashboard filters, labelled counts, room links, empty states and no financial duplication.
- [ ] Implement Overview/Maintenance/Import/Debugging - Assumptions navigation, schematic Map/List room views, right-side room card and inline editors using the UI/UX specification.
- [ ] Implement room-card Log fault navigation to a room-preselected Maintenance draft, explicit Save/Cancel, manager owner assignment/progress updates and preserved Overview return context.
- [ ] Add upper-right Language/Currency dropdowns and the read-only UX-019 assumptions inventory with actual configured FX rates/date and honest missing/invalid states.
- [ ] Implement confirmed styling, keyboard access, focus/feedback and responsive layouts down to 360px, including the narrow-screen room overlay.
- [ ] Implement approved financial dates, depreciation, complete FX and replacement windows/proxies.
- [ ] Implement mandatory English, independent local/USD switch and persistent preferences.
- [ ] Deliver stretch translation sets if feasible, with English fallback.

## Verification and assessment

- [ ] Record E-IMPORT: independent initialisation/update uploads, blocked/atomic success/failure, stale previews, warnings, repeated/changed sources and invoice precedence.
- [ ] Record E-ROOM: filters/counts, observations and independent room/asset faults.
- [ ] Record E-ASSET/E-MAINT: editing, invoice before/after/override history, fixed identities/categories/associations, transitions, persistence and explicit AR-002 add-asset gap.
- [ ] Record E-FINANCE: numerical/date boundaries, overrides, FX and spending scopes.
- [ ] Record E-UI: display boundaries, fallback/preferences and financial/operational clock separation.
- [ ] Verify UX-001–019: navigation/Map/List consistency, room-card context/Log fault handoff, maintenance owner/progress changes, dropdowns, assumptions/FX configuration, editor cancellation/failure, import states, keyboard operation and responsive styling; record actual results with the mapped evidence groups.
- [ ] Resolve deferred translation verification with Alex; disclose sets lacking fluent review.
- [ ] Record E-STARTUP using an actual clean-start web application and restart.
- [ ] Record E-DEMO with a timed 12-minute rehearsal and required explanations.
- [ ] Review confidentiality and fictional-data scope; disclose unmet requirements.
- [ ] If later authorised, prepare controlled repository/preview sharing and storage disclosures.

All application tests, fixture generation, rehearsal and publishing remain pending. No task above authorises code, dependency installation, commit, or deployment during this documentation-only change.

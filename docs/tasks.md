# Task checklist

Version: 0.2

Revised: 2026-10-02

Target delivery: 2026-10-05

This checklist follows [the plan](plan.md). Completed documentation is not application evidence.

## Documentation revision

- [x] Revise product specification with owner decisions, retained IDs, and new FR-016–019/SC-008.
- [x] Separate assessment obligations and legacy SC mappings.
- [x] Document explicit proposed four-file contracts and source/operational boundaries.
- [x] Document fictional sample/template coverage without generating files.
- [x] Expand existing demo and align plan/README.
- [ ] Obtain review of exact technical contract proposals before implementation reliance.

## Future implementation and fixtures

- [ ] Select implementation details separately, respecting views/services/db boundaries.
- [ ] Create blank prescribed Excel templates and fictional four-location fixtures/invoices.
- [ ] Create deliberate invalid batches and boundary test fixtures.
- [ ] Implement atomic preview/validation/confirmation/import and detailed diagnostics.
- [ ] Preserve source baselines/provenance; verify repeat skips, conflicts, and unique invoice links.
- [ ] Implement generated-ID assets, allowed edits, paired overrides/resets and history.
- [ ] Implement room observations with required metadata and Clear → Unknown.
- [ ] Implement maintenance ownership, permitted edits, ordering, transitions/history and resolved immutability.
- [ ] Implement dashboard filters, labelled counts, room links, empty states and no financial duplication.
- [ ] Implement approved financial dates, depreciation, complete FX and replacement windows/proxies.
- [ ] Implement mandatory English, independent local/USD switch and persistent preferences.
- [ ] Deliver stretch translation sets if feasible, with English fallback.

## Verification and assessment

- [ ] Record E-IMPORT: blocked batches, atomic success/failure, warnings, repeated/changed sources.
- [ ] Record E-ROOM: filters/counts, observations and independent room/asset faults.
- [ ] Record E-ASSET/E-MAINT: edit validation/history, association integrity, transitions and persistence.
- [ ] Record E-FINANCE: numerical/date boundaries, overrides, FX and spending scopes.
- [ ] Record E-UI: display boundaries, fallback/preferences and financial/operational clock separation.
- [ ] Resolve deferred translation verification with Alex; disclose sets lacking fluent review.
- [ ] Record E-STARTUP using an actual clean-start web application and restart.
- [ ] Record E-DEMO with a timed 12-minute rehearsal and required explanations.
- [ ] Review confidentiality and fictional-data scope; disclose unmet requirements.
- [ ] If later authorised, prepare controlled repository/preview sharing and storage disclosures.

All application tests, fixture generation, rehearsal and publishing remain pending. No task above authorises code, dependency installation, commit, or deployment during this documentation-only change.

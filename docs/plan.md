# Delivery and implementation plan

Version: 0.3

Revised: 2026-10-03

Owner: Alex

Target delivery: 2026-10-05

Status: Documentation revised; application work not started

The [product specification](product-spec.md) defines behaviour, [UI/UX specification](ui-ux-spec.md) records confirmed design choices and proposed interactions, [contracts](data-contracts.md) define proposed input/logical interfaces, and [assessment requirements](assessment-requirements.md) define external obligations. This ordered backlog does not select a new framework/database/hosting architecture or authorise implementation.

## 1. Settle interfaces and verification coverage

Review technical proposals in the contracts: exact headers/types, identifier grammar, normalisation/comparison, invoice-update/override history representation and configuration details. Keep approved owner policies distinct from these proposals.

Map US/FR/SC/AR coverage to actual tests and evidence. Translation verification remains Alex's deferred submission check. Preserve fixed target date without relying on obsolete relative-day estimates.

## 2. Establish trusted data and persistence

In later authorised work, implement independent Assets baseline and Invoices update workflows with previews, comprehensive diagnostics and atomic confirmed persistence. Validate consistent repeated property/room values, readable identifiers and exactly one record per room/category. Initial cost/currency comes from baseline, without invoice dependencies. Preserve source identities, compare repeats against original evidence and validate complete fixed FX configuration.

Resolve invoice items to existing room/category assets. Apply the newest invoice_date snapshot, retain older evidence, block conflicting controlling-date snapshots, skip identical identities and reject changed source identities. Record before/after updates, clear active overrides with linked history, recalculate finance and roll back evidence/updates/history together on failure. Recheck stale previews at confirmation.

Create the two blank Excel templates later. One invocation of the generation prompt must produce valid and invalid Assets/Invoices pairs plus one manifest; verify saved files and before/after expected values. No separate observations/maintenance import or PDF requirement. Verify blocked/failed uploads write nothing and successful records/history survive restart.

## 3. Build the primary operational journey

Implement dashboard filters/count units/prioritised unresolved tickets and room drill-down. Add latest observation editing/clearing, viewing/editing of the three fixed asset records, paired overrides/resets/history, and the three-status maintenance workflow.

Use the UI/UX specification's Overview/Maintenance/Import/Debugging - Assumptions navigation, central schematic Map/List view and right-side room card. Its Log fault button opens Maintenance with a room-preselected new-item draft; only a valid Save creates an Open ticket. Maintenance lets managers log faults, assign an owner and update maintenance progress. Retain filters and return context, keep observation/asset editors within the card and new fault forms on Maintenance, and apply the confirmed monochrome/beige styling with bright primary actions and no shadows or animated effects. Proposed interaction details are identified separately from confirmed design choices.

Check same-room links, fixed associations, owner restrictions, chronology, resolved immutability, and edits surviving identical baseline/invoice repeats and historical-only evidence, with explicit replacement on newer invoices. Reset cost/currency to the latest applied invoice or baseline fallback. Finance must not duplicate assets through ticket joins.

## 4. Add supporting reporting and display

Implement approved depreciation/month conventions and secondary replacement horizons/proxies. Separate actual operational dates from the session financial date. Add independent USD/local grouping and persistent preferences.

Place labelled Language and Currency dropdowns in the upper-right header on every page. Add the read-only Debugging - Assumptions page with the complete UX-019 inventory, actual configured fictional FX rates/date, depreciation math/examples, source references and explicit missing/invalid configuration states; do not fabricate rates or introduce configuration editing.

Mandatory English precedes stretch Traditional/Simplified Chinese/Japanese translation sets. Apply fallback and source/user-text boundaries; defer linguistic accuracy claims until reviewed.

## 5. Verify and rehearse

Run meaningful tests for agreed behaviour and edge cases, then the clean-start/restart checks. Record actual evidence under SC and AR IDs. Rehearse the existing demo sequence within 12 minutes and disclose unmet criteria/limits, explicitly including AR-002's omitted manual add-asset workflow.

Verify UX-001–019 for Map/List consistency, room-card selection/closing, Log fault handoff/draft cancellation, maintenance owner/progress changes, shared filters, failed/cancelled forms, import states, header dropdowns, assumptions/actual FX configuration, keyboard operation and 360px layouts alongside the existing preferences/date checks. Documentation consistency checks are not application evidence.

Optional repository/preview sharing is a separate future decision, subject to confidentiality. No deployment is selected or performed by this documentation revision.

## Repository boundaries

app.py remains the entry point; src/views contains presentation, src/services contains domain behaviour, src/db contains persistence, and tests contains verification. Keep domain/persistence logic out of views. sample_data holds fictional development fixtures; runtime holds local generated state and must not be committed.

Current code is a title-printing scaffold. Empty application/test/fixture directories do not establish implemented features or passing checks.

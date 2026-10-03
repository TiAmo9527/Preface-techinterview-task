# Delivery and implementation plan

Version: 0.4

Revised: 2026-10-03

Owner: Alex

Target delivery: 2026-10-05

Status: Documentation revised. Application implementation and verification: NOT RUN.

[Product requirements](product-spec.md) define behavior. [UI/UX requirements](ui-ux-spec.md) distinguish Confirmed and Proposed details.
[Contracts](data-contracts.md) define proposed technical interfaces. [Assessment requirements](assessment-requirements.md) preserve external obligations.
Use [acceptance scenarios](acceptance-scenarios.md) and the [shared glossary](glossary.md).

## 1. Settle technical interfaces

1. Review proposed headers, types, identifiers, normalization, comparisons, and history representation.
2. Select the framework, persistence design, configuration interfaces, and startup process during technical planning.
3. Define selection of normal and isolated demo stores without destructive reset.
4. Preserve existing identities and public workbook interfaces.
5. Map acceptance scenarios to actual tests and evidence records.
6. Keep Proposed UI choices separate from approved requirements.

Translation review remains Alex's pre-submission responsibility. The target date is fixed, not a relative-day estimate.

## 2. Establish trusted data and persistence

1. Implement independent baseline and invoice workflows with preview, diagnostics, confirmation, and atomic persistence.
2. Validate repeated baselines, identities, exactly three categories, and existing invoice targets.
3. Preserve baselines, invoice items, provenance, and source equality.
4. Apply newest eligible invoices with tied-conflict checks and historical-only evidence.
5. Replace snapshot fields and clear overrides with linked before/after history.
6. Recheck stale previews before confirmation.
7. Preserve previous saved state on failure.
8. Validate complete fictional FX configuration.
9. Implement normal restart persistence and isolated rehearsal stores.

Generate templates and valid/invalid samples later. Use one generation invocation and verify all saved files and expected updates.
Do not add maintenance imports, observation imports, or PDF requirements.

## 3. Build the primary operational journey

1. Implement Overview filters, distinct counts, unresolved priorities, and room selection.
2. Implement Map/List, right-side room cards, and confirmed styling.
3. Implement latest observation editing and Clear without observation history.
4. Implement permitted asset edits, source evidence, paired overrides, reset, and history.
5. Implement room-card Log fault navigation to Maintenance.
6. Implement fault creation, ownership, forward-only progression, and read-only resolution.
7. Check fixed same-room links and actual timestamps.
8. Check identical repeats and historical-only items preserve edits.
9. Sum each asset value once regardless of ticket or evidence joins.

Proposed complete return context, focus rules, and numeric layout defaults remain design proposals.

## 4. Add supporting financial and display behavior

1. Implement depreciation anniversaries, fallback dates, life caps, and replacement windows.
2. Separate actual operational date from session financial reporting date.
3. Implement mandatory English and independent persistent local/USD preferences.
4. Add delivered stretch languages only with English fallback.
5. Implement upper-right Language/Currency controls.
6. Implement Debugging - Assumptions with complete inventory and actual configuration.
7. Display missing configuration honestly without fabricated rates or partial totals.

## 5. Verify and rehearse

1. Execute required scenarios independently.
2. Record actual SC/AR evidence with expected and actual results.
3. Check Windows-laptop Chrome context and record actual versions.
4. Check keyboard operation and all required viewport widths.
5. Check clean startup, normal restart, new-store isolation, and retained browser preferences.
6. Rehearse the existing demo within twelve minutes.
7. Disclose missing manual creation, undelivered translations, and failed criteria.
8. Review fictional-data and confidentiality boundaries before any authorized sharing.

Optional publication remains a separate future decision. No hosting design is selected by this documentation revision.

## Repository boundaries

app.py is the entry point. src/views contains presentation. src/services contains business behavior. src/db contains persistence.
tests contains verification. Keep business and persistence logic outside views.

sample_data contains supplied fictional fixtures. runtime contains ignored local generated state.
The current code only prints a title. Placeholder directories do not establish implementation or passing checks.
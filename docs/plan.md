# Delivery and implementation plan

Version: 0.2

Revised: 2026-10-02

Owner: Alex

Target delivery: 2026-10-05

Status: Documentation revised; application work not started

The [specification](spec.md) defines behaviour, [contracts](data-contracts.md) define proposed input/logical interfaces, and [assessment requirements](assessment-requirements.md) define external obligations. This ordered backlog does not select a new framework/database/hosting architecture or authorise implementation.

## 1. Settle interfaces and verification coverage

Review technical proposals in the contracts: exact headers/types, normalisation/comparison, manual reset baseline, history representation, and configuration details. Keep approved owner policies distinct from these proposals.

Map US/FR/SC/AR coverage to actual tests and evidence. Translation verification remains Alex's deferred submission check. Preserve fixed target date without relying on obsolete relative-day estimates.

## 2. Establish trusted data and persistence

In later authorised work, implement four-file preview, comprehensive diagnostics, explicit valid-batch confirmation, atomic persistence, meaningful source baselines, repeat skips/conflicts, unique invoice links, and validated complete fixed FX configuration.

Create blank Excel templates and fictional valid/invalid fixtures later from the sample-data plan. No fifth observations import or maintenance import path. Verify blocked/failed batches write nothing and successful records survive restart.

## 3. Build the primary operational journey

Implement dashboard filters/count units/prioritised unresolved tickets and room drill-down. Add latest observation editing/clearing, generated-ID manual assets, permitted asset edits, paired overrides/resets/history, and the three-status maintenance workflow.

Check same-room links, fixed associations, owner restrictions, chronology, resolved immutability, and operational edits surviving original-source re-imports. Finance must not duplicate assets through ticket joins.

## 4. Add supporting reporting and display

Implement approved depreciation/month conventions and secondary replacement horizons/proxies. Separate actual operational dates from the session financial date. Add independent USD/local grouping and persistent preferences.

Mandatory English precedes stretch Traditional/Simplified Chinese/Japanese translation sets. Apply fallback and source/user-text boundaries; defer linguistic accuracy claims until reviewed.

## 5. Verify and rehearse

Run meaningful tests for agreed behaviour and edge cases, then the clean-start/restart checks. Record actual evidence under SC and AR IDs. Rehearse the existing demo sequence within 12 minutes and disclose unmet criteria/limits.

Optional repository/preview sharing is a separate future decision, subject to confidentiality. No deployment is selected or performed by this documentation revision.

## Repository boundaries

app.py remains the entry point; src/views contains presentation, src/services contains domain behaviour, src/db contains persistence, and tests contains verification. Keep domain/persistence logic out of views. sample_data holds fictional development fixtures; runtime holds local generated state and must not be committed.

Current code is a title-printing scaffold. Empty application/test/fixture directories do not establish implemented features or passing checks.

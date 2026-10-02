# Interview walkthrough and evidence plan

Version: 0.2

Revised: 2026-10-02

Target: 2026-10-05

Status: Planned; application not implemented and walkthrough not rehearsed

This is the existing demo document, expanded rather than duplicated. [Assessment requirements](assessment-requirements.md) define AR-006; [product specification](spec.md) and [sample-data plan](sample-data-plan.md) define the behaviours and fictional fixtures.

## 1. Proposed 12-minute sequence

| Time | Demonstration | Evidence/requirement |
|---|---|---|
| 0:00–1:00 | State room-understanding/maintenance outcome; start the verified web application and introduce fictional data | AR-002/007; E-STARTUP |
| 1:00–3:00 | Upload four files with one deliberate blocking error; show diagnostics and no writes. Correct it, preview warnings, explicitly confirm valid batch, inspect actual counts/provenance | US-01; SC-001/002; E-IMPORT |
| 3:00–5:00 | Filter dashboard, drill into a room, inspect three observations/assets/tickets; edit an assessment to Healthy with metadata, then demonstrate Clear → Unknown | US-02; FR-009/016; E-ROOM |
| 5:00–7:00 | Create manual asset with generated ID; edit permitted fields; inspect an imported asset's invoice source; apply paired override with reason/history and reset | US-03; FR-010/019; E-ASSET |
| 7:00–9:00 | Log fault Open, select owner, progress to In progress, resolve with note; inspect persistent history, read-only result, and unchanged observation | US-04; FR-012/013; E-MAINT |
| 9:00–10:30 | Review secondary financial/replacement results; change financial date; inspect effective-cost proxy and separate horizons; switch USD/local without changing stored values | US-05; FR-011/014/018; E-FINANCE |
| 10:30–12:00 | Explain actual technology choices, validation, limitations, verification results, and how AI assisted development; disclose deferred/undelivered scope | AR-006; E-DEMO |

This timing is a proposal, not a successful rehearsal. Show repeat-import-after-edit and restart evidence from recorded verification if live repetition would exceed time. Never replace evidence with a claim that a demonstration action happened earlier.

## 2. Reporting-date presets

Proposed financial controls/presets for rehearsal: Today, Today + 90 days, Today + 12 calendar months, and a custom date for the documented depreciation example (2026-07-14 / 2026-07-15). The preset choices are demo proposals, not additional owner-approved UI requirements.

- Label Financial reporting date separately from Current operational date.
- Use one selected financial date for book values/replacement outputs.
- Show that ticket history, observation data, and actual overdue priority do not change.
- Do not imply a historical snapshot, simulated clock, or generated faults.
- Choose dates that exercise prepared fictional asset boundaries; do not change source evidence to fake a result.

## 3. Verification before rehearsal

Use the evidence groups in [assessment requirements](assessment-requirements.md). Every entry needs method, build/date, expected/actual outcome, and status.

- Import: valid commit, blocked mixed-validity batch, duplicate/conflicting IDs, repeat after operational edits, same-line collisions, rollback, warning-only success.
- Room/dashboard: all filters, incompatible-child clearing, empty results, count units, room links, condition metadata/clear, Healthy plus unresolved ticket, no asset financial duplication.
- Asset/finance: generated manual ID, immutable links, validation/cancel/failure, source evidence, override/reset history, fixed FX integrity, numerical/month-end/leap results, replacement endpoints.
- Maintenance: owner requirement/removal restriction, same-room linkage, stage skipping prohibited, unresolved edits/order/history, resolved immutability, no inferred asset flags.
- UI: mandatory English, persistent independent preferences, grouped local totals, fallback and unchanged source/user text for any delivered stretch translations.
- Startup/persistence: actual documented web-app startup in a clean local environment; successful records/history survive restart.
- Presentation: a timed run at or below 12 minutes, with all required explanations.

No application verification has been run. The current app only prints a scaffold title. Record failures and unmet criteria rather than checking tasks off based on documentation.

## 4. Explanation and disclosure checklist

Explain technology decisions actually made during later implementation, keeping domain/persistence logic outside views. State validation and source comparison rules, manual observation/ticket independence, fixed fictional FX and depreciation assumptions, and replacement proxies.

Describe AI's real assistance in planning/coding/testing and how Alex checked its output; do not imply AI functions inside the app. Disclose unavailable stretch translations and unreviewed linguistic accuracy. Translation review is deferred, not completed.

Disclose prototype limits: prescribed spreadsheets, no OCR/live rates/sensors/authentication, import-only master data, fixed associations, no reopening/deleting/resolved edits, and no production accounting/hosting claims. Share a repository/preview only if separately authorised, with confidentiality and durability limits reviewed.

## 5. Rehearsal record

Pending entries: date/build, elapsed time, completed steps, skipped steps, evidence references, defects/limitations, and follow-up owner action. Keep confidential evidence local or within the explicitly approved interview-sharing scope.

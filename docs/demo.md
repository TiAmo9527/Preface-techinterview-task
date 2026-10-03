# Interview walkthrough and evidence plan

Version: 0.4

Revised: 2026-10-03

Target delivery: 2026-10-05

Status: Planned. Application verification and rehearsal: NOT RUN.

[Product requirements](product-spec.md), [UI/UX requirements](ui-ux-spec.md), and [assessment requirements](assessment-requirements.md) define this demonstration.
Use fictional [planned samples](sample-data-plan.md). Use the [shared glossary](glossary.md) for terms.

## 1. Rehearsal state

Required context: Windows laptop with Chrome. Record the actual browser and Windows versions with the build/date.
Store-selection commands and controls remain technical-planning work. No working startup or store-selection command is claimed.

Before each later rehearsal:

1. Select a new isolated demo data store.
2. Check that it contains no imported records, observations, tickets, overrides, or histories.
3. Check that normal saved data remains unchanged.
4. Retain existing browser language/currency preferences.
5. Start a new session with actual Hong Kong today as the financial reporting date.
6. Select any required financial example date explicitly.

Normal restart uses the same selected store and retains its saved state.
Another rehearsal uses another empty store. No destructive reset button is required.
English/USD apply only when no saved preferences exist. Store isolation does not erase browser preferences.
Operational date remains actual Hong Kong today regardless of the financial example date.

Required checks: [Demo scenarios](acceptance-scenarios.md#demo). Application status remains NOT RUN.

## 2. Proposed 12-minute sequence

The following timing remains a proposal. It is not a successful rehearsal record.

| Time | Demonstration | Trace |
|---|---|---|
| 0:00–1:00 | State the room manager's maintenance decision. Start the later verified web application. Introduce fictional data and isolated rehearsal state. | AR-002, AR-007, E-STARTUP |
| 1:00–3:00 | Preview invalid Assets with no writes. Confirm valid Assets alone. Review three categories and baseline finance. Preview invalid Invoices. Confirm valid Invoices and inspect thirty-six updates. | US-01, SC-001, SC-002, E-IMPORT |
| 3:00–5:00 | Filter Overview. Switch Map/List. Open the room card. Record Healthy with metadata. Clear to Unknown. Close the card with retained view context. | US-02, FR-009, FR-016, UX-002–UX-005, UX-009, E-ROOM |
| 5:00–7:00 | Edit an existing asset. Inspect source/update history. Apply an override. Reset to latest invoice values. Present recorded invoice-ordering and override-clearing evidence. | US-03, FR-010, FR-019, E-ASSET |
| 7:00–9:00 | Choose Log fault. Save Open. Assign an owner. Start work. Resolve with a note. Inspect history, read-only resolution, and unchanged observation. | US-04, FR-012, FR-013, UX-005, UX-006, UX-012, E-MAINT |
| 9:00–10:30 | Review supporting finance/replacement. Select a reporting date. Compare separate spending horizons. Switch Currency. Explain actual FX and depreciation on Debugging - Assumptions. | US-05, FR-011, FR-014, FR-018, UX-014, UX-019, E-FINANCE |
| 10:30–12:00 | Explain actual technology, validation, limitations, evidence, and AI assistance. Disclose missing manual creation and undelivered scope. | AR-006, E-DEMO |

Use recorded verification for extra ordering, warning, repeat, and restart cases when live execution would exceed twelve minutes.
Do not claim an earlier action without evidence.

## 3. Reporting-date proposals and verification

Optional proposed presets are Today, Today + 90 days, Today + 12 calendar months, and custom example dates.
The documented example uses 2026-07-14 and 2026-07-15. Preset controls are not additional approved UI requirements.

1. Label Financial reporting date separately from Current operational date.
2. Use one financial date for book values and replacement outputs.
3. Show unchanged ticket history, observations, and operational overdue order.
4. Do not imply historical snapshots or a simulated clock.
5. Do not alter source evidence to imitate a financial result.

Before later rehearsal:

1. Execute every required [acceptance scenario](acceptance-scenarios.md) or its applicable conditional cases.
2. Record actual evidence under the SC and AR identifiers.
3. Check required Chrome context, keyboard access, responsive widths, and confirmed styling.
4. Check source imports, permitted edits, condition independence, maintenance progression, FX, and replacement boundaries.
5. Check clean startup, normal restart, and new-store isolation.
6. Record any failed or omitted checks.
7. Measure the walkthrough duration.

The current application only prints a title. No application verification or timed rehearsal occurred.

## 4. Explanation and disclosure

Explain actual technology choices only after implementation. Keep business and persistence logic outside views.
Explain independent uploads, atomic validation, source equality, invoice ordering, overrides, histories, condition independence, depreciation, and fictional FX.
Explain the difference between planning dates, spending proxies, quotations, and predicted failures.

Describe AI's actual planning, coding, and testing assistance. Explain how Alex checked the output.
Do not imply AI features inside the application. Disclose undelivered stretch languages and unreviewed linguistic accuracy.

Disclose prescribed spreadsheets, three fixed categories, import-only master data, and missing manual asset creation under AR-002.
Disclose excluded OCR, live rates, sensors, authentication, ticket reopening/deletion, and production accounting compliance.
Disclose actual storage limits if hosting occurs later. Repository/preview sharing remains a separate owner decision.

## 5. Rehearsal record

Status: NOT RUN.

Each later record must include:

- Date, build, Windows version, Chrome version, and selected demo store reference.
- Starting-state and isolation checks.
- Elapsed time and completed steps.
- Skipped steps and their reasons.
- Evidence references and actual results.
- Defects, limitations, and required follow-up actions.

Keep confidential evidence local or within explicitly authorized interview sharing.

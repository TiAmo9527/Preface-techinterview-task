# Interview walkthrough and evidence plan

Version: 0.5

Revised: 2026-10-03

Target delivery: 2026-10-05

Status: Planned. Application verification and rehearsal: NOT RUN.

[Product requirements](product-spec.md), [UI/UX requirements](ui-ux-spec.md), and [assessment requirements](assessment-requirements.md) define this demonstration.
Use fictional [planned samples](sample-data-plan.md). Use the [shared glossary](glossary.md) for terms.

## 1. Rehearsal state

Required context: Windows laptop with Chrome. Record actual versions, build, and date.
Use one shared local demo store. The earlier isolated-rehearsal-store requirement is superseded by confirmed reset.
Independent automated tests still use temporary isolated stores.

Before each later rehearsal:

1. Start the later implemented local application.
2. Open Debugging - Assumptions and choose Reset data.
3. Review the warning that all shared domain records, evidence, and histories will be removed.
4. Confirm reset. Cancel instead to preserve all saved data.
5. Check empty Overview and invalidated previews/drafts.
6. Check retained browser language/currency preferences and fictional configuration.
7. Check actual Hong Kong today as the new reporting date.
8. Select financial example dates explicitly when required.

Normal restart retains successful saved state. Startup never resets or reseeds automatically.
Reset intentionally removes earlier saves in this store. It preserves no separate normal portfolio.
English/USD apply only when browser preferences do not exist.
Operational date remains actual Hong Kong today regardless of financial example dates.

Required checks: [Demo scenarios](acceptance-scenarios.md#demo) and [infrastructure scenarios](acceptance-scenarios.md#infrastructure).
Application status remains NOT RUN.

## 2. Proposed 12-minute sequence

The following timing remains a proposal. It is not a successful rehearsal record.

| Time | Demonstration | Trace |
|---|---|---|
| 0:00–1:00 | State the room manager's maintenance decision. Start the later verified web application. Introduce fictional data and the reset shared local state. | AR-002, AR-007, E-STARTUP |
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
5. Check clean startup, normal restart, and shared-store reset and stale drafts.
6. Record any failed or omitted checks.
7. Measure the walkthrough duration.

The current application only prints a title. No application verification or timed rehearsal occurred.

## 4. Explanation and disclosure

Explain actual technology choices only after implementation. Keep business and persistence logic outside views.
Explain independent uploads, atomic validation, source equality, invoice ordering, overrides, histories, condition independence, depreciation, and fictional FX.
Explain the difference between planning dates, spending proxies, quotations, and predicted failures.

Describe AI's actual planning, coding, and testing assistance. Explain how Alex checked the output.
Do not imply AI features inside the application. Disclose undelivered stretch languages and unreviewed linguistic accuracy.

Disclose prescribed spreadsheets, three fixed categories, import-only master data, and unconfirmed maintenance interpretation and omitted manual asset creation under AR-002.
Disclose excluded OCR, live rates, sensors, authentication, ticket reopening/deletion, and production accounting compliance.
Disclose actual storage limits if hosting occurs later. Repository/preview sharing remains a separate owner decision.

## 5. Rehearsal record

Status: NOT RUN.

Each later record must include:

- Date, build, Windows version, Chrome version, and local database reference.
- Starting-state, reset, and stale-draft checks.
- Elapsed time and completed steps.
- Skipped steps and their reasons.
- Evidence references and actual results.
- Defects, limitations, and required follow-up actions.

Keep confidential evidence local or within explicitly authorized interview sharing.

## 6. Local runtime procedures

Status: Approved future command contract. These commands require later application implementation and have NOT RUN.
The current python app.py command prints a title. It does not implement these options.
Run from the repository root. Keep one application process on port 8000.
Use Python 3.11. Initial installation downloads dependencies. Later application operation is fully local.

### Install and initialize

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.\.venv\Scripts\python.exe app.py --init-db
```

Implementation must supply tested requirements.lock and requirements-dev.lock files with pinned versions.
The development lock includes runtime packages plus the test packages.
--init-db applies schema version 1 to runtime/app.sqlite3 and exits. It retains supported existing records.
An unsupported schema or failed migration blocks startup with an actionable message.

### Start, stop, and restart

```powershell
.\.venv\Scripts\python.exe app.py
```

The launcher runs one Uvicorn worker at 127.0.0.1:8000 with automatic reload disabled.
Open http://127.0.0.1:8000 in Chrome. Stop with Ctrl+C. Run the same command to restart.
The fixed database path resolves from the repository root, even when launched from another directory.
Startup initializes a missing store without source rows. It never clears existing records or imports samples automatically.
Restart preserves domain state and command receipts. Pending in-memory previews require another upload/review.
Browser-tab sessions retain their reporting date during reload. A newly opened session starts with Hong Kong today.

### Seed through reviewed imports

1. Reset the shared store through the confirmed UI when an empty state is needed.
2. Select Import Assets and upload sample/2026-10-03/invalid/Assets.xlsx.
3. Check blockers and zero saved domain effects.
4. Upload sample/2026-10-03/valid/Assets.xlsx and inspect the preview.
5. Confirm four properties, twelve rooms, and thirty-six asset inserts.
6. Select Import Invoices and upload sample/2026-10-03/invalid/Invoices.xlsx.
7. Check blockers and unchanged baseline state.
8. Upload sample/2026-10-03/valid/Invoices.xlsx and inspect the preview.
9. Confirm thirty-six invoice items and thirty-six distinct asset updates.

These are expected results, not observed application results. No separate seed command bypasses review or validation.
Use [fixture prerequisites](../sample/2026-10-03/fixture-inventory.md) for independent checks outside the timed demonstration.

### Test and evidence

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest tests/unit tests/integration
.\.venv\Scripts\python.exe -m pytest tests/browser --browser chromium
```

Browser installation requires an initial download. Test runs use local assets and isolated temporary stores.
The browser fixture starts its own local test server. It never resets runtime/app.sqlite3.
Record manual installed-Chrome checks separately from automated Chromium results.
Save local results/screenshots under runtime/verification/<build>/<scenario-or-check-id>/.
Use the [verification plan](verification-plan.md) for expected cases, filenames, and evidence fields.

### Reset verification and presentation limits

Test Cancel, confirmed success, injected database failure, stale drafts in another tab, and a retried reset request.
Record unchanged state after cancellation/failure and retained browser preferences after success.
Reset is a destructive demonstration action. Its dialog uses Cancel and Reset data, without a typed confirmation word.
All local tabs share the store. Another visitor's local action can change it, and version checks protect saved edits.
Remote public access, hosting, cloud accounts, and publication are outside this delivery.

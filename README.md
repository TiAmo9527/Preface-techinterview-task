# Hotel asset-management interview prototype

Owner: Alex. Target delivery: 2026-10-05.

The room manager is the primary user. The primary decision concerns required maintenance action and its ticket owner.

## Current status

Product specification v0.4 covers the 28-item readiness checklist. UI/UX specification v0.3 retains Confirmed choices and separate Proposed details.
The documentation defines 109 independent Given/When/Then scenarios. Every application scenario remains NOT RUN.
The supplied ASD-STE100 guidance controls the writing. This revision does not claim official dictionary compliance.

Assets establishes complete initial records. Independent Invoices uploads update existing room/category records.
Each room has exactly one Lighting, Water supply, and Air conditioning asset record.
Manual asset creation remains excluded and leaves part of AR-002 unmet.
Exact technical-contract review and translation review remain pending.

The required demonstration uses a Windows laptop with Chrome. Each rehearsal uses a new isolated store without clearing normal data or preferences.
Normal restart must preserve successful saves in the selected store. These behaviors are specified, not implemented.

The application remains a title-printing scaffold. Application, test, and fixture directories contain placeholders.
No working UI, dataset, passing application tests, or successful rehearsal is claimed.

## Documents

- [Product specification](docs/product-spec.md): purpose, scope, journeys, policies, decisions, and 28-item checklist.
- [Acceptance scenarios](docs/acceptance-scenarios.md): prerequisites, Given/When/Then results, and evidence references.
- [Shared glossary](docs/glossary.md): domain meanings and consistent terms.
- [UI/UX specification](docs/ui-ux-spec.md): confirmed views, separate proposals, browser context, and required checks.
- [Data contracts](docs/data-contracts.md): preserved workbook interfaces and proposed technical details.
- [Assessment requirements](docs/assessment-requirements.md): external obligations, confidentiality, and pending evidence.
- [Sample-data plan](docs/sample-data-plan.md): fictional fixtures and proposed templates.
- [Sample-generation instructions](docs/sample-excel-generation-instructions.md): one valid/invalid run with saved-file checks.
- [Delivery plan](docs/plan.md): later implementation sequence.
- [Task checklist](docs/tasks.md): completed documentation and pending application work.
- [Demo](docs/demo.md): isolated rehearsal setup and proposed twelve-minute walkthrough.
- [Documentation review](docs/spec-review.md): actual documentation checks and writing limits.
- [Repository guide](AGENTS.md): code and data boundaries.

## Startup status

The scaffold requires Python 3.11 or newer.

From the repository root, run:

```powershell
python app.py
```

This command prints the title. It does not start a web application.
Later implementation must document and check clean startup and store selection. No working demo-store command exists yet.

## Data and confidentiality

Use fictional data only. Keep business and persistence logic outside views.
Use sample_data for supplied fictional fixtures. Use ignored runtime for generated local state.
Do not commit real customer data or runtime state. Do not publish confidential assessment materials.

Optional sharing remains a separate owner decision.
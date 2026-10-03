# Hotel asset-management interview prototype

Owner: Alex. Target delivery: 2026-10-05.

The room manager reviews rooms and creates/edits maintenance records through a Maintenance-page card.
Permitted asset editing and financial overrides remain. Asset creation is through baseline imports only.
Assessor acceptance of the maintenance interpretation of asset-add/edit remains unconfirmed under AR-002.

## Current status

Product v0.5, UI v0.4, input contracts, and the local technical design are approved documentation.
The [readiness matrix](docs/spec-review.md#readiness-matrix) records prior evidence for seven artifacts.
The [approved implementation plan](docs/tasks.md) links 21 jobs across seven feature series.
The [planning review](docs/implementation-planning-review.md) records approved adaptations and pending pseudocode gates. No jobs have executed.
Application scenarios remain NOT RUN. The current application prints a title and has no working web UI.
Supplied workbooks exist in sample/2026-10-03. Their hashes, structure, and deliberate defects are inventoried.
Original generation provenance is unverified. Application import validation and rehearsal are NOT RUN.

The planned application runs entirely on localhost with FastAPI, browser modules, and SQLite.
It requires no external runtime API, API key, cloud database, or hosting account.
Normal restart preserves saves. Confirmed Reset data clears the shared demo store while retaining configuration/preferences.
English is required. Other languages remain stretch. Linguistic review remains pending.

## Documents

- [Product specification](docs/product-spec.md): scope, journeys, rules, decisions, and checklist.
- [Data contracts](docs/data-contracts.md): approved source-file interfaces.
- [Technical design](docs/technical-design.md): components, schema, transactions, endpoint shapes, and browser state.
- [UI specification](docs/ui-ux-spec.md): confirmed views, interactions, maintenance cards, and reset.
- [Acceptance scenarios](docs/acceptance-scenarios.md) and [verification mapping](docs/verification-plan.md): required outcomes and evidence methods.
- [Assessment requirements](docs/assessment-requirements.md): external obligations and pending results.
- [Sample plan](docs/sample-data-plan.md) and [fixture inventory](sample/2026-10-03/fixture-inventory.md): supplied basis and read-only evidence.
- [Optional future generation](docs/sample-excel-generation-instructions.md): preserve existing files during regeneration.
- [Delivery approach](docs/plan.md), [work-plan index](docs/tasks.md), and [pseudocode approvals](docs/pseudocode-review.md): implementation boundaries.
- [Runtime/demo procedures](docs/demo.md): future install, start, import, reset, test, and rehearsal procedures.
- [Glossary](docs/glossary.md), [agent instructions](AGENTS.md), and [readiness review](docs/spec-review.md): terminology, authority, and document evidence.

## Current scaffold command

```powershell
python app.py
```

This prints a title. It does not start the planned web application.
Use [future runtime procedures](docs/demo.md#6-local-runtime-procedures) only after implementation and verification.

## Data boundaries

Use fictional data. Preserve sample/2026-10-03 as the approved existing-fixture exception.
Future supplied fixtures belong in sample_data. Local SQLite and generated evidence belong in ignored runtime.
Keep real customer data, runtime state, and confidential assessment material uncommitted and unpublished.

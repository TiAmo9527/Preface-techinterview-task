# Hotel asset-management interview prototype

Owner: Alex. Target delivery: 2026-10-05.

The room manager reviews rooms and creates/edits maintenance records through a Maintenance-page card.
Permitted asset editing and financial overrides remain. Asset creation is through baseline imports only.
Assessor acceptance of the maintenance interpretation of asset-add/edit remains unconfirmed under AR-002.

## Current status

Product v0.5, UI v0.4, input contracts, and the local technical design are approved documentation.
The [readiness matrix](docs/spec-review.md#readiness-matrix) records prior evidence for seven artifacts.
The [approved implementation plan](docs/tasks.md) links 21 jobs across seven feature series.
The [planning review](docs/implementation-planning-review.md) records approved adaptations and pseudocode gates.
The [f001 status](docs/jobs/feature-job-reports/f001-status-local-runtime.md) records execution and remaining scope.
F001A provides the durable local store, and F001B provides validated service contracts and command boundaries.
F001C will deliver the local browser shell and reset flow; the working web UI remains pending.
The current F001 foundation run passes 346 tests, including persistence and service-boundary coverage.
Routes, imported workflows, full browser journeys, and complete application scenarios remain unverified.
Supplied workbooks exist in sample/2026-10-03. Their hashes, structure, and deliberate defects are inventoried.
Original generation provenance is unverified. Application import validation and rehearsal are NOT RUN.

The planned application runs entirely on localhost with FastAPI, browser modules, and SQLite.
It requires no external runtime API, API key, cloud database, or hosting account.
Normal restart preserves saves. Confirmed Reset data clears the shared demo store while retaining configuration/preferences.
English is required. Other languages remain stretch. Linguistic review remains pending.

## Code size

As of the F001A/F001B implementation snapshot on 2026-10-03, production Python contains **1,398 lines** across 11 files, and Python tests contain **1,148 lines** across 5 files.
Counts exclude blank lines and full-line comments. Production counts include `app.py` and `src/`; test counts include `tests/`. Documentation, configuration, and generated runtime files are excluded.

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

## Current initialization commands

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.\.venv\Scripts\python.exe app.py --init-db
.\.venv\Scripts\python.exe -m pytest tests/integration/test_runtime.py tests/integration/test_records.py
```

Use Python 3.12.5, approved after local feasibility checks. requirements.lock contains runtime packages only.
--init-db creates the supported empty store or validates and preserves an existing supported store.
It works when launched from another directory and never imports samples automatically.
Browser serving, source imports, reset UI, and feature routes remain future work.
See the [runtime procedures](docs/demo.md#6-local-runtime-procedures) and [f001 report](docs/jobs/feature-job-reports/f001-report-local-runtime.md).

## Data boundaries

Use fictional data. Preserve sample/2026-10-03 as the approved existing-fixture exception.
Future supplied fixtures belong in sample_data. Local SQLite and generated evidence belong in ignored runtime.
Keep real customer data, runtime state, and confidential assessment material uncommitted and unpublished.

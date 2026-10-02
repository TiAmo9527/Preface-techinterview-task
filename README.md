# Hotel asset-management interview prototype

Fictional hotel facilities and accountable maintenance prototype. Owner: Alex. Target delivery: 2026-10-05.

## Current status

Documentation is revised to v0.3: Assets.xlsx establishes a complete baseline, and independent Invoices.xlsx uploads update existing room/category records. Every room has exactly one lighting, one water-supply and one air-conditioning asset. Viewing/editing is retained; manual asset creation is excluded, leaving the assessment's add-asset obligation unmet. Translation verification and exact technical-contract review remain pending.

The application is not implemented: app.py prints a title, and application, test, and sample-data directories contain placeholders. No working web UI, imported dataset, passing application tests, or rehearsed demonstration is claimed.

## Documents

- [Product specification](docs/spec.md): behaviour, business rules, acceptance criteria and owner decisions.
- [Data contracts](docs/data-contracts.md): two independent workbook contracts, baseline values, invoice-update precedence, provenance and operational interfaces.
- [Assessment requirements](docs/assessment-requirements.md): external obligations, confidentiality and evidence.
- [Sample-data plan](docs/sample-data-plan.md): fictional four-location fixtures and proposed blank template layouts.
- [AI sample-generation instructions](docs/sample-excel-generation-instructions.md): self-contained prompt generating both fully populated valid and deliberately invalid baseline/update pairs in one run, with saved-file verification.
- [Delivery plan](docs/plan.md) and [tasks](docs/tasks.md): later implementation and verification backlog.
- [Demo](docs/demo.md): existing walkthrough plan and disclosures.
- [Repository guide](AGENTS.md): code/data boundaries.

## Startup status

The scaffold requires Python 3.11 or newer. From the repository root:

```powershell
python app.py
```

This command prints the scaffold title; it does not start a web application. A reproducible clean-environment startup procedure for the implemented application must be documented and verified during later work.

## Data and confidentiality

Use fictional data only. Keep domain/persistence behaviour outside views. sample_data is for fictional supplied development fixtures; generated local state belongs in ignored runtime. Do not commit real data or publish confidential assessment materials. Optional repository/application sharing is a separate later authorisation.

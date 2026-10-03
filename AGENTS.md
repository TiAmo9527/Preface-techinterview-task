# Repository Guide

## Governing documents

Before implementation, read docs/product-spec.md and docs/technical-design.md.
For imports, also read docs/data-contracts.md and docs/sample-data-plan.md.
For views, read docs/ui-ux-spec.md. For verification, read docs/verification-plan.md and the relevant docs/acceptance-scenarios.md cases.
For startup or reset, read docs/demo.md. Use docs/glossary.md for domain meanings.
External obligations are in docs/assessment-requirements.md. Preserve the unconfirmed AR-002 reinterpretation explicitly.
Product behavior, approved input contracts, technical design, UI requirements, and acceptance scenarios govern their respective concerns.
Resolve contradictions with Alex before dependent implementation. Draft docs/tasks.md is an inventory, not implementation authority.

## Pseudocode-first process

Before coding each behavior group, present pseudocode and wait for Alex's explicit approval.
Groups: persistence/reset, imports, observations/reporting, assets/overrides, maintenance, finance/display settings.
Include inputs, outputs, governing rules, validations, state changes, transactions, failure handling, and acceptance/check IDs.
Record approvals and scope in docs/pseudocode-review.md. Complete this review before coding that group.
Request renewed approval for consequential deviations. Routine choices within the approved design need no additional gate.
Documentation edits and read-only exploration can proceed under their existing authorization.
Run the mapped checks after implementation and record actual outcomes. Completion requires evidence, not checked task boxes.

## Layout and working conventions

- app.py is the entry point.
- src/views, src/services, and src/db own presentation, business behavior, and persistence.
- Keep domain and persistence logic out of views. Reuse the shared validators and transaction helper.
- tests contains automated verification. Add or update tests with behavior changes.
- sample/2026-10-03 is the approved existing-fixture basis. Preserve its workbooks and source identities.
- sample_data holds future supplied fixtures and test boundary fixtures.
- runtime holds ignored local generated state, SQLite files, and local verification evidence.
- Commit fictional supplied fixtures and documentation only within the authorized scope. Keep runtime and real customer data uncommitted.

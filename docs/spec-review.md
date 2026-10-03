# Specification documentation review

Date: 2026-10-03

Scope: Product v0.5, UI v0.4, approved input/local technical contracts, and linked repository documentation.

Status: Seven artifacts ready as documentation. Task plan deliberately Draft. Application verification: NOT RUN.
This record supersedes the earlier v0.4/v0.3 review. It preserves prior scenario and requirement identities.
It does not re-establish historical approvals, generator provenance, or previous manual writing-review claims.

## Readiness matrix

READY means the approved documents define decisions, interfaces, procedures, and verification obligations.
It does not mean application implementation, passing tests, or external assessment acceptance.

| Artifact | Status | Concrete completion evidence |
|---|---|---|
| Technical plan | READY: documentation | [Stack/ownership/trade-offs](technical-design.md#1-stack-ownership-and-trade-offs). One local process, synchronous services, SQLite, local browser modules, shared helpers. |
| Persistence design | READY: documentation | [Schema](technical-design.md#2-data-representation-and-schema) and [transactions/reset](technical-design.md#3-connections-commands-and-reset). Keys, constraints, representation, atomic histories/receipts, versions, restart and reset generations. |
| Input contracts | READY: documentation | [Approved contracts](data-contracts.md) and [actual fixture inventory](../sample/2026-10-03/fixture-inventory.md). Exact sheets/headers/types/identifiers/errors and independent import prerequisites. |
| UI implementation approach | READY: documentation | [Approved interactions](ui-ux-spec.md#4-requirements-and-approved-interaction-checks), [state ownership](technical-design.md#6-browser-state-and-ui-safeguards), and IX checks. Maintenance cards, dirty forms, refresh, localisation, and responsive/focus rules. |
| Verification plan | READY: documentation | [Scenario mapping](verification-plan.md#2-scenario-to-check-matrix). All 118 scenarios and nineteen approved interaction companions have methods and evidence obligations. |
| Task plan | DRAFT: deliberately deferred | [Draft inventory](tasks.md). Dependency-ordered bounded jobs and their completion evidence are the next planning step. |
| Agent instructions | READY: documentation | [Governing documents/process](../AGENTS.md) and [pseudocode ledger](pseudocode-review.md). Explicit review gates, group boundaries, authority, and evidence rules. |
| Runtime/demo plan | READY: documentation | [Future runtime procedures](demo.md#6-local-runtime-procedures). Install/init/start/import/reset/restart/test commands, empty-state rehearsal, retained preferences, and recorded limits. |

## Actual documentation checks

The reviewer executed local Python read-only audits against the working documents, supplied workbooks, and committed baseline.
The checks below describe document or saved-file evidence only. Application checks remain NOT RUN.

| Check | Method | Actual result |
|---|---|---|
| Local Markdown references | Resolve file targets, explicit anchors, and heading slugs | PASS. All local references resolve across eighteen Markdown documents. |
| Scenario identity and structure | Compare committed scenario IDs, then inspect Given/When/Then/trace fields | PASS. All 109 original IDs remain. Nine new infrastructure cases produce 118 unique scenarios. |
| Verification coverage | Compare scenario IDs with matrix rows and count IX checks | PASS. 118 unique scenario mappings and nineteen interaction companions. |
| Stable requirement/checklist IDs | Compare defining identities with committed versions | PASS. Five US, nineteen FR, eight SC, eight AR, nineteen UX, and 28 CL identities remain unchanged. |
| Supplied workbook structure | Read actual XLSX sheets, headers, formulas, merged cells, and identity types | PASS. Required sole sheets and approved 26/twelve-column headers. No formulas, merges, or numeric identity cells. |
| Fixture inspection consistency | Compare complete workbook table values with inspection sidecars after date normalization | PASS. All four sidecars match actual saved table values. |
| Fixture identity/content preservation | Compare SHA-256 with committed workbook bytes and record inventory hashes | PASS. All four supplied workbooks remain byte-identical. Seed namespace remains S20261002-. |
| Invalid fixture differences | Compare valid and invalid tables cell by cell | PASS. Eight changed original cells and two appended invoice rows. Inventory names actual coordinates and prerequisites. |
| Approval and policy consistency | Inspect current labels, decision record, agent gates, reset, and local-only scope | PASS. Contracts/UI proposals approved. D-019 supersedes isolated rehearsals. AR-002 interpretation remains unconfirmed externally. |
| Transaction/retry consistency | Review helper ownership, FK deletion order, receipt/version order, reset generation, and preview races | PASS: design review only. Correct transaction ordering and old-generation preview eviction are specified. |
| Prose screen | Scan non-table/non-code prose for sentences over 25 words and semicolons | PASS for this mechanical screen. Formal controlled-English compliance remains unverified. |
| Change boundaries | Inspect Git paths and compare app.py/pyproject.toml/workbooks with the baseline | PASS. Documentation and fixture inventory only. Application files and supplied XLSX files unchanged. |
| Whitespace | Run git diff --check | PASS. No whitespace errors. |

## Approval and execution boundaries

Alex's planning answers approve maintenance cards, retained asset editing, typed recorders, existing contracts, and existing UI proposals.
They approve local-only delivery, empty shared-store reset with button confirmation, fictional configuration, and pseudocode review by behavior group.
The instruction to proceed authorizes this documentation pass and the infrastructure simplifications.

No application behavior group has pseudocode approval yet. The ledger records NOT SUBMITTED, not an invented approval.
The task inventory remains Draft. This revision creates no application implementation, templates, replacement workbooks, or hosted deployment.
Future runtime commands are specified contracts. The current scaffold still only prints a title.
Formal ASD-STE100 dictionary/linter checks and linguistic review remain unverified.
Metadata, exact interfaces, Markdown tables, code blocks, and formulas are precision notation outside the prose screen.

## Remaining application and assessment work

Implement only after the required pseudocode review. Execute every applicable scenario and interaction companion on the implemented build.
Record actual startup/restart/reset, Windows/Chrome versions, numerical results, accessibility behavior, and timed rehearsal.
Original sample-generation provenance remains unverified. Structural file inspection is not application import evidence.
Assessor acceptance of maintenance add/edit as the interpretation of asset-add/edit remains unconfirmed.
Preserve the external AR-002 obligation and disclose this discrepancy until accepted by the assessor.

All application evidence groups remain NOT RUN. Documentation readiness does not remove these remaining obligations.

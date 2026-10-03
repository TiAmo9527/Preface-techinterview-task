# Assessment requirements and evidence

Version: 0.4

Revised: 2026-10-03

Owner: Alex

Target delivery: 2026-10-05, supplied by the owner.

Status: External obligations recorded. Application verification and presentation: NOT RUN.

## 1. Source and authority

Source: The supplied confidential one-page brief, “2026 Sep_Skills Test for Alex (Part-time).pdf”.
Earlier documentation records read-only inspection. This revision preserves that source record and does not claim another PDF inspection.
Do not commit the brief or publish confidential materials. This document paraphrases obligations for internal planning.

The brief defines external assessment constraints. [Product specification v0.4](product-spec.md) defines owner-selected behavior.
Record contradictions explicitly. Alex must resolve them without silently changing either requirement source.

The brief permits suitable technology and AI coding assistance. It does not require AI functionality in the application.
Owner scope uses manual monitoring and prescribed source workbooks. Live integrations and arbitrary PDF OCR remain excluded.
Assets initializes the baseline. Independent Invoices uploads update existing room/category records.

Workbook information and provenance provide evidence without a PDF requirement.
Use [the glossary](glossary.md) and [required scenarios](acceptance-scenarios.md) for consistent meaning and verification.

## 2. Obligation-to-evidence map

| ID | External obligation | Product/delivery trace | Required evidence | Current state |
|---|---|---|---|---|
| AR-001 | Fictional Hong Kong, Singapore, London, and Japan data. Consolidate invoices and separate Excel source tables into linked records. | US-01, FR-001–FR-005, SC-001, sample plan | Four-location baseline, independent invoice updates, provenance, and relationship checks. | NOT RUN. No files generated. |
| AR-002 | Working web application with import, room review, and asset add/edit. | US-01–US-03, FR-006, FR-010, FR-015, SC-002, SC-004, SC-005 | Verified startup, imports, permitted editing, restart, and explicit missing manual-creation disclosure. | NOT RUN. Manual asset creation remains unmet. |
| AR-003 | Asset type, dates, cost/currency, useful life, depreciation, book value, replacement date, and stated assumptions. | US-03, US-05, FR-011, FR-014, FR-019, SC-003 | Field review, numerical/calendar results, visible assumptions, and fixed FX date. | NOT RUN. |
| AR-004 | Portfolio filters and Lighting, Water supply, and Air conditioning room status. | US-02, FR-006–FR-009, FR-016, SC-005 | Filter consistency and independent manual observations. | NOT RUN. |
| AR-005 | Fault logging, ownership, and maintenance progress. | US-04, FR-012, FR-013, SC-004 | Creation, owner requirements, permitted transitions, rejected actions, and persistent history. | NOT RUN. |
| AR-006 | Twelve-minute import-to-maintenance walkthrough. Explain choices, validation, limitations, and AI assistance. | Existing demo, legacy SC-006 | Timed rehearsal, explanation checklist, and honest limitations. | NOT RUN. |
| AR-007 | Fictional data and confidential interview use. | Product sections 3 and 13, sample plan | Fictional-data review and artifact/publication review. | Final artifact review pending. |
| AR-008 | Optional controlled repository or application sharing. | Demo and repository overview | Authorized sharing scope, access, durability, and limits. | Optional. No sharing authorized or performed. |

### Explicit AR-002 scope gap

The brief requires asset add/edit. Alex selected exactly three fixed room/category records and excluded manual creation.
Baseline imports initialize records. Invoice imports update their values. Neither provides the omitted manual add-asset workflow.

The 2026-10-03 planning answers reconfirm this owner decision. Owner approval does not establish client acceptance of the gap.
Keep the external obligation unchanged. Disclose the unmet part in E-ASSET, E-DEMO, and submission.

Four-language scope is an owner addition, not a brief obligation.
English is mandatory. Traditional Chinese, Simplified Chinese, and Japanese remain stretch.
Alex must review delivered translations before submission or disclose missing linguistic review.

## 3. Legacy completion mapping

- v0.1 SC-001 combined four-location coverage and relationship integrity. AR-001 owns coverage. SC-001 retains integrity.
- v0.1 SC-006 maps to AR-006. SC-006 remains a traceability marker.
- SC-007 requires product acceptance evidence. This document also tracks assessment evidence.
- Atomic imports supersede valid-subset imports in SC-002. They preserve the consolidation obligation.
- The v0.3 manual-creation exclusion does not remove AR-002.

## 4. Submission and confidentiality

Prepare fictional materials and an accurate description of actual behavior.
Do not imply passing tests, reviewed translations, durable hosting, or a working application without evidence.
Windows-laptop Chrome context and isolated demo stores are owner requirements. They do not add external assessment obligations.

Optional sharing requires a separate explicit publication decision.
Do not publish assessment PDFs, real data, private context, or generated runtime state.
Disclose actual hosted persistence/reset limits if hosting occurs later.

## 5. Evidence ledger

For each applicable acceptance scenario and AR/SC identifier:

1. Record the scenario and evidence reference.
2. Record the method and prepared starting state.
3. Record the build, date, and relevant environment versions.
4. Record expected and actual outcomes.
5. Record PASS, FAIL, or NOT RUN.
6. Record omissions, failures, and limitations before submission.

Windows/Chrome version records apply to UI, startup, and demonstration evidence.
Store references and isolation outcomes apply to startup and rehearsal evidence.
Conditional stretch scenarios apply only to delivered translation sets.
Unapproved proposal checks remain separate from required acceptance results.

| Evidence group | Coverage | Status |
|---|---|---|
| E-IMPORT | AR-001, AR-002, US-01, SC-001, SC-002 | NOT RUN |
| E-ROOM | AR-004, US-02, FR-016, SC-004, SC-005 | NOT RUN |
| E-ASSET | AR-002, AR-003, US-03, FR-019, SC-003, SC-004 | NOT RUN |
| E-MAINT | AR-005, US-04, SC-004 | NOT RUN |
| E-FINANCE | AR-003, US-05, SC-003, SC-008 | NOT RUN |
| E-UI | Confirmed UX requirements, FR-017, FR-018, SC-008 | NOT RUN. Linguistic review pending. |
| E-STARTUP | AR-002, FR-015, SC-004, SC-008, clean startup, restart, and store isolation | NOT RUN |
| E-DEMO | AR-006, timed walkthrough, browser context, and rehearsal isolation | NOT RUN |
| E-CONFIDENTIAL | AR-007, AR-008 | Final artifact review pending |

Actual documentation checks appear in [the review record](spec-review.md).
They do not establish application evidence. Later actual results must replace the pending application states.

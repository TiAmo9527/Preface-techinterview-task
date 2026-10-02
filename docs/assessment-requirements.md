# Assessment requirements and evidence

Version: 0.3

Revised: 2026-10-03

Owner: Alex

Target delivery: 2026-10-05 (owner-supplied date)

Status: Obligations recorded; application and presentation evidence pending

## 1. Source and authority

Source: the supplied confidential interview brief, "2026 Sep_Skills Test for Alex (Part-time).pdf" (one page), inspected read-only. Do not commit the brief, reproduce it publicly, or publish confidential assessment materials. This document paraphrases the obligations for internal planning.

The brief sets external assessment constraints. The [product specification](spec.md) governs approved implementation behaviour within them. If a contradiction appears, record both sides and obtain an explicit owner resolution rather than silently applying precedence.

The brief permits suitable technology and AI coding assistance. That permission does not require AI functionality inside the application. Manual monitoring and structured invoice-item input are compatible with the brief; live integrations and arbitrary PDF OCR are excluded by owner scope. The v0.3 owner-approved model initialises Assets first and uploads Invoices independently to update existing room/category records. Workbook records and provenance provide invoice evidence without a PDF requirement.

## 2. Obligation-to-evidence map

| ID | Assessment obligation | Product/delivery trace | Required evidence | Current state |
|---|---|---|---|---|
| AR-001 | Small fictional data set covering Hong Kong, Singapore, London, Japan; invoices and separate Excel source tables consolidated into linked records | US-01; FR-001–005; SC-001; [sample-data plan](sample-data-plan.md) | Four-location baseline, independent invoice updates/provenance, relationship checks | Planned; no files/data generated |
| AR-002 | Working web application with import, room review, and asset add/edit | US-01–03; FR-006, FR-010, FR-015; SC-002/004/005 | Verified startup, baseline/update/edit workflows, including restart; explicitly disclose missing manual creation | Not implemented; owner scope excludes manual asset creation, so add-asset obligation remains unmet |
| AR-003 | Facility type, purchase/installation dates, cost/currency, useful life, depreciation, remaining value, replacement date; stated assumptions | US-03/05; FR-011/014/019; SC-003 | Field review, numerical/boundary results, visible assumptions and FX date | Not implemented |
| AR-004 | Portfolio filters and lighting/water/air-conditioning room status | US-02; FR-006–009/016; SC-005 | Filter consistency, room observations, manual assessment evidence | Not implemented |
| AR-005 | Fault logging, ownership, maintenance progress | US-04; FR-012–013; SC-004 | Owner/transition validations and persistent history | Not implemented |
| AR-006 | 12-minute walkthrough from import to room review and maintenance updates; explain choices, validation, limitations, AI assistance | [Existing demo plan](demo.md); legacy SC-006 | Timed rehearsal plus explanation checklist and honest limitations | Not rehearsed |
| AR-007 | Fictional data and confidentiality; materials solely for interview use | Spec §§3/13; sample-data plan | Fictional-data review and artifact/publication scope review | Constraints recorded; final artifacts pending |
| AR-008 | Optional controlled repository/application preview sharing | Demo limitations and README status | If chosen, scope/access/durability disclosure and owner-authorised sharing | Optional; no sharing authorised or performed |

### Explicit AR-002 scope gap

The brief requires asset add/edit. Alex selected exactly three fixed room/category records and removed manual asset creation while retaining view/edit. Baseline imports initialise assets, and invoice uploads update their values; neither provides the omitted manual add-asset workflow. Preserve the external obligation unchanged, mark that part unmet, and disclose the gap in E-ASSET/E-DEMO and submission. Alex explicitly authorised this scope choice in the v0.3 implementation plan; it is not client approval.

Four-language interface scope is an owner addition, not a source-brief obligation. English is mandatory; Traditional Chinese, Simplified Chinese, Japanese are stretch. Translation verification remains deferred to Alex before submission.

## 3. Legacy completion mapping

- v0.1 SC-001 contained both four-location fixture coverage and relationship integrity. AR-001 now owns coverage; product SC-001 retains integrity.
- v0.1 SC-006 maps to AR-006. Keep SC-006 as a relocation marker in the spec.
- Product SC-007 concerns product acceptance evidence; this document additionally tracks assessment-delivery evidence.
- Atomic import replaces the previous valid-subset promise in SC-002; v0.3 applies it independently to baseline and invoice uploads. It does not remove the source obligation to consolidate usable sample data.
- v0.3 removes product manual asset creation but does not remove AR-002's external add-asset obligation; track this as the explicit gap above.

## 4. Submission and confidentiality

Prepare fictional source materials and an accurate account of implemented functionality. Do not imply tests passed, translations were fluently reviewed, storage is durable, or a web app exists without evidence.

Optional repository/preview sharing requires a later explicit publication decision. Fictional examples may support that decision, but confidentiality does not permit assessment PDFs, real data, private context, or generated runtime state to be published. Keep any hosted persistence/reset limitations explicit.

## 5. Evidence ledger

For each AR/SC or acceptance scenario, record evidence reference, method, date/build, expected/actual outcome, and PASS/FAIL/NOT RUN. Record unmet criteria and limitations before submission.

Initial ledger:

| Evidence group | Coverage | Status |
|---|---|---|
| E-IMPORT | AR-001/002; US-01; SC-001/002 | NOT RUN |
| E-ROOM | AR-004; US-02; FR-016; SC-004/005 | NOT RUN |
| E-ASSET | AR-002/003; US-03; FR-019; SC-003/004 | NOT RUN |
| E-MAINT | AR-005; US-04; SC-004/005 | NOT RUN |
| E-FINANCE | AR-003; US-05; SC-003/008 | NOT RUN |
| E-UI | FR-017/018; SC-008 | NOT RUN; linguistic review deferred |
| E-STARTUP | AR-002; FR-015; SC-004 | NOT RUN |
| E-DEMO | AR-006 | NOT RUN |
| E-CONFIDENTIAL | AR-007/008 | Final review pending |

Documentation consistency checks are not execution evidence for these groups. Actual verification results must replace the pending states during later implementation and rehearsal.

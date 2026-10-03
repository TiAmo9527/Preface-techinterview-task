# Implementation planning review

Date: 2026-10-03. Target: Monday, 2026-10-05.
Status: Plan and listed adaptations APPROVED by Alex on 2026-10-03. Initial planning checks below remain historical. Current execution evidence is in the [f001 report](jobs/feature-job-reports/f001-report-local-runtime.md).

This review explains readiness and proposed adaptations. [Tasks](tasks.md) owns order, dependencies, and coverage.
It is not another task index or execution status ledger.

## Context and evidence inspected

Read root AGENTS.md and every existing governing Markdown document in docs/.
Read app.py, pyproject.toml, README.md, .gitignore, the supplied fixture inventory, and existing local review records.
Read both job-specification skills at C:/Users/alexl/.codex/skills/ and the writing-for-agents skill.
The documentation skill was not used. No jobs were executed.

Only root AGENTS.md existed before this pass. No nested instruction file was available.
In particular, docs/jobs/AGENTS.md required by both job skills was missing. This pass creates it.
Both requested job skills were available and read. The original confidential assessment PDF is not present.
Its obligations are preserved from assessment-requirements.md. This pass does not claim direct PDF inspection.

| Surface | Actual inspected state | Evidence limit |
|---|---|---|
| Application | app.py prints a title. src/db, src/services, src/views contain only .gitkeep. | No working web application. |
| Dependencies | pyproject.toml defines Python >=3.11 and pytest testpaths. No runtime dependencies or locks exist. | FastAPI/openpyxl/HTTPX/Playwright installation remains future work. |
| Tests | tests contains only .gitkeep. | No application tests or browser evidence. |
| Store | No implemented database helpers/schema. | Persistence/retry/reset design has not executed. |
| Workbooks | Four supplied XLSX files and inspection sidecars exist. Inventory records hashes and deliberate defects. | Original generation provenance and application validation remain unverified. |
| Prior audits | runtime/doc-review.json records 351 links, 118 scenario mappings, nineteen IX companions, and no failures. | Historical document/file evidence only. The earlier 109-scenario audit predates infrastructure additions. |
| Working tree | git status --short was empty before this pass. HEAD was 51b6bd3. | Baseline for planning-only change review. |
| Local interpreter | python --version returned 3.12.5. | This is not approved Python 3.11 clean-startup evidence. |

## Authority, overlap, and decisions

Product v0.5 governs behavior. Contracts v0.5 govern input interfaces.
Technical design v1.0 governs architecture. UI v0.4 governs confirmed interactions.
Acceptance v0.2 defines outcomes. Verification v1.0 defines methods and evidence.
Assessment requirements preserve external obligations. Pseudocode review owns actual algorithm approvals.

plan.md is the delivery approach, not a competing work-plan index.
tasks.md was the actual draft checklist. It now links the bounded specifications and owns planned sequencing.
spec-review.md preserves historical documentation checks. This review records the new planning pass separately.
README.md is an overview. Fixture inventory owns saved-file observations.
Generation instructions describe optional later regeneration, not permission to replace existing samples.
Repeated summaries and approval records are useful cross-references. They are not alternative authorities.

Preserve D-001–D-023, FR-001–FR-019, SC-001–SC-008, AR-001–AR-008, UX-001–UX-019, and CL-01–CL-28.
Existing UI proposals were approved. Optional reporting-date presets and stretch translations remain optional.
The proposed twelve-minute timing has no measured rehearsal evidence.
AR-002 manual asset creation remains unmet. Assessor acceptance of maintenance add/edit as its interpretation remains unconfirmed.
This gap blocks claiming full external acceptance. It does not change Alex's approved implementation scope.

## Essential architecture proposals

Reuse one FastAPI/Uvicorn process, synchronous services, SQLite, and local browser modules.
Keep the approved schema, transaction rules, internal endpoints, navigation, and financial rules.
No new external service, deployment, ORM, queue, cache, or frontend framework is proposed.

| ID | Approved planning decision | Reason and dependent work |
|---|---|---|
| P-01 | Use a small application factory with injectable store path, clock, and local configuration for tests. Production keeps the approved fixed path/launcher. **Approved by Alex, 2026-10-03.** | Isolated API/browser tests must use production helpers without resetting runtime/app.sqlite3. f001a/f001c establish this seam. It adds no production database selector. |
| P-02 | Verify multipart upload support and Asia/Hong_Kong timezone availability on Python 3.11 Windows. Pin python-multipart and tzdata if the tested runtime needs them. **Approved by Alex, 2026-10-03.** | These support approved uploads/timezone behavior. f001a selects tested versions in future locks. No dependency is changed now. |
| P-03 | Return operational room/overview data with an explicit invalid-finance diagnostic and absent financial totals when FX fails. Config/assumptions remain readable. **Approved by Alex, 2026-10-03.** | Technical endpoints do not define the nested failure shape. This keeps room understanding usable without fabricating totals. f001b defines the response shape. |
| P-04 | Use shared validation/contracts and a command coordinator in src/services. Keep SQL and the transaction helper in src/db. Thin routes remain in src/views. **Approved by Alex, 2026-10-03.** | Concrete allocation of the existing shared-helper design. f001b freezes contracts before feature services and views. File names are routine choices within these boundaries. |
| P-05 | Correct the stale product section 11 sentence that says database columns/storage types are deferred. Reference technical-design.md section 2 instead. **Approved by Alex, 2026-10-03.** | The approved technical design now defines those details. No schema change is proposed. |

P-03's response shape is approved for dependent endpoint implementation.
P-05 resolves a documentation inconsistency. It does not redesign persistence.
All six behavior groups still require separate submitted pseudocode and Alex's explicit approval.
Plan approval does not establish those approvals. Keep the ledger NOT SUBMITTED until actual submissions occur.

## Skill compatibility decisions

The installed skills are read-only inputs. This pass does not edit them.

| ID | Incompatible assumption | Adaptation and approval |
|---|---|---|
| S-01 | The writing skill requests model guidance beyond Alex's selected model. | **APPROVED by Alex, 2026-10-03:** remove those model fields. Keep only a GPT-6.1 Sol reasoning-effort recommendation in each job. Apply its reasoning gate when the runtime setting is available. If hidden, do not claim the gate was verified. |
| S-02 | Example ownership uses shared/server/ui folders. | **APPROVED by Alex, 2026-10-03:** Map shared contracts to src/services, persistence to src/db, and HTTP/browser presentation to src/views. Use tests and explicit root-file exceptions. Create no artificial layer folders. |
| S-03 | Execution requires npm run lint, typecheck, and count. No package.json or npm scripts exist. | **APPROVED by Alex, 2026-10-03:** Use pinned Python/pytest/browser commands from demo.md and targeted compileall as a syntax check. Syntax checking is not lint/typechecking. Record lint/typecheck/count as NOT RUN because the stack has no configured equivalents. Do not add tools solely to satisfy foreign-stack commands. |

S-01–S-03 are settled. Alex approved these skill adaptations on 2026-10-03.
S-03 does not waive tests or mapped browser/manual methods.
Every execution handoff must state lint, typecheck, tests, and count results or their concrete absence.

## Deadline and review gates

Monday delivery is at risk because all behavior remains unimplemented and six algorithm reviews remain pending.
There is no measured implementation velocity or confirmed hour budget. The plan makes no completion-time guarantee.
Prioritise the required English path, supplied files, local operation, and failure/retry correctness.
Defer undelivered translations, optional presets, regeneration, hosting, and publication.
Do not drop required acceptance methods to fit the deadline.

Proposed checkpoints:

1. Saturday: approve adaptations and persistence/reset pseudocode, then establish runtime and reviewed imports.
2. Sunday first checkpoint: demonstrate imported room context, observations, and maintenance ownership/progression.
3. Sunday second checkpoint: complete edits/overrides, financial integration, and installed-Chrome checks.
4. Reserve the final available session for reset/restart checks and a measured twelve-minute rehearsal.

These checkpoints are planning targets. Actual scope/time is recorded during execution in series tracking.
If a checkpoint fails, disclose remaining required work and ask Alex to choose a scope or deadline change.
Do not silently weaken approved policies or label an intermediate demonstration complete.

Alex approved the dependency plan, P-01–P-05, and S-01–S-03 on 2026-10-03.
Next, submit Persistence/reset pseudocode for f001a/f001b/f001c to Alex.
That submission must cover inputs, outputs, rules, validation, transactions, failures, retries, and mapped check IDs.
No application coding occurs in this planning pass.

## Planning verification

Executed a read-only Python audit with explicit UTF-8 after an initial Windows code-page decoding failure.
The failed attempt produced no passing result. The corrected audit completed successfully.

| Check | Actual planning result |
|---|---|
| Local links/anchors | PASS: 590 links across 46 inspected Markdown documents before this result section was added. |
| Job shape and guidance | PASS: 21 jobs retain required frontmatter/section order, one GPT-6.1 Sol reasoning field, DAG, Parallelization, and ownership. |
| Dependencies | PASS: 21 jobs have known prerequisites and an acyclic graph. Default index rows follow dependency order. |
| Series size/tracking | PASS: seven series contain 3/4/3/3/3/3/2 jobs. Planned report/status names agree. No execution artifacts exist. |
| Scenario coverage | PASS: jobs reference all 118 existing scenarios without unknown IDs. The original matrix retains nineteen IX companions. |
| Historical work | PASS: all sixteen completed-documentation items remain verbatim. Original implementation/verification inventory is retained as history. |
| Change boundaries | PASS: only Markdown changed. Protected application/dependency/configuration and governing requirement/scenario/approval files remain byte-identical. |
| Supplied data | PASS: all four XLSX files remain byte-identical to HEAD, with hashes matching the supplied inventory. No fixtures were generated. |
| Prose screen | PASS: screened new review/jobs/instructions contain no prose sentences over 25 words after precision metadata is excluded. This is a mechanical screen only. |
| Whitespace | PASS: git diff --check after removing an extra final blank line. |

Manually reviewed job ownership, default order, approval gates, deferred browser methods, and final handoff scope.
Ownership/reference lists, DAGs, model metadata, paths, and exact commands are precision notation, outside the prose screen.
Formal controlled-English dictionary compliance remains unverified. The historical review is not rewritten to imply another earlier audit.
No application tests, npm checks, installs, browser runs, or fixture generation ran during this planning pass.
Lint/typecheck/count were not run: no configured equivalents exist, and this task is planning-only.
Application implementation, startup, Chrome accessibility, and rehearsal evidence remain NOT RUN.

## f001 Persistence/reset submission verification — 2026-10-03

Recorded the [f001 submission](pseudocode-review.md#f001-persistencereset-submission) under the existing documentation authorization.
PR-01–PR-06 cover the Persistence/reset portions of f001a/f001b/f001c.
The group is SUBMITTED — PENDING APPROVAL. No algorithm approval is inferred from authorization to record the submission.
Other behavior groups remain NOT SUBMITTED. Imports and Finance/display foundations retain their separate gates.

Read the applicable instructions, governing documents, three jobs, and both job-specification skills during this review session.
Applied approved P-01–P-05 and S-01–S-03 within their recorded scopes.
The active reasoning effort was unavailable. Its comparison against each job's High recommendation remains unverified.

Rechecked HEAD 4cdd533, the clean starting tree, interpreter registrations, scaffold, and absent environment/store/lock/report files.
Python 3.11 is not registered locally. Python 3.12.5 is the available interpreter.
Existing global packages do not establish target-runtime acceptance or tested dependency pins.
The submission retains the full local prerequisite observations and evidence limits.

Used a read-only Python audit with explicit UTF-8 file reads and Git baseline comparisons.
The first audit invocation had an orchestration syntax error and ran no audit command.
Corrected the invocation and completed the audit successfully.
Repeated the audit after adding this result record.

| Check | Actual documentation result |
|---|---|
| Local links/anchors | PASS: 21 local links across the two edited documents resolve, including the submission anchor. |
| Job references/shape | PASS: three f001 jobs retain required section order and High GPT-6.1 Sol guidance. Their 30 local links resolve. |
| Scenario coverage | PASS: all 24 scenario IDs required by f001 appear in the submission. Its 25 acceptance IDs and six IX IDs are mapped. |
| Algorithm completeness | PASS: PR-01–PR-06 each specify inputs, outputs, state changes, failures/retries, and mapped IDs. Validation and transaction boundaries were reviewed. |
| Approval/history boundaries | PASS: all other group ledger rows remain verbatim. Persistence/reset is pending, with no algorithm approval recorded. |
| Fixture preservation | PASS: all four supplied workbook SHA-256 hashes still match their inventory. |
| Change boundaries | PASS: only pseudocode-review.md and this planning review changed. Application, dependency, fixture, and job files remain unchanged. |
| Execution artifacts | PASS: no series report/status or master execution artifacts were created. |
| Whitespace | PASS: git diff --check. |

Manually reviewed the exact reset deletion order, transaction ownership, receipt ordering, and browser reset/retry boundaries.
Checked separate group approvals, deferred checks, unknown transport outcomes, and the explicit AR-002 gap.
Pseudocode, identifiers, tables, paths, and precision metadata retain necessary technical notation.
Formal controlled-English dictionary compliance remains unverified.

No application changes, dependency/browser installations, job execution, or generated samples occurred.
Tests, compileall, browser/manual checks, startup, and rehearsal remain NOT RUN because this task records a review only.
Lint/typecheck/count remain NOT RUN under S-03 because this Python stack has no configured equivalents.
Documentation PASS results do not establish application acceptance.

## f001 authorized execution and runtime amendment — 2026-10-03

The preceding planning/submission checks remain historical evidence of their documentation tasks.
Alex subsequently approved Persistence/reset PR-01–PR-06: "approve pseudocode - directly work on the feature job as needed".
The [approval record](pseudocode-review.md#approval-decision-record) retains the response, date, and limited scope.

Alex's later runtime instruction was: "evaluate if we can use the current version of python as feasibility check, if can, ignore python 3.11".
Python 3.12.5 passed dependency resolution/installation, framework imports, P-02 multipart/timezone checks, and SQLite foundation integration.
It is now the tested delivery runtime. [Technical design v1.1](technical-design.md) records the runtime-only amendment; P-02 uses this runtime.
The earlier missing-Python-3.11 observations no longer block execution. No Python download was retried after Alex declined it.

Current implementation, test results, deferred checks, and provisioning outcomes are owned by the [f001 report](jobs/feature-job-reports/f001-report-local-runtime.md).
The [series status](jobs/feature-job-reports/f001-status-local-runtime.md) and [master series row](jobs/feature-job-reports/job-status.md) record progress.
The combined foundation suite passed 102 tests. This does not establish full feature or browser acceptance.
Remaining Imports and Finance/display algorithms retain their separate pseudocode gates. PR-04–PR-06 remain approved and deferred by f001c prerequisites.
AR-002 manual asset creation remains unmet; assessor acceptance of the maintenance reinterpretation remains unconfirmed.

### Execution documentation verification

The [final audit](../runtime/verification/4cdd533-f001/final-audit.json) records actual checked paths and counts.
Local links/anchors, all 21 job formats, the acyclic dependency graph, 24 f001 scenario identities, stable requirement IDs, installed lock pins, consolidated report/status/master structure, and whitespace passed.
All four supplied workbook hashes still match their inventory. No runtime state or generated evidence is included in tracked changes.
Documentation status links were refreshed without changing planned dependencies, acceptance definitions, or other group approvals.

## Jobs instruction update — 2026-10-03

Updated [docs/jobs/AGENTS.md](jobs/AGENTS.md) at Alex's request with directory-wide scope, mandatory stage-specific job skills, writing-before-execution order, and the functional-specification boundary.
Used writing-for-agents for the instruction edit. Skill references use the verified installed paths under C:/Users/alexl/.codex/skills.
The requested docs/product/requirements directory is absent; its future template/instruction references are explicit, while current root governing documents remain authoritative.
Preserved repository ownership, consolidated reporting, reasoning guidance, pseudocode gates, and approved S-03 verification adaptation.

Verification: Governing/skill references, requested instruction branches, retained safeguards, and all 21 existing job formats passed inspection. git diff --check passed.
This update changes only the jobs instructions and this documentation record. Application tests were not rerun for this instruction-only edit; prior execution results remain unchanged.

## Feature execution report rewrite — 2026-10-03

At Alex's request, used job-specification-execution to rewrite the [f001 report](jobs/feature-job-reports/f001-report-local-runtime.md) as short dated implementation entries and align its [status table](jobs/feature-job-reports/f001-status-local-runtime.md) and [master row](jobs/feature-job-reports/job-status.md).
Preserved delivered scope, pending approvals, scenario limitations, runtime amendment, provisioning outcomes, and recorded verification. Only the active f001 series has execution artifacts.
Verification: Local links/anchors, one consolidated report/status/master row, all three job statuses, and the original JUnit evidence of 58 runtime plus 44 coordinator passes checked successfully. git diff --check passed.
This is a documentation-only rewrite. No implementation, installation, or application test run occurred; lint/typecheck/count and browser/manual UI checks retain their recorded NOT RUN status.

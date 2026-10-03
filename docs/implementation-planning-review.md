# Implementation planning review

Date: 2026-10-03. Target: Monday, 2026-10-05.
Status: Plan and listed adaptations APPROVED by Alex on 2026-10-03. Application implementation and verification: NOT RUN.

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

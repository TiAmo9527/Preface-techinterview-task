# AI Jobs Directory Instructions

## Scope

These instructions apply to all files and subdirectories under `docs/jobs/`.
This folder owns bounded job specifications and consolidated execution artifacts.

Read root and docs/AGENTS.md, docs/tasks.md, and docs/implementation-planning-review.md first.

## Mandatory Skills

Work under `docs/jobs/` uses both job skills, each governing its own workflow stage.
Use the installed skill paths for this repository:

- Apply `C:/Users/alexl/.codex/skills/job-specification-writing/SKILL.md` when creating, updating, or splitting feature or bugfix job specifications.
- Apply `C:/Users/alexl/.codex/skills/job-specification-execution/SKILL.md` when implementing an existing feature or bugfix job and updating its consolidated series report, series status, and master status artifacts.
- When a task includes authoring and executing jobs, apply both skills in that order and observe each skill's scope boundaries.
- Each skill governs its own stage; neither substitutes for the other.
- When using job-specification-writing, do not use `C:/Users/alexl/.codex/skills/documentation/SKILL.md`.

For execution, also read the target job's adjacent dependencies.
Read existing series report/status files when present. Their absence before first execution is intentional.

## Functional Specification Boundary

These job skills do not govern functional specifications under `docs/product/requirements/`.
Functional specifications there must follow `docs/product/requirements/_spec-template.md` and `docs/product/requirements/AGENTS.md`.
That directory is not present in this checkout. Existing governing documents listed in root AGENTS.md remain authoritative for current work.

## Repository Job Conventions

Author feature jobs in feature-jobs/f<series><phase>-<slug>.md.
Retain the skill's exact eight-part order, DAG, Parallelization, and ownership boundaries.
Use only the GPT-6.1 Sol reasoning-effort recommendation field. Alex approved this format on 2026-10-03.
Map ownership to src/services, src/db, src/views, tests, and explicit root-file exceptions.
Do not create shared/server/ui folders to match examples.

Writing owns specifications only. It must not create or update report/status artifacts or master job-status.md.
Execution later maintains one report, one status file, and one master row per series.
Planned filenames are listed in docs/tasks.md. There are no per-subjob reports.
The task index owns dependencies and coverage. The series status file owns execution progress.

Job authoring alone authorizes no execution.
After plan approval, retain each root pseudocode gate and the execution skill's reasoning-effort gate.
Do not infer approval of all six behavior groups from approval of this plan.
Apply the Python verification adaptation S-03 approved by Alex on 2026-10-03.
Validate section order, prerequisite resolution, acyclic dependencies, ownership serialization, and scenario coverage after specification changes.

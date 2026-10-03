# Job specifications and execution artifacts

Read root and docs/AGENTS.md, docs/tasks.md, and docs/implementation-planning-review.md first.
This folder owns bounded job specifications and the execution skill's consolidated series artifacts.

For authoring, read C:/Users/alexl/.codex/skills/job-specification-writing/SKILL.md.
For execution, read C:/Users/alexl/.codex/skills/job-specification-execution/SKILL.md and the target job's adjacent dependencies.
Read existing series report/status files when present. Their absence before first execution is intentional.

Author feature jobs in feature-jobs/f<series><phase>-<slug>.md.
Retain the skill's exact eight-part order, DAG, Parallelization, and ownership boundaries.
Use only the GPT-6.1 Sol reasoning-effort recommendation field. Alex approved this format on 2026-10-03.
Map ownership to src/services, src/db, src/views, tests, and explicit root-file exceptions.
Do not create shared/server/ui folders to match examples.

Writing owns specifications only. It must not create or update report/status artifacts or master job-status.md.
Execution later maintains one report, one status file, and one master row per series.
Planned filenames are listed in docs/tasks.md. There are no per-subjob reports.
The task index owns dependencies and coverage. The series status file owns execution progress.

The current planning pass authorizes no execution.
After plan approval, retain each root pseudocode gate and the execution skill's reasoning-effort gate.
Do not infer approval of all six behavior groups from approval of this plan.
Apply the Python verification adaptation S-03 approved by Alex on 2026-10-03.
Validate section order, prerequisite resolution, acyclic dependencies, ownership serialization, and scenario coverage after specification changes.

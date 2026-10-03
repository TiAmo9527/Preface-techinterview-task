# Business behavior scope

Read root AGENTS.md, docs/product-spec.md, docs/technical-design.md, and the target execution job.
For imports, read docs/data-contracts.md and docs/sample-data-plan.md.
Read docs/glossary.md, docs/verification-plan.md, and applicable acceptance scenarios.
This folder owns validators, request/response contracts, import planning, reporting, calculations, and permitted mutations.

Implement only after the applicable behavior group's recorded pseudocode approval.
Use shared validators and the caller-owned transaction helper. Nested calls neither open transactions nor commit.
Keep HTTP rendering and browser state in src/views. Keep connection/schema mechanics in src/db.
Keep financial arithmetic in Decimal with original-day calendar clamping and approved effective-value rules.
Preserve immutable evidence and independent observations. Keep maintenance links/status boundaries explicit.
Do not add public APIs, external integrations, caches, queues, or alternate policy implementations.

Add mapped unit/integration checks beside each behavior change.
Test stale versions, retries, rollback, and unchanged-state requirements using production helpers.
Report actual checks through the execution skill's series artifacts and linked scenario evidence.

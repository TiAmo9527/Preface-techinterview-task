# Persistence scope

Read root AGENTS.md, docs/technical-design.md sections 2-4, docs/demo.md, and the target execution job.
Read docs/verification-plan.md and the applicable infrastructure scenarios before changing persistence.
This folder owns SQLite connections, schema migrations, parameterized queries, and the transaction helper.

Implement only after Persistence/reset pseudocode approval and applicable job prerequisites.
Use the approved schema and one caller-owned connection per synchronous operation.
Services own domain validation. Views own presentation. Keep those responsibilities outside this folder.
Domain writes, histories, versions, and receipts commit together through the shared helper.
Preserve normal restart and the generation-guarded reset deletion order.
Schema or transaction-policy deviations require renewed design/pseudocode review.

Use isolated on-disk stores for mapped integration tests, including busy locks and half-written rollback.
Do not reset runtime/app.sqlite3 for automated checks or commit runtime state.
Report actual checks through the execution skill's series artifacts and linked scenario evidence.

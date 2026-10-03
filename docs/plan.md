# Approved delivery approach

Version: 0.5

Revised: 2026-10-03

Owner: Alex. Target delivery: 2026-10-05.

Status: Documentation readiness completed subject to the recorded review. Application implementation and verification: NOT RUN.
The dependency-ordered implementation task plan remains [Draft](tasks.md).

## 1. Governing decisions

[Product requirements](product-spec.md) define behavior. [Contracts](data-contracts.md) define approved inputs.
[Technical design](technical-design.md) selects the local stack, persistence, internal endpoints, and shared helpers.
[UI requirements](ui-ux-spec.md) include the formerly proposed interactions, now approved.
[Assessment requirements](assessment-requirements.md) preserve external obligations and the unconfirmed AR-002 interpretation.

Use one local FastAPI/Uvicorn process, browser modules, and SQLite. No external runtime API or hosting account applies.
Manual maintenance creation/editing uses the Maintenance-page card. Permitted asset edits and financial overrides remain.
Each manual maintenance change requires a typed recorder separate from the assigned owner.
Use sample/2026-10-03 as the supplied fixture basis. Preserve its files and seeded identities.
Normal restart preserves saved data. Explicit shared-store reset clears domain data and retains preferences/configuration.

## 2. Implementation controls

Follow the [pseudocode-first approval process](pseudocode-review.md) before coding each behavior group.
Keep views thin. Services own business rules and financial calculations. Persistence owns connections and atomic transactions.
Use one service implementation for each rule, one transaction helper, and one browser state/request boundary.
Use versions/generation checks and durable command receipts for stale writes and safe retries.
Refresh actual server results after writes. Reject obsolete browser responses.

English is mandatory. Delivered stretch languages use local dictionaries and English fallback.
Alex reviews linguistic accuracy before submission or records its omission.
The fixed fictional FX/owner configuration is in the technical design.

## 3. Verification and delivery evidence

[Verification mapping](verification-plan.md) maps every scenario to automated or manual checks and evidence groups.
[Runtime/demo procedures](demo.md) define planned install, startup, imports, reset, restart, and rehearsal commands.
[Fixture inventory](../sample/2026-10-03/fixture-inventory.md) records actual supplied-file inspection and expected import outcomes.
[Readiness review](spec-review.md) records documentation checks, limitations, and the eight-artifact matrix.

Application completion requires actual scenario results, actual Windows/Chrome versions, and a timed twelve-minute rehearsal.
Disclose the unconfirmed asset-add reinterpretation and all failed or omitted checks.
Hosting and publication are outside the approved delivery.

## 4. Repository boundaries

app.py is the entry point. src/views, src/services, and src/db retain their presentation/business/persistence responsibilities.
tests contains verification. sample/2026-10-03 is the existing-fixture exception. sample_data holds future supplied fixtures.
runtime holds ignored generated local state. The current application only prints a title.
This revision changes documentation and fixture evidence only. It does not implement the planned commands or application behavior.

# f001 local runtime status

Updated: 2026-10-03. Series status: **in progress**.
Build: `4cdd533` plus uncommitted foundation changes. [Execution report](f001-report-local-runtime.md).

| Job | Status | Delivered scope / remaining work |
|---|---|---|
| [f001a](../feature-jobs/f001a-durable-local-store.md) | implemented | Persistence schema, transactions, initialization, test seams, dependency pins; 58 integration cases passed. Browser startup is outside this job's stated foundation limits. |
| [f001b](../feature-jobs/f001b-validated-command-boundaries.md) | implemented | Strict contracts for all 18 endpoints, reusable value/metadata validators, typed command/receipt boundary, local owner/FX validation, operational clock, and P-03 finance envelope; 288 F001B cases passed. Actual feature mutations/routes/UI remain downstream. |
| [f001c](../feature-jobs/f001c-browser-shell-and-reset.md) | not implemented | F001B prerequisite delivered. Scoped Finance/display browser-state approval is still required. Approved reset/browser algorithms PR-04–PR-06 remain deferred. |

Latest verification: **346 passed**, 0 failures, 1 upstream dependency warning (18.65s): 288 F001B cases plus 58 F001A regressions. Targeted compileall, pip check, and all four supplied workbook hashes passed. [Evidence](../../../runtime/verification/4cdd533-f001b-completion/environment.json). Lint/typecheck/count have no configured equivalents under S-03; browser/manual UI checks remain NOT RUN.
Python 3.12.5 is the approved tested runtime. Full scenario completion and AR-002 assessor acceptance remain pending.
[Approval scope](../../pseudocode-review.md#f001b-shared-boundary-approval--fb-01fb-03): Alex approved FB-01–FB-03 before the remaining F001B implementation. Later group algorithms remain gated. [Planned dependencies](../../tasks.md) remain unchanged.

Completion metric: **2/3 F001 jobs = 66.7%**; **2/21 approved project jobs = 9.5%**. Count only fully implemented jobs within their stated acceptance limits; partial jobs receive no credit. This is an equal-job milestone measure, not an effort estimate or completed product-acceptance percentage. Full scenario/browser acceptance remains pending; AC-US01-007 parser methods remain NOT RUN.

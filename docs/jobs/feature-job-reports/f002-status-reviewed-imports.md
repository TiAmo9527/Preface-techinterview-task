# F002 reviewed imports status

Updated: 2026-10-04. Series status: **implemented** within the approved scope and Alex's narrowed verification scope.
Verified build: `3e2eac2` plus F002A–D changes; rebased by branch creation onto tree-equivalent `origin/main` (`b288475`).
[Execution report](f002-report-reviewed-imports.md).
[Algorithm approval](../../pseudocode-review.md#f002-imports-submission--im-01im-04).

| Job | Status | Delivered scope / remaining work |
|---|---|---|
| [f002a](../feature-jobs/f002a-workbook-parser-and-templates.md) | implemented | In-memory parser, immutable normalized/source rows, diagnostics, independent assessments, warnings, blank templates; 204 targeted cases and 465 unit/integration regression cases passed. Planner/commit/browser methods remain downstream. |
| [f002b](../feature-jobs/f002b-deterministic-import-plans.md) | implemented | Read-only snapshot/planner, baseline/source/target rules, invoice precedence, reviewed histories/override effects and deterministic equality; 528 unit/integration regressions passed. Actual commits/API/browser acceptance remain F002C/D. |
| [f002c](../feature-jobs/f002c-atomic-preview-confirmation.md) | implemented | Locked 20-entry/30-minute registry, re-planning and renewed stale review, atomic entities/evidence/history/version/receipt writes, strict import endpoints, selective reset eviction, rollback/busy/race and actual process-restart retry checks. Browser/manual methods remain F002D. |
| [f002d](../feature-jobs/f002d-reviewed-import-browser-flow.md) | implemented | Independent upload/review/confirm UI; labelled counts, source diagnostics, six-field changes and override clearing; guarded pending/stale/retry flows; refreshed server counts; mapped browser methods. Installed-Chrome computer-use review omitted by Alex. |

Final F002 verification: **576 unit/integration + 66 Chromium browser = 642 passed**, 0 failures; upstream Starlette/AnyIO warning only.
Targeted compileall, pip check, templates and all four supplied hashes passed.
[Local environment/evidence](../../../runtime/verification/3e2eac2-f002d/environment.json).
Lint/typecheck/count are NOT RUN under S-03. Installed-Chrome computer-use review is NOT RUN at Alex's explicit request on 2026-10-04.
API/service/database checks confirm supplied baseline counts of 4/12/36 and invoice counts of 36/36.
The mapped import browser journeys passed. Financial recalculation/display, full room/evidence cards and integrated product acceptance remain downstream.

Completion: **4/4 F002 jobs = 100%**, **7/21 project jobs = 33.3%**.
Equal job weighting counts only completed jobs within their acceptance limits, not effort or full product acceptance.
AR-002's unconfirmed reinterpretation and omitted manual asset creation remain open.

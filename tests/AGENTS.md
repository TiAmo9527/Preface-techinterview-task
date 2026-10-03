# Verification scope

Read root AGENTS.md, docs/verification-plan.md, docs/acceptance-scenarios.md, docs/demo.md, and the target execution job.
This folder owns independent unit, service/database/API, and browser verification and shared fixture helpers.

Follow mapped methods and test_<scenario_id_lowercase_with_underscores> entry names.
Prepare each scenario independently. Test helpers use real validators and transaction helpers with temporary on-disk stores.
Inject failures after an initial write and before history/receipt completion. Inspect all relevant state before and after.
Use explicit clocks. Check before-service, month-end/leap-year, replacement horizons, FX, and unrounded totals independently.
Boundary workbooks belong in temporary test paths. Preserve sample/2026-10-03 workbooks and identities.
Browser servers use isolated stores. Never reset the shared demo store from automated tests.
Keep fixture helpers/conftest serialized unless the job names disjoint ownership explicitly.

Implement new checks within an approved job and applicable behavior approval.
Do not alter production behavior, loosen source contracts, or substitute mocks for the mapped integration evidence.
Save generated evidence under ignored runtime/verification. Record build/environment, method, expected/actual result, and omissions.
Update series reporting through the execution skill. Chromium success does not establish installed-Chrome or linguistic acceptance.

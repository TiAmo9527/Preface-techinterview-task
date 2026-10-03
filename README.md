# Hotel asset-management prototype

Owner: Alex. Target delivery: 2026-10-05.

This local website supports a fictional hotel demonstration.
F001 provides the website shell, display settings, assumptions page, and safe data reset.
Imports, room details, maintenance forms, asset editing, and financial reports require later jobs.

## Start the demonstration from zero

These instructions use Windows and Google Chrome.
Internet access is necessary for the first download and installation.
After installation, the website operates locally.

### 1. Get Python and the project

1. Install Google Chrome if it is absent.
2. Open the [Python 3.12.5 download page](https://www.python.org/downloads/release/python-3125/).
3. Select **Windows installer (64-bit)** for the tested Windows computer.
4. Open the installer.
5. Select **Add python.exe to PATH**.
6. Select **Install Now**.
7. Open the [project repository](https://github.com/TiAmo9527/Preface-techinterview-task).
8. Select the branch that contains the approved demonstration build.
9. Select **Code**.
10. Select **Download ZIP**.
11. Open the downloaded ZIP file.
12. Select **Extract all**.
13. Open the extracted folder that contains `app.py`, `README.md`, and `requirements.lock`.

Git users can clone the repository instead.
The F001C changes require `codex/f001c-browser-shell-and-reset` until the pull request is merged.

### 2. Prepare the website once

1. Right-click an empty area inside the project folder.
2. Select **Open in Terminal**.
3. Use a PowerShell tab in Windows Terminal.
4. Enter this command to check Python.

```powershell
py -3.12 --version
```

The tested version is `Python 3.12.5`.
The terminal must show the project folder before you continue.

5. Enter each command separately.
6. Wait for each command to finish before you enter the next command.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
.\.venv\Scripts\python.exe app.py --init-db
```

The first command creates the project's private Python environment.
The second command installs the required packages.
The third command creates or checks the local database.
`Store ready` confirms that the database is available.
Initialization preserves existing records.
It does not import the sample files.
You do not need to activate the Python environment.

### 3. Start each demonstration session

1. Open PowerShell in the same project folder.
2. Enter this command.

```powershell
.\.venv\Scripts\python.exe app.py
```

3. Wait for `Uvicorn running on http://127.0.0.1:8000`.
4. Keep the terminal open.
5. Open Chrome.
6. Enter [http://127.0.0.1:8000](http://127.0.0.1:8000) in the address bar.

Overview is the first page.
The website is available only on this computer.
Use one running website process at a time.

### 4. Prepare an empty demonstration

Reset removes all shared records, source evidence, and histories from this local database.
All browser tabs share this database.
Reset preserves language, currency, configuration, and the database file.

1. Open **Debugging - Assumptions**.
2. Select **Reset data**.
3. Read the deletion message.
4. Select **Cancel** if you need to retain the records.
5. Select **Reset data** if you need an empty store.
6. Wait for the saved confirmation.
7. Check that Overview is empty.
8. Check that the financial reporting date is Hong Kong today.

Discard any invalid old draft in another tab.
If reset has no confirmed result, check the website message before you retry.

### 5. Show the available features

1. Show Overview and its labelled saved counts.
2. Change Currency between **USD** and **Local transaction currency**.
3. Select a financial reporting date.
4. Select **Reset to today** to restore Hong Kong today.
5. Open **Debugging - Assumptions**.
6. Show the fictional owners, fixed exchange rates, and stated limitations.

English is the delivered language.
Other languages remain optional future work.
The financial reporting date belongs to the current browser tab.
Reload preserves that date.
A new tab starts with Hong Kong today.

Maintenance and Import currently show workflow availability messages.
The sample workbooks cannot be imported through this build.
The complete import-to-maintenance demonstration requires later jobs.

### 6. Stop and restart

1. Return to the terminal that runs the website.
2. Press **Ctrl+C**.
3. Wait for the shutdown message.
4. Run the startup command again when needed.

Normal restart preserves saved records.
Repeat package installation only when the approved requirements change.

### If startup fails

| Message or symptom | Action |
|---|---|
| `py` is not recognized | Install Python with its launcher. Reopen the terminal. |
| `app.py` or `requirements.lock` is missing | Open the extracted project folder that contains those files. |
| `.venv` Python is missing | Repeat the environment and package installation commands. |
| Package installation fails | Check the internet connection. Retry the package installation command. |
| Port 8000 is already in use | Stop the earlier website process with Ctrl+C. Start one process. |
| Chrome cannot connect | Check the running terminal. Use the exact localhost address shown above. |
| Initialization is blocked | Retain the database. Record the message before requesting help. |

## Current project status

F001A, F001B, and F001C are implemented within their approved foundation scope.
The automated suite passed **393 tests**.
Alex confirmed that the remaining F001C checks passed on 2026-10-03.
This confirmation is separate from automated evidence.

**F001 completion: 3/3 jobs, 100%. Project completion: 3/21 jobs, 14.3%.**
The percentage counts completed jobs equally.
It does not measure effort or complete product acceptance.
See the [execution status](docs/jobs/feature-job-reports/job-status.md) and [F001 report](docs/jobs/feature-job-reports/f001-report-local-runtime.md).

The application uses FastAPI, local browser files, and SQLite.
It needs no external runtime API, API key, cloud database, or hosting account.
Manual asset creation remains excluded.
Assessor acceptance of the maintenance interpretation remains unconfirmed under AR-002.
The complete workflow demonstration and timed rehearsal remain pending.

## Developer verification

Install the development packages only when you need to run tests.
The Chromium installation also requires internet access.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest tests/unit tests/integration tests/browser --browser chromium
```

Automated tests use isolated temporary databases.
They do not reset the demonstration database.
Record manual installed-Chrome checks separately from automated Chromium checks.
Lint, typecheck, and npm count have no configured equivalents under approved adaptation S-03.

## Documents

- [Product specification](docs/product-spec.md): approved behavior and boundaries.
- [Data contracts](docs/data-contracts.md): supported workbook and value interfaces.
- [Technical design](docs/technical-design.md): application, database, and browser design.
- [UI specification](docs/ui-ux-spec.md): layout and interaction requirements.
- [Acceptance scenarios](docs/acceptance-scenarios.md): required outcomes.
- [Verification plan](docs/verification-plan.md): methods and evidence requirements.
- [Assessment requirements](docs/assessment-requirements.md): external obligations and the AR-002 gap.
- [Task index](docs/tasks.md): approved job order and dependencies.
- [Pseudocode approvals](docs/pseudocode-review.md): approved algorithm scopes.
- [Demo plan](docs/demo.md): the complete future walkthrough and evidence requirements.
- [Fixture inventory](sample/2026-10-03/fixture-inventory.md): supplied workbook identities and hashes.
- [Glossary](docs/glossary.md): domain meanings.

## Data boundaries

Use fictional data only.
Preserve the supplied files in `sample/2026-10-03`.
Future supplied fixtures belong in `sample_data`.
The local database is `runtime/app.sqlite3`.
Generated verification evidence also stays in ignored `runtime`.
Keep local databases, real customer data, and confidential assessment materials out of Git commits.

## Code size

Production Python: **1509 lines across 14 files**.
Python tests: **1682 lines across 7 files**.
Browser HTML, CSS, and JavaScript: **529 lines across 6 files**.
These direct file counts exclude blank lines and full-line Python or JavaScript comments.
Counts exclude documentation, dependencies, and generated runtime files.
These counts do not come from an npm script.

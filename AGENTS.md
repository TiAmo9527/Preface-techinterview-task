# Repository Guide

## Layout

- `app.py` is the application entry point.
- `src/views`, `src/services`, and `src/db` contain presentation, business-logic, and persistence code.
- `tests` contains automated tests.
- `sample_data` holds supplied development fixtures only.
- `runtime` is for local generated state and is not committed.

## Working conventions

- Keep domain and persistence logic out of views.
- Add or update tests with behavior changes.
- Do not commit generated runtime data or real customer data.

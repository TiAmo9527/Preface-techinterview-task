"""F002B snapshots and F002C atomic service/database/API verification."""

from dataclasses import replace
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from io import BytesIO
import subprocess
import sys
from threading import Event
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from openpyxl import Workbook

from app import create_app
from src.db.import_queries import read_import_state
from src.db.store import Store
from src.services.imports import plan_import
from src.services.workbooks import NormalizedRow, ParsedWorkbook, parse_workbook
from src.services.workbooks import headers_for
from src.services.contracts import ImportConfirmRequest, ResetRequest
from src.services.errors import CommandError
from src.services.previews import PreviewRegistry, confirm_import, preview_import
from src.services.runtime import reset_store


NOW = datetime(2026, 10, 4, tzinfo=timezone.utc)


def workbook_bytes(workflow, rows):
    book = Workbook()
    sheet = book.active
    sheet.title = "Assets" if workflow == "ASSETS" else "Invoices"
    headers = headers_for(workflow)
    sheet.append(headers)
    for row in rows:
        sheet.append([row.get(key) for key in headers])
    stream = BytesIO()
    book.save(stream)
    book.close()
    return stream.getvalue()


def review(store, registry, workflow, rows=None, *, invalid=False, filename=None):
    filename = filename or ("Assets.xlsx" if workflow == "ASSETS" else "Invoices.xlsx")
    data = (SAMPLE / ("invalid" if invalid else "valid") / filename).read_bytes() if rows is None else workbook_bytes(workflow, rows)
    return preview_import(store, registry, data, filename=filename, workflow=workflow)


def confirmation(preview):
    return ImportConfirmRequest(generation_id=preview.generation_id,
                                submission_id=str(uuid4()), preview_id=preview.preview_id)


def saved(store):
    with store.transaction(write=False) as connection:
        return database_rows(connection)


def commit_review(store, registry, preview):
    return confirm_import(store, registry, confirmation(preview), clock=lambda: NOW)


@pytest.fixture
def import_store(tmp_path):
    store = Store(tmp_path / "import.sqlite3")
    store.initialize()
    return store


def invoice_row(**changes):
    return dict(supplied("INVOICES").normalized_rows[0].as_dict(), **changes)


def target_id(store, row):
    with store.transaction(write=False) as connection:
        return connection.execute("SELECT asset_id FROM assets WHERE room_id=? AND facility_type=?",
                                  (row["room_id"], row["facility_type"])).fetchone()[0]


def manager_edits(store, asset):
    with store.transaction() as connection:
        connection.execute("""UPDATE assets SET asset_name='Manager edit', override_cost='9',
            override_currency='USD', version=version+1 WHERE asset_id=?""", (asset,))
        connection.execute("UPDATE observations SET status='UNKNOWN', observed_on=NULL, recorder=NULL, note=NULL, version=version+1")
        room = connection.execute("SELECT room_id FROM assets WHERE asset_id=?", (asset,)).fetchone()[0]
        connection.execute("""INSERT INTO maintenance_tickets VALUES
            (?,?,?,'Fictional existing fault','MEDIUM','OPEN',NULL,NULL,?,?,NULL,NULL,1)""",
            (str(uuid4()), room, asset, "2026-10-04T00:00:00Z", "2026-10-04T00:00:00Z"))


def test_ac_us01_001_atomic_supplied_baseline(import_store):
    registry = PreviewRegistry(clock=lambda: NOW)
    before = saved(import_store)
    preview = review(import_store, registry, "ASSETS")
    assert saved(import_store) == before
    result = commit_review(import_store, registry, preview)
    assert (result["counts"]["properties_inserted"], result["counts"]["rooms_inserted"], result["counts"]["assets_inserted"]) == (4, 12, 36)
    after = saved(import_store)
    assert len(after["observations"]) == len(after["baseline_coordinates"]) == 36
    assert len(after["asset_baselines"]) == 36 and len(after["command_receipts"]) == 1
    assert len(after["uploads"]) == 1 and not after["invoice_items"]
    assert after["uploads"][0][3] == "2026-10-04T00:00:00Z"
    for original in supplied("ASSETS").normalized_rows:
        row = original.as_dict()
        coordinate = next(item for item in after["baseline_coordinates"] if item[5] == row["asset_id"])
        assert coordinate[1:3] == (original.source.row, "Assets")
        assert coordinate[3:5] == (row["property_id"], row["room_id"])
    reopened = Store(import_store.path)
    reopened.initialize()
    assert saved(reopened) == after


@pytest.mark.parametrize("subset", [False, True])
def test_ac_us01_002_atomic_invoice_counts(import_store, subset):
    seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    before = saved(import_store)
    rows = [invoice_row()] if subset else None
    result = commit_review(import_store, registry, review(import_store, registry, "INVOICES", rows))
    count = 1 if subset else 36
    assert result["counts"]["invoice_items_inserted"] == result["counts"]["assets_updated"] == count
    after = saved(import_store)
    assert len(after["invoice_items"]) == len(after["invoice_updates"]) == count
    assert len(after["invoice_update_refs"]) == count
    for table in ("properties", "rooms", "observations", "asset_baselines", "baseline_coordinates", "maintenance_tickets"):
        assert after[table] == before[table]
    with import_store.transaction(write=False) as connection:
        state = read_import_state(connection)
    for item in state["invoice_items"]:
        asset = next(a for a in state["assets"] if a["asset_id"] == item["asset_id"])
        assert asset["version"] == 2 and asset["applied_invoice_date"] == item["invoice_date"]
        assert asset["source_cost"] == item["acquisition_cost"]
        assert asset["source_currency"] == item["currency"]


@pytest.mark.parametrize("workflow", ["ASSETS", "INVOICES"])
def test_ac_us01_004_supplied_invalid_atomic(import_store, workflow):
    if workflow == "INVOICES": seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    before = saved(import_store)
    preview = review(import_store, registry, workflow, invalid=True)
    assert preview.counts.blockers > 0 and preview.diagnostics
    with pytest.raises(CommandError, match="domain_rule"):
        commit_review(import_store, registry, preview)
    assert saved(import_store) == before


@pytest.mark.parametrize("case", ["unknown", "changed_baseline", "value", "header", "conflict", "changed_item", "duplicate"])
def test_ac_us01_003_005_006_007_012_016_017_atomic_blockers(import_store, case):
    seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    workflow = "INVOICES"
    row = invoice_row()
    rows = [row]
    if case == "unknown": row["room_id"] = "HK-P99-R999"
    if case == "value": row["acquisition_cost"] = "-1"
    if case == "duplicate": rows.append(dict(row))
    if case == "conflict": rows.append(dict(row, line_id="conflict", asset_name="Different"))
    if case == "changed_item":
        commit_review(import_store, registry, review(import_store, registry, workflow, rows))
        row["asset_name"] = "Changed source"
    if case == "changed_baseline":
        workflow = "ASSETS"
        rows = [dict(r.as_dict()) for r in supplied(workflow).normalized_rows]
        rows[0]["asset_name"] = "Changed baseline"
    before = saved(import_store)
    if case == "header":
        preview = preview_import(import_store, registry, b"unreadable", filename="bad.xlsx", workflow=workflow)
    else:
        preview = review(import_store, registry, workflow, rows)
    assert preview.counts.blockers > 0
    with pytest.raises(CommandError) as error: commit_review(import_store, registry, preview)
    assert error.value.code == "DOMAIN_RULE"
    assert saved(import_store) == before


def test_ac_us01_008_019_warning_and_blank_installation(import_store):
    seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    row = invoice_row(installation_date=None, acquisition_cost="0", supplier_name=None)
    preview = review(import_store, registry, "INVOICES", [row])
    assert preview.counts.warnings == 3 and preview.counts.blockers == 0
    assert len(preview.asset_changes[0].changes) == 6
    commit_review(import_store, registry, preview)
    with import_store.transaction(write=False) as connection:
        asset = dict(connection.execute("SELECT * FROM assets WHERE asset_id=?", (target_id(import_store, row),)).fetchone())
        event = dict(connection.execute("SELECT * FROM invoice_updates").fetchone())
    assert asset["installation_date"] is None and asset["source_cost"] == "0"
    assert json.loads(event["before_json"])["installation_date"] is not None
    assert json.loads(event["after_json"])["installation_date"] is None


@pytest.mark.parametrize("reverse", [False, True])
def test_ac_us01_010_newest_independent_order(import_store, reverse):
    seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    rows = [invoice_row(invoice_date="2026-09-01", line_id="old", asset_name="Older"),
            invoice_row(invoice_date="2026-10-01", line_id="new", asset_name="Newest")]
    if reverse: rows.reverse()
    result = commit_review(import_store, registry, review(import_store, registry, "INVOICES", rows))
    assert result["counts"]["invoice_items_inserted"] == 2
    assert result["counts"]["assets_updated"] == result["counts"]["historical_only_items"] == 1
    with import_store.transaction(write=False) as connection:
        assert connection.execute("SELECT asset_name FROM assets WHERE asset_id=?", (target_id(import_store, rows[0]),)).fetchone()[0] == "Newest"


@pytest.mark.parametrize("case", ["older", "equivalent", "baseline_repeat", "invoice_repeat", "newer", "older_differences"])
def test_ac_us01_011_013_014_015_018_023_024_preservation(import_store, case):
    seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    row = invoice_row(invoice_date="2026-10-01")
    commit_review(import_store, registry, review(import_store, registry, "INVOICES", [row]))
    asset = target_id(import_store, row)
    manager_edits(import_store, asset)
    before = saved(import_store)
    rows = [dict(row, line_id="new")]
    workflow = "INVOICES"
    if case in ("older", "older_differences"):
        rows[0].update(invoice_date="2026-09-01", asset_name="Old different")
    if case == "older_differences": rows.append(dict(rows[0], line_id="other", asset_name="Other old"))
    if case == "invoice_repeat": rows = [row]
    if case == "baseline_repeat": workflow, rows = "ASSETS", None
    if case == "newer": rows[0]["invoice_date"] = "2026-11-01"
    preview = review(import_store, registry, workflow, rows)
    assert saved(import_store) == before
    result = commit_review(import_store, registry, preview)
    after = saved(import_store)
    for table in ("properties", "rooms", "observations", "asset_baselines", "baseline_coordinates", "maintenance_tickets"):
        assert after[table] == before[table]
    if case == "newer":
        assert preview.asset_changes[0].clears_override
        assert len(preview.asset_changes[0].changes) == 6
        assert next(change for change in preview.asset_changes[0].changes if change.field == "asset_name").before == "Manager edit"
        assert result["counts"]["assets_updated"] == 1
        assert len(after["override_history"]) == 1
        history = after["override_history"][0]
        assert history[2] == "CLEAR_ON_INVOICE" and history[6] == "SYSTEM"
        assert history[8] == after["invoice_updates"][-1][0]
        assert json.loads(history[3])["override"] == {"cost": "9", "currency": "USD"}
        assert json.loads(history[4])["override"] is None
        with import_store.transaction(write=False) as connection:
            current = dict(connection.execute("SELECT * FROM assets WHERE asset_id=?", (asset,)).fetchone())
        assert current["asset_name"] == row["asset_name"] and current["override_cost"] is None
        assert current["version"] == 4
        refs = [ref for ref in after["invoice_update_refs"] if ref[0] == history[8]]
        assert {ref[1] for ref in refs} == {"BEFORE", "AFTER"}
    else:
        assert after["assets"] == before["assets"]
        assert after["invoice_updates"] == before["invoice_updates"]
        assert after["override_history"] == before["override_history"]
        if "repeat" in case:
            assert result["upload_id"] is None
            assert after["uploads"] == before["uploads"] and after["invoice_items"] == before["invoice_items"]
        else:
            assert result["counts"]["historical_only_items"] == len(rows)


def test_ac_us01_021_stale_review_requires_confirmation(import_store):
    seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    row = invoice_row()
    preview = review(import_store, registry, "INVOICES", [row])
    manager_edits(import_store, target_id(import_store, row))
    before = saved(import_store)
    with pytest.raises(CommandError) as error: commit_review(import_store, registry, preview)
    assert error.value.code == "STALE_PREVIEW" and saved(import_store) == before
    replacement = error.value.details["preview"]
    assert replacement["preview_id"] != preview.preview_id
    assert replacement["asset_changes"][0]["clears_override"]
    request = ImportConfirmRequest(generation_id=preview.generation_id, submission_id=str(uuid4()), preview_id=replacement["preview_id"])
    result = confirm_import(import_store, registry, request, clock=lambda: NOW)
    assert result["counts"]["assets_updated"] == 1


@pytest.mark.parametrize("workflow", ["ASSETS", "INVOICES"])
def test_ac_us01_014_015_skip_review_survives_manager_edits(import_store, workflow):
    seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    row = invoice_row()
    if workflow == "INVOICES":
        commit_review(import_store, registry, review(import_store, registry, workflow, [row]))
    preview = review(import_store, registry, workflow, [row] if workflow == "INVOICES" else None)
    manager_edits(import_store, target_id(import_store, row))
    before = saved(import_store)
    result = commit_review(import_store, registry, preview)
    assert result["upload_id"] is None and result["counts"]["assets_updated"] == 0
    after = saved(import_store)
    after.pop("command_receipts")
    before.pop("command_receipts")
    assert after == before


@pytest.mark.parametrize("rows", [[], [{}]])
def test_ac_us01_022_noop_receipt_only(import_store, rows):
    registry = PreviewRegistry(clock=lambda: NOW)
    before = saved(import_store)
    preview = review(import_store, registry, "ASSETS", rows)
    assert saved(import_store) == before  # abandoning/cancelling the review performs no command
    result = commit_review(import_store, registry, preview)
    assert not any(result["counts"].values()) and result["upload_id"] is None
    after = saved(import_store)
    assert len(after.pop("command_receipts")) == 1
    before.pop("command_receipts")
    assert after == before


def test_ac_us01_025_new_room_coordinates(import_store):
    seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    parsed = supplied("ASSETS")
    room = parsed.normalized_rows[0].as_dict()["room_id"]
    rows = [dict(row.as_dict()) for row in parsed.normalized_rows if row.as_dict()["room_id"] == room]
    for row in rows:
        row["room_id"] = room.rsplit("-R", 1)[0] + "-R999"
        row["asset_id"] = row["room_id"] + "-A" + row["asset_id"].rsplit("-A", 1)[1]
        row["room_number"] = "999"
    result = commit_review(import_store, registry, review(import_store, registry, "ASSETS", rows, filename="new-room.xlsx"))
    assert (result["counts"]["properties_inserted"], result["counts"]["rooms_inserted"], result["counts"]["assets_inserted"]) == (0, 1, 3)
    coordinates = [item for item in saved(import_store)["baseline_coordinates"] if item[0] == result["upload_id"]]
    assert len(coordinates) == 3 and {item[1] for item in coordinates} == {2, 3, 4}


def test_ac_us01_023_first_invoice_before_baseline_purchase(import_store):
    seed_baseline(import_store)
    registry = PreviewRegistry(clock=lambda: NOW)
    row = invoice_row(invoice_date="2000-01-01")
    asset = target_id(import_store, row)
    with import_store.transaction(write=False) as connection:
        assert connection.execute("SELECT purchase_date FROM assets WHERE asset_id=?", (asset,)).fetchone()[0] > row["invoice_date"]
    result = commit_review(import_store, registry, review(import_store, registry, "INVOICES", [row]))
    assert result["counts"]["assets_updated"] == 1


def test_ac_infra_007_actual_process_restart_receipt(import_store):
    registry = PreviewRegistry(clock=lambda: NOW)
    command = confirmation(review(import_store, registry, "ASSETS"))
    result = confirm_import(import_store, registry, command)
    pending = confirmation(review(import_store, registry, "INVOICES"))
    before = saved(import_store)
    # A separate Python process constructs a fresh app/registry against the persisted store.
    script = """
import json, sys
from pathlib import Path
from app import create_app
from fastapi.testclient import TestClient
with TestClient(create_app(store_path=Path(sys.argv[1]))) as client:
    replay = client.post('/api/imports/confirm', json=json.loads(sys.argv[2]))
    missing = client.post('/api/imports/confirm', json=json.loads(sys.argv[3]))
    print(json.dumps({'replay': replay.json(), 'status': replay.status_code,
                      'missing': missing.json(), 'missing_status': missing.status_code}))
"""
    process = subprocess.run([sys.executable, "-c", script, str(import_store.path),
                              command.model_dump_json(), pending.model_dump_json()],
                             cwd=ROOT, capture_output=True, text=True, timeout=30, check=True)
    output = json.loads(process.stdout)
    assert output["status"] == 200 and output["replay"] == result
    assert output["missing_status"] == 409 and output["missing"]["code"] == "PREVIEW_EXPIRED"
    assert saved(import_store) == before


@pytest.mark.parametrize("stage", ["asset_baselines", "invoice_updates", "override_history", "command_receipts"])
def test_ac_us01_020_ac_infra_008_rollback(import_store, stage):
    registry = PreviewRegistry(clock=lambda: NOW)
    workflow = "ASSETS"
    if stage != "asset_baselines":
        seed_baseline(import_store)
        manager_edits(import_store, target_id(import_store, invoice_row()))
        workflow = "INVOICES"
    preview = review(import_store, registry, workflow)
    with import_store.transaction() as connection:
        connection.execute(f"CREATE TRIGGER injected_failure BEFORE INSERT ON {stage} BEGIN SELECT RAISE(ABORT, 'injected'); END")
    before = saved(import_store)
    request = confirmation(preview)
    with pytest.raises(CommandError) as error: confirm_import(import_store, registry, request)
    assert error.value.code == "SAVE_FAILED" and saved(import_store) == before
    with import_store.transaction() as connection: connection.execute("DROP TRIGGER injected_failure")
    assert confirm_import(import_store, registry, request)["upload_id"] is not None


def test_ac_infra_008_import_busy_lock(import_store):
    registry = PreviewRegistry(clock=lambda: NOW)
    request = confirmation(review(import_store, registry, "ASSETS"))
    before = saved(import_store)
    with import_store.transaction():
        with pytest.raises(CommandError) as error: confirm_import(import_store, registry, request)
    assert error.value.code == "STORE_BUSY" and saved(import_store) == before
    assert confirm_import(import_store, registry, request)["counts"]["assets_inserted"] == 36


@pytest.mark.parametrize("loss", ["expiry", "eviction", "restart"])
def test_ac_infra_007_lifetime_and_receipt(import_store, loss):
    time = [NOW]
    registry = PreviewRegistry(clock=lambda: time[0])
    committed = confirmation(review(import_store, registry, "ASSETS"))
    result = confirm_import(import_store, registry, committed)
    pending = confirmation(review(import_store, registry, "INVOICES"))
    if loss == "expiry": time[0] += timedelta(minutes=30)
    if loss == "eviction":
        for _ in range(20): review(import_store, registry, "ASSETS", [])
    if loss == "restart":
        registry = PreviewRegistry(clock=lambda: NOW)
        import_store = Store(import_store.path)
        import_store.initialize()
    before = saved(import_store)
    with pytest.raises(CommandError) as error: confirm_import(import_store, registry, pending)
    assert error.value.code == "PREVIEW_EXPIRED" and saved(import_store) == before
    assert confirm_import(import_store, registry, committed) == result
    assert saved(import_store) == before
    conflicting = committed.model_copy(update={"preview_id": str(uuid4())})
    with pytest.raises(CommandError) as error: confirm_import(import_store, registry, conflicting)
    assert error.value.code == "SUBMISSION_CONFLICT"


def test_ac_infra_005_selective_reset_race(import_store):
    registry = PreviewRegistry(clock=lambda: NOW)
    old = review(import_store, registry, "ASSETS")
    committed = Event()
    cleanup = Event()

    def delayed_eviction(generation):
        committed.set()
        assert cleanup.wait(10)
        registry.evict_generation(generation)

    with ThreadPoolExecutor() as pool:
        future = pool.submit(reset_store, import_store, ResetRequest(generation_id=old.generation_id, confirm=True), evict_previews=delayed_eviction)
        assert committed.wait(10)
        new = review(import_store, registry, "ASSETS")
        cleanup.set()
        result = future.result(timeout=10)
    assert new.generation_id == result.generation_id
    before = saved(import_store)
    with pytest.raises(CommandError) as error: commit_review(import_store, registry, old)
    assert error.value.code == "STALE_STORE" and saved(import_store) == before
    assert commit_review(import_store, registry, new)["counts"]["assets_inserted"] == 36


def test_ac_infra_007_concurrent_same_submission(import_store):
    registry = PreviewRegistry(clock=lambda: NOW)
    request = confirmation(review(import_store, registry, "ASSETS"))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: confirm_import(import_store, registry, request), range(2)))
    assert results[0] == results[1]
    after = saved(import_store)
    assert len(after["uploads"]) == len(after["command_receipts"]) == 1


def test_ac_infra_007_registry_thread_safety(import_store):
    registry = PreviewRegistry(clock=lambda: NOW)
    with ThreadPoolExecutor(max_workers=8) as pool:
        previews = list(pool.map(lambda _: review(import_store, registry, "ASSETS", []), range(40)))
    assert len({preview.preview_id for preview in previews}) == 40
    retained = 0
    for preview in previews:
        try:
            registry.get(preview.preview_id, preview.generation_id)
            retained += 1
        except CommandError as error:
            assert error.code == "PREVIEW_EXPIRED"
    assert retained == 20
    assert not saved(import_store)["command_receipts"]


def test_ac_infra_005_confirm_then_reset_serializes(import_store, monkeypatch):
    import src.services.previews as module
    registry = PreviewRegistry(clock=lambda: NOW)
    preview = review(import_store, registry, "ASSETS")
    writing = Event()
    release = Event()
    writer = module.write_import_plan

    def paused_writer(*args, **kwargs):
        writing.set()
        assert release.wait(10)
        return writer(*args, **kwargs)

    monkeypatch.setattr(module, "write_import_plan", paused_writer)
    with ThreadPoolExecutor(max_workers=2) as pool:
        confirm = pool.submit(commit_review, import_store, registry, preview)
        assert writing.wait(10)
        reset = pool.submit(reset_store, import_store, ResetRequest(generation_id=preview.generation_id, confirm=True), evict_previews=registry.evict_generation)
        release.set()
        assert confirm.result(timeout=10)["counts"]["assets_inserted"] == 36
        assert reset.result(timeout=10).generation_id != preview.generation_id
    assert not saved(import_store)["assets"] and not saved(import_store)["command_receipts"]
    with pytest.raises(CommandError) as error: commit_review(import_store, registry, preview)
    assert error.value.code == "STALE_STORE"


def test_ac_infra_005_preview_snapshot_then_reset(import_store, monkeypatch):
    registry = PreviewRegistry(clock=lambda: NOW)
    adding = Event()
    release = Event()
    original = registry.add

    def paused_add(*args):
        adding.set()
        assert release.wait(10)
        return original(*args)

    monkeypatch.setattr(registry, "add", paused_add)
    generation = import_store.metadata().generation_id
    with ThreadPoolExecutor(max_workers=2) as pool:
        preview_future = pool.submit(review, import_store, registry, "ASSETS")
        assert adding.wait(10)
        reset_future = pool.submit(reset_store, import_store, ResetRequest(generation_id=generation, confirm=True), evict_previews=registry.evict_generation)
        release.set()
        preview = preview_future.result(timeout=10)
        reset_future.result(timeout=10)
    with pytest.raises(CommandError) as error: registry.get(preview.preview_id, generation)
    assert error.value.code == "PREVIEW_EXPIRED"
    with pytest.raises(CommandError) as error: commit_review(import_store, registry, preview)
    assert error.value.code == "STALE_STORE"


def test_ac_us01_009_http_boundary_and_replay(tmp_path, monkeypatch):
    application = create_app(store_path=tmp_path / "api.sqlite3", clock=lambda: NOW)
    import src.services.previews as module
    parse = module.parse_workbook
    calls = []

    def counted(*args, **kwargs):
        calls.append(True)
        return parse(*args, **kwargs)

    monkeypatch.setattr(module, "parse_workbook", counted)
    with TestClient(application) as client:
        data = (SAMPLE / "valid" / "Assets.xlsx").read_bytes()
        response = client.post("/api/imports/preview", data={"workflow": "ASSETS"}, files={"file": ("Assets.xlsx", data)})
        assert response.status_code == 200 and response.headers["cache-control"] == "no-store"
        preview = response.json()
        command = {"generation_id": preview["generation_id"], "preview_id": preview["preview_id"], "submission_id": str(uuid4())}
        before = saved(application.state.store)
        assert client.post("/api/imports/confirm", json=dict(command, rows=[])).status_code == 422
        assert saved(application.state.store) == before
        result = client.post("/api/imports/confirm", json=command)
        assert result.status_code == 200 and result.json()["counts"]["assets_inserted"] == 36
        application.state.preview_registry = PreviewRegistry(clock=lambda: NOW)
        assert client.post("/api/imports/confirm", json=command).json() == result.json()
        assert len(calls) == 1
        assert client.post("/api/imports/preview", data={"workflow": "INVALID"}, files={"file": ("Assets.xlsx", data)}).status_code == 422
        assert client.post("/api/imports/preview", data={"workflow": "ASSETS"}).status_code == 422
        assert client.post("/api/imports/preview", data={"workflow": "ASSETS", "rows": "replacement"}, files={"file": ("Assets.xlsx", data)}).status_code == 422
        assert client.post("/api/imports/preview", data={"workflow": "ASSETS"}, files=[("file", ("one.xlsx", data)), ("file", ("two.xlsx", data))]).status_code == 422
        reset = client.post("/api/reset", json={"generation_id": command["generation_id"], "confirm": True})
        assert reset.status_code == 200
        obsolete = client.post("/api/imports/confirm", json=command)
        assert obsolete.status_code == 409 and obsolete.json()["code"] == "STALE_STORE"


@pytest.mark.parametrize("case", ["blocker", "expired", "stale", "receipt_conflict", "write_failure"])
def test_ac_us01_020_021_ac_infra_007_http_errors(tmp_path, case):
    application = create_app(store_path=tmp_path / "http-errors.sqlite3", clock=lambda: NOW)
    with TestClient(application) as client:
        if case == "stale": seed_baseline(application.state.store)
        workflow = "INVOICES" if case == "stale" else "ASSETS"
        data = workbook_bytes("ASSETS", [{}]) if case == "expired" else (SAMPLE / ("invalid" if case == "blocker" else "valid") / ("Invoices.xlsx" if case == "stale" else "Assets.xlsx")).read_bytes()
        preview = client.post("/api/imports/preview", data={"workflow": workflow}, files={"file": ("source.xlsx", data)}).json()
        command = {"generation_id": preview["generation_id"], "preview_id": preview["preview_id"], "submission_id": str(uuid4())}
        expected = {"blocker": (422, "DOMAIN_RULE"), "expired": (409, "PREVIEW_EXPIRED"),
                    "stale": (409, "STALE_PREVIEW"), "receipt_conflict": (409, "SUBMISSION_CONFLICT"),
                    "write_failure": (500, "SAVE_FAILED")}[case]
        if case == "expired": command["preview_id"] = str(uuid4())
        if case == "stale": manager_edits(application.state.store, target_id(application.state.store, invoice_row()))
        if case == "receipt_conflict":
            assert client.post("/api/imports/confirm", json=command).status_code == 200
            command["preview_id"] = str(uuid4())
        if case == "write_failure":
            with application.state.store.transaction() as connection:
                connection.execute("CREATE TRIGGER fail_receipt BEFORE INSERT ON command_receipts BEGIN SELECT RAISE(ABORT, 'failure'); END")
        before = saved(application.state.store)
        response = client.post("/api/imports/confirm", json=command)
        assert (response.status_code, response.json()["code"]) == expected
        assert response.json()["generation_id"] == command["generation_id"]
        assert response.headers["cache-control"] == "no-store"
        assert saved(application.state.store) == before


ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "sample" / "2026-10-03"


def supplied(workflow, invalid=False):
    filename = "Assets.xlsx" if workflow == "ASSETS" else "Invoices.xlsx"
    path = SAMPLE / ("invalid" if invalid else "valid") / filename
    return parse_workbook(path.read_bytes(), filename=filename, workflow=workflow)


def seed_baseline(store):
    """Independent fixture insertion on real production transactions, no import commit claim."""
    parsed = supplied("ASSETS")
    plan = plan_import(parsed, dict(properties=[], rooms=[], assets=[], invoice_items=[])).as_dict()
    with store.transaction() as connection:
        connection.execute("INSERT INTO uploads VALUES ('fixture', 'ASSETS', 'Assets.xlsx', '2026-10-04T00:00:00Z')")
        for row in plan["properties"]:
            connection.execute("INSERT INTO properties VALUES (?,?,?,?)", tuple(row[key] for key in ("property_id", "property_name", "location", "city")))
        for row in plan["rooms"]:
            connection.execute("INSERT INTO rooms VALUES (?,?,?,?)", (row["room_id"], row["property_id"], row["room_number"], json.dumps(row["assessments"])))
            for system, observation in row["assessments"].items():
                connection.execute("INSERT INTO observations VALUES (?,?,?,?,?,?,1)", (row["room_id"], system, *(observation[key] for key in ("status", "observed_on", "recorder", "note"))))
        for row in plan["assets"]:
            snap = row["baseline"]
            connection.execute("INSERT INTO assets VALUES (?,?,?,?,?,?,?,NULL,?,?,NULL,NULL,1)",
                               (row["asset_id"], row["room_id"], row["facility_type"], *(snap[key] for key in ("asset_name", "purchase_date", "installation_date", "useful_life_months", "acquisition_cost", "currency"))))
            connection.execute("INSERT INTO asset_baselines VALUES (?,?)", (row["asset_id"], json.dumps(snap)))
        for row in parsed.normalized_rows:
            values = row.as_dict()
            connection.execute("INSERT INTO baseline_coordinates VALUES ('fixture',?,'Assets',?,?,?)", (row.source.row, values["property_id"], values["room_id"], values["asset_id"]))


def changed(parsed, **values):
    row = parsed.normalized_rows[0]
    return replace(parsed, normalized_rows=(NormalizedRow(row.source, tuple(dict(row.as_dict(), **values).items())),))


def database_rows(connection):
    names = [row[0] for row in connection.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name")]
    return {name: [tuple(row) for row in connection.execute(f"SELECT * FROM {name} ORDER BY rowid")] for name in names}


@pytest.mark.parametrize("scenario", ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "021", "022", "023", "024", "025"])
def test_ac_us01_planner_snapshot_read_only(tmp_path, scenario):
    store = Store(tmp_path / "isolated.sqlite3")
    store.initialize()
    if scenario not in ("001", "004"):
        seed_baseline(store)
    parsed = supplied("ASSETS" if scenario in ("001", "004", "005", "014", "025") else "INVOICES", invalid=scenario in ("003", "004", "006", "007", "012", "017"))
    with store.transaction(write=False) as connection:
        state = read_import_state(connection)
    if scenario == "005": parsed = changed(parsed, asset_name="Changed baseline")
    if scenario in ("002", "008", "009", "010", "011", "013", "015", "016", "018", "019", "021", "023", "024"):
        parsed = changed(supplied("INVOICES"))
    if scenario in ("008", "019"):
        parsed = changed(parsed, installation_date=None)
    if scenario == "022": parsed = replace(parsed, normalized_rows=(), source_rows=(), diagnostics=())
    # Seed accepted invoice evidence/manager edits independently for precedence/repeat cases.
    if scenario in ("011", "013", "015", "016", "018", "021", "023", "024"):
        value = parsed.normalized_rows[0].as_dict()
        asset = next(a for a in state["assets"] if (a["room_id"], a["facility_type"]) == (value["room_id"], value["facility_type"]))
        snapshot = {key: value[key] for key in ("asset_name", "purchase_date", "installation_date", "useful_life_months", "acquisition_cost", "currency")}
        with store.transaction() as connection:
            connection.execute("INSERT INTO uploads VALUES ('invoice-fixture','INVOICES','Invoices.xlsx','2026-10-04T00:00:00Z')")
            connection.execute("INSERT INTO invoice_items VALUES (?,?,?,?,?,?,?,?,?,?,?)", (value["invoice_id"], value["line_id"], asset["asset_id"], value["room_id"], value["facility_type"], json.dumps(snapshot), value["invoice_date"], value["supplier_name"], "invoice-fixture", "Invoices", 2))
            connection.execute("""UPDATE assets SET applied_invoice_date=?, asset_name='Manager edit',
                               purchase_date=?, installation_date=?, useful_life_months=?,
                               source_cost=?, source_currency=?, override_cost='9',
                               override_currency='USD', version=2 WHERE asset_id=?""",
                               (value["invoice_date"], value["purchase_date"], value["installation_date"],
                                value["useful_life_months"], value["acquisition_cost"], value["currency"], asset["asset_id"]))
        if scenario != "015": parsed = changed(parsed, line_id="new-identity")
        if scenario in ("011", "024"): parsed = changed(parsed, invoice_date="2020-01-01", asset_name="Older difference")
        if scenario in ("018", "021", "023"): parsed = changed(parsed, invoice_date="2030-01-01")
        if scenario == "016": parsed = changed(parsed, line_id=value["line_id"], asset_name="Changed evidence")
    with store.transaction(write=False) as connection:
        before = database_rows(connection)
        state = read_import_state(connection)
        plan = plan_import(parsed, state)
        assert database_rows(connection) == before
        assert plan == plan_import(replace(parsed, normalized_rows=tuple(reversed(parsed.normalized_rows))), state)
    assert store.metadata().generation_id == before["store_metadata"][0][2]
    if scenario == "001":
        assert (plan.counts["properties_inserted"], plan.counts["rooms_inserted"], plan.counts["assets_inserted"]) == (4, 12, 36)
    if scenario in ("003", "004", "005", "006", "007", "012", "016", "017"):
        assert plan.blocked and not plan.as_dict()["asset_updates"] and not plan.as_dict()["invoice_items"]
    if scenario in ("011", "013", "024"):
        assert plan.counts["historical_only_items"] == 1 and plan.counts["assets_updated"] == 0
    if scenario in ("014", "015"):
        assert plan.counts["skips"] == (36 if scenario == "014" else 1)
    if scenario == "009": assert len(plan.as_dict()["asset_updates"][0]["changes"]) == 6
    if scenario == "018": assert plan.as_dict()["asset_updates"][0]["clears_override"]
    if scenario == "019": assert plan.as_dict()["asset_updates"][0]["after"]["installation_date"] is None
    if scenario == "021":
        target = plan.as_dict()["asset_updates"][0]["asset_id"]
        next(a for a in state["assets"] if a["asset_id"] == target)["override_cost"] = "10"
        assert plan != plan_import(parsed, state)
    if scenario == "022": assert not any(plan.counts.values())
    if scenario == "023": assert plan.counts["assets_updated"] == 1


def test_ac_us01_002_supplied_invoice_counts(tmp_path):
    store = Store(tmp_path / "isolated.sqlite3")
    store.initialize()
    seed_baseline(store)
    with store.transaction(write=False) as connection:
        plan = plan_import(supplied("INVOICES"), read_import_state(connection))
    assert not plan.blocked
    assert (plan.counts["invoice_items_inserted"], plan.counts["assets_updated"]) == (36, 36)

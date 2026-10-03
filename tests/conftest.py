"""Independent on-disk state for persistence foundation checks."""

from datetime import datetime, timezone
import hashlib
import json
from uuid import uuid4
import socket
from threading import Thread
import time

import pytest

from src.db import Store


def pytest_configure(config):
    # Mapped integration/browser files intentionally share test_runtime.py.
    # Import by qualified path so the prescribed full-suite command collects both.
    if config.option.importmode == 'prepend':
        config.option.importmode = 'importlib'


@pytest.fixture
def runtime_server(store, clock):
    """One production Uvicorn server and isolated on-disk store per browser case."""
    import uvicorn
    from app import create_app
    application = create_app(store_path=store.path, clock=clock)
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(application, host='127.0.0.1', port=port, log_level='error'))
    thread = Thread(target=server.run, kwargs={'sockets': [sock]}, daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started and thread.is_alive() and time.monotonic() < deadline:
        time.sleep(.02)
    if not server.started:
        server.should_exit = True
        thread.join(timeout=10)
        sock.close()
        raise RuntimeError('Isolated browser server failed to start')
    yield {'url': f'http://127.0.0.1:{port}', 'app': application, 'store': store}
    server.should_exit = True
    thread.join(timeout=10)
    sock.close()
    assert not thread.is_alive(), 'Browser server did not stop'


def json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


@pytest.fixture
def clock():
    return lambda: datetime(2026, 10, 3, 8, 30, tzinfo=timezone.utc)


@pytest.fixture
def local_config():
    # Configuration interpretation/validation remains with f001b and its separate approval.
    return {"fixture": "fictional", "nested": {"isolated": True}}


@pytest.fixture
def store(tmp_path):
    result = Store(tmp_path / "store.sqlite3")
    result.initialize()
    return result


@pytest.fixture
def seeded_store(store, clock):
    """Prepare all persisted surfaces directly, without executing another scenario."""
    happened_at = clock().isoformat().replace("+00:00", "Z")
    generation = store.metadata().generation_id
    baseline = {
        "asset_name": "Fictional LIGHTING", "purchase_date": "2026-01-15",
        "installation_date": None, "useful_life_months": 12,
        "acquisition_cost": "1200.25", "currency": "USD",
    }
    invoice = {**baseline, "asset_name": "Replacement lamp", "acquisition_cost": "9007199254740993.125"}
    with store.transaction() as connection:
        connection.execute("INSERT INTO properties VALUES (?, ?, ?, ?)",
                           ("HK-P01", "Fictional hotel", "HONG_KONG", "Hong Kong"))
        assessments = {system: {"status": "UNKNOWN", "observed_on": None, "recorder": None, "note": None}
                       for system in ("LIGHTING", "WATER_SUPPLY", "AIR_CONDITIONING")}
        connection.execute("INSERT INTO rooms VALUES (?, ?, ?, ?)",
                           ("HK-P01-R001", "HK-P01", "001", json_text(assessments)))
        connection.execute("INSERT INTO uploads VALUES (?, ?, ?, ?)", ("baseline-upload", "ASSETS", "Assets.xlsx", happened_at))
        connection.execute("INSERT INTO uploads VALUES (?, ?, ?, ?)", ("invoice-upload", "INVOICES", "Invoices.xlsx", happened_at))
        for index, category in enumerate(("LIGHTING", "WATER_SUPPLY", "AIR_CONDITIONING"), 1):
            asset_id = f"HK-P01-R001-A{index:03d}"
            snapshot = {**baseline, "asset_name": f"Fictional {category}"}
            connection.execute(
                "INSERT INTO assets (asset_id, room_id, facility_type, asset_name, purchase_date, installation_date, "
                "useful_life_months, source_cost, source_currency, version) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (asset_id, "HK-P01-R001", category, snapshot["asset_name"], "2026-01-15", None, 12, "1200.25", "USD", 1),
            )
            connection.execute("INSERT INTO asset_baselines VALUES (?, ?)", (asset_id, json_text(snapshot)))
            connection.execute("INSERT INTO observations VALUES (?, ?, ?, ?, ?, ?, ?)",
                               ("HK-P01-R001", category, "UNKNOWN", None, None, None, 1))
            connection.execute("INSERT INTO baseline_coordinates VALUES (?, ?, ?, ?, ?, ?)",
                               ("baseline-upload", index + 1, "Assets", "HK-P01", "HK-P01-R001", asset_id))
        connection.execute(
            "INSERT INTO invoice_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("INVOICE-0001", "001", "HK-P01-R001-A001", "HK-P01-R001", "LIGHTING", json_text(invoice),
             "2026-10-01", "Fictional supplier", "invoice-upload", "Invoices", 2),
        )
        connection.execute(
            "UPDATE assets SET asset_name=?, source_cost=?, applied_invoice_date=?, version=2 WHERE asset_id=?",
            (invoice["asset_name"], invoice["acquisition_cost"], "2026-10-01", "HK-P01-R001-A001"),
        )
        before = {"snapshot": baseline, "source_cost": "1200.25", "source_currency": "USD", "override": None,
                  "effective_cost": "1200.25", "effective_currency": "USD", "applied_invoice_date": None}
        after = {"snapshot": invoice, "source_cost": invoice["acquisition_cost"], "source_currency": "USD", "override": None,
                 "effective_cost": invoice["acquisition_cost"], "effective_currency": "USD", "applied_invoice_date": "2026-10-01"}
        connection.execute("INSERT INTO invoice_updates VALUES (?, ?, ?, ?, ?, ?, ?)",
                           ("invoice-event", "HK-P01-R001-A001", "2026-10-01", json_text(before), json_text(after), "invoice-upload", happened_at))
        connection.execute("INSERT INTO invoice_update_refs VALUES (?, ?, ?, ?)", ("invoice-event", "AFTER", "INVOICE-0001", "001"))
        connection.execute("UPDATE assets SET override_cost='987.65', override_currency='GBP', version=3 WHERE asset_id=?",
                           ("HK-P01-R001-A001",))
        override_after = {**after, "override": {"cost": "987.65", "currency": "GBP"}, "effective_cost": "987.65", "effective_currency": "GBP"}
        connection.execute("INSERT INTO override_history VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           ("override-event", "HK-P01-R001-A001", "SET_OVERRIDE", json_text(after), json_text(override_after),
                            "Fictional correction", "Fixture recorder", happened_at, None))
        connection.execute(
            "INSERT INTO maintenance_tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("ticket-1", "HK-P01-R001", "HK-P01-R001-A001", "Fictional fault", "MEDIUM", "IN_PROGRESS",
             "owner-alex", "2026-10-04", happened_at, happened_at, None, None, 2),
        )
        for version, action in ((1, "CREATE"), (2, "START")):
            connection.execute("INSERT INTO maintenance_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (f"ticket-event-{version}", "ticket-1", action, json_text({"version": version - 1}),
                                json_text({"version": version, "status": "OPEN" if version == 1 else "IN_PROGRESS"}),
                                "Fixture recorder", happened_at, version))
        connection.execute("INSERT INTO command_receipts VALUES (?, ?, ?, ?, ?)",
                           (generation, str(uuid4()), "fixture-command", hashlib.sha256(b"fixture").hexdigest(),
                            json_text({"generation_id": generation, "version": 3})))
    return store

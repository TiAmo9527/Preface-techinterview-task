"""f001a integration evidence; scenario names cover only the documented foundation slices."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sqlite3
import subprocess
import sys
from threading import Event
import time
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
import pytest

from app import create_app
from src.db import SaveFailed, SchemaError, Store, StoreBusy
from src.db import schema
from src.db.store import DEFAULT_STORE_PATH, REPOSITORY_ROOT
from src.db import reset_queries
from src.services.runtime import reset_store
from src.services.contracts import ResetRequest
from src.services.errors import CommandError


def snapshot(store):
    with store.transaction(write=False) as connection:
        tables = [row[0] for row in connection.execute(
            "SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )]
        return {table: [tuple(row) for row in connection.execute(f'SELECT * FROM "{table}" ORDER BY rowid')] for table in tables}


def test_ac_demo_001_reset(seeded_store, clock):
    before = seeded_store.metadata()
    application = create_app(store_path=seeded_store.path, clock=clock)
    evicted = []
    application.state.evict_previews = evicted.append
    with TestClient(application) as client:
        config = client.get('/api/config')
        assert config.status_code == 200 and config.headers['cache-control'] == 'no-store'
        result = client.post('/api/reset', json={'generation_id': before.generation_id, 'confirm': True})
        assert result.status_code == 200
        assert result.headers['cache-control'] == 'no-store'
        assert result.json()['generation_id'] != before.generation_id
        assert all(value == 0 for value in result.json()['counts'].values())
        updated = client.get('/api/config').json()
        for key in ('fx', 'configured_fx', 'owners', 'delivered_languages', 'schema_version', 'configuration_version'):
            assert updated[key] == config.json()[key]
        assert '/static/shell.js' in client.get('/').text
        assert client.get('/static/shell.js').status_code == 200
    assert evicted == [before.generation_id]
    assert seeded_store.path.exists()
    assert all(not rows for name, rows in snapshot(seeded_store).items() if name != 'store_metadata')
    assert seeded_store.initialize().schema_version == before.schema_version


@pytest.mark.parametrize('payload', [{}, {'confirm': False}, {'confirm': 'true'}, {'confirm': 1},
                                     {'confirm': True, 'extra': 'no'}, {'confirm': True, 'generation_id': 'bad'}])
def test_ac_infra_004_invalid_reset(seeded_store, payload):
    before = snapshot(seeded_store)
    body = {'generation_id': seeded_store.metadata().generation_id, **payload}
    with TestClient(create_app(store_path=seeded_store.path)) as client:
        result = client.post('/api/reset', json=body)
    assert result.status_code == 422
    assert result.json()['code'] == 'INVALID_INPUT'
    assert snapshot(seeded_store) == before


@pytest.mark.parametrize('failure_at', ['halfway', 'metadata', 'commit'])
def test_ac_infra_004_failed_reset(seeded_store, monkeypatch, failure_at):
    before = snapshot(seeded_store)
    if failure_at == 'halfway':
        original = reset_queries.DELETE_ORDER
        monkeypatch.setattr(reset_queries, 'DELETE_ORDER', original[:7] + ('missing_reset_table',) + original[7:])
    elif failure_at == 'metadata':
        def fail(connection, replacement):
            raise sqlite3.DatabaseError('injected metadata failure')
        monkeypatch.setattr(reset_queries, 'replace_generation', fail)
    else:
        original_connect = Store._connect

        class FailingCommit:
            def __init__(self, connection):
                self.connection = connection
            def __getattr__(self, name):
                return getattr(self.connection, name)
            def commit(self):
                raise sqlite3.DatabaseError('injected commit failure')

        def connect(self, *, write):
            connection = original_connect(self, write=write)
            return FailingCommit(connection) if write else connection
        monkeypatch.setattr(Store, '_connect', connect)
    evicted = []
    with pytest.raises(CommandError) as caught:
        reset_store(seeded_store, ResetRequest(generation_id=seeded_store.metadata().generation_id, confirm=True),
                    evict_previews=evicted.append)
    assert caught.value.code == 'SAVE_FAILED'
    assert snapshot(seeded_store) == before and evicted == []


def test_ac_infra_005_generation_selective_hook(seeded_store):
    old = seeded_store.metadata().generation_id
    entries = {'old': old}
    def evict(generation):
        # This read must work after commit and must see the replacement generation.
        replacement = seeded_store.metadata().generation_id
        assert replacement != old
        entries['new'] = replacement
        for key in list(entries):
            if entries[key] == generation:
                del entries[key]
    result = reset_store(seeded_store, ResetRequest(generation_id=old, confirm=True), evict_previews=evict)
    assert entries == {'new': result.generation_id}


def test_ac_infra_005_hook_failure_does_not_claim_rollback(seeded_store, caplog):
    old = seeded_store.metadata().generation_id
    def fail(generation):
        raise RuntimeError('injected registry cleanup failure')
    result = reset_store(seeded_store, ResetRequest(generation_id=old, confirm=True), evict_previews=fail)
    assert result.generation_id == seeded_store.metadata().generation_id != old
    assert all(value == 0 for value in result.counts.model_dump().values())
    assert 'after committed reset' in caplog.text


def test_ac_infra_006_old_reset_preserves_new_portfolio(seeded_store):
    old = seeded_store.metadata().generation_id
    with TestClient(create_app(store_path=seeded_store.path)) as client:
        assert client.post('/api/reset', json={'generation_id': old, 'confirm': True}).status_code == 200
        with seeded_store.transaction() as connection:
            connection.execute("INSERT INTO properties VALUES ('HK-P02', 'New fictional portfolio', 'HONG_KONG', 'Hong Kong')")
        before = snapshot(seeded_store)
        result = client.post('/api/reset', json={'generation_id': old, 'confirm': True})
        assert result.status_code == 409 and result.json()['code'] == 'STALE_STORE'
    assert snapshot(seeded_store) == before


def test_ac_infra_004_http_failure_preserves_store(seeded_store, monkeypatch):
    before = snapshot(seeded_store)
    with TestClient(create_app(store_path=seeded_store.path)) as client:
        monkeypatch.setattr(reset_queries, 'DELETE_ORDER', reset_queries.DELETE_ORDER[:7] + ('missing',))
        result = client.post('/api/reset', json={'generation_id': seeded_store.metadata().generation_id, 'confirm': True})
        assert result.status_code == 500 and result.json()['code'] == 'SAVE_FAILED'
    assert snapshot(seeded_store) == before


def test_ac_us02_017_config_invalid_fx_readable(store, clock):
    from copy import deepcopy
    from src.services.configuration import DEFAULT_CONFIGURATION
    config = deepcopy(DEFAULT_CONFIGURATION)
    config['fx']['usd_per_unit']['USD'] = '2'
    before = snapshot(store)
    with TestClient(create_app(store_path=store.path, config=config, clock=clock)) as client:
        result = client.get('/api/config')
        assert result.status_code == 200
        assert result.json()['fx'] is None and result.json()['diagnostics']
        assert result.json()['configured_fx']['usd_per_unit']['USD'] == '2'
        assert result.json()['operational_date'] == '2026-10-03'
        assert result.json()['delivered_languages'] == ['en']
        assert client.get('/').status_code == 200
    assert snapshot(store) == before


def test_ac_infra_004_busy_reset(seeded_store):
    before = snapshot(seeded_store)
    generation = seeded_store.metadata().generation_id
    with TestClient(create_app(store_path=seeded_store.path)) as client:
        with seeded_store.transaction():
            result = client.post('/api/reset', json={'generation_id': generation, 'confirm': True})
            assert result.status_code == 503 and result.json()['code'] == 'STORE_BUSY'
    assert snapshot(seeded_store) == before


def test_ac_demo_002(seeded_store):
    """Reopen/reinitialize retains every table, version, receipt, and source coordinate."""
    before = snapshot(seeded_store)
    metadata = seeded_store.metadata()
    for _ in range(2):
        reopened = Store(seeded_store.path)
        assert reopened.initialize() == metadata
        assert snapshot(reopened) == before
    with reopened.transaction(write=False) as connection:
        assert connection.execute("SELECT room_number FROM rooms").fetchone()[0] == "001"
        row = connection.execute("SELECT source_cost, typeof(source_cost), override_cost, version FROM assets WHERE asset_id=?",
                                 ("HK-P01-R001-A001",)).fetchone()
        assert tuple(row) == ("9007199254740993.125", "text", "987.65", 3)
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []


def test_ac_demo_005(tmp_path, clock, local_config):
    """The actual application lifecycle initializes only its injected store, without seeding."""
    demo_before = DEFAULT_STORE_PATH.read_bytes() if DEFAULT_STORE_PATH.exists() else None
    application = create_app(store_path=tmp_path / "isolated.sqlite3", clock=clock, config=local_config)
    assert not application.state.store.path.exists()
    local_config["nested"]["isolated"] = False
    with TestClient(application) as client:
        assert client.get("/").status_code == 200  # F001C now supplies the browser shell.
        metadata = application.state.store.metadata()
        assert metadata.schema_version == 1
        assert str(uuid4()) != metadata.generation_id
        assert application.state.clock() == clock()
        assert application.state.local_config["nested"]["isolated"] is True
        saved = snapshot(application.state.store)
        assert len(saved) == 15
        assert len(saved["store_metadata"]) == 1
        assert all(not rows for name, rows in saved.items() if name != "store_metadata")
    assert (DEFAULT_STORE_PATH.read_bytes() if DEFAULT_STORE_PATH.exists() else None) == demo_before


def test_ac_demo_005_cli_from_other_directory(tmp_path, seeded_store):
    before = snapshot(seeded_store)
    code = (
        "import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); "
        "import app; app.app = app.create_app(store_path=Path(sys.argv[2])); "
        "raise SystemExit(app.main(['--init-db']))"
    )
    result = subprocess.run([sys.executable, "-c", code, str(REPOSITORY_ROOT), str(seeded_store.path)],
                            cwd=tmp_path, text=True, capture_output=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert str(seeded_store.path) in result.stdout
    assert snapshot(seeded_store) == before
    result = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); "
                             "from src.db.store import DEFAULT_STORE_PATH; print(DEFAULT_STORE_PATH)", str(REPOSITORY_ROOT)],
                            cwd=tmp_path, text=True, capture_output=True, timeout=15)
    assert result.returncode == 0
    assert Path(result.stdout.strip()) == REPOSITORY_ROOT / "runtime" / "app.sqlite3"


def test_migration_failure_is_atomic(tmp_path, monkeypatch):
    store = Store(tmp_path / "migration.sqlite3")
    with monkeypatch.context() as patch:
        patch.setattr(schema, "MIGRATION_STATEMENTS", schema.MIGRATION_STATEMENTS[:4] + ("INVALID SQL",))
        with pytest.raises(SaveFailed):
            store.initialize()
    with sqlite3.connect(store.path) as connection:
        assert connection.execute("SELECT name FROM sqlite_schema WHERE type='table'").fetchall() == []
    assert store.initialize().schema_version == 1


@pytest.mark.parametrize("defect", ["newer-version", "missing-table", "missing-trigger", "invalid-generation", "foreign-key"])
def test_startup_blocks_damaged_or_unsupported_store(store, defect):
    with sqlite3.connect(store.path, isolation_level=None) as connection:
        if defect == "newer-version":
            connection.execute("UPDATE store_metadata SET schema_version=2")
        elif defect == "missing-table":
            connection.execute("DROP TABLE observations")
        elif defect == "missing-trigger":
            connection.execute("DROP TRIGGER invoice_items_immutable_update")
        elif defect == "invalid-generation":
            connection.execute("UPDATE store_metadata SET generation_id='invalid'")
        else:
            connection.execute("INSERT INTO rooms VALUES ('HK-P01-R001', 'missing-property', '001', '{}')")
    before = snapshot(store) if defect != "invalid-generation" else store.path.read_bytes()
    with pytest.raises(SchemaError):
        store.initialize()
    after = snapshot(store) if defect != "invalid-generation" else store.path.read_bytes()
    assert after == before


def test_startup_does_not_replace_unversioned_data(tmp_path):
    store = Store(tmp_path / "unversioned.sqlite3")
    with sqlite3.connect(store.path) as connection:
        connection.execute("CREATE TABLE legacy (value TEXT)")
        connection.execute("INSERT INTO legacy VALUES ('preserve me')")
    before = snapshot(store)
    with pytest.raises(SchemaError, match="unversioned"):
        store.initialize()
    assert snapshot(store) == before


def test_lifespan_blocks_unsupported_store(store):
    with store.transaction() as connection:
        connection.execute("UPDATE store_metadata SET schema_version=2")
    with pytest.raises(SchemaError, match="unsupported"):
        with TestClient(create_app(store_path=store.path)):
            pytest.fail("An unsupported store must not serve requests")


def test_connections_are_configured_owned_and_closed(store):
    with store.transaction() as connection:
        assert connection.isolation_level is None
        assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert connection.execute("PRAGMA busy_timeout").fetchone()[0] == 5000
        assert connection.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
        with ThreadPoolExecutor(max_workers=1) as worker:
            with pytest.raises(sqlite3.ProgrammingError, match="same thread"):
                worker.submit(connection.execute, "SELECT 1").result(timeout=5)
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        connection.execute("SELECT 1")


def test_nested_operations_share_the_callers_transaction(store):
    def nested(connection):
        connection.execute("INSERT INTO properties VALUES (?, ?, ?, ?)", ("HK-P01", "Nested fixture", "HONG_KONG", "HK"))
    before = snapshot(store)
    with pytest.raises(RuntimeError, match="injected"):
        with store.transaction() as connection:
            nested(connection)
            assert connection.execute("SELECT COUNT(*) FROM properties").fetchone()[0] == 1
            raise RuntimeError("injected after nested write")
    assert snapshot(store) == before


def test_read_snapshot_remains_consistent_during_another_write(seeded_store):
    written, release = Event(), Event()
    def writer():
        with seeded_store.transaction() as connection:
            connection.execute("UPDATE assets SET asset_name='Concurrent fixture', version=version+1 WHERE asset_id=?",
                               ("HK-P01-R001-A001",))
            written.set()
            assert release.wait(5)
    with ThreadPoolExecutor(max_workers=1) as executor:
        try:
            with seeded_store.transaction(write=False) as connection:
                initial = connection.execute("SELECT asset_name FROM assets WHERE asset_id=?", ("HK-P01-R001-A001",)).fetchone()[0]
                future = executor.submit(writer)
                assert written.wait(5)
                assert connection.execute("SELECT asset_name FROM assets WHERE asset_id=?", ("HK-P01-R001-A001",)).fetchone()[0] == initial
        finally:
            release.set()
        future.result(timeout=5)
    with seeded_store.transaction(write=False) as connection:
        assert connection.execute("SELECT asset_name FROM assets WHERE asset_id=?", ("HK-P01-R001-A001",)).fetchone()[0] == "Concurrent fixture"


def test_read_of_missing_store_does_not_create_a_database(tmp_path):
    store = Store(tmp_path / "missing" / "read.sqlite3")
    with pytest.raises(SaveFailed):
        with store.transaction(write=False):
            pytest.fail("A missing store cannot be read")
    assert not store.path.exists()


def test_filesystem_failure_has_safe_feedback(tmp_path):
    parent = tmp_path / "not-a-directory"
    parent.write_text("preserve this file", encoding="utf-8")
    with pytest.raises(SaveFailed):
        Store(parent / "store.sqlite3").initialize()
    assert parent.read_text(encoding="utf-8") == "preserve this file"


def test_runtime_multipart_and_timezone_support(clock):
    """P-02 verifies framework support only, without implementing the Imports algorithms."""
    application = FastAPI()

    @application.post("/probe")
    def probe(file: UploadFile = File()):
        return {"filename": file.filename, "bytes": len(file.file.read())}

    with TestClient(application) as client:
        response = client.post("/probe", files={"file": ("fixture.xlsx", b"fictional", "application/octet-stream")})
    assert response.status_code == 200
    assert response.json() == {"filename": "fixture.xlsx", "bytes": 9}
    assert clock().astimezone(ZoneInfo("Asia/Hong_Kong")).isoformat() == "2026-10-03T16:30:00+08:00"


@pytest.mark.parametrize("stage", ["entity", "history", "receipt", "commit"])
def test_ac_infra_008(seeded_store, monkeypatch, stage):
    before = snapshot(seeded_store)
    generation = seeded_store.metadata().generation_id
    original_connect = Store._connect
    class CommitFailure:
        def __init__(self, connection):
            self.connection = connection
        def __getattr__(self, name):
            return getattr(self.connection, name)
        def commit(self):
            raise sqlite3.OperationalError("injected commit failure")
    with monkeypatch.context() as patch:
        if stage == "commit":
            patch.setattr(Store, "_connect", lambda self, *, write: CommitFailure(original_connect(self, write=write)))
        with pytest.raises(SaveFailed):
            with seeded_store.transaction() as connection:
                connection.execute("UPDATE assets SET asset_name='Unsaved fixture', version=4 WHERE asset_id=?", ("HK-P01-R001-A001",))
                if stage == "entity":
                    raise sqlite3.OperationalError("injected after entity write")
                connection.execute("INSERT INTO override_history VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   ("failed-history", "HK-P01-R001-A001", "RESET_TO_SOURCE", '{}', '{}', "Fixture reason", "Recorder", "2026-10-03T09:00:00Z", None))
                if stage == "history":
                    raise sqlite3.OperationalError("injected after history write")
                connection.execute("INSERT INTO command_receipts VALUES (?, ?, ?, ?, ?)", (generation, str(uuid4()), "fixture-failure", "hash", '{}'))
                if stage == "receipt":
                    raise sqlite3.OperationalError("injected after receipt write")
    assert snapshot(seeded_store) == before


def test_ac_infra_008_busy_timeout(seeded_store):
    before = snapshot(seeded_store)
    with seeded_store.transaction() as holder:
        holder.execute("UPDATE assets SET asset_name=asset_name WHERE asset_id=?", ("HK-P01-R001-A001",))
        started = time.monotonic()
        with pytest.raises(StoreBusy) as failure:
            with seeded_store.transaction():
                pytest.fail("The second writer must not acquire this lock")
        elapsed = time.monotonic() - started
        assert failure.value.code == "STORE_BUSY"
        assert 4.5 <= elapsed < 15
    assert snapshot(seeded_store) == before


@pytest.mark.parametrize("statement", [
    "INSERT INTO rooms VALUES ('HK-P02-R001', 'missing', '001', '{}')",
    "INSERT INTO rooms VALUES ('HK-P01-R002', 'HK-P01', '001', '{}')",
    "UPDATE assets SET facility_type='OTHER' WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET facility_type='WATER_SUPPLY' WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET source_currency='EUR' WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET override_currency=NULL WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET override_cost=NULL WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET override_currency='EUR' WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET useful_life_months=0 WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET useful_life_months=-1 WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET useful_life_months=1.5 WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET version=0 WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE assets SET asset_name=' ' WHERE asset_id='HK-P01-R001-A001'",
    "UPDATE observations SET status='HEALTHY' WHERE system='LIGHTING'",
    "UPDATE observations SET observed_on='2026-10-03' WHERE system='LIGHTING'",
    "UPDATE observations SET note='note only' WHERE system='LIGHTING'",
    "UPDATE observations SET system='OTHER' WHERE system='LIGHTING'",
    "UPDATE maintenance_tickets SET owner_id=NULL WHERE ticket_id='ticket-1'",
    "UPDATE maintenance_tickets SET status='RESOLVED' WHERE ticket_id='ticket-1'",
    "UPDATE maintenance_tickets SET status='INVALID' WHERE ticket_id='ticket-1'",
    "DELETE FROM properties WHERE property_id='HK-P01'",
    "INSERT INTO invoice_update_refs VALUES ('invoice-event','AFTER','missing','001')",
    "INSERT INTO maintenance_history VALUES ('duplicate', 'ticket-1', 'START', '{}', '{}', 'Recorder', '2026-10-03T09:00:00Z', 2)",
    "INSERT INTO command_receipts VALUES ('generation','submission','operation','hash','not json')",
    "INSERT INTO store_metadata VALUES (2,1,'generation')",
], ids=[
    "foreign-key", "room-label-unique", "category", "room-category-unique", "currency",
    "override-missing-currency", "override-missing-cost", "override-currency", "life-zero", "life-negative",
    "life-fraction", "version-zero", "required-name", "assessment-without-metadata", "assessment-without-recorder",
    "unknown-note-only", "system-enum", "owner-required", "resolution-required", "ticket-status",
    "restrict-delete", "invoice-composite-link", "history-version-unique", "receipt-json", "metadata-singleton",
])
def test_schema_constraints_roll_back_invalid_state(seeded_store, statement):
    before = snapshot(seeded_store)
    with pytest.raises(SaveFailed) as failure:
        with seeded_store.transaction() as connection:
            connection.execute(statement)
    assert isinstance(failure.value.__cause__, sqlite3.IntegrityError)
    assert snapshot(seeded_store) == before


@pytest.mark.parametrize("table", schema.IMMUTABLE_TABLES)
def test_evidence_and_history_cannot_be_rewritten(seeded_store, table):
    before = snapshot(seeded_store)
    with seeded_store.transaction(write=False) as connection:
        column = connection.execute(f'PRAGMA table_info("{table}")').fetchone()[1]
    with pytest.raises(SaveFailed) as failure:
        with seeded_store.transaction() as connection:
            connection.execute(f'UPDATE "{table}" SET "{column}"="{column}"')
    assert "Immutable evidence" in str(failure.value.__cause__)
    assert snapshot(seeded_store) == before

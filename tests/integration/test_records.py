"""f001b PR-03 foundation slices, without implementing asset/ticket/import services."""

from concurrent.futures import ThreadPoolExecutor
import json
import sqlite3
from threading import Event
import time
from uuid import uuid4

import pytest

from src.db import Store
from src.db import command_queries
from src.services.commands import canonical_json, execute_command, prepare_command
from src.services.errors import CommandError, ERROR_STATUS


ASSET = "HK-P01-R001-A001"


def snapshot(store):
    with store.transaction(write=False) as connection:
        tables = [row[0] for row in connection.execute(
            "SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )]
        return {table: [tuple(row) for row in connection.execute(f'SELECT * FROM "{table}" ORDER BY rowid')] for table in tables}


def command(store, **changes):
    values = {
        "envelope": {"generation_id": store.metadata().generation_id, "submission_id": str(uuid4())},
        "operation": "foundation-save", "targets": {"asset": ASSET},
        "fields": {"change": "Saved fixture"}, "allowed_fields": frozenset({"change", "note"}),
        "expected_versions": {"asset": 3},
    }
    values.update(changes)
    return prepare_command(**values)


def load_records(connection, targets):
    return {alias: (dict(row) if (row := connection.execute(
        "SELECT * FROM assets WHERE asset_id=?", (identity,),
    ).fetchone()) else None) for alias, identity in targets.items()}


def prepared_mutation(connection, fields, records):
    """Raw independent test writes, not an application asset-edit implementation."""
    previous = records["asset"]
    connection.execute("UPDATE assets SET asset_name=?, version=version+1 WHERE asset_id=?",
                       (fields["change"], previous["asset_id"]))
    saved = dict(connection.execute("SELECT * FROM assets WHERE asset_id=?", (previous["asset_id"],)).fetchone())
    event_id = str(uuid4())
    connection.execute("INSERT INTO override_history VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (event_id, previous["asset_id"], "RESET_TO_SOURCE", canonical_json(previous), canonical_json(saved),
                        "Foundation atomicity fixture", "Fixture recorder", "2026-10-03T08:30:00Z", None))
    return {"saved": saved, "history_id": event_id}


def must_not_run(*args):
    pytest.fail("This callback/query must not run before generation or committed receipt checks")


def test_ac_infra_001(seeded_store):
    before = snapshot(seeded_store)
    pending = command(seeded_store, expected_versions={"asset": 2})
    with pytest.raises(CommandError) as failure:
        execute_command(seeded_store, pending, load_records=load_records, mutate=must_not_run)
    assert failure.value.code == "STALE_RECORD"
    assert failure.value.status_code == 409
    assert failure.value.details["latest"]["version"] == 3
    assert failure.value.details["latest"]["asset_name"] == "Replacement lamp"
    assert snapshot(seeded_store) == before
    assert json.loads(pending.payload_json)["fields"]["change"] == "Saved fixture"
    assert json.loads(pending.payload_json)["expected_versions"] == {"asset": 2}
    # Explicit review uses the latest version and a new submission, never automatic resubmission.
    reviewed = command(seeded_store, expected_versions={"asset": 3})
    result = execute_command(seeded_store, reviewed, load_records=load_records, mutate=prepared_mutation)
    assert result["saved"]["version"] == 4
    assert reviewed.submission_id != pending.submission_id


def test_ac_infra_002(seeded_store):
    """Receipt coordination only; full maintenance card/recorder behavior remains downstream."""
    pending = command(seeded_store)
    first = execute_command(seeded_store, pending, load_records=load_records, mutate=prepared_mutation)
    after_first = snapshot(seeded_store)
    reopened = Store(seeded_store.path)
    reopened.initialize()
    replay = execute_command(reopened, pending, load_records=must_not_run, mutate=must_not_run)
    assert replay == first
    assert first["saved"]["version"] == 4
    assert snapshot(reopened) == after_first
    assert len(after_first["command_receipts"]) == 2  # One independently prepared receipt plus this command.
    assert len(after_first["override_history"]) == 2


@pytest.mark.parametrize("change", ["operation", "fields", "targets", "expected_versions"])
def test_changed_submission_conflicts(seeded_store, change):
    pending = command(seeded_store)
    execute_command(seeded_store, pending, load_records=load_records, mutate=prepared_mutation)
    before = snapshot(seeded_store)
    changed = {"operation": "different-operation", "fields": {"change": "Changed draft"},
               "targets": {"asset": "missing-asset"}, "expected_versions": {"asset": 4}}
    conflicting = command(seeded_store, envelope={"generation_id": pending.generation_id, "submission_id": pending.submission_id},
                          **{change: changed[change]})
    with pytest.raises(CommandError) as failure:
        execute_command(seeded_store, conflicting, load_records=must_not_run, mutate=must_not_run)
    assert failure.value.code == "SUBMISSION_CONFLICT"
    assert snapshot(seeded_store) == before


def test_generation_precedes_receipt_record_and_preview_lookup(seeded_store, monkeypatch):
    pending = command(seeded_store)
    execute_command(seeded_store, pending, load_records=load_records, mutate=prepared_mutation)
    with seeded_store.transaction() as connection:
        # Independently simulate changed metadata; reset implementation belongs to f001c.
        generation = str(uuid4())
        connection.execute("UPDATE store_metadata SET generation_id=?", (generation,))
    before = snapshot(seeded_store)
    monkeypatch.setattr(command_queries, "find_receipt", must_not_run)
    with pytest.raises(CommandError) as failure:
        execute_command(seeded_store, pending, load_records=must_not_run, mutate=must_not_run)
    assert failure.value.as_dict() == {"code": "STALE_STORE", "message_key": "errors.stale_store",
                                       "details": {}, "generation_id": generation}
    assert snapshot(seeded_store) == before


def test_missing_record_is_structured_and_atomic(seeded_store):
    before = snapshot(seeded_store)
    with pytest.raises(CommandError) as failure:
        execute_command(seeded_store, command(seeded_store, targets={"asset": "missing"}),
                        load_records=load_records, mutate=must_not_run)
    assert failure.value.code == "RECORD_NOT_FOUND"
    assert failure.value.status_code == 404
    assert failure.value.details == {"target": "asset", "identity": "missing"}
    assert snapshot(seeded_store) == before


def test_receipt_replay_survives_expired_prerequisite_and_changed_saved_version(seeded_store):
    pending = command(seeded_store, fields={"change": "Reviewed effect", "note": str(uuid4())})
    original = execute_command(seeded_store, pending, load_records=load_records, mutate=prepared_mutation)
    with seeded_store.transaction() as connection:
        connection.execute("UPDATE assets SET asset_name='Later independent save', version=5 WHERE asset_id=?", (ASSET,))
    before = snapshot(seeded_store)
    def expired(*args):
        raise CommandError("PREVIEW_EXPIRED")
    replay = execute_command(Store(seeded_store.path), pending, load_records=must_not_run, mutate=expired)
    assert replay == original
    assert replay["saved"]["version"] == 4
    assert snapshot(seeded_store) == before


def test_canonical_hash_freezes_input_and_preserves_null_omission(seeded_store):
    identity = {"generation_id": seeded_store.metadata().generation_id, "submission_id": str(uuid4())}
    fields = {"note": "測試", "change": "fixture"}
    first = command(seeded_store, envelope=identity, fields=fields)
    equal = command(seeded_store, envelope=identity, fields={"change": "fixture", "note": "測試"})
    assert first.payload_hash == equal.payload_hash
    fields["change"] = "mutated caller draft"
    assert json.loads(first.payload_json)["fields"]["change"] == "fixture"
    omitted = command(seeded_store, fields={"change": "fixture"})
    explicit_null = command(seeded_store, fields={"change": "fixture", "note": None})
    assert omitted.payload_hash != explicit_null.payload_hash
    another_identity = command(seeded_store, fields={"change": "fixture", "note": "測試"})
    assert another_identity.submission_id != first.submission_id
    assert another_identity.payload_hash == first.payload_hash


@pytest.mark.parametrize("invalid", [
    {"envelope": {"generation_id": "bad", "submission_id": str(uuid4())}},
    {"envelope": {"generation_id": str(uuid4()), "submission_id": True}},
    {"envelope": {"generation_id": str(uuid4()), "submission_id": str(uuid4()), "protected": "extra"}},
    {"envelope": {"generation_id": str(uuid4())}},
    {"fields": {"asset_id": "protected"}},
    {"fields": {"source_cost": "99"}},
    {"fields": {"change": 0.1}},
    {"fields": {"change": float("nan")}},
    {"fields": {"change": float("inf")}},
    {"expected_versions": {"asset": True}},
    {"expected_versions": {"asset": 0}},
    {"expected_versions": {"asset": 1.5}},
    {"expected_versions": {"unknown": 1}},
    {"targets": {"asset": 123}},
    {"operation": " "},
])
def test_malformed_or_unapproved_command_is_rejected_before_transaction(seeded_store, invalid, monkeypatch):
    before = snapshot(seeded_store)
    # Capture metadata first; forbid any subsequent connection for rejected input.
    valid = command(seeded_store)
    values = {"envelope": {"generation_id": valid.generation_id, "submission_id": valid.submission_id},
              "operation": valid.operation, "targets": {"asset": ASSET}, "fields": {"change": "fixture"},
              "expected_versions": {"asset": 3}, "allowed_fields": frozenset({"change", "note"})}
    values.update(invalid)
    with monkeypatch.context() as patch:
        patch.setattr(Store, "_connect", must_not_run)
        with pytest.raises(CommandError) as failure:
            prepare_command(**values)
        assert failure.value.code == "INVALID_INPUT"
        assert failure.value.status_code == 422
    assert snapshot(seeded_store) == before


@pytest.mark.parametrize("stage", ["mutation", "history", "receipt", "commit", "response"])
def test_ac_infra_008(seeded_store, monkeypatch, stage):
    before = snapshot(seeded_store)
    pending = command(seeded_store)
    original_connect = Store._connect
    class CommitFailure:
        def __init__(self, connection):
            self.connection = connection
        def __getattr__(self, name):
            return getattr(self.connection, name)
        def commit(self):
            raise sqlite3.OperationalError("injected commit failure")
    def failure_receipt(connection, *args):
        command_queries.original_insert(connection, *args)
        raise sqlite3.OperationalError("injected after receipt insert")
    def mutation(connection, fields, records):
        if stage == "history":
            connection.execute("UPDATE assets SET version=version+1 WHERE asset_id=?", (ASSET,))
            connection.execute("INSERT INTO override_history VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (str(uuid4()), "missing-parent", "RESET_TO_SOURCE", '{}', '{}', 'reason', 'recorder', 'instant', None))
        result = prepared_mutation(connection, fields, records)
        if stage == "mutation":
            raise sqlite3.OperationalError("injected after writes")
        if stage == "response":
            return {"bad_decimal": 0.1}
        return result
    with monkeypatch.context() as patch:
        if stage == "receipt":
            patch.setattr(command_queries, "original_insert", command_queries.insert_receipt, raising=False)
            patch.setattr(command_queries, "insert_receipt", failure_receipt)
        if stage == "commit":
            patch.setattr(Store, "_connect", lambda self, *, write: CommitFailure(original_connect(self, write=write)))
        with pytest.raises(CommandError) as failure:
            execute_command(seeded_store, pending, load_records=load_records, mutate=mutation)
        assert failure.value.code == "SAVE_FAILED"
        assert failure.value.status_code == 500
        assert "injected" not in json.dumps(failure.value.as_dict())
    assert snapshot(seeded_store) == before
    # A failed command has no receipt: exactly the original ID/payload can succeed later.
    assert execute_command(seeded_store, pending, load_records=load_records, mutate=prepared_mutation)["saved"]["version"] == 4


def test_domain_prerequisite_failure_preserves_state_and_can_retry(seeded_store):
    before = snapshot(seeded_store)
    pending = command(seeded_store)
    def reject(connection, fields, records):
        raise CommandError("DOMAIN_RULE", details={"reason": "fixture prerequisite"})
    with pytest.raises(CommandError) as failure:
        execute_command(seeded_store, pending, load_records=load_records, mutate=reject)
    assert failure.value.generation_id == pending.generation_id
    assert snapshot(seeded_store) == before
    assert execute_command(seeded_store, pending, load_records=load_records, mutate=prepared_mutation)["saved"]["version"] == 4


def test_ac_infra_008_command_busy(seeded_store):
    pending = command(seeded_store)
    before = snapshot(seeded_store)
    with seeded_store.transaction() as lock:
        started = time.monotonic()
        with pytest.raises(CommandError) as failure:
            execute_command(seeded_store, pending, load_records=must_not_run, mutate=must_not_run)
        elapsed = time.monotonic() - started
        assert failure.value.code == "STORE_BUSY"
        assert failure.value.status_code == 503
        assert failure.value.generation_id is None
        assert 4.5 <= elapsed < 8
        assert lock.execute("SELECT version FROM assets WHERE asset_id=?", (ASSET,)).fetchone()[0] == 3
    assert snapshot(seeded_store) == before


def test_concurrent_duplicate_submissions_commit_once(seeded_store):
    pending = command(seeded_store)
    entered, release = Event(), Event()
    calls = []
    def mutate(connection, fields, records):
        calls.append(1)
        entered.set()
        assert release.wait(3)
        return prepared_mutation(connection, fields, records)
    def submit():
        return execute_command(seeded_store, pending, load_records=load_records, mutate=mutate)
    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(submit)
        try:
            assert entered.wait(3)
            second = executor.submit(submit)
        finally:
            release.set()
        assert first.result(timeout=8) == second.result(timeout=8)
    assert len(calls) == 1
    with seeded_store.transaction(write=False) as connection:
        assert connection.execute("SELECT COUNT(*) FROM command_receipts WHERE submission_id=?", (pending.submission_id,)).fetchone()[0] == 1
        assert connection.execute("SELECT version FROM assets WHERE asset_id=?", (ASSET,)).fetchone()[0] == 4


def test_successful_zero_effect_command_writes_only_its_receipt(store):
    pending = command(store, targets={}, fields={}, allowed_fields=frozenset(), expected_versions={})
    before = snapshot(store)
    response = execute_command(store, pending, load_records=lambda *args: {}, mutate=lambda *args: {"count": 0})
    after = snapshot(store)
    assert response == {"count": 0, "generation_id": pending.generation_id}
    assert len(after["command_receipts"]) == 1
    assert {key: rows for key, rows in after.items() if key != "command_receipts"} == {
        key: rows for key, rows in before.items() if key != "command_receipts"}


@pytest.mark.parametrize("code,status", list(ERROR_STATUS.items()))
def test_structured_error_status_mapping(code, status):
    details = {"latest": {"version": 7}}
    error = CommandError(code, details=details, generation_id="known-generation")
    details["latest"]["version"] = 99
    assert error.status_code == status
    assert set(error.as_dict()) == {"code", "message_key", "details", "generation_id"}
    assert error.as_dict()["details"]["latest"]["version"] == 7


def typed_asset_request(store, **fields):
    from src.services.contracts import AssetPatchRequest, validate_request
    return validate_request(AssetPatchRequest, {
        "generation_id": store.metadata().generation_id, "submission_id": str(uuid4()),
        "expected_version": 3, "asset_name": "Saved typed fixture", **fields,
    })


def typed_fixture_mutation(connection, fields, records):
    """Adapt the existing independent atomicity fixture, not a feature service."""
    result = prepared_mutation(connection, {"change": fields["asset_name"]}, records)
    asset = result["saved"]
    return {"asset": {**asset, "effective_cost": asset["override_cost"] or asset["source_cost"],
                      "effective_currency": asset["override_currency"] or asset["source_currency"]}}


def test_ac_infra_002_typed_response_replay_after_reopen(seeded_store):
    from src.services.contracts import AssetResponse, execute_validated_command
    request = typed_asset_request(seeded_store)
    first = execute_validated_command(seeded_store, request, target_id=ASSET,
                                      load_records=load_records, mutate=typed_fixture_mutation)
    saved = snapshot(seeded_store)
    replay = execute_validated_command(Store(seeded_store.path), request, target_id=ASSET,
                                       load_records=must_not_run, mutate=must_not_run)
    assert replay == first
    assert AssetResponse.model_validate(first).asset.version == 4
    assert snapshot(seeded_store) == saved


def test_ac_infra_001_typed_boundary_exposes_latest_and_keeps_draft(seeded_store):
    from src.services.contracts import execute_validated_command
    request = typed_asset_request(seeded_store, expected_version=2)
    before = snapshot(seeded_store)
    with pytest.raises(CommandError) as failure:
        execute_validated_command(seeded_store, request, target_id=ASSET,
                                  load_records=load_records, mutate=must_not_run)
    assert failure.value.code == "STALE_RECORD"
    assert failure.value.details["latest"]["version"] == 3
    assert request.asset_name == "Saved typed fixture"
    assert request.expected_version == 2
    assert snapshot(seeded_store) == before


@pytest.mark.parametrize("defect", ["extra-field", "numeric-amount", "wrong-generation", "missing-version"])
def test_ac_infra_008_typed_response_failure_rolls_back_writes_and_history(seeded_store, defect):
    from src.services.contracts import execute_validated_command
    before = snapshot(seeded_store)

    def failed_response(connection, fields, records):
        result = typed_fixture_mutation(connection, fields, records)
        if defect == "extra-field":
            result["raw_sql_error"] = "must never escape"
        elif defect == "numeric-amount":
            result["asset"]["effective_cost"] = 987.65
        elif defect == "wrong-generation":
            result["generation_id"] = str(uuid4())
        else:
            del result["asset"]["version"]
        return result

    with pytest.raises(CommandError) as failure:
        execute_validated_command(seeded_store, typed_asset_request(seeded_store), target_id=ASSET,
                                  load_records=load_records, mutate=failed_response)
    assert failure.value.code == "SAVE_FAILED"
    assert failure.value.status_code == 500
    assert snapshot(seeded_store) == before
    assert "raw_sql_error" not in json.dumps(failure.value.as_dict())


@pytest.mark.parametrize("model_name,fields", [
    ("MaintenanceCreateRequest", {"room_id": "HK-P01-R001", "description": "Fault", "severity": "LOW"}),
    ("MaintenancePatchRequest", {"expected_version": 2, "description": "Fault"}),
    ("MaintenanceStartRequest", {"expected_version": 2}),
    ("MaintenanceResolveRequest", {"expected_version": 2, "resolution_note": "Fixed"}),
])
def test_ac_infra_009_recorder_boundary_blocks_before_any_store_write(seeded_store, model_name, fields):
    from src.services import contracts as c
    body = {"generation_id": seeded_store.metadata().generation_id, "submission_id": str(uuid4()), **fields}
    before = snapshot(seeded_store)
    for recorder in (None, "", "  ", 123, True):
        with pytest.raises(CommandError) as failure:
            c.validate_request(getattr(c, model_name), {**body, "recorder": recorder})
        assert failure.value.code == "INVALID_INPUT"
        assert snapshot(seeded_store) == before
    valid = c.validate_request(getattr(c, model_name), {**body, "recorder": " Recorder "})
    assert valid.recorder == "Recorder"
    # Actual ticket actions and histories are downstream F005 obligations.
    assert snapshot(seeded_store) == before


@pytest.mark.parametrize("fields", [{"status": "HEALTHY"},
    {"status": "UNKNOWN", "observed_on": "2026-10-03", "recorder": " "}])
def test_ac_us02_010_observation_contract_preserves_saved_state(seeded_store, fields):
    from src.services.contracts import ObservationSaveRequest, validate_request
    before = snapshot(seeded_store)
    with pytest.raises(CommandError):
        validate_request(ObservationSaveRequest, {"generation_id": seeded_store.metadata().generation_id,
                         "submission_id": str(uuid4()), "expected_version": 1, **fields})
    assert snapshot(seeded_store) == before


def test_ac_us01_006_invalid_json_value_has_coordinates_and_no_effects(seeded_store):
    from src.services.contracts import AssetSnapshot, validate_request
    before = snapshot(seeded_store)
    with pytest.raises(CommandError) as failure:
        validate_request(AssetSnapshot, {"asset_name": "Fixture", "purchase_date": "2026-01-01",
                         "installation_date": "2025-12-31", "useful_life_months": 12,
                         "acquisition_cost": "100", "currency": "USD"},
                         file="Assets.xlsx", sheet="Assets", row=2)
    assert failure.value.details["diagnostics"][0]["row"] == 2
    assert snapshot(seeded_store) == before


def test_ac_us05_009_invalid_fx_preserves_source_values_and_readable_configuration(seeded_store, clock):
    from src.services.configuration import (configuration_response, finance_configuration_failure,
                                             local_configuration)
    before = snapshot(seeded_store)
    config = local_configuration()
    del config.fx["usd_per_unit"]["JPY"]
    finance = finance_configuration_failure(config)
    response = configuration_response(generation_id=seeded_store.metadata().generation_id,
                                      schema_version=1, config=config, clock=clock)
    assert finance.results is None and finance.diagnostics
    assert response.owners and response.configured_fx["as_of_date"] == "2026-10-03"
    assert snapshot(seeded_store) == before


def test_generation_precedes_typed_domain_loading(seeded_store):
    from src.services.contracts import execute_validated_command
    request = typed_asset_request(seeded_store, generation_id=str(uuid4()))
    before = snapshot(seeded_store)
    with pytest.raises(CommandError) as failure:
        execute_validated_command(seeded_store, request, target_id=ASSET,
                                  load_records=must_not_run, mutate=must_not_run)
    assert failure.value.code == "STALE_STORE"
    assert snapshot(seeded_store) == before

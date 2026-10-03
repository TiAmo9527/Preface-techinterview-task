"""F001B contracts/configuration/clock; no finance arithmetic or browser claims."""

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import json

import pytest
from pydantic import ValidationError

from src.services import contracts as c
from src.services.clock import operational_time
from src.services.configuration import (configuration_response, finance_configuration_failure,
                                         local_configuration, validate_owner, validated_fx)
from src.services.errors import CommandError


GENERATION = "00000000-0000-0000-0000-000000000001"
SUBMISSION = "00000000-0000-0000-0000-000000000002"
TICKET = "00000000-0000-0000-0000-000000000003"
ROOM = "HK-P01-R001"
ASSET = ROOM + "-A001"
ENVELOPE = {"generation_id": GENERATION, "submission_id": SUBMISSION}
EDIT = {**ENVELOPE, "expected_version": 1}
REQUESTS = [
    (c.ConfigRequest, {}), (c.OverviewRequest, {}), (c.RoomRequest, {}),
    (c.AssetEvidenceRequest, {}), (c.MaintenanceListRequest, {}), (c.MaintenanceDetailRequest, {}),
    (c.ObservationSaveRequest, {**EDIT, "status": "healthy", "observed_on": "2026-10-03", "recorder": "Recorder"}),
    (c.ObservationClearRequest, EDIT),
    (c.AssetPatchRequest, {**EDIT, "asset_name": "Lamp"}),
    (c.AssetOverrideRequest, {**EDIT, "cost": "00120.2500", "currency": "usd", "reason": "Correction", "recorder": "Recorder"}),
    (c.AssetResetToSourceRequest, {**EDIT, "reason": "Restore source", "recorder": "Recorder"}),
    (c.MaintenanceCreateRequest, {**ENVELOPE, "room_id": ROOM, "description": "Fault", "severity": "medium", "recorder": "Recorder"}),
    (c.MaintenancePatchRequest, {**EDIT, "owner_id": None, "recorder": "Recorder"}),
    (c.MaintenanceStartRequest, {**EDIT, "recorder": "Recorder"}),
    (c.MaintenanceResolveRequest, {**EDIT, "resolution_note": "Fixed", "recorder": "Recorder"}),
    (c.ImportPreviewRequest, {"file": b"transient workbook", "workflow": "assets"}),
    (c.ImportConfirmRequest, {**ENVELOPE, "preview_id": TICKET}),
    (c.ResetRequest, {"generation_id": GENERATION, "confirm": True}),
]


@pytest.mark.parametrize("model,body", REQUESTS, ids=[model.__name__ for model, _ in REQUESTS])
def test_endpoint_requests_validate_real_boundary_values(model, body):
    result = c.validate_request(model, deepcopy(body))
    if model is not c.ImportPreviewRequest:
        assert model.model_validate_json(result.model_dump_json(exclude_unset=True)) == result


@pytest.mark.parametrize("model,body", REQUESTS, ids=[model.__name__ for model, _ in REQUESTS])
def test_endpoint_requests_reject_extra_fields(model, body):
    with pytest.raises(CommandError) as failure:
        c.validate_request(model, {**deepcopy(body), "unexpected": "value"})
    assert failure.value.status_code == 422
    assert any(item["field"] == "unexpected" for item in failure.value.details["diagnostics"])


@pytest.mark.parametrize("field,value", [
    ("asset_id", ASSET), ("room_id", ROOM), ("facility_type", "LIGHTING"),
    ("source_cost", "1"), ("source_currency", "USD"), ("override_cost", "1"),
    ("effective_cost", "1"), ("version", 2), ("applied_invoice_date", "2026-10-03"),
])
def test_asset_patch_rejects_protected_fields(field, value):
    with pytest.raises(CommandError):
        c.validate_request(c.AssetPatchRequest, {**EDIT, "asset_name": "Lamp", field: value})


@pytest.mark.parametrize("model", [c.MaintenanceCreateRequest, c.MaintenancePatchRequest])
@pytest.mark.parametrize("field,value", [("status", "RESOLVED"), ("ticket_id", TICKET),
    ("opened_at", "2026-10-03T00:00:00Z"), ("resolved_at", "2026-10-03T00:00:00Z")])
def test_maintenance_rejects_generated_fields(model, field, value):
    body = dict(next(body for candidate, body in REQUESTS if candidate is model))
    with pytest.raises(CommandError):
        c.validate_request(model, {**body, field: value})


@pytest.mark.parametrize("field,value", [("room_id", ROOM), ("asset_id", ASSET)])
def test_maintenance_patch_rejects_link_changes(field, value):
    with pytest.raises(CommandError):
        c.validate_request(c.MaintenancePatchRequest, {**EDIT, "description": "Fault", "recorder": "Recorder", field: value})


@pytest.mark.parametrize("value", [None, True, False, 0, -1, 1.0, "1"])
def test_edit_versions_are_required_positive_strict_integers(value):
    with pytest.raises(CommandError):
        c.validate_request(c.AssetPatchRequest, {**EDIT, "expected_version": value, "asset_name": "Lamp"})


@pytest.mark.parametrize("value", [GENERATION.upper().replace("0", "A", 1), "not-a-uuid", 1,
    "00000000000000000000000000000001", "{" + GENERATION + "}"])
def test_canonical_envelope_uuid_required(value):
    with pytest.raises(CommandError):
        c.validate_request(c.ImportConfirmRequest, {**ENVELOPE, "submission_id": value, "preview_id": TICKET})


@pytest.mark.parametrize("value", [120.25, Decimal("120.25"), True, "NaN", "-1"])
def test_override_json_requires_nonnegative_decimal_strings(value):
    with pytest.raises(CommandError):
        c.validate_request(c.AssetOverrideRequest, {**EDIT, "cost": value, "currency": "USD", "reason": "Correction", "recorder": "Recorder"})


@pytest.mark.parametrize("value", [False, 1, "true", None])
def test_reset_confirmation_is_strict_boolean(value):
    with pytest.raises(CommandError):
        c.validate_request(c.ResetRequest, {"generation_id": GENERATION, "confirm": value})


def test_patch_omission_clear_and_merged_date_validation():
    saved = {"asset_name": "Lamp", "purchase_date": "2026-01-15", "installation_date": "2026-02-01", "useful_life_months": 12}
    rename = c.validate_request(c.AssetPatchRequest, {**EDIT, "asset_name": " Changed "})
    clear = c.validate_request(c.AssetPatchRequest, {**EDIT, "installation_date": None})
    assert rename.supplied_fields() == {"asset_name": "Changed"}
    assert c.merged_asset_fields(saved, rename)["installation_date"] == "2026-02-01"
    assert c.merged_asset_fields(saved, clear)["installation_date"] is None
    with pytest.raises(CommandError):
        c.validate_request(c.AssetPatchRequest, {**EDIT, "asset_name": None})
    later_purchase = c.validate_request(c.AssetPatchRequest, {**EDIT, "purchase_date": "2026-03-01"})
    with pytest.raises(CommandError) as failure:
        c.merged_asset_fields(saved, later_purchase)
    assert failure.value.code == "DOMAIN_RULE"
    assert saved["purchase_date"] == "2026-01-15"


def test_empty_patches_and_incomplete_override_are_rejected():
    for model, body in [(c.AssetPatchRequest, EDIT), (c.MaintenancePatchRequest, {**EDIT, "recorder": "Recorder"}),
                        (c.AssetOverrideRequest, {**EDIT, "cost": "10", "reason": "Reason", "recorder": "Recorder"})]:
        with pytest.raises(CommandError):
            c.validate_request(model, body)


@pytest.mark.parametrize("body", [
    {"property_id": "JP-P01", "location": "LONDON"},
    {"property_id": "HK-P01", "room_id": "HK-P02-R001"},
    {"location": "JAPAN", "room_id": ROOM},
])
def test_scope_contract_checks_parent_and_region(body):
    with pytest.raises(CommandError):
        c.validate_request(c.OverviewRequest, body)


def test_maintenance_creation_contract_checks_asset_parent():
    body = {**ENVELOPE, "room_id": ROOM, "asset_id": "HK-P02-R001-A001", "description": "Fault", "severity": "LOW", "recorder": "Recorder"}
    with pytest.raises(CommandError):
        c.validate_request(c.MaintenanceCreateRequest, body)


@pytest.mark.parametrize("model,body", [(model, body) for model, body in REQUESTS if issubclass(model, c.MutationRequest)])
def test_typed_commands_bind_server_operation_target_and_version(model, body):
    request = c.validate_request(model, body)
    path = {"target_id": ASSET} if request.target_kind == "asset" else {}
    if request.target_kind == "ticket":
        path = {"target_id": TICKET}
    if request.target_kind == "observation":
        path = {"target_id": ROOM, "system": "lighting"}
    command = request.to_command(**path)
    payload = json.loads(command.payload_json)
    assert command.operation == request.operation
    assert command.generation_id == GENERATION
    assert payload["fields"] == request.supplied_fields()
    if isinstance(request, c.EditRequest):
        assert payload["expected_versions"] == {request.target_alias: 1}
    if request.target_kind == "observation":
        assert payload["targets"] == {"observation": ROOM + "/LIGHTING"}


def test_command_normalization_hash_equivalence_and_explicit_null():
    original = {**EDIT, "cost": "000120.2500", "currency": " usd ", "reason": " Reason ", "recorder": " Recorder "}
    canonical = {**EDIT, "cost": "120.25", "currency": "USD", "reason": "Reason", "recorder": "Recorder"}
    assert c.validate_request(c.AssetOverrideRequest, original).to_command(target_id=ASSET).payload_hash == c.validate_request(c.AssetOverrideRequest, canonical).to_command(target_id=ASSET).payload_hash
    omitted = c.validate_request(c.MaintenancePatchRequest, {**EDIT, "description": "Fault", "recorder": "Recorder"})
    cleared = c.validate_request(c.MaintenancePatchRequest, {**EDIT, "description": "Fault", "recorder": "Recorder", "owner_id": None})
    assert omitted.to_command(target_id=TICKET).payload_hash != cleared.to_command(target_id=TICKET).payload_hash


def test_default_configuration_is_approved_and_independently_copied():
    config = local_configuration()
    fx, errors = validated_fx(config.fx)
    assert not errors
    assert fx.as_of_date == "2026-10-03"
    assert fx.usd_per_unit == {"HKD": "0.128", "SGD": "0.74", "GBP": "1.25", "JPY": "0.0067", "USD": "1"}
    assert [(item.owner_id, item.display_name) for item in config.owners] == [
        ("owner-alex", "Alex Chan"), ("owner-mei", "Mei Wong"), ("owner-sam", "Sam Lee")]
    assert config.delivered_languages == ["en"]
    assert validate_owner(" owner-alex ", config) == "owner-alex"
    assert validate_owner(None, config) is None
    with pytest.raises(ValueError):
        validate_owner("not-an-owner", config)
    config.fx["usd_per_unit"]["USD"] = "2"
    assert local_configuration().fx["usd_per_unit"]["USD"] == "1"


@pytest.mark.parametrize("defect", ["missing-rate", "date", "duplicate", "zero", "negative", "nan", "infinite", "usd", "boolean", "missing-fx", "extra-field"])
def test_ac_us05_009_invalid_configuration_diagnostics_without_totals(defect):
    config = local_configuration()
    raw = config.fx
    if defect == "missing-rate":
        del raw["usd_per_unit"]["JPY"]
    elif defect == "date":
        del raw["as_of_date"]
    elif defect == "duplicate":
        raw["usd_per_unit"][" usd "] = "1"
    elif defect == "missing-fx":
        raw = None
    elif defect == "extra-field":
        raw["live"] = True
    else:
        key, value = {"zero": ("HKD", "0"), "negative": ("GBP", "-1"), "nan": ("JPY", float("nan")),
                      "infinite": ("SGD", Decimal("Infinity")), "usd": ("USD", "2"), "boolean": ("HKD", True)}[defect]
        raw["usd_per_unit"][key] = value
    supplied = local_configuration({**config.model_dump(), "fx": raw})
    result = finance_configuration_failure(supplied)
    assert result.status == "INVALID_CONFIGURATION"
    assert result.results is None and result.diagnostics
    response = configuration_response(generation_id=GENERATION, schema_version=1, config=supplied,
                                      clock=lambda: datetime(2026, 10, 2, 16, tzinfo=timezone.utc))
    assert response.fx is None and response.diagnostics and response.owners
    assert response.operational_date == "2026-10-03"
    assert response.configured_fx is not None or defect == "missing-fx"
    # Even non-finite invalid rates remain readable without invalid JSON tokens.
    json.loads(response.model_dump_json(), parse_constant=lambda token: pytest.fail(token))


@pytest.mark.parametrize("defect", ["duplicate-owner", "blank-name", "numeric-id", "no-english", "duplicate-language"])
def test_local_owner_and_language_configuration_integrity(defect):
    raw = local_configuration().model_dump()
    if defect == "duplicate-owner":
        raw["owners"].append(raw["owners"][0])
    elif defect == "blank-name":
        raw["owners"][0]["display_name"] = " "
    elif defect == "numeric-id":
        raw["owners"][0]["owner_id"] = 10
    elif defect == "no-english":
        raw["delivered_languages"] = ["ja"]
    else:
        raw["delivered_languages"] = ["en", "en"]
    with pytest.raises(ValueError):
        local_configuration(raw)


@pytest.mark.parametrize("instant,expected", [
    (datetime(2026, 10, 2, 15, 59, 59, tzinfo=timezone.utc), "2026-10-02"),
    (datetime(2026, 10, 2, 16, tzinfo=timezone.utc), "2026-10-03"),
    (datetime(2026, 10, 3, 1, tzinfo=timezone(timedelta(hours=9))), "2026-10-03"),
])
def test_hong_kong_operational_day_boundary(instant, expected):
    result = operational_time(lambda: instant)
    assert result.operational_date == expected
    assert result.operational_time.endswith("+08:00")
    assert result.utc_instant.endswith("Z")
    assert result.timezone == "Asia/Hong_Kong"


@pytest.mark.parametrize("value", [datetime(2026, 10, 3), "2026-10-03", None])
def test_operational_clock_rejects_naive_and_non_datetime_values(value):
    with pytest.raises(ValueError):
        operational_time(lambda: value)


def test_configuration_clock_is_independent_of_reporting_date():
    clock = lambda: datetime(2026, 10, 2, 16, tzinfo=timezone.utc)
    request = c.validate_request(c.OverviewRequest, {"financial_date": "2040-01-01"})
    config = local_configuration()
    response = configuration_response(generation_id=GENERATION, schema_version=1, config=config, clock=clock)
    assert request.financial_date == "2040-01-01"
    assert response.operational_date == "2026-10-03"
    assert response.fx.as_of_date == "2026-10-03"
    assert finance_configuration_failure(config) is None


def test_finance_envelope_rejects_fabricated_partial_results():
    diagnostic = c.Diagnostic(entity="FX", field="JPY", reason="Missing rate")
    with pytest.raises(ValidationError):
        c.FinanceEnvelope(status="INVALID_CONFIGURATION", diagnostics=[diagnostic], results={"totals": []})
    with pytest.raises(ValidationError):
        c.FinanceEnvelope(status="VALID", diagnostics=[], results=None)
    with pytest.raises(ValidationError):
        c.FinanceEnvelope(status="INVALID_CONFIGURATION", diagnostics=[], results=None)


def test_empty_store_response_counts_reject_nonzero_and_boolean_values():
    values = {key: 0 for key in c.EmptyStoreCounts.model_fields}
    assert c.EmptyStoreCounts.model_validate(values).properties == 0
    for value in (1, False):
        with pytest.raises(ValidationError):
            c.EmptyStoreCounts.model_validate({**values, "properties": value})


def test_contract_inventory_covers_existing_endpoints_without_registering_routes():
    assert len(c.ENDPOINT_CONTRACTS) == 18
    assert {entry.request for entry in c.ENDPOINT_CONTRACTS.values()} == {model for model, _ in REQUESTS}
    for entry in c.ENDPOINT_CONTRACTS.values():
        assert entry.request.model_config["extra"] == "forbid"
        assert entry.response.model_config["extra"] == "forbid"
        assert "generation_id" in entry.response.model_fields
        entry.request.model_json_schema()
        entry.response.model_json_schema()


def room_response_values():
    """Independent fictional response values, without pretending to query a room."""
    diagnostic = c.Diagnostic(entity="FX", field="JPY", reason="Missing rate")
    observations = [c.Observation(room_id=ROOM, system=system, version=1) for system in ("LIGHTING", "WATER_SUPPLY", "AIR_CONDITIONING")]
    assets = [c.Asset(asset_id=ROOM + f"-A{index:03d}", room_id=ROOM, facility_type=system,
                     asset_name="Fictional " + system, purchase_date="2026-01-01", installation_date=None,
                     useful_life_months=12, source_cost="9007199254740993.125", source_currency="USD",
                     override_cost=None, override_currency=None, effective_cost="9007199254740993.125",
                     effective_currency="USD", applied_invoice_date=None, version=1)
              for index, system in enumerate(("LIGHTING", "WATER_SUPPLY", "AIR_CONDITIONING"), 1)]
    return {"generation_id": GENERATION,
            "property": c.Property(property_id="HK-P01", property_name="Fictional hotel", location="HONG_KONG", city="Hong Kong"),
            "room": c.Room(room_id=ROOM, property_id="HK-P01", room_number="001"),
            "observations": observations, "assets": assets, "unresolved_tickets": [], "resolved_tickets": [],
            "finance": c.FinanceEnvelope(status="INVALID_CONFIGURATION", diagnostics=[diagnostic], results=None)}


def test_invalid_finance_preserves_operational_room_payload_and_decimal_strings():
    response = c.RoomResponse.model_validate(room_response_values())
    body = json.loads(response.model_dump_json())
    assert len(body["observations"]) == len(body["assets"]) == 3
    assert body["room"]["room_number"] == "001"
    assert body["assets"][0]["source_cost"] == "9007199254740993.125"
    assert body["finance"]["results"] is None and body["finance"]["diagnostics"]
    assert c.RoomResponse.model_validate_json(response.model_dump_json()) == response


@pytest.mark.parametrize("defect", ["duplicate-system", "missing-asset", "wrong-room", "property", "extra", "version"])
def test_room_response_rejects_incomplete_or_inconsistent_operational_contract(defect):
    values = c.RoomResponse.model_validate(room_response_values()).model_dump(mode="json")
    if defect == "duplicate-system":
        values["observations"][1]["system"] = "LIGHTING"
    elif defect == "missing-asset":
        values["assets"].pop()
    elif defect == "wrong-room":
        values["observations"][0]["room_id"] = "HK-P01-R002"
    elif defect == "property":
        values["room"]["property_id"] = "HK-P02"
    elif defect == "extra":
        values["assets"][0]["cost"] = "0"
    else:
        values["assets"][0]["version"] = True
    with pytest.raises(ValidationError):
        c.RoomResponse.model_validate(values)


def test_financial_wire_values_keep_unrounded_and_formatted_amounts_separate():
    fields = ("acquisition_cost", "accumulated_depreciation", "remaining_book_value",
              "overdue_spending", "due_today_spending", "future_spending")
    totals = c.CurrencyTotals(currency="USD", **{key: "0.008" for key in fields},
                              displayed={key: "0.01" for key in fields})
    results = c.FinanceResults(financial_date="2026-10-03", currency_mode="USD", assets=[], totals=[totals])
    response = c.FinanceEnvelope(status="VALID", diagnostics=[], results=results)
    assert json.loads(response.model_dump_json())["results"]["totals"][0]["acquisition_cost"] == "0.008"
    assert c.DisplayedAssetFinance(currency="USD", acquisition_cost="1.00", accumulated_depreciation="0.00",
                                   remaining_book_value="1.00").acquisition_cost == "1.00"
    # These are supplied wire examples; calculations/rounding remain F003A work.

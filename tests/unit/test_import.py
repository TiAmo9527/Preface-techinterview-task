"""F001B shared value foundation; no workbook parser/preview acceptance claim."""

from datetime import date, datetime, timezone
from decimal import Decimal

import pytest

from src.services import validators as v
from src.services.contracts import AssetSnapshot, validate_request
from src.services.errors import CommandError
from src.services.imports import plan_import


@pytest.mark.parametrize("value", ["  001 ", "Case  内部 space", "S20261002-HK-P01"])
def test_text_preserves_case_internal_space_and_leading_zeros(value):
    assert v.text(value) == value.strip()


@pytest.mark.parametrize("value", [1, 1.0, True, False, None, "", "  "])
def test_ac_us01_006_required_text_and_identity_values(value):
    with pytest.raises(ValueError):
        v.text(value)


@pytest.mark.parametrize("value", [None, "", "  "])
def test_optional_text_normalizes_absence(value):
    assert v.text(value, optional=True) is None


@pytest.mark.parametrize("kind,value,parent,location", [
    ("property", "HK-P01", None, "hong_kong"),
    ("property", "S20261002-LDN-P0001", None, "LONDON"),
    ("room", "S20261002-JP-P01-R001", "S20261002-JP-P01", "JAPAN"),
    ("asset", "SG-P01-R001-A0001", "SG-P01-R001", "SINGAPORE"),
])
def test_source_identities_preserve_namespace_and_exact_parent(kind, value, parent, location):
    assert v.source_identity(" " + value + " ", kind, parent=parent, location=location) == value


@pytest.mark.parametrize("kind,value,parent,location", [
    ("property", "HK-P1", None, None), ("property", "hk-P01", None, None),
    ("property", "EU-P01", None, None), ("property", "S-HK-P01", None, None),
    ("property", "HK-P01", None, "JAPAN"), ("property", 1001, None, None),
    ("room", "HK-P01-R01", None, None), ("room", "HK-P01-R001", "HK-P02", None),
    ("room", "S1-HK-P01-R001", "S2-HK-P01", None),
    ("asset", "HK-P01-R001-A001", "HK-P01-R002", None),
    ("asset", "S1-HK-P01-R001-A001", "HK-P01-R001", None),
    ("asset", "HK-P01-R001-A001-extra", None, None),
])
def test_ac_us01_006_identity_grammar_parents_and_region(kind, value, parent, location):
    with pytest.raises(ValueError):
        v.source_identity(value, kind, parent=parent, location=location)


@pytest.mark.parametrize("value", ["2024-02-29", date(2024, 2, 29), datetime(2024, 2, 29)])
def test_equivalent_calendar_representations(value):
    assert v.calendar_date(value) == "2024-02-29"


@pytest.mark.parametrize("value", ["2023-02-29", "2026-13-01", "03/10/2026", "2026-1-01",
    "20261003", "2026-10-03T00:00:00", datetime(2026, 10, 3, 0, 0, 1),
    datetime(2026, 10, 3, tzinfo=timezone.utc), True, 45000, None])
def test_ac_us01_006_impossible_ambiguous_or_timed_dates(value):
    with pytest.raises(ValueError):
        v.calendar_date(value)


@pytest.mark.parametrize("value", [120.25, Decimal("120.2500"), "00120.2500", " 120.25 "])
def test_equivalent_decimal_representations(value):
    assert v.decimal_amount(value) == "120.25"


def test_decimal_canonicalization_never_rounds_large_precise_values():
    value = "123456789012345678901234567890.1234567890123456789000"
    assert v.decimal_amount(value) == value.rstrip("0")
    assert v.decimal_amount(Decimal("1E+32")) == "1" + "0" * 32
    assert v.decimal_amount(Decimal("-0.00")) == "0"


@pytest.mark.parametrize("value", [True, False, -1, float("nan"), float("inf"), Decimal("NaN"),
    Decimal("-Infinity"), "NaN", "Infinity", "-1", "1e2", "$10", "1,000", "+1", ".5", "1.", None])
def test_ac_us01_006_invalid_decimal_amounts(value):
    with pytest.raises(ValueError):
        v.decimal_amount(value)


@pytest.mark.parametrize("value", [12, 12.0, Decimal("12.00")])
def test_integral_months(value):
    assert v.whole_months(value) == 12


@pytest.mark.parametrize("value", [True, False, 0, -1, 0.5, "12", None, float("inf"), Decimal("NaN")])
def test_ac_us01_006_invalid_useful_life(value):
    with pytest.raises(ValueError):
        v.whole_months(value)


@pytest.mark.parametrize("choices,value,expected", [
    (v.CURRENCIES, " hkd ", "HKD"), (v.LOCATIONS, "london", "LONDON"),
    (v.SYSTEMS, " water_supply ", "WATER_SUPPLY"), (v.CONDITIONS, "healthy", "HEALTHY"),
])
def test_supported_enum_normalization(choices, value, expected):
    assert v.enum_value(value, choices) == expected


@pytest.mark.parametrize("choices,value", [(v.CURRENCIES, "EUR"), (v.SYSTEMS, "OTHER"),
    (v.CONDITIONS, "GOOD"), (v.LOCATIONS, "HK"), (v.CURRENCIES, True)])
def test_ac_us01_006_unsupported_enums(choices, value):
    with pytest.raises(ValueError):
        v.enum_value(value, choices)


def test_ac_us01_006_service_date_order():
    assert v.date_order("2026-01-15", None) == ("2026-01-15", None)
    assert v.date_order("2026-01-15", "2026-01-15") == ("2026-01-15", "2026-01-15")
    with pytest.raises(ValueError):
        v.date_order("2026-01-15", "2026-01-14")


@pytest.mark.parametrize("status,date_value,recorder,note", [
    (None, None, None, None), ("UNKNOWN", None, None, None), ("  ", "", "", "  "),
])
def test_unassessed_observation_normalization(status, date_value, recorder, note):
    assert v.observation_metadata(status, date_value, recorder, note) == {
        "status": "UNKNOWN", "observed_on": None, "recorder": None, "note": None}


@pytest.mark.parametrize("status", ["HEALTHY", "ATTENTION_NEEDED", "CRITICAL", "UNKNOWN"])
def test_recorded_observations_require_complete_metadata(status):
    assert v.observation_metadata(status, "2026-10-03", " Recorder ", " Note ") == {
        "status": status, "observed_on": "2026-10-03", "recorder": "Recorder", "note": "Note"}


@pytest.mark.parametrize("fields", [
    {"status": "HEALTHY"}, {"status": "UNKNOWN", "note": "Only note"},
    {"observed_on": "2026-10-03", "recorder": "Recorder"},
    {"status": "CRITICAL", "observed_on": "2026-10-03"},
    {"status": "UNKNOWN", "recorder": "Recorder"},
    {"status": "HEALTHY", "observed_on": "2026-10-03", "recorder": "  "},
])
def test_ac_us02_010_incomplete_observation_metadata(fields):
    with pytest.raises(ValueError):
        v.observation_metadata(**fields)


def test_field_diagnostics_preserve_available_source_coordinates():
    row = {"asset_name": "Lamp", "purchase_date": "2026-01-15", "installation_date": None,
           "useful_life_months": 12, "acquisition_cost": "-1", "currency": "USD"}
    with pytest.raises(CommandError) as failure:
        validate_request(AssetSnapshot, row, file="Assets.xlsx", sheet="Assets", row=7)
    body = failure.value.as_dict()
    assert failure.value.status_code == 422
    diagnostic = body["details"]["diagnostics"][0]
    assert diagnostic["field"] == "acquisition_cost"
    assert diagnostic["value"] == "-1"
    assert (diagnostic["file"], diagnostic["sheet"], diagnostic["row"]) == ("Assets.xlsx", "Assets", 7)
    assert row["acquisition_cost"] == "-1"


# IM-01 workbook tests exercise the production parser, without planner/commit claims.
from dataclasses import FrozenInstanceError
from io import BytesIO
from pathlib import Path
import hashlib

from openpyxl import Workbook, load_workbook

from src.services.workbooks import ASSET_HEADERS, INVOICE_HEADERS, headers_for, parse_workbook
from pydantic import ValidationError


def workbook_row(workflow="ASSETS"):
    common = dict(room_id="HK-P01-R001", facility_type="LIGHTING", asset_name="Lamp",
                  purchase_date="2026-01-15", installation_date="2026-01-16",
                  useful_life_months=12, acquisition_cost="120.25", currency="USD")
    if workflow == "INVOICES":
        return dict(common, invoice_id="0001", line_id="001", invoice_date="2026-02-01", supplier_name="Supplier")
    result = dict(common, property_id="HK-P01", property_name="Hotel", location="HONG_KONG",
                  city="City", room_number="001", asset_id="HK-P01-R001-A001")
    for system in ("lighting", "water_supply", "air_conditioning"):
        result.update({f"{system}_status": None, f"{system}_observed_on": None,
                       f"{system}_recorder": None, f"{system}_note": None})
    return result


def workbook_bytes(workflow="ASSETS", rows=None, headers=None, edit=None):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Assets" if workflow == "ASSETS" else "Invoices"
    selected_headers = headers_for(workflow) if headers is None else headers
    if selected_headers:
        sheet.append(list(selected_headers))
    for row in ([] if rows is None else rows):
        sheet.append([row.get(field) for field in selected_headers])
    if edit:
        edit(workbook, sheet)
    stream = BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def parse_rows(workflow="ASSETS", rows=None, headers=None, edit=None):
    return parse_workbook(workbook_bytes(workflow, rows, headers, edit), filename="source.xlsx", workflow=workflow)


def planner_baseline():
    return [dict(workbook_row(), asset_id=f"HK-P01-R001-A00{index}", facility_type=system)
            for index, system in enumerate(sorted(v.SYSTEMS), 1)]


def planner_state():
    plan = plan_import(parse_rows(rows=planner_baseline()),
                       dict(properties=[], rooms=[], assets=[], invoice_items=[])).as_dict()
    state = {key: plan[key] for key in ("properties", "rooms", "assets", "invoice_items")}
    for asset in state["assets"]:
        snapshot = asset["baseline"]
        asset.update({field: snapshot[field] for field in ("asset_name", "purchase_date", "installation_date", "useful_life_months")})
        asset.update(source_cost=snapshot["acquisition_cost"], source_currency=snapshot["currency"],
                     override_cost=None, override_currency=None, applied_invoice_date=None)
    return state


def planner_invoice(**changes):
    return dict(workbook_row("INVOICES"), **changes)


def test_ac_us01_001_planner_complete_baseline():
    plan = plan_import(parse_rows(rows=planner_baseline()), dict(properties=[], rooms=[], assets=[], invoice_items=[]))
    assert not plan.blocked
    assert (plan.counts["properties_inserted"], plan.counts["rooms_inserted"], plan.counts["assets_inserted"]) == (1, 1, 3)
    assert len(plan.as_dict()["properties"][0]["coordinates"]) == 3


@pytest.mark.parametrize("defect", ["property", "room", "assessment", "missing", "category", "duplicate", "label"])
def test_ac_us01_004_planner_cross_row_blockers(defect):
    rows = planner_baseline()
    if defect == "property": rows[1]["property_name"] = "Changed"
    if defect == "room": rows[1]["room_number"] = "002"
    if defect == "assessment":
        rows[1].update(lighting_status="HEALTHY", lighting_observed_on="2026-01-01", lighting_recorder="Manager")
    if defect == "missing": rows.pop()
    if defect == "category": rows[1]["facility_type"] = rows[0]["facility_type"]
    if defect == "duplicate": rows.append(rows[0])
    if defect == "label":
        rows.extend(dict(row, room_id="HK-P01-R002", asset_id=row["asset_id"].replace("R001", "R002")) for row in planner_baseline())
    plan = plan_import(parse_rows(rows=rows), dict(properties=[], rooms=[], assets=[], invoice_items=[]))
    assert plan.blocked
    assert not any(plan.as_dict()[key] for key in ("properties", "rooms", "assets", "invoice_items", "asset_updates"))


@pytest.mark.parametrize("field,value", [("property_name", "Other"), ("room_number", "other"), ("asset_name", "Other"), ("asset_id", "HK-P01-R001-A099")])
def test_ac_us01_005_planner_immutable_and_occupied(field, value):
    rows = planner_baseline()
    rows[0][field] = value
    assert plan_import(parse_rows(rows=rows), planner_state()).blocked


def test_ac_us01_014_planner_baseline_repeat_preserves_edits():
    state = planner_state()
    state["assets"][0].update(asset_name="Manager edit", source_cost="999", override_cost="777", override_currency="HKD")
    plan = plan_import(parse_rows(rows=planner_baseline()), state)
    assert not plan.blocked and plan.counts["skips"] == 3
    assert not plan.as_dict()["asset_updates"]


@pytest.mark.parametrize("target", ["unknown", "absent", "ambiguous"])
def test_ac_us01_003_planner_target_resolution(target):
    state = planner_state()
    invoice = planner_invoice()
    if target == "unknown": invoice["room_id"] = "HK-P01-R999"
    if target == "absent": state["assets"] = []
    if target == "ambiguous": state["assets"].append(dict(next(a for a in state["assets"] if a["facility_type"] == invoice["facility_type"]), asset_id="HK-P01-R001-A099"))
    assert plan_import(parse_rows("INVOICES", [invoice]), state).blocked


def test_ac_us01_002_planner_subset():
    state = planner_state()
    rows = [planner_invoice(line_id=str(i), facility_type=system) for i, system in enumerate(sorted(v.SYSTEMS)[:2])]
    plan = plan_import(parse_rows("INVOICES", rows), state)
    assert plan.counts["assets_updated"] == 2 and plan.counts["invoice_items_inserted"] == 2
    assert plan.counts["assets_inserted"] == 0


def test_ac_us01_010_planner_order_independence():
    from dataclasses import replace
    state = planner_state()
    parsed = parse_rows("INVOICES", [planner_invoice(line_id="old", invoice_date="2026-09-01", asset_name="Old"), planner_invoice(line_id="new", invoice_date="2026-10-01", asset_name="New")])
    plan = plan_import(parsed, state)
    assert plan == plan_import(replace(parsed, normalized_rows=tuple(reversed(parsed.normalized_rows))), state)
    assert plan.counts["historical_only_items"] == 1
    assert plan.as_dict()["asset_updates"][0]["after"]["asset_name"] == "New"


def applied_planner_state():
    state = planner_state()
    invoice = parse_rows("INVOICES", [planner_invoice()]).normalized_rows[0].as_dict()
    asset = next(a for a in state["assets"] if a["facility_type"] == invoice["facility_type"])
    state["invoice_items"].append(dict(invoice, asset_id=asset["asset_id"]))
    asset.update(applied_invoice_date=invoice["invoice_date"], asset_name="Manager edit", override_cost="900", override_currency="HKD", version=7)
    return state


@pytest.mark.parametrize("date", ["2026-01-01", "2026-02-01"])
def test_ac_us01_011_013_planner_historical_preserves_edits(date):
    state = applied_planner_state()
    row = planner_invoice(line_id="distinct", invoice_date=date)
    plan = plan_import(parse_rows("INVOICES", [row]), state)
    assert not plan.blocked and plan.counts["historical_only_items"] == 1
    assert plan.counts["assets_updated"] == 0


def test_ac_us01_012_planner_controlling_conflict():
    for state, rows in [(planner_state(), [planner_invoice(), planner_invoice(line_id="other", asset_name="Other")]),
                        (applied_planner_state(), [planner_invoice(line_id="other", asset_name="Other")])]:
        plan = plan_import(parse_rows("INVOICES", rows), state)
        assert plan.blocked and plan.counts["invoice_items_inserted"] == 0


def test_ac_us01_013_planner_equivalent_ties_retain_all_refs():
    plan = plan_import(parse_rows("INVOICES", [planner_invoice(line_id="z"), planner_invoice(line_id="a")]), planner_state())
    assert plan.counts["invoice_items_inserted"] == 2 and plan.counts["assets_updated"] == 1
    assert [r["line_id"] for r in plan.as_dict()["asset_updates"][0]["after_refs"]] == ["a", "z"]


def test_ac_us01_015_planner_repeat_preserves_edits():
    state = applied_planner_state()
    plan = plan_import(parse_rows("INVOICES", [planner_invoice()]), state)
    assert plan.counts["skips"] == 1 and plan.counts["assets_updated"] == 0


@pytest.mark.parametrize("field,value", [("asset_name", "Changed"), ("supplier_name", "Changed"), ("invoice_date", "2026-03-01"), ("room_id", "HK-P01-R999")])
def test_ac_us01_016_planner_changed_invoice_identity(field, value):
    assert plan_import(parse_rows("INVOICES", [planner_invoice(**{field: value})]), applied_planner_state()).blocked


def test_ac_us01_017_planner_duplicate_invoice():
    assert plan_import(parse_rows("INVOICES", [planner_invoice(), planner_invoice()]), planner_state()).blocked


def test_ac_us01_009_018_019_planner_reviewed_effects():
    state = applied_planner_state()
    plan = plan_import(parse_rows("INVOICES", [planner_invoice(line_id="new", invoice_date="2026-03-01", installation_date=None)]), state)
    update = plan.as_dict()["asset_updates"][0]
    assert update["before"]["asset_name"] == "Manager edit"
    assert update["after"]["installation_date"] is None
    assert update["after"]["override"] is None and update["clears_override"]
    assert update["override_history"]["action"] == "CLEAR_ON_INVOICE"
    assert update["override_history"]["invoice_update_asset_id"] == update["asset_id"]
    assert len(update["changes"]) == 6
    assert (update["expected_version"], update["resulting_version"]) == (7, 8)
    state["assets"][0]["version"] += 1
    # Change the actual target's version, which is part of reviewed effects.
    next(a for a in state["assets"] if a["asset_id"] == update["asset_id"])["version"] += 1
    assert plan != plan_import(parse_rows("INVOICES", [planner_invoice(line_id="new", invoice_date="2026-03-01", installation_date=None)]), state)


def test_ac_us01_023_planner_first_and_newer_equal_values():
    state = planner_state()
    row = planner_invoice(invoice_date="2025-01-01")
    assert plan_import(parse_rows("INVOICES", [row]), state).counts["assets_updated"] == 1
    state = applied_planner_state()
    assert plan_import(parse_rows("INVOICES", [planner_invoice(line_id="new", invoice_date="2026-03-01")]), state).counts["assets_updated"] == 1


def test_ac_us01_024_planner_older_differences_do_not_control():
    rows = [planner_invoice(line_id="old1", invoice_date="2026-01-01", asset_name="Old one"),
            planner_invoice(line_id="old2", invoice_date="2026-01-01", asset_name="Old two")]
    plan = plan_import(parse_rows("INVOICES", rows), applied_planner_state())
    assert not plan.blocked and plan.counts["historical_only_items"] == 2


def test_ac_us01_025_planner_new_complete_room_unchanged_property():
    rows = [dict(row, room_id="HK-P01-R002", room_number="002", asset_id=row["asset_id"].replace("R001", "R002")) for row in planner_baseline()]
    plan = plan_import(parse_rows(rows=rows), planner_state())
    assert not plan.blocked
    assert (plan.counts["properties_inserted"], plan.counts["rooms_inserted"], plan.counts["assets_inserted"]) == (0, 1, 3)
    assert plan_import(parse_rows(rows=rows[:1]), planner_state()).blocked


def test_ac_us01_006_007_008_022_planner_parser_diagnostics_and_empty():
    state = planner_state()
    for parsed in [parse_rows("INVOICES", [planner_invoice(useful_life_months=0)]), parse_rows("INVOICES", [], headers=("wrong",))]:
        plan = plan_import(parsed, state)
        assert plan.blocked and not plan.as_dict()["invoice_items"]
    assert plan_import(parse_rows("INVOICES", []), state).counts["invoice_items_inserted"] == 0
    plan = plan_import(parse_rows("INVOICES", [planner_invoice(installation_date=None, acquisition_cost="0", supplier_name=None)]), state)
    assert not plan.blocked and plan.counts["warnings"] == 3


def test_ac_us01_010_planner_separate_upload_order():
    import copy
    from src.services.imports import SNAPSHOT_FIELDS
    old = planner_invoice(line_id="old", invoice_date="2026-09-01", asset_name="Old")
    new = planner_invoice(line_id="new", invoice_date="2026-10-01", asset_name="New")
    results = []
    for order in ((old, new), (new, old)):
        state = copy.deepcopy(planner_state())
        for row in order:
            plan = plan_import(parse_rows("INVOICES", [row]), state).as_dict()
            for item in plan["invoice_items"]:
                state["invoice_items"].append(item)
            for update in plan["asset_updates"]:
                asset = next(a for a in state["assets"] if a["asset_id"] == update["asset_id"])
                asset.update({field: update["snapshot"][field] for field in SNAPSHOT_FIELDS[:4]})
                asset.update(source_cost=update["after"]["source"]["cost"], source_currency=update["after"]["source"]["currency"],
                             applied_invoice_date=update["invoice_date"], version=update["resulting_version"])
        asset = next(a for a in state["assets"] if a["facility_type"] == old["facility_type"])
        results.append((asset["asset_name"], asset["applied_invoice_date"], len(state["invoice_items"])))
    assert results == [("New", "2026-10-01", 2)] * 2


def test_ac_us01_013_planner_normalized_equivalent_snapshots():
    rows = [planner_invoice(line_id="a", acquisition_cost="120.250", purchase_date=date(2026, 1, 15)),
            planner_invoice(line_id="b", acquisition_cost=120.25, purchase_date=datetime(2026, 1, 15))]
    plan = plan_import(parse_rows("INVOICES", rows), planner_state())
    assert not plan.blocked and plan.counts["invoice_items_inserted"] == 2
    assert plan.counts["assets_updated"] == 1


def test_ac_us01_015_planner_older_repeat_after_edits():
    state = applied_planner_state()
    old = parse_rows("INVOICES", [planner_invoice(line_id="old", invoice_date="2025-01-01")]).normalized_rows[0].as_dict()
    asset = next(a for a in state["assets"] if a["facility_type"] == old["facility_type"])
    state["invoice_items"].append(dict(old, asset_id=asset["asset_id"]))
    plan = plan_import(parse_rows("INVOICES", [planner_invoice(line_id="old", invoice_date="2025-01-01")]), state)
    assert plan.counts["skips"] == 1 and plan.counts["assets_updated"] == 0


def test_ac_us01_006_planner_invalid_historical_row_blocks_surrounding_evidence():
    rows = [planner_invoice(line_id="old", invoice_date="2020-01-01", useful_life_months=0), planner_invoice(line_id="valid")]
    plan = plan_import(parse_rows("INVOICES", rows), planner_state())
    assert plan.blocked and plan.counts["invoice_items_inserted"] == 0


def test_ac_us01_009_planner_input_and_retained_plan_immutable():
    import copy
    state = planner_state()
    saved = copy.deepcopy(state)
    parsed = parse_rows("INVOICES", [planner_invoice()])
    plan = plan_import(parsed, state)
    assert state == saved
    detached = plan.as_dict()
    detached["asset_updates"][0]["before"]["asset_name"] = "Changed"
    assert plan == plan_import(parsed, state)
    asset = next(a for a in state["assets"] if a["facility_type"] == "LIGHTING")
    asset["asset_name"] = "Saved edit"
    assert plan != plan_import(parsed, state)


@pytest.mark.parametrize("workflow", ["ASSETS", "INVOICES"])
def test_ac_us01_006_workbook_normalizes_equivalent_values_and_preserves_coordinates(workflow):
    first = workbook_row(workflow)
    second = dict(first, acquisition_cost=120.25, purchase_date=datetime(2026, 1, 15), currency=" usd ")
    headers = tuple(reversed(headers_for(workflow)))
    result = parse_rows(workflow, [first, second], headers)
    assert not result.diagnostics
    assert result.normalized_rows[0].as_dict() == result.normalized_rows[1].as_dict()
    assert result.normalized_rows[0].as_dict()["room_number" if workflow == "ASSETS" else "invoice_id"] == ("001" if workflow == "ASSETS" else "0001")
    cost_cell = next(cell for cell in result.source_rows[0].cells if cell.field == "acquisition_cost")
    assert cost_cell.coordinate == ("B2" if workflow == "ASSETS" else "D2")
    assert (result.source_rows[0].file, result.source_rows[0].sheet, result.source_rows[0].row) == (
        "source.xlsx", "Assets" if workflow == "ASSETS" else "Invoices", 2)


@pytest.mark.parametrize("field,value", [
    ("asset_name", None), ("acquisition_cost", None), ("acquisition_cost", -1),
    ("acquisition_cost", "NaN"), ("acquisition_cost", "$1"), ("acquisition_cost", True),
    ("currency", "EUR"), ("currency", None), ("location", "HK"), ("facility_type", "OTHER"),
    ("purchase_date", "2026-02-30"), ("purchase_date", None), ("purchase_date", "01/02/2026"),
    ("installation_date", "2026-01-14"), ("useful_life_months", 0),
    ("useful_life_months", -1), ("useful_life_months", 1.5), ("useful_life_months", "12"),
    ("asset_id", 1), ("asset_id", None), ("room_id", "HK-P02-R001"),
    ("asset_id", "HK-P01-R002-A001"), ("property_id", "SG-P01"),
    ("lighting_status", "GOOD"), ("asset_name", "#VALUE!"),
])
def test_ac_us01_006_workbook_invalid_values_are_retained(field, value):
    result = parse_rows(rows=[dict(workbook_row(), **{field: value})])
    assert not result.normalized_rows
    assert len(result.source_rows) == 1
    diagnostic = next(item for item in result.blockers if item.field == field)
    assert (diagnostic.file, diagnostic.sheet, diagnostic.row, diagnostic.value) == ("source.xlsx", "Assets", 2, value)
    assert any(cell.field == field and cell.value == value for cell in result.source_rows[0].cells)


@pytest.mark.parametrize("filename,content,workflow", [
    ("file.xls", b"anything", "ASSETS"), ("file.csv", b"a,b", "ASSETS"),
    ("file.xlsx", b"broken ZIP", "ASSETS"), ("file.xlsx", b"", "ASSETS"),
    ("", b"", "ASSETS"), ("file.xlsx", b"", "OTHER"),
])
def test_ac_us01_007_unsupported_missing_unreadable_workbooks(filename, content, workflow):
    result = parse_workbook(content, filename=filename, workflow=workflow)
    assert result.blockers and not result.normalized_rows


@pytest.mark.parametrize("headers", [
    ASSET_HEADERS[:-1], ASSET_HEADERS + ("unexpected",), ASSET_HEADERS + ("asset_id",),
    ("PROPERTY_ID",) + ASSET_HEADERS[1:], (), (None,) + ASSET_HEADERS[1:],
    (" property_id ",) + ASSET_HEADERS[1:],
])
def test_ac_us01_007_exact_missing_duplicate_unexpected_headers(headers):
    result = parse_rows(headers=headers)
    assert result.blockers and not result.normalized_rows
    assert all(item.row == 1 and item.sheet == "Assets" for item in result.blockers)


@pytest.mark.parametrize("edit", [
    lambda workbook, sheet: workbook.create_sheet("Extra"),
    lambda workbook, sheet: setattr(sheet, "title", "Wrong"),
    lambda workbook, sheet: sheet.merge_cells("A2:B2"),
    lambda workbook, sheet: setattr(sheet["Y2"], "value", "=1+1"),
    lambda workbook, sheet: setattr(sheet["A1"], "value", '=CONCAT("property", "_id")'),
    lambda workbook, sheet: setattr(sheet["Z3"], "value", "=1"),
])
def test_ac_us01_007_sheets_merges_and_formulas_block(edit):
    result = parse_rows(rows=[workbook_row()], edit=edit)
    assert result.blockers and not result.normalized_rows


@pytest.mark.parametrize("workflow", ["ASSETS", "INVOICES"])
def test_ac_us01_008_warning_only_values(workflow):
    row = dict(workbook_row(workflow), installation_date="  ", acquisition_cost=0)
    if workflow == "INVOICES":
        row["supplier_name"] = " "
    result = parse_rows(workflow, [row])
    assert not result.blockers
    assert len(result.normalized_rows) == 1
    assert {item.field for item in result.warnings} == ({"installation_date", "acquisition_cost"} |
                                                       ({"supplier_name"} if workflow == "INVOICES" else set()))
    assert result.normalized_rows[0].as_dict()["acquisition_cost"] == "0"
    assert result.normalized_rows[0].as_dict()["installation_date"] is None


def test_ac_us01_009_results_are_deeply_immutable_and_detached():
    result = parse_rows(rows=[workbook_row()])
    with pytest.raises(FrozenInstanceError):
        result.source_rows[0].cells[0].value = "changed"
    with pytest.raises(FrozenInstanceError):
        result.normalized_rows[0].values = ()
    working = result.normalized_rows[0].as_dict()
    working["asset_name"] = "changed"
    assert result.normalized_rows[0].as_dict()["asset_name"] == "Lamp"
    warning = parse_rows(rows=[dict(workbook_row(), acquisition_cost=0)]).warnings[0]
    with pytest.raises(ValidationError) as failure:
        warning.value = 10
    assert "frozen" in str(failure.value)


@pytest.mark.parametrize("field,value", [
    ("invoice_id", 1), ("line_id", 1), ("room_id", "unknown"),
    ("invoice_date", "2026-02-30"), ("supplier_name", True),
])
def test_ac_us01_006_invoice_specific_fields(field, value):
    result = parse_rows("INVOICES", [dict(workbook_row("INVOICES"), **{field: value})])
    assert not result.normalized_rows
    assert any(item.field == field and item.value == value for item in result.blockers)


def test_ac_us01_006_excel_error_does_not_hide_independent_row_errors():
    result = parse_rows(rows=[dict(workbook_row(), asset_name="#VALUE!", acquisition_cost=-1)])
    assert {item.field for item in result.blockers} == {"asset_name", "acquisition_cost"}


@pytest.mark.parametrize("scenario,rows,headers,expected_blocked", [
    ("AC-US01-006", [{"asset_name": "Partial"}], None, True),
    ("AC-US01-007", [], ASSET_HEADERS[:-1], True),
    ("AC-US01-008", [dict(workbook_row(), installation_date=None, acquisition_cost=0)], None, False),
    ("AC-US01-009", [workbook_row()], None, False),
    ("AC-US01-022", [], None, False),
    ("AC-US02-009", [workbook_row()], None, False),
    ("AC-US02-014", [dict(workbook_row(), lighting_note="Note only")], None, True),
])
@pytest.mark.parametrize("store_fixture", ["store", "seeded_store"])
def test_parser_store_boundary_preserves_all_state_and_saves_no_workbook(
    request, tmp_path, monkeypatch, scenario, rows, headers, expected_blocked, store_fixture,
):
    store = request.getfixturevalue(store_fixture)
    before = store.path.read_bytes()
    generation = store.metadata().generation_id
    content = workbook_bytes(rows=rows, headers=headers)
    workspace = tmp_path / "parse-only"
    workspace.mkdir()
    monkeypatch.chdir(workspace)
    result = parse_workbook(content, filename="Assets.xlsx", workflow="ASSETS")
    assert bool(result.blockers) == expected_blocked
    assert store.path.read_bytes() == before
    assert store.metadata().generation_id == generation
    assert not list(workspace.iterdir())


@pytest.mark.parametrize("workflow", ["ASSETS", "INVOICES"])
def test_ac_us01_022_headers_only_empty_and_partial_rows(workflow):
    empty = parse_rows(workflow)
    assert not empty.diagnostics and not empty.source_rows and not empty.normalized_rows
    result = parse_rows(workflow, [{}, {field: " " for field in headers_for(workflow)}, workbook_row(workflow)])
    assert not result.diagnostics and len(result.normalized_rows) == 1
    assert result.normalized_rows[0].source.row == 4
    partial = parse_rows(workflow, [{"asset_name": "Partial"}])
    assert partial.blockers and len(partial.source_rows) == 1 and not partial.normalized_rows


@pytest.mark.parametrize("status", [None, "UNKNOWN", " unknown "])
def test_ac_us02_009_unassessed_unknown_is_independent(status):
    row = workbook_row()
    row.update(lighting_status=status, water_supply_status="HEALTHY",
               water_supply_observed_on="2026-01-20", water_supply_recorder=" Recorder ")
    result = parse_rows(rows=[row])
    assert not result.diagnostics
    values = result.normalized_rows[0].as_dict()
    assert values["lighting_status"] == values["air_conditioning_status"] == "UNKNOWN"
    assert values["lighting_recorder"] is values["lighting_observed_on"] is values["lighting_note"] is None
    assert values["water_supply_status"] == "HEALTHY"
    assert values["water_supply_recorder"] == "Recorder"


@pytest.mark.parametrize("system", ["lighting", "water_supply", "air_conditioning"])
@pytest.mark.parametrize("metadata", [
    {"status": "HEALTHY"}, {"status": "UNKNOWN", "note": "Only note"},
    {"observed_on": "2026-01-20", "recorder": "Recorder"},
    {"status": "CRITICAL", "observed_on": "2026-01-20"},
    {"status": "UNKNOWN", "recorder": "Recorder"},
    {"status": "HEALTHY", "observed_on": "2026-02-30", "recorder": "Recorder"},
])
def test_ac_us02_014_invalid_imported_assessment(system, metadata):
    row = dict(workbook_row(), **{f"{system}_{field}": value for field, value in metadata.items()})
    result = parse_rows(rows=[row])
    assert result.blockers and not result.normalized_rows
    assert all(item.field.startswith(system) and item.row == 2 for item in result.blockers)


def test_ac_us02_014_all_three_groups_report_errors_independently():
    row = dict(workbook_row(), lighting_status="BAD", water_supply_status="HEALTHY",
               air_conditioning_note="Note only")
    result = parse_rows(rows=[row])
    assert {item.field.split("_status")[0] for item in result.blockers if item.field.endswith("_status")} == {
        "lighting", "air_conditioning"}
    assert any(item.field == "water_supply_recorder" for item in result.blockers)


@pytest.mark.parametrize("status", ["HEALTHY", "ATTENTION_NEEDED", "CRITICAL", "UNKNOWN"])
def test_ac_us02_009_recorded_conditions_include_recorded_unknown(status):
    row = dict(workbook_row(), lighting_status=status, lighting_observed_on="2026-01-20",
               lighting_recorder="Recorder", lighting_note=" Note ")
    result = parse_rows(rows=[row])
    assert not result.diagnostics
    assert result.normalized_rows[0].as_dict()["lighting_status"] == status
    assert result.normalized_rows[0].as_dict()["lighting_note"] == "Note"


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_HASHES = {
    "invalid/Assets.xlsx": "caf81d1c37cec01be4715a1498193049dca64c93967d4fb0e36a262e527c3aad",
    "invalid/Invoices.xlsx": "7b933802f6e7382e1138801e3a707a56d3a89564981cfbcf9bc5a6ce3b24b72d",
    "valid/Assets.xlsx": "16862ba1ec2b12cf07d24459c9f024d15b705dd7cd44b91970cef8e9a79a2647",
    "valid/Invoices.xlsx": "1bae2192e28d52e66304af07c9d15a602df0d2d9c0aa76f124eedef45164edb7",
}


@pytest.mark.parametrize("relative,expected_hash", FIXTURE_HASHES.items())
def test_supplied_workbooks_parse_without_modification(relative, expected_hash):
    path = ROOT / "sample/2026-10-03" / relative
    content = path.read_bytes()
    assert hashlib.sha256(content).hexdigest() == expected_hash
    workflow = "ASSETS" if path.stem == "Assets" else "INVOICES"
    result = parse_workbook(content, filename=path.name, workflow=workflow)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash
    if relative.startswith("valid"):
        assert not result.diagnostics and len(result.normalized_rows) == 36
    elif workflow == "ASSETS":
        # Supplied defects are cross-row consistency/category checks, owned by F002B.
        assert not result.diagnostics and len(result.normalized_rows) == 36
    else:
        assert len(result.source_rows) == 38
        assert {item.field for item in result.blockers} == {
            "facility_type", "currency", "purchase_date", "installation_date", "useful_life_months"}


@pytest.mark.parametrize("workflow", ["ASSETS", "INVOICES"])
def test_blank_templates_use_approved_schema_and_have_no_data(workflow):
    name = "Assets" if workflow == "ASSETS" else "Invoices"
    path = ROOT / "sample_data/spreadsheets/templates" / f"{name}.xlsx"
    workbook = load_workbook(path, data_only=False)
    try:
        assert workbook.sheetnames == [name]
        sheet = workbook[name]
        assert sheet.max_row == 1
        assert tuple(cell.value for cell in sheet[1]) == headers_for(workflow)
        assert not sheet.merged_cells.ranges
        assert all(cell.data_type != "f" for cell in sheet[1])
    finally:
        workbook.close()
    result = parse_workbook(path.read_bytes(), filename=path.name, workflow=workflow)
    assert not result.diagnostics and not result.source_rows and not result.normalized_rows

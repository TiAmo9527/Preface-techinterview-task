"""F001B shared value foundation; no workbook parser/preview acceptance claim."""

from datetime import date, datetime, timezone
from decimal import Decimal

import pytest

from src.services import validators as v
from src.services.contracts import AssetSnapshot, validate_request
from src.services.errors import CommandError


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

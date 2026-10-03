"""FB-01 pure normalization shared by workbook and service boundaries.

Workbook structure, target existence and cross-record prerequisites belong to the
later parser/planner or mutation transaction. These helpers never write state.
"""

from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
import re


CURRENCIES = frozenset({"HKD", "SGD", "GBP", "JPY", "USD"})
REGIONS = {"HK": "HONG_KONG", "SG": "SINGAPORE", "LDN": "LONDON", "JP": "JAPAN"}
LOCATIONS = frozenset(REGIONS.values())
SYSTEMS = frozenset({"LIGHTING", "WATER_SUPPLY", "AIR_CONDITIONING"})
CONDITIONS = frozenset({"HEALTHY", "ATTENTION_NEEDED", "CRITICAL", "UNKNOWN"})
SEVERITIES = frozenset({"LOW", "MEDIUM", "CRITICAL"})
TICKET_STATUSES = frozenset({"OPEN", "IN_PROGRESS", "RESOLVED"})
WORKFLOWS = frozenset({"ASSETS", "INVOICES"})
_PROPERTY = r"(?:S[0-9]+-)?(?P<region>HK|SG|LDN|JP)-P[0-9]{2,}"
_PATTERNS = {"property": _PROPERTY, "room": _PROPERTY + r"-R[0-9]{3,}",
             "asset": _PROPERTY + r"-R[0-9]{3,}-A[0-9]{3,}"}
_DECIMAL = re.compile(r"[0-9]+(?:\.[0-9]+)?", re.ASCII)


def text(value: object, *, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if type(value) is not str:
        raise ValueError("Text is required; numeric identities and booleans are not text")
    result = value.strip()
    if not result:
        if optional:
            return None
        raise ValueError("Text cannot be blank")
    return result


def enum_value(value: object, choices: frozenset[str]) -> str:
    result = text(value).upper()
    if result not in choices:
        raise ValueError("Unsupported enum value; choose one of " + ", ".join(sorted(choices)))
    return result


def source_identity(value: object, kind: str, *, parent: str | None = None,
                    location: str | None = None) -> str:
    result = text(value)
    match = re.fullmatch(_PATTERNS[kind], result, flags=re.ASCII)
    if match is None:
        raise ValueError(f"Malformed {kind} identity")
    if location is not None and REGIONS[match["region"]] != enum_value(location, LOCATIONS):
        raise ValueError("Identity region differs from location")
    if parent is not None:
        parent_kind, suffix = {"room": ("property", "-R"), "asset": ("room", "-A")}[kind]
        normalized_parent = source_identity(parent, parent_kind)
        if result.rsplit(suffix, 1)[0] != normalized_parent:
            raise ValueError("Identity must use the exact parent prefix and namespace")
    return result


def calendar_date(value: object, *, optional: bool = False) -> str | None:
    if optional and (value is None or (type(value) is str and not value.strip())):
        return None
    if isinstance(value, datetime):
        if value.tzinfo is not None or value.time() != time():
            raise ValueError("A calendar date cannot contain a time or timezone")
        return value.date().isoformat()
    if type(value) is date:
        return value.isoformat()
    if type(value) is not str or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value.strip()) is None:
        raise ValueError("An ISO YYYY-MM-DD date is required")
    return date.fromisoformat(value.strip()).isoformat()


def decimal_amount(value: object, *, positive: bool = False) -> str:
    if type(value) not in (str, int, float, Decimal):
        raise ValueError("A finite decimal amount is required")
    if type(value) is str:
        value = value.strip()
        if _DECIMAL.fullmatch(value) is None:
            raise ValueError("Decimal text cannot contain signs, exponents or grouping/currency symbols")
    try:
        amount = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError("Invalid decimal amount") from error
    if not amount.is_finite() or amount < 0 or (positive and amount <= 0):
        raise ValueError("Amount must be finite and positive" if positive else "Amount must be finite and non-negative")
    # Formatting/zero removal is exact and does not use Decimal context rounding.
    if amount == 0:
        return "0"
    result = format(amount, "f")
    return result.rstrip("0").rstrip(".") if "." in result else result


def whole_months(value: object) -> int:
    if type(value) not in (int, float, Decimal) or type(value) is bool:
        raise ValueError("Useful life must be a positive whole number of months")
    number = Decimal(str(value))
    if not number.is_finite() or number <= 0 or number != number.to_integral_value():
        raise ValueError("Useful life must be a positive whole number of months")
    return int(number)


def date_order(purchase_date: object, installation_date: object) -> tuple[str, str | None]:
    purchase = calendar_date(purchase_date)
    installation = calendar_date(installation_date, optional=True)
    if installation is not None and installation < purchase:
        raise ValueError("Installation date cannot precede purchase date")
    return purchase, installation


def observation_metadata(status: object = None, observed_on: object = None,
                         recorder: object = None, note: object = None) -> dict:
    state = enum_value(status, CONDITIONS) if text(status, optional=True) is not None else None
    observed = calendar_date(observed_on, optional=True)
    recorded_by = text(recorder, optional=True)
    normalized_note = text(note, optional=True)
    if state in (None, "UNKNOWN") and observed is None and recorded_by is None and normalized_note is None:
        return {"status": "UNKNOWN", "observed_on": None, "recorder": None, "note": None}
    if state is None or observed is None or recorded_by is None:
        raise ValueError("Recorded assessments require status, date and recorder")
    return {"status": state, "observed_on": observed, "recorder": recorded_by, "note": normalized_note}

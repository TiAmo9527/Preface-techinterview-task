"""FB-03 versioned fictional configuration, independently readable when FX fails."""

from copy import deepcopy
from datetime import date
from decimal import Decimal
import math
from typing import Mapping

from pydantic import ValidationError

from src.services.clock import operational_time
from src.services.contracts import (ConfigResponse, Contract, Diagnostic, FinanceEnvelope,
                                    FXConfiguration, Language, Owner, Version)
from src.services import validators as v


DEFAULT_CONFIGURATION = {
    "configuration_version": 1,
    "owners": [
        {"owner_id": "owner-alex", "display_name": "Alex Chan"},
        {"owner_id": "owner-mei", "display_name": "Mei Wong"},
        {"owner_id": "owner-sam", "display_name": "Sam Lee"},
    ],
    "delivered_languages": ["en"],
    "fx": {
        "as_of_date": "2026-10-03",
        "disclaimer": "Fictional fixed rates — not live market rates",
        "usd_per_unit": {"HKD": "0.128", "SGD": "0.74", "GBP": "1.25", "JPY": "0.0067", "USD": "1"},
    },
}


class LocalConfiguration(Contract):
    configuration_version: Version
    owners: list[Owner]
    delivered_languages: list[Language]
    # Raw FX is retained for assumptions even when it cannot support reporting.
    fx: dict | None


def local_configuration(config: Mapping | None = None) -> LocalConfiguration:
    result = LocalConfiguration.model_validate(deepcopy(DEFAULT_CONFIGURATION if config is None else dict(config)))
    owner_ids = [owner.owner_id for owner in result.owners]
    if not owner_ids or len(owner_ids) != len(set(owner_ids)):
        raise ValueError("Owner identities must be non-empty and unique")
    if "en" not in result.delivered_languages or len(result.delivered_languages) != len(set(result.delivered_languages)):
        raise ValueError("Delivered languages must be unique and include English")
    return result


def validate_owner(owner_id: object, config: LocalConfiguration) -> str | None:
    identity = v.text(owner_id, optional=True)
    if identity is not None and identity not in {owner.owner_id for owner in config.owners}:
        raise ValueError("Owner must be selected from the local owner configuration")
    return identity


def validated_fx(raw: object) -> tuple[FXConfiguration | None, list[Diagnostic]]:
    """Detect duplicate normalized keys before a mapping could overwrite them."""
    try:
        if type(raw) is not dict:
            raise ValueError("FX configuration is missing")
        rates = raw.get("usd_per_unit")
        if type(rates) is not dict:
            raise ValueError("FX requires a currency-to-rate mapping")
        normalized = {}
        for currency, rate in rates.items():
            key = v.enum_value(currency, v.CURRENCIES)
            if key in normalized:
                raise ValueError(f"Duplicate FX currency: {key}")
            normalized[key] = v.decimal_amount(rate, positive=True)
        fx = FXConfiguration.model_validate({**raw, "usd_per_unit": normalized})
        return fx, []
    except (ValueError, ValidationError) as error:
        if isinstance(error, ValidationError):
            diagnostics = [Diagnostic(entity="FX", field=".".join(map(str, item["loc"])) or "fx",
                                      reason=item["msg"]) for item in error.errors(include_context=False, include_url=False)]
        else:
            diagnostics = [Diagnostic(entity="FX", field="usd_per_unit", reason=str(error))]
        return None, diagnostics


def finance_configuration_failure(config: LocalConfiguration) -> FinanceEnvelope | None:
    """No calculations here: downstream reporting consumes this failure or valid FX."""
    fx, diagnostics = validated_fx(config.fx)
    return FinanceEnvelope(status="INVALID_CONFIGURATION", diagnostics=diagnostics, results=None) if fx is None else None


def configuration_response(*, generation_id: str, schema_version: int,
                           config: LocalConfiguration, clock=None) -> ConfigResponse:
    now = operational_time(clock)
    fx, diagnostics = validated_fx(config.fx)
    return ConfigResponse(generation_id=generation_id, schema_version=schema_version,
                          configuration_version=config.configuration_version,
                          operational_date=now.operational_date, operational_time=now.operational_time,
                          timezone=now.timezone, fx=fx, configured_fx=_display_config(config.fx), owners=config.owners,
                          delivered_languages=config.delivered_languages, diagnostics=diagnostics)


def _display_config(value):
    """Expose invalid settings honestly without emitting NaN or Python objects."""
    if isinstance(value, dict):
        return {str(key): _display_config(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_display_config(item) for item in value]
    if isinstance(value, (Decimal, date)):
        return str(value)
    if type(value) is float and not math.isfinite(value):
        return str(value)
    if value is None or type(value) in (str, int, float, bool):
        return value
    return repr(value)

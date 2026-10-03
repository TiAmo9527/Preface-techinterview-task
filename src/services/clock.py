"""FB-03 operational clock; reporting dates never enter this boundary."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable
from zoneinfo import ZoneInfo


TIMEZONE = "Asia/Hong_Kong"


@dataclass(frozen=True)
class OperationalTime:
    operational_date: str
    operational_time: str
    utc_instant: str
    timezone: str = TIMEZONE


def operational_time(clock: Callable[[], datetime] | None = None) -> OperationalTime:
    instant = (clock or (lambda: datetime.now(timezone.utc)))()
    if not isinstance(instant, datetime) or instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError("The operational clock must return a timezone-aware datetime")
    local = instant.astimezone(ZoneInfo(TIMEZONE))
    return OperationalTime(local.date().isoformat(), local.isoformat(),
                           instant.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"))

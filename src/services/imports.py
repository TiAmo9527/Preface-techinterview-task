"""IM-02 deterministic, read-only import planning. Generated IDs belong to commit."""

from collections import defaultdict
from dataclasses import dataclass
import json

from src.services.contracts import AssetSnapshot, Diagnostic
from src.services import validators as v
from src.services.workbooks import ParsedWorkbook, headers_for


SNAPSHOT_FIELDS = tuple(AssetSnapshot.model_fields)
PROPERTY_FIELDS = ("property_id", "property_name", "location", "city")
ROOM_FIELDS = ("room_id", "property_id", "room_number")
SYSTEM_PREFIXES = ("lighting", "water_supply", "air_conditioning")


def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


@dataclass(frozen=True)
class ImportPlan:
    """Canonical retained value; detached access prevents preview-input mutation."""

    canonical: str

    def as_dict(self) -> dict:
        return json.loads(self.canonical)

    @property
    def counts(self) -> dict:
        return self.as_dict()["counts"]

    @property
    def blocked(self) -> bool:
        return bool(self.counts["blockers"])


def _pick(row, fields):
    return {field: row[field] for field in fields}


def _room(row):
    return {**_pick(row, ROOM_FIELDS), "assessments": {
        prefix.upper(): {suffix: row[f"{prefix}_{suffix}"]
                         for suffix in ("status", "observed_on", "recorder", "note")}
        for prefix in SYSTEM_PREFIXES
    }}


def _state(asset):
    source = {"cost": asset["source_cost"], "currency": asset["source_currency"]}
    override = None if asset["override_cost"] is None else {
        "cost": asset["override_cost"], "currency": asset["override_currency"]}
    return {**_pick(asset, SNAPSHOT_FIELDS[:4]), "source": source, "override": override,
            "effective": override or source, "applied_invoice_date": asset["applied_invoice_date"]}


def plan_import(normalized_rows: ParsedWorkbook, saved_state: dict) -> ImportPlan:
    """Plan parser-approved input against one snapshot without modifying either.

    saved_state is the detached value from read_import_state. Accepting the whole
    parsed result keeps invalid source diagnostics in the same all-or-nothing plan.
    """
    parsed = normalized_rows
    diagnostics = [item.model_dump(mode="json") for item in parsed.diagnostics]
    effects = {key: [] for key in ("properties", "rooms", "assets", "invoice_items",
                                   "asset_updates", "historical_only_items", "skips")}
    properties = {row["property_id"]: row for row in saved_state["properties"]}
    rooms = {row["room_id"]: row for row in saved_state["rooms"]}
    assets = {row["asset_id"]: row for row in saved_state["assets"]}
    items = {(row["invoice_id"], row["line_id"]): row for row in saved_state["invoice_items"]}
    targets = defaultdict(list)
    for asset in assets.values():
        targets[(asset["room_id"], asset["facility_type"])].append(asset)

    def issue(row, field, reason):
        values = row.as_dict()
        diagnostics.append(Diagnostic(
            entity="asset" if parsed.workflow == "ASSETS" else "invoice_item",
            file=row.source.file, sheet=row.source.sheet, row=row.source.row,
            field=field, value=values.get(field),
            identity=values.get("asset_id") or f"{values.get('invoice_id')}/{values.get('line_id')}",
            reason=reason).model_dump(mode="json"))

    def coordinates(rows):
        return sorted(({"file": row.source.file, "sheet": row.source.sheet,
                        "row": row.source.row,
                        "cells": {cell.field: cell.coordinate for cell in row.source.cells}}
                       for row in rows), key=_canonical)

    rows = sorted(parsed.normalized_rows, key=lambda row: (_canonical(row.as_dict()), _canonical(coordinates([row]))))
    identities = defaultdict(list)
    for row in rows:
        value = row.as_dict()
        identity = value["asset_id"] if parsed.workflow == "ASSETS" else (value["invoice_id"], value["line_id"])
        identities[identity].append(row)
    for group in identities.values():
        if len(group) > 1:
            for row in group:
                issue(row, "asset_id" if parsed.workflow == "ASSETS" else "line_id", "Duplicate source identity inside upload; remove every duplicate")

    if parsed.workflow == "ASSETS":
        property_groups, room_groups = defaultdict(list), defaultdict(list)
        for row in rows:
            value = row.as_dict()
            property_groups[value["property_id"]].append(row)
            room_groups[value["room_id"]].append(row)
        for identity, group in property_groups.items():
            baseline = _pick(group[0].as_dict(), PROPERTY_FIELDS)
            for row in group:
                if _pick(row.as_dict(), PROPERTY_FIELDS) != baseline:
                    issue(row, "property_id", "Repeated property baseline disagrees")
                if identity in properties and _pick(properties[identity], PROPERTY_FIELDS) != _pick(row.as_dict(), PROPERTY_FIELDS):
                    issue(row, "property_id", "Existing immutable property baseline differs")
            if identity not in properties:
                effects["properties"].append({**baseline, "coordinates": coordinates(group)})
        labels = {(row["property_id"], row["room_number"]): row["room_id"] for row in rooms.values()}
        for identity, group in room_groups.items():
            baseline = _room(group[0].as_dict())
            categories = [row.as_dict()["facility_type"] for row in group]
            if identity not in rooms and (len(categories) != 3 or set(categories) != v.SYSTEMS):
                issue(group[0], "facility_type", "New room requires exactly one asset in each of the three categories")
            if len(categories) != len(set(categories)):
                issue(group[0], "facility_type", "Repeated room category inside upload")
            label = (baseline["property_id"], baseline["room_number"])
            if label in labels and labels[label] != identity:
                issue(group[0], "room_number", "Room number is already used in this property")
            labels[label] = identity
            for row in group:
                if _room(row.as_dict()) != baseline:
                    issue(row, "room_id", "Repeated room baseline or assessment disagrees")
                if identity in rooms and _room(row.as_dict()) != _pick(rooms[identity], (*ROOM_FIELDS, "assessments")):
                    issue(row, "room_id", "Existing immutable room baseline differs")
            if identity not in rooms:
                effects["rooms"].append({**baseline, "version": 1, "coordinates": coordinates(group)})
        for row in rows:
            value = row.as_dict()
            identity = value["asset_id"]
            snapshot = _pick(value, SNAPSHOT_FIELDS)
            if identity in assets:
                asset = assets[identity]
                if (asset["room_id"], asset["facility_type"], asset["baseline"]) != (value["room_id"], value["facility_type"], snapshot):
                    issue(row, "asset_id", "Existing immutable asset source differs")
                else:
                    effects["skips"].append({"asset_id": identity})
            elif targets[(value["room_id"], value["facility_type"])]:
                issue(row, "facility_type", "Existing room/category is occupied; baseline cannot replace it")
            else:
                effects["assets"].append({**_pick(value, ("asset_id", "room_id", "facility_type")),
                                          "baseline": snapshot, "version": 1, "coordinates": coordinates([row])})
    elif parsed.workflow == "INVOICES":
        incoming = defaultdict(list)
        for row in rows:
            value = row.as_dict()
            target = targets[(value["room_id"], value["facility_type"])]
            if value["room_id"] not in rooms or len(target) != 1:
                issue(row, "room_id", "Room/category must resolve to exactly one existing asset")
                continue
            identity = (value["invoice_id"], value["line_id"])
            if identity in items:
                if _pick(items[identity], headers_for("INVOICES")) != value or items[identity]["asset_id"] != target[0]["asset_id"]:
                    issue(row, "line_id", "Existing immutable invoice source differs")
                else:
                    effects["skips"].append(_pick(value, ("invoice_id", "line_id")))
                continue
            item = {**value, "asset_id": target[0]["asset_id"], "coordinates": coordinates([row])}
            effects["invoice_items"].append(item)
            incoming[item["asset_id"]].append((row, item))
        for identity, group in incoming.items():
            asset = assets[identity]
            evidence = [item for item in items.values() if item["asset_id"] == identity] + [item for _, item in group]
            maximum = max(item["invoice_date"] for item in evidence)
            controlling = sorted((item for item in evidence if item["invoice_date"] == maximum),
                                 key=lambda item: (item["invoice_id"], item["line_id"]))
            snapshot = _pick(controlling[0], SNAPSHOT_FIELDS)
            if any(_pick(item, SNAPSHOT_FIELDS) != snapshot for item in controlling):
                for row, _ in group:
                    issue(row, "invoice_date", "Different six-field snapshots at the controlling maximum date")
                continue
            applies = asset["applied_invoice_date"] is None or maximum > asset["applied_invoice_date"]
            for _, item in group:
                if not applies or item["invoice_date"] < maximum:
                    effects["historical_only_items"].append(_pick(item, ("invoice_id", "line_id", "asset_id")))
            if not applies:
                continue
            before = _state(asset)
            after = {**_pick(snapshot, SNAPSHOT_FIELDS[:4]),
                     "source": {"cost": snapshot["acquisition_cost"], "currency": snapshot["currency"]},
                     "override": None, "effective": {"cost": snapshot["acquisition_cost"], "currency": snapshot["currency"]},
                     "applied_invoice_date": maximum}
            refs = lambda entries: [_pick(item, ("invoice_id", "line_id")) for item in sorted(entries, key=lambda item: (item["invoice_id"], item["line_id"]))]
            override_history = None if before["override"] is None else {
                "action": "CLEAR_ON_INVOICE", "recorder": "SYSTEM", "reason": "Cleared by controlling invoice update",
                "invoice_update_asset_id": identity, "before": before, "after": after}
            effects["asset_updates"].append({"asset_id": identity, "invoice_date": maximum,
                "expected_version": asset["version"], "resulting_version": asset["version"] + 1,
                "before": before, "after": after, "snapshot": snapshot,
                "before_refs": refs([item for item in items.values() if item["asset_id"] == identity and item["invoice_date"] == asset["applied_invoice_date"]]),
                "after_refs": refs(controlling), "override_history": override_history,
                "clears_override": before["override"] is not None,
                "changes": [{"field": field, "before": (before["effective"]["cost" if field == "acquisition_cost" else "currency"] if field in ("acquisition_cost", "currency") else before[field]), "after": snapshot[field]} for field in SNAPSHOT_FIELDS]})
    # A blocked plan exposes diagnostics and skips, but no executable effects.
    diagnostics.sort(key=_canonical)
    blocked = sum(item["severity"] == "BLOCKER" for item in diagnostics)
    if blocked:
        for key in effects:
            if key != "skips":
                effects[key] = []
    for entries in effects.values():
        entries.sort(key=_canonical)
    count_fields = {"properties_inserted": "properties", "rooms_inserted": "rooms",
                    "assets_inserted": "assets", "invoice_items_inserted": "invoice_items",
                    "assets_updated": "asset_updates", "historical_only_items": "historical_only_items",
                    "skips": "skips"}
    counts = {field: len(effects[key]) for field, key in count_fields.items()}
    counts.update(warnings=sum(item["severity"] == "WARNING" for item in diagnostics), blockers=blocked)
    return ImportPlan(_canonical({"workflow": parsed.workflow, "counts": counts, "diagnostics": diagnostics, **effects}))

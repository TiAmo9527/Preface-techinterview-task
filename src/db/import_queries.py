"""Import reads/writes on the caller's connection; never own transactions."""

import json
import sqlite3

from src.db.store import SaveFailed


def _json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def write_import_plan(connection, plan, *, upload_id, filename, instant):
    """Persist approved effects and count actual writes. The coordinator owns receipts."""
    counts = dict(plan["counts"])
    for key in ("properties_inserted", "rooms_inserted", "assets_inserted",
                "invoice_items_inserted", "assets_updated"):
        counts[key] = 0
    if upload_id is None:
        return counts
    connection.execute("INSERT INTO uploads VALUES (?,?,?,?)", (upload_id, plan["workflow"], filename, instant))
    for row in plan["properties"]:
        counts["properties_inserted"] += connection.execute(
            "INSERT INTO properties VALUES (?,?,?,?)",
            tuple(row[key] for key in ("property_id", "property_name", "location", "city"))).rowcount
    for row in plan["rooms"]:
        counts["rooms_inserted"] += connection.execute("INSERT INTO rooms VALUES (?,?,?,?)",
            (row["room_id"], row["property_id"], row["room_number"], _json(row["assessments"]))).rowcount
        for system, observation in row["assessments"].items():
            connection.execute("INSERT INTO observations VALUES (?,?,?,?,?,?,1)",
                (row["room_id"], system, *(observation[key] for key in ("status", "observed_on", "recorder", "note"))))
    for row in plan["assets"]:
        snap = row["baseline"]
        counts["assets_inserted"] += connection.execute(
            "INSERT INTO assets VALUES (?,?,?,?,?,?,?,NULL,?,?,NULL,NULL,1)",
            (row["asset_id"], row["room_id"], row["facility_type"],
             *(snap[key] for key in ("asset_name", "purchase_date", "installation_date", "useful_life_months", "acquisition_cost", "currency")))).rowcount
        connection.execute("INSERT INTO asset_baselines VALUES (?,?)", (row["asset_id"], _json(snap)))
        for source in row["coordinates"]:
            connection.execute("""INSERT INTO baseline_coordinates
                SELECT ?,?,?,property_id,room_id,? FROM rooms WHERE room_id=?""",
                (upload_id, source["row"], source["sheet"], row["asset_id"], row["room_id"]))
    for row in plan["invoice_items"]:
        snap = {key: row[key] for key in ("asset_name", "purchase_date", "installation_date", "useful_life_months", "acquisition_cost", "currency")}
        source = row["coordinates"][0]
        counts["invoice_items_inserted"] += connection.execute("INSERT INTO invoice_items VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (row["invoice_id"], row["line_id"], row["asset_id"], row["room_id"], row["facility_type"],
             _json(snap), row["invoice_date"], row["supplier_name"], upload_id, source["sheet"], source["row"])).rowcount
    for row in plan["asset_updates"]:
        after = row["after"]
        count = connection.execute("""UPDATE assets SET asset_name=?, purchase_date=?, installation_date=?,
            useful_life_months=?, source_cost=?, source_currency=?, override_cost=NULL,
            override_currency=NULL, applied_invoice_date=?, version=? WHERE asset_id=? AND version=?""",
            (*(after[key] for key in ("asset_name", "purchase_date", "installation_date", "useful_life_months")),
             after["source"]["cost"], after["source"]["currency"], row["invoice_date"], row["resulting_version"],
             row["asset_id"], row["expected_version"])).rowcount
        if count != 1:
            raise SaveFailed()
        counts["assets_updated"] += count
        connection.execute("INSERT INTO invoice_updates VALUES (?,?,?,?,?,?,?)",
            (row["event_id"], row["asset_id"], row["invoice_date"], _json(row["before"]), _json(after), upload_id, instant))
        for role, refs in (("BEFORE", row["before_refs"]), ("AFTER", row["after_refs"])):
            for ref in refs:
                connection.execute("INSERT INTO invoice_update_refs VALUES (?,?,?,?)",
                    (row["event_id"], role, ref["invoice_id"], ref["line_id"]))
        history = row["override_history"]
        if history is not None:
            connection.execute("INSERT INTO override_history VALUES (?,?,?,?,?,?,?,?,?)",
                (history["event_id"], row["asset_id"], history["action"], _json(history["before"]), _json(history["after"]),
                 history["reason"], history["recorder"], instant, row["event_id"]))
    return counts


def read_import_state(connection: sqlite3.Connection) -> dict:
    properties = [dict(row) for row in connection.execute("SELECT * FROM properties ORDER BY property_id")]
    rooms = []
    for row in connection.execute("SELECT * FROM rooms ORDER BY room_id"):
        room = dict(row)
        room["assessments"] = json.loads(room.pop("baseline_assessments_json"))
        rooms.append(room)
    assets = []
    for row in connection.execute("SELECT a.*, b.snapshot_json FROM assets a JOIN asset_baselines b USING(asset_id) ORDER BY asset_id"):
        asset = dict(row)
        asset["baseline"] = json.loads(asset.pop("snapshot_json"))
        assets.append(asset)
    items = []
    for row in connection.execute("SELECT * FROM invoice_items ORDER BY invoice_id, line_id"):
        item = dict(row)
        item.update(json.loads(item.pop("snapshot_json")))
        items.append(item)
    return {"properties": properties, "rooms": rooms, "assets": assets, "invoice_items": items}

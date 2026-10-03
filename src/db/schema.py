"""Version-one SQLite schema from technical-design.md section 2.

Calendar, decimal, identity-parent, and cross-record validation belongs to services.
These statements enforce persisted structural invariants without implicit commits.
"""

SCHEMA_VERSION = 1

TABLE_STATEMENTS = (
    """CREATE TABLE store_metadata (
        singleton_id INTEGER PRIMARY KEY CHECK (singleton_id = 1),
        schema_version INTEGER NOT NULL CHECK (schema_version >= 1),
        generation_id TEXT NOT NULL CHECK (trim(generation_id) <> '')
    )""",
    """CREATE TABLE properties (
        property_id TEXT PRIMARY KEY NOT NULL CHECK (trim(property_id) <> ''),
        property_name TEXT NOT NULL CHECK (trim(property_name) <> ''),
        location TEXT NOT NULL CHECK (location IN ('HONG_KONG','SINGAPORE','LONDON','JAPAN')),
        city TEXT NOT NULL CHECK (trim(city) <> '')
    )""",
    """CREATE TABLE rooms (
        room_id TEXT PRIMARY KEY NOT NULL CHECK (trim(room_id) <> ''),
        property_id TEXT NOT NULL REFERENCES properties(property_id) ON DELETE RESTRICT,
        room_number TEXT NOT NULL CHECK (trim(room_number) <> ''),
        baseline_assessments_json TEXT NOT NULL CHECK (json_valid(baseline_assessments_json)),
        UNIQUE (property_id, room_number)
    )""",
    """CREATE TABLE assets (
        asset_id TEXT PRIMARY KEY NOT NULL CHECK (trim(asset_id) <> ''),
        room_id TEXT NOT NULL REFERENCES rooms(room_id) ON DELETE RESTRICT,
        facility_type TEXT NOT NULL CHECK (facility_type IN ('LIGHTING','WATER_SUPPLY','AIR_CONDITIONING')),
        asset_name TEXT NOT NULL CHECK (trim(asset_name) <> ''),
        purchase_date TEXT NOT NULL CHECK (trim(purchase_date) <> ''),
        installation_date TEXT CHECK (installation_date IS NULL OR trim(installation_date) <> ''),
        useful_life_months INTEGER NOT NULL CHECK (typeof(useful_life_months) = 'integer' AND useful_life_months > 0),
        applied_invoice_date TEXT CHECK (applied_invoice_date IS NULL OR trim(applied_invoice_date) <> ''),
        source_cost TEXT NOT NULL CHECK (trim(source_cost) <> ''),
        source_currency TEXT NOT NULL CHECK (source_currency IN ('HKD','SGD','GBP','JPY','USD')),
        override_cost TEXT CHECK (override_cost IS NULL OR trim(override_cost) <> ''),
        override_currency TEXT CHECK (override_currency IN ('HKD','SGD','GBP','JPY','USD')),
        version INTEGER NOT NULL CHECK (typeof(version) = 'integer' AND version >= 1),
        CHECK ((override_cost IS NULL AND override_currency IS NULL) OR
               (override_cost IS NOT NULL AND override_currency IS NOT NULL)),
        UNIQUE (room_id, facility_type)
    )""",
    """CREATE TABLE asset_baselines (
        asset_id TEXT PRIMARY KEY NOT NULL REFERENCES assets(asset_id) ON DELETE RESTRICT,
        snapshot_json TEXT NOT NULL CHECK (json_valid(snapshot_json))
    )""",
    """CREATE TABLE observations (
        room_id TEXT NOT NULL REFERENCES rooms(room_id) ON DELETE RESTRICT,
        system TEXT NOT NULL CHECK (system IN ('LIGHTING','WATER_SUPPLY','AIR_CONDITIONING')),
        status TEXT NOT NULL CHECK (status IN ('HEALTHY','ATTENTION_NEEDED','CRITICAL','UNKNOWN')),
        observed_on TEXT CHECK (observed_on IS NULL OR trim(observed_on) <> ''),
        recorder TEXT CHECK (recorder IS NULL OR trim(recorder) <> ''),
        note TEXT CHECK (note IS NULL OR trim(note) <> ''),
        version INTEGER NOT NULL CHECK (typeof(version) = 'integer' AND version >= 1),
        CHECK ((status = 'UNKNOWN' AND observed_on IS NULL AND recorder IS NULL AND note IS NULL) OR
               (observed_on IS NOT NULL AND recorder IS NOT NULL)),
        PRIMARY KEY (room_id, system)
    )""",
    """CREATE TABLE uploads (
        upload_id TEXT PRIMARY KEY NOT NULL CHECK (trim(upload_id) <> ''),
        workflow TEXT NOT NULL CHECK (workflow IN ('ASSETS','INVOICES')),
        filename TEXT NOT NULL CHECK (trim(filename) <> ''),
        imported_at TEXT NOT NULL CHECK (trim(imported_at) <> '')
    )""",
    """CREATE TABLE baseline_coordinates (
        upload_id TEXT NOT NULL REFERENCES uploads(upload_id) ON DELETE RESTRICT,
        row_number INTEGER NOT NULL CHECK (typeof(row_number) = 'integer' AND row_number >= 2),
        sheet TEXT NOT NULL CHECK (trim(sheet) <> ''),
        property_id TEXT NOT NULL REFERENCES properties(property_id) ON DELETE RESTRICT,
        room_id TEXT NOT NULL REFERENCES rooms(room_id) ON DELETE RESTRICT,
        asset_id TEXT NOT NULL REFERENCES assets(asset_id) ON DELETE RESTRICT,
        PRIMARY KEY (upload_id, row_number)
    )""",
    """CREATE TABLE invoice_items (
        invoice_id TEXT NOT NULL CHECK (trim(invoice_id) <> ''),
        line_id TEXT NOT NULL CHECK (trim(line_id) <> ''),
        asset_id TEXT NOT NULL REFERENCES assets(asset_id) ON DELETE RESTRICT,
        room_id TEXT NOT NULL REFERENCES rooms(room_id) ON DELETE RESTRICT,
        facility_type TEXT NOT NULL CHECK (facility_type IN ('LIGHTING','WATER_SUPPLY','AIR_CONDITIONING')),
        snapshot_json TEXT NOT NULL CHECK (json_valid(snapshot_json)),
        invoice_date TEXT NOT NULL CHECK (trim(invoice_date) <> ''),
        supplier_name TEXT CHECK (supplier_name IS NULL OR trim(supplier_name) <> ''),
        upload_id TEXT NOT NULL REFERENCES uploads(upload_id) ON DELETE RESTRICT,
        sheet TEXT NOT NULL CHECK (trim(sheet) <> ''),
        row_number INTEGER NOT NULL CHECK (typeof(row_number) = 'integer' AND row_number >= 2),
        PRIMARY KEY (invoice_id, line_id)
    )""",
    """CREATE TABLE invoice_updates (
        event_id TEXT PRIMARY KEY NOT NULL CHECK (trim(event_id) <> ''),
        asset_id TEXT NOT NULL REFERENCES assets(asset_id) ON DELETE RESTRICT,
        invoice_date TEXT NOT NULL CHECK (trim(invoice_date) <> ''),
        before_json TEXT NOT NULL CHECK (json_valid(before_json)),
        after_json TEXT NOT NULL CHECK (json_valid(after_json)),
        upload_id TEXT NOT NULL REFERENCES uploads(upload_id) ON DELETE RESTRICT,
        happened_at TEXT NOT NULL CHECK (trim(happened_at) <> '')
    )""",
    """CREATE TABLE invoice_update_refs (
        event_id TEXT NOT NULL REFERENCES invoice_updates(event_id) ON DELETE RESTRICT,
        role TEXT NOT NULL CHECK (role IN ('BEFORE','AFTER')),
        invoice_id TEXT NOT NULL,
        line_id TEXT NOT NULL,
        PRIMARY KEY (event_id, role, invoice_id, line_id),
        FOREIGN KEY (invoice_id, line_id) REFERENCES invoice_items(invoice_id, line_id) ON DELETE RESTRICT
    )""",
    """CREATE TABLE override_history (
        event_id TEXT PRIMARY KEY NOT NULL CHECK (trim(event_id) <> ''),
        asset_id TEXT NOT NULL REFERENCES assets(asset_id) ON DELETE RESTRICT,
        action TEXT NOT NULL CHECK (action IN ('SET_OVERRIDE','RESET_TO_SOURCE','CLEAR_ON_INVOICE')),
        before_json TEXT NOT NULL CHECK (json_valid(before_json)),
        after_json TEXT NOT NULL CHECK (json_valid(after_json)),
        reason TEXT NOT NULL CHECK (trim(reason) <> ''),
        recorder TEXT NOT NULL CHECK (trim(recorder) <> ''),
        happened_at TEXT NOT NULL CHECK (trim(happened_at) <> ''),
        invoice_update_id TEXT REFERENCES invoice_updates(event_id) ON DELETE RESTRICT
    )""",
    """CREATE TABLE maintenance_tickets (
        ticket_id TEXT PRIMARY KEY NOT NULL CHECK (trim(ticket_id) <> ''),
        room_id TEXT NOT NULL REFERENCES rooms(room_id) ON DELETE RESTRICT,
        asset_id TEXT REFERENCES assets(asset_id) ON DELETE RESTRICT,
        description TEXT NOT NULL CHECK (trim(description) <> ''),
        severity TEXT NOT NULL CHECK (severity IN ('LOW','MEDIUM','CRITICAL')),
        status TEXT NOT NULL CHECK (status IN ('OPEN','IN_PROGRESS','RESOLVED')),
        owner_id TEXT CHECK (owner_id IS NULL OR trim(owner_id) <> ''),
        target_date TEXT CHECK (target_date IS NULL OR trim(target_date) <> ''),
        opened_at TEXT NOT NULL CHECK (trim(opened_at) <> ''),
        updated_at TEXT NOT NULL CHECK (trim(updated_at) <> ''),
        resolved_at TEXT CHECK (resolved_at IS NULL OR trim(resolved_at) <> ''),
        resolution_note TEXT CHECK (resolution_note IS NULL OR trim(resolution_note) <> ''),
        version INTEGER NOT NULL CHECK (typeof(version) = 'integer' AND version >= 1),
        CHECK (status = 'OPEN' OR owner_id IS NOT NULL),
        CHECK (status <> 'RESOLVED' OR (resolution_note IS NOT NULL AND resolved_at IS NOT NULL))
    )""",
    """CREATE TABLE maintenance_history (
        event_id TEXT PRIMARY KEY NOT NULL CHECK (trim(event_id) <> ''),
        ticket_id TEXT NOT NULL REFERENCES maintenance_tickets(ticket_id) ON DELETE RESTRICT,
        action TEXT NOT NULL CHECK (action IN ('CREATE','EDIT','START','RESOLVE')),
        before_json TEXT NOT NULL CHECK (json_valid(before_json)),
        after_json TEXT NOT NULL CHECK (json_valid(after_json)),
        recorder TEXT NOT NULL CHECK (trim(recorder) <> ''),
        happened_at TEXT NOT NULL CHECK (trim(happened_at) <> ''),
        resulting_version INTEGER NOT NULL CHECK (typeof(resulting_version) = 'integer' AND resulting_version >= 1),
        UNIQUE (ticket_id, resulting_version)
    )""",
    """CREATE TABLE command_receipts (
        generation_id TEXT NOT NULL CHECK (trim(generation_id) <> ''),
        submission_id TEXT NOT NULL CHECK (trim(submission_id) <> ''),
        operation TEXT NOT NULL CHECK (trim(operation) <> ''),
        payload_hash TEXT NOT NULL CHECK (trim(payload_hash) <> ''),
        response_json TEXT NOT NULL CHECK (json_valid(response_json)),
        PRIMARY KEY (generation_id, submission_id)
    )""",
)

# UPDATE protection preserves evidence. DELETE remains available for the approved reset.
IMMUTABLE_TABLES = (
    "properties", "rooms", "asset_baselines", "uploads", "baseline_coordinates",
    "invoice_items", "invoice_updates", "invoice_update_refs", "override_history",
    "maintenance_history", "command_receipts",
)

TRIGGER_STATEMENTS = tuple(
    f"""CREATE TRIGGER {table}_immutable_update BEFORE UPDATE ON {table}
    BEGIN SELECT RAISE(ABORT, 'Immutable evidence cannot be updated'); END"""
    for table in IMMUTABLE_TABLES
)

MIGRATION_STATEMENTS = TABLE_STATEMENTS + TRIGGER_STATEMENTS

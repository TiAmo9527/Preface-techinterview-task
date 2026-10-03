"""Approved PR-04 deletion order and counts on the caller's connection."""

DELETE_ORDER = (
    "command_receipts", "override_history", "invoice_update_refs", "invoice_updates",
    "maintenance_history", "maintenance_tickets", "invoice_items", "baseline_coordinates",
    "uploads", "observations", "asset_baselines", "assets", "rooms", "properties",
)


def domain_counts(connection):
    def count(table):
        # Table names are implementation constants, never request values.
        return connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]

    return {
        "properties": count("properties"), "rooms": count("rooms"), "assets": count("assets"),
        "observations": count("observations"), "tickets": count("maintenance_tickets"),
        "uploads": count("uploads"), "invoice_items": count("invoice_items"),
        "histories": sum(count(name) for name in ("override_history", "invoice_updates", "maintenance_history")),
        "receipts": count("command_receipts"),
    }


def clear_domain(connection):
    for table in DELETE_ORDER:
        connection.execute(f'DELETE FROM "{table}"')


def replace_generation(connection, generation_id):
    connection.execute("UPDATE store_metadata SET generation_id=? WHERE singleton_id=1", (generation_id,))

"""Parameterized receipt queries on a connection owned by the caller."""

import sqlite3


def current_generation(connection: sqlite3.Connection) -> str:
    row = connection.execute("SELECT generation_id FROM store_metadata WHERE singleton_id=1").fetchone()
    if row is None:
        raise sqlite3.DatabaseError("Missing store metadata")
    return row[0]


def find_receipt(connection: sqlite3.Connection, generation_id: str, submission_id: str):
    return connection.execute(
        "SELECT operation, payload_hash, response_json FROM command_receipts "
        "WHERE generation_id=? AND submission_id=?", (generation_id, submission_id),
    ).fetchone()


def insert_receipt(connection: sqlite3.Connection, generation_id: str, submission_id: str,
                   operation: str, payload_hash: str, response_json: str) -> None:
    connection.execute(
        "INSERT INTO command_receipts (generation_id, submission_id, operation, payload_hash, response_json) "
        "VALUES (?, ?, ?, ?, ?)", (generation_id, submission_id, operation, payload_hash, response_json),
    )

"""Caller-owned synchronous SQLite operations and atomic schema initialization."""

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
import sqlite3
from typing import Iterator
from urllib.parse import quote
from uuid import UUID, uuid4

from src.db import schema

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE_PATH = REPOSITORY_ROOT / "runtime" / "app.sqlite3"
BUSY_TIMEOUT_SECONDS = 5


class StoreError(RuntimeError):
    """Safe persistence failure. The original exception remains available for local logs."""


class StoreBusy(StoreError):
    code = "STORE_BUSY"

    def __init__(self) -> None:
        super().__init__("The local store is busy. Retry the operation when it is available.")


class SaveFailed(StoreError):
    code = "SAVE_FAILED"

    def __init__(self) -> None:
        super().__init__("The database operation failed. No transaction changes were committed.")


class SchemaError(StoreError):
    """Unsupported or damaged store. Initialization never replaces existing state."""

    code = "UNSUPPORTED_STORE"


@dataclass(frozen=True)
class StoreMetadata:
    schema_version: int
    generation_id: str


@dataclass(frozen=True)
class Store:
    path: Path = DEFAULT_STORE_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", Path(self.path).resolve())

    def _connect(self, *, write: bool) -> sqlite3.Connection:
        if write:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            database = str(self.path)
        else:
            database = f"file:{quote(self.path.as_posix(), safe='/:')}?mode=ro"
        connection = sqlite3.connect(
            database, uri=not write, timeout=BUSY_TIMEOUT_SECONDS,
            isolation_level=None, check_same_thread=True,
        )
        try:
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(f"PRAGMA busy_timeout = {BUSY_TIMEOUT_SECONDS * 1000}")
            if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
                raise SchemaError("Foreign-key enforcement is unavailable. Startup is blocked.")
        except BaseException:
            connection.close()
            raise
        return connection

    @contextmanager
    def transaction(self, *, write: bool = True) -> Iterator[sqlite3.Connection]:
        """The caller passes this connection to nested operations without another commit."""
        connection = None
        try:
            connection = self._connect(write=write)
            connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
            yield connection
            connection.commit()
        except (sqlite3.Error, OSError) as error:
            if connection is not None and connection.in_transaction:
                connection.rollback()
            code = getattr(error, "sqlite_errorcode", 0) or 0
            if code & 0xFF in (sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED):
                raise StoreBusy() from error
            raise SaveFailed() from error
        except BaseException:
            if connection is not None and connection.in_transaction:
                connection.rollback()
            raise
        finally:
            if connection is not None:
                connection.close()

    def initialize(self) -> StoreMetadata:
        """Create version one atomically or validate and preserve an existing store."""
        with self.transaction() as connection:
            tables = {
                row[0] for row in connection.execute(
                    "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
                )
            }
            if not tables:
                for statement in schema.MIGRATION_STATEMENTS:
                    connection.execute(statement)
                connection.execute(
                    "INSERT INTO store_metadata (singleton_id, schema_version, generation_id) VALUES (1, ?, ?)",
                    (schema.SCHEMA_VERSION, str(uuid4())),
                )
            elif "store_metadata" not in tables:
                raise SchemaError("This store is unversioned. Restore a supported store before startup.")
            metadata = self._metadata(connection)
            if metadata.schema_version != schema.SCHEMA_VERSION:
                raise SchemaError(
                    f"Schema version {metadata.schema_version} is unsupported. "
                    f"This application supports version {schema.SCHEMA_VERSION}. Use a compatible application."
                )
            self._validate_schema(connection)
        return metadata

    @staticmethod
    def _metadata(connection: sqlite3.Connection) -> StoreMetadata:
        try:
            rows = connection.execute(
                "SELECT singleton_id, schema_version, generation_id FROM store_metadata"
            ).fetchall()
            if len(rows) != 1 or rows[0][0] != 1:
                raise ValueError("Invalid singleton")
            version, generation = rows[0][1], rows[0][2]
            if type(version) is not int or str(UUID(generation)) != generation:
                raise ValueError("Invalid metadata")
        except (sqlite3.Error, ValueError, TypeError, AttributeError) as error:
            raise SchemaError("Store metadata is invalid. Restore a supported store before startup.") from error
        return StoreMetadata(version, generation)

    @staticmethod
    def _validate_schema(connection: sqlite3.Connection) -> None:
        # Compare this version's persisted DDL, including constraints and immutable-update guards.
        expected = {" ".join(sql.split()).rstrip(";") for sql in schema.MIGRATION_STATEMENTS}
        actual = {
            " ".join(row[0].split()).rstrip(";") for row in connection.execute(
                "SELECT sql FROM sqlite_schema WHERE type IN ('table', 'trigger') AND name NOT LIKE 'sqlite_%'"
            )
        }
        if actual != expected:
            raise SchemaError("Schema version 1 is incomplete or changed. Restore a supported store before startup.")
        if connection.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
            raise SchemaError("This store requires DELETE journal mode. Startup is blocked.")
        if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise SchemaError("The store contains broken foreign keys. Restore valid data before startup.")

    def metadata(self) -> StoreMetadata:
        with self.transaction(write=False) as connection:
            return self._metadata(connection)

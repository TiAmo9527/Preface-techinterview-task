"""PR-03 coordination of already-normalized commands, without domain mutations.

Endpoint models/validators supply normalized fields and an explicit allowlist. Domain
callbacks use only the supplied connection, perform prerequisites, write histories,
initialize created versions at 1, and increment each mutated version once. They must
neither commit nor open another transaction. Their response contains saved versions.
"""

from dataclasses import dataclass
import hashlib
import json
import sqlite3
from typing import Callable, Mapping
from uuid import UUID

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from src.db import SaveFailed, Store, StoreBusy
from src.db import command_queries
from src.services.errors import CommandError


class CommandEnvelope(BaseModel):
    """Shared identity envelope extended by the endpoint models in contracts.py."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    generation_id: str
    submission_id: str

    @field_validator("generation_id", "submission_id")
    @classmethod
    def canonical_uuid(cls, value: str) -> str:
        if str(UUID(value)) != value:
            raise ValueError("A canonical UUID is required")
        return value


def canonical_json(value) -> str:
    """JSON boundary values only. Amounts must already be normalized decimal strings."""
    def validate(item):
        if item is None or type(item) in (str, int, bool):
            return
        if type(item) is list:
            for child in item:
                validate(child)
            return
        if type(item) is dict and all(type(key) is str for key in item):
            for child in item.values():
                validate(child)
            return
        raise ValueError("Only normalized JSON values are permitted")
    validate(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


@dataclass(frozen=True)
class NormalizedCommand:
    generation_id: str
    submission_id: str
    operation: str
    payload_json: str

    @property
    def payload_hash(self) -> str:
        return hashlib.sha256(self.payload_json.encode("utf-8")).hexdigest()


def prepare_command(*, envelope: dict, operation: str, targets: dict, fields: dict,
                    allowed_fields: frozenset[str], expected_versions: dict | None = None) -> NormalizedCommand:
    """Freeze caller-normalized input; omission and explicit null remain different.

    The allowlist belongs to the endpoint service, never to the browser. Generated
    timestamps/IDs are created by its mutation callback and do not enter this payload.
    """
    versions = {} if expected_versions is None else expected_versions
    try:
        identity = CommandEnvelope.model_validate(envelope)
        if type(operation) is not str or not operation.strip():
            raise ValueError("Operation is required")
        if type(targets) is not dict or any(
            type(key) is not str or not key.strip() or type(value) is not str or not value.strip()
            for key, value in targets.items()
        ):
            raise ValueError("Targets must be text identities")
        if type(fields) is not dict or not fields.keys() <= allowed_fields:
            raise ValueError("Unexpected or protected command fields")
        if type(versions) is not dict or not versions.keys() <= targets.keys() or any(
            type(version) is not int or version < 1 for version in versions.values()
        ):
            raise ValueError("Expected versions must be positive integers for named targets")
        payload = canonical_json({"targets": targets, "fields": fields, "expected_versions": versions})
    except (ValidationError, ValueError, TypeError) as error:
        raise CommandError("INVALID_INPUT") from error
    return NormalizedCommand(identity.generation_id, identity.submission_id, operation, payload)


LoadRecords = Callable[[sqlite3.Connection, dict], Mapping[str, dict | None]]
Mutate = Callable[[sqlite3.Connection, dict, Mapping[str, dict]], dict]


def execute_command(store: Store, command: NormalizedCommand, *, load_records: LoadRecords, mutate: Mutate) -> dict:
    """Check generation/receipt before invoking any target or preview prerequisite."""
    generation = None
    payload = json.loads(command.payload_json)
    try:
        with store.transaction() as connection:
            generation = command_queries.current_generation(connection)
            if command.generation_id != generation:
                raise CommandError("STALE_STORE", generation_id=generation)
            receipt = command_queries.find_receipt(connection, generation, command.submission_id)
            if receipt is not None:
                if receipt[0] != command.operation or receipt[1] != command.payload_hash:
                    raise CommandError("SUBMISSION_CONFLICT", generation_id=generation)
                response = json.loads(receipt[2])
            else:
                records = load_records(connection, payload["targets"])
                for alias, identity in payload["targets"].items():
                    saved = records.get(alias)
                    if saved is None:
                        raise CommandError("RECORD_NOT_FOUND", details={"target": alias, "identity": identity},
                                           generation_id=generation)
                    if alias in payload["expected_versions"] and saved["version"] != payload["expected_versions"][alias]:
                        raise CommandError("STALE_RECORD", details={"target": alias, "latest": saved}, generation_id=generation)
                response = mutate(connection, payload["fields"], records)
                if type(response) is not dict or ("generation_id" in response and response["generation_id"] != generation):
                    raise SaveFailed()
                try:
                    response_json = canonical_json({**response, "generation_id": generation})
                except ValueError as error:
                    raise SaveFailed() from error
                command_queries.insert_receipt(connection, generation, command.submission_id, command.operation,
                                               command.payload_hash, response_json)
                response = json.loads(response_json)
        # Expose success only after transaction exit has committed (including replay).
        return response
    except CommandError as error:
        if error.generation_id is None:
            error.generation_id = generation
        raise
    except (StoreBusy, SaveFailed) as error:
        raise CommandError(error.code, generation_id=generation) from error

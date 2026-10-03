"""PR-04 reset and read-only shell/config snapshots, without feature reporting."""

import logging
from uuid import uuid4

from src.db import StoreBusy, SaveFailed
from src.db.command_queries import current_generation
from src.db import reset_queries
from src.services.configuration import configuration_response, local_configuration
from src.services.contracts import ResetRequest, ResetResponse
from src.services.errors import CommandError

logger = logging.getLogger(__name__)


def read_configuration(store, *, config=None, clock=None):
    with store.transaction(write=False) as connection:
        metadata = store._metadata(connection)
        return configuration_response(generation_id=metadata.generation_id,
                                      schema_version=metadata.schema_version,
                                      config=local_configuration(config), clock=clock)


def shell_snapshot(store):
    with store.transaction(write=False) as connection:
        return {"generation_id": current_generation(connection), "counts": reset_queries.domain_counts(connection)}


def reset_store(store, request: ResetRequest, *, evict_previews=None):
    generation = None
    try:
        with store.transaction() as connection:
            generation = current_generation(connection)
            if request.generation_id != generation:
                raise CommandError("STALE_STORE", generation_id=generation)
            reset_queries.clear_domain(connection)
            replacement = str(uuid4())
            while replacement == generation:
                replacement = str(uuid4())
            reset_queries.replace_generation(connection, replacement)
            result = ResetResponse(generation_id=replacement, counts=reset_queries.domain_counts(connection))
    except (StoreBusy, SaveFailed) as error:
        raise CommandError(error.code, generation_id=generation) from error
    # F002C registers its locked, generation-selective registry operation here.
    # Cleanup errors cannot turn committed deletion into a false rollback response.
    if evict_previews is not None:
        try:
            evict_previews(generation)
        except Exception:
            logger.exception("Old-generation preview eviction failed after committed reset")
    return result

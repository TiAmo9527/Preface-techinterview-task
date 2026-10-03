"""Structured service failures; thin HTTP routes consume the status and body later."""

from copy import deepcopy


ERROR_STATUS = {
    "INVALID_INPUT": 422,
    "DOMAIN_RULE": 422,
    "RECORD_NOT_FOUND": 404,
    "STALE_STORE": 409,
    "STALE_RECORD": 409,
    "STALE_PREVIEW": 409,
    "PREVIEW_EXPIRED": 409,
    "SUBMISSION_CONFLICT": 409,
    "STORE_BUSY": 503,
    "SAVE_FAILED": 500,
}


class CommandError(Exception):
    def __init__(self, code: str, *, details: dict | None = None, generation_id: str | None = None):
        self.code = code
        self.status_code = ERROR_STATUS[code]
        self.message_key = f"errors.{code.lower()}"
        self.details = deepcopy(details) if details is not None else {}
        # Null means current metadata could not be read, for example while acquiring a lock.
        self.generation_id = generation_id
        super().__init__(self.message_key)

    def as_dict(self) -> dict:
        return {
            "code": self.code, "message_key": self.message_key,
            "details": deepcopy(self.details), "generation_id": self.generation_id,
        }

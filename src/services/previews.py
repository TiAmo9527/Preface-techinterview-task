"""IM-03 bounded process-local review and atomic import confirmation."""

from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from threading import RLock
from uuid import uuid4

from src.db.command_queries import current_generation
from src.db.import_queries import read_import_state, write_import_plan
from src.services.clock import operational_time
from src.services.contracts import ImportPreviewResponse, execute_validated_command
from src.services.errors import CommandError
from src.services.imports import ImportPlan, plan_import
from src.services.workbooks import ParsedWorkbook, parse_workbook


@dataclass(frozen=True)
class Preview:
    preview_id: str
    generation_id: str
    parsed: ParsedWorkbook
    plan: ImportPlan
    expires_at: datetime

    def response(self) -> ImportPreviewResponse:
        plan = self.plan.as_dict()
        return ImportPreviewResponse(
            generation_id=self.generation_id, preview_id=self.preview_id,
            workflow=self.parsed.workflow, counts=plan["counts"],
            diagnostics=plan["diagnostics"],
            asset_changes=[{key: row[key] for key in ("asset_id", "changes", "clears_override")}
                           for row in plan["asset_updates"]],
            expires_at=self.expires_at.isoformat().replace("+00:00", "Z"))


class PreviewRegistry:
    """Never hold this lock while acquiring a database lock. Entries are immutable."""

    def __init__(self, *, clock=None):
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self._entries = OrderedDict()
        self._lock = RLock()

    def _now(self):
        # Reuse aware-clock validation and canonical UTC conversion.
        return datetime.fromisoformat(operational_time(self.clock).utc_instant.replace("Z", "+00:00"))

    def _prune(self, now):
        for identity, entry in list(self._entries.items()):
            if entry.expires_at <= now:
                del self._entries[identity]

    def add(self, generation, parsed, plan):
        with self._lock:
            now = self._now()
            self._prune(now)
            entry = Preview(str(uuid4()), generation, parsed, plan, now + timedelta(minutes=30))
            self._entries[entry.preview_id] = entry
            while len(self._entries) > 20:
                self._entries.popitem(last=False)
            return entry

    def get(self, identity, generation):
        with self._lock:
            self._prune(self._now())
            entry = self._entries.get(identity)
            if entry is None:
                raise CommandError("PREVIEW_EXPIRED", generation_id=generation)
            if entry.generation_id != generation:
                raise CommandError("STALE_STORE", generation_id=generation)
            return entry

    def evict_generation(self, generation):
        with self._lock:
            for identity, entry in list(self._entries.items()):
                if entry.generation_id == generation:
                    del self._entries[identity]


def preview_import(store, registry, data, *, filename, workflow):
    parsed = parse_workbook(data, filename=filename, workflow=workflow)
    with store.transaction(write=False) as connection:
        generation = current_generation(connection)
        plan = plan_import(parsed, read_import_state(connection))
        # Register while the snapshot is still held; reset cannot commit before this.
        return registry.add(generation, parsed, plan).response()


def confirm_import(store, registry, request, *, clock=None):
    def mutate(connection, fields, records):
        entry = registry.get(fields["preview_id"], request.generation_id)
        plan = plan_import(entry.parsed, read_import_state(connection))
        if plan != entry.plan:
            replacement = registry.add(request.generation_id, entry.parsed, plan)
            raise CommandError("STALE_PREVIEW", details={"preview": replacement.response().model_dump(mode="json")})
        if plan.blocked:
            raise CommandError("DOMAIN_RULE", details={"diagnostics": plan.as_dict()["diagnostics"]})
        effects = plan.as_dict()
        has_evidence = any(effects[key] for key in ("properties", "rooms", "assets", "invoice_items"))
        upload_id = str(uuid4()) if has_evidence else None
        instant = operational_time(clock).utc_instant if has_evidence else None
        for update in effects["asset_updates"]:
            update["event_id"] = str(uuid4())
            if update["override_history"] is not None:
                update["override_history"]["event_id"] = str(uuid4())
        counts = write_import_plan(connection, effects, upload_id=upload_id,
                                   filename=entry.parsed.filename, instant=instant)
        return {"counts": counts, "upload_id": upload_id}

    return execute_validated_command(store, request, load_records=lambda connection, targets: {}, mutate=mutate)

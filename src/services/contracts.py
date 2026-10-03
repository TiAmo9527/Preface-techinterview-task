"""FB-02 internal endpoint contracts, without routes or feature mutations.

Dates/amounts normalize through the same helpers used by later workbook parsing.
Only endpoint-specific request models can select production command allowlists.
PATCH callers must use supplied_fields(), then check merged saved values inside
their caller-owned transaction. A missing optional field is not an explicit clear.
"""

from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Annotated, ClassVar, Literal, TypeVar
from uuid import UUID

from pydantic import (BaseModel, BeforeValidator, ConfigDict, Field, JsonValue,
                      ValidationError, model_validator)

from src.db import SaveFailed, Store
from src.services.commands import (CommandEnvelope, LoadRecords, Mutate, NormalizedCommand,
                                   execute_command, prepare_command)
from src.services.errors import CommandError
from src.services import validators as v


def canonical_uuid(value: object) -> str:
    if type(value) is not str or str(UUID(value)) != value:
        raise ValueError("A canonical UUID is required")
    return value


def money_string(value: object) -> str:
    if type(value) is not str:
        raise ValueError("JSON amounts must be decimal strings")
    return v.decimal_amount(value)


def formatted_money_string(value: object) -> str:
    # Calculation jobs format after aggregation. Preserve their trailing places.
    money_string(value)
    return value.strip()


def utc_instant(value: object) -> str:
    if type(value) is not str or not value.endswith("Z"):
        raise ValueError("A UTC ISO instant ending in Z is required")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed) or "T" not in value:
        raise ValueError("A UTC ISO instant is required")
    return parsed.isoformat().replace("+00:00", "Z")


Text = Annotated[str, BeforeValidator(v.text)]
OptionalText = Annotated[str | None, BeforeValidator(lambda x: v.text(x, optional=True))]
UUIDText = Annotated[str, BeforeValidator(canonical_uuid)]
Calendar = Annotated[str, BeforeValidator(v.calendar_date)]
OptionalCalendar = Annotated[str | None, BeforeValidator(lambda x: v.calendar_date(x, optional=True))]
Money = Annotated[str, BeforeValidator(money_string)]
FormattedMoney = Annotated[str, BeforeValidator(formatted_money_string)]
Months = Annotated[int, BeforeValidator(v.whole_months)]
Version = Annotated[int, Field(ge=1)]
Count = Annotated[int, Field(ge=0)]
Instant = Annotated[str, BeforeValidator(utc_instant)]
PropertyID = Annotated[str, BeforeValidator(lambda x: v.source_identity(x, "property"))]
RoomID = Annotated[str, BeforeValidator(lambda x: v.source_identity(x, "room"))]
AssetID = Annotated[str, BeforeValidator(lambda x: v.source_identity(x, "asset"))]
Currency = Annotated[Literal["HKD", "SGD", "GBP", "JPY", "USD"],
                     BeforeValidator(lambda x: v.enum_value(x, v.CURRENCIES))]
Location = Annotated[Literal["HONG_KONG", "SINGAPORE", "LONDON", "JAPAN"],
                     BeforeValidator(lambda x: v.enum_value(x, v.LOCATIONS))]
System = Annotated[Literal["LIGHTING", "WATER_SUPPLY", "AIR_CONDITIONING"],
                   BeforeValidator(lambda x: v.enum_value(x, v.SYSTEMS))]
Condition = Annotated[Literal["HEALTHY", "ATTENTION_NEEDED", "CRITICAL", "UNKNOWN"],
                      BeforeValidator(lambda x: v.enum_value(x, v.CONDITIONS))]
Severity = Annotated[Literal["LOW", "MEDIUM", "CRITICAL"],
                     BeforeValidator(lambda x: v.enum_value(x, v.SEVERITIES))]
TicketStatus = Annotated[Literal["OPEN", "IN_PROGRESS", "RESOLVED"],
                         BeforeValidator(lambda x: v.enum_value(x, v.TICKET_STATUSES))]
Workflow = Annotated[Literal["ASSETS", "INVOICES"],
                     BeforeValidator(lambda x: v.enum_value(x, v.WORKFLOWS))]
CurrencyMode = Literal["USD", "LOCAL_TRANSACTION"]
Language = Literal["en", "zh-Hant", "zh-Hans", "ja"]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True, allow_inf_nan=False)


class Diagnostic(Contract):
    severity: Literal["BLOCKER", "WARNING"] = "BLOCKER"
    entity: Text
    field: Text
    reason: Text
    file: Text | None = None
    sheet: Text | None = None
    row: Annotated[int, Field(ge=1)] | None = None
    identity: str | None = None
    value: JsonValue = None


class ErrorResponse(Contract):
    code: Literal["INVALID_INPUT", "DOMAIN_RULE", "RECORD_NOT_FOUND", "STALE_STORE",
                  "STALE_RECORD", "STALE_PREVIEW", "PREVIEW_EXPIRED", "SUBMISSION_CONFLICT",
                  "STORE_BUSY", "SAVE_FAILED"]
    message_key: Text
    details: dict[str, JsonValue]
    generation_id: UUIDText | None


T = TypeVar("T", bound=BaseModel)


def validate_request(model: type[T], value: object, *, generation_id: str | None = None,
                     file: str | None = None, sheet: str | None = None,
                     row: int | None = None) -> T:
    """Translate boundary failures without exposing exception/context objects."""
    try:
        return model.model_validate(value)
    except ValidationError as error:
        diagnostics = []
        for item in error.errors(include_url=False, include_context=False):
            offending = item.get("input")
            # A whole rejected body may contain files or nested non-JSON values.
            display_value = offending if type(offending) in (str, int, bool, type(None)) else repr(offending)
            diagnostic = Diagnostic(entity=model.__name__, field=".".join(map(str, item["loc"])) or "request",
                                    reason=item["msg"], value=display_value, file=file, sheet=sheet, row=row)
            diagnostics.append(diagnostic.model_dump(mode="json", exclude_none=True))
        raise CommandError("INVALID_INPUT", details={"diagnostics": diagnostics},
                           generation_id=generation_id) from error


class ConfigRequest(Contract):
    pass


class ScopeRequest(Contract):
    location: Location | None = None
    property_id: PropertyID | None = None
    room_id: RoomID | None = None

    @model_validator(mode="after")
    def parents(self):
        if self.property_id is not None:
            v.source_identity(self.property_id, "property", location=self.location)
        if self.room_id is not None:
            v.source_identity(self.room_id, "room", parent=self.property_id, location=self.location)
        return self


class OverviewRequest(ScopeRequest):
    financial_date: Calendar | None = None
    currency_mode: CurrencyMode = "USD"


class RoomRequest(Contract):
    financial_date: Calendar | None = None
    currency_mode: CurrencyMode = "USD"


class MaintenanceListRequest(ScopeRequest):
    view: Literal["UNRESOLVED", "RESOLVED"] = "UNRESOLVED"


class AssetEvidenceRequest(Contract):
    pass


class MaintenanceDetailRequest(Contract):
    pass


class MutationRequest(CommandEnvelope):
    operation: ClassVar[str]
    target_kind: ClassVar[str | None] = None
    target_alias: ClassVar[str | None] = None

    def supplied_fields(self) -> dict:
        return self.model_dump(mode="json", exclude_unset=True,
                               exclude={"generation_id", "submission_id", "expected_version"})

    def to_command(self, *, target_id: str | None = None, system: str | None = None) -> NormalizedCommand:
        """Bind validated body/path values to PR-03, with a server-owned operation."""
        try:
            targets = {}
            if self.target_kind == "observation":
                room = v.source_identity(target_id, "room")
                targets = {"observation": f"{room}/{v.enum_value(system, v.SYSTEMS)}"}
            elif self.target_kind is not None:
                identity = canonical_uuid(target_id) if self.target_kind == "ticket" else v.source_identity(target_id, self.target_kind)
                targets = {self.target_alias: identity}
                if system is not None:
                    raise ValueError("System is only permitted for observation commands")
            elif target_id is not None or system is not None:
                raise ValueError("This command has no path target")
            if isinstance(self, MaintenanceCreateRequest):
                targets = {"room": self.room_id}
                if self.asset_id is not None:
                    targets["asset"] = self.asset_id
            versions = {self.target_alias: self.expected_version} if isinstance(self, EditRequest) else {}
            return prepare_command(
                envelope={"generation_id": self.generation_id, "submission_id": self.submission_id},
                operation=self.operation, targets=targets, fields=self.supplied_fields(),
                allowed_fields=frozenset(type(self).model_fields) - {"generation_id", "submission_id", "expected_version"},
                expected_versions=versions,
            )
        except (ValueError, TypeError) as error:
            raise CommandError("INVALID_INPUT", details={"field": "target", "reason": str(error)}) from error


class EditRequest(MutationRequest):
    expected_version: Version


class ObservationSaveRequest(EditRequest):
    operation = "observation.save"
    target_kind = "observation"
    target_alias = "observation"
    status: Condition
    observed_on: Calendar
    recorder: Text
    note: OptionalText = None


class ObservationClearRequest(EditRequest):
    operation = "observation.clear"
    target_kind = "observation"
    target_alias = "observation"


class AssetPatchRequest(EditRequest):
    operation = "asset.edit"
    target_kind = "asset"
    target_alias = "asset"
    # Defaults express omission only; explicit null is rejected on nonnullable fields.
    asset_name: Text = None
    purchase_date: Calendar = None
    installation_date: OptionalCalendar = None
    useful_life_months: Months = None

    @model_validator(mode="after")
    def supplied_patch(self):
        if not self.supplied_fields():
            raise ValueError("At least one editable asset field is required")
        if {"purchase_date", "installation_date"} <= self.model_fields_set:
            v.date_order(self.purchase_date, self.installation_date)
        return self


def merged_asset_fields(saved: dict, patch: AssetPatchRequest) -> dict:
    """Pure merge validation for use after loading saved state in the transaction."""
    fields = {name: saved[name] for name in ("asset_name", "purchase_date", "installation_date", "useful_life_months")}
    fields.update(patch.supplied_fields())
    try:
        purchase, installation = v.date_order(fields["purchase_date"], fields["installation_date"])
        return {**fields, "asset_name": v.text(fields["asset_name"]), "purchase_date": purchase,
                "installation_date": installation, "useful_life_months": v.whole_months(fields["useful_life_months"])}
    except ValueError as error:
        raise CommandError("DOMAIN_RULE", details={"field": "installation_date", "reason": str(error)}) from error


class AssetOverrideRequest(EditRequest):
    operation = "asset.override"
    target_kind = "asset"
    target_alias = "asset"
    cost: Money
    currency: Currency
    reason: Text
    recorder: Text


class AssetResetToSourceRequest(EditRequest):
    operation = "asset.reset_to_source"
    target_kind = "asset"
    target_alias = "asset"
    reason: Text
    recorder: Text


class MaintenanceCreateRequest(MutationRequest):
    operation = "maintenance.create"
    room_id: RoomID
    asset_id: AssetID | None = None
    description: Text
    severity: Severity
    owner_id: OptionalText = None
    target_date: OptionalCalendar = None
    recorder: Text

    @model_validator(mode="after")
    def parent(self):
        if self.asset_id is not None:
            v.source_identity(self.asset_id, "asset", parent=self.room_id)
        return self


class MaintenancePatchRequest(EditRequest):
    operation = "maintenance.edit"
    target_kind = "ticket"
    target_alias = "ticket"
    description: Text = None
    severity: Severity = None
    owner_id: OptionalText = None
    target_date: OptionalCalendar = None
    recorder: Text

    @model_validator(mode="after")
    def supplied_patch(self):
        if not self.supplied_fields().keys() - {"recorder"}:
            raise ValueError("At least one editable maintenance field is required")
        return self


class MaintenanceStartRequest(EditRequest):
    operation = "maintenance.start"
    target_kind = "ticket"
    target_alias = "ticket"
    recorder: Text


class MaintenanceResolveRequest(MaintenanceStartRequest):
    operation = "maintenance.resolve"
    resolution_note: Text


class ImportPreviewRequest(Contract):
    """Multipart bytes are transient inputs, never evidence persisted by this model."""
    file: bytes
    workflow: Workflow


class ImportConfirmRequest(MutationRequest):
    operation = "import.confirm"
    preview_id: UUIDText


class ResetRequest(Contract):
    generation_id: UUIDText
    confirm: Literal[True]

    @model_validator(mode="before")
    @classmethod
    def strict_confirmation(cls, value):
        if isinstance(value, dict) and value.get("confirm") is not True:
            raise ValueError("Reset requires explicit boolean confirm=true")
        return value


class DomainResponse(Contract):
    generation_id: UUIDText


class Owner(Contract):
    owner_id: Text
    display_name: Text


class FXConfiguration(Contract):
    as_of_date: Calendar
    disclaimer: Text
    usd_per_unit: dict[Currency, Money]

    @model_validator(mode="before")
    @classmethod
    def unique_currencies(cls, value):
        if isinstance(value, dict) and isinstance(value.get("usd_per_unit"), dict):
            seen = set()
            for currency in value["usd_per_unit"]:
                key = v.enum_value(currency, v.CURRENCIES)
                if key in seen:
                    raise ValueError("Duplicate normalized FX currency")
                seen.add(key)
        return value

    @model_validator(mode="after")
    def rates(self):
        if self.usd_per_unit.keys() != v.CURRENCIES or any(v.decimal_amount(rate, positive=True) != rate for rate in self.usd_per_unit.values()):
            raise ValueError("Exactly five positive finite canonical FX rates are required")
        if self.usd_per_unit["USD"] != "1":
            raise ValueError("USD rate must equal 1")
        return self


class ConfigResponse(DomainResponse):
    schema_version: Version
    configuration_version: Version
    operational_date: Calendar
    operational_time: Text
    timezone: Literal["Asia/Hong_Kong"]
    fx: FXConfiguration | None
    configured_fx: dict[str, JsonValue] | None
    owners: list[Owner]
    delivered_languages: list[Language]
    diagnostics: list[Diagnostic] = Field(default_factory=list)

    @model_validator(mode="after")
    def operational_context(self):
        instant = datetime.fromisoformat(self.operational_time)
        if ("T" not in self.operational_time or instant.tzinfo is None
                or instant.utcoffset().total_seconds() != 8 * 3600
                or instant.date().isoformat() != self.operational_date):
            raise ValueError("Operational time/date must represent Asia/Hong_Kong with explicit +08:00 offset")
        return self


class Property(Contract):
    property_id: PropertyID
    property_name: Text
    location: Location
    city: Text

    @model_validator(mode="after")
    def region(self):
        v.source_identity(self.property_id, "property", location=self.location)
        return self


class Room(Contract):
    room_id: RoomID
    property_id: PropertyID
    room_number: Text

    @model_validator(mode="after")
    def parent(self):
        v.source_identity(self.room_id, "room", parent=self.property_id)
        return self


class ObservationState(Contract):
    status: Condition = "UNKNOWN"
    observed_on: OptionalCalendar = None
    recorder: OptionalText = None
    note: OptionalText = None

    @model_validator(mode="after")
    def metadata(self):
        v.observation_metadata(self.status, self.observed_on, self.recorder, self.note)
        return self


class Observation(ObservationState):
    room_id: RoomID
    system: System
    version: Version


class AssetSnapshot(Contract):
    asset_name: Text
    purchase_date: Calendar
    installation_date: OptionalCalendar = None
    useful_life_months: Months
    acquisition_cost: Money
    currency: Currency

    @model_validator(mode="after")
    def dates(self):
        v.date_order(self.purchase_date, self.installation_date)
        return self


class FinancialPair(Contract):
    cost: Money
    currency: Currency


class Asset(Contract):
    asset_id: AssetID
    room_id: RoomID
    facility_type: System
    asset_name: Text
    purchase_date: Calendar
    installation_date: OptionalCalendar
    useful_life_months: Months
    source_cost: Money
    source_currency: Currency
    override_cost: Money | None
    override_currency: Currency | None
    effective_cost: Money
    effective_currency: Currency
    applied_invoice_date: OptionalCalendar
    version: Version

    @model_validator(mode="after")
    def relationships(self):
        v.source_identity(self.asset_id, "asset", parent=self.room_id)
        v.date_order(self.purchase_date, self.installation_date)
        if (self.override_cost is None) != (self.override_currency is None):
            raise ValueError("Override cost and currency must be paired")
        pair = (self.source_cost, self.source_currency) if self.override_cost is None else (self.override_cost, self.override_currency)
        if (self.effective_cost, self.effective_currency) != pair:
            raise ValueError("Effective financial values must match override or source")
        return self


class Ticket(Contract):
    ticket_id: UUIDText
    room_id: RoomID
    asset_id: AssetID | None
    description: Text
    severity: Severity
    status: TicketStatus
    owner_id: Text | None
    target_date: OptionalCalendar
    opened_at: Instant
    updated_at: Instant
    resolved_at: Instant | None
    resolution_note: OptionalText
    version: Version

    @model_validator(mode="after")
    def relationships(self):
        if self.asset_id is not None:
            v.source_identity(self.asset_id, "asset", parent=self.room_id)
        if self.status != "OPEN" and self.owner_id is None:
            raise ValueError("In-progress/resolved tickets require an owner")
        if self.status == "RESOLVED" and (self.resolution_note is None or self.resolved_at is None):
            raise ValueError("Resolved tickets require a note and resolution instant")
        if self.status != "RESOLVED" and (self.resolution_note is not None or self.resolved_at is not None):
            raise ValueError("Unresolved tickets cannot contain resolution metadata")
        return self


class TicketSummary(Contract):
    ticket: Ticket
    owner_label: Text
    target_date_label: Text
    overdue: bool


class EntityCounts(Contract):
    properties: Count
    rooms: Count
    assets: Count
    unresolved_tickets: Count
    critical_unresolved_tickets: Count
    observations: dict[System, dict[Condition, Count]]


class RoomSummary(Contract):
    property: Property
    room: Room
    observations: list[Observation]
    unresolved_ticket_count: Count


class DisplayedAssetFinance(Contract):
    currency: Currency
    acquisition_cost: FormattedMoney
    accumulated_depreciation: FormattedMoney
    remaining_book_value: FormattedMoney


class AssetFinance(Contract):
    asset_id: AssetID
    service_anchor: Calendar
    purchase_fallback: bool
    completed_months: Count
    effective_cost: Money
    effective_currency: Currency
    currency: Currency
    acquisition_cost: Money
    accumulated_depreciation: Money
    remaining_book_value: Money
    replacement_date: Calendar
    replacement_category: Literal["OVERDUE", "DUE_TODAY", "DUE_SOON", "LATER"]
    critical_unresolved_asset: bool
    displayed: DisplayedAssetFinance


class DisplayedCurrencyTotals(Contract):
    acquisition_cost: FormattedMoney
    accumulated_depreciation: FormattedMoney
    remaining_book_value: FormattedMoney
    overdue_spending: FormattedMoney
    due_today_spending: FormattedMoney
    future_spending: FormattedMoney


class CurrencyTotals(Contract):
    currency: Currency
    acquisition_cost: Money
    accumulated_depreciation: Money
    remaining_book_value: Money
    overdue_spending: Money
    due_today_spending: Money
    future_spending: Money
    displayed: DisplayedCurrencyTotals


class FinanceResults(Contract):
    financial_date: Calendar
    currency_mode: CurrencyMode
    assets: list[AssetFinance]
    totals: list[CurrencyTotals]


class FinanceEnvelope(Contract):
    status: Literal["VALID", "INVALID_CONFIGURATION"]
    diagnostics: list[Diagnostic]
    results: FinanceResults | None

    @model_validator(mode="after")
    def valid_result(self):
        if self.status == "INVALID_CONFIGURATION" and (self.results is not None or not self.diagnostics):
            raise ValueError("Invalid finance requires diagnostics and null results")
        if self.status == "VALID" and (self.results is None or self.diagnostics):
            raise ValueError("Valid finance requires complete results and no configuration blockers")
        return self


class OverviewResponse(DomainResponse):
    scope: ScopeRequest
    counts: EntityCounts
    rooms: list[RoomSummary]
    unresolved_tickets: list[TicketSummary]
    finance: FinanceEnvelope
    diagnostics: list[Diagnostic] = Field(default_factory=list)


class RoomResponse(DomainResponse):
    property: Property
    room: Room
    observations: list[Observation]
    assets: list[Asset]
    unresolved_tickets: list[TicketSummary]
    resolved_tickets: list[TicketSummary]
    finance: FinanceEnvelope

    @model_validator(mode="after")
    def complete_room(self):
        if self.room.property_id != self.property.property_id:
            raise ValueError("Room property context must match")
        for records, field in ((self.observations, "system"), (self.assets, "facility_type")):
            if len(records) != 3 or {getattr(item, field) for item in records} != v.SYSTEMS:
                raise ValueError("Room responses require exactly three distinct systems/assets")
            if any(item.room_id != self.room.room_id for item in records):
                raise ValueError("Room records must belong to the selected room")
        for tickets, resolved in ((self.unresolved_tickets, False), (self.resolved_tickets, True)):
            if any(item.ticket.room_id != self.room.room_id or (item.ticket.status == "RESOLVED") != resolved for item in tickets):
                raise ValueError("Ticket room/status group must match")
        return self


class ObservationResponse(DomainResponse):
    observation: Observation


class AssetResponse(DomainResponse):
    asset: Asset


class AssetHistoryResponse(AssetResponse):
    history_id: UUIDText


class MaintenanceResponse(DomainResponse):
    ticket: Ticket
    history_id: UUIDText


class MaintenanceListResponse(DomainResponse):
    scope: ScopeRequest
    view: Literal["UNRESOLVED", "RESOLVED"]
    tickets: list[TicketSummary]


class MaintenanceHistory(Contract):
    event_id: UUIDText
    ticket_id: UUIDText
    action: Literal["CREATE", "EDIT", "START", "RESOLVE"]
    before: Ticket | None
    after: Ticket
    recorder: Text
    happened_at: Instant
    resulting_version: Version


class MaintenanceDetailResponse(DomainResponse):
    ticket: Ticket
    history: list[MaintenanceHistory]


class Provenance(Contract):
    upload_id: UUIDText
    filename: Text
    sheet: Text
    row: Annotated[int, Field(ge=2)]
    imported_at: Instant


class InvoiceReference(Contract):
    invoice_id: Text
    line_id: Text


class InvoiceItem(InvoiceReference):
    asset_id: AssetID
    room_id: RoomID
    facility_type: System
    snapshot: AssetSnapshot
    invoice_date: Calendar
    supplier_name: OptionalText
    provenance: Provenance


class AssetValueState(Contract):
    asset_name: Text
    purchase_date: Calendar
    installation_date: OptionalCalendar
    useful_life_months: Months
    source: FinancialPair
    override: FinancialPair | None
    effective: FinancialPair
    applied_invoice_date: OptionalCalendar

    @model_validator(mode="after")
    def values(self):
        v.date_order(self.purchase_date, self.installation_date)
        if self.effective != (self.override or self.source):
            raise ValueError("Effective pair must match override or source")
        return self


class InvoiceUpdate(Contract):
    event_id: UUIDText
    asset_id: AssetID
    invoice_date: Calendar
    before: AssetValueState
    after: AssetValueState
    before_refs: list[InvoiceReference]
    after_refs: list[InvoiceReference]
    upload_id: UUIDText
    happened_at: Instant


class OverrideHistory(Contract):
    event_id: UUIDText
    asset_id: AssetID
    action: Literal["SET_OVERRIDE", "RESET_TO_SOURCE", "CLEAR_ON_INVOICE"]
    before: AssetValueState
    after: AssetValueState
    reason: Text
    recorder: Text
    happened_at: Instant
    invoice_update_id: UUIDText | None


class AssetEvidenceResponse(DomainResponse):
    asset: Asset
    baseline: AssetSnapshot
    baseline_coordinates: list[Provenance]
    invoice_items: list[InvoiceItem]
    applied_updates: list[InvoiceUpdate]
    override_history: list[OverrideHistory]
    applied_invoice_refs: list[InvoiceReference]


class ImportCounts(Contract):
    properties_inserted: Count
    rooms_inserted: Count
    assets_inserted: Count
    assets_updated: Count
    invoice_items_inserted: Count
    historical_only_items: Count
    skips: Count
    warnings: Count
    blockers: Count


class FieldChange(Contract):
    field: Text
    before: JsonValue
    after: JsonValue


class ProposedAssetChange(Contract):
    asset_id: AssetID
    changes: list[FieldChange]
    clears_override: bool


class ImportPreviewResponse(DomainResponse):
    preview_id: UUIDText
    workflow: Workflow
    counts: ImportCounts
    diagnostics: list[Diagnostic]
    asset_changes: list[ProposedAssetChange]
    expires_at: Instant


class ImportConfirmResponse(DomainResponse):
    counts: ImportCounts
    upload_id: UUIDText | None


class EmptyStoreCounts(Contract):
    properties: Annotated[int, Field(ge=0, le=0)]
    rooms: Annotated[int, Field(ge=0, le=0)]
    assets: Annotated[int, Field(ge=0, le=0)]
    observations: Annotated[int, Field(ge=0, le=0)]
    tickets: Annotated[int, Field(ge=0, le=0)]
    uploads: Annotated[int, Field(ge=0, le=0)]
    invoice_items: Annotated[int, Field(ge=0, le=0)]
    histories: Annotated[int, Field(ge=0, le=0)]
    receipts: Annotated[int, Field(ge=0, le=0)]


class ResetResponse(DomainResponse):
    counts: EmptyStoreCounts


@dataclass(frozen=True)
class EndpointContract:
    request: type[BaseModel]
    response: type[BaseModel]


# Contract inventory only. Actual FastAPI route registration is owned by later jobs.
ENDPOINT_CONTRACTS = {
    ("GET", "/api/config"): EndpointContract(ConfigRequest, ConfigResponse),
    ("GET", "/api/overview"): EndpointContract(OverviewRequest, OverviewResponse),
    ("GET", "/api/rooms/{room_id}"): EndpointContract(RoomRequest, RoomResponse),
    ("GET", "/api/assets/{asset_id}/evidence"): EndpointContract(AssetEvidenceRequest, AssetEvidenceResponse),
    ("PUT", "/api/rooms/{room_id}/observations/{system}"): EndpointContract(ObservationSaveRequest, ObservationResponse),
    ("POST", "/api/rooms/{room_id}/observations/{system}/clear"): EndpointContract(ObservationClearRequest, ObservationResponse),
    ("PATCH", "/api/assets/{asset_id}"): EndpointContract(AssetPatchRequest, AssetResponse),
    ("POST", "/api/assets/{asset_id}/override"): EndpointContract(AssetOverrideRequest, AssetHistoryResponse),
    ("POST", "/api/assets/{asset_id}/reset-to-source"): EndpointContract(AssetResetToSourceRequest, AssetHistoryResponse),
    ("GET", "/api/maintenance"): EndpointContract(MaintenanceListRequest, MaintenanceListResponse),
    ("GET", "/api/maintenance/{ticket_id}"): EndpointContract(MaintenanceDetailRequest, MaintenanceDetailResponse),
    ("POST", "/api/maintenance"): EndpointContract(MaintenanceCreateRequest, MaintenanceResponse),
    ("PATCH", "/api/maintenance/{ticket_id}"): EndpointContract(MaintenancePatchRequest, MaintenanceResponse),
    ("POST", "/api/maintenance/{ticket_id}/start"): EndpointContract(MaintenanceStartRequest, MaintenanceResponse),
    ("POST", "/api/maintenance/{ticket_id}/resolve"): EndpointContract(MaintenanceResolveRequest, MaintenanceResponse),
    ("POST", "/api/imports/preview"): EndpointContract(ImportPreviewRequest, ImportPreviewResponse),
    ("POST", "/api/imports/confirm"): EndpointContract(ImportConfirmRequest, ImportConfirmResponse),
    ("POST", "/api/reset"): EndpointContract(ResetRequest, ResetResponse),
}


def execute_validated_command(store: Store, request: MutationRequest, *, load_records: LoadRecords,
                              mutate: Mutate, target_id: str | None = None,
                              system: str | None = None) -> dict:
    """Validate the saved response before PR-03 commits effects and its receipt.

    Only later feature services supply mutation/prerequisite callbacks. Response
    replay stays inside PR-03 and does not invoke callbacks or rebuild timestamps.
    """
    boundary = next((entry for entry in ENDPOINT_CONTRACTS.values() if entry.request is type(request)), None)
    if boundary is None:
        raise CommandError("INVALID_INPUT")
    command = request.to_command(target_id=target_id, system=system)

    def checked_mutation(connection, fields, records):
        raw = mutate(connection, fields, records)
        if type(raw) is not dict:
            raise SaveFailed()
        try:
            saved = boundary.response.model_validate({"generation_id": command.generation_id, **raw})
            if saved.generation_id != command.generation_id:
                raise ValueError("Mutation response changed the store generation")
            return saved.model_dump(mode="json")
        except (ValueError, ValidationError) as error:
            raise SaveFailed() from error

    return execute_command(store, command, load_records=load_records, mutate=checked_mutation)

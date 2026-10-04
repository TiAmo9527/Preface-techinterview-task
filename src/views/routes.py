"""Thin local runtime endpoints. Services own all store/config/reset behavior."""

import json
import logging
from pathlib import Path

from fastapi import Depends, File, Form, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from src.db import StoreError
from src.services.contracts import ConfigResponse, ResetRequest, ResetResponse
from src.services.contracts import ImportConfirmRequest, ImportConfirmResponse, ImportPreviewResponse, Workflow
from src.services.previews import PreviewRegistry, confirm_import, preview_import
from src.services.errors import CommandError
from src.services.runtime import read_configuration, reset_store, shell_snapshot

ASSETS = Path(__file__).parent / "static"
logger = logging.getLogger(__name__)


async def import_form_boundary(request: Request):
    form = await request.form()
    if set(form) != {"file", "workflow"} or any(len(form.getlist(key)) != 1 for key in form):
        raise CommandError("INVALID_INPUT", details={"reason": "Supply exactly one file and one workflow"})


def register_runtime_routes(application):
    registry = PreviewRegistry(clock=application.state.clock)
    application.state.preview_registry = registry
    application.state.evict_previews = registry.evict_generation

    @application.middleware("http")
    async def cache_policy(request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/api/") or request.url.path == "/":
            response.headers["Cache-Control"] = "no-store"
        return response

    @application.exception_handler(CommandError)
    async def command_error(request, error):
        return JSONResponse(error.as_dict(), status_code=error.status_code)

    @application.exception_handler(StoreError)
    async def store_error(request, error):
        code = error.code if error.code in ("STORE_BUSY", "SAVE_FAILED") else "SAVE_FAILED"
        return JSONResponse(CommandError(code).as_dict(), status_code=503 if code == "STORE_BUSY" else 500)

    @application.exception_handler(RequestValidationError)
    async def invalid_request(request, error):
        # Do not echo arbitrary inputs or unserializable Pydantic exception context.
        details = {"fields": [{"field": ".".join(map(str, item["loc"])), "reason": item["msg"]}
                              for item in error.errors()]}
        return JSONResponse(CommandError("INVALID_INPUT", details=details).as_dict(), status_code=422)

    @application.get("/", response_class=HTMLResponse)
    def shell(request: Request):
        bootstrap = json.dumps(shell_snapshot(request.app.state.store)).replace("<", "\\u003c")
        return (ASSETS / "index.html").read_text(encoding="utf-8").replace("__BOOTSTRAP__", bootstrap)

    @application.get("/api/config", response_model=ConfigResponse)
    def configuration(request: Request):
        state = request.app.state
        return read_configuration(state.store, config=state.local_config, clock=state.clock)

    @application.post("/api/reset", response_model=ResetResponse)
    def reset(payload: ResetRequest, request: Request):
        state = request.app.state
        return reset_store(state.store, payload, evict_previews=state.evict_previews)

    @application.post("/api/imports/preview", response_model=ImportPreviewResponse,
                      dependencies=[Depends(import_form_boundary)])
    def import_preview(request: Request, file: UploadFile = File(...), workflow: Workflow = Form(...)):
        state = request.app.state
        try:
            data = file.file.read()
        finally:
            file.file.close()
        return preview_import(state.store, state.preview_registry, data,
                              filename=file.filename or "upload.xlsx", workflow=workflow)

    @application.post("/api/imports/confirm", response_model=ImportConfirmResponse)
    def import_confirm(payload: ImportConfirmRequest, request: Request):
        state = request.app.state
        return confirm_import(state.store, state.preview_registry, payload, clock=state.clock)

    application.mount("/static", StaticFiles(directory=ASSETS), name="static")

"""One-worker localhost launcher and injectable application seam."""

import argparse
from contextlib import asynccontextmanager
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Callable, Mapping

from fastapi import FastAPI
import uvicorn

from src.db import Store, StoreError
from src.db.store import DEFAULT_STORE_PATH
from src.views.routes import register_runtime_routes


def create_app(
    *, store_path: Path | None = None,
    clock: Callable[[], datetime] | None = None,
    config: Mapping | None = None,
) -> FastAPI:
    """Inject isolated test state without exposing a production database selector."""
    store = Store(DEFAULT_STORE_PATH if store_path is None else store_path)

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        store.initialize()
        yield

    application = FastAPI(
        title="Hotel asset-management prototype", lifespan=lifespan,
        docs_url=None, redoc_url=None, openapi_url=None,
    )
    application.state.store = store
    application.state.clock = clock or (lambda: datetime.now(timezone.utc))
    application.state.local_config = deepcopy(dict(config)) if config is not None else None
    application.state.evict_previews = None
    register_runtime_routes(application)
    return application


app = create_app()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve the local hotel asset-management prototype.")
    parser.add_argument("--init-db", action="store_true", help="Initialize or validate the supported store without clearing it.")
    arguments = parser.parse_args(argv)
    try:
        metadata = app.state.store.initialize()
    except StoreError as error:
        print(f"Initialization blocked: {error}", file=sys.stderr)
        return 1
    print(f"Store ready: {app.state.store.path} (schema {metadata.schema_version}, generation {metadata.generation_id})")
    if not arguments.init_db:
        uvicorn.run(app, host="127.0.0.1", port=8000, workers=1, reload=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

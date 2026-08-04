"""Read-only REST API over the local FoxESS device (Phase 8).

Built on the async core. Endpoints are versioned under ``/api/v1``. The app is
created via :func:`create_app`, which takes a dependency returning an
:class:`~foxess.aio.AsyncFoxESS` — this makes it trivial to inject a mock device
in tests and to configure the host from the environment in production.

Requires the optional ``[api]`` extra (``fastapi``). Import is lazy so the core
SDK has no hard FastAPI dependency.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any

from .aio import ADDR_GATEWAY, ADDR_INVERTER, AsyncFoxESS
from .errors import (
    FoxDeviceError,
    FoxModelNotFound,
    FoxProtocolError,
    FoxTransportError,
)

FoxProvider = Callable[[], Awaitable[AsyncFoxESS]]

API_PREFIX = "/api/v1"


def _fox_host() -> str:
    """Device IP from ``FOX_HOST``. Required — no hardcoded fallback."""
    host = os.environ.get("FOX_HOST", "").strip()
    if not host:
        raise RuntimeError(
            "FOX_HOST is not set. Set it to your FoxESS device IP "
            "(e.g. in docker/.env or export FOX_HOST=...)."
        )
    return host


def _default_provider() -> FoxProvider:
    host = _fox_host()

    async def provide() -> AsyncFoxESS:
        return AsyncFoxESS(host)

    return provide


def create_app(provider: FoxProvider | None = None) -> Any:
    """Create the FastAPI application. ``provider`` returns an AsyncFoxESS."""
    from fastapi import Depends, FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware

    get_provider = provider or _default_provider()
    app = FastAPI(
        title="foxess-local",
        version="0.4.0",
        description="Read-only local access to FoxESS Smart WiLAN devices.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.environ.get("FOX_CORS_ORIGINS", "*").split(","),
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    async def get_fox() -> AsyncIterator[AsyncFoxESS]:
        fox = await get_provider()
        try:
            yield fox
        finally:
            await fox.aclose()

    Fox = Depends(get_fox)

    @app.exception_handler(FoxModelNotFound)
    async def _not_found(_req: Any, exc: FoxModelNotFound) -> Any:
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=404, content={"error": str(exc)})

    @app.exception_handler(FoxTransportError)
    async def _unreachable(_req: Any, exc: FoxTransportError) -> Any:
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=503, content={"error": str(exc)})

    @app.exception_handler(FoxDeviceError)
    async def _device_err(_req: Any, exc: FoxDeviceError) -> Any:
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=502, content={"error": str(exc)})

    @app.exception_handler(FoxProtocolError)
    async def _proto_err(_req: Any, exc: FoxProtocolError) -> Any:
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=502, content={"error": str(exc)})

    # -- measurement endpoints --------------------------------------------------

    @app.get(f"{API_PREFIX}/system")
    async def system(fox: AsyncFoxESS = Fox) -> Any:
        return await fox.system()

    @app.get(f"{API_PREFIX}/battery")
    async def battery(fox: AsyncFoxESS = Fox) -> Any:
        return await fox.battery()

    @app.get(f"{API_PREFIX}/grid")
    async def grid(fox: AsyncFoxESS = Fox) -> Any:
        return await fox.grid()

    @app.get(f"{API_PREFIX}/solar")
    async def solar(fox: AsyncFoxESS = Fox) -> Any:
        return await fox.solar()

    @app.get(f"{API_PREFIX}/load")
    async def load(fox: AsyncFoxESS = Fox) -> Any:
        return await fox.load()

    @app.get(f"{API_PREFIX}/inverter")
    async def inverter(fox: AsyncFoxESS = Fox) -> Any:
        return await fox.inverter()

    # -- model / raw access -----------------------------------------------------

    @app.get(f"{API_PREFIX}/models")
    async def models(fox: AsyncFoxESS = Fox) -> Any:
        return [
            {
                "id": m.id,
                "name": m.name,
                "address": m.modbus_address,
                "fields": len(m.fields),
                "report": m.report,
            }
            for m in fox.registry
        ]

    @app.get(f"{API_PREFIX}/models/{{model_id}}")
    async def model_def(model_id: int, fox: AsyncFoxESS = Fox) -> Any:
        from .errors import FoxUnknownModel

        try:
            m = fox.registry.get(model_id)
        except FoxUnknownModel:
            raise HTTPException(status_code=404, detail=f"unknown model {model_id}") from None
        return {
            "id": m.id,
            "name": m.name,
            "address": m.modbus_address,
            "report": m.report,
            "fields": [
                {
                    "name": f.name,
                    "label": f.label,
                    "type": f.type,
                    "unit": f.unit,
                    "writable": f.writable,
                }
                for f in m.fields
            ],
        }

    @app.get(f"{API_PREFIX}/raw/{{addr}}/{{model_id}}")
    async def raw(addr: int, model_id: int, fox: AsyncFoxESS = Fox) -> Any:
        model = await fox.read_model(addr, model_id)
        return {
            "addr": model.addr,
            "id": model.id,
            "name": model.name,
            "fields": [
                {
                    "name": f.name,
                    "label": f.label,
                    "value": f.value,
                    "unit": f.unit,
                    "address": f.address,
                }
                for f in model.fields
            ],
        }

    # -- health / readiness -----------------------------------------------------

    @app.get("/metrics")
    async def metrics() -> Any:
        from fastapi.responses import Response
        from starlette.concurrency import run_in_threadpool

        try:
            from .client import FoxESS
            from .prometheus import render
        except ImportError:
            raise HTTPException(status_code=501, detail="prometheus extra not installed") from None

        host = _fox_host()

        def _render() -> bytes:
            with FoxESS(host) as fox:
                return render(fox)

        body = await run_in_threadpool(_render)
        return Response(content=body, media_type="text/plain; version=0.0.4")

    @app.get(f"{API_PREFIX}/health")
    async def health() -> Any:
        return {"status": "ok"}

    @app.get(f"{API_PREFIX}/ready")
    async def ready(fox: AsyncFoxESS = Fox) -> Any:
        from fastapi.responses import JSONResponse

        try:
            await fox.read_raw(ADDR_INVERTER, 1)
        except (FoxTransportError, FoxDeviceError, FoxProtocolError) as exc:
            return JSONResponse(status_code=503, content={"status": "not ready", "error": str(exc)})
        return {"status": "ready", "gateway": ADDR_GATEWAY, "inverter": ADDR_INVERTER}

    from .ws import register as _register_ws

    _register_ws(app, get_provider)

    return app

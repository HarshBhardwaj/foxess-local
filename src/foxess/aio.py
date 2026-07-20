"""Async core: ``AsyncTransport`` and ``AsyncFoxESS``.

Mirrors the synchronous API using ``httpx.AsyncClient``. The frame, registry,
decoder, and measurement layers are pure and shared unchanged.
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

from .errors import (
    ERRNO_ID_NOT_FOUND,
    ERRNO_SUCCESS,
    FoxDeviceError,
    FoxModelNotFound,
    FoxProtocolError,
    FoxTimeoutError,
    FoxTransportError,
)
from .frame import reassemble_hex
from .measurements import (
    BatteryInfo,
    GridMeasurement,
    InverterStatus,
    LoadInfo,
    SolarInfo,
    SystemInfo,
)
from .models import DecodedModel
from .registry import ModelRegistry, default_registry
from .transport import (
    DEFAULT_BACKOFF,
    DEFAULT_RETRIES,
    DEFAULT_TIMEOUT,
    DataResponse,
)

ADDR_GATEWAY = 1
ADDR_INVERTER = 2


class AsyncTransport:
    """Async transport over a persistent HTTP connection."""

    def __init__(
        self,
        host: str,
        *,
        username: str = "admin",
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        backoff: float = DEFAULT_BACKOFF,
        scheme: str = "http",
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.host = host
        self.base_url = f"{scheme}://{host}"
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers={"Accept": "application/json, text/plain, */*"},
            cookies={"fox_energy_username": username},
        )

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> AsyncTransport:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()

    async def read_data(self, addr: int, model_id: int) -> DataResponse:
        obj = await self._get_json("/api/v1/sunspec/data", {"addr": addr, "id": model_id})
        errno = int(obj.get("errno", -1))
        if errno != ERRNO_SUCCESS:
            errmsg = str(obj.get("errmsg", ""))
            if errno == ERRNO_ID_NOT_FOUND:
                raise FoxModelNotFound(errno, errmsg, addr, model_id)
            raise FoxDeviceError(errno, errmsg, addr, model_id)
        data = obj.get("data")
        if not isinstance(data, dict) or "tbl" not in data:
            raise FoxProtocolError(f"missing data.tbl in response for ({addr},{model_id})")
        return DataResponse(
            addr=addr,
            model_id=int(data.get("id", model_id)),
            reg_addr=int(data.get("reg_addr", -1)),
            tbl_hex=str(data["tbl"]),
            mstype=int(obj.get("mstype", -1)),
        )

    async def _get_json(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        last_exc: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                resp = await self._client.get(path, params=params)
                resp.raise_for_status()
                parsed: dict[str, Any] = resp.json()
                return parsed
            except httpx.TimeoutException:
                last_exc = FoxTimeoutError(f"timeout on {path} {params}")
            except httpx.HTTPError as exc:
                last_exc = FoxTransportError(f"HTTP error on {path} {params}: {exc}")
            except ValueError as exc:
                last_exc = FoxProtocolError(f"non-JSON response on {path}: {exc}")
                break
            if attempt < self.retries:
                await asyncio.sleep(self.backoff * (2**attempt))
        assert last_exc is not None
        raise last_exc


class AsyncFoxESS:
    """Async facade over transport + frame + decoder + measurement views."""

    def __init__(
        self,
        host: str,
        *,
        username: str = "admin",
        timeout: float = DEFAULT_TIMEOUT,
        registry: ModelRegistry | None = None,
        transport: AsyncTransport | None = None,
    ) -> None:
        self._registry = registry or default_registry()
        self._transport = transport or AsyncTransport(host, username=username, timeout=timeout)

    async def aclose(self) -> None:
        await self._transport.aclose()

    async def __aenter__(self) -> AsyncFoxESS:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()

    @property
    def registry(self) -> ModelRegistry:
        return self._registry

    async def read_raw(self, addr: int, model_id: int) -> DataResponse:
        return await self._transport.read_data(addr, model_id)

    async def read_model(
        self, addr: int, model_id: int, *, validate_crc: bool = True
    ) -> DecodedModel:
        from .decoder import decode_payload

        resp = await self._transport.read_data(addr, model_id)
        frame = reassemble_hex(resp.tbl_hex, validate_crc=validate_crc)
        return decode_payload(frame.payload, self._registry.get(model_id), addr=addr)

    async def read_models(
        self, addr: int, ids: tuple[int, ...], *, validate_crc: bool = True
    ) -> dict[int, DecodedModel]:
        """Read several models concurrently, skipping any the device lacks."""

        async def one(mid: int) -> tuple[int, DecodedModel | None]:
            try:
                return mid, await self.read_model(addr, mid, validate_crc=validate_crc)
            except FoxModelNotFound:
                return mid, None

        results = await asyncio.gather(*(one(mid) for mid in ids))
        return {mid: model for mid, model in results if model is not None}

    async def scan(self, addr: int, *, ids: tuple[int, ...] | None = None) -> dict[int, bool]:
        candidate = ids or self._registry.ids

        async def probe(mid: int) -> tuple[int, bool]:
            try:
                await self._transport.read_data(addr, mid)
                return mid, True
            except FoxModelNotFound:
                return mid, False

        results = await asyncio.gather(*(probe(mid) for mid in candidate))
        return dict(results)

    async def system(self) -> SystemInfo:
        return SystemInfo.from_models(
            await self.read_models(ADDR_INVERTER, SystemInfo.REQUIRED_MODELS)
        )

    async def battery(self) -> BatteryInfo:
        return BatteryInfo.from_models(
            await self.read_models(ADDR_INVERTER, BatteryInfo.REQUIRED_MODELS)
        )

    async def grid(self) -> GridMeasurement:
        return GridMeasurement.from_models(
            await self.read_models(ADDR_INVERTER, GridMeasurement.REQUIRED_MODELS)
        )

    async def solar(self) -> SolarInfo:
        return SolarInfo.from_models(
            await self.read_models(ADDR_INVERTER, SolarInfo.REQUIRED_MODELS)
        )

    async def load(self) -> LoadInfo:
        return LoadInfo.from_models(
            await self.read_models(ADDR_INVERTER, LoadInfo.REQUIRED_MODELS)
        )

    async def inverter(self) -> InverterStatus:
        return InverterStatus.from_models(
            await self.read_models(ADDR_INVERTER, InverterStatus.REQUIRED_MODELS)
        )

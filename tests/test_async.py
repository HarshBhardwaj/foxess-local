"""Async core tests (no event-loop plugin needed: drive via asyncio.run)."""

from __future__ import annotations

import asyncio

import httpx

from foxess.aio import AsyncFoxESS, AsyncTransport
from foxess.errors import FoxModelNotFound


def _transport(sweep) -> AsyncTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        addr = int(request.url.params["addr"])
        mid = int(request.url.params["id"])
        rec = sweep[(addr, mid)]
        if rec.errno != 0:
            return httpx.Response(200, json={"errno": rec.errno, "errmsg": rec.errmsg})
        return httpx.Response(
            200,
            json={
                "errno": 0,
                "errmsg": "success",
                "mstype": 2,
                "data": {"id": mid, "reg_addr": rec.reg_addr, "tbl": rec.tbl_hex},
            },
        )

    client = httpx.AsyncClient(base_url="http://mock", transport=httpx.MockTransport(handler))
    return AsyncTransport("mock", client=client)


def test_async_read_and_decode(sweep) -> None:
    async def run() -> None:
        async with AsyncFoxESS("mock", transport=_transport(sweep)) as fox:
            common = await fox.read_model(2, 1)
            assert common.get("Md") == "AIO-H1-11.4-US"
            battery = await fox.battery()
            assert battery.soc_percent == 51.0
            assert battery.charging is True

    asyncio.run(run())


def test_async_scan_concurrent(sweep) -> None:
    async def run() -> None:
        async with AsyncFoxESS("mock", transport=_transport(sweep)) as fox:
            result = await fox.scan(1, ids=(1, 701, 702, 713))
            assert result == {1: True, 701: True, 702: False, 713: True}

    asyncio.run(run())


def test_async_model_not_found(sweep) -> None:
    async def run() -> None:
        async with AsyncFoxESS("mock", transport=_transport(sweep)) as fox:
            try:
                await fox.read_model(1, 702)
            except FoxModelNotFound:
                return
            raise AssertionError("expected FoxModelNotFound")

    asyncio.run(run())

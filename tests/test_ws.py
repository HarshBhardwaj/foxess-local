"""WebSocket streaming tests (deterministic fake socket + TestClient smoke)."""

from __future__ import annotations

import asyncio

import httpx
import pytest

from foxess.aio import AsyncFoxESS, AsyncTransport
from foxess.ws import PROTOCOL_VERSION, _Subscription, stream


def _async_fox(sweep) -> AsyncFoxESS:
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
    return AsyncFoxESS("mock", transport=AsyncTransport("mock", client=client))


class _FakeWS:
    def __init__(self) -> None:
        self.sent: list[dict] = []

    async def send_json(self, message: dict) -> None:
        self.sent.append(message)

    async def receive_json(self) -> dict:
        await asyncio.Event().wait()  # never returns; no client control messages
        raise AssertionError("unreachable")


def test_subscription_apply() -> None:
    sub = _Subscription()
    sub.apply({"action": "set", "groups": ["solar", "battery"]})
    assert sub.groups == {"solar", "battery"}
    sub.apply({"action": "unsubscribe", "groups": ["battery"]})
    assert sub.groups == {"solar"}
    sub.apply({"action": "subscribe", "groups": ["grid", "bogus"]})
    assert sub.groups == {"solar", "grid"}


def test_stream_emits_versioned_envelopes(sweep) -> None:
    async def run() -> None:
        ws = _FakeWS()
        fox = _async_fox(sweep)
        await stream(ws, fox, interval=0.0, clock=lambda: 1.0, max_cycles=1)
        await fox.aclose()

        assert ws.sent[0]["type"] == "hello"
        assert all(m["v"] == PROTOCOL_VERSION for m in ws.sent)
        assert all("ts" in m for m in ws.sent)
        by_group = {(m["group"], m["type"]): m for m in ws.sent}
        assert by_group[("battery", "update")]["data"]["soc_percent"] == 51.0
        assert by_group[("solar", "update")]["data"]["power_w"] == 1795
        assert any(m["type"] == "heartbeat" for m in ws.sent)

    asyncio.run(run())


def test_ws_endpoint_hello(sweep) -> None:
    fastapi = pytest.importorskip("fastapi")  # noqa: F841
    from fastapi.testclient import TestClient

    from foxess.api import create_app

    async def provider() -> AsyncFoxESS:
        return _async_fox(sweep)

    client = TestClient(create_app(provider))
    with client.websocket_connect("/api/v1/ws?interval=0.01") as ws:
        hello = ws.receive_json()
        assert hello["type"] == "hello"
        assert hello["v"] == PROTOCOL_VERSION
        # drain to the first heartbeat, collecting update groups
        groups = set()
        for _ in range(30):
            msg = ws.receive_json()
            if msg["type"] == "update":
                groups.add(msg["group"])
            if msg["type"] == "heartbeat":
                break
        assert "battery" in groups

"""REST API tests using FastAPI TestClient against a mock device."""

from __future__ import annotations

import httpx
import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from foxess.aio import AsyncFoxESS, AsyncTransport  # noqa: E402
from foxess.api import create_app  # noqa: E402


@pytest.fixture
def client(sweep) -> TestClient:
    def handler(request: httpx.Request) -> httpx.Response:
        addr = int(request.url.params["addr"])
        mid = int(request.url.params["id"])
        rec = sweep[(addr, mid)]
        if rec.errno != 0:
            return httpx.Response(200, json={"errno": rec.errno, "errmsg": rec.errmsg})
        return httpx.Response(
            200,
            json={
                "errno": 0, "errmsg": "success", "mstype": 2,
                "data": {"id": mid, "reg_addr": rec.reg_addr, "tbl": rec.tbl_hex},
            },
        )

    async def provider() -> AsyncFoxESS:
        c = httpx.AsyncClient(base_url="http://mock", transport=httpx.MockTransport(handler))
        return AsyncFoxESS("mock", transport=AsyncTransport("mock", client=c))

    return TestClient(create_app(provider))


def test_health(client: TestClient) -> None:
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ready(client: TestClient) -> None:
    r = client.get("/api/v1/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"


def test_battery_endpoint(client: TestClient) -> None:
    r = client.get("/api/v1/battery")
    assert r.status_code == 200
    body = r.json()
    assert body["soc_percent"] == 51.0
    assert body["voltage_v"] == 180.3


def test_system_endpoint(client: TestClient) -> None:
    r = client.get("/api/v1/system")
    assert r.json()["model"] == "AIO-H1-11.4-US"


def test_models_list(client: TestClient) -> None:
    r = client.get("/api/v1/models")
    assert r.status_code == 200
    assert len(r.json()) == 54


def test_model_def(client: TestClient) -> None:
    r = client.get("/api/v1/models/702")
    body = r.json()
    assert body["name"] == "DER Capacity"
    assert any(f["name"] == "WMaxRtg" for f in body["fields"])


def test_raw_decode(client: TestClient) -> None:
    r = client.get("/api/v1/raw/2/702")
    body = r.json()
    wmax = next(f for f in body["fields"] if f["name"] == "WMaxRtg")
    assert wmax["value"] == 11400


def test_unknown_model_404(client: TestClient) -> None:
    r = client.get("/api/v1/models/99999")
    assert r.status_code == 404


def test_model_not_on_device_404(client: TestClient) -> None:
    # gateway (addr=1) does not implement 702
    r = client.get("/api/v1/raw/1/702")
    assert r.status_code == 404

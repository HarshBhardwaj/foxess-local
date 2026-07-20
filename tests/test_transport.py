"""Transport tests using a mock HTTP layer (no hardware required)."""

from __future__ import annotations

import httpx
import pytest

from foxess.client import FoxESS
from foxess.errors import FoxModelNotFound
from foxess.transport import Transport


def _make_transport(sweep) -> Transport:
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

    client = httpx.Client(base_url="http://mock", transport=httpx.MockTransport(handler))
    return Transport("mock", client=client)


def test_read_data_success(sweep) -> None:
    t = _make_transport(sweep)
    resp = t.read_data(2, 1)
    assert resp.model_id == 1
    assert resp.tbl_hex.startswith("0203")


def test_id_not_found_raises(sweep) -> None:
    t = _make_transport(sweep)
    with pytest.raises(FoxModelNotFound):
        t.read_data(1, 702)  # gateway does not implement 702


def test_client_read_model_decodes(sweep) -> None:
    fox = FoxESS("mock", transport=_make_transport(sweep))
    common = fox.read_model(2, 1)
    assert common.get("Md") == "AIO-H1-11.4-US"


def test_client_scan(sweep) -> None:
    fox = FoxESS("mock", transport=_make_transport(sweep))
    result = fox.scan(1, ids=(1, 701, 702, 713))
    assert result == {1: True, 701: True, 702: False, 713: True}

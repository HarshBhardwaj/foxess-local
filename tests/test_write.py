"""Write-path safety tests: gating, dry-run, validation, and a mock write."""

from __future__ import annotations

import httpx
import pytest

from foxess.client import FoxESS
from foxess.errors import (
    FoxWriteNotAllowed,
    FoxWriteNotConfirmed,
    FoxWriteRangeError,
    FoxWritesDisabled,
)
from foxess.transport import Transport


def _transport(sweep, *, capture: list | None = None) -> Transport:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/modbus_rw"):
            import json

            body = json.loads(request.content)
            if capture is not None:
                capture.append(body["cmd"])
            # echo a success result that mirrors function 0x10
            return httpx.Response(
                200, json={"errno": 0, "errmsg": "success", "data": {"result": "0210abcd"}}
            )
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


def test_writes_disabled_by_default(sweep) -> None:
    fox = FoxESS("mock", transport=_transport(sweep))
    with pytest.raises(FoxWritesDisabled):
        fox.write_field(2, 1, "DA", 3, confirm=True)


def test_dry_run_allowed_even_when_disabled(sweep) -> None:
    fox = FoxESS("mock", transport=_transport(sweep))
    result = fox.write_field(2, 1, "DA", 3, dry_run=True)
    assert result.sent is False
    assert result.frame_hex == "02109c840001020003b0ec"
    assert result.register == 0x9C84


def test_enabled_but_unconfirmed_refuses(sweep) -> None:
    fox = FoxESS("mock", transport=_transport(sweep), allow_writes=True)
    with pytest.raises(FoxWriteNotConfirmed):
        fox.write_field(2, 1, "DA", 3)


def test_read_only_field_refused(sweep) -> None:
    fox = FoxESS("mock", transport=_transport(sweep), allow_writes=True)
    with pytest.raises(FoxWriteNotAllowed):
        fox.write_field(2, 1, "Mn", "X", confirm=True)  # Manufacturer is read-only


def test_range_validation(sweep) -> None:
    fox = FoxESS("mock", transport=_transport(sweep), allow_writes=True)
    with pytest.raises(FoxWriteRangeError):
        fox.write_field(2, 1, "DA", 300, confirm=True)  # DA hint is 1-246


def test_successful_write_sends_frame(sweep) -> None:
    sent: list[str] = []
    fox = FoxESS("mock", transport=_transport(sweep, capture=sent), allow_writes=True)
    result = fox.write_field(2, 1, "DA", 5, confirm=True)
    assert result.sent is True
    assert result.result_hex == "0210abcd"
    assert sent == [result.frame_hex]
    assert result.frame_hex.startswith("0210")  # addr 02, func 0x10

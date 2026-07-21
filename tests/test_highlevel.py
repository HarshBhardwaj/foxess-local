"""High-level measurement API tests (mock device, values from real captures)."""

from __future__ import annotations

import httpx
import pytest

from foxess.client import FoxESS


@pytest.fixture
def fox(sweep) -> FoxESS:
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

    from foxess.transport import Transport

    client = httpx.Client(base_url="http://mock", transport=httpx.MockTransport(handler))
    return FoxESS("mock", transport=Transport("mock", client=client))


def test_system(fox: FoxESS) -> None:
    s = fox.system
    assert s.model == "AIO-H1-11.4-US"
    assert s.serial == "601U113057GH041"
    assert s.device_address == 2


def test_battery(fox: FoxESS) -> None:
    b = fox.battery
    assert b.soc_percent == 51.0
    assert b.soh_percent == 100
    assert b.voltage_v == 180.3
    assert b.current_a == 9.8
    assert b.temperature_c == 32.3
    assert b.power_w == -1783
    assert b.charging is True          # negative power = charging
    assert b.energy_rated_wh == 11925


def test_grid(fox: FoxESS) -> None:
    # fox.grid is net grid flow from model 65031 (HubInfo) at the gateway addr.
    # Captured during a pure grid-import moment: importing 959 W.
    g = fox.grid
    assert g.power_w == -959          # negative = import (verified sign)
    assert g.import_power_w == 959
    assert g.export_power_w == 0.0
    assert g.import_energy_total_kwh == 3660.5
    assert g.export_energy_total_kwh == 316.5


def test_load(fox: FoxESS) -> None:
    # Whole-home load from model 65031 (HubInfo): +959 W == the import above.
    assert fox.load.power_w == 959


def test_ac(fox: FoxESS) -> None:
    # Inverter AC terminal (model 701), previously exposed as "grid".
    ac = fox.ac
    assert ac.frequency_hz == 59.98
    assert ac.voltage_v == 120.0
    assert ac.power_w == 0


def test_battery_energy_counters(fox: FoxESS) -> None:
    b = fox.battery
    assert b.energy_charged_total_kwh == 390.1
    assert b.energy_discharged_total_kwh == 335.2
    assert b.charge_power_w == 1783   # power_w == -1783 -> charging
    assert b.discharge_power_w == 0.0


def test_solar(fox: FoxESS) -> None:
    s = fox.solar
    assert s.power_w == 1795
    # Energy counters carry the En_SF ÷10 scale (verified against the UI):
    assert s.total_energy_kwh == 315.9
    assert s.daily_energy_kwh == 1.4


def test_inverter_status(fox: FoxESS) -> None:
    inv = fox.inverter
    assert inv.temperature_c == 35.2
    assert inv.inverter_state == 3

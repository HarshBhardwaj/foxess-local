"""Prometheus exporter tests (render exposition against a mock device)."""

from __future__ import annotations

import httpx
import pytest

pytest.importorskip("prometheus_client")

from foxess.client import FoxESS  # noqa: E402
from foxess.prometheus import FoxCollector, render  # noqa: E402
from foxess.transport import Transport  # noqa: E402


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
            json={"errno": 0, "errmsg": "success", "mstype": 2,
                  "data": {"id": mid, "reg_addr": rec.reg_addr, "tbl": rec.tbl_hex}},
        )

    client = httpx.Client(base_url="http://mock", transport=httpx.MockTransport(handler))
    return FoxESS("mock", transport=Transport("mock", client=client))


def test_render_contains_core_metrics(fox: FoxESS) -> None:
    text = render(fox).decode()
    assert "fox_battery_soc_percent 51.0" in text
    assert "fox_battery_voltage_volts 180.3" in text
    assert "fox_grid_frequency_hertz 59.98" in text
    assert "fox_pv_power_watts 1795.0" in text


def test_operational_metrics_present(fox: FoxESS) -> None:
    text = render(fox).decode()
    for name in (
        "fox_up",
        "fox_poll_success_total",
        "fox_poll_errors_total",
        "fox_decoder_errors_total",
        "fox_last_success_timestamp_seconds",
        "fox_scrape_duration_seconds",
        "fox_device_info",
    ):
        assert name in text


def test_up_is_one_on_success(fox: FoxESS) -> None:
    text = render(fox).decode()
    assert "fox_up 1.0" in text


def test_device_info_labels(fox: FoxESS) -> None:
    text = render(fox).decode()
    assert 'serial="601U10000000000"' in text
    assert 'model="AIO-H1-11.4-US"' in text


def test_counters_increment_across_scrapes(fox: FoxESS) -> None:
    collector = FoxCollector(fox)
    list(collector.collect())
    list(collector.collect())
    assert collector._stats.poll_success == 2

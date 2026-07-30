"""MQTT + Home Assistant discovery tests (pure builders + fake client)."""

from __future__ import annotations

import json

import httpx
import pytest

from foxess.client import FoxESS
from foxess.measurements import SystemInfo
from foxess.mqtt import (
    AVAILABILITY_OFFLINE,
    AVAILABILITY_ONLINE,
    SENSORS,
    MqttConfig,
    MqttPublisher,
    build_discovery,
    build_states,
    collect_views,
)
from foxess.transport import Transport


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
                "errno": 0,
                "errmsg": "success",
                "mstype": 2,
                "data": {"id": mid, "reg_addr": rec.reg_addr, "tbl": rec.tbl_hex},
            },
        )

    client = httpx.Client(base_url="http://mock", transport=httpx.MockTransport(handler))
    return FoxESS("mock", transport=Transport("mock", client=client))


def test_discovery_payloads() -> None:
    system = SystemInfo("FOX", "AIO-H1-11.4-US", "601U10000000000", "1.1.11.8c", 2)
    cfg = MqttConfig(prefix="fox")
    disc = build_discovery(system, cfg)
    assert len(disc) == len(SENSORS)
    topics = {t for t, _ in disc}
    soc_topic = "homeassistant/sensor/foxess_601U10000000000/battery_soc_percent/config"
    assert soc_topic in topics
    payload = next(p for t, p in disc if t == soc_topic)
    assert payload["device_class"] == "battery"
    assert payload["unit_of_measurement"] == "%"
    assert payload["state_topic"] == "fox/battery"
    assert payload["value_template"] == "{{ value_json.soc_percent }}"
    assert payload["unique_id"] == "foxess_601U10000000000_battery_soc_percent"
    assert payload["availability_topic"] == "fox/status"
    assert payload["device"]["identifiers"] == ["foxess_601U10000000000"]
    assert payload["device"]["model"] == "AIO-H1-11.4-US"


def test_unique_ids_are_unique() -> None:
    system = SystemInfo("FOX", "M", "SN123", "v", 2)
    disc = build_discovery(system, MqttConfig())
    uids = [p["unique_id"] for _, p in disc]
    assert len(uids) == len(set(uids))


def test_state_payloads_from_real_views(fox: FoxESS) -> None:
    cfg = MqttConfig(prefix="fox")
    states = dict(build_states(collect_views(fox), cfg))
    battery = json.loads(states["fox/battery"])
    assert battery["soc_percent"] == 51.0
    assert battery["voltage_v"] == 180.3
    assert battery["energy_discharged_total_kwh"] == 335.2
    # Net grid flow (model 65031 HubInfo, gateway addr) on fox/grid; AC freq on fox/ac.
    grid = json.loads(states["fox/grid"])
    assert grid["power_w"] == -959  # negative = import
    assert grid["import_energy_total_kwh"] == 3660.5  # real Hub meter counter
    ac = json.loads(states["fox/ac"])
    assert ac["frequency_hz"] == 59.98


class _FakeClient:
    def __init__(self, *, raise_on_publish: bool = False) -> None:
        self.published: list[tuple[str, str, bool]] = []
        self._raise_on_publish = raise_on_publish
        self.loop_stop_called = False
        self.disconnect_called = False

    def publish(self, topic: str, payload: str = "", retain: bool = False) -> None:
        if self._raise_on_publish:
            raise RuntimeError("boom")
        self.published.append((topic, payload, retain))

    def loop_stop(self) -> None:
        self.loop_stop_called = True

    def disconnect(self) -> None:
        self.disconnect_called = True


def test_publisher_emits_discovery_and_state(fox: FoxESS) -> None:
    pub = MqttPublisher(fox, MqttConfig(prefix="fox"))
    pub._client = _FakeClient()
    pub.publish_discovery()
    pub.publish_once()
    topics = [t for t, _, _ in pub._client.published]
    # discovery is retained
    assert any(t.endswith("/battery_soc_percent/config") for t in topics)
    assert all(retain for t, _, retain in pub._client.published if t.endswith("/config"))
    # state topics present
    assert "fox/battery" in topics
    assert "fox/solar" in topics


@pytest.fixture
def flaky_fox(sweep):
    """A device whose first ``fail_until`` HTTP calls time out, then behaves
    like the real captured sweep. ``retries=0`` on the Transport so a "failed"
    call fails immediately (no real sleep from the transport's own backoff) --
    this fixture is for exercising MqttPublisher.run's resilience, not
    Transport's own retry behaviour (covered in test_transport.py)."""
    calls = {"n": 0}
    state = {"fail_until": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] <= state["fail_until"]:
            raise httpx.TimeoutException("simulated device timeout", request=request)
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
    transport = Transport("mock", client=client, retries=0, backoff=0.0)
    fox = FoxESS("mock", transport=transport)
    return fox, state, calls


def test_run_survives_transient_device_failure_and_recovers(flaky_fox) -> None:
    """Regression test for the crash-loop bug: a device that times out on
    startup (during the discovery read) or on any later poll must not take
    ``run`` down -- it should flip availability to "offline", count the
    failure, and keep going, exactly like foxess.prometheus.FoxCollector
    already does per-scrape."""
    fox, state, calls = flaky_fox
    # Fails the discovery read (1 call) and the first poll's first model read
    # (the next call) -- i.e. the whole first iteration -- then recovers.
    state["fail_until"] = 2

    pub = MqttPublisher(fox, MqttConfig(prefix="fox", interval=0.0))
    pub._client = _FakeClient()

    pub.run(iterations=3)  # must not raise

    assert pub.poll_errors == 1
    assert pub.poll_success == 2

    avail = [p for t, p, _ in pub._client.published if t == "fox/status"]
    assert AVAILABILITY_OFFLINE in avail
    assert AVAILABILITY_ONLINE in avail
    assert avail.index(AVAILABILITY_OFFLINE) < avail.index(AVAILABILITY_ONLINE)

    # Discovery retried after the first failed attempt and eventually published.
    topics = [t for t, _, _ in pub._client.published]
    assert any(t.endswith("/battery_soc_percent/config") for t in topics)
    # And state kept flowing once the device recovered.
    assert "fox/battery" in topics


def test_run_gives_up_on_non_fox_errors(fox: FoxESS) -> None:
    """A bug (or any non-FoxError failure) must still surface, not be silently
    retried forever -- resilience is scoped to the known "device/broker didn't
    answer" failure modes, not a blanket except-and-continue."""
    pub = MqttPublisher(fox, MqttConfig(prefix="fox", interval=0.0))
    pub._client = _FakeClient(raise_on_publish=True)

    with pytest.raises(RuntimeError, match="boom"):
        pub.run(iterations=3)

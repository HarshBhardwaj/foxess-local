"""MQTT + Home Assistant discovery tests (pure builders + fake client)."""

from __future__ import annotations

import json

import httpx
import pytest

from foxess.client import FoxESS
from foxess.measurements import SystemInfo
from foxess.mqtt import (
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
            json={"errno": 0, "errmsg": "success", "mstype": 2,
                  "data": {"id": mid, "reg_addr": rec.reg_addr, "tbl": rec.tbl_hex}},
        )

    client = httpx.Client(base_url="http://mock", transport=httpx.MockTransport(handler))
    return FoxESS("mock", transport=Transport("mock", client=client))


def test_discovery_payloads() -> None:
    system = SystemInfo("FOX", "AIO-H1-11.4-US", "601U113057GH041", "1.1.11.8c", 2)
    cfg = MqttConfig(prefix="fox")
    disc = build_discovery(system, cfg)
    assert len(disc) == len(SENSORS)
    topics = {t for t, _ in disc}
    soc_topic = "homeassistant/sensor/foxess_601U113057GH041/battery_soc_percent/config"
    assert soc_topic in topics
    payload = next(p for t, p in disc if t == soc_topic)
    assert payload["device_class"] == "battery"
    assert payload["unit_of_measurement"] == "%"
    assert payload["state_topic"] == "fox/battery"
    assert payload["value_template"] == "{{ value_json.soc_percent }}"
    assert payload["unique_id"] == "foxess_601U113057GH041_battery_soc_percent"
    assert payload["availability_topic"] == "fox/status"
    assert payload["device"]["identifiers"] == ["foxess_601U113057GH041"]
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
    grid = json.loads(states["fox/grid"])
    assert grid["frequency_hz"] == 59.98


class _FakeClient:
    def __init__(self) -> None:
        self.published: list[tuple[str, str, bool]] = []

    def publish(self, topic: str, payload: str = "", retain: bool = False) -> None:
        self.published.append((topic, payload, retain))


def test_publisher_emits_discovery_and_state(fox: FoxESS) -> None:
    pub = MqttPublisher(fox, MqttConfig(prefix="fox"))
    pub._client = _FakeClient()
    pub.publish_discovery()
    pub.publish_once()
    topics = [t for t, _, _ in pub._client.published]
    # discovery is retained
    assert any(t.endswith("/battery_soc_percent/config") for t in topics)
    assert all(
        retain for t, _, retain in pub._client.published if t.endswith("/config")
    )
    # state topics present
    assert "fox/battery" in topics
    assert "fox/solar" in topics

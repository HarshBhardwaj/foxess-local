"""MQTT publishing with Home Assistant MQTT Discovery (Phase 6).

Design:
- One JSON *state* topic per group (``<prefix>/battery`` …); each HA sensor reads
  a field from it via a ``value_template``. Fewer topics, atomic updates.
- One retained *discovery* config per sensor under ``<discovery_prefix>/sensor/…``
  so Home Assistant auto-creates entities with the right device_class, unit,
  and state_class, all attached to one device (keyed by the inverter serial).
- A device *availability* topic (``<prefix>/status``) set as the MQTT LWT, so
  entities go "unavailable" if the publisher dies.

The payload builders are pure and unit-tested; the paho-mqtt client is a thin
loop imported lazily (optional ``[mqtt]`` extra).
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .measurements import SystemInfo

AVAILABILITY_ONLINE = "online"
AVAILABILITY_OFFLINE = "offline"


@dataclass(frozen=True, slots=True)
class SensorSpec:
    """One Home Assistant sensor derived from a measurement-view field."""

    group: str  # state-topic group, e.g. "battery"
    field: str  # attribute on the view / key in the JSON state
    name: str  # human name (device name is prepended by HA)
    device_class: str | None = None
    unit: str | None = None
    state_class: str | None = "measurement"
    icon: str | None = None

    @property
    def object_id(self) -> str:
        return f"{self.group}_{self.field}"


# Sensor catalogue. Units/classes follow Home Assistant conventions.
SENSORS: tuple[SensorSpec, ...] = (
    # Battery
    SensorSpec("battery", "soc_percent", "Battery SoC", "battery", "%"),
    SensorSpec("battery", "soh_percent", "Battery Health", None, "%", icon="mdi:heart-pulse"),
    SensorSpec("battery", "voltage_v", "Battery Voltage", "voltage", "V"),
    SensorSpec("battery", "current_a", "Battery Current", "current", "A"),
    SensorSpec("battery", "power_w", "Battery Power", "power", "W"),
    SensorSpec("battery", "charge_power_w", "Battery Charge Power", "power", "W"),
    SensorSpec("battery", "discharge_power_w", "Battery Discharge Power", "power", "W"),
    SensorSpec("battery", "temperature_c", "Battery Temperature", "temperature", "°C"),
    SensorSpec(
        "battery", "energy_available_wh", "Battery Energy Available", "energy_storage", "Wh"
    ),
    # Battery cumulative energy (for the HA Energy dashboard battery in/out tiles)
    SensorSpec(
        "battery",
        "energy_charged_total_kwh",
        "Battery Energy Charged Total",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    SensorSpec(
        "battery",
        "energy_discharged_total_kwh",
        "Battery Energy Discharged Total",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    SensorSpec(
        "battery",
        "energy_charged_today_kwh",
        "Battery Energy Charged Today",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    SensorSpec(
        "battery",
        "energy_discharged_today_kwh",
        "Battery Energy Discharged Today",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    # Grid (net import/export -- model 65031 'HubInfo' at the gateway address).
    # power_w is signed: negative = import, positive = export.
    SensorSpec("grid", "power_w", "Grid Power", "power", "W"),
    SensorSpec("grid", "import_power_w", "Grid Import Power", "power", "W"),
    SensorSpec("grid", "export_power_w", "Grid Export Power", "power", "W"),
    SensorSpec(
        "grid",
        "import_energy_total_kwh",
        "Grid Import Energy",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    SensorSpec(
        "grid",
        "export_energy_total_kwh",
        "Grid Export Energy",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    SensorSpec(
        "grid",
        "import_energy_today_kwh",
        "Grid Import Energy Today",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    SensorSpec(
        "grid",
        "export_energy_today_kwh",
        "Grid Export Energy Today",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    # Inverter AC terminal (model 701 -- previously mislabeled "grid")
    SensorSpec("ac", "power_w", "Inverter AC Power", "power", "W"),
    SensorSpec("ac", "frequency_hz", "Grid Frequency", "frequency", "Hz"),
    SensorSpec("ac", "voltage_v", "AC Voltage", "voltage", "V"),
    SensorSpec("ac", "current_a", "AC Current", "current", "A"),
    SensorSpec("ac", "power_factor", "Power Factor", "power_factor", None),
    SensorSpec(
        "ac",
        "energy_injected_wh",
        "AC Energy Injected",
        "energy",
        "Wh",
        state_class="total_increasing",
    ),
    # Solar
    SensorSpec("solar", "power_w", "Solar Power", "power", "W"),
    SensorSpec(
        "solar",
        "daily_energy_kwh",
        "Solar Energy Today",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    SensorSpec(
        "solar",
        "total_energy_kwh",
        "Solar Energy Total",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    # Load
    SensorSpec("load", "power_w", "Load Power", "power", "W"),
    SensorSpec(
        "load",
        "total_energy_kwh",
        "Load Energy Total",
        "energy",
        "kWh",
        state_class="total_increasing",
    ),
    # Inverter status
    SensorSpec("inverter", "temperature_c", "Inverter Temperature", "temperature", "°C"),
    SensorSpec(
        "inverter",
        "operating_state",
        "Operating State",
        None,
        None,
        state_class=None,
        icon="mdi:state-machine",
    ),
    SensorSpec(
        "inverter",
        "inverter_state",
        "Inverter State",
        None,
        None,
        state_class=None,
        icon="mdi:state-machine",
    ),
)


@dataclass(frozen=True, slots=True)
class MqttConfig:
    host: str = "localhost"
    port: int = 1883
    username: str | None = None
    password: str | None = None
    prefix: str = "fox"
    discovery_prefix: str = "homeassistant"
    client_id: str = "foxess-local"
    interval: float = 15.0
    retain_state: bool = False


def _node_id(serial: str | None) -> str:
    return f"foxess_{serial or 'unknown'}"


def availability_topic(cfg: MqttConfig) -> str:
    return f"{cfg.prefix}/status"


def state_topic(cfg: MqttConfig, group: str) -> str:
    return f"{cfg.prefix}/{group}"


def _device_block(system: SystemInfo, cfg: MqttConfig) -> dict[str, Any]:
    node = _node_id(system.serial)
    return {
        "identifiers": [node],
        "manufacturer": system.manufacturer or "FoxESS",
        "model": system.model or "Smart WiLAN",
        "name": f"FoxESS {system.model or ''}".strip(),
        "sw_version": system.version,
        "serial_number": system.serial,
    }


def build_discovery(system: SystemInfo, cfg: MqttConfig) -> list[tuple[str, dict[str, Any]]]:
    """Return (config_topic, payload) pairs for every sensor (retained)."""
    node = _node_id(system.serial)
    device = _device_block(system, cfg)
    avail = availability_topic(cfg)
    out: list[tuple[str, dict[str, Any]]] = []
    for spec in SENSORS:
        uid = f"{node}_{spec.object_id}"
        topic = f"{cfg.discovery_prefix}/sensor/{node}/{spec.object_id}/config"
        payload: dict[str, Any] = {
            "name": spec.name,
            "unique_id": uid,
            "object_id": uid,
            "state_topic": state_topic(cfg, spec.group),
            "value_template": f"{{{{ value_json.{spec.field} }}}}",
            "availability_topic": avail,
            "payload_available": AVAILABILITY_ONLINE,
            "payload_not_available": AVAILABILITY_OFFLINE,
            "device": device,
        }
        if spec.device_class:
            payload["device_class"] = spec.device_class
        if spec.unit:
            payload["unit_of_measurement"] = spec.unit
        if spec.state_class:
            payload["state_class"] = spec.state_class
        if spec.icon:
            payload["icon"] = spec.icon
        out.append((topic, payload))
    return out


Views = Mapping[str, Any]


def build_states(views: Views, cfg: MqttConfig) -> list[tuple[str, str]]:
    """Return (state_topic, json_payload) pairs from measurement views.

    ``views`` maps group name -> view object (battery/grid/solar/load/inverter).
    Missing groups are skipped; ``None`` fields are emitted as JSON null so Home
    Assistant renders them as unknown rather than a stale value.
    """
    groups: dict[str, list[str]] = {}
    for spec in SENSORS:
        groups.setdefault(spec.group, []).append(spec.field)
    out: list[tuple[str, str]] = []
    for group, fields in groups.items():
        view = views.get(group)
        if view is None:
            continue
        payload = {f: getattr(view, f, None) for f in fields}
        out.append((state_topic(cfg, group), json.dumps(payload)))
    return out


def collect_views(fox: Any) -> dict[str, Any]:
    """Read the five publishable views from a (sync) FoxESS client."""
    return {
        "battery": fox.battery,
        "grid": fox.grid,  # GridFlow (model 65004) -- net import/export
        "ac": fox.ac,  # AcMeasurement (model 701) -- inverter AC terminal
        "solar": fox.solar,
        "load": fox.load,
        "inverter": fox.inverter,
    }


class MqttPublisher:
    """Thin paho-mqtt publisher: discovery once, then a state poll loop."""

    def __init__(self, fox: Any, cfg: MqttConfig | None = None) -> None:
        self._fox = fox
        self._cfg = cfg or MqttConfig()
        self._client: Any = None

    def _connect(self) -> Any:
        try:
            import paho.mqtt.client as mqtt
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "MQTT support requires the [mqtt] extra: pip install 'foxess-local[mqtt]'"
            ) from exc
        cfg = self._cfg
        client = mqtt.Client(client_id=cfg.client_id)
        if cfg.username:
            client.username_pw_set(cfg.username, cfg.password)
        client.will_set(availability_topic(cfg), AVAILABILITY_OFFLINE, retain=True)
        client.connect(cfg.host, cfg.port)
        client.loop_start()
        client.publish(availability_topic(cfg), AVAILABILITY_ONLINE, retain=True)
        return client

    def publish_discovery(self) -> None:
        system: SystemInfo = self._fox.system
        for topic, payload in build_discovery(system, self._cfg):
            self._client.publish(topic, json.dumps(payload), retain=True)

    def publish_once(self) -> None:
        for topic, payload in build_states(collect_views(self._fox), self._cfg):
            self._client.publish(topic, payload, retain=self._cfg.retain_state)

    def run(self, *, iterations: int | None = None) -> None:
        """Connect, announce discovery, then publish states every ``interval`` s."""
        import time

        self._client = self._connect()
        try:
            self.publish_discovery()
            count = 0
            while iterations is None or count < iterations:
                self.publish_once()
                count += 1
                if iterations is not None and count >= iterations:
                    break
                time.sleep(self._cfg.interval)
        finally:
            cfg = self._cfg
            self._client.publish(availability_topic(cfg), AVAILABILITY_OFFLINE, retain=True)
            self._client.loop_stop()
            self._client.disconnect()

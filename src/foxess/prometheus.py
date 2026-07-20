"""Prometheus exporter (Phase 7).

A pull exporter: metrics are read from the device on each scrape via a custom
collector. Measurement gauges (``fox_*``) come from the high-level views;
operational metrics (up, poll counters, last-success timestamp, decoder errors,
scrape duration) let you alert on the exporter itself.

No unbounded-cardinality labels: measurement series are label-free; device
identity is exposed once via ``fox_device_info``.

Requires the optional ``[prometheus]`` extra (``prometheus-client``). Imports are
lazy so the core SDK has no hard dependency.
"""

from __future__ import annotations

import time
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Any

from .errors import FoxError

# (metric, help, group, field). Gauges only; unit encoded in the name per
# Prometheus convention.
_GAUGES: tuple[tuple[str, str, str, str], ...] = (
    ("fox_battery_soc_percent", "Battery state of charge", "battery", "soc_percent"),
    ("fox_battery_soh_percent", "Battery state of health", "battery", "soh_percent"),
    ("fox_battery_voltage_volts", "Battery voltage", "battery", "voltage_v"),
    ("fox_battery_current_amps", "Battery current", "battery", "current_a"),
    ("fox_battery_power_watts", "Battery power (negative=charging)", "battery", "power_w"),
    ("fox_battery_temperature_celsius", "Battery temperature", "battery", "temperature_c"),
    ("fox_battery_remaining_energy_wh", "Battery available energy",
     "battery", "energy_available_wh"),
    ("fox_grid_power_watts", "Inverter AC / grid power", "grid", "power_w"),
    ("fox_grid_voltage_volts", "Grid voltage (L1-N)", "grid", "voltage_v"),
    ("fox_grid_current_amps", "Grid current (L1)", "grid", "current_a"),
    ("fox_grid_frequency_hertz", "Grid frequency", "grid", "frequency_hz"),
    ("fox_grid_power_factor", "Power factor", "grid", "power_factor"),
    ("fox_pv_power_watts", "PV / DC power", "solar", "power_w"),
    ("fox_load_power_watts", "Site load power (needs CT meter)", "load", "power_w"),
    ("fox_inverter_temperature_celsius", "Inverter heat-sink temperature",
     "inverter", "temperature_c"),
    ("fox_inverter_state", "Inverter state code", "inverter", "inverter_state"),
    ("fox_inverter_operating_state", "Operating state code", "inverter", "operating_state"),
)

# Monotonic energy counters (Prometheus counter semantics).
_COUNTERS: tuple[tuple[str, str, str, str], ...] = (
    ("fox_grid_energy_injected_wh_total", "Total energy injected to grid",
     "grid", "energy_injected_wh"),
    ("fox_pv_energy_total_kwh_total", "Lifetime PV generation", "solar", "total_energy_kwh"),
)

_GROUPS = ("battery", "grid", "solar", "load", "inverter")


@dataclass
class _Stats:
    poll_success: int = 0
    poll_errors: int = 0
    decoder_errors: int = 0
    last_success: float = 0.0


class FoxCollector:
    """Prometheus collector that reads a sync ``FoxESS`` client on each scrape."""

    def __init__(self, fox: Any, *, clock: Any = time.time) -> None:
        self._fox = fox
        self._clock = clock
        self._stats = _Stats()

    def _read_views(self) -> tuple[dict[str, Any], bool]:
        views: dict[str, Any] = {}
        ok = True
        for group in _GROUPS:
            try:
                views[group] = getattr(self._fox, group)
            except FoxError:
                ok = False
        return views, ok

    def collect(self) -> Iterator[Any]:
        from prometheus_client.core import (
            CounterMetricFamily,
            GaugeMetricFamily,
            InfoMetricFamily,
        )

        start = self._clock()
        views, ok = self._read_views()
        if ok and views:
            self._stats.poll_success += 1
            self._stats.last_success = self._clock()
        else:
            self._stats.poll_errors += 1

        # device_info (single info series; identity as labels, value implicit)
        system = views.get("_system")
        if system is None:
            try:
                system = self._fox.system
            except FoxError:
                system = None
        if system is not None:
            yield InfoMetricFamily(
                "fox_device", "FoxESS device identity",
                value={
                    "serial": str(system.serial or ""),
                    "model": str(system.model or ""),
                    "manufacturer": str(system.manufacturer or ""),
                    "version": str(system.version or ""),
                },
            )

        for metric, doc, group, field in _GAUGES:
            g = GaugeMetricFamily(metric, doc)
            value = _view_value(views, group, field)
            if isinstance(value, (int, float)):
                g.add_metric([], float(value))
            yield g

        for metric, doc, group, field in _COUNTERS:
            c = CounterMetricFamily(metric, doc)
            value = _view_value(views, group, field)
            if isinstance(value, (int, float)):
                c.add_metric([], float(value))
            yield c

        # alarm bitfield (parse the hex string from the inverter view)
        alarm = GaugeMetricFamily("fox_inverter_alarm_bitfield", "Inverter alarm bitfield")
        inv = views.get("inverter")
        if inv is not None and isinstance(getattr(inv, "alarm", None), str):
            try:
                alarm.add_metric([], float(int(inv.alarm, 16)))
            except ValueError:
                pass
        yield alarm

        # operational metrics
        up = GaugeMetricFamily("fox_up", "1 if the last scrape read the device successfully")
        up.add_metric([], 1.0 if ok else 0.0)
        yield up

        succ = CounterMetricFamily("fox_poll_success_total", "Successful device scrapes")
        succ.add_metric([], float(self._stats.poll_success))
        yield succ

        errs = CounterMetricFamily("fox_poll_errors_total", "Failed device scrapes")
        errs.add_metric([], float(self._stats.poll_errors))
        yield errs

        derr = CounterMetricFamily("fox_decoder_errors_total", "Decoder failures")
        derr.add_metric([], float(self._stats.decoder_errors))
        yield derr

        last = GaugeMetricFamily(
            "fox_last_success_timestamp_seconds", "Unix time of last successful scrape"
        )
        last.add_metric([], float(self._stats.last_success))
        yield last

        dur = GaugeMetricFamily("fox_scrape_duration_seconds", "Duration of this scrape")
        dur.add_metric([], float(self._clock() - start))
        yield dur


def _view_value(views: dict[str, Any], group: str, field: str) -> Any:
    view = views.get(group)
    if view is None:
        return None
    return getattr(view, field, None)


def build_registry(fox: Any) -> Any:
    """Return a CollectorRegistry with a FoxCollector registered."""
    from prometheus_client import CollectorRegistry

    registry = CollectorRegistry()
    registry.register(FoxCollector(fox))
    return registry


def render(fox: Any) -> bytes:
    """Render the exposition text for one scrape (useful for tests / embedding)."""
    from prometheus_client import generate_latest

    return bytes(generate_latest(build_registry(fox)))


def serve(fox: Any, host: str = "0.0.0.0", port: int = 9110) -> None:  # noqa: S104
    """Run a blocking WSGI /metrics server backed by ``fox``."""
    from wsgiref.simple_server import make_server

    from prometheus_client import make_wsgi_app

    app = make_wsgi_app(build_registry(fox))
    with make_server(host, port, app) as httpd:
        httpd.serve_forever()


def iter_metric_names(families: Iterable[Any]) -> list[str]:
    """Helper for tests: metric-family names from a collect() iterator."""
    return [f.name for f in families]

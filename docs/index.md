# foxess-local

A fully-local, **evidence-first** Python SDK for FoxESS "Smart WiLAN" devices
(e.g. Fox Hub G2 gateway + AIO-H1 inverter). No FoxCloud, no account, no
internet — it talks to the device's own `http://<ip>/api/v1/sunspec/data`
endpoint and decodes the SunSpec/Modbus frames locally.

> Every register mapping in this SDK was extracted from the device's own
> frontend decoder and verified against live device values. See
> `docs/01-technical-discovery-report.md` and
> `docs/02-frontend-decoder-and-register-map.md`.

## Status

- ✅ CRC-16/Modbus, verified against every captured frame
- ✅ Frame layer — splits concatenated Modbus RTU frames, CRC-checks each, reassembles
- ✅ Model registry — all **54 models** loaded from the extracted register map
- ✅ Decoder — full type system, scale factors (incl. `sfm` constants), enums; verified
- ✅ Sync + **async** cores (`FoxESS` / `AsyncFoxESS`)
- ✅ **High-level API** — `battery`, `grid`, `solar`, `load`, `inverter`, `system`
- ✅ **REST API** (FastAPI) — read-only, versioned, OpenAPI docs
- ✅ **MQTT + Home Assistant MQTT Discovery** — auto-created entities on one device
- ✅ **Prometheus exporter** — `fox_*` gauges + health/polling metrics, `/metrics`
- ✅ **WebSocket streaming** — `/api/v1/ws`, versioned envelopes, subscription filtering, heartbeats
- ✅ CLI — `models`, `decode`, `read`, `scan`, `serve`, `mqtt`, `exporter`
- ✅ **Write support** — verified encoder, disabled-by-default, opt-in, dry-run, validated (Phase 11)
- ✅ **Docker** stack + **GitHub Actions CI** + pre-commit + docs + release checklist

All 11 phases of the requirements document are implemented. 61 tests (no
hardware required), ruff + mypy-strict clean.

Cross-checked against FoxCloud: local battery SoC read **80.0%** vs cloud **80%**
(exact); battery V×A matched the reported charge power. Grid/load instantaneous
power needs a CT meter (not fitted on the reference unit — FoxCloud derives it).

## Install

```bash
pip install -e ".[dev]"
```

## Quick start

Offline (decode a captured `tbl` payload, no device needed):

```python
from foxess import decode, reassemble_hex

frame = reassemble_hex(tbl_hex)          # split + CRC-check + reassemble
model = decode(frame.payload, 702, addr=2)
print(model.get("WMaxRtg"))              # 11400  (matches the 11.4 kW nameplate)
```

High-level (against a device on your LAN):

```python
from foxess import FoxESS

with FoxESS("192.168.1.38") as fox:
    print(fox.system.model)          # 'AIO-H1-11.4-US'
    print(fox.battery.soc_percent)   # 80.0
    print(fox.battery.power_w)        # -2668  (negative = charging)
    print(fox.solar.power_w)          # 2685
    print(fox.grid.frequency_hz)      # 60.01
```

Async (concurrent model reads under the hood):

```python
import asyncio
from foxess import AsyncFoxESS

async def main():
    async with AsyncFoxESS("192.168.1.38") as fox:
        b, s = await asyncio.gather(fox.battery(), fox.solar())
        print(b.soc_percent, s.power_w)

asyncio.run(main())
```

CLI:

```bash
fox models                 # list the register map
fox decode 702 <tbl_hex>   # decode a captured payload offline
fox read 192.168.1.38 2 1  # read + decode a live model
fox scan 192.168.1.38 2    # probe available models
fox serve 192.168.1.38     # run the read-only REST API (needs [api] extra)
```

## REST API

```bash
pip install -e ".[api]"
fox serve 192.168.1.38 --bind 0.0.0.0 --port 8080
```

Endpoints (versioned under `/api/v1`, OpenAPI docs at `/docs`):

```
GET /api/v1/system        GET /api/v1/battery      GET /api/v1/grid
GET /api/v1/solar         GET /api/v1/load         GET /api/v1/inverter
GET /api/v1/models        GET /api/v1/models/{id}  GET /api/v1/raw/{addr}/{id}
GET /api/v1/health        GET /api/v1/ready
```

## MQTT + Home Assistant

```bash
pip install -e ".[mqtt]"
fox mqtt 192.168.1.38 --broker 192.168.1.10 --username user --password pass
```

The publisher announces Home Assistant MQTT Discovery once (retained), then
publishes grouped JSON state every `--interval` seconds. Home Assistant
auto-creates ~20 sensors (SoC, battery/grid/solar/load power, voltages,
frequency, temperatures, energy counters) attached to a single device keyed by
the inverter serial, each with the correct `device_class`, unit, and
`state_class`. An availability topic (MQTT last-will) marks entities
unavailable if the publisher stops. State topics: `fox/battery`, `fox/grid`,
`fox/solar`, `fox/load`, `fox/inverter` (JSON); discovery under
`homeassistant/sensor/foxess_<serial>/…`.

## Prometheus

```bash
pip install -e ".[prometheus]"
fox exporter 192.168.1.38 --port 9110      # standalone /metrics on :9110
# or, if the REST API is running, GET /metrics on that server
```

Exposes measurement gauges (`fox_battery_soc_percent`, `fox_grid_power_watts`,
`fox_pv_power_watts`, `fox_battery_voltage_volts`, …), monotonic energy counters
(`fox_pv_energy_total_kwh_total`), the inverter alarm bitfield, and operational
metrics for alerting: `fox_up`, `fox_poll_success_total`, `fox_poll_errors_total`,
`fox_decoder_errors_total`, `fox_last_success_timestamp_seconds`,
`fox_scrape_duration_seconds`. Device identity is a single `fox_device_info`
series — measurement series carry no labels (no unbounded cardinality).

## WebSocket streaming

Connect to `ws://<host>:8080/api/v1/ws?interval=5` (served by the REST app). On
connect you get a `hello` envelope listing groups and protocol version, then
periodic `update` envelopes per group, `event` envelopes for inverter alarms
(`faults`), and `heartbeat`s. Every message is versioned:

```json
{"v": 1, "type": "update", "group": "battery", "ts": 1721490000.0,
 "data": {"soc_percent": 80.0, "power_w": -2668, ...}}
```

Filter with control messages: `{"action": "set", "groups": ["battery","solar"]}`
(also `subscribe` / `unsubscribe`). Sends are awaited, so a slow client throttles
its own feed (backpressure) rather than growing an unbounded queue.

## Architecture

```
transport.py   HTTP  ->  {errno, mstype, data:{id, reg_addr, tbl}}
frame.py       tbl   ->  split concatenated Modbus RTU frames, CRC each, reassemble
registry.py    data/fox_model_defs.json (54 models) -> typed FoxModelDef
decoder.py     payload + model -> DecodedModel (typed, scaled, enum-mapped)
client.py      FoxESS facade: read_raw / read_model / scan
```

Addressing primitive is `(addr, id)`: `addr=1` is the gateway, `addr=2` the
inverter. The transport, frame, and decode layers are independent and each
testable in isolation.

## Testing

```bash
pytest        # 21 tests, all run against captured fixtures — no hardware needed
ruff check .
mypy
```

The test suite decodes real captured frames and asserts known-good values
(device identity strings, `WMaxRtg == 11400 W`, battery SoC/SoH), and confirms
the one documented gateway framing anomaly (`addr=1 id=65004`) is rejected
cleanly.

## Layout

```
src/foxess/            the package (crc, frame, registry, decoder, transport, client, cli)
src/foxess/data/       fox_model_defs.json — the extracted register map (source of truth)
docs/                  discovery report + decoder/register-map analysis
tests/                 pytest suite + captured fixtures
examples/              runnable examples
tools/                 reverse-engineering scripts (parse_sweep, verify_decode)
frontend/              recovered + beautified device frontend (evidence)
```

## Safety

The local read API is effectively unauthenticated (only a username cookie).
Treat the device as an untrusted IoT endpoint: put it on an isolated VLAN,
firewall it, and never expose port 80 to the internet. Write support is
deliberately not implemented yet — the write path is not fully understood.

## License

MIT

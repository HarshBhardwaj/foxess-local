# MQTT & Home Assistant Guide

The `foxess-local` MQTT bridge polls the device locally and publishes to an MQTT
broker with Home Assistant MQTT Discovery, so entities appear automatically with
no YAML.

## Quick start

```bash
# foxess-local isn't published to PyPI yet — install from a clone
git clone https://github.com/HarshBhardwaj/foxess-local
cd foxess-local
pip install -e ".[mqtt]"

export FOX_HOST=<your-device-ip>
export MQTT_BROKER=<your-mqtt-broker>
fox mqtt "$FOX_HOST" --broker "$MQTT_BROKER" --username <u> --password <p>
```

Options: `--prefix` (default `fox`), `--discovery-prefix` (default
`homeassistant`), `--interval` seconds (default 15), `--port` (default 1883).

## Topic layout

| Purpose            | Topic                                               | Payload                                                                                                         |
| ------------------ | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Availability (LWT) | `fox/status`                                        | `online` / `offline` (retained)                                                                                 |
| Battery state      | `fox/battery`                                       | JSON: `soc_percent`, `soh_percent`, `voltage_v`, `current_a`, `power_w`, `temperature_c`, `energy_available_wh` |
| Grid state         | `fox/grid`                                          | JSON: `power_w`, `frequency_hz`, `voltage_v`, `current_a`, `power_factor`, `energy_injected_wh`                 |
| Solar state        | `fox/solar`                                         | JSON: `power_w`, `daily_energy_kwh`, `total_energy_kwh`                                                         |
| Load state         | `fox/load`                                          | JSON: `power_w`, `total_energy_kwh`                                                                             |
| Inverter state     | `fox/inverter`                                      | JSON: `temperature_c`, `operating_state`, `inverter_state`                                                      |
| Discovery          | `homeassistant/sensor/foxess_<serial>/<obj>/config` | HA sensor config (retained)                                                                                     |

Each discovery config points its `value_template` at the group's JSON state
topic, so one publish updates many entities atomically.

## What you get in Home Assistant

~20 sensors on one device (named `FoxESS <model>`, keyed by inverter serial,
carrying manufacturer / model / firmware version), including:

- **Battery**: SoC (`device_class: battery`, %), Health, Voltage, Current, Power
  (negative = charging), Temperature, Energy Available.
- **Grid/AC**: Power, Frequency, Voltage, Current, Power Factor, Energy Injected.
- **Solar**: Power, Energy Today, Energy Total (`state_class: total_increasing`
  → works with the HA Energy dashboard).
- **Inverter**: Heat-sink Temperature, Operating/Inverter state.

## Notes & caveats

- **Grid/Load instantaneous power needs a CT meter.** On installs without one
  (like the reference unit), `TotalActivePowerOfGrid`/`TotalActivePowerOfLoad`
  read ~0; those sensors will show 0/unknown. Solar and battery come straight
  from the inverter and are always populated.
- Values are published as JSON `null` when a source model/field is unavailable,
  so Home Assistant shows "unknown" rather than a stale reading.
- Energy counters carry the device's own scaling (verified against the UI); the
  `total_increasing` state class handles daily counter resets.
- **A device or broker outage degrades to `fox/status: offline`, it does not
  crash the bridge.** `MqttPublisher.run()` catches `FoxError` around both the
  discovery announce and every state poll (the same per-cycle pattern
  `foxess.prometheus.FoxCollector` already used for Prometheus scrapes), flips
  availability, counts the failure (`poll_success` / `poll_errors`), and
  retries next tick with capped exponential backoff instead of exiting. This
  fixes a crash-loop bug where a single slow device response (a timeout on
  the startup discovery read, in particular) took the whole `fox mqtt`
  process down; under the Home Assistant app's Watchdog that meant an
  immediate restart into the same timeout, repeating until the app landed in
  an `Error` state needing a manual restart. See `CHANGELOG.md` (Unreleased).

## Programmatic use

```python
import os
from foxess import FoxESS, MqttConfig, MqttPublisher

with FoxESS(os.environ["FOX_HOST"]) as fox:
    MqttPublisher(
        fox,
        MqttConfig(host=os.environ.get("MQTT_BROKER", "localhost"), interval=10),
    ).run()
```

# Changelog

All notable changes to this project are documented here
([Keep a Changelog](https://keepachangelog.com/en/1.1.0/)).
This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- **`fox mqtt` / the Home Assistant app no longer crash-loop on a transient
  device or broker outage.** `MqttPublisher.run()` previously let any
  `FoxError` (most commonly `FoxTimeoutError` from a slow inverter response)
  propagate out of the poll loop uncaught, killing the whole process; under a
  Supervisor Watchdog that meant an immediate restart into the same timeout,
  repeating until the app landed in `Error` needing a manual restart — even
  though the underlying outage was only a few seconds. The loop now mirrors
  `foxess.prometheus.FoxCollector`'s existing per-scrape resilience: a failed
  discovery announce or state poll flips MQTT availability to `offline`
  (Home Assistant shows "unavailable" instead of a stale value), is counted
  (`MqttPublisher.poll_success` / `poll_errors`), and is retried on the next
  tick with capped exponential backoff — it never ends the loop. The initial
  broker connect gets the same treatment instead of raising once and exiting.
  Non-`FoxError` failures (a missing extra, a real bug) still propagate, since
  retrying those would not help.

## [0.3.0] - 2026-07-20

Public-release hardening plus corrected grid/load metering for Home Assistant Energy.

### Added

- `GridFlow` high-level view (model **65031** HubInfo at the **gateway**) for
  net grid import/export power and daily/lifetime energy counters.
- `AcMeasurement` view for inverter AC-terminal readings (model **701**);
  accessible as `fox.ac` (and via the `GridMeasurement` alias).
- Battery charge/discharge power helpers and daily/lifetime charge/discharge
  energy fields on `BatteryInfo`.
- MQTT / Prometheus sensors for grid import/export and battery energy counters
  (Home Assistant Energy dashboard tiles).
- Sentinel handling in measurement decoding: int16/32 and uint16/32 “not
  available” register values map to `None` instead of nonsense numbers.
- `.gitignore` so local `.env`, caches, and build artifacts stay out of git.
- Gitleaks secret/PII gate (`.gitleaks.toml`): pre-commit hook + CI
  `secret-scan` job. Blocks FoxESS serials, private LAN IPs, and common
  credentials/tokens from being committed or merged.
- Documented secrets policy in `CONTRIBUTING.md`.

### Changed

- **Breaking:** `fox.grid` now returns `GridFlow` (HubInfo / gateway), not the
  old inverter AC (701) view. Use `fox.ac` for inverter AC-terminal data.
- **Breaking:** `fox.load` reads whole-home load from HubInfo (**65031**) at
  the gateway address (1), not model 65004 on the inverter.
- Docs, README, examples, and Docker references use `FOX_HOST` /
  `$MQTT_BROKER` placeholders instead of real LAN IPs.
- Package / image version aligned to **0.3.0**.

### Security

- Equipment serial numbers redacted from fixtures, tests, docs, and git
  history (placeholders `60HUB0000000000` / `601U10000000000`).
- `docker/.env` removed from version control; only `.env.example` is tracked.

### Fixed

- Grid and load power now match FoxCloud / Hub metering on units without an
  external revenue CT (previously mislabeled 701 AC as “grid”).
- Ruff unused-import / import-sort failures in CI after the metering PR.

## [0.2.0] - 2026-07-20

Configuration and Docker hardening so the stack is driven by environment
variables (no baked-in device IP).

### Added

- `docker/.env.example` documenting all Compose variables (`FOX_HOST`,
  `FOX_CORS_ORIGINS`, `API_PORT`, `MQTT_PORT`, `PROMETHEUS_PORT`,
  `GRAFANA_PORT`, `GRAFANA_PASSWORD`).
- Configurable host port mappings via env (`API_PORT`, etc.).

### Changed

- **Breaking (deploy):** `FOX_HOST` is **required**. Compose fails fast if
  unset (`${FOX_HOST:?…}`); the REST API raises if the env var is missing.
- Dockerfile no longer bakes a default device IP into the image.
- `examples/live_summary.py` reads `FOX_HOST` (or argv); no silent IP default.
- Docker deployment docs updated for required `FOX_HOST` and port clashes.

### Removed

- Hardcoded default device IP from runtime paths (`api.py`, Dockerfile,
  Compose defaults).

## [0.1.0] - 2026-07-20

Initial public SDK release.

### Added

- Evidence-first protocol layer: CRC-16/Modbus, concatenated-frame reassembly.
- Model registry: 54 SunSpec/FoxESS models extracted from the device firmware
  and verified against live values (incl. `sfm` constant scale factors).
- Decoder with full type system, scale factors, and enum mapping.
- Sync (`FoxESS`) and async (`AsyncFoxESS`) clients.
- High-level views: battery, grid, solar, load, inverter, system.
- REST API (FastAPI, versioned, read-only), WebSocket streaming, `/metrics`.
- MQTT publisher with Home Assistant MQTT Discovery.
- Prometheus exporter with health/polling metrics.
- CLI: models, decode, read, scan, serve, mqtt, exporter.
- Write support (Phase 11): verified encoder, disabled-by-default, opt-in,
  confirm-required, dry-run, range/enum validation, structured logging.
- Docker image + compose stack; GitHub Actions CI; pre-commit; docs.

### Security

- Documented that both read and write local APIs are effectively
  unauthenticated; deployment guide covers VLAN/firewall/VPN isolation.

[0.3.0]: https://github.com/HarshBhardwaj/foxess-local/releases/tag/v0.3.0
[0.2.0]: https://github.com/HarshBhardwaj/foxess-local/releases/tag/v0.2.0
[0.1.0]: https://github.com/HarshBhardwaj/foxess-local/releases/tag/v0.1.0

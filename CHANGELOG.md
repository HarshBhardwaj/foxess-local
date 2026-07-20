# Changelog

All notable changes to this project are documented here (Keep a Changelog).

## [0.1.0] - 2026-07-20

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

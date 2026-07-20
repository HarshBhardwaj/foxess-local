# FoxESS Local — Documentation Index

The complete documentation set for the local FoxESS Smart WiLAN SDK.

| # | Document | What it covers |
|---|----------|----------------|
| — | [README](../README.md) | Project overview, install, quick start, API examples |
| 01 | [Technical Discovery Report](01-technical-discovery-report.md) | Protocol reverse-engineering: endpoints, envelope, framing, CRC, model taxonomy, error codes |
| 02 | [Frontend Decoder & Register Map](02-frontend-decoder-and-register-map.md) | The 54-model register map extracted from firmware; decode type system, scale factors, enums |
| 03 | [SDK Core README](03-sdk-core-readme.md) | The SDK surface: sync/async clients, high-level API, REST, WebSocket, MQTT, CLI |
| 04 | [MQTT & Home Assistant](04-mqtt-homeassistant.md) | MQTT topics, Home Assistant discovery, sensor catalogue |
| 05 | [Write Path & Endpoints](05-write-path.md) | The `modbus_rw` write protocol, full endpoint inventory, safety model, confirmed write round-trip |
| 06 | [Deployment & Security](06-deployment-and-security.md) | Security model (unauthenticated APIs), network isolation, observability |
| 07 | [Verification Status](07-verification-status.md) | Hardware-in-the-loop decoder verification (98.8% exact vs the device's own decoder) |
| 08 | [Docker Deployment](08-docker-deployment.md) | Running the container stack, `.env` variables, profiles, troubleshooting |
| — | [CONTRIBUTING](../CONTRIBUTING.md) · [CHANGELOG](../CHANGELOG.md) · [RELEASE](../RELEASE.md) | Contribution, changelog, release checklist |

## Machine-readable data
- `data/fox_model_defs.json` — the verified 54-model register map (the SDK's source of truth)
- `fixtures/` — captured device sweeps and verification pairs used by the test suite

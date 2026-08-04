# Deployment & Security Guide

## Docker

The image bundles the REST API, `/metrics`, and the WebSocket endpoint. Optional
MQTT and Prometheus/Grafana services are behind compose profiles.

```bash
cd docker
cp .env.example .env   # then set FOX_HOST=<your-device-ip>
docker compose up -d                     # REST API on :8080
docker compose --profile full up -d      # + mosquitto, prometheus, grafana, mqtt bridge
```

Endpoints once up: `http://localhost:8080/api/v1/health`, `/api/v1/battery`,
`/metrics`, `ws://localhost:8080/api/v1/ws`. Prometheus scrapes the exporter at
`foxess-local:8080/metrics`; Grafana is on `:3000` (login `admin` /
`${GRAFANA_PASSWORD}`).

### Grafana dashboard

A pre-built dashboard (`docker/grafana/dashboards/foxess.json`) is
auto-provisioned along with the Prometheus datasource. It shows a live power-flow
row (SoC gauge, battery/solar/grid/load stats), a combined power timeseries,
battery voltage/current/temperature/SoC, grid frequency/voltage, lifetime PV
energy, and health panels (poll errors, decoder errors, scrape duration). Import
the JSON manually into any existing Grafana if you are not using the compose
stack.

Image properties (per the requirements): multi-stage build, non-root user
(`uid 10001`), `read_only` root filesystem, `no-new-privileges`, all Linux
capabilities dropped, container HEALTHCHECK on `/api/v1/health`, graceful
termination (`stop_grace_period`), and environment-variable configuration
(`FOX_HOST`, `FOX_CORS_ORIGINS`, `PORT`). No writable volume is required.

Run a single integration instead of the API:

```bash
export FOX_HOST=<your-device-ip>
docker run --rm -e FOX_HOST="$FOX_HOST" foxess-local:0.4.0 \
  fox exporter "$FOX_HOST" --port 9110
```

`FOX_HOST` is required for the REST API entrypoint; CLI commands (`fox exporter`,
`fox mqtt`, …) take the device IP as an explicit argument.

## Security model (read this)

The FoxESS WiLAN device is an IoT appliance with **weak local security**:

- The **read API is unauthenticated** (only a `fox_energy_username` cookie).
- The **write API (`modbus_rw`) is also unauthenticated** — anyone who can reach
  the device on the network can change inverter, grid-protection, and EMS
  parameters (see `docs/05-write-path.md`).

Recommended controls:

- **Dedicated IoT VLAN** for the device; no lateral access from general LAN.
- **Static DHCP reservation** so the IP is stable for firewall rules.
- **Firewall**: allow only the host running `foxess-local` to reach the device's
  port 80; deny everything else, especially inbound from untrusted networks.
- **Never expose port 80 to the internet.** For remote access use a **VPN**, or a
  reverse proxy that adds authentication and TLS in front of this SDK's REST API
  (which is read-only by default).
- Keep `allow_writes=False` (the default) unless you specifically need writes,
  and gate the process on a trusted network segment.
- The REST API is read-only; it never exposes `write_field`. If you build a
  write-capable service, put authentication in front of it.

## Observability

- `/metrics` exposes device gauges plus `fox_up`, poll success/error counters,
  `fox_last_success_timestamp_seconds`, `fox_scrape_duration_seconds`, and
  `fox_decoder_errors_total` — alert on `fox_up == 0` or a stale last-success.
- Structured logs: set `FOXESS_LOG_LEVEL` / configure the `foxess` and
  `foxess.write` loggers. Every write attempt is logged with the exact frame.

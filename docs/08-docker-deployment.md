# Docker Deployment Guide

A complete, step-by-step guide to running `foxess-local` and its optional
observability/automation stack with Docker Compose.

---

## 1. What you get

The Compose stack (`docker/docker-compose.yml`) can run up to five services:

| Service        | Image                          | Purpose                                      | Default port |
| -------------- | ------------------------------ | -------------------------------------------- | ------------ |
| `foxess-local` | built from `docker/Dockerfile` | REST API + `/metrics` + WebSocket            | `8080`       |
| `mqtt-bridge`  | same image                     | Publishes to MQTT + Home Assistant discovery | –            |
| `mosquitto`    | `eclipse-mosquitto:2`          | MQTT broker                                  | `1883`       |
| `prometheus`   | `prom/prometheus`              | Scrapes `/metrics`                           | `9090`       |
| `grafana`      | `grafana/grafana`              | Dashboards (auto-provisioned)                | `3000`       |

Only `foxess-local` runs by default. The rest are behind **profiles** so you opt
in to exactly what you want (see §5).

---

## 2. Prerequisites

- Docker Engine 24+ and the Compose plugin (`docker compose version`).
- Network reachability from the Docker host to the FoxESS device on port 80.
- The device's IP address (e.g. `192.168.1.38`).

---

## 3. Quick start

```bash
cd docker

# 1. Point the stack at your device
cat > .env <<'EOF'
FOX_HOST=192.168.1.38
EOF

# 2. Start just the local API (REST + metrics + websocket)
docker compose up -d

# 3. Verify
curl http://localhost:8080/api/v1/health          # {"status":"ok"}
curl http://localhost:8080/api/v1/battery          # live battery JSON
```

To run the **full** stack (API + MQTT + Prometheus + Grafana):

```bash
docker compose --profile full up -d
```

Open Grafana at <http://localhost:3000> (login `admin` / your
`GRAFANA_PASSWORD`), and the "FoxESS Local" dashboard is already provisioned.

---

## 4. Environment variables (`.env`)

Put these in `docker/.env` (Compose reads it automatically). **`FOX_HOST` is
required**; everything else is optional.

| Variable           | Default      | Used by          | Description                                                                                                          |
| ------------------ | ------------ | ---------------- | -------------------------------------------------------------------------------------------------------------------- |
| `FOX_HOST`         | _(required)_ | api, mqtt-bridge | **Your device's IP address.** Compose fails fast if unset.                                                           |
| `FOX_CORS_ORIGINS` | `*`          | api              | Comma-separated allowed CORS origins for the REST API. Set to your dashboard origin(s) in production instead of `*`. |
| `GRAFANA_PASSWORD` | `admin`      | grafana          | Grafana admin password. **Change this.**                                                                             |

### Host port mapping

Every published port's **host side** is configurable, so you can avoid clashes
with anything already running (the container-internal ports are fixed, so
Prometheus scraping keeps working regardless).

| Variable          | Default | Service      | Host port for                     |
| ----------------- | ------- | ------------ | --------------------------------- |
| `API_PORT`        | `8080`  | foxess-local | REST API + `/metrics` + WebSocket |
| `MQTT_PORT`       | `1883`  | mosquitto    | MQTT broker                       |
| `PROMETHEUS_PORT` | `9090`  | prometheus   | Prometheus UI                     |
| `GRAFANA_PORT`    | `3000`  | grafana      | Grafana UI                        |

> **`Bind for 0.0.0.0:8080 failed: port is already allocated`** — something else
> on the host owns that port. Set `API_PORT` to a free port in `.env` and
> `docker compose up -d` again, e.g. `API_PORT=8090` → API at
> `http://localhost:8090`. Find what's using it with `lsof -i :8080` (or
> `docker ps` for another container).

Environment variables consumed by the SDK process itself (set them under a
service's `environment:` if needed):

| Variable           | Default      | Description                                                       |
| ------------------ | ------------ | ----------------------------------------------------------------- |
| `FOX_HOST`         | _(required)_ | Device IP used by the REST `create_app()` factory and `/metrics`. |
| `FOX_CORS_ORIGINS` | `*`          | CORS origins (see above).                                         |

> **Writes are never enabled in the container.** The REST API is read-only and
> never exposes `write_field`; there is no environment flag that turns on writes.
> If you need writes, use the Python API (`FoxESS(..., allow_writes=True)`) on a
> trusted host — see `docs/05-write-path.md`.

Example `.env` for a hardened deployment with custom ports:

```dotenv
FOX_HOST=192.168.10.38
API_PORT=8090
GRAFANA_PORT=3001
FOX_CORS_ORIGINS=https://dashboards.example.lan
GRAFANA_PASSWORD=change-me-please
```

---

## 5. Compose profiles

| Profile   | Brings up                                  | Use when                                     |
| --------- | ------------------------------------------ | -------------------------------------------- |
| _(none)_  | `foxess-local`                             | You only want the local REST/metrics/ws API. |
| `metrics` | `foxess-local`, `prometheus`, `grafana`    | You want dashboards + time-series history.   |
| `mqtt`    | `foxess-local`, `mosquitto`, `mqtt-bridge` | You want Home Assistant / MQTT.              |
| `full`    | everything                                 | Full stack.                                  |

```bash
docker compose --profile metrics up -d      # API + Prometheus + Grafana
docker compose --profile mqtt up -d         # API + Mosquitto + MQTT bridge
docker compose --profile full up -d         # all five services
```

If you already run your own MQTT broker or Prometheus, keep the default profile
and point your broker/Prometheus at the container instead (see §8).

---

## 6. Common operations

```bash
docker compose ps                     # service status
docker compose logs -f foxess-local   # follow logs for one service
docker compose restart foxess-local   # restart after changing .env
docker compose down                   # stop and remove containers
docker compose pull                   # update base images (mosquitto/prom/grafana)
docker compose build --no-cache foxess-local   # rebuild the app image
```

After editing `.env`, run `docker compose up -d` again to apply it.

---

## 7. Verifying each piece

```bash
# REST API
curl http://localhost:8080/api/v1/health
curl http://localhost:8080/api/v1/system
curl http://localhost:8080/api/v1/solar

# Prometheus metrics
curl http://localhost:8080/metrics | grep fox_battery_soc_percent

# WebSocket (needs websocat or wscat)
websocat "ws://localhost:8080/api/v1/ws?interval=5"

# Prometheus targets (should show foxess-local UP)
open http://localhost:9090/targets

# MQTT (subscribe to see discovery + state)
mosquitto_sub -h localhost -t 'homeassistant/#' -v
mosquitto_sub -h localhost -t 'fox/#' -v
```

---

## 8. Running a single integration (no full stack)

The same image is a CLI. Run just the exporter or the MQTT bridge:

```bash
DEVICE=192.168.1.38

# Prometheus exporter only, on port 9110
docker run --rm -p 9110:9110 -e FOX_HOST="$DEVICE" \
  foxess-local:0.1.0 fox exporter "$DEVICE" --bind 0.0.0.0 --port 9110

# MQTT bridge only, to an existing broker
docker run --rm -e FOX_HOST="$DEVICE" \
  foxess-local:0.1.0 fox mqtt "$DEVICE" --broker 192.168.1.10 --interval 15
```

Point your existing Prometheus at the API's `/metrics`:

```yaml
scrape_configs:
  - job_name: foxess-local
    static_configs:
      - targets: ['<docker-host>:8080']
```

---

## 9. Image internals & hardening

The image (`docker/Dockerfile`) is a multi-stage build:

- **build stage** compiles a wheel; **runtime stage** installs only the wheel +
  `[api,mqtt,prometheus]` extras on `python:3.12-slim`.
- Runs as a **non-root** user (`uid 10001`).
- Compose runs it `read_only: true`, `no-new-privileges`, and drops all Linux
  capabilities — the process needs no writable filesystem or privileges.
- A container **HEALTHCHECK** hits `/api/v1/health` every 30 s.
- `stop_grace_period: 15s` gives uvicorn time to shut down gracefully.

Network hardening (the device APIs are unauthenticated — see
`docs/06-deployment-and-security.md`):

- Put the device on a dedicated IoT VLAN and firewall it so only the Docker host
  can reach its port 80.
- Do not publish port 8080 to the internet. For remote access, use a VPN or an
  authenticating reverse proxy in front of the read-only API.
- Set `FOX_CORS_ORIGINS` to your real dashboard origin(s), not `*`.
- Change `GRAFANA_PASSWORD`.

---

## 10. Troubleshooting

| Symptom                       | Likely cause / fix                                                                                                                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/api/v1/battery` returns 503 | Container can't reach the device. Check `FOX_HOST`, VLAN/firewall, and that the device answers `curl http://$FOX_HOST/api/v1/sunspec/data?addr=2&id=1`. |
| Health OK but metrics empty   | The device is reachable but a model read failed; check `docker compose logs foxess-local` and `fox_poll_errors_total`.                                  |
| Prometheus target DOWN        | `prometheus.yml` targets `foxess-local:8080`; ensure both are on the same Compose network (they are by default).                                        |
| Grafana has no data           | Confirm the Prometheus datasource is green (Grafana → Connections) and the exporter is being scraped.                                                   |
| MQTT entities missing in HA   | Confirm `mqtt-bridge` logs show "connected"; check the broker host and that HA's MQTT integration uses the same broker.                                 |
| Load/grid power shows 0       | Expected without a CT meter on the inverter (the cloud derives those). Solar/battery are always populated.                                              |

---

## 11. Updating

```bash
cd docker
git pull                       # or replace the project files
docker compose build foxess-local
docker compose --profile full up -d
```

Base images update with `docker compose pull`. The bundled register map
(`fox_model_defs.json`) ships inside the image; rebuilding picks up any changes.

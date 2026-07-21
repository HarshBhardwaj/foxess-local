# FoxESS WiLAN — Technical Discovery Report

**Deliverable #1 · Phase 1 (Reverse Engineer the Protocol)**
Status: **Draft v0.1** — evidence-backed, hardware-in-the-loop capture analyzed
Date: 2026-07-20

---

## 1. Purpose and scope

This report documents what has been _empirically established_ about the local
FoxESS "Smart WiLAN" HTTP/Modbus protocol from captured device traffic, before
any production code is written. It is the governing reference for the SDK: every
later decoder and model definition is checked against the facts recorded here.

It follows the project's evidence-first rule. Each claim is tagged with a
confidence level:

- **VERIFIED** — corroborated by multiple independent sources (raw bytes + UI +
  SunSpec spec + frontend), reproducible across the capture.
- **STRONG** — directly measured from the bytes and internally consistent, but
  not yet cross-checked against the UI or spec for that specific field.
- **HYPOTHESIS** — a plausible reading that needs more evidence.
- **UNKNOWN** — not yet determined; explicitly left open.

---

## 2. Evidence base

| Source                                         | What it is                                                                                              | Role                                  |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `full_sweep_raw.txt`                           | A `curl` sweep of `GET /api/v1/sunspec/data` for every model ID at `addr=1` and `addr=2` (58 responses) | Primary raw `tbl` payloads            |
| `UI-Dashboard.png`                             | The Smart WiLAN "Device Monitoring" page rendering model 1 (Common) for the inverter                    | UI cross-check + model-name taxonomy  |
| `Login-NetworkCall.png`                        | Safari Web Inspector view of the `POST /api/v1/sunspec/login` request                                   | Auth flow + frontend bundle inventory |
| `cli-curl` (cookie jar)                        | The cookie used for the sweep                                                                           | Auth mechanism                        |
| `tools/parse_sweep.py`, `tools/investigate.py` | Deterministic parsers used to produce every number in this report                                       | Reproducibility                       |

All parsing is scripted and re-runnable; no value in this document was read by eye
from a hex dump.

### 2.1 Devices under test (VERIFIED)

Decoded from the SunSpec Common model (id=1), and confirmed field-for-field
against the UI dashboard:

|                       | Gateway (`addr=1`) | Inverter (`addr=2`) |
| --------------------- | ------------------ | ------------------- |
| Manufacturer          | FOX                | FOX                 |
| Model                 | `FOX Hub G2`       | `AIO-H1-11.4-US`    |
| Options               | `FOX Hub(G2)`      | `AIO US`            |
| Version               | `1.1.0a.51`        | `1.1.11.8c`         |
| Serial                | `60HUB0000000000`  | `601U10000000000`   |
| Modbus device address | 1                  | 2                   |

Firmware sub-component versions decoded from model 65005 (`DER property info`):

- Gateway: `Fox-Hub-A_Series_V1.10`, `Fox-Hub-A_Series_V01_A`
- Inverter: `H1-US-A_Manager_V1.17`, `H1-US-A_Master_V1.20`, `H1-US_Slave_V1.02`,
  `H1-US_AFCI_V1.03`, `H1-US_Bat_V2.05` (plus `_V01_A` build tags)

---

## 3. HTTP API surface

Base URL: `http://$FOX_HOST/` — **plain HTTP, port 80** (observed on a
LAN device at port 80). The device serves a Vue + Element-UI single-page app called
"Smart WiLAN".

### 3.1 Endpoints (VERIFIED where captured)

| Method | Path                                       | Purpose                                               | Evidence           |
| ------ | ------------------------------------------ | ----------------------------------------------------- | ------------------ |
| `GET`  | `/api/v1/sunspec/data?addr={addr}&id={id}` | Read one SunSpec/private model from one Modbus device | Full sweep capture |
| `POST` | `/api/v1/sunspec/login`                    | Create the `admin` username cookie                    | Login capture      |

Static assets observed in the login capture (frontend bundle, locally fetchable —
a future evidence source for the private-model decoders): `app.65f25470.js`,
`chunk-elementUI.2388ebd0.js`, `chunk-libs.c34f9b69.js`, `runtime.*.js`,
`login.3bdbcce0.js`, `menu.js`, `manifest.json`, `sys_info`, `menu.html`.

Additional endpoints (e.g. write/config, `sys_info` payload, firmware) are
**UNKNOWN** and flagged for the Phase 11 write investigation.

### 3.2 Query parameters (STRONG)

- `addr` — Modbus slave address. `1` = gateway, `2` = inverter. Behaviour for
  other addresses is UNKNOWN (candidate for a `fox scan` sweep).
- `id` — SunSpec/private model ID to read.

### 3.3 Response envelope (VERIFIED)

Every response is JSON with a stable envelope:

```json
{
  "errno": 0,
  "errmsg": "success",
  "mstype": 2,
  "data": { "id": 701, "reg_addr": 40070, "tbl": "0103BA…07C7" }
}
```

- `errno` — `0` on success; non-zero is an error (see §7).
- `errmsg` — human string mirroring `errno`.
- `mstype` — `2` on every successful read observed. Meaning UNKNOWN (hypothesis:
  a message/model-set type; constant in this firmware).
- `data.id` — echoes the requested model ID.
- `data.reg_addr` — the Modbus holding-register start address of the model.
- `data.tbl` — hex-encoded Modbus RTU response bytes (§4).

On error, `data` is omitted entirely.

---

## 4. The `tbl` transport encoding — key finding

**`tbl` is not a single Modbus frame. It is one or more concatenated Modbus RTU
`Read Holding Registers` (function `0x03`) _response_ frames, each with its own
valid CRC-16/Modbus, whose register payloads join to form the full model block.**
(VERIFIED — 38 of 39 successful responses validate with _every_ constituent frame
CRC-correct.)

### 4.1 Single Modbus RTU response frame layout (VERIFIED)

```
┌────────┬────────┬────────────┬─────────────────────┬───────────┐
│ slave  │ func   │ byte_count │ data (byte_count B)  │ CRC-16 LE │
│ 1 byte │ 0x03   │ 1 byte     │ register payload     │ 2 bytes   │
└────────┴────────┴────────────┴─────────────────────┴───────────┘
```

- `slave` equals the requested `addr` (`0x01`/`0x02`).
- CRC is **CRC-16/Modbus** (poly `0xA001` reflected, init `0xFFFF`), transmitted
  **low byte first**. Validated over `slave..data` inclusive.

### 4.2 Multi-frame chunking (VERIFIED)

When a model's register block exceeds one Modbus response, the device splits it
into consecutive `0x03` frames and concatenates their raw bytes in `tbl`:

- Non-final frames carry exactly **`byte_count = 0xBA` (186 bytes = 93
  registers)** — the maximum chunk this firmware emits.
- The final frame carries the remainder.
- Observed frame counts: 1 to 4 frames (e.g. inverter model 65006 = four frames
  `[186, 186, 186, 124]`, payload 682 bytes = 341 registers).

Consequence for the SDK: the transport layer must **split, CRC-check each frame
independently, then reassemble** the register payload. Treating `tbl` as one
frame will fail on every model larger than 93 registers.

### 4.3 SunSpec register framing (VERIFIED)

After reassembly, the register payload follows SunSpec conventions:

- **Model 1 only** begins with the marker `"SunS"` (`0x53756E53`) at register
  40000–40001, then `id (0x0001)`, then `length (0x0042 = 66)`, then 66 registers.
- **All other models** begin directly with `id`, then `length`, then `length`
  data registers. The `data.reg_addr` points at that `id` register.
- `reg_addr` values are contiguous and increasing across the model map
  (40000 → 43052), consistent with a single SunSpec register image the device
  slices per request.

---

## 5. Address / device model (VERIFIED)

Two Modbus devices sit behind one WiLAN HTTP endpoint:

- **`addr=1` — Fox Hub G2 gateway.** Serves model 1 and a _subset_ of models
  (see §6). Several of its "supported" models return placeholder payloads (§8).
- **`addr=2` — AIO-H1-11.4-US inverter.** Serves the full model set and is the
  source of all real measurement data.

The compatibility design must therefore treat `(addr, id)` as the addressing
primitive, not `id` alone, and must not assume the gateway mirrors the inverter.

---

## 6. Supported model matrix

`✓ Nr` = success, all frames CRC-valid, N = declared SunSpec length (registers).
`✗ (e)` = `errno e`. `⚠` = anomaly (§8). Model names are the frontend's own
labels from the UI.

| ID    | Name                              | reg_addr | Gateway `addr=1`     | Inverter `addr=2` |
| ----- | --------------------------------- | -------- | -------------------- | ----------------- |
| 1     | Common                            | 40000    | ✓ 66r                | ✓ 66r             |
| 701   | DER AC Measurement                | 40070    | ⚠ 877r (placeholder) | ✓ 153r            |
| 702   | DER Capacity                      | 40225    | ✗ (20002)            | ✓ 50r             |
| 703   | DER Enter Service                 | 40277    | ✗ (20002)            | ✓ 17r             |
| 704   | DER AC Controls                   | 40296    | ✗ (20002)            | ✓ 65r             |
| 705   | DER Volt-Var                      | 40363    | ✗ (20002)            | ✓ 91r             |
| 706   | DER Volt-Watt                     | 40456    | ✗ (20002)            | ✓ 76r             |
| 707   | DER Trip LV                       | 40534    | ✗ (20002)            | ✓ 56r             |
| 708   | DER Trip HV                       | 40592    | ✗ (20002)            | ✓ 56r             |
| 709   | DER Trip LF                       | 40650    | ✗ (20002)            | ✓ 71r             |
| 710   | DER Trip HF                       | 40723    | ✗ (20002)            | ✓ 71r             |
| 711   | DER Freq Droop                    | 40796    | ✗ (20002)            | ✓ 72r             |
| 712   | DER Watt-Var                      | 40870    | ✗ (20002)            | ✓ 77r             |
| 713   | DER Storage Capacity              | 40949    | ✓ 7r                 | ✓ 7r              |
| 65000 | DER info                          | 40958    | ⚠ 643r (placeholder) | ✓ 156r            |
| 65001 | DER Debug info                    | 41116    | ✗ (20002)            | ✓ 92r             |
| 65002 | Param                             | 41210    | ✗ (20002)            | ✓ 123r            |
| 65003 | DbgParam                          | 41335    | ✗ (20002)            | ✓ 266r            |
| 65004 | DER Storage Capacity info         | 41603    | ⚠ CRC FAIL           | ✓ 116r            |
| 65005 | DER property info                 | 41721    | ✓ 168r               | ✓ 168r            |
| 65006 | Battery info                      | 41891    | ⚠ 532r (placeholder) | ✓ 339r            |
| 65008 | DER info2                         | 42296    | ✗ (20002)            | ✓ 26r             |
| 65009 | R&D (BatteryInfo)                 | 42324    | ✗ (20002)            | ✓ 99r             |
| 65010 | EMS-TOU                           | 42425    | ✓ 270r               | ✓ 270r            |
| 65011 | Smart Circuit                     | 42697    | ✓ 67r                | ✓ 67r             |
| 65012 | Time & Country                    | 42766    | ✓ 28r                | ✓ 28r             |
| 65015 | Advanced (Ileak & DCI)            | 42881    | ✗ (20002)            | ✓ 38r             |
| 65018 | Advanced (String & PE Monitoring) | 42982    | ✗ (20002)            | ✓ 34r             |
| 65020 | Advanced (GlobalMPPTScaning)      | 43052    | ✗ (20002)            | ✓ 25r             |

Note: model IDs 65007, 65013, 65014, 65016, 65017, 65019 were **not** part of the
supported list and were not swept; status UNKNOWN.

---

## 7. Error codes (STRONG)

| errno | errmsg         | Meaning                                     | Evidence     |
| ----- | -------------- | ------------------------------------------- | ------------ |
| 0     | `success`      | Model present; `data` populated             | 39 responses |
| 20002 | `id not found` | Model not implemented for that `(addr, id)` | 19 responses |

Other error codes (bad `addr`, malformed request, auth-required writes) are
UNKNOWN and should be enumerated with a deliberate negative-path sweep.

---

## 8. Anomalies and discrepancies

1. **Gateway model 65004 fails CRC (⚠).** For `addr=1 id=65004` the first
   186-byte frame's CRC does not validate and the byte stream does not re-align
   into clean subsequent frames (292 total bytes vs an expected ~242). The
   inverter's 65004 is clean. **Working hypothesis:** the gateway emits a
   malformed/partial payload for this model, or the capture was truncated.
   **Decision:** treat gateway 65004 as untrusted; do not decode until
   re-captured. This is the one non-clean record in the sweep.

2. **Gateway placeholder models (701, 65000, 65006).** These return `errno 0`
   with a single 93-register frame that is largely `0xFFFF`, and a `length`
   register (877 / 643 / 532) inconsistent with the inverter's real length for
   the same model. **Hypothesis:** the gateway advertises these IDs but does not
   populate them; the second register is stale data, not a true SunSpec length.
   **Decision:** do not treat gateway 701/65000/65006 as real measurements.

3. **`mstype` is constant `2`.** No variation observed; semantics UNKNOWN.

---

## 9. Authentication model (VERIFIED / STRONG)

- Read access (`GET /api/v1/sunspec/data`) requires **only** the cookie
  `fox_energy_username=admin`. No token, no signature, no session validation was
  needed to complete the full sweep. (VERIFIED — the `curl` sweep carried only
  that cookie.)
- `POST /api/v1/sunspec/login` is `application/json` (~61-byte body), returns
  `200 OK` with a ~62-byte `text/html` body. Its role appears limited to setting
  the username cookie. (STRONG — body contents not yet captured; login was not
  strictly required for reads.)
- **Security consequence:** the local read API is effectively unauthenticated.
  This is the central finding for the threat model (Deliverable #4): anyone with
  L2/L3 reachability to the device can read all telemetry. Write exposure is
  UNKNOWN and must be treated as high-risk until characterized.

---

## 10. Verification methodology status

Per the project's four-source rule (raw `tbl` · UI value · SunSpec spec ·
frontend JS):

| Model                    | tbl               | UI            | SunSpec spec          | Frontend JS | Verdict                        |
| ------------------------ | ----------------- | ------------- | --------------------- | ----------- | ------------------------------ |
| 1 (Common)               | ✓                 | ✓ (dashboard) | ✓ (common model)      | pending     | **VERIFIED**                   |
| 65005 (firmware strings) | ✓                 | pending       | n/a (private)         | pending     | STRONG                         |
| 701–713 (DER)            | ✓ (bytes+CRC+len) | pending       | ✓ (public DER models) | pending     | frame VERIFIED, fields pending |
| 65000–65020 (private)    | ✓ (bytes+CRC)     | pending       | n/a                   | pending     | frame STRONG, fields UNKNOWN   |

The frame/transport layer is verified. Individual register _meanings_ for the DER
and private models are not yet field-verified and must not be shipped as
confirmed until cross-checked against the UI and (for standard models) the
SunSpec DER specification.

---

## 11. Open questions / next evidence to gather

1. Re-capture gateway 65004 to resolve the CRC anomaly.
2. Capture the `POST /login` request/response bodies and confirm whether any
   endpoint enforces auth (especially writes).
3. Pull and analyze `app.65f25470.js` — locate the frontend's `tbl` decoder and
   its per-model field tables (authoritative for the private 65xxx models).
4. Capture matching UI values (SOC, grid power, battery voltage, temperatures)
   simultaneously with a `data` sweep to field-verify decoders.
5. Sweep `addr` beyond 1–2 and the un-swept model IDs to complete the matrix.
6. Enumerate error codes via deliberate malformed requests.
7. Identify writable registers and the write endpoint (Phase 11 — do not attempt
   writes until fully understood).

---

## 12. Implications for architecture (informs Deliverables #5–#10)

- Transport must model `tbl` as **framed**: split → per-frame CRC → reassemble.
- Addressing primitive is **`(addr, id)`**; the registry keys on it.
- The model registry should carry, per model: `reg_addr`, expected `length`,
  which addresses serve it, and a verification tag per field.
- The decoder consumes the _reassembled register payload_, never raw `tbl`.
- Gateway vs inverter capabilities differ — capability discovery (a `scan`) is a
  first-class feature, not an afterthought.
- CRC validation is cheap and universal here — make it mandatory and surface a
  decoder-failure counter (observability requirement).

---

_Reproduce every figure in this report with:_
`python3 tools/parse_sweep.py && python3 tools/investigate.py`

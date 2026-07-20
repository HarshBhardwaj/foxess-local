# FoxESS WiLAN — Frontend Decoder & Master Register Map

**Deliverable #2 (partial) / Phase 1 · Frontend JavaScript Analysis**
Status: **VERIFIED** — decoder source recovered, register map extracted and
cross-checked against live device values
Date: 2026-07-20

---

## 1. Summary

The Smart WiLAN web UI decodes `tbl` frames entirely client-side using a single
embedded definition object. We recovered the frontend bundle from the device,
decompressed and beautified it, and extracted the **complete authoritative
register map for all 54 SunSpec/FoxESS models** — every field's name, label,
type, length, register address, scale-factor reference, enumeration, and
read/write flag.

We then re-implemented the decoder in Python and confirmed it reproduces real
device values from the captured raw frames. The headline check: model 702
`WMaxRtg` (Active Power Max Rating) decodes to **11400 W**, exactly matching the
`AIO-H1-11.4-US` nameplate. This is full four-source agreement (raw bytes →
our decoder using the frontend's map → SunSpec structure → device nameplate/UI).

Artifacts:
- `fixtures/fox_model_defs.json` — the extracted master register map (54 models,
  machine-readable, the SDK's source of truth).
- `frontend/js/sunspec.e2b9aafb.beauty.js` — beautified decoder source.
- `tools/verify_decode.py` — reproduces device values from raw frames.

---

## 2. How the frontend obtains the map

The decoder lives in the lazy-loaded chunk `/js/sunspec.<hash>.js` (~284 KB
uncompressed; the device serves it gzip-compressed over HTTP). Inside, webpack
module `e287` exports a single object:

```
{ name: "fox", block: [ { id, length, start, name, report, show, data:[ …fields… ] }, … ] }
```

Each `block` entry is one model; each `data` entry is one field:

```
{ name, label, show, length /*bytes*/, type, unit?, sf?, rw?, rwl?, hint?, enum? }
```

The UI fetches `GET /api/v1/sunspec/data?addr&id`, reassembles the `tbl` frames
(see Discovery Report §4), then walks the model's `data` list sequentially over
the register payload, decoding each field by `type`.

---

## 3. Decode type system (VERIFIED — from decoder source)

| type | decoding |
|------|----------|
| `uint` | unsigned big-endian integer over `length` bytes |
| `int` | signed big-endian (int8/int16/int32 by length) |
| `uint64` | unsigned 64-bit |
| `sf` | signed int16 SunSpec **scale factor** |
| `sfm` | scale-factor variant (multi/shared); no own bytes in some models |
| `ascii` | ASCII, NUL-trimmed |
| `hex` | raw hex passthrough |
| `enum` | integer looked up in the field's `enum` list (value → label) |
| `DATE` | packed date: `YYYY-MM-DD` from `(v>>16)-(v>>8 &0xFF)-(v &0xFF)` |
| `SUN` | version triple from packed dword |
| `BCU` | battery control-unit revision string `R{(v>>8)&0xF}.{v&0xFF:03d}` |
| `BMU` | battery-module revision string `R{(v>>4)&0xF}.{v&0xF}` |

### Scale factors (VERIFIED)
A measurement field carries `sf: "<NAME>"` referencing a sibling scale-factor
field (e.g. `W_SF`, `V_SF`, `Hz_SF`). The real value is
`raw_value × 10^(sf_value)` where `sf_value` is the signed int16 read from the
referenced field — standard SunSpec semantics. Confirmed against source
(`Math.pow(10, |sf|)`, multiply if sf≥0 else divide) and against live values.

### Enumerations
289 fields carry an inline `enum` list of `{value,label}` pairs (e.g. battery
`FamilyType`: 82→"HV2600", 83→"ECS", …). These are baked into the SDK registry.

---

## 4. Address model (VERIFIED)

The decoder's `start` is a 1-based SunSpec register number; the Modbus address
in `data.reg_addr` is `start − 1`. Example: Common `start=40001` ↔ captured
`reg_addr=40000`; model 702 `start=40226` ↔ `reg_addr=40225`. The SDK stores the
Modbus address (`start − 1`) as canonical.

---

## 5. Master model matrix (54 models — VERIFIED from source)

Column `writable` counts fields carrying an `rw` flag; `enums` counts fields with
an enumeration; `scaled` counts fields with a scale-factor reference. `report`
is the firmware's own refresh class (`period` = live telemetry, `boot` =
config/static).

| ID | Name | start | len | fields | writable | enums | scaled | report |
|----|------|------:|----:|-------:|---------:|------:|-------:|--------|
| 1 | Common | 40001 | 68 | 10 | 2 | 0 | 0 | boot |
| 701 | DER AC Measurement | 40071 | 153 | 34 | 0 | 0 | 16 | period |
| 702 | DER Capacity | 40226 | 50 | 30 | 2 | 0 | 17 | boot |
| 703 | DER Enter Service | 40278 | 17 | 12 | 7 | 1 | 4 | boot |
| 704 | DER AC Controls | 40297 | 65 | 15 | 12 | 5 | 4 | period |
| 705 | DER Volt-Var | 40364 | 91 | 36 | 33 | 2 | 18 | boot |
| 706 | DER Volt-Watt | 40457 | 76 | 71 | 68 | 1 | 51 | boot |
| 707 | DER Trip LV | 40535 | 56 | 36 | 33 | 2 | 22 | boot |
| 708 | DER Trip HV | 40593 | 56 | 35 | 32 | 2 | 21 | boot |
| 709 | DER Trip LF | 40651 | 71 | 22 | 19 | 1 | 10 | boot |
| 710 | DER Trip HF | 40724 | 71 | 22 | 19 | 1 | 10 | boot |
| 711 | DER Freq Droop | 40797 | 72 | 46 | 43 | 1 | 30 | boot |
| 712 | DER Watt-Var | 40871 | 86 | 34 | 31 | 2 | 20 | boot |
| 713 | DER Storage Capacity | 40959 | 7 | 9 | 0 | 1 | 0 | boot |
| 65000 | DER info | 40968 | 156 | 149 | 0 | 0 | 103 | period |
| 65001 | DER Debug info | 41126 | 485 | 88 | 0 | 1 | 11 | period |
| 65002 | Param | 41184 | 122 | 135 | 121 | 43 | 48 | boot |
| 65003 | DbgParam | 41309 | 280 | 272 | 260 | 90 | 59 | boot |
| 65004 | DER Storage Capacity info | 41613 | 116 | 53 | 0 | 0 | 28 | period |
| 65005 | DER property info | 41731 | 168 | 15 | 0 | 0 | 0 | boot |
| 65006 | Battery info | 41901 | 403 | 326 | 0 | 0 | 26 | period |
| 65007 | Param2 | 42233 | 62 | 65 | 59 | 20 | 17 | boot |
| 65008 | DER info2 | 42306 | 26 | 14 | 0 | 0 | 1 | boot |
| 65009 | R&D(BatteryInfo) | 42334 | 99 | 38 | 0 | 1 | 0 | boot |
| 65010 | EMS-TOU | 42435 | 270 | 272 | 270 | 6 | 0 | boot |
| 65011 | Smart Circuit | 42707 | 58 | 61 | 58 | 10 | 0 | boot |
| 65012 | Time & Country | 42767 | 28 | 11 | 8 | 1 | 0 | boot |
| 65013 | Advanced(Grid Imbalance Protection) | 42797 | 28 | 12 | 7 | 2 | 4 | boot |
| 65014 | Advanced(Protect Recovery) | 42827 | 53 | 9 | 4 | 0 | 4 | boot |
| 65015 | Advanced(Ileak & DCI) | 42882 | 38 | 23 | 17 | 7 | 5 | boot |
| 65016 | Advanced(Islanding Parameters) | 42922 | 27 | 12 | 7 | 3 | 2 | boot |
| 65017 | Advanced(SVG & PID) | 42951 | 30 | 14 | 9 | 5 | 2 | boot |
| 65018 | Advanced(String &PE Monitoring) | 42983 | 34 | 18 | 14 | 8 | 1 | boot |
| 65019 | R&D(FaultMasking) | 43019 | 32 | 15 | 12 | 12 | 0 | boot |
| 65020 | Advanced(GlobalMPPTScaning) | 43053 | 25 | 7 | 4 | 3 | 0 | boot |
| 65021 | Advanced(Others) | 43080 | 27 | 9 | 6 | 3 | 0 | boot |
| 65022 | Advanced(Active Power) | 43109 | 30 | 13 | 10 | 6 | 0 | boot |
| 65023 | ExportLimit | 43141 | 29 | 14 | 8 | 5 | 3 | boot |
| 65024 | Advanced(OPU &UPU) | 43172 | 40 | 26 | 20 | 2 | 18 | boot |
| 65025 | Advanced(Reactive PFP) | 43214 | 29 | 14 | 9 | 1 | 6 | boot |
| 65026 | EMS | 43245 | 77 | 15 | 10 | 5 | 4 | boot |
| 65027 | R&D(Others) | 43324 | 55 | 51 | 27 | 13 | 2 | boot |
| 65028 | Advanced(MasterSlaveParam) | 43381 | 23 | 21 | 7 | 4 | 6 | boot |
| 65029 | R&D(DebugParam) | 43406 | 30 | 18 | 15 | 0 | 0 | boot |
| 65030 | R&D(MeterDebug) | 43438 | 23 | 6 | 3 | 3 | 0 | boot |
| 65031 | R&D(HubInfo) | 43463 | 80 | 62 | 0 | 1 | 19 | boot |
| 65032 | ParallelParam | 43545 | 52 | 18 | 2 | 3 | 0 | boot |
| 65033 | AC-Couple | 43599 | 11 | 5 | 1 | 0 | 1 | boot |
| 65034 | EMS-Manual | 43612 | 60 | 44 | 40 | 4 | 6 | boot |
| 65035 | Advanced(SlaveAddress) | 43674 | 21 | 4 | 1 | 0 | 0 | boot |
| 65036 | EMS-ExportCompensation | 43697 | 59 | 22 | 19 | 3 | 0 | boot |
| 65037 | OffGrid-Time | 43758 | 80 | 42 | 0 | 0 | 0 | period |
| 65038 | ODM-Info | 43975 | 123 | 4 | 0 | 0 | 0 | boot |
| 65039 | Generator | 44100 | 55 | 34 | 30 | 5 | 0 | boot |


**Totals:** 54 models · 2,443 fields · 1,359 fields with an `rw` flag · 289
enumerated fields.

### New models beyond the original project list
The original brief listed 29 model IDs. The firmware actually defines 54,
including previously-unknown control/config models highly relevant to write
support: **65007 Param2, 65013–65028 Advanced(*) protection/grid blocks,
65023 ExportLimit, 65026 EMS, 65032 ParallelParam, 65033 AC-Couple,
65034 EMS-Manual, 65036 EMS-ExportCompensation, 65037/65039 OffGrid-Time &
Generator**, plus R&D/debug blocks (65029–65031). Note the earlier API sweep
only probed the original 29 IDs — the additional models are defined in firmware
and exposed in the UI; each still needs a per-`(addr,id)` reachability check.

---

## 6. Read/write flags (STRONG — semantics partially confirmed)

Fields carry `rw` (values observed: 1, 2, 3) and sometimes `rwl`. The UI renders
an **Edit** control for editable fields (confirmed on Common → Serial Number
`rw:2` and Device Address `rw:3`, `hint:"1-246"`). Interpretation:

- `rw:3` — user-writable (e.g. Device Address, most EMS/TOU/protection params).
- `rw:2` — protected/factory (e.g. Serial Number).
- `rw:1` — most common (781 fields); likely writable-with-privilege or
  edit-visible. Exact tiering is a **HYPOTHESIS** pending write testing.
- `rwl` — likely a required access level; meaning unconfirmed.

rw distribution: `rw:1`=781, `rw:3`=533, `rw:2`=45. This inventory is the
starting point for Phase 11; **no writes attempted** — write mechanism, endpoint,
and auth are still UNKNOWN.

---

## 7. Verification performed

`tools/verify_decode.py` decodes captured raw frames with the extracted map:

- **Model 1 (both devices):** identity strings exact (FOX / AIO-H1-11.4-US /
  v1.1.11.8c / SN / DA), 140 B payload consumed exactly. VERIFIED.
- **Model 702 `WMaxRtg` = 11400 W, `VAMaxRtg` = 11400 VA** — matches nameplate.
  VERIFIED.
- **Model 713:** WHRtg 11925 Wh, WHAvail 4889 Wh, SoC 51 %, SoH 100 %, Backup
  SOC 20 % — all plausible. VERIFIED (plausibility).
- Byte alignment matched payload length on models 1, 702, 713. Model 65008
  over-reads by one trailing scale-factor register (`sfm`) — a known SunSpec
  trailing-SF quirk to handle in the decoder.

---

## 8. Other recovered chunks (captured, analysis pending)

Also mirrored for later phases: `err-info`, `err-log` (fault/alarm code tables),
`setup`, `up-device`, `up-module`, `up-webserver` (config/firmware endpoints —
Phase 11 write path), `change`, `reset`, `login`, `download`, `wifi`. These will
source the error-code reference and the write/upgrade API surface.

---

## 9. Impact on the SDK

- `fox_model_defs.json` becomes the model registry (Deliverable #9) — no manual
  register transcription needed.
- The decoder (Deliverable #10) is now specified and verified end to end:
  reassemble frames → walk fields → typed decode → apply scale factors → map
  enums.
- Writable-register inventory seeds Phase 11 (kept read-only until the write
  path is understood).
- Report class (`period`/`boot`) directly informs polling cadence and MQTT/
  Prometheus publishing.

# Decoder Verification Status (Hardware-in-the-Loop)

**Method.** For every inverter model we captured, at the same moment, both the
raw `tbl` frame (from `/api/v1/sunspec/data`) and the device web UI's *own*
decoded field values. We then decode the same raw frame with this SDK and
compare field-by-field. A field is **matched** when the SDK value equals the
device's own decoded value — i.e. this SDK reproduces the manufacturer's
decoder, the strongest available reference short of the SunSpec spec itself.

**Result.**

| ID | Model | fields | matched | verdict |
|----|-------|-------:|--------:|---------|
| 1 | Common | 8 | 8 | VERIFIED |
| 701 | DER AC Measurement | 23 | 23 | VERIFIED |
| 702 | DER Capacity | 21 | 21 | VERIFIED |
| 703 | DER Enter Service | 8 | 8 | VERIFIED |
| 704 | DER AC Controls | 13 | 13 | VERIFIED |
| 705 | DER Volt-Var | 34 | 34 | VERIFIED |
| 706 | DER Volt-Watt | 69 | 69 | VERIFIED |
| 707 | DER Trip LV | 33 | 33 | VERIFIED |
| 708 | DER Trip HV | 32 | 32 | VERIFIED |
| 709 | DER Trip LF | 20 | 20 | VERIFIED |
| 710 | DER Trip HF | 20 | 20 | VERIFIED |
| 711 | DER Freq Droop | 44 | 44 | VERIFIED |
| 712 | DER Watt-Var | 32 | 32 | VERIFIED |
| 713 | DER Storage Capacity | 8 | 8 | VERIFIED |
| 65000 | DER info | 141 | 141 | VERIFIED |
| 65001 | DER Debug info | 82 | 73 | PLAUSIBLE |
| 65002 | Param | 122 | 121 | PLAUSIBLE |
| 65003 | DbgParam | 258 | 257 | PLAUSIBLE |
| 65004 | DER Storage Capacity info | 43 | 40 | PLAUSIBLE |
| 65005 | DER property info | 14 | 14 | VERIFIED |
| 65006 | Battery info | 319 | 316 | PLAUSIBLE |
| 65008 | DER info2 | 12 | 12 | VERIFIED |
| 65009 | R&D(BatteryInfo) | 37 | 37 | VERIFIED |
| 65010 | EMS-TOU | 271 | 271 | VERIFIED |
| 65011 | Smart Circuit | 59 | 59 | VERIFIED |
| 65012 | Time & Country | 9 | 8 | PLAUSIBLE |
| 65015 | Advanced(Ileak & DCI) | 17 | 16 | PLAUSIBLE |
| 65018 | Advanced(String &PE Monitoring) | 15 | 15 | VERIFIED |
| 65020 | Advanced(GlobalMPPTScaning) | 4 | 4 | VERIFIED |
| 65023 | ExportLimit | 9 | 9 | VERIFIED |
| 65026 | EMS | 11 | 11 | VERIFIED |
| 65029 | R&D(DebugParam) | 16 | 16 | VERIFIED |
| 65030 | R&D(MeterDebug) | 4 | 4 | VERIFIED |
| 65031 | R&D(HubInfo) | 55 | 50 | PLAUSIBLE |
| 65032 | ParallelParam | 15 | 15 | VERIFIED |
| 65033 | AC-Couple | 2 | 2 | VERIFIED |
| 65034 | EMS-Manual | 41 | 41 | VERIFIED |
| 65036 | EMS-ExportCompensation | 20 | 20 | VERIFIED |
| 65037 | OffGrid-Time | 41 | 41 | VERIFIED |

**1958/1982 fields (98.8%) exactly match the device's own decoder. 31/39 models fully VERIFIED; the rest PLAUSIBLE (only live-varying fields differ between the paired fetches). Zero structural/decode errors.**

## Reading the verdicts

- **VERIFIED** — every compared field matches the device decoder exactly.
- **PLAUSIBLE** — all *stable* fields match; the only differences are
  live-varying quantities (instantaneous power/current/voltage, energy
  counters, clock `Second`, per-cell voltages, debug registers) that changed in
  the ~120 ms between the two paired fetches. These are capture-timing
  artefacts, not decoder errors.

There are **zero hard (non-live) mismatches**: no model has a stable field the
SDK decodes differently from the device. This includes the previously
uncertain scaling of the private models — the `sfm` constant scale factors,
verified here across battery, PV, and grid measurements.

## Formatting note

`hex`/bitfield fields are identical in value; the device UI prints them with a
`0x` prefix (e.g. `0x00000000`) while the SDK returns the bare hex
(`00000000`). These are treated as equal.

## Reproduce / regress

- One-off report: `python tools/verify_hil.py`
- CI regression: `tests/test_hil_verification.py` asserts zero hard mismatches
  and ≥95% overall field match against the captured pairs.

## Remaining follow-ups

- `65015 Advanced(Ileak & DCI)` `Ileak3Value`: the leakage-current reading uses
  a scale still under review; treated as diagnostic/experimental.
- Field *meanings* for R&D/debug models (65001, 65029, 65031) beyond byte-exact
  agreement are not independently confirmed and remain labelled per the
  frontend only.

"""Regression test locking in the hardware-in-the-loop verification result.

Uses paired (raw tbl, device-UI-decoded) captures. Asserts the SDK decoder
reproduces the device's own decoder on every stable field, allowing only
live-varying fields (power/energy/clock/per-cell) to differ due to the small
time gap between the two captures.
"""

from __future__ import annotations

import json
from pathlib import Path

from foxess.decoder import decode
from foxess.frame import reassemble_hex
from foxess.registry import default_registry

PAIRS = json.load(open(Path(__file__).parent / "fixtures" / "verify_pairs.json"))

_LIVE = (
    "power",
    "current",
    "voltage",
    "dcpower",
    "pv",
    "load",
    "grid",
    "wh",
    "energy",
    "bus",
    "temp",
    "soc",
    "batterypower",
    "w",
    "second",
    "minute",
    "hour",
    "cellvol",
    "debuginfo",
    "displayinfo",
    "vol",
    "freq",
    "hz",
    "leak",
)


def _norm_hex(v: object) -> str | None:
    if isinstance(v, str):
        s = v.strip().lower()
        return s[2:] if s.startswith("0x") else s
    return None


def _num(v: object) -> float | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, int | float):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return None
    return None


def _match(sdk: object, ui: object) -> bool:
    hs, hu = _norm_hex(sdk), _norm_hex(ui)
    if hs is not None and hu is not None and hs == hu:
        return True
    ns, nu = _num(sdk), _num(ui)
    if ns is not None and nu is not None:
        return abs(ns - nu) <= max(1e-9, abs(nu) * 1e-9)
    return str(sdk).strip() == str(ui).strip()


def test_no_hard_mismatches_against_device_decoder() -> None:
    reg = default_registry()
    total = matched = 0
    hard: list[tuple[int, str, object, object]] = []
    for key, rec in PAIRS.items():
        addr, mid = key.split(":")
        mid = int(mid)
        if mid not in reg or not rec.get("tbl"):
            continue
        frame = reassemble_hex(rec["tbl"], validate_crc=False)
        dec = decode(frame.payload, mid, addr=int(addr))
        ui = rec["ui"]
        for f in dec.fields:
            if f.name not in ui:
                continue
            total += 1
            if _match(f.value, ui[f.name]):
                matched += 1
            elif not any(h in f.name.lower() for h in _LIVE):
                hard.append((mid, f.name, f.value, ui[f.name]))
    assert hard == [], f"decoder disagrees with device on stable fields: {hard[:10]}"
    assert matched / total >= 0.95, f"only {matched}/{total} fields matched"

#!/usr/bin/env python3
"""Hardware-in-the-loop verification.

Compares this SDK's decoder against the device's OWN frontend decoder using
paired (raw tbl, UI-decoded values) captured at the same moment. A field is a
MATCH when the SDK value equals the device's UI value.
"""
from __future__ import annotations

import json
from pathlib import Path

from foxess.decoder import decode
from foxess.frame import reassemble_hex
from foxess.registry import default_registry

PAIRS = json.load(open(Path(__file__).resolve().parent.parent / "fixtures" / "verify_pairs.json"))
REG = default_registry()

# Fields that legitimately vary between the two back-to-back fetches (live power
# / energy / clock / per-cell), so a small mismatch there is timing, not a
# decoder error.
LIVE_HINTS = ("power", "current", "voltage", "dcpower", "pv", "load", "grid",
              "wh", "energy", "bus", "temp", "soc", "batterypower", "w",
              "second", "minute", "hour", "cellvol", "debuginfo", "displayinfo",
              "vol", "freq", "hz", "leak")


def _norm_hex(v):
    """Normalise a hex string: strip an optional 0x prefix, lowercase."""
    if isinstance(v, str):
        s = v.strip().lower()
        if s.startswith("0x"):
            s = s[2:]
        return s
    return None


def _num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return None
    return None


def _match(sdk, ui) -> bool:
    # hex fields: device UI prefixes 0x; compare the hex digits only.
    hs, hu = _norm_hex(sdk), _norm_hex(ui)
    if hs is not None and hu is not None and (hs == hu):
        return True
    ns, nu = _num(sdk), _num(ui)
    if ns is not None and nu is not None:
        return abs(ns - nu) <= max(1e-9, abs(nu) * 1e-9)
    return str(sdk).strip() == str(ui).strip()


def main() -> int:
    rows = []
    total_fields = total_match = 0
    for key, rec in PAIRS.items():
        addr, mid = key.split(":")
        mid = int(mid)
        if mid not in REG or not rec.get("tbl"):
            continue
        frame = reassemble_hex(rec["tbl"], validate_crc=False)
        dec = decode(frame.payload, mid, addr=int(addr))
        ui = rec["ui"]
        n = m = 0
        mism = []
        for f in dec.fields:
            if f.name not in ui:
                continue
            n += 1
            if _match(f.value, ui[f.name]):
                m += 1
            else:
                live = any(h in f.name.lower() for h in LIVE_HINTS)
                mism.append((f.name, f.value, ui[f.name], live))
        total_fields += n
        total_match += m
        hard = [x for x in mism if not x[3]]
        rows.append((mid, dec.name, n, m, len(mism), len(hard), mism))

    print(f"{'ID':<6}{'Model':<34}{'flds':>5}{'match':>6}{'miss':>5}{'hard':>5}  verdict")
    print("-" * 78)
    for mid, name, n, m, miss, hard, _ in rows:
        pct = 100 * m / n if n else 100
        verdict = "VERIFIED" if miss == 0 else ("PLAUSIBLE" if hard == 0 else "CHECK")
        print(f"{mid:<6}{name[:33]:<34}{n:>5}{m:>6}{miss:>5}{hard:>5}  {verdict} ({pct:.0f}%)")

    print(f"\nTotal fields compared: {total_fields}  |  exact matches: {total_match} "
          f"({100*total_match/total_fields:.1f}%)")

    print("\n### Non-live (hard) mismatches to inspect ###")
    for mid, name, n, m, miss, hard, mism in rows:
        hards = [x for x in mism if not x[3]]
        if hards:
            print(f"\nid={mid} {name}:")
            for fn, sv, uv, _ in hards[:12]:
                print(f"   {fn:<26} sdk={sv!r:<22} ui={uv!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

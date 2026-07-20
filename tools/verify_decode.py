#!/usr/bin/env python3
"""Verify the extracted fox register map decodes raw tbl frames to correct values.

Walks each model's field list sequentially over the reassembled register payload,
decodes by type, applies SunSpec scale factors (value * 10**sf), and prints a
sample so we can eyeball against known device facts (e.g. 11.4 kW inverter).
"""
from __future__ import annotations
import json
from parse_sweep import parse_raw, RAW

defs = json.load(open("../fixtures/fox_model_defs.json"))
BLOCK = {b["id"]: b for b in defs["block"]}
records = {(r.addr, r.model_id): r for r in parse_raw(RAW.read_text())}


def decode_model(payload: bytes, model):
    """Return list of (name,label,type,value,unit,sf_ref)."""
    fields = model["data"]
    off = 0
    raw_vals = {}
    out = []
    # pass 1: decode raw
    for f in fields:
        blen = f.get("length", 0)
        chunk = payload[off: off + blen]
        off += blen
        t = f.get("type")
        val = None
        try:
            if t == "ascii":
                val = chunk.split(b"\x00")[0].decode("latin1")
            elif t == "uint":
                val = int.from_bytes(chunk, "big") if chunk else None
            elif t in ("int", "sf", "sfm"):
                val = int.from_bytes(chunk, "big", signed=True) if chunk else None
            elif t == "enum":
                val = int.from_bytes(chunk, "big") if chunk else None
            elif t == "uint64":
                val = int.from_bytes(chunk, "big") if chunk else None
            else:
                val = chunk.hex()
        except Exception as e:
            val = f"ERR:{e}"
        raw_vals[f.get("name")] = (val, t)
        out.append([f.get("name"), f.get("label"), t, val, f.get("unit"), f.get("sf")])
    # pass 2: apply scale factors
    scaled = []
    for row in out:
        name, label, t, val, unit, sfref = row
        sval = val
        if sfref and isinstance(sfref, str) and sfref in raw_vals:
            sfv = raw_vals[sfref][0]
            if isinstance(sfv, int) and isinstance(val, int):
                sval = val * (10 ** sfv)
        scaled.append([name, label, t, val, sval, unit, sfref])
    return scaled, off


def show(addr, mid, names=None):
    r = records.get((addr, mid))
    m = BLOCK.get(mid)
    if not r or not m or not r.payload:
        print(f"-- ({addr},{mid}) no data"); return
    rows, consumed = decode_model(r.payload, m)
    print(f"\n=== addr={addr} id={mid} {m['name']} | payload={len(r.payload)}B consumed={consumed}B "
          f"start={m.get('start')} ===")
    for row in rows:
        name, label, t, raw, scaled, unit, sfref = row
        if names and name not in names:
            continue
        extra = f"  x10^SF({sfref})->{scaled}" if sfref else ""
        print(f"  {name:<16}{(label or '')[:30]:<31}{t:<6} raw={raw}{extra} {unit or ''}")


# Model 1 identity (known-good)
show(2, 1)
# 702 DER Capacity: WMaxRtg should be ~11400 W for AIO-H1-11.4
show(2, 702, names={"ID","WMaxRtg","WMaxRtg_SF","VAMaxRtg","VAMaxRtg_SF","ARtg","ARtg_SF"})
# 713 storage capacity (SoC-ish)
show(2, 713)
# 65008 small model with 1 sf
show(2, 65008)

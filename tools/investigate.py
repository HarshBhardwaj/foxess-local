#!/usr/bin/env python3
"""Focused investigation: chunk sizes, the id=65004 CRC anomaly, and full
decode of the SunSpec common model (id=1) device-identity block for both
addresses (fully verifiable against UI + SunSpec spec)."""
from __future__ import annotations
import json, re
from pathlib import Path
from parse_sweep import crc16_modbus, split_frames, parse_raw, RAW

records = parse_raw(RAW.read_text())
by = {(r.addr, r.model_id): r for r in records}

print("### Chunk-size analysis (non-final frame byte counts) ###")
sizes = set()
for r in records:
    if len(r.frames) > 1:
        for f in r.frames[:-1]:
            sizes.add(f.byte_count)
        print(f"addr={r.addr} id={r.model_id}: bytecounts={[f.byte_count for f in r.frames]}")
print("Distinct non-final chunk byte counts:", sorted(sizes), "(0xBA =", 0xBA, ")")

print("\n### id=65004 addr=1 CRC anomaly ###")
r = by[(1, 65004)]
tbl = bytes.fromhex(r.tbl_hex)
print("total tbl bytes:", len(tbl))
print("first 6 bytes:", tbl[:6].hex())
# Manually walk expected frames of 0xBA
i = 0
fn = 0
while i < len(tbl):
    if i + 3 > len(tbl):
        print(f"  tail {len(tbl)-i} bytes: {tbl[i:].hex()}"); break
    slave, func, bc = tbl[i], tbl[i+1], tbl[i+2]
    end = i + 3 + bc + 2
    ok = None
    if end <= len(tbl):
        crc_rx = tbl[i+3+bc] | (tbl[i+4+bc] << 8)
        crc_calc = crc16_modbus(tbl[i:i+3+bc])
        ok = (crc_rx == crc_calc)
    print(f"  frame{fn}: off={i} slave={slave:02x} func={func:02x} bc={bc}({bc:#x}) end={end} crc_ok={ok}")
    i = end; fn += 1
    if fn > 20: break

def decode_common(payload: bytes) -> dict:
    # payload begins with 'SunS'(2 regs) + id(1) + len(1) + 66 regs
    assert payload[:4] == b"SunS"
    body = payload[8:]  # skip SunS, id, len
    def s(off, n):  # string of n registers (2n bytes)
        return body[off*2:(off+n)*2].split(b"\x00")[0].decode("latin1")
    return {
        "Mn_manufacturer": s(0, 16),
        "Md_model": s(16, 16),
        "Opt_options": s(32, 8),
        "Vr_version": s(40, 8),
        "SN_serial": s(48, 16),
        "DA_device_address": int.from_bytes(body[64*2:65*2], "big"),
    }

print("\n### SunSpec Common Model (id=1) device identity ###")
for addr in (1, 2):
    r = by[(addr, 1)]
    print(f"addr={addr}:", json.dumps(decode_common(r.payload), indent=None))

# Cross-check: model string field / firmware versions in 65005 (ascii-rich)
print("\n### id=65005 ASCII strings (firmware version block) ###")
for addr in (1, 2):
    r = by[(addr, 65005)]
    ascii_str = re.sub(rb"[^\x20-\x7e]", b" ", r.payload).decode()
    toks = [t for t in ascii_str.split() if len(t) >= 4]
    print(f"addr={addr}:", toks)

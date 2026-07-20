#!/usr/bin/env python3
"""Evidence-first parser for FoxESS WiLAN /api/v1/sunspec/data captures.

Reads the raw sweep dump, extracts (addr, id, errno, reg_addr, tbl) records,
splits each tbl into constituent Modbus RTU response frames, validates
CRC-16/Modbus on every frame, reassembles the register payload, and checks
the SunSpec (model_id, length) header.

No hardcoded protocol assumptions beyond the Modbus RTU frame format and the
CRC-16/Modbus algorithm; everything else is measured from the bytes.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "fixtures" / "full_sweep_raw.txt"


def crc16_modbus(data: bytes) -> int:
    """CRC-16/Modbus: poly 0xA001 (reflected), init 0xFFFF. Returns int."""
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


@dataclass
class Frame:
    slave: int
    func: int
    byte_count: int
    data: bytes
    crc_rx: int
    crc_calc: int
    crc_ok: bool


@dataclass
class Record:
    addr: int
    model_id: int
    errno: int
    errmsg: str
    reg_addr: int | None = None
    tbl_hex: str | None = None
    frames: list[Frame] = field(default_factory=list)
    payload: bytes = b""          # reassembled register bytes (data minus headers)
    hdr_model_id: int | None = None
    hdr_length: int | None = None
    all_crc_ok: bool | None = None
    notes: list[str] = field(default_factory=list)


def split_frames(tbl: bytes) -> list[Frame]:
    """Greedily split concatenated Modbus RTU (func 0x03) response frames.

    Each frame: slave(1) func(1) byte_count(1) data(byte_count) crc(2, LE).
    """
    frames: list[Frame] = []
    i = 0
    n = len(tbl)
    while i < n:
        if i + 3 > n:
            frames.append(Frame(-1, -1, -1, tbl[i:], -1, -1, False))
            break
        slave = tbl[i]
        func = tbl[i + 1]
        bc = tbl[i + 2]
        frame_len = 3 + bc + 2
        if i + frame_len > n:
            # not enough bytes for declared frame; record remainder as bad
            frames.append(Frame(slave, func, bc, tbl[i + 3:], -1, -1, False))
            break
        data = tbl[i + 3 : i + 3 + bc]
        crc_rx = tbl[i + 3 + bc] | (tbl[i + 4 + bc] << 8)  # little-endian
        crc_calc = crc16_modbus(tbl[i : i + 3 + bc])
        frames.append(Frame(slave, func, bc, data, crc_rx, crc_calc, crc_rx == crc_calc))
        i += frame_len
    return frames


def parse_raw(text: str) -> list[Record]:
    records: list[Record] = []
    blocks = re.split(r"^===== addr=(\d+) id=(\d+) =====\s*$", text, flags=re.M)
    # re.split with 2 groups yields: [pre, addr, id, json, addr, id, json, ...]
    it = iter(blocks[1:])
    for addr_s, id_s, body in zip(it, it, it):
        addr = int(addr_s)
        mid = int(id_s)
        try:
            obj = json.loads(body)
        except json.JSONDecodeError:
            # tolerate trailing text
            obj = json.loads(body[: body.rindex("}") + 1])
        rec = Record(addr=addr, model_id=mid, errno=obj.get("errno", -1),
                     errmsg=obj.get("errmsg", ""))
        data = obj.get("data")
        if data:
            rec.reg_addr = data.get("reg_addr")
            rec.tbl_hex = data.get("tbl")
            tbl = bytes.fromhex(rec.tbl_hex)
            rec.frames = split_frames(tbl)
            rec.all_crc_ok = all(f.crc_ok for f in rec.frames)
            rec.payload = b"".join(f.data for f in rec.frames)
            # SunSpec header: for models whose reg_addr is the id register,
            # payload starts with model_id, length. Model 1 payload starts
            # with 'SunS' marker then id, length.
            p = rec.payload
            if p[:4] == b"SunS":
                rec.hdr_model_id = int.from_bytes(p[4:6], "big")
                rec.hdr_length = int.from_bytes(p[6:8], "big")
            elif len(p) >= 4:
                rec.hdr_model_id = int.from_bytes(p[0:2], "big")
                rec.hdr_length = int.from_bytes(p[2:4], "big")
        records.append(rec)
    return records


def main() -> int:
    text = RAW.read_text()
    records = parse_raw(text)

    supported = [r for r in records if r.errno == 0]
    unsupported = [r for r in records if r.errno != 0]

    print("=" * 78)
    print("FRAME / CRC VALIDATION REPORT")
    print("=" * 78)
    bad = 0
    for r in supported:
        nframes = len(r.frames)
        crc_flags = "".join("." if f.crc_ok else "X" for f in r.frames)
        hdr_match = "OK" if r.hdr_model_id == r.model_id else f"MISMATCH(hdr={r.hdr_model_id})"
        # length sanity: expected payload registers vs declared length
        if not r.all_crc_ok:
            bad += 1
        print(f"addr={r.addr} id={r.model_id:<5} reg={r.reg_addr} "
              f"frames={nframes:<2} crc[{crc_flags}] "
              f"payload={len(r.payload):>4}B hdr_id={hdr_match} len={r.hdr_length}")
    print()
    print(f"Supported records: {len(supported)}  |  Unsupported: {len(unsupported)}")
    print(f"Records with ALL frames CRC-valid: {sum(1 for r in supported if r.all_crc_ok)}"
          f" / {len(supported)}")
    print(f"Records with a CRC failure: {bad}")
    print()
    print("Unsupported IDs (errno/errmsg):")
    from collections import defaultdict
    by_err = defaultdict(list)
    for r in unsupported:
        by_err[(r.errno, r.errmsg)].append((r.addr, r.model_id))
    for (en, em), lst in by_err.items():
        print(f"  errno={en} '{em}': {lst}")

    # Emit machine-readable inventory
    out = []
    for r in records:
        out.append({
            "addr": r.addr, "model_id": r.model_id, "errno": r.errno,
            "errmsg": r.errmsg, "reg_addr": r.reg_addr,
            "n_frames": len(r.frames),
            "frame_bytecounts": [f.byte_count for f in r.frames],
            "all_crc_ok": r.all_crc_ok,
            "payload_len_bytes": len(r.payload),
            "payload_len_regs": len(r.payload) // 2,
            "hdr_model_id": r.hdr_model_id,
            "hdr_length": r.hdr_length,
        })
    inv = Path(__file__).resolve().parent.parent / "fixtures" / "inventory.json"
    inv.write_text(json.dumps(out, indent=2))
    print(f"\nWrote inventory -> {inv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

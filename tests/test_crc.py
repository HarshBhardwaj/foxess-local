"""CRC-16/Modbus tests."""

from __future__ import annotations

from foxess.crc import crc16, crc16_bytes
from foxess.frame import split_frames


def test_known_vector() -> None:
    # Classic Modbus CRC test vector: value 0x80B8, appended low-byte-first.
    assert crc16(b"\x01\x04\x02\xff\xff") == 0x80B8
    assert crc16_bytes(b"\x01\x04\x02\xff\xff") == b"\xb8\x80"


def test_empty() -> None:
    assert crc16(b"") == 0xFFFF


def test_all_captured_frames_validate(sweep) -> None:
    """Every constituent frame of every successful capture must CRC-validate,
    except the one documented gateway anomaly (addr=1 id=65004)."""
    failures: list[tuple[int, int]] = []
    for (addr, mid), rec in sweep.items():
        if rec.errno != 0 or not rec.tbl_hex:
            continue
        if (addr, mid) == (1, 65004):
            continue  # documented framing anomaly (see test_frame)
        frames = split_frames(bytes.fromhex(rec.tbl_hex))
        if not all(f.crc_ok for f in frames):
            failures.append((addr, mid))
    assert failures == [], f"unexpected CRC failures: {failures}"

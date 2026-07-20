"""Frame split / reassemble tests."""

from __future__ import annotations

import pytest

from foxess.errors import FoxCRCError, FoxProtocolError
from foxess.frame import MAX_CHUNK_DATA_BYTES, reassemble, reassemble_hex, split_frames


def test_single_frame_model_1(sweep) -> None:
    rec = sweep[(2, 1)]
    frame = reassemble_hex(rec.tbl_hex)
    assert frame.slave == 2
    assert len(frame.frames) == 1
    assert frame.payload[:4] == b"SunS"


def test_multi_frame_reassembly(sweep) -> None:
    # Inverter Battery info (65006) arrives as four frames.
    rec = sweep[(2, 65006)]
    frame = reassemble_hex(rec.tbl_hex)
    assert len(frame.frames) == 4
    # non-final frames are the maximum chunk size
    for f in frame.frames[:-1]:
        assert f.byte_count == MAX_CHUNK_DATA_BYTES
    assert frame.payload[:2] == (65006).to_bytes(2, "big")


def test_crc_validation_raises_on_corruption(sweep) -> None:
    raw = bytearray.fromhex(sweep[(2, 1)].tbl_hex)
    raw[5] ^= 0xFF  # flip a data byte
    with pytest.raises(FoxCRCError):
        reassemble(bytes(raw))


def test_truncated_frame_raises() -> None:
    with pytest.raises(FoxProtocolError):
        split_frames(b"\x02\x03")  # header incomplete


def test_gateway_65004_anomaly_documented(sweep) -> None:
    """The one known-bad capture is malformed at the framing level (documented
    in the discovery report): its concatenation does not re-align into clean
    frames, so parsing raises before any decode."""
    rec = sweep[(1, 65004)]
    with pytest.raises(FoxProtocolError):
        reassemble_hex(rec.tbl_hex)

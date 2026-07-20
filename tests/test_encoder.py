"""Encoder round-trip tests: decode -> encode must reproduce original bytes."""

from __future__ import annotations

import pytest

from foxess.crc import crc16
from foxess.decoder import decode
from foxess.encoder import build_write_frame, encode_value, resolve_scale
from foxess.frame import reassemble_hex
from foxess.registry import default_registry

REG = default_registry()


def _roundtrip_ok(sweep, addr, mid, names):
    rec = sweep[(addr, mid)]
    frame = reassemble_hex(rec.tbl_hex, validate_crc=False)
    model = REG.get(mid)
    decoded = decode(frame.payload, mid, addr=addr)
    offset = 0
    checked = 0
    for field in model.fields:
        orig = frame.payload[offset:offset + field.length_bytes]
        offset += field.length_bytes
        if field.name not in names:
            continue
        scale = resolve_scale(field, model, decoded)
        enc = encode_value(field, decoded[field.name].value, scale)
        assert enc == orig, f"{field.name}: {enc.hex()} != {orig.hex()}"
        checked += 1
    return checked


def test_roundtrip_common_identity(sweep) -> None:
    assert _roundtrip_ok(sweep, 2, 1, {"Mn", "Md", "Vr", "SN", "DA"}) == 5


def test_roundtrip_scaled_battery_fields(sweep) -> None:
    # sfm-scaled fields must invert exactly (voltage/current/temp/soc).
    assert _roundtrip_ok(
        sweep, 2, 65004,
        {"BatteryVoltage", "BatteryCurrent", "BatteryTemperature", "SOC"},
    ) == 4


def test_roundtrip_grid_ac(sweep) -> None:
    assert _roundtrip_ok(sweep, 2, 701, {"Hz", "W", "PF"}) == 3


def test_build_write_frame_is_crc_valid() -> None:
    frame = build_write_frame(2, 0x9C84, (3).to_bytes(2, "big"))
    assert frame[1] == 0x10                       # function code
    assert frame.hex() == "02109c840001020003b0ec"
    body, crc_rx = frame[:-2], frame[-2] | (frame[-1] << 8)
    assert crc16(body) == crc_rx


def test_encode_odd_length_rejected() -> None:
    from foxess.encoder import FoxEncodeError

    with pytest.raises(FoxEncodeError):
        build_write_frame(2, 100, b"\x01")  # not a whole register

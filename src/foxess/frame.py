"""Modbus RTU frame layer for FoxESS ``tbl`` payloads.

A ``tbl`` value returned by ``/api/v1/sunspec/data`` is one *or more*
concatenated Modbus RTU "Read Holding Registers" (function 0x03) response
frames. Each frame is::

    slave(1) | func(1) | byte_count(1) | data(byte_count) | crc16(2, little-endian)

When a model's register block exceeds one response the device chunks it, with
non-final frames carrying the maximum 0xBA (186) data bytes. This module splits
the concatenation, validates each frame's CRC, and reassembles the register
payload.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .crc import crc16
from .errors import FoxCRCError, FoxProtocolError

FUNC_READ_HOLDING = 0x03
MAX_CHUNK_DATA_BYTES = 0xBA  # 186 bytes = 93 registers, observed device maximum


@dataclass(frozen=True, slots=True)
class ModbusFrame:
    """One decoded Modbus RTU response frame."""

    slave: int
    func: int
    byte_count: int
    data: bytes
    crc_received: int
    crc_calculated: int

    @property
    def crc_ok(self) -> bool:
        return self.crc_received == self.crc_calculated


@dataclass(frozen=True, slots=True)
class ReassembledFrame:
    """The result of splitting and reassembling a full ``tbl`` payload."""

    slave: int
    payload: bytes
    frames: tuple[ModbusFrame, ...] = field(default_factory=tuple)

    @property
    def register_count(self) -> int:
        return len(self.payload) // 2


def split_frames(tbl: bytes) -> list[ModbusFrame]:
    """Split a raw ``tbl`` byte string into its constituent Modbus RTU frames.

    Raises :class:`FoxProtocolError` if the byte stream cannot be parsed as a
    sequence of well-formed frames (bad length framing).
    """
    frames: list[ModbusFrame] = []
    i = 0
    n = len(tbl)
    while i < n:
        if i + 3 > n:
            raise FoxProtocolError(
                f"truncated frame header at offset {i} (need 3 bytes, have {n - i})"
            )
        slave = tbl[i]
        func = tbl[i + 1]
        byte_count = tbl[i + 2]
        end = i + 3 + byte_count + 2
        if end > n:
            raise FoxProtocolError(
                f"frame at offset {i} declares {byte_count} data bytes but only "
                f"{n - i - 3} remain"
            )
        data = tbl[i + 3 : i + 3 + byte_count]
        crc_received = tbl[i + 3 + byte_count] | (tbl[i + 4 + byte_count] << 8)
        crc_calculated = crc16(tbl[i : i + 3 + byte_count])
        frames.append(ModbusFrame(slave, func, byte_count, data, crc_received, crc_calculated))
        i = end
    return frames


def reassemble(tbl: bytes, *, validate_crc: bool = True) -> ReassembledFrame:
    """Split, CRC-check, and reassemble a ``tbl`` payload into register bytes.

    :param validate_crc: if True (default), raise :class:`FoxCRCError` on the
        first frame whose CRC does not validate.
    """
    frames = split_frames(tbl)
    if not frames:
        raise FoxProtocolError("empty tbl payload")
    if validate_crc:
        for idx, fr in enumerate(frames):
            if not fr.crc_ok:
                raise FoxCRCError(fr.crc_calculated, fr.crc_received, idx)
    payload = b"".join(fr.data for fr in frames)
    return ReassembledFrame(slave=frames[0].slave, payload=payload, frames=tuple(frames))


def reassemble_hex(tbl_hex: str, *, validate_crc: bool = True) -> ReassembledFrame:
    """Convenience wrapper accepting the hex string as returned in JSON."""
    try:
        raw = bytes.fromhex(tbl_hex)
    except ValueError as exc:  # pragma: no cover - defensive
        raise FoxProtocolError(f"tbl is not valid hex: {exc}") from exc
    return reassemble(raw, validate_crc=validate_crc)

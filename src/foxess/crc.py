"""CRC-16/Modbus.

Polynomial 0xA001 (reflected 0x8005), initial value 0xFFFF, no final XOR,
input and output reflected. Transmitted little-endian at the end of a frame.

Verified against every constituent frame of the captured device sweep.
"""

from __future__ import annotations


def _build_table() -> tuple[int, ...]:
    table = []
    for byte in range(256):
        crc = byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
        table.append(crc)
    return tuple(table)


_TABLE: tuple[int, ...] = _build_table()


def crc16(data: bytes | bytearray | memoryview) -> int:
    """Return the CRC-16/Modbus of ``data`` as an ``int`` in [0, 0xFFFF]."""
    crc = 0xFFFF
    for b in data:
        crc = (crc >> 8) ^ _TABLE[(crc ^ b) & 0xFF]
    return crc


def crc16_bytes(data: bytes | bytearray | memoryview) -> bytes:
    """Return the CRC-16/Modbus as the 2 little-endian bytes appended on the wire."""
    crc = crc16(data)
    return bytes((crc & 0xFF, (crc >> 8) & 0xFF))


def check_crc(frame_without_crc: bytes, crc_le: bytes) -> bool:
    """True if ``crc_le`` (little-endian, as received) matches ``frame_without_crc``."""
    return crc16_bytes(frame_without_crc) == crc_le

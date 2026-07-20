"""Encode field values back into a Modbus *Write Multiple Registers* (0x10) frame.

This is the exact inverse of :mod:`foxess.decoder`, mirroring the device
frontend's ``genData`` / ``genValue`` (see ``docs/05-write-path.md``). The write
frame is::

    slave(1) | 0x10 | start_register(2) | num_registers(2) | byte_count(1)
             | data(byte_count) | CRC-16/Modbus(2, little-endian)

and is delivered as ``POST /api/v1/sunspec/modbus_rw`` with body
``{"cmd": "<hex>"}``.

Correctness is proven by round-tripping captured frames: decode a field, encode
the decoded value, and confirm the bytes match the original. **No hardware
writes are performed by this module** — it only builds byte strings.
"""

from __future__ import annotations

from typing import Any

from .crc import crc16_bytes
from .errors import FoxError
from .models import DecodedModel, FoxField, FoxModelDef

FUNC_WRITE_MULTIPLE = 0x10


class FoxEncodeError(FoxError):
    """A value could not be encoded for its field (type/range/format)."""


def _scale_op(sf_value: int) -> tuple[str, int]:
    return ("mul", 10 ** abs(sf_value)) if sf_value >= 0 else ("div", 10 ** abs(sf_value))


def resolve_scale(
    field: FoxField, model: FoxModelDef, decoded: DecodedModel | None
) -> tuple[str, int] | None:
    """Resolve the (op, factor) for a field's scale reference.

    ``sfm`` scale factors are constants baked into the model definition; ``sf``
    scale factors are read from the live decoded model (``decoded``).
    """
    if not field.sf_ref:
        return None
    ref = next((f for f in model.fields if f.name == field.sf_ref), None)
    if ref is None:
        return None
    if ref.type == "sfm" and ref.const_value is not None:
        return _scale_op(ref.const_value)
    if ref.type == "sf" and decoded is not None:
        raw = decoded[ref.name].raw if ref.name in {f.name for f in decoded.fields} else None
        if isinstance(raw, int):
            return _scale_op(raw)
    return None


def encode_value(field: FoxField, value: Any, scale: tuple[str, int] | None) -> bytes:
    """Encode one field's human value to its on-wire bytes (``length_bytes`` long)."""
    length = field.length_bytes
    t = field.type
    try:
        if t == "ascii":
            raw = str(value).encode("latin1")[:length]
            return raw.ljust(length, b"\x00")
        if t == "hex":
            return int(str(value), 16).to_bytes(length, "big")
        if t == "DATE":
            parts = str(value).split("-")
            if len(parts) != 3:
                raise FoxEncodeError(f"DATE must be YYYY-MM-DD, got {value!r}")
            y, mo, d = (int(p) for p in parts)
            return y.to_bytes(2, "big") + bytes((mo & 0xFF, d & 0xFF))
        if t in ("uint", "int", "sf", "sfm", "enum"):
            scaled = _apply_scale_for_encode(value, scale)
            nbytes = 4 if length == 4 else 2
            signed = t in ("int", "sf", "sfm")
            return int(scaled).to_bytes(nbytes, "big", signed=signed)
    except FoxEncodeError:
        raise
    except (ValueError, OverflowError) as exc:
        raise FoxEncodeError(f"cannot encode {value!r} as {t}[{length}]: {exc}") from exc
    raise FoxEncodeError(f"unsupported writable type {t!r} for field {field.name}")


def _apply_scale_for_encode(value: Any, scale: tuple[str, int] | None) -> int:
    if scale is None:
        return int(value)
    op, factor = scale
    v = float(value)
    # inverse of decode: decode 'div' means raw/factor, so encode multiplies
    v = v * factor if op == "div" else v / factor
    return round(v)


def build_write_frame(slave_addr: int, start_register: int, payload: bytes) -> bytes:
    """Assemble a Modbus 0x10 write frame (with CRC) for ``payload`` bytes.

    ``start_register`` is the 0-based Modbus address (i.e. ``reg_addr``).
    """
    if len(payload) % 2 != 0:
        raise FoxEncodeError("payload must be a whole number of 16-bit registers")
    num_registers = len(payload) // 2
    header = bytes((slave_addr, FUNC_WRITE_MULTIPLE))
    header += start_register.to_bytes(2, "big")
    header += num_registers.to_bytes(2, "big")
    header += bytes((len(payload),))
    body = header + payload
    return body + crc16_bytes(body)


def encode_field_write(
    field: FoxField,
    value: Any,
    model: FoxModelDef,
    *,
    addr: int,
    decoded: DecodedModel | None = None,
) -> bytes:
    """Build the full write frame for a single field write (0x10)."""
    scale = resolve_scale(field, model, decoded)
    payload = encode_value(field, value, scale)
    # field.address is set on decode; fall back to the model start + offset walk.
    reg = _field_address(field, model)
    return build_write_frame(addr, reg, payload)


def _field_address(field: FoxField, model: FoxModelDef) -> int:
    addr = model.modbus_address
    for f in model.fields:
        if f.name == field.name:
            return addr
        addr += f.length_bytes // 2
    raise FoxEncodeError(f"field {field.name} not found in model {model.id}")

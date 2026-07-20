"""Decode a reassembled register payload into typed field values.

Faithfully reproduces the device's own frontend decoder (see
``docs/02-frontend-decoder-and-register-map.md``):

1. Walk the model's fields in order, slicing ``length`` bytes each from the
   payload (offset 0 = first field).
2. Decode each field by ``type``.
3. Apply SunSpec scale factors: a field referencing an ``sf``-typed sibling is
   multiplied by ``10**sf`` (multiply when sf >= 0, divide when sf < 0).
4. Map ``enum`` fields to their label.
"""

from __future__ import annotations

from typing import Any

from .models import DecodedField, DecodedModel, FoxField, FoxModelDef
from .registry import ModelRegistry, default_registry


def _scale_op(sf_value: int) -> tuple[str, int]:
    """Return the (op, factor) for a scale-factor value (SunSpec 10**sf)."""
    return ("mul", 10 ** abs(sf_value)) if sf_value >= 0 else ("div", 10 ** abs(sf_value))


def _decode_scalar(field: FoxField, chunk: bytes) -> Any:
    """Decode one field's raw bytes according to its type (pre-scale)."""
    t = field.type
    if not chunk:
        return None
    if t == "ascii":
        return chunk.split(b"\x00")[0].decode("latin1").strip()
    if t == "uint":
        return int.from_bytes(chunk, "big")
    if t in ("int", "sf", "sfm"):
        return int.from_bytes(chunk, "big", signed=True)
    if t == "uint64":
        return int.from_bytes(chunk, "big")
    if t == "enum":
        return int.from_bytes(chunk, "big")
    if t == "hex":
        return chunk.hex()
    if t == "BCU":
        i = int.from_bytes(chunk, "big")
        return f"R{(i >> 8) & 0x0F}.{i & 0xFF:03d}" if i > 0 else ""
    if t == "BMU":
        i = int.from_bytes(chunk, "big")
        return f"R{(i >> 4) & 0x0F}.{i & 0x0F}" if i > 0 else ""
    if t == "SUN":
        i = int.from_bytes(chunk, "big")
        return f"{(i >> 8) & 0xFF}.{i & 0xFF}.{i >> 24}"
    if t == "DATE":
        i = int.from_bytes(chunk, "big")
        return f"{i >> 16}-{(i >> 8) & 0xFF}-{i & 0xFF}"
    return chunk.hex()  # unknown type: expose raw hex rather than guess


def decode_payload(
    payload: bytes,
    model: FoxModelDef,
    *,
    addr: int = 0,
) -> DecodedModel:
    """Decode ``payload`` (reassembled register bytes) using ``model``."""
    raw_values: dict[str, Any] = {}
    scale_ops: dict[str, tuple[str, int]] = {}
    fields_meta: list[tuple[FoxField, Any, int]] = []

    offset = 0
    address = model.modbus_address
    for fld in model.fields:
        blen = fld.length_bytes
        chunk = payload[offset : offset + blen]
        # 'sfm' fields are constant scale factors baked into the definition and
        # are NOT read from the wire (the device's own decoder does the same);
        # every field still advances the offset to stay byte-aligned.
        if fld.type == "sfm":
            raw = fld.const_value
        else:
            raw = _decode_scalar(fld, chunk)
        raw_values[fld.name] = raw
        if fld.type in ("sf", "sfm") and isinstance(raw, int):
            scale_ops[fld.name] = _scale_op(raw)
        fields_meta.append((fld, raw, address))
        offset += blen
        address += blen // 2

    decoded: list[DecodedField] = []
    for fld, raw, faddr in fields_meta:
        value: Any = raw
        if fld.type == "enum":
            value = _map_enum(fld, raw)
        elif fld.sf_ref and fld.sf_ref in scale_ops and isinstance(raw, int):
            op, factor = scale_ops[fld.sf_ref]
            value = raw * factor if op == "mul" else raw / factor
        decoded.append(
            DecodedField(
                name=fld.name,
                label=fld.label,
                type=fld.type,
                raw=raw,
                value=value,
                unit=fld.unit,
                address=faddr,
                writable=fld.writable,
            )
        )
    return DecodedModel(addr=addr, id=model.id, name=model.name, fields=tuple(decoded))


def _map_enum(field: FoxField, raw: Any) -> Any:
    if not isinstance(raw, int):
        return raw
    for member in field.enum:
        if member.value == raw:
            return member.label
    return raw  # unknown enum value: keep the integer


def decode(
    payload: bytes,
    model_id: int,
    *,
    addr: int = 0,
    registry: ModelRegistry | None = None,
) -> DecodedModel:
    """Decode a payload for ``model_id`` using the given (or default) registry."""
    reg = registry or default_registry()
    return decode_payload(payload, reg.get(model_id), addr=addr)

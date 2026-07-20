"""Typed data structures for model definitions and decoded results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class EnumMember:
    value: int
    label: str


@dataclass(frozen=True, slots=True)
class FoxField:
    """One field within a model definition (from the register map)."""

    name: str
    label: str
    type: str
    length_bytes: int
    show: int = 0
    unit: str | None = None
    sf_ref: str | None = None
    rw: int | None = None
    rwl: int | None = None
    hint: str | None = None
    enum: tuple[EnumMember, ...] = field(default_factory=tuple)
    const_value: int | None = None
    """Baked-in constant for ``sfm`` (shared/fixed) scale-factor fields."""

    @property
    def length_registers(self) -> int:
        return self.length_bytes // 2

    @property
    def writable(self) -> bool:
        """True if the field carries a read/write flag (see decoder analysis §6)."""
        return self.rw is not None


@dataclass(frozen=True, slots=True)
class FoxModelDef:
    """A model definition: id, address, and its ordered field list."""

    id: int
    name: str
    start_register: int      # 1-based SunSpec register number (from frontend)
    length_registers: int
    report: str
    fields: tuple[FoxField, ...]

    @property
    def modbus_address(self) -> int:
        """Canonical Modbus holding-register address (== reg_addr in the API)."""
        return self.start_register - 1


@dataclass(frozen=True, slots=True)
class DecodedField:
    """A decoded field: raw value plus scale-applied value and enum label."""

    name: str
    label: str
    type: str
    raw: Any
    value: Any                 # scale-applied (numbers) or mapped (enum label)
    unit: str | None = None
    address: int | None = None
    writable: bool = False


@dataclass(frozen=True, slots=True)
class WriteResult:
    """Outcome of a (possibly dry-run) register write."""

    addr: int
    model_id: int
    field: str
    value: Any
    register: int
    frame_hex: str
    sent: bool
    result_hex: str | None = None


@dataclass(frozen=True, slots=True)
class DecodedModel:
    """The result of decoding one model's register payload."""

    addr: int
    id: int
    name: str
    fields: tuple[DecodedField, ...]

    def __getitem__(self, name: str) -> DecodedField:
        for f in self.fields:
            if f.name == name:
                return f
        raise KeyError(name)

    def get(self, name: str, default: Any = None) -> Any:
        for f in self.fields:
            if f.name == name:
                return f.value
        return default

    def as_dict(self) -> dict[str, Any]:
        """Map of field name -> decoded value (scale-applied)."""
        return {f.name: f.value for f in self.fields}

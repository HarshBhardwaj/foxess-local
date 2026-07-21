"""High-level client: fetch + reassemble + decode in one call.

    import os
    from foxess import FoxESS
    fox = FoxESS(os.environ["FOX_HOST"])
    common = fox.read_model(2, 1)
    print(common.get("Md"))          # 'AIO-H1-11.4-US'

Convenience accessors (``fox.battery.soc`` etc.) build on ``read_model`` and are
added incrementally as decoders are field-verified.
"""

from __future__ import annotations

import logging
import re

from .encoder import encode_field_write
from .errors import (
    FoxModelNotFound,
    FoxWriteNotAllowed,
    FoxWriteNotConfirmed,
    FoxWriteRangeError,
    FoxWritesDisabled,
)
from .frame import reassemble_hex
from .measurements import (
    AcMeasurement,
    BatteryInfo,
    GridFlow,
    InverterStatus,
    LoadInfo,
    SolarInfo,
    SystemInfo,
)
from .models import DecodedModel, FoxField, WriteResult
from .registry import ModelRegistry, default_registry
from .transport import DataResponse, Transport

# Modbus addresses observed on this hardware.
ADDR_GATEWAY = 1
ADDR_INVERTER = 2

_HINT_RANGE = re.compile(r"^\s*(-?\d+)\s*-\s*(-?\d+)\s*$")
_log = logging.getLogger("foxess.write")


class FoxESS:
    """Facade over transport + frame + decoder."""

    def __init__(
        self,
        host: str,
        *,
        username: str = "admin",
        timeout: float = 5.0,
        registry: ModelRegistry | None = None,
        transport: Transport | None = None,
        allow_writes: bool = False,
    ) -> None:
        self._registry = registry or default_registry()
        self._transport = transport or Transport(host, username=username, timeout=timeout)
        self._allow_writes = allow_writes

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> FoxESS:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    @property
    def registry(self) -> ModelRegistry:
        return self._registry

    # -- write support (Phase 11) ----------------------------------------------
    # Disabled by default. Requires allow_writes=True AND an explicit confirm=True
    # per call. dry_run builds and returns the exact frame without sending.

    def write_field(
        self,
        addr: int,
        model_id: int,
        field_name: str,
        value: object,
        *,
        confirm: bool = False,
        dry_run: bool = False,
    ) -> WriteResult:
        """Write one register field. Safe by construction — see class docs.

        Raises :class:`FoxWritesDisabled` unless the client was created with
        ``allow_writes=True``; :class:`FoxWriteNotConfirmed` unless ``confirm``
        (or ``dry_run``) is set; :class:`FoxWriteNotAllowed` for read-only fields;
        :class:`FoxWriteRangeError` for out-of-range values.
        """
        if not self._allow_writes and not dry_run:
            raise FoxWritesDisabled(
                "writes are disabled; construct FoxESS(..., allow_writes=True) to enable"
            )
        model = self._registry.get(model_id)
        field = next((f for f in model.fields if f.name == field_name), None)
        if field is None:
            raise FoxWriteNotAllowed(f"model {model_id} has no field {field_name!r}")
        if not field.writable:
            raise FoxWriteNotAllowed(f"field {field_name!r} is read-only (no rw flag)")
        _validate_range(field, value)

        # Resolve dynamic (sf) scale factors from the current device reading.
        decoded = None
        if field.sf_ref:
            ref = next((f for f in model.fields if f.name == field.sf_ref), None)
            if ref is not None and ref.type == "sf":
                decoded = self.read_model(addr, model_id)

        frame = encode_field_write(field, value, model, addr=addr, decoded=decoded)
        register = frame[2] << 8 | frame[3]
        _log.info(
            "WRITE addr=%s model=%s field=%s value=%r register=%s frame=%s dry_run=%s",
            addr, model_id, field_name, value, register, frame.hex(), dry_run,
        )
        if dry_run:
            return WriteResult(addr, model_id, field_name, value, register, frame.hex(), sent=False)
        if not confirm:
            raise FoxWriteNotConfirmed(
                "refusing to write without confirm=True (use dry_run=True to preview)"
            )
        result = self._transport.write_modbus(frame.hex())
        return WriteResult(addr, model_id, field_name, value, register, frame.hex(),
                           sent=True, result_hex=result)

    def read_raw(self, addr: int, model_id: int) -> DataResponse:
        """Return the raw envelope (tbl hex, reg_addr) without decoding."""
        return self._transport.read_data(addr, model_id)

    def read_model(
        self, addr: int, model_id: int, *, validate_crc: bool = True
    ) -> DecodedModel:
        """Fetch, CRC-check, reassemble, and decode one model."""
        resp = self._transport.read_data(addr, model_id)
        frame = reassemble_hex(resp.tbl_hex, validate_crc=validate_crc)
        model = self._registry.get(model_id)
        from .decoder import decode_payload

        return decode_payload(frame.payload, model, addr=addr)

    def scan(self, addr: int, *, ids: tuple[int, ...] | None = None) -> dict[int, bool]:
        """Probe which model IDs are present for ``addr``. Returns id -> available."""
        candidate = ids or self._registry.ids
        result: dict[int, bool] = {}
        for mid in candidate:
            try:
                self._transport.read_data(addr, mid)
                result[mid] = True
            except FoxModelNotFound:
                result[mid] = False
        return result

    def read_models(
        self, addr: int, ids: tuple[int, ...], *, validate_crc: bool = True
    ) -> dict[int, DecodedModel]:
        """Read and decode several models, skipping any the device lacks."""
        out: dict[int, DecodedModel] = {}
        for mid in ids:
            try:
                out[mid] = self.read_model(addr, mid, validate_crc=validate_crc)
            except FoxModelNotFound:
                continue
        return out

    # -- high-level measurement views (default to the inverter) -----------------

    @property
    def system(self) -> SystemInfo:
        return SystemInfo.from_models(
            self.read_models(ADDR_INVERTER, SystemInfo.REQUIRED_MODELS)
        )

    @property
    def battery(self) -> BatteryInfo:
        return BatteryInfo.from_models(
            self.read_models(ADDR_INVERTER, BatteryInfo.REQUIRED_MODELS)
        )

    @property
    def grid(self) -> GridFlow:
        """Net grid import/export (model 65031 'HubInfo', read at the gateway)."""
        return GridFlow.from_models(
            self.read_models(ADDR_GATEWAY, GridFlow.REQUIRED_MODELS)
        )

    @property
    def gridflow(self) -> GridFlow:
        """Alias for :attr:`grid` (net grid import/export, model 65031)."""
        return self.grid

    @property
    def ac(self) -> AcMeasurement:
        """Inverter AC-terminal measurement (model 701)."""
        return AcMeasurement.from_models(
            self.read_models(ADDR_INVERTER, AcMeasurement.REQUIRED_MODELS)
        )

    @property
    def solar(self) -> SolarInfo:
        return SolarInfo.from_models(
            self.read_models(ADDR_INVERTER, SolarInfo.REQUIRED_MODELS)
        )

    @property
    def load(self) -> LoadInfo:
        """Whole-home load (model 65031 'HubInfo', read at the gateway)."""
        return LoadInfo.from_models(
            self.read_models(ADDR_GATEWAY, LoadInfo.REQUIRED_MODELS)
        )

    @property
    def inverter(self) -> InverterStatus:
        return InverterStatus.from_models(
            self.read_models(ADDR_INVERTER, InverterStatus.REQUIRED_MODELS)
        )


def _validate_range(field: FoxField, value: object) -> None:
    """Best-effort range/enum validation from the field's own metadata."""
    if field.enum:
        allowed = {m.value for m in field.enum}
        labels = {m.label for m in field.enum}
        if value not in allowed and value not in labels:
            raise FoxWriteRangeError(
                f"{field.name}: {value!r} not a valid enum ({sorted(allowed)})"
            )
        return
    if field.hint:
        m = _HINT_RANGE.match(field.hint)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            try:
                numeric = float(value)  # type: ignore[arg-type]
            except (TypeError, ValueError):
                return
            if not lo <= numeric <= hi:
                raise FoxWriteRangeError(f"{field.name}: {value!r} outside {lo}..{hi}")

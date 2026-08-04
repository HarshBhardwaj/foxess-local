"""High-level EMS (energy-management) control — Phase 11 write layer.

This is a **typed convenience wrapper** over the verified low-level
:meth:`foxess.client.FoxESS.write_field` primitive (see ``docs/05-write-path.md``).
It exposes the battery/grid strategy controls a home automation actually needs —
work mode, on-grid min/max SoC, grid-charge enable, and the forced
charge/discharge schedules — without callers hand-addressing registers.

Evidence base (decoded live from the reference AIO-H1-11.4-US, addr 2):

* **Model 65026 "EMS"** — ``EMSMode`` (Self-Use/Force/Manual/TOU/Backup),
  ``SOCLowerLimit`` (on-grid min SoC, firmware-capped 5-20 %), ``SOCUpperLimit``
  (80-100 %), ``ChargeByGridEnable`` / ``ChargeByGridValue``,
  ``BatBackupSOCOffgrid``. All rw.
* **Model 65034 "EMS-Manual"** — three forced-charge and three forced-discharge
  time slots (start/end H:M, target SoC, power) plus master enable + effective
  days. All rw.

Every mutating method is **disabled-by-default, dry-run-capable, confirm-gated**
— it simply forwards to ``write_field``, so it inherits that primitive's safety
model unchanged. Multi-field operations (e.g. a forced-charge slot) are written
field-by-field as independent single-register 0x10 writes; see the note on
``force_charge`` about atomicity, an open verification item.

Nothing in this module writes to the device unless the caller passes
``confirm=True`` on a client built with ``allow_writes=True``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import DecodedModel, WriteResult


class _WritableClient(Protocol):
    """The subset of the FoxESS facade the EMS controller depends on."""

    def read_model(self, addr: int, model_id: int) -> DecodedModel: ...

    def write_field(
        self,
        addr: int,
        model_id: int,
        field_name: str,
        value: object,
        *,
        confirm: bool = ...,
        dry_run: bool = ...,
    ) -> WriteResult: ...

MODEL_EMS = 65026
MODEL_EMS_MANUAL = 65034

# EMSMode enum (model 65026, field EMSMode) — labels are the device's own.
WORK_MODES: dict[str, int] = {
    "self-use": 0,
    "force": 2,
    "manual": 5,
    "tou": 6,
    "backup": 7,
}
_WORK_MODE_LABELS = {v: k for k, v in WORK_MODES.items()}

_ENABLE = 170  # device convention: 0xAA = enable
_DISABLE = 85  # 0x55 = disable
_DAYS_WORKDAY = 0
_DAYS_EVERYDAY = 1

# Firmware-documented ranges (from the register map `hint`s).
MIN_SOC_RANGE = (5.0, 20.0)  # SOCLowerLimit, %, after S_SF (/10)
MAX_SOC_RANGE = (80.0, 100.0)  # SOCUpperLimit, %


@dataclass(frozen=True)
class EmsState:
    """Decoded snapshot of the battery/grid strategy (model 65026)."""

    mode: str
    mode_value: int
    min_soc_pct: float
    max_soc_pct: float
    charge_by_grid: bool
    charge_by_grid_kw: float
    backup_soc_offgrid_pct: float


@dataclass(frozen=True)
class ForceChargeSlot:
    """One forced-charge time slot (model 65034, slot 1-3)."""

    slot: int
    enabled: bool
    everyday: bool
    start_hour: int
    start_min: int
    end_hour: int
    end_min: int
    target_soc: int
    power_kw: float


def _clamp_check(name: str, value: float, lo: float, hi: float) -> None:
    if not (lo <= value <= hi):
        raise ValueError(f"{name} {value} outside firmware range {lo}-{hi}")


class EmsController:
    """``fox.ems`` — typed reads and safe writes for the EMS models.

    Bound to a :class:`~foxess.client.FoxESS` (or async facade); all writes are
    delegated to ``client.write_field`` so the disabled-by-default / confirm /
    dry-run guarantees hold with no duplication.
    """

    def __init__(self, client: _WritableClient, addr: int) -> None:
        self._c = client
        self._addr = addr

    # -- reads -----------------------------------------------------------------

    def read(self) -> EmsState:
        """Decode the current EMS strategy (model 65026)."""
        m: DecodedModel = self._c.read_model(self._addr, MODEL_EMS)
        mode_value = int(m.get("EMSMode"))
        return EmsState(
            mode=_WORK_MODE_LABELS.get(mode_value, f"unknown({mode_value})"),
            mode_value=mode_value,
            min_soc_pct=float(m.get("SOCLowerLimit")),
            max_soc_pct=float(m.get("SOCUpperLimit")),
            charge_by_grid=int(m.get("ChargeByGridEnable")) == _ENABLE,
            charge_by_grid_kw=float(m.get("ChargeByGridValue")),
            backup_soc_offgrid_pct=float(m.get("BatBackupSOCOffgrid")),
        )

    def read_force_charge(self, slot: int = 1) -> ForceChargeSlot:
        """Decode a forced-charge slot (1-3) from model 65034."""
        if slot not in (1, 2, 3):
            raise ValueError("slot must be 1, 2, or 3")
        m: DecodedModel = self._c.read_model(self._addr, MODEL_EMS_MANUAL)
        p = "Forced_charging"
        return ForceChargeSlot(
            slot=slot,
            enabled=int(m.get("Forced_charging")) == _ENABLE,
            everyday=int(m.get("Effective_time_of_forced_charging")) == _DAYS_EVERYDAY,
            start_hour=int(m.get(f"{p}_start_time_{slot}_Hour")),
            start_min=int(m.get(f"{p}_start_time_{slot}_Min")),
            end_hour=int(m.get(f"{p}_end_time_{slot}_Hour")),
            end_min=int(m.get(f"{p}_end_time_{slot}_Min")),
            target_soc=int(m.get(f"{p}_target_SOC_{slot}")),
            power_kw=float(m.get(f"{p}_target_Power_{slot}")),
        )

    # -- single-field writes (thin, typed) -------------------------------------

    def set_min_soc(
        self, pct: float, *, confirm: bool = False, dry_run: bool = False
    ) -> WriteResult:
        """Set the on-grid minimum SoC (SOCLowerLimit). Firmware range 5-20 %."""
        _clamp_check("min_soc", pct, *MIN_SOC_RANGE)
        return self._c.write_field(
            self._addr, MODEL_EMS, "SOCLowerLimit", pct, confirm=confirm, dry_run=dry_run
        )

    def set_max_soc(
        self, pct: float, *, confirm: bool = False, dry_run: bool = False
    ) -> WriteResult:
        """Set the charge ceiling (SOCUpperLimit). Firmware range 80-100 %."""
        _clamp_check("max_soc", pct, *MAX_SOC_RANGE)
        return self._c.write_field(
            self._addr, MODEL_EMS, "SOCUpperLimit", pct, confirm=confirm, dry_run=dry_run
        )

    def set_work_mode(
        self, mode: str, *, confirm: bool = False, dry_run: bool = False
    ) -> WriteResult:
        """Set EMSMode by name: self-use | force | manual | tou | backup."""
        key = mode.strip().lower()
        if key not in WORK_MODES:
            raise ValueError(f"unknown work mode {mode!r}; valid: {sorted(WORK_MODES)}")
        return self._c.write_field(
            self._addr, MODEL_EMS, "EMSMode", WORK_MODES[key], confirm=confirm, dry_run=dry_run
        )

    # -- multi-field: forced charge schedule -----------------------------------

    def force_charge(
        self,
        *,
        start: tuple[int, int],
        end: tuple[int, int],
        target_soc: int,
        power_kw: float,
        slot: int = 1,
        everyday: bool = True,
        enable: bool = True,
        confirm: bool = False,
        dry_run: bool = False,
    ) -> list[WriteResult]:
        """Program a forced-charge slot (model 65034) and optionally enable it.

        Writes the slot's six fields, the effective-days field, and the master
        ``Forced_charging`` enable as **independent single-register 0x10 writes**,
        returning one :class:`WriteResult` per field (in send order). With
        ``dry_run=True`` every frame is built and returned but nothing is sent.

        .. note::
           Whether the inverter applies these fields atomically or one-by-one is
           an open verification item (``docs/05`` §8). We write the schedule
           fields **before** the enable flag so a partially-applied group is
           never left *enabled* with stale times. Always ``read_force_charge``
           back to confirm.
        """
        if slot not in (1, 2, 3):
            raise ValueError("slot must be 1, 2, or 3")
        for label, (h, mn) in (("start", start), ("end", end)):
            if not (0 <= h <= 23 and 0 <= mn <= 59):
                raise ValueError(f"{label} {h:02d}:{mn:02d} out of range")
        if not (0 <= target_soc <= 100):
            raise ValueError("target_soc must be 0-100")
        if power_kw < 0:
            raise ValueError("power_kw must be >= 0")

        p = "Forced_charging"
        # Schedule fields first, enable LAST (see note).
        writes: list[tuple[str, object]] = [
            (f"{p}_start_time_{slot}_Hour", start[0]),
            (f"{p}_start_time_{slot}_Min", start[1]),
            (f"{p}_end_time_{slot}_Hour", end[0]),
            (f"{p}_end_time_{slot}_Min", end[1]),
            (f"{p}_target_SOC_{slot}", target_soc),
            (f"{p}_target_Power_{slot}", power_kw),
            ("Effective_time_of_forced_charging", _DAYS_EVERYDAY if everyday else _DAYS_WORKDAY),
            (p, _ENABLE if enable else _DISABLE),
        ]
        results: list[WriteResult] = []
        for field_name, value in writes:
            results.append(
                self._c.write_field(
                    self._addr, MODEL_EMS_MANUAL, field_name, value,
                    confirm=confirm, dry_run=dry_run,
                )
            )
        return results

    def disable_force_charge(
        self, *, confirm: bool = False, dry_run: bool = False
    ) -> WriteResult:
        """Clear only the master forced-charge enable (leaves the schedule intact)."""
        return self._c.write_field(
            self._addr, MODEL_EMS_MANUAL, "Forced_charging", _DISABLE,
            confirm=confirm, dry_run=dry_run,
        )

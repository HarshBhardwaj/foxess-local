"""High-level measurement views built from decoded models.

Each view maps friendly, unit-bearing attributes to specific verified register
fields. Source fields and their confidence are documented inline; see
``docs/02-frontend-decoder-and-register-map.md``. Values are ``None`` when the
source model or field is unavailable, so callers never crash on a missing sensor.

Sentinel handling
-----------------
Some registers read a fixed "not available" sentinel when the underlying sensor
or accessory is absent (e.g. no external revenue/CT meter): int32 max
(``2147483647``), uint32 max (``4294967295``), and ``0xFFFF0000``
(``4294901760``). ``_val`` maps these to ``None`` so consumers render
"unavailable" rather than a nonsense number like ``429490176 kWh``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .models import DecodedModel

Models = Mapping[int, DecodedModel]

# Raw integer sentinels that mean "field not populated / accessory absent".
# Checked against the *raw* register value before scaling.
_SENTINELS: frozenset[int] = frozenset(
    {
        0x7FFFFFFF,  # 2147483647  int32 max  (RGM* active power w/o revenue meter)
        0xFFFFFFFF,  # 4294967295  uint32 max
        0xFFFF0000,  # 4294901760  (GenerationPower/TotalPVPower/GridMeter* na)
        0x7FFF,      # 32767       int16 max
        0xFFFF,      # 65535       uint16 max
    }
)


def _val(models: Models, model_id: int, field: str) -> Any:
    """Return a field's scaled value, or ``None`` if missing or a sentinel."""
    model = models.get(model_id)
    if model is None:
        return None
    try:
        decoded = model[field]
    except KeyError:
        return None
    if isinstance(decoded.raw, int) and decoded.raw in _SENTINELS:
        return None
    return decoded.value


# Backwards-compatible alias (older code/tests import ``_get``).
_get = _val


@dataclass(frozen=True, slots=True)
class BatteryInfo:
    """Battery state. Sources: model 65004 (electrical + energy) + 713 (SoH)."""

    soc_percent: float | None
    soh_percent: float | None
    voltage_v: float | None
    current_a: float | None
    power_w: float | None            # negative = charging, positive = discharging
    temperature_c: float | None
    energy_rated_wh: float | None
    energy_available_wh: float | None
    # Lifetime / daily energy counters (VERIFIED valid on the reference unit).
    energy_charged_total_kwh: float | None
    energy_discharged_total_kwh: float | None
    energy_charged_today_kwh: float | None
    energy_discharged_today_kwh: float | None

    @property
    def charging(self) -> bool | None:
        if self.power_w is None:
            return None
        return self.power_w < 0

    @property
    def discharge_power_w(self) -> float | None:
        """Discharge power (>=0). Positive ``power_w`` is discharge."""
        if self.power_w is None:
            return None
        return self.power_w if self.power_w > 0 else 0.0

    @property
    def charge_power_w(self) -> float | None:
        """Charge power (>=0). Negative ``power_w`` is charge."""
        if self.power_w is None:
            return None
        return -self.power_w if self.power_w < 0 else 0.0

    @classmethod
    def from_models(cls, models: Models) -> BatteryInfo:
        return cls(
            soc_percent=_val(models, 65004, "SOC"),
            soh_percent=_val(models, 713, "StateOfHealth"),  # 65004 SOH is unscaled/buggy
            voltage_v=_val(models, 65004, "BatteryVoltage"),
            current_a=_val(models, 65004, "BatteryCurrent"),
            power_w=_val(models, 65004, "BatteryPower"),
            temperature_c=_val(models, 65004, "BatteryTemperature"),
            energy_rated_wh=_val(models, 713, "WHRtg"),
            energy_available_wh=_val(models, 713, "WHAvail"),
            energy_charged_total_kwh=_val(models, 65004, "TotalBatteryCharge"),
            energy_discharged_total_kwh=_val(models, 65004, "TotalBatteryDischarge"),
            energy_charged_today_kwh=_val(models, 65004, "DailyBatteryCharge"),
            energy_discharged_today_kwh=_val(models, 65004, "DailyBatteryDischarge"),
        )

    REQUIRED_MODELS = (65004, 713)


@dataclass(frozen=True, slots=True)
class GridFlow:
    """Net grid import/export at the grid interface.

    Source: model **65031** ("R&D(HubInfo)"), the Fox Hub G2's aggregate
    metering block, read at the **gateway** Modbus address (1) -- NOT the
    inverter address (2), where these registers are zeroed. This is the same
    data FoxCloud displays.

    VERIFIED against the device during a pure grid-import moment (battery
    offline, no solar): ``TotalActivePowerOfGrid`` read -959 W and
    ``TotalActivePowerOfLoad`` +959 W, matching FoxCloud's ~941 W import.

    Sign convention (VERIFIED): ``power_w`` negative = **import** from grid,
    positive = **export** to grid.
    """

    power_w: float | None                  # signed: negative=import, positive=export
    import_energy_total_kwh: float | None   # lifetime grid import (kWh)
    export_energy_total_kwh: float | None   # lifetime grid export (kWh)
    import_energy_today_kwh: float | None
    export_energy_today_kwh: float | None

    @property
    def export_power_w(self) -> float | None:
        if self.power_w is None:
            return None
        return self.power_w if self.power_w > 0 else 0.0

    @property
    def import_power_w(self) -> float | None:
        if self.power_w is None:
            return None
        return -self.power_w if self.power_w < 0 else 0.0

    @classmethod
    def from_models(cls, models: Models) -> GridFlow:
        return cls(
            power_w=_val(models, 65031, "TotalActivePowerOfGrid"),
            import_energy_total_kwh=_val(models, 65031, "Grid_total_Grid_Energy_consumption"),
            export_energy_total_kwh=_val(models, 65031, "Grid_total_Grid_Energy"),
            import_energy_today_kwh=_val(models, 65031, "Grid_daily_Grid_Energy_consumption"),
            export_energy_today_kwh=_val(models, 65031, "Grid_daily_Grid_Energy"),
        )

    REQUIRED_MODELS = (65031,)


@dataclass(frozen=True, slots=True)
class AcMeasurement:
    """Inverter AC-terminal measurement. Source: model 701.

    This is the inverter's own AC output, *not* net grid import/export (use
    :class:`GridFlow` for that). Kept as a distinct view to avoid the earlier
    mislabel of 701 as "grid".
    """

    power_w: float | None
    apparent_va: float | None
    reactive_var: float | None
    power_factor: float | None
    frequency_hz: float | None
    voltage_v: float | None          # L1-N
    current_a: float | None          # L1
    energy_injected_wh: float | None
    connection_state: int | None

    @classmethod
    def from_models(cls, models: Models) -> AcMeasurement:
        return cls(
            power_w=_val(models, 701, "W"),
            apparent_va=_val(models, 701, "VA"),
            reactive_var=_val(models, 701, "Var"),
            power_factor=_val(models, 701, "PF"),
            frequency_hz=_val(models, 701, "Hz"),
            voltage_v=_val(models, 701, "VL1"),
            current_a=_val(models, 701, "AL1"),
            energy_injected_wh=_val(models, 701, "TotWhInj"),
            connection_state=_val(models, 701, "ConnSt"),
        )

    REQUIRED_MODELS = (701,)


# Backwards-compatible alias: the old name for the 701 view.
GridMeasurement = AcMeasurement


@dataclass(frozen=True, slots=True)
class SolarInfo:
    """PV production. Sources: model 65000 (DC power) + 65004 (energy counters)."""

    power_w: float | None
    daily_energy_kwh: float | None
    total_energy_kwh: float | None

    @classmethod
    def from_models(cls, models: Models) -> SolarInfo:
        return cls(
            power_w=_val(models, 65000, "TotalDCPower"),
            daily_energy_kwh=_val(models, 65004, "DailyPVGeneration"),
            total_energy_kwh=_val(models, 65004, "TotalPVGeneration"),
        )

    REQUIRED_MODELS = (65000, 65004)


@dataclass(frozen=True, slots=True)
class LoadInfo:
    """Whole-home load. Source: model **65031** ("HubInfo") at the gateway
    address (1). ``TotalActivePowerOfLoad`` is the Hub's aggregate house load
    (VERIFIED: read +959 W matching FoxCloud during a grid-import moment)."""

    power_w: float | None
    total_energy_kwh: float | None

    @classmethod
    def from_models(cls, models: Models) -> LoadInfo:
        return cls(
            power_w=_val(models, 65031, "TotalActivePowerOfLoad"),
            total_energy_kwh=None,  # no cumulative house-load counter in HubInfo
        )

    REQUIRED_MODELS = (65031,)


@dataclass(frozen=True, slots=True)
class InverterStatus:
    """Inverter operating status. Source: model 701."""

    operating_state: int | None
    inverter_state: int | None
    connection_state: int | None
    temperature_c: float | None      # heat-sink temperature
    alarm: Any | None                # alarm bitfield (hex string)

    @classmethod
    def from_models(cls, models: Models) -> InverterStatus:
        return cls(
            operating_state=_val(models, 701, "St"),
            inverter_state=_val(models, 701, "InvSt"),
            connection_state=_val(models, 701, "ConnSt"),
            temperature_c=_val(models, 701, "TmpSnk"),
            alarm=_val(models, 701, "Alrm"),
        )

    REQUIRED_MODELS = (701,)


@dataclass(frozen=True, slots=True)
class SystemInfo:
    """Device identity. Source: model 1 (SunSpec Common)."""

    manufacturer: str | None
    model: str | None
    serial: str | None
    version: str | None
    device_address: int | None

    @classmethod
    def from_models(cls, models: Models) -> SystemInfo:
        return cls(
            manufacturer=_val(models, 1, "Mn"),
            model=_val(models, 1, "Md"),
            serial=_val(models, 1, "SN"),
            version=_val(models, 1, "Vr"),
            device_address=_val(models, 1, "DA"),
        )

    REQUIRED_MODELS = (1,)

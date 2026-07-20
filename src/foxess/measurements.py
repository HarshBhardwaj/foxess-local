"""High-level measurement views built from decoded models.

Each view maps friendly, unit-bearing attributes to specific verified register
fields. Source fields and their confidence are documented inline; see
``docs/02-frontend-decoder-and-register-map.md``. Values are ``None`` when the
source model or field is unavailable, so callers never crash on a missing sensor.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .models import DecodedModel

Models = Mapping[int, DecodedModel]


def _get(models: Models, model_id: int, field: str) -> Any:
    model = models.get(model_id)
    if model is None:
        return None
    try:
        return model[field].value
    except KeyError:
        return None


@dataclass(frozen=True, slots=True)
class BatteryInfo:
    """Battery state. Sources: model 65004 (electrical) + 713 (SoC/SoH/energy)."""

    soc_percent: float | None
    soh_percent: float | None
    voltage_v: float | None
    current_a: float | None
    power_w: float | None            # negative = charging, positive = discharging
    temperature_c: float | None
    energy_rated_wh: float | None
    energy_available_wh: float | None

    @property
    def charging(self) -> bool | None:
        if self.power_w is None:
            return None
        return self.power_w < 0

    @classmethod
    def from_models(cls, models: Models) -> BatteryInfo:
        return cls(
            soc_percent=_get(models, 65004, "SOC"),
            soh_percent=_get(models, 713, "StateOfHealth"),  # 65004 SOH is unscaled/buggy
            voltage_v=_get(models, 65004, "BatteryVoltage"),
            current_a=_get(models, 65004, "BatteryCurrent"),
            power_w=_get(models, 65004, "BatteryPower"),
            temperature_c=_get(models, 65004, "BatteryTemperature"),
            energy_rated_wh=_get(models, 713, "WHRtg"),
            energy_available_wh=_get(models, 713, "WHAvail"),
        )

    REQUIRED_MODELS = (65004, 713)


@dataclass(frozen=True, slots=True)
class GridMeasurement:
    """Inverter AC / grid-interface measurement. Source: model 701."""

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
    def from_models(cls, models: Models) -> GridMeasurement:
        return cls(
            power_w=_get(models, 701, "W"),
            apparent_va=_get(models, 701, "VA"),
            reactive_var=_get(models, 701, "Var"),
            power_factor=_get(models, 701, "PF"),
            frequency_hz=_get(models, 701, "Hz"),
            voltage_v=_get(models, 701, "VL1"),
            current_a=_get(models, 701, "AL1"),
            energy_injected_wh=_get(models, 701, "TotWhInj"),
            connection_state=_get(models, 701, "ConnSt"),
        )

    REQUIRED_MODELS = (701,)


@dataclass(frozen=True, slots=True)
class SolarInfo:
    """PV production. Sources: model 65000 (DC power) + 65004 (energy counters)."""

    power_w: float | None
    daily_energy_kwh: float | None
    total_energy_kwh: float | None

    @classmethod
    def from_models(cls, models: Models) -> SolarInfo:
        return cls(
            power_w=_get(models, 65000, "TotalDCPower"),
            daily_energy_kwh=_get(models, 65004, "DailyPVGeneration"),
            total_energy_kwh=_get(models, 65004, "TotalPVGeneration"),
        )

    REQUIRED_MODELS = (65000, 65004)


@dataclass(frozen=True, slots=True)
class LoadInfo:
    """Site load. Source: model 65004 (requires a load/CT meter to be non-zero)."""

    power_w: float | None
    total_energy_kwh: float | None

    @classmethod
    def from_models(cls, models: Models) -> LoadInfo:
        return cls(
            power_w=_get(models, 65004, "TotalActivePowerOfLoad"),
            total_energy_kwh=_get(models, 65004, "LoadTotalEnergy"),
        )

    REQUIRED_MODELS = (65004,)


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
            operating_state=_get(models, 701, "St"),
            inverter_state=_get(models, 701, "InvSt"),
            connection_state=_get(models, 701, "ConnSt"),
            temperature_c=_get(models, 701, "TmpSnk"),
            alarm=_get(models, 701, "Alrm"),
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
            manufacturer=_get(models, 1, "Mn"),
            model=_get(models, 1, "Md"),
            serial=_get(models, 1, "SN"),
            version=_get(models, 1, "Vr"),
            device_address=_get(models, 1, "DA"),
        )

    REQUIRED_MODELS = (1,)

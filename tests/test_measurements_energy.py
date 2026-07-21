"""Battery/grid energy views + sentinel handling (battery discharge & grid I/E).

Covers the fields added so the Home Assistant Energy dashboard can show battery
in/out and grid import/export on an inverter without an external revenue meter.
"""

from __future__ import annotations

from foxess.measurements import (
    _SENTINELS,
    AcMeasurement,
    BatteryInfo,
    GridFlow,
    _val,
)
from foxess.models import DecodedField, DecodedModel


def _model(model_id: int, pairs: dict[str, tuple[int, object]]) -> DecodedModel:
    fields = tuple(
        DecodedField(name=n, label=n, type="int", raw=r, value=v)
        for n, (r, v) in pairs.items()
    )
    return DecodedModel(addr=2, id=model_id, name=str(model_id), fields=fields)


def test_sentinel_values_map_to_none() -> None:
    for s in _SENTINELS:
        m = {65004: _model(65004, {"GridMeterExportTotalEnergy": (s, s / 10)})}
        assert _val(m, 65004, "GridMeterExportTotalEnergy") is None


def test_battery_charge_discharge_split_and_energy() -> None:
    # negative power == charging (documented device convention)
    m = {
        65004: _model(
            65004,
            {
                "BatteryPower": (-2500, -2500),
                "SOC": (1000, 100.0),
                "TotalBatteryCharge": (3963, 396.3),
                "TotalBatteryDischarge": (3352, 335.2),
                "DailyBatteryCharge": (76, 7.6),
                "DailyBatteryDischarge": (0, 0.0),
            },
        ),
        713: _model(713, {"StateOfHealth": (100, 100), "WHAvail": (10732, 10732)}),
    }
    b = BatteryInfo.from_models(m)
    assert b.charging is True
    assert b.charge_power_w == 2500
    assert b.discharge_power_w == 0.0
    assert b.energy_charged_total_kwh == 396.3
    assert b.energy_discharged_total_kwh == 335.2

    # positive power == discharging
    m[65004] = _model(65004, {"BatteryPower": (6580, 6580)})
    b2 = BatteryInfo.from_models(m)
    assert b2.discharge_power_w == 6580
    assert b2.charge_power_w == 0.0
    assert b2.charging is False


def test_grid_import_export_from_hubinfo() -> None:
    # Grid now comes from model 65031 (HubInfo). Sign verified: negative = import.
    m = {
        65031: _model(
            65031,
            {
                "TotalActivePowerOfGrid": (-959, -959),
                "TotalActivePowerOfLoad": (959, 959),
                "Grid_total_Grid_Energy_consumption": (36605, 3660.5),  # import
                "Grid_total_Grid_Energy": (3165, 316.5),                # export
                "Grid_daily_Grid_Energy_consumption": (624, 62.4),
                "Grid_daily_Grid_Energy": (159, 15.9),
            },
        )
    }
    g = GridFlow.from_models(m)
    assert g.power_w == -959
    assert g.import_power_w == 959
    assert g.export_power_w == 0.0
    assert g.import_energy_total_kwh == 3660.5
    assert g.export_energy_total_kwh == 316.5
    from foxess.measurements import LoadInfo
    assert LoadInfo.from_models(m).power_w == 959


def test_ac_view_reads_model_701() -> None:
    m = {701: _model(701, {"W": (4500, 4500), "Hz": (5996, 59.96)})}
    ac = AcMeasurement.from_models(m)
    assert ac.power_w == 4500
    assert ac.frequency_hz == 59.96

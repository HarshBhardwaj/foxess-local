"""Registry loading tests."""

from __future__ import annotations

from foxess.registry import default_registry


def test_bundled_registry_loads_all_models() -> None:
    reg = default_registry()
    assert len(reg) == 54
    assert 1 in reg
    assert 65039 in reg


def test_common_model_shape() -> None:
    reg = default_registry()
    common = reg.get(1)
    assert common.name == "Common"
    assert common.modbus_address == 40000  # start 40001 - 1
    names = [f.name for f in common.fields]
    assert names[:3] == ["SunSpecID", "ID", "L"]
    da = next(f for f in common.fields if f.name == "DA")
    assert da.writable and da.hint == "1-246"


def test_scale_and_enum_metadata_present() -> None:
    reg = default_registry()
    cap = reg.get(702)
    wmax = next(f for f in cap.fields if f.name == "WMaxRtg")
    assert wmax.sf_ref == "W_SF"
    batinfo = reg.get(65009)
    assert any(f.enum for f in batinfo.fields)

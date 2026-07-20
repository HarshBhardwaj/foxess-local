"""End-to-end decode tests against captured frames (four-source verification)."""

from __future__ import annotations

from foxess.decoder import decode
from foxess.frame import reassemble_hex


def _decode(sweep, addr, mid):
    frame = reassemble_hex(sweep[(addr, mid)].tbl_hex)
    return decode(frame.payload, mid, addr=addr)


def test_common_identity_inverter(sweep) -> None:
    m = _decode(sweep, 2, 1)
    assert m.get("Mn") == "FOX"
    assert m.get("Md") == "AIO-H1-11.4-US"
    assert m.get("Vr") == "1.1.11.8c"
    assert m.get("SN") == "601U10000000000"
    assert m.get("DA") == 2


def test_common_identity_gateway(sweep) -> None:
    m = _decode(sweep, 1, 1)
    assert m.get("Md") == "FOX Hub G2"
    assert m.get("SN") == "60HUB0000000000"


def test_der_capacity_nameplate(sweep) -> None:
    # WMaxRtg must match the AIO-H1-11.4 nameplate: 11400 W.
    m = _decode(sweep, 2, 702)
    assert m.get("WMaxRtg") == 11400
    assert m.get("VAMaxRtg") == 11400


def test_storage_capacity_plausible(sweep) -> None:
    m = _decode(sweep, 2, 713)
    assert m.get("StateOfCharge") == 51
    assert m.get("StateOfHealth") == 100
    assert m.get("WHRtg") == 11925


def test_firmware_strings(sweep) -> None:
    m = _decode(sweep, 2, 65005)
    vals = m.as_dict()
    assert vals["mcu_ver_1"] == "H1-US-A_Manager_V1.17"


def test_all_supported_models_decode_without_error(sweep) -> None:
    """Every successful capture (except the gateway 65004 anomaly) decodes."""
    from foxess.registry import default_registry

    reg = default_registry()
    for (addr, mid), rec in sweep.items():
        if rec.errno != 0 or not rec.tbl_hex or (addr, mid) == (1, 65004):
            continue
        if mid not in reg:
            continue
        frame = reassemble_hex(rec.tbl_hex, validate_crc=False)
        m = decode(frame.payload, mid, addr=addr)
        assert m.id == mid
        assert m.fields  # produced at least one field

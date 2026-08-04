"""Phase 11 EMS layer — decode fixtures + write-frame (dry-run) correctness.

No hardware. Decode assertions use frames captured live from the reference
inverter; write assertions check the exact 0x10 frames the SDK would send,
including CRC, target register, and encoded value bytes.
"""
from __future__ import annotations

# --- exact live captures (addr 2), stored verbatim in tests/data ------------
import pathlib as _pl

import pytest

from foxess import FoxESS
from foxess.crc import crc16
from foxess.decoder import decode
from foxess.ems import WORK_MODES, EmsController
from foxess.frame import reassemble_hex

_D = _pl.Path(__file__).parent / 'data'
EMS_65026 = (_D / 'ems_65026.hex').read_text().strip()
EMS_MANUAL_65034 = (_D / 'ems_65034.hex').read_text().strip()


class _FakeClient:
    """Serves decoded fixtures for read; delegates writes to a real dry-run client."""

    def __init__(self) -> None:
        self._writer = FoxESS("stub", transport=_NullTransport())
        self._frames = {65026: EMS_65026, 65034: EMS_MANUAL_65034}

    def read_model(self, addr, model_id):
        fr = reassemble_hex(self._frames[model_id])
        return decode(fr.payload, model_id, addr=addr)

    def write_field(self, *a, **k):
        return self._writer.write_field(*a, **k)


class _NullTransport:
    def close(self) -> None: ...
    def read_data(self, *a, **k):  # pragma: no cover - not used in dry-run
        raise AssertionError("no network in dry-run tests")
    def write_modbus(self, *a, **k):  # pragma: no cover
        raise AssertionError("no network in dry-run tests")


@pytest.fixture
def ems() -> EmsController:
    return EmsController(_FakeClient(), addr=2)


def test_read_ems_state_matches_device(ems):
    st = ems.read()
    assert st.mode_value == 2 and st.mode == "force"
    assert st.min_soc_pct == 10.0
    assert st.max_soc_pct == 100.0
    assert st.charge_by_grid is True
    assert st.charge_by_grid_kw == 11.4
    assert st.backup_soc_offgrid_pct == 20.0


def test_read_force_charge_slot1(ems):
    slot = ems.read_force_charge(1)
    assert slot.enabled is False           # currently disabled on the device
    assert slot.everyday is True
    assert (slot.start_hour, slot.start_min) == (23, 0)
    assert (slot.end_hour, slot.end_min) == (5, 0)
    assert slot.target_soc == 50
    assert slot.power_kw == 3.0


def _assert_valid_0x10(frame_hex: str, *, expect_register: int, expect_value_word: int):
    b = bytes.fromhex(frame_hex)
    assert b[0] == 0x02                      # inverter slave addr
    assert b[1] == 0x10                      # write-multiple function
    register = b[2] << 8 | b[3]
    assert register == expect_register
    num_regs = b[4] << 8 | b[5]
    byte_count = b[6]
    assert byte_count == num_regs * 2
    data = b[7:7 + byte_count]
    assert int.from_bytes(data[:2], "big") == expect_value_word
    # CRC-16/Modbus over everything but the last two bytes, little-endian.
    body = b[:-2]
    assert crc16(body).to_bytes(2, "little") == b[-2:]


def test_set_min_soc_frame(ems):
    # SOCLowerLimit is register 43250 -> modbus reg_addr 43249; S_SF=/10 so 15% -> 150.
    r = ems.set_min_soc(15, dry_run=True)
    _assert_valid_0x10(r.frame_hex, expect_register=43249, expect_value_word=150)
    assert r.sent is False


def test_set_min_soc_rejects_out_of_range(ems):
    with pytest.raises(ValueError):
        ems.set_min_soc(50, dry_run=True)   # firmware cap is 20%


def test_set_work_mode_tou_frame(ems):
    # EMSMode register 43253 -> reg_addr 43252; 'tou' -> 6.
    r = ems.set_work_mode("tou", dry_run=True)
    _assert_valid_0x10(r.frame_hex, expect_register=43252, expect_value_word=WORK_MODES["tou"])


def test_force_charge_orders_enable_last_and_encodes(ems):
    results = ems.force_charge(
        start=(12, 0), end=(15, 0), target_soc=80, power_kw=5.0, slot=1,
        everyday=True, enable=True, dry_run=True,
    )
    # 8 writes, master enable field is last.
    assert len(results) == 8
    assert results[-1].field == "Forced_charging"
    # last frame writes 0xAA (enable=170)
    _assert_valid_0x10(results[-1].frame_hex, expect_register=43613, expect_value_word=170)
    # target SOC 80 encodes as literal 80 (no scale)
    soc_write = next(r for r in results if r.field == "Forced_charging_target_SOC_1")
    _assert_valid_0x10(soc_write.frame_hex, expect_register=43619, expect_value_word=80)
    # power 5.0 kW with P_SF=/100 -> 500
    pwr_write = next(r for r in results if r.field == "Forced_charging_target_Power_1")
    _assert_valid_0x10(pwr_write.frame_hex, expect_register=43620, expect_value_word=500)


def test_writes_blocked_without_confirm_on_live_client():
    live = FoxESS("stub", transport=_NullTransport())          # allow_writes=False
    from foxess.errors import FoxWritesDisabled
    with pytest.raises(FoxWritesDisabled):
        live.ems.set_min_soc(15, confirm=True)                 # not dry-run -> refused

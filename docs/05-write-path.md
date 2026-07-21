# Write Path & Endpoint Inventory (Phase 11)

**Status:** protocol VERIFIED end-to-end — encoder round-trip against captured
frames **and one confirmed, reversible no-op write against the live device**
(§7). Write support is implemented **disabled-by-default, opt-in, dry-run-first**.

## 1. How the UI writes registers

Recovered from the frontend (`sunspec` chunk `editDeviceData` / `genData` /
`genValue`, and the API module in `app.js`).

- **Endpoint:** `POST /api/v1/sunspec/modbus_rw`
- **Body:** `{"cmd": "<hex modbus frame>"}`
- **Frame:** Modbus **Write Multiple Registers (function 0x10)**:

  ```
  slave(1) | 0x10 | start_register(2) | num_registers(2) | byte_count(1)
           | data(byte_count) | CRC-16/Modbus(2, little-endian)
  ```

  `start_register = reg_addr = (field 1-based register) − 1`.

- **Success:** response `errno == 0` and `data.result[2:4] == "10"` (echoes the
  function code). Write responses carry `mstype: 3` (reads use `mstype: 2`), and
  `data.result` is the standard Modbus 0x10 echo:
  `slave | 10 | start_register(2) | num_registers(2) | CRC(2)`.

### Value encoding (`genData` / `genValue`) — inverse of the decoder

- `ascii`: latin1 bytes, right-padded with `0x00` to the field length.
- `uint` / `int` / `sf`: big-endian integer (2 or 4 bytes; signed for int/sf).
- Scale factors are re-applied inversely: a field decoded as `raw / 10^n` is
  encoded as `value × 10^n` (and vice-versa), then rounded.
- `DATE`: `year(2B) month(1B) day(1B)`.

This was verified by round-tripping every captured frame: decode a field, encode
the decoded value, and confirm the bytes are identical (`tests/test_encoder.py`).
Example write frame produced for Device Address = 3 on the inverter:
`02 10 9C84 0001 02 0003 B0EC` (CRC valid, function 0x10).

## 2. Authentication — critical

Writes go through the **same axios client and the same `fox_energy_username`
cookie** as reads. No token, signature, or elevated auth is required. **The
local write API is therefore effectively unauthenticated** — anyone with network
reachability to the device can change inverter/grid/EMS parameters. This is the
single most important item for the threat model: the device MUST be isolated
(dedicated VLAN, firewalled, never exposed to the internet).

## 3. Full endpoint inventory (discovered)

| Method   | Path                                                  | Purpose                         |
| -------- | ----------------------------------------------------- | ------------------------------- |
| GET      | `/api/v1/sunspec/data?addr&id`                        | Read a model (verified)         |
| GET      | `/api/v1/sunspec/devlist`                             | List devices behind the gateway |
| GET      | `/api/v1/sunspec/scanlist`                            | Device scan                     |
| POST     | `/api/v1/sunspec/modbus_rw`                           | **Write registers (0x10)**      |
| GET      | `/api/v1/sunspec/param_get`                           | Read parameters                 |
| POST     | `/api/v1/sunspec/param_set`                           | Set parameters                  |
| POST     | `/api/v1/sunspec/login`                               | Set username cookie             |
| POST     | `/api/v1/sunspec/change_password`                     | Change password                 |
| POST     | `/api/v1/sunspec/reset_password`                      | Reset password                  |
| GET      | `/api/v1/sunspec/sys_info`                            | System info                     |
| GET/POST | `/api/v1/sunspec/net_config`, `net_status`            | Network config/status           |
| POST     | `/api/v1/sunspec/ip_config`, `ap_config`              | IP / AP config                  |
| GET      | `/api/v1/sunspec/log`                                 | Device logs                     |
| GET      | `/api/v1/sunspec/inv_file_list`, `inv_upgrade_status` | Firmware files/status           |
| POST     | `/api/v1/sunspec/upgrade`                             | Firmware upgrade                |

`param_get`/`param_set`, config, and `upgrade` are catalogued for future phases
but **not implemented** — they are higher-risk and need their own evidence pass.

## 4. Safety model (implemented)

`FoxESS.write_field(addr, model_id, field, value, *, confirm, dry_run)`:

- **Disabled by default.** Requires `FoxESS(..., allow_writes=True)`; otherwise
  raises `FoxWritesDisabled`.
- **Explicit confirmation.** Even when enabled, a real write needs `confirm=True`
  or it raises `FoxWriteNotConfirmed`.
- **Dry-run first.** `dry_run=True` builds and returns the exact frame (hex +
  target register) **without sending**, and works even when writes are disabled —
  so you can always preview safely.
- **Read-only guard.** Fields without an `rw` flag raise `FoxWriteNotAllowed`.
- **Range/enum validation.** Values are checked against the field's `hint`
  (e.g. Device Address `1-246`) and enum membership.
- **Structured logging.** Every attempt logs addr/model/field/value/register/
  frame/dry_run to the `foxess.write` logger.
- **No dangerous defaults.** Nothing is written on construction or read paths.

```python
import os
from foxess import FoxESS

fox = FoxESS(os.environ["FOX_HOST"], allow_writes=True)
print(fox.write_field(2, 1, "DA", 3, dry_run=True).frame_hex)  # preview only
# fox.write_field(2, 1, "DA", 3, confirm=True)                 # actually writes
```

## 5. High-risk registers (handle with extreme care)

The register map flags **1,359 writable fields**. Many are grid-protection and
energy-control parameters where wrong values are unsafe or can violate grid
codes: model **704 DER AC Controls**, **705–712** (Volt-Var / Volt-Watt / trip
curves / freq-droop), **65002 Param**, **65010 EMS-TOU**, **65023 ExportLimit**,
**65034 EMS-Manual**, **65012 Time & Country**. These are intentionally **not**
surfaced through any convenience API. Treat all writes as experimental until
validated on a specific firmware, and never expose them casually.

## 7. Confirmed write round-trip (hardware-in-the-loop)

A single **reversible no-op** write was performed to validate the path safely:
the inverter's Device Address (model 1, `DA`) was written back to its _current_
value (2 → 2), so no state changed.

- SDK frame (DA=2): `02 10 9C84 0001 02 0002 712C` — its pre-CRC bytes are
  **byte-for-byte identical** to the frame the device's own frontend builds.
- `POST /api/v1/sunspec/modbus_rw` body `{"cmd":"02109c840001020002712c"}`.
- Response: `{"errno":0,"errmsg":"success","data":{"mstype":3,
"result":"02109C8400016F83"}}` — a valid Modbus 0x10 echo (register 0x9C84,
  1 register written).
- Read-back afterwards: `DA == 2`, unchanged. Fully reversible.

This confirms: the endpoint, the frame format, the SDK encoder, the success
detection (`result[2:4] == "10"`), and the `mstype: 3` write marker.

## 8. Open items

- Characterise `param_set` vs `modbus_rw` (which parameters use which path).
- Determine whether multi-register / `rwl` grouped writes behave identically.
- Investigate cloud-sync side effects of local writes.
- Resolve the `65015 Ileak3Value` scale (see verification status doc).

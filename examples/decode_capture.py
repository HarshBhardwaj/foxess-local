"""Offline example: decode a captured tbl payload with no device present.

Run: python examples/decode_capture.py
"""

from __future__ import annotations

from foxess import decode, reassemble_hex

# Model 702 (DER Capacity) captured from the inverter (addr=2).
TBL = (
    "02036802BE00322C8823A0000823A000082C881AB81AB809600A50083E01DB001C000100020599"
    "496B2C882C880000FFFF00000000FFFFFFFFFFFB2C882C88FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA59D"
)


def main() -> None:
    frame = reassemble_hex(TBL)
    model = decode(frame.payload, 702, addr=2)
    print(f"{model.name} (id={model.id}):")
    print(f"  Active power max rating : {model.get('WMaxRtg')} W")
    print(f"  Apparent power max rating: {model.get('VAMaxRtg')} VA")


if __name__ == "__main__":
    main()

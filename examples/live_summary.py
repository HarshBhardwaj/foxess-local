"""Live example: print a one-line system summary (sync + async).

    export FOX_HOST=192.168.1.38
    python examples/live_summary.py
    # or: python examples/live_summary.py 192.168.1.38
"""

from __future__ import annotations

import asyncio
import os
import sys

from foxess import AsyncFoxESS, FoxESS


def sync_summary(host: str) -> None:
    with FoxESS(host) as fox:
        b, g, s = fox.battery, fox.grid, fox.solar
        print(f"[sync ] SoC {b.soc_percent}% | batt {b.power_w} W | "
              f"solar {s.power_w} W | grid {g.power_w} W @ {g.frequency_hz} Hz")


async def async_summary(host: str) -> None:
    async with AsyncFoxESS(host) as fox:
        b, s = await asyncio.gather(fox.battery(), fox.solar())
        print(f"[async] SoC {b.soc_percent}% | batt {b.power_w} W | solar {s.power_w} W")


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("FOX_HOST", "").strip()
    if not host:
        print(
            "Device IP required: set FOX_HOST or pass it as argv[1]\n"
            "  export FOX_HOST=192.168.1.38 && python examples/live_summary.py",
            file=sys.stderr,
        )
        raise SystemExit(2)
    sync_summary(host)
    asyncio.run(async_summary(host))


if __name__ == "__main__":
    main()

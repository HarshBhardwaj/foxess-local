"""Live example: print a one-line system summary (sync + async).

    python examples/live_summary.py 192.168.1.38
"""

from __future__ import annotations

import asyncio
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
    host = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.38"
    sync_summary(host)
    asyncio.run(async_summary(host))


if __name__ == "__main__":
    main()

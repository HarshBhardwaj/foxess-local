"""Shared fixtures: parse the captured device sweep into (addr, id) records."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "full_sweep_raw.txt"

_BLOCK_RE = re.compile(r"^===== addr=(\d+) id=(\d+) =====\s*$", re.M)


@dataclass(frozen=True)
class SweepRecord:
    addr: int
    model_id: int
    errno: int
    errmsg: str
    reg_addr: int | None
    tbl_hex: str | None


def _parse(text: str) -> dict[tuple[int, int], SweepRecord]:
    parts = _BLOCK_RE.split(text)
    it = iter(parts[1:])
    out: dict[tuple[int, int], SweepRecord] = {}
    for addr_s, id_s, body in zip(it, it, it, strict=False):
        addr, mid = int(addr_s), int(id_s)
        obj = json.loads(body[: body.rindex("}") + 1])
        data = obj.get("data") or {}
        out[(addr, mid)] = SweepRecord(
            addr=addr,
            model_id=mid,
            errno=int(obj.get("errno", -1)),
            errmsg=str(obj.get("errmsg", "")),
            reg_addr=data.get("reg_addr"),
            tbl_hex=data.get("tbl"),
        )
    return out


@pytest.fixture(scope="session")
def sweep() -> dict[tuple[int, int], SweepRecord]:
    return _parse(FIXTURE.read_text())

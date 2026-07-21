"""WebSocket live streaming (Phase 9).

Pushes structured, versioned event envelopes to subscribed clients:

    {"v": 1, "type": "hello|update|event|heartbeat|error",
     "group": "<group>", "ts": <unix>, "data": {...}}

Features: per-connection subscription filtering (``subscribe`` / ``unsubscribe``
control messages), periodic heartbeats, alarm-derived ``faults`` events, and
natural backpressure (sends are awaited; a slow client throttles its own feed).
Version is pinned in every envelope for forward compatibility.
"""

from __future__ import annotations

import asyncio
import contextlib
import dataclasses
from typing import Any

# WebSocket must be importable at module scope so FastAPI can resolve the
# endpoint's string annotation (this module uses `from __future__ import
# annotations`). ws.py is the WebSocket API layer and requires the [api] extra.
from fastapi import WebSocket, WebSocketDisconnect

from .aio import AsyncFoxESS

PROTOCOL_VERSION = 1

# Streamable measurement groups -> AsyncFoxESS coroutine methods.
_MEASUREMENT_GROUPS = ("battery", "grid", "solar", "load", "inverter")
# Non-measurement virtual groups.
_ALL_GROUPS = (*_MEASUREMENT_GROUPS, "system", "faults")


def _envelope(clock: Any, type_: str, group: str, data: Any) -> dict[str, Any]:
    return {"v": PROTOCOL_VERSION, "type": type_, "group": group, "ts": clock(), "data": data}


class _Subscription:
    def __init__(self) -> None:
        self.groups: set[str] = set(_ALL_GROUPS)

    def apply(self, message: dict[str, Any]) -> None:
        action = message.get("action")
        groups = message.get("groups")
        if not isinstance(groups, list):
            return
        valid = {g for g in groups if g in _ALL_GROUPS}
        if action == "subscribe":
            self.groups |= valid
        elif action == "unsubscribe":
            self.groups -= valid
        elif action == "set":
            self.groups = valid


async def _read_group(fox: AsyncFoxESS, group: str) -> Any:
    method = getattr(fox, group)
    view = await method()
    return dataclasses.asdict(view)


async def stream(
    websocket: Any,
    fox: AsyncFoxESS,
    *,
    interval: float = 5.0,
    clock: Any = None,
    max_cycles: int | None = None,
) -> None:
    """Run the streaming loop for one accepted WebSocket connection.

    ``max_cycles`` bounds the loop for tests; ``None`` runs until disconnect.
    """
    import time

    now = clock or time.time
    sub = _Subscription()

    async def receive_control() -> None:
        while True:
            msg = await websocket.receive_json()
            if isinstance(msg, dict):
                sub.apply(msg)

    await websocket.send_json(
        _envelope(
            now,
            "hello",
            "system",
            {"protocol": PROTOCOL_VERSION, "groups": list(_ALL_GROUPS), "interval": interval},
        )
    )

    receiver = asyncio.create_task(receive_control())
    cycles = 0
    try:
        while max_cycles is None or cycles < max_cycles:
            if "system" in sub.groups:
                await websocket.send_json(
                    _envelope(now, "update", "system", await _read_group(fox, "system"))
                )
            for group in _MEASUREMENT_GROUPS:
                if group not in sub.groups:
                    continue
                try:
                    data = await _read_group(fox, group)
                except Exception as exc:  # noqa: BLE001 - report, keep streaming
                    await websocket.send_json(_envelope(now, "error", group, {"error": str(exc)}))
                    continue
                await websocket.send_json(_envelope(now, "update", group, data))
                # alarm-derived fault event
                if group == "inverter" and "faults" in sub.groups:
                    alarm = data.get("alarm")
                    if isinstance(alarm, str) and alarm.strip("0") != "":
                        await websocket.send_json(
                            _envelope(now, "event", "faults", {"alarm": alarm})
                        )
            await websocket.send_json(_envelope(now, "heartbeat", "system", None))
            cycles += 1
            if max_cycles is not None and cycles >= max_cycles:
                break
            await asyncio.sleep(interval)
    finally:
        receiver.cancel()
        with contextlib.suppress(asyncio.CancelledError, Exception):
            await receiver


def register(app: Any, provider: Any) -> None:
    """Attach the ``/api/v1/ws`` endpoint to a FastAPI app."""

    async def ws(websocket: WebSocket) -> None:
        await websocket.accept()
        interval = float(websocket.query_params.get("interval", "5"))
        fox = await provider()
        try:
            await stream(websocket, fox, interval=interval)
        except WebSocketDisconnect:
            pass
        finally:
            await fox.aclose()

    # Prefer add_api_websocket_route over the untyped ``@app.websocket`` decorator
    # so mypy stays clean across versions.
    app.add_api_websocket_route("/api/v1/ws", ws)

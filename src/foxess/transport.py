"""Synchronous HTTP transport for the FoxESS Smart WiLAN local API.

Talks to ``GET /api/v1/sunspec/data?addr=&id=`` and returns the raw envelope.
Read access requires only the ``fox_energy_username`` cookie (see Discovery
Report §9); no token or session is used.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import httpx

from .errors import (
    ERRNO_ID_NOT_FOUND,
    ERRNO_SUCCESS,
    FoxDeviceError,
    FoxModelNotFound,
    FoxProtocolError,
    FoxTimeoutError,
    FoxTransportError,
)

DEFAULT_TIMEOUT = 5.0
DEFAULT_RETRIES = 2
DEFAULT_BACKOFF = 0.5


@dataclass(frozen=True, slots=True)
class DataResponse:
    """A successful ``/data`` envelope."""

    addr: int
    model_id: int
    reg_addr: int
    tbl_hex: str
    mstype: int


class Transport:
    """Blocking transport over a persistent HTTP connection."""

    def __init__(
        self,
        host: str,
        *,
        username: str = "admin",
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        backoff: float = DEFAULT_BACKOFF,
        scheme: str = "http",
        client: httpx.Client | None = None,
    ) -> None:
        self.host = host
        self.base_url = f"{scheme}://{host}"
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self._owns_client = client is None
        self._client = client or httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={"Accept": "application/json, text/plain, */*"},
            cookies={"fox_energy_username": username},
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> Transport:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def read_data(self, addr: int, model_id: int) -> DataResponse:
        """Fetch and validate one model envelope. Raises on device/transport error."""
        params = {"addr": addr, "id": model_id}
        obj = self._get_json("/api/v1/sunspec/data", params)
        errno = int(obj.get("errno", -1))
        if errno != ERRNO_SUCCESS:
            errmsg = str(obj.get("errmsg", ""))
            if errno == ERRNO_ID_NOT_FOUND:
                raise FoxModelNotFound(errno, errmsg, addr, model_id)
            raise FoxDeviceError(errno, errmsg, addr, model_id)
        data = obj.get("data")
        if not isinstance(data, dict) or "tbl" not in data:
            raise FoxProtocolError(f"missing data.tbl in response for ({addr},{model_id})")
        return DataResponse(
            addr=addr,
            model_id=int(data.get("id", model_id)),
            reg_addr=int(data.get("reg_addr", -1)),
            tbl_hex=str(data["tbl"]),
            mstype=int(obj.get("mstype", -1)),
        )

    def write_modbus(self, cmd_hex: str) -> str:
        """POST a Modbus write frame to ``/sunspec/modbus_rw``. Returns the result hex.

        Raises :class:`FoxDeviceError` on a non-zero errno or a result that does
        not echo the write function code (``10``).
        """
        obj = self._post_json("/api/v1/sunspec/modbus_rw", {"cmd": cmd_hex})
        errno = int(obj.get("errno", -1))
        if errno != ERRNO_SUCCESS:
            raise FoxDeviceError(errno, str(obj.get("errmsg", "")))
        data = obj.get("data")
        result = data.get("result", "") if isinstance(data, dict) else ""
        if not (isinstance(result, str) and result[2:4] == "10"):
            raise FoxDeviceError(errno, f"unexpected write result {result!r}")
        return result

    def _post_json(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        try:
            resp = self._client.post(path, json=body)
            resp.raise_for_status()
            parsed: dict[str, Any] = resp.json()
            return parsed
        except httpx.TimeoutException as exc:
            raise FoxTimeoutError(f"timeout on {path}") from exc
        except httpx.HTTPError as exc:
            raise FoxTransportError(f"HTTP error on {path}: {exc}") from exc
        except ValueError as exc:
            raise FoxProtocolError(f"non-JSON response on {path}: {exc}") from exc

    def _get_json(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        last_exc: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                resp = self._client.get(path, params=params)
                resp.raise_for_status()
                parsed: dict[str, Any] = resp.json()
                return parsed
            except httpx.TimeoutException:
                last_exc = FoxTimeoutError(f"timeout on {path} {params}")
            except httpx.HTTPError as exc:
                last_exc = FoxTransportError(f"HTTP error on {path} {params}: {exc}")
            except ValueError as exc:
                last_exc = FoxProtocolError(f"non-JSON response on {path}: {exc}")
                break  # retrying a malformed body is pointless
            if attempt < self.retries:
                time.sleep(self.backoff * (2**attempt))
        assert last_exc is not None
        raise last_exc

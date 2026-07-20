"""Exception hierarchy and device error codes for the FoxESS local SDK."""

from __future__ import annotations


class FoxError(Exception):
    """Base class for all foxess-local errors."""


class FoxTransportError(FoxError):
    """Network/HTTP-level failure talking to the device."""


class FoxTimeoutError(FoxTransportError):
    """The device did not respond within the configured timeout."""


class FoxProtocolError(FoxError):
    """The device replied but the envelope or payload was malformed."""


class FoxCRCError(FoxProtocolError):
    """A Modbus RTU frame inside a ``tbl`` payload failed CRC-16/Modbus."""

    def __init__(self, expected: int, actual: int, frame_index: int) -> None:
        super().__init__(
            f"CRC mismatch on frame {frame_index}: "
            f"expected 0x{expected:04X}, got 0x{actual:04X}"
        )
        self.expected = expected
        self.actual = actual
        self.frame_index = frame_index


class FoxDeviceError(FoxError):
    """The device returned a non-zero ``errno`` in the JSON envelope."""

    def __init__(self, errno: int, errmsg: str, addr: int | None = None,
                 model_id: int | None = None) -> None:
        super().__init__(f"device errno={errno} ({errmsg!r}) addr={addr} id={model_id}")
        self.errno = errno
        self.errmsg = errmsg
        self.addr = addr
        self.model_id = model_id


class FoxModelNotFound(FoxDeviceError):
    """The requested ``(addr, id)`` is not implemented on the device (errno 20002)."""


class FoxUnknownModel(FoxError):
    """The model ID is not present in the register map."""


class FoxWriteError(FoxError):
    """Base class for write-related refusals."""


class FoxWritesDisabled(FoxWriteError):
    """Writes are not enabled on this client (the safe default)."""


class FoxWriteNotConfirmed(FoxWriteError):
    """A write was attempted without explicit confirmation."""


class FoxWriteNotAllowed(FoxWriteError):
    """The target field is read-only or otherwise not writable."""


class FoxWriteRangeError(FoxWriteError):
    """The value is outside the field's documented range."""


# Known device error codes (evidence: captured sweep; extend as discovered).
ERRNO_SUCCESS = 0
ERRNO_ID_NOT_FOUND = 20002

ERRNO_MESSAGES: dict[int, str] = {
    ERRNO_SUCCESS: "success",
    ERRNO_ID_NOT_FOUND: "id not found",
}

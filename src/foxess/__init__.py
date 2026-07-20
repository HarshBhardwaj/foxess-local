"""foxess-local — a fully-local, evidence-first SDK for FoxESS Smart WiLAN.

Public API is intentionally small and stable:

    from foxess import FoxESS, reassemble_hex, decode, default_registry
"""

from __future__ import annotations

from .aio import AsyncFoxESS, AsyncTransport
from .client import ADDR_GATEWAY, ADDR_INVERTER, FoxESS
from .crc import crc16
from .decoder import decode, decode_payload
from .encoder import FoxEncodeError, build_write_frame, encode_field_write
from .errors import (
    FoxCRCError,
    FoxDeviceError,
    FoxError,
    FoxModelNotFound,
    FoxProtocolError,
    FoxTransportError,
    FoxUnknownModel,
    FoxWriteError,
    FoxWriteNotAllowed,
    FoxWriteNotConfirmed,
    FoxWriteRangeError,
    FoxWritesDisabled,
)
from .frame import ModbusFrame, ReassembledFrame, reassemble, reassemble_hex, split_frames
from .measurements import (
    BatteryInfo,
    GridMeasurement,
    InverterStatus,
    LoadInfo,
    SolarInfo,
    SystemInfo,
)
from .models import DecodedField, DecodedModel, FoxField, FoxModelDef, WriteResult
from .mqtt import MqttConfig, MqttPublisher, build_discovery, build_states
from .prometheus import FoxCollector
from .prometheus import render as render_metrics
from .registry import ModelRegistry, default_registry

__version__ = "0.1.0"

__all__ = [
    "ADDR_GATEWAY",
    "ADDR_INVERTER",
    "AsyncFoxESS",
    "AsyncTransport",
    "BatteryInfo",
    "DecodedField",
    "DecodedModel",
    "FoxCRCError",
    "FoxCollector",
    "FoxDeviceError",
    "FoxESS",
    "FoxEncodeError",
    "FoxError",
    "FoxField",
    "FoxModelDef",
    "FoxModelNotFound",
    "FoxProtocolError",
    "FoxTransportError",
    "FoxUnknownModel",
    "FoxWriteError",
    "FoxWriteNotAllowed",
    "FoxWriteNotConfirmed",
    "FoxWriteRangeError",
    "FoxWritesDisabled",
    "WriteResult",
    "build_write_frame",
    "encode_field_write",
    "GridMeasurement",
    "InverterStatus",
    "LoadInfo",
    "ModbusFrame",
    "ModelRegistry",
    "MqttConfig",
    "MqttPublisher",
    "ReassembledFrame",
    "SolarInfo",
    "SystemInfo",
    "build_discovery",
    "build_states",
    "render_metrics",
    "__version__",
    "crc16",
    "decode",
    "decode_payload",
    "default_registry",
    "reassemble",
    "reassemble_hex",
    "split_frames",
]

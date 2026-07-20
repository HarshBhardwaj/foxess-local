"""Model registry: loads the extracted FoxESS register map into typed objects.

The register map (``data/fox_model_defs.json``) was extracted from the device's
own frontend decoder and verified against live device values. See
``docs/02-frontend-decoder-and-register-map.md``.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from functools import lru_cache
from importlib import resources
from typing import Any

from .errors import FoxUnknownModel
from .models import EnumMember, FoxField, FoxModelDef

_DATA_PACKAGE = "foxess.data"
_DATA_FILE = "fox_model_defs.json"


def _field_from_raw(raw: dict[str, Any]) -> FoxField:
    enum_raw = raw.get("enum") or []
    enum = tuple(
        EnumMember(int(m["value"]), str(m["label"]))
        for m in enum_raw
        if "value" in m and "label" in m
    )
    return FoxField(
        name=str(raw.get("name", "")),
        label=str(raw.get("label", "")),
        type=str(raw.get("type", "")),
        length_bytes=int(raw.get("length", 0)),
        show=int(raw.get("show", 0)),
        unit=raw.get("unit"),
        sf_ref=raw.get("sf"),
        rw=raw.get("rw"),
        rwl=raw.get("rwl"),
        hint=raw.get("hint"),
        enum=enum,
        const_value=raw.get("value"),
    )


def _model_from_raw(raw: dict[str, Any]) -> FoxModelDef:
    return FoxModelDef(
        id=int(raw["id"]),
        name=str(raw.get("name", "")),
        start_register=int(raw.get("start", 0)),
        length_registers=int(raw.get("length", 0)),
        report=str(raw.get("report", "")),
        fields=tuple(_field_from_raw(f) for f in raw.get("data", [])),
    )


class ModelRegistry:
    """Immutable registry of model definitions keyed by model ID."""

    def __init__(self, models: dict[int, FoxModelDef]) -> None:
        self._models = models

    @classmethod
    def from_json(cls, text: str) -> ModelRegistry:
        obj = json.loads(text)
        models = {}
        for block in obj.get("block", []):
            model = _model_from_raw(block)
            models[model.id] = model
        return cls(models)

    @classmethod
    def bundled(cls) -> ModelRegistry:
        """Load the register map bundled with the package."""
        text = resources.files(_DATA_PACKAGE).joinpath(_DATA_FILE).read_text("utf-8")
        return cls.from_json(text)

    def __contains__(self, model_id: int) -> bool:
        return model_id in self._models

    def __iter__(self) -> Iterator[FoxModelDef]:
        return iter(self._models.values())

    def __len__(self) -> int:
        return len(self._models)

    def get(self, model_id: int) -> FoxModelDef:
        try:
            return self._models[model_id]
        except KeyError:
            raise FoxUnknownModel(f"model id {model_id} not in register map") from None

    @property
    def ids(self) -> tuple[int, ...]:
        return tuple(sorted(self._models))


@lru_cache(maxsize=1)
def default_registry() -> ModelRegistry:
    """Return the process-wide bundled registry (cached)."""
    return ModelRegistry.bundled()

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pf.config.loader import load_yaml


@dataclass(frozen=True)
class FieldSpec:
    """Definition of a canonical field and provider mappings."""

    variable_name: str
    short_name: str
    long_name: str
    description: str
    dtype: str
    shape: str
    providers: dict[str, str]


@dataclass(frozen=True)
class FieldCatalog:
    """Catalog of canonical fields."""

    fields: tuple[FieldSpec, ...]

    def fields_for_provider(self, provider: str) -> dict[str, FieldSpec]:
        mapping: dict[str, FieldSpec] = {}
        for field in self.fields:
            provider_key = field.providers.get(provider)
            if provider_key:
                mapping[provider_key] = field
        return mapping


def _parse_field(raw: dict[str, Any]) -> FieldSpec:
    return FieldSpec(
        variable_name=raw["variable_name"],
        short_name=raw["short_name"],
        long_name=raw["long_name"],
        description=raw["description"],
        dtype=raw["dtype"],
        shape=raw["shape"],
        providers=raw.get("providers", {}),
    )


def load_field_catalog(path: str | Path) -> FieldCatalog:
    """Load a field catalog from YAML.

    Args:
        path: Path to the field catalog configuration.

    Returns:
        FieldCatalog instance.
    """

    data = load_yaml(path)
    fields = tuple(_parse_field(raw) for raw in data.get("fields", []))
    return FieldCatalog(fields=fields)

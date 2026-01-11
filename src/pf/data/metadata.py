from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

from pf.config.loader import load_yaml


class FieldSpec(BaseModel):
    """Definition of a canonical field and provider mappings."""

    variable_name: str
    short_name: str
    long_name: str
    description: str
    dtype: str
    shape: str
    providers: dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class FieldCatalog(BaseModel):
    """Catalog of canonical fields."""

    fields: tuple[FieldSpec, ...]

    model_config = ConfigDict(frozen=True)

    def fields_for_provider(self, provider: str) -> dict[str, FieldSpec]:
        mapping: dict[str, FieldSpec] = {}
        for field in self.fields:
            provider_key = field.providers.get(provider)
            if provider_key:
                mapping[provider_key] = field
        return mapping

    @field_validator("fields")
    @classmethod
    def ensure_unique_variables(cls, fields: tuple[FieldSpec, ...]) -> tuple[FieldSpec, ...]:
        seen = set()
        for field in fields:
            if field.variable_name in seen:
                raise ValueError(f"Duplicate variable_name: {field.variable_name}")
            seen.add(field.variable_name)
        return fields


def load_field_catalog(path: str | Path) -> FieldCatalog:
    """Load a field catalog from YAML."""

    data = load_yaml(path)
    return FieldCatalog.model_validate(data)

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, field_validator

from pf.config.loader import load_yaml


class AssetUniverse(BaseModel):
    """Configured universe of asset tickers."""

    assets: tuple[str, ...]

    model_config = ConfigDict(frozen=True)

    @field_validator("assets")
    @classmethod
    def normalize_assets(cls, assets: tuple[str, ...]) -> tuple[str, ...]:
        normalized = {asset.strip().upper() for asset in assets}
        return tuple(sorted(normalized))


def load_asset_universe(path: str | Path) -> AssetUniverse:
    """Load an asset universe YAML file.

    Args:
        path: Path to the asset universe configuration.

    Returns:
        AssetUniverse with sorted unique tickers.
    """

    data = load_yaml(path)
    assets = tuple(data.get("assets", []))
    return AssetUniverse.model_validate({"assets": assets})

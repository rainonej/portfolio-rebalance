from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pf.config.loader import load_yaml


@dataclass(frozen=True)
class AssetUniverse:
    """Configured universe of asset tickers."""

    assets: tuple[str, ...]



def load_asset_universe(path: str | Path) -> AssetUniverse:
    """Load an asset universe YAML file.

    Args:
        path: Path to the asset universe configuration.

    Returns:
        AssetUniverse with sorted unique tickers.
    """

    data = load_yaml(path)
    assets = sorted({asset.strip().upper() for asset in data.get("assets", [])})
    return AssetUniverse(assets=tuple(assets))

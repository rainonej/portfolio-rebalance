"""Data configuration loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pf.config.loader import load_yaml
from pf.constants import DEFAULT_CACHE_DIR
from pf.data.assets import AssetUniverse, load_asset_universe


@dataclass(frozen=True)
class DataFetchConfig:
    """Configuration for provider data fetching."""

    provider: str
    frequency: str
    assets: AssetUniverse
    start_date: str
    end_date: str
    output_path: Path
    cache_dir: Path
    use_cache: bool
    force_refresh: bool


def _resolve_assets(raw: dict[str, Any]) -> AssetUniverse:
    assets_source = raw.get("assets_source")
    if assets_source:
        return load_asset_universe(assets_source)
    assets = raw.get("assets", [])
    return AssetUniverse(assets=tuple(sorted({asset.upper() for asset in assets})))


def load_data_fetch_config(path: str | Path) -> DataFetchConfig:
    """Load a data fetch configuration file."""

    raw = load_yaml(path)
    assets = _resolve_assets(raw)
    cache_dir = Path(raw.get("cache_dir", DEFAULT_CACHE_DIR))
    return DataFetchConfig(
        provider=raw["provider"],
        frequency=raw["frequency"],
        assets=assets,
        start_date=raw["start_date"],
        end_date=raw["end_date"],
        output_path=Path(raw["output_path"]),
        cache_dir=cache_dir,
        use_cache=raw.get("use_cache", True),
        force_refresh=raw.get("force_refresh", False),
    )

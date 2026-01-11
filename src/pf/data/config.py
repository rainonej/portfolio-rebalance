from __future__ import annotations

from pathlib import Path
from typing import Any

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from pf.config.loader import load_yaml
from pf.constants import DEFAULT_CACHE_DIR
from pf.data.assets import AssetUniverse, load_asset_universe


Frequency = Literal["daily"]


class DataFetchConfig(BaseModel):
    provider: str
    frequency: Frequency
    assets: AssetUniverse
    start_date: str
    end_date: str
    output_path: Path
    cache_dir: Path = Field(default_factory=lambda: DEFAULT_CACHE_DIR)
    use_cache: bool = True
    force_refresh: bool = False

    model_config = ConfigDict(frozen=True)


def _resolve_assets(raw: dict[str, Any]) -> AssetUniverse:
    assets_source = raw.get("assets_source")
    if assets_source:
        return load_asset_universe(assets_source)
    assets = raw.get("assets", [])
    return AssetUniverse.model_validate({"assets": tuple(assets)})


def load_data_fetch_config(path: str | Path) -> DataFetchConfig:
    """Load a data fetch configuration file."""

    raw = load_yaml(path)
    assets = _resolve_assets(raw)
    resolved = {
        **raw,
        "assets": assets,
        "output_path": Path(raw["output_path"]),
        "cache_dir": Path(raw.get("cache_dir", DEFAULT_CACHE_DIR)),
    }
    return DataFetchConfig.model_validate(resolved)

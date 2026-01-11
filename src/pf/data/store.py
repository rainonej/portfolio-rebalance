"""Cache storage for provider data."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Callable

import pandas as pd

from pf.constants import DEFAULT_CACHE_DIR


@dataclass(frozen=True)
class DataRequest:
    """Definition of a data request for caching."""

    provider: str
    symbols: tuple[str, ...]
    start_date: str
    end_date: str
    frequency: str

    def cache_key(self) -> str:
        payload = "|".join(
            [
                self.provider,
                ",".join(self.symbols),
                self.start_date,
                self.end_date,
                self.frequency,
            ]
        )
        return sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CachePaths:
    """Cache paths for request metadata and data."""

    data_path: Path
    metadata_path: Path


@dataclass(frozen=True)
class CacheResult:
    """Return type for cache operations."""

    frame: pd.DataFrame
    from_cache: bool


def _cache_paths(cache_dir: Path, request: DataRequest) -> CachePaths:
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = request.cache_key()
    return CachePaths(
        data_path=cache_dir / f"{key}.parquet",
        metadata_path=cache_dir / f"{key}.json",
    )


def load_or_fetch(
    request: DataRequest,
    fetcher: Callable[[], pd.DataFrame],
    cache_dir: Path | None = None,
    use_cache: bool = True,
    force_refresh: bool = False,
) -> CacheResult:
    """Load cached data or fetch and cache it.

    Args:
        request: DataRequest describing the query.
        fetcher: Callable to fetch data if cache is missing.
        cache_dir: Directory for cached data.
        use_cache: Whether to use cached data if available.
        force_refresh: Whether to ignore cache and fetch fresh data.

    Returns:
        CacheResult with the dataframe and cache flag.
    """

    cache_dir = cache_dir or DEFAULT_CACHE_DIR
    paths = _cache_paths(cache_dir, request)

    if use_cache and not force_refresh and paths.data_path.exists():
        frame = pd.read_parquet(paths.data_path)
        return CacheResult(frame=frame, from_cache=True)

    frame = fetcher()
    frame.to_parquet(paths.data_path, index=False)
    paths.metadata_path.write_text(
        pd.Series(asdict(request)).to_json(), encoding="utf-8"
    )
    return CacheResult(frame=frame, from_cache=False)

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from pf.constants import DEFAULT_CACHE_DIR
from pf.data.providers.base import Frequency, ProviderPriceRequest
from pf.data.providers.registry import provider_registry
from pf.data.schemas import canonicalize_prices, validate_price_frame
from pf.data.store import DataRequest, load_or_fetch


@dataclass(frozen=True)
class FetchResult:
    """Result of a provider fetch."""

    frame: pd.DataFrame
    from_cache: bool


def fetch_prices(
    provider_name: str,
    symbols: tuple[str, ...],
    start_date: str,
    end_date: str,
    frequency: Frequency,
    cache_dir: Path | None = None,
    use_cache: bool = True,
    force_refresh: bool = False,
) -> FetchResult:
    """Fetch prices from a provider with caching and schema checks.

    Args:
        provider_name: Provider key (e.g., "stooq").
        symbols: Asset tickers (e.g., ("AAPL", "MSFT")).
        start_date: ISO-8601 date string (YYYY-MM-DD).
        end_date: ISO-8601 date string (YYYY-MM-DD).
        frequency: Data frequency. Supported values: "daily".
        cache_dir: Directory for cached data.
        use_cache: Whether to reuse cached data if available.
        force_refresh: Whether to bypass cache and re-fetch.
    """

    provider = provider_registry.get(provider_name)
    request = ProviderPriceRequest(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
    )

    data_request = DataRequest(
        provider=provider_name,
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
    )

    cache_dir = cache_dir or DEFAULT_CACHE_DIR

    def _fetch() -> pd.DataFrame:
        frame = provider.fetch_prices(request)
        frame = canonicalize_prices(frame)
        result = validate_price_frame(frame)
        if not result.is_valid:
            message = "; ".join(result.errors)
            raise ValueError(f"Provider {provider_name} returned invalid data: {message}")
        return frame

    cached = load_or_fetch(
        data_request,
        _fetch,
        cache_dir=cache_dir,
        use_cache=use_cache,
        force_refresh=force_refresh,
    )
    return FetchResult(frame=cached.frame, from_cache=cached.from_cache)

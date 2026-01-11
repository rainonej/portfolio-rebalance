"""Provider interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

import pandas as pd

Frequency = Literal["daily"]


@dataclass(frozen=True)
class ProviderPriceRequest:
    """Request details for provider price fetches.

    Args:
        symbols: Asset tickers (e.g., "AAPL").
        start_date: ISO-8601 date string (YYYY-MM-DD).
        end_date: ISO-8601 date string (YYYY-MM-DD).
        frequency: Data frequency. Supported values: "daily".
    """

    symbols: tuple[str, ...]
    start_date: str
    end_date: str
    frequency: Frequency


class DataProvider(Protocol):
    """Protocol for price providers."""

    name: str

    def fetch_prices(self, request: ProviderPriceRequest) -> pd.DataFrame:
        """Fetch price data for the given request."""
        raise NotImplementedError

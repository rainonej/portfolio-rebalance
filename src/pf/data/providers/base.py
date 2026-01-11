"""Provider interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


@dataclass(frozen=True)
class ProviderPriceRequest:
    """Request details for provider price fetches."""

    symbols: tuple[str, ...]
    start_date: str
    end_date: str
    frequency: str


class DataProvider(Protocol):
    """Protocol for price providers."""

    name: str

    def fetch_prices(self, request: ProviderPriceRequest) -> pd.DataFrame:
        """Fetch price data for the given request."""
        raise NotImplementedError

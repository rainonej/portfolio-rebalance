"""Canonical data schemas for provider outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

PRICE_COLUMNS = (
    "date",
    "symbol",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
)


@dataclass(frozen=True)
class SchemaValidationResult:
    """Validation result for schema checks."""

    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors



def canonicalize_prices(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a canonicalized price frame.

    Ensures column ordering and sort by symbol/date.
    """

    frame = frame.copy()
    frame = frame[list(PRICE_COLUMNS)]
    frame["date"] = pd.to_datetime(frame["date"], utc=True)
    frame = frame.sort_values(["symbol", "date"]).reset_index(drop=True)
    return frame


def validate_price_frame(frame: pd.DataFrame) -> SchemaValidationResult:
    """Validate that a price dataframe conforms to the canonical schema.

    Args:
        frame: Dataframe of price data.

    Returns:
        SchemaValidationResult with any errors.
    """

    errors: list[str] = []
    missing = [col for col in PRICE_COLUMNS if col not in frame.columns]
    if missing:
        errors.append(f"Missing columns: {missing}")
        return SchemaValidationResult(errors=tuple(errors))

    if frame["symbol"].isna().any():
        errors.append("Symbol column contains nulls.")

    if frame["date"].isna().any():
        errors.append("Date column contains nulls.")

    numeric_cols: Iterable[str] = [
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]
    for col in numeric_cols:
        if frame[col].isna().any():
            errors.append(f"Column {col} contains nulls.")

    return SchemaValidationResult(errors=tuple(errors))

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
    columns: list[str] = list(PRICE_COLUMNS)
    frame = frame.loc[:, columns]
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

    if bool(frame["symbol"].isna().any()):
        errors.append("Symbol column contains nulls.")

    if bool(frame["date"].isna().any()):
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
        # Null checks for numeric columns
        if bool(frame[col].isna().any()):
            errors.append(f"Column {col} contains nulls.")

        # Ensure values are numeric by attempting conversion
        numeric_series = pd.to_numeric(frame[col], errors="coerce")
        non_numeric_mask = numeric_series.isna() & frame[col].notna()
        if bool(non_numeric_mask.any()):
            errors.append(f"Column {col} contains non-numeric values.")

        # Basic range validation: numeric columns should not be negative
        negative_mask = numeric_series < 0
        # Ignore NaNs introduced by coercion when checking ranges
        if bool(negative_mask.fillna(False).any()):
            errors.append(f"Column {col} contains negative values, which are invalid.")

    # Check for duplicate (date, symbol) pairs, which can indicate data quality issues
    if bool(frame.duplicated(subset=["date", "symbol"]).any()):
        errors.append("Duplicate (date, symbol) pairs detected.")
    return SchemaValidationResult(errors=tuple(errors))

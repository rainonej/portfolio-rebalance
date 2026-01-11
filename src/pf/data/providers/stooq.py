"""Stooq data provider implementation."""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

import pandas as pd
import requests

from pf.data.providers.base import ProviderPriceRequest
from pf.data.schemas import PRICE_COLUMNS


@dataclass
class StooqProvider:
    """Provider for Stooq daily price data."""

    name: str = "stooq"

    def fetch_prices(self, request: ProviderPriceRequest) -> pd.DataFrame:
        frames: list[pd.DataFrame] = []
        for symbol in request.symbols:
            stooq_symbol = _to_stooq_symbol(symbol)
            csv_text = _download_csv(stooq_symbol, request.frequency)
            frame = pd.read_csv(StringIO(csv_text))
            frame = _normalize_frame(frame, symbol)
            frame = _filter_dates(frame, request.start_date, request.end_date)
            frames.append(frame)

        if not frames:
            return pd.DataFrame(columns=list(PRICE_COLUMNS))

        combined = pd.concat(frames, ignore_index=True)
        return combined


def _to_stooq_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if "." in symbol:
        return symbol
    return f"{symbol}.US"


def _download_csv(symbol: str, frequency: str) -> str:
    if frequency != "daily":
        raise ValueError(f"Unsupported frequency for Stooq: {frequency}")
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def _normalize_frame(frame: pd.DataFrame, symbol: str) -> pd.DataFrame:
    rename_map = {
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    }
    frame = frame.rename(columns=rename_map)
    frame["symbol"] = symbol
    frame["adj_close"] = frame["close"]
    for column in ["open", "high", "low", "close", "adj_close", "volume"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame = frame[list(PRICE_COLUMNS)]
    return frame


def _filter_dates(frame: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame["date"], utc=True)
    mask = (frame["date"] >= pd.to_datetime(start_date, utc=True)) & (
        frame["date"] <= pd.to_datetime(end_date, utc=True)
    )
    return frame.loc[mask].reset_index(drop=True)

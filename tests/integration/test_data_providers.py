"""Contract tests for data providers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from pf.data.assets import load_asset_universe
from pf.data.fetch import fetch_prices
from pf.data.metadata import load_field_catalog
from pf.data.providers.registry import provider_registry
from pf.data.schemas import canonicalize_prices, validate_price_frame

ASSET_CONFIG = Path("configs/data/asset_universe.yaml")
FIELD_CONFIG = Path("configs/data/fields.yaml")
GOLDEN_PATH = Path("tests/data/golden/stooq_aapl_2010_01_04_2010_01_08.csv")
GOLDEN_SYMBOL = "AAPL"
GOLDEN_START = "2010-01-04"
GOLDEN_END = "2010-01-08"


@pytest.mark.long
@pytest.mark.parametrize("provider_name", provider_registry.names())
def test_provider_prices_schema(provider_name: str) -> None:
    assets = load_asset_universe(ASSET_CONFIG)
    symbols = assets.assets[:2]
    result = fetch_prices(
        provider_name,
        symbols=symbols,
        start_date=GOLDEN_START,
        end_date=GOLDEN_END,
        frequency="daily",
    )
    validation = validate_price_frame(result.frame)
    assert validation.is_valid, f"Schema errors: {validation.errors}"
    assert not result.frame.empty


@pytest.mark.long
@pytest.mark.parametrize("provider_name", provider_registry.names())
def test_provider_fields_exist(provider_name: str) -> None:
    catalog = load_field_catalog(FIELD_CONFIG)
    provider_fields = catalog.fields_for_provider(provider_name)
    result = fetch_prices(
        provider_name,
        symbols=(GOLDEN_SYMBOL,),
        start_date=GOLDEN_START,
        end_date=GOLDEN_END,
        frequency="daily",
    )
    for provider_key in provider_fields:
        assert provider_key in result.frame.columns


@pytest.mark.long
@pytest.mark.parametrize("provider_name", provider_registry.names())
def test_provider_assets_exist(provider_name: str) -> None:
    """Test that provider can fetch data for assets without error.

    Note: Some assets may not have data for the test date range (e.g., TSLA IPO'd
    in June 2010, META in May 2012), so we only verify that the request succeeds
    and returns valid data for symbols that exist in that period.
    """
    assets = load_asset_universe(ASSET_CONFIG)
    result = fetch_prices(
        provider_name,
        symbols=assets.assets,
        start_date=GOLDEN_START,
        end_date=GOLDEN_END,
        frequency="daily",
    )
    # Verify the request succeeded and returned valid schema
    validation = validate_price_frame(result.frame)
    assert validation.is_valid, f"Schema errors: {validation.errors}"
    # Verify that at least some symbols were found (not all may exist for this date range)
    symbols_found = set(result.frame["symbol"].unique())
    assert len(symbols_found) > 0, "No symbols found in result"
    # Verify that all found symbols were requested
    assert symbols_found.issubset(set(assets.assets)), f"Found unexpected symbols: {symbols_found - set(assets.assets)}"


@pytest.mark.long
@pytest.mark.parametrize("provider_name", provider_registry.names())
def test_provider_matches_golden(provider_name: str) -> None:
    expected = pd.read_csv(GOLDEN_PATH)
    if expected.empty:
        pytest.skip("Golden file is empty; regenerate with scripts/generate_golden.py")
    result = fetch_prices(
        provider_name,
        symbols=(GOLDEN_SYMBOL,),
        start_date=GOLDEN_START,
        end_date=GOLDEN_END,
        frequency="daily",
    )
    expected = canonicalize_prices(expected)
    actual = canonicalize_prices(result.frame)
    pd.testing.assert_frame_equal(actual, expected)

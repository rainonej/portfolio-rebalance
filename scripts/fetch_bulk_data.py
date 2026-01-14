"""Bulk data fetching script with caching support."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from pf.data.config import load_data_fetch_config
from pf.data.fetch import fetch_prices


def main() -> None:
    """Fetch bulk data using configuration file."""
    parser = argparse.ArgumentParser(description="Fetch bulk market data with caching support")
    parser.add_argument(
        "config",
        type=str,
        help="Path to data fetch configuration YAML file",
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Force refresh even if cached data exists",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching (fetch fresh data but don't save to cache)",
    )

    args = parser.parse_args()

    # Load configuration
    config = load_data_fetch_config(args.config)

    print("=" * 60)
    print("BULK DATA FETCH")
    print("=" * 60)
    print(f"Provider: {config.provider}")
    print(f"Frequency: {config.frequency}")
    print(f"Date range: {config.start_date} to {config.end_date}")
    print(f"Assets: {len(config.assets.assets)}")
    print(f"Output: {config.output_path}")
    print(f"Cache dir: {config.cache_dir}")
    print(f"Use cache: {config.use_cache and not args.no_cache}")
    print(f"Force refresh: {args.force_refresh or config.force_refresh}")
    print()

    # Determine cache settings
    use_cache = config.use_cache and not args.no_cache
    force_refresh = args.force_refresh or config.force_refresh

    # Fetch data
    print("Fetching data...")
    result = fetch_prices(
        provider_name=config.provider,
        symbols=config.assets.assets,
        start_date=config.start_date,
        end_date=config.end_date,
        frequency=config.frequency,
        cache_dir=config.cache_dir,
        use_cache=use_cache,
        force_refresh=force_refresh,
    )

    print("\nFetch complete!")
    print(f"  Rows: {len(result.frame):,}")
    print(f"  Symbols: {result.frame['symbol'].nunique()}")
    print(f"  From cache: {result.from_cache}")

    # Save to output path
    output_path = Path(config.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.frame.to_parquet(output_path, index=False)

    print(f"\nSaved to: {output_path}")
    print(f"File size: {output_path.stat().st_size / (1024**2):.2f} MB")

    # Show summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    summary = (
        result.frame.groupby("symbol")
        .agg(
            {
                "date": ["min", "max", "count"],
                "close": ["min", "max", "mean"],
                "volume": ["mean"],
            }
        )
        .round(2)
    )

    print("\nPer-symbol statistics (first 10):")
    print(summary.head(10).to_string())

    # Check for data quality issues
    print("\n" + "=" * 60)
    print("DATA QUALITY CHECKS")
    print("=" * 60)

    issues = []

    # Check for missing symbols
    missing_symbols = set(config.assets.assets) - set(result.frame["symbol"].unique())
    if missing_symbols:
        issues.append(f"Missing symbols: {sorted(missing_symbols)}")

    # Check for missing dates
    date_range = pd.date_range(
        start=config.start_date,
        end=config.end_date,
        freq="D",
    )
    for symbol in result.frame["symbol"].unique()[:5]:  # Check first 5
        symbol_dates = set(result.frame[result.frame["symbol"] == symbol]["date"])
        expected_trading_days = len([d for d in date_range if d.weekday() < 5])  # Weekdays
        actual_days = len(symbol_dates)
        if actual_days < expected_trading_days * 0.9:  # Allow 10% missing
            issues.append(
                f"{symbol}: Only {actual_days}/{expected_trading_days} expected trading days"
            )

    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No major issues detected.")


if __name__ == "__main__":
    main()

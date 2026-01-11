"""Fetch provider data via config and write parquet output."""

from __future__ import annotations

from pathlib import Path

from pf.data.config import load_data_fetch_config
from pf.data.fetch import fetch_prices


def main() -> None:
    config_path = Path("configs/data/stooq_daily.yaml")
    config = load_data_fetch_config(config_path)
    result = fetch_prices(
        config.provider,
        symbols=config.assets.assets,
        start_date=config.start_date,
        end_date=config.end_date,
        frequency=config.frequency,
        cache_dir=config.cache_dir,
        use_cache=config.use_cache,
        force_refresh=config.force_refresh,
    )
    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    result.frame.to_parquet(config.output_path, index=False)
    print(
        f"Wrote {len(result.frame)} rows to {config.output_path} (from_cache={result.from_cache})"
    )


if __name__ == "__main__":
    main()

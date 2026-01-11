"""Generate provider golden files for contract tests."""

from __future__ import annotations

from pathlib import Path

from pf.data.fetch import fetch_prices

GOLDEN_PATH = Path("tests/data/golden/stooq_aapl_2010_01_04_2010_01_08.csv")


def main() -> None:
    result = fetch_prices(
        "stooq",
        symbols=("AAPL",),
        start_date="2010-01-04",
        end_date="2010-01-08",
        frequency="daily",
        force_refresh=True,
    )
    GOLDEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.frame.to_csv(GOLDEN_PATH, index=False)
    print(f"Wrote {len(result.frame)} rows to {GOLDEN_PATH}")


if __name__ == "__main__":
    main()

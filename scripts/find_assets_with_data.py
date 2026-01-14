"""Find assets with continuous data for the specified date range."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from pf.data.fetch import fetch_prices

# Target date range: 10 years prior to 2025-12-12
END_DATE = "2025-12-12"
START_DATE = (datetime(2025, 12, 12) - timedelta(days=365 * 10)).strftime("%Y-%m-%d")

# Diverse list of potential assets across sectors
# Large cap, mid cap, different sectors, different industries
CANDIDATE_ASSETS = [
    # Technology
    "AAPL",
    "MSFT",
    "GOOGL",
    "GOOG",
    "AMZN",
    "META",
    "NVDA",
    "INTC",
    "AMD",
    "CRM",
    "ORCL",
    "ADBE",
    "CSCO",
    "AVGO",
    "TXN",
    "QCOM",
    "NOW",
    "INTU",
    "AMAT",
    "MU",
    # Finance
    "JPM",
    "BAC",
    "WFC",
    "C",
    "GS",
    "MS",
    "BLK",
    "SCHW",
    "AXP",
    "COF",
    "USB",
    "PNC",
    "TFC",
    "BK",
    "STT",
    "CFG",
    "HBAN",
    "KEY",
    "MTB",
    "ZION",
    # Healthcare
    "JNJ",
    "UNH",
    "PFE",
    "ABT",
    "TMO",
    "ABBV",
    "MRK",
    "BMY",
    "AMGN",
    "GILD",
    "CVS",
    "CI",
    "HUM",
    "CNC",
    "ELV",
    "HCA",
    "DVA",
    "UHS",
    "THC",
    "ENSG",
    # Consumer
    "WMT",
    "HD",
    "MCD",
    "NKE",
    "SBUX",
    "TGT",
    "LOW",
    "TJX",
    "DG",
    "COST",
    "BBY",
    "ROST",
    "DLTR",
    "FIVE",
    "OLLI",
    "DKS",
    "ASO",
    "BGS",
    "CASY",
    "BJ",
    # Industrial
    "BA",
    "CAT",
    "GE",
    "HON",
    "RTX",
    "LMT",
    "NOC",
    "GD",
    "TDG",
    "TXT",
    "EMR",
    "ETN",
    "ITW",
    "PH",
    "ROK",
    "SWK",
    "DOV",
    "GGG",
    "AOS",
    "FAST",
    # Energy
    "XOM",
    "CVX",
    "SLB",
    "EOG",
    "COP",
    "MPC",
    "VLO",
    "PSX",
    "HES",
    "FANG",
    "OVV",
    "CTRA",
    "MRO",
    "APA",
    "DVN",
    "PR",
    "SWN",
    "MTDR",
    "SM",
    "NOG",
    # Materials
    "LIN",
    "APD",
    "ECL",
    "SHW",
    "DD",
    "PPG",
    "FCX",
    "NEM",
    "DOW",
    "VMC",
    "FMC",
    "CF",
    "MOS",
    "NTR",
    "IP",
    "PKG",
    "WRK",
    "SEE",
    "AVY",
    "SLGN",
    # Utilities
    "NEE",
    "DUK",
    "SO",
    "D",
    "AEP",
    "SRE",
    "EXC",
    "XEL",
    "WEC",
    "ES",
    "PEG",
    "ETR",
    "FE",
    "AEE",
    "CMS",
    "LNT",
    "ATO",
    "CNP",
    "NI",
    "OGE",
    # Real Estate
    "AMT",
    "PLD",
    "EQIX",
    "PSA",
    "WELL",
    "VICI",
    "SPG",
    "O",
    "EXPI",
    "CBRE",
    "IRM",
    "AVB",
    "EQR",
    "MAA",
    "UDR",
    "ESS",
    "CPT",
    "AIRC",
    "INVH",
    "SUI",
    # Communication
    "VZ",
    "T",
    "TMUS",
    "CMCSA",
    "DIS",
    "NFLX",
    "PARA",
    "FOX",
    "FOXA",
    "WBD",
    # Consumer Staples
    "PG",
    "KO",
    "PEP",
    "WMT",
    "COST",
    "TGT",
    "CL",
    "KMB",
    "CHD",
    "CLX",
]

# Approximately 10 years of trading days (accounting for weekends/holidays)
MIN_TRADING_DAYS = 250 * 10


def check_asset_data_quality(symbol: str, start_date: str, end_date: str) -> dict:
    """Check if an asset has sufficient continuous data."""
    try:
        result = fetch_prices(
            "stooq",
            symbols=(symbol,),
            start_date=start_date,
            end_date=end_date,
            frequency="daily",
            use_cache=True,
            force_refresh=False,
        )

        df = result.frame
        if df.empty:
            return {"symbol": symbol, "valid": False, "reason": "No data", "rows": 0}

        # Check for sufficient data points
        if len(df) < MIN_TRADING_DAYS:
            return {
                "symbol": symbol,
                "valid": False,
                "reason": f"Insufficient data: {len(df)} rows (need {MIN_TRADING_DAYS})",
                "rows": len(df),
            }

        # Check for date continuity (no large gaps)
        df = df.sort_values("date")
        date_diffs = df["date"].diff().dt.days
        max_gap = date_diffs.max()

        # Allow gaps up to 10 days (weekends + holidays)
        if max_gap > 10:
            return {
                "symbol": symbol,
                "valid": False,
                "reason": f"Large date gap: {max_gap} days",
                "rows": len(df),
            }

        # Check for missing values in critical columns
        critical_cols = ["open", "high", "low", "close", "volume"]
        missing = df[critical_cols].isna().sum().sum()
        if missing > len(df) * 0.01:  # More than 1% missing
            return {
                "symbol": symbol,
                "valid": False,
                "reason": f"Too many missing values: {missing}",
                "rows": len(df),
            }

        return {
            "symbol": symbol,
            "valid": True,
            "reason": "OK",
            "rows": len(df),
            "start": df["date"].min().strftime("%Y-%m-%d"),
            "end": df["date"].max().strftime("%Y-%m-%d"),
        }

    except Exception as e:
        return {"symbol": symbol, "valid": False, "reason": f"Error: {str(e)[:50]}", "rows": 0}


def main() -> None:
    """Find 100 valid assets with continuous data."""
    print("=" * 60)
    print("FINDING ASSETS WITH CONTINUOUS DATA")
    print("=" * 60)
    print(f"Date range: {START_DATE} to {END_DATE}")
    print(f"Minimum trading days: {MIN_TRADING_DAYS}")
    print(f"Candidate assets: {len(CANDIDATE_ASSETS)}")
    print()

    valid_assets = []
    invalid_assets = []

    for i, symbol in enumerate(CANDIDATE_ASSETS, 1):
        print(f"[{i}/{len(CANDIDATE_ASSETS)}] Checking {symbol}...", end=" ")
        result = check_asset_data_quality(symbol, START_DATE, END_DATE)

        if result["valid"]:
            valid_assets.append(result)
            print(f"[OK] Valid ({result['rows']} rows)")
        else:
            invalid_assets.append(result)
            print(f"[FAIL] {result['reason']}")

        # Stop if we have enough
        if len(valid_assets) >= 100:
            print("\nFound 100 valid assets! Stopping search.")
            break

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Valid assets: {len(valid_assets)}")
    print(f"Invalid assets: {len(invalid_assets)}")

    if valid_assets:
        print("\nValid assets (first 20):")
        for asset in valid_assets[:20]:
            print(f"  {asset['symbol']}: {asset['rows']} rows, {asset['start']} to {asset['end']}")

        # Save to file
        output_file = Path("configs/data/asset_universe_100.yaml")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        symbols = [a["symbol"] for a in valid_assets[:100]]
        content = "assets:\n"
        for symbol in sorted(symbols):
            content += f"  - {symbol}\n"

        output_file.write_text(content, encoding="utf-8")
        print(f"\nSaved {len(symbols)} assets to {output_file}")

    if invalid_assets:
        print("\nInvalid assets (first 10):")
        for asset in invalid_assets[:10]:
            print(f"  {asset['symbol']}: {asset['reason']}")


if __name__ == "__main__":
    main()

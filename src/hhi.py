import argparse
from pathlib import Path
import pandas as pd

try:
    from config import DATA_RAW, DATA_PROCESSED, TABLES
except ImportError:
    from .config import DATA_RAW, DATA_PROCESSED, TABLES


def classify_hhi(value: float) -> str:
    if value < 0.15:
        return "Diversified"
    if value < 0.25:
        return "Moderately diversified"
    return "Least diversified"


def compute_hhi(df: pd.DataFrame,
                value_col: str = "value_added",
                year_col: str = "year",
                sector_col: str = "sector") -> pd.DataFrame:
    required = {year_col, sector_col, value_col}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    tmp = df.copy()
    tmp[value_col] = pd.to_numeric(tmp[value_col], errors="coerce")
    if tmp[value_col].isna().any():
        raise ValueError("Value column contains nonnumeric or missing values.")

    total = tmp.groupby(year_col)[value_col].transform("sum")
    tmp["share"] = tmp[value_col] / total
    tmp["share_sq"] = tmp["share"] ** 2

    out = (
        tmp.groupby(year_col, as_index=False)["share_sq"]
        .sum()
        .rename(columns={"share_sq": "hhi"})
    )
    out["classification"] = out["hhi"].apply(classify_hhi)
    return out


def load_paper_table() -> pd.DataFrame:
    path = DATA_PROCESSED / "hhi_values_from_paper_table3.csv"
    return pd.read_csv(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute HHI for sectoral diversification.")
    parser.add_argument("--input", type=str, default=None,
                        help="CSV with year, sector, value_added.")
    parser.add_argument("--paper-table", action="store_true",
                        help="Print the benchmark HHI table if available in data/processed.")
    args = parser.parse_args()

    TABLES.mkdir(parents=True, exist_ok=True)

    if args.paper_table:
        out = load_paper_table()
        print(out.to_string(index=False))
        out.to_csv(TABLES / "hhi_paper_table3.csv", index=False)
        return

    if args.input is None:
        raise SystemExit("Use --input path/to/gfcf_sector.csv or --paper-table")

    df = pd.read_csv(args.input)
    out = compute_hhi(df)
    out.to_csv(TABLES / "hhi_computed.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()

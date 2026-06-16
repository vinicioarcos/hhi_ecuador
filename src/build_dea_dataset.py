import argparse
from pathlib import Path
import pandas as pd

# Define mapping from WDI series name to DEA input/output name
COLUMN_MAPPING = {
    "year": "factor",
    # Inputs
    "rd_expenditure_pct_gdp": "input_rd_expenditure_pct_gdp",
    "researchers_rd_per_million": "input_researchers_rd_per_million",
    "secure_internet_servers_per_million": "input_secure_internet_servers_per_million",
    "fuel_exports_pct_merchandise": "input_fuel_exports_pct_merchandise",
    "patent_applications_residents": "input_patent_applications_residents",
    "patent_applications_nonresidents": "input_patent_applications_nonresidents",
    # Outputs
    "gdp_constant_2015_usd": "output_gdp_constant_2015_usd",
    "international_tourism_arrivals": "output_international_tourism_arrivals",
    "ict_goods_exports_pct_total": "output_ict_goods_exports_pct_total",
    "scientific_technical_journal_articles": "output_scientific_technical_journal_articles",
    "internet_users_pct_population": "output_internet_users_pct_population"
}

def main() -> None:
    parser = argparse.ArgumentParser(description="Build DEA dataset from raw WDI data.")
    parser.add_argument("--input", default="data/raw/wdi/wdi_uae_2000_2020.csv",
                        help="Path to the raw WDI CSV file.")
    parser.add_argument("--output", default="data/processed/dea_input.csv",
                        help="Path to save the processed DEA CSV file.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Load data
    df = pd.read_csv(input_path)

    # Rename columns to DEA standard (input_* and output_*)
    processed_df = df.rename(columns=COLUMN_MAPPING)

    # Keep only columns defined in the mapping
    cols_to_keep = [col for col in COLUMN_MAPPING.values() if col in processed_df.columns]
    processed_df = processed_df[cols_to_keep]

    print("=== DEA DATASET VALIDATION REPORT ===")
    print(f"Total rows (years): {len(processed_df)}")
    print("\nMissing values count per column:")
    missing_counts = processed_df.isnull().sum()
    for col, count in missing_counts.items():
        pct = (count / len(processed_df)) * 100
        print(f"  - {col}: {count} missing ({pct:.1f}%)")

    # Identify years with missing values for reporting
    print("\nMissing values by year details:")
    for idx, row in processed_df.iterrows():
        year = int(row["factor"])
        missing_cols = [col for col in processed_df.columns if pd.isnull(row[col])]
        if missing_cols:
            print(f"  * Year {year} is missing: {', '.join(missing_cols)}")

    # Ensure output directory exists and save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(output_path, index=False)
    print(f"\nSaved processed DEA dataset to: {output_path}")

if __name__ == "__main__":
    main()

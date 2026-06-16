import argparse
from pathlib import Path
import requests
import pandas as pd

WDI_SERIES = {
    "NY.GDP.MKTP.KD": "gdp_constant_2015_usd",
    "ST.INT.ARVL": "international_tourism_arrivals",
    "TX.VAL.ICTG.ZS.UN": "ict_goods_exports_pct_total",
    "IP.PAT.NRES": "patent_applications_nonresidents",
    "IP.PAT.RESD": "patent_applications_residents",
    "IP.JRN.ARTC.SC": "scientific_technical_journal_articles",
    "TX.VAL.FUEL.ZS.UN": "fuel_exports_pct_merchandise",
    "IT.NET.SECR.P6": "secure_internet_servers_per_million",
    "IT.NET.USER.ZS": "internet_users_pct_population",
    "GB.XPD.RSDV.GD.ZS": "rd_expenditure_pct_gdp",
    "SP.POP.SCIE.RD.P6": "researchers_rd_per_million",
}

def fetch_series(country: str, indicator: str, start: int, end: int) -> pd.DataFrame:
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    params = {"format": "json", "per_page": 20000, "date": f"{start}:{end}"}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    payload = r.json()
    rows = payload[1] or []
    return pd.DataFrame([{"year": int(x["date"]), indicator: x["value"]} for x in rows])

def main() -> None:
    parser = argparse.ArgumentParser(description="Download WDI series for replication.")
    parser.add_argument("--country", default="ARE", help="World Bank ISO3 code. UAE = ARE.")
    parser.add_argument("--start", type=int, default=2000)
    parser.add_argument("--end", type=int, default=2020)
    parser.add_argument("--output", default="data/raw/wdi/wdi_uae_2000_2020.csv")
    args = parser.parse_args()

    merged = None
    for code, name in WDI_SERIES.items():
        df = fetch_series(args.country, code, args.start, args.end).rename(columns={code: name})
        merged = df if merged is None else merged.merge(df, on="year", how="outer")

    merged = merged.sort_values("year")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out, index=False)
    print(f"Saved {out}")

if __name__ == "__main__":
    main()

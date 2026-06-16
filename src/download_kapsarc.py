"""Descarga reproducible de la Formacion Bruta de Capital Fijo (GFCF) de EAU
por actividad economica (ISIC), usada para calcular el HHI del paper.

Fuente: KAPSARC Data Portal (dataset replicado del Federal Competitiveness
and Statistics Centre, FCSC, de EAU), en millones de AED a precios corrientes.
Cubre 18 sectores 2010-2020, los mismos 18 sectores que lista el paper
(Bayanat, 2020).

Salida: data/raw/hhi/gfcf_sector_template.csv con columnas
    year, sector, gross_fixed_capital_formation_million_aed
"""
import argparse
from pathlib import Path

import pandas as pd
import requests

try:
    from config import DATA_RAW
except ImportError:
    from .config import DATA_RAW

API_URL = "https://datasource.kapsarc.org/api/records/1.0/search/"
DATASET = "gross-fixed-capital-formation"
# Agregados que NO son sectores y deben excluirse del HHI.
AGGREGATES = {"Total", "Total Non-oil"}


def fetch_records() -> pd.DataFrame:
    records = []
    start = 0
    while True:
        resp = requests.get(
            API_URL,
            params={"dataset": DATASET, "rows": 100, "start": start},
            timeout=60,
        )
        resp.raise_for_status()
        payload = resp.json()
        batch = payload.get("records", [])
        if not batch:
            break
        records.extend(r["fields"] for r in batch)
        start += 100
        if start >= payload.get("nhits", 0):
            break

    df = pd.DataFrame(records)[["time_period", "isic", "value"]]
    df.columns = ["year", "sector", "gross_fixed_capital_formation_million_aed"]
    df["year"] = df["year"].astype(int)
    df = df[~df["sector"].isin(AGGREGATES)].copy()
    return df.sort_values(["year", "sector"]).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default=str(DATA_RAW / "hhi" / "gfcf_sector_template.csv"),
        help="Ruta de salida del CSV.",
    )
    args = parser.parse_args()

    df = fetch_records()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Guardado {len(df)} filas en {out}")
    print(f"Sectores: {df['sector'].nunique()} | Anios: {sorted(df['year'].unique())}")


if __name__ == "__main__":
    main()

"""Genera la tabla de validacion del HHI: recomputado vs. publicado en el paper.

Cruza el HHI calculado desde los datos PRIMARIOS de EAU (Formacion Bruta de
Capital Fijo por 18 sectores, KAPSARC/FCSC) contra los valores publicados en la
Tabla 3 de Siddiqui & Afzal (2022). El paper solo reporta 2010-2017, asi que el
cruce es por interseccion de anios.

Salida: outputs/tables/hhi_replication_comparison.csv con columnas
    year, hhi_computed, hhi_paper, abs_diff,
    classification_computed, classification_paper

Este archivo es consumido por paper/replication_report.qmd.
"""
import argparse
from pathlib import Path

import pandas as pd

try:
    from config import DATA_RAW, DATA_PROCESSED, TABLES
    from hhi import compute_hhi, classify_hhi
except ImportError:
    from .config import DATA_RAW, DATA_PROCESSED, TABLES
    from .hhi import compute_hhi, classify_hhi

DEFAULT_GFCF = DATA_RAW / "hhi" / "gfcf_sector_template.csv"
PAPER_TABLE = DATA_PROCESSED / "hhi_values_from_paper_table3.csv"


def build_comparison(gfcf_path: Path) -> pd.DataFrame:
    raw = pd.read_csv(gfcf_path)
    computed = compute_hhi(raw)[["year", "hhi"]].rename(columns={"hhi": "hhi_computed"})

    paper = pd.read_csv(PAPER_TABLE).rename(columns={"hhi_paper": "hhi_paper"})
    paper = paper[["year", "hhi_paper"]]

    merged = paper.merge(computed, on="year", how="inner").sort_values("year")
    merged["hhi_computed"] = merged["hhi_computed"].round(4)
    merged["abs_diff"] = (merged["hhi_computed"] - merged["hhi_paper"]).abs().round(5)
    merged["classification_computed"] = merged["hhi_computed"].apply(classify_hhi)
    merged["classification_paper"] = merged["hhi_paper"].apply(classify_hhi)

    return merged[[
        "year", "hhi_computed", "hhi_paper", "abs_diff",
        "classification_computed", "classification_paper",
    ]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gfcf", type=str, default=str(DEFAULT_GFCF),
                        help="CSV de GFCF sectorial de EAU (datos primarios).")
    args = parser.parse_args()

    gfcf_path = Path(args.gfcf)
    if not gfcf_path.exists():
        raise SystemExit(
            f"No existe {gfcf_path}. Ejecute src/download_kapsarc.py primero."
        )

    out = build_comparison(gfcf_path)
    TABLES.mkdir(parents=True, exist_ok=True)
    out_path = TABLES / "hhi_replication_comparison.csv"
    out.to_csv(out_path, index=False)

    print("HHI: recomputado (datos primarios) vs. publicado (Tabla 3):")
    print(out.to_string(index=False))
    print(f"\nDiferencia absoluta maxima: {out['abs_diff'].max():.5f}")
    print(f"Diferencia absoluta media:  {out['abs_diff'].mean():.5f}")
    print(f"Guardado: {out_path}")


if __name__ == "__main__":
    main()

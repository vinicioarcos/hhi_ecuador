"""DEA sectorial para Ecuador usando ramas ISIC como DMU.

Este modelo fortalece la extension Ecuador porque cambia la unidad de decision
desde anos hacia sectores comparables. Usa la misma fuente oficial UNSD que el
HHI: participaciones de valor agregado por siete ramas ISIC.

DMU = sector.
Input = participacion promedio inicial en el VAB.
Output = participacion promedio reciente en el VAB.

La lectura es de eficiencia de transicion sectorial: que ramas mantienen o
amplian su peso reciente dado su peso inicial. Es un DEA parsimonioso para
respetar la regla n_DMU >= 3*(inputs+outputs) con 7 sectores.
"""
from pathlib import Path
import sys

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from config import TABLES
from dea_ccr import dea_ccr_input_oriented


EXCLUDED_COLUMNS = {"year", "hhi", "classification"}


def build_sector_dea_dataset(
    hhi_ecuador: pd.DataFrame,
    initial_years: tuple[int, int] = (2000, 2004),
    recent_years: tuple[int, int] = (2020, 2024),
) -> pd.DataFrame:
    """Build a sector-as-DMU DEA dataset from Ecuador branch shares."""
    required = {"year"}
    missing = required - set(hhi_ecuador.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    sectors = [c for c in hhi_ecuador.columns if c not in EXCLUDED_COLUMNS]
    if not sectors:
        raise ValueError("No sector columns found.")

    initial = hhi_ecuador[
        hhi_ecuador["year"].between(initial_years[0], initial_years[1])
    ][sectors].mean()
    recent = hhi_ecuador[
        hhi_ecuador["year"].between(recent_years[0], recent_years[1])
    ][sectors].mean()

    out = pd.DataFrame(
        {
            "factor": sectors,
            "input_initial_share": [initial[s] for s in sectors],
            "output_recent_share": [recent[s] for s in sectors],
        }
    )
    return out.dropna()


def run_sector_dea(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    input_cols = ["input_initial_share"]
    output_cols = ["output_recent_share"]
    n = len(data)
    threshold = 3 * (len(input_cols) + len(output_cols))
    adequate = n >= threshold

    results = dea_ccr_input_oriented(
        data=data,
        dmu_col="factor",
        input_cols=input_cols,
        output_cols=output_cols,
    )
    merged = data.merge(results, on="factor", how="left")
    merged["share_change"] = merged["output_recent_share"] - merged["input_initial_share"]
    merged["share_ratio"] = merged["output_recent_share"] / merged["input_initial_share"]
    merged = merged.sort_values("efficiency_ccr_input", ascending=False)

    summary = pd.DataFrame(
        [
            {
                "model": "Ecuador_Sector_Transition_DEA",
                "dmu": "sector",
                "n_inputs": len(input_cols),
                "n_outputs": len(output_cols),
                "n_dmu": n,
                "threshold_3x": threshold,
                "adequate": adequate,
                "verdict": "VALIDO" if adequate else "SUBESPECIFICADO",
                "n_efficient": int((merged["efficiency_ccr_input"].round(6) >= 1.0).sum()),
                "mean_efficiency": round(float(merged["efficiency_ccr_input"].mean()), 4),
            }
        ]
    )
    return merged, summary


def main() -> None:
    source = TABLES / "hhi_ecuador.csv"
    if not source.exists():
        raise SystemExit(f"{source} no existe. Ejecute src/ecuador_hhi.py primero.")

    data = build_sector_dea_dataset(pd.read_csv(source))
    results, summary = run_sector_dea(data)

    dataset_path = TABLES / "dea_ecuador_sector_dataset.csv"
    results_path = TABLES / "dea_results_ecuador_sector_transition.csv"
    summary_path = TABLES / "dea_ecuador_sector_summary.csv"
    data.to_csv(dataset_path, index=False)
    results.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)

    print("=== DEA Ecuador: transicion sectorial ===")
    print(summary.to_string(index=False))
    print(results.round(4).to_string(index=False))
    print(f"\nGuardado: {dataset_path}")
    print(f"Guardado: {results_path}")
    print(f"Guardado: {summary_path}")


if __name__ == "__main__":
    main()

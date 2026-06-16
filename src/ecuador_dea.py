"""DEA exploratorio para Ecuador usando ramas ISIC como resultados.

DMU = ano. El modelo pregunta si cada ano logra participaciones altas en ramas
productivas y de servicios usando como input la participacion de mineria y
utilities. No es un DEA de economia del conocimiento completo; es una prueba
de diversificacion productiva con los mismos datos UNSD usados para el HHI.
"""
from pathlib import Path
import sys

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from config import TABLES
from dea_ccr import dea_ccr_input_oriented


INPUTS = ["input_mining_utilities_share"]
OUTPUTS = [
    "output_manufacturing_share",
    "output_transport_communication_share",
    "output_trade_hotels_share",
]


def build_ecuador_dea_dataset(hhi_ecuador: pd.DataFrame) -> pd.DataFrame:
    """Build a DEA-ready dataset from the Ecuador HHI branch-share table."""
    required = {
        "year",
        "Mining & utilities",
        "Manufacturing",
        "Transport & communication",
        "Trade, restaurants & hotels",
    }
    missing = required - set(hhi_ecuador.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = hhi_ecuador.rename(
        columns={
            "year": "factor",
            "Mining & utilities": "input_mining_utilities_share",
            "Manufacturing": "output_manufacturing_share",
            "Transport & communication": "output_transport_communication_share",
            "Trade, restaurants & hotels": "output_trade_hotels_share",
        }
    )[["factor", *INPUTS, *OUTPUTS]].copy()
    out["factor"] = out["factor"].astype(int)
    return out.dropna()


def run_ecuador_dea(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run input-oriented CCR and return results plus a one-row summary."""
    n = len(data)
    threshold = 3 * (len(INPUTS) + len(OUTPUTS))
    adequate = n >= threshold
    results = dea_ccr_input_oriented(
        data=data,
        dmu_col="factor",
        input_cols=INPUTS,
        output_cols=OUTPUTS,
    )
    results["factor"] = results["factor"].astype(int)
    n_efficient = int((results["efficiency_ccr_input"].round(6) >= 1.0).sum())
    mean_efficiency = float(results["efficiency_ccr_input"].mean())
    summary = pd.DataFrame(
        [
            {
                "model": "Ecuador_Diversification_DEA",
                "dmu": "year",
                "n_inputs": len(INPUTS),
                "n_outputs": len(OUTPUTS),
                "n_dmu": n,
                "threshold_3x": threshold,
                "adequate": adequate,
                "verdict": "VALIDO" if adequate else "SUBESPECIFICADO",
                "n_efficient": n_efficient,
                "mean_efficiency": round(mean_efficiency, 4),
            }
        ]
    )
    return results, summary


def main() -> None:
    source = TABLES / "hhi_ecuador.csv"
    if not source.exists():
        raise SystemExit(f"{source} no existe. Ejecute src/ecuador_hhi.py primero.")

    data = build_ecuador_dea_dataset(pd.read_csv(source))
    results, summary = run_ecuador_dea(data)

    TABLES.mkdir(parents=True, exist_ok=True)
    dataset_path = TABLES / "dea_ecuador_dataset.csv"
    results_path = TABLES / "dea_results_ecuador_diversification.csv"
    summary_path = TABLES / "dea_ecuador_summary.csv"
    data.to_csv(dataset_path, index=False)
    results.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)

    print("=== DEA Ecuador: diversificacion productiva ===")
    print(summary.to_string(index=False))
    print(results.round(4).to_string(index=False))
    print(f"\nGuardado: {dataset_path}")
    print(f"Guardado: {results_path}")
    print(f"Guardado: {summary_path}")


if __name__ == "__main__":
    main()

"""DEA de frontera de producción para Ecuador con DMU = sector-año.

Rediseño metodológico (ruta b). El DEA sectorial previo usaba un solo input
(empleo) y un solo output (productividad = VAB/empleo). Eso tenía dos defectos:

1. Con un único input y un único output el CCR colapsa a un simple ranking del
   ratio output/input, sin información más allá de ordenar la productividad.
2. La productividad NO es independiente del input: es exactamente el cociente
   output/input, de modo que el modelo correlaciona una variable consigo misma.

Aquí se especifica una frontera de producción genuina:

    DMU    = sector-año (siete ramas ISIC x ventana común 2018-2023)
    Inputs = empleo (trabajo) y FBKF (capital), dos factores independientes
    Output = valor agregado (VAB)

Agrupar las observaciones sector-año eleva el número de DMU a 7 x 6 = 42, muy
por encima del umbral de adecuación n_DMU >= 3*(inputs + outputs) = 9, de modo
que el modelo deja de estar subespecificado.

Fuente: BCE MEI 2018-2024p (empleo, VAB) y BCE FBKF 1965-2024p (capital),
armonizados a las siete ramas por `src/build_ecuador_sector_metrics.py`.
"""
import argparse
from pathlib import Path
import sys

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_RAW, TABLES
from dea_ccr import dea_ccr_input_oriented
from dea_bootstrap import simar_wilson_bootstrap

PANEL_FILE = DATA_RAW / "ecuador" / "sector_year_panel.csv"
INPUTS = ["input_employment", "input_capital_fbkf"]
BASE_OUTPUTS = ["output_value_added"]


def resolve_outputs(data: pd.DataFrame) -> list[str]:
    """Outputs = valor agregado mas cualquier output_ verificado adicional.

    Si el panel trae columnas `output_` extra (p. ej. `output_exports` una vez
    que exista una serie de exportaciones por rama verificada y completa), el
    modelo las incorpora automaticamente. La regla de adecuacion se recalcula
    con el numero efectivo de outputs.
    """
    extra = [c for c in data.columns if c.startswith("output_") and c not in BASE_OUTPUTS]
    return BASE_OUTPUTS + extra


def run_panel_dea(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run input-oriented CCR on the sector-year production panel."""
    outputs = resolve_outputs(data)
    missing = set(["dmu", *INPUTS, *outputs]) - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    n = len(data)
    threshold = 3 * (len(INPUTS) + len(outputs))
    adequate = n >= threshold

    results = dea_ccr_input_oriented(
        data=data,
        dmu_col="dmu",
        input_cols=INPUTS,
        output_cols=outputs,
    )
    results = data[["dmu", "factor", "year"]].merge(results, on="dmu", how="left")
    results = results.sort_values("efficiency_ccr_input", ascending=False)

    # Eficiencia media por rama: lectura sectorial agregando los años.
    by_sector = (
        results.groupby("factor", as_index=False)["efficiency_ccr_input"]
        .mean()
        .rename(columns={"efficiency_ccr_input": "mean_efficiency_sector"})
        .sort_values("mean_efficiency_sector", ascending=False)
    )

    summary = pd.DataFrame(
        [
            {
                "model": "Ecuador_Production_Frontier_DEA",
                "dmu": "sector-year",
                "n_inputs": len(INPUTS),
                "n_outputs": len(outputs),
                "n_dmu": n,
                "threshold_3x": threshold,
                "adequate": adequate,
                "verdict": "VALIDO" if adequate else "SUBESPECIFICADO",
                "n_efficient": int((results["efficiency_ccr_input"].round(6) >= 1.0).sum()),
                "mean_efficiency": round(float(results["efficiency_ccr_input"].mean()), 4),
                "inputs_used": ", ".join(INPUTS),
                "outputs_used": ", ".join(outputs),
                "coverage_note": (
                    f"Panel sector-año {int(data['year'].min())}-{int(data['year'].max())}; "
                    "trabajo (empleo) y capital (FBKF) como inputs independientes, "
                    "valor agregado como output."
                ),
            }
        ]
    )
    return results, summary, by_sector


def run_bootstrap(data: pd.DataFrame, results: pd.DataFrame,
                  n_boot: int = 2000, alpha: float = 0.05) -> pd.DataFrame:
    """Simar-Wilson bias correction and confidence intervals for the panel DEA."""
    outputs = resolve_outputs(data)
    X = data[INPUTS].to_numpy(dtype=float)
    Y = data[outputs].to_numpy(dtype=float)
    delta = data.merge(results[["dmu", "efficiency_ccr_input"]], on="dmu")[
        "efficiency_ccr_input"
    ].to_numpy(dtype=float)

    boot = simar_wilson_bootstrap(X, Y, delta, n_boot=n_boot, alpha=alpha)
    boot.insert(0, "dmu", data["dmu"].to_numpy())
    boot.insert(1, "factor", data["factor"].to_numpy())
    boot.insert(2, "year", data["year"].to_numpy())
    return boot.sort_values("efficiency_bias_corrected", ascending=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-boot", type=int, default=2000,
                        help="Replicas del bootstrap Simar-Wilson (default 2000).")
    parser.add_argument("--alpha", type=float, default=0.05,
                        help="Nivel para el intervalo de confianza 1-alpha (default 0.05).")
    args = parser.parse_args()

    if not PANEL_FILE.exists():
        raise SystemExit(
            f"{PANEL_FILE} no existe. Ejecute src/build_ecuador_sector_metrics.py primero."
        )

    data = pd.read_csv(PANEL_FILE)
    results, summary, by_sector = run_panel_dea(data)

    print("=== DEA Ecuador: frontera de producción (sector-año) ===")
    print(summary.to_string(index=False))
    print("\nEficiencia media por rama:")
    print(by_sector.round(4).to_string(index=False))

    print(f"\nBootstrap Simar-Wilson ({args.n_boot} replicas)...")
    boot = run_bootstrap(data, results, n_boot=args.n_boot, alpha=args.alpha)
    summary["mean_efficiency_bias_corrected"] = round(
        float(boot["efficiency_bias_corrected"].mean()), 4
    )
    summary["ci_level"] = 1 - args.alpha
    summary["n_boot"] = args.n_boot

    TABLES.mkdir(parents=True, exist_ok=True)
    results_path = TABLES / "dea_results_ecuador_production_frontier.csv"
    summary_path = TABLES / "dea_ecuador_panel_summary.csv"
    sector_path = TABLES / "dea_ecuador_panel_by_sector.csv"
    boot_path = TABLES / "dea_ecuador_panel_bootstrap.csv"
    results.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)
    by_sector.to_csv(sector_path, index=False)
    boot.to_csv(boot_path, index=False)

    print("\nEficiencias corregidas por sesgo (IC bootstrap), top y bottom:")
    cols = ["dmu", "efficiency_ccr_input", "efficiency_bias_corrected", "ci_low", "ci_high"]
    print(pd.concat([boot[cols].head(5), boot[cols].tail(5)]).round(4).to_string(index=False))
    print(f"\nGuardado: {results_path}")
    print(f"Guardado: {summary_path}")
    print(f"Guardado: {sector_path}")
    print(f"Guardado: {boot_path}")


if __name__ == "__main__":
    main()

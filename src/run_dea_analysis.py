"""Ejecuta modelos DEA CCR (input-oriented) sobre los indicadores WDI de EAU.

Rediseno metodologico (Fase 3): el paper original reporta eficiencias de
exactamente 1.0 para sus pilares de economia del conocimiento. Eso es un
artefacto de FALTA DE PODER DISCRIMINANTE: cuando el numero de DMU no supera
holgadamente la suma de inputs y outputs, el modelo DEA clasifica a casi todas
las unidades como eficientes.

Regla empirica de adecuacion (Cooper, Seiford & Tone, 2007):

    n_DMU >= max( m * s , 3 * (m + s) )

donde m = numero de inputs y s = numero de outputs. Aqui usamos el umbral
3*(m+s) y etiquetamos cada modelo como VALIDO o SUBESPECIFICADO.

DMU = ano (cross-section temporal). Se eligen ventanas y variables con
cobertura completa para maximizar el numero de DMU.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from dea_ccr import dea_ccr_input_oriented

# Cada modelo declara inputs/outputs. Los modelos VALIDOS respetan la regla de
# adecuacion; "Table2_Macro_Degenerate" se conserva a proposito para demostrar
# por que el paper obtuvo eficiencias = 1.0.
MODELS = {
    # ICT: infraestructura -> difusion del conocimiento. 2010-2020, n=11.
    # m+s=3 -> umbral 3*(m+s)=9. 11 >= 9  => VALIDO.
    "ICT_Knowledge_Diffusion": {
        "inputs": ["input_secure_internet_servers_per_million"],
        "outputs": [
            "output_internet_users_pct_population",
            "output_scientific_technical_journal_articles",
        ],
        "note": "Infraestructura TIC -> usuarios de internet y articulos cientificos.",
    },
    # Innovacion: esfuerzo en patentes -> producto economico. 2010-2020, n=11.
    # m+s=3 -> umbral 9. 11 >= 9 => VALIDO.
    "Innovation_to_GDP": {
        "inputs": [
            "input_patent_applications_residents",
            "input_patent_applications_nonresidents",
        ],
        "outputs": ["output_gdp_constant_2015_usd"],
        "note": "Solicitudes de patentes (res. y no res.) -> PIB constante.",
    },
    # Macro de transicion: dependencia de combustibles -> resultados de
    # conocimiento. 2000-2020, n=21. m+s=4 -> umbral 12. 21 >= 12 => VALIDO.
    "Diversification_Efficiency": {
        "inputs": ["input_fuel_exports_pct_merchandise"],
        "outputs": [
            "output_gdp_constant_2015_usd",
            "output_scientific_technical_journal_articles",
            "output_internet_users_pct_population",
        ],
        "note": "Menor dependencia de combustibles con mayores resultados de conocimiento.",
    },
    # Replica literal del modelo macro del paper (Tabla 2): 3 inputs + 4 outputs
    # con datos completos solo 2015-2020 (n=6). m+s=7 -> umbral 21. 6 << 21
    # => SUBESPECIFICADO. Se incluye para reproducir la degeneracion del paper.
    "Table2_Macro_Degenerate": {
        "inputs": [
            "input_patent_applications_residents",
            "input_patent_applications_nonresidents",
            "input_fuel_exports_pct_merchandise",
        ],
        "outputs": [
            "output_gdp_constant_2015_usd",
            "output_international_tourism_arrivals",
            "output_ict_goods_exports_pct_total",
            "output_scientific_technical_journal_articles",
        ],
        "note": "Replica del diseno del paper; subespecificado a proposito.",
    },
}


def main() -> None:
    input_file = Path("data/processed/dea_input.csv")
    if not input_file.exists():
        print(f"Error: {input_file} no existe. Ejecute build_dea_dataset.py primero.")
        sys.exit(1)

    df = pd.read_csv(input_file)
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = []
    for name, cols in MODELS.items():
        m, s = len(cols["inputs"]), len(cols["outputs"])
        threshold = 3 * (m + s)

        model_cols = ["factor"] + cols["inputs"] + cols["outputs"]
        model_df = df[model_cols].dropna().copy()
        n = len(model_df)
        adequate = n >= threshold
        verdict = "VALIDO" if adequate else "SUBESPECIFICADO"

        print("\n=========================================")
        print(f"Modelo DEA: {name}  [{verdict}]")
        print(f"  {cols['note']}")
        print(f"  inputs={m} outputs={s} | DMU(anios completos)={n} | umbral 3*(m+s)={threshold}")

        if n == 0:
            print("  Omitido: sin anios con datos completos.")
            continue

        res = dea_ccr_input_oriented(
            model_df, dmu_col="factor",
            input_cols=cols["inputs"], output_cols=cols["outputs"],
        )
        res["factor"] = res["factor"].astype(int)
        n_eff = int((res["efficiency_ccr_input"].round(6) >= 1.0).sum())
        mean_eff = float(res["efficiency_ccr_input"].mean())

        print(f"  Anios: {list(res['factor'])}")
        print(f"  Eficientes (=1.0): {n_eff}/{n} | eficiencia media: {mean_eff:.3f}")
        print(res[["factor", "efficiency_ccr_input"]].round(4).to_string(index=False))

        out_path = output_dir / f"dea_results_{name.lower()}.csv"
        res.to_csv(out_path, index=False)
        print(f"  Guardado: {out_path}")

        summary.append({
            "model": name,
            "n_inputs": m,
            "n_outputs": s,
            "n_dmu": n,
            "threshold_3x": threshold,
            "adequate": adequate,
            "verdict": verdict,
            "n_efficient": n_eff,
            "mean_efficiency": round(mean_eff, 4),
        })

    summary_df = pd.DataFrame(summary)
    summary_path = output_dir / "dea_models_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print("\n=== RESUMEN DE ADECUACION DE MODELOS ===")
    print(summary_df.to_string(index=False))
    print(f"\nGuardado: {summary_path}")


if __name__ == "__main__":
    main()

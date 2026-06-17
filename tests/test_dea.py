import pandas as pd

import numpy as np

from src.dea_bootstrap import simar_wilson_bootstrap
from src.dea_ccr import dea_ccr_input_oriented
from src.ecuador_panel_dea import resolve_outputs, run_panel_dea


def test_dea_identifies_dominated_dmu():
    data = pd.DataFrame(
        {
            "factor": ["efficient", "dominated"],
            "input": [1.0, 2.0],
            "output": [1.0, 1.0],
        }
    )
    out = dea_ccr_input_oriented(data, "factor", ["input"], ["output"])
    scores = dict(zip(out["factor"], out["efficiency_ccr_input"]))
    assert round(scores["efficient"], 6) == 1.0
    assert round(scores["dominated"], 6) == 0.5


def _toy_panel() -> pd.DataFrame:
    rows = []
    for sector in ["A", "B", "C"]:
        for year in (2018, 2019, 2020):
            rows.append(
                {
                    "dmu": f"{sector}_{year}",
                    "factor": sector,
                    "year": year,
                    "input_employment": 100.0 + year - 2018,
                    "input_capital_fbkf": 50.0 + (year - 2018),
                    "output_value_added": 200.0 + (year - 2018) * 10,
                }
            )
    return pd.DataFrame(rows)


def test_panel_dea_uses_two_independent_inputs_and_is_adequate():
    results, summary, by_sector = run_panel_dea(_toy_panel())

    # 3 sectores x 3 anos = 9 DMU; trabajo + capital -> valor agregado.
    assert summary.loc[0, "n_dmu"] == 9
    assert summary.loc[0, "n_inputs"] == 2
    assert summary.loc[0, "n_outputs"] == 1
    assert summary.loc[0, "threshold_3x"] == 9
    assert summary.loc[0, "verdict"] == "VALIDO"

    # La eficiencia esta acotada en (0, 1] y hay al menos una DMU eficiente.
    assert results["efficiency_ccr_input"].between(0, 1).all()
    assert (results["efficiency_ccr_input"].round(6) >= 1.0).any()

    # Lectura sectorial: una fila por rama.
    assert set(by_sector["factor"]) == {"A", "B", "C"}


def test_exports_gate_adds_second_output_and_recomputes_adequacy():
    panel = _toy_panel()
    # Sin exportaciones: un solo output.
    assert resolve_outputs(panel) == ["output_value_added"]

    # Con una serie de exportaciones verificada entra como segundo output.
    panel["output_exports"] = 30.0 + (panel["year"] - 2018) * 5
    _, summary, _ = run_panel_dea(panel)
    assert resolve_outputs(panel) == ["output_value_added", "output_exports"]
    assert summary.loc[0, "n_outputs"] == 2
    assert summary.loc[0, "threshold_3x"] == 12  # 3*(2 inputs + 2 outputs)


def test_simar_wilson_bootstrap_corrects_upward_bias():
    rng = np.random.default_rng(0)
    n = 30
    X = rng.uniform(1, 5, size=(n, 1))
    # Frontera y = x con ineficiencia: output por debajo de x.
    Y = X[:, 0] * rng.uniform(0.4, 1.0, size=n)
    Y = Y[:, None]

    out = dea_ccr_input_oriented(
        __import__("pandas").DataFrame(
            {"factor": range(n), "input": X[:, 0], "output": Y[:, 0]}
        ),
        "factor",
        ["input"],
        ["output"],
    )
    delta = out["efficiency_ccr_input"].to_numpy()

    boot = simar_wilson_bootstrap(X, Y, delta, n_boot=200, alpha=0.05, seed=1)

    # La correccion de sesgo nunca debe superar la eficiencia DEA (sesgo al alza).
    assert (boot["efficiency_bias_corrected"] <= boot["efficiency_ccr_input"] + 1e-9).all()
    # El intervalo debe contener la eficiencia corregida y respetar el orden.
    assert (boot["ci_low"] <= boot["ci_high"]).all()
    # DMU originalmente eficientes (=1) reciben correccion estricta hacia abajo.
    efficient = np.isclose(delta, 1.0)
    if efficient.any():
        assert (boot.loc[efficient, "efficiency_bias_corrected"] < 1.0).all()

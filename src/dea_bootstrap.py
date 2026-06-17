"""Bootstrap homogeneo de Simar & Wilson (1998) para eficiencias DEA.

Las eficiencias DEA son estimadores deterministas: no traen error estandar ni
intervalos de confianza y estan sesgados hacia arriba (la frontera estimada
queda por dentro de la verdadera). Antes de cualquier lectura inferencial hay
que corregir ese sesgo y cuantificar la incertidumbre. Este modulo implementa
el bootstrap suavizado de Simar & Wilson (1998) para un modelo CCR orientado a
insumos.

Algoritmo (orientacion a insumos, eficiencia delta en (0, 1], 1 = eficiente):

1. Estimar delta_k para cada DMU con DEA.
2. En cada replica b = 1..B:
   a. Remuestrear delta* con reemplazo del conjunto observado.
   b. Suavizar con kernel gaussiano y reflexion en la frontera delta = 1 para
      respetar el soporte acotado, corrigiendo media y varianza.
   c. Construir insumos pseudo: x*_j = x_j * delta_j / delta**_j.
   d. Re-evaluar cada DMU original contra la pseudo-frontier {(x*_j, y_j)}.
3. Sesgo_k = mean_b(delta*_kb) - delta_k; delta_corr_k = delta_k - sesgo_k.
   IC = (delta_k - q_{1-alpha/2}, delta_k - q_{alpha/2}) sobre (delta*_kb - delta_k).

Referencia: Simar, L. & Wilson, P.W. (1998), "Sensitivity Analysis of
Efficiency Scores: How to Bootstrap in Nonparametric Frontier Models",
Management Science 44(1), 49-61.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

try:
    from dea_ccr import dea_ccr_input_oriented, ccr_efficiency_against_reference
except ImportError:
    from .dea_ccr import dea_ccr_input_oriented, ccr_efficiency_against_reference


def _silverman_bandwidth(delta: np.ndarray) -> float:
    """Bandwidth de referencia normal (Silverman) sobre la muestra reflejada.

    Se refleja en 1 para que la regla use una dispersion no truncada por la
    frontera; se aplica un piso pequeno para evitar h = 0 cuando casi todas las
    DMU son eficientes.
    """
    reflected = np.concatenate([delta, 2.0 - delta])
    n = len(delta)
    sigma = reflected.std(ddof=1)
    iqr = np.subtract(*np.percentile(reflected, [75, 25]))
    spread = min(sigma, iqr / 1.349) if iqr > 0 else sigma
    h = 0.9 * spread * n ** (-1 / 5)
    return float(max(h, 1e-3))


def _smooth_resample(delta: np.ndarray, h: float, rng: np.random.Generator) -> np.ndarray:
    """Una extraccion suavizada con reflexion en 1 y correccion media/varianza."""
    n = len(delta)
    sampled = rng.choice(delta, size=n, replace=True)
    noise = h * rng.standard_normal(n)
    perturbed = sampled + noise
    # Reflexion en la frontera delta = 1 (soporte (0, 1]).
    perturbed = np.where(perturbed > 1.0, 2.0 - perturbed, perturbed)

    # Correccion de media y varianza (Simar & Wilson 1998, ec. 3.27).
    mean_s = sampled.mean()
    var_delta = delta.var(ddof=0)
    factor = 1.0 / np.sqrt(1.0 + h ** 2 / var_delta) if var_delta > 0 else 1.0
    corrected = mean_s + factor * (perturbed - mean_s)
    # Reflejar de nuevo por si la correccion empujo algun valor sobre 1.
    corrected = np.where(corrected > 1.0, 2.0 - corrected, corrected)
    # Evitar valores no positivos por ruido extremo.
    corrected = np.clip(corrected, 1e-6, 1.0)
    return corrected


def simar_wilson_bootstrap(
    X: np.ndarray,
    Y: np.ndarray,
    delta: np.ndarray,
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 20240617,
) -> pd.DataFrame:
    """Bootstrap de Simar-Wilson para CCR orientado a insumos.

    Parameters
    ----------
    X, Y : matrices (n_dmu x m) y (n_dmu x s) de insumos y productos.
    delta : eficiencias DEA originales en (0, 1].
    n_boot : numero de replicas bootstrap.
    alpha : nivel para el intervalo de confianza (1 - alpha).
    """
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    h = _silverman_bandwidth(delta)

    boot = np.empty((n_boot, n), dtype=float)
    for b in range(n_boot):
        delta_star = _smooth_resample(delta, h, rng)
        # Insumos pseudo: contraer/expandir hacia la pseudo-frontier.
        scale = (delta / delta_star)[:, None]
        X_star = X * scale
        for k in range(n):
            boot[b, k] = ccr_efficiency_against_reference(X[k], Y[k], X_star, Y)

    boot_mean = np.nanmean(boot, axis=0)
    bias = boot_mean - delta
    delta_corrected = delta - bias

    # IC por percentiles de (delta*_b - delta).
    diff = boot - delta[None, :]
    lo = np.nanpercentile(diff, 100 * (alpha / 2), axis=0)
    hi = np.nanpercentile(diff, 100 * (1 - alpha / 2), axis=0)
    ci_low = delta - hi
    ci_high = delta - lo

    return pd.DataFrame(
        {
            "efficiency_ccr_input": delta,
            "bias": bias,
            "efficiency_bias_corrected": delta_corrected,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "boot_std": np.nanstd(boot, axis=0, ddof=1),
            "bandwidth": h,
            "n_boot": n_boot,
        }
    )

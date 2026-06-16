"""HHI de diversificacion sectorial para Ecuador (extension del paper).

Correccion metodologica (Fase 4): la version anterior usaba solo 3 macro-
sectores del WDI (agricultura/industria/servicios). Con 3 sectores el HHI tiene
un piso matematico de 1/3 = 0.333, de modo que SIEMPRE cae en "Least
diversified" por construccion, no por concentracion economica real.

Aqui usamos el Valor Agregado Bruto por rama de actividad (ISIC) de la base
National Accounts Main Aggregates de la UNSD, que ofrece 7 ramas mutuamente
excluyentes. El piso del HHI baja a 1/7 = 0.143, por debajo del umbral de
"Diversified" (0.15), devolviendo poder discriminante al indice.

Fuente: UNSD AMA API, "GDP and its breakdown at current prices in National
currency" (https://unstats.un.org/unsd/amaapi/api/file/1).
"""
import argparse
import io
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

try:
    from hhi import compute_hhi, classify_hhi
except ImportError:
    from .hhi import compute_hhi, classify_hhi

AMA_URL = "https://unstats.un.org/unsd/amaapi/api/file/1"
COUNTRY = "Ecuador"

# Particion mutuamente excluyente y exhaustiva del Valor Agregado.
# "Mining, Manufacturing, Utilities (C-E)" incluye Manufacturing (D); para no
# duplicar, separamos: mining_utilities = (C-E) - (D).
ISIC_AB = "Agriculture, hunting, forestry, fishing (ISIC A-B)"
ISIC_CE = "Mining, Manufacturing, Utilities (ISIC C-E)"
ISIC_D = "Manufacturing (ISIC D)"
ISIC_F = "Construction (ISIC F)"
ISIC_GH = "Wholesale, retail trade, restaurants and hotels (ISIC G-H)"
ISIC_I = "Transport, storage and communication (ISIC I)"
ISIC_JP = "Other Activities (ISIC J-P)"


def fetch_ecuador_value_added() -> pd.DataFrame:
    """Devuelve VAB por rama en formato largo: year, sector, value."""
    resp = requests.get(AMA_URL, timeout=120)
    resp.raise_for_status()
    df = pd.read_excel(io.BytesIO(resp.content), sheet_name=0, header=2)
    ec = df[df["Country"] == COUNTRY].set_index("IndicatorName")
    years = [c for c in df.columns if isinstance(c, int)]

    def series(name: str) -> pd.Series:
        return ec.loc[name, years].astype(float)

    branches = {
        "Agriculture, forestry & fishing": series(ISIC_AB),
        "Mining & utilities": series(ISIC_CE) - series(ISIC_D),
        "Manufacturing": series(ISIC_D),
        "Construction": series(ISIC_F),
        "Trade, restaurants & hotels": series(ISIC_GH),
        "Transport & communication": series(ISIC_I),
        "Other activities": series(ISIC_JP),
    }
    long = (
        pd.DataFrame(branches)
        .rename_axis("year")
        .reset_index()
        .melt(id_vars="year", var_name="sector",
              value_name="gross_fixed_capital_formation_million_aed")
    )
    long["year"] = long["year"].astype(int)
    return long.dropna()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=2000)
    parser.add_argument("--end", type=int, default=2024)
    args = parser.parse_args()

    print(f"Descargando VAB por rama (UNSD) para {COUNTRY}...")
    data = fetch_ecuador_value_added()
    data = data[(data["year"] >= args.start) & (data["year"] <= args.end)]
    n_sectors = data["sector"].nunique()
    print(f"Sectores: {n_sectors} | piso HHI = 1/{n_sectors} = {1/n_sectors:.3f}")

    out = compute_hhi(data)
    out["hhi"] = out["hhi"].round(4)

    print("\nHHI de Ecuador (VAB por rama, ISIC):")
    print(out.to_string(index=False))

    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)
    # Guardar tambien las participaciones para trazabilidad.
    total = data.groupby("year")["gross_fixed_capital_formation_million_aed"].transform("sum")
    data = data.assign(share=data["gross_fixed_capital_formation_million_aed"] / total)
    shares_wide = data.pivot(index="year", columns="sector", values="share").round(4)
    merged = shares_wide.merge(out.set_index("year"), left_index=True, right_index=True).reset_index()
    merged.to_csv(output_dir / "hhi_ecuador.csv", index=False)
    print(f"\nGuardado: {output_dir / 'hhi_ecuador.csv'}")

    plt.figure(figsize=(10, 6))
    plt.plot(out["year"], out["hhi"], marker="o", color="forestgreen", linewidth=2,
             label=f"HHI Ecuador ({n_sectors} ramas ISIC)")
    plt.axhline(y=0.15, color="gray", linestyle="--", alpha=0.7, label="Diversified (< 0.15)")
    plt.axhline(y=0.25, color="red", linestyle="--", alpha=0.7, label="Least diversified (> 0.25)")
    plt.axhline(y=1 / n_sectors, color="blue", linestyle=":", alpha=0.5,
                label=f"Piso teorico 1/{n_sectors} = {1/n_sectors:.3f}")
    plt.xlabel("Year")
    plt.ylabel("HHI (0 a 1)")
    plt.title("Ecuador: diversificacion sectorial del VAB (HHI, ISIC)")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    figures_dir = Path("outputs/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(figures_dir / "hhi_ecuador.png", dpi=300)
    print(f"Guardado: {figures_dir / 'hhi_ecuador.png'}")


if __name__ == "__main__":
    main()

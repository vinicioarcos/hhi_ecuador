"""Build harmonized sector metrics for the Ecuador sector DEA.

Current official implementation:
- Source: BCE annual national accounts, Matriz de Empleo e Ingresos (MEI)
- Coverage: 2018-2024 (2024 provisional)
- Variables used in DEA:
  - input_employment: average total employment by harmonized sector
  - output_productivity: average VAB per employment by harmonized sector

The script aggregates BCE industries into the seven ISIC-consistent branches
already used by the Ecuador HHI series. Capital formation files are kept as
official references, but are not loaded into the DEA because 7 DMUs only allow
two DEA variables under the rule n_DMU >= 3*(inputs + outputs).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import DATA_RAW


BCE_DIR = DATA_RAW / "ecuador" / "bce"
MEI_FILE = BCE_DIR / "bam_mei_2018_2024p.xlsx"
FBKF_FILE = BCE_DIR / "fbkf_1965_2024p.xlsx"
OUTPUT_FILE = DATA_RAW / "ecuador" / "sector_comparable_metrics.csv"
FBKF_OUTPUT_FILE = DATA_RAW / "ecuador" / "sector_capital_context.csv"
PANEL_OUTPUT_FILE = DATA_RAW / "ecuador" / "sector_year_panel.csv"
# Compuerta de datos para exportaciones por rama: solo se incorpora al DEA si
# existe una serie oficial verificada (factor, year, exports) que cubra las
# siete ramas en la misma ventana que el panel. Mientras no exista, el output
# de exportaciones queda fuera (estado PENDIENTE_VERIFICAR).
EXPORTS_BRANCH_FILE = DATA_RAW / "ecuador" / "sector_exports_by_branch.csv"

YEARS = [2018, 2019, 2020, 2021, 2022, 2023, "2024 (p)"]
HARMONIZED_ORDER = [
    "Agriculture, forestry & fishing",
    "Construction",
    "Manufacturing",
    "Mining & utilities",
    "Other activities",
    "Trade, restaurants & hotels",
    "Transport & communication",
]
SECTION_TO_FACTOR = {
    "A -Agricultura, ganadería y silvicultura": "Agriculture, forestry & fishing",
    "A -Pesca y acuicultura": "Agriculture, forestry & fishing",
    "B -Explotación de minas y canteras": "Mining & utilities",
    "C -Manufactura de productos alimenticios": "Manufacturing",
    "C -Manufactura de productos no alimenticios": "Manufacturing",
    "C -Refinados de petroleo": "Manufacturing",
    "D-E -Suministro de electricidad y agua": "Mining & utilities",
    "F -Construcción": "Construction",
    "G -Comercio": "Trade, restaurants & hotels",
    "H -Transporte y almacenamiento": "Transport & communication",
    "I -Alojamiento y comidas": "Trade, restaurants & hotels",
    "J -Información y comunicación": "Transport & communication",
    "K -Actividades financieras y de seguros": "Other activities",
    "L -Actividades inmobiliarias": "Other activities",
    "M - N -Actividades profesionales, técnicas": "Other activities",
    "O -Administración pública": "Other activities",
    "P -Enseñanza": "Other activities",
    "Q -Salud y asistencia social": "Other activities",
    "R - S - U -Arte, entretenimiento y otras actividades de servicios": "Other activities",
}
EXCLUDED_SECTIONS = {"T -Actividades de los Hogares como empleadores"}
FBKF_COLUMN_TO_FACTOR = {
    "Agricultura, ganadería, silvicultura y pesca": "Agriculture, forestry & fishing",
    "\t\nExplotación de minas y canteras": "Mining & utilities",
    "\t\nIndustrias manufactureras": "Manufacturing",
    "Suministros de electricidad y agua": "Mining & utilities",
    "Construcción": "Construction",
    "Comercio al por mayor y al por menor; reparación de vehículos automotores y motocicletas": "Trade, restaurants & hotels",
    "Transporte y almacenamiento": "Transport & communication",
    "Actividades de alojamiento y de servicio de comidas": "Trade, restaurants & hotels",
    "Información y comunicación": "Transport & communication",
    "Actividades financieras y de seguros": "Other activities",
    "Actividades inmobiliarias": "Other activities",
    "Actividades profesionales, científicas, técnicas y administrativas": "Other activities",
    "Administración pública y defensa; planes de seguridad social de afiliación obligatoria": "Other activities",
    "Servicios a los hogares (*)": "Other activities",
}


def tidy_mei_sheet(path: Path, sheet_name: str, value_name: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=sheet_name, header=9)
    marker = df.index[
        df.iloc[:, 0].astype(str).str.contains("ESTRUCTURA PORCENTUAL", case=False, na=False)
    ]
    if len(marker) > 0:
        df = df.loc[: marker.min() - 1].copy()
    first_cols = list(df.columns[:3])
    if str(first_cols[0]).strip().upper() == "SECCIÓN CIIU":
        df = df.rename(columns={df.columns[0]: "section", df.columns[1]: "cie", df.columns[2]: "industry"})
    else:
        value_cols = [c for c in df.columns if c in YEARS]
        df = df.rename(columns={df.columns[0]: "cie", df.columns[1]: "industry"})
        df["section"] = pd.NA
        df = df[["section", "cie", "industry", *value_cols]]
    df = df.melt(
        id_vars=["section", "cie", "industry"],
        value_vars=YEARS,
        var_name="year",
        value_name=value_name,
    )
    df["year"] = df["year"].replace({"2024 (p)": 2024}).astype(int)
    df["section"] = df["section"].ffill()
    df = df.dropna(subset=[value_name])
    df = df[~df["cie"].isna()].copy()
    df["cie"] = df["cie"].astype(str)
    df = df[~df["cie"].str.contains("Total", case=False, na=False)].copy()
    return df


def build_employment_vab_panel() -> pd.DataFrame:
    """Sector-year panel of employment and (implied) value added, 2018-2024.

    Returns one row per harmonized branch and year with columns
    ``factor``, ``year``, ``employment`` and ``value_added``. Value added is
    rebuilt as employment * (VAB per employment), giving a genuine output that
    is independent from the labor input (unlike productivity, which is the
    output/input ratio itself).
    """
    if not MEI_FILE.exists():
        raise SystemExit(f"Missing source file: {MEI_FILE}")

    employment = tidy_mei_sheet(MEI_FILE, "TOTAL EMPLEO", "employment")
    productivity = tidy_mei_sheet(MEI_FILE, "VAB por empleo", "productivity")
    productivity = productivity.merge(
        employment[["cie", "industry", "section"]].drop_duplicates(),
        on=["cie", "industry"],
        how="left",
        suffixes=("", "_employment"),
        validate="many_to_one",
    )
    productivity["section"] = productivity["section"].fillna(productivity["section_employment"])
    productivity = productivity.drop(columns=["section_employment"])

    merged = employment.merge(
        productivity[["cie", "industry", "year", "productivity"]],
        on=["cie", "industry", "year"],
        how="inner",
        validate="one_to_one",
    )
    merged["factor"] = merged["section"].map(SECTION_TO_FACTOR)
    merged = merged[~merged["section"].isin(EXCLUDED_SECTIONS)].copy()
    if merged["factor"].isna().any():
        missing_sections = sorted(merged.loc[merged["factor"].isna(), "section"].dropna().unique())
        raise ValueError(f"Unmapped BCE sections: {missing_sections}")

    merged["vab_implied"] = merged["employment"] * merged["productivity"]
    sector_year = (
        merged.groupby(["factor", "year"], as_index=False)
        .agg(employment=("employment", "sum"), value_added=("vab_implied", "sum"))
    )
    return sector_year


def build_metrics() -> pd.DataFrame:
    if not MEI_FILE.exists():
        raise SystemExit(f"Missing source file: {MEI_FILE}")

    employment = tidy_mei_sheet(MEI_FILE, "TOTAL EMPLEO", "employment")
    productivity = tidy_mei_sheet(MEI_FILE, "VAB por empleo", "productivity")
    productivity = productivity.merge(
        employment[["cie", "industry", "section"]].drop_duplicates(),
        on=["cie", "industry"],
        how="left",
        suffixes=("", "_employment"),
        validate="many_to_one",
    )
    productivity["section"] = productivity["section"].fillna(productivity["section_employment"])
    productivity = productivity.drop(columns=["section_employment"])

    merged = employment.merge(
        productivity[["cie", "industry", "year", "productivity"]],
        on=["cie", "industry", "year"],
        how="inner",
        validate="one_to_one",
    )
    merged["factor"] = merged["section"].map(SECTION_TO_FACTOR)
    merged = merged[~merged["section"].isin(EXCLUDED_SECTIONS)].copy()
    if merged["factor"].isna().any():
        missing_sections = sorted(merged.loc[merged["factor"].isna(), "section"].dropna().unique())
        raise ValueError(f"Unmapped BCE sections: {missing_sections}")

    merged["vab_implied"] = merged["employment"] * merged["productivity"]
    sector_year = (
        merged.groupby(["factor", "year"], as_index=False)
        .agg(employment=("employment", "sum"), vab_implied=("vab_implied", "sum"))
    )
    sector_year["productivity"] = sector_year["vab_implied"] / sector_year["employment"]

    summary = (
        sector_year.groupby("factor", as_index=False)
        .agg(
            input_employment=("employment", "mean"),
            output_productivity=("productivity", "mean"),
        )
    )
    summary["coverage_start_year"] = sector_year.groupby("factor")["year"].min().values
    summary["coverage_end_year"] = sector_year.groupby("factor")["year"].max().values
    summary["source"] = (
        "BCE MEI 2018-2024p: "
        "https://contenido.bce.fin.ec/documentos/informacioneconomica/"
        "cuentasnacionales/anuales/bam_mei_2018_2024p.xlsx"
    )
    summary["notes"] = (
        "Promedio 2018-2024 por rama armonizada; productividad agregada como "
        "VAB implicito total / empleo total."
    )
    summary["factor"] = pd.Categorical(summary["factor"], categories=HARMONIZED_ORDER, ordered=True)
    summary = summary.sort_values("factor").reset_index(drop=True)
    return summary[
        [
            "factor",
            "coverage_start_year",
            "coverage_end_year",
            "input_employment",
            "output_productivity",
            "source",
            "notes",
        ]
    ]


def build_fbkf_panel() -> pd.DataFrame:
    """Sector-year panel of gross fixed capital formation (FBKF), 2018-2023.

    Returns one row per harmonized branch and year with columns ``factor``,
    ``year`` and ``fbkf_musd``.
    """
    if not FBKF_FILE.exists():
        raise SystemExit(f"Missing source file: {FBKF_FILE}")

    df = pd.read_excel(FBKF_FILE, sheet_name="4. Industria", header=9)
    df = df.rename(columns={df.columns[0]: "year"})
    valid_cols = [c for c in df.columns if c in FBKF_COLUMN_TO_FACTOR]
    df = df[["year", *valid_cols]].dropna(subset=["year"]).copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df[df["year"].notna()].copy()
    df["year"] = df["year"].astype(int)
    df = df[df["year"].between(2018, 2024)].copy()

    long = df.melt(id_vars="year", var_name="industry_bce", value_name="fbkf_musd")
    long["factor"] = long["industry_bce"].map(FBKF_COLUMN_TO_FACTOR)
    return (
        long.groupby(["factor", "year"], as_index=False)["fbkf_musd"].sum()
        .sort_values(["factor", "year"])
    )


def build_dea_panel() -> pd.DataFrame:
    """Genuine production-frontier panel: labor + capital -> value added.

    DMU = sector-year. Inputs are employment (labor) and FBKF (capital), two
    independent factors of production; the output is value added. Pooling the
    seven branches across the common 2018-2023 window yields enough DMUs to
    satisfy the CCR adequacy rule n_DMU >= 3*(inputs + outputs).
    """
    labor_vab = build_employment_vab_panel()
    capital = build_fbkf_panel()
    panel = labor_vab.merge(capital, on=["factor", "year"], how="inner", validate="one_to_one")
    panel = panel.rename(
        columns={
            "employment": "input_employment",
            "fbkf_musd": "input_capital_fbkf",
            "value_added": "output_value_added",
        }
    )
    panel = _merge_optional_exports(panel)
    panel["dmu"] = panel["factor"] + "_" + panel["year"].astype(str)
    value_cols = [c for c in panel.columns if c.startswith("input_") or c.startswith("output_")]
    ordered = ["dmu", "factor", "year", *value_cols]
    panel = panel[ordered].sort_values(["factor", "year"]).reset_index(drop=True)
    if (panel[value_cols] <= 0).any().any():
        raise ValueError("DEA panel requires strictly positive inputs and outputs.")
    return panel


def _merge_optional_exports(panel: pd.DataFrame) -> pd.DataFrame:
    """Merge a verified branch-level exports series as a second output, if any.

    The file must cover the seven branches across the panel's common window with
    no gaps; otherwise it is rejected and exports stay out of the DEA. This keeps
    exports gated on verified evidence instead of an ad hoc product-to-branch
    mapping.
    """
    if not EXPORTS_BRANCH_FILE.exists():
        print(f"Exportaciones por rama: sin archivo verificado ({EXPORTS_BRANCH_FILE.name}); "
              "se excluyen del DEA (PENDIENTE_VERIFICAR).")
        return panel

    exports = pd.read_csv(EXPORTS_BRANCH_FILE)
    required = {"factor", "year", "exports"}
    missing = required - set(exports.columns)
    if missing:
        raise ValueError(f"{EXPORTS_BRANCH_FILE} requiere columnas {sorted(required)}; faltan {sorted(missing)}.")

    expected = panel[["factor", "year"]].drop_duplicates()
    merged = expected.merge(exports[["factor", "year", "exports"]], on=["factor", "year"], how="left")
    if merged["exports"].isna().any() or (merged["exports"] <= 0).any():
        raise ValueError(
            f"{EXPORTS_BRANCH_FILE} debe cubrir las siete ramas en toda la ventana del panel "
            "con valores estrictamente positivos para entrar al DEA."
        )

    out = panel.merge(
        exports[["factor", "year", "exports"]].rename(columns={"exports": "output_exports"}),
        on=["factor", "year"],
        how="left",
        validate="one_to_one",
    )
    print(f"Exportaciones por rama verificadas: incorporadas como output_exports desde {EXPORTS_BRANCH_FILE.name}.")
    return out


def build_fbkf_context() -> pd.DataFrame:
    summary = build_fbkf_panel()
    avg = (
        summary.groupby("factor", as_index=False)
        .agg(
            coverage_start_year=("year", "min"),
            coverage_end_year=("year", "max"),
            fbkf_avg_musd=("fbkf_musd", "mean"),
            fbkf_latest_musd=("fbkf_musd", "last"),
        )
    )
    avg["source"] = (
        "BCE FBKF 1965-2024p: "
        "https://contenido.bce.fin.ec/documentos/informacioneconomica/"
        "cuentasnacionales/anuales/fbkf_1965_2024p.xlsx"
    )
    avg["notes"] = (
        "FBKF promedio y ultimo dato 2018-2023 por rama armonizada; "
        "serie contextual, no usada en el DEA por restriccion de DMUs."
    )
    avg["factor"] = pd.Categorical(avg["factor"], categories=HARMONIZED_ORDER, ordered=True)
    avg = avg.sort_values("factor").reset_index(drop=True)
    return avg


def main() -> None:
    metrics = build_metrics()
    fbkf_context = build_fbkf_context()
    dea_panel = build_dea_panel()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(OUTPUT_FILE, index=False)
    fbkf_context.to_csv(FBKF_OUTPUT_FILE, index=False)
    dea_panel.to_csv(PANEL_OUTPUT_FILE, index=False)
    print(metrics.round(4).to_string(index=False))
    print()
    print(fbkf_context.round(4).to_string(index=False))
    print()
    print(f"Panel DEA sector-año: {len(dea_panel)} DMU "
          f"({dea_panel['year'].min()}-{dea_panel['year'].max()})")
    print(dea_panel.round(2).to_string(index=False))
    print(f"\nGuardado: {OUTPUT_FILE}")
    print(f"Guardado: {FBKF_OUTPUT_FILE}")
    print(f"Guardado: {PANEL_OUTPUT_FILE}")


if __name__ == "__main__":
    main()

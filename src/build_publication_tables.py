"""Build compact CSV tables intended for direct use in the report/article."""
from pathlib import Path

import pandas as pd

from config import TABLES


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)

    ecuador = pd.read_csv(TABLES / "hhi_ecuador.csv")
    ecuador_pub = ecuador[["year", "hhi", "classification"]]
    ecuador_pub.to_csv(TABLES / "publication_table_ecuador_hhi.csv", index=False)

    dea_frames = []
    ecuador_dea_paths = [
        TABLES / "dea_ecuador_panel_summary.csv",
    ]
    for ecuador_dea_path in ecuador_dea_paths:
        if ecuador_dea_path.exists():
            dea_frames.append(pd.read_csv(ecuador_dea_path))
    if not dea_frames:
        raise SystemExit("No Ecuador DEA summary files found.")
    dea = pd.concat(dea_frames, ignore_index=True, sort=False)
    for col in ["inputs_used", "outputs_used", "coverage_note"]:
        if col not in dea.columns:
            dea[col] = pd.NA
    dea_pub = dea[
        [
            "model",
            "dmu",
            "n_inputs",
            "n_outputs",
            "n_dmu",
            "threshold_3x",
            "verdict",
            "n_efficient",
            "mean_efficiency",
            "inputs_used",
            "outputs_used",
            "coverage_note",
        ]
    ]
    dea_pub.to_csv(TABLES / "publication_table_ecuador_dea_summary.csv", index=False)

    sector_context = Path("data/raw/ecuador/sector_capital_context.csv")
    if sector_context.exists():
        pd.read_csv(sector_context).to_csv(
            TABLES / "publication_table_ecuador_sector_capital_context.csv",
            index=False,
        )
    exports_status = Path("data/raw/ecuador/sector_exports_context_status.csv")
    if exports_status.exists():
        pd.read_csv(exports_status).to_csv(
            TABLES / "publication_table_ecuador_sector_exports_status.csv",
            index=False,
        )

    inventory_rows = [
        {
            "dataset": "UNSD National Accounts Main Aggregates",
            "file": "outputs/tables/hhi_ecuador.csv",
            "source": "UNSD AMA API, GDP and breakdown at current prices",
            "use": "HHI de Ecuador y base para DEA por ano y por rama",
        },
    ]
    sector_metrics = Path("data/raw/ecuador/sector_comparable_metrics.csv")
    if sector_metrics.exists():
        inventory_rows.append(
            {
                "dataset": "Ecuador sector comparable metrics",
                "file": str(sector_metrics),
                "source": "BCE MEI 2018-2024p",
                "use": "Variables adicionales para enriquecer el DEA sectorial por rama",
            }
        )
    if sector_context.exists():
        inventory_rows.append(
            {
                "dataset": "Ecuador sector capital context",
                "file": str(sector_context),
                "source": "BCE FBKF 1965-2024p",
                "use": "Contexto de formacion bruta de capital fijo por rama armonizada",
            }
        )
    if exports_status.exists():
        inventory_rows.append(
            {
                "dataset": "Ecuador sector exports status",
                "file": str(exports_status),
                "source": "BCE Comercio Exterior de Bienes",
                "use": "Estado metodologico de exportaciones por rama para futura extension",
            }
        )
    inventory = pd.DataFrame(inventory_rows)
    inventory.to_csv(TABLES / "publication_data_inventory.csv", index=False)

    print("Publication tables written to outputs/tables.")


if __name__ == "__main__":
    main()

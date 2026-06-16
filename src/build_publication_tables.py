"""Build compact CSV tables intended for direct use in the report/article."""
from pathlib import Path

import pandas as pd

from config import TABLES


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)

    hhi = pd.read_csv(TABLES / "hhi_replication_comparison.csv")
    hhi_pub = hhi[
        [
            "year",
            "hhi_computed",
            "hhi_paper",
            "abs_diff",
            "classification_computed",
        ]
    ].rename(
        columns={
            "hhi_computed": "replicated_hhi",
            "hhi_paper": "published_hhi",
            "classification_computed": "classification",
        }
    )
    hhi_pub.to_csv(TABLES / "publication_table_uae_hhi_replication.csv", index=False)

    dea = pd.read_csv(TABLES / "dea_models_summary.csv")
    ecuador_dea_paths = [
        TABLES / "dea_ecuador_summary.csv",
        TABLES / "dea_ecuador_sector_summary.csv",
    ]
    for ecuador_dea_path in ecuador_dea_paths:
        if ecuador_dea_path.exists():
            dea = pd.concat([dea, pd.read_csv(ecuador_dea_path)], ignore_index=True, sort=False)
    dea_pub = dea[
        [
            "model",
            "n_inputs",
            "n_outputs",
            "n_dmu",
            "threshold_3x",
            "verdict",
            "n_efficient",
            "mean_efficiency",
        ]
    ]
    dea_pub.to_csv(TABLES / "publication_table_dea_model_audit.csv", index=False)

    ecuador = pd.read_csv(TABLES / "hhi_ecuador.csv")
    ecuador_pub = ecuador[["year", "hhi", "classification"]]
    ecuador_pub.to_csv(TABLES / "publication_table_ecuador_hhi.csv", index=False)

    inventory = pd.DataFrame(
        [
            {
                "dataset": "UAE GFCF by sector",
                "file": "data/raw/hhi/gfcf_sector_template.csv",
                "source": "KAPSARC Data Portal / FCSC, originally Bayanat/UAE Open Data",
                "use": "UAE HHI replication",
            },
            {
                "dataset": "Published UAE HHI values",
                "file": "data/processed/hhi_values_from_paper_table3.csv",
                "source": "Siddiqui & Afzal (2022), Table 3",
                "use": "Replication benchmark",
            },
            {
                "dataset": "World Development Indicators",
                "file": "data/raw/wdi/wdi_uae_2000_2020.csv",
                "source": "World Bank WDI API",
                "use": "UAE DEA audit",
            },
            {
                "dataset": "UNSD National Accounts Main Aggregates",
                "file": "outputs/tables/hhi_ecuador.csv",
                "source": "UNSD AMA API, GDP and breakdown at current prices",
                "use": "Ecuador HHI, year-level DEA, and sector-level DEA",
            },
        ]
    )
    inventory.to_csv(TABLES / "publication_data_inventory.csv", index=False)

    print("Publication tables written to outputs/tables.")


if __name__ == "__main__":
    main()

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
        TABLES / "dea_ecuador_summary.csv",
        TABLES / "dea_ecuador_sector_summary.csv",
    ]
    for ecuador_dea_path in ecuador_dea_paths:
        if ecuador_dea_path.exists():
            dea_frames.append(pd.read_csv(ecuador_dea_path))
    if not dea_frames:
        raise SystemExit("No Ecuador DEA summary files found.")
    dea = pd.concat(dea_frames, ignore_index=True, sort=False)
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
        ]
    ]
    dea_pub.to_csv(TABLES / "publication_table_ecuador_dea_summary.csv", index=False)

    inventory = pd.DataFrame(
        [
            {
                "dataset": "UNSD National Accounts Main Aggregates",
                "file": "outputs/tables/hhi_ecuador.csv",
                "source": "UNSD AMA API, GDP and breakdown at current prices",
                "use": "HHI de Ecuador y base para DEA por ano y por rama",
            },
        ]
    )
    inventory.to_csv(TABLES / "publication_data_inventory.csv", index=False)

    print("Publication tables written to outputs/tables.")


if __name__ == "__main__":
    main()

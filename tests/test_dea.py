import pandas as pd

from src.dea_ccr import dea_ccr_input_oriented
from src.ecuador_dea import build_ecuador_dea_dataset, run_ecuador_dea
from src.ecuador_sector_dea import build_sector_dea_dataset, run_sector_dea


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


def test_ecuador_dea_dataset_and_summary():
    hhi_ecuador = pd.DataFrame(
        {
            "year": [2000, 2001, 2002],
            "Mining & utilities": [0.20, 0.15, 0.10],
            "Manufacturing": [0.30, 0.25, 0.20],
            "Transport & communication": [0.10, 0.15, 0.20],
            "Trade, restaurants & hotels": [0.20, 0.25, 0.30],
        }
    )
    data = build_ecuador_dea_dataset(hhi_ecuador)
    assert list(data.columns) == [
        "factor",
        "input_mining_utilities_share",
        "output_manufacturing_share",
        "output_transport_communication_share",
        "output_trade_hotels_share",
    ]

    results, summary = run_ecuador_dea(data)
    assert len(results) == 3
    assert summary.loc[0, "n_dmu"] == 3
    assert summary.loc[0, "threshold_3x"] == 12


def test_ecuador_sector_dea_dataset_and_summary():
    hhi_ecuador = pd.DataFrame(
        {
            "year": [2000, 2001, 2002, 2020, 2021, 2022],
            "Sector A": [0.20, 0.20, 0.20, 0.30, 0.30, 0.30],
            "Sector B": [0.30, 0.30, 0.30, 0.20, 0.20, 0.20],
            "hhi": [0.5] * 6,
            "classification": ["Moderately diversified"] * 6,
        }
    )
    data = build_sector_dea_dataset(
        hhi_ecuador,
        initial_years=(2000, 2002),
        recent_years=(2020, 2022),
    )
    assert list(data.columns) == [
        "factor",
        "input_initial_share",
        "output_recent_share",
    ]
    assert data.loc[data["factor"] == "Sector A", "output_recent_share"].iloc[0] == 0.30

    results, summary = run_sector_dea(data)
    assert len(results) == 2
    assert summary.loc[0, "n_dmu"] == 2
    assert summary.loc[0, "threshold_3x"] == 6

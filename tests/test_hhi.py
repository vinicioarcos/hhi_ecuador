import pandas as pd
from src.hhi import compute_hhi, classify_hhi

def test_classification():
    assert classify_hhi(0.10) == "Diversified"
    assert classify_hhi(0.20) == "Moderately diversified"
    assert classify_hhi(0.30) == "Least diversified"

def test_compute_hhi_simple():
    df = pd.DataFrame({
        "year": [2020, 2020],
        "sector": ["A", "B"],
        "value_added_share_proxy": [50, 50],
    })
    out = compute_hhi(df, value_col="value_added_share_proxy")
    assert round(float(out.loc[0, "hhi"]), 4) == 0.5

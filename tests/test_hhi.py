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
        "gross_fixed_capital_formation_million_aed": [50, 50],
    })
    out = compute_hhi(df)
    assert round(float(out.loc[0, "hhi"]), 4) == 0.5

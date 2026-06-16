import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))

import pandas as pd
import matplotlib.pyplot as plt

DATA = ROOT / "data" / "processed" / "hhi_values_from_paper_table3.csv"
FIGURES = ROOT / "outputs" / "figures"

def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)

    plt.figure()
    plt.plot(df["year"], df["hhi_paper"], marker="o")
    plt.xlabel("Year")
    plt.ylabel("HHI")
    plt.title("HHI values reported in Siddiqui & Afzal")
    plt.tight_layout()
    plt.savefig(FIGURES / "hhi_paper_table3.png", dpi=300)
    print(f"Saved {FIGURES / 'hhi_paper_table3.png'}")

if __name__ == "__main__":
    main()

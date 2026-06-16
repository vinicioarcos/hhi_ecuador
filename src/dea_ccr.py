import argparse
import pandas as pd
import numpy as np
from scipy.optimize import linprog


def dea_ccr_input_oriented(data: pd.DataFrame, dmu_col: str, input_cols: list[str], output_cols: list[str]) -> pd.DataFrame:
    """
    Input-oriented CCR DEA.

    For each DMU o:
        minimize theta
        subject to:
            X * lambda <= theta * x_o
            Y * lambda >= y_o
            lambda >= 0

    Efficiency theta ranges from 0 to 1, where 1 is efficient.
    """
    X = data[input_cols].to_numpy(dtype=float)
    Y = data[output_cols].to_numpy(dtype=float)
    n = len(data)

    results = []
    for o in range(n):
        # Variables: lambda_1 ... lambda_n, theta
        c = np.zeros(n + 1)
        c[-1] = 1.0

        A_ub = []
        b_ub = []

        # Input constraints: X lambda - theta*x_o <= 0
        for i in range(X.shape[1]):
            row = np.zeros(n + 1)
            row[:n] = X[:, i]
            row[-1] = -X[o, i]
            A_ub.append(row)
            b_ub.append(0.0)

        # Output constraints: -Y lambda <= -y_o
        for r in range(Y.shape[1]):
            row = np.zeros(n + 1)
            row[:n] = -Y[:, r]
            row[-1] = 0.0
            A_ub.append(row)
            b_ub.append(-Y[o, r])

        bounds = [(0, None)] * n + [(0, 1)]
        res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=bounds, method="highs")

        efficiency = np.nan if not res.success else res.x[-1]
        results.append({
            dmu_col: data.iloc[o][dmu_col],
            "efficiency_ccr_input": efficiency,
            "status": res.message
        })

    return pd.DataFrame(results)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CCR DEA input-oriented model.")
    parser.add_argument("--input", required=True, help="CSV with DMU, inputs and outputs.")
    parser.add_argument("--output", required=True, help="Output CSV path.")
    parser.add_argument("--dmu-col", default="factor")
    parser.add_argument("--inputs", nargs="+", default=None,
                        help="Input columns. If omitted, columns starting with input_ are used.")
    parser.add_argument("--outputs", nargs="+", default=None,
                        help="Output columns. If omitted, columns starting with output_ are used.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    input_cols = args.inputs or [c for c in df.columns if c.startswith("input_")]
    output_cols = args.outputs or [c for c in df.columns if c.startswith("output_")]

    if not input_cols or not output_cols:
        raise ValueError("DEA requires at least one input and one output column.")

    out = dea_ccr_input_oriented(df, args.dmu_col, input_cols, output_cols)
    Path = __import__("pathlib").Path
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()

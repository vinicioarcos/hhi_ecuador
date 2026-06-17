"""Wrapper for the UAE DEA audit."""

from subprocess import run


def main() -> None:
    run(["python", "src/build_dea_dataset.py"], check=True)
    run(["python", "src/run_dea_analysis.py"], check=True)


if __name__ == "__main__":
    main()

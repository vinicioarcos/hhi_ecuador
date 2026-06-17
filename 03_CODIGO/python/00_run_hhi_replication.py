"""Wrapper for the UAE HHI replication pipeline."""

from subprocess import run


def main() -> None:
    run(["python", "src/hhi.py", "--paper-table"], check=True)
    run(["python", "src/hhi.py", "--input", "data/raw/hhi/gfcf_sector_template.csv"], check=True)
    run(["python", "src/compare_hhi.py"], check=True)
    run(["python", "src/visualize.py"], check=True)


if __name__ == "__main__":
    main()

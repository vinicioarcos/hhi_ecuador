"""Wrapper for the Ecuador extension."""

from subprocess import run


def main() -> None:
    run(["python", "src/ecuador_hhi.py"], check=True)
    run(["python", "src/build_ecuador_sector_metrics.py"], check=True)
    run(["python", "src/ecuador_panel_dea.py"], check=True)
    run(["python", "src/build_publication_tables.py"], check=True)


if __name__ == "__main__":
    main()

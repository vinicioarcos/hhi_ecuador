"""Render Quarto outputs for the replication project."""

from subprocess import run


def main() -> None:
    run(["quarto", "render", "paper/replication_report.qmd", "--to", "html"], check=True)
    run(["quarto", "render", "09_REPORTS_QUARTO/replication_report.qmd", "--to", "html"], check=True)
    run(["quarto", "render", "10_SLIDES/defense_slides.qmd", "--to", "revealjs"], check=True)


if __name__ == "__main__":
    main()

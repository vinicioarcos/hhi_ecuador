.PHONY: all ecuador report test clean

# Pipeline Ecuador-only.
all: ecuador report

# --- Extension Ecuador: HHI por rama ISIC (requiere internet) ---
ecuador:
	python src/ecuador_hhi.py
	python src/ecuador_dea.py
	python src/ecuador_sector_dea.py
	python src/build_publication_tables.py

# --- Reporte Quarto (HTML + Typst PDF) ---
report:
	quarto render

test:
	python -m pytest -q

clean:
	rm -f outputs/tables/*.csv outputs/figures/*.png
	rm -rf paper/replication_report.html paper/replication_report.pdf

.PHONY: all data hhi dea ecuador report test clean

# Pipeline completo de replicacion, en orden de dependencia.
all: hhi dea ecuador report

# --- Descarga de datos crudos (requiere internet) ---
data:
	python src/download_kapsarc.py
	python src/fetch_wdi.py

# --- UAE: HHI desde datos primarios + validacion contra el paper ---
hhi:
	python src/hhi.py --paper-table
	python src/hhi.py --input data/raw/hhi/gfcf_sector_template.csv
	python src/compare_hhi.py
	python src/visualize.py

# --- UAE: DEA CCR (construye dataset y corre los modelos) ---
dea:
	python src/build_dea_dataset.py
	python src/run_dea_analysis.py

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

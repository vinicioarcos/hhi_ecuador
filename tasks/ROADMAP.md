# Roadmap de replicación

## Fase 1 — Auditoría del paper
- [x] Identificar objetivo, fuente de datos, metodología y tablas clave.
- [x] Registrar HHI publicado en Tabla 3.
- [x] Registrar sectores utilizados para HHI.
- [x] Descargar datos sectoriales originales desde UAE Open Data/Bayanat (vía KAPSARC Data Portal, fuente FCSC; `src/download_kapsarc.py`).
- [x] Descargar WDI 2000–2020 para indicadores DEA.

## Fase 2 — Replicación HHI
- [x] Completar `data/raw/hhi/gfcf_sector_template.csv` (descarga automatizada desde KAPSARC/FCSC, 18 sectores 2010-2020).
- [x] Ejecutar `python src/hhi.py --input data/raw/hhi/gfcf_sector_template.csv`.
- [x] Comparar con `hhi_values_from_paper_table3.csv` (ver `outputs/tables/hhi_replication_comparison.csv`; diff ≤ 0.0003 en 7/8 años).
- [x] Explicar diferencias por redondeo, fuente o actualización (Documentado en el reporte).

## Fase 3 — Replicación DEA
- [x] Descargar indicadores WDI.
- [x] Construir `data/processed/dea_input.csv`.
- [x] Ejecutar `src/dea_ccr.py` (y `src/run_dea_analysis.py`).
- [x] Contrastar resultados con Tabla 4.
- [x] Rediseñar DEA con regla de adecuación n_DMU ≥ 3·(inputs+outputs); 3 modelos válidos + réplica degenerada documentada (`outputs/tables/dea_models_summary.csv`).

## Fase 4 — Extensión
- [x] Adaptar a Ecuador: VAB por rama de actividad (ISIC, 7 ramas) desde UNSD National Accounts; corrige el sesgo de piso 1/3 de la versión de 3 sectores.
- [x] Probar HHI por ramas económicas (resultado corregido: moderadamente diversificado, HHI 0.18-0.24).
- [ ] Probar DEA por años, provincias o sectores.
- [ ] Preparar artículo Quarto.

# Datos GFCF sectoriales de EAU (insumo del HHI)

`gfcf_sector_template.csv` contiene la Formación Bruta de Capital Fijo (GFCF)
de Emiratos Árabes Unidos por actividad económica, en **millones de AED a
precios corrientes**, 18 sectores, 2010–2020.

## Fuente

- Portal: KAPSARC Data Portal — dataset `gross-fixed-capital-formation`
  (https://datasource.kapsarc.org/explore/dataset/gross-fixed-capital-formation/).
- Fuente primaria declarada en el dataset: **Federal Competitiveness and
  Statistics Centre (FCSC)** de EAU.
- El paper original (Siddiqui & Afzal, 2022) usó estos mismos 18 sectores
  publicados por **Bayanat (2020)**, el portal de datos abiertos de EAU hoy
  consolidado bajo el FCSC.

## Reproducción

```bash
python src/download_kapsarc.py
python src/hhi.py --input data/raw/hhi/gfcf_sector_template.csv
```

Se excluyen los agregados `Total` y `Total Non-oil` (no son sectores).

## Validación contra el paper (Tabla 3)

El HHI calculado reproduce los valores publicados con diferencia absoluta
≤ 0.0003 en 7 de 8 años (2010–2017); 2017 difiere 0.0023, atribuible a una
revisión posterior de las cuentas nacionales. Ver
`outputs/tables/hhi_replication_comparison.csv`.

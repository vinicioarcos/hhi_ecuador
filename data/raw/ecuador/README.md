Base opcional para enriquecer el DEA sectorial de Ecuador.

- Use `sector_comparable_metrics_template.csv` como plantilla.
- La version oficial actual se puede generar con `src/build_ecuador_sector_metrics.py`.
- El archivo esperado por el DEA es `sector_comparable_metrics.csv`.
- `factor` debe coincidir exactamente con las siete ramas ISIC del archivo `outputs/tables/hhi_ecuador.csv`.
- `coverage_start_year` y `coverage_end_year` deben ser iguales para las siete ramas.
- Toda variable DEA adicional debe empezar con `input_` o `output_`.
- No deje celdas vacias en una variable que quiera usar.
- No use valores cero o negativos en columnas `input_` o `output_`.
- Fuente oficial ya localizada:
  - `data/raw/ecuador/bce/bam_mei_2018_2024p.xlsx` para empleo y productividad (`VAB por empleo`).
  - `data/raw/ecuador/bce/fbkf_1965_2024p.xlsx` como referencia oficial para FBKF por industria.
  - `https://contenido.bce.fin.ec/documentos/informacioneconomica/SectorExterno/ix_ComercioExterior.html` para auditoria de exportaciones.
- Decision metodologica actual:
  - `sector_comparable_metrics.csv` usa empleo y productividad del BCE con cobertura comun 2018-2024.
  - La seccion `T - Actividades de los Hogares como empleadores` se excluye porque no tiene contraparte directa en la particion HHI de siete ramas.
  - FBKF por industria queda como fuente oficial disponible, pero no entra al DEA actual para no violar la regla `n_DMU >= 3*(inputs + outputs)` con solo 7 sectores.
  - Exportaciones quedan fuera por ahora: el BCE publica comercio exterior por productos y por paises; no se verifico un correlacionador oficial producto-rama compatible con las 7 ramas del HHI.
- Si la evidencia de comparabilidad no esta cerrada, deje la base fuera del pipeline y marque el trabajo como `PENDIENTE_VERIFICAR`.

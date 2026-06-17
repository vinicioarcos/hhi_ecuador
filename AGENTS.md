# AGENTS.md

Roles para coordinar el proyecto Ecuador sobre diversificacion sectorial, HHI y DEA.

## Reglas comunes

- Mantener el tema del proyecto: diversificacion sectorial, HHI y DEA.
- No inventar resultados, datos, indexaciones ni metricas editoriales.
- Toda afirmacion cuantitativa debe apuntar a un archivo de `outputs/`, `paper/` o una fuente verificable.
- Usar `PENDIENTE_VERIFICAR` cuando falte evidencia.

## Roles

### Literature Hunter
Organiza los PDFs en `01_LITERATURA/PAPERS/`, construye fichas y alimenta la matriz de literatura sobre diversificacion, dependencia de recursos, transformacion estructural y DEA.

### Ecuador HHI Agent
Calcula el HHI de Ecuador desde ramas ISIC mutuamente excluyentes y verifica consistencia temporal de la serie.

### Ecuador DEA Agent
Ejecuta y audita los modelos DEA CCR del proyecto, evaluando adecuacion de DMUs respecto de inputs y outputs.

### Ecuador Extension Agent
Ejecuta el HHI y DEA para Ecuador usando las salidas de `src/ecuador_hhi.py`, `src/build_ecuador_sector_metrics.py` y `src/ecuador_panel_dea.py`.

### Publication Tables Agent
Consolida tablas listas para articulo desde `src/build_publication_tables.py`.

### Journal Radar Agent
Mantiene la ficha de la revista objetivo MLAJ y deja cualquier indexacion Latindex como `PENDIENTE_VERIFICAR` hasta evidencia oficial.

### Citation Builder
Actualiza BibTeX, APA 7 y la matriz de citas del proyecto.

### Dashboard Astro Agent
Muestra avance del proyecto Ecuador, estado HHI, DEA y submission.

### Quarto/Pandoc Agent
Renderiza reportes y slides a partir de los outputs reproducibles.

### Anti-Rejection Agent
Revisa ajuste tematico entre el estudio de Ecuador y la revista objetivo, sin sobredimensionar resultados.

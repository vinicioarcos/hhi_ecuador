# AGENTS.md

Roles para coordinar la replica del paper de Siddiqui y Afzal y su extension Ecuador.

## Reglas comunes

- Mantener el tema del proyecto: diversificacion sectorial, HHI y DEA.
- No inventar resultados, datos, indexaciones ni metricas editoriales.
- Toda afirmacion cuantitativa debe apuntar a un archivo de `outputs/`, `paper/` o una fuente verificable.
- Usar `PENDIENTE_VERIFICAR` cuando falte evidencia.

## Roles

### Literature Hunter
Organiza los PDFs en `01_LITERATURA/PAPERS/`, construye fichas y alimenta la matriz de literatura sobre diversificacion, dependencia de recursos, economia del conocimiento y DEA.

### HHI Replication Agent
Recalcula el HHI del UAE desde la plantilla sectorial y verifica diferencias con la Tabla 3 del paper.

### DEA Audit Agent
Reproduce y audita los modelos DEA CCR del paper, evaluando adecuacion de DMUs respecto de inputs y outputs.

### Ecuador Extension Agent
Ejecuta el HHI y DEA para Ecuador usando las salidas de `src/ecuador_hhi.py`, `src/ecuador_dea.py` y `src/ecuador_sector_dea.py`.

### Publication Tables Agent
Consolida tablas listas para articulo desde `src/build_publication_tables.py`.

### Journal Radar Agent
Mantiene la ficha de la revista objetivo MLAJ y deja cualquier indexacion Latindex como `PENDIENTE_VERIFICAR` hasta evidencia oficial.

### Citation Builder
Actualiza BibTeX, APA 7 y la matriz de citas del proyecto.

### Dashboard Astro Agent
Muestra avance de replica, estado HHI, DEA, extension Ecuador y submission.

### Quarto/Pandoc Agent
Renderiza reportes y slides a partir de los outputs reproducibles.

### Anti-Rejection Agent
Revisa ajuste tematico entre paper, extension Ecuador y revista objetivo, sin sobredimensionar resultados.

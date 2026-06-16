# REPLICA_AFZAL_2021_UAE

Carpeta para replicar y extender el paper:

**Siddiqui, S. A. & Afzal, M. N. I. (2022). _Sectoral diversification of UAE toward a knowledge-based economy_. Review of Economics and Political Science, 7(3), 177–193.**

## Qué replica

El paper combina tres componentes:

1. Visualización de indicadores de economía del conocimiento.
2. Cálculo del índice Herfindahl-Hirschman, HHI, usando formación bruta de capital fijo por 18 sectores de Emiratos Árabes Unidos, 2010–2017.
3. DEA CCR para evaluar eficiencia relativa de pilares de economía del conocimiento: régimen económico-institucional, innovación, TIC y educación/capital humano.

## Estructura

```text
REPLICA_AFZAL_2021_UAE/
├── data/
│   ├── raw/
│   │   ├── hhi/                 # Plantilla para datos sectoriales Bayanat/UAE Open Data
│   │   └── wdi/                 # Datos descargados desde World Bank API
│   └── processed/               # Datos limpios y resultados intermedios
├── literature/                  # PDF base y referencias
├── notebooks/                   # Notebook reproducible
├── outputs/
│   ├── figures/
│   └── tables/
├── paper/                       # Reporte Quarto/Pandoc
├── src/                         # Código Python
├── tests/                       # Pruebas básicas
├── docs/                        # Notas metodológicas
├── tasks/                       # Roadmap de replicación
└── prompts/                     # Prompts para Codex/Claude/Gemini
```

## Instalación

```bash
cd REPLICA_AFZAL_2021_UAE
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```powershell
cd REPLICA_AFZAL_2021_UAE
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Flujo mínimo

Primero calcula/valida HHI con los valores publicados:

```bash
python src/hhi.py --paper-table
```

Luego genera figuras:

```bash
python src/visualize.py
```

Para DEA con datos propios:

```bash
python src/dea_ccr.py --input data/processed/dea_input.csv --output outputs/tables/dea_efficiency.csv
```

## Dato importante

La carpeta incluye una plantilla para cargar los datos de formación bruta de capital fijo por sector. No inventa los datos sectoriales originales. Eso sería cocina econométrica con humo, y aquí no vendemos parrilladas.

Para replicación exacta del HHI, descargue los datos de UAE Open Data/Bayanat indicados en el paper y complete:

`data/raw/hhi/gfcf_sector_template.csv`

con columnas:

```text
year, sector, gross_fixed_capital_formation_million_aed
```

## Extensión sugerida para Ecuador

La misma arquitectura puede adaptarse a Ecuador usando cuentas nacionales por rama de actividad del BCE, exportaciones por producto o empleo por rama ENEMDU. El HHI se mantiene igual; cambia la fuente y la unidad de análisis.
# hhi_ecuador

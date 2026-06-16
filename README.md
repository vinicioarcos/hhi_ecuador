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

## Procedencia de los datos

El proyecto combina datos de **dos universos** distintos. Es importante no
mezclarlos:

| Origen | Archivo | Fuente | Se usa para |
|---|---|---|---|
| **Paper (UAE)** | `data/raw/hhi/gfcf_sector_template.csv` | KAPSARC / FCSC (←Bayanat 2020), GFCF por 18 sectores, AED corrientes | Recalcular el HHI |
| **Paper (UAE)** | `data/processed/hhi_values_from_paper_table3.csv` | Valores **publicados** en la Tabla 3 de Siddiqui & Afzal (2022) | Validar la réplica |
| **Paper (UAE)** | `data/raw/wdi/wdi_uae_2000_2020.csv` | World Bank WDI, 2000–2020 | DEA CCR (pilares de economía del conocimiento) |
| **Extensión (Ecuador)** | descarga en vivo | UNSD National Accounts Main Aggregates, VAB por 7 ramas ISIC | HHI de Ecuador |

La comparación recalculado-vs-publicado se materializa en
`outputs/tables/hhi_replication_comparison.csv` (lo genera `src/compare_hhi.py`).

## Flujo completo

Todo el pipeline está orquestado en el `Makefile` y respeta el orden de
dependencias:

```bash
make all        # hhi -> dea -> ecuador -> report
```

O por etapas:

```bash
make data       # descarga KAPSARC + WDI (requiere internet)
make hhi        # HHI UAE desde datos primarios + comparación contra el paper + figura
make dea        # construye dataset WDI y corre los modelos DEA CCR
make ecuador    # extensión Ecuador: HHI UNSD + DEA anual/sectorial + tablas de publicación
make report     # renderiza el reporte Quarto (HTML + PDF Typst)
make test       # pruebas
```

Ejecución manual equivalente de las piezas clave:

```bash
python src/hhi.py --input data/raw/hhi/gfcf_sector_template.csv   # HHI UAE
python src/compare_hhi.py                                         # validación vs Tabla 3
python src/run_dea_analysis.py                                    # DEA CCR (4 modelos)
python src/ecuador_dea.py                                         # DEA exploratorio Ecuador
python src/ecuador_sector_dea.py                                  # DEA sectorial Ecuador
python src/build_publication_tables.py                            # tablas finales del artículo
quarto render                                                     # reporte final
```

El PDF usa el formato Typst de Quarto, por lo que no requiere una instalación de LaTeX/TinyTeX.

## Dato importante

La carpeta incluye una plantilla para cargar los datos de formación bruta de capital fijo por sector. No inventa los datos sectoriales originales. Eso sería cocina econométrica con humo, y aquí no vendemos parrilladas.

Para replicación exacta del HHI, descargue los datos de UAE Open Data/Bayanat indicados en el paper y complete:

`data/raw/hhi/gfcf_sector_template.csv`

con columnas:

```text
year, sector, gross_fixed_capital_formation_million_aed
```

## Extensión para Ecuador

La extensión implementada usa VAB por 7 ramas ISIC desde UNSD para calcular el HHI de Ecuador
2000-2024. Incluye dos DEA:

- DEA anual exploratorio: años como DMU; minería/utilities como input; manufactura,
  transporte/comunicación y comercio/hoteles como outputs.
- DEA sectorial fortalecido: sectores como DMU; participación promedio 2000-2004 como input y
  participación promedio 2020-2024 como output. Este diseño usa 7 sectores, 1 input y 1 output,
  por lo que supera el umbral 3*(m+s)=6.

Para una versión todavía más fuerte del artículo, el siguiente salto sería enriquecer el DEA
sectorial con empleo, exportaciones, productividad, capital, innovación o adopción digital por
rama; o construir un DEA provincial con datos administrativos comparables.

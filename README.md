# REPLICA_AFZAL_2021_UAE

Proyecto reproducible para replicar y extender el paper de Siddiqui y Afzal sobre diversificacion sectorial de Emiratos Arabes Unidos hacia una economia del conocimiento, manteniendo el tema original del repositorio.

## Paper base

**Siddiqui, S. A. & Afzal, M. N. I. (2022). _Sectoral diversification of UAE toward a knowledge-based economy_. Review of Economics and Political Science, 7(3), 177-193.**

DOI verificado en la bibliografia local: `10.1108/REPS-07-2021-0075`.

## Pregunta del proyecto

El proyecto replica tres piezas del paper base y anade una extension a Ecuador:

1. Recalculo del indice Herfindahl-Hirschman (HHI) para la formacion bruta de capital fijo por 18 sectores del UAE.
2. Auditoria metodologica del ejercicio DEA CCR usado para evaluar eficiencia de pilares de economia del conocimiento.
3. Extension a Ecuador con HHI por ramas ISIC y ejercicios DEA exploratorios/sectoriales.

## Estructura operativa

El motor de la replica ya existente sigue en:

```text
src/            Scripts Python de HHI, DEA y tablas publicables
data/           Datos raw y processed del flujo original
outputs/        Tablas y figuras generadas
paper/          Reporte Quarto original de la replica
tests/          Pruebas basicas
```

La estructura numerada se usa como capa de gobierno, literatura, submission y monitoreo:

```text
00_GOBIERNO/              Roadmap, bitacora y control del proyecto
01_LITERATURA/            PDFs, fichas, matrices y referencias
02_DATOS/                 Inventarios y notas del flujo reproducible
03_CODIGO/                Wrappers, Stata auxiliar y utilidades del proyecto
04_RESULTADOS/            Resultados compilados y verificaciones
05_MANUSCRITO/            Manuscrito base ES/EN y anexos
06_JOURNAL_RADAR/         Revista objetivo y estrategia editorial
07_SUBMISSION/            Cover letter, highlights y declaraciones
08_DASHBOARD_ASTRO/       Dashboard web del avance del proyecto
09_REPORTS_QUARTO/        Reporte reproducible complementario
10_SLIDES/                Slides para defensa y congreso
11_PANDOC/                Comandos de exportacion
12_SYSTEMATIC_REVIEW/     Protocolo y matriz de literatura sobre diversificacion
13_CONFERENCE_RADAR/      Congresos y seminarios
14_CITATION_ENGINE/       BibTeX, APA 7 y matriz de citas
15_AGENTS/                Roles academicos y tecnicos
16_PROMPTS/               Prompts especializados
17_AUTOMATION/            Pipeline completo
18_COMMON_PROTOCOLS/      Protocolos de integridad y no fabricacion
19_POLICY_BRIEF/          Policy brief del proyecto
20_AI_EXPOSURE_LINK/      No aplica por defecto; reservado para extensiones futuras
```

## Instalacion

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Flujo reproducible

Pipeline principal del proyecto:

```bash
make all
```

Etapas:

```bash
make hhi
make dea
make ecuador
make report
make test
```

Wrapper equivalente:

```bash
bash 17_AUTOMATION/run_pipeline.sh
```

## Datos

Fuentes actualmente contempladas:

- `data/raw/hhi/gfcf_sector_template.csv`: plantilla para UAE GFCF por 18 sectores.
- `data/processed/hhi_values_from_paper_table3.csv`: valores publicados en la Tabla 3 del paper.
- `data/raw/wdi/wdi_uae_2000_2020.csv`: WDI para auditoria DEA.
- `outputs/tables/hhi_ecuador.csv`: salida de la extension Ecuador basada en UNSD.

La tabla inventario para el manuscrito se genera con `src/build_publication_tables.py`.

## Regla de integridad

No inventar resultados, coeficientes, rankings, indexaciones ni cuartiles. Toda cifra debe salir de `outputs/`, `paper/` o fuentes verificables. Cuando falte verificacion usar `PENDIENTE_VERIFICAR`.

## Revista objetivo

La revista objetivo indicada por el usuario es **Multidisciplinary Latin American Journal (MLAJ)**. Su posible vinculacion con Latindex queda `PENDIENTE_VERIFICAR` hasta contrastar la indexacion oficial. Ver [06_JOURNAL_RADAR/mlaj_target_journal.md](/mnt/windows/1.-CODIGO/2.-PAPERS/REPLICA_AFZAL_2021_UAE/06_JOURNAL_RADAR/mlaj_target_journal.md).

# ECUADOR_HHI_DEA

## Pregunta del proyecto

El proyecto estudia la diversificacion sectorial de Ecuador con dos herramientas
reproducibles:

1. HHI por ramas ISIC a partir del Valor Agregado Bruto de la base UNSD.
2. Modelos DEA CCR exploratorios y sectoriales para evaluar transicion
   productiva entre ramas.

## Estructura operativa

El nucleo reproducible vive en:

```text
src/            Scripts Python para HHI, DEA y tablas publicables de Ecuador
data/           Datos auxiliares del flujo reproducible
outputs/        Tablas y figuras generadas
paper/          Reporte Quarto principal
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
20_AI_EXPOSURE_LINK/      Reservado para extensiones futuras
```

## Instalacion

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Flujo reproducible

Pipeline principal:

```bash
make all
```

Etapas:

```bash
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

- `outputs/tables/hhi_ecuador.csv`: participaciones por rama, HHI y
  clasificacion anual para Ecuador.
- `outputs/tables/dea_ecuador_dataset.csv`: dataset DEA con anos como DMU.
- `outputs/tables/dea_ecuador_sector_dataset.csv`: dataset DEA con ramas como
  DMU.

La tabla inventario para el manuscrito se genera con `src/build_publication_tables.py`.

## Regla de integridad

No inventar resultados, coeficientes, rankings, indexaciones ni cuartiles. Toda cifra debe salir de `outputs/`, `paper/` o fuentes verificables. Cuando falte verificacion usar `PENDIENTE_VERIFICAR`.

## Revista objetivo

La revista objetivo indicada por el usuario es **Multidisciplinary Latin American Journal (MLAJ)**. Su posible vinculacion con Latindex queda `PENDIENTE_VERIFICAR` hasta contrastar la indexacion oficial. Ver [06_JOURNAL_RADAR/mlaj_target_journal.md](/mnt/windows/1.-CODIGO/2.-PAPERS/REPLICA_AFZAL_2021_UAE/06_JOURNAL_RADAR/mlaj_target_journal.md).

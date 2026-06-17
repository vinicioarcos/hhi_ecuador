# Gobernanza del repositorio

## Alcance operativo

El nucleo reproducible del proyecto vive en:

- `src/`
- `data/`
- `outputs/`
- `paper/`
- `tests/`

La estructura numerada cumple funciones de gobierno, literatura, manuscrito,
submission y monitoreo. No reemplaza a `outputs/` ni a `paper/` como fuentes
oficiales de resultados.

## Reglas de orden

- Los artefactos generados localmente no deben ensuciar `git status`.
- Los resultados heredados de proyectos ajenos al tema HHI/DEA deben quedar
  archivados y rotulados como no nucleares.
- Toda cifra para manuscrito, dashboard o submission debe poder rastrearse a
  `outputs/`, `paper/` o una fuente externa verificable.

## Decisiones aplicadas

- Se ignoraron artefactos locales de Astro en `08_DASHBOARD_ASTRO/`.
- Se ignoraron exportaciones generadas en `09_REPORTS_QUARTO/` y `10_SLIDES/`.
- Se eliminaron remanentes de `overeducation` y mismatch educativo por estar
  fuera del alcance del proyecto.

## Pendientes de limpieza

- Los directorios nuevos del esquema numerado siguen sin commit; requieren una
  consolidacion selectiva cuando se decida el primer commit estructural.

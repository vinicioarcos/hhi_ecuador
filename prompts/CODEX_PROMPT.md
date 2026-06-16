# Prompt para Codex/Claude/Gemini

Actúa como econometrista reproducible. Debes completar y auditar la carpeta `REPLICA_AFZAL_2021_UAE`.

Objetivo: replicar el paper de Siddiqui & Afzal sobre diversificación sectorial de UAE hacia economía del conocimiento.

Tareas:
1. Verifica que `src/hhi.py` calcule correctamente HHI por año.
2. Crea un script `src/build_dea_dataset.py` que tome datos WDI descargados y construya un dataset DEA con columnas `factor`, `input_*`, `output_*`.
3. Añade validaciones de datos faltantes.
4. Genera tablas comparativas contra los valores publicados.
5. No inventes datos. Si falta fuente, deja TODO y documenta.
6. Mantén todo reproducible con comandos claros en README.
7. Genera una versión extendida para Ecuador usando BCE, ENEMDU o exportaciones si los datos están disponibles.

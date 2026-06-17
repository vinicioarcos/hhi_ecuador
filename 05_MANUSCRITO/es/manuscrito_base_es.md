# Titulo

Diversificacion sectorial de Ecuador: HHI por ramas ISIC y ejercicios DEA de transicion productiva

# Resumen

Este manuscrito analiza la diversificacion sectorial de Ecuador con una base
reproducible. El trabajo calcula el HHI usando siete ramas ISIC mutuamente
excluyentes derivadas del Valor Agregado Bruto de la base UNSD y complementa la
lectura con dos ejercicios DEA CCR: uno por anos y otro por ramas economicas.
Todas las cifras reportadas deben provenir del pipeline reproducible del
proyecto.

# Introduccion

La diversificacion economica ocupa un lugar central en economias expuestas a
choques externos y restricciones estructurales. En Ecuador, la medicion del
cambio sectorial exige una particion de ramas con poder discriminante y un uso
prudente de herramientas de frontera como DEA.

# Literatura

Integrar literatura sobre diversificacion sectorial, dependencia de recursos,
transformacion estructural e indicadores de concentracion usando los documentos
de `01_LITERATURA/PAPERS/` con metadata verificadas.

# Metodologia

- Recalculo del HHI por sector y ano.
- Construccion de ramas ISIC mutuamente excluyentes.
- DEA CCR con regla de adecuacion `n_DMU >= 3(m+s)`.
- Comparacion entre DEA por anos y DEA por ramas.

# Datos

- UNSD National Accounts Main Aggregates.
- Tablas derivadas en `outputs/tables/`.

# Resultados

Insertar solo tablas y figuras generadas en `outputs/` y `paper/`.

# Robustez

Discutir sensibilidad del HHI a la agregacion sectorial y sensibilidad del DEA
al numero de DMUs respecto de inputs y outputs.

# Discusion

Separar con claridad los hallazgos descriptivos del HHI y el alcance
exploratorio de los ejercicios DEA.

# Conclusion

Sintetizar la evidencia sin extrapolar mas alla de los resultados reproducibles.

# Referencias

Usar `14_CITATION_ENGINE/references.bib`.

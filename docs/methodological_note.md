# Nota metodológica de replicación

## HHI

El índice se calcula como:

```text
HHI_t = sum_i (X_it / X_t)^2
```

donde `X_it` es la formación bruta de capital fijo del sector `i` en el año `t`, y `X_t` es el total sectorial del año.

Clasificación usada en el paper:

- HHI < 0.15: economía diversificada.
- 0.15 < HHI < 0.25: moderadamente diversificada.
- HHI > 0.25: menos diversificada.

## DEA

El paper usa DEA CCR. Esta carpeta implementa una versión input-oriented CCR con `scipy.optimize.linprog`.

Para una réplica publicable, conviene reportar:

- Modelo DEA usado: CCR/BCC, orientación input/output.
- DMU: pilares o años, según diseño.
- Inputs/outputs por pilar.
- Tratamiento de datos faltantes.
- Robustez: ventana temporal, sensibilidad por variable, comparación con bootstrap DEA si se desea.

Regla operativa usada en la réplica:

```text
n_DMU >= 3 * (inputs + outputs)
```

Los modelos que no cumplen esta regla se reportan como subespecificados. La extensión Ecuador
incluye dos diseños: un DEA anual exploratorio y un DEA sectorial fortalecido con ramas ISIC como
DMU. El modelo sectorial usa participación promedio inicial como input y participación promedio
reciente como output. Es reproducible con la fuente UNSD existente, pero todavía debería
enriquecerse con empleo, productividad, exportaciones, capital, innovación o datos provinciales si
esas fuentes comparables se incorporan al proyecto.

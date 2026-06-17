version 18
clear

import delimited "outputs/tables/publication_table_dea_model_audit.csv", varnames(1)
summ n_inputs n_outputs n_dmu threshold_3x mean_efficiency
export delimited using "04_RESULTADOS/tablas/dea_audit_stata.csv", replace

version 18
clear

import delimited "outputs/tables/publication_table_uae_hhi_replication.csv", varnames(1)
summ year replicated_hhi published_hhi abs_diff
export delimited using "04_RESULTADOS/tablas/uae_hhi_validation_stata.csv", replace

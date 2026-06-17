# Agents registry

| Agent | Scope | Inputs | Outputs |
|---|---|---|---|
| HHI Replication Agent | UAE Table 3 replication | `data/raw/hhi/`, `data/processed/hhi_values_from_paper_table3.csv` | `outputs/tables/hhi_replication_comparison.csv` |
| DEA Audit Agent | UAE DEA audit | `data/raw/wdi/`, DEA scripts in `src/` | `outputs/tables/dea_models_summary.csv` |
| Ecuador Extension Agent | Ecuador diversification extension | `src/ecuador_*` | `outputs/tables/hhi_ecuador.csv` and DEA outputs |
| Journal Radar Agent | MLAJ submission prep | Official journal website | Journal file and submission templates |

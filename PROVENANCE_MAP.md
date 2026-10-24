# Provenance map

Every reported number traces through this chain:

```
coded evidence tables (CSV)  ->  deterministic builders (*.py)  ->  generated tables / figures  ->  manuscript.tex / supplement.tex
```

## Coded evidence

The coded evidence tables are frozen in the private research repository, under the decision records cited in the manuscript.

| Layer | Files (under `05_papers/representation_transport/`) | Content |
|---|---|---|
| Frame | `evidence_universe/layer_a_reconciliation/RECONCILED_LAYER_A_MANIFEST.csv`, `ANALYSIS_UNITS.csv` | The 43 Layer A frame members, their verification status, dependence groups and transport families |
| Layer A cells | `evidence_universe/layer_a_geometry/LAYER_A_SUPPORT_GRID.csv` | 43 experiments × 6 dimensions; V / I / E / U codes per cell |
| Layer A geometry | `evidence_universe/layer_a_geometry/LAYER_A_SUPPORT_GEOMETRY.csv`, `LAYER_A_BLOCKER_DECOMPOSITION.csv`, `PRE_CENSUS_MAPPED_LAYER_A_SUBSET_GEOMETRY.csv` | Family counts per stage; the selection audit |
| Layer B (audit, not a census) | `final_scope_c/LAYER_B_SUPPORT_AUDIT.csv`; `evidence_universe/layer_b_extraction/rime/*.csv` | The 9 audited historical and adjacent designs; the RIME extraction |
| Support paths | `final_scope_c/*_SUPPORT_PATHS_FINAL.csv`, `SCOPE_C_SUPPORT_UNION.csv`, `SCOPE_C_FINAL_SUPPORT_GEOMETRY.csv` | Every focal comparison, with the last strict stage reached |
| Labels and reporting | `final_scope_c/FINAL_SCOPE_C_T_SUPPORT.csv`, `MINIMUM_REPORTING_FOR_TRANSPORTABLE_BI_EVIDENCE.md` | Transport-support labels (supplementary); the 11-item reporting list |
| Coding manual | `coding_reliability/CODEBOOK_v1.4.md`, `reliability_results_pre_adjudication.csv` | The codebook; the pre-adjudication agreement statistics |
| Numeric claims | `paper/PAPER_NUMERIC_CLAIMS.csv`; `manuscript/revision_v1/V1_NUMERIC_CLAIMS.csv`; `manuscript/supplement/SUPPLEMENT_NUMERIC_CLAIMS.csv` | Claim ids N-xx, F-01 and S-xx, cited in TeX comments next to each number |

## Builders

| Builder (under `05_papers/representation_transport/manuscript/`) | Produces |
|---|---|
| `scripts/build_manuscript_tables.py` | `generated/table1.tex`, `generated/table2.tex`, `supplement/table_s3_near_miss.tex`, `revision_v1/V1_NUMERIC_CLAIMS.csv` |
| `scripts/build_supplement_tables.py` | `supplement/generated/*.tex`, `supplement/SUPPLEMENT_NUMERIC_CLAIMS.csv` (it stops if any recomputed count differs from the frozen claims) |
| `scripts/build_ontology_audit.py` | `revision_v1/NEAR_MISS_ONTOLOGY_AUDIT.csv` and `NEAR_MISS_ONTOLOGY_COUNTS.csv` (counting units of Table S3 and Figure 4) |
| `figures/build_figures.py` | `figures/fig1`–`fig5` (PDF / SVG / PNG), the figure data CSVs and `FIGURE_BUILD_MANIFEST.csv` |
| `scripts/build_manuscript.py`, `scripts/build_supplement.py` | `manuscript.pdf`, `supplement/supplement.pdf`, the build records and the numeric audits |
| `scripts/build_tex_audit.py` | `revision_v1/TEX_NUMERIC_AUDIT.csv`: every number in the manuscript and its provenance tag |

## Reliability authority

`09_meta/decision_log/2026-10-18_support-coding-reliability-adjudication.md` is the decision record that holds the pre-adjudication reliability table. `build_tex_audit.py` reads the rows of that table, which are the REL tag.

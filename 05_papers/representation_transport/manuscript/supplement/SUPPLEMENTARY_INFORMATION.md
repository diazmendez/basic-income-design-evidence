# Supplementary Information: plan and contents (manuscript v1, D047)

**D048A:** the supplement is now compiled from [`supplement.tex`](supplement.tex) to `supplement.pdf` by `scripts/build_supplement.py` (tables from `scripts/build_supplement_tables.py`; build record `SUPPLEMENT_BUILD_RECORD.csv`; numeric audit `SUPPLEMENT_NUMERIC_AUDIT.csv`; visual audit `SUPPLEMENT_VISUAL_AUDIT.md`). This plan is kept as the D047 index; the S10 definitions table below is read by the builder.

This file indexes the material moved out of the main text by D046 / D047. Each entry points to a frozen, deterministic authority, and no number here is hand-typed.

| Section | Content | Authority / build |
|---|---|---|
| S1 | Frame members and verification status: 39 verified, 2 pending, 2 frame conflict (F-01) | `evidence_universe/layer_a_reconciliation/RECONCILED_LAYER_A_MANIFEST.csv`; `revision_v1/V1_NUMERIC_CLAIMS.csv` |
| S2 | All 43 × 6 census support cells | `evidence_universe/layer_a_geometry/LAYER_A_SUPPORT_GRID.csv` |
| S3 | **Table S3** (former main Table 3): where key designs stop | `supplement/table_s3_near_miss.tex` (built by `scripts/build_manuscript_tables.py`) |
| S4 | Full path tables for withdrawal, conditionality and cadence; Layer-B design audit | `final_scope_c/*_SUPPORT_PATHS_FINAL.csv`; `LAYER_B_SUPPORT_AUDIT.csv` |
| S5 | Full 11-item minimum reporting standard, with the blocker each item addresses | `final_scope_c/MINIMUM_REPORTING_FOR_TRANSPORTABLE_BI_EVIDENCE.md` |
| S6 | Coding manual (v1.4) and a summary of the rule history (rules H, I and J; general clarifications) | `coding_reliability/CODEBOOK_v1.4.md` |
| S7 | RIME plan matrix, contrast graph and source log | `evidence_universe/layer_b_extraction/rime/` |
| S8 | **Source-access table**, including the WRP restricted-data route (see below) | `manuscript/POST_D044_ACCESS_RECOVERABILITY_NOTE.md`; D042 source log |
| S9 | **Validation**: validators and mutation tests for every stage | `final_scope_c/validate_final_scope_c.py`; `layer_a_geometry/validate_layer_a_geometry.py`; `paper/validate_paper_architecture.py`; `manuscript/validate_manuscript_v1.py`; the mutation harnesses |
| S10 | **Dimension-level qualitative summaries** (the T0–T3 transport-support labels moved from the main text), with definitions and operational readings | `final_scope_c/FINAL_SCOPE_C_T_SUPPORT.csv`; `layer_a_geometry/LAYER_A_T_SUPPORT_ASSESSMENT.md` |
| Figure S1 | **Status-changing evidence by dimension** (former main Figure 5) | `figures/fig5_status_changing_evidence.pdf` (built by `figures/build_figures.py`) |

## S8 draft text: WRP route (neutral; supplement only)

> "For the Vermont Welfare Restructuring Project, restricted-use data are held by a data archive under a secure-download mechanism that requires ethics review, a data-security plan and an institutional data-use agreement. These requirements were not pursued in this independent project. The WRP conditionality contrast is therefore coded from its published report (stars only; no usable uncertainty)."

The draft names no fee, employer or correspondence. Its provenance is the author-supplied access metadata in `POST_D044_ACCESS_RECOVERABILITY_NOTE.md`. It is access metadata, not evidence.

## S10 definitions (as moved from the main text)

| Label | Meaning |
|---|---|
| T0 | No informative variation |
| T1 | Support from at most one independent family with a compatible estimate and inference beyond a verbal statement |
| T2 | At least two independent families with variation and a compatible estimate with inference beyond a verbal statement (stars or an exact p count here), but no clean discovery-and-validation separation |
| T3 | Independent discovery and validation support possible |

Baseline employment is a state summary, never T3.

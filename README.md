# Design variation is not design evidence: replication package

This is the replication package for the manuscript *Design variation is not design evidence: an audit of basic-income and guaranteed-income experiments* (Rogelio Diaz-Mendez).

- **Release:** v1.1.0.
- **Repository:** https://github.com/diazmendez/basic-income-design-evidence.
- **Source:** this tree is generated from private research-repository commit `62f393c755f373318b2e8a2f2e4fef4e72f5d793`.

## 1. What the paper asks

What can the existing experimental basic-income (BI) and guaranteed-income (GI) literature tell policymakers about specific choices in programme architecture? Those choices are the withdrawal schedule, conditionality, payment cadence, transfer magnitude, promised duration and baseline employment.

The paper audits, comparison by comparison, whether each design feature has evidence that passes four stages:
1. **variation**: the feature varies;
2. **isolation**: the feature is isolated;
3. **compatible estimand**: a compatible employment estimate is reported;
4. **usable uncertainty**: a published standard error or confidence interval is reported.

It counts independent transport families, and asks whether two of them exist, as a prospective discovery-and-validation test would require. Independent validation is a requirement of that test, not a fifth stage.

The main result is a structured negative feasibility result for employment. It is not a test of whether basic income works, and not evidence that design features are unimportant.

## 2. Evidence frame

| Layer | What it is | Size |
|---|---|---|
| **Layer A** | A census of a frozen, frame-defined universe of modern randomised BI/GI experiments with employment outcomes | 43 experiments: 39 verified, 2 pending, 2 frame conflicts |
| **Layer B** | An audit of historical and adjacent designs (not a census) | 9 designs |

The two layers are never pooled into one denominator. The frame is defined in the manuscript's Methods. It is not "every BI experiment ever run".

## 3. Authoritative files

| What | Where (under `05_papers/representation_transport/`) |
|---|---|
| Manuscript source and PDF | `manuscript/manuscript.tex`, `manuscript/references.bib`, `manuscript/manuscript.pdf` |
| Supplementary Information | `manuscript/supplement/supplement.tex`, `manuscript/supplement/supplement.pdf` |
| Coded evidence (frozen) | `evidence_universe/…`, `final_scope_c/…`, `coding_reliability/CODEBOOK_v1.4.md` |
| Numeric claims | `paper/PAPER_NUMERIC_CLAIMS.csv` and the claim files listed in `PROVENANCE_MAP.md` |
| Audits and build records | `manuscript/revision_v1/` (TeX numeric audit, ontology audit, bibliography verification, build record); `manuscript/supplement/SUPPLEMENT_*` |

`PROVENANCE_MAP.md` maps every table and figure to its builder and input files.

## 4. Rebuilding

Run these commands from the repository root. `ENVIRONMENT.md` lists the versions used.

```
cd 05_papers/representation_transport/manuscript
python3 -I scripts/build_manuscript_tables.py      # main tables, Table S3
python3 -I scripts/build_ontology_audit.py         # counting-unit audit of Table S3 / Figure 4
python3 -I scripts/build_supplement_tables.py      # supplement tables (stops if a count differs from the frozen claims)
python3 -I figures/build_figures.py                # Figures 1-5
python3 -I scripts/build_manuscript.py             # manuscript.pdf (needs pdflatex, bibtex, latexmk, pdfinfo)
python3 -I scripts/build_supplement.py             # supplement.pdf and its numeric audit
python3 -I scripts/build_tex_audit.py              # manuscript numeric audit
```

## 5. Validating

From the repository root:

```
python3 -I -B validate_release.py
```

It checks two things:
- every file against `RELEASE_MANIFEST.csv` (SHA-256);
- that every builder, run in check mode, reproduces the shipped tables, figure data and numeric audits.

**Other validators:** `validate_*.py` files elsewhere in the tree are the project's stage validators, listed in Supplementary Table S16. They are included for transparency. Most of them need the private repository's history, frozen-input hashes and intermediate records, so they are not expected to run here.

These are software consistency checks. They are not scientific validation of the coding or of the conclusions.

## 6. What is not included, and why

**Third-party documents.** Primary reports, articles and books are cited, not redistributed. That includes an author-shared book manuscript used in the prior-art audit.

**Restricted-use data.** None was used. That includes ICPSR restricted files.

**No participant-level data.** The audit codes published study-level information only.

**The private research repository.** It holds:
- the working history;
- decision records beyond the one needed for reproduction;
- intermediate extraction files;
- literature workspace;
- correspondence.

It stays private and is the source of truth. This repository is a one-way, derived snapshot. Do not edit it by hand: changes are made in the private repository and re-exported.

**AI session logs and transcripts.** Not included. The manuscript's GenAI-use disclosure describes the AI-assisted workflow.

## 7. Version correspondence

| Item | Value |
|---|---|
| Release | v1.1.0 |
| Generated from private commit | `62f393c755f373318b2e8a2f2e4fef4e72f5d793` |
| Manifest | `RELEASE_MANIFEST.csv` (path, bytes, SHA-256, licence) |
| Release metadata | `RELEASE_INFO.json` |

This repository is hosted on GitHub and has **no DOI or archival deposit**. GitHub hosting does not guarantee permanence.

## Licences

- **Code (MIT; `LICENSE`):** every `*.py` file (builders, validators, scripts).
- **Original non-code content (CC BY 4.0; `LICENSE-CC-BY-4.0.txt`):** the coded evidence tables produced by the project, documentation, the figures, and the manuscript and supplement sources and PDFs. Copyright 2026 Rogelio Diaz-Mendez.
- **Third-party material:** this package does not relicense any of it. Bibliographic references, and short quotations or factual extracts from cited sources within the coded tables, remain subject to their original rights. The cited works themselves are not included.
- The licence of each file is listed in `RELEASE_MANIFEST.csv`.

## Citation

See `CITATION.cff`.

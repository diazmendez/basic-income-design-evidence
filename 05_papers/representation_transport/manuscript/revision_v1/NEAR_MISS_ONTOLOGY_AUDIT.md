# Near-miss ontology and counting-unit audit (D048C)

**Built by:** `scripts/build_ontology_audit.py`. The machine-readable outputs are:
- `NEAR_MISS_ONTOLOGY_AUDIT.csv`: one row per entity;
- `NEAR_MISS_ONTOLOGY_COUNTS.csv`: the counts.

**Authorities:**
- `final_scope_c/{WITHDRAWAL,CONDITIONALITY,CADENCE}_SUPPORT_PATHS_FINAL.csv`;
- `final_scope_c/SCOPE_C_SUPPORT_UNION.csv`, for the dependence groups;
- the Table S3 case list (`scripts/build_manuscript_tables.py`, `CASES`);
- the Figure 4 row rule (`figures/build_figures.py`, `fig4()`).

The builder stops if the isolated entries differ from the frozen support-union isolated counts (N-13, N-14, N-15).

## Result

> **Table S3 contains 13 rows representing 12 unique designs, 12 unique transport families (and 12 dependence groups), and 11 isolated family–dimension support entries; the other 2 rows are bundled key comparators. Figure 4 shows exactly those 11 isolated family–dimension entries, which come from 10 distinct transport families.**

**How the counts relate:**
- **13 rows versus 12 designs.** Wageningen (X057, `LA-TF-X057-WAGENINGEN-PW`) is isolated on two dimensions, withdrawal and conditionality, so it occupies two rows.
- **13 rows versus 11 isolated entries.** Two rows are deliberately included bundled comparators that are not isolated: Seattle-Denver (X003, withdrawal, BUNDLED) and Minnesota MFIP (X067, conditionality, BUNDLED).
- **11 isolated entries.**
  - These are 5 withdrawal entries (B-MINCOME, Wageningen, NJ-P, Gary, RIME), 3 conditionality entries (Wageningen, Utrecht, Vermont WRP) and 3 cadence entries (Compton, Newark, FNLP).
  - They equal the support-union isolated counts N-13, N-14 and N-15 (5 / 3 / 3).
  - Because Wageningen appears twice, they come from 10 distinct transport families.
- **The historical "11".** The number appeared in task prose (the D048A brief), not in the repository's scientific files. It is exact only as **11 isolated family–dimension entries**, which is the row count of Figure 4. As "11 families" or "11 isolated families" it is wrong: there are 10 distinct families among the isolated entries and 12 designs in Table S3. This label is not used.

No scientific inconsistency was found:
- the entity sets of Table S3 and Figure 4 match their definitions;
- the counts match the frozen support-union counts.

The problem was **terminology and display units only**.

## Counting units (definitions used from D048C on)

| # | Unit | Definition | Example count |
|---|---|---|---|
| 1 | **Table row** | One printed row of a table | Table S3: 13 |
| 2 | **Dimension × design entry** | One architecture dimension paired with one design; equals one table row in Table S3 | 13 |
| 3 | **Experiment** | A Layer A frame member or a Layer B audited member (`experiment_id`, X…) | Table S3: 12 |
| 4 | **Design** | Used here as a display synonym for the experiment's design, named by the design label (B-MINCOME, RIME, …); one design = one experiment | 12 |
| 5 | **Focal comparison** | The comparison (contrast) on which V, I, E and U are coded for one dimension (`support_path`); a family-dimension can have several, and the cell representative is the one shown | One per row |
| 6 | **Support case** | A coded support row (`support_case_id`) linking a family, a dimension and an outcome domain to its comparisons | — |
| 7 | **Statistical dependence group** | `dependence_group_id`: estimates that share samples or assignment (D026) | 12 in Table S3 |
| 8 | **Transport family** | `transport_family_id`: sources that share the identifying variation; arms or sites of one coordinated experiment are one family (D026). **All "family" counts in the paper count these** | 12 in Table S3; 10 in Figure 4 |
| 9 | **Family-dimension support path / entry** | One transport family on one architecture dimension, represented by its cell-representative focal comparison | Figure 4: 11 |
| 10 | **Isolated comparison / entry** | A focal comparison with V = Y and I ∈ {PURE, CONDITIONABLE-BUNDLE} | 11 entries (5 / 3 / 3) |
| 11 | **Strict supporting family** | A transport family whose focal comparison on a dimension passes V, I, E-A-compatible E, and SE or CI | 1 withdrawal (B-MINCOME), 1 conditionality (Utrecht), 0 cadence (N-16) |
| 12 | **Broader-sensitivity supporting family** | An isolated family with an E-B (other extensive-margin) object and usable uncertainty. Sensitivity only | Wageningen on withdrawal and on conditionality (N-17: 2, 2, 0 together with the strict families) |

## Global terminology search

**Search scope:** the whole repository, excluding the gitignored `.literature/`.

**Patterns searched:**
- "11 (isolated) families";
- "isolated families";
- "near-miss families";
- "13 near";
- "12 design";
- "isolated designs";
- "near-miss design";
- "every independent family".

| Location | Wording | Exact? | Action |
|---|---|---|---|
| `manuscript.tex`, Figure 4 caption | "Rows are every independent family whose focal comparison is isolated" | **No.** Rows are family–dimension entries; Wageningen appears twice | **Corrected:** "Each row is one family–dimension entry: a transport family whose focal comparison on that dimension is isolated … (a family isolated on two dimensions appears twice: Wageningen)" |
| `figures/build_figures.py`, Figure 4 in-figure note | "Rows: every independent family whose focal path is isolated." | **No** | **Corrected:** "Rows: family-dimension entries whose focal path is isolated (a family can appear under two dimensions)." Figure 4 re-rendered; data CSV byte-identical; hashes in `D048A_AUTHORISED_REVISIONS.csv` |
| `supplement/supplement.tex`, S3 text | "lists every independent family whose focal comparison is isolated, or that is a key bundled comparator" | **No** | **Corrected:** exact 13 / 12 / 11 / 10 / 2 statement, traced to claim S-04 (from `NEAR_MISS_ONTOLOGY_COUNTS.csv`) |
| Supplement, Table S3 caption | "Where key designs stop" | Imprecise unit | Caption now states one row per dimension–design entry |
| `manuscript.tex` §5 | "Strictly supported isolated families were unchanged" | Yes: transport families per dimension | None |
| `manuscript.tex` §6 | "3 Layer-B families isolate the feature" | Yes (N-22) | None |
| `layer_a_geometry/LAYER_A_SUPPORT_GEOMETRY.csv`; `final_scope_c/RESEARCH_AGENDA_GAPS.csv` | "1 of 2 isolated families"; "1 of 5 isolated families" | Yes: per dimension | None (frozen authorities) |
| `09_meta/decision_log/2026-10-23_manuscript-adversarial-review.md` (D046) | "Figure 4 rows are chosen mechanically (every isolated family)" | Imprecise historical wording | Not edited (frozen record). Superseded by this audit |
| `09_meta/decision_log/2026-10-24_bibliography-and-supplement.md` (D048A) | "13 rows covering 12 distinct designs, not the '11 families' mentioned in the brief" | Correct as far as it goes | Clarified in D048C: 11 = isolated family–dimension entries |
| `05_papers/state_of_understanding/sou-v1/` | Earlier map-level counts | Frozen earlier output, different denominator | Out of scope; not edited |

## Figure 4 audit

| Question | Finding |
|---|---|
| Entity set | Every cell-representative path on withdrawal, conditionality or cadence with V = Y and isolation PURE or CONDITIONABLE-BUNDLE, in both layers |
| Counting unit | Family–dimension entry. There are 11 rows from 10 transport families |
| Is the entity set consistent with its intended definition? | **Yes.** It equals the support-union isolated counts N-13, N-14 and N-15 |
| Duplicated design | Wageningen, under withdrawal and conditionality. Intentional: it is isolated on both dimensions. Now stated in the caption and the figure note |
| Bundled comparators | **Not shown in Figure 4.** They appear only in Table S3, which says so |
| Kenya cadence path (C-SG10-05) | Not shown, correctly. It is not the cell representative (`cell_representative = NO`), so it does not count among the 3 isolated cadence entries |

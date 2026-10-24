# D034 Support-coding reliability adjudication and CODEBOOK v1.1

Date: 2026-10-18

Status:
accepted

**Type:** methods / evidence-map correction, after blinding. D034 adjudicates; [D033](2026-10-18_support-coding-reliability-protocol.md) remains the authoritative description of the blind protocol.
- No new H / R / M / E / QEU / COM records.
- No T-level change. H002 not created. D022 stays OPEN — WAITING.
- No literature search and no new study extraction. **Layer A extraction has not started.**

## Context

D033 froze CODEBOOK_v1 and built a blind 25-case packet. An independent second coder received only `CODEBOOK_v1.md`, `BLIND_RECODING_PROTOCOL.md`, `blind_case_packets.md` and the empty `blind_cases.csv`. They had no access to the repository, the sealed manifest, the original codes or the project history. The completed file was placed in the working tree as `second_coder_blind_cases.csv`.

## Decision

### 1. Returned file (primary provenance, preserved byte-for-byte)

- **File:** `05_papers/representation_transport/coding_reliability/second_coder_blind_cases.csv`
- **SHA-256 (recorded on receipt, before any comparison):** `bdc941fe130b5c364484c7ebf4b427fe2e2c526097bb6d00a76a433407d4965c`
- **Structure (checked before the manifest was opened):**
  - 25 rows, BC001–BC025, with no duplicates or gaps;
  - the columns are identical to the D033 template, with no original-code columns;
  - every primary code, confidence, reason and ambiguity flag is populated, using allowed values only.
- **Confidence:**

  | Variable | HIGH | MEDIUM | LOW |
  |---|---|---|---|
  | V | 25 | 0 | 0 |
  | I | 22 | 1 | 2 |
  | E | 24 | 1 | 0 |
  | U | 24 | 0 | 1 |

- **ambiguity_flag = YES:** BC015, BC019.
- **Preservation:** the file is never written by any script. The empty template `blind_cases.csv` is unchanged.

### 2. Sealed manifest (opened after §1 passed)

All of the following were verified against the D033 commit `4fb85a0`:
- seed 20261018;
- frozen `support_incidence` SHA-256 `3937049e…5de10`;
- the BC ↔ support-row map is one-to-one and follows the recorded permutation;
- the hashes of CODEBOOK_v1, the packet and the manifest match.

Nothing in it was altered.

### 3. Pre-adjudication reliability: the independent result

Computed by script from the two files. No value is hard-coded.

| Variable | Agreement | Raw | Cohen's kappa (unweighted) |
|---|---|---|---|
| V | 25 / 25 | 1.00 | **NOT DEFINED — no marginal variation** (all codes Y) |
| I | 23 / 25 | 0.92 | 0.884 |
| E (separate codes) | 19 / 25 | 0.76 | 0.490 |
| E (E-A / caveat merged, protocol §3) | 21 / 25 | 0.84 | 0.606 |
| U (exact raw code) | 24 / 25 | 0.96 | 0.936 |
| usable_U | 24 / 25 | 0.96 | 0.918 |

- **Disagreement cases (8):** BC003, BC009, BC016, BC017, BC018, BC019, BC020, BC023.
  - All 8 are within-study cases. The 11 between-study cases have 0 disagreements.
  - By dimension: withdrawal 3 / 4; cadence 2 / 3; conditionality 2 / 4; duration 1 / 8; magnitude 0 / 5; baseline 0 / 1.
- **BC015** has an ambiguity flag but no primary disagreement.
- **Detail:** [`reliability_summary.md`](../../05_papers/representation_transport/coding_reliability/reliability_summary.md), [`reliability_confusion_matrices.md`](../../05_papers/representation_transport/coding_reliability/reliability_confusion_matrices.md), [`reliability_results_pre_adjudication.csv`](../../05_papers/representation_transport/coding_reliability/reliability_results_pre_adjudication.csv).

**No post-adjudication agreement is computed or reported as reliability.**

### 4. Adjudication

Full record: [`adjudication_log.md`](../../05_papers/representation_transport/coding_reliability/adjudication_log.md).

Each disagreement was decided from codebook semantics and repository source records. None was decided by support strength, T-levels, P2 or earlier prose.

| Case (row) | Field: original → second → **final** | Cause | Pipeline effect |
|---|---|---|---|
| BC003 (SG10 cadence, enterprise) | E: NOT-APPLICABLE → E-C → **E-C** | ORIGINAL-CODER-ERROR | none (not employment domain) |
| BC009 (FNLP cadence) | I: PURE → CB → **CONDITIONABLE-BUNDLE** | ORIGINAL-CODER-ERROR | none (still isolated) |
| | E: E-A → caveat → **E-A (caveat)** | ORIGINAL-CODER-ERROR | none (caveat passes the E stage) |
| BC016 (Gary withdrawal) | E: E-A → NONE → **NONE** | ORIGINAL-CODER-ERROR | **leaves the E-A stage** |
| BC017 (MFIP conditionality) | E: E-A → caveat → **E-A (caveat)** | ORIGINAL-CODER-ERROR | none |
| BC018 (DIME withdrawal arms) | U: SE → NOT-INTEGRATED → **NOT-INTEGRATED**; usable_U: YES → **NO** | ORIGINAL-CODER-ERROR | none (BUNDLED) |
| BC019 (SIME/DIME duration, employment) | E: NONE → E-C → **NONE** | AMBIGUOUS-CODEBOOK | none |
| BC020 (Utrecht conditionality) | I: CB → PURE → **PURE** | AMBIGUOUS-CODEBOOK | none (still isolated) |
| BC023 (NJ-P withdrawal) | E: E-A → NONE → **NONE** | ORIGINAL-CODER-ERROR | **leaves the E-A stage** |

**Cause counts (per disagreeing field):**

| Cause | Count |
|---|---|
| ORIGINAL-CODER-ERROR | 8 (BC018's U and usable_U counted separately) |
| AMBIGUOUS-CODEBOOK | 2 |
| SECOND-CODER-ERROR | 0 |
| AMBIGUOUS-SOURCE | 0 |
| PACKET-OMISSION | 0 |

The undocumented guarantee / tax-rate mix by duration in SIME/DIME, behind the BC015 and BC019 I-LOW flags, is a residual source gap. It caused no disagreement.

Five of the original-coder errors had been anticipated in the sealed author notes (D033). The second coder applied v1 as written.

### 5. CODEBOOK_v1.1 (frozen)

[`CODEBOOK_v1.1.md`](../../05_papers/representation_transport/coding_reliability/CODEBOOK_v1.1.md) = v1 plus general clarifications. v1 is preserved byte-identical.

| ID | Rule |
|---|---|
| A | **Design availability ≠ reported estimand.** No estimate, test or result statement for the focal comparison → E = NONE, U = NONE. `V = Y, I = PURE, E = NONE, U = NONE` is a valid case. A source-reported but not transcribed estimate counts as reported |
| B | "Any work" including own farm / business, averages of period employment indicators, and one-month recall are **E-A (caveat)**. E-A (caveat) **passes** the E-A-compatible stage |
| C | An independently crossed substantive policy factor, averaged over or conditioned on → **CONDITIONABLE-BUNDLE**, even when balanced by design |
| D | **Rule M for conditionality.** Intrinsic to the focal obligation rule: enforcement contacts, meetings, monitoring, mandatory activation referrals (and their removal), and the rule's own defined period. **Co-treatments:** independent services, counselling packages, changed caseworker models, cash-commitment changes, unrelated administrative changes |
| E | **Strict outcome-domain scoping** of E and U (see the BC019 resolution below) |
| F | Uncertainty form not described → **NOT-INTEGRATED**, usable_U = NO. Never inferred from historical codes or other-domain tables |
| G | I is coded from **documented** differences. Undocumented balance → `cotreatment` UNKNOWN, noted |

**BC019 resolution, rule E.** Support rows are indexed by `outcome_domain`: row grain S-{group}-{dimension}-{domain}, schema §2.
- An employment row codes only extensive-margin objects.
- A result in another labour domain belongs to that domain's own row, which codes it E-C. It is never copied, so one estimate cannot be counted in two rows.
- U pairs with the domain-scoped estimand.
- The rule was chosen for row grain and double-counting. Both options are pipeline-neutral (E-C never passes the E-A stage), so it was not chosen for support strength.

### 6. All 25 cases recoded under v1.1

[`final_adjudicated_codes.csv`](../../05_papers/representation_transport/coding_reliability/final_adjudicated_codes.csv) re-evaluates all 25 cases, with one note per case.
- The 17 agreeing cases keep their codes after re-evaluation. This includes rule C for the B-MINCOME and SIME/DIME crossed designs, and rule B for the single-period indicators.
- **Changed primary codes: 8 V / I / E / U fields** (plus the derived usable_U of BC018) **in 7 support rows.**
  - E: 5 (BC003, BC009, BC016, BC017, BC023);
  - I: 2 (BC009, BC020);
  - U: 1 (BC018).

### 7. Master map updated

The changes were made in `03_models/scripts/author_master_evidence_map_v1.py` (the authoring source of truth), not by hand-editing generated tables. The author and builder were then re-run.

**Changed support rows:**

| Support row | Change |
|---|---|
| `S-SG10-CADENCE-enterprise activity` | E NOT-APPLICABLE → E-C |
| `S-SG-FNLP-CADENCE-employment` | I PURE → CONDITIONABLE-BUNDLE; E E-A → E-A (caveat) |
| `S-SG08-WITHDRAWAL-employment` | E E-A → NONE |
| `S-SG-NJP-WITHDRAWAL-employment` | E E-A → NONE |
| `S-SG-MFIP-CONDITIONALITY-employment` | E E-A → E-A (caveat) |
| `S-SG07-WITHDRAWAL-employment` | U SE → NOT-INTEGRATED |
| `S-SG12-CONDITIONALITY-employment` | I CONDITIONABLE-BUNDLE → PURE |

Each changed row's `decision_ids` gains D034.

**Rebuilt views:**
- `support_incidence.csv`, `architecture_support_matrix.csv`, `evidence_pipeline_matrix.csv`, `master_evidence_map.csv` and `summary.md`.
- `contrasts.csv`, `outcome_evidence.csv`, `dependence_groups.csv` and `access_and_missingness.csv` are byte-unchanged.
- **Not modified:** point estimates, QEUs, E-records, contrast definitions, transport families and statistical groups.

The D033 packet builder and validator now read the frozen D033 universe from commit `4fb85a0`, because the live table carries v1.1 codes. A rebuild of the packet is byte-identical.

**Residual, recorded rather than changed** (reconciliation R-26, open):
- `contrasts.csv` isolation_status for C-FNLP-01 (PURE) and C-SG12-01 (CONDITIONABLE-BUNDLE) differs from the v1.1 support codes.
- The MFIP outcome-evidence compatibility_class (D025 rule, E-A) differs from the support E (E-A (caveat)).

These are contrast- and outcome-level attributes coded under the D025 schema. Changing them is excluded by this task. The support table is authoritative for support geometry, and no pipeline count depends on them.

### 8. Support geometry, before → after

Employment domain. Counts are transport families (D026).

| Dimension | Variation | Isolated | Isolated ∧ E-A-compatible | ∧ usable U | Between-study E-A ∧ U | Independent isolated split possible | T (unchanged) |
|---|---|---|---|---|---|---|---|
| MAGNITUDE_B2 | 5 → 5 | 0 → 0 | 0 → 0 | 0 → 0 | 5 → 5 | NO → NO | T3 |
| **WITHDRAWAL** | 4 → 4 | 3 → 3 | **3 → 1** | 1 → 1 | 0 → 0 | NO → NO | T1 |
| CONDITIONALITY | 4 → 4 | 2 → 2 | 2 → 2 | 1 → 1 | 0 → 0 | NO → NO | T2 |
| CADENCE | 2 → 2 | 2 → 2 | 2 → 2 | 0 → 0 | 0 → 0 | NO → NO | T1 |
| DURATION | 6 → 6 | 1 → 1 | 0 → 0 | 0 → 0 | 5 → 5 | NO → NO | T2 |
| BASELINE_EMPLOYMENT | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 | 1 → 1 | NO → NO | T0 |

**Withdrawal:**
- 4 families vary it: B-MINCOME, Gary, NJ-P, SIME/DIME.
- 3 isolate it by design: B-MINCOME, Gary, NJ-P.
- Only **1** publishes a compatible employment estimand for the isolated contrast: B-MINCOME, which also has usable U.
- Gary and NJ-P are **design-only**.

**Other dimensions:**
- **Conditionality:** the isolated families are still 2 (Utrecht now PURE, WRP PURE).
- **Cadence:** still 2 (Compton PURE, FNLP now CONDITIONABLE-BUNDLE with E-A (caveat)).

Independent-validation availability (≥ 2 isolated families with E-A and usable U) is NO for every dimension, before and after.

### 9. Reliability verdict: RELIABLE-WITH-REVISION

D033 §4 was applied after adjudication. Kappa was not used for the verdict.
- **Not RELIABLE:** two disagreements are pipeline-relevant (BC016, BC023 move two withdrawal families out of the E-A-compatible stage).
- **Not NOT-RELIABLE:** every disagreement is resolved by a frozen v1 rule or by a general v1.1 clarification re-applied to all 25 cases. No case-specific exception is used, and no material disagreement remains.
- **Interpretation:**
  - The codebook, applied by an independent coder, reproduces the geometry.
  - The weak point was the **original single-coder E codes**: E agreement was 19 / 25.
  - V, I and U agreement was high.

### 10. T-level safety check

The existing governance checks were re-run:
- master-map check 8: T-levels agree with the support map, and the D026 family-level necessary conditions hold;
- 4A3;
- H001;
- the estimand registry;
- the crosswalk.

All PASS. Every current T-level still satisfies its assignment conditions:
- **Withdrawal T1** rests on B-MINCOME local identification, which is unchanged. Gary and NJ-P were already "design-level candidates" in D018 / D019.
- **Conditionality T2** rests on MFIP and Utrecht as independent locally identified sources (D014). MFIP's E-A (caveat) still passes E.
- **Cadence T1**, **duration T2** and **B2 T3** rest on unchanged employment rows and unchanged between-study counts.

**T-levels unchanged.** The H002 trigger (D013 §9: some dimension with independent identification and validation, ≥ T3 transport) is **not met**, so H002 is not created. No STOP.

### 11. D022 and P2

- **D022:** OPEN — WAITING. D034 is not a support search and fires no reopen trigger.
- **P2 (narrow assessment):** the adjudication **strengthens the descriptive core** of the reporting-bottleneck diagnosis without changing the P2 status.
  - Before: withdrawal looked like "3 isolated, E-A-compatible families, but only 1 with usable uncertainty" (a U bottleneck).
  - After: **2 of the 3 isolated withdrawal families have the variation in their design but no reported compatible estimand at all.** The bottleneck sits earlier, at the E stage.
  - This separates two facts: **"the experiment design contains variation"** and **"the published record contains a compatible quantitative estimand with valid uncertainty"**. That distinction is a methodological result worth reporting.
  - It does not change novelty: D030 records that Burtless 1986 and Elmore 1986 anticipated the NIT diagnosis. It does not change coverage either: D032, Layer A 7 / 43.
  - **P2 stays WEAKENED (conditional). SCOPE-C unchanged.** The support-geometry coding is reproducible, so there is no ground to downgrade.

### 12. SoU v1 (immutable; not edited)

SoU v1 is a correct snapshot of `sou-v1-source` (737178a); `validate_report.py` PASS. Against the D034 map it is **historically stale** on these descriptive cells:
- Table 3 / REPORT support-geometry table: withdrawal *families isolated ∧ E-A* **3 → 1**.
- Table 3b / family-support matrix (and the figure built from it):
  - TF-GARY withdrawal `VIE-` → `VI--`;
  - TF-NJP withdrawal `VIE-` → `VI--`;
  - TF-SIMEDIME withdrawal `ViEU` → `ViE-`.

All other SoU-v1 counts are unchanged, and none of these cells carries a T-level. A future sou-v2 may incorporate them. This is not an error in v1.

### 13. Layer A freeze

CODEBOOK_v1.1 is frozen. The verdict is accepted, all 25 cases are recoded, the map is consistent and the validators pass. **Only now** may the primary reports for the 36 new Layer A experiments and RIME be coded (D032 NEXT-1), under v1.1 unchanged. **That extraction has not started.**

## Rationale

The blind design separates two questions: whether the rules are reproducible, and whether the existing codes followed them. The pre-adjudication comparison answers the first. Adjudication against the source records answers the second. Writing the clarifications as general rules and re-applying them to all rows prevents the codebook from being tuned to individual cases or to the Layer A evidence that follows.

## Alternatives considered

- **Patch only the 8 disagreement cases.** Rejected: the protocol requires all 25 cases to be re-coded under v1.1.
- **Option B for BC019** (code the best labour object across domains). Rejected: it breaks the domain-indexed row grain and double-counts the SIME/DIME hours contrasts, which already have their own hours row.
- **Keep Gary / NJ-P as E-A, because the design identifies the contrast.** Rejected: v1's reporting rule says the opposite, and the distinction is the point of the E stage.
- **Report post-adjudication agreement.** Rejected: it would not be independent.
- **Edit `contrasts.csv` / `outcome_evidence.csv` now.** Excluded by task scope; recorded as R-26.

## Evidence

- The returned file (SHA above) and the sealed manifest.
- Source records:
  - E028 (Kenya);
  - the FNLP audit (§3, §5);
  - the Gary and NJ-P audits (D019, D018);
  - E034 (MFIP);
  - contrast-graph CG-11 / CG-12 and E024 Table 12 (DIME; the SEs there are for hours);
  - the SIME/DIME duration audit (D021);
  - E031 regimes and implementation tables (Utrecht).

## Confidence

**High** for the metrics, which are mechanical and reproducible, and for the E / U corrections, which follow explicit v1 text.

**Medium** for:
- the BC020 PURE reading, which rests on rule D (implementation-intrinsic contacts) and has an unobserved sanctions first stage;
- the BC019 domain-scoping rule, a design choice.

## Consequences

- The support geometry now distinguishes **design-only** from **reported** variation.
- Withdrawal's isolated-and-reported count is 1 family.
- The Layer A extension is unblocked, under CODEBOOK_v1.1 only.

## Revisit when

- A Layer A coding needs a rule that v1.1 does not settle. That would create v1.2, re-applied to all cases.
- R-26 is reconciled in a map-level decision.
- Gary or NJ-P plan-level estimates with tests become available (for example via COM-004). E would then be re-coded from the new record.

## Related items

- D033, D032, D030, D026, D025, D022, D021, D020, D019, D018, D014, D013.
- [coding_reliability/](../../05_papers/representation_transport/coding_reliability/).
- [Master map](../../02_evidence/master_map/).
- PROSPECTUS §14.
- Validator: `validate_reliability_adjudication.py`.

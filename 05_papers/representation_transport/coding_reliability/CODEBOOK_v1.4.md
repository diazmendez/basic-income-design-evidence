# Support-geometry codebook v1.4 (FROZEN; current coding authority)

**Authority:** [D040](../../../09_meta/decision_log/2026-10-19_layer-A-post-census-reconciliation.md). Frozen 2026-10-19, **after** the completion of the D037 Layer A census extraction (6604b44) and before any Layer A aggregate geometry is computed. v1.4 is the coding authority for the reconciled Layer A census and all later coding.

Earlier authority (v1.3): [D039](../../../09_meta/decision_log/2026-10-18_outcome-definition-sufficiency-and-B2-heterogeneous-schedules.md), frozen 2026-10-18 after Layer A Batch 2.

**Lineage:**
- v1.4 = [CODEBOOK_v1.3](CODEBOOK_v1.3.md) (D039, preserved byte-identical) **plus one general rule, J: research-procedure co-interventions** (§11; marked **[v1.4]** where it touches earlier sections). No earlier rule was deleted or changed in meaning.
- v1.3 = [CODEBOOK_v1.2](CODEBOOK_v1.2.md) (D038, preserved byte-identical) **plus one general rule, I: the outcome-definition sufficiency rule**, with a clarification of the reporting rule for narrative subcomponent mentions and of U pairing (§10; marked **[v1.3]** where it touches earlier sections). No v1 / v1.1 / v1.2 rule was deleted or changed in meaning.
- v1.2 = [CODEBOOK_v1.1](CODEBOOK_v1.1.md) (D034, byte-identical) plus rule H, the employment-domain positive-state rule (§9).
- v1.1 = [CODEBOOK_v1](CODEBOOK_v1.md) (D033, unchanged) plus general clarifications A–G (§8).
- Rule H was triggered by RC-01 (Batch 1). Rule I was triggered by RC-02 and RC-03 (Batch 2). Rule J was triggered by RC-05 (Batch 6). Each was re-applied to **all** existing cases ([v1_2_reapplication.csv](v1_2_reapplication.csv); [v1_3_reapplication.csv](v1_3_reapplication.csv); [v1_4_reapplication.csv](v1_4_reapplication.csv)). Rules are never tuned case by case.

**Reliability status:**
- RELIABLE-WITH-REVISION (D033 / D034) remains the historical reliability result for v1 / v1.1. It is not recomputed.
- Rule H (v1.2) was frozen prospectively after Batch 1.
- Rule I (v1.3) was frozen prospectively after Batch 2 and before Batch 3.
- Rule J (v1.4) was frozen after the completion of the census, before any Layer A geometry.
- **Rules H, I and J have not been independently blind-second-coded.**

**Changes:** any later change creates v1.5 under the same procedure (re-apply to all cases; record every changed code).

## 0. What a case is

A **case** concerns:
- one **focal architecture dimension**;
- one **comparison**, or a small set of comparisons named in the packet;
- one **outcome domain**.

You code how the evidence described in the packet relates to that dimension. You do **not** judge whether the policy works, and you do **not** produce support levels.

**Two kinds of case:**
- **Within-study case:** the focal comparison is between randomised (or otherwise assigned) groups of one study.
- **Cross-study case:** the packet says the case is one study's contribution to a **predefined cross-study comparison** of the focal feature. Inside the study the feature takes a single value; it varies only *across* studies.

**Current outcome target** (for E): an employment-domain intention-to-treat (ITT) effect on **P(employed / working)** during treatment.

**[v1.1] Outcome domain is part of the case** (clarification E). E and U are coded only from estimands whose outcome object belongs to the case's declared outcome domain.

## 1. V — variation

**Question:** does the focal architecture dimension take different values in the focal comparison?

| Code | Rule |
|---|---|
| Y | **Within-study case:** the packet documents that the focal dimension differs between the compared groups (for example different withdrawal rates, payment schedules, promised durations, obligations). **Cross-study case:** the packet states that the case is defined in advance as a contribution to a cross-study comparison and gives the study's value of the feature |
| N | The packet documents that the focal dimension is identical between the compared groups (within-study), or the feature is not defined for the study (cross-study) |
| UNKNOWN | The packet does not establish whether the dimension differs |

**Decision tree:**
1. Is the case cross-study? If yes, and the packet gives a study-level value and states a predefined cross-study comparison, code **Y**. Otherwise code UNKNOWN.
2. Within-study: does a documented design fact show different values of the focal dimension between the groups? If yes, code **Y**; if documented identical, code **N**; otherwise **UNKNOWN**.

Never infer variation from programme or arm **names** alone ("higher-incentive", "basic income"). Use the documented parameters.

## 2. I — isolation

**Question:** does the focal comparison change the focal dimension without other substantive changes?

| Code | Operational definition |
|---|---|
| **PURE** | The focal dimension changes. **No other substantively relevant policy or implementation dimension changes** in the focal comparison, except **mechanical consequences** intrinsic to the focal dimension (see the rule below) |
| **CONDITIONABLE-BUNDLE** | Another substantive dimension also changes, **but** the design has an orthogonal or factorial structure, or a direct comparison, that lets the focal feature be compared **holding the other variation fixed or balanced**. For example: withdrawal crossed with an activation factor and the estimate averages over the crossed cells; a co-treatment randomised independently of the focal feature |
| **BUNDLED** | The focal feature changes **together with** one or more substantive features, **and** neither the design nor the report separates them. For example: an arm-vs-control contrast in which the arm differs from control in several policy parameters at once |
| **NOT-ISOLATED** | The feature varies **only between studies** (cross-study cases), or is otherwise inseparable from study identity or context |
| MODEL-ONLY | Evidence is a model counterfactual |
| NOT-APPLICABLE | No comparison exists |

**Rule M (mechanical consequences).** A consequence **intrinsic** to the focal policy profile is **not** a co-treatment. Examples:
- a lower withdrawal rate pays more to people with earnings;
- a front-loaded schedule gives more cumulative cash early;
- a work requirement needs enforcement contacts.

**But** an added service, a different benefit level unrelated to the focal rule, a different population or a different reference regime **is** a substantive change.

**[v1.1] Rule M for conditionality** (clarification D): administrative contacts, meetings, monitoring actions and mandatory activation referrals that exist **to implement the obligation regime**, and their removal or reduction when the obligations are removed, are intrinsic to the focal conditionality rule. So is the **defined period** of an obligation regime or exemption, when it is the period of the focal rule itself and the cash commitment is unchanged. By contrast, **independent services**, a **treatment-specific counselling or support package**, a changed caseworker model not required by the obligation rule, a changed cash commitment, or unrelated administrative changes **are** substantive co-treatments.

**Rule R (changed reference systems).** If the reference group's policy changes during the evaluation window (for example an activation model introduced for controls in year 2), that change is an **additional difference** in the comparison for that window.

**Decision tree:**
1. Is the case cross-study (the feature constant within the study)? → **NOT-ISOLATED**.
2. Is the evidence a model? → MODEL-ONLY.
3. List the documented differences between the compared groups, then remove the mechanical consequences (Rule M).
   - Only the focal dimension remains → **PURE**.
   - Others remain, and an orthogonal / factorial / direct comparison in the design or report holds them fixed → **CONDITIONABLE-BUNDLE**.
   - Others remain, with no such structure → **BUNDLED**.
4. A sample selected after randomisation does **not** change I. It is coded in `analysis_sample_class` and `post_randomisation_selection`.
5. **[v1.1] Crossed factors** (clarification C): a substantively distinct policy factor that is **independently crossed** with the focal feature (factorial or orthogonal assignment) **counts as an "other remaining" dimension in step 3**, even when it is balanced across the focal groups. If the estimate averages over, or conditions on, the crossed factor → **CONDITIONABLE-BUNDLE** (never PURE). Only if the focal comparison is reported **within one level** of the crossed factor, with no averaging, is it PURE.
6. **[v1.1] Undocumented balance** (clarification G): step 3 lists **documented** differences only. If the packet says that the balance of another factor across the focal groups is not documented, do not invent a difference: code I from the documented differences, set `cotreatment` = UNKNOWN, and state the gap in the reason.
7. **[v1.1] Baseline imbalance** arising by chance after valid randomisation is **not** a policy or implementation difference and does not change I.
8. **[v1.4] J. Research-procedure co-interventions** (§11): in step 3, documented research-procedure differences by assigned group (incentives, substantive framing, information beyond the minimum needed to communicate the focal rule, differential research contact, or a procedure the source calls inseparable from the intervention) are "other remaining" differences. Undocumented procedures are never inferred (G).

## 3. E — estimand compatibility

**Question:** what outcome estimand does the source report **for the case's comparison**?

**Reporting rule:** E classifies an estimand **for which the source reports an estimate, a test or an explicit result statement for this comparison**. A design that *could* identify an employment effect but **reports nothing** for this comparison is **NONE**.

**[v1.1] A. Design availability vs reported estimand.** A design that could identify the focal effect is **never enough** for E. If no estimate, test or explicit result statement for the focal comparison is reported in the case's outcome domain, **E = NONE** and **U = NONE**, whatever V and I are. A case may therefore validly be `V = Y, I = PURE, E = NONE, U = NONE`: the variation exists in the design but not in the published record. An estimate that a repository record says **is reported in the source but was not transcribed** still counts as reported (code E from its outcome object; U per §4 NOT-INTEGRATED).

**[v1.1] E. Outcome-domain scoping.** Support cases (support-incidence rows) are indexed by `outcome_domain`. E is coded **strictly within that domain**:
- **employment** domain: extensive-margin objects only (E-A, E-A (caveat), E-B); if the only reported labour result for the comparison is on another labour domain (hours, earnings, enterprise activity, job search), E = **NONE** for the employment case;
- **another labour domain** (hours, earnings, enterprise activity, job search…): the domain's object is **E-C**;
- a labour result of a different domain is mentioned in the reason but **never copied** into this case; it belongs to (or motivates) a separate case of its own domain. This prevents the same estimate from being counted in two domain rows;
- U is paired with the estimand that set E (so it is also domain-scoped).

**[v1.2] H. Employment-domain positive-state rule** (full text in §9): E-A, E-A (caveat) and E-B require that the estimated event / state is **entirely** a labour-market extensive-margin object. A positive category that a person can satisfy **solely** through a substantively non-labour-market state (unpaid caregiving, homemaking, student status, retirement, disability / inability to work, another explicitly non-labour state) is not an employment-domain outcome, **whatever the source calls it**. Read the exact positive and negative states; never code from the label.

**[v1.3] I. Outcome-definition sufficiency rule** (full text in §10): E-A, E-A (caveat) and E-B also require that the **factual record is sufficient** to establish that the positive state belongs entirely to the labour-market extensive margin. If the record documents the positive-state definition as UNKNOWN, AMBIGUOUS or NOT-STATED, the result establishes no compatible employment-domain estimand.

| Code | Rule |
|---|---|
| **E-A** | Individual-level binary **employed / working / labour-market participation** (worked, positive earnings, hours > 0), as a causal ITT or a directly equivalent treatment-effect contrast, during the treatment horizon |
| **E-A (caveat)** | As E-A, with a limited documented definitional issue that does not change the extensive-margin construct. For example "any work including own farm", a quarterly employment indicator averaged over quarters, or a one-month reference period. **[v1.1] B:** these examples are **always** E-A (caveat), never plain E-A: "any work" that includes own farm / own business; an average of quarterly (or other period) employment indicators over several periods used as the outcome; a one-month "worked in the past month" recall indicator. A single-period indicator (e.g. P(employed in quarter q), positive earnings in month m, weekly hours > 0) is plain E-A. **E-A (caveat) passes the E-A-compatible pipeline stage** (V → I → E-A-compatible → usable U); the caveat is carried as a flag |
| **E-B** | Another extensive-margin labour object: days employed; labour-force participation not equivalent to P(employed); an aggregate employment rate; a household-level employment indicator; a self-sufficiency threshold |
| **E-C** | Hours, earnings, work intensity, **enterprise activity**, job search or other non-extensive-margin labour objects |
| **NONE** | The source reports **no** estimate, test or result statement for this comparison on any labour outcome. **Descriptive arm-level shares reported without any between-arm estimate or test are NONE** (never upgraded to E-A). **[v1.2] H:** in an employment-domain case, also NONE when the **only** reported estimate / test / result statement is on a mixed labour + non-labour composite (no compatible employment estimand is reported) |
| NOT-APPLICABLE | The reported outcome is not a labour outcome at all (health, consumption, etc.). **[v1.2]** Used when the **case itself** concerns an outcome outside the labour domain under the schema's grain; never for an employment-domain case whose only result is a mixed composite (that is NONE) |

**Additional rules:**
- **Multiple outcomes for one comparison:** code the **most compatible** reported estimand. Order of compatibility: E-A > E-A (caveat) > E-B > E-C > NONE. Record the others in the reason.
- **Several comparisons in one case** (for example a 2017 and a 2018 contrast, or several subgroups): code the most compatible across them and note the others.
- **Arm vs control vs direct arm vs arm:** E describes the outcome object. Which comparison is reported is captured in I and in `contrast_directness_class`.
- **Pooled-site analyses:** code what the pooled analysis reports.
- **Selected completer samples:** E is unaffected **unless** only descriptive shares are reported (then NONE). The selection is coded in `analysis_sample_class`.

## 4. U — uncertainty

**Question:** what is the strongest **published** uncertainty information for the estimate(s) that determined E?

| Raw code | Rule |
|---|---|
| SE | A standard error of the estimate is published |
| CI | A confidence interval is published (and no SE) |
| EXACT-P | Only an exact p-value (or q-value) of the estimate or test is published; no SE or CI |
| TEST-STAT | Only a test statistic (t, z, F) is published with the estimate; no SE, CI or exact p |
| P-CATEGORY | Only "p < x" categories |
| STARS | Only significance stars |
| VERBAL | Only a verbal statement (for example "not statistically different") |
| NONE | No uncertainty information, or no estimate at all |
| NOT-INTEGRATED | A repo record says the estimate and its uncertainty exist in a source but were not transcribed. **Code the uncertainty form the record describes** if it is described; NOT-INTEGRATED only if the form is not described. **[v1.1] F:** when the form is not described, U = NOT-INTEGRATED and usable_U = **NO**. Never infer SE or CI from a historical code, from the study's other tables (another outcome or domain), or from the general reporting style of the source |
| MODEL-ONLY | Model output |

**Precedence:** SE > CI > EXACT-P > TEST-STAT > P-CATEGORY > STARS > VERBAL > NONE. **Pair U with the outcome chosen for E.**

**usable_U = YES only if the raw code is SE or CI.** Otherwise NO. This is deliberately stricter than "some inferential information exists".

**Additional rules:**
- **Derived uncertainty:** an SE **computed by the project** (for example |estimate| / t) is **not** published uncertainty. Code the published form (TEST-STAT) and usable_U = NO.
- **Exact p without coefficient uncertainty:** EXACT-P, usable_U = NO.
- **Stars only:** STARS. **Verbal null:** VERBAL.
- **Arm-vs-control SEs only, focal arm-vs-arm not reported:** code U for the comparison(s) named in the case. If the case's comparisons are the arm-vs-control ones, code their SE. Do **not** combine arm SEs into an arm-vs-arm SE.
- **Cross-study cases:** U is the uncertainty of the study's own estimate used in the cross-study comparison.

## 5. Auxiliary diagnostic fields (code where the packet allows)

| Field | Codes |
|---|---|
| `variation_level` | WITHIN-STUDY / BETWEEN-STUDY |
| `analysis_sample_class` | A (randomised ITT, full or near-full sample) / B (selected after randomisation, e.g. completers, continuous households, structural-model sample) / C (non-randomised or model-dependent) / UNKNOWN / NOT-APPLICABLE |
| `contrast_directness_class` | A (a direct randomised contrast estimate is reported) / B (a regression or factorial coefficient directly identifies the contrast) / C (arm-vs-control only, or a test without an estimate, or a non-randomised comparison) / D (structural / model) / DESIGN-ONLY (design exists; no estimate reported) |
| `post_randomisation_selection` | YES / NO / UNKNOWN / NOT-APPLICABLE |
| `cotreatment` | A (none) / B (present but orthogonal or conditionable) / NONE-KNOWN (none documented) / UNKNOWN |

## 6. Edge cases settled in advance

| Edge case | Rule |
|---|---|
| Arm-v-control vs direct arm-arm | I: an arm-vs-control comparison that changes several parameters is BUNDLED unless a factorial / direct structure exists. U: code the comparisons the case names; never combine SEs |
| Stars only | U = STARS; usable_U NO |
| Exact p without coefficient uncertainty | U = EXACT-P; usable_U NO |
| Selected completer samples | `analysis_sample_class` = B; E unchanged unless only descriptive shares are reported (then NONE) |
| Factorial designs | Averaging over an orthogonal crossed factor → CONDITIONABLE-BUNDLE for I (when the crossed factor is a substantive policy dimension). **[v1.1] C:** applies even when the crossed factor is balanced across the focal groups by design |
| Between-study variation | V = Y only for predefined cross-study cases; I = NOT-ISOLATED; E / U from the study's own estimate |
| Multiple outcomes from one contrast | E = most compatible; U paired |
| Pooled-site analyses | Code what is reported. Pooling sites does not by itself change I |
| Verbal nulls | E per the outcome object named (a result statement counts); U = VERBAL |
| Derived uncertainty | Not published; use the published form |
| Intrinsic payment-profile consequences | Rule M: not co-treatments |
| Changed reference systems | Rule R: an additional difference |
| Model-only evidence | I = MODEL-ONLY, U = MODEL-ONLY, E per the model outcome |
| **[v1.1]** Design exists, nothing reported for the focal comparison | E = NONE, U = NONE (A) |
| **[v1.1]** Employment case, only an hours (or other labour-domain) result | E = NONE; the hours result belongs to the hours case (E) |
| **[v1.1]** Conditionality exemption with fewer enforcement contacts / activation referrals, fixed exemption period | Rule M for conditionality: intrinsic, not a co-treatment (D) |
| **[v1.1]** Uncertainty exists, form not transcribed | U = NOT-INTEGRATED, usable_U NO (F) |
| **[v1.1]** Balance of another factor undocumented | Code from documented differences; `cotreatment` UNKNOWN (G) |
| **[v1.2]** Employment case, only result on "employed OR unpaid caregiver" (or another labour + non-labour composite) | E = NONE, U = NONE, usable_U NO; the composite result stays in the factual outcome table with its full inference (H) |
| **[v1.3]** Employment case, only result(s) on an employment-like label whose positive state the record documents as UNKNOWN / AMBIGUOUS / NOT-STATED | E = NONE, U = NONE, usable_U NO; the raw result stays in the factual table under `EMPLOYMENT-DEFINITION-UNRESOLVED` (I) |
| **[v1.4]** Arms differ in research procedures (compensation, comparison-group framing, invited vs never contacted, a source-declared inseparable communication effect) | Rule J: a substantive co-intervention for I; not PURE (BUNDLED unless held fixed) (§11) |
| **[v1.3]** Mixed or unresolved result accompanied by prose naming a compatible subcomponent ("notably full-time employment") | Not a separate estimand unless the inference is clearly attached to the subcomponent itself and its state is sufficient (I, §10.3) |

## 7. What you must not code

T-levels, support roles, discovery / validation roles, blockers, hypothesis status, transport-family assignment.

## 8. v1.1 clarifications (D034), in one place

| ID | Clarification | Motivating adjudication |
|---|---|---|
| A | Design availability ≠ reported estimand: no estimate / test / result statement for the focal comparison in the case's domain → E = NONE, U = NONE. A not-transcribed but source-reported estimate counts as reported | Gary and NJ-P withdrawal cases |
| B | "Any work" including own farm / business, averages of period employment indicators, one-month recall → E-A (caveat); E-A (caveat) passes the E-A-compatible stage | FNLP cadence; MFIP conditionality |
| C | An independently crossed substantive policy factor, averaged over or conditioned on → CONDITIONABLE-BUNDLE, even when balanced by design | FNLP cadence (graduation programme crossed) |
| D | Rule M for conditionality: enforcement contacts, meetings, monitoring, mandatory activation referrals and the defined period of the focal rule are intrinsic; independent services, counselling packages, changed caseworker models, cash changes are not | Utrecht exemption |
| E | Strict outcome-domain scoping of E and U; no copying of another domain's estimate into a row | SIME/DIME duration employment row |
| F | Uncertainty form not described → NOT-INTEGRATED, usable_U NO; never inferred | DIME withdrawal arms |
| G | Isolation is coded from documented differences; undocumented balance → `cotreatment` UNKNOWN, noted in the reason | SIME/DIME duration rows (flagged ambiguity) |

**What did not change:** the code vocabularies; the U precedence; usable_U = SE or CI only; the V rules; the definitions of PURE / CONDITIONABLE-BUNDLE / BUNDLED / NOT-ISOLATED; Rule R; the auxiliary fields; §7.

## 9. v1.2 rule H (D038): employment-domain positive-state rule

**Trigger:** RC-01 (D037 Batch 1, X015 Stockton). The only reported employment test used a binary whose positive category pooled full-time employment, part-time employment **and stay-at-home parent / caregiver**. v1.1 did not settle whether such a composite is an employment-domain object.

### 9.1 The rule

An outcome can be coded **E-A, E-A (caveat) or E-B** in the employment domain **only if the event / state being estimated is entirely a labour-market extensive-margin object.**

A positive category **may** include:
- paid employment;
- working;
- positive earnings;
- hours > 0;
- own-farm / own-business economic work;
- labour-force participation or another explicitly labour-market extensive margin, subject to the existing E-A / E-B distinctions.

A positive category is **not** an employment-domain outcome if a person can satisfy it **solely** through a substantively non-labour-market state, such as:
- unpaid stay-at-home caregiving;
- homemaking;
- student status;
- retirement;
- disability / inability to work;
- another explicitly non-labour state.

If employment and one or more such non-labour states are pooled into the same positive category, the composite is **not** E-A, E-A (caveat) or E-B. This holds **even if the source labels the composite "employment"**. Source labels do not override the estimand definition.

**What is read:** the exact positive and negative states of the stored outcome definition. Exclusions from the analysis **sample** (e.g. retirees removed from the population) are not part of the positive state and do not by themselves make an outcome mixed.

### 9.2 Coding an employment-domain case

- **A.** If a valid employment / labour-market estimand is reported **separately**, apply the existing compatibility hierarchy (§3) to that estimand.
- **B.** If the **only** reported causal estimate / test / result statement is on a mixed labour + non-labour composite: **E = NONE, U = NONE, usable_U = NO.** Reason: the employment-domain case has no reported compatible employment estimand.

The mixed result is **preserved factually** in the raw outcome table (definition, estimate, F / t, exact p, CI, SE, sample, provenance), under an explicit descriptive domain token such as `MIXED-LABOUR-NONLABOUR-STATUS`. Inferential information is never deleted from the factual extraction, but **its uncertainty is not transferred** into employment-domain support coding. The raw row is never called E-A / E-B.

### 9.3 NONE vs NOT-APPLICABLE

- **NONE:** the declared employment-domain case has no reported compatible outcome estimand in that domain.
- **NOT-APPLICABLE:** the case itself concerns an outcome outside the labour domain under the schema's applicable grain.

So an employment-domain support row whose only result is a mixed composite is **NONE**, not NOT-APPLICABLE. This clarification does **not** change the outcome-domain scoping of v1.1 (E).

### 9.4 Non-equivalences (what rule H does NOT change)

| Outcome | Code | Reason |
|---|---|---|
| "Any work including own farm / business" | **E-A (caveat)** (v1.1 B) | The positive state remains economic work |
| Labour-force participation, not equivalent to P(employed) | **E-B** | Employed persons and unemployed active jobseekers both belong to a labour-market extensive-margin state |
| Employment-category coefficients (full-time vs unemployed, part-time vs unemployed) | may remain **E-B** | A labour-status object, though not directly P(employed) |
| Household labour-market participation indicator; self-sufficiency earnings threshold | **E-B** (v1.1) | The positive state is labour-market activity / earnings |
| "Employed OR unpaid caregiver" (and similar composites) | **not** E-A / E-A (caveat) / E-B | The event can be true without labour-market participation |

### 9.5 Re-application and reliability

- Rule H was re-applied to all 25 reliability-frame cases, all master-map support and outcome rows, and all Batch 1 staging rows, from stored repository facts only ([v1_2_reapplication.csv](v1_2_reapplication.csv), built by `build_v1_2_reapplication.py`).
- The D033 / D034 inter-rater agreement is **not** recomputed: it remains the historical result for v1 / v1.1. No claim is made that rule H was independently second-coded.

**What did not change:** every v1.1 rule (A–G), the code vocabularies, the U precedence, usable_U = SE or CI only, the V and I rules, the auxiliary fields, §7.

## 10. v1.3 rule I (D039): outcome-definition sufficiency

**Trigger:** RC-02 (X030 Baltimore) and RC-03 (X034 CLIMB), Layer A Batch 2. Employment-like results were reported under labels ("labor force participation", "employed") whose positive states the sources do not state, next to results that are mixed or descriptive. v1.2 did not settle whether such a label-only result, or a narrative subcomponent phrase, is a "separately reported" compatible estimand (rule H §9.2A).

### 10.1 The rule

An employment-like result can enter **E-A, E-A (caveat) or E-B** only when the available factual record is **sufficient to establish** that the estimated positive state belongs entirely to the employment / labour-market extensive-margin domain, under rule H and the existing E definitions.

**Do not infer domain membership solely from labels such as:**
- employment;
- employed;
- working;
- labor force participation;
- economically active.

**When the record fails the test:** the factual extraction explicitly records the positive-state definition as **UNKNOWN**, **AMBIGUOUS** or **NOT-STATED**, or otherwise documents that the label cannot be mapped confidently to the underlying states.

**Then:** the result does **not** establish a compatible employment-domain estimand. For the **employment** support case, when no other compatible estimand is established:

    E = NONE
    U = NONE
    usable_U = NO

**The raw result is preserved:** its estimate and inferential information stay separately in the factual outcome table, under the explicit raw domain token `EMPLOYMENT-DEFINITION-UNRESOLVED`.

This is **conservative domain verification**, not an assertion that the source's outcome was actually non-labour.

**Known incompatible vs unknown:**
- `MIXED-LABOUR-NONLABOUR-STATUS` (rule H) is kept for composites whose definition is **known** to mix labour and non-labour states.
- `EMPLOYMENT-DEFINITION-UNRESOLVED` (rule I) is for labels whose definition is **unknown**.
- The two are never confused.

### 10.2 Scope limit

Rule I applies when **the factual record itself** establishes that the state definition is unknown, ambiguous or insufficient. It does **not** turn every historical compact label into missingness.
- A source that explicitly reports **"full-time employment" as a mutually exclusive labour-status category** is sufficient to establish a labour-only state, even if the questionnaire wording is not reproduced.
- A record that says only **"employed"** and **explicitly notes that the source does not state which status categories were counted** is definitionally unresolved: rule I applies.

Records that do not contain the newer exact-state fields are not thereby unresolved.

### 10.3 Narrative subcomponent mentions (clarification of the reporting rule)

A narrative mention of a compatible subcomponent does **not** become a separately reported estimand merely because the phrase appears in prose. It counts as a separately reported estimand or result statement only if the source makes clear that:
- the comparison or inference applies **specifically to that subcomponent**; **and**
- its outcome state is definitionally sufficient under rules H and I.

Example: a tested mixed composite followed by prose saying the changes were "notably full-time employment" does **not** establish a separate full-time-employment result when the report does not clearly attach the treatment-control inference to full-time employment itself. An incompatible composite is not rescued by an ambiguous narrative gloss.

### 10.4 U semantics (clarification)

- Raw inferential information is **preserved** in the factual outcome table even when support E = NONE under rule H or rule I. Examples: exact p, F or chi-square, stars, a verbal "significant", a verbal null.
- Support U is paired with the **compatible estimand that determines E**.
- When no compatible employment estimand is established, then support E = NONE, U = NONE and usable_U = NO.
- Raw inference from an incompatible or unresolved outcome object is **never** copied into support U.

### 10.5 Re-application and reliability

- Rule I was re-applied, from stored repository facts only, to:
  - the 25 reliability-frame cases;
  - every master-map support and outcome row;
  - every Layer A Batch 1 and Batch 2 staging row.
- The record is [v1_3_reapplication.csv](v1_3_reapplication.csv), built by `build_v1_3_reapplication.py`.
- No inter-rater agreement is recomputed. Rule I has not been independently second-coded.

**What did not change:** every v1.1 rule (A–G); rule H; the code vocabularies; the U precedence; usable_U = SE or CI only; the V and I rules; the auxiliary fields; §7.

## 11. v1.4 rule J (D040): research-procedure co-interventions

**Trigger:** RC-05 (X054 Groningen), Layer A Batch 6. After Rule M only the focal policy dimension differed between the compared groups, but documented research-communication and research-participation differences remained: group-specific invitation letters (the control letter framed members as the comparison group), a source statement that the letter effects cannot be separated from the interventions, questionnaire vouchers for consenting controls, and invited vs never-contacted reference comparisons. v1.3 did not settle whether such differences are substantively relevant implementation dimensions.

### 11.1 The rule

Research procedures are not policy constructs. They **count as substantive co-interventions for I** when they **differ by assigned group during the causal window** and introduce one or more of:

- material resources or incentives;
- substantive behavioural framing;
- differential information beyond what is mechanically necessary to communicate the assigned focal policy;
- differential research participation / contact exposure;
- another procedure that the source itself says cannot be separated from the intervention effect.

**Examples that CAN count as co-interventions:**
- only one arm receives research-participation compensation;
- a control arm is explicitly framed as a comparison group while another arm receives different motivational / treatment framing;
- one comparison group is invited / contacted and the other is never contacted, when research contact itself differs;
- assignment-specific communications contain substantive behavioural content beyond the minimum needed to implement the focal rule.

**Examples that do NOT automatically count:**
- the minimal communication necessary to tell a participant which focal policy rule applies to them;
- identical survey administration across arms;
- purely clerical wording differences with no substantive information, incentive or contact difference;
- outcome measurement itself, when administered equivalently.

**Source statements:** if a source explicitly states that the research-procedure effect cannot be separated from the intervention effect, treat that as strong evidence that the comparison is **not PURE**.

### 11.2 How it enters the I decision tree

In §2 step 3, research-procedure differences that satisfy §11.1 are listed among the documented differences **after** Rule M. They are "other remaining" substantive differences:
- if the design or report holds them fixed (an orthogonal or direct comparison that equalises them) → CONDITIONABLE-BUNDLE;
- otherwise → **BUNDLED**.

Rule G still applies: code from **documented** differences only. Silence about research procedures is not evidence of a difference, and hidden procedures are never inferred.

### 11.3 Scope

- Rule J affects **I and the co-treatment classification only**. It does not change V, E or U, and it creates no new Stage-3 construct or support dimension.
- It does not make research procedures part of any architecture feature (C001-C006, DS34).

### 11.4 Re-application and reliability

- Rule J was re-applied, from stored repository facts only, to the 25 reliability-frame cases, every master-map support row and every Layer A Batch 1-6 staging support row ([v1_4_reapplication.csv](v1_4_reapplication.csv), built by `build_v1_4_reapplication.py`).
- No inter-rater agreement is recomputed. Rule J has not been independently second-coded.

**What did not change:** every v1.1 rule (A-G); rules H and I; Rule M and Rule R; the code vocabularies; the U precedence; usable_U = SE or CI only; the V and E rules; the auxiliary fields; §7.

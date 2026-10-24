# D049 Canonical manuscript audit

**Date:** 2026-10-24.

**Status:** **CANONICAL MANUSCRIPT v1 — SCIENTIFICALLY AND EDITORIALLY CLOSED.** The manuscript is not submitted, not journal-formatted and not anonymised.

**Scope:** an editorial and positioning closure of `manuscript.tex`. No frozen authority, count, classification, target or H002 status changed.

## 1. Title

**Retained:** "Design variation is not design evidence: an audit of basic-income and guaranteed-income experiments". This is the author's revision of 908b786, which dropped "evidence-support" from the D047 working title.

| Alternative | Why not chosen |
|---|---|
| "Can basic-income experiments tell us how to design a basic income?" | Clear for policy readers, but a question title hides the result |
| "Many trials, little design evidence: …" | Catchy, but "little" sounds dismissive of the trial literature |
| "What basic-income experiments can and cannot tell policymakers about programme design" | Accurate but long, and does not state the central distinction |
| "Design variation is not design evidence: an evidence-support audit of …" (D047) | "Evidence-support" is project jargon |

**Why the retained title wins.** It names BI/GI explicitly. It states the central distinction (variation ≠ evidence) without claiming that design does not matter or that BI does not work. It is memorable and serious, and not methodological.

## 2. Abstract

Rewritten for policy readers. It is 256 words (by TeX-source token count).

**What it now covers, in order:**
1. the architecture decision;
2. the gap between variation and evidence;
3. the evidence universe (43 + 9);
4. the four requirements in plain words, plus the separate validation requirement;
5. the results (9 / 2 / 1; 7 / 2 / 1; cadence none with usable uncertainty);
6. the selection finding;
7. what the result does not mean (not effects of BI; not the importance of design).

The abstract contains no internal labels and no V / I / E / U notation.

## 3. Structural changes

**Introduction (rewritten, BI-first):**
1. the architecture decision faced by governments;
2. half a century of experiments that vary the architecture;
3. BI scholarship's established diagnoses: NIT packages, untestability of the full policy, non-paradigmatic trials, political scale, heterogeneity and the community-effects gap, incompatible employment definitions, and the 2022 debate on whether design questions need experiments;
4. component learning as an established objective, with the framing sentence;
5. the variation-versus-evidence distinction, explained in plain terms before any machinery;
6. the approach;
7. the result;
8. a narrow contribution.

**Section titles:** "The census geometry: where design support is lost" became "Where design support is lost in the census".

**Near-miss section:**
- A new framing sentence distinguishes five reasons an object is missing: no isolating design; not reported; not located after a bounded search; inaccessible; incompatible outcome or model-based.
- The withdrawal paragraph now says that the published labour results are pooled programme effects or model-based response functions, and that the final RIME technical report could not be accessed.

**Reporting:** a sentence states that reporting can rescue the estimand and uncertainty stages but cannot supply isolation. "Transport and compression analysis" was replaced by plain wording.

**Discussion:**
- "What is established" now includes the subset overstatement.
- "What is not established" adds that the test was not run and is not evidence for or against design-based prediction.
- "Relation to prior work" opens with the BI scholarship and states the narrower operational question. It adds the NIT response-surface point (Orr & Gubits), with the distinction between model-based and isolated estimates.
- New implication paragraphs address researchers and funders (including analytical recoverability, now folded in), governments and policy designers, and evidence synthesis and public debate.

**Limitations:** expanded from 7 to 12 items (§7).

**Conclusion:** acknowledges what BI experimentation has produced, then states the design-evidence gap and how future experiments can close it.

**New sections:** a generic Acknowledgments section (§9).

**Data availability:** cites release v1.1.0.

**Table 1 role labels:** "Census support geometry" became "Census of where design support is lost"; "support paths" became "comparisons". These are display labels only.

## 4. Citation audit (sentence level)

Every sentence about history, design, NIT, policy learning, external validity, adaptation, components, response surfaces, heterogeneity, trial politics, scale, implementation, individual-versus-community evidence, prior reviews, reporting or gaps was classified as:
- an original result (counts, geometry, selection audit);
- project interpretation (the implication paragraphs);
- an external claim.

External claims were checked against the source classifications in D030, D048C and D048D.

| Finding | Action |
|---|---|
| "Debates about basic income frequently turn on exactly these design choices" was uncited | Replaced by sourced statements (Gentilini et al. for design features; Castro & West for open cadence and amount questions) |
| "Many areas of social policy now hold numerous randomised trials" was a generic opener | Removed |
| Laín 2022a and 2022b were cited together for the normative-grounds argument | Split: the normative-grounds and implementation-details claim goes to 2022b; the political and epistemic uses go to 2022a |
| Corinth & Mayhew were cited for design variation | Narrowed to incompatible employment definitions, which is what D030 verified |
| The Widerquist critique was absent although read in D030 | Added for "cannot test a permanent universal policy" and "struggle to separate the effects of size from type" (ch. 4 summary) |
| The De Wispelaere, Doussard & Chrisp 2025 politics-of-scale agenda was absent | Added for "design and implementation of trials vary with political scale" |
| The NIT response-surface objective | Attributed to Orr & Gubits (full text, D048D) |
| "Five sources could not be read" (stale count) | Now "several sources" |
| Chrisp et al. 2022 printed "to be completed" | Completed from the report's title page |

**New references:** 3. Metadata from Crossref. Each claim was verified against a full text already held for the D030 audit; see `D049_REFERENCE_ADDITIONS.csv` and `BIBLIOGRAPHY_VERIFICATION.md`.
- `gentilini2020`: DOI 10.1596/978-1-4648-1458-7.
- `widerquist2018`: DOI 10.1007/978-3-030-03849-6.
- `dewispelaere2025`: DOI 10.1111/psj.70006.

**Bibliography integrity:**
- 39 entries; no duplicate keys or DOIs; no missing citations.
- One uncited entry, `papineni2025`. It has never been cited since D047, and plainnat does not print it.
- bibtex: 0 warnings.

## 5. BI-literature integration

The Introduction and Discussion now credit BI scholarship with:
- trial heterogeneity;
- non-paradigmatic designs and their constraints;
- the political scale and political functions of trials;
- the impossibility of testing the full policy;
- external validity;
- the individual-versus-community gap;
- the NIT package diagnosis;
- the debate on policy details.

The paper is positioned as asking the narrower operational question, without claiming that the field missed design.

## 6. De Wispelaere, Doussard & Chrisp

| Work | Before D049 | After D049 |
|---|---|---|
| `doussard2026` | Introduction (heterogeneity and community gap); Discussion (community gap distinct from design evidence) | Introduction (amount, frequency, duration tabulated; patchwork; community gap); Discussion (prior scholarship; distinct community and general-equilibrium gap) |
| `dewispelaere2025` | Not cited | Introduction and Discussion (political scale) |
| Chrisp & De Wispelaere 2022 (policy-impact special issue) | Not cited | Still not cited: R1-abs only, and no current sentence needs it |
| `chrisp2022` (rapid review) | Cited | Retained, with author names completed |

Nothing in the manuscript implies that these authors ignore architecture, design heterogeneity or policy design. Citation follows substantive relevance only; the private sharing of the book manuscript plays no role.

## 7. Limitations (12 items)

1. **Frame:** a frame-defined census.
2. **Audit layer:** not a census and not exhaustive.
3. **Outcome domain:** employment only.
4. **Target:** project-specific.
5. **Uncertainty rule:** conservative.
6. **Unlocated or inaccessible evidence.**
7. **Model-based historical analyses:** potentially informative.
8. **Coding reliability:** the second pass covered 25 pre-census cases; AI versus AI under a written codebook; estimand agreement weaker; three later rules not second-coded; the census not fully double-coded.
9. **Two-family requirement:** belongs to this test, not a transportability theorem.
10. **Prior-art search:** bounded.
11. **Generalisation:** remains a hypothesis.
12. **No effects tested.**

## 8. Hostile-review findings

**Lenses:** a skeptical BI scholar; a methods reviewer; a policy editor; a BI-sympathetic reader alert to overclaiming.

| Lens | Finding | Resolution |
|---|---|---|
| BI scholar | The earlier Introduction opened generically and credited prior BI work only after the result | Rewritten BI-first, crediting prior work before the contribution |
| BI scholar | Novelty by omission: Widerquist and De Wispelaere et al. were uncited | Added (§4) |
| Methods | Risk that validation reads as a fifth stage | Retained "a requirement of the test, not a fifth stage"; the limitation on the two-family rule was added |
| Methods | "Independent experiments" in the abstract versus "families" in the Results | Layer A experiments are transport families one-to-one (N-01), so the abstract wording is exact. Families are defined in Methods |
| Methods | Model-based response functions versus "no estimates" | The RIME wording stays bounded ("not located … accessible record"; "we do not conclude … never estimated"). The response-function attribution and the model-only coding are stated |
| Policy editor | Jargon: "structured negative feasibility result", "census geometry", "support paths", "transport and compression analysis" | Replaced |
| Policy editor | Missing "so what" for practitioners | Implication paragraphs added |
| Sympathetic reader | Any "BI does not work" or "design does not matter" reading | The abstract, Introduction, Discussion and Conclusion each state the negative scope explicitly. The Conclusion opens by acknowledging what BI experimentation has produced |
| All | "Registered", "52-study census", H002 tested, 13 / 12 / 11 / 10 / 2 drift | None found. Enforced by validator checks 14, 20, 43, 45 and 47 |

## 9. Acknowledgments

The canonical manuscript uses a generic acknowledgment. Candidates and consent status are recorded privately in `ACKNOWLEDGMENTS_PLAN.md`, which is not in the public release. No named acknowledgment was made without consent.

## 10. Final measures

| Measure | Value |
|---|---|
| Pages | 19 |
| Main text, Introduction to Conclusion, including captions (TeX-source token count) | about 5,400 words |
| Main text, excluding captions | about 5,050 words |
| Methods | about 1,150 words |
| Abstract | 256 words |

**Build:**
- 0 undefined citations or references;
- 0 missing files;
- 0 overfull boxes;
- 0 bibtex warnings;
- deterministic.

**Numeric audit:** 202 numbers in the manuscript and 652 in the supplement, none untraced.

## 11. Remaining issues (none blocking the canonical freeze)

- The abstract (256 words) and main text are longer than some venues allow. That is handled in journal derivatives.
- Named acknowledgments wait on consent from the author's contacts.
- Residual unread prior art: the Merrill, Neves & Laín 2022 book; Neves 2021; Cartwright & Hardie.
- `papineni2025` remains in the `.bib` file uncited (not printed).

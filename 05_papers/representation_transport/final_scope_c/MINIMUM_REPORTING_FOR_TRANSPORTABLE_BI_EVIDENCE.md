# Minimum reporting for the current transport / compression programme

**Scope.** This is the minimum reporting that **this project's current transport / compression programme** (frozen SCOPE-C, employment domain) needs. It is **not** a universal causal-inference reporting standard.

**Basis.** Every item maps to a blocker observed in the final SCOPE-C support tables. The column `blocker_code` names the strict-gate stage, or the measurement field, where evidence was lost.

| # | Requirement | blocker_code | Observed blocker (frozen evidence) |
|---|---|---|---|
| 1 | Exact architecture of each intervention arm: transfer rule, withdrawal schedule, conditionality, payment cadence, promised horizon | V | Cells with V UNKNOWN / NOT-ESTABLISHED: Almere (all architecture dimensions), B-MINCOME and Ontario conditionality, Utrecht withdrawal isolation |
| 2 | Exact assignment counts and analysis populations | I | RIME plan probabilities NR; post-randomisation-selected analysis subsamples (RIME, Gary) |
| 3 | Direct, pre-specified arm-arm contrasts for each architecture factor | E | NJ-P, Gary and RIME same-G designs (PURE, E = NONE); Newark cadence (PURE, E = NONE); DIME higher vs lower groups not reported directly |
| 4 | Exact employment positive / negative states | E | Rules H / I: E-B threshold objects (Participatiewet municipalities); mixed or unresolved states in Layer A |
| 5 | ITT-compatible estimates where applicable | E | RIME analyses only post-randomisation-selected subsamples; response-surface (MODEL-ONLY) results substitute for design contrasts |
| 6 | SE or CI for every focal architecture contrast | U | WRP conditionality (stars only); Compton cadence (exact p only); FNLP cadence (verbal only); RIME (no SE / CI anywhere) |
| 7 | Covariance or factorial-estimator information when contrasts share a control | U | Multi-arm designs (RIME, NJ-P, Participatiewet) report arm-vs-control results only; combining them is not allowed |
| 8 | Baseline mean household income and the ex-ante transfer schedule (for B2) | B2 | QS-101 NR or not established for RIME, Ontario, Finland and GWW (D041 cells); B-MINCOME B2 measurement class M3 (nonconforming) |
| 9 | Baseline employment definition and share for the assigned population | BASELINE | QS-105 NR in most families; RIME reports only subsample values |
| 10 | Implementation differences and services by arm | I | Bundled arms: MFIP (mandate + services), Participatiewet combination arms, DIME (G and duration pooled) |
| 11 | Machine-readable tables / data, or a reproducibility route | U / E | Restricted or embargoed data (WRP, FNLP COM-005); RIME and NJ-P access not established |

Satisfying these items does not guarantee support. It removes the reporting blockers observed here. Isolation is a design property and cannot be fixed by reporting.

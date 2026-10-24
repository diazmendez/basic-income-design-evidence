# Supplement visual audit (supplement.pdf, D048A)

**Method.** All 18 pages were rendered with pdftoppm at 70 dpi and inspected as contact sheets. Landscape pages (S2 grid, S4 path and Layer B tables) were checked in their rotated orientation.

**Build diagnostics.** These are recorded in `SUPPLEMENT_BUILD_RECORD.csv`:
- 0 undefined references; 0 missing files; 0 LaTeX errors; 0 overfull boxes; 0 rerun warnings.
- The supplement is compiled twice per build, and the rebuild is byte-identical.
- The numeric audit (`SUPPLEMENT_NUMERIC_AUDIT.csv`) traces 647 numbers, with 0 untraced.

| Check | Finding | Action taken during the build |
|---|---|---|
| Overflow / clipping | The first build had 148 overfull boxes (long code words and paths in narrow columns) | Breakpoints at hyphens, underscores, slashes and semicolons; ragged columns sized net of padding; codes abbreviated with an S2 legend in the path tables; S2 grid set in landscape; Table S3 scaled to text width. Final: 0 overfull |
| Cross-references | All table, section and figure references resolve; the contents list shows S1–S10 | TOC number width widened for "S10" |
| Frame composition | S1 text and Table S1: 43 members; 39 verified, 2 pending, 2 frame conflict; frame-defined, not every experiment | None |
| Denominators and counts | The S2 summary rows reproduce the V = Y counts 26 / 9 / 7 / 2 / 33 / 6, the strict counts 6 / 1 / 1 / 0 / 6 / 2 and the unknown counts 17 / 37. The builder stops on any mismatch with the frozen claims | None |
| Layer B wording | "a separate audit of 9 … not a census"; union counts labelled "not a census prevalence" | None |
| Near-miss cells | Table S3 matches the frozen path tables (B-MINCOME and Utrecht pass; RIME, NJ-P and Gary stop at the estimand; WRP stars; Compton exact p; FNLP verbal; Newark no result). The duration table caption was corrected so that it does not deny RIME's between-study E-A (caveat) estimate | Caption corrected |
| RIME | Bounded sentence present; "we do not conclude that the contrast was never estimated" | None |
| T labels | T3, T1, T2, T1, T2, T2; supplementary only | None |
| Figure S1 | Matches the frozen status-changing objects (fig5 data); no effect sizes, signs or significance | None |
| Language | No "registered" / "preregistered" wording (a display substitution covers the frozen CSV phrase); no 52-study census; no statement that H002 was tested or rejected. The rule quotes render in bold correctly | The bold-markup conversion was fixed |

## D048C re-audit

**Page count:** 18, unchanged.

**Pages re-inspected:**
- p. 6 (S3): the new counting-unit paragraph (13 rows / 12 designs / 11 isolated entries / 10 families / 2 bundled comparators) and the new Table S3 caption.
- All pages, via the build log.

**Diagnostics:**
- 0 overfull boxes;
- 0 errors;
- the numeric audit traces 652 numbers, 0 untraced (new claim S-04).

## D048D re-audit

- **p. 16 (S8, Table S15):** the WRP row's record column now cites `manuscript/supplement/S8_ACCESS_STATEMENT.md`. The table is legible, with no overflow.
- **Page count:** 18, unchanged.
- **Build:** 0 overfull boxes; 0 errors; the rebuild is deterministic.
- **Numeric audit:** 652 numbers, 0 untraced. The S-03 authority moved to the public statement.

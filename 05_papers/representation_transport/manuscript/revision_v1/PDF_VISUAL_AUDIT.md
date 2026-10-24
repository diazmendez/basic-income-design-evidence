# PDF visual audit (manuscript.pdf, v1)

**Method.** Every page of `manuscript.pdf` was rendered with pdftoppm and inspected as contact sheets at 50 dpi; pages 6 and 10 were also inspected at 80 dpi. The page count and hash are in `BUILD_RECORD.csv`.

## Checks

| Check | Finding | Action |
|---|---|---|
| Figure readability | Figures 1–4 are vector PDFs at full text width (Figure 4 at 0.86 width). Labels are legible at print size; the design is greyscale | None |
| Table width | Table 2 initially overflowed by 52 pt | Fixed: the tabular is scaled to text width in the generator. The build now has 0 overfull boxes |
| Caption placement | Figure captions below and table captions above, per the article-class defaults | None |
| Page breaks | Floats placed `[t]`. Figure 2 and Table 2 share page 6. No float strands a section heading | None |
| Widows / orphans | None conspicuous | None |
| White space | Moderate around floats on pages 4–8; acceptable for a review PDF | None (layout is venue-dependent; deferred) |
| Overfull boxes | 0 (log) | None |
| Reference formatting | plainnat author–year. **Five methodological anchors show no title and carry an explicit "Title … to be verified from the DOI" note**, by design (metadata not recorded in the repository) | Blocking bibliography item; resolve by DOI verification |
| Heading hierarchy | Numbered sections 1–11; unnumbered Methods and end matter; paragraph run-in heads | None |
| Reporting box | Framed box, legible, six numbered items | None |
| Front matter | Title carries the "Working title; not final" footnote; the author block shows [AUTHOR NAME AND AFFILIATION: AUTHOR FACT REQUIRED] | Blocking author fact |
| Front matter and end matter (D048B re-check, 17 pages) | Pages 1 and 14 were re-rendered at 60 dpi. The author block shows the name placeholder, then the affiliation on three lines. The AI-use statement (p. 14) and the Funding, Competing interests, Author note and Data and code availability sections are legible, with no overflow; the repository URL breaks across a line | Name and repository release remain author facts |

No scientific content was changed for aesthetic reasons.

## D048A re-audit (manuscript.pdf, 17 pages)

**Method.** All 17 pages were rendered with pdftoppm at 70 dpi and inspected as contact sheets. Page count and hash are in `BUILD_RECORD.csv`. Build diagnostics: 0 undefined citations or references, 0 missing files, 0 LaTeX errors, 0 overfull boxes, 0 rerun warnings, 0 bibtex warnings (5 in D047). Two consecutive builds produce the same PDF hash.

| Check | Finding | Action |
|---|---|---|
| Front matter (author edits, 908b786) | Name, affiliation line, email and disclaimer footnotes are legible. **The date printed "October 23, 2025"**: `\date` is commented out, so `\today` took the build's fixed `SOURCE_DATE_EPOCH` (1761177600, a 2025 timestamp) | Mechanical build fix: the epoch was set to 2026-10-24 in `build_manuscript.py` and `build_supplement.py`. The page now reads "October 24, 2026". The text is unchanged |
| Figure 1 (redrawn) | Four bracketed stages and a dashed, separate validation box; labels legible at print size (p. 4) | None |
| Figures 2–4, Tables 1–2, Box 1 | Unchanged rendering; no clipping (pp. 5–10) | None |
| Page breaks after the D048B / 908b786 end matter | The GenAI disclosure starts at the foot of p. 14 and continues cleanly; Funding, Competing interests and Data and code availability are on p. 15 | None |
| Bibliography (pp. 15–17) | The five anchors render with full authors, titles, volume(issue): pages and DOI; no "to be verified" note | None |

## D048C re-audit (manuscript.pdf, 18 pages)

The PDF went from 17 to 18 pages because of the positioning sentences and the nine added references.

**Method:**
- all 18 pages rendered at 60 dpi;
- page 9 (Figure 4) also rendered at 110 dpi.

**Build diagnostics:**
- 0 undefined citations or references;
- 0 missing files;
- 0 LaTeX errors;
- 0 overfull boxes;
- 0 bibtex warnings;
- two consecutive builds give the same hash.

**Checks:**
- **Figure 4.** The re-rendered in-figure note reads "Rows: family-dimension entries…" and is legible. The caption states the unit and names Wageningen as the doubly listed family.
- **New references.** Laín 2022a / 2022b are disambiguated by plainnat. Doussard et al. 2026 has its chapter note.
- **Front and end matter.** No page breaks inside the end-matter sections. Front matter unchanged apart from the typo fixes in the GenAI section.

## D048D re-audit (manuscript.pdf, 18 pages)

The only change is the new NIT sentence in §6 (p. 8), which reflows into the RIME paragraph after Figure 3. No page-count change.

**Build:**
- 0 undefined citations or references;
- 0 missing files;
- 0 errors;
- 0 overfull boxes;
- 0 bibtex warnings;
- two builds give the same hash.

## D049 re-audit (manuscript.pdf, 19 pages)

**Method:** all 19 pages rendered at 55 dpi and inspected as contact sheets.

**Findings:**
- The rewritten Introduction (pp. 1–3) and Discussion (pp. 11–13) flow without stranded headings.
- Box 1 and Figures 1–4 are unchanged and legible.
- The Table 1 role labels have been reworded.
- The bibliography (pp. 17–19) shows the three new references and the completed Chrisp et al. entry. No "to be completed" or "to be verified" note remains.

**Build:**
- 0 undefined citations or references;
- 0 overfull boxes;
- 0 bibtex warnings;
- deterministic.

# Environment

The release 1.2.0 outputs were produced and checked with:

| Component | Version |
|---|---|
| Python | 3.12.3 (standard library only, plus matplotlib for the figures) |
| matplotlib | 3.6.3 (with numpy 1.26.4) |
| TeX | pdfTeX 3.141592653-2.6-1.40.25 (TeX Live 2023) |
| latexmk | 4.83 |
| BibTeX | 0.99d |
| poppler (`pdfinfo`) | 24.02.0 (used to count pages in the build records) |

**Fixed build date:** the PDFs are compiled with `SOURCE_DATE_EPOCH=1792800000` (2026-10-24 UTC) and `FORCE_SOURCE_DATE=1`.

**Determinism:** rebuilding with the same versions gives byte-identical PDFs, tables and figures. A different TeX or matplotlib version may change PDF or figure bytes. It does not change the tables, counts or audits, which are checked separately by `validate_release.py`.

All Python commands are run with `python3 -I` (isolated mode).

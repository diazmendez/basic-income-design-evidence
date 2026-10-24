# Bibliography verification: five methodological anchors (D048A)

**Access date:** 2026-10-24.

**Scope:** metadata closure only, for entries already cited since D047. This was not a new prior-art search, and no reference was added or removed.

**Method.** Each DOI was resolved against the Crossref REST API (`api.crossref.org/works/{DOI}`). That is the metadata the publisher deposited with the DOI registration agency.

The three biomedical-journal articles were also checked independently in Europe PMC (REST search by DOI), which is the PubMed-indexed record.

For the two statistics articles, which are not indexed in Europe PMC, the publisher landing pages were tried:
- **Project Euclid** (Pearl & Bareinboim): the DOI resolved to a URL whose path repeats the journal, volume, issue and title. The page itself carried no machine-readable citation metadata.
- **Annual Reviews** (Degtiar & Rose): the server returned HTTP 403. Access controls were respected and not circumvented.

For both, Crossref's publisher-deposited record is the source of record.

**bibtex.** Titles are entered in the title case of the rest of `references.bib`. The plainnat style sets article titles in sentence case when typesetting. The exact capitalisation each source returned is recorded in the "Sources" column below. After the update, bibtex reports 0 warnings (5 in D047).

| Key | DOI | Authors (order verified) | Title | Journal, volume(issue), pages, year | Sources | Discrepancy from the expected metadata in the D048A brief |
|---|---|---|---|---|---|---|
| pearl2014 | 10.1214/14-STS486 | Judea Pearl; Elias Bareinboim | External Validity: From Do-Calculus to Transportability Across Populations | Statistical Science 29(4): 579–595, 2014 (issued 2014-11-01) | Crossref (publisher: Institute of Mathematical Statistics); Project Euclid DOI landing URL (journal, volume 29, issue 4, title) | None |
| degtiar2023 | 10.1146/annurev-statistics-042522-103837 | Irina Degtiar; Sherri Rose | A Review of Generalizability and Transportability | Annual Review of Statistics and Its Application 10(1): 501–524, 2023 (issued 2023-03-10) | Crossref (publisher: Annual Reviews). Landing page HTTP 403, not circumvented | None. Crossref also records issue 1 |
| hernan2011 | 10.1097/EDE.0b013e3182109296 | Miguel A. Hernán; Tyler J. VanderWeele | Compound Treatments and Transportability of Causal Inference | Epidemiology 22(3): 368–377, 2011 (May) | Crossref (publisher: Ovid Technologies / Wolters Kluwer Health); Europe PMC (PMID 21399502) | Capitalisation only: Crossref gives title case; Europe PMC gives sentence case, as in the brief |
| thompson2002 | 10.1002/sim.1187 | Simon G. Thompson; Julian P. T. Higgins | How should meta-regression analyses be undertaken and interpreted? | Statistics in Medicine 21(11): 1559–1573, 2002 (online 2002-05-21; print issue 2002-06-15) | Crossref (publisher: Wiley); Europe PMC (PMID 12111920) | None. Crossref and Europe PMC both add issue 11, which the brief did not give |
| riley2020 | 10.1002/sim.8516 | Richard D. Riley; Thomas P. A. Debray; David Fisher; Miriam Hattle; Nadine Marlin; Jeroen Hoogland; Francois Gueyffier; Jan A. Staessen; Jiguang Wang; Karel G. M. Moons; Johannes B. Reitsma; Joie Ensor | Individual participant data meta-analysis to examine interactions between treatment effect and participant-level covariates: Statistical recommendations for conduct and planning | Statistics in Medicine 39(15): 2115–2137, 2020 (online 2020-04-30; print issue 2020-07-10) | Crossref (publisher: Wiley); Europe PMC (PMID 32350891) | None. The 12 authors and their order match the brief. Volume 39, issue 15 and pages 2115–2137 were verified; the brief gave no pages |

## Changes to `references.bib`

For each of the five entries:
- the author field now carries the full author list with given names;
- the verified title has been added;
- the issue number has been added where it was missing (degtiar2023, thompson2002, riley2020);
- the note "Title … to be verified from the DOI before submission" has been removed.

The DOIs, volumes, pages and years recorded since D024 were all confirmed unchanged. Citation meaning is unchanged: the same keys are cited at the same places.

## D049 additions and completions (2026-10-24)

**Completed:** `chrisp2022`. The given names, institution and date were taken from the report's own title and imprint pages: the local D030 copy of the EPPI / IPPO report, March 2022, ISBN 978-1-911605-27-0. The "to be completed" note has been removed.

**Added references.** Metadata comes from Crossref. Each supported claim was checked against a full text already held for the D030 audit (`revision_v1/D049_REFERENCE_ADDITIONS.csv`).

| Key | Metadata | Notes |
|---|---|---|
| `gentilini2020` | World Bank, DOI 10.1596/978-1-4648-1458-7; Crossref issued 2019-11-25, print 2020 | — |
| `widerquist2018` | Springer / Palgrave, DOI 10.1007/978-3-030-03849-6 | — |
| `dewispelaere2025` | *Policy Studies Journal* 54(3):e70006, DOI 10.1111/psj.70006; online 2025-02-28, print 2026-08 | The article number is taken from the PDF footer; Crossref gives no pages. The bibliography uses the print year, 2026; the key keeps the online year |

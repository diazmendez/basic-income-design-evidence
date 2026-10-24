#!/usr/bin/env python3
"""D047: validate manuscript v1 (LaTeX source of truth, compiled PDF, references, traceability, readiness status).
Exits 1 on failure. Checks 1-39 follow D047 section 33; checks 23, 34 and 35 were revised by D048B after the author supplied the disclosure facts,
and aligned by D048A with the author's own edits in commit 908b786 (author block, footnoted disclaimer, "GenAI use disclosure" section).
D048A adds checks 40-44 (verified bibliography, V-I-E-U / validation terminology, compiled supplement, supplement wording, no new references)
and accepts only the figure files listed, with their hashes, in revision_v1/D048A_AUTHORISED_REVISIONS.csv as changes to the frozen inputs.
D048C revises check 44 (only the audited reference additions in revision_v1/D048C_REFERENCE_ADDITIONS.csv) and adds checks 45-48
(counting-unit / ontology wording; disclosure typos; prior-art positioning; public replication package).
D049 extends check 44 to the audited D049 additions and adds check 49 (canonical closure).
D050 adds check 50 (independent-critique revision: disclosure chronology, abstract sensitivity, two-panel Figure 1).
Usage: python3 -I validate_manuscript_v1.py [--tex PATH] [--bib PATH] [--readiness PATH]
"""
import csv
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RT = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(RT, "..", ".."))
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
TEX = arg("--tex", os.path.join(HERE, "manuscript.tex"))
BIB = arg("--bib", os.path.join(HERE, "references.bib"))
READY = arg("--readiness", os.path.join(HERE, "revision_v1", "SUBMISSION_READINESS.md"))
DEFAULT = TEX == os.path.join(HERE, "manuscript.tex") and BIB == os.path.join(HERE, "references.bib")
REV = "67157b2"
sys.path.insert(0, os.path.join(HERE, "scripts"))
import build_tex_audit as TA  # noqa: E402

err = []
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, "rb").read() if os.path.exists(p) else b""
rd = lambda p: list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []
git = lambda rev, p: subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{p}"], capture_output=True).stdout
gitls = lambda rev, p: subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", rev, p], capture_output=True, text=True).stdout.split()
tex = rb(TEX).decode()
bib = rb(BIB).decode()
body = tex.split(r"\begin{document}", 1)[1] if r"\begin{document}" in tex else ""
VIS = re.sub(r"(?<!\\)%.*$", "", body, flags=re.M)
FLAT = re.sub(r"\s+", " ", VIS)
SENT = re.split(r"(?<=[.!?])\s+", FLAT)
NEG = re.compile(r"\b(not|no|never|nor|neither|without|cannot)\b", re.I)
REC = (rd(os.path.join(HERE, "revision_v1", "BUILD_RECORD.csv")) or [{}])[0]
MSREL = "05_papers/representation_transport/manuscript"


def section(title):
    m = re.search(r"\\section\*?\{[^}]*" + re.escape(title) + r"[^}]*\}(.*?)(?=\\section|\\bibliographystyle|\Z)", VIS, re.S)
    return re.sub(r"\s+", " ", m.group(1)) if m else ""


def bibentry(key):
    m = re.search(r"@\w+\{" + re.escape(key) + r",(.*?)\n\}", bib, re.S)
    return m.group(1) if m else ""


cites = set(k.strip() for grp in re.findall(r"\\cite[pt]?(?:\[[^\]]*\])*\{([^}]*)\}", VIS) for k in grp.split(","))
bibkeys = set(re.findall(r"@\w+\{([^,]+),", bib))

# 1 / 2 / 3
if rb(os.path.join(ROOT, MSREL, "manuscript_v0.md")) != git(REV, f"{MSREL}/manuscript_v0.md"):
    err.append("[1] manuscript_v0.md changed")
fz = rd(os.path.join(HERE, "revision_v1", "D046_V1_INPUT_FREEZE.csv"))
if len(fz) < 40:
    err.append("[2] D046_V1_INPUT_FREEZE.csv incomplete")
AUTHREV = {r["file"]: r["sha256"] for r in rd(os.path.join(HERE, "revision_v1", "D048A_AUTHORISED_REVISIONS.csv"))}
revised = lambda p: p in AUTHREV and sha(rb(os.path.join(ROOT, p))) == AUTHREV[p]
for r in fz:
    if revised(r["file"]) and sha(git(REV, r["file"])) == r["sha256"]:
        continue
    if sha(git(REV, r["file"])) != r["sha256"] or sha(rb(os.path.join(ROOT, r["file"]))) != r["sha256"]:
        err.append(f"[2] frozen input changed: {r['file']}")
for sub in ("05_papers/representation_transport/final_scope_c", "05_papers/representation_transport/paper", "05_papers/representation_transport/evidence_universe",
            f"{MSREL}/review", f"{MSREL}/figures"):
    for p in gitls(REV, sub):
        if "__pycache__" not in p and rb(os.path.join(ROOT, p)) != git(REV, p) and not revised(p):
            err.append(f"[{3 if 'final_scope_c' in p or 'evidence_universe' in p or 'paper/' in p else 2}] authority changed since {REV}: {p}")
# 4 / 5 / 6 / 7 / 8 / 37
if not tex:
    err.append("[4] manuscript.tex missing")
pdf = os.path.join(HERE, "manuscript.pdf")
if not os.path.exists(pdf) or not REC or int(REC.get("pdf_pages", 0)) < 1:
    err.append("[5] manuscript.pdf not compiled / no build record")
if not bib:
    err.append("[6] references.bib missing")
if REC.get("undefined_citations") != "0" or (cites - bibkeys):
    err.append(f"[7] undefined citations: {sorted(cites - bibkeys)} / build record {REC.get('undefined_citations')}")
if REC.get("undefined_references") != "0" or REC.get("missing_files") != "0":
    err.append("[8] undefined references or missing files in the build")
if DEFAULT and (REC.get("manuscript_pdf_sha256") != sha(rb(pdf)) or REC.get("manuscript_tex_sha256") != sha(rb(TEX)) or REC.get("references_bib_sha256") != sha(rb(BIB))):
    err.append("[37] build record hashes do not match manuscript.tex / references.bib / manuscript.pdf (rebuild required)")
# 9 / 10 / 11 / 12 / 13
for f in ("fig1_support_chain", "fig2_census_attrition", "fig3_selection_audit", "fig4_near_miss_matrix"):
    if f"\\includegraphics[width=" not in VIS or f"{{{f}.pdf}}" not in VIS:
        err.append(f"[9] main figure not included: {f}")
inputs = re.findall(r"\\input\{([^}]*)\}", VIS)
if sorted(inputs) != ["generated/table1.tex", "generated/table2.tex"] or "\\begin{table}" in VIS:
    err.append(f"[10] main tables are not exactly Tables 1-2: {inputs}")
t2 = rb(os.path.join(HERE, "generated", "table2.tex")).decode()
if re.search(r"\bT[0-3]\b", FLAT) or re.search(r"\bT[0-3]\b", t2) or "transport-support label" in FLAT.lower():
    err.append("[11] T labels in the main narrative / Table 2")
if "fig5" in VIS:
    err.append("[12] Figure 5 in the main text")
if "table_s3" in VIS or re.search(r"Table~?\s?3\b", FLAT):
    err.append("[13] Table 3 in the main text")
# 14 / 15 / 16
for s in SENT:
    if re.search(r"pre-?regist|\bregistered\b|registration", s, re.I) and not re.search(r"no external public preregistration", s):
        err.append(f"[14] registration language: {s[:80]}")
    if re.search(r"(universal\w*|always|in general|any|all)[^.]{0,40}transport\w*[^.]{0,40}(requires?|needs?) (at least )?two independent", s, re.I) or \
            re.search(r"transportable claim needs at least two", s, re.I):
        err.append(f"[15] universal two-source transport claim: {s[:80]}")
if "For the prospective empirical test considered here, we require one independent family for identification or discovery and another for validation" not in FLAT:
    err.append("[15] prospective discovery-and-validation sentence missing")
for k in ("pearl2014", "degtiar2023", "hernan2011", "thompson2002", "riley2020"):
    if k not in cites:
        err.append(f"[16] methodological anchor not cited: {k}")
# 17 / 18 / 19 / 20
claims = {r["claim_id"]: r["value"] for r in rd(os.path.join(RT, "paper", "PAPER_NUMERIC_CLAIMS.csv"))}
if claims.get("N-01") != "43" or "frozen, frame-defined universe of 43" not in FLAT:
    err.append("[17] Layer A denominator / frame wording")
man = rd(os.path.join(RT, "evidence_universe/layer_a_reconciliation/RECONCILED_LAYER_A_MANIFEST.csv"))
comp = {s: sum(1 for m in man if m["verification_status"] == s) for s in ("VERIFIED", "PENDING", "FRAME-CONFLICT")}
v1 = {r["claim_id"]: r["value"] for r in rd(os.path.join(HERE, "revision_v1", "V1_NUMERIC_CLAIMS.csv"))}
if v1.get("F-01") != f"{comp['VERIFIED']}; {comp['PENDING']}; {comp['FRAME-CONFLICT']}" or \
        f"Of the 43 frame members, {comp['VERIFIED']} were verified against primary sources, {comp['PENDING']} remained pending and {comp['FRAME-CONFLICT']} had unresolved frame conflicts" not in FLAT:
    err.append("[18] frame composition does not reproduce the authority")
strict_exp = set()
for d in ("WITHDRAWAL", "CONDITIONALITY", "CADENCE"):
    strict_exp |= {r["experiment_id"] for r in rd(os.path.join(RT, f"final_scope_c/{d}_SUPPORT_PATHS_FINAL.csv")) if r["failure_reason"] == "STRICT PASS"}
if strict_exp & {m["layer_a_id"] for m in man if m["verification_status"] != "VERIFIED"}:
    err.append("[18] a non-verified frame member belongs to a strictly supported family (claim in Section 3 false)")
for s in SENT:
    if re.search(r"Layer B", s) and re.search(r"\bcensus\b|prevalence", s) and not NEG.search(s):
        err.append(f"[19] Layer B as census / prevalence: {s[:80]}")
    if re.search(r"\b52\b", s) and not NEG.search(s):
        err.append(f"[20] 52-study statement: {s[:80]}")
    if re.search(r"(every|all)[^.]{0,25}(basic-income|guaranteed-income|BI)[^.]{0,30}experiments?[^.]{0,15}(ever|conducted|run)\b", s, re.I) and not NEG.search(s):
        err.append(f"[19] frame overstated as all experiments: {s[:80]}")
if "Layer B is not a census" not in FLAT:
    err.append("[19] Layer B audit wording missing")
# 21 / 22 / 23 / 24 / 25
inf = section("currently infeasible")
if "two supporting families" not in inf or "Wageningen" not in inf or "Broader (E-B)" not in t2:
    err.append("[21] E-B sensitivity not visible")
if "No compatible published direct contrast was located in the accessible RIME-family record after the bounded search" not in FLAT:
    err.append("[22] RIME bounded wording missing")
for s in SENT:
    if re.search(r"does not exist|was never published|never published anywhere", s) or (re.search(r"never estimated", s) and "do not conclude" not in s):
        err.append(f"[22] absence asserted beyond the bounded search: {s[:80]}")
    if re.search(r"Vermont|WRP", s) and re.search(r"restricted|secure|access (route|mechanism)|archive|available to (the|this) (author|project)", s, re.I):
        err.append(f"[23] WRP-specific access route in the main text: {s[:80]}")
    m24 = re.search(r"\b(basic income|guaranteed income|BI) (works|is effective|does not work|reduces employment|increases employment|should be adopted)\b", s, re.I)
    if m24 and not NEG.search(s.replace(m24.group(0), "")):
        err.append(f"[24] effect / desirability claim: {s[:80]}")
# D048B: the affiliation and the independence disclaimer are author-authorised; the employer may appear only there
AUTH = re.search(r"\\author\{.*?\}\s*\n", tex, re.S)  # title block precedes \begin{document}
NOTE = section("Author note")
DISC = re.sub(r"\s+", " ", (AUTH.group(0) if AUTH else "") + " " + NOTE)
EMP = FLAT.replace(NOTE.strip(), " ") if NOTE.strip() else FLAT
if re.search(r"ICPSR|USD ?[0-9]|Ericsson", EMP):
    err.append("[23] access metadata or employer in the main text")
if not re.search(r"Ericsson AB did not sponsor, fund, commission, supervise or participate in the research", DISC) or "personal capacity" not in DISC \
        or not (AUTH and "Ericsson AB" in AUTH.group(0)) or re.search(r"Ericsson[^.]{0,80}\b(funded|sponsored|supported|commissioned|approved)\b", DISC):
    err.append("[23] affiliation or independence disclaimer missing / altered")
if re.search(r"\b(NHB|Nature Human Behaviour|JPAM|Journal of Economic Surveys|Research Synthesis Methods|Basic Income Studies|PNAS|target journal)\b", tex):
    err.append("[25] journal named / selected")
# 26-32 references
NAMED = {"Burtless": "burtless1986", "Elmore": "elmore1986", "Chrisp": "chrisp2022", "Corinth": "corinth2026", "Crosta": "crosta2024", "Bastagli": "bastagli2016",
         "RIME": "irp1976rime", "New Jersey-Pennsylvania": "watts1974", "Gary": "kehrer1979", "Seattle-Denver": "riddell2024", "Mincome": "hum1993", "Kenya": "banerjee2023",
         "Vermont": "scrivener2002", "Minnesota": "miller2000", "Utrecht": "verlaat2026", "B-MINCOME": "verlaat2025", "Wageningen": "muffels2020", "Compton": "balakrishnan2024",
         "Nigeria": "bastian2017", "Newark": "tandon2025"}
for name, key in NAMED.items():
    if name in FLAT and key not in cites:
        err.append(f"[26] named study uncited: {name} ({key})")
b = bibentry("balakrishnan2024")
if not all(x in b for x in ("Balakrishnan, Sidhya", "Chan, Sewin", "Constantino, Sara", "Haushofer, Johannes", "Morduch, Jonathan", "33209", "10.3386/w33209", "2024", "nov",
                            "Household Responses to Guaranteed Income: Experimental Evidence from {Compton, California}")):
    err.append("[27] Compton metadata differs from the supplied lookup")
b = bibentry("bastian2017")
if not all(x in b for x in ("Bastian, Gautam", "Goldstein, Markus", "Papineni, Sreelakshmi", "Gender Innovation Lab Policy Brief", "{21}", "World Bank", "2017")):
    err.append("[28] FNLP 2017 metadata differs from the supplied lookup")
b = bibentry("papineni2025")
if not all(x in b for x in ("Papineni, Sreelakshmi", "Gonzalez Martinez, Paula Lorena", "Goldstein, Markus", "Friedman, Jed", "11112", "10.1596/1813-9450-11112", "may", "2025")):
    err.append("[28] FNLP 2025 metadata differs from the supplied lookup")
b = bibentry("watts1974")
if not all(x in b for x in ("Watts, Harold W.", "Cain, Glen G.", "196-74", "Institute for Research on Poverty", "1974")):
    err.append("[29] NJ-P metadata differs from the supplied lookup")
b = bibentry("kehrer1979")
if not all(x in b for x in ("Kehrer, Kenneth C.", "McDonald, John F.", "Moffitt, Robert A.", "Final Report of the {Gary} Income Maintenance Experiment: Labor Supply",
                            "Mathematica Policy Research", "nov", "1979")) or not re.search(r"Gary[^.]{0,40}\\cite[pt]?\{kehrer1979\}", VIS):
    err.append("[30] Gary metadata / primary source differs from the supplied lookup")
if "{206--217}" not in bibentry("elmore1986"):
    err.append("[31] Elmore pages are not 206-217")
if not all(x in bibentry("bastagli2016") for x in ("Bastagli, Francesca", "Hagen-Zanker, Jessica", "Harman, Luke", "Barca, Valentina", "Sturge, Georgina", "Schmidt, Tanja", "Pellerano, Luca")):
    err.append("[32] Bastagli author list incomplete")
# 33
rows = TA.audit(tex)
if any(r["status"] != "TRACED" for r in rows):
    err.append(f"[33] untraced numbers: {[r['number'] + ' @ ' + r['text'][:40] for r in rows if r['status'] != 'TRACED'][:4]}")
if DEFAULT and subprocess.run([sys.executable, "-I", os.path.join(HERE, "scripts", "build_tex_audit.py"), "--check"], capture_output=True).returncode:
    err.append("[33] TEX_NUMERIC_AUDIT.csv not current")
if DEFAULT and subprocess.run([sys.executable, "-I", os.path.join(HERE, "scripts", "build_manuscript_tables.py"), "--check"], capture_output=True).returncode:
    err.append("[33] generated tables not current")
# 34 / 35 / 36  (D048B: disclosure facts supplied by the author; see revision_v1/AUTHOR_AI_DISCLOSURE_PROVENANCE.md)
ai = section("GenAI use") or section("AI use")
meth = section("Methods")
if "[AUTHOR FACT REQUIRED" in ai or not all(x in ai for x in ("Claude Code agent (Claude Opus 5.5)", "second coding pass of 25 cases was performed by GPT-5.6 Sol", "session", "not to the original codes",
        "under the author's scientific oversight and final decision authority", "ChatGPT", "No participant-level data were processed by any AI system")) \
        or re.search(r"\b(GPT-?\d(?!\.6 Sol)|OpenAI|Llama|Mistral)\b|Gemini(?! 3\.1 Pro)", tex) or re.search(r"ChatGPT[^.]{0,80}\b(original|operational) cod", ai) \
        or re.search(r"independent second coder|human expert|second (human )?expert|human (second )?coder (performed|coded)", FLAT, re.I) \
        or "a blinded second coding pass, carried out separately from the original coding and without access to the original codes" not in FLAT \
        or "inter-coding reproducibility diagnostics for the written codebook, not conventional inter-rater reliability" not in meth \
        or re.search(r"Whether these statistics are read as", FLAT) or re.search(r"(?<!not conventional )inter-rater reliability(?! between human coders)", FLAT):
    err.append("[34] AI disclosure missing / altered or second pass mis-described")
fund, coi = section("Funding"), section("Competing interests")
if "This research received no external funding." not in fund or "[AUTHOR FACT" in fund or "The author declares no competing interests." not in coi \
        or re.search(r"normative|motivat|ideolog|support(s|ed)? (for )?basic income|policy preference", coi + " " + section("Author note"), re.I):
    err.append("[34] funding / competing-interests statement missing or altered")
facts = rb(os.path.join(HERE, "revision_v1", "AUTHOR_FACTS_REQUIRED.md")).decode()
rd_txt = rb(READY).decode()
dec = rb(os.path.join(ROOT, "09_meta/decision_log/2026-10-23_author-ai-disclosure.md")).decode()
left = re.findall(r"\[AUTHOR (?:NAME: AUTHOR )?FACT REQUIRED[^\]]*\]", VIS + (AUTH.group(0) if AUTH else ""))
if len(left) > 1 or any("repository is currently private" not in x for x in left) or "AUTHOR FACT" in (AUTH.group(0) if AUTH else "AUTHOR FACT") \
        or (left and ("SUBMISSION BLOCKED" not in rd_txt or "SUBMISSION BLOCKED" not in dec or re.search(r"(?m)^\*\*Verdict:.*READY FOR SUBMISSION", rd_txt))) \
        or "AUTHOR/AI DISCLOSURE READY" not in rd_txt or re.search(r"(?m)^\| (1[0-1]|[1-9]) \|.*\[AUTHOR FACT REQUIRED\]", facts):
    err.append("[35] unresolved author facts beyond name / repository release, or readiness status inconsistent")
if "publication-facing source of truth" not in tex[:300] or "manuscript.tex" not in dec:
    err.append("[36] manuscript.tex not declared the source of truth")
# 38 / 39
if DEFAULT:
    if subprocess.run([sys.executable, "-I", os.path.join(RT, "final_scope_c/validate_final_scope_c.py")], capture_output=True).returncode:
        err.append("[38] D043 validator fails")
    if subprocess.run([sys.executable, "-I", os.path.join(HERE, "review/validate_d046_review.py")], capture_output=True).returncode:
        err.append("[39] D046 validator fails")

# 40-44 (D048A)
D48 = rb(os.path.join(ROOT, "09_meta/decision_log/2026-10-24_bibliography-and-supplement.md")).decode()
VER = {"pearl2014": ("Pearl, Judea and Bareinboim, Elias", "External Validity: From Do-Calculus to Transportability Across Populations", "{4}", "{579--595}"),
       "degtiar2023": ("Degtiar, Irina and Rose, Sherri", "A Review of Generalizability and Transportability", "{10}", "{501--524}"),
       "hernan2011": ("Hern{\\'a}n, Miguel A. and VanderWeele, Tyler J.", "Compound Treatments and Transportability of Causal Inference", "{3}", "{368--377}"),
       "thompson2002": ("Thompson, Simon G. and Higgins, Julian P. T.", "How Should Meta-Regression Analyses Be Undertaken and Interpreted?", "{11}", "{1559--1573}"),
       "riley2020": ("Riley, Richard D. and Debray, Thomas P. A. and Fisher, David and Hattle, Miriam and Marlin, Nadine and Hoogland, Jeroen and Gueyffier, Francois and "
                     "Staessen, Jan A. and Wang, Jiguang and Moons, Karel G. M. and Reitsma, Johannes B. and Ensor, Joie", "Participant-Level Covariates", "{15}", "{2115--2137}")}
if re.search(r"to be verified", bib, re.I) or any(not all(x in bibentry(k) for x in v) for k, v in VER.items()) or REC.get("bibtex_warnings") != "0" \
        or not os.path.exists(os.path.join(HERE, "revision_v1", "BIBLIOGRAPHY_VERIFICATION.md")):
    err.append("[40] methodological anchors not closed with verified metadata")
f1 = section("From experiment counts")
cap1 = re.search(r"\\caption\{(Comparison-level audit stages.*?)\}\s*\\label\{fig:chain\}", VIS, re.S)
if re.search(r"five (operational )?audit stages|chain of audit stages---variation, isolation, compatible estimand, usable uncertainty and an independent validation", FLAT) \
        or "not a fifth stage" not in f1 or not cap1 or "not a fifth stage" not in cap1.group(1) or "in four stages" not in FLAT[:3000] \
        or "not a fifth stage" not in rb(os.path.join(HERE, "figures", "build_figures.py")).decode() or "Formal transport results can identify an effect in a new setting from a single source" not in FLAT:
    err.append("[41] validation presented as a fifth comparison-level stage, or one-source transport no longer acknowledged")
SUP = os.path.join(HERE, "supplement")
SREC = (rd(os.path.join(SUP, "SUPPLEMENT_BUILD_RECORD.csv")) or [{}])[0]
saud = rd(os.path.join(SUP, "SUPPLEMENT_NUMERIC_AUDIT.csv"))
if not os.path.exists(os.path.join(SUP, "supplement.pdf")) or any(SREC.get(k) != "0" for k in ("undefined_references", "missing_files", "latex_errors", "rerun_warnings", "overfull_boxes")) \
        or SREC.get("supplement_pdf_sha256") != sha(rb(os.path.join(SUP, "supplement.pdf"))) or SREC.get("supplement_tex_sha256") != sha(rb(os.path.join(SUP, "supplement.tex"))) \
        or not saud or any(r["status"] != "TRACED" for r in saud):
    err.append("[42] supplement not compiled cleanly / build record stale / untraced supplement numbers")
if DEFAULT and (subprocess.run([sys.executable, "-I", os.path.join(HERE, "scripts", "build_supplement_tables.py"), "--check"], capture_output=True).returncode
                or subprocess.run([sys.executable, "-I", os.path.join(HERE, "scripts", "build_supplement.py"), "--check-audit"], capture_output=True).returncode):
    err.append("[42] supplement tables / numeric audit are not a deterministic rebuild")
stex = rb(os.path.join(SUP, "supplement.tex")).decode()
SV = re.sub(r"\s+", " ", re.sub(r"(?<!\\)%.*$", "", stex, flags=re.M))
sgen = " ".join(rb(p).decode() for p in sorted(__import__("glob").glob(os.path.join(SUP, "generated", "*.tex"))))
if re.search(r"pre-?regist|\bregistered\b", SV + sgen, re.I) or re.search(r"\b52\b(?![}-])", re.sub(r"\\texttt\{[^}]*\}", " ", SV)) \
        or re.search(r"H002[^.]{0,60}\b(rejected|falsified|tested|refuted)\b", SV + sgen) or "not a census" not in SV or "frame-defined universe of 43" not in SV \
        or "39 were verified against primary sources, 2 remained pending and 2 had unresolved frame conflicts" not in SV \
        or "No compatible published direct contrast was located in the accessible RIME-family record after the bounded search" not in SV \
        or not all(f"\\section{{{t}" in stex for t in ("Evidence frame status", "Full architecture-support grid", "Near-miss inventory", "Full support paths",
                                                        "Minimum reporting", "Codebook", "RIME bounded search", "Source access", "Software validation", "Transport-support labels")) \
        or "fig5_status_changing_evidence.pdf" not in stex or "not scientific validation" not in SV or "not a fifth stage" not in SV:
    err.append("[43] supplement wording / structure departs from the frozen claims")
old_keys = set(re.findall(r"@\w+\{([^,]+),", git("e93f365", f"{MSREL}/references.bib").decode()))
ADD = {r["key"]: r for f in ("D048C_REFERENCE_ADDITIONS.csv", "D049_REFERENCE_ADDITIONS.csv") for r in rd(os.path.join(HERE, "revision_v1", f))}
PFA = rb(os.path.join(RT, "POLICYMAKER_FIRST_PRIOR_ART_AUDIT.md")).decode()
D49 = rb(os.path.join(HERE, "revision_v1", "D049_CANONICAL_MANUSCRIPT_AUDIT.md")).decode()
if bibkeys != old_keys | set(ADD) or (old_keys - bibkeys) or any((r["doi"] not in PFA and r["doi"] not in D49) or r["doi"].lower() not in bibentry(k).lower() for k, r in ADD.items()):
    err.append(f"[44] references differ from D047 + the audited D048C additions: {sorted(bibkeys ^ (old_keys | set(ADD)))}")
if "D048A" not in D48 or "policymaker-first prior-art audit" not in D48:
    err.append("[44] D048A decision record missing")

# 45-48 (D048C)
D48C = rb(os.path.join(ROOT, "09_meta/decision_log/2026-10-24_ontology-prior-art-and-public-release.md")).decode()
cap4 = re.search(r"\\caption\{(Where isolated designs stop.*?)\}\s*\\label\{fig:nearmiss\}", VIS, re.S)
cap4 = cap4.group(1) if cap4 else re.search(r"\\caption\{(Where isolated designs stop[^%]*)", VIS).group(1)
if "family--dimension entry" not in cap4 or re.search(r"every independent family whose focal (comparison|path) is isolated", VIS + rb(os.path.join(HERE, "figures", "build_figures.py")).decode()) \
        or "contains 13 rows, each one dimension--design entry, representing 12 unique designs" not in SV \
        or (DEFAULT and subprocess.run([sys.executable, "-I", os.path.join(HERE, "scripts", "build_ontology_audit.py"), "--check"], capture_output=True).returncode) \
        or not os.path.exists(os.path.join(HERE, "revision_v1", "NEAR_MISS_ONTOLOGY_AUDIT.md")):
    err.append("[45] near-miss counting units ambiguous or ontology audit stale")
if re.search(r"saparated|every AI-generated outputs", tex):
    err.append("[46] known disclosure typos present")
if "P2 = SURVIVES, NARROWED" not in PFA or "Component-level learning is thus an established policy-analysis objective; this paper audits whether a major experimental basic-income evidence base actually supplies the evidence required to do it" not in FLAT \
        or any(re.search(r"\b(we are the first|first (study|paper) to|novel (framework|theory)|new (causal|transport)[- ]?(framework|theory|method)|prior reviews (failed|ignored))\b", x, re.I) and not NEG.search(x) for x in SENT) \
        or "policymaker-first" not in D48C or not all(k in cites for k in ADD):
    err.append("[47] prior-art positioning missing, novelty overclaimed, or audited references uncited")
# 49 (D049 canonical closure)
lim = section("Limitations")
ack = section("Acknowledgments")
jr = rb(os.path.join(HERE, "journals", "README.md")).decode()
if len(re.findall(r"\\item", re.search(r"\\section\{Limitations\}(.*?)\\section", VIS, re.S).group(1))) < 12 \
        or not all(x in lim for x in ("frame-defined universe", "deliberately conservative", "Model-based historical analyses", "not conventional inter-rater reliability",
                                       "Validation requirement", "remains a hypothesis")) \
        or not all(x in FLAT for x in ("For researchers and funders.", "For governments and policy designers.", "For evidence synthesis and public debate.")) \
        or not ack or re.search(r"\b(De Wispelaere|ICPSR|Riddell|Gonzalez|MDRC)\b", ack) or "did not review this article" not in ack \
        or "canonical scientific source" not in jr or "must never become independent scientific authorities" not in jr \
        or any(re.search(r"(design|architecture)( features?)? (does|do) not matter|(design|architecture) is irrelevant", x, re.I) and not NEG.search(x.replace("not matter", "").replace("is irrelevant", "")) for x in SENT) \
        or "SCIENTIFICALLY AND EDITORIALLY CLOSED" not in rb(os.path.join(HERE, "revision_v1", "D049_CANONICAL_MANUSCRIPT_AUDIT.md")).decode():
    err.append("[49] canonical closure elements missing (limitations, implications, generic acknowledgment, journals README) or design-irrelevance claim")
# 50 (D050 independent-critique revision)
abstract = re.sub(r"\\s+", " ", re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", VIS, re.S).group(1))
fb = rb(os.path.join(HERE, "figures", "build_figures.py")).decode()
f1 = fb[fb.index("def fig1():"):fb.index("def fig2():")]
if re.search(r"adversarial|stress[- ]test", ai, re.I) \
        or not all(x in abstract for x in ("hours or earnings thresholds", "withdrawal and conditionality each have two supporting experiments", "does not replace the prespecified target")) \
        or "Panel B is physically separate" not in f1 or "Independent\\nvalidation" in f1 or "\\item \\textbf{Coding reproducibility.}" not in VIS \
        or "(B) A feasibility rule specific to the prospective discovery-and-validation test" not in FLAT:
    err.append("[50] D050 revision missing: disclosure chronology, abstract sensitivity, two-panel Figure 1 or reproducibility wording")
PUB = os.path.join(ROOT, "scripts", "validate_public_release.py")
if DEFAULT and (not os.path.exists(PUB) or subprocess.run([sys.executable, "-I", PUB], capture_output=True).returncode):
    err.append("[48] public replication package missing or invalid")

if err:
    print("FAIL")
    for e in err:
        print("  -", e)
    sys.exit(1)
print(f"PASS (D047: manuscript.tex compiled ({REC.get('pdf_pages')} pp.); {len(cites)} citation keys resolved; {len(rows)} numbers traced; disclosure resolved; bibliography verified; supplement compiled; ontology audited; public release valid; canonical closure; independent-critique revision; 50 checks)")

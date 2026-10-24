#!/usr/bin/env python3
"""D045: validate manuscript draft v0. Exits 1 on failure. Checks 1-30 follow D045 section 34.
Usage: python3 -I validate_manuscript_v0.py [--dir D]
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
D = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else HERE
REV = "86aea5c"
sys.path.insert(0, HERE)
import build_manuscript_audits as AUD  # noqa: E402

err = []
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, "rb").read() if os.path.exists(p) else b""
git = lambda rev, p: subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{p}"], capture_output=True).stdout
gitls = lambda rev, p: subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", rev, p], capture_output=True, text=True).stdout.split()
MS = rb(os.path.join(D, "manuscript_v0.md")).decode()
VIS = re.sub(r"<!--.*?-->", "", MS)
FLAT = re.sub(r"\s+", " ", VIS)
SENT = re.split(r"(?<=[.!?])\s+|\n", VIS)
NEG = re.compile(r"\b(not|no|never|nor|neither|rather than|without)\b", re.I)
DOCS = {n: rb(os.path.join(D, n)).decode() for n in os.listdir(D) if n.endswith((".md", ".csv"))}
DOCS["D045"] = rb(os.path.join(ROOT, "09_meta/decision_log/2026-10-23_manuscript-draft-v0.md")).decode()


def section(title):
    m = re.search(rf"^## [^\n]*{re.escape(title)}[^\n]*\n(.*?)(?=^## |\Z)", MS, re.M | re.S)
    return re.sub(r"<!--.*?-->", "", m.group(1)) if m else ""


# 1 / 2
fz = list(csv.DictReader(open(os.path.join(D, "D044_MANUSCRIPT_INPUT_FREEZE.csv"), newline=""))) if os.path.exists(os.path.join(D, "D044_MANUSCRIPT_INPUT_FREEZE.csv")) else []
need = ["paper/README.md", "PAPER_CLAIM_MATRIX.md", "PAPER_NUMERIC_CLAIMS.csv", "validate_paper_architecture.py", "BI_SPECIFIC_PRIOR_ART_AUDIT.md",
        "bi-specific-paper-prior-art-audit.md", "support-coding-reliability-protocol.md", "support-coding-reliability-adjudication.md",
        "layer-A-census-support-geometry.md", "RIME-layer-B-extraction.md", "final-SCOPE-C-support-synthesis.md", "paper-architecture-and-research-agenda.md"]
if any(not any(r["file"].endswith(n) for r in fz) for n in need):
    err.append("[1] D044_MANUSCRIPT_INPUT_FREEZE.csv lacks a required input")
for r in fz:
    if sha(git(REV, r["file"])) != r["sha256"] or sha(rb(os.path.join(ROOT, r["file"]))) != r["sha256"]:
        err.append(f"[1] frozen input changed: {r['file']}")
for sub in ("05_papers/representation_transport/final_scope_c", "05_papers/representation_transport/evidence_universe", "05_papers/representation_transport/paper",
            "05_papers/representation_transport/coding_reliability"):
    for p in gitls(REV, sub):
        if "__pycache__" not in p and rb(os.path.join(ROOT, p)) != git(REV, p):
            err.append(f"[2] scientific input changed since {REV}: {p}")
# 3 / 4
EXPECTED = {"D044_MANUSCRIPT_INPUT_FREEZE.csv", "manuscript_v0.md", "RELATED_WORK_DRAFT_BASIS.md", "CODING_RELIABILITY_MANUSCRIPT_NOTE.md",
            "POST_D044_ACCESS_RECOVERABILITY_NOTE.md", "REFERENCES_DRAFT.md", "CITATION_GAPS.md", "FIGURE_CAPTIONS_v0.md", "FIGURE_DATA_MAP.csv",
            "MANUSCRIPT_NUMERIC_AUDIT.csv", "MANUSCRIPT_CLAIM_AUDIT.md", "MANUSCRIPT_OVERCLAIM_AUDIT.md", "README.md", "build_manuscript_tables.py",
            "build_manuscript_audits.py", "validate_manuscript_v0.py", "tables", "__pycache__"}
if set(os.listdir(D)) - EXPECTED:
    err.append(f"[3] unexpected files in manuscript/: {sorted(set(os.listdir(D)) - EXPECTED)}")
repo_text = "".join(rb(os.path.join(ROOT, p)).decode(errors="ignore") for p in gitls(REV, "02_evidence/studies") + gitls(REV, "05_papers/representation_transport/BI_SPECIFIC_PRIOR_ART_AUDIT.md")
                    + gitls(REV, "05_papers/representation_transport/evidence_universe/layer_a_extraction/SOURCE_LOG.csv"))
for doi in re.findall(r"10\.\d{4,}/[^\s)\]]+", DOCS.get("REFERENCES_DRAFT.md", "")):
    if doi.rstrip(".") not in repo_text:
        err.append(f"[3] reference metadata not in repository records: {doi}")
if re.search(r"https?://", VIS):
    err.append("[3] the manuscript cites a URL source")
for f in ("build_manuscript_tables.py", "build_manuscript_audits.py"):
    if re.search(r"\b(urllib|requests|socket|http\.client)\b|https?://", rb(os.path.join(HERE, f)).decode()):
        err.append(f"[4] {f} requires network acquisition")
# 5 / 6
SECTIONS = ["Introduction", "From experiment counts to transport-ready evidence", "Evidence universe", "census geometry", "Selection dependence",
            "Historical and adjacent designs", "currently infeasible", "What evidence would change the status", "Discussion", "Limitations", "Methods"]
heads = re.findall(r"^## (.*)$", MS, re.M)
for s in SECTIONS:
    if not any(s.lower() in h.lower() for h in heads):
        err.append(f"[5] missing planned section: {s}")
abs_words = len(re.findall(r"[A-Za-z0-9][\w'’\-/.]*", section("Abstract")))
if not 180 <= abs_words <= 230:
    err.append(f"[6] abstract has {abs_words} words (180-230 required)")
# 7 / 8 / 9
for name in ("Burtless", "Elmore", "Crosta", "Chrisp", "Bastagli", "Corinth"):
    if name not in VIS:
        err.append(f"[7] prior art not acknowledged: {name}")
if "Burtless (1986) and Elmore (1986) made central parts of it" not in FLAT or "confirms and updates these diagnoses rather than discovering them" not in FLAT \
        or "is not new" not in section("Introduction"):
    err.append("[8] the Burtless / Elmore anticipation is hidden")
for s in SENT:
    if re.search(r"\b(first|novel|unprecedented)\b", s, re.I) and not NEG.search(s):
        err.append(f"[8] novelty overclaim: {s[:70]}")
if "five sources that could not be read" not in FLAT or re.search(r"Merrill|Salamanca|What Works Scotland", VIS):
    err.append("[9] R0 sources not treated as unread limitations (or characterised)")
# 10 / 11 / 12
rel = AUD.rel_tokens()
tab = re.search(r"\| Variation \| 25 of 25.*?\n((?:\|.*\n)+)", MS)
ms_rel = AUD.tokens(tab.group(0)) if tab else set()
REQUIRED_REL = {"25", "23", "19", "21", "24", ".92", ".884", ".76", ".490", ".84", ".606", ".96", ".936", ".918"}
if not ms_rel <= rel or not REQUIRED_REL <= ms_rel:
    err.append(f"[10] reliability metrics differ from D034: extra {sorted(ms_rel - rel)}, missing {sorted(REQUIRED_REL - ms_rel)}")
if "Post-adjudication agreement is not reported as reliability" not in FLAT or re.search(r"post-adjudication agreement (was|of|reached)\b", FLAT, re.I):
    err.append("[11] post-adjudication agreement reported as reliability")
for s in SENT:
    if re.search(r"second-coded|double-coded|double coding", s) and not NEG.search(s):
        err.append(f"[12] rules / census described as independently second-coded: {s[:70]}")
if "were not independently second-coded" not in FLAT:
    err.append("[12] H / I / J caveat missing")
# 13
rows = AUD.numeric_audit(MS)
if any(r["status"] != "TRACED" for r in rows):
    err.append(f"[13] untraced numbers: {[r['number'] + ' @ ' + r['manuscript_location'] for r in rows if r['status'] != 'TRACED'][:5]}")
if D == HERE and subprocess.run([sys.executable, "-I", os.path.join(HERE, "build_manuscript_audits.py"), "--check"], capture_output=True).returncode:
    err.append("[13] audit files are not a fresh rebuild")
_, oc = AUD.overclaim_audit(MS)
if any(r[3] == "UNJUSTIFIED" for r in oc):
    err.append(f"[13] unjustified risky term: {[r[:2] for r in oc if r[3] == 'UNJUSTIFIED'][:3]}")
# 14 / 15 / 16
for s in SENT:
    if re.search(r"\b52\b", s) and not NEG.search(s):
        err.append(f"[14] 52-study statement: {s[:70]}")
    if re.search(r"Layer B", s) and re.search(r"\bcensus\b|prevalence", s) and not NEG.search(s):
        err.append(f"[16] Layer B as census / prevalence: {s[:70]}")
if "43 modern" not in FLAT or "Layer B is not a census" not in FLAT:
    err.append("[15/16] Layer A 43 / Layer B audit wording missing")
# 17
if "No compatible published direct contrast was located in the accessible RIME-family record after the bounded search" not in FLAT:
    err.append("[17] RIME bounded-access wording missing")
for s in SENT:
    if re.search(r"(estimate|contrast|result) does not exist|RIME (did not|never) report", s, re.I) or (re.search(r"\bRIME\b", s) and re.search(r"was never estimated", s) and "do not conclude" not in s):
        err.append(f"[17] RIME absence asserted: {s[:70]}")
# 18 / 19
if any(p.startswith("H002") for p in os.listdir(os.path.join(ROOT, "09_meta/hypotheses"))) or re.search(r"\bMET\b", VIS):
    err.append("[18] H002 created or described as MET")
if "currently infeasible" not in FLAT:
    err.append("[19] feasibility wording missing")
for s in SENT:
    if re.search(r"falsif|\brefuted\b|\brejected\b|\bfailed\b", s, re.I) and not NEG.search(s):
        err.append(f"[19] falsification language: {s[:70]}")
    if re.search(r"architecture (does not|doesn't) matter|irrelevan", s, re.I) and not NEG.search(s.replace("does not matter", "")):
        err.append(f"[19] architecture irrelevance claimed: {s[:70]}")
# 20 / 21
s7 = section("currently infeasible")
if "two supporting families" not in s7 or "Wageningen" not in s7 or "registered conclusion is unchanged" not in s7:
    err.append("[20] E-B sensitivity not visible in the feasibility section")
if re.search(r"\bP1\b|P2 (is )?(weakened|downgraded)", VIS):
    err.append("[21] paper-viability status altered")
# 22 / 23
for s in SENT:
    m22 = re.search(r"\b(basic income|BI|guaranteed income) (works|is effective|does not work|reduces employment|increases employment|should be adopted)\b", s, re.I)
    if m22 and not NEG.search(s.replace(m22.group(0), "")):
        err.append(f"[22] effectiveness / desirability claim: {s[:70]}")
for n, t in DOCS.items():
    if re.search(r"\b(NHB|Nature Human Behaviour|JPAM|Journal of Economic Surveys|Research Synthesis Methods|Basic Income Studies|PNAS|target journal|selected journal)\b", t) \
            and n not in ("CITATION_GAPS.md",):
        err.append(f"[23] journal named / selected in {n}")
# 24 / 25
note = DOCS.get("POST_D044_ACCESS_RECOVERABILITY_NOTE.md", "")
wrp = [r for r in csv.DictReader(open(os.path.join(RT, "final_scope_c/CONDITIONALITY_SUPPORT_PATHS_FINAL.csv"), newline="")) if r["experiment_id"] == "X066"]
if "ACCESS METADATA ONLY" not in note or not wrp or (wrp[0]["I"], wrp[0]["E"], wrp[0]["U"], wrp[0]["usable_U"]) != ("PURE", "E-A", "STARS", "NO") \
        or "U = STARS, usable_U = NO" not in note or re.search(r"1,174|Ericsson|ICPSR", VIS):
    err.append("[24] WRP access metadata altered support coding or entered the main text")
for s in SENT:
    if re.search(r"\bWRP\b|Vermont", s) and re.search(r"\b(now|therefore) (supports|passes|qualifies)|second strict family (exists|is available)", s, re.I):
        err.append(f"[24] access metadata turned into support: {s[:70]}")
for n, t in DOCS.items():
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+|atlassian|jira|ticket[/=]\d|token[:=]|servicedesk", t, re.I):
        err.append(f"[25] private identifier / token / correspondence in {n}")
# 26 / 27
for sub in ("02_evidence/master_map", "05_papers/state_of_understanding"):
    for p in gitls(REV, sub):
        if rb(os.path.join(ROOT, p)) != git(REV, p):
            err.append(f"[{26 if 'master' in sub else 27}] changed: {p}")
# 28 / 29 / 30
if D == HERE and subprocess.run([sys.executable, "-I", os.path.join(HERE, "build_manuscript_tables.py"), "--check"], capture_output=True).returncode:
    err.append("[28] manuscript tables are not a deterministic rebuild")
claims = {r["claim_id"] for r in csv.DictReader(open(os.path.join(RT, "paper/PAPER_NUMERIC_CLAIMS.csv"), newline=""))}
for r in csv.DictReader(open(os.path.join(D, "FIGURE_DATA_MAP.csv"), newline="")) if os.path.exists(os.path.join(D, "FIGURE_DATA_MAP.csv")) else []:
    first = r["authority_file"].split(";")[0].strip()
    if not os.path.exists(os.path.join(ROOT, first)):
        err.append(f"[29] figure authority missing: {first}")
    elif first.endswith(".csv"):
        hdr = open(os.path.join(ROOT, first), newline="").readline()
        for col in [c.split(" ")[0] for c in r["authority_columns_or_rows"].split(";")]:
            if col.strip() and col.strip() not in hdr:
                err.append(f"[29] figure column not in authority: {col.strip()} ({first})")
    if r["numeric_claim_ids"] != "NONE (conceptual)" and not set(r["numeric_claim_ids"].split(";")) <= claims:
        err.append(f"[29] figure claim ids without provenance: {r['numeric_claim_ids']}")
if D == HERE:
    # D044 check 2 is a task-scope guard ("nothing outside paper/ changed since b5ef008") that cannot hold after any later task.
    # The D044 validator is therefore run in content mode (--dir on a byte-identical copy of paper/), which executes every other check.
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    shutil.copytree(os.path.join(RT, "paper"), os.path.join(tmp, "paper"), ignore=shutil.ignore_patterns("__pycache__"))
    p30 = subprocess.run([sys.executable, "-I", os.path.join(RT, "paper/validate_paper_architecture.py"), "--dir", os.path.join(tmp, "paper")], capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)
    if p30.returncode:
        err.append(f"[30] D044 validator fails (content mode): {p30.stdout.strip()[:200]}")

if err:
    print("FAIL")
    for e in err:
        print("  -", e)
    sys.exit(1)
print(f"PASS (D045: manuscript v0; abstract {abs_words} words; {len(rows)} numbers traced; reliability = D034; feasibility wording intact; 30 checks)")

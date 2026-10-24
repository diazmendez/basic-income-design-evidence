#!/usr/bin/env python3
"""D046: validate the adversarial review, figure build and revision plan. Exits 1 on failure. Checks 1-26 follow D046 section 29.
Usage: python3 -I validate_d046_review.py [--review DIR] [--figs DIR]
"""
import csv
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MSD = os.path.dirname(HERE)
RT = os.path.dirname(MSD)
ROOT = os.path.abspath(os.path.join(RT, "..", ".."))
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
R = arg("--review", HERE)
F = arg("--figs", os.path.join(MSD, "figures"))
REV = "56a63a2"
err = []
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, "rb").read() if os.path.exists(p) else b""
rd = lambda p: list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []
git = lambda rev, p: subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{p}"], capture_output=True).stdout
gitls = lambda rev, p: subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", rev, p], capture_output=True, text=True).stdout.split()
DOC = {n: rb(os.path.join(R, n)).decode() for n in os.listdir(R) if n.endswith(".md")}
DOC["FIGURE_VISUAL_AUDIT.md"] = rb(os.path.join(F, "FIGURE_VISUAL_AUDIT.md")).decode()
DOC["D046"] = rb(os.path.join(ROOT, "09_meta/decision_log/2026-10-23_manuscript-adversarial-review.md")).decode()
LINES = [(n, l) for n, t in DOC.items() for l in t.splitlines()]
NEG = re.compile(r"\b(not|no|never|nor|nowhere|neither|without|avoid|forbid\w*|instead of|rather than|INVALID|overstates?|never done)\b", re.I)
ARCH = ["WITHDRAWAL", "CONDITIONALITY", "CADENCE"]

# 1 / 2 / 4
MS_REL = "05_papers/representation_transport/manuscript/manuscript_v0.md"
if rb(os.path.join(ROOT, MS_REL)) != git(REV, MS_REL):
    err.append("[1] manuscript_v0.md changed")
fz = rd(os.path.join(R, "D045_REVIEW_INPUT_FREEZE.csv"))
need = ["manuscript_v0.md", "2026-10-17_stage-4-formal-framework-prior-art-audit.md", "formal_framework_prior_art_audit.md",
        "formal_representation_compression_transport.md", "bi-specific-paper-prior-art-audit.md", "support-coding-reliability-protocol.md",
        "support-coding-reliability-adjudication.md", "layer-A-census-support-geometry.md", "RIME-layer-B-extraction.md",
        "final-SCOPE-C-support-synthesis.md", "paper-architecture-and-research-agenda.md", "2026-10-23_manuscript-draft-v0.md"]
if any(not any(r["file"].endswith(n) for r in fz) for n in need):
    err.append("[2] D045_REVIEW_INPUT_FREEZE.csv lacks a required input")
for r in fz:
    if sha(git(REV, r["file"])) != r["sha256"] or sha(rb(os.path.join(ROOT, r["file"]))) != r["sha256"]:
        err.append(f"[2] frozen input changed: {r['file']}")
for sub in ("05_papers/representation_transport/final_scope_c", "05_papers/representation_transport/paper", "05_papers/representation_transport/evidence_universe",
            "05_papers/representation_transport/coding_reliability", "05_papers/representation_transport/manuscript"):
    for p in gitls(REV, sub):
        if "__pycache__" not in p and rb(os.path.join(ROOT, p)) != git(REV, p):
            err.append(f"[{4 if 'final_scope_c' in p or 'evidence_universe' in p else 2}] authority changed since {REV}: {p}")
if "SCIENTIFIC REOPEN REQUIRED — none" not in DOC.get("ADVERSARIAL_REVIEW.md", ""):
    err.append("[4] the review does not record the scientific-reopen status")
# 3
d24 = rb(os.path.join(ROOT, "03_models/formal_framework_prior_art_audit.md")).decode()
for n, l in LINES:
    if re.search(r"https?://|\.literature/", l):
        err.append(f"[3] {n}: new source reference: {l[:70]}")
    for doi in re.findall(r"10\.\d{4,}/[^\s,;)|]+", l):
        if doi.rstrip(".") not in d24 and doi.rstrip(".") not in rb(os.path.join(MSD, "REFERENCES_DRAFT.md")).decode():
            err.append(f"[3] {n}: DOI not in frozen records: {doi}")
# 5 / 6
ta = DOC.get("TRANSPORTABILITY_WORDING_AUDIT.md", "")
if "For the prospective empirical test considered here, we require one independent family for identification / discovery and another for validation" not in ta \
        or "Pearl & Bareinboim" not in ta or "L45" not in ta:
    err.append("[5] transportability wording audit missing or incomplete")
for n, l in LINES:
    if re.search(r"(universal\w*|always|in general|formal transportability)[^.\n]{0,40}requires? (at least )?two independent", l, re.I) and not NEG.search(l):
        err.append(f"[5] two independent sources stated as a universal transport requirement: {n}: {l[:70]}")
mp = DOC.get("METHODS_PRIOR_ART_INTEGRATION_PLAN.md", "")
for a in ("Pearl & Bareinboim (2014)", "Bareinboim & Pearl (2016)", "Degtiar & Rose", "Hotz, Imbens & Mortimer", "Allcott", "Hernán & VanderWeele", "Thompson & Higgins",
          "Fisher et al.", "Riley et al.", "Raudenbush & Bloom", "Olsen et al."):
    if a not in mp:
        err.append(f"[6] D024 anchor not considered: {a}")
# 7
pa = DOC.get("PROSPECTIVE_SPECIFICATION_WORDING_AUDIT.md", "")
ms = git(REV, MS_REL).decode()
reg_lines = sorted({i + 1 for i, l in enumerate(ms.splitlines()) if re.search(r"preregist|pre-regist|\bregistered\b|registration", re.sub(r"<!--.*?-->", "", l), re.I)})
if not pa or any(f"L{i}" not in pa for i in reg_lines):
    err.append(f"[7] prospective-specification audit misses manuscript lines {[i for i in reg_lines if f'L{i}' not in pa]}")
for row in [l for l in pa.splitlines() if l.startswith("| ") and not l.startswith("| #") and "---" not in l]:
    cells = [c.strip() for c in row.split("|")[1:-1]]
    if len(cells) >= 5 and re.search(r"pre-?registered|\bregistered\b|registration", cells[-1].replace("not the prospectively", ""), re.I):
        err.append(f"[7] proposed wording retains registration language: {cells[-1][:60]}")
# 8 / 9 / 24
cd = DOC.get("CODER_AI_DISCLOSURE_STATUS.md", "")
if "BLOCKING AUTHOR DISCLOSURE REQUIRED" not in cd or "[AUTHOR FACT REQUIRED]" not in cd or "No second coding was performed by Claude" not in cd:
    err.append("[8] coder / AI disclosure status missing or incomplete")
for n, l in LINES:
    if re.search(r"second (coder|coding pass)[^.\n]{0,60}\b(was|is|=)\b[^.\n]{0,30}\b(human|expert|researcher|GPT|ChatGPT|OpenAI|Gemini|Claude|Llama|Mistral)\b", l, re.I) \
            and "AUTHOR FACT" not in l and "human or AI" not in l and "whether" not in l and not NEG.search(l):
        err.append(f"[9] coder identity asserted without author fact: {n}: {l[:80]}")
    if re.search(r"\b(GPT-?\d|ChatGPT|Gemini|Llama|Mistral)\b", l):
        err.append(f"[9] model name inferred: {n}: {l[:70]}")
for f in ("AI_USE_DISCLOSURE_DRAFT.md", "FUNDING_STATEMENT_DRAFT.md", "COMPETING_INTERESTS_DRAFT.md", "DATA_CODE_AVAILABILITY_DRAFT.md"):
    t = DOC.get(f, "")
    if not t or "[AUTHOR FACT REQUIRED" not in t or re.search(r"Ericsson", t):
        err.append(f"[24] disclosure draft missing author-fact markers or naming an employer: {f}")
if re.search(r"received no (project-specific )?(external )?funding", DOC.get("FUNDING_STATEMENT_DRAFT.md", ""), re.I):
    err.append("[24] funding absence asserted without author fact")
# 10
uw = DOC.get("UNCERTAINTY_RULE_WORDING.md", "")
if "would require additional information or assumptions" not in uw:
    err.append("[10] uncertainty-rule wording audit missing")
for n, l in LINES:
    if re.search(r"(p-values?|test statistics?)[^.\n]{0,40}(can never|never (encode|provide|yield)|cannot (ever )?(encode|provide|yield))", l, re.I) and "too strong" not in l:
        err.append(f"[10] overstated uncertainty rationale: {n}: {l[:70]}")
# 11
fc = DOC.get("FRAME_CENSUS_WORDING_AUDIT.md", "")
st = {}
for r in rd(os.path.join(RT, "evidence_universe/layer_a_reconciliation/RECONCILED_LAYER_A_MANIFEST.csv")):
    st[r["verification_status"]] = st.get(r["verification_status"], 0) + 1
if not fc or any(f"| {k} | {v} |" not in fc for k, v in st.items()):
    err.append("[11] census audit missing or verification composition differs from the frozen manifest")
for n, l in LINES:
    if re.search(r"(every|all)[^.\n]{0,20}(basic-income|BI|guaranteed-income)[^.\n]{0,30}experiments?[^.\n]{0,10}(ever|conducted|run)", l, re.I) and not NEG.search(l):
        err.append(f"[11] census scope overstated: {n}: {l[:70]}")
    if re.search(r"\b52\b", l) and not NEG.search(l):
        err.append(f"[11] 52-study statement: {n}: {l[:70]}")
# 12 / 13
ol = DOC.get("OTHER_LANGUAGE_AUDIT.md", "")
if "No compatible published direct contrast was located in the accessible RIME-family record after the bounded search" not in ol:
    err.append("[12] RIME bounded wording not preserved")
for n, l in LINES:
    if re.search(r"RIME", l) and re.search(r"does not exist|never published|was never estimated", l) and not NEG.search(l.replace("never published", "").replace("never estimated", "")):
        err.append(f"[12] RIME absence asserted: {n}: {l[:70]}")
    if re.search(r"\b(WRP|Vermont)\b", l) and re.search(r"now supports|second strict family (exists|is available)|passes the strict|is strict support", l, re.I) and not NEG.search(l):
        err.append(f"[13] WRP access metadata promoted to evidence: {n}: {l[:70]}")
# 14 / 15 / 16 / 17 / 18 / 19
FIGS = ["fig1_support_chain", "fig2_census_attrition", "fig3_selection_audit", "fig4_near_miss_matrix", "fig5_status_changing_evidence"]
for fg in FIGS:
    for ext in ("pdf", "svg", "png"):
        if not os.path.exists(os.path.join(F, f"{fg}.{ext}")) or os.path.getsize(os.path.join(F, f"{fg}.{ext}")) < 1000:
            err.append(f"[14] figure not rendered: {fg}.{ext}")
man = rd(os.path.join(F, "FIGURE_BUILD_MANIFEST.csv"))
if [m["figure"] for m in man] != FIGS:
    err.append("[14] figure manifest incomplete")
for m in man:
    if m["data_file"] != "NONE (conceptual)" and sha(rb(os.path.join(F, m["data_file"]))) != m["data_sha256"]:
        err.append(f"[15] figure data differ from the manifest: {m['data_file']}")
G = os.path.join(RT, "evidence_universe/layer_a_geometry")
geo = {r["architecture_dimension"]: r for r in rd(os.path.join(G, "LAYER_A_SUPPORT_GEOMETRY.csv"))}
sub = {r["architecture_dimension"]: r for r in rd(os.path.join(G, "PRE_CENSUS_MAPPED_LAYER_A_SUBSET_GEOMETRY.csv"))}
blk = {r["architecture_dimension"]: r for r in rd(os.path.join(G, "LAYER_A_BLOCKER_DECOMPOSITION.csv")) if r["scope"] == "LAYER-A-CENSUS-43"}
for r in rd(os.path.join(F, "fig2_census_attrition_data.csv")):
    if r["panel"] == "A" and r["dimension"] not in ARCH:
        err.append(f"[15] between-study dimension plotted in the isolation panel: {r['dimension']}")
    src = geo[r["dimension"]].get(r["quantity"]) if r["quantity"].startswith("families") else blk[r["dimension"]].get(r["quantity"]) if r["quantity"].startswith("V_") \
        else geo[r["dimension"]].get("families_between_study_EA_usableU")
    if src is None or str(src) != r["value"]:
        err.append(f"[15] fig2 value differs from authority: {r['dimension']} {r['quantity']}")
for r in rd(os.path.join(F, "fig3_selection_audit_data.csv")):
    if r["panel"] == "A":
        k = sub if "subset" in r["set"] else geo
        if r["count"] != k[r["dimension"]]["families_between_study_EA_usableU"]:
            err.append(f"[15] fig3 panel A differs: {r['dimension']} {r['set']}")
    else:
        col = r["set"].split(" ")[0]
        if r["count"] != f"{sub[r['dimension']][col]}->{geo[r['dimension']][col]}":
            err.append(f"[15] fig3 panel B differs: {r['dimension']} {col}")
fin = {d: {x["experiment_id"]: x for x in rd(os.path.join(RT, f"final_scope_c/{d}_SUPPORT_PATHS_FINAL.csv")) if x["cell_representative"] == "YES"} for d in ARCH}
for r in rd(os.path.join(F, "fig4_near_miss_matrix_data.csv")):
    x = fin[r["dimension"].upper()].get(r["experiment_id"])
    if not x or any(x[k] != r[k] for k in ("V", "I", "E", "U", "usable_U")):
        err.append(f"[15] fig4 row differs from frozen path: {r['experiment_id']}")
for n in os.listdir(F):
    if n.endswith("_data.csv"):
        hdr = open(os.path.join(F, n)).readline().lower()
        if re.search(r"estimate|effect|p_value|\bse\b|signif|coef", hdr):
            err.append(f"[16] effect field plotted: {n}")
bsrc = rb(os.path.join(F, "build_figures.py")).decode()
if re.search(r"employment_outcomes|outcome_evidence|percent_differential", bsrc):
    err.append("[16] figure builder reads an effect table")
if "nested within" not in bsrc or "no test statistic is computed" not in bsrc or any(re.search(r"p_?val|pvalue", open(os.path.join(F, "fig3_selection_audit_data.csv")).readline(), re.I) for _ in [0]):
    err.append("[17] Figure 3 does not preserve the nested-denominator interpretation")
if "Not a ranking of study quality" not in bsrc or re.search(r"\brank", open(os.path.join(F, "fig4_near_miss_matrix_data.csv")).readline(), re.I):
    err.append("[18] Figure 4 ranking safeguard missing")
if "no claim is made that data access or new trials are currently feasible" not in bsrc or re.search(r"(is|are) (currently )?(accessible|available now|feasible)\b", bsrc.split("SHORT = {")[1].split("}")[0]):
    err.append("[19] Figure 5 makes an access-feasibility claim")
if D := (F == os.path.join(MSD, "figures")):
    if subprocess.run([sys.executable, "-I", os.path.join(F, "build_figures.py"), "--check"], capture_output=True).returncode:
        err.append("[15] figure data / manifest are not a deterministic rebuild")
# 20 / 21 / 22 / 23 / E-B visibility
if "Final main display set" not in DOC.get("DISPLAY_ITEM_DECISION.md", ""):
    err.append("[20] display redundancy decision missing")
if "CONTENT-NECESSARY" not in DOC.get("WORD_BUDGET_REASSESSMENT.md", ""):
    err.append("[21] word-budget reassessment missing")
plan = DOC.get("MANUSCRIPT_V1_REVISION_PLAN.md", "")
for kw in ("transport", "anchors", "registered", "Uncertainty rationale", "Coder identity", "Census scope", "Title", "Abstract", "T table", "Vermont", "reproducibility",
           "citations", "Displays", "Word budget", "E-B sensitivity unchanged"):
    if kw.lower() not in plan.lower():
        err.append(f"[22] revision plan lacks: {kw}")
if "E-B" not in DOC.get("PRIMARY_CLAIM_REVIEW.md", "") or "E-B" not in DOC.get("ADVERSARIAL_REVIEW.md", ""):
    err.append("[22] E-B sensitivity hidden in the review")
for n, l in LINES:
    if re.search(r"\b(NHB|Nature Human Behaviour|JPAM|Journal of Economic Surveys|Research Synthesis Methods|Basic Income Studies|PNAS|target journal|selected journal)\b", l):
        err.append(f"[23] journal named / selected: {n}: {l[:70]}")
# 25 / 26
if subprocess.run([sys.executable, "-I", os.path.join(RT, "final_scope_c/validate_final_scope_c.py")], capture_output=True).returncode:
    err.append("[25] D043 validator fails")
tmp = tempfile.mkdtemp()
try:
    dst = os.path.join(tmp, "manuscript")
    for p in gitls(REV, "05_papers/representation_transport/manuscript"):
        out = os.path.join(dst, p.split("manuscript/", 1)[1])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "wb").write(git(REV, p))
    p26 = subprocess.run([sys.executable, "-I", os.path.join(MSD, "validate_manuscript_v0.py"), "--dir", dst], capture_output=True, text=True)
    if p26.returncode:
        err.append(f"[26] D045 validator fails on its frozen inputs (content mode): {p26.stdout.strip()[:200]}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

if err:
    print("FAIL")
    for e in err:
        print("  -", e)
    sys.exit(1)
print("PASS (D046: manuscript_v0 unchanged; 5 figures rendered from frozen authorities; review / disclosure / revision plan complete; no scientific reopen; 26 checks)")

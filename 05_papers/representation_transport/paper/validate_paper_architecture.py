#!/usr/bin/env python3
"""D044: validate the paper architecture. Exits 1 on failure.

Checks (D044 section 32):
  1  D043 inputs unchanged (freeze vs b5ef008)          11 selection-audit numbers match D041 (recomputed)
  2  no new scientific evidence is added                12 final geometry numbers match D043 (recomputed)
  3  no effect direction / magnitude enters             13 RIME wording respects the bounded-access limitation
  4  no H002 record is created                          14 the E-B sensitivity is not hidden
  5  H002 remains NOT MET / UNREGISTERED                15 the novelty statement respects D030
  6  GENERAL remains UNRESOLVED, not FAILED             16 research-agenda rows map to D043 blockers
  7  P2 remains SURVIVES                                17 every main numeric claim has reproducibility provenance
  8  Layer A remains 43                                 18 the paper claims no BI effectiveness
  9  Layer B remains 9 audited cases, not a census      19 the paper claims no predictive theory
  10 no 52-study denominator is used                    20 no journal is selected
Usage: python3 -I validate_paper_architecture.py [--dir D]
"""
import csv
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
D = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else HERE
REV = "b5ef008"
sys.path.insert(0, HERE)
import build_paper_numbers as N  # noqa: E402

err = []
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, "rb").read() if os.path.exists(p) else b""
rd = lambda p: list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []
git = lambda rev, p: subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{p}"], capture_output=True).stdout
DOCS = {n: rb(os.path.join(D, n)).decode() for n in sorted(os.listdir(D)) if n.endswith(".md")}
DOCS["D044"] = rb(os.path.join(ROOT, "09_meta", "decision_log", "2026-10-19_paper-architecture-and-research-agenda.md")).decode()
NEG = re.compile(r"\b(not|never|no|NOT|NEVER|NO|Not|Never|No|nor|Excluded|excluded|rather than)\b")
lines = [(n, l) for n, t in DOCS.items() for l in t.splitlines()]
claims = {r["claim_id"]: r for r in rd(os.path.join(D, "PAPER_NUMERIC_CLAIMS.csv"))}
fresh = {r["claim_id"]: r for r in N.claims()}

# 1
fz = rd(os.path.join(D, "D043_PAPER_INPUT_FREEZE.csv"))
need = ["FINAL_SCOPE_C_STATUS.md", "SCOPE_C_FINAL_SUPPORT_GEOMETRY.csv", "LAYER_B_SUPPORT_AUDIT.csv", "WITHDRAWAL_SUPPORT_PATHS_FINAL.csv", "CONDITIONALITY_SUPPORT_PATHS_FINAL.csv",
        "CADENCE_SUPPORT_PATHS_FINAL.csv", "FINAL_SCOPE_C_T_SUPPORT.csv", "FINAL_H002_TRIGGER_ASSESSMENT.md", "STAGE4_EMPLOYMENT_STATUS.md", "P2_FINAL_SCOPE_C_ASSESSMENT.md",
        "RESEARCH_AGENDA_GAPS.csv", "MINIMUM_REPORTING_FOR_TRANSPORTABLE_BI_EVIDENCE.md", "WHAT_WOULD_CHANGE_THE_STATUS.md", "STRICT_VS_EXTENSIVE_GATE_SENSITIVITY.md",
        "CLAIM_BOUNDARIES.md", "LAYER_A_SUPPORT_GEOMETRY.csv", "LAYER_A_SELECTION_AUDIT.md", "PRE_CENSUS_MAPPED_LAYER_A_SUBSET_GEOMETRY.csv", "RIME_EXTRACTION_REPORT.md",
        "bi-specific-paper-prior-art-audit.md", "paper-evidence-universe-and-coverage.md", "layer-A-census-support-geometry.md", "RIME-layer-B-extraction.md",
        "final-SCOPE-C-support-synthesis.md"]
if any(not any(r["file"].endswith(n) for r in fz) for n in need):
    err.append("[1] D043_PAPER_INPUT_FREEZE.csv lacks a required input")
for r in fz:
    if r["commit"] != REV or sha(git(REV, r["file"])) != r["sha256"] or sha(rb(os.path.join(ROOT, r["file"]))) != r["sha256"]:
        err.append(f"[1] frozen input changed: {r['file']}")
# 2
EXPECTED = {"D043_PAPER_INPUT_FREEZE.csv", "PAPER_NUMERIC_CLAIMS.csv", "build_paper_numbers.py", "validate_paper_architecture.py", "__pycache__"}
if any(not (f in EXPECTED or f.endswith(".md")) for f in os.listdir(D)):
    err.append(f"[2] non-architecture files in paper/: {sorted(f for f in os.listdir(D) if not (f in EXPECTED or f.endswith('.md')))}")
for n, l in lines:
    if re.search(r"https?://|\.literature/|doi\.org", l):
        err.append(f"[2] {n}: new source reference: {l[:70]}")
        break
if D == HERE:
    ch = subprocess.run(["git", "-C", ROOT, "diff", "--name-only", REV], capture_output=True, text=True).stdout.split()
    ch += subprocess.run(["git", "-C", ROOT, "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True).stdout.split()
    allowed = ("05_papers/representation_transport/paper/", "09_meta/decision_log/2026-10-19_paper-architecture-and-research-agenda.md", "09_meta/changelog.md")
    bad = [p for p in ch if not p.startswith(allowed)]
    if bad:
        err.append(f"[2] files outside the paper architecture changed since {REV}: {bad[:5]}")
# 3
for n, l in lines:
    if re.search(r"\b(effect size of|reduced employment|increased employment|employment (rose|fell)|positive effect|negative effect|\d+(\.\d+)? ?(percentage points|percent) (more|less|lower|higher))\b", l, re.I) and not NEG.search(l):
        err.append(f"[3] {n}: effect direction / magnitude: {l[:70]}")
if re.search(r"employment_outcomes|outcome_evidence|percent_differential|\"estimate\"", rb(os.path.join(HERE, "build_paper_numbers.py")).decode()):
    err.append("[3] the number builder reads an effect table")
# 4 / 5
if any(p.startswith("H002") for p in os.listdir(os.path.join(ROOT, "09_meta", "hypotheses"))):
    err.append("[4] an H002 record exists")
if not claims.get("N-16", {}).get("value", "").endswith("NOT MET"):
    err.append("[5] N-16 does not carry the NOT MET trigger")
for n, l in lines:
    if "H002" in l and re.search(r"\bMET\b", l) and "NOT MET" not in l:
        err.append(f"[5] {n}: H002 described as MET: {l[:70]}")
    if re.search(r"\bregistered H002\b|H002 (is|was) registered", l) and not NEG.search(l):
        err.append(f"[5] {n}: H002 described as registered: {l[:70]}")
# 6
for n, l in lines:
    if re.search(r"general", l, re.I) and re.search(r"\b(failed|falsified|refuted)\b", l, re.I) and not NEG.search(l):
        err.append(f"[6] {n}: GENERAL labelled failed / falsified: {l[:70]}")
if "infeasible, not falsified" not in DOCS.get("PAPER_CLAIM_MATRIX.md", ""):
    err.append("[6] the primary claim lacks 'infeasible, not falsified'")
# 7
for n, l in lines:
    if re.search(r"P2 — SURVIVES, WEAKENED|P1 — DOWNGRADED|P2 (is )?(downgraded|weakened)", l) and not NEG.search(l):
        err.append(f"[7] {n}: P2 changed: {l[:70]}")
if "P2 — SURVIVES" not in rb(os.path.join(ROOT, "05_papers/representation_transport/final_scope_c/P2_FINAL_SCOPE_C_ASSESSMENT.md")).decode():
    err.append("[7] D043 P2 decision missing")
# 8 / 9 / 10
if claims.get("N-01", {}).get("value") != "43" or fresh["N-01"]["value"] != "43":
    err.append("[8] Layer A denominator is not 43")
if claims.get("N-02", {}).get("value") != "9" or fresh["N-02"]["value"] != "9":
    err.append("[9] Layer B membership is not 9")
for n, t in DOCS.items():
    for m in re.finditer(r"Layer[- ]B([^.\n|]{0,60}?)\bcensus\b", t, re.I):
        if not NEG.search(m.group(1)):
            err.append(f"[9] {n}: Layer B called a census: {m.group(0)[:70]}")
for n, l in lines:
    if re.search(r"\b52\b", l) and not NEG.search(l):
        err.append(f"[10] {n}: 52-study statement: {l[:70]}")
# 11 / 12 / 17
for k, r in fresh.items():
    if k not in claims or claims[k]["value"] != r["value"]:
        err.append(f"[{11 if k in ('N-09', 'N-10', 'N-11', 'N-12') else 12 if k in ('N-13', 'N-14', 'N-15', 'N-16', 'N-17', 'N-18', 'N-22') else 17}] {k} differs from the frozen tables")
sel = DOCS.get("SELECTION_AUDIT_PAPER_ROLE.md", "")
a, b = fresh["N-09"]["value"].split(" vs ")
if f"{a.split('/')[0]} of 7 in the subset vs {b.split('/')[0]} of 43" not in sel:
    err.append("[11] SELECTION_AUDIT_PAPER_ROLE.md does not state the D041 B2 selection numbers")
for d, k in (("withdrawal", "N-03"), ("conditionality", "N-04"), ("cadence", "N-05")):
    if f"{d} {fresh[k]['value'].replace('/', ' / ')}" not in DOCS.get("ABSTRACT_SKELETONS.md", ""):
        err.append(f"[12] abstract skeleton {d} pipeline differs from D041 / D043")
cited = set(re.findall(r"\bN-\d\d\b", "\n".join(DOCS.values())))
if cited - set(claims):
    err.append(f"[17] cited numeric tags without provenance: {sorted(cited - set(claims))}")
rmap = DOCS.get("PAPER_REPRODUCIBILITY_MAP.md", "")
covered = set(re.findall(r"\bN-\d\d\b", rmap))
for x, y in re.findall(r"N-(\d\d) – N-(\d\d)", rmap):
    covered |= {f"N-{i:02d}" for i in range(int(x), int(y) + 1)}
if set(claims) - covered:
    err.append(f"[17] numeric claims missing from the reproducibility map: {sorted(set(claims) - covered)}")
for r in claims.values():
    for f in (r["script"], r["validator"].split(";")[0]):
        if not os.path.exists(os.path.join(ROOT, "05_papers/representation_transport", f)):
            err.append(f"[17] {r['claim_id']}: provenance file missing: {f}")
if D == HERE and subprocess.run([sys.executable, "-I", os.path.join(HERE, "build_paper_numbers.py"), "--check"], capture_output=True).returncode:
    err.append("[17] PAPER_NUMERIC_CLAIMS.csv is not a fresh rebuild")
# 13
rime = DOCS.get("RIME_PAPER_ROLE.md", "")
if "not located in the accessible" not in rime or "accessible record" not in DOCS.get("PAPER_CLAIM_MATRIX.md", "") or "not authorised" not in rime:
    err.append("[13] RIME bounded-access wording missing")
for n, l in lines:
    if re.search(r"RIME", l) and re.search(r"(never|did not|didn't) (report|publish)|(estimate|contrast) (was|is) (absent|missing) from RIME", l):
        err.append(f"[13] {n}: RIME absence asserted beyond the bounded search: {l[:70]}")
# 14
if "N-17" not in DOCS.get("ESTIMAND_SENSITIVITY_PAPER_ROLE.md", "") or "E-B" not in DOCS.get("TABLE_PLAN.md", "") or "N-17" not in DOCS.get("MANUSCRIPT_OUTLINE.md", "") \
        or "N-17" not in DOCS.get("PAPER_CLAIM_MATRIX.md", ""):
    err.append("[14] the E-B sensitivity is not visible in claims / outline / tables")
# 15
nov = DOCS.get("NOVELTY_STATEMENT.md", "")
if not all(s in nov for s in ("Burtless", "Elmore", "D030", "Claims we must not make")):
    err.append("[15] novelty statement does not record the D030 prior art / prohibitions")
for n, l in lines:
    if re.search(r"\b(novel (statistical )?(theory|method|framework)|new (statistical )?theory|(we are|is|are) the first)\b", l, re.I) and not NEG.search(l):
        err.append(f"[15] {n}: novelty overclaim: {l[:70]}")
# 16
ra = {r["architecture_dimension"]: r for r in rd(os.path.join(ROOT, "05_papers/representation_transport/final_scope_c/RESEARCH_AGENDA_GAPS.csv"))}
ag = DOCS.get("ACTIONABLE_RESEARCH_AGENDA.md", "")
for d, title in (("WITHDRAWAL", "Withdrawal"), ("CONDITIONALITY", "Conditionality"), ("CADENCE", "Cadence")):
    if f"## {title} ({ra[d]['current_final_T']}; binding stage {ra[d]['binding_support_stage']})" not in ag:
        err.append(f"[16] agenda heading for {d} does not match the D043 blocker")
if "binding stage" not in ag or "## Duration" not in ag:
    err.append("[16] agenda incomplete")
# 18 / 19 / 20
for n, l in lines:
    if re.search(r"\b(BI|basic income) (works|is effective|does not work|fails|should be adopted)\b", l, re.I) and not (NEG.search(l) or '"' in l or "“" in l):
        err.append(f"[18] {n}: BI effectiveness claim: {l[:70]}")
    if re.search(r"predictive (basic-income |BI )?theory", l, re.I) and not NEG.search(l):
        err.append(f"[19] {n}: predictive theory claimed: {l[:70]}")
    if re.search(r"\b(NHB|Nature Human Behaviour|JPAM|Journal of Policy Analysis|Journal of Economic Surveys|PNAS|Science Advances|American Economic Review|Econometrica|selected journal|target journal)\b", l):
        err.append(f"[20] {n}: journal named / selected: {l[:70]}")

if err:
    print("FAIL")
    for e in err:
        print("  -", e)
    sys.exit(1)
print(f"PASS (D044: {len(fz)} frozen inputs; {len(claims)} numeric claims with provenance; framing B; trigger {fresh['N-16']['value']}; 20 checks)")

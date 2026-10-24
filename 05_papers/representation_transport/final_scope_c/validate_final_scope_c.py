#!/usr/bin/env python3
"""D043: validate the final SCOPE-C support synthesis. Exits 1 on failure.

Checks (D043 section 36):
  1  D041 inputs unchanged (freeze vs a35cd3b)          16 one path supplies V / I / E / U (union rows equal their frozen source rows)
  2  D042 RIME staging unchanged                         17 transport families, not contrasts, establish independence (independent recount)
  3  CODEBOOK_v1.4 unchanged                             18 final H002 trigger recomputed independently and reported consistently
  4  crosswalk v2 unchanged                              19 an H002 file exists only if the trigger is MET
  5  Layer A denominator stays 43                        20 trigger NOT MET -> H002 absent
  6  Layer B frozen membership is exactly 9              21 NOT MET is never described as H002 rejection / falsification / failure
  7  Layer B is never called a census                    22 GENERAL is never labelled failed without a predictive test
  8  no 52-study pooled census denominator               23 P2 decision uses no effect sign (no effect field read; no effect wording)
  9  no Layer-A experiment duplicated via the master map 24 research-agenda rows trace to the final blocker states
  10 RIME is one TF only                                 25 minimum-reporting items map to observed blocker stages
  11 RIME same-G paths: V / I but not strict E / U       26 master-map files byte-identical
  12 MODEL-ONLY RIME TAXDEV does not pass                27 sou-v1 byte-identical
  13 pooled RIME vs control does not pass isolation      28 H001 / R001 unchanged
  14 strict E gate excludes E-B (geometry recomputed)    29 the builder needs no source / network acquisition
  15 usable U requires SE / CI                           30 no participant-level data
Usage: python3 -I validate_final_scope_c.py [--dir D] [--geo G] [--rime R] [--coding C] [--mm M] [--xw X]
"""
import csv
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EUREL = "05_papers/representation_transport/evidence_universe/"
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
D = arg("--dir", HERE)
GEO = arg("--geo", os.path.join(ROOT, EUREL, "layer_a_geometry"))
RIME = arg("--rime", os.path.join(ROOT, EUREL, "layer_b_extraction", "rime"))
COD = arg("--coding", os.path.join(ROOT, "05_papers", "representation_transport", "coding_reliability"))
MM = arg("--mm", os.path.join(ROOT, "02_evidence", "master_map"))
XW = arg("--xw", os.path.join(ROOT, "03_models", "stage4_quantitative_crosswalk_v2.csv"))
REV = "a35cd3b"
err = []
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, "rb").read() if os.path.exists(p) else b""
rd = lambda p: list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []
git = lambda rev, p: subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{p}"], capture_output=True).stdout
gitls = lambda rev, p: subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", rev, p], capture_output=True, text=True).stdout.split()
LOC = {EUREL + "layer_a_geometry/": GEO, EUREL + "layer_b_extraction/rime/": RIME, "02_evidence/master_map/": MM,
       "05_papers/representation_transport/coding_reliability/": COD, "03_models/stage4_quantitative_crosswalk_v2.csv": XW}


def local(p):
    for k, v in LOC.items():
        if p == k:
            return v
        if p.startswith(k):
            return os.path.join(v, p[len(k):])
    return os.path.join(ROOT, p)


T = lambda n: rd(os.path.join(D, n))
UN, GEOM, TL, AUD, RA = T("SCOPE_C_SUPPORT_UNION.csv"), T("SCOPE_C_FINAL_SUPPORT_GEOMETRY.csv"), T("FINAL_SCOPE_C_T_SUPPORT.csv"), T("LAYER_B_SUPPORT_AUDIT.csv"), T("RESEARCH_AGENDA_GAPS.csv")
DOCS = {n: rb(os.path.join(D, n)).decode() for n in sorted(os.listdir(D)) if n.endswith(".md")}
DOCS["D043"] = rb(os.path.join(ROOT, "09_meta", "decision_log", "2026-10-19_final-SCOPE-C-support-synthesis.md")).decode()
CSVTXT = {n: rb(os.path.join(D, n)).decode() for n in sorted(os.listdir(D)) if n.endswith(".csv")}
NEG = re.compile(r"\b(not|never|no|NOT|NEVER|NO|Not|Never|No)\b")
DIMS = ["MAGNITUDE_B2", "WITHDRAWAL", "CONDITIONALITY", "CADENCE", "DURATION", "BASELINE_EMPLOYMENT"]
LAYER_B = {"X001", "X002", "X003", "X004", "X005", "X063", "X066", "X067", "X068"}

# 1 / 2 / 3 / 4
fz = T("D042_FINAL_INPUT_FREEZE.csv")
roles = {r["role"] for r in fz}
if len(fz) < 30 or not {"D041", "D042", "AUTHORITY", "STRATEGIC-MAP"} <= roles:
    err.append("[1] D042_FINAL_INPUT_FREEZE.csv incomplete")
for r in fz:
    if r["commit"] != REV or sha(git(REV, r["file"])) != r["sha256"] or sha(rb(local(r["file"]))) != r["sha256"]:
        err.append(f"[{ {'D041': 1, 'D042': 2}.get(r['role'], 1) }] frozen input changed: {r['file']}")
for p in gitls(REV, EUREL + "layer_a_geometry") + gitls(REV, EUREL + "layer_b_extraction"):
    if "__pycache__" not in p and rb(local(p)) != git(REV, p):
        err.append(f"[{1 if 'layer_a_geometry' in p else 2}] {p} changed since {REV}")
if sha(rb(os.path.join(COD, "CODEBOOK_v1.4.md"))) != "b5364e01b58b1e178982fae501804a304e55d56312c6a023513074f5e21fba6f":
    err.append("[3] CODEBOOK_v1.4 changed")
if rb(XW) != git(REV, "03_models/stage4_quantitative_crosswalk_v2.csv"):
    err.append("[4] crosswalk v2 changed")
# 5 / 6 / 9
man = rd(os.path.join(ROOT, EUREL, "layer_a_reconciliation", "RECONCILED_LAYER_A_MANIFEST.csv"))
la_ids = {m["layer_a_id"] for m in man}
A_ = [u for u in UN if u["scope_layer"] == "A"]
if len(la_ids) != 43 or {u["experiment_id"] for u in A_} != la_ids or len(A_) != 258 or any(g["layer_a_census_denominator"] != "43" for g in GEOM):
    err.append("[5] Layer A denominator is not 43 (manifest / union / geometry)")
frameB = {r["exp_id"] for r in rd(os.path.join(ROOT, EUREL, "universe_frame.csv")) if r["U3_layer"] == "B"}
if frameB != LAYER_B or {a["experiment"] for a in AUD} != LAYER_B or any(g["layer_b_audited_members"] != "9" for g in GEOM):
    err.append("[6] Layer B frozen membership is not exactly the 9 D032 members")
if {u["experiment_id"] for u in UN if u["scope_layer"] == "B"} & la_ids or any(sum(1 for u in A_ if u["experiment_id"] == e) != 6 for e in la_ids):
    err.append("[9] a Layer-A experiment is duplicated (master-map reuse) or a census cell is missing")
# 7 / 8 / 21 / 22
for n, t in list(DOCS.items()) + list(CSVTXT.items()):
    for m in re.finditer(r"Layer[- ]B([^.\n|]{0,60}?)\bcensus\b", t, re.I):
        if not NEG.search(m.group(1)):
            err.append(f"[7] {n}: Layer B called a census: {m.group(0)[:70]}")
    for line in t.splitlines():
        if re.search(r"\b52\b", line) and not NEG.search(line):
            err.append(f"[8] {n}: 52-study pooled statement: {line[:70]}")
        if re.search(r"H002", line) and re.search(r"reject|falsif|\bfail", line, re.I) and not NEG.search(line):
            err.append(f"[21] {n}: H002 described as rejected / falsified / failed: {line[:70]}")
        if re.search(r"general", line, re.I) and re.search(r"\b(failed|falsified)\b", line, re.I) and not NEG.search(line):
            err.append(f"[22] {n}: GENERAL labelled failed: {line[:70]}")
if any(re.search(r"denominator", k) and v.strip() == "52" for g in GEOM for k, v in g.items()):
    err.append("[8] a 52 denominator in the geometry")
st4 = DOCS.get("STAGE4_EMPLOYMENT_STATUS.md", "")
if "UNRESOLVED" not in st4 or "STOPPED AT SUPPORT GATE" not in st4 or "H001 NOT SUPPORTED" not in st4:
    err.append("[22] STAGE4_EMPLOYMENT_STATUS.md lacks the SIMPLE / GENERAL distinction")
# 10-13 / 15 / 16: union rows equal their frozen source rows
grid = {(c["layer_a_id"], c["architecture_dimension"]): c for c in rd(os.path.join(GEO, "LAYER_A_SUPPORT_GRID.csv"))}
pre = {(u["scope_member_id"], u["support_case_ids"]): u for u in rd(os.path.join(GEO, "CURRENT_SCOPE_C_SUPPORT_PRE_RIME.csv")) if u["layer"] == "B" and u["record_type"] == "LAYER-B-MASTER-SUPPORT-ROW"}
rime = {s["support_row_id"]: s for s in rd(os.path.join(RIME, "support_codes.csv"))}
K = ("V", "I", "E", "U", "usable_U", "transport_family_id")
for u in UN:
    if u["scope_layer"] == "A":
        src = grid.get((u["experiment_id"], u["architecture_dimension"]))
    elif u["experiment_id"] == "X002":
        src = rime.get(u["support_case_id"])
    else:
        src = pre.get((u["experiment_id"], u["support_case_id"]))
    if not src or any(u[k] != src[k] for k in K):
        err.append(f"[16] union row differs from its frozen single-path source: {u['experiment_id']} {u['support_case_id']}")
    if (u["usable_U"] == "YES") != (u["U"] in ("SE", "CI")):
        err.append(f"[15] usable_U without SE / CI: {u['experiment_id']} {u['support_case_id']}")
if len([u for u in UN if u["scope_layer"] == "B" and u["experiment_id"] != "X002"]) != len(pre) or len([u for u in UN if u["experiment_id"] == "X002"]) != len(rime):
    err.append("[16] Layer-B paths missing from the union")
rx = [u for u in UN if u["experiment_id"] == "X002"]
if {u["transport_family_id"] for u in rx} != {"LB-TF-X002-RIME"}:
    err.append("[10] RIME is not exactly one transport family")
sameg = [u for u in rx if "W-SAMEG" in u["support_case_id"]]
if len(sameg) != 3 or any((u["V"], u["I"], u["E"], u["U"], u["usable_U"]) != ("Y", "PURE", "NONE", "NONE", "NO") for u in sameg):
    err.append("[11] RIME same-G paths are not V = Y / PURE / E NONE / U NONE")
if any(u["I"] in ("PURE", "CONDITIONABLE-BUNDLE") for u in rx if "TAXDEV" in u["support_case_id"] or "GARDEV" in u["support_case_id"]):
    err.append("[12] RIME response-surface path treated as isolated empirical support")
if any(u["I"] in ("PURE", "CONDITIONABLE-BUNDLE") for u in rx if "POOLED" in u["support_case_id"] or "PLAN-VS-CONTROL" in u["support_case_id"]):
    err.append("[13] RIME pooled / plan vs control passes withdrawal isolation")
# 14 / 17 / 18: independent recomputation (own gate code)
ISO, EA = {"PURE", "CONDITIONABLE-BUNDLE"}, {"E-A", "E-A (caveat)"}
gate = {"v": lambda c: c["V"] == "Y", "i": lambda c: c["V"] == "Y" and c["I"] in ISO,
        "ea": lambda c: c["V"] == "Y" and c["I"] in ISO and c["E"] in EA,
        "eau": lambda c: c["V"] == "Y" and c["I"] in ISO and c["E"] in EA and c["usable_U"] == "YES" and c["U"] in ("SE", "CI"),
        "ext": lambda c: c["V"] == "Y" and c["I"] in ISO and c["E"] in EA | {"E-B"},
        "extu": lambda c: c["V"] == "Y" and c["I"] in ISO and c["E"] in EA | {"E-B"} and c["usable_U"] == "YES"}
fam = lambda cs, f, ind=False: {c["transport_family_id"] for c in cs if f(c) and not (ind and "UNRESOLVED" in c["transport_family_id"])}
rep = [u for u in UN if u["cell_representative"] == "YES"]
if any(sum(1 for u in rep if u["experiment_id"] == "X002" and u["architecture_dimension"] == d) != 1 for d in DIMS):
    err.append("[16] RIME must have exactly one representative path per dimension")
for g in GEOM:
    d = g["architecture_dimension"]
    for layer, cs in (("layer_a", [c for c in rep if c["scope_layer"] == "A" and c["architecture_dimension"] == d]),
                      ("layer_b_audited", [c for c in rep if c["scope_layer"] == "B" and c["architecture_dimension"] == d]),
                      ("scope_c_union", [c for c in rep if c["architecture_dimension"] == d])):
        for col, f in (("families_with_variation", "v"), ("families_isolated", "i"), ("families_isolated_EA", "ea"), ("families_isolated_EA_usableU", "eau")):
            if g.get(f"{layer}_{col}") != str(len(fam(cs, gate[f]))):
                err.append(f"[{14 if 'EA' in col else 17}] {d} {layer}_{col} != independent TF recount")
    us = [c for c in rep if c["architecture_dimension"] == d]
    if g["scope_c_union_families_isolated_EXTENSIVE_usableU"] != str(len(fam(us, gate["extu"]))):
        err.append(f"[17] {d} extensive column != recount")
    if "NOT A CENSUS PREVALENCE" not in g["count_type"] or "SECONDARY" not in g["notes"]:
        err.append(f"[7] {d}: union counts not labelled support-union / not prevalence")
trig = {}
for d in ("WITHDRAWAL", "CONDITIONALITY", "CADENCE", "DURATION"):
    pool = [u for u in UN if u["architecture_dimension"] == d and (d != "DURATION" or u["variation_level"] == "WITHIN-STUDY")]
    trig[d] = fam(pool, gate["eau"], True)
status = "MET" if any(len(v) >= 2 for v in trig.values()) else "NOT MET"
for n in ("FINAL_H002_TRIGGER_ASSESSMENT.md", "FINAL_SCOPE_C_STATUS.md"):
    if f"FINAL SCOPE-C H002 TRIGGER: {status}." not in DOCS.get(n, "") or (status == "NOT MET" and "FINAL SCOPE-C H002 TRIGGER: MET" in DOCS.get(n, "")):
        err.append(f"[18] {n} does not report the recomputed trigger ({status})")
for g in GEOM:
    d = g["architecture_dimension"]
    if d in trig and d != "DURATION" and set(filter(None, g["strict_families"].replace("NONE", "").split(";"))) != trig[d]:
        err.append(f"[18] {d} strict_families != recomputation")
# 19 / 20
h = [p for p in os.listdir(os.path.join(ROOT, "09_meta", "hypotheses")) if p.startswith("H002")]
if status == "MET" and not h:
    err.append("[19] trigger MET but no H002 record")
if status == "NOT MET" and h:
    err.append("[20] H002 record created although the trigger is NOT MET")
# 23
p2 = DOCS.get("P2_FINAL_SCOPE_C_ASSESSMENT.md", "")
if "P2 — SURVIVES" not in p2 and "P2 — SURVIVES, WEAKENED" not in p2 and "P1 — DOWNGRADED" not in p2:
    err.append("[23] P2 decision missing")
if re.search(r"\b(increase[sd]?|decrease[sd]?|reduc(e|ed|es|tion)|positive|negative|significan\w*|harm\w*|benefit(s|ed)? employment)\b", p2, re.I):
    err.append("[23] P2 assessment uses effect-direction wording")
bsrc = rb(os.path.join(HERE, "build_final_scope_c.py")).decode()
if re.search(r"employment_outcomes|outcome_evidence|\[\"estimate\"\]|percent_differential", bsrc):
    err.append("[23] the builder reads an effect field / outcome table")
# 24
gb = {g["architecture_dimension"]: g["primary_blocker"] for g in GEOM}
tl = {t["architecture_dimension"]: t["final_t_support"] for t in TL}
if {r["architecture_dimension"] for r in RA} != set(DIMS):
    err.append("[24] research agenda does not cover the six dimensions")
for r in RA:
    d = r["architecture_dimension"]
    if not r["blocker_trace"] or r["blocker_trace"] != gb.get(d) or r["binding_support_stage"] != gb.get(d, "").split(":")[0].split(" ")[0] or r["current_final_T"] != tl.get(d):
        err.append(f"[24] {d}: agenda row not traceable to the final blocker / T label")
if "RIME" in "".join(r["possible_route"] for r in RA if r["architecture_dimension"] == "WITHDRAWAL") and not all(
        s in next(r["possible_route"] for r in RA if r["architecture_dimension"] == "WITHDRAWAL")
        for s in ("DESIGN SUITABLE IN PRINCIPLE", "DATA / ACCESS ROUTE NOT ESTABLISHED", "REANALYSIS NOT AUTHORISED BY D043")):
    err.append("[24] RIME reanalysis route not marked as required")
# 25
mr = DOCS.get("MINIMUM_REPORTING_FOR_TRANSPORTABLE_BI_EVIDENCE.md", "")
items = re.findall(r"^\| (\d+) \| [^|]+ \| ([^|]+) \| ([^|]+) \|$", mr, re.M)
fail_stages = {"V" if r["strict_gate_stage_reached"] == "NONE" else {"V": "I", "I": "E", "E": "U"}.get(r["strict_gate_stage_reached"], "")
               for n in ("WITHDRAWAL", "CONDITIONALITY", "CADENCE") for r in T(f"{n}_SUPPORT_PATHS_FINAL.csv")}
if len(items) < 11 or "CURRENT transport" not in mr.replace("current transport", "CURRENT transport") or "not** a universal" not in mr:
    err.append("[25] minimum reporting standard incomplete or not scoped to the current programme")
for num, code, basis in items:
    codes = {c.strip() for c in code.split("/")}
    if not codes <= {"V", "I", "E", "U", "B2", "BASELINE"} or not (codes & ({"B2", "BASELINE"} | fail_stages)) or not basis.strip():
        err.append(f"[25] reporting item {num} not mapped to an observed blocker")
# 26 / 27 / 28
for p in gitls(REV, "02_evidence/master_map"):
    if rb(local(p)) != git(REV, p):
        err.append(f"[26] master-map file changed: {p}")
if any(rb(local(p)) != git("3527fad", p) for p in ("02_evidence/master_map/support_incidence.csv", "02_evidence/master_map/evidence_pipeline_matrix.csv")):
    err.append("[26] master map differs from 3527fad")
for p in gitls(REV, "05_papers/state_of_understanding"):
    if rb(os.path.join(ROOT, p)) != git(REV, p):
        err.append(f"[27] sou-v1 file changed: {p}")
for p in ("09_meta/hypotheses/H001_simple-magnitude-vs-nominal-class-employment.md", "09_meta/results/R001_H001-simple-compression-employment.md"):
    if rb(os.path.join(ROOT, p)) != git(REV, p):
        err.append(f"[28] {p} changed")
# 29 / 30
for f in ("build_final_scope_c.py",):
    s = rb(os.path.join(HERE, f)).decode()
    if re.search(r"\b(urllib|requests|socket|http\.client|subprocess)\b|\.literature|https?://", s):
        err.append(f"[29] {f} requires source / network acquisition")
EXPECTED = {"D042_FINAL_INPUT_FREEZE.csv", "SCOPE_C_SUPPORT_UNION.csv", "LAYER_B_SUPPORT_AUDIT.csv", "SCOPE_C_FINAL_SUPPORT_GEOMETRY.csv", "FINAL_SCOPE_C_T_SUPPORT.csv",
            "WITHDRAWAL_SUPPORT_PATHS_FINAL.csv", "CONDITIONALITY_SUPPORT_PATHS_FINAL.csv", "CADENCE_SUPPORT_PATHS_FINAL.csv", "RESEARCH_AGENDA_GAPS.csv",
            "FINAL_H002_TRIGGER_ASSESSMENT.md", "STAGE4_EMPLOYMENT_STATUS.md", "P2_FINAL_SCOPE_C_ASSESSMENT.md", "MINIMUM_REPORTING_FOR_TRANSPORTABLE_BI_EVIDENCE.md",
            "WHAT_WOULD_CHANGE_THE_STATUS.md", "STRICT_VS_EXTENSIVE_GATE_SENSITIVITY.md", "CLAIM_BOUNDARIES.md", "FINAL_SCOPE_C_STATUS.md", "README.md",
            "build_final_scope_c.py", "validate_final_scope_c.py", "__pycache__"}
extra = set(os.listdir(D)) - EXPECTED
if extra:
    err.append(f"[30] unexpected files (possible participant-level data): {sorted(extra)}")
if any(re.search(r"participant_id|person_id|respondent_id|household_id|\bpid\b", t.splitlines()[0] if t else "", re.I) for t in CSVTXT.values()):
    err.append("[30] participant-level identifier column present")
# determinism
if D == HERE:
    p = subprocess.run([sys.executable, "-I", os.path.join(HERE, "build_final_scope_c.py"), "--check"], capture_output=True, text=True)
    if p.returncode:
        err.append("[16] tables differ from a fresh build")

if err:
    print("FAIL")
    for e in err:
        print("  -", e)
    sys.exit(1)
print(f"PASS (D043: Layer A 43 census + Layer B 9 audited (not a census); union {len(UN)} paths; strict families "
      f"{ {k: len(v) for k, v in trig.items()} }; FINAL TRIGGER {status}; H002 unregistered; 30 checks)")

#!/usr/bin/env python3
"""D042: validate the RIME (X002) Layer-B extraction. Exits 1 on failure.

Checks (D042 section 34):
  1  D041_PRE_RIME_FREEZE.csv matches fb9360b and the frozen files are unchanged
  2  CODEBOOK_v1.4 unchanged (sha256) and ACTIVE with verify_commit d595ecf
  3  crosswalk v2 unchanged
  4  Layer-A extraction / reconciliation / geometry files unchanged since fb9360b (only the authorised D042 scope line in the D037 validator)
  5  X002 is the only newly extracted experiment
  6  no non-RIME source family is used for evidence
  7  the full assigned plan matrix is represented (five plans + control, exact S-RIME-01 values)
  8  G and t are separate numeric fields
  9  WITHDRAWAL V = Y only on contrasts with a documented t / earnings-rule difference
  10 PURE only with same G (withdrawal) / same t (magnitude) and no other substantive difference
  11 treatment-vs-control (and pooled-vs-control) is never PURE / CONDITIONABLE-BUNDLE
  12 the contrast graph is a function of the plan matrix only (recomputed) and carries no effect field
  13 E != NONE on a WITHDRAWAL path requires a reported result on that path's own contrast
  14 separate arm-vs-control estimates are never combined into a plan-vs-plan row
  15 the strict employment classes never rest on hours / earnings / income
  16 rules H / I: every E-A / E-B row has a labour-only, definitionally sufficient outcome state
  17 usable_U = YES only with published SE / CI
  18 no SE / CI is derived (none is published in the sources read); support U is paired with its rows
  19 delta B2 for same-G / different-t contrasts is NR (measurement failure), never 0
  20 QS-103 uses the finite promised payment horizon only
  21 sites / arms / paths are not independent transport families; RIME is not merged with another NIT record
  22 no H002 hypothesis record exists
  23 no programme-wide trigger verdict is written
  24 no P2 update is written
  25 master map unchanged
  26 Layer-A geometry files unchanged (D041 freeze)
  27 no microdata outcome reanalysis (no data file, no data-analysis code, microdata source unused)
  28 rule conflicts explicitly registered (RC-06 / RC-07 only; none open; no CODEBOOK_v1.5)
  29 extraction report and decision record carry the terminal status
Usage: python3 -I validate_rime_extraction.py [--dir D] [--coding C] [--mm M] [--geo G] [--rec R] [--stg S] [--xw CROSSWALK]
"""
import csv
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 5))
EU = os.path.join(ROOT, "05_papers", "representation_transport", "evidence_universe")
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
D = arg("--dir", HERE)
COD = arg("--coding", os.path.join(ROOT, "05_papers", "representation_transport", "coding_reliability"))
MM = arg("--mm", os.path.join(ROOT, "02_evidence", "master_map"))
GEO = arg("--geo", os.path.join(EU, "layer_a_geometry"))
REC = arg("--rec", os.path.join(EU, "layer_a_reconciliation"))
STG = arg("--stg", os.path.join(EU, "layer_a_extraction"))
XW = arg("--xw", os.path.join(ROOT, "03_models", "stage4_quantitative_crosswalk_v2.csv"))
sys.path.insert(0, HERE)
import author_rime as A  # noqa: E402

err = []
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, "rb").read() if os.path.exists(p) else b""
rd = lambda n: list(csv.DictReader(open(os.path.join(D, n), newline="", encoding="utf-8"))) if os.path.exists(os.path.join(D, n)) else []
git = lambda rev, p: subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{p}"], capture_output=True).stdout
gitls = lambda rev, p: subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", rev, p], capture_output=True, text=True).stdout.split()
EUREL = "05_papers/representation_transport/evidence_universe/"
LOC = {EUREL + "layer_a_geometry/": GEO, EUREL + "layer_a_reconciliation/": REC, EUREL + "layer_a_extraction/": STG,
       "02_evidence/master_map/": MM, "05_papers/representation_transport/coding_reliability/": COD}


def local(p):
    if p == "03_models/stage4_quantitative_crosswalk_v2.csv":
        return XW
    for k, v in LOC.items():
        if p.startswith(k):
            return os.path.join(v, p[len(k):])
    return os.path.join(ROOT, p)


T = {n: rd(n) for n in ["SOURCE_LOG.csv", "experiment.csv", "arms.csv", "temporal_fields.csv", "contrasts.csv", "employment_outcomes.csv",
                        "outcome_states.csv", "quantitative_summaries.csv", "support_codes.csv", "identity_dependence_review.csv",
                        "source_conflicts.csv", "rule_conflicts.csv"]}
SUP, CON, OUT, ARM = T["support_codes.csv"], T["contrasts.csv"], T["employment_outcomes.csv"], T["arms.csv"]
CONI = {c["contrast_id"]: c for c in CON}
OUTI = {o["outcome_row_id"]: o for o in OUT}
EA, EXT = {"E-A", "E-A (caveat)"}, {"E-A", "E-A (caveat)", "E-B"}
cids = lambda s: [x for x in s["contrast_ids"].split(";") if x and x != "NOT-APPLICABLE"]
oids = lambda s: [x for x in s["outcome_row_ids"].split(";") if x and x != "NOT-APPLICABLE"]
# independently transcribed from S-RIME-01 Table 2 (p. 13) and Table 8 (p. 44): (G % of poverty line, t %)
SR10_PLANS = {(50, 50), (75, 30), (75, 50), (75, 70), (100, 50)}
PUBLISHED_SE_OR_CI = set()  # no SE or CI is printed for any RIME labour result in the sources read (S-RIME-01, -04, -05, -06)

# 1
fz = rd("D041_PRE_RIME_FREEZE.csv")
need = ["2026-10-19_layer-A-census-support-geometry.md", "LAYER_A_SUPPORT_GRID.csv", "LAYER_A_SUPPORT_GEOMETRY.csv", "LAYER_A_BLOCKER_DECOMPOSITION.csv",
        "PRE_CENSUS_MAPPED_LAYER_A_SUBSET_GEOMETRY.csv", "CURRENT_SCOPE_C_SUPPORT_PRE_RIME.csv", "H002_TRIGGER_ASSESSMENT.md", "P2_POST_CENSUS_ASSESSMENT.md",
        "RECONCILED_LAYER_A_MANIFEST.csv", "CODEBOOK_v1.4.md", "stage4_quantitative_crosswalk_v2.csv", "master_map/support_incidence.csv", "evidence_pipeline_matrix.csv"]
if any(not any(r["file"].endswith(n) for r in fz) for n in need):
    err.append("[1] D041_PRE_RIME_FREEZE.csv missing a required file")
for r in fz:
    if r["commit"] != "fb9360b" or sha(git("fb9360b", r["file"])) != r["sha256"] or sha(rb(local(r["file"]))) != r["sha256"]:
        err.append(f"[1] frozen file differs from fb9360b: {r['file']}")
# 2
if sha(rb(os.path.join(COD, "CODEBOOK_v1.4.md"))) != "b5364e01b58b1e178982fae501804a304e55d56312c6a023513074f5e21fba6f":
    err.append("[2] CODEBOOK_v1.4.md changed")
auth = [r for r in csv.DictReader(open(os.path.join(STG, "AUTHORITY_STATUS.csv"), newline="")) if "v1.4" in ",".join(r.values())]
if not auth or not any("ACTIVE" in r.values() and "d595ecf" in r.values() for r in auth):
    err.append("[2] CODEBOOK_v1.4 not ACTIVE with verify_commit d595ecf")
# 3
if rb(XW) != git("fb9360b", "03_models/stage4_quantitative_crosswalk_v2.csv"):
    err.append("[3] crosswalk v2 changed")
# 4
VAL37 = EUREL + "layer_a_extraction/validate_layer_a_extraction.py"
for sub in ("layer_a_extraction", "layer_a_reconciliation", "layer_a_geometry"):
    tracked = [p for p in gitls("fb9360b", EUREL + sub) if "__pycache__" not in p]
    for p in tracked:
        cur, old = rb(local(p)), git("fb9360b", p)
        if p == VAL37:
            allowed = old.replace(b'"layer_a_reconciliation", "layer_a_geometry"]):',
                                  b'"layer_a_reconciliation", "layer_a_geometry", "layer_b_extraction"]):  # D042: authorised RIME Layer-B staging (validated there)')
            if cur != allowed:
                err.append("[4] D037 validator changed beyond the authorised D042 scope line")
        elif cur != old:
            err.append(f"[4] Layer-A file changed since fb9360b: {p}")
    cur_files = {os.path.relpath(os.path.join(r_, f), local(EUREL + sub + "/")) for r_, _, fs in os.walk(local(EUREL + sub + "/")) if "__pycache__" not in r_ for f in fs}
    if cur_files != {p[len(EUREL + sub) + 1:] for p in tracked}:
        err.append(f"[4] files added / removed in {sub}")
# 5
if any(r.get("exp_id") not in ("X002", None) for n, rows in T.items() if n != "SOURCE_LOG.csv" for r in rows):
    err.append("[5] a non-X002 experiment appears in RIME staging")
lbx = os.path.dirname(D)
if os.path.basename(D) == "rime" and sorted(x for x in os.listdir(lbx) if x != "__pycache__") != ["rime"]:
    err.append("[5] layer_b_extraction holds more than the RIME extraction")
if any("X002" in l.split(",")[:1] for l in open(os.path.join(STG, "EXTRACTION_MANIFEST.csv"))):
    err.append("[5] X002 entered the Layer-A manifest")
# 6
src = {r["source_id"]: r for r in T["SOURCE_LOG.csv"]}
used = set()
for n, rows in T.items():
    for r in rows:
        if r.get("estimate") in ("NOT-ACCESSIBLE", "NOT-LOCATED"):
            continue  # explicit missingness rows cite the inaccessible sources they could not use
        for f in ("source_id", "source_ids", "source", "primary_design_source_id", "primary_outcome_source_id"):
            used |= set(re.findall(r"S-[A-Z]+-\d+|S-FRAME-[A-Z]+", r.get(f, "") if n != "SOURCE_LOG.csv" else ""))
for s in sorted(used):
    if s not in src or src[s]["rime_family"] != "YES" or src[s]["used_for_evidence"] != "YES":
        err.append(f"[6] evidence cites a source outside the opened RIME family: {s}")
if any(r["rime_family"] != "YES" and r["used_for_evidence"] != "NO" for r in src.values()):
    err.append("[6] a non-RIME source is marked as used for evidence")
for r in src.values():
    for f in ("source_id", "title", "authors_or_agency", "year", "source_type", "primary_or_secondary", "purpose", "url_or_archive_identifier", "access_status", "pages_or_tables_used", "notes"):
        if f not in r:
            err.append(f"[6] SOURCE_LOG lacks field {f}")
            break
# 7 / 8
plans = [a for a in ARM if a["arm_type"] == "NIT-PLAN"]
try:
    got = {(int(a["guarantee_G"]), int(a["tax_or_withdrawal_rate_t"])) for a in plans}
except ValueError:
    got = None
    err.append("[8] guarantee_G / tax_or_withdrawal_rate_t are not separate numeric fields")
if got != SR10_PLANS or len(plans) != 5 or sum(a["arm_type"] == "CONTROL" for a in ARM) != 1:
    err.append("[7] plan matrix differs from S-RIME-01 Tables 2 / 8 (five plans + control)")
if any(a["plan_id"] != f"X002-P{a['guarantee_G']}-{a['tax_or_withdrawal_rate_t']}" or "S-RIME-01" not in a["source"] for a in plans):
    err.append("[7] plan id / provenance inconsistent with the plan parameters")
if any(not a["duration_or_commitment"].startswith("three years") or "two weeks" not in a["payment_frequency"] for a in plans):
    err.append("[7] plan duration / payment frequency not as documented")
for a in ARM:
    for f in A.ARM_F:
        if f not in a:
            err.append(f"[8] arms.csv lacks {f}")
            break
# 9-11
gt = {a["plan_id"]: (a["guarantee_G"], a["tax_or_withdrawal_rate_t"]) for a in plans}
for s in SUP:
    cs = [CONI.get(c) for c in cids(s)]
    if None in cs:
        err.append(f"[9] {s['support_row_id']} cites an unknown contrast")
        continue
    if s["architecture_dimension"] == "WITHDRAWAL" and s["V"] == "Y":
        for c in cs:
            ok = (c["contrast_class"] in ("C-TREATMENT-VS-CONTROL", "D-POOLED-VS-CONTROL") or c["arm_treatment"].startswith("TAXDEV")
                  or (c["arm_treatment"] in gt and c["arm_reference"] in gt and gt[c["arm_treatment"]][1] != gt[c["arm_reference"]][1]))
            if not ok or "WITHDRAWAL" not in c["C001_diff"]:
                err.append(f"[9] WITHDRAWAL V = Y without a documented t difference: {s['support_row_id']} / {c['contrast_id']}")
    if s["I"] == "PURE":
        for c in cs:
            if c["contrast_class"] in ("C-TREATMENT-VS-CONTROL", "D-POOLED-VS-CONTROL", "M-RESPONSE-SURFACE"):
                err.append(f"[11] {s['support_row_id']}: PURE on a {c['contrast_class']} contrast")
                continue
            same = c["same_G"] if s["architecture_dimension"] == "WITHDRAWAL" else c["same_t"]
            if (same != "Y" or c["arm_treatment"] not in gt or c["arm_reference"] not in gt
                    or (gt[c["arm_treatment"]][0] == gt[c["arm_reference"]][0]) != (c["same_G"] == "Y")
                    or any(not c[f].startswith("0") for f in ("C002_diff", "C005_diff", "C006_diff"))):
                err.append(f"[10] PURE without same G / same t and no other substantive difference: {s['support_row_id']}")
    if s["I"] in ("PURE", "CONDITIONABLE-BUNDLE") and any(c["contrast_class"] in ("C-TREATMENT-VS-CONTROL", "D-POOLED-VS-CONTROL") for c in cs):
        err.append(f"[11] {s['support_row_id']}: treatment-vs-control isolated")
for c in CON:
    if c["contrast_class"] in ("C-TREATMENT-VS-CONTROL", "D-POOLED-VS-CONTROL", "E-DIFF-G-DIFF-T") and "PURE" in c["isolation_candidate"]:
        err.append(f"[11] {c['contrast_id']} is a PURE candidate")
# 12
if [{k: v for k, v in r.items()} for r in A.contrasts(ARM)] != CON:
    err.append("[12] contrasts.csv is not the plan-matrix function (graph not authored from design facts only)")
if any(re.search(r"estimate|effect|signif|stars|_p$|SE$", f, re.I) for f in (CON[0] if CON else {})):
    err.append("[12] contrasts.csv carries an effect field")
src_auth = open(os.path.join(HERE, "author_rime.py"), encoding="utf-8").read()
body = src_auth.split("def contrasts(")[1].split("\nCON = contrasts()")[0]
if re.search(r"\bOUT\b|\bestimate\b|percent_differential|signific", body):
    err.append("[12] the contrast generator references outcome information")
# 13 / 14 / 15 / 16
ost = {r["outcome_row_id"]: r for r in T["outcome_states.csv"]}
for s in SUP:
    if s["E"] == "NONE":
        continue
    rows = [OUTI.get(o) for o in oids(s)]
    if not rows or None in rows:
        err.append(f"[13] {s['support_row_id']}: E = {s['E']} without its outcome rows")
        continue
    for o in rows:
        if o["contrast_id"] not in cids(s):
            err.append(f"[13] {s['support_row_id']}: E taken from another contrast's row ({o['outcome_row_id']})")
        if s["I"] == "MODEL-ONLY":
            if not o["model_based"].startswith("YES"):
                err.append(f"[13] {s['support_row_id']}: model path backed by a non-model row")
        elif not o["direct_contrast_reported"].startswith("YES"):
            err.append(f"[13] {s['support_row_id']}: no direct result for the path's contrast")
        if s["E"] in EA and o["raw_domain_token"] != "EMPLOYMENT-WAGE-WORK-QUARTER":
            err.append(f"[15] {s['support_row_id']}: strict employment class rests on {o['raw_domain_token']}")
        if s["E"] in EXT:
            st = ost.get(o["outcome_row_id"])
            if not st or not st["rule_H_reading"].startswith("LABOUR-ONLY") or not st["rule_I_reading"].startswith("SUFFICIENT") \
                    or re.match(r"(UNKNOWN|AMBIGUOUS|NOT-STATED)", st["state_definition_status"]):
                err.append(f"[16] {s['support_row_id']}: {o['outcome_row_id']} lacks a labour-only, sufficient outcome state")
for o in OUT:
    if o["derived_from_other_rows"] != "NO":
        err.append(f"[14] {o['outcome_row_id']} is derived from other rows")
    c = CONI.get(o["contrast_id"])
    if c and c["contrast_class"] in ("A-SAME-G-DIFF-T", "B-SAME-T-DIFF-G", "E-DIFF-G-DIFF-T"):
        err.append(f"[14] plan-vs-plan result row {o['outcome_row_id']} (none is published; arm-vs-control rows may not be combined)")
    tok = set(o["raw_domain_token"].split(";"))
    if tok & {"HOURS", "EARNINGS", "INCOME", "WAGE-RATE", "FARM-PROFIT", "JOB-SEARCH"} and o["E_class_employment_case"].split(" ")[0] in EXT:
        err.append(f"[15] {o['outcome_row_id']}: hours / earnings classed {o['E_class_employment_case']}")
    if o["E_class_employment_case"].split(" (")[0].split(" object")[0] in EXT and o["outcome_row_id"] not in ost and o["contrast_id"] != "NOT-APPLICABLE":
        err.append(f"[16] {o['outcome_row_id']}: employment-class row without exact outcome states")
# 17 / 18
for s in SUP:
    if (s["usable_U"] == "YES") != (s["U"] in ("SE", "CI")):
        err.append(f"[17] {s['support_row_id']}: usable_U inconsistent with U = {s['U']}")
    if s["U"] in ("SE", "CI") and not set(oids(s)) <= PUBLISHED_SE_OR_CI:
        err.append(f"[17] {s['support_row_id']}: U = {s['U']} without a published SE / CI")
    if s["U"] in ("EXACT-P", "TEST-STAT", "STARS", "VERBAL") and any(OUTI[o]["uncertainty_form"] != s["U"] for o in oids(s) if o in OUTI):
        err.append(f"[18] {s['support_row_id']}: U not paired with its outcome rows")
for o in OUT:
    if any(o[f] != "NR" for f in ("SE", "CI_lower", "CI_upper")) and o["outcome_row_id"] not in PUBLISHED_SE_OR_CI:
        err.append(f"[18] {o['outcome_row_id']}: SE / CI present although none is published (derived uncertainty)")
    if o["uncertainty_form"] in ("SE", "CI") and o["outcome_row_id"] not in PUBLISHED_SE_OR_CI:
        err.append(f"[18] {o['outcome_row_id']}: uncertainty form {o['uncertainty_form']} not published")
# 19 / 20
qs = T["quantitative_summaries.csv"]
for c in CON:
    if c["contrast_class"] == "A-SAME-G-DIFF-T":
        r = [q for q in qs if q["component"] == f"contrast {c['contrast_id']}: delta B2"]
        if len(r) != 1 or r[0]["value"] != "NR" or r[0]["status"] != "NR" or "NOT zero" not in r[0]["note"] or "measurement failure" not in r[0]["note"]:
            err.append(f"[19] delta B2 for {c['contrast_id']} is not NR / measurement failure")
if any(q["qs_id"] == "QS-101" and q["value"] not in ("NR",) for q in qs):
    err.append("[19] a QS-101 value was encoded without its D012 inputs")
q103 = [q for q in qs if q["qs_id"] == "QS-103"]
tmp = [t for t in T["temporal_fields.csv"] if t["plan_id"] in gt]
if len(q103) != 1 or q103[0]["value"] != "3" or q103[0]["unit"] != "years" or "promised" not in q103[0]["component"] \
        or any(t["finite_promised_payment_horizon"] != "3 years" or t["payment_continuation_type"] != "FIXED-TERM" for t in tmp) or len(tmp) != 5:
    err.append("[20] QS-103 not the finite promised payment horizon (3 years, FIXED-TERM, all plans)")
dur = {s["path_id"]: s for s in SUP if s["architecture_dimension"] == "DURATION"}
if dur.get("DUR-WITHIN", {}).get("V") != "N":
    err.append("[20] within-study DURATION must be V = N (all plans three years)")
# 21
tfs = {s["transport_family_id"] for s in SUP} | {e["transport_family_id"] for e in T["experiment.csv"]}
dgs = {s["dependence_group_id"] for s in SUP} | {e["dependence_group_id"] for e in T["experiment.csv"]}
mm_tf = {r["transport_family_id"] for r in csv.DictReader(open(os.path.join(MM, "dependence_groups.csv"), newline=""))}
if len(tfs) != 1 or len(dgs) != 1 or tfs & mm_tf or any(t.startswith("UNRESOLVED") for t in tfs) and not any("UNRESOLVED" in r["relation_status"] for r in T["identity_dependence_review.csv"]):
    err.append(f"[21] RIME paths / sites / arms not one family, or merged with an existing family: {sorted(tfs)}")
idr = {r["related_record"].split(" ")[0]: r["relation_status"] for r in T["identity_dependence_review.csv"]}
if any(idr.get(k) != "DISTINCT" for k in ("X001", "X003", "X004", "X005", "SG11")):
    err.append("[21] identity relation to another NIT record not DISTINCT as documented")
# 22
if any(os.path.basename(p).startswith("H002") for p in os.listdir(os.path.join(ROOT, "09_meta", "hypotheses"))):
    err.append("[22] an H002 hypothesis record exists")
# 23 / 24 / 29
docs = {n: rb(os.path.join(D, n)).decode() for n in ("README.md", "RIME_EXTRACTION_REPORT.md")}
docs["D042"] = rb(os.path.join(ROOT, "09_meta", "decision_log", "2026-10-19_RIME-layer-B-extraction.md")).decode()
for n, t in docs.items():
    if re.search(r"\bMET\b", t):
        err.append(f"[23] {n}: a trigger verdict (MET / NOT MET) is written")
    for line in t.splitlines():
        if re.search(r"\bP2\b", line) and not re.search(r"\bnot\b|\bno\b|unchanged", line, re.I):
            err.append(f"[24] {n}: P2 statement without 'not' / 'unchanged': {line[:80]}")
            break
    if "RIME EXTRACTION COMPLETE — FINAL SCOPE-C SYNTHESIS PENDING" not in t and n != "README.md":
        err.append(f"[29] {n}: terminal status missing")
if sha(git("fb9360b", EUREL + "layer_a_geometry/P2_POST_CENSUS_ASSESSMENT.md")) != sha(rb(os.path.join(GEO, "P2_POST_CENSUS_ASSESSMENT.md"))):
    err.append("[24] P2 assessment changed")
# 25
for p in gitls("fb9360b", "02_evidence/master_map"):
    if rb(local(p)) != git("fb9360b", p):
        err.append(f"[25] master-map file changed: {p}")
if set(os.listdir(MM)) != {os.path.basename(p) for p in gitls("fb9360b", "02_evidence/master_map")}:
    err.append("[25] master-map files added / removed")
if any(rb(local(p)) != git("3527fad", p) for p in ("02_evidence/master_map/support_incidence.csv", "02_evidence/master_map/evidence_pipeline_matrix.csv")):
    err.append("[25] master map differs from 3527fad")
# 26
for r in fz:
    if "layer_a_geometry/" in r["file"] and sha(rb(local(r["file"]))) != r["sha256"]:
        err.append(f"[26] Layer-A geometry file changed: {r['file']}")
# 27
EXPECTED = {"D041_PRE_RIME_FREEZE.csv", "README.md", "RIME_EXTRACTION_REPORT.md", "author_rime.py", "build_rime_staging.py", "validate_rime_extraction.py",
            "__pycache__"} | set(T)
extra = set(os.listdir(D)) - EXPECTED
if extra:
    err.append(f"[27] unexpected files in the RIME staging directory: {sorted(extra)}")
for f in os.listdir(D):
    if f.endswith(".py") and f != "validate_rime_extraction.py":
        s = open(os.path.join(D, f), encoding="utf-8").read()
        if re.search(r"^\s*(import|from)\s+(pandas|numpy|statsmodels|scipy|pyreadstat|sklearn)\b|\.dta\b|\.sav\b|sas7bdat|read_csv\(", s, re.M):
            err.append(f"[27] {f}: data-analysis code present")
if src.get("S-RIME-14", {}).get("used_for_evidence") != "NO" or any("S-RIME-14" in o["source_id"] for o in OUT):
    err.append("[27] RIME microdata used")
# 28
rc = T["rule_conflicts.csv"]
if not rc and not os.path.exists(os.path.join(D, "rule_conflicts.csv")):
    err.append("[28] rule_conflicts.csv missing")
if any(not re.match(r"^(RC-0[67]|CAND-\d\d)$", r["rc_id"]) for r in rc):
    err.append("[28] rule-conflict id outside RC-06 / RC-07 / considered candidates")
open_rc = {r["rc_id"] for r in rc if r["rc_id"].startswith("RC-")}
flagged = any("RULE-CONFLICT" in v for s in SUP for v in s.values())
if flagged != bool(open_rc):
    err.append("[28] RULE-CONFLICT fields and registered RC rows do not match")
if os.path.exists(os.path.join(COD, "CODEBOOK_v1.5.md")):
    err.append("[28] CODEBOOK_v1.5 created")
# determinism
p = subprocess.run([sys.executable, "-I", os.path.join(HERE, "build_rime_staging.py"), "--check"], capture_output=True, text=True)
if D == HERE and p.returncode:
    err.append("[12] staging CSVs differ from a fresh render of author_rime.py")

if err:
    print("FAIL")
    for e in err:
        print("  -", e)
    sys.exit(1)
print(f"PASS (D042: X002 only; 5 plans + control; {len(CON)} contrasts; {len(SUP)} support paths; one dependence group / one transport family; "
      f"no published SE / CI; no rule conflict; 29 checks)")

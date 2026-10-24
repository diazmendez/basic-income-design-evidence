#!/usr/bin/env python3
"""D040: validate the Layer A post-census reconciliation. Exits 1 on failure.

Checks:
  1  FINAL_EXTRACTION_FREEZE_6604b44.csv reproduces every staging row and file hash of 6604b44, and the current staging equals the freeze
     except the registered D040 changes (X054 within-study support rows: I / factual_basis / codebook_version; RC-05 status)
  2  EXTRACTION_MANIFEST.csv byte-identical to 318a581
  3  CODEBOOK_v1 / v1.1 / v1.2 / v1.3 byte-identical to their release commits
  4  CODEBOOK_v1.4 is the deterministic output of build_codebook_v1_4.py and contains rule J
  5  RC-05 RESOLVED BY D040 with its original description preserved
  6  v1_4_reapplication.csv is the deterministic output of its builder and covers every D034 case, master-map support row and
     Layer A Batch 1-6 support row
  7  every I code that differs from its pre-D040 value is registered in v1_4_reapplication.csv with the same new value (staging,
     master map, D034 cases); the X054 within-study rows are BUNDLED
  8  no source re-reading: the re-application cites repository facts only (no .literature path, no unknown source id) and SOURCE_LOG is frozen
  9  every one of the 43 frame members (universe_frame U3_layer = A) appears exactly once in FRAME_RECONCILIATION.csv
  10 PENDING / FRAME-CONFLICT members stay INCLUDED-BY-FROZEN-FRAME and denominator members
  11 the denominator changes only for an established SAME-EXPERIMENT relation between two Layer A members
  12 IR-02 cannot change the denominator (X028 outside Layer A; X028 not a member)
  13 IR-10 cannot change the denominator (X055 outside Layer A; X055 not a member)
  14 IR-09 does not split Apeldoorn / Epe (one member, one dependence group)
  15 every denominator member has a dependence group
  16 every group has a transport family (an UNRESOLVED family states its reason)
  17 one analysis unit per experiment: arms of one experiment never form separate groups or families
  18 no two experiments share a dependence group, and a shared family needs a recorded shared sample / assignment / multi-site
     experiment basis (shared evaluator or statute alone never merges); Participatiewet municipalities are not folded into TF-UTRECHT
  19 the 7 mapped Layer A experiments keep their existing master-map group and family ids
  20 master-map scientific files unchanged since D036 (3527fad)
  21 no aggregate geometry output; the reconciliation directory holds only the expected files; tables are deterministic
  22 no T-level, H002 or P2 update (no T-level field / value, no H002 record, evidence-universe and coverage records unchanged)
  23 sou-v1 unchanged; D040 record and authority lineage (CODEBOOK_v1.4 ACTIVE, v1.3 SUPERSEDED; crosswalk v2 current, no v3)
Usage: python3 -I validate_layer_a_reconciliation.py [--dir RECON_DIR] [--stg STAGING_DIR] [--coding CODING_DIR]
"""
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EU = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(EU, "..", "..", ".."))
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
D = arg("--dir", HERE)
S = arg("--stg", os.path.join(EU, "layer_a_extraction"))
C = arg("--coding", os.path.join(ROOT, "05_papers", "representation_transport", "coding_reliability"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "05_papers", "representation_transport", "coding_reliability"))
import build_layer_a_reconciliation as BR  # noqa: E402
import build_codebook_v1_4 as BC  # noqa: E402
import build_v1_4_reapplication as BJ  # noqa: E402

REL_S = "05_papers/representation_transport/evidence_universe/layer_a_extraction"
REL_C = "05_papers/representation_transport/coding_reliability"
FREEZE = "6604b44"
err = []
sha = lambda b: hashlib.sha256(b).hexdigest()
git = lambda rev, p: subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{p}"], capture_output=True, check=True).stdout
rd = lambda p: list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []
rb = lambda p: open(p, "rb").read() if os.path.exists(p) else b""
rowsha = lambda r: sha(json.dumps(r, sort_keys=True, ensure_ascii=False).encode())
TABLES = ["SOURCE_LOG.csv", "experiments.csv", "arms.csv", "temporal_fields.csv", "contrasts.csv", "employment_outcomes.csv", "outcome_states.csv",
          "quantitative_summaries.csv", "support_codes.csv", "eligibility_identity_review.csv", "identity_relations.csv", "rule_conflicts.csv",
          "EXTRACTION_STATUS.csv"]
REG_SUP = {("X054", "CONDITIONALITY", "WITHIN-STUDY"), ("X054", "WITHDRAWAL", "WITHIN-STUDY")}
REG_FIELDS = {"I", "factual_basis", "codebook_version"}

# 1
fz = rd(os.path.join(S, "FINAL_EXTRACTION_FREEZE_6604b44.csv"))
if not fz:
    err.append("[1] FINAL_EXTRACTION_FREEZE_6604b44.csv missing")
for t in TABLES:
    old = list(csv.DictReader(io.StringIO(git(FREEZE, f"{REL_S}/{t}").decode())))
    fr = [f for f in fz if f["kind"] == "ROW" and f["table"] == t]
    if len(fr) != len(old) or any(f["sha256"] != rowsha(r) for f, r in zip(fr, old)):
        err.append(f"[1] {t}: freeze does not reproduce the 6604b44 rows")
    cur = rd(os.path.join(S, t))
    if len(cur) != len(old):
        err.append(f"[1] {t}: row count changed since the census freeze")
        continue
    for a, b in zip(old, cur):
        diff = {k for k in a if a[k] != b.get(k)}
        if not diff:
            continue
        ok = (t == "support_codes.csv" and (a["exp_id"], a["architecture_dimension"], a["variation_level"]) in REG_SUP and diff <= REG_FIELDS) or \
             (t == "rule_conflicts.csv" and a["rc_id"] == "RC-05" and diff == {"status"})
        if not ok:
            err.append(f"[1] {t} {a.get('exp_id')}: unregistered change to the frozen extraction ({sorted(diff)})")
for f in fz:
    if f["kind"] == "FILE" and sha(git(FREEZE, f["table"])) != f["sha256"]:
        err.append(f"[1] freeze file hash for {f['table']} does not match 6604b44")
# 2
if rb(os.path.join(S, "EXTRACTION_MANIFEST.csv")) != git("318a581", f"{REL_S}/EXTRACTION_MANIFEST.csv"):
    err.append("[2] EXTRACTION_MANIFEST.csv changed since 318a581")
# 3
for f, c in [("CODEBOOK_v1.md", "4fb85a0"), ("CODEBOOK_v1.1.md", "4a2f5d0"), ("CODEBOOK_v1.2.md", "9b61868"), ("CODEBOOK_v1.3.md", "40c0d95")]:
    if rb(os.path.join(C, f)) != git(c, f"{REL_C}/{f}"):
        err.append(f"[3] {f} is not byte-identical to {c}")
# 4
v14 = rb(os.path.join(C, "CODEBOOK_v1.4.md")).decode()
if v14 != BC.build():
    err.append("[4] CODEBOOK_v1.4.md is not the deterministic output of build_codebook_v1_4.py")
for need in ["rule J (D040): research-procedure co-interventions", "material resources or incentives", "substantive behavioural framing",
             "differential research participation / contact exposure", "cannot be separated from the intervention effect", "Rules H, I and J have not been independently blind-second-coded"]:
    if need not in v14:
        err.append(f"[4] CODEBOOK_v1.4.md missing rule-J text: {need!r}")
# 5
rcs = {r["rc_id"]: r for r in rd(os.path.join(S, "rule_conflicts.csv"))}
old_rc = {r["rc_id"]: r for r in csv.DictReader(io.StringIO(git(FREEZE, f"{REL_S}/rule_conflicts.csv").decode()))}
if not rcs.get("RC-05", {}).get("status", "").startswith("RESOLVED BY D040") or rcs.get("RC-05", {}).get("description") != old_rc["RC-05"]["description"]:
    err.append("[5] RC-05 must be RESOLVED BY D040 with its original description")
if any(r["status"].startswith("OPEN") for r in rcs.values()):
    err.append("[5] an open rule conflict remains")
# 6
reap = rd(os.path.join(C, "v1_4_reapplication.csv"))
if not reap or open(os.path.join(C, "v1_4_reapplication.csv"), newline="").read() != BJ.render(BJ.build()):
    err.append("[6] v1_4_reapplication.csv is not the deterministic output of build_v1_4_reapplication.py")
n_mm = len(rd(os.path.join(ROOT, "02_evidence", "master_map", "support_incidence.csv")))
cnt = {k: sum(r["source_layer"] == k for r in reap) for k in ("D034-CASE", "MM-SUPPORT", "LA-SUPPORT")}
if cnt != {"D034-CASE": 25, "MM-SUPPORT": n_mm, "LA-SUPPORT": len(rd(os.path.join(S, "support_codes.csv")))}:
    err.append(f"[6] re-application coverage incomplete: {cnt}")
# 7
reg = {r["case_or_row_id"]: r for r in reap}
old_sup = list(csv.DictReader(io.StringIO(git(FREEZE, f"{REL_S}/support_codes.csv").decode())))
for a, b in zip(old_sup, rd(os.path.join(S, "support_codes.csv"))):
    k = f"{a['exp_id']}-{a['architecture_dimension']}-{a['outcome_domain']}-{a['variation_level']}"
    if a["I"] != b["I"] and (reg.get(k, {}).get("changed") != "YES" or reg[k]["new_I"] != b["I"]):
        err.append(f"[7] {k}: I changed without a registered rule-J re-application row")
    if reg.get(k, {}).get("changed") == "YES" and b["I"] != reg[k]["new_I"]:
        err.append(f"[7] {k}: registered rule-J change not applied")
for r in rd(os.path.join(S, "support_codes.csv")):
    if r["exp_id"] == "X054" and r["variation_level"] == "WITHIN-STUDY" and r["I"] != "BUNDLED":
        err.append(f"[7] X054 {r['architecture_dimension']}: rule J facts require BUNDLED (got {r['I']})")
for r in reap:
    if r["source_layer"] in ("MM-SUPPORT", "D034-CASE") and r["changed"] == "YES":
        err.append(f"[7] {r['case_or_row_id']}: pre-census case changed; downstream implications must be traced in D040 before this passes")
mm_now = rb(os.path.join(ROOT, "02_evidence", "master_map", "support_incidence.csv"))
if mm_now != git("3527fad", "02_evidence/master_map/support_incidence.csv"):
    err.append("[7] master-map support codes changed")
# 8
src_ids = {r["source_id"] for r in rd(os.path.join(S, "SOURCE_LOG.csv"))}
for r in reap:
    if ".literature" in r["factual_basis"] or any(x not in src_ids for x in re.findall(r"S-X\d{3}-\d{2}", r["factual_basis"])):
        err.append(f"[8] {r['case_or_row_id']}: re-application cites something other than stored repository facts")
# 9-14
frame = {r["exp_id"]: r for r in csv.DictReader(io.StringIO(git("318a581", "05_papers/representation_transport/evidence_universe/universe_frame.csv").decode())) if r["U3_layer"] == "A"}
FR = rd(os.path.join(D, "FRAME_RECONCILIATION.csv"))
ids = [r["layer_a_id"] for r in FR]
if sorted(ids) != sorted(frame) or len(ids) != len(set(ids)) or len(frame) != 43:
    err.append(f"[9] FRAME_RECONCILIATION.csv must list the 43 frame members exactly once ({len(ids)} rows)")
IDR = {r["relation_id"]: r for r in rd(os.path.join(D, "IDENTITY_RECONCILIATION.csv"))}
MAN = {r["layer_a_id"]: r for r in rd(os.path.join(D, "RECONCILED_LAYER_A_MANIFEST.csv"))}
AU = rd(os.path.join(D, "ANALYSIS_UNITS.csv"))
for r in FR:
    if r["frame_membership"] != "INCLUDED-BY-FROZEN-FRAME":
        err.append(f"[10] {r['layer_a_id']}: frame membership must stay INCLUDED-BY-FROZEN-FRAME")
    if r["primary_verification_status"] in ("PENDING", "FRAME-CONFLICT") and (r["denominator_status"] != "MEMBER" or MAN.get(r["layer_a_id"], {}).get("denominator_member") != "YES"):
        err.append(f"[10] {r['layer_a_id']}: a verification flag cannot remove a member from the denominator")
for e, st in [("X008", "FRAME-CONFLICT"), ("X051", "PENDING"), ("X052", "FRAME-CONFLICT"), ("X058", "PENDING")]:
    if next((r["primary_verification_status"] for r in FR if r["layer_a_id"] == e), None) != st:
        err.append(f"[10] {e}: verification status must be {st}")
dups = [r for r in IDR.values() if r["relation_status"] == "SAME-EXPERIMENT" and r["a_in_layer_a"] == "YES" and r["b_in_layer_a"] == "YES"]
members = [e for e, r in MAN.items() if r["denominator_member"] == "YES"]
if len(MAN) != 43 or len(members) != 43 - len(dups) or any(r["denominator_status"] != "MEMBER" for r in FR if r["layer_a_id"] not in {d["entity_b"] for d in dups}):
    err.append(f"[11] denominator may change only for established within-Layer-A duplicates ({len(members)} members, {len(dups)} duplicates)")
for r in IDR.values():
    out_side = [x for x in r["entity_b"].split(";") if not x.startswith("UNIT:") and x not in frame]
    if (out_side or r["entity_b"].startswith("UNIT:")) and r["denominator_relevant"] != "NO":
        err.append(f"[11] {r['relation_id']}: a relation with a record outside Layer A cannot be denominator-relevant")
if IDR.get("IR-02", {}).get("denominator_relevant") != "NO" or "X028" in MAN or "X028" in ids:
    err.append("[12] IR-02 / X028 must not change the Layer A denominator")
if IDR.get("IR-10", {}).get("denominator_relevant") != "NO" or "X055" in MAN or "X055" in ids:
    err.append("[13] IR-10 / X055 must not change the Layer A denominator")
x58 = [u for u in AU if u["layer_a_id"].startswith("X058")]
if len(x58) != 1 or not IDR.get("IR-09", {}).get("final_reconciliation", "").startswith("FRAME-UNIT CONSISTENT") or \
        "APELDOORN-EPE" not in x58[0]["transport_family_id"] or \
        any(re.search(r"(?<!APELDOORN-)EPE\b|APELDOORN(?!-EPE)", u["dependence_group_id"] + " " + u["transport_family_id"]) for u in AU):
    err.append("[14] Apeldoorn / Epe must stay one joint experiment (one unit, one group, one family)")
# 15-19
for u in AU:
    if MAN.get(u["layer_a_id"], {}).get("denominator_member") == "YES" and not (u["dependence_group_id"] or "NOT-APPLICABLE" in u["dependence_basis"]):
        err.append(f"[15] {u['layer_a_id']}: no dependence group")
    if not u["transport_family_id"] or ("UNRESOLVED" in u["transport_family_id"] and "cannot be assessed" not in u["transport_family_basis"]):
        err.append(f"[16] {u['layer_a_id']}: transport family missing or unresolved without a reason")
if len(AU) != len({u["layer_a_id"] for u in AU}) or sorted(u["layer_a_id"] for u in AU) != sorted(frame):
    err.append("[17] ANALYSIS_UNITS.csv must hold exactly one unit per Layer A experiment")
arm_ids = {a["arm_id"] for a in rd(os.path.join(S, "arms.csv"))}
if any(any(re.search(rf"{re.escape(a)}(?![A-Za-z0-9])", u["dependence_group_id"] + " " + u["transport_family_id"]) for a in arm_ids) for u in AU):
    err.append("[17] an arm of an experiment forms its own group / family")
by_dg, by_tf = {}, {}
for u in AU:
    by_dg.setdefault(u["dependence_group_id"], []).append(u)
    by_tf.setdefault(u["transport_family_id"], []).append(u)
for g, us in by_dg.items():
    if len(us) > 1:
        err.append(f"[18] dependence group {g} merges separate experiments {[u['layer_a_id'] for u in us]}")
for t, us in by_tf.items():
    if len(us) > 1 and not all(re.search(r"shared sample|shared assignment machinery|common multi-site experiment", u["transport_family_basis"]) for u in us):
        err.append(f"[18] transport family {t} merges experiments {[u['layer_a_id'] for u in us]} without a shared sample / assignment / multi-site basis")
for u in AU:
    if u["layer_a_id"] in ("X053", "X054", "X056", "X057", "X058", "X059", "X061", "X052") and u["transport_family_id"] == "TF-UTRECHT":
        err.append(f"[18] {u['layer_a_id']}: folded into TF-UTRECHT")
mmdg = {r["dependence_group_id"]: r for r in csv.DictReader(io.StringIO(git("3527fad", "02_evidence/master_map/dependence_groups.csv").decode()))}
for e, f in frame.items():
    if f["master_map_groups"]:
        u = next((x for x in AU if x["layer_a_id"] == e), {})
        if u.get("dependence_group_id") != f["master_map_groups"] or u.get("transport_family_id") != mmdg[f["master_map_groups"]]["transport_family_id"]:
            err.append(f"[19] {e}: existing master-map ids {f['master_map_groups']} / {mmdg[f['master_map_groups']]['transport_family_id']} not preserved")
# 20
for n in ["support_incidence.csv", "contrasts.csv", "outcome_evidence.csv", "dependence_groups.csv", "access_and_missingness.csv", "master_evidence_map.csv",
          "architecture_support_matrix.csv", "outcome_coverage_matrix.csv", "evidence_pipeline_matrix.csv", "access_gap_matrix.csv", "summary.md"]:
    if rb(os.path.join(ROOT, "02_evidence", "master_map", n)) != git("3527fad", f"02_evidence/master_map/{n}"):
        err.append(f"[20] master map {n} changed")
# 21
EXPECTED = {"build_layer_a_reconciliation.py", "validate_layer_a_reconciliation.py", "FRAME_RECONCILIATION.csv", "IDENTITY_RECONCILIATION.csv", "ANALYSIS_UNITS.csv",
            "RECONCILED_LAYER_A_MANIFEST.csv", "LAYER_A_DENOMINATOR_LOCK.md", "LAYER_A_RECONCILIATION_COMPLETE.md", "README.md", "__pycache__"}
extra = sorted(set(os.listdir(D)) - EXPECTED)
if extra:
    err.append(f"[21] unexpected files in the reconciliation directory: {extra}")
for base in (D, S):
    for fn in os.listdir(base):
        if re.search(r"aggregat|geometr|support_count|layer_a_counts|pipeline_matrix", fn, re.I):
            err.append(f"[21] aggregate / geometry output found: {fn}")
for n, t in BR.outputs().items():
    if open(os.path.join(D, n), newline="", encoding="utf-8").read() != t if os.path.exists(os.path.join(D, n)) else True:
        err.append(f"[21] {n} is not the deterministic output of build_layer_a_reconciliation.py")
comp = rb(os.path.join(D, "LAYER_A_RECONCILIATION_COMPLETE.md")).decode() + rb(os.path.join(D, "LAYER_A_DENOMINATOR_LOCK.md")).decode()
if re.search(r"\b(PURE|BUNDLED|CONDITIONABLE-BUNDLE|E-A|E-B|E-C|usable_U)\b|\bV\s*=\s*Y\b", comp):
    err.append("[21] reconciliation summaries must not report support codes or counts")
if "RECONCILED — GEOMETRY NOT YET COMPUTED" not in comp or "43" not in comp:
    err.append("[21] completion file must state the final denominator and RECONCILED — GEOMETRY NOT YET COMPUTED")
# 22
for n in ("FRAME_RECONCILIATION.csv", "ANALYSIS_UNITS.csv", "RECONCILED_LAYER_A_MANIFEST.csv", "IDENTITY_RECONCILIATION.csv"):
    for r in rd(os.path.join(D, n)):
        if any(re.search(r"t_level|h002|p2_", k, re.I) for k in r) or any(re.fullmatch(r"T[0-4]", (v or "").strip()) for v in r.values()):
            err.append(f"[22] {n}: T-level / H002 / P2 field or value")
            break
hyp = subprocess.run(["git", "-C", ROOT, "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True).stdout + \
      subprocess.run(["git", "-C", ROOT, "ls-files"], capture_output=True, text=True).stdout
if re.search(r"(^|/)09_meta/hypotheses/H002", hyp, re.M):
    err.append("[22] an H002 record exists")
for p in ("05_papers/representation_transport/EVIDENCE_UNIVERSE_AND_COVERAGE.md", "05_papers/representation_transport/evidence_universe/coverage_metrics.csv",
          "05_papers/representation_transport/evidence_universe/universe_frame.csv"):
    if rb(os.path.join(ROOT, p)) != git(FREEZE, p):
        err.append(f"[22] {p} changed (P2 / SCOPE-C records are not updated in D040)")
# 23
r = subprocess.run(["git", "-C", ROOT, "diff", "--quiet", "65e85dd", "--", "05_papers/state_of_understanding/sou-v1"])
if r.returncode:
    err.append("[23] sou-v1 changed")
d040 = rb(os.path.join(ROOT, "09_meta", "decision_log", "2026-10-19_layer-A-post-census-reconciliation.md")).decode()
if "RECONCILED — GEOMETRY NOT YET COMPUTED" not in d040 or "D040" not in d040:
    err.append("[23] D040 record missing or without its status")
auth = {(a["authority"], a["version"]): a for a in rd(os.path.join(S, "AUTHORITY_STATUS.csv"))}
if auth.get(("codebook", "v1.4"), {}).get("status") != "ACTIVE" or auth.get(("codebook", "v1.3"), {}).get("status") != "SUPERSEDED" or \
        auth.get(("codebook", "v1.4"), {}).get("sha256") != sha(v14.encode()) or auth.get(("crosswalk", "v2"), {}).get("status", "").find("ACTIVE") < 0:
    err.append("[23] authority lineage: CODEBOOK_v1.4 ACTIVE (hash), v1.3 SUPERSEDED, crosswalk v2 ACTIVE")
if os.path.exists(os.path.join(ROOT, "03_models", "stage4_quantitative_crosswalk_v3.csv")):
    err.append("[23] crosswalk v3 must not exist")

if err:
    print("FAIL")
    [print("  -", e) for e in err]
    sys.exit(1)
print(f"PASS (D040: freeze 6604b44 reproduced; CODEBOOK_v1.4 rule J; RC-05 resolved; {len(FR)} frame members; denominator {len(members)}; "
      f"{len(by_dg)} dependence groups; {len(by_tf)} transport families; 23 checks; no geometry)")

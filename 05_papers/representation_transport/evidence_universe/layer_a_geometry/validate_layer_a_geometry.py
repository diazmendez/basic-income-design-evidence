#!/usr/bin/env python3
"""D041: validate the Layer A census support geometry. Exits 1 on failure.

Checks:
  1  D040_RECONCILIATION_FREEZE.csv matches d595ecf and every frozen input is unchanged
  2  RECONCILED_LAYER_A_MANIFEST has exactly 43 denominator members, all analysis-ready
  3  the support grid has exactly 43 x 6 = 258 cells
  4  every Layer A member appears once in every governed dimension
  5  no experiment is dropped for PENDING or FRAME-CONFLICT (X008, X051, X052, X058 present in all six dimensions)
  6  the 7 mapped Layer A experiments are not duplicated (one cell per dimension; one family per experiment)
  7  a cell without a support row is V = N only as DOCUMENTED-NO-VARIATION with a coded basis; otherwise UNKNOWN / DERIVED
  8  a cell that reaches the I gate has ONE support path (one contrast), and a staging path's E / U is backed by an outcome row
     on that same contrast with that uncertainty form
  9  family counts deduplicate arms / contrasts (recomputed independently; one family per experiment)
  10 isolated = PURE or CONDITIONABLE-BUNDLE only
  11 strict gate = E-A / E-A (caveat) only
  12 E-B never passes the strict gate
  13 the EXTENSIVE view includes E-B and is labelled SECONDARY — NOT REGISTERED H002 GATE
  14 usable_U = YES exactly for SE / CI
  15 denominator 43 in every geometry row
  16 the 7-study comparison is exactly the frozen mapped subset (recomputed)
  17 the full strategic-map comparison is labelled non-denominator-comparable
  18 the geometry builder reads no effect value or sign (no outcome / registry table opened, no estimate field)
  19 no aggregate effect statistic is produced (no estimate / effect / mean / SE column in any output)
  20 the unresolved-independence family (X052) cannot satisfy an independent pair
  21 only the six governed dimensions appear
  22 RIME has no extracted support row
  23 H002 = MET only if a strict independent pair exists (recomputed on Layer A and the pre-RIME union)
  24 otherwise the programme-wide status is PENDING-RIME, never NOT MET
  25 no H002 hypothesis record exists
  26 authoritative master-map T-levels unchanged; the D041 T reading reproduces the master's own architecture labels on its scope
  27 master-map scientific files byte-identical to D036
  28 CODEBOOK_v1.4 unchanged
  29 CODEBOOK_v1.4 verify_commit = d595ecf
  30 crosswalk v2 unchanged
  31 sou-v1 unchanged; outputs deterministic; D041 record present
Usage: python3 -I validate_layer_a_geometry.py [--dir GEOM] [--rec REC] [--stg STG] [--mm MM] [--coding CODING]
"""
import csv
import hashlib
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EU = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(EU, "..", "..", ".."))
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
D = arg("--dir", HERE)
REC = arg("--rec", os.path.join(EU, "layer_a_reconciliation"))
STG = arg("--stg", os.path.join(EU, "layer_a_extraction"))
MM = arg("--mm", os.path.join(ROOT, "02_evidence", "master_map"))
COD = arg("--coding", os.path.join(ROOT, "05_papers", "representation_transport", "coding_reliability"))
sys.path.insert(0, HERE)
import build_layer_a_geometry as B  # noqa: E402

err = []
sha = lambda b: hashlib.sha256(b).hexdigest()
git = lambda rev, p: subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{p}"], capture_output=True, check=True).stdout
rb = lambda p: open(p, "rb").read() if os.path.exists(p) else b""
rd = lambda p: list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []
DIMS = ["MAGNITUDE_B2", "WITHDRAWAL", "CONDITIONALITY", "CADENCE", "DURATION", "BASELINE_EMPLOYMENT"]
ISO, EA, EXT = {"PURE", "CONDITIONABLE-BUNDLE"}, {"E-A", "E-A (caveat)"}, {"E-A", "E-A (caveat)", "E-B"}
MAPPED = ["X006", "X007", "X013", "X014", "X016", "X060", "X065"]
LOCMAP = {"layer_a_reconciliation/": REC, "layer_a_extraction/": STG, "02_evidence/master_map/": MM, "coding_reliability/": COD}


def local(p):
    for k, v in LOCMAP.items():
        if k in p:
            return os.path.join(v, p.split(k)[1])
    return os.path.join(ROOT, p)


# 1
fz = rd(os.path.join(D, "D040_RECONCILIATION_FREEZE.csv"))
if len(fz) < 11:
    err.append("[1] D040_RECONCILIATION_FREEZE.csv missing or incomplete")
for f in fz:
    if f["commit"] != "d595ecf" or sha(git("d595ecf", f["file"])) != f["sha256"] or sha(rb(local(f["file"]))) != f["sha256"]:
        err.append(f"[1] frozen input {f['file']} differs from d595ecf")
# 2
man = rd(os.path.join(REC, "RECONCILED_LAYER_A_MANIFEST.csv"))
if len(man) != 43 or any(m["denominator_member"] != "YES" or m["analysis_ready"] != "YES" for m in man):
    err.append("[2] reconciled manifest must hold 43 analysis-ready denominator members")
ids = {m["layer_a_id"] for m in man}
# 3-7
g = rd(os.path.join(D, "LAYER_A_SUPPORT_GRID.csv"))
if len(g) != 258:
    err.append(f"[3] grid has {len(g)} cells, not 258")
for e in sorted(ids):
    for d in DIMS:
        n = sum(c["layer_a_id"] == e and c["architecture_dimension"] == d for c in g)
        if n != 1:
            err.append(f"[4] {e} {d}: {n} cells")
for e in ("X008", "X051", "X052", "X058"):
    if sum(c["layer_a_id"] == e for c in g) != 6:
        err.append(f"[5] {e} dropped from the grid")
for e in MAPPED:
    if len({c["transport_family_id"] for c in g if c["layer_a_id"] == e}) != 1 or sum(c["layer_a_id"] == e for c in g) != 6:
        err.append(f"[6] mapped experiment {e} duplicated")
for c in g:
    if c["support_case_ids"].startswith("NONE"):
        if c["V"] == "N" and (c["cell_status"] != "DOCUMENTED-NO-VARIATION" or not re.search(r"coded|crosswalk|contrast graph", c["cell_basis"])):
            err.append(f"[7] {c['layer_a_id']} {c['architecture_dimension']}: missing support row converted to V = N without a coded basis")
        if c["cell_status"] == "DIRECT-SUPPORT-ROW":
            err.append(f"[7] {c['layer_a_id']} {c['architecture_dimension']}: DIRECT status without a support row")
        if c["cell_status"] == "UNKNOWN-NOT-ESTABLISHED" and (c["V"] != "UNKNOWN" or c["I"] != "NOT-ESTABLISHED"):
            err.append(f"[7] {c['layer_a_id']} {c['architecture_dimension']}: UNKNOWN cell carries codes")
# 8
outs = [{k: r[k] for k in ("contrast_id", "uncertainty_form")} for r in rd(os.path.join(STG, "employment_outcomes.csv"))]  # no estimate column read
for c in g:
    if c["V"] == "Y" and c["I"] in ISO and c["variation_level"] == "WITHIN-STUDY":
        if ";" in c["support_path"] or not re.fullmatch(r"(LA-X\d{3}|C-SG\d+)-C?\d+", c["support_path"]):
            err.append(f"[8] {c['layer_a_id']} {c['architecture_dimension']}: gated cell assembled from several contrasts ({c['support_path']})")
        elif c["source_layer"] == "LA-STAGING" and c["E"] not in ("NONE",) and not any(o["contrast_id"] == c["support_path"] and o["uncertainty_form"] == c["U"] for o in outs):
            err.append(f"[8] {c['layer_a_id']} {c['architecture_dimension']}: E / U not backed by an outcome row on the same contrast {c['support_path']}")
# 9-16 independent recomputation
fam = lambda cs, f, ind=False: {c["transport_family_id"] for c in cs if f(c) and not (ind and "UNRESOLVED" in c["transport_family_id"])}
if len({c["transport_family_id"] for c in g}) != len(ids) or any(len({x["layer_a_id"] for x in g if x["transport_family_id"] == t}) != 1 for t in {c["transport_family_id"] for c in g}):
    err.append("[9] a transport family covers several experiments or an experiment several families")
v_ = lambda c: c["V"] == "Y"
i_ = lambda c: v_(c) and c["I"] in ISO
st = lambda c: i_(c) and c["E"] in EA and c["usable_U"] == "YES"


def recompute(cs, denom):
    rows = []
    for d in DIMS:
        x = [c for c in cs if c["architecture_dimension"] == d]
        rows.append(dict(architecture_dimension=d, denominator_experiments=str(denom), families_with_variation=str(len(fam(x, v_))),
                         families_isolated=str(len(fam(x, i_))), families_isolated_EA=str(len(fam(x, lambda c: i_(c) and c["E"] in EA))),
                         families_isolated_EA_usableU=str(len(fam(x, st))), families_isolated_EXTENSIVE=str(len(fam(x, lambda c: i_(c) and c["E"] in EXT))),
                         families_isolated_EXTENSIVE_usableU=str(len(fam(x, lambda c: i_(c) and c["E"] in EXT and c["usable_U"] == "YES"))),
                         families_between_study_EA_usableU=str(len(fam(x, lambda c: v_(c) and c["variation_level"] == "BETWEEN-STUDY" and c["E"] in EA and c["usable_U"] == "YES"))),
                         families_between_study_EXTENSIVE_usableU=str(len(fam(x, lambda c: v_(c) and c["variation_level"] == "BETWEEN-STUDY" and c["E"] in EXT and c["usable_U"] == "YES"))),
                         independent_strict_discovery_validation_possible="YES" if len(fam(x, st, True)) >= 2 else "NO"))
    return rows


for name, cs, denom, tag in [("LAYER_A_SUPPORT_GEOMETRY.csv", g, 43, "15"), ("PRE_CENSUS_MAPPED_LAYER_A_SUBSET_GEOMETRY.csv", [c for c in g if c["layer_a_id"] in MAPPED], 7, "16")]:
    got = rd(os.path.join(D, name))
    for want, have in zip(recompute(cs, denom), got):
        bad = {k for k in want if have.get(k) != want[k]}
        if bad:
            err.append(f"[{'15' if 'denominator_experiments' in bad else '10-12'}] {name} {want['architecture_dimension']}: {sorted(bad)} differ from an independent recomputation")
    if len(got) != 6:
        err.append(f"[{tag}] {name} must have six rows")
    for r in got:
        if "SECONDARY — NOT REGISTERED H002 GATE" not in r.get("notes", ""):
            err.append(f"[13] {name}: EXTENSIVE columns not labelled SECONDARY — NOT REGISTERED H002 GATE")
if sorted({c["layer_a_id"] for c in g if c["layer_a_id"] in MAPPED}) != MAPPED or \
        sorted(e for e, f in {r["exp_id"]: r for r in csv.DictReader(io.StringIO(git("318a581", "05_papers/representation_transport/evidence_universe/universe_frame.csv").decode()))}.items()
               if f["U3_layer"] == "A" and f["master_map_groups"]) != MAPPED:
    err.append("[16] the comparison subset is not exactly the frozen mapped Layer A subset")
# 14
for c in g:
    if (c["usable_U"] == "YES") != (c["U"] in ("SE", "CI")):
        err.append(f"[14] {c['layer_a_id']} {c['architecture_dimension']}: usable_U must be YES exactly for SE / CI")
# 17
ctx = rb(os.path.join(D, "STRATEGIC_MAP_VS_LAYER_A_CONTEXT.md")).decode()
if "NOT denominator-comparable" not in ctx or "No ratio" not in ctx:
    err.append("[17] strategic-map comparison must be labelled NOT denominator-comparable (no ratio)")
# 18
src = open(os.path.join(HERE, "build_layer_a_geometry.py"), encoding="utf-8").read()
code = re.sub(r'"""[\s\S]*?"""', "", src)
if re.search(r"employment_outcomes|estimand_registry|point_estimate|\[\"estimate\"\]|\bcoef|\bsign\(|verbal_result", code):
    err.append("[18] the geometry builder reads outcome / estimate fields")
# 19
for n in os.listdir(D):
    if n.endswith(".csv"):
        hdr = (rd(os.path.join(D, n)) or [{}])[0].keys()
        if any(re.search(r"estimate|effect|mean|^se$|coefficient|pooled", h, re.I) for h in hdr):
            err.append(f"[19] {n}: an effect-statistic column")
# 20
x52 = [c for c in g if c["layer_a_id"] == "X052"]
if not x52 or not all("UNRESOLVED-INDEPENDENCE" in c["transport_family_id"] for c in x52):
    err.append("[20] X052 must carry its unresolved-independence family")
# 21
if {c["architecture_dimension"] for c in g} != set(DIMS) or any(r["architecture_dimension"] not in DIMS for r in rd(os.path.join(D, "CURRENT_SCOPE_C_SUPPORT_PRE_RIME.csv")) if r["architecture_dimension"] != "NONE"):
    err.append("[21] a non-governed dimension appears")
# 22
un = rd(os.path.join(D, "CURRENT_SCOPE_C_SUPPORT_PRE_RIME.csv"))
rime = [u for u in un if u["scope_member_id"] == "X002"]
if any(c["layer_a_id"] == "X002" for c in g) or len(rime) != 1 or rime[0]["V"] != "NOT-EXTRACTED" or rime[0]["record_type"] != "LAYER-B-MEMBER-NOT-EXTRACTED":
    err.append("[22] RIME must appear once, as NOT-EXTRACTED, with no support codes")
if len({u["scope_member_id"] for u in un if u["layer"] == "A"}) != 43 or any(u["layer"] == "B" and u["scope_member_id"] in ids for u in un):
    err.append("[22] the pre-RIME union must hold each Layer A member once and no Layer B copy of a Layer A experiment")
# 23-25
arch = ("WITHDRAWAL", "CONDITIONALITY", "CADENCE")
pair_A = any(len(fam([c for c in g if c["architecture_dimension"] == d], st, True)) >= 2 for d in arch)
uc = [u for u in un if u["record_type"] != "LAYER-B-MEMBER-NOT-EXTRACTED"]
pair_U = any(len(fam([u for u in uc if u["architecture_dimension"] == d], st, True)) >= 2 for d in arch)
h = rb(os.path.join(D, "H002_TRIGGER_ASSESSMENT.md")).decode()
if pair_A and "Layer A trigger: MET" not in h:
    err.append("[23] a strict independent pair exists but H002 is not MET")
if not pair_A and ("Layer A trigger: NOT MET" not in h or re.search(r"Layer A trigger: MET", h)):
    err.append("[23] H002 must not be MET without a strict independent pair")
if not pair_U and ("Current SCOPE-C trigger: PENDING-RIME" not in h or re.search(r"(Current SCOPE-C|programme-wide)[^.\n]*: NOT MET", h)):
    err.append("[24] programme-wide H002 status must be PENDING-RIME, never NOT MET, while RIME is unextracted")
hyp = subprocess.run(["git", "-C", ROOT, "ls-files", "--cached", "--others", "--exclude-standard"], capture_output=True, text=True).stdout
if re.search(r"(^|/)09_meta/hypotheses/H002", hyp, re.M):
    err.append("[25] an H002 record exists")
# 26-27
for n in ["support_incidence.csv", "contrasts.csv", "outcome_evidence.csv", "dependence_groups.csv", "access_and_missingness.csv", "master_evidence_map.csv",
          "architecture_support_matrix.csv", "outcome_coverage_matrix.csv", "evidence_pipeline_matrix.csv", "access_gap_matrix.csv", "summary.md"]:
    if rb(os.path.join(MM, n)) != git("3527fad", f"02_evidence/master_map/{n}"):
        err.append(f"[27] master map {n} changed")
pipe = {r["architecture_dimension"]: r["current_t_level"] for r in rd(os.path.join(MM, "evidence_pipeline_matrix.csv"))}
if pipe != {"MAGNITUDE_B2": "T3", "WITHDRAWAL": "T1", "CONDITIONALITY": "T2", "CADENCE": "T1", "DURATION": "T2", "BASELINE_EMPLOYMENT": "T0"}:
    err.append("[26] authoritative master-map T-levels changed")
dg = {r["dependence_group_id"]: r for r in rd(os.path.join(MM, "dependence_groups.csv"))}
mcells = [dict(transport_family_id=dg[s["dependence_group_id"]]["transport_family_id"], architecture_dimension=s["architecture_dimension"], V=s["V"], I=s["I"], E=s["E"],
               U=s["U"], usable_U="YES" if s["U"] in ("SE", "CI") else "NO", variation_level=s["variation_level"], layer_a_id=s["dependence_group_id"])
          for s in rd(os.path.join(MM, "support_incidence.csv")) if s["outcome_domain"] == "employment"]
for d in arch:
    if B.t_label(mcells, d)[0] != pipe[d]:
        err.append(f"[26] the D041 T reading does not reproduce the master's own {d} label ({B.t_label(mcells, d)[0]} vs {pipe[d]})")
t = {r["architecture_dimension"]: r for r in rd(os.path.join(D, "T_SUPPORT_LABELS.csv"))}
if any(r["scope_c_status"] != "PROVISIONAL — RIME NOT YET EXTRACTED" for r in t.values()) or any(r["layer_a_t_support"] == "T4" for r in t.values()):
    err.append("[26] SCOPE-C labels must be PROVISIONAL — RIME NOT YET EXTRACTED; no T4 assigned")
for d in arch:
    if t.get(d, {}).get("layer_a_t_support") == "T3" and not len(fam([c for c in g if c["architecture_dimension"] == d], st, True)) >= 2:
        err.append(f"[20] {d}: T3 without an independent strict pair (unresolved families excluded)")
# 28-31
v14 = rb(os.path.join(COD, "CODEBOOK_v1.4.md"))
if sha(v14) != "b5364e01b58b1e178982fae501804a304e55d56312c6a023513074f5e21fba6f":
    err.append("[28] CODEBOOK_v1.4.md changed")
auth = {(a["authority"], a["version"]): a for a in rd(os.path.join(STG, "AUTHORITY_STATUS.csv"))}
if auth.get(("codebook", "v1.4"), {}).get("verify_commit") != "d595ecf" or sha(git("d595ecf", "05_papers/representation_transport/coding_reliability/CODEBOOK_v1.4.md")) != auth[("codebook", "v1.4")]["sha256"]:
    err.append("[29] CODEBOOK_v1.4 verify_commit must be d595ecf and verify")
if rb(os.path.join(ROOT, "03_models", "stage4_quantitative_crosswalk_v2.csv")) != git("3527fad", "03_models/stage4_quantitative_crosswalk_v2.csv"):
    err.append("[30] crosswalk v2 changed")
if subprocess.run(["git", "-C", ROOT, "diff", "--quiet", "65e85dd", "--", "05_papers/state_of_understanding/sou-v1"]).returncode:
    err.append("[31] sou-v1 changed")
for n, txt in B.outputs().items():
    if not os.path.exists(os.path.join(D, n)) or open(os.path.join(D, n), newline="", encoding="utf-8").read() != txt:
        err.append(f"[31] {n} is not the deterministic output of build_layer_a_geometry.py")
d041 = rb(os.path.join(ROOT, "09_meta", "decision_log", "2026-10-19_layer-A-census-support-geometry.md")).decode()
if "D041" not in d041 or "PENDING-RIME" not in d041:
    err.append("[31] D041 record missing")

if err:
    print("FAIL")
    [print("  -", e) for e in err]
    sys.exit(1)
print(f"PASS (D041: 258 cells; denominator 43; strict pair Layer A {'YES' if pair_A else 'NO'}, pre-RIME {'YES' if pair_U else 'NO'}; H002 Layer A "
      f"{'MET' if pair_A else 'NOT MET'}, programme-wide {'MET' if pair_U else 'PENDING-RIME'}; 31 checks)")

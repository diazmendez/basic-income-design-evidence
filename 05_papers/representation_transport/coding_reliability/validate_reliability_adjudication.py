#!/usr/bin/env python3
"""D034: validate the reliability comparison, the adjudication and the master-map update. Exits 1 on failure.

Checks:
  1  second_coder_blind_cases.csv SHA-256 equals the value recorded in the D034 decision record (and the builder)
  2  the returned file is unmodified: structure valid, and identical to the committed copy when one exists
  3  25-case one-to-one join BC001..BC025 <-> frozen support rows
  4  original_code_manifest.json is byte-identical to the D033 commit and its internal checks pass
  5  pre-adjudication metrics / outputs reproduce deterministically (rebuild == files on disk)
  6  disagreement set reproduces deterministically and equals the adjudicated set
  7  every disagreement has an adjudication entry (### BCxxx) in adjudication_log.md with a cause
  8  every final code uses the CODEBOOK_v1.1 vocabulary; usable_U_final consistent with U_final
  9  all 25 cases present in final_adjudicated_codes.csv, rule_version CODEBOOK_v1.1, a note on every case
  10 every original -> final change has a row (with cause and rule) in adjudication_log.md
  11 support_incidence.csv V / I / E / U equal the final adjudicated codes (plus registered later amendments: D036)
  12 derived master-map files are current (validate_master_evidence_map.py check 14)
  13 T-level governance checks pass (validate_master_evidence_map.py, check 8) and T-levels are the pre-D034 ones
  14 no H002 record exists
  15 sou-v1 is unchanged since its release commit
  16 CODEBOOK_v1.md (and the other D033 files) are byte-identical to D033; CODEBOOK_v1.1.md exists
  17 (D038) CODEBOOK_v1.1.md and final_adjudicated_codes.csv byte-identical to D034 (historical v1.1 result); CODEBOOK_v1.2.md
     exists with rule H; v1_2_reapplication.csv registers all 25 cases, old codes = the final v1.1 codes, and any change cites rule H
  18 (D039) CODEBOOK_v1.2.md byte-identical to D038 (9b61868); CODEBOOK_v1.3.md exists with rule I; v1_3_reapplication.csv registers
     all 25 cases with old codes = the final v1.1 codes, and any change cites rule I
Usage: python3 -I validate_reliability_adjudication.py [--dir CODING_DIR] [--sup SUPPORT_INCIDENCE_CSV]
       (--dir / --sup point at mutated copies for mutation tests)
"""
import csv
import glob
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_reliability_adjudication as B  # noqa: E402

D = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else HERE
SUP = (sys.argv[sys.argv.index("--sup") + 1] if "--sup" in sys.argv
       else os.path.join(B.ROOT, "02_evidence", "master_map", "support_incidence.csv"))
P = lambda n: os.path.join(D, n)
D034 = os.path.join(B.ROOT, "09_meta", "decision_log", "2026-10-18_support-coding-reliability-adjudication.md")
SOU_RELEASE = "65e85dd"
T_EXPECTED = {"MAGNITUDE_B2": "T3", "WITHDRAWAL": "T1", "CONDITIONALITY": "T2", "CADENCE": "T1", "DURATION": "T2",
              "BASELINE_EMPLOYMENT": "T0"}
err = []

# 1
rec = re.search(r"SHA-256 \(recorded on receipt[^`]*`([0-9a-f]{64})`", open(D034).read())
got = B.sha(P(B.SECOND_FILE)) if os.path.exists(P(B.SECOND_FILE)) else None
if not rec or got != rec.group(1) or got != B.SECOND_SHA:
    err.append(f"[1] returned-file SHA-256 {got} != recorded {rec.group(1) if rec else None}")
# 2
second, serr, facts = B.load_second(D)
err += [f"[2] {e}" for e in serr]
tracked = subprocess.run(["git", "-C", B.ROOT, "cat-file", "-e", f"HEAD:{B.REL}/{B.SECOND_FILE}"], capture_output=True)
if tracked.returncode == 0 and got != B.sha_bytes(B.git_show("HEAD", f"{B.REL}/{B.SECOND_FILE}")):
    err.append("[2] returned file differs from the committed copy")
# 3, 4
man, merr = B.load_manifest(D)
err += [f"[4] {e}" for e in merr]
if second and sorted(r["blind_case_id"] for r in second) != sorted(man["original_codes"]):
    err.append("[3] join is not one-to-one over BC001..BC025")
# 5, 6 (rebuild in memory from the files under test)
out = None
try:
    out, info = B.build(D)
except SystemExit as e:
    err.append(f"[5/6] rebuild refused: {e}")
if out:
    for n, t in out.items():
        if not os.path.exists(P(n)) or open(P(n)).read() != t:
            err.append(f"[5] {n} is not the deterministic rebuild")
    rows = list(csv.DictReader(io.StringIO(out["reliability_results_pre_adjudication.csv"])))
    dis = [r["blind_case_id"] for r in rows if r["any_primary_disagreement"] == "YES"]
    if dis != B.EXPECTED_DISAGREEMENTS:
        err.append(f"[6] disagreement set {dis} != adjudicated set")
# 7, 10
log = open(P("adjudication_log.md")).read() if os.path.exists(P("adjudication_log.md")) else ""
CAUSES = {"ORIGINAL-CODER-ERROR", "SECOND-CODER-ERROR", "AMBIGUOUS-SOURCE", "AMBIGUOUS-CODEBOOK", "PACKET-OMISSION"}
for bc in B.EXPECTED_DISAGREEMENTS:
    m = re.search(rf"^### {bc} .*?(?=^### |^## )", log, re.M | re.S)
    if not m or not any(c in m.group(0) for c in CAUSES) or "**Factual source:**" not in m.group(0):
        err.append(f"[7] {bc}: no adjudication entry with cause and source")
fin = list(csv.DictReader(open(P("final_adjudicated_codes.csv")))) if os.path.exists(P("final_adjudicated_codes.csv")) else []
oc = man["original_codes"]
for f in fin:
    for v in B.PRIMARY:
        if f.get(f"{v}_final") != oc.get(f["blind_case_id"], {}).get(v):
            if not re.search(rf"^\| {f['blind_case_id']} \| [^|]+ \| {re.escape(v)} \| [^|]+ \| [^|]+ \| "
                             rf"{re.escape(f[v + '_final'])} \| ({'|'.join(CAUSES)}) \| [^|]+ \|$", log, re.M):
                err.append(f"[10] {f['blind_case_id']} {v}: change {oc[f['blind_case_id']][v]} -> {f[v + '_final']} has no logged reason")
# 8, 9
if [f["blind_case_id"] for f in fin] != [f"BC{i:03d}" for i in range(1, 26)]:
    err.append("[9] final_adjudicated_codes.csv must hold BC001..BC025")
for f in fin:
    for v in B.PRIMARY:
        if f[f"{v}_final"] not in B.VOCAB[v]:
            err.append(f"[8] {f['blind_case_id']}: {v}_final {f[v + '_final']!r} not in v1.1 vocabulary")
    if (f["U_final"] in B.USABLE) != (f["usable_U_final"] == "YES"):
        err.append(f"[8] {f['blind_case_id']}: usable_U_final inconsistent with U_final")
    if f["rule_version"] != "CODEBOOK_v1.1" or not f["adjudication_note"].strip():
        err.append(f"[9] {f['blind_case_id']}: rule_version / note missing")
# 11 (later registered amendments by subsequent decisions are applied on top of the D034 final codes)
POST_D034 = {"S-SG12-DURATION-employment": dict(V_final="N", I_final="NOT-APPLICABLE", decision="D036")}
sup = {s["support_row_id"]: s for s in csv.DictReader(open(SUP))}
for f in fin:
    s = sup.get(f["support_row_id"])
    f = {**f, **{k: v for k, v in POST_D034.get(f["support_row_id"], {}).items() if k.endswith("_final")}}
    if not s or (s["V"], s["I"], s["E"], s["U"]) != (f["V_final"], f["I_final"], f["E_final"], f["U_final"]):
        err.append(f"[11] {f['support_row_id']}: support_incidence != final adjudicated codes")
if len(sup) != 25:
    err.append("[11] support_incidence must have 25 rows")
# 12, 13 (live repository)
r = subprocess.run([sys.executable, "-I", os.path.join(B.ROOT, "03_models", "scripts", "validate_master_evidence_map.py")],
                   capture_output=True, text=True)
if r.returncode != 0 or "PASS" not in r.stdout:
    err.append("[12/13] validate_master_evidence_map.py FAILS (derived views or T-level governance): "
               + (r.stdout + r.stderr).strip()[-400:])
for s in sup.values():
    if s["current_t_level_dimension"] != T_EXPECTED[s["architecture_dimension"]]:
        err.append(f"[13] {s['support_row_id']}: T-level changed to {s['current_t_level_dimension']}")
# 14
if glob.glob(os.path.join(B.ROOT, "09_meta", "hypotheses", "H002*")):
    err.append("[14] an H002 record exists; D034 does not authorise it")
# 15
r = subprocess.run(["git", "-C", B.ROOT, "diff", "--quiet", SOU_RELEASE, "--", "05_papers/state_of_understanding/sou-v1"])
u = subprocess.run(["git", "-C", B.ROOT, "ls-files", "--others", "--exclude-standard", "05_papers/state_of_understanding/sou-v1"],
                   capture_output=True, text=True).stdout.strip()
if r.returncode != 0 or u:
    err.append("[15] sou-v1 changed since its release")
# 16
for n in ["CODEBOOK_v1.md", "BLIND_RECODING_PROTOCOL.md", "blind_case_packets.md", "blind_cases.csv", "original_code_manifest.json"]:
    if not os.path.exists(P(n)) or B.sha(P(n)) != B.sha_bytes(B.git_show(B.D033_COMMIT, f"{B.REL}/{n}")):
        err.append(f"[16] {n} is not byte-identical to D033")
if not os.path.exists(P("CODEBOOK_v1.1.md")):
    err.append("[16] CODEBOOK_v1.1.md missing")

# 17
D034_COMMIT = "4a2f5d0"
for n in ["CODEBOOK_v1.1.md", "final_adjudicated_codes.csv"]:
    if not os.path.exists(P(n)) or B.sha(P(n)) != B.sha_bytes(B.git_show(D034_COMMIT, f"{B.REL}/{n}")):
        err.append(f"[17] {n} is not byte-identical to D034 (historical v1.1 result)")
if not os.path.exists(P("CODEBOOK_v1.2.md")) or "employment-domain positive-state rule" not in open(P("CODEBOOK_v1.2.md")).read():
    err.append("[17] CODEBOOK_v1.2.md missing or without rule H")
re12 = {r["case_or_row_id"].split(" ")[0]: r for r in csv.DictReader(open(P("v1_2_reapplication.csv")))
        if r["scope"] == "D034-CASE"} if os.path.exists(P("v1_2_reapplication.csv")) else {}
fin = {r["blind_case_id"]: r for r in csv.DictReader(open(P("final_adjudicated_codes.csv")))} if os.path.exists(P("final_adjudicated_codes.csv")) else {}
if sorted(re12) != [f"BC{i:03d}" for i in range(1, 26)]:
    err.append("[17] v1_2_reapplication.csv must register all 25 D034 cases")
for bc, r in re12.items():
    f = fin.get(bc, {})
    if (r["old_E"], r["old_U"]) != (f.get("E_final"), f.get("U_final")):
        err.append(f"[17] {bc}: re-application old codes differ from the final v1.1 codes")
    if (r["old_E"], r["old_U"]) != (r["new_E"], r["new_U"]) and (r["changed"] != "YES" or "rule H" not in r["rule_basis"]):
        err.append(f"[17] {bc}: unregistered v1.2 change")

# 18
if not os.path.exists(P("CODEBOOK_v1.2.md")) or B.sha(P("CODEBOOK_v1.2.md")) != B.sha_bytes(B.git_show("9b61868", f"{B.REL}/CODEBOOK_v1.2.md")):
    err.append("[18] CODEBOOK_v1.2.md is not byte-identical to D038")
if not os.path.exists(P("CODEBOOK_v1.3.md")) or "outcome-definition sufficiency" not in open(P("CODEBOOK_v1.3.md")).read():
    err.append("[18] CODEBOOK_v1.3.md missing or without rule I")
re13 = {r["case_or_row_id"].split(" ")[0]: r for r in csv.DictReader(open(P("v1_3_reapplication.csv")))
        if r["source_layer"] == "D034-CASE"} if os.path.exists(P("v1_3_reapplication.csv")) else {}
if sorted(re13) != [f"BC{i:03d}" for i in range(1, 26)]:
    err.append("[18] v1_3_reapplication.csv must register all 25 D034 cases")
for bc, r in re13.items():
    f = fin.get(bc, {})
    if (r["old_E"], r["old_U"]) != (f.get("E_final"), f.get("U_final")):
        err.append(f"[18] {bc}: v1.3 re-application old codes differ from the final v1.1 codes")
    if (r["old_E"], r["old_U"]) != (r["new_E"], r["new_U"]) and (r["changed"] != "YES" or "rule I" not in r["rule_basis"]):
        err.append(f"[18] {bc}: unregistered v1.3 change")

if err:
    print("FAIL")
    [print("  -", e) for e in err]
    sys.exit(1)
m = info["met"]
print("PASS (18 checks; returned file %s...; disagreements %d; verdict %s)" % (got[:12], len(B.EXPECTED_DISAGREEMENTS), B.VERDICT))
print("  " + "; ".join(f"{v} {m[v]['agree']}/25 k={B.fmt_k(m[v]['kappa'])}" for v in B.PRIMARY))

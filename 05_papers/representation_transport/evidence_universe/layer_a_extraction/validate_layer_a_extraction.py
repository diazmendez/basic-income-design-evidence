#!/usr/bin/env python3
"""D037: validate the Layer A STAGING extraction (Batches 1-6, final; D038 and D039 re-applications). Exits 1 on failure.

Checks:
  1  EXTRACTION_MANIFEST.csv byte-identical to commit 318a581; 36 rows; frozen order and six-batch assignment; all NOT-STARTED
  2  EXTRACTION_STATUS.csv marks every manifest experiment extracted in its own batch (BATCH-n-EXTRACTED, n = 1-6); none NOT-STARTED
  3  only the 36 frozen manifest candidates have staging rows (no X055 Oss, no non-manifest experiment, no RIME / X002)
  4  every extracted experiment has a source log with a design-source attempt and an outcome-source attempt
  5  every field of every staging table is populated (a value or an explicit missingness token); no blank cells
  6  typed temporal fields obey D036: continuation vocabulary; a finite horizon only with FIXED-END; NO-FIXED-END -> QS-103 NA;
     QS-103 equals the treatment arm's finite promised payment horizon; no finite horizon on a no-transfer arm
  7  support codes use the CODEBOOK_v1.2 vocabulary (RULE-CONFLICT in E / U only with an OPEN registered rule conflict for that
     experiment and field in rule_conflicts.csv, described in the batch report);
     usable_U = YES only for SE / CI; outcome rows use the U vocabulary
  8  no T-level column or value anywhere in staging
  9  every referenced source_id exists in SOURCE_LOG.csv
  10 staging tables are the deterministic output of build_layer_a_staging.py (batch author files)
  11 master-map canonical and derived tables unchanged from D036 (3527fad)
  12 crosswalk v1 and v2 unchanged from D036; sou-v1 unchanged since its release commit
  13 (D038) CODEBOOK_v1 / v1.1 byte-identical to D033 / D034; CODEBOOK_v1.2 exists and contains rule H; RC-01 marked resolved
     (D038 record, D037 record, batch report); AUTHORITY_STATUS.csv: manifest hashes = frozen manifest, active hashes = current
     files, protocol at 318a581 = manifest hash, amended protocol carries the D038 positive-state section
  14 (D038) X015 employment support E = NONE, U = NONE, usable_U = NO; every pre-D038 raw outcome fact (definition, estimate,
     SE / CI / exact p / test statistic, sample, provenance) preserved; only registered mixed rows relabelled
     MIXED-LABOUR-NONLABOUR-STATUS; no mixed raw row feeds an E-A / E-B support code
  15 (D038) v1_2_reapplication.csv is the deterministic output of build_v1_2_reapplication.py; it covers all 25 D034 cases, every
     master-map support / outcome row and every Batch 1 staging support / outcome row; current codes equal its new codes (no
     unregistered change); every changed row cites rule H; no Batch 2-6 experiment appears in it (D038 scope = Batch 1 rows)
  16 (Batch 2) every Batch-1 row of every cumulative table is unchanged from commit 9b61868 (same rows, same order, same values)
     and matches the BATCH_01_FREEZE.csv row hashes
  17 (Batch 2) completeness: every Batch-2 experiment has an experiment row, >= 2 arms, typed temporal fields for every arm,
     >= 1 contrast, >= 1 outcome row, QS-101 / QS-103 / QS-105 components, the three cross-study support rows and an
     eligibility row with an allowed status (VERIFIED / FRAME-CONFLICT / PENDING)
  18 (Batch 2, rule H) every Batch-2 outcome row has an outcome_states.csv row with explicit positive and negative states
     (a value or an explicit UNKNOWN); MIXED states <-> outcome_domain MIXED-LABOUR-NONLABOUR-STATUS; an E-A / E-A (caveat) /
     E-B support code needs a LABOUR-state outcome row of that experiment with a reported estimate / test / result statement
  19 (Batch 2) the Denver equal-total payment-profile contrast is recorded as PAYMENT-PROFILE with identical monthly spacing and
     is not coded CADENCE (no CADENCE anywhere for X035 in contrasts or support codes)
  20 (Batch 2) the X034 CLIMB <-> SG15 identity relation is recorded with an allowed status (DISTINCT /
     SAME-EXPERIMENT-CANDIDATE / UNCLEAR); no merge (X034 keeps its own rows; no staging row for SG15)
  21 support dimensions are only the governed six; RULE-CONFLICT values anywhere (support codes, quantitative summaries) are
     registered as OPEN in rule_conflicts.csv; RC-01 is RESOLVED BY D038
  22 no aggregate geometry: the staging directory holds only the expected files, and no aggregate / geometry output exists
     under evidence_universe/
  23 (D039) CODEBOOK_v1.2 byte-identical to 9b61868; CODEBOOK_v1.3 contains rule I; RC-02 / RC-03 / RC-04 RESOLVED BY D039
     (rule_conflicts.csv, batch_02_report.md, D037 and D039 records); X030 and X034 employment support E NONE / U NONE / usable_U NO;
     raw X030 mixed / label-only rows and the raw X034 'significantly more likely to be employed' statement present;
     no RULE-CONFLICT value remains in support codes or quantitative summaries
  24 (D039, RC-04) X033 B2: numerator and derived B2 NR as MEASUREMENT FAILURE unless a flagged D012 realised-mean substitute
     exists; never a schedule value ($2,400 / $3,600 / $4,800), equal weight, midpoint or mode; X033 MAGNITUDE_B2 V UNKNOWN /
     I NOT-ISOLATED; X033 employment E-A (caveat) / SE / usable_U YES intact
  25 (D039) v1_3_reapplication.csv is the deterministic output of build_v1_3_reapplication.py; it covers all D034 cases, master-map
     rows and Batch 1-2 staging rows; current codes and raw domains equal its new values (no unregistered change); every change cites
     rule I; EMPLOYMENT-DEFINITION-UNRESOLVED only on rows whose recorded positive state is UNKNOWN / AMBIGUOUS / NOT-STATED
  26 (D039) every Batch-2 row is unchanged from d1428de except the fields D039 may change (raw outcome domain; support E / U /
     usable_U / basis / codebook version; X033 QS-101 value / status / note; rule-conflict status); no raw number changed
  27 (Batch 3) every Batch-2 row matches BATCH_02_FREEZE.csv (row hashes frozen after D039, before any Batch 3 source); active
     authority rows (CODEBOOK_v1.3, post-D039 protocol) verify against commit 40c0d95
  28 (Batch 3) Batch-3 completeness (as check 17); exact states (as check 18); support U = NONE whenever E = NONE; QS-101
     numerators never built from equal weights / midpoint / mode / a representative unit; the In Her Hands (X039) equal-total
     B-vs-A contrast is PAYMENT-PROFILE and never CADENCE; X039 <-> X028 identity relation recorded with an allowed status;
     no staging row for X028 (not merged / altered)
  29 (Batch 4) every Batch-3 row matches BATCH_03_FREEZE.csv (row hashes frozen before any Batch 4 source); Batch 1 and Batch 2 freezes
     re-checked by checks 16 and 27
  30 (Batch 4) completeness (checks 17-18 extended to Batch 4; X045 may add within-study rows); support U = NONE when E = NONE; the
     promised horizons of extended pilots (X046, X047) are the promised 1.0, not the realised period; X045 Newark: the architecture comes
     from X045 primary sources (the recurring-vs-lump-sum contrast cites S-X045 sources, not the frame); a CADENCE row needs differing
     event spacing in the arms and the contrast; payment profile is recorded in the contrast and is never a support dimension; a DURATION
     within-study row needs differing arm-level finite promised horizons; the direct arm-arm employment case is E NONE / U NONE unless an
     arm-arm employment row with reported inference exists, and no arm-arm SE / CI may appear without a published arm-arm result; the
     B2 numerator is the common $6,000 per year
  31 (Batch 5) every Batch-4 row matches BATCH_04_FREEZE.csv (row hashes frozen before any Batch 5 source); Batches 1-3 re-checked by
     checks 16, 27 and 29
  32 (Batch 5) Participatiewet: QS-103 never a finite number or the experiment window; X053 QS-103 NA (NO-FIXED-END) with exemption
     intervals typed as C006; contrast-level B2 = 0 only with documented cash-rule equality (C001 and C002 both 0); no study-level B2 = 0
     when a contrast changes the disregard; WITHDRAWAL needs a documented benefit-vs-earnings rule difference between arms; no PURE
     within-study isolation; no direct arm-arm employment inference where none is reported; UNCLEAR randomisation never VERIFIED; Batch-5
     rows carry no Batch-6 municipality result; U NONE when E NONE
  33 (Batch 6) every Batch-5 row matches BATCH_05_FREEZE.csv (row hashes frozen before any Batch 6 source); Batches 1-4 re-checked by
     checks 16, 27, 29 and 31; X051 stays PENDING and X052 FRAME-CONFLICT (no silent change without a reconciliation record)
  34 (Batch 6) Participatiewet rules for X054-X061: every arm NO-FIXED-END / NA and QS-103 NA (experiment windows never QS-103); exemption
     intervals typed as C006; WITHDRAWAL needs a documented benefit-vs-earnings rule difference ('WITHDRAWAL rule differs') and >= 2 distinct
     arm C001 rules; contrast B2 = 0 only with C001 and C002 both 0 and a design-zero note; no study-level B2 = 0 when a contrast changes
     the disregard; a direct arm-arm outcome row needs direct_contrast_reported YES, is never derived from arm-control rows and never carries
     an SE / CI; PURE only where the contrast's documented differences leave only the focal dimension (no co-treatment class B); I =
     RULE-CONFLICT only with an OPEN RC for that experiment and field; municipality rows separate (each Batch-6 row cites only its own
     S-<exp> sources); shared-source rows name the municipality-specific provenance; no transport-family / dependence-group assignment
  35 (final) all 36 manifest candidates processed; LAYER_A_EXTRACTION_COMPLETION.md reports 36 / 36 and says reconciliation is pending, no
     denominator reconciliation, no aggregate geometry and no master-map integration, and holds no support counts; D037 record and README
     carry EXTRACTION COMPLETE - RECONCILIATION PENDING; RIME (X002, Layer B) untouched: no staging row, evidence_universe files and the
     frame / coverage tables unchanged since 318a581
Usage: python3 -I validate_layer_a_extraction.py [--dir STAGING_DIR] [--mm MASTER_MAP_DIR] [--coding CODING_DIR]
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
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
import author_layer_a_batch_01 as A  # noqa: E402
import author_layer_a_batch_02 as A2  # noqa: E402
import build_layer_a_staging as BLD  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "05_papers", "representation_transport", "coding_reliability"))
import build_v1_2_reapplication as RA  # noqa: E402
import build_v1_3_reapplication as RB  # noqa: E402

D = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else HERE
MM = sys.argv[sys.argv.index("--mm") + 1] if "--mm" in sys.argv else os.path.join(ROOT, "02_evidence", "master_map")
CD = sys.argv[sys.argv.index("--coding") + 1] if "--coding" in sys.argv else os.path.dirname(RA.__file__)
REL = os.path.relpath(HERE, ROOT)
CREL = "05_papers/representation_transport/coding_reliability"
D033_COMMIT, D034_COMMIT, PRE_D038_COMMIT, D038_COMMIT, PRE_D039_COMMIT = "4fb85a0", "4a2f5d0", "6184e5a", "9b61868", "d1428de"
MANIFEST_COMMIT, D036_COMMIT, SOU_COMMIT = "318a581", "3527fad", "65e85dd"
ORDER = ["X008", "X015", "X021", "X025", "X026", "X029", "X030", "X031", "X032", "X033", "X034", "X035", "X036", "X037", "X038",
         "X039", "X040", "X041", "X042", "X043", "X044", "X045", "X046", "X047", "X048", "X049", "X050", "X051", "X052", "X053",
         "X054", "X056", "X057", "X058", "X059", "X061"]
BATCH1 = ORDER[:6]
BATCH2 = ORDER[6:12]
BATCH3 = ORDER[12:18]
BATCH4 = ORDER[18:24]
BATCH5 = ORDER[24:30]
BATCH6 = ORDER[30:36]
DONE = BATCH1 + BATCH2 + BATCH3 + BATCH4 + BATCH5 + BATCH6
LATER = BATCH2 + BATCH3 + BATCH4 + BATCH5 + BATCH6
DIMS = {"MAGNITUDE_B2", "WITHDRAWAL", "CONDITIONALITY", "CADENCE", "DURATION", "BASELINE_EMPLOYMENT"}
TOKENS = {"NR", "NA", "NOT-APPLICABLE", "UNKNOWN", "NOT-LOCATED", "INACCESSIBLE", "RULE-CONFLICT"}
V_C = {"Y", "N", "UNKNOWN"}
I_C = {"PURE", "CONDITIONABLE-BUNDLE", "BUNDLED", "NOT-ISOLATED", "MODEL-ONLY", "NOT-APPLICABLE"}
E_C = {"E-A", "E-A (caveat)", "E-B", "E-C", "NONE", "NOT-APPLICABLE"}
U_C = {"SE", "CI", "EXACT-P", "TEST-STAT", "P-CATEGORY", "STARS", "VERBAL", "NONE", "NOT-INTEGRATED", "MODEL-ONLY"}
CONT = {"FIXED-END", "NO-FIXED-END", "CONDITIONAL-RENEWAL", "NR", "NOT-APPLICABLE"}
TABLES = list(BLD.CUMULATIVE) + list(BLD.FROM_BATCH2)
err = []
sha = lambda b: hashlib.sha256(b).hexdigest()
git = lambda rev, p: subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{p}"], capture_output=True, check=True).stdout
P = lambda n: os.path.join(D, n)
rd = lambda n: list(csv.DictReader(open(P(n), newline=""))) if os.path.exists(P(n)) else []

# 1
mb = open(P("EXTRACTION_MANIFEST.csv"), "rb").read()
if mb != git(MANIFEST_COMMIT, f"{REL}/EXTRACTION_MANIFEST.csv"):
    err.append("[1] EXTRACTION_MANIFEST.csv differs from commit 318a581 (frozen; never regenerate)")
man = list(csv.DictReader(io.StringIO(mb.decode())))
if [m["exp_id"] for m in man] != ORDER or any(int(m["batch"]) != i // 6 + 1 for i, m in enumerate(man)):
    err.append("[1] manifest order / batch assignment differs from the frozen D037 order")
if any(m["extraction_status"] != "NOT-STARTED" for m in man):
    err.append("[1] manifest statuses must stay NOT-STARTED (status lives in EXTRACTION_STATUS.csv)")
# 2
st = rd("EXTRACTION_STATUS.csv")
if [s["exp_id"] for s in st] != ORDER:
    err.append("[2] EXTRACTION_STATUS.csv must list the 36 manifest experiments in order")
if sorted(s["exp_id"] for s in st if s["extraction_status"] == "BATCH-1-EXTRACTED") != sorted(BATCH1) or \
        sorted(s["exp_id"] for s in st if s["extraction_status"] == "BATCH-2-EXTRACTED") != sorted(BATCH2) or \
        sorted(s["exp_id"] for s in st if s["extraction_status"] == "BATCH-3-EXTRACTED") != sorted(BATCH3) or \
        sorted(s["exp_id"] for s in st if s["extraction_status"] == "BATCH-4-EXTRACTED") != sorted(BATCH4) or \
        sorted(s["exp_id"] for s in st if s["extraction_status"] == "BATCH-5-EXTRACTED") != sorted(BATCH5) or \
        sorted(s["exp_id"] for s in st if s["extraction_status"] == "BATCH-6-EXTRACTED") != sorted(BATCH6) or \
        any(s["extraction_status"] == "NOT-STARTED" for s in st):
    err.append("[2] every manifest experiment must be marked extracted in its own batch (Batches 1-6); none NOT-STARTED")
# 3, 5, 8
tabs = {n: rd(n) for n in TABLES}
for n, rows in tabs.items():
    if not rows:
        err.append(f"[5] {n} missing or empty")
    for r in rows:
        e = r.get("exp_id", "")
        if e not in DONE and not (n == "SOURCE_LOG.csv" and e == "FRAME"):
            err.append(f"[3] {n}: row for {e}, which is not a frozen manifest candidate")
        for k, v in r.items():
            if v is None or not v.strip():
                err.append(f"[5] {n}: blank field {k} ({e})")
            if v and re.fullmatch(r"T[0-4]", v.strip()):
                err.append(f"[8] {n}: T-level value in field {k} ({e})")
    if rows and any(re.search(r"t_level|transport_support|t-level", k, re.I) for k in rows[0]):
        err.append(f"[8] {n}: T-level column present")
# 4
src = {s["source_id"]: s for s in tabs["SOURCE_LOG.csv"]}
for e in DONE:
    ss = [s for s in src.values() if s["exp_id"] == e]
    if not any(s["design_used"] == "YES" for s in ss):
        err.append(f"[4] {e}: no design-source attempt")
    if not any(s["outcome_used"] == "YES" or s["access_status"] in ("NOT-LOCATED", "INACCESSIBLE") for s in ss):
        err.append(f"[4] {e}: no outcome-source attempt")
    if not any(s["primary_or_secondary"] == "PRIMARY" and s["access_status"] == "ACCESSED" for s in ss):
        err.append(f"[4] {e}: no accessed primary source")
# 6
qs103 = {q["exp_id"]: q for q in tabs["quantitative_summaries.csv"] if q["qs_id"] == "QS-103"}
arms = {a["arm_id"]: a for a in tabs["arms.csv"]}
for t in tabs["temporal_fields.csv"]:
    c, h = t["payment_continuation_type"], t["finite_promised_payment_horizon"]
    if c not in CONT:
        err.append(f"[6] {t['arm_id']}: continuation type {c!r}")
    num = re.fullmatch(r"\d+(\.\d+)?", h) is not None
    if num and c != "FIXED-END":
        err.append(f"[6] {t['arm_id']}: finite horizon {h} without FIXED-END continuation")
    if c == "FIXED-END" and not num:
        err.append(f"[6] {t['arm_id']}: FIXED-END without a numeric finite horizon")
    if c == "NO-FIXED-END" and h != "NA":
        err.append(f"[6] {t['arm_id']}: NO-FIXED-END must carry horizon NA")
    if arms.get(t["arm_id"], {}).get("cash_amount_rule", "").startswith("NOT-APPLICABLE") and (num or c not in ("NOT-APPLICABLE",)):
        err.append(f"[6] {t['arm_id']}: payment horizon on a no-transfer arm")
    if re.search(r"-T\d*$", t["arm_id"]):
        q = qs103.get(t["exp_id"], {})
        want = {"FIXED-END": (h, "OBSERVED"), "NO-FIXED-END": ("NA", "NA"), "NR": ("NR", "NR")}.get(c)
        if want and (q.get("value"), q.get("status")) != want:
            err.append(f"[6] {t['exp_id']}: QS-103 {q.get('value')}/{q.get('status')} inconsistent with typed temporal fields ({c}, {h})")
for e, q in qs103.items():
    if re.search(r"exemption|follow-up|trial duration|work requirement|service", q["note"], re.I) and q["status"] in ("OBSERVED", "DERIVED"):
        err.append(f"[6] {e}: QS-103 derived from a non-C002 period")
# 7
RJ = list(csv.DictReader(open(os.path.join(CD, "v1_4_reapplication.csv"), newline=""))) if os.path.exists(os.path.join(CD, "v1_4_reapplication.csv")) else []
RJ_CHANGED = {r["case_or_row_id"]: r for r in RJ if r["source_layer"] == "LA-SUPPORT" and r["changed"] == "YES"}  # D040 rule-J re-application
reports = "".join(open(P(n)).read() for n in ("batch_01_report.md", "batch_02_report.md", "batch_03_report.md", "batch_04_report.md", "batch_05_report.md", "batch_06_report.md") if os.path.exists(P(n)))
rcs = rd("rule_conflicts.csv")
open_rc = lambda e, f: [r for r in rcs if r["exp_id"] == e and r["status"].startswith("OPEN") and f in r["field"].split(";")]
for s in tabs["support_codes.csv"]:
    if s["V"] not in V_C or (s["I"] not in I_C and s["I"] != "RULE-CONFLICT") or (s["U"] not in U_C and s["U"] != "RULE-CONFLICT") or (s["E"] not in E_C and s["E"] != "RULE-CONFLICT"):
        err.append(f"[7] {s['exp_id']} {s['architecture_dimension']}: code outside the CODEBOOK_v1.2 vocabulary")
    for f in ("I", "E", "U"):
        if s[f] == "RULE-CONFLICT":
            reg = open_rc(s["exp_id"], f)
            if not reg or not all(re.search(rf"{r['rc_id']}\b[^\n]*{s['exp_id']}", reports) for r in reg):
                err.append(f"[7] {s['exp_id']}: {f} = RULE-CONFLICT without an OPEN registered rule conflict (rule_conflicts.csv + batch report)")
    if (s["usable_U"] == "YES") != (s["U"] in ("SE", "CI")):
        err.append(f"[7] {s['exp_id']} {s['architecture_dimension']}: usable_U must be YES only for SE / CI")
    if s["codebook_version"] != ("CODEBOOK_v1.2" if s["exp_id"] in BATCH1 else ("CODEBOOK_v1.4" if f"{s['exp_id']}-{s['architecture_dimension']}-{s['outcome_domain']}-{s['variation_level']}" in RJ_CHANGED else "CODEBOOK_v1.3")) or s["outcome_domain"] != "employment":
        err.append(f"[7] {s['exp_id']}: codebook version / domain")
for o in tabs["employment_outcomes.csv"]:
    if o["uncertainty_form"] not in U_C:
        err.append(f"[7] {o['outcome_row_id']}: uncertainty_form {o['uncertainty_form']!r}")
    if o["uncertainty_form"] in ("SE", "CI") and o["SE"] in TOKENS and o["CI_lower"] in TOKENS:
        err.append(f"[7] {o['outcome_row_id']}: usable uncertainty claimed without a published SE / CI")
# 9
ids = set(src)
for n in ("experiments.csv", "arms.csv", "temporal_fields.csv", "contrasts.csv", "employment_outcomes.csv",
          "quantitative_summaries.csv", "support_codes.csv", "eligibility_identity_review.csv", "outcome_states.csv",
          "identity_relations.csv"):
    for r in tabs[n]:
        for f in ("source_id", "source_ids", "primary_design_source_id", "primary_outcome_source_id", "state_source_ids"):
            for x in re.split(r"[;\s]+", r.get(f, "") or ""):
                if x and x.startswith("S-") and x not in ids:
                    err.append(f"[9] {n}: unknown source {x}")
# 10
for n, text in BLD.render(manifest_path=P("EXTRACTION_MANIFEST.csv")).items():
    if not os.path.exists(P(n)) or open(P(n), newline="").read() != text:
        err.append(f"[10] {n} is not the deterministic output of build_layer_a_staging.py")
# 11, 12
for n in ["support_incidence.csv", "contrasts.csv", "outcome_evidence.csv", "dependence_groups.csv", "access_and_missingness.csv",
          "master_evidence_map.csv", "architecture_support_matrix.csv", "outcome_coverage_matrix.csv",
          "evidence_pipeline_matrix.csv", "access_gap_matrix.csv", "summary.md"]:
    p = os.path.join(MM, n)
    if not os.path.exists(p) or open(p, "rb").read() != git(D036_COMMIT, f"02_evidence/master_map/{n}"):
        err.append(f"[11] master map {n} changed since D036")
for p in ["03_models/stage4_quantitative_crosswalk_v1.csv", "03_models/stage4_quantitative_crosswalk_v1.md",
          "03_models/stage4_quantitative_crosswalk_v2.csv", "03_models/stage4_quantitative_crosswalk_v2.md"]:
    if open(os.path.join(ROOT, p), "rb").read() != git(D036_COMMIT, p):
        err.append(f"[12] {p} changed since D036")
r = subprocess.run(["git", "-C", ROOT, "diff", "--quiet", SOU_COMMIT, "--", "05_papers/state_of_understanding/sou-v1"])
u = subprocess.run(["git", "-C", ROOT, "ls-files", "--others", "--exclude-standard", "05_papers/state_of_understanding/sou-v1"],
                   capture_output=True, text=True).stdout.strip()
if r.returncode or u:
    err.append("[12] sou-v1 changed")
# 13
cp = lambda n: os.path.join(CD, n)
rb = lambda p: open(p, "rb").read() if os.path.exists(p) else b""
if rb(cp("CODEBOOK_v1.md")) != git(D033_COMMIT, f"{CREL}/CODEBOOK_v1.md"):
    err.append("[13] CODEBOOK_v1.md is not byte-identical to D033")
if rb(cp("CODEBOOK_v1.1.md")) != git(D034_COMMIT, f"{CREL}/CODEBOOK_v1.1.md") or sha(rb(cp("CODEBOOK_v1.1.md"))) != man[0]["codebook_v1_1_sha256"]:
    err.append("[13] CODEBOOK_v1.1.md is not byte-identical to D034 / the manifest hash")
cb12 = rb(cp("CODEBOOK_v1.2.md")).decode()
for need in ["employment-domain positive-state rule", "entirely a labour-market extensive-margin object", "Source labels do not override",
             "E = NONE, U = NONE, usable_U = NO", "MIXED-LABOUR-NONLABOUR-STATUS", "NONE vs NOT-APPLICABLE", "has not been independently second-coded"]:
    if need not in cb12:
        err.append(f"[13] CODEBOOK_v1.2.md missing rule-H text: {need!r}")
d038 = os.path.join(ROOT, "09_meta", "decision_log", "2026-10-18_mixed-status-outcome-semantics.md")
d037 = os.path.join(ROOT, "09_meta", "decision_log", "2026-10-18_layer-A-census-extraction.md")
for path, label in [(d038, "D038 record"), (d037, "D037 record"), (P("batch_01_report.md"), "batch report"), (P("README.md"), "README")]:
    if not re.search(r"RC-01[^\n]*RESOLVED BY D038", rb(path).decode()):
        err.append(f"[13] {label}: RC-01 not marked RESOLVED BY D038")
auth = rd("AUTHORITY_STATUS.csv")
mcol = {"universe_frame": "universe_frame_sha256", "codebook": "codebook_v1_1_sha256", "crosswalk": "crosswalk_v2_sha256",
        "layer_a_protocol": "layer_a_protocol_sha256"}
if {a["authority"] for a in auth} != set(mcol) or any(len([a for a in auth if a["authority"] == k and "ACTIVE" in a["status"]]) != 1 for k in mcol):
    err.append("[13] AUTHORITY_STATUS.csv must list the four authorities, each with exactly one ACTIVE version")
apath = lambda a: os.path.join(CD, os.path.basename(a["path"])) if a["authority"] == "codebook" else os.path.join(ROOT, a["path"])
for a in auth:
    if "MANIFEST-FROZEN" in a["status"] and a["sha256"] != man[0][mcol.get(a["authority"], "")]:
        err.append(f"[13] AUTHORITY_STATUS {a['authority']} {a['version']}: manifest-era hash differs from the frozen manifest")
    if "ACTIVE" in a["status"] and sha(rb(apath(a))) != a["sha256"]:
        err.append(f"[13] AUTHORITY_STATUS {a['authority']} {a['version']}: active hash differs from the current file")
    if a["verify_commit"] != "WORKING-TREE" and sha(git(a["verify_commit"], a["path"])) != a["sha256"]:
        err.append(f"[13] AUTHORITY_STATUS {a['authority']} {a['version']}: hash does not match the file at {a['verify_commit']}")
act = {a["authority"]: a for a in auth if "ACTIVE" in a["status"]}
if act.get("codebook", {}).get("version") != "v1.4" or act.get("layer_a_protocol", {}).get("version") != "post-D039":
    err.append("[13] active authorities must be CODEBOOK_v1.4 (D040) and the post-D039 protocol")
proto = "05_papers/representation_transport/evidence_universe/LAYER_A_EXTRACTION_PROTOCOL.md"
if sha(git(MANIFEST_COMMIT, proto)) != man[0]["layer_a_protocol_sha256"]:
    err.append("[13] protocol at 318a581 does not match the manifest hash")
pt = rb(os.path.join(ROOT, proto)).decode()
if "exact positive and negative states" not in pt or "CODEBOOK_v1.2" not in pt or "Do not rely on labels" not in pt:
    err.append("[13] LAYER_A_EXTRACTION_PROTOCOL.md lacks the D038 positive-state amendment")
if "CODEBOOK_v1.3" not in pt or "EMPLOYMENT-DEFINITION-UNRESOLVED" not in pt or "measurement failure" not in pt or "never** use arbitrary equal weights" not in pt.replace("**Never** use", "never** use"):
    err.append("[13] LAYER_A_EXTRACTION_PROTOCOL.md lacks the D039 amendments (rule I; B2 heterogeneous schedules)")
# 14
for s in tabs["support_codes.csv"]:
    if s["exp_id"] == "X015" and (s["E"], s["U"], s["usable_U"]) != ("NONE", "NONE", "NO"):
        err.append(f"[14] X015 {s['architecture_dimension']}: must be E NONE / U NONE / usable_U NO under CODEBOOK_v1.2 (D038)")
reap = list(csv.DictReader(open(cp("v1_2_reapplication.csv"), newline=""))) if os.path.exists(cp("v1_2_reapplication.csv")) else []
mixed_ids = {r["case_or_row_id"] for r in reap if r["scope"] == "STAGING-OUTCOME" and r["new_outcome_domain"] == RA.MIXED_TOKEN}
pre = {o["outcome_row_id"]: o for o in csv.DictReader(io.StringIO(git(PRE_D038_COMMIT, f"{REL}/employment_outcomes.csv").decode()))}
cur = {o["outcome_row_id"]: o for o in tabs["employment_outcomes.csv"]}
FACT = [f for f in A.OUT_F if f not in ("outcome_domain", "notes")]
for rid, o in pre.items():
    c = cur.get(rid)
    if c is None or any(c[f] != o[f] for f in FACT):
        err.append(f"[14] {rid}: pre-D038 raw outcome fact removed or altered")
    elif c["outcome_domain"] != (RA.MIXED_TOKEN if rid in mixed_ids else o["outcome_domain"]):
        err.append(f"[14] {rid}: outcome domain {c['outcome_domain']!r} not as registered in v1_2_reapplication.csv")
if not mixed_ids or any(cur.get(r, {}).get("exp_id") != "X015" for r in mixed_ids):
    err.append("[14] the registered mixed raw rows must be X015 rows present in the outcome table")
for s in tabs["support_codes.csv"]:
    mine = [o for o in cur.values() if o["exp_id"] == s["exp_id"]]
    if s["E"] in ("E-A", "E-A (caveat)", "E-B") and mine and all(o["outcome_domain"] == RA.MIXED_TOKEN or o["uncertainty_form"] == "NONE" for o in mine):
        err.append(f"[14] {s['exp_id']} {s['architecture_dimension']}: E-A / E-B code with only mixed or descriptive raw rows")
# 15
if not reap or open(cp("v1_2_reapplication.csv"), newline="").read() != RA.render(RA.build()):
    err.append("[15] v1_2_reapplication.csv is not the deterministic output of build_v1_2_reapplication.py")
by = {}
for r in reap:
    by.setdefault(r["scope"], {})[r["case_or_row_id"]] = r
fin = list(csv.DictReader(open(cp("final_adjudicated_codes.csv"), newline="")))
mm_sup = list(csv.DictReader(open(os.path.join(MM, "support_incidence.csv"), newline="")))
mm_out = list(csv.DictReader(open(os.path.join(MM, "outcome_evidence.csv"), newline="")))
want = {"D034-CASE": {f"{c['blind_case_id']} ({c['support_row_id']})": (c["E_final"], c["U_final"]) for c in fin},
        "MM-SUPPORT": {s["support_row_id"]: (s["E"], s["U"]) for s in mm_sup},
        "MM-OUTCOME": {o["evidence_row_id"]: (o["compatibility_class"], o["uncertainty_status"]) for o in mm_out},
        "STAGING-SUPPORT": {f"{s['exp_id']}-{s['architecture_dimension']}-{s['outcome_domain']}": (s["E"], s["U"]) for s in tabs["support_codes.csv"] if s["exp_id"] in BATCH1},
        "STAGING-OUTCOME": {o["outcome_row_id"]: ("NOT-CODED (raw factual row)", o["uncertainty_form"]) for o in tabs["employment_outcomes.csv"] if o["exp_id"] in BATCH1}}
if len(want["D034-CASE"]) != 25:
    err.append("[15] final_adjudicated_codes.csv must hold the 25 D034 cases")
for sc, ids in want.items():
    got_ids = set(by.get(sc, {}))
    if got_ids != set(ids):
        err.append(f"[15] {sc}: re-application does not cover exactly the current rows ({len(got_ids ^ set(ids))} differ)")
    for rid, codes in ids.items():
        r = by.get(sc, {}).get(rid)
        if r and (r["new_E"], r["new_U"]) != codes:
            err.append(f"[15] {sc} {rid}: current codes {codes} differ from the registered v1.2 codes (unregistered change)")
for r in reap:
    if r["changed"] == "YES" and "rule H" not in r["rule_basis"]:
        err.append(f"[15] {r['case_or_row_id']}: changed without a rule-H basis")
    if r["changed"] != ("YES" if (r["old_E"], r["old_U"], r["old_outcome_domain"]) != (r["new_E"], r["new_U"], r["new_outcome_domain"]) else "NO"):
        err.append(f"[15] {r['case_or_row_id']}: 'changed' flag inconsistent")
    if any(x in r["case_or_row_id"] for x in ORDER[6:]):
        err.append(f"[15] {r['case_or_row_id']}: Batch 2-6 experiment in the re-application")
# 16
for n in BLD.CUMULATIVE:
    old = list(csv.DictReader(io.StringIO(git(D038_COMMIT, f"{REL}/{n}").decode())))
    new = [r for r in tabs[n] if r["exp_id"] in BATCH1 or r["exp_id"] == "FRAME"]
    if old != new:
        err.append(f"[16] {n}: a Batch-1 row changed, moved or disappeared since 9b61868")
for f in rd("BATCH_01_FREEZE.csv"):
    rows = tabs.get(f["table"], [])
    i = int(f["batch1_row_index"])
    if i >= len(rows) or sha(json.dumps(rows[i], sort_keys=True, ensure_ascii=False).encode()) != f["row_sha256"]:
        err.append(f"[16] {f['table']} row {i} ({f['exp_id']}) differs from BATCH_01_FREEZE.csv")
# 17
ELIG = {"VERIFIED", "FRAME-CONFLICT", "PENDING"}
for e in LATER:
    by = lambda n: [r for r in tabs[n] if r["exp_id"] == e]
    arms_e = by("arms.csv")
    if len(by("experiments.csv")) != 1 or len(arms_e) < 2 or not by("contrasts.csv") or not by("employment_outcomes.csv"):
        err.append(f"[17] {e}: experiment / arms / contrasts / outcome rows incomplete")
    if {a["arm_id"] for a in arms_e} != {t["arm_id"] for t in by("temporal_fields.csv")}:
        err.append(f"[17] {e}: typed temporal fields missing for an arm")
    if sorted(q["qs_id"] for q in by("quantitative_summaries.csv") if not q["component"].startswith("contrast ")) != ["QS-101"] * 3 + ["QS-103", "QS-105"]:
        err.append(f"[17] {e}: quantitative-summary components incomplete")
    if sorted(s["architecture_dimension"] for s in by("support_codes.csv") if s["variation_level"] == "BETWEEN-STUDY") != sorted(["MAGNITUDE_B2", "DURATION", "BASELINE_EMPLOYMENT"]) or \
            (e not in ("X045", "X053", "X054", "X056", "X057", "X059") and any(s["variation_level"] != "BETWEEN-STUDY" for s in by("support_codes.csv"))):
        err.append(f"[17] {e}: cross-study support rows incomplete")
    el = by("eligibility_identity_review.csv")
    ex = by("experiments.csv")
    if len(el) != 1 or el[0]["layer_A_eligibility"] not in ELIG or (ex and ex[0]["layer_A_eligibility"] != el[0]["layer_A_eligibility"]):
        err.append(f"[17] {e}: eligibility status missing / not allowed / inconsistent")
# 18
states = {r["outcome_row_id"]: r for r in tabs["outcome_states.csv"]}
HREAD = ("LABOUR", "MIXED", "UNKNOWN", "NOT-APPLICABLE")
b2out = [o for o in tabs["employment_outcomes.csv"] if o["exp_id"] in LATER]
if set(states) != {o["outcome_row_id"] for o in b2out}:
    err.append("[18] outcome_states.csv must cover exactly the Batch-2 to Batch-6 outcome rows")
for o in b2out:
    st_ = states.get(o["outcome_row_id"])
    if not st_:
        continue
    for f in ("positive_states", "negative_states"):
        if not st_[f].strip() or st_[f].strip().lower() in ("none", "nr", "n/a"):
            err.append(f"[18] {o['outcome_row_id']}: {f} must be explicit (a state list or UNKNOWN)")
    if not st_["rule_H_reading"].startswith(HREAD):
        err.append(f"[18] {o['outcome_row_id']}: rule_H_reading {st_['rule_H_reading']!r}")
    if (st_["rule_H_reading"] == "MIXED") != (o["outcome_domain"] == RA.MIXED_TOKEN):
        err.append(f"[18] {o['outcome_row_id']}: MIXED states and the MIXED-LABOUR-NONLABOUR-STATUS domain must coincide (rule H)")
    if st_["rule_H_reading"] == "UNKNOWN" and not st_["positive_states"].startswith("UNKNOWN"):
        err.append(f"[18] {o['outcome_row_id']}: UNKNOWN rule-H reading needs an explicit UNKNOWN positive state")
    unk = bool(RB.UNKNOWN_STATE.match(st_["positive_states"])) and st_["rule_H_reading"] != "MIXED"
    if unk != (o["outcome_domain"] == RB.UNRES):
        err.append(f"[18] {o['outcome_row_id']}: an unknown positive state and the EMPLOYMENT-DEFINITION-UNRESOLVED domain must coincide (rule I)")
for s in tabs["support_codes.csv"]:
    if s["exp_id"] in LATER and s["E"] in ("E-A", "E-A (caveat)", "E-B"):
        ok = [o for o in b2out if o["exp_id"] == s["exp_id"] and states.get(o["outcome_row_id"], {}).get("rule_H_reading") == "LABOUR"
              and o["uncertainty_form"] != "NONE"]
        if not ok:
            err.append(f"[18] {s['exp_id']} {s['architecture_dimension']}: {s['E']} without a LABOUR-state reported estimate / test / statement (rule H)")
# 19
den_c = [c for c in tabs["contrasts.csv"] if c["exp_id"] == "X035"]
prof = [c for c in den_c if c["treatment_arm"] == "X035-T2" and c["reference_arm"] == "X035-T1"]
if not prof or "PAYMENT-PROFILE" not in prof[0]["C002_diff"] or "SAME monthly event spacing" not in prof[0]["C002_diff"]:
    err.append("[19] X035: the equal-total B-vs-A contrast must be recorded as PAYMENT-PROFILE with identical monthly spacing")
if any(re.search(r"CADENCE", c["C002_diff"] + c["focal_architecture_dimensions"].replace("not CADENCE", "")) for c in den_c) or \
        any(s["exp_id"] == "X035" and s["architecture_dimension"] == "CADENCE" for s in tabs["support_codes.csv"]):
    err.append("[19] X035: front-loading coded as CADENCE without spacing variation")
# 20
idr = [r for r in tabs["identity_relations.csv"] if r["exp_id"] == "X034" and r["related_record"].startswith("SG15")]
if len(idr) != 1 or idr[0]["relation_status"] not in ("DISTINCT", "SAME-EXPERIMENT-CANDIDATE", "UNCLEAR"):
    err.append("[20] X034: identity relation to SG15 missing or status not DISTINCT / SAME-EXPERIMENT-CANDIDATE / UNCLEAR")
if any(r.get("exp_id") == "SG15" for n in TABLES for r in tabs[n]) or \
        any(re.search(r"\bmerged? (with|into) SG15", " ".join(r.values()), re.I) for n in TABLES for r in tabs[n]) or \
        not [r for r in tabs["experiments.csv"] if r["exp_id"] == "X034"]:
    err.append("[20] X034 merged with SG15 (or X034 rows missing)")
# 21
for s in tabs["support_codes.csv"]:
    if s["architecture_dimension"] not in DIMS:
        err.append(f"[21] {s['exp_id']}: unregistered support dimension {s['architecture_dimension']!r}")
for q in tabs["quantitative_summaries.csv"]:
    if q["value"] == "RULE-CONFLICT" and not [r for r in rcs if r["exp_id"] == q["exp_id"] and r["status"].startswith("OPEN") and q["qs_id"] in r["field"]]:
        err.append(f"[21] {q['exp_id']} {q['qs_id']}: RULE-CONFLICT value without an OPEN registered rule conflict")
rc1 = [r for r in rcs if r["rc_id"] == "RC-01"]
if not rc1 or not rc1[0]["status"].startswith("RESOLVED BY D038"):
    err.append("[21] RC-01 must be registered as RESOLVED BY D038")
for r in rcs:
    if r["status"].startswith("OPEN") and not re.search(rf"{r['rc_id']}\b[^\n]*{r['exp_id']}", reports):
        err.append(f"[21] {r['rc_id']}: not described in the batch report")
# 22
EXPECTED = {"README.md", "EXTRACTION_MANIFEST.csv", "EXTRACTION_STATUS.csv", "AUTHORITY_STATUS.csv", "BATCH_01_FREEZE.csv", "BATCH_02_FREEZE.csv", "BATCH_03_FREEZE.csv", "BATCH_04_FREEZE.csv", "BATCH_05_FREEZE.csv", "FINAL_EXTRACTION_FREEZE_6604b44.csv",
            "author_layer_a_batch_01.py", "author_layer_a_batch_02.py", "author_layer_a_batch_03.py", "author_layer_a_batch_04.py", "author_layer_a_batch_05.py", "author_layer_a_batch_06.py", "build_layer_a_staging.py",
            "validate_layer_a_extraction.py", "batch_01_report.md", "batch_02_report.md", "batch_03_report.md", "batch_04_report.md", "batch_05_report.md", "batch_06_report.md",
            "LAYER_A_EXTRACTION_COMPLETION.md", "__pycache__"} | set(TABLES)
extra = sorted(set(os.listdir(D)) - EXPECTED)
if extra:
    err.append(f"[22] unexpected files in the staging directory (no aggregate outputs before post-census reconciliation): {extra}")
for root_, _, files in os.walk(os.path.dirname(HERE)):
    if os.path.basename(root_) in ("layer_a_geometry", "__pycache__") or "layer_a_geometry" in root_.split(os.sep):
        continue  # D041: the authorised census geometry lives in evidence_universe/layer_a_geometry (validated there)
    for fn in files:
        if re.search(r"aggregat|geometr|layer_a_(counts|summary_matrix)", fn, re.I):
            err.append(f"[22] aggregate / geometry output found: {os.path.join(root_, fn)}")
# 23
if rb(cp("CODEBOOK_v1.2.md")) != git(D038_COMMIT, f"{CREL}/CODEBOOK_v1.2.md"):
    err.append("[23] CODEBOOK_v1.2.md is not byte-identical to 9b61868")
if rb(cp("CODEBOOK_v1.3.md")) != git("40c0d95", f"{CREL}/CODEBOOK_v1.3.md"):
    err.append("[23] CODEBOOK_v1.3.md is not byte-identical to 40c0d95 (superseded by v1.4, never edited)")
cb13 = rb(cp("CODEBOOK_v1.3.md")).decode()
for need in ["outcome-definition sufficiency", "sufficient to establish", "Do not infer domain membership solely from labels",
             "EMPLOYMENT-DEFINITION-UNRESOLVED", "Narrative subcomponent mentions", "never** copied into support U",
             "Neither rule H nor rule I has been independently second-coded"]:
    if need not in cb13:
        err.append(f"[23] CODEBOOK_v1.3.md missing rule-I text: {need!r}")
d039 = os.path.join(ROOT, "09_meta", "decision_log", "2026-10-18_outcome-definition-sufficiency-and-B2-heterogeneous-schedules.md")
for rc in ("RC-02", "RC-03", "RC-04"):
    r = [x for x in rcs if x["rc_id"] == rc]
    if not r or not r[0]["status"].startswith("RESOLVED BY D039"):
        err.append(f"[23] {rc} not RESOLVED BY D039 in rule_conflicts.csv")
    for path, label in [(P("batch_02_report.md"), "batch report"), (d037, "D037 record"), (d039, "D039 record")]:
        if not re.search(rf"{rc}[^\n]*RESOLVED BY D039", rb(path).decode()):
            err.append(f"[23] {label}: {rc} not marked RESOLVED BY D039")
old_rc = {r["rc_id"]: r for r in csv.DictReader(io.StringIO(git(PRE_D039_COMMIT, f"{REL}/rule_conflicts.csv").decode()))}
for r in rcs:
    if r["rc_id"] in old_rc and r["description"] != old_rc[r["rc_id"]]["description"]:
        err.append(f"[23] {r['rc_id']}: original conflict description altered")
for e in ("X030", "X034"):
    for s in tabs["support_codes.csv"]:
        if s["exp_id"] == e and (s["E"], s["U"], s["usable_U"]) != ("NONE", "NONE", "NO"):
            err.append(f"[23] {e} {s['architecture_dimension']}: must be E NONE / U NONE / usable_U NO (rule I)")
outs = {o["outcome_row_id"]: o for o in tabs["employment_outcomes.csv"]}
if [k for k in [f"LO-X030-0{i}" for i in range(1, 8)] if k not in outs] or \
        [o for o in [outs.get("LO-X030-01")] if not o or o["outcome_domain"] != RA.MIXED_TOKEN or "70%" not in o["estimate"] or o["stars"] != "*"]:
    err.append("[23] raw X030 mixed / label-only evidence missing or altered")
if not [o for o in outs.values() if o["exp_id"] == "X034" and o["verbal_result"] == "significantly more likely to be employed"]:
    err.append("[23] raw X034 'significantly more likely to be employed' statement missing")
if any("RULE-CONFLICT" in (s["I"], s["E"], s["U"]) for s in tabs["support_codes.csv"] if s["exp_id"] not in BATCH6) or \
        any(q["value"] == "RULE-CONFLICT" for q in tabs["quantitative_summaries.csv"] if q["exp_id"] not in BATCH6):
    err.append("[23] a RULE-CONFLICT value remains in Batches 1-5 after D039")
# 24
q33 = {q["component"]: q for q in tabs["quantitative_summaries.csv"] if q["exp_id"] == "X033" and q["qs_id"] == "QS-101"}
num, b2 = q33.get("ex-ante incremental annual transfer", {}), q33.get("derived B2", {})
subst = "D012 SUBSTITUTE" in num.get("note", "")
if num.get("value") in ("2400", "3600", "4800", "2400.0", "3600.0", "4800.0") or re.search(r"equal[- ]weight|midpoint|modal|representative", num.get("note", "").replace("No equal weights, midpoint, mode or representative unit used", ""), re.I):
    err.append("[24] X033 B2 numerator built from a schedule value / equal weights / midpoint / mode")
if not subst and ((num.get("value"), num.get("status"), b2.get("value"), b2.get("status")) != ("NR", "NR", "NR", "NR") or "MEASUREMENT FAILURE" not in num.get("note", "")):
    err.append("[24] X033 B2 must be NR (MEASUREMENT FAILURE) unless a flagged D012 realised-mean substitute exists")
sx = {s["architecture_dimension"]: s for s in tabs["support_codes.csv"] if s["exp_id"] == "X033"}
if b2.get("value") == "NR" and (sx.get("MAGNITUDE_B2", {}).get("V"), sx.get("MAGNITUDE_B2", {}).get("I")) != ("UNKNOWN", "NOT-ISOLATED"):
    err.append("[24] X033 MAGNITUDE_B2 must be V UNKNOWN / I NOT-ISOLATED while B2 is NR")
if any((s["E"], s["U"], s["usable_U"]) != ("E-A (caveat)", "SE", "YES") for s in sx.values()) or len(sx) != 3:
    err.append("[24] X033 employment E-A (caveat) / SE / usable_U YES altered")
# 25
reb = rd_c = (lambda n: list(csv.DictReader(open(cp(n), newline=""))) if os.path.exists(cp(n)) else [])
re13 = reb("v1_3_reapplication.csv")
if not re13 or open(cp("v1_3_reapplication.csv"), newline="").read() != RB.render(RB.build()):
    err.append("[25] v1_3_reapplication.csv is not the deterministic output of build_v1_3_reapplication.py")
by13 = {}
for r in re13:
    by13.setdefault(r["source_layer"], {})[r["case_or_row_id"]] = r
want13 = {"D034-CASE": {f"{c['blind_case_id']} ({c['support_row_id']})": (c["E_final"], c["U_final"], None) for c in fin},
          "MM-SUPPORT": {s["support_row_id"]: (s["E"], s["U"], None) for s in mm_sup},
          "MM-OUTCOME": {o["evidence_row_id"]: (o["compatibility_class"], o["uncertainty_status"], None) for o in mm_out}}
for b, ids in (("BATCH1", BATCH1), ("BATCH2", BATCH2)):
    want13[f"{b}-SUPPORT"] = {f"{s['exp_id']}-{s['architecture_dimension']}-{s['outcome_domain']}": (s["E"], s["U"], None)
                              for s in tabs["support_codes.csv"] if s["exp_id"] in ids}
    want13[f"{b}-OUTCOME"] = {o["outcome_row_id"]: (RB.RAW, o["uncertainty_form"], o["outcome_domain"])
                              for o in tabs["employment_outcomes.csv"] if o["exp_id"] in ids}
for sc, ids in want13.items():
    got = by13.get(sc, {})
    if set(got) != set(ids):
        err.append(f"[25] {sc}: v1.3 re-application does not cover exactly the current rows")
    for rid, (e_, u_, dom) in ids.items():
        r = got.get(rid)
        if r and ((r["new_E"], r["new_U"]) != (e_, u_) or (dom is not None and r["new_outcome_domain"] != dom)):
            err.append(f"[25] {sc} {rid}: current value differs from the registered v1.3 value (unregistered change)")
for r in re13:
    if r["changed"] == "YES" and "rule I" not in r["rule_basis"]:
        err.append(f"[25] {r['case_or_row_id']}: changed without a rule-I basis")
for o in tabs["employment_outcomes.csv"]:
    if o["outcome_domain"] == RB.UNRES and not RB.UNKNOWN_STATE.match(states.get(o["outcome_row_id"], {}).get("positive_states", "")):
        err.append(f"[25] {o['outcome_row_id']}: EMPLOYMENT-DEFINITION-UNRESOLVED without a recorded unknown positive state")
# 26
MAY = {"employment_outcomes.csv": {"outcome_domain"}, "support_codes.csv": {"E", "U", "usable_U", "factual_basis", "codebook_version"},
       "rule_conflicts.csv": {"status"}}
for n in list(BLD.CUMULATIVE) + list(BLD.FROM_BATCH2):
    old = [r for r in csv.DictReader(io.StringIO(git(PRE_D039_COMMIT, f"{REL}/{n}").decode())) if r["exp_id"] in BATCH2]
    new = [r for r in tabs[n] if r["exp_id"] in BATCH2]
    if len(old) != len(new):
        err.append(f"[26] {n}: Batch-2 row count changed since d1428de")
        continue
    for a, b in zip(old, new):
        may = set(MAY.get(n, set()))
        if n == "quantitative_summaries.csv" and a["exp_id"] == "X033" and a["qs_id"] == "QS-101":
            may |= {"value", "status", "note"}
        diff = {k for k in a if a[k] != b.get(k)}
        if diff - may:
            err.append(f"[26] {n} {a.get('outcome_row_id') or a.get('arm_id') or a.get('exp_id')}: Batch-2 fact changed: {sorted(diff - may)}")
# 27
fz2 = rd("BATCH_02_FREEZE.csv")
if not fz2:
    err.append("[27] BATCH_02_FREEZE.csv missing")
for n in sorted({f["table"] for f in fz2}):
    frozen = [f for f in fz2 if f["table"] == n]
    cur = [r for r in tabs.get(n, []) if r["exp_id"] in BATCH2]
    if frozen and frozen[0]["batch2_row_index"] == "NONE":
        if cur:
            err.append(f"[27] {n}: Batch-2 rows appeared where the freeze records none")
        continue
    if len(cur) != len(frozen):
        err.append(f"[27] {n}: Batch-2 row count differs from BATCH_02_FREEZE.csv")
        continue
    for f, r in zip(frozen, cur):
        if sha(json.dumps(r, sort_keys=True, ensure_ascii=False).encode()) != f["row_sha256"]:
            err.append(f"[27] {n} Batch-2 row {f['batch2_row_index']} ({f['exp_id']}) differs from BATCH_02_FREEZE.csv")
for a in auth:
    if (a["authority"], a["version"]) in (("codebook", "v1.3"), ("layer_a_protocol", "post-D039")) and a["verify_commit"] != "40c0d95":
        err.append(f"[27] AUTHORITY_STATUS {a['authority']} {a['version']}: verify_commit must be 40c0d95")
# 28
for s in tabs["support_codes.csv"]:
    if s["E"] == "NONE" and s["U"] != "NONE":
        err.append(f"[28] {s['exp_id']} {s['architecture_dimension']}: support U must be NONE when E is NONE (rules H / I)")
for q in tabs["quantitative_summaries.csv"]:
    if q["qs_id"] == "QS-101" and q["component"].startswith("ex-ante") and q["value"] not in ("NR", "NA") and \
            re.search(r"equal[- ]weight|midpoint|modal|representative", q["note"].replace("No equal weights, midpoint, mode or representative unit used", ""), re.I):
        err.append(f"[28] {q['exp_id']}: QS-101 numerator built from equal weights / midpoint / mode / a representative unit")
q39 = {q["component"]: q for q in tabs["quantitative_summaries.csv"] if q["exp_id"] == "X039" and q["qs_id"] == "QS-101"}
if q39.get("baseline mean annual household income (denominator)", {}).get("value") == "NR" and q39.get("derived B2", {}).get("value") != "NR":
    err.append("[28] X039 B2 derived without a reported baseline mean income")
ihh = [c for c in tabs["contrasts.csv"] if c["exp_id"] == "X039"]
p39 = [c for c in ihh if c["treatment_arm"] == "X039-T2" and c["reference_arm"] == "X039-T1"]
if not p39 or "PAYMENT-PROFILE" not in p39[0]["C002_diff"] or "SAME monthly event spacing" not in p39[0]["C002_diff"]:
    err.append("[28] X039: the equal-total B-vs-A contrast must be recorded as PAYMENT-PROFILE with identical monthly spacing")
if any(re.search(r"CADENCE", c["C002_diff"] + c["focal_architecture_dimensions"].replace("not CADENCE", "")) for c in ihh) or \
        any(s["exp_id"] == "X039" and s["architecture_dimension"] == "CADENCE" for s in tabs["support_codes.csv"]):
    err.append("[28] X039: front-loading coded as CADENCE without spacing variation")
ir39 = [r for r in tabs["identity_relations.csv"] if r["exp_id"] == "X039" and r["related_record"].startswith("X028")]
if len(ir39) != 1 or ir39[0]["relation_status"] not in ("DISTINCT", "SAME-EXPERIMENT-CANDIDATE", "UNCLEAR"):
    err.append("[28] X039: identity relation to X028 missing or status not DISTINCT / SAME-EXPERIMENT-CANDIDATE / UNCLEAR")
if any(r.get("exp_id") == "X028" for n in TABLES for r in tabs[n]) or \
        any(re.search(r"\bmerged? (with|into) X0(28|39)", " ".join(r.values()), re.I) for n in TABLES for r in tabs[n]):
    err.append("[28] X028 has staging rows or is recorded as merged with X039")

# 29
fz3 = rd("BATCH_03_FREEZE.csv")
if not fz3:
    err.append("[29] BATCH_03_FREEZE.csv missing")
for n in sorted({f["table"] for f in fz3}):
    frozen = [f for f in fz3 if f["table"] == n]
    cur = [r for r in tabs.get(n, []) if r["exp_id"] in BATCH3]
    if frozen and frozen[0]["batch3_row_index"] == "NONE":
        if cur:
            err.append(f"[29] {n}: Batch-3 rows appeared where the freeze records none")
        continue
    if len(cur) != len(frozen):
        err.append(f"[29] {n}: Batch-3 row count differs from BATCH_03_FREEZE.csv")
        continue
    for f, r in zip(frozen, cur):
        if sha(json.dumps(r, sort_keys=True, ensure_ascii=False).encode()) != f["row_sha256"]:
            err.append(f"[29] {n} Batch-3 row {f['batch3_row_index']} ({f['exp_id']}) differs from BATCH_03_FREEZE.csv")
if fz3 and sorted({f["table"] for f in fz3}) != sorted(TABLES):
    err.append("[29] BATCH_03_FREEZE.csv must cover every cumulative staging table (NONE marker where empty)")
# 30
q103 = {q["exp_id"]: q for q in tabs["quantitative_summaries.csv"] if q["qs_id"] == "QS-103"}
for e in ("X046", "X047"):
    if q103.get(e, {}).get("value") != "1.0":
        err.append(f"[30] {e}: QS-103 must be the promised 1.0-year horizon (extensions are realised, DS34)")
a45 = {a["arm_id"]: a for a in tabs["arms.csv"] if a["exp_id"] == "X045"}
t45 = {t["arm_id"]: t for t in tabs["temporal_fields.csv"] if t["exp_id"] == "X045"}
c45 = [c for c in tabs["contrasts.csv"] if c["exp_id"] == "X045" and {c["treatment_arm"], c["reference_arm"]} == {"X045-T1", "X045-T2"}]
s45 = {}
for s in tabs["support_codes.csv"]:
    if s["exp_id"] == "X045":
        s45.setdefault(s["architecture_dimension"], []).append(s)
o45 = [o for o in tabs["employment_outcomes.csv"] if c45 and o["contrast_id"] == c45[0]["contrast_id"]]
if len(c45) != 1 or not all(x.startswith("S-X045-") for x in c45[0]["source_id"].split(";")):
    err.append("[30] X045: the recurring-vs-lump-sum contrast must exist once and cite X045 primary sources (architecture not taken from the frame)")
else:
    c = c45[0]
    if "PAYMENT-PROFILE" not in c["C002_diff"]:
        err.append("[30] X045: the payment-profile / lumpiness difference must be recorded in the arm-arm contrast")
    freq = lambda a: a45.get(a, {}).get("payment_frequency", "").split(" (")[0]
    spacing = freq("X045-T1") != freq("X045-T2")
    if "CADENCE" in s45 and (not spacing or "event spacing" not in c["C002_diff"] or "SAME monthly event spacing" in c["C002_diff"]):
        err.append("[30] X045: CADENCE support requires differing event spacing in the arms and in the contrast (payment profile alone is not CADENCE)")
    hors = {t45.get(a, {}).get("finite_promised_payment_horizon") for a in ("X045-T1", "X045-T2")}
    if any(s["variation_level"] == "WITHIN-STUDY" for s in s45.get("DURATION", [])) and len(hors) < 2:
        err.append("[30] X045: a within-study DURATION row needs differing arm-level finite promised horizons")
    reported = [o for o in o45 if o["uncertainty_form"] != "NONE"]
    for cad in s45.get("CADENCE", []):
        if not reported and (cad["E"], cad["U"], cad["usable_U"]) != ("NONE", "NONE", "NO"):
            err.append("[30] X045: no direct arm-arm employment result is reported, so CADENCE must be E NONE / U NONE / usable_U NO")
    for o in o45:
        if o["uncertainty_form"] in ("SE", "CI") or o["SE"] not in TOKENS or o["CI_lower"] not in TOKENS:
            err.append(f"[30] {o['outcome_row_id']}: arm-arm SE / CI without a published arm-arm employment result (never combine arm-control SEs)")
n45 = {q["component"]: q for q in tabs["quantitative_summaries.csv"] if q["exp_id"] == "X045" and q["qs_id"] == "QS-101"}
if n45.get("ex-ante incremental annual transfer", {}).get("value") not in ("6000", "NR"):
    err.append("[30] X045: B2 numerator must be the common $6,000 per year (or NR), never an averaged schedule")
for s in tabs["support_codes.csv"]:
    if s["exp_id"] in BATCH4 and s["E"] in ("NONE", "NOT-APPLICABLE") and (s["U"] != "NONE" or s["usable_U"] != "NO"):
        err.append(f"[30] {s['exp_id']} {s['architecture_dimension']}: E {s['E']} requires U NONE / usable_U NO")

# 31
fz4 = rd("BATCH_04_FREEZE.csv")
if not fz4:
    err.append("[31] BATCH_04_FREEZE.csv missing")
for n in sorted({f["table"] for f in fz4}):
    frozen = [f for f in fz4 if f["table"] == n]
    cur = [r for r in tabs.get(n, []) if r["exp_id"] in BATCH4]
    if frozen and frozen[0]["batch4_row_index"] == "NONE":
        if cur:
            err.append(f"[31] {n}: Batch-4 rows appeared where the freeze records none")
        continue
    if len(cur) != len(frozen):
        err.append(f"[31] {n}: Batch-4 row count differs from BATCH_04_FREEZE.csv")
        continue
    for f, r in zip(frozen, cur):
        if sha(json.dumps(r, sort_keys=True, ensure_ascii=False).encode()) != f["row_sha256"]:
            err.append(f"[31] {n} Batch-4 row {f['batch4_row_index']} ({f['exp_id']}) differs from BATCH_04_FREEZE.csv")
if fz4 and sorted({f["table"] for f in fz4}) != sorted(TABLES):
    err.append("[31] BATCH_04_FREEZE.csv must cover every cumulative staging table (NONE marker where empty)")
# 32
PW = ("X052", "X053")
qs5 = [q for q in tabs["quantitative_summaries.csv"] if q["exp_id"] in BATCH5]
con5 = {c["contrast_id"]: c for c in tabs["contrasts.csv"] if c["exp_id"] in BATCH5}
arm5 = {a["arm_id"]: a for a in tabs["arms.csv"] if a["exp_id"] in BATCH5}
tmp5 = {t["arm_id"]: t for t in tabs["temporal_fields.csv"] if t["exp_id"] in BATCH5}
for q in qs5:
    if q["exp_id"] in PW and q["qs_id"] == "QS-103" and re.fullmatch(r"\d+(\.\d+)?", q["value"]):
        err.append(f"[32] {q['exp_id']}: Participatiewet QS-103 must not be a finite number (experiment window is C006, D036)")
    if q["exp_id"] in PW and q["qs_id"] == "QS-103" and re.search(r"2017|2019|experiment", q["value"]):
        err.append(f"[32] {q['exp_id']}: QS-103 value taken from the experiment window")
q53 = [q for q in qs5 if q["exp_id"] == "X053" and q["qs_id"] == "QS-103"]
if not q53 or (q53[0]["value"], q53[0]["status"]) != ("NA", "NA") or "NO-FIXED-END" not in q53[0]["note"]:
    err.append("[32] X053: QS-103 must be NA (NO-FIXED-END entitlement) with a note")
for aid, t in tmp5.items():
    if t["exp_id"] == "X053":
        if (t["payment_continuation_type"], t["finite_promised_payment_horizon"]) != ("NO-FIXED-END", "NA"):
            err.append(f"[32] {aid}: Participatiewet arm must be NO-FIXED-END / NA")
        if "exempt" in arm5.get(aid, {}).get("C006_obligations", "") and "C006" not in t["conditionality_end"]:
            err.append(f"[32] {aid}: exemption interval must be recorded as C006 conditionality, not as a payment horizon")
for q in qs5:
    m = re.match(r"contrast (LA-[\w-]+): ", q["component"])
    if m and q["value"] in ("0", "0.0", "0.000"):
        c = con5.get(m.group(1), {})
        if not c or not c["C001_diff"].startswith("0") or not c["C002_diff"].startswith("0") or "design zero" not in (q["note"] + " ").replace("zero numerator", "design zero"):
            err.append(f"[32] {q['component']}: B2 = 0 requires documented equality of the cash schedule (C001 and C002 both 0)")
for q in qs5:
    if q["qs_id"] == "QS-101" and q["value"] in ("0", "0.0", "0.000") and not q["component"].startswith("contrast "):
        if any(c["exp_id"] == q["exp_id"] and re.search(r"disregard|WITHDRAWAL", c["C001_diff"]) for c in con5.values()):
            err.append(f"[32] {q['exp_id']}: study-level B2 = 0 although a contrast changes the withdrawal / disregard rule")
for s in tabs["support_codes.csv"]:
    if s["exp_id"] in BATCH5 and s["architecture_dimension"] == "WITHDRAWAL":
        docs = [c for c in con5.values() if c["exp_id"] == s["exp_id"] and re.search(r"WITHDRAWAL rule differs|disregard", c["C001_diff"]) and not c["C001_diff"].startswith("0")]
        arms_rules = {a["C001_withdrawal_rule"] for a in arm5.values() if a["exp_id"] == s["exp_id"] and a["C001_withdrawal_rule"] not in TOKENS}
        if not docs or len(arms_rules) < 2:
            err.append(f"[32] {s['exp_id']}: WITHDRAWAL requires a documented benefit-vs-earnings rule difference between arms")
    if s["exp_id"] in BATCH5 and s["architecture_dimension"] in ("CONDITIONALITY", "WITHDRAWAL", "CADENCE", "DURATION") and s["variation_level"] == "WITHIN-STUDY" and s["I"] == "PURE":
        err.append(f"[32] {s['exp_id']} {s['architecture_dimension']}: PURE not allowed when every contrast bundles another substantive change")
for c in con5.values():
    tarms = c["treatment_arm"].split(";") + c["reference_arm"].split(";")
    if all(re.search(r"-T\d*$", a) for a in tarms):
        for o in tabs["employment_outcomes.csv"]:
            if o["contrast_id"] == c["contrast_id"] and (o["uncertainty_form"] != "NONE" or o["SE"] not in TOKENS):
                err.append(f"[32] {o['outcome_row_id']}: direct arm-arm employment inference recorded for {c['contrast_id']}, which no source reports")
for e in BATCH5:
    el = [r for r in tabs["eligibility_identity_review.csv"] if r["exp_id"] == e]
    if el and el[0]["randomisation_verified"] == "UNCLEAR" and el[0]["layer_A_eligibility"] == "VERIFIED":
        err.append(f"[32] {e}: UNCLEAR randomisation cannot be VERIFIED")
for s in tabs["SOURCE_LOG.csv"]:
    if "SHARED PRIMARY SOURCE" in s["notes"] and s["exp_id"] not in ("X052", "X053") + tuple(BATCH6):
        err.append(f"[32] {s['source_id']}: shared Participatiewet source attached to a non-Participatiewet experiment")
for n in TABLES:
    for r in tabs[n]:
        if r.get("exp_id") in BATCH5 and n != "SOURCE_LOG.csv" and re.search(r"\b(Groningen|Tilburg|Wageningen|Nijmegen|Apeldoorn|Amsterdam)\b[^;]*\b(effect|estimate|0[.,]\d{2,})", " ".join(v for v in r.values() if v)):
            err.append(f"[32] {n}: a Batch-6 municipality result appears in a Batch-5 row")
for s in tabs["support_codes.csv"]:
    if s["exp_id"] in BATCH5 and s["E"] in ("NONE", "NOT-APPLICABLE") and (s["U"] != "NONE" or s["usable_U"] != "NO"):
        err.append(f"[32] {s['exp_id']} {s['architecture_dimension']}: E {s['E']} requires U NONE / usable_U NO")

# 33
fz5 = rd("BATCH_05_FREEZE.csv")
if not fz5:
    err.append("[33] BATCH_05_FREEZE.csv missing")
for n in sorted({f["table"] for f in fz5}):
    frozen = [f for f in fz5 if f["table"] == n]
    cur = [r for r in tabs.get(n, []) if r["exp_id"] in BATCH5]
    if frozen and frozen[0]["batch5_row_index"] == "NONE":
        if cur:
            err.append(f"[33] {n}: Batch-5 rows appeared where the freeze records none")
        continue
    if len(cur) != len(frozen):
        err.append(f"[33] {n}: Batch-5 row count differs from BATCH_05_FREEZE.csv")
        continue
    for f, r in zip(frozen, cur):
        if sha(json.dumps(r, sort_keys=True, ensure_ascii=False).encode()) != f["row_sha256"]:
            err.append(f"[33] {n} Batch-5 row {f['batch5_row_index']} ({f['exp_id']}) differs from BATCH_05_FREEZE.csv")
if fz5 and sorted({f["table"] for f in fz5}) != sorted(TABLES):
    err.append("[33] BATCH_05_FREEZE.csv must cover every cumulative staging table (NONE marker where empty)")
elig = {r["exp_id"]: r for r in tabs["eligibility_identity_review.csv"]}
if elig.get("X051", {}).get("layer_A_eligibility") != "PENDING" or elig.get("X052", {}).get("layer_A_eligibility") != "FRAME-CONFLICT":
    err.append("[33] X051 must stay PENDING and X052 FRAME-CONFLICT until an explicit reconciliation record changes them")
# 34
con6 = {c["contrast_id"]: c for c in tabs["contrasts.csv"] if c["exp_id"] in BATCH6}
arm6 = {a["arm_id"]: a for a in tabs["arms.csv"] if a["exp_id"] in BATCH6}
qs6 = [q for q in tabs["quantitative_summaries.csv"] if q["exp_id"] in BATCH6]
TREAT = lambda a: re.search(r"-T\d+$", a) is not None
for t in tabs["temporal_fields.csv"]:
    if t["exp_id"] in BATCH6:
        if (t["payment_continuation_type"], t["finite_promised_payment_horizon"]) != ("NO-FIXED-END", "NA"):
            err.append(f"[34] {t['arm_id']}: Participatiewet arm must be NO-FIXED-END / NA (experiment windows are never C002)")
        if arm6.get(t["arm_id"], {}).get("C006_obligations", "").startswith("exempt") and "C006" not in t["conditionality_end"]:
            err.append(f"[34] {t['arm_id']}: exemption interval must be typed as C006, not as a payment horizon")
for e in BATCH6:
    q = [x for x in qs6 if x["exp_id"] == e and x["qs_id"] == "QS-103"]
    if not q or (q[0]["value"], q[0]["status"]) != ("NA", "NA") or "NO-FIXED-END" not in q[0]["note"]:
        err.append(f"[34] {e}: QS-103 must be NA with a NO-FIXED-END note (the experiment window is not QS-103)")
for q in qs6:
    m = re.match(r"contrast (LA-[\w-]+): ", q["component"])
    if m and q["value"] in ("0", "0.0", "0.000"):
        c = con6.get(m.group(1), {})
        if not c or not c["C001_diff"].startswith("0") or not c["C002_diff"].startswith("0") or "design zero" not in (q["note"] + " ").replace("zero numerator", "design zero"):
            err.append(f"[34] {q['component']}: B2 = 0 requires documented equality of the cash schedule (C001 and C002 both 0)")
    if q["qs_id"] == "QS-101" and not q["component"].startswith("contrast ") and q["value"] in ("0", "0.0", "0.000"):
        if any(c["exp_id"] == q["exp_id"] and re.search(r"WITHDRAWAL rule differs|disregard 50|exit premium", c["C001_diff"]) and not c["C001_diff"].startswith("0") for c in con6.values()):
            err.append(f"[34] {q['exp_id']}: study-level B2 = 0 although a contrast changes the withdrawal / disregard rule")
for s in tabs["support_codes.csv"]:
    if s["exp_id"] not in BATCH6:
        continue
    if s["architecture_dimension"] == "WITHDRAWAL":
        docs = [c for c in con6.values() if c["exp_id"] == s["exp_id"] and "WITHDRAWAL rule differs" in c["C001_diff"]]
        rules = {a["C001_withdrawal_rule"] for a in arm6.values() if a["exp_id"] == s["exp_id"] and a["C001_withdrawal_rule"] not in TOKENS}
        if not docs or len(rules) < 2:
            err.append(f"[34] {s['exp_id']}: WITHDRAWAL requires a documented benefit-vs-earnings rule difference between arms")
    if s["variation_level"] == "WITHIN-STUDY":
        mine = [c for c in con6.values() if c["exp_id"] == s["exp_id"] and s["architecture_dimension"] in c["focal_architecture_dimensions"]]
        if not mine:
            err.append(f"[34] {s['exp_id']} {s['architecture_dimension']}: within-study support row without a contrast naming the dimension")
        if s["I"] == "PURE" and not any(c["cotreatment_class"] in ("A", "NONE-KNOWN") and "BUNDLED" not in c["focal_architecture_dimensions"] for c in mine):
            err.append(f"[34] {s['exp_id']} {s['architecture_dimension']}: PURE needs a contrast whose documented differences leave only the focal dimension")
        if s["architecture_dimension"] == "CONDITIONALITY" and not any(not c["C006_diff"].startswith("0") for c in mine):
            err.append(f"[34] {s['exp_id']}: CONDITIONALITY needs a formal obligation-regime difference (C006)")
    if s["E"] in ("NONE", "NOT-APPLICABLE") and (s["U"] != "NONE" or s["usable_U"] != "NO"):
        err.append(f"[34] {s['exp_id']} {s['architecture_dimension']}: E {s['E']} requires U NONE / usable_U NO")
for c in con6.values():
    if TREAT(c["treatment_arm"]) and TREAT(c["reference_arm"]):
        for o in tabs["employment_outcomes.csv"]:
            if c["contrast_id"] in o["contrast_id"].split(";") and o["contrast_id"] == c["contrast_id"]:
                if o["direct_contrast_reported"] != "YES" or re.search(r"derived|difference of|from (the )?arm", o["estimand_description"] + o["source_location"], re.I):
                    err.append(f"[34] {o['outcome_row_id']}: arm-arm row for {c['contrast_id']} must be a directly reported result (never derived from arm-control rows)")
                if o["SE"] not in TOKENS or o["CI_lower"] not in TOKENS or o["uncertainty_form"] in ("SE", "CI"):
                    err.append(f"[34] {o['outcome_row_id']}: arm-arm SE / CI for {c['contrast_id']} (no published arm-arm SE / CI exists in Batch 6; never combine arm-control SEs)")
for n in TABLES:
    for r in tabs[n]:
        e = r.get("exp_id")
        if e in BATCH6 and n != "identity_relations.csv":  # identity relations compare records, so they may cite both sides
            refs = set()
            for f in ("source_id", "source_ids", "primary_design_source_id", "primary_outcome_source_id", "state_source_ids"):
                refs |= {x for x in re.split(r"[;\s]+", r.get(f, "") or "") if x.startswith("S-")}
            if any(not x.startswith(f"S-{e}-") for x in refs):
                err.append(f"[34] {n}: {e} row cites another experiment's source ({sorted(refs)}); municipality rows must stay separate")
        if any(re.search(r"transport[_ -]?family[_ -]?id\s*[:=]|dependence[_ -]?group[_ -]?id\s*[:=]", v or "", re.I) for v in r.values()) or \
                any(re.search(r"transport_family|dependence_group", k) for k in r):
            err.append(f"[34] {n}: transport-family / dependence-group assignment in staging ({e})")
for s in tabs["SOURCE_LOG.csv"]:
    if s["exp_id"] in BATCH6 and "CPB" in s["authors_or_org"] and ("SHARED PRIMARY SOURCE" not in s["notes"] or "Read for this municipality" not in s["notes"]):
        err.append(f"[34] {s['source_id']}: shared CPB source without the shared-source flag and municipality-specific provenance")
for r in rcs:
    if r["rc_id"] not in ("RC-01", "RC-02", "RC-03", "RC-04") and (not re.fullmatch(r"RC-0[5-9]|RC-[1-9]\d", r["rc_id"]) or r["batch"] != "6"):
        err.append(f"[34] {r['rc_id']}: new rule conflicts must be RC-05+ registered in Batch 6")
if os.path.exists(cp("CODEBOOK_v1.4.md")) and not os.path.exists(os.path.join(ROOT, "09_meta", "decision_log", "2026-10-19_layer-A-post-census-reconciliation.md")):
    err.append("[34] CODEBOOK_v1.4 may exist only under D040 (post-census reconciliation), never inside Batch 6")
if os.path.exists(os.path.join(ROOT, "03_models", "stage4_quantitative_crosswalk_v3.csv")):
    err.append("[34] crosswalk v3 must not be created inside Batch 6")
# 35
comp = rb(P("LAYER_A_EXTRACTION_COMPLETION.md")).decode()
for need in ["36 / 36", "RECONCILIATION PENDING", "No denominator reconciliation has occurred", "No aggregate support geometry has been computed",
             "No master-map integration has occurred"]:
    if need not in comp:
        err.append(f"[35] LAYER_A_EXTRACTION_COMPLETION.md missing: {need!r}")
if re.search(r"\b(PURE|BUNDLED|CONDITIONABLE-BUNDLE|E-A|E-B|E-C|usable_U)\b", comp):
    err.append("[35] LAYER_A_EXTRACTION_COMPLETION.md must not report support codes or counts")
for e in ORDER:
    if e not in comp:
        err.append(f"[35] LAYER_A_EXTRACTION_COMPLETION.md does not list {e}")
for path, label in [(d037, "D037 record"), (P("README.md"), "README")]:
    if "EXTRACTION COMPLETE — RECONCILIATION PENDING" not in rb(path).decode():
        err.append(f"[35] {label}: status must read EXTRACTION COMPLETE — RECONCILIATION PENDING")
if any(r.get("exp_id") == "X002" for n in TABLES for r in tabs[n]):
    err.append("[35] RIME (X002) has staging rows (Layer B; not extracted in this task)")
EU = os.path.dirname(HERE)
if sorted(x for x in os.listdir(EU) if x != os.path.basename(HERE)) != sorted(["coverage_metrics.csv", "build_coverage.py", "universe_frame.csv", "LAYER_A_EXTRACTION_PROTOCOL.md", "layer_a_reconciliation", "layer_a_geometry", "layer_b_extraction"]):  # D042: authorised RIME Layer-B staging (validated there)
    err.append("[35] evidence_universe holds unexpected files (RIME / Layer B extraction is not part of this task)")
for f in ("universe_frame.csv", "coverage_metrics.csv"):
    if rb(os.path.join(EU, f)) != git(MANIFEST_COMMIT, f"05_papers/representation_transport/evidence_universe/{f}"):
        err.append(f"[35] {f} changed since 318a581")

if err:
    print("FAIL")
    [print("  -", e) for e in err]
    sys.exit(1)
print(f"PASS (manifest frozen; Batches 1-6 extracted = 36 / 36; Batch 6 = {', '.join(BATCH6)}; {sum(len(v) for v in tabs.values())} staging rows; 35 checks; CODEBOOK_v1.4 active (D040); RC-05 resolved)")

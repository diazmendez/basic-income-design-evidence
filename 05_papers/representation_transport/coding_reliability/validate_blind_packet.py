#!/usr/bin/env python3
"""D033: validate the blind recoding packet. Exits 1 on failure.

Checks:
  1  exactly 25 BC cases in blind_cases.csv and blind_case_packets.md, BC001..BC025
  2  one-to-one mapping BC <-> frozen support rows (manifest) and deterministic permutation (rebuild matches)
  3  support_incidence.csv SHA-256 equals the frozen hash in the builder and in the manifest
     (after D034 the frozen D033 version is read from the D033 commit; the live table carries v1.1 codes)
  4  blind_cases.csv has exactly the second-coder columns and every second-coder cell is empty
  5  no original-code columns, T-levels, roles, support_row_ids, SG / TF IDs or forbidden vocabulary in the packets
  6  every packet field present and populated (or explicitly UNKNOWN); every case has resolvable provenance
  7  the manifest is consistent with the frozen support_incidence (original codes) and is not referenced by the packet
  8  codebook / packet hashes in the manifest match the files
Usage: python3 -I validate_blind_packet.py [--dir PACKET_DIR]
"""
import csv
import glob
import hashlib
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_blind_packet as B  # noqa: E402

err = []
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
PK = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else HERE   # packet dir (for mutation tests)
P = lambda n: os.path.join(PK, n)

rows = list(csv.DictReader(open(P("blind_cases.csv"))))
pk = open(P("blind_case_packets.md")).read()
man = json.load(open(P("original_code_manifest.json")))
sup = {s["support_row_id"]: s for s in B.frozen_sup_rows()}   # D033 frozen universe (live table recoded by D034)
# 1
ids = [r["blind_case_id"] for r in rows]
if ids != [f"BC{i:03d}" for i in range(1, 26)]:
    err.append("[1] blind_cases.csv must list BC001..BC025 in order")
if re.findall(r"^## (BC\d{3})$", pk, re.M) != [f"BC{i:03d}" for i in range(1, 26)]:
    err.append("[1] packets must contain BC001..BC025 in order")
# 2
mp = {k: v["support_row_id"] for k, v in man["original_codes"].items()}
if sorted(mp.values()) != sorted(sup) or len(set(mp.values())) != 25:
    err.append("[2] BC -> support-row mapping is not one-to-one onto the 25 frozen rows")
perm = sorted(sup)
random.Random(man["permutation_seed"]).shuffle(perm)
if any(mp.get(f"BC{i + 1:03d}") != sid for i, sid in enumerate(perm)):
    err.append("[2] mapping does not follow the recorded deterministic permutation")
# 3
if not (hashlib.sha256(B.frozen_sup_bytes()).hexdigest() == B.EXPECTED_SUP_SHA == man["support_incidence_sha256"]):
    err.append("[3] support_incidence.csv hash differs from the frozen universe")
# 4
if list(rows[0].keys()) != B.SECOND:
    err.append("[4] blind_cases.csv columns differ from the second-coder template")
for r in rows:
    if any(v.strip() for k, v in r.items() if k != "blind_case_id"):
        err.append(f"[4] {r['blind_case_id']}: second-coder cells must be empty")
banned_cols = {"V", "I", "E", "U", "support_row_id", "current_t_level_dimension", "possible_transport_role", "blocker"}
if banned_cols & set(rows[0].keys()):
    err.append("[4] original-code / role columns present in blind_cases.csv")
# 5
for pat in B.FORBIDDEN:
    for m in re.finditer(pat, pk):
        err.append(f"[5] forbidden vocabulary {pat!r} at: {pk[max(0, m.start() - 30):m.end() + 10]!r}")
for sid in sup:
    if sid in pk:
        err.append(f"[5] support_row_id {sid} leaked into packets")
if "original_code_manifest" in pk or "original_code_manifest" in open(P("blind_cases.csv")).read():
    err.append("[5] packet references the sealed manifest")
# 6
blocks = re.split(r"^## BC\d{3}$", pk, flags=re.M)[1:]
for i, b in enumerate(blocks, 1):
    for f in B.FIELDS:
        m = re.search(rf"^- \*\*{re.escape(f.replace('_', ' '))}:\*\* (.+)$", b, re.M)
        if not m or not m.group(1).strip():
            err.append(f"[6] BC{i:03d}: field {f} missing or empty")
        elif f == "provenance":
            for ref in re.findall(r"(\d\d_[\w/.*\-]+\.(?:md|csv))", m.group(1)):
                if not glob.glob(os.path.join(B.ROOT, ref)):
                    err.append(f"[6] BC{i:03d}: provenance path does not resolve: {ref}")
# 7
for bc, o in man["original_codes"].items():
    s = sup[o["support_row_id"]]
    if (o["V"], o["I"], o["E"], o["U"]) != (s["V"], s["I"], s["E"], s["U"]):
        err.append(f"[7] {bc}: manifest original codes differ from support_incidence")
# 8
if man["codebook_v1_sha256"] != sha(P("CODEBOOK_v1.md")) or man["packets_sha256"] != sha(P("blind_case_packets.md")):
    err.append("[8] codebook or packet changed after the manifest was frozen")

if err:
    print("FAIL")
    [print("  -", e) for e in err]
    sys.exit(1)
print("PASS (25 blind cases; seed %d; universe %s...)" % (man["permutation_seed"], man["support_incidence_sha256"][:12]))

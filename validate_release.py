#!/usr/bin/env python3
"""Validate this public replication package (run from the repository root: python3 -I -B validate_release.py).

1. every file listed in RELEASE_MANIFEST.csv exists with the recorded SHA-256, and no unlisted file is present;
2. every shipped builder, run in --check mode, reproduces the shipped tables, figure data, ontology audit and numeric audits.
These are software consistency checks, not scientific validation. Exits 1 on failure.
"""
import csv
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MS = "05_papers/representation_transport/manuscript"
CHECKS = [[f"{MS}/scripts/build_manuscript_tables.py", "--check"], [f"{MS}/scripts/build_supplement_tables.py", "--check"],
          [f"{MS}/scripts/build_supplement.py", "--check-audit"], [f"{MS}/scripts/build_tex_audit.py", "--check"],
          [f"{MS}/scripts/build_ontology_audit.py", "--check"], [f"{MS}/figures/build_figures.py", "--check"]]
SKIP = {"RELEASE_MANIFEST.csv"}

err = []
man = {r["path"]: r for r in csv.DictReader(open(os.path.join(HERE, "RELEASE_MANIFEST.csv"), newline="", encoding="utf-8"))}
present = set()
for dp, dn, fn in os.walk(HERE):
    dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), HERE).replace(os.sep, "/")
        if rel.endswith(".pyc") or rel in SKIP:
            continue
        present.add(rel)
for p, r in man.items():
    fp = os.path.join(HERE, p)
    if not os.path.exists(fp):
        err.append(f"missing: {p}")
    elif hashlib.sha256(open(fp, "rb").read()).hexdigest() != r["sha256"]:
        err.append(f"hash differs: {p}")
for p in sorted(present - set(man)):
    err.append(f"not in manifest: {p}")
for cmd in CHECKS:
    q = subprocess.run([sys.executable, "-I", "-B", os.path.join(HERE, cmd[0]), *cmd[1:]], capture_output=True, text=True, cwd=HERE)
    if q.returncode:
        err.append(f"rebuild check failed: {' '.join(cmd)}")
if err:
    print("FAIL")
    for e in err:
        print("  -", e)
    sys.exit(1)
print(f"PASS: {len(man)} files match RELEASE_MANIFEST.csv; {len(CHECKS)} rebuild checks reproduce the shipped outputs")

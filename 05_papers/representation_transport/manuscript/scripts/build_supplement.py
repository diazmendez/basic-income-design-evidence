#!/usr/bin/env python3
"""D048A: build the Supplementary Information PDF, its build record and its numeric audit.

1. rebuilds the main deterministic tables (table S3) and the supplement tables (scripts/build_supplement_tables.py);
2. compiles supplement/supplement.tex twice with latexmk (-g), with a fixed SOURCE_DATE_EPOCH;
3. parses the log (undefined references, missing files, LaTeX errors, overfull boxes, rerun warnings);
4. writes supplement/SUPPLEMENT_BUILD_RECORD.csv and supplement/last_build.log.txt;
5. writes supplement/SUPPLEMENT_NUMERIC_AUDIT.csv: every number in the prose must be covered by the paragraph's provenance
   tags (N-xx, F-01, REL as in the main audit; S-xx -> supplement/SUPPLEMENT_NUMERIC_CLAIMS.csv); every number in a generated
   table is traced to its generating script and source. Identifiers in \\texttt{} are not numbers;
6. removes LaTeX auxiliary files.
Run: python3 -I scripts/build_supplement.py [--audit-only] [--check-audit]
"""
import csv
import glob
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys

MS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPD = os.path.join(MS, "supplement")
sys.path.insert(0, os.path.join(MS, "scripts"))
import build_manuscript as BM  # noqa: E402
import build_tex_audit as TA  # noqa: E402

sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
GEN = [("supplement/table_s3_near_miss.tex", "scripts/build_manuscript_tables.py")] + \
      [(f"supplement/generated/{n}", "scripts/build_supplement_tables.py") for n in
       ("s1_frame.tex", "s2_grid.tex", "s3_duration.tex", "s4_withdrawal.tex", "s4_conditionality.tex", "s4_cadence.tex", "s4_layer_b.tex",
        "s4_union.tex", "s5_reporting.tex", "s6_codebook.tex", "s7_rime.tex", "s8_access.tex", "s9_validators.tex", "s10_tlabels.tex")]


def authorities():
    a = TA.authorities()
    for r in csv.DictReader(open(os.path.join(SUPD, "SUPPLEMENT_NUMERIC_CLAIMS.csv"), newline="")):
        a[r["claim_id"]] = TA.tok(r["value"])
    return a


def audit(text=None):
    text = text if text is not None else open(os.path.join(SUPD, "supplement.tex"), encoding="utf-8").read()
    auth = authorities()
    rows = []
    for start, lines in TA.paragraphs(text):
        tags = set(" ".join(re.findall(r"(?<!\\)%\s*((?:N-\d\d|F-\d\d|S-\d\d|REL)(?:\s+(?:N-\d\d|F-\d\d|S-\d\d|REL))*)", "\n".join(lines))).split())
        allowed = set().union(*(auth.get(t, set()) for t in tags)) if tags else set()
        for l in lines:
            vis = re.sub(r"(?<!\\)%.*$", "", l)
            vis = re.sub(r"\\texttt\{[^}]*\}", " ", vis)
            for p in TA.EXCL + [r"\\(?:graphicspath|setlength|renewcommand|newcommand)\{.*$", r"\\large|\\\\\[[^\]]*\]", r"\[\s*\d+(\.\d+)?em\]"]:
                vis = re.sub(p, " ", vis)
            for n in TA.NUM.findall(vis):
                t = n.lstrip("0") or "0"
                rows.append(dict(location=f"supplement.tex body line {start}", text=re.sub(r"\s+", " ", l.strip())[:90], number=n,
                                 claim_ids=";".join(sorted(tags)) or "NONE", status="TRACED" if t in allowed else "UNTRACED"))
    for g, script in GEN:
        src = ""
        for l in open(os.path.join(MS, g), encoding="utf-8"):
            if l.startswith("%"):
                continue
            m = re.search(r"Source: \\texttt\{([^}]*)\}", l)
            src = m.group(1).replace("\\_", "_") if m else src
            vis = re.sub(r"\\texttt\{[^}]*\}|\\[a-zA-Z]+\*?(\{[^}]*\})?|\{?\d?\.?\d+\\textwidth\}?|\d+(\.\d+)?(pt|em|ex)", " ", l)
            for n in TA.NUM.findall(vis):
                rows.append(dict(location=g, text=re.sub(r"\s+", " ", l.strip())[:90], number=n, claim_ids=f"GENERATED ({script})", status="TRACED"))
    return rows


def render(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["location", "text", "number", "claim_ids", "status"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def compile_pdf():
    for s in ("build_manuscript_tables.py", "build_supplement_tables.py"):
        subprocess.run([sys.executable, "-I", os.path.join(MS, "scripts", s)], check=True, capture_output=True)
    env = dict(os.environ, SOURCE_DATE_EPOCH="1792800000", FORCE_SOURCE_DATE="1")
    for _ in range(2):
        subprocess.run(["latexmk", "-pdf", "-g", "-interaction=nonstopmode", "-halt-on-error", "supplement.tex"], cwd=SUPD, env=env, capture_output=True)
    return open(os.path.join(SUPD, "supplement.log"), encoding="latin-1").read()


def main():
    if "--check-audit" in sys.argv:
        p = os.path.join(SUPD, "SUPPLEMENT_NUMERIC_AUDIT.csv")
        ok = os.path.exists(p) and open(p, encoding="utf-8").read() == render(audit())
        print("audit current" if ok else "SUPPLEMENT_NUMERIC_AUDIT.csv differs")
        sys.exit(0 if ok else 1)
    if "--audit-only" not in sys.argv:
        log = compile_pdf()
        pdf = os.path.join(SUPD, "supplement.pdf")
        if not os.path.exists(pdf):
            print("COMPILE FAILED")
            sys.exit(1)
        pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
        f = BM.findings(log, "")
        f.pop("bibtex_warnings")
        f.pop("bibtex_errors")
        f["latex_errors"] = len(re.findall(r"^! ", log, re.M))
        f["underfull_or_overfull_vbox"] = len(re.findall(r"(Overfull|Underfull) \\vbox", log))
        rec = dict(supplement_tex_sha256=sha(os.path.join(SUPD, "supplement.tex")), supplement_pdf_sha256=sha(pdf), pdf_pages=pages, **f)
        with open(os.path.join(SUPD, "SUPPLEMENT_BUILD_RECORD.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rec), lineterminator="\n")
            w.writeheader()
            w.writerow(rec)
        shutil.copy(os.path.join(SUPD, "supplement.log"), os.path.join(SUPD, "last_build.log.txt"))
        for ext in ("aux", "fdb_latexmk", "fls", "log", "out", "toc", "synctex.gz"):
            for p in glob.glob(os.path.join(SUPD, f"supplement.{ext}")):
                os.remove(p)
        print(rec)
    rows = audit()
    open(os.path.join(SUPD, "SUPPLEMENT_NUMERIC_AUDIT.csv"), "w", encoding="utf-8").write(render(rows))
    print(len(rows), "numbers;", sum(r["status"] == "UNTRACED" for r in rows), "untraced")
    for r in rows:
        if r["status"] == "UNTRACED":
            print(" ", r)


if __name__ == "__main__":
    main()

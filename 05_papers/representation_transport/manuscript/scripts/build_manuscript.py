#!/usr/bin/env python3
"""D047: build the v1 review PDF and its build record.

1. rebuilds the deterministic tables (scripts/build_manuscript_tables.py);
2. compiles manuscript.tex with latexmk (pdflatex + bibtex), falling back to pdflatex/bibtex/pdflatex/pdflatex;
3. parses the log for undefined citations / references, missing files and overfull boxes;
4. writes revision_v1/BUILD_RECORD.csv (page count, sha256 of manuscript.tex, references.bib, manuscript.pdf, log findings);
5. removes LaTeX auxiliary files (they are not committed).
Run: python3 -I scripts/build_manuscript.py
"""
import csv
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys

MS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def compile_pdf():
    subprocess.run([sys.executable, "-I", os.path.join(MS, "scripts", "build_manuscript_tables.py")], check=True, capture_output=True)
    env = dict(os.environ, SOURCE_DATE_EPOCH="1792800000", FORCE_SOURCE_DATE="1")
    if shutil.which("latexmk"):
        subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "manuscript.tex"], cwd=MS, env=env, capture_output=True)
    else:
        for cmd in (["pdflatex", "-interaction=nonstopmode", "manuscript.tex"], ["bibtex", "manuscript"],
                    ["pdflatex", "-interaction=nonstopmode", "manuscript.tex"], ["pdflatex", "-interaction=nonstopmode", "manuscript.tex"]):
            subprocess.run(cmd, cwd=MS, env=env, capture_output=True)
    log = open(os.path.join(MS, "manuscript.log"), encoding="latin-1").read()
    blg = open(os.path.join(MS, "manuscript.blg"), encoding="latin-1").read() if os.path.exists(os.path.join(MS, "manuscript.blg")) else ""
    return log, blg


def findings(log, blg):
    overfull = [float(x) for x in re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)", log)]
    return dict(
        undefined_citations=len(re.findall(r"Citation `[^']+' (on page \d+ )?undefined", log)),
        undefined_references=len(re.findall(r"Reference `[^']+' on page \d+ undefined", log)),
        missing_files=len(re.findall(r"File `[^']+' not found|LaTeX Error", log)),
        rerun_warnings=len(re.findall(r"Rerun to get", log)),
        overfull_boxes=len(overfull), max_overfull_pt=max(overfull) if overfull else 0.0,
        bibtex_warnings=len(re.findall(r"^Warning--", blg, re.M)), bibtex_errors=len(re.findall(r"error message", blg)))


def main():
    log, blg = compile_pdf()
    pdf = os.path.join(MS, "manuscript.pdf")
    if not os.path.exists(pdf):
        print("COMPILE FAILED")
        sys.exit(1)
    pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    f = findings(log, blg)
    rec = dict(manuscript_tex_sha256=sha(os.path.join(MS, "manuscript.tex")), references_bib_sha256=sha(os.path.join(MS, "references.bib")),
               manuscript_pdf_sha256=sha(pdf), pdf_pages=pages, **f)
    with open(os.path.join(MS, "revision_v1", "BUILD_RECORD.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rec), lineterminator="\n")
        w.writeheader()
        w.writerow(rec)
    shutil.copy(os.path.join(MS, "manuscript.log"), os.path.join(MS, "revision_v1", "last_build.log.txt"))
    for ext in ("aux", "bbl", "blg", "fdb_latexmk", "fls", "log", "out", "toc", "synctex.gz"):
        for p in glob.glob(os.path.join(MS, f"manuscript.{ext}")):
            os.remove(p)
    print(rec)


if __name__ == "__main__":
    main()

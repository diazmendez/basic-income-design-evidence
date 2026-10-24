#!/usr/bin/env python3
"""D047: numeric traceability audit of manuscript.tex (and the generated tables it inputs).

Every visible number in a paragraph must be covered by the provenance tags in that paragraph's TeX comments:
  N-xx -> paper/PAPER_NUMERIC_CLAIMS.csv;  F-01 -> revision_v1/V1_NUMERIC_CLAIMS.csv;  REL -> D034 pre-adjudication table.
Numbers inside generated/*.tex are traced to their generating script and authority (GENERATED).
Excluded (not scientific claims): years, decades, section / figure / table / box labels, list markers, LaTeX layout arguments,
AI model version labels (disclosure statement, D048B), licence labels such as CC BY 4.0 (D048C).
Writes revision_v1/TEX_NUMERIC_AUDIT.csv. Run: python3 -I scripts/build_tex_audit.py [--check] [--tex PATH]
"""
import csv
import io
import os
import re
import sys

MS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RT = os.path.dirname(MS)
ROOT = os.path.dirname(os.path.dirname(RT))
TEX = sys.argv[sys.argv.index("--tex") + 1] if "--tex" in sys.argv else os.path.join(MS, "manuscript.tex")
NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])")
EXCL = [r"\\(?:cite[pt]?|ref|label|input|includegraphics|bibliography|bibliographystyle|graphicspath|usepackage|documentclass|setlist|section|paragraph)\*?(?:\[[^\]]*\])*\{[^}]*\}",
        r"\[[^\]]*(?:pt|cm|textwidth)[^\]]*\]", r"\b(?:19|20)\d\d\b", r"\b\d{4}s\b", r"(?:Figure|Table|Box|Section|Sections)~?\s?(?:\\ref\{[^}]*\})?\d*",
        r"\\item", r"0\.\d+\\textwidth", r"\d+pt", r"Manuscript draft v\d", r"Claude Opus \d+(?:\.\d+)?|GPT-\d+(?:\.\d+)?|Gemini \d+(?:\.\d+)?", r"CC BY \d\.\d"]


def tok(s):
    return {t.lstrip("0") or "0" for t in NUM.findall(s)}


def authorities():
    a = {}
    for r in csv.DictReader(open(os.path.join(RT, "paper", "PAPER_NUMERIC_CLAIMS.csv"), newline="")):
        a[r["claim_id"]] = tok(r["value"].replace("/", " ").replace("->", " "))
    for r in csv.DictReader(open(os.path.join(MS, "revision_v1", "V1_NUMERIC_CLAIMS.csv"), newline="")):
        a[r["claim_id"]] = tok(r["value"])
    d034 = open(os.path.join(ROOT, "09_meta", "decision_log", "2026-10-18_support-coding-reliability-adjudication.md"), encoding="utf-8").read()
    rows = [re.sub(r"§\s?\d+", " ", l) for l in d034.splitlines() if re.match(r"^\| (V|I|E|U|usable_U)\b", l) and "/ 25" in l]
    a["REL"] = set().union(*(tok(l) for l in rows))
    return a


def paragraphs(text):
    body = text.split(r"\begin{document}", 1)[1]
    out, cur, start = [], [], 0
    lines = body.splitlines()
    for i, l in enumerate(lines, 1):
        if not l.strip():
            if cur:
                out.append((start, cur))
            cur = []
            continue
        if not cur:
            start = i
        cur.append(l)
    if cur:
        out.append((start, cur))
    return out


def audit(text=None):
    text = text if text is not None else open(TEX, encoding="utf-8").read()
    auth = authorities()
    rows = []
    for start, lines in paragraphs(text):
        tags = set(re.findall(r"(?<!\\)%\s*((?:N-\d\d|F-\d\d|REL)(?:\s+(?:N-\d\d|F-\d\d|REL))*)", "\n".join(lines)))
        tags = set(" ".join(tags).split())
        allowed = set().union(*(auth.get(t, set()) for t in tags)) if tags else set()
        for l in lines:
            vis = re.sub(r"(?<!\\)%.*$", "", l)
            for p in EXCL:
                vis = re.sub(p, " ", vis)
            for n in NUM.findall(vis):
                t = n.lstrip("0") or "0"
                rows.append(dict(location=f"manuscript.tex body line {start}", text=re.sub(r"\s+", " ", l.strip())[:90], number=n, claim_ids=";".join(sorted(tags)) or "NONE",
                                 status="TRACED" if t in allowed else "UNTRACED"))
    for g in ("generated/table1.tex", "generated/table2.tex"):
        for l in open(os.path.join(MS, g), encoding="utf-8"):
            if l.startswith("%"):
                continue
            vis = re.sub(r"\\[a-zA-Z]+(\{[^}]*\})?|0\.\d+\\textwidth|\d+(\.\d+)?pt", " ", l)
            for n in NUM.findall(vis):
                rows.append(dict(location=g, text=re.sub(r"\s+", " ", l.strip())[:90], number=n, claim_ids="GENERATED (scripts/build_manuscript_tables.py)", status="TRACED"))
    return rows


def render(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["location", "text", "number", "claim_ids", "status"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


if __name__ == "__main__":
    t = render(audit())
    p = os.path.join(MS, "revision_v1", "TEX_NUMERIC_AUDIT.csv")
    if "--check" in sys.argv:
        ok = os.path.exists(p) and open(p, encoding="utf-8").read() == t
        print("audit current" if ok else "TEX_NUMERIC_AUDIT.csv differs")
        sys.exit(0 if ok else 1)
    open(p, "w", encoding="utf-8").write(t)
    rows = audit()
    print(len(rows), "numbers;", sum(r["status"] == "UNTRACED" for r in rows), "untraced")
    for r in rows:
        if r["status"] == "UNTRACED":
            print(" ", r)

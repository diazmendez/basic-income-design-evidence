#!/usr/bin/env python3
"""D048C: counting-unit (ontology) audit of the near-miss displays (Supplementary Table S3 and Figure 4).

Recomputes, from the frozen authorities only, which entities Table S3 and Figure 4 show and in which counting unit:
  table row = one (architecture dimension x design) entry = the cell-representative support path of one
  transport family on one dimension (a "family-dimension support path").
The design list of Table S3 is taken from scripts/build_manuscript_tables.py (CASES); Figure 4's row rule is the one in
figures/build_figures.py (cell representative, V = Y, isolation PURE or CONDITIONABLE-BUNDLE). Identifiers come from
final_scope_c/*_SUPPORT_PATHS_FINAL.csv and final_scope_c/SCOPE_C_SUPPORT_UNION.csv.
Writes revision_v1/NEAR_MISS_ONTOLOGY_AUDIT.csv and revision_v1/NEAR_MISS_ONTOLOGY_COUNTS.csv; stops if the isolated
entries differ from the frozen support-union isolated counts (N-13, N-14, N-15).
Run: python3 -I scripts/build_ontology_audit.py [--check]
"""
import csv
import io
import os
import sys

MS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RT = os.path.dirname(MS)
FIN = os.path.join(RT, "final_scope_c")
sys.path.insert(0, os.path.join(MS, "scripts"))
import build_manuscript_tables as T  # noqa: E402

rd = lambda p: list(csv.DictReader(open(p, newline="", encoding="utf-8")))
ISO = ("PURE", "CONDITIONABLE-BUNDLE")
DIMS = ("WITHDRAWAL", "CONDITIONALITY", "CADENCE")


def rows():
    union = {(r["architecture_dimension"], r["experiment_id"], r["support_path"]): r for r in rd(os.path.join(FIN, "SCOPE_C_SUPPORT_UNION.csv"))}
    s3 = set(T.CASES)
    out = []
    for d in DIMS:
        for r in rd(os.path.join(FIN, f"{d}_SUPPORT_PATHS_FINAL.csv")):
            if r["cell_representative"] != "YES":
                continue
            iso = r["V"] == "Y" and r["I"] in ISO
            in_s3 = (d, r["experiment_id"]) in s3
            if not (iso or in_s3):
                continue
            u = union.get((d, r["experiment_id"], r["support_path"]), {})
            out.append(dict(
                dimension=d, design=T.LABEL.get(r["experiment_id"], r["experiment_name"]), experiment_id=r["experiment_id"], scope_layer=r["scope_layer"],
                support_case_id=r["support_case_id"], support_path=r["support_path"], dependence_group_id=u.get("dependence_group_id", "NOT-IN-UNION"),
                transport_family_id=r["transport_family_id"], isolation_code=r["I"], E=r["E"], U=r["U"], usable_U=r["usable_U"],
                strict_stage_reached=r["strict_gate_stage_reached"], strict_pass="YES" if r["failure_reason"] == "STRICT PASS" else "NO",
                broader_EB_isolated_usableU="YES" if iso and r["E"] == "E-B" and r["usable_U"] == "YES" else "NO",
                included_in_s3="YES" if in_s3 else "NO", included_in_fig4="YES" if iso else "NO",
                isolated_flag="YES" if iso else "NO", bundled_key_comparator_flag="YES" if in_s3 and not iso else "NO",
                reason_for_inclusion=("isolated cell-representative path (V = Y; I = PURE or CONDITIONABLE-BUNDLE)" if iso
                                      else "key bundled comparator listed in Table S3 (not isolated; not in Figure 4)")))
    seen = set()
    for i, r in enumerate(out, 1):
        r["row_id"] = f"NM{i:02d}"
        r["unique_design_flag"] = "FIRST" if r["experiment_id"] not in seen else "REPEAT (same design on another dimension)"
        seen.add(r["experiment_id"])
    return out


def counts(out):
    s3 = [r for r in out if r["included_in_s3"] == "YES"]
    f4 = [r for r in out if r["included_in_fig4"] == "YES"]
    u = lambda rs, k: len({r[k] for r in rs})
    c = [("table_s3_rows (dimension x design entries)", len(s3)), ("table_s3_unique_designs (experiments)", u(s3, "experiment_id")),
         ("table_s3_unique_transport_families", u(s3, "transport_family_id")), ("table_s3_unique_dependence_groups", u(s3, "dependence_group_id")),
         ("table_s3_isolated_family_dimension_entries", sum(r["isolated_flag"] == "YES" for r in s3)),
         ("table_s3_bundled_key_comparators", sum(r["bundled_key_comparator_flag"] == "YES" for r in s3)),
         ("figure4_rows (isolated family-dimension entries)", len(f4)), ("figure4_unique_transport_families", u(f4, "transport_family_id")),
         ("strict_supporting_family_dimension_entries", sum(r["strict_pass"] == "YES" for r in out)),
         ("broader_EB_sensitivity_family_dimension_entries (isolated E-B + usable U)", sum(r["broader_EB_isolated_usableU"] == "YES" for r in out))]
    for d in DIMS:
        c.append((f"figure4_isolated_entries_{d.lower()}", sum(r["dimension"] == d for r in f4)))
    return c


def check_frozen(out):
    claims = {r["claim_id"]: r["value"] for r in rd(os.path.join(RT, "paper", "PAPER_NUMERIC_CLAIMS.csv"))}
    for d, k in zip(DIMS, ("N-13", "N-14", "N-15")):
        n = sum(r["dimension"] == d and r["isolated_flag"] == "YES" for r in out)
        if str(n) != claims[k].split("/")[1]:
            raise SystemExit(f"isolated entries for {d} ({n}) differ from frozen {k} ({claims[k]})")
    if [r for r in out if r["included_in_s3"] == "YES" and r["isolated_flag"] == "NO" and r["bundled_key_comparator_flag"] != "YES"]:
        raise SystemExit("unclassified Table S3 row")


def render(dicts, fields):
    b = io.StringIO()
    w = csv.DictWriter(b, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(dicts)
    return b.getvalue()


def build():
    out = rows()
    check_frozen(out)
    f = ["row_id", "dimension", "design", "experiment_id", "scope_layer", "support_case_id", "support_path", "dependence_group_id", "transport_family_id",
         "isolation_code", "E", "U", "usable_U", "strict_stage_reached", "strict_pass", "broader_EB_isolated_usableU", "included_in_s3", "included_in_fig4",
         "reason_for_inclusion", "unique_design_flag", "isolated_flag", "bundled_key_comparator_flag"]
    return {"revision_v1/NEAR_MISS_ONTOLOGY_AUDIT.csv": render(out, f),
            "revision_v1/NEAR_MISS_ONTOLOGY_COUNTS.csv": render([dict(quantity=q, value=v) for q, v in counts(out)], ["quantity", "value"])}


if __name__ == "__main__":
    res = build()
    bad = []
    for k, v in res.items():
        p = os.path.join(MS, k)
        cur = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        if "--check" in sys.argv:
            bad += [k] if cur != v else []
        elif cur != v:
            open(p, "w", encoding="utf-8").write(v)
    print(("differ: " + str(bad)) if bad else ("ontology audit current" if "--check" in sys.argv else "written"))
    print(res["revision_v1/NEAR_MISS_ONTOLOGY_COUNTS.csv"])
    sys.exit(1 if bad else 0)

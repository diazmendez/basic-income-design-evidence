#!/usr/bin/env python3
"""D046: deterministic candidate figures for manuscript v1 (PDF + SVG + PNG) from frozen authorities only.

No numeric value is typed by hand: every plotted count is read from the D041 / D043 CSVs listed in FIGURE_BUILD_MANIFEST.csv,
and each figure's plotted data are written next to it (figN_data.csv). No effect size, sign or significance is read or drawn.
Greyscale-safe: black / grey fills, hatching and distinct marker shapes; no information carried by colour alone.
Run: python3 -I build_figures.py [--check]   (--check: data CSVs and manifest equal a fresh build)
"""
import csv
import hashlib
import io
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RT = os.path.abspath(os.path.join(HERE, "..", ".."))
GEO = os.path.join(RT, "evidence_universe", "layer_a_geometry")
FIN = os.path.join(RT, "final_scope_c")
rd = lambda p: list(csv.DictReader(open(p, newline="", encoding="utf-8")))
REL = lambda p: os.path.relpath(p, os.path.abspath(os.path.join(RT, "..", "..")))

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.spines.top": False, "axes.spines.right": False,
                     "svg.hashsalt": "d046", "svg.fonttype": "none", "pdf.fonttype": 42, "hatch.linewidth": 0.6})
META = {"pdf": {"CreationDate": None, "ModDate": None, "Producer": "matplotlib"}, "svg": {"Date": None}, "png": {"Software": "matplotlib"}}
ARCH = [("WITHDRAWAL", "Withdrawal"), ("CONDITIONALITY", "Conditionality"), ("CADENCE", "Cadence")]
CROSS = [("MAGNITUDE_B2", "Transfer magnitude"), ("DURATION", "Promised duration"), ("BASELINE_EMPLOYMENT", "Baseline employment")]
GREYS = ["#1a1a1a", "#555555", "#8c8c8c", "#c8c8c8"]
HATCH = ["", "////", "....", "xxxx"]
MANIFEST = []


def put(path, data):
    """Write only when the content changes (D048A): an unchanged rebuild leaves files untouched, so editor auto-builds are not triggered."""
    if not os.path.exists(path) or open(path, "rb").read() != data:
        open(path, "wb").write(data)


def save(fig, name, data_rows, sources):
    for ext in ("pdf", "svg", "png"):
        b = io.BytesIO()
        fig.savefig(b, format=ext, dpi=300 if ext == "png" else None, bbox_inches="tight", metadata=META[ext])
        put(os.path.join(HERE, f"{name}.{ext}"), b.getvalue())
    plt.close(fig)
    dpath = os.path.join(HERE, f"{name}_data.csv")
    if data_rows:
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(data_rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(data_rows)
        put(dpath, buf.getvalue().encode("utf-8"))
    MANIFEST.append(dict(figure=name, outputs=f"{name}.pdf;{name}.svg;{name}.png", data_file=f"{name}_data.csv" if data_rows else "NONE (conceptual)",
                         authorities=";".join(REL(s) for s in sources), data_sha256=hashlib.sha256(open(dpath, "rb").read()).hexdigest() if data_rows else "NONE"))


def fig1():
    # D048A: V -> I -> E -> U are the four comparison-level support stages; independent validation is drawn apart,
    # as a separate requirement of the prospective discovery-and-validation test (not a fifth stage).
    stages = [("Variation", "feature differs\nbetween the\ncompared groups", "no difference documented"),
              ("Isolation", "no other feature\nchanges, or it is\nheld fixed", "bundled arms"),
              ("Compatible\nestimand", "employment\nprobability reported\nfor that comparison", "hours only; mixed states;\nnot reported"),
              ("Usable\nuncertainty", "published SE or CI\nfor that estimate", "stars, p-value or\nverbal only"),
              ("Independent\nvalidation", "a second\nindependent family\npasses the same\nfour stages", "single source")]
    fig, ax = plt.subplots(figsize=(7.4, 2.9))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 3.55)
    ax.axis("off")
    for i, (h, test, fail) in enumerate(stages):
        x = 0.1 + i * 1.95 + (0.35 if i == 4 else 0)
        ax.add_patch(FancyBboxPatch((x, 1.55), 1.7, 1.2, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white" if i < 4 else "#e6e6e6", ec="#1a1a1a",
                                    lw=1, ls="-" if i < 4 else "--"))
        ax.text(x + 0.85, 2.48, h, ha="center", va="center", fontsize=8, fontweight="bold")
        ax.text(x + 0.85, 1.9, test, ha="center", va="center", fontsize=6)
        ax.text(x + 0.85, 1.05, "Typical failure:\n" + fail, ha="center", va="center", fontsize=6.3, color="#444444")
        if i < 3:
            ax.annotate("", xy=(x + 1.93, 2.15), xytext=(x + 1.72, 2.15), arrowprops=dict(arrowstyle="-|>", color="#1a1a1a", lw=1))
    ax.plot([0.1, 0.1, 7.65, 7.65], [2.9, 3.0, 3.0, 2.9], color="#1a1a1a", lw=0.8)
    ax.text(3.875, 3.2, "Comparison-level support stages (V \u2192 I \u2192 E \u2192 U)", ha="center", va="center", fontsize=7.5, fontweight="bold")
    ax.plot([8.25, 8.25, 9.95, 9.95], [2.9, 3.0, 3.0, 2.9], color="#1a1a1a", lw=0.8, ls="--")
    ax.text(9.1, 3.2, "Requirement of the\nprospective test", ha="center", va="center", fontsize=7, fontstyle="italic")
    ax.text(5.1, 0.35, "The four stages are evaluated on one comparison at a time. Independent validation is not a fifth stage: it is a requirement of this\n"
            "prospective test (one family for discovery, one for validation). Operational audit criteria, not a new causal theory.",
            ha="center", va="center", fontsize=6.6, style="italic")
    save(fig, "fig1_support_chain", [], [os.path.join(RT, "coding_reliability", "CODEBOOK_v1.4.md")])


def fig2():
    geo = {r["architecture_dimension"]: r for r in rd(os.path.join(GEO, "LAYER_A_SUPPORT_GEOMETRY.csv"))}
    blk = {r["architecture_dimension"]: r for r in rd(os.path.join(GEO, "LAYER_A_BLOCKER_DECOMPOSITION.csv")) if r["scope"] == "LAYER-A-CENSUS-43"}
    data = []
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1.25, 1]})
    st = [("families_with_variation", "Varies"), ("families_isolated", "Isolated"), ("families_isolated_EA", "+ compatible\nestimand"), ("families_isolated_EA_usableU", "+ usable\nuncertainty")]
    for j, (d, lab) in enumerate(ARCH):
        for k, (col, sl) in enumerate(st):
            v = int(geo[d][col])
            x = j * 5 + k
            a.bar(x, v, color=GREYS[k], hatch=HATCH[k], edgecolor="#1a1a1a", lw=0.6, width=0.85)
            a.text(x, v + 0.25, str(v), ha="center", fontsize=7)
            data.append(dict(panel="A", dimension=d, quantity=col, value=v, denominator=geo[d]["denominator_experiments"]))
        a.text(j * 5 + 1.5, -2.6, lab, ha="center", fontsize=8, fontweight="bold")
        a.text(j * 5 + 1.5, -4.3, f"no variation {blk[d]['V_N']}\nunknown {blk[d]['V_UNKNOWN']}", ha="center", fontsize=6.2, color="#444444")
        data += [dict(panel="A", dimension=d, quantity="V_N", value=int(blk[d]["V_N"]), denominator=43), dict(panel="A", dimension=d, quantity="V_UNKNOWN", value=int(blk[d]["V_UNKNOWN"]), denominator=43)]
    a.set_xticks([])
    a.set_ylabel("Transport families (of 43)")
    a.set_ylim(0, max(int(geo[d]["families_with_variation"]) for d, _ in ARCH) + 2)
    a.set_title("A  Architecture dimensions: support chain within studies", loc="left", fontsize=8.5)
    a.legend(handles=[plt.Rectangle((0, 0), 1, 1, fc=GREYS[k], hatch=HATCH[k], ec="#1a1a1a", lw=0.6) for k in range(4)], labels=[s for _, s in st],
             fontsize=6.2, frameon=False, loc="upper right", ncol=2)
    for j, (d, lab) in enumerate(CROSS):
        vy, vn, vu = int(blk[d]["V_Y"]), int(blk[d]["V_N"]), int(blk[d]["V_UNKNOWN"])
        bs = int(geo[d]["families_between_study_EA_usableU"])
        left = 0
        for k, (val, nm) in enumerate([(vy, "value established"), (vn, "no value / not defined"), (vu, "unknown")]):
            b.barh(j, val, left=left, color=["#555555", "white", "#c8c8c8"][k], hatch=["", "", "...."][k], edgecolor="#1a1a1a", lw=0.6, height=0.55)
            if val:
                b.text(left + val / 2, j, str(val), ha="center", va="center", fontsize=6.8, color="white" if k == 0 else "#1a1a1a")
            left += val
        b.plot([bs], [j + 0.42], marker="v", color="#1a1a1a", ms=6)
        b.text(bs + 0.8, j + 0.42, f"{bs} with strict estimand + usable U", va="center", fontsize=6.2)
        data += [dict(panel="B", dimension=d, quantity=q, value=v, denominator=43) for q, v in (("V_Y", vy), ("V_N", vn), ("V_UNKNOWN", vu), ("between_study_EA_usableU", bs))]
    b.set_yticks(range(len(CROSS)))
    b.set_yticklabels([l for _, l in CROSS])
    b.set_xlim(0, 43)
    b.set_xlabel("Experiments (of 43)")
    b.invert_yaxis()
    b.set_title("B  Between-study dimensions (never isolated)", loc="left", fontsize=8.5)
    b.legend(handles=[plt.Rectangle((0, 0), 1, 1, fc=c, hatch=h, ec="#1a1a1a", lw=0.6) for c, h in (("#555555", ""), ("white", ""), ("#c8c8c8", "...."))],
             labels=["value established", "no value / not defined", "unknown"], fontsize=6.2, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3)
    fig.tight_layout()
    save(fig, "fig2_census_attrition", data, [os.path.join(GEO, "LAYER_A_SUPPORT_GEOMETRY.csv"), os.path.join(GEO, "LAYER_A_BLOCKER_DECOMPOSITION.csv")])


def fig3():
    la = {r["architecture_dimension"]: r for r in rd(os.path.join(GEO, "LAYER_A_SUPPORT_GEOMETRY.csv"))}
    sb = {r["architecture_dimension"]: r for r in rd(os.path.join(GEO, "PRE_CENSUS_MAPPED_LAYER_A_SUBSET_GEOMETRY.csv"))}
    n_sub, n_cen = int(sb["WITHDRAWAL"]["denominator_experiments"]), int(la["WITHDRAWAL"]["denominator_experiments"])
    data = []
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw={"width_ratios": [1, 1.3]})
    for j, (d, lab) in enumerate([("MAGNITUDE_B2", "Transfer magnitude"), ("DURATION", "Promised duration")]):
        ks, kc = int(sb[d]["families_between_study_EA_usableU"]), int(la[d]["families_between_study_EA_usableU"])
        for off, (k, n, nm, mk) in enumerate([(ks, n_sub, "pre-census subset", "o"), (kc, n_cen, "full census", "s")]):
            a.plot(k / n, j + (off - 0.5) * 0.28, marker=mk, color="#1a1a1a", mfc="#1a1a1a" if off else "white", ms=7, ls="")
            a.text(k / n + 0.04, j + (off - 0.5) * 0.28, f"{k} of {n}", va="center", fontsize=7)
            data.append(dict(panel="A", dimension=d, set=nm, count=k, denominator=n))
    a.set_yticks([0, 1])
    a.set_yticklabels(["Transfer magnitude", "Promised duration"])
    a.set_xlim(0, 1)
    a.set_ylim(1.6, -0.6)
    a.set_xlabel("Share with strict employment estimand + usable uncertainty")
    a.set_title("A  Usable between-study support", loc="left", fontsize=8.5)
    a.legend(handles=[plt.Line2D([], [], marker="o", mfc="white", color="#1a1a1a", ls=""), plt.Line2D([], [], marker="s", color="#1a1a1a", ls="")],
             labels=[f"pre-census subset ({n_sub})", f"full census ({n_cen})"], fontsize=6.4, frameon=False, loc="lower right")
    for j, (d, lab) in enumerate(ARCH):
        for row, (col, nm) in enumerate([("families_with_variation", "varies"), ("families_isolated_EA_usableU", "strict support")]):
            s, c = int(sb[d][col]), int(la[d][col])
            y = j * 3 + row
            b.plot([s, c], [y, y], color="#8c8c8c", lw=1.2)
            b.plot(s, y, marker="o", mfc="white", color="#1a1a1a", ms=6)
            b.plot(c, y, marker="s", color="#1a1a1a", ms=6)
            b.text(max(s, c) + 0.35, y, f"{nm}: {s} → {c}", va="center", fontsize=6.8)
            data.append(dict(panel="B", dimension=d, set=f"{col} subset->census", count=f"{s}->{c}", denominator=f"{n_sub}->{n_cen}"))
    b.set_yticks([j * 3 + 0.5 for j in range(3)])
    b.set_yticklabels([l for _, l in ARCH])
    b.set_xlim(-0.3, max(int(la[d]["families_with_variation"]) for d, _ in ARCH) + 5)
    b.invert_yaxis()
    b.set_xlabel("Transport families")
    b.set_title("B  Architecture: variation vs strict support", loc="left", fontsize=8.5)
    fig.text(0.5, -0.03, f"The {n_sub}-experiment subset is nested within the {n_cen}-experiment census (not an independent sample); no test statistic is computed.",
             ha="center", fontsize=6.6, style="italic")
    fig.tight_layout()
    save(fig, "fig3_selection_audit", data, [os.path.join(GEO, "PRE_CENSUS_MAPPED_LAYER_A_SUBSET_GEOMETRY.csv"), os.path.join(GEO, "LAYER_A_SUPPORT_GEOMETRY.csv")])


NAMES = {"X007": "B-MINCOME", "X057": "Wageningen", "X001": "New Jersey-Pennsylvania NIT", "X004": "Gary NIT", "X002": "RIME (rural NIT)",
         "X060": "Utrecht", "X066": "Vermont WRP", "X016": "Compton Pledge", "X068": "Nigeria FNLP cash", "X045": "Newark"}


def fig4():
    """Cases chosen mechanically: every family whose representative path on an architecture dimension passes isolation."""
    rows, data = [], []
    for d, lab in ARCH:
        for r in rd(os.path.join(FIN, f"{d}_SUPPORT_PATHS_FINAL.csv")):
            if r["cell_representative"] == "YES" and r["V"] == "Y" and r["I"] in ("PURE", "CONDITIONABLE-BUNDLE") and "UNRESOLVED" not in r["transport_family_id"] \
                    and not r["outcome_domain" if "outcome_domain" in r else "support_case_id"].startswith("S-SG10"):
                rows.append((lab, r))
    fig, ax = plt.subplots(figsize=(6.2, 0.32 * len(rows) + 1.2))
    cols = ["Variation", "Isolation", "Compatible\nestimand", "Usable\nuncertainty"]
    for i, (lab, r) in enumerate(rows):
        e_ok, e_b, u_ok = r["E"] in ("E-A", "E-A (caveat)"), r["E"] == "E-B", r["usable_U"] == "YES"
        state = ["pass", "pass", "pass" if e_ok else ("broader E-B only" if e_b else "not passed"),
                 ("pass" if u_ok else "not passed") if e_ok else ("broader E-B only" if (e_b and u_ok) else "not reached")]
        for k, s in enumerate(state):
            mk = {"pass": dict(marker="o", mfc="#1a1a1a"), "broader E-B only": dict(marker="D", mfc="#bdbdbd"), "not passed": dict(marker="X", mfc="white"),
                  "not reached": dict(marker="o", mfc="white")}[s]
            ax.plot(k, i, ls="", color="#1a1a1a", ms=7 if s != "not reached" else 5, mec="#1a1a1a", **mk)
        ax.text(-0.6, i, f"{NAMES.get(r['experiment_id'], r['experiment_id'])}", ha="right", va="center", fontsize=7)
        ax.text(3.6, i, r["U"] if e_ok else r["E"], ha="left", va="center", fontsize=6.2, color="#444444")
        data.append(dict(dimension=lab, experiment_id=r["experiment_id"], V=r["V"], I=r["I"], E=r["E"], U=r["U"], usable_U=r["usable_U"],
                         stage_states=";".join(state)))
    groups = [lab for lab, _ in rows]
    for g in dict.fromkeys(groups):
        idx = [i for i, x in enumerate(groups) if x == g]
        ax.text(-3.9, (idx[0] + idx[-1]) / 2, g, rotation=90, ha="center", va="center", fontsize=7.5, fontweight="bold")
        if idx[0]:
            ax.axhline(idx[0] - 0.5, color="#c8c8c8", lw=0.6)
    ax.set_xticks(range(4))
    ax.set_xticklabels(cols, fontsize=7)
    ax.xaxis.tick_top()
    ax.set_yticks([])
    ax.set_xlim(-4.2, 4.6)
    ax.set_ylim(len(rows) - 0.5, -0.7)
    for s in ("left", "bottom", "top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(handles=[plt.Line2D([], [], ls="", color="#1a1a1a", **m) for m in (dict(marker="o", mfc="#1a1a1a"), dict(marker="D", mfc="#bdbdbd"),
                                                                              dict(marker="X", mfc="white"), dict(marker="o", mfc="white", ms=5))],
              labels=["passes", "broader E-B object only", "not passed", "not reached"], fontsize=6.3, frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 0.0))
    ax.text(0.5, -0.12, "Rows: family-dimension entries whose focal path is isolated (a family can appear under two dimensions). Not a ranking of study quality; a stop does not indicate an absent effect.",
            transform=ax.transAxes, ha="center", fontsize=6.2, style="italic")
    save(fig, "fig4_near_miss_matrix", data, [os.path.join(FIN, f"{d}_SUPPORT_PATHS_FINAL.csv") for d, _ in ARCH])


SHORT = {  # short display labels for RESEARCH_AGENDA_GAPS.csv fields (text only; the stage and T label are read from the CSV)
    "WITHDRAWAL": ("a second independent same-guarantee contrast with a direct employment estimate and SE / CI", "existing isolated designs (in principle) or a new trial"),
    "CONDITIONALITY": ("SE / CI for an existing isolated contrast with a compatible estimate", "existing design (uncertainty only)"),
    "CADENCE": ("SE / CI for two independent isolated cadence contrasts", "existing designs (reporting / uncertainty)"),
    "DURATION": ("assigned horizon contrasts with employment estimates and SE / CI in two families", "likely new designs"),
}
STAGE = {"V": "variation", "I": "isolation", "E": "estimand", "U": "uncertainty"}


def fig5():
    ag = {r["architecture_dimension"]: r for r in rd(os.path.join(FIN, "RESEARCH_AGENDA_GAPS.csv"))}
    data = []
    import textwrap
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    ax.axis("off")
    hdr = ["Dimension", "Stops at", "Smallest missing evidence object", "Possible source of that object"]
    xs = [0.0, 0.16, 0.30, 0.73]
    for x, h in zip(xs, hdr):
        ax.text(x, 0.95, h, fontsize=7.5, fontweight="bold", va="top", transform=ax.transAxes)
    for i, d in enumerate(SHORT):
        y = 0.78 - i * 0.2
        stage = STAGE[ag[d]["binding_support_stage"]]
        vals = [d.title(), stage, textwrap.fill(SHORT[d][0], 46), textwrap.fill(SHORT[d][1], 30)]
        for x, v in zip(xs, vals):
            ax.text(x, y, v, fontsize=6.8, va="top", transform=ax.transAxes, wrap=True)
        data.append(dict(dimension=d, binding_support_stage=ag[d]["binding_support_stage"], final_T=ag[d]["current_final_T"], missing_object_label=SHORT[d][0], route_label=SHORT[d][1]))
    ax.text(0.0, -0.05, "Requirements that would change the evidence status; no claim is made that data access or new trials are currently feasible.",
            fontsize=6.4, style="italic", transform=ax.transAxes)
    save(fig, "fig5_status_changing_evidence", data, [os.path.join(FIN, "RESEARCH_AGENDA_GAPS.csv")])


def build():
    MANIFEST.clear()
    fig1(), fig2(), fig3(), fig4(), fig5()
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["figure", "outputs", "data_file", "authorities", "data_sha256"], lineterminator="\n")
    w.writeheader()
    w.writerows(MANIFEST)
    return buf.getvalue()


if __name__ == "__main__":
    if "--check" in sys.argv:
        old = {n: open(os.path.join(HERE, n), "rb").read() for n in os.listdir(HERE) if n.endswith(".csv")}
        man = build()
        new = {n: open(os.path.join(HERE, n), "rb").read() for n in os.listdir(HERE) if n.endswith("_data.csv")}
        bad = [n for n in new if old.get(n) != new[n]] + ([] if old.get("FIGURE_BUILD_MANIFEST.csv") == man.encode() else ["FIGURE_BUILD_MANIFEST.csv"])
        print("figures current" if not bad else f"differ: {bad}")
        sys.exit(1 if bad else 0)
    put(os.path.join(HERE, "FIGURE_BUILD_MANIFEST.csv"), build().encode("utf-8"))
    print("built:", [m["figure"] for m in MANIFEST])

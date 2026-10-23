"""espmap-sesiidae-001: the results report, filled from ~/s001/analysis.json.

  python s001_report.py --atlas <sha> --arrowfield <sha> [--deviations FILE]

Writes ~/s001/report.md. Every sentence a result licenses is taken from the
frozen plan's section 5 table, chosen by the outcome; nothing here is written
after seeing a number. Order: what was run, exclusions, the primary result per
contrast against the plan's stated expectation, secondary, sensitivity, what
no outcome means, provenance. Every primary site is reported whatever it
shows. A PARTIAL analysis.json makes a report headed DRAFT FROM PARTIAL DATA.
"""
import argparse
import json
from pathlib import Path

OUT = Path.home() / "s001"
PLAN = "https://github.com/Azuromalachite/sesiidae-pheromone-atlas/blob/7e3465859bc2b8950078238f0bffb0ea6b4dd512/analyses/espmap-sesiidae-001/analysis-plan.md"
NAME = {"z3_z13_18_oac": "Z3,Z13-18:OAc", "e3_z13_18_oac": "E3,Z13-18:OAc", "e2_z13_18_oac": "E2,Z13-18:OAc",
        "z3_z13_18_oh": "Z3,Z13-18:OH", "z3_z13_18_al": "Z3,Z13-18:Al (teaching control)"}
# section 5, verbatim in substance: outcome -> (we may say, we may not say)
MAY = {
    "resolved": ("under this protocol, the free molecule's ESP at this site distinguishes the two compounds "
                 "by more than their conformational variation",
                 "that this difference explains any biological difference"),
    "different on average": ("the ensemble means differ, but some single conformations of the two molecules "
                             "are electrostatically indistinguishable at this site",
                             "that the site is resolved"),
    "unresolved": ("under this protocol, free-molecule ESP does not resolve the two compounds at this site",
                   "that the compounds are electrostatically identical, or that electrostatics plays no "
                   "biological role"),
    "not evaluable": ("nothing about this contrast", "anything"),
    "no data": ("nothing: fewer than two members, or the site has no surface in some member", "anything"),
}
# section 5 'Expected, from the pilot': (contrast, site) -> outcome
EXPECTED = {("B_stereo", "C3-H"): "unresolved", ("B_stereo", "C4-H"): "unresolved",
            ("C_position", "C4-H"): "resolved", ("C_position", "C2-H"): "unresolved",
            ("C_position", "C3-H"): "unresolved", ("A_headgroup", "global V_max"): "resolved"}
STATS_NOTE = (
    "**How to read the statistics.** The 20 members per molecule are a designed coverage set "
    "(the lowest-MMFF conformer plus 19 spread over Rg, of 100 embeddings), not independent random "
    "draws from an equilibrium population. Range non-overlap is therefore used as a deterministic "
    "robustness criterion over this prespecified, shape-diverse ensemble. The combinatorial "
    "probability the frozen plan quotes (2/C(40,20)) assumes exchangeable random observations, and "
    "is not read here as a p-value or a false-positive probability. The bootstrap interval "
    "resamples the selected conformer set: it describes that set, it is not a population-level "
    "confidence interval, and 'different on average' stays descriptive.\n")
NEVER = ["that receptor or enzyme discrimination is explained", "that biological activity is predicted",
         "that a site is where a desaturase or other enzyme acts",
         "anything about solvated, bound or membrane-embedded states",
         "anything about taxa or compounds outside the case bundle"]


def row(site, r):
    if "delta" not in r:
        return f"| {site} | **{r['outcome']}** | – | – | – | – | – |"
    c = r["conditions"]
    tick = "".join("✓" if c[k] else "✗" for k in ("1_ranges_disjoint", "2_beyond_partition", "3_same_sign"))
    return (f"| {site} | **{r['outcome']}** | {r['delta']:+.2f} | "
            f"{r['range_x'][0]:.2f}…{r['range_x'][1]:.2f} / {r['range_y'][0]:.2f}…{r['range_y'][1]:.2f} | "
            f"{r['partition_sensitivity']:.2f} ({r['partition_sensitivity_max_member']:.2f}) | "
            f"{r['bootstrap_interval'][0]:+.2f}…{r['bootstrap_interval'][1]:+.2f} | {tick} |")


HEAD = ("| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |\n"
        "| --- | --- | --- | --- | --- | --- | --- |")


def main(a):
    res = json.loads((OUT / "analysis.json").read_text())
    md = []
    if res["partial"]:
        md += ["> **DRAFT FROM PARTIAL DATA** — members still pending: "
               f"{res['pending']}. Nothing below is a result.\n"]
    md += ["# espmap-sesiidae-001: results\n",
           f"Prospective analysis plan: [Atlas analyses/espmap-sesiidae-001 at 7e34658]({PLAN}), frozen "
           "2026-10-23 before any member was computed. A confirmatory replication of the pilot, on a new "
           "conformer draw (seed 20261024, K = 20), under the plan's section 4 rule. Not a preregistration.\n",
           "Potential in kcal/mol, B3LYP/def2-SVP + RI, gas phase, 0.26 bohr, nearest-nucleus partition "
           "primary. Every verdict below is under espmap-sesiidae-001/range_partition_sign_v1, the frozen "
           "plan's rule, never espmap.compare/1's generic resolved_under. "
           "Δ = mean(Y) − mean(X). Conditions: 1 ranges disjoint, 2 |Δ| beyond the partition "
           "sensitivity (section 4 definition; the pilot-style number in brackets, never used), 3 same sign "
           "under the radius-scaled rule. Global extrema involve no partition, so 2 and 3 hold trivially.\n",
           STATS_NOTE, "## Members and exclusions\n", "| molecule | members | folded | excluded | evaluable |",
           "| --- | --- | --- | --- | --- |"]
    for s, m in res["molecules"].items():
        exc = "; ".join(f"{e['conformer']} ({e['reason']}, Rg {e['rg_angstrom']:.2f}, folded {e['folded']})"
                        for e in m["excluded"]) or "none"
        md.append(f"| {NAME[s]} | {m['n_ok']} | {m['n_folded']} | {exc} | {'yes' if m['evaluable'] else '**no**'} |")
    by = {(c["id"], c["population"]): c for c in res["contrasts"]}
    for cid in ["B_stereo", "C_position", "A_headgroup"]:
        c = by[(cid, "all")]
        md += [f"\n## {cid}: X = {NAME[c['X']]}, Y = {NAME[c['Y']]} (n = {c['n'][0]} / {c['n'][1]})\n",
               "### Primary\n", HEAD]
        prim = {k.split(':', 1)[1]: r for k, r in c["sites"].items() if k.startswith("primary:")}
        md += [row(s, r) for s, r in prim.items()]
        md.append("")
        for s, r in prim.items():
            say, never = MAY[r["outcome"]]
            exp = EXPECTED.get((cid, s))
            met = "" if exp is None else (f" The plan expected **{exp}**; this outcome cannot test it."
                                          if r["outcome"] in ("no data", "not evaluable") else
                                          f" The plan expected **{exp}**: "
                                          + ("as expected." if exp == r["outcome"] else
                                             "observed different on average (also not resolved). The pilot "
                                             "predicted no resolution and none occurred; the means do differ "
                                             "(descriptive)."
                                             if (exp, r["outcome"]) == ("unresolved", "different on average") else
                                             "**not as expected**" + (
                                                 " — the pilot's C4-H call did not replicate under the stricter "
                                                 "test." if (cid, s) == ("C_position", "C4-H") else ".")))
            md.append(f"- **{s}: {r['outcome']}.** We may say: {say}. We may not say: {never}.{met}")
        md += ["\n### Secondary\n", HEAD]
        md += [row(k.split(':', 1)[1], r) for k, r in c["sites"].items() if k.startswith("secondary:")]
        e = by[(cid, "extended")]
        md += [f"\n### Sensitivity: extended members only (n = {e['n'][0]} / {e['n'][1]}), beside, never instead of, "
               "the result above\n", HEAD]
        md += [row(k.split(':', 1)[1], r) for k, r in e["sites"].items() if k.startswith("primary:")]
        md += ["\nSecondary sites, extended members only (plan section 6 applies the rule to the extended "
               "population; reported beside the secondary rows above, never instead of them):\n", HEAD]
        md += [row(k.split(':', 1)[1], r) for k, r in e["sites"].items() if k.startswith("secondary:")]
        changed = [f"{k.split(':', 1)[1]} ({c['sites'][k]['outcome']} → {r['outcome']})"
                   for k, r in e["sites"].items() if k.split(":", 1)[0] in ("primary", "secondary")
                   and r["outcome"] != c["sites"][k]["outcome"]]
        md.append("\nOutcomes that differ between all members and extended members only: "
                  + ("; ".join(changed) if changed else "none") + ".")
        ex = [k.split(':', 1)[1] for k, r in c["sites"].items() if k.startswith("exploratory:") and r["outcome"] == "resolved"]
        md.append("\nExploratory, never interpreted (plan section 2): other chain sites meeting the rule: "
                  + (", ".join(ex) if ex else "none") + ".")
    md += ["\n## The teaching control (descriptive chemistry, no biological claim)\n", HEAD]
    for cid in ["A_headgroup (control: Al vs OAc)", "A_headgroup (control: Al vs OH)"]:
        c = by[(cid, "all")]
        md += [row(f"{cid.split(': ')[1].rstrip(')')} {k.split(':', 1)[1]}", r)
               for k, r in c["sites"].items() if not k.startswith("exploratory:")]
    md += ["\n## Sensitivity analyses not run\n",
           "- Basis (def2-TZVP single points, plan section 6): " + (a.basis or "**not run**") + ".",
           "- Solvent: not studied; gas phase is the stated baseline.",
           "\n## Deviations from the plan\n", (Path(a.deviations).read_text().strip() if a.deviations else "None."),
           "\n## No outcome of this study means\n"] + [f"- {x}{'.' if i == len(NEVER) - 1 else ';'}"
                                                      for i, x in enumerate(NEVER)]
    md += ["\n## Provenance\n",
           "- espmap v0.2.1 (41a989d), each member an espmap.record/1 with its sha256 in the Atlas index.",
           f"- Atlas commit (records): {a.atlas or '_to fill_'}; plan frozen at 7e34658.",
           f"- Arrowfield commit: {a.arrowfield or '_to fill_'}.",
           "- Folded: an intramolecular contact (espmap master 5175515's provisional rule) or surface genus > 0.",
           "- Partition sensitivity: section 4's definition decides; on 2026-10-23, before any analysis, the "
           "user chose to keep it and to report the pilot's max-member number beside it. The plan's pilot "
           "table quotes that pilot-style number (1.43 at C4-H); section 4's gives 0.77 on the same data."]
    (OUT / "report.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--atlas"), ap.add_argument("--arrowfield"), ap.add_argument("--deviations")
    ap.add_argument("--basis", help="one line on the def2-TZVP sensitivity, if run")
    main(ap.parse_args())

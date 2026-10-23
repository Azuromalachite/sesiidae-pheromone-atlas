"""espmap-sesiidae-001: the frozen plan's decision rule (Atlas
analyses/espmap-sesiidae-001/analysis-plan.md, frozen at 7e34658), applied to
the members s001_build.py accepted (~/s001/<slug>/members.json).

  python s001_analyse.py [--partial]

Writes ~/s001/analysis.json and ~/s001/analysis.md. With --partial, contrasts
are evaluated on whatever members exist and every line says PARTIAL; such
output is a test of this script, never a result.

Section 4, per primary site, Delta = mean(Y) - mean(X), nearest-nucleus rule:
  resolved   iff (1) the two ensembles' site-mean ranges do not overlap,
                 (2) |Delta| > partition sensitivity = max over the two
                     molecules of |mean(nearest) - mean(radius-scaled)|,
                 (3) Delta has the same sign under the radius-scaled rule;
  different on average  iff the bootstrap 95 % interval of Delta (10,000
                 resamples of members within each ensemble, seed 20261024)
                 excludes 0 and (2)-(3) hold while (1) fails;
  unresolved otherwise;
  not evaluable  if a molecule has more than 2 of 20 members excluded or any
                 excluded member is folded (section 3).
Global extrema use the members' V_min / V_max. They involve no partition, so
(2) and (3) hold trivially (sensitivity 0, one sign): stated in the report as
this script's reading of "the same rule applies".
Section 6 population sensitivity: the same rule on extended members only,
reported beside, never instead of, the all-member result.
"""
import json
import sys
from pathlib import Path

import numpy as np

OUT = Path.home() / "s001"
SEED, K, NBOOT = 20261024, 20, 10_000
PRIMARY_RULE, OTHER_RULE = "nearest_nucleus", "radius_scaled"
NAME = {"z3_z13_18_oac": "Z3,Z13-18:OAc", "e3_z13_18_oac": "E3,Z13-18:OAc", "e2_z13_18_oac": "E2,Z13-18:OAc",
        "z3_z13_18_oh": "Z3,Z13-18:OH", "z3_z13_18_al": "Z3,Z13-18:Al (teaching control)"}
GLOBAL = {"global V_min": "V_min_kcal_mol", "global V_max": "V_max_kcal_mol"}
# (id, X, Y, primary, secondary): Delta = Y - X
CONTRASTS = [
    ("B_stereo", "z3_z13_18_oac", "e3_z13_18_oac", ["C3-H", "C4-H"], ["head O", "global V_min", "global V_max"]),
    ("C_position", "e3_z13_18_oac", "e2_z13_18_oac", ["C2-H", "C3-H", "C4-H"],
     ["head O", "global V_min", "global V_max"]),
    ("A_headgroup", "z3_z13_18_oac", "z3_z13_18_oh", ["global V_max", "global V_min"], ["head O"]),
    # the teaching control: descriptive chemistry, no biological claim (case bundle)
    ("A_headgroup (control: Al vs OAc)", "z3_z13_18_oac", "z3_z13_18_al", ["global V_max", "global V_min"], ["head O"]),
    ("A_headgroup (control: Al vs OH)", "z3_z13_18_oh", "z3_z13_18_al", ["global V_max", "global V_min"], ["head O"]),
]
EXPLORATORY = [f"C{n}-H" for n in range(1, 19)]
# The study verdict, named so it is never confused with espmap.compare/1's
# generic resolved_under rule: a site is "resolved" for this study only under this.
VERDICT_RULE = "espmap-sesiidae-001/range_partition_sign_v1"
PARTITION_NOTE = (
    "**Partition sensitivity.** Condition 2 uses the plan's section 4 definition: the larger, "
    "over the two molecules, of |mean(nearest-nucleus) − mean(radius-scaled)| at the site. "
    "Beside it, never used in the decision, is the pilot-style number: the largest "
    "|nearest-nucleus − radius-scaled| of any single member, over both molecules. The plan's "
    "disclosure table quotes the pilot's partition sensitivity at C4-H as **1.43**. That is the "
    "pilot-style number (the pilot's analysis script computed it that way); the section 4 "
    "definition gives 0.77 on the same pilot data. The user chose, on 2026-10-23 and before any "
    "member of this study was analysed, to decide on the frozen section 4 text and to report the "
    "pilot-style number alongside it. This is the plan's own text applied as written, not a "
    "deviation.\n")


def load(slug):
    rows = json.loads((OUT / slug / "members.json").read_text())
    ok = [r for r in rows if r["status"] == "ok"]
    exc = [r for r in rows if r["status"] == "excluded"]
    for r in ok:
        rec = json.loads((OUT / slug / "conformers" / f"{r['conformer']}.json").read_text())
        r["V"] = {g: rec["results"][k] for g, k in GLOBAL.items()}
        r["site"] = {s["label"]: {rule: s[rule]["V_area_mean_kcal_mol"] if s[rule]["area_A2"] > 0 else None
                                  for rule in (PRIMARY_RULE, OTHER_RULE)}
                     for s in rec["sites"]["reaction_sites"]}
    evaluable = len(exc) <= 2 and not any(r["folded"] for r in exc)
    return dict(ok=ok, excluded=exc, pending=sum(r["status"] == "pending" for r in rows), evaluable=evaluable)


def values(members, site, rule):
    if site in GLOBAL:
        return np.array([m["V"][site] for m in members])
    v = [m["site"][site][rule] for m in members]
    if any(x is None for x in v):
        return None                      # a member with no area at this site: no site mean
    return np.array(v, dtype=float)


def boot_ci(x, y, rng):
    bx = rng.choice(x, size=(NBOOT, len(x)), replace=True).mean(1)
    by = rng.choice(y, size=(NBOOT, len(y)), replace=True).mean(1)
    return [float(v) for v in np.percentile(by - bx, [2.5, 97.5])]


def decide(mx, my, site, rng):
    x, y = values(mx, site, PRIMARY_RULE), values(my, site, PRIMARY_RULE)
    if x is None or y is None or len(x) < 2 or len(y) < 2:
        return dict(outcome="no data", n=[0 if x is None else len(x), 0 if y is None else len(y)])
    delta = float(y.mean() - x.mean())
    if site in GLOBAL:
        sens = sens_member = 0.0
        delta_other = delta
    else:
        xo, yo = values(mx, site, OTHER_RULE), values(my, site, OTHER_RULE)
        if xo is None or yo is None:
            return dict(outcome="no data", n=[len(x), len(y)], why="no area under the radius-scaled rule")
        sens = float(max(abs(x.mean() - xo.mean()), abs(y.mean() - yo.mean())))
        # reported, never used: the pilot's definition (largest single-member rule
        # difference), which the plan's disclosure table quotes (1.43 at C4-H)
        sens_member = float(max(np.abs(x - xo).max(), np.abs(y - yo).max()))
        delta_other = float(yo.mean() - xo.mean())
    c1 = bool(x.max() < y.min() or y.max() < x.min())
    c2 = bool(abs(delta) > sens)
    c3 = bool(np.sign(delta) == np.sign(delta_other) and delta != 0)
    ci = boot_ci(x, y, rng)
    if c1 and c2 and c3:
        outcome = "resolved"
    elif c2 and c3 and (ci[0] > 0 or ci[1] < 0):
        outcome = "different on average"
    else:
        outcome = "unresolved"
    return dict(outcome=outcome, delta=delta, delta_other_rule=delta_other, partition_sensitivity=sens,
                partition_sensitivity_max_member=sens_member,
                range_x=[float(x.min()), float(x.max())], range_y=[float(y.min()), float(y.max())],
                mean_x=float(x.mean()), mean_y=float(y.mean()), bootstrap_interval=ci, n=[len(x), len(y)],
                conditions={"1_ranges_disjoint": c1, "2_beyond_partition": c2, "3_same_sign": c3})


def run_contrast(data, cid, X, Y, primary, secondary, population):
    pick = (lambda ms: ms) if population == "all" else (lambda ms: [m for m in ms if not m["folded"]])
    mx, my = pick(data[X]["ok"]), pick(data[Y]["ok"])
    ev = data[X]["evaluable"] and data[Y]["evaluable"]
    out = {}
    explore = [x for x in EXPLORATORY if x not in primary and x not in secondary]
    for tier, sites in (("primary", primary), ("secondary", secondary), ("exploratory", explore)):
        if cid.startswith("A_") and tier == "exploratory":
            continue
        for s in sites:
            rng = np.random.default_rng(SEED)        # one fixed stream per site: order-independent
            r = decide(mx, my, s, rng)
            if not ev:
                r["outcome"] = "not evaluable"
            out[f"{tier}:{s}"] = r
    return dict(X=X, Y=Y, population=population, n=[len(mx), len(my)], evaluable=ev, sites=out)


def fmt(r):
    if "delta" not in r:
        return f"{r['outcome']} (n {r['n']})"
    c = r["conditions"]
    return (f"**{r['outcome']}** | Δ {r['delta']:+.2f} (radius-scaled {r['delta_other_rule']:+.2f}) | "
            f"ranges X {r['range_x'][0]:.2f}…{r['range_x'][1]:.2f}, Y {r['range_y'][0]:.2f}…{r['range_y'][1]:.2f} | "
            f"partition {r['partition_sensitivity']:.2f} (pilot-style {r['partition_sensitivity_max_member']:.2f}) | bootstrap (selected set) {r['bootstrap_interval'][0]:+.2f}…{r['bootstrap_interval'][1]:+.2f} | "
            f"1 {'✓' if c['1_ranges_disjoint'] else '✗'} 2 {'✓' if c['2_beyond_partition'] else '✗'} "
            f"3 {'✓' if c['3_same_sign'] else '✗'} | n {r['n']}")


def main(partial):
    slugs = list(NAME)
    data = {s: load(s) for s in slugs}
    missing = {s: d["pending"] for s, d in data.items() if d["pending"]}
    if missing and not partial:
        raise SystemExit(f"members not computed yet: {missing}; --partial for a test run")
    res = {"plan": "Atlas analyses/espmap-sesiidae-001/analysis-plan.md @ 7e34658",
           "verdict_rule": VERDICT_RULE,
           "partial": bool(missing), "pending": missing,
           "molecules": {s: dict(n_ok=len(d["ok"]), n_folded=sum(m["folded"] for m in d["ok"]),
                                 excluded=[{k: m.get(k) for k in ("conformer", "reason", "rg_angstrom", "folded")}
                                           for m in d["excluded"]], evaluable=d["evaluable"]) for s, d in data.items()},
           "contrasts": []}
    for c in CONTRASTS:
        for pop in ("all", "extended"):
            res["contrasts"].append(dict(id=c[0], **run_contrast(data, *c, pop)))
    (OUT / "analysis.json").write_text(json.dumps(res, indent=1, allow_nan=False))
    tag = "PARTIAL — a test of the script, not a result. " if missing else ""
    md = [f"# espmap-sesiidae-001 analysis\n", f"{tag}Plan: {res['plan']}. kcal/mol; Δ = Y − X; "
          f"primary rule nearest-nucleus. Global extrema: no partition, so conditions 2–3 hold trivially.\n",
          PARTITION_NOTE]
    for s, m in res["molecules"].items():
        md.append(f"- {NAME[s]}: {m['n_ok']} members ({m['n_folded']} folded), excluded {len(m['excluded'])}"
                  + ("" if m["evaluable"] else " — NOT EVALUABLE") + (f", pending {missing[s]}" if s in missing else ""))
    for c in res["contrasts"]:
        md.append(f"\n## {c['id']} — {c['population']} members (X = {NAME[c['X']]}, Y = {NAME[c['Y']]}, n {c['n']})\n")
        for k, r in c["sites"].items():
            tier, site = k.split(":", 1)
            if tier == "exploratory":
                continue
            md.append(f"- {tier} **{site}**: {fmt(r)}")
        ex = [k.split(":", 1)[1] for k, r in c["sites"].items() if k.startswith("exploratory") and r["outcome"] == "resolved"]
        if ex:
            md.append(f"- exploratory, never interpreted (plan section 2): non-primary sites meeting the rule: {', '.join(ex)}")
    (OUT / "analysis.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main("--partial" in sys.argv)

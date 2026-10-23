"""A human spot-check of curated records against their PDFs.

Every record was extracted by Claude and re-read by Claude reviewers. This
is the check no model can do for itself: a person reads the source.
Following PAZy's practice (Feuerriegel et al. 2026, NAR), the sample has two
parts:
- a simple random sample of observations, which estimates the error rate
  over the whole Atlas;
- hand-picked hard cases, where a reading was a judgement call. These are
  reported separately, never pooled into the rate.

    python scripts/spot_check.py draw review/spot-check-001 --seed 20261023 --random 24
    python scripts/spot_check.py summarise review/spot-check-001

draw writes sheet.md (what to check, record by record) and results.yaml
(where the checker writes verdicts). It refuses to overwrite either.
summarise reads results.yaml and reports, for the random part, the error
rate with a Wilson 95 % interval, and for the hard part the counts.
It also says which records changed since the draw (sha256 of the YAML).
"""
import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import atlas_validate as av  # noqa: E402

VERDICTS = ("ok", "error", "unclear")

# Hard cases: each one a reading the curator or a reviewer had to decide.
HARD = {
    "spa.obs.eichlinia_cucurbitae.klun_1990.ovipositor":
        "Klun's peaks 2,12 and 11,13 are each one peak; the record carries 2,12 once as the authors' Z,Z-3,13 assignment and leaves 11,13 out",
    "spa.obs.macroscelesia_japona.naka_2007.trap_oh_10_added.test3":
        "Table 1 prints 100 ug twice; the record reads the 13.0 a row as 10 ug from the text's 1:100",
    "spa.obs.macroscelesia_longipes.naka_2007.approach_ald_50_added":
        "Table 2's 'Touched' and 'Attracted' headers are read as swapped",
    "spa.obs.synanthedon_scitula.zhang_2005.trap_ez2_3_added.fig4_wv":
        "means read from a bar chart (Fig. 4C), letters against the base lure",
    "spa.obs.synanthedon_haitangvora.yang_2009.trap_z3z13oh_added.exp2":
        "bar-chart means; the standard read as 500 + 500 ug and the 2 % addition left without an amount",
    "spa.obs.synanthedon_pictipes.tumlinson_1974.bioassay_ez_zz_99_1":
        "Fig. 2 bar heights; 120 ng chosen over the text's 120 ug; significance taken from the text",
    "spa.obs.paranthrene_tabaniformis.zhang_1986.ovipositor":
        "three negatives read from the m/z 266 trace in Fig. 2B, which the text never states",
    "spa.obs.glossosphecia_romanovi.naka_2010.trap_five_components.test_a":
        "the five-component lure recorded as printed, though it conflicts with the gland findings",
    "spa.obs.synanthedon_tenuis.naka_2013.gland":
        "eight negatives from mass chromatograms; two co-eluting isomers deliberately left out",
    "spa.obs.synanthedon_tenuis.yang_2012.gland":
        "the Korean gland result behind the Japan-Korea reversal",
    "spa.obs.synanthedon_tipuliformis.szocs_1990.trap_e3.tasmania_1986":
        "the Tasmanian E3 inhibition later disputed; significance as the paper reports it",
    "spa.obs.vitacea_polistiformis.snow_1987.trap_z3z13_1.moultrie_1986":
        "Duncan letters read across a table where low letters mean low catches",
    "spa.obs.synanthedon_tenuis.tamaki_1977.trap_e3oac_added":
        "a Japanese-language paper; the quotation is the curator's translation",
    "spa.obs.synanthedon_bicingulata.kwon_2021.trap_ratio_2_8.exp1_2018.gongju":
        "lure purity recorded as measured GC-MS peak area, with the paper's isomer claims unverified",
}


def record_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fields(o, records):
    """(field, value) pairs a checker can find in the source, as the record holds them."""
    sh = lambda cid: records["compounds"][cid][1]["names"]["shorthand"]
    amt = lambda q: f"{json.dumps(q['value'])} {q['unit']}" if q else "no amount"
    lure = lambda bl: "; ".join(f"{sh(b['compound'])} {amt(b.get('amount'))}" for b in bl or []) or "none"
    ctx, ev = o.get("context") or {}, o["evidence"]
    rows = [("taxon as the paper names it", ev["taxon_name_as_reported"]),
            ("population / locality", " / ".join(str(ctx.get(k)) for k in ("population", "locality"))),
            ("where in the paper", ev["source_location"])]
    t = o["observation_type"]
    if t == "behavioural_response":
        comp = o.get("comparator") or {}
        r = o.get("response") or {}
        rows += [("trial", json.dumps(ev.get("experiment_id"))),
                 ("treatment lure", lure(o["blend"])),
                 ("comparator", f"{comp.get('description')}" + (f" [{lure(comp['blend'])}]" if comp.get("blend") else "")),
                 ("trap, dispenser", f"{(o.get('trap') or {}).get('design')}, {(o.get('dispenser') or {}).get('design')}"),
                 ("effect, significance", f"{o['effect']}, {o.get('significance')}"),
                 ("response", f"{r.get('treatment_value')} vs {r.get('comparator_value')} {r.get('unit')} ({r.get('qualifier')})" if r else "none")]
    elif t == "chemical_measurement":
        rows += [("context", ", ".join(f"{k} {ctx.get(k)}" for k in ("sex", "mating_status", "behavioural_state", "sampling_unit", "n_individuals", "rearing"))),
                 ("material", o["sample"]["material_as_reported"])]
        for c in o["components"]:
            ms = "; ".join(f"{json.dumps(m['value'])} {m['unit']} {m.get('qualifier', '')}".strip() for m in c.get("measurements") or [])
            rows.append((f"component {sh(c['compound'])}",
                         f"detected {c['detected']}" + (f", {c['identification']}" if c.get("identification") else "")
                         + (f", {c['abundance_class']}" if c.get("abundance_class") else "") + (f", {ms}" if ms else "")))
    else:
        for r in o["responses"]:
            rows.append((f"response {sh(r['compound'])}", f"{r['method']}, {r['response']} ({r['preparation']})"))
    if ev.get("author_statement"):
        rows.append(("quotation (verbatim unless marked)", f"{ev['author_statement']}" + (f" [{ev['author_statement_form']}]" if ev.get("author_statement_form") else "")))
    return rows


def draw(out, seed, n_random):
    out = Path(out)
    if (out / "sheet.md").exists() or (out / "results.yaml").exists():
        raise SystemExit(f"{out} already holds a draw; a sample is drawn once")
    records, findings = av.load_root(ROOT / "data")
    if findings:
        raise SystemExit("records do not load; run atlas_validate.py first")
    obs = records["observations"]
    missing = [k for k in HARD if k not in obs]
    if missing:
        raise SystemExit(f"hard cases with no record: {missing}")
    pool = sorted(k for k in obs if k not in HARD)
    picked = random.Random(seed).sample(pool, n_random)
    sample = [(k, "random", None) for k in sorted(picked)] + [(k, "hard", why) for k, why in HARD.items()]
    refs = records["references"]
    lines = [f"# Spot-check {out.name}", "",
             f"Drawn by `scripts/spot_check.py draw` with seed {seed}: {n_random} observations at random from {len(obs)} "
             f"(simple random sample over all observations, hard cases excluded from the pool), and {len(HARD)} hard cases picked by hand.",
             "", "For each record, open the paper, find the place named under *where in the paper*, and check each row against it. "
             "Write the verdict in `results.yaml`:",
             "- `ok`: every row matches the paper;",
             "- `error`: name the rows that do not, with what the paper says;",
             "- `unclear`: the paper does not settle it; say why.",
             "", "Record what you see, not what you think the curator meant. A record whose notes explain a reading is still checked against the paper.", ""]
    for i, (oid, part, why) in enumerate(sample, start=1):
        path, o = obs[oid]
        ref = refs[o["evidence"]["reference"]][1]
        lines += [f"## {i}. {oid}", "", f"*{part}*" + (f": {why}" if why else ""), "",
                  f"{ref['citation']} [doi:{ref['doi']}](https://doi.org/{ref['doi']})" if ref.get("doi") else ref["citation"], "",
                  "| field | Atlas value |", "|---|---|"]
        lines += [f"| {f} | {str(v).replace('None', 'not given').replace('|', '/')} |" for f, v in fields(o, records)]
        lines += [""]
    results = {"spot_check": out.name, "seed": seed, "n_random": n_random, "checker": None, "date": None,
               "records": [{"observation_id": oid, "part": part, "record_sha256": record_sha(obs[oid][0]),
                            "verdict": None, "wrong_rows": [], "notes": ""} for oid, part, _ in sample]}
    out.mkdir(parents=True, exist_ok=True)
    (out / "sheet.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (out / "results.yaml").write_text(
        "# Fill checker, date and one verdict per record (ok | error | unclear). Do not change observation_id, part or record_sha256.\n"
        + yaml.safe_dump(results, sort_keys=False, allow_unicode=True, width=200), encoding="utf-8", newline="\n")
    return sample


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def summarise(out):
    res = av.strict_load((Path(out) / "results.yaml").read_text(encoding="utf-8"))
    records, _ = av.load_root(ROOT / "data")
    obs = records["observations"]
    lines, problems = [], []
    for r in res["records"]:
        if r["verdict"] not in VERDICTS + (None,):
            problems.append(f"{r['observation_id']}: verdict {r['verdict']!r} is not one of {VERDICTS}")
        if r["verdict"] == "error" and not r["wrong_rows"]:
            problems.append(f"{r['observation_id']}: an error must name its wrong rows")
        if r["observation_id"] not in obs:
            problems.append(f"{r['observation_id']}: no longer a record")
        elif record_sha(obs[r["observation_id"]][0]) != r["record_sha256"]:
            lines.append(f"changed since the draw: {r['observation_id']}")
    for part in ("random", "hard"):
        rows = [r for r in res["records"] if r["part"] == part]
        done = [r for r in rows if r["verdict"] in VERDICTS]
        err = sum(r["verdict"] == "error" for r in done)
        unc = sum(r["verdict"] == "unclear" for r in done)
        s = f"{part}: {len(done)} of {len(rows)} checked, {err} error, {unc} unclear"
        if part == "random" and done:
            judged = len(done) - unc
            lo, hi = wilson(err, judged)
            s += f"; error rate {err}/{judged}, Wilson 95 % interval {100 * lo:.1f}-{100 * hi:.1f} %"
        lines.append(s)
    return lines, problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draw")
    d.add_argument("out")
    d.add_argument("--seed", type=int, required=True)
    d.add_argument("--random", type=int, default=24)
    s = sub.add_parser("summarise")
    s.add_argument("out")
    a = ap.parse_args(argv)
    if a.cmd == "draw":
        sample = draw(a.out, a.seed, a.random)
        print(f"wrote {a.out}/sheet.md and results.yaml: {len(sample)} records")
        return 0
    lines, problems = summarise(a.out)
    for line in lines + problems:
        print(line)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

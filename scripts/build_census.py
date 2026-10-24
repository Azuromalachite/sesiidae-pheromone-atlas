"""The census: what the Atlas holds, counted from the records.

It counts evidence coverage, not what any species "uses". There is no status
field (pheromone, synergist, antagonist, inactive): those labels depend on
population, assay, dose, blend and study (docs/scope-v0.1.md). Every number
is a count of records or of distinct values in them.

- tables/census_taxa.tsv: one row per taxon, with its evidence layers
  (chemistry, behaviour, electrophysiology) and how much each holds, and
  whether it has a genome. The genome is a resource, not evidence, so
  n_evidence_layers leaves it out.
- tables/census_taxon_compound.tsv: one row per taxon and compound that any
  record links, counting observations by what they report about it.
- census.json: the headline numbers.

Behaviour columns count observations whose treatment lure contains the
compound. They say nothing about which component caused the effect; the
evidence classes (docs/evidence-classes.md) isolate true additions.

Called by scripts/build_release.py.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import atlas_validate as av  # noqa: E402
import build_tables as bt  # noqa: E402

LAYERS = {"chemistry": "chemical_measurement", "behaviour": "behavioural_response", "electrophysiology": "electrophysiology"}
TAXA_COLUMNS = ["taxon_id", "species", "n_observations", "n_chemistry", "n_behaviour", "n_electrophysiology", "genome",
                "female_chemistry", "n_evidence_layers", "n_compounds_detected_in_females", "n_compounds_in_treatment_lures",
                "n_compounds_tested_antennally", "n_references", "n_populations"]
CHEMISTRY = ["chemical_detected", "chemical_not_detected", "chemical_not_tested"]
BEHAVIOUR_BUCKETS = ["behaviour_increased_significant", "behaviour_decreased_significant", "behaviour_not_significant",
                     "behaviour_significance_not_tested"]
ANTENNAL = ["antennal_active", "antennal_inconsistent", "antennal_inactive", "antennal_not_tested"]
COUNT_COLUMNS = CHEMISTRY + BEHAVIOUR_BUCKETS + ANTENNAL
PAIR_COLUMNS = ["taxon_id", "compound_id", *CHEMISTRY, "behaviour_n", *BEHAVIOUR_BUCKETS, *ANTENNAL]


def behaviour_bucket(o):
    """Increased or decreased with a significant test; a test that found no difference; or no test
    (not run, not reported, or a catch with no control)."""
    sig = o.get("significance")
    if sig == "significant" and o["effect"] in ("increased", "decreased"):
        return f"behaviour_{o['effect']}_significant"
    if sig == "not_significant":
        return "behaviour_not_significant"
    return "behaviour_significance_not_tested"


def place(o):
    ctx = o.get("context") or {}
    return ctx.get("population") or ctx.get("locality")


def tables(records):
    obs = [o for _, o in records["observations"].values()]
    genomes = {g["taxon"] for _, g in records["genomes"].values()}
    pairs = defaultdict(lambda: dict.fromkeys(COUNT_COLUMNS + ["behaviour_n"], 0))
    for o in obs:
        t = o["observation_type"]
        if t == "chemical_measurement":
            for c in o["components"]:
                key = {True: "chemical_detected", False: "chemical_not_detected"}.get(c["detected"], "chemical_not_tested")
                pairs[(o["taxon"], c["compound"])][key] += 1
        elif t == "behavioural_response":
            for cid in sorted({b["compound"] for b in o["blend"]}):
                p = pairs[(o["taxon"], cid)]
                p["behaviour_n"] += 1
                p[behaviour_bucket(o)] += 1
        else:
            for r in o["responses"]:
                pairs[(o["taxon"], r["compound"])][f"antennal_{r['response']}"] += 1

    taxa = []
    for tid, (_, t) in records["taxa"].items():
        mine = [o for o in obs if o["taxon"] == tid]
        n = {layer: sum(o["observation_type"] == kind for o in mine) for layer, kind in LAYERS.items()}
        mine_pairs = {cid: p for (tx, cid), p in pairs.items() if tx == tid}
        taxa.append({
            "taxon_id": tid, "species": t["accepted_name"], "n_observations": len(mine),
            **{f"n_{layer}": v for layer, v in n.items()},
            "genome": tid in genomes,
            "female_chemistry": any(o["observation_type"] == "chemical_measurement" and (o.get("context") or {}).get("sex") == "female" for o in mine),
            "n_evidence_layers": sum(v > 0 for v in n.values()),
            "n_compounds_detected_in_females": len({c["compound"] for o in mine if o["observation_type"] == "chemical_measurement"
                                                    and (o.get("context") or {}).get("sex") == "female"
                                                    for c in o["components"] if c["detected"] is True}),
            "n_compounds_in_treatment_lures": sum(p["behaviour_n"] > 0 for p in mine_pairs.values()),
            "n_compounds_tested_antennally": sum(sum(p[c] for c in ANTENNAL[:3]) > 0 for p in mine_pairs.values()),
            "n_references": len({o["evidence"]["reference"] for o in mine}),
            "n_populations": len({place(o) for o in mine} - {None}),
        })
    pair_rows = [{"taxon_id": tx, "compound_id": cid, **p} for (tx, cid), p in pairs.items()]
    return taxa, pair_rows


def build(data):
    records, findings = av.load_root(data)
    if findings:
        raise SystemExit("records do not load")
    taxa, pair_rows = tables(records)
    headline = {
        "note": "Counts of what the Atlas holds, from the records. Not a census of Sesiidae pheromones, and no taxon or compound has a status.",
        "taxa": len(records["taxa"]), "compounds": len(records["compounds"]), "references": len(records["references"]),
        "observations": len(records["observations"]), "genomes": len(records["genomes"]),
        "taxon_compound_pairs": len(pair_rows),
        "taxa_with": {
            "female_chemistry": sum(t["female_chemistry"] for t in taxa),
            "behaviour": sum(t["n_behaviour"] > 0 for t in taxa),
            "electrophysiology": sum(t["n_electrophysiology"] > 0 for t in taxa),
            "genome": sum(t["genome"] for t in taxa),
            "two_or_more_evidence_layers": sum(t["n_evidence_layers"] >= 2 for t in taxa),
        },
    }
    return {"tables/census_taxa.tsv": bt.tsv(TAXA_COLUMNS, taxa),
            "tables/census_taxon_compound.tsv": bt.tsv(PAIR_COLUMNS, pair_rows),
            "census.json": json.dumps(headline, sort_keys=True, indent=2, ensure_ascii=False) + "\n"}

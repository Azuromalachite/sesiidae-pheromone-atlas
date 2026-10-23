"""Evidence classes: what the records show about each taxon-compound pair.

One row per taxon, compound and evidence class, with the observations that
support it. Every class is a rule over record fields (docs/evidence-classes.md);
nothing here is an author's claim or the curator's opinion. Contradictions
stay visible: a compound that raised catches in one study and lowered them in
another gets both rows, and nothing is netted out.

Called by scripts/build_release.py, which writes derived/tables/evidence_classes.tsv.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import atlas_validate as av  # noqa: E402
import build_tables as bt  # noqa: E402

COLUMNS = ["taxon_id", "compound_id", "evidence_class", "n_observations", "n_significant", "n_tentative", "populations", "population_match", "observation_ids"]
CLASSES = [
    "female_detected_gland", "female_detected_emission", "female_detected_combined", "female_not_detected",
    "antennal_active", "antennal_inconsistent", "antennal_inactive",
    "attractant_alone", "attractive_lure_component",
    "addition_increased", "addition_decreased", "addition_no_effect",
    "female_pheromone_component",
]
BLANK = re.compile(r"unbaited|blank|control|without a dispenser|hexane|empty|\b0 (mg|ug|micrograms?)\b", re.I)
GLAND = {"gland_extract", "ovipositor_extract"}


def is_blank(comparator):
    return not comparator.get("blend") and bool(BLANK.search(comparator.get("description", "")))


def amounts(blend):
    return {b["compound"]: repr(b.get("amount")) for b in blend or []}


def added_compound(o):
    """The one compound a true addition adds: the treatment is the comparator
    plus one compound, every shared compound at the same amount, in the same
    trap and dispenser. Replacements and removals are not additions."""
    comp = o.get("comparator") or {}
    if not comp.get("blend") or "trap" in comp or "dispenser" in comp:
        return None
    t, c = amounts(o["blend"]), amounts(comp["blend"])
    extra = set(t) - set(c)
    if len(extra) != 1 or set(c) - set(t) or any(t[k] != c[k] for k in c):
        return None
    return next(iter(extra))


def classify(records):
    """{(taxon, compound, class): [(observation_id, significant, tentative)]}"""
    out = defaultdict(list)

    def add(o, cid, cls, significant=False, tentative=False):
        out[(o["taxon"], cid, cls)].append((o["observation_id"], significant, tentative))

    for _, o in records["observations"].values():
        t = o["observation_type"]
        if t == "chemical_measurement" and (o.get("context") or {}).get("sex") == "female":
            mats = set(o["sample"]["materials"])
            where = ("female_detected_combined" if o["sample"]["result_scope"] == "combined"
                     else "female_detected_gland" if mats <= GLAND else "female_detected_emission" if mats == {"effluvium"} else None)
            for c in o["components"]:
                if c["detected"] is True and where:
                    add(o, c["compound"], where, tentative=c.get("identification") == "tentative")
                elif c["detected"] is False:
                    add(o, c["compound"], "female_not_detected")
        elif t == "electrophysiology":
            for r in o["responses"]:
                if r["response"] in ("active", "inconsistent", "inactive"):
                    add(o, r["compound"], f"antennal_{r['response']}")
        elif t == "behavioural_response" and o.get("assay") == "field_trapping":
            sig = o.get("significance") == "significant"
            comp = o.get("comparator") or {}
            if is_blank(comp) and o["effect"] == "increased":
                blend = [b["compound"] for b in o["blend"]]
                if len(blend) == 1:
                    add(o, blend[0], "attractant_alone", sig)
                for cid in blend:
                    add(o, cid, "attractive_lure_component", sig)
            x = added_compound(o)
            if x is not None:
                effect = {"increased": "addition_increased", "decreased": "addition_decreased", "no_effect": "addition_no_effect"}.get(o["effect"])
                if effect:
                    add(o, x, effect, sig)
    # derived: made by the female (gland, emission or combined) and part of a lure that worked in the
    # same taxon. Whether the two lines of evidence come from one population is reported, never assumed
    # (population_match): free-text places can name one population two ways, and a missing place matches nothing.
    for taxon, cid in sorted({(t, c) for t, c, _ in out}):
        chem = [e for k in ("female_detected_gland", "female_detected_emission", "female_detected_combined") for e in out.get((taxon, cid, k), [])]
        beh = [e for k in ("attractive_lure_component", "addition_increased") for e in out.get((taxon, cid, k), [])]
        if chem and beh:
            out[(taxon, cid, "female_pheromone_component")] = sorted(set(chem + beh))
    return out


def population_match(obs, chem_ids, beh_ids):
    """yes: a named place is shared; no: both sides are named and none is shared; unknown: a side has no place."""
    a, b = {place(obs[i]) for i in chem_ids}, {place(obs[i]) for i in beh_ids}
    if (a & b) - {None}:
        return "yes"
    return "unknown" if None in a or None in b else "no"


def place(o):
    ctx = o.get("context") or {}
    return ctx.get("population") or ctx.get("locality")


def rows(records):
    """The evidence rows with typed values: counts as int (None where a count
    does not apply), populations and observation IDs as sorted lists. The
    derived table and the teaching bundle are both built from this list."""
    obs = {k: v[1] for k, v in records["observations"].items()}
    where = lambda oid: place(obs[oid]) or "not given"
    classes = classify(records)
    chem_ids = lambda t, c: {e[0] for k in ("female_detected_gland", "female_detected_emission", "female_detected_combined") for e in classes.get((t, c, k), [])}
    beh_ids = lambda t, c: {e[0] for k in ("attractive_lure_component", "addition_increased") for e in classes.get((t, c, k), [])}
    out = []
    for (taxon, cid, cls), support in classes.items():
        ids = sorted({oid for oid, _, _ in support})
        behaviour = cls.startswith(("attract", "addition")) or cls == "female_pheromone_component"
        chemistry = cls.startswith("female_detected") or cls == "female_pheromone_component"
        out.append({"taxon_id": taxon, "compound_id": cid, "evidence_class": cls, "n_observations": len(ids),
                    "n_significant": len({oid for oid, s, _ in support if s}) if behaviour else None,
                    "n_tentative": len({oid for oid, _, t in support if t}) if chemistry else None,
                    "populations": sorted({where(oid) for oid in ids}),
                    "population_match": population_match(obs, chem_ids(taxon, cid), beh_ids(taxon, cid)) if cls == "female_pheromone_component" else None,
                    "observation_ids": ids})
    return sorted(out, key=lambda r: (r["taxon_id"], r["compound_id"], r["evidence_class"]))


def build(data):
    records, findings = av.load_root(data)
    if findings:
        raise SystemExit("records do not load")
    flat = [{k: ";".join(v) if isinstance(v, list) else v for k, v in r.items()} for r in rows(records)]
    return {"tables/evidence_classes.tsv": bt.tsv(COLUMNS, flat)}

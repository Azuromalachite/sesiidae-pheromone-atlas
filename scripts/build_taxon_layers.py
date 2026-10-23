"""Build derived/taxon_layers.tsv, the taxon x layer matrix, from the records.

Every cell comes from a record. "Not found" comes only from a search record
(data/searches/), never from the absence of other records, so the table
distinguishes curated evidence, a dated search that found nothing, and no
search at all.

    python scripts/build_taxon_layers.py           # write derived/taxon_layers.tsv
    python scripts/build_taxon_layers.py --check   # exit 1 if the committed table is stale

The output depends on the records only: no dates, commits or versions, so
--check is stable across commits (docs/releases-and-occurrences.md).
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import atlas_validate as av  # noqa: E402

OUT = ROOT / "derived" / "taxon_layers.tsv"
COLUMNS = [
    "taxon_id", "species", "genome_status", "assembly_accession", "assembly_name", "assembly_level",
    "annotation_id", "pep_fasta_md5", "pheromone_status", "chemical_materials", "compounds_detected_in_females",
    "compounds_tested_negative", "n_chemical_measurement", "n_behavioural_response", "n_electrophysiology",
    "references", "search_basis",
]


def build(data):
    records, findings = av.load_root(data)
    if findings:
        raise SystemExit("records do not load: " + "; ".join(f.code for f in findings))
    taxa = {tid: t for tid, (_, t) in records["taxa"].items()}
    shorthand = {cid: c["names"]["shorthand"] for cid, (_, c) in records["compounds"].items()}
    genomes, obs, searches = {}, {}, {}
    for _, g in records["genomes"].values():
        genomes.setdefault(g["taxon"], []).append(g)
    for _, o in records["observations"].values():
        obs.setdefault(o["taxon"], []).append(o)
    for _, s in records["searches"].values():
        searches.setdefault(s["layer"], []).append(s)

    rows = []
    for tid, t in sorted(taxa.items(), key=lambda kv: kv[1]["accepted_name"]):
        row = dict.fromkeys(COLUMNS, "")
        row["taxon_id"], row["species"] = tid, t["accepted_name"]
        basis = []

        # genome layer: a record, or a census of the taxon's family that did not find one
        gs = sorted(genomes.get(tid, []), key=lambda g: g["genome_id"])
        if gs:
            g = gs[0]
            a = g["assembly"]
            row["genome_status"] = "assembly"
            row["assembly_accession"] = f"{a['accession']}.{a['version']}"
            row["assembly_name"], row["assembly_level"] = a["name"], a["level"]
            ann = sorted(g.get("annotations") or [], key=lambda x: x["annotation_id"])
            if ann:
                row["annotation_id"] = ann[0]["annotation_id"]
                row["pep_fasta_md5"] = ann[0]["files"]["protein_fasta"]["md5"]
        else:
            census = sorted(s["search_id"] for s in searches.get("genome", [])
                            if s["outcome"] == "census" and s["scope"].get("family") == t["taxonomy"]["family"])
            row["genome_status"] = "no_assembly_in_census" if census else "not_searched"
            basis += census

        # pheromone layer: curated records first, then dated searches
        mine = obs.get(tid, [])
        chem = [o for o in mine if o["observation_type"] == "chemical_measurement"]
        found = {c["compound"] for o in chem for c in o["components"] if c.get("detected") is True}
        negative = {c["compound"] for o in chem for c in o["components"] if c.get("detected") is False}
        n = {k: sum(o["observation_type"] == k for o in mine) for k in ("chemical_measurement", "behavioural_response", "electrophysiology")}
        mine_searches = sorted((s for s in searches.get("pheromone", []) if s["scope"].get("taxon") == tid),
                               key=lambda s: s["date"], reverse=True)
        if found:
            status = "female_chemistry_curated"
        elif n["behavioural_response"]:
            status = "attraction_curated"
        elif mine_searches:
            status = {"found_not_curated": "found_not_curated", "not_found": "searched_not_found"}[mine_searches[0]["outcome"]]
            basis.append(mine_searches[0]["search_id"])
        else:
            status = "not_searched"
        row["pheromone_status"] = status
        row["chemical_materials"] = "; ".join(sorted({m for o in chem for m in o["sample"]["materials"]}))
        row["compounds_detected_in_females"] = "; ".join(sorted(shorthand[c] for c in found))
        row["compounds_tested_negative"] = "; ".join(sorted(shorthand[c] for c in negative))
        row["n_chemical_measurement"] = str(n["chemical_measurement"])
        row["n_behavioural_response"] = str(n["behavioural_response"])
        row["n_electrophysiology"] = str(n["electrophysiology"])
        row["references"] = "; ".join(sorted({o["evidence"]["reference"] for o in mine}))
        row["search_basis"] = "; ".join(basis)
        rows.append(row)
    lines = ["\t".join(COLUMNS)] + ["\t".join(r[c] for c in COLUMNS) for r in rows]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if the committed table differs from a fresh build")
    ap.add_argument("--data", default=str(ROOT / "data"))
    args = ap.parse_args(argv)
    text = build(args.data)
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print(f"{OUT.relative_to(ROOT)} is stale: run python scripts/build_taxon_layers.py", file=sys.stderr)
            return 1
        print("taxon_layers.tsv is current")
        return 0
    OUT.write_bytes(text.encode("utf-8"))
    print(f"wrote {OUT.relative_to(ROOT)} ({text.count(chr(10)) - 1} taxa)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

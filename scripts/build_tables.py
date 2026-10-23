"""Tidy relational tables generated from the records: the Atlas's analytical form.

The YAML records are the normalised source. These tables are views of them:
one entity or one kind of measurement per table, one row per thing, keyed
by Atlas IDs, so they join and load into any data frame or DuckDB/SQLite as
they are. Prose (notes, author statements, unresolved items) stays out: it
is provenance, not data to compute with, and it is in the JSONL exports.

Called by scripts/build_release.py, which writes derived/tables/ and checks
it. Every table is sorted by its key columns; empty cells are missing values.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import atlas_validate as av  # noqa: E402


def cell(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v).replace("\t", " ").replace("\r", " ").replace("\n", " ")


def tsv(columns, rows):
    rows = sorted(rows, key=lambda r: tuple(cell(r.get(c)) for c in columns))
    return "\t".join(columns) + "\n" + "".join("\t".join(cell(r.get(c)) for c in columns) + "\n" for r in rows)


TABLES = {
    "taxa": ["taxon_id", "accepted_name", "authority", "family", "genus", "species", "ncbi_taxid", "gbif"],
    "taxon_synonyms": ["taxon_id", "name", "authority", "source"],
    "references": ["reference_id", "doi", "pmid", "read", "citation"],
    "compounds": ["compound_id", "entity_type", "shorthand", "chain_length", "unsaturation_count", "terminal_group",
                  "canonical_isomeric_smiles", "inchikey", "represents"],
    "compound_double_bonds": ["compound_id", "position", "geometry"],
    "genomes": ["genome_id", "taxon_id", "accession", "version", "assembly_name", "assembly_level", "bioproject",
                "biosample", "specimen_sex", "specimen_locality"],
    "genome_annotations": ["annotation_id", "genome_id", "provider", "method", "geneset", "protein_coding_genes",
                           "protein_fasta_url", "protein_fasta_md5", "gff3_url", "gff3_md5"],
    "searches": ["search_id", "layer", "scope_taxon_id", "scope_family", "date", "outcome", "found_doi", "read"],
    "observations": ["observation_id", "observation_type", "taxon_id", "taxon_name_as_reported", "reference_id",
                     "source_location", "author_statement_form", "sex", "life_stage", "population", "locality",
                     "habitat", "rearing", "mating_status", "behavioural_state", "sampling_unit", "n_individuals"],
    "observation_experiments": ["observation_id", "experiment_id"],
    "chemical_samples": ["observation_id", "material", "result_scope", "material_as_reported"],
    "chemical_components": ["observation_id", "compound_id", "detected", "identification", "abundance_class", "method",
                            "detection_limit_value", "detection_limit_unit"],
    "chemical_values": ["observation_id", "compound_id", "value", "unit", "qualifier", "spread_value", "spread_kind", "method"],
    "behavioural_assays": ["observation_id", "assay", "effect", "significance", "dose_value", "dose_unit",
                           "response_measure", "response_unit", "treatment_value", "comparator_value",
                           "response_qualifier", "comparator_description"],
    "behavioural_stimuli": ["observation_id", "role", "compound_id", "amount_value", "amount_unit", "purity_value",
                            "purity_kind", "purity_basis", "purity_qualifier"],
    "behavioural_setups": ["observation_id", "role", "trap_design", "trap_colour", "trap_L", "trap_a", "trap_b",
                           "trap_supplier", "dispenser_design", "dispenser_description", "differs_from_treatment"],
    "electrophysiology_responses": ["observation_id", "compound_id", "method", "preparation", "response"],
}


def build(data):
    records, findings = av.load_root(data)
    if findings:
        raise SystemExit("records do not load")
    out = {name: [] for name in TABLES}
    for tid, (_, t) in records["taxa"].items():
        tx, ids = t.get("taxonomy") or {}, t.get("identifiers") or {}
        out["taxa"].append({"taxon_id": tid, "accepted_name": t["accepted_name"], "authority": t.get("authority"),
                            "family": tx.get("family"), "genus": tx.get("genus"), "species": tx.get("species"),
                            "ncbi_taxid": ids.get("ncbi_taxid"), "gbif": ids.get("gbif")})
        for s in t.get("synonyms") or []:
            out["taxon_synonyms"].append({"taxon_id": tid, **{k: s.get(k) for k in ("name", "authority", "source")}})
    for rid, (_, r) in records["references"].items():
        out["references"].append({"reference_id": rid, **{k: r.get(k) for k in ("doi", "pmid", "read", "citation")}})
    for cid, (_, c) in records["compounds"].items():
        g = c.get("generated") or {}
        la = g.get("lipid_annotation") or {}
        out["compounds"].append({"compound_id": cid, "entity_type": c["entity_type"], "shorthand": c["names"]["shorthand"],
                                 "chain_length": la.get("chain_length"), "unsaturation_count": la.get("unsaturation_count"),
                                 "terminal_group": la.get("terminal_group"),
                                 "canonical_isomeric_smiles": g.get("canonical_isomeric_smiles"),
                                 "inchikey": g.get("inchikey"), "represents": c.get("represents")})
        for db in la.get("double_bonds") or []:
            out["compound_double_bonds"].append({"compound_id": cid, **db})
    for gid, (_, g) in records["genomes"].items():
        a, sp = g["assembly"], g.get("specimen") or {}
        out["genomes"].append({"genome_id": gid, "taxon_id": g["taxon"], "accession": a["accession"], "version": a["version"],
                               "assembly_name": a["name"], "assembly_level": a["level"], "bioproject": g.get("bioproject"),
                               "biosample": g.get("biosample"), "specimen_sex": sp.get("sex"), "specimen_locality": sp.get("locality")})
        for an in g.get("annotations") or []:
            f = an["files"]
            out["genome_annotations"].append({
                "annotation_id": an["annotation_id"], "genome_id": gid, "provider": an["provider"], "method": an["method"],
                "geneset": an["geneset"], "protein_coding_genes": an.get("protein_coding_genes"),
                "protein_fasta_url": f["protein_fasta"]["url"], "protein_fasta_md5": f["protein_fasta"]["md5"],
                "gff3_url": (f.get("gff3") or {}).get("url"), "gff3_md5": (f.get("gff3") or {}).get("md5")})
    for sid, (_, s) in records["searches"].items():
        out["searches"].append({"search_id": sid, "layer": s["layer"], "scope_taxon_id": s["scope"].get("taxon"),
                                "scope_family": s["scope"].get("family"), "date": s["date"], "outcome": s["outcome"],
                                "found_doi": s.get("found_doi"), "read": s.get("read")})
    for oid, (_, o) in records["observations"].items():
        ev, ctx = o["evidence"], o.get("context") or {}
        out["observations"].append({
            "observation_id": oid, "observation_type": o["observation_type"], "taxon_id": o["taxon"],
            "taxon_name_as_reported": ev["taxon_name_as_reported"], "reference_id": ev["reference"],
            "source_location": ev["source_location"], "author_statement_form": ev.get("author_statement_form") or ("verbatim" if ev.get("author_statement") else None),
            **{k: ctx.get(k) for k in ("sex", "life_stage", "population", "locality", "habitat", "rearing",
                                       "mating_status", "behavioural_state", "sampling_unit", "n_individuals")}})
        exps = ev.get("experiment_id")
        for e in (exps if isinstance(exps, list) else [exps] if exps else []):
            out["observation_experiments"].append({"observation_id": oid, "experiment_id": e})
        if o["observation_type"] == "chemical_measurement":
            smp = o["sample"]
            for m in smp["materials"]:
                out["chemical_samples"].append({"observation_id": oid, "material": m, "result_scope": smp["result_scope"],
                                                "material_as_reported": smp["material_as_reported"]})
            for c in o["components"]:
                dl = c.get("detection_limit") or {}
                out["chemical_components"].append({
                    "observation_id": oid, "compound_id": c["compound"], "detected": c["detected"],
                    "identification": c.get("identification"), "abundance_class": c.get("abundance_class"),
                    "method": c.get("method"), "detection_limit_value": dl.get("value"), "detection_limit_unit": dl.get("unit")})
                for m in c.get("measurements") or []:
                    sp = m.get("spread") or {}
                    out["chemical_values"].append({
                        "observation_id": oid, "compound_id": c["compound"], "value": m["value"], "unit": m["unit"],
                        "qualifier": m.get("qualifier"), "spread_value": sp.get("value"), "spread_kind": sp.get("kind"),
                        "method": m.get("method") or c.get("method")})
        elif o["observation_type"] == "behavioural_response":
            comp, dose, resp = o.get("comparator") or {}, o.get("dose") or {}, o.get("response") or {}
            out["behavioural_assays"].append({
                "observation_id": oid, "assay": o["assay"], "effect": o["effect"], "significance": o.get("significance"),
                "dose_value": dose.get("value"), "dose_unit": dose.get("unit"), "response_measure": resp.get("measure"),
                "response_unit": resp.get("unit"), "treatment_value": resp.get("treatment_value"),
                "comparator_value": resp.get("comparator_value"), "response_qualifier": resp.get("qualifier"),
                "comparator_description": comp.get("description")})
            for role, blend in (("treatment", o.get("blend")), ("comparator", comp.get("blend"))):
                for b in blend or []:
                    a, p = b.get("amount") or {}, b.get("purity") or {}
                    out["behavioural_stimuli"].append({
                        "observation_id": oid, "role": role, "compound_id": b["compound"], "amount_value": a.get("value"),
                        "amount_unit": a.get("unit"), "purity_value": p.get("value"), "purity_kind": p.get("kind"),
                        "purity_basis": p.get("basis"), "purity_qualifier": p.get("qualifier")})
            for role in ("treatment", "comparator"):
                if role == "comparator" and not comp:
                    continue
                own = comp if role == "comparator" else o
                trap = own.get("trap", o.get("trap")) or {}
                disp = own.get("dispenser", o.get("dispenser")) or {}
                if not trap and not disp:
                    continue
                lab = trap.get("colour_lab") or {}
                out["behavioural_setups"].append({
                    "observation_id": oid, "role": role, "trap_design": trap.get("design"), "trap_colour": trap.get("colour"),
                    "trap_L": lab.get("L"), "trap_a": lab.get("a"), "trap_b": lab.get("b"), "trap_supplier": trap.get("supplier"),
                    "dispenser_design": disp.get("design"), "dispenser_description": disp.get("description"),
                    "differs_from_treatment": (role == "comparator" and ("trap" in comp or "dispenser" in comp))})
        elif o["observation_type"] == "electrophysiology":
            for r in o["responses"]:
                out["electrophysiology_responses"].append({"observation_id": oid, "compound_id": r["compound"],
                                                            "method": r["method"], "preparation": r["preparation"],
                                                            "response": r["response"]})
    return {f"tables/{name}.tsv": tsv(TABLES[name], rows) for name, rows in out.items()}

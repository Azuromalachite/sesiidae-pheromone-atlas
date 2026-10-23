"""Build a teaching bundle (spa.teaching/0) for one case in teaching/cases/.

A case names records; this script says what they show, and only from their
fields: every statement is assembled from lure and comparator, setup
differences, dose, effect, significance, response values and qualifier,
detections, negatives with their limits, untested compounds, measurements
with their qualifiers, and antennal readings. Nothing is rounded or left
out. The case's own words (case_title, case_label) are the only text not
built from records, and they are named as such. Teaching prose (acts,
prompts, site labels) belongs to the consumer.

build_release.py writes derived/teaching/<case_id>.json with no
atlas_version, like the rest of derived/. An exported copy names the commit
or tag it was built from:

    python scripts/export_teaching_bundle.py sesiidae-homework-1 --out bundle.json            # atlas_version = HEAD
    python scripts/export_teaching_bundle.py sesiidae-homework-1 --out bundle.json --atlas-version v0.1.0
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import atlas_validate as av  # noqa: E402

BUNDLE = "spa.teaching/0"
SCHEMA_VERSION = "0.1"
UNIT = {"picogram": "pg", "nanogram": "ng", "microgram": "ug", "milligram": "mg", "gram": "g", "ratio_part": "parts"}


def num(v):
    """A number exactly as the record holds it (JSON form: no rounding, no exponent invented)."""
    return json.dumps(v)


def amount(q):
    return f"{num(q['value'])} {UNIT[q['unit']]}" if q else "amount not given"


def lure(blend, shorthand):
    return " + ".join(f"{shorthand(b['compound'])} {amount(b.get('amount'))}" for b in blend or [])


def where(ctx):
    parts = [ctx[k] for k in ("population", "locality") if ctx.get(k)]
    return "; ".join(parts) or "place not given"


def measured(m):
    s = f"{num(m['value'])} {m['unit']}"
    if m.get("spread"):
        s += f" +- {num(m['spread']['value'])} {m['spread']['kind']}"
    return s + f" {m.get('qualifier', 'as_reported')}"


def statement(o, shorthand, taxon_name):
    head = f"{taxon_name} ({where(o.get('context') or {})})"
    t = o["observation_type"]
    if t == "behavioural_response":
        comp = o.get("comparator") or {}
        desc = comp.get("description", "no comparator")
        vs = f"{lure(comp['blend'], shorthand)} ({desc})" if comp.get("blend") else desc
        differs = [part for part in ("trap", "dispenser") if part in comp]
        s = f"{head}, {o['assay']}: {lure(o['blend'], shorthand)} vs {vs}"
        if differs:
            s += f" (comparator differs in {' and '.join(differs)})"
        if o.get("dose"):
            s += f"; dose {amount(o['dose'])}"
        s += f": {o['effect']}, {o.get('significance', 'significance not given')}"
        r = o.get("response")
        if r:
            tv = num(r["treatment_value"]) if r.get("treatment_value") is not None else "not given"
            cv = num(r["comparator_value"]) if r.get("comparator_value") is not None else "not given"
            s += f"; {tv} vs {cv} {r['unit']} ({r['measure']}, {r.get('qualifier', 'as_reported')})"
        return s
    if t == "chemical_measurement":
        pos, neg, untested = [], [], []
        for c in o["components"]:
            name = shorthand(c["compound"])
            notes = [c["identification"]] if c.get("identification") else []
            if c.get("abundance_class"):
                notes.append(c["abundance_class"])
            notes += [measured(m) for m in c.get("measurements") or []]
            if c["detected"] is True:
                pos.append(name + (f" [{'; '.join(notes)}]" if notes else ""))
            elif c["detected"] is False:
                lim = c.get("detection_limit")
                neg.append(name + (f" [limit {amount(lim)}]" if lim else ""))
            else:
                untested.append(name)
        s = f"{head}, {'+'.join(o['sample']['materials'])}: detected {', '.join(pos) or 'none'}"
        if neg:
            s += f"; not detected {', '.join(neg)}"
        if untested:
            s += f"; not tested {', '.join(untested)}"
        return s
    return f"{head}: " + "; ".join(f"{r['method']} {shorthand(r['compound'])} {r['response']} ({r['preparation']})" for r in o["responses"])


def blend_entries(blend):
    return [{"atlas_id": b["compound"], "amount": b.get("amount"), "purity": b.get("purity")} for b in blend or []]


def summary(o, records, shorthand):
    taxa, refs = records["taxa"], records["references"]
    tax = taxa[o["taxon"]][1]
    ev = o["evidence"]
    ref = refs[ev["reference"]][1]
    ctx = o.get("context") or {}
    out = {"observation_id": o["observation_id"], "observation_type": o["observation_type"],
           "taxon": {"atlas_id": o["taxon"], "accepted_name": tax["accepted_name"], "name_as_reported": ev["taxon_name_as_reported"]},
           "reference": {"atlas_id": ev["reference"], "citation": ref["citation"], "doi": ref.get("doi")},
           "context": dict(ctx),
           "evidence": {"author_statement": ev.get("author_statement"), "author_statement_form": ev.get("author_statement_form"),
                        "unresolved": list(ev.get("unresolved") or []), "atlas_notes": ev.get("notes")},
           "experiment_id": ev.get("experiment_id"), "source_location": ev["source_location"]}
    t = o["observation_type"]
    if t == "behavioural_response":
        comp = o.get("comparator") or {}
        out.update(assay=o["assay"], treatment=blend_entries(o["blend"]), trap=o.get("trap"), dispenser=o.get("dispenser"), dose=o.get("dose"),
                   comparator={"description": comp.get("description"), "blend": blend_entries(comp.get("blend")) or None,
                               "trap": comp.get("trap"), "dispenser": comp.get("dispenser")},
                   outcome={"effect": o["effect"], "significance": o.get("significance"), "response": o.get("response")})
    elif t == "chemical_measurement":
        out.update(materials=o["sample"]["materials"],
                   components=[{"atlas_id": c["compound"], "detected": c["detected"], "identification": c.get("identification"),
                                "abundance_class": c.get("abundance_class"), "method": c.get("method"),
                                "measurements": c.get("measurements") or [], "detection_limit": c.get("detection_limit")}
                               for c in o["components"]])
    else:
        out["responses"] = [{"atlas_id": r["compound"], "method": r["method"], "preparation": r["preparation"], "response": r["response"]}
                            for r in o["responses"]]
    out["statement"] = statement(o, shorthand, tax["accepted_name"])
    return out


def roles(o, cid):
    """How a compound occurs in one observation, from the record's own fields."""
    out = []
    if any(b.get("compound") == cid for b in o.get("blend") or []):
        out.append("treatment")
    if any(b.get("compound") == cid for b in (o.get("comparator") or {}).get("blend") or []):
        out.append("comparator")
    for c in o.get("components") or []:
        if c.get("compound") == cid:
            out.append({True: "detected", False: "not_detected"}.get(c["detected"], "not_tested"))
    for r in o.get("responses") or []:
        if r.get("compound") == cid:
            out.append(f"antennal_{r['response']}")
    return out


def ensembles(computed, compound_ids):
    """The ensembles the gate read (av.ensemble_paths): never a path it skipped."""
    out = []
    for path in av.ensemble_paths(computed):
        ens = json.loads(path.read_text(encoding="utf-8"))
        if ens.get("atlas_id") in compound_ids:
            out.append({"atlas_id": ens["atlas_id"], "protocol": ens["protocol"],
                        "path": path.relative_to(Path(computed).parent).as_posix(),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return out


def build(data, case_id, atlas_version=None, validated=False):
    """The bundle for teaching/cases/<case_id>.yaml beside the data root."""
    findings = [] if validated else av.validate(data)
    if findings:
        raise SystemExit(f"records or cases do not validate ({len(findings)} findings); run atlas_validate.py first")
    if case_id not in cases(data):
        raise SystemExit(f"{case_id!r} is not a case in teaching/cases/; only gated cases are exported")
    records, _ = av.load_root(data)
    computed, teaching = av.siblings(data)
    case = av.strict_load((teaching / "cases" / f"{case_id}.yaml").read_text(encoding="utf-8"))
    comps = records["compounds"]
    shorthand = lambda cid: comps[cid][1]["names"]["shorthand"]
    obs = {oid: records["observations"][oid][1] for oid in case["observations"]}
    entries = {oid: summary(o, records, shorthand) for oid, o in obs.items()}
    bundle = {
        "bundle": BUNDLE, "case_id": case["case_id"], "case_title": case["title"], "schema_version": SCHEMA_VERSION,
        "compounds": [{"atlas_id": cid, "inchikey": comps[cid][1]["generated"]["inchikey"],
                       "shorthand": comps[cid][1]["names"]["shorthand"], "systematic": comps[cid][1]["names"].get("systematic"),
                       "occurrences": [{"observation_id": oid, "roles": roles(o, cid)} for oid, o in obs.items() if roles(o, cid)]}
                      for cid in case["compounds"]],
        "observations": [entries[oid] for oid in case["observations"]],
        "comparisons": [{"case_label": c["label"], "observation_ids": [c["a"], c["b"]],
                         "observed_contrast": {"a": entries[c["a"]]["statement"], "b": entries[c["b"]]["statement"]}}
                        for c in case["comparisons"]],
        "espmap": ensembles(computed, set(case["compounds"])),
    }
    if atlas_version is not None:
        bundle["atlas_version"] = atlas_version
    return bundle


def dumps(bundle):
    return json.dumps(bundle, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


def cases(data):
    """The case files the gate reads: plain files, not symlinks."""
    _, teaching = av.siblings(data)
    d = teaching / "cases"
    if not d.is_dir() or d.is_symlink() or teaching.is_symlink():
        return []
    return sorted(p.stem for p in d.glob("*.yaml") if p.is_file() and not p.is_symlink())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("case_id")
    ap.add_argument("--out", required=True, help="where to write the bundle JSON")
    ap.add_argument("--atlas-version", help="commit or tag to record; default: git HEAD")
    a = ap.parse_args(argv)
    version = a.atlas_version or subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    Path(a.out).write_text(dumps(build(ROOT / "data", a.case_id, version)), encoding="utf-8", newline="\n")
    print(f"wrote {a.out} ({a.case_id} at {version})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Validate Sesiidae Pheromone Atlas records.

    python atlas_validate.py [ROOT]                 # validate ROOT (default: data/)
    python atlas_validate.py [ROOT] --write-generated

ROOT holds one YAML record per file in taxa/, compounds/, observations/,
genomes/ and references/. Head groups are read from data/headgroups.yaml.

What is checked, in order (concept §12, §13, §35):

1. every record against its JSON Schema;
2. ids unique, and every cross-reference resolves;
3. compounds: the heavy-atom map rule (all-or-none, unique, never on a
   hydrogen -- the same three conditions as espmap's gate, implemented here
   so that Atlas CI never needs espmap installed); chain maps 1..n along one
   unbranched carbon path; the head group exactly as in headgroups.yaml;
   every chain double bond's position and E/Z read from the structure by map
   number and compared with the shorthand; and the generated block
   regenerated and compared at the same generator versions;
4. observations: semantic rules the schema cannot express.

Exit status 1 if any error is found. Every error carries a code, so tests
can assert *which* check failed, not just that something did.
"""

import argparse
import copy
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
SCHEMAS = HERE / "schemas"
HEADGROUPS = HERE / "data" / "headgroups.yaml"

KINDS = {  # directory -> (schema file, id field)
    "taxa": ("taxon.schema.json", "taxon_id"),
    "references": ("reference.schema.json", "reference_id"),
    "compounds": ("compound.schema.json", "compound_id"),
    "genomes": ("genome.schema.json", "genome_id"),
    "observations": ("observation.schema.json", "observation_id"),
}

HEAD_MAP_MIN = 101
SHORTHAND = re.compile(r"^(?:(?P<dbs>[EZ][0-9]+(?:,[EZ][0-9]+)*)-)?(?P<n>[0-9]+):(?P<head>[A-Za-z]+)$")


@dataclass
class Finding:
    code: str
    path: str
    message: str

    def __str__(self):
        return f"{self.code}  {self.path}: {self.message}"


# ---------------------------------------------------------------- loading

def load_root(root):
    """{kind: {id: (path, record)}} plus findings for unreadable files."""
    records, findings = {k: {} for k in KINDS}, []
    for kind, (_, id_field) in KINDS.items():
        for path in sorted((Path(root) / kind).glob("*.yaml")):
            try:
                rec = yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as e:
                findings.append(Finding("YAML", str(path), str(e).splitlines()[0]))
                continue
            rid = rec.get(id_field) if isinstance(rec, dict) else None
            if rid in records[kind]:
                findings.append(Finding("DUPLICATE_ID", str(path), f"{rid} also in {records[kind][rid][0]}"))
                continue
            records[kind][rid if rid is not None else str(path)] = (str(path), rec)
    return records, findings


def load_headgroups(path=HEADGROUPS):
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    out = {}
    for token, g in raw.items():
        atoms = {int(m): el for m, el in g["atoms"].items()}
        bonds = {frozenset((int(a), int(b))): float(o) for a, b, o in g["bonds"]}
        out[token] = {"name": g["name"], "atoms": atoms, "bonds": bonds}
    return out


# ---------------------------------------------------------------- schema

def schema_findings(records):
    out = []
    for kind, (schema_file, _) in KINDS.items():
        validator = Draft202012Validator(json.loads((SCHEMAS / schema_file).read_text(encoding="utf-8")))
        for path, rec in records[kind].values():
            for err in sorted(validator.iter_errors(rec), key=lambda e: list(e.path)):
                where = "/".join(str(p) for p in err.path) or "(record)"
                out.append(Finding("SCHEMA", path, f"{where}: {err.message[:200]}"))
    return out


# ---------------------------------------------------------------- taxon names

def taxon_name_findings(records):
    """A name string is never identity. Two concepts may not share an accepted
    name, and a synonym that spells another concept's accepted name must say
    whose name it is: both authorities given, and different. 'bicingulata'
    is the reason -- Sesia bicingulata Rebel, 1910 sits under S. myopaeformis
    in GBIF, while Synanthedon bicingulata is the East Asian species."""
    out = []
    accepted = {}
    for path, t in records["taxa"].values():
        name = t.get("accepted_name")
        if name in accepted:
            out.append(Finding("TAXON_NAME_DUPLICATE", path, f"{name!r} is also the accepted name of {accepted[name][1]}"))
        else:
            accepted[name] = (t, t.get("taxon_id"))
    for path, t in records["taxa"].values():
        for syn in t.get("synonyms") or []:
            other = accepted.get(syn.get("name"))
            if other is None or other[0] is t:
                continue
            a, b = syn.get("authority"), other[0].get("authority")
            if not a or not b or a == b:
                out.append(Finding("NAME_AMBIGUOUS", path,
                                   f"synonym {syn.get('name')!r} spells the accepted name of {other[1]}; "
                                   "give both authorities so the two usages can be told apart"))
    return out


# ---------------------------------------------------------------- references

def reference_findings(records):
    """Every id a record points at must exist, and point at the right kind."""
    out = []
    taxa, refs, comps = records["taxa"], records["references"], records["compounds"]

    def need(ok, path, what):
        if not ok:
            out.append(Finding("REF_MISSING", path, what))

    for path, g in records["genomes"].values():
        need(g.get("taxon") in taxa, path, f"taxon {g.get('taxon')!r} has no record")
        a = g.get("assembly") or {}
        want = f".{a.get('accession')}.{a.get('version')}"
        if not str(g.get("genome_id", "")).endswith(want):
            out.append(Finding("GENOME_ID", path, f"genome_id must end with the assembly accession.version {want[1:]!r}"))
    for path, c in comps.values():
        if c.get("compound_class") == "computational_model":
            need(c.get("represents") in comps, path, f"represents {c.get('represents')!r} has no record")
    for path, o in records["observations"].values():
        need(o.get("taxon") in taxa, path, f"taxon {o.get('taxon')!r} has no record")
        need((o.get("evidence") or {}).get("reference") in refs, path,
             f"reference {(o.get('evidence') or {}).get('reference')!r} has no record")
        for cid in observed_compounds(o):
            need(cid in comps, path, f"compound {cid!r} has no record")
            if cid in comps and comps[cid][1].get("compound_class") == "computational_model":
                out.append(Finding("OBS_MODEL_COMPOUND", path,
                                   f"{cid} is a computational model; observations are of real compounds"))
    return out


def observed_compounds(o):
    ids = [c.get("compound") for c in o.get("components") or []]
    ids += [b.get("compound") for b in o.get("blend") or []]
    ids += [b.get("compound") for b in (o.get("comparator") or {}).get("blend") or []]
    ids += [r.get("compound") for r in o.get("responses") or []]
    return [i for i in ids if i is not None]


# ---------------------------------------------------------------- observations

def observation_findings(records):
    """Rules the schema cannot say: amounts belong to detections, a
    detection limit belongs to a negative, and a comparator differs from the
    treatment in its blend or its trap."""
    out = []
    for path, o in records["observations"].values():
        for c in o.get("components") or []:
            name = c.get("compound")
            if c.get("measurements") and c.get("detected") is not True:
                out.append(Finding("OBS_FIELD_CONFLICT", path,
                                   f"{name}: measurements given but detected is {c.get('detected')!r}"))
            if "detection_limit" in c and c.get("detected") is not False:
                out.append(Finding("OBS_FIELD_CONFLICT", path,
                                   f"{name}: detection_limit belongs to detected: false"))
        comp = o.get("comparator") or {}
        if (o.get("blend") is not None and comp.get("blend") == o.get("blend")
                and comp.get("trap", o.get("trap")) == o.get("trap")):
            out.append(Finding("OBS_FIELD_CONFLICT", path,
                               "comparator has the treatment's blend and trap: nothing was compared"))
    return out


# ---------------------------------------------------------------- compounds

def parse_shorthand(text):
    """'E2,Z13-18:OAc' -> (18, [(2, 'E'), (13, 'Z')], 'OAc'), or None."""
    m = SHORTHAND.match(text or "")
    if not m:
        return None
    dbs = [(int(t[1:]), t[0]) for t in (m["dbs"] or "").split(",") if t]
    return int(m["n"]), sorted(dbs), m["head"]


def map_rule_findings(smiles, path):
    """All-or-none on heavy atoms, unique, never on a hydrogen. The SMILES is
    read with hydrogens kept: RDKit's default parser merges [H:105] into an
    implicit hydrogen and loses the map without a word."""
    from rdkit import Chem
    ps = Chem.SmilesParserParams()
    ps.removeHs = False
    raw = Chem.MolFromSmiles(smiles, ps)
    if raw is None:
        return [Finding("SMILES", path, f"RDKit cannot parse {smiles!r}")]
    out = []
    h_maps = [a.GetAtomMapNum() for a in raw.GetAtoms() if a.GetAtomicNum() == 1 and a.GetAtomMapNum()]
    heavy = [a.GetAtomMapNum() for a in raw.GetAtoms() if a.GetAtomicNum() > 1]
    mapped = [m for m in heavy if m]
    if h_maps:
        out.append(Finding("MAPPED_HYDROGEN", path, f"atom map(s) {h_maps} on hydrogen; map the heavy atom only"))
    if len(mapped) < len(heavy):
        out.append(Finding("PARTIAL_ATOM_MAP", path, f"{len(mapped)} of {len(heavy)} heavy atoms carry a map; map every heavy atom"))
    dup = sorted({m for m in mapped if mapped.count(m) > 1})
    if dup:
        out.append(Finding("DUPLICATE_ATOM_MAP", path, f"atom map(s) {dup} used more than once"))
    return out


def structure_findings(rec, path, headgroups):
    """Chain, head group and double bonds, all read by map number."""
    from rdkit import Chem
    from rdkit.Chem import rdCIPLabeler

    sh = parse_shorthand((rec.get("names") or {}).get("shorthand"))
    if sh is None:
        return [Finding("SHORTHAND_SYNTAX", path, f"cannot parse shorthand {(rec.get('names') or {}).get('shorthand')!r}")]
    n, dbs, head = sh
    if head not in headgroups:
        return [Finding("HEADGROUP_UNKNOWN", path, f"head group {head!r} is not in data/headgroups.yaml ({', '.join(headgroups)})")]
    hg = headgroups[head]

    mol = Chem.MolFromSmiles(rec["mapped_smiles"])
    by_map = {a.GetAtomMapNum(): a for a in mol.GetAtoms()}
    out = []

    if any(a.GetFormalCharge() for a in mol.GetAtoms()) or any(a.GetNumRadicalElectrons() for a in mol.GetAtoms()):
        out.append(Finding("CHARGE", path, "v0.1 compounds are neutral closed-shell molecules"))

    chain = sorted(m for m in by_map if m < HEAD_MAP_MIN)
    heads = sorted(m for m in by_map if m >= HEAD_MAP_MIN)
    if chain != list(range(1, n + 1)):
        out.append(Finding("CHAIN_MAPS", path, f"chain maps are {chain}, expected 1..{n} from the shorthand"))
        return out
    for m in chain:
        if by_map[m].GetSymbol() != "C":
            out.append(Finding("CHAIN_MAPS", path, f"map {m} is {by_map[m].GetSymbol()}, not a chain carbon"))
            return out

    def bond(a, b):
        return mol.GetBondBetweenAtoms(by_map[a].GetIdx(), by_map[b].GetIdx())

    # one unbranched path: consecutive maps bonded, and nothing else between chain atoms
    for m in chain[:-1]:
        if bond(m, m + 1) is None:
            out.append(Finding("CHAIN_MAPS", path, f"C{m} and C{m + 1} are not bonded"))
    for i in chain:
        for j in chain:
            if j > i + 1 and bond(i, j) is not None:
                out.append(Finding("CHAIN_MAPS", path, f"C{i} is bonded to C{j}: the chain is branched or cyclic"))
    if out:
        return out

    # head group: exactly the table's atoms and bonds, attached only at C1
    got_atoms = {m: by_map[m].GetSymbol() for m in heads}
    if got_atoms != hg["atoms"]:
        out.append(Finding("HEADGROUP_MISMATCH", path,
                           f"{head} expects head-group atoms {hg['atoms']}, structure has {got_atoms}"))
        return out
    hg_maps = set(heads) | {1}
    got_bonds = {}
    for b in mol.GetBonds():
        ma, mb = b.GetBeginAtom().GetAtomMapNum(), b.GetEndAtom().GetAtomMapNum()
        if ma in hg_maps and mb in hg_maps and (ma >= HEAD_MAP_MIN or mb >= HEAD_MAP_MIN):
            got_bonds[frozenset((ma, mb))] = b.GetBondTypeAsDouble()
        elif (ma >= HEAD_MAP_MIN) != (mb >= HEAD_MAP_MIN):
            out.append(Finding("HEADGROUP_MISMATCH", path, f"head-group atom bonded to chain C{min(ma, mb)}; only C1 may carry it"))
    if got_bonds != hg["bonds"]:
        fmt = lambda d: sorted((tuple(sorted(k)), v) for k, v in d.items())
        out.append(Finding("HEADGROUP_MISMATCH", path, f"{head} expects bonds {fmt(hg['bonds'])}, structure has {fmt(got_bonds)}"))
    if out:
        return out

    # chain bonds: only single and double, double bonds where the shorthand says, with its geometry
    rdCIPLabeler.AssignCIPLabels(mol)
    found = []
    for m in chain[:-1]:
        b = bond(m, m + 1)
        order = b.GetBondTypeAsDouble()
        if order not in (1.0, 2.0):
            out.append(Finding("BOND_ORDER", path, f"C{m}-C{m + 1} has bond order {order}; v0.1 chains have single and double bonds only"))
            continue
        if order == 2.0:
            # in an unbranched chain each sp2 carbon carries one chain neighbour and one H,
            # so the CIP label is the chain geometry
            label = b.GetProp("_CIPCode") if b.HasProp("_CIPCode") else None
            if label not in ("E", "Z"):
                out.append(Finding("STEREO_UNSPECIFIED", path, f"C{m}=C{m + 1} has no E/Z in the structure"))
                continue
            found.append((m, label))
    if out:
        return out
    if found != dbs:
        fmt = lambda xs: ",".join(f"{g}{p}" for p, g in xs) or "none"
        out.append(Finding("DOUBLE_BOND_MISMATCH", path, f"shorthand says {fmt(dbs)}, structure has {fmt(found)}"))
    return out


def generated_block(rec):
    """The fields CI regenerates. Maps are stripped before canonicalising, so
    the canonical SMILES and InChI describe the molecule, not its numbering."""
    from rdkit import Chem, rdBase
    from rdkit.Chem import inchi

    mol = Chem.MolFromSmiles(rec["mapped_smiles"])
    for a in mol.GetAtoms():
        a.SetAtomMapNum(0)
    n, dbs, head = parse_shorthand(rec["names"]["shorthand"])
    ii = inchi.MolToInchi(mol)
    return {
        "generator": {"rdkit": rdBase.rdkitVersion, "inchi": inchi.GetInchiVersion()},
        "canonical_isomeric_smiles": Chem.MolToSmiles(mol),
        "inchi": ii,
        "inchikey": inchi.InchiToInchiKey(ii),
        "lipid_annotation": {
            "chain_length": n,
            "unsaturation_count": len(dbs),
            "double_bonds": [{"position": p, "geometry": g} for p, g in dbs],
            "terminal_group": load_headgroups()[head]["name"],
        },
    }


def generated_findings(rec, path):
    want = generated_block(rec)
    have = rec.get("generated")
    if not have:
        return [Finding("GENERATED_MISSING", path, "no generated block; run --write-generated")]
    if have.get("generator") != want["generator"]:
        return [Finding("GENERATOR_VERSION", path,
                        f"generated with {have.get('generator')}, this run is {want['generator']}; "
                        "regenerate every record in one dedicated commit")]
    stale = [k for k in want if k != "generator" and have.get(k) != want[k]]
    if stale:
        return [Finding("GENERATED_STALE", path, f"{', '.join(stale)} differ from the structure; run --write-generated")]
    return []


def compound_findings(records, headgroups):
    out = []
    for path, rec in records["compounds"].values():
        if not isinstance(rec.get("mapped_smiles"), str):
            continue  # the schema already reported it
        maps = map_rule_findings(rec["mapped_smiles"], path)
        out += maps
        if maps:
            continue
        struct = structure_findings(rec, path, headgroups)
        out += struct
        if not struct:
            out += generated_findings(rec, path)
    return out


# ---------------------------------------------------------------- driver

def validate(root):
    records, findings = load_root(root)
    findings += schema_findings(records)
    if findings:  # cross-checks on malformed records only add noise
        return findings
    findings += taxon_name_findings(records)
    findings += reference_findings(records)
    findings += observation_findings(records)
    findings += compound_findings(records, load_headgroups())
    return findings


def write_generated(root):
    """Fill or refresh every compound's generated block. Only for compounds
    whose structure passes; a broken record is reported, never papered over."""
    records, _ = load_root(root)
    headgroups, written, refused = load_headgroups(), 0, []
    for path, rec in records["compounds"].values():
        problems = map_rule_findings(rec.get("mapped_smiles", ""), path) or structure_findings(rec, path, headgroups)
        if problems:
            refused += problems
            continue
        new = copy.deepcopy(rec)
        new["generated"] = generated_block(rec)
        if new != rec:
            Path(path).write_text(yaml.safe_dump(new, sort_keys=False, allow_unicode=True, width=200), encoding="utf-8")
            written += 1
    return written, refused


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", nargs="?", default=str(HERE / "data"))
    ap.add_argument("--write-generated", action="store_true",
                    help="regenerate the generated block of every valid compound")
    a = ap.parse_args(argv)
    if a.write_generated:
        written, refused = write_generated(a.root)
        for f in refused:
            print(f)
        print(f"{written} compound record(s) written, {len(refused)} refused")
        return 1 if refused else 0
    findings = validate(a.root)
    for f in findings:
        print(f)
    print(f"{len(findings)} error(s)" if findings else "ok")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

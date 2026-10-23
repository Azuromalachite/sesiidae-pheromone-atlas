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
4. observations: semantic rules the schema cannot express;
5. the data root's siblings, when present: computed/espmap/ (espmap
   ensembles indexed against Atlas compounds, checksummed, no NPZ in git)
   and teaching/cases/ (which records a teaching bundle may assert).

Exit status 1 if any error is found. Every error carries a code, so tests
can assert *which* check failed, not just that something did.
"""

import argparse
import copy
import hashlib
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
    "searches": ("search.schema.json", "search_id"),
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

class DuplicateKey(yaml.YAMLError):
    pass


class StrictLoader(yaml.SafeLoader):
    """SafeLoader that refuses a repeated mapping key. PyYAML's default keeps
    the last value silently, so `taxon:` typed twice would reach the schema as
    one valid taxon and the first entry would vanish before any check ran."""

    def construct_mapping(self, node, deep=False):
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise DuplicateKey(f"duplicate key {key!r} at line {key_node.start_mark.line + 1}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def strict_load(text):
    return yaml.load(text, Loader=StrictLoader)


def uncovered_files(root):
    """YAML under root that no record kind reads: a record nobody validates
    must not look like source data. Subdirectories of a kind are read."""
    root = Path(root)
    covered = {root / "headgroups.yaml"}
    for kind in KINDS:
        covered |= set((root / kind).rglob("*.yaml"))
    return sorted(p for p in root.rglob("*") if p.suffix in (".yaml", ".yml") and p not in covered)


def nonfinite(node, where=""):
    """Paths of NaN or infinite numbers: YAML reads .nan and .inf as floats,
    and JSON Schema's minimum and maximum never reject NaN."""
    if isinstance(node, float) and (node != node or node in (float("inf"), float("-inf"))):
        return [where or "(record)"]
    if isinstance(node, dict):
        return [p for k, v in node.items() for p in nonfinite(v, f"{where}/{k}")]
    if isinstance(node, list):
        return [p for i, v in enumerate(node) for p in nonfinite(v, f"{where}/{i}")]
    return []


def load_root(root):
    """{kind: {id: (path, record)}} plus findings for unreadable files."""
    records, findings = {k: {} for k in KINDS}, []
    for path in uncovered_files(root):
        findings.append(Finding("DATA_OUTSIDE_GATE", str(path), "YAML outside every record directory (or .yml): it would never be validated"))
    for kind, (_, id_field) in KINDS.items():
        for path in sorted((Path(root) / kind).rglob("*.yaml")):
            try:
                rec = strict_load(path.read_text(encoding="utf-8"))
            except DuplicateKey as e:
                findings.append(Finding("YAML_DUPLICATE_KEY", str(path), str(e)))
                continue
            except (yaml.YAMLError, UnicodeDecodeError) as e:
                findings.append(Finding("YAML", str(path), str(e).splitlines()[0]))
                continue
            for where in nonfinite(rec):
                findings.append(Finding("NUMBER_NOT_FINITE", str(path), f"{where}: NaN or infinity is not a measurement"))
            rid = rec.get(id_field) if isinstance(rec, dict) else None
            if rid in records[kind]:
                findings.append(Finding("DUPLICATE_ID", str(path), f"{rid} also in {records[kind][rid][0]}"))
                continue
            records[kind][rid if rid is not None else str(path)] = (str(path), rec)
    return records, findings


def load_headgroups(path=HEADGROUPS):
    raw = strict_load(Path(path).read_text(encoding="utf-8"))
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

    seen_annot = {}
    for path, g in records["genomes"].values():
        need(g.get("taxon") in taxa, path, f"taxon {g.get('taxon')!r} has no record")
        a = g.get("assembly") or {}
        want = f".{a.get('accession')}.{a.get('version')}"
        if not str(g.get("genome_id", "")).endswith(want):
            out.append(Finding("GENOME_ID", path, f"genome_id must end with the assembly accession.version {want[1:]!r}"))
        prefix = f"spa.annot.{str(g.get('taxon', '')).removeprefix('spa.tax.')}."
        for a in g.get("annotations") or []:
            aid = str(a.get("annotation_id", ""))
            if not aid.startswith(prefix):
                out.append(Finding("ANNOT_ID", path, f"{aid}: annotation_id must start with {prefix}"))
            elif aid in seen_annot:
                out.append(Finding("ANNOT_ID", path, f"{aid} also in {seen_annot[aid]}"))
            seen_annot.setdefault(aid, path)
    for path, s in records["searches"].values():
        scope = s.get("scope") or {}
        if "taxon" in scope:
            need(scope["taxon"] in taxa, path, f"taxon {scope['taxon']!r} has no record")
        slug = scope.get("taxon", "").removeprefix("spa.tax.") or str(scope.get("family", "")).lower()
        want = f"spa.search.{slug}.{s.get('layer')}.{str(s.get('date', '')).replace('-', '_')}"
        if s.get("search_id") != want:
            out.append(Finding("SEARCH_ID", path, f"search_id must be {want}, from its scope, layer and date"))
    for path, c in comps.values():
        if c.get("entity_type") == "computational_model":
            need(c.get("represents") in comps, path, f"represents {c.get('represents')!r} has no record")
    for path, o in records["observations"].values():
        need(o.get("taxon") in taxa, path, f"taxon {o.get('taxon')!r} has no record")
        ev = o.get("evidence") or {}
        reported = ev.get("taxon_name_as_reported")
        if o.get("taxon") in taxa and reported:
            t = taxa[o["taxon"]][1]
            known = {t.get("accepted_name")} | {s.get("name") for s in t.get("synonyms") or []}
            if reported not in known:
                out.append(Finding("NAME_AS_REPORTED", path,
                                   f"{reported!r} is neither the accepted name nor a listed synonym of {o['taxon']}; add the synonym, with its source"))
        exps = ev.get("experiment_id")
        prefix = f"spa.exp.{str(ev.get('reference', '')).removeprefix('spa.ref.')}."
        for e in (exps if isinstance(exps, list) else [exps] if exps else []):
            if not str(e).startswith(prefix):
                out.append(Finding("EXP_ID", path, f"{e}: an experiment belongs to its paper and must start with {prefix}"))
        need((o.get("evidence") or {}).get("reference") in refs, path,
             f"reference {(o.get('evidence') or {}).get('reference')!r} has no record")
        for cid in observed_compounds(o):
            need(cid in comps, path, f"compound {cid!r} has no record")
            if cid in comps and comps[cid][1].get("entity_type") == "computational_model":
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

def same_blend(a, b):
    """Blends are sets of components: listing order means nothing."""
    key = lambda item: json.dumps(item, sort_keys=True)
    return sorted(map(key, a)) == sorted(map(key, b))


def observation_findings(records):
    """Rules the schema cannot say: an observation_id is built from its taxon
    and reference, amounts belong to detections, a
    detection limit belongs to a negative, and a comparator differs from the
    treatment in its blend, trap or dispenser."""
    out = []
    for path, o in records["observations"].values():
        oid = str(o.get("observation_id", ""))
        want = (f"spa.obs.{str(o.get('taxon', '')).removeprefix('spa.tax.')}."
                f"{str((o.get('evidence') or {}).get('reference', '')).removeprefix('spa.ref.')}.")
        if not oid.startswith(want) or len(oid) == len(want):
            out.append(Finding("OBS_ID", path, f"observation_id must be {want}<what>, from its taxon and reference"))
        for c in o.get("components") or []:
            name = c.get("compound")
            if c.get("measurements") and c.get("detected") is not True:
                out.append(Finding("OBS_FIELD_CONFLICT", path,
                                   f"{name}: measurements given but detected is {c.get('detected')!r}"))
            if "detection_limit" in c and c.get("detected") is not False:
                out.append(Finding("OBS_FIELD_CONFLICT", path,
                                   f"{name}: detection_limit belongs to detected: false"))
        comp = o.get("comparator") or {}
        if (o.get("blend") is not None and comp.get("blend") is not None
                and same_blend(comp["blend"], o["blend"])
                and comp.get("trap", o.get("trap")) == o.get("trap")
                and comp.get("dispenser", o.get("dispenser")) == o.get("dispenser")):
            out.append(Finding("OBS_FIELD_CONFLICT", path,
                               "comparator has the treatment's blend, trap and dispenser: nothing was compared"))
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


# ---------------------------------------------------------------- identity

def canonical_structure(mapped_smiles):
    """Canonical isomeric SMILES with maps stripped: the molecular graph, not its numbering."""
    from rdkit import Chem
    mol = Chem.MolFromSmiles(mapped_smiles)
    if mol is None:
        return None
    for a in mol.GetAtoms():
        a.SetAtomMapNum(0)
    return Chem.MolToSmiles(mol)


def identity_findings(records):
    """IDs are unique by construction; real things must be too. Two Atlas IDs
    for one molecule, paper, assembly or taxon split the graph silently."""
    out = []

    def unique(kind, label, key_of):
        seen = {}
        for path, rec in records[kind].values():
            key = key_of(rec)
            if key in (None, ""):
                continue
            if key in seen:
                out.append(Finding("IDENTITY_DUPLICATE", path, f"same {label} {key!r} as {seen[key]}"))
            else:
                seen[key] = path

    unique("compounds", "structure", lambda c: canonical_structure(c["mapped_smiles"]) if isinstance(c.get("mapped_smiles"), str) else None)
    unique("compounds", "InChIKey", lambda c: (c.get("generated") or {}).get("inchikey"))
    unique("references", "DOI", lambda r: str(r["doi"]).strip().lower() if r.get("doi") else None)
    unique("references", "PMID", lambda r: r.get("pmid"))
    unique("genomes", "assembly", lambda g: f"{(g.get('assembly') or {}).get('accession')}.{(g.get('assembly') or {}).get('version')}")
    unique("taxa", "NCBI taxid", lambda t: (t.get("identifiers") or {}).get("ncbi_taxid"))
    unique("taxa", "GBIF key", lambda t: (t.get("identifiers") or {}).get("gbif"))
    return out


def entry_findings(records):
    """One observation may not contradict itself: a compound appears once per
    component list and once per blend, an antennal reading once per compound,
    method and preparation, and an abundance class only on a detection."""
    out = []
    for path, o in records["observations"].values():
        def dup(items, key, where):
            seen = set()
            for it in items or []:
                k = key(it)
                if k in seen:
                    out.append(Finding("OBS_DUPLICATE_ENTRY", path, f"{where}: {k} appears twice"))
                seen.add(k)
        dup(o.get("components"), lambda c: c.get("compound"), "components")
        dup(o.get("blend"), lambda b: b.get("compound"), "blend")
        dup((o.get("comparator") or {}).get("blend"), lambda b: b.get("compound"), "comparator blend")
        dup(o.get("responses"), lambda r: (r.get("compound"), r.get("method"), r.get("preparation")), "responses")
        for c in o.get("components") or []:
            if "abundance_class" in c and c.get("detected") is not True:
                out.append(Finding("OBS_FIELD_CONFLICT", path,
                                   f"{c.get('compound')}: abundance_class belongs to detected: true"))
    return out


# ---------------------------------------------------------------- computed/espmap

ENSEMBLE_SCHEMA = "spa.espmap_ensemble/0"
ESPMAP_RECORD = "espmap.record/1"
SLUG = re.compile(r"^[a-z0-9_]+$")
PROTOCOL = re.compile(r"^[a-z0-9_.-]+$")
CONFORMER_FILE = re.compile(r"^conf_[0-9]{2,}\.json$")


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


SUMS_LINE = re.compile(r"^([0-9a-f]{64})  (\S+)$")
MAX_RECORD_BYTES = 1_000_000  # a C18 espmap record with its site table is about 175 kB; surfaces belong in NPZ assets


class StrictJSONError(ValueError):
    pass


def _no_duplicate_keys(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise StrictJSONError(f"duplicate key {k!r}")
        out[k] = v
    return out


def _no_constant(name):
    raise StrictJSONError(f"{name} is not a number JSON allows")


def strict_json(path):
    """JSON as the gate reads it: UTF-8, no repeated key (the last would win
    silently, as in YAML), no NaN or Infinity (not JSON, and every comparison
    with NaN is false). Raises StrictJSONError with the reason."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        raise StrictJSONError(f"not UTF-8: {e.reason}") from None
    try:
        return json.loads(text, object_pairs_hook=_no_duplicate_keys, parse_constant=_no_constant)
    except json.JSONDecodeError as e:
        raise StrictJSONError(f"not JSON: {e}") from None


def read_sums(path):
    """({name: sha256}, problems) from a SHA256SUMS file: UTF-8, exactly
    '<64 lowercase hex>  <name>' per line, each name once, as sha256sum writes it."""
    out, problems = {}, []
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return out, ["not UTF-8"]
    for n, line in enumerate(lines, start=1):
        m = SUMS_LINE.match(line)
        if not m:
            problems.append(f"line {n} is not '<sha256>  <name>'")
        elif m[2] in out:
            problems.append(f"line {n}: {m[2]} listed twice")
        else:
            out[m[2]] = m[1]
    return out, problems


def computed_layout(computed):
    """({(slug, protocol): [names]}, findings) for every file under computed/.
    espmap computes; the Atlas keeps an index of what was computed for its
    compounds. NPZ surfaces are refused here: they ship as release assets.
    A symlink anywhere, the root included, is refused: what the gate does not
    walk, nothing may read."""
    out, dirs = [], {}
    computed = Path(computed)
    if computed.is_symlink():
        return dirs, [Finding("COMPUTED_LAYOUT", str(computed), "computed/ must not be a symlink")]
    if not computed.is_dir():
        return dirs, [Finding("COMPUTED_LAYOUT", str(computed), "computed must be a directory")]
    for p in sorted(computed.rglob("*")):
        if p.is_symlink():
            out.append(Finding("COMPUTED_LAYOUT", str(p), "symlinks are not allowed under computed/"))
            continue
        if not p.is_file():
            continue
        rel = p.relative_to(computed).parts
        if p.suffix.lower() == ".npz":
            out.append(Finding("COMPUTED_NPZ_IN_GIT", str(p), "NPZ surfaces ship as release-bundle assets; keep only their sha256 in ensemble.json"))
            continue
        ok = (len(rel) in (4, 5) and rel[0] == "espmap" and SLUG.match(rel[1]) and PROTOCOL.match(rel[2])
              and ((len(rel) == 4 and rel[3] in ("ensemble.json", "SHA256SUMS"))
                   or (len(rel) == 5 and rel[3] == "conformers" and CONFORMER_FILE.match(rel[4]))))
        if not ok:
            out.append(Finding("COMPUTED_LAYOUT", str(p),
                               "computed/ holds only espmap/<slug>/<protocol>/{ensemble.json, SHA256SUMS, conformers/conf_NN.json}, "
                               "slug [a-z0-9_], protocol [a-z0-9_.-]"))
            continue
        dirs.setdefault((rel[1], rel[2]), []).append("/".join(rel[3:]))
    return dirs, out


def ensemble_paths(computed):
    """The ensemble.json files the gate reads, in order. The exporter and the
    bundle builder use this list, so they never read a path the gate skipped.
    Both run the full validator first, so a listed ensemble has also passed."""
    if not Path(computed).exists():
        return []
    dirs, _ = computed_layout(computed)
    return [Path(computed) / "espmap" / slug / proto / "ensemble.json"
            for (slug, proto), names in sorted(dirs.items()) if "ensemble.json" in names]


def _as_dict(x):
    return x if isinstance(x, dict) else {}


def member_findings(rec_path, rec, m, ens, aid, want):
    """One member record against its ensemble: the same espmap protocol
    (analysis_key and key_fields.analysis, espmap's own normalised form), the
    same espmap version, espmap's own verification, a neutral closed-shell
    input, the stated geometry, and the Atlas molecule."""
    out = []
    if rec.get("analysis_key") != ens["analysis_key"] or _as_dict(rec.get("key_fields")).get("analysis") != ens["analysis"]:
        out.append(Finding("COMPUTED_PROTOCOL", str(rec_path), "analysis_key or key_fields.analysis differs from the ensemble's: another protocol"))
    if _as_dict(rec.get("provenance")).get("espmap_version") != ens["espmap"]["version"]:
        out.append(Finding("COMPUTED_PROTOCOL", str(rec_path),
                           f"computed with espmap {_as_dict(rec.get('provenance')).get('espmap_version')!r}, the ensemble says {ens['espmap']['version']!r}"))
    inp, geom = _as_dict(rec.get("input")), _as_dict(rec.get("geometry"))
    if inp.get("structure_verified") is not True or _as_dict(rec.get("validity")).get("input") is not True:
        out.append(Finding("COMPUTED_RECORD", str(rec_path), "espmap did not verify this structure (input.structure_verified and validity.input must be true)"))
    if any(x.get(k) != 0 for x in (inp, geom) for k in ("charge", "spin")):
        out.append(Finding("COMPUTED_RECORD", str(rec_path), "v0.1 compounds are neutral closed-shell: input and geometry charge and spin must be 0"))
    if geom.get("sha1") != m["geometry_sha1"]:
        out.append(Finding("COMPUTED_MEMBER", str(rec_path), f"geometry.sha1 {geom.get('sha1')!r} is not the member's geometry_sha1"))
    smiles = inp.get("computed_smiles")
    if want is not None and (not isinstance(smiles, str) or canonical_structure(smiles) != want):
        out.append(Finding("COMPUTED_STRUCTURE", str(rec_path), f"input.computed_smiles {smiles!r} is not {aid}: this conformer is another molecule"))
    return out


def computed_findings(computed, records, crossref=True):
    """crossref=False when the records themselves failed: the layout,
    checksums and record shapes are still checked, the links to records not."""
    computed = Path(computed)
    if not computed.exists() and not computed.is_symlink():
        return []
    dirs, out = computed_layout(computed)
    validator = Draft202012Validator(json.loads((SCHEMAS / "espmap-ensemble.schema.json").read_text(encoding="utf-8")))
    by_slug = {}
    for cid in records["compounds"]:
        by_slug.setdefault(str(cid).split(".")[-1], []).append(cid)
    for (slug, proto), names in sorted(dirs.items()):
        d = computed / "espmap" / slug / proto
        present = sorted(n for n in names if n != "SHA256SUMS")
        if "SHA256SUMS" not in names:
            out.append(Finding("COMPUTED_CHECKSUM", str(d), "no SHA256SUMS"))
        else:
            listed, bad_lines = read_sums(d / "SHA256SUMS")
            out += [Finding("COMPUTED_CHECKSUM", str(d / "SHA256SUMS"), b) for b in bad_lines]
            for n in present:
                if n not in listed:
                    out.append(Finding("COMPUTED_CHECKSUM", str(d / n), "not listed in SHA256SUMS"))
                elif file_sha256(d / n) != listed[n]:
                    out.append(Finding("COMPUTED_CHECKSUM", str(d / n), "sha256 differs from SHA256SUMS"))
            for n in sorted(set(listed) - set(present)):
                out.append(Finding("COMPUTED_CHECKSUM", str(d / n), "listed in SHA256SUMS but absent"))
        if "ensemble.json" not in names:
            out.append(Finding("COMPUTED_SCHEMA", str(d), "no ensemble.json"))
            continue
        path = d / "ensemble.json"
        try:
            ens = strict_json(path)
        except StrictJSONError as e:
            out.append(Finding("COMPUTED_SCHEMA", str(path), str(e)))
            continue
        errs = sorted(validator.iter_errors(ens), key=lambda e: list(e.path))
        if errs:
            out += [Finding("COMPUTED_SCHEMA", str(path), f"{'/'.join(map(str, e.path)) or '(record)'}: {e.message[:200]}") for e in errs]
            continue
        aid = ens["atlas_id"]
        want = None   # the record's canonical structure, when the record can be trusted
        if aid.split(".")[-1] != slug:
            out.append(Finding("COMPUTED_ID", str(path), f"atlas_id {aid} does not match the directory slug {slug!r}"))
            continue
        if crossref:
            if aid not in records["compounds"]:
                out.append(Finding("COMPUTED_ID", str(path), f"{aid} has no compound or model record"))
                continue
            if len(by_slug.get(slug, [])) > 1:
                out.append(Finding("COMPUTED_ID", str(path), f"slug {slug!r} names {sorted(by_slug[slug])}; rename one record"))
            target = records["compounds"][aid][1]
            got, want = canonical_structure(ens["smiles"]), canonical_structure(target.get("mapped_smiles", ""))
            if got is None or got != want:
                out.append(Finding("COMPUTED_STRUCTURE", str(path),
                                   f"smiles canonicalises to {got!r}, {aid} is {want!r}: a different molecule was computed"))
            key = (target.get("generated") or {}).get("inchikey")
            if ens["inchikey"] != key:
                out.append(Finding("COMPUTED_INCHIKEY", str(path), f"InChIKey {ens['inchikey']} is not {aid}'s {key}: a different molecule was computed"))
        if ens["protocol"] != proto:
            out.append(Finding("COMPUTED_PROTOCOL", str(path), f"protocol {ens['protocol']!r} is not the directory {proto!r}"))
        seen, records_used, npz_hashes, geometries = set(), set(), set(), set()
        for m in ens["members"]:
            c = m["conformer"]
            if c in seen:
                out.append(Finding("COMPUTED_MEMBER", str(path), f"{c} listed twice"))
            seen.add(c)
            if m["npz_sha256"] in npz_hashes:
                out.append(Finding("COMPUTED_MEMBER", str(path), f"{c}: npz_sha256 repeats another member's; one surface cannot be two conformers"))
            npz_hashes.add(m["npz_sha256"])
            if m["geometry_sha1"] in geometries:
                out.append(Finding("COMPUTED_MEMBER", str(path), f"{c}: geometry_sha1 repeats another member's; one geometry cannot be two conformers"))
            geometries.add(m["geometry_sha1"])
            if m["record"] != f"conformers/{c}.json" or m["npz"] != f"{c}.npz":
                out.append(Finding("COMPUTED_MEMBER", str(path), f"{c}: record must be conformers/{c}.json and npz {c}.npz"))
                continue
            records_used.add(m["record"])
            rec_path = d / m["record"]
            if not rec_path.is_file():
                out.append(Finding("COMPUTED_MEMBER", str(path), f"{c}: {m['record']} is missing"))
                continue
            if file_sha256(rec_path) != m["record_sha256"]:
                out.append(Finding("COMPUTED_CHECKSUM", str(rec_path), "sha256 differs from record_sha256 in ensemble.json"))
            if rec_path.stat().st_size > MAX_RECORD_BYTES:
                out.append(Finding("COMPUTED_RECORD", str(rec_path), f"larger than {MAX_RECORD_BYTES} bytes: surfaces belong in NPZ assets, not in git"))
                continue
            try:
                rec = strict_json(rec_path)
            except StrictJSONError as e:
                out.append(Finding("COMPUTED_RECORD", str(rec_path), str(e)))
                continue
            if not isinstance(rec, dict) or rec.get("schema") != ESPMAP_RECORD:
                out.append(Finding("COMPUTED_RECORD", str(rec_path), f"not an {ESPMAP_RECORD}"))
                continue
            out += member_findings(rec_path, rec, m, ens, aid, want)
        for n in present:
            if n.startswith("conformers/") and n not in records_used:
                out.append(Finding("COMPUTED_MEMBER", str(d / n), "conformer record not listed in ensemble.json members"))
    return out


# ---------------------------------------------------------------- teaching/cases

def teaching_findings(teaching, records, crossref=True):
    """A teaching case may name only records that exist, compounds that occur
    in its own observations, and comparisons between two of its observations,
    each pair once. crossref=False when the records themselves failed."""
    teaching = Path(teaching)
    if not teaching.exists() and not teaching.is_symlink():
        return []
    if teaching.is_symlink() or (teaching / "cases").is_symlink():
        return [Finding("TEACH_LAYOUT", str(teaching), "teaching/ and teaching/cases/ must not be symlinks")]
    if not teaching.is_dir():
        return [Finding("TEACH_LAYOUT", str(teaching), "teaching must be a directory")]
    out = []
    validator = Draft202012Validator(json.loads((SCHEMAS / "teaching-case.schema.json").read_text(encoding="utf-8")))
    obs = records["observations"]
    for p in sorted(teaching.rglob("*")):
        if p.is_symlink():
            out.append(Finding("TEACH_LAYOUT", str(p), "symlinks are not allowed under teaching/"))
            continue
        if not p.is_file():
            continue
        rel = p.relative_to(teaching).parts
        if not (len(rel) == 2 and rel[0] == "cases" and p.suffix == ".yaml"):
            out.append(Finding("TEACH_LAYOUT", str(p), "teaching/ holds only cases/<case_id>.yaml"))
            continue
        try:
            case = strict_load(p.read_text(encoding="utf-8"))
        except DuplicateKey as e:
            out.append(Finding("YAML_DUPLICATE_KEY", str(p), str(e)))
            continue
        except (yaml.YAMLError, UnicodeDecodeError) as e:
            out.append(Finding("YAML", str(p), str(e).splitlines()[0]))
            continue
        errs = sorted(validator.iter_errors(case), key=lambda e: list(e.path))
        if errs:
            out += [Finding("TEACH_SCHEMA", str(p), f"{'/'.join(map(str, e.path)) or '(record)'}: {e.message[:200]}") for e in errs]
            continue
        if case["case_id"] != p.stem:
            out.append(Finding("TEACH_CASE_ID", str(p), f"case_id {case['case_id']!r} must equal the file name {p.stem!r}"))
        listed = case["observations"]
        if crossref:
            for oid in listed:
                if oid not in obs:
                    out.append(Finding("TEACH_REF", str(p), f"observation {oid} has no record"))
            observed = {cid for oid in listed if oid in obs for cid in observed_compounds(obs[oid][1])}
            for cid in case["compounds"]:
                if cid not in records["compounds"]:
                    out.append(Finding("TEACH_REF", str(p), f"compound {cid} has no record"))
                elif cid not in observed:
                    out.append(Finding("TEACH_COMPOUND_UNOBSERVED", str(p), f"{cid} occurs in none of the case's observations"))
        pairs = set()
        for c in case["comparisons"]:
            pair = frozenset((c["a"], c["b"]))
            if pair in pairs:
                out.append(Finding("TEACH_COMPARISON", str(p), f"{c['label']!r}: {c['a']} and {c['b']} are already compared"))
            pairs.add(pair)
            if c["a"] == c["b"]:
                out.append(Finding("TEACH_COMPARISON", str(p), f"{c['label']!r} compares {c['a']} with itself"))
            for side in ("a", "b"):
                if c[side] not in listed:
                    out.append(Finding("TEACH_COMPARISON", str(p), f"{c['label']!r}: {c[side]} is not among the case's observations"))
    return out


# ---------------------------------------------------------------- driver

def siblings(root):
    """computed/ and teaching/ sit beside the data root, as in the repository."""
    parent = Path(root).resolve().parent
    return parent / "computed", parent / "teaching"


def validate(root):
    records, findings = load_root(root)
    findings += schema_findings(records)
    if not findings:  # cross-checks on malformed records only add noise
        findings += taxon_name_findings(records)
        findings += reference_findings(records)
        findings += observation_findings(records)
        findings += compound_findings(records, load_headgroups())
        findings += identity_findings(records)
        findings += entry_findings(records)
    # the siblings are always checked; their links to records only when the records are sound
    sound = not findings
    computed, teaching = siblings(root)
    findings += computed_findings(computed, records, crossref=sound)
    findings += teaching_findings(teaching, records, crossref=sound)
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

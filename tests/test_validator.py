"""The validator must accept the good fixtures and refuse every bad one, for
the stated reason. A gate that has never been seen to fail is not a gate.

Each directory under fixtures/bad/ overlays one or more files on a copy of
fixtures/good/ and names, in EXPECT, the error code it must produce.
"""

import json
import re
import shutil
from pathlib import Path

import pytest
import yaml

import atlas_validate as av

FIX = Path(__file__).parent / "fixtures"
GOOD = FIX / "good"
ROOT = Path(__file__).parent.parent
BAD_CASES = sorted(p.name for p in (FIX / "bad").iterdir() if p.is_dir())


def codes(root):
    return {f.code for f in av.validate(root)}


def overlay(tmp_path, case):
    root = tmp_path / "root"
    shutil.copytree(GOOD, root)
    for src in (p for p in (FIX / "bad" / case).rglob("*") if p.is_file() and p.name != "EXPECT"):
        dst = root / src.relative_to(FIX / "bad" / case)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)
    return root


def test_good_fixtures_pass():
    assert av.validate(GOOD) == []


def test_every_bad_case_names_its_expected_code():
    assert len(BAD_CASES) >= 20
    for case in BAD_CASES:
        assert (FIX / "bad" / case / "EXPECT").read_text().strip(), case


@pytest.mark.parametrize("case", BAD_CASES)
def test_bad_fixture_fails_for_the_stated_reason(tmp_path, case):
    """EXPECT lists every code the fixture must produce, one per line, and
    nothing else may appear: a one-mutation fixture that starts failing for a
    second reason no longer proves the first."""
    expected = {line.strip() for line in (FIX / "bad" / case / "EXPECT").read_text().splitlines() if line.strip()}
    got = codes(overlay(tmp_path, case))
    assert got == expected, f"{case}: expected exactly {sorted(expected)}, got {sorted(got) or 'no error'}"


# ---- the mutation test from concept §12: flip every E/Z, in the name and in the structure

def compounds_with_double_bonds():
    out = []
    for path in sorted((GOOD / "compounds").glob("*.yaml")):
        rec = yaml.safe_load(path.read_text(encoding="utf-8"))
        _, dbs, _ = av.parse_shorthand(rec["names"]["shorthand"])
        out += [(path.name, pos) for pos, _ in dbs]
    return out


MUTATIONS = compounds_with_double_bonds()


def rewrite(root, name, fn):
    path = root / "compounds" / name
    rec = yaml.safe_load(path.read_text(encoding="utf-8"))
    fn(rec)
    path.write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")


@pytest.mark.parametrize("name,pos", MUTATIONS)
def test_flipping_geometry_in_the_shorthand_is_caught(tmp_path, name, pos):
    root = tmp_path / "root"
    shutil.copytree(GOOD, root)

    def flip(rec):
        new = re.sub(rf"(?<![0-9])([EZ]){pos}(?![0-9])",
                     lambda m: ("Z" if m[1] == "E" else "E") + str(pos), rec["names"]["shorthand"])
        assert new != rec["names"]["shorthand"]
        rec["names"]["shorthand"] = new

    rewrite(root, name, flip)
    assert "DOUBLE_BOND_MISMATCH" in codes(root)


@pytest.mark.parametrize("name,pos", MUTATIONS)
def test_flipping_geometry_in_the_structure_is_caught(tmp_path, name, pos):
    root = tmp_path / "root"
    shutil.copytree(GOOD, root)

    def flip(rec):
        # the bond direction written after C(pos+1) sets this double bond's geometry
        pat = rf"=\[CH:{pos + 1}\]([/\\])"
        assert re.search(pat, rec["mapped_smiles"]), "fixture style changed"
        rec["mapped_smiles"] = re.sub(
            pat, lambda m: f"=[CH:{pos + 1}]" + ("\\" if m[1] == "/" else "/"), rec["mapped_smiles"])

    rewrite(root, name, flip)
    assert "DOUBLE_BOND_MISMATCH" in codes(root)


# ---- regeneration

def test_generator_version_change_is_its_own_error(tmp_path):
    root = tmp_path / "root"
    shutil.copytree(GOOD, root)
    rewrite(root, "e2_z13_18_oac.yaml", lambda r: r["generated"]["generator"].update(rdkit="2020.03.1"))
    assert codes(root) == {"GENERATOR_VERSION"}


def test_write_generated_fills_a_missing_block(tmp_path):
    root = tmp_path / "root"
    shutil.copytree(GOOD, root)
    rewrite(root, "z3_z13_18_oh.yaml", lambda r: r.update(generated=None))
    assert "GENERATED_MISSING" in codes(root)
    written, refused = av.write_generated(root)
    assert (written, refused) == (1, [])
    assert av.validate(root) == []


def test_write_generated_refuses_a_broken_structure(tmp_path):
    root = overlay(tmp_path, "structure_ez_flipped")
    written, refused = av.write_generated(root)
    assert written == 0 and {f.code for f in refused} == {"DOUBLE_BOND_MISMATCH"}


# ---- the head-group table itself

def test_headgroup_oxygen_keeps_map_101():
    """The oxygen on C1 is 101 in every head group, so it keeps its number
    from acid to alcohol to acetate (concept §11)."""
    for token, g in av.load_headgroups().items():
        on_c1 = [m for pair in g["bonds"] for m in pair if 1 in pair and m != 1]
        assert 101 in on_c1 and g["atoms"][101] == "O", token


# ---- derived tables are a function of the records, and say why a cell is empty

def test_taxon_layers_is_current():
    import subprocess, sys
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_taxon_layers.py"), "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_taxon_layers_never_infers_not_found():
    import importlib.util
    spec = importlib.util.spec_from_file_location("btl", ROOT / "scripts" / "build_taxon_layers.py")
    btl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(btl)
    rows = [line.split("\t") for line in btl.build(ROOT / "data").splitlines()]
    head, body = rows[0], rows[1:]
    col = {name: i for i, name in enumerate(head)}
    for r in body:
        # a status that rests on a search names the search
        if r[col["pheromone_status"]] in ("searched_not_found", "found_not_curated") or r[col["genome_status"]] == "no_assembly_in_census":
            assert r[col["search_basis"]], r[col["species"]]


# ---- release machinery: derived/ is current and byte-deterministic; the lock covers the constraints

def _load(name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_derived_is_current():
    import subprocess, sys
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_release.py"), "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_derived_is_deterministic():
    br = _load("build_release")
    assert br.derived_files(ROOT / "data") == br.derived_files(ROOT / "data")


def test_derived_carries_no_release_metadata():
    br = _load("build_release")
    files = br.derived_files(ROOT / "data")
    summary = json.loads(files["summary.json"])
    for key in ("git_commit", "tag", "doi", "date", "commit_date", "atlas_version"):
        assert key not in summary, key


def test_lock_pins_every_constraint():
    from packaging.requirements import Requirement
    lock = {}
    for line in (ROOT / "requirements.lock.txt").read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            name, version = line.split("==")
            lock[name.lower().replace("_", "-")] = version
    for line in (ROOT / "requirements.in").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            req = Requirement(line)
            name = req.name.lower().replace("_", "-")
            assert name in lock, f"{name} is not in requirements.lock.txt"
            assert req.specifier.contains(lock[name]), f"{name}=={lock[name]} does not satisfy {req.specifier}"


def test_citation_cff_is_complete():
    cff = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    for key in ("cff-version", "message", "title", "authors", "type", "license", "version"):
        assert cff.get(key), key
    assert "doi" not in cff, "no DOI until one is minted (docs/releases-and-occurrences.md)"


# ---- the v0.1 record shape is frozen: schema changes must be additive

def test_schema_shape_is_additive_over_v0_1():
    ss = _load("schema_shape")
    import json as _json
    problems = ss.breaks(_json.loads(ss.FROZEN.read_text(encoding="utf-8")), ss.current())
    assert not problems, problems


def test_freeze_check_catches_a_breaking_change():
    ss = _load("schema_shape")
    import copy, json as _json
    frozen = _json.loads(ss.FROZEN.read_text(encoding="utf-8"))
    now = copy.deepcopy(ss.current())
    obs = now["observation.schema.json"]
    path = next(p for p, e in obs.items() if "unit" in p and "enum" in e)
    obs[path]["enum"] = obs[path]["enum"][1:]               # drop one unit
    obs["/"]["required"] = obs["/"]["required"] + ["new"]  # add a required field
    problems = ss.breaks(frozen, now)
    assert any("enum lost" in p for p in problems) and any("required changed" in p for p in problems), problems


# ---- tidy tables: rectangular, and every key joins to its entity table

def test_tables_are_rectangular_and_join():
    bt = _load("build_tables")
    tables = {}
    for name, text in bt.build(ROOT / "data").items():
        lines = text.splitlines()
        head = lines[0].split("\t")
        rows = [dict(zip(head, line.split("\t"))) for line in lines[1:]]
        assert all(len(line.split("\t")) == len(head) for line in lines), name
        tables[name.removeprefix("tables/").removesuffix(".tsv")] = rows
    ids = {t: {r[k] for r in tables[t]} for t, k in [("taxa", "taxon_id"), ("references", "reference_id"),
                                                       ("compounds", "compound_id"), ("genomes", "genome_id"),
                                                       ("observations", "observation_id")]}
    joins = [("observations", "taxon_id", "taxa"), ("observations", "reference_id", "references"),
             ("genomes", "taxon_id", "taxa"), ("genome_annotations", "genome_id", "genomes"),
             ("taxon_synonyms", "taxon_id", "taxa"), ("compound_double_bonds", "compound_id", "compounds")]
    for t in ("observation_experiments", "chemical_samples", "chemical_components", "chemical_values",
              "behavioural_assays", "behavioural_stimuli", "behavioural_setups", "electrophysiology_responses"):
        joins.append((t, "observation_id", "observations"))
    for t in ("chemical_components", "chemical_values", "behavioural_stimuli", "electrophysiology_responses"):
        joins.append((t, "compound_id", "compounds"))
    for table, key, target in joins:
        missing = {r[key] for r in tables[table] if r[key]} - ids[target]
        assert not missing, f"{table}.{key} not in {target}: {sorted(missing)[:3]}"
    # one row per behavioural observation in its assay table
    n_beh = sum(r["observation_type"] == "behavioural_response" for r in tables["observations"])
    assert len(tables["behavioural_assays"]) == n_beh

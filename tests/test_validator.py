"""The validator must accept the good fixtures and refuse every bad one, for
the stated reason. A gate that has never been seen to fail is not a gate.

Each directory under fixtures/bad/ overlays one or more files on a copy of
fixtures/good/ and names, in EXPECT, the error code it must produce.
"""

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
    for src in (FIX / "bad" / case).rglob("*.yaml"):
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
    expected = (FIX / "bad" / case / "EXPECT").read_text().strip()
    got = codes(overlay(tmp_path, case))
    assert expected in got, f"{case}: expected {expected}, got {sorted(got) or 'no error'}"


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

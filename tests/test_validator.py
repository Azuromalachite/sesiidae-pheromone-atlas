"""The validator must accept the good fixtures and refuse every bad one, for
the stated reason. A gate that has never been seen to fail is not a gate.

Each directory under fixtures/bad/ overlays one or more files on a copy of
fixtures/good/ and names, in EXPECT, the error code it must produce. The data
root's siblings are validated too, as in the repository: fixtures/computed/
and fixtures/teaching/ are the good copies of computed/ and teaching/, and a
bad case's files under computed/ or teaching/ overlay those.
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


SIBLINGS = ("computed", "teaching")


def overlay(tmp_path, case):
    root = tmp_path / "root"
    shutil.copytree(GOOD, root)
    for sib in SIBLINGS:
        shutil.copytree(FIX / sib, tmp_path / sib)
    for src in (p for p in (FIX / "bad" / case).rglob("*") if p.is_file() and p.name != "EXPECT"):
        rel = src.relative_to(FIX / "bad" / case)
        dst = (tmp_path if rel.parts[0] in SIBLINGS else root) / rel
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


# ---- analyses read only derived/tables/, and their committed reports are current

def test_analysis_reports_are_current():
    import subprocess, sys
    for script in sorted((ROOT / "analyses").glob("*.py")):
        r = subprocess.run([sys.executable, str(script), "--check"], capture_output=True, text=True)
        assert r.returncode == 0, f"{script.name}: {r.stderr}"


# ---- computed/espmap: the siblings of the data root are part of the gate

def test_good_siblings_exist_and_are_read():
    # the good fixtures include a computed tree and a teaching case, so a gate
    # that silently skipped the siblings would not pass the bad cases above
    assert (FIX / "computed" / "espmap").is_dir() and any((FIX / "teaching" / "cases").glob("*.yaml"))


def test_npz_assets_are_verified_before_bundling(tmp_path):
    br = _load("build_release")
    computed = FIX / "computed"
    assert {p.code for p in br.npz_problems(computed, tmp_path)} == {"BUNDLE_NPZ_MISSING"}
    ens = json.loads((computed / "espmap/z13_18_sme/b3lyp_def2-svp_gas_espmap-v0.2.0/ensemble.json").read_text(encoding="utf-8"))
    for slug, proto, members in br.listed_npz(computed):
        for m in members:
            p = tmp_path / slug / proto / m["npz"]
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(f"npz-{slug}-{m['conformer'][-1]}".encode())   # the fixture's stand-in contents
    assert br.npz_problems(computed, tmp_path) == []
    wrong = tmp_path / "z13_18_sme" / "b3lyp_def2-svp_gas_espmap-v0.2.0" / ens["members"][0]["npz"]
    wrong.write_bytes(b"changed")
    assert {p.code for p in br.npz_problems(computed, tmp_path)} == {"BUNDLE_NPZ_CHECKSUM"}


# ---- teaching bundles: built from records only, and valid against their schema

def _bundle_schema():
    from jsonschema import Draft202012Validator
    return Draft202012Validator(json.loads((ROOT / "schemas" / "teaching-bundle.schema.json").read_text(encoding="utf-8")))


def test_fixture_teaching_bundle_is_valid_and_complete():
    tb = _load("export_teaching_bundle")
    b = tb.build(GOOD, "fixture_case")
    assert list(_bundle_schema().iter_errors(b)) == []
    assert "atlas_version" not in b
    keys = {c["atlas_id"]: c["inchikey"] for c in b["compounds"]}
    for p in (GOOD / "compounds").glob("*.yaml"):
        rec = yaml.safe_load(p.read_text(encoding="utf-8"))
        if rec["compound_id"] in keys:
            assert keys[rec["compound_id"]] == rec["generated"]["inchikey"]
    # the ensemble of a case compound is listed with the hash of its index; the model's is not
    assert [(e["atlas_id"], e["protocol"]) for e in b["espmap"]] == [("spa.cmpd.z3_z13_18_oac", "b3lyp_def2-svp_gas_espmap-v0.2.0")]
    path = FIX / b["espmap"][0]["path"]
    import hashlib
    assert b["espmap"][0]["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()


def test_teaching_statements_come_from_record_fields(tmp_path):
    tb = _load("export_teaching_bundle")
    root = overlay(tmp_path, "teaching_unknown_observation")   # any overlay: a writable copy
    shutil.copy(FIX / "teaching" / "cases" / "fixture_case.yaml", tmp_path / "teaching" / "cases" / "fixture_case.yaml")
    before = tb.build(root, "fixture_case")
    trap = root / "observations" / "trap.yaml"
    rec = yaml.safe_load(trap.read_text(encoding="utf-8"))
    rec["significance"] = "not_tested"
    trap.write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")
    after = tb.build(root, "fixture_case")
    oid = rec["observation_id"]
    s_before = next(o["statement"] for o in before["observations"] if o["observation_id"] == oid)
    s_after = next(o["statement"] for o in after["observations"] if o["observation_id"] == oid)
    assert "not_tested" in s_after and s_before != s_after
    comp = after["comparisons"][0]
    assert comp["observed_contrast"]["b"] == s_after and comp["observation_ids"][1] == oid


def test_real_teaching_bundles_are_valid():
    tb = _load("export_teaching_bundle")
    cases = sorted(p.stem for p in (ROOT / "teaching" / "cases").glob("*.yaml"))
    assert cases
    for case in cases:
        assert list(_bundle_schema().iter_errors(tb.build(ROOT / "data", case))) == [], case


def test_exported_copy_carries_its_version_and_derived_does_not():
    tb = _load("export_teaching_bundle")
    b = tb.build(GOOD, "fixture_case", atlas_version="e8ca212")
    assert b["atlas_version"] == "e8ca212" and list(_bundle_schema().iter_errors(b)) == []
    br = _load("build_release")
    for name, data in br.derived_files(ROOT / "data").items():
        if name.startswith("teaching/"):
            assert "atlas_version" not in json.loads(data), name


def test_a_symlink_under_computed_is_refused_and_never_read(tmp_path):
    import os
    root = overlay(tmp_path, "computed_npz_in_git")   # a writable copy; drop the overlay's NPZ
    proto = tmp_path / "computed/espmap/z3_z13_18_oac/b3lyp_def2-svp_gas_espmap-v0.2.0"
    (proto / "conf_00.npz").unlink()
    elsewhere = tmp_path / "elsewhere"
    shutil.move(str(proto), str(elsewhere))
    try:
        os.symlink(elsewhere, proto, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks not available here")
    assert "COMPUTED_LAYOUT" in codes(root)
    assert all("z3_z13_18_oac" not in str(p) for p in av.ensemble_paths(tmp_path / "computed"))


def test_bundle_ships_only_verified_npz_bytes(tmp_path):
    br = _load("build_release")
    computed = FIX / "computed"
    with pytest.raises(SystemExit, match="--npz-dir"):
        br.computed_contents(computed, None)
    with pytest.raises(SystemExit, match="do not match"):
        br.computed_contents(computed, tmp_path)
    expected = {}
    for slug, proto, members in br.listed_npz(computed):
        for m in members:
            p = tmp_path / slug / proto / m["npz"]
            p.parent.mkdir(parents=True, exist_ok=True)
            data = f"npz-{slug}-{int(m['conformer'][5:])}".encode()   # the fixture's stand-in contents
            p.write_bytes(data)
            expected[f"computed/espmap/{slug}/{proto}/{m['npz']}"] = data
    contents = br.computed_contents(computed, tmp_path)
    assert {k: v for k, v in contents.items() if k.endswith(".npz")} == expected
    assert all(not k.endswith(".npz") or k in expected for k in contents)
    first = next(iter(expected))
    (tmp_path / first.removeprefix("computed/espmap/")).write_bytes(b"swapped")
    with pytest.raises(SystemExit, match="do not match"):
        br.computed_contents(computed, tmp_path)


def test_statement_is_exactly_the_record_fields():
    tb = _load("export_teaching_bundle")
    b = tb.build(GOOD, "fixture_case")
    trap = next(o for o in b["observations"] if o["observation_id"].endswith(".trap.population_b"))
    assert trap["statement"] == ("Fixturia testa (population_b), field_trapping: E2,Z13-18:OAc 100 parts + E3,Z13-18:OAc 3 parts "
                                 "vs E2,Z13-18:OAc 100 parts (major component alone): decreased, not_reported; 0.5 vs 1 fold_change_vs_comparator (trap_catch, approximate)")
    assert tb.num(1234567) == "1234567" and tb.num(1.2345678e-05) == "1.2345678e-05"
    roles = {c["atlas_id"]: c["occurrences"] for c in b["compounds"]}
    gland_roles = {o["observation_id"]: o["roles"] for o in roles["spa.cmpd.z3_z13_18_oac"]}
    assert gland_roles["spa.obs.fixture_species_a.fixture_2026.ead"] == ["antennal_active"]


@pytest.mark.parametrize("sibling", ["computed", "teaching"])
def test_a_symlinked_sibling_root_is_refused(tmp_path, sibling):
    import os
    root = overlay(tmp_path, "computed_npz_in_git")
    (tmp_path / "computed/espmap/z3_z13_18_oac/b3lyp_def2-svp_gas_espmap-v0.2.0/conf_00.npz").unlink()
    real = tmp_path / f"{sibling}_real"
    shutil.move(str(tmp_path / sibling), str(real))
    try:
        os.symlink(real, tmp_path / sibling, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks not available here")
    got = codes(root)
    assert ("COMPUTED_LAYOUT" if sibling == "computed" else "TEACH_LAYOUT") in got
    if sibling == "computed":
        assert av.ensemble_paths(tmp_path / "computed") == []


def test_exporter_refuses_a_case_outside_the_gate(tmp_path):
    tb = _load("export_teaching_bundle")
    with pytest.raises(SystemExit, match="not a case"):
        tb.build(GOOD, "../../fixture_case")


# ---- the human spot-check: drawn once, deterministically, and its results file stays well-formed

def test_spot_check_draw_is_deterministic(tmp_path):
    sc = _load("spot_check")
    a = sc.draw(tmp_path / "a", 7, 10)
    b = sc.draw(tmp_path / "b", 7, 10)
    assert a == b and len(a) == 10 + len(sc.HARD)
    assert (tmp_path / "a" / "sheet.md").read_text(encoding="utf-8").replace("# Spot-check a", "") == \
           (tmp_path / "b" / "sheet.md").read_text(encoding="utf-8").replace("# Spot-check b", "")
    with pytest.raises(SystemExit, match="already holds a draw"):
        sc.draw(tmp_path / "a", 7, 10)
    lines, problems = sc.summarise(tmp_path / "a")
    assert problems == [] and "random: 0 of 10 checked" in lines[0]
    res = yaml.safe_load((tmp_path / "a" / "results.yaml").read_text(encoding="utf-8"))
    res["records"][0]["verdict"] = "error"
    (tmp_path / "a" / "results.yaml").write_text(yaml.safe_dump(res), encoding="utf-8")
    assert any("must name its wrong rows" in p for p in sc.summarise(tmp_path / "a")[1])


def test_committed_spot_checks_are_well_formed():
    sc = _load("spot_check")
    for d in sorted((ROOT / "review").glob("spot-check-*")):
        assert sc.summarise(d)[1] == [], d.name

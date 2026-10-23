"""espmap-sesiidae-001: build the Atlas index (spa.espmap_ensemble/0) for each
molecule from the computed members, and list the plan's exclusions.

  python s001_build.py [--partial] [slug...]

Writes ~/s001/atlas/computed/espmap/<slug>/<PROTOCOL>/{ensemble.json, SHA256SUMS,
conformers/conf_NN.json} for the four Atlas compounds, and the same layout under
~/s001/control/ for the aldehyde teaching control (not an Atlas compound). NPZ
surfaces are not copied: their sha256 goes in ensemble.json, the files stay in
~/s001/<slug>/conformers/ for the release assets. Also writes
~/s001/<slug>/members.json, the per-member facts the analysis reads (folded,
contacts, genus, exclusion), so both scripts use one folded call.

Without --partial a molecule with fewer than K finished members is refused.

Folded, per the frozen plan section 3: an intramolecular contact OR surface
genus > 0. The contact rule is espmap master's intramolecular_contacts at
5175515 (heavy atoms >= 5 bonds apart, closer than the Bondi sum + 0.5 A),
provisional in espmap; v0.2.1, which computed the members, has no contact rule.
Exclusions, plan section 3: a member is excluded only if its surface fails
espmap's integrity checks or its record's validity is false (a run that wrote
no record is excluded for the same reason).
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

OUT = Path.home() / "s001"
HERE = Path(__file__).resolve().parent
PROTOCOL = "b3lyp_def2-svp_gas_espmap-v0.2.1"
K = 20
ATLAS = {"z3_z13_18_oac": "spa.cmpd.z3_z13_18_oac", "e3_z13_18_oac": "spa.cmpd.e3_z13_18_oac",
         "e2_z13_18_oac": "spa.cmpd.e2_z13_18_oac", "z3_z13_18_oh": "spa.cmpd.z3_z13_18_oh"}
CONTROL = {"z3_z13_18_al": "arrowfield.control.z3_z13_18_al"}
MASTER = "5175515"
FOLDED_NOTE = ("folded = an intramolecular contact OR surface genus > 0 (frozen plan section 3). "
               "Contact: heavy atoms at least 5 bonds apart and closer than their Bondi radii + 0.5 A, "
               f"espmap master's intramolecular_contacts at {MASTER} (provisional in espmap; v0.2.1 has none), "
               "applied to each member's SDF. rg_angstrom: heavy atoms, unweighted, from the record's geometry. "
               "Selection used RDKit RadiusOfGyration (mass-weighted, all atoms).")


def master_module():
    spec = importlib.util.spec_from_file_location("espmap_master", HERE / f"espmap_master_{MASTER}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def heavy_rg(rec):
    g = rec["geometry"]
    X = np.array([x for s, x in zip(g["symbols"], g["xyz_angstrom"]) if s != "H"])
    return float(np.sqrt(((X - X.mean(0)) ** 2).sum(1).mean()))


def exclusion(rec):
    """None, or why the plan excludes this member."""
    bad = [k for k, v in rec["validity"].items() if v is False]
    surf = rec["results"]["surface"]
    if not surf.get("valid", False) or surf.get("problems"):
        return f"surface integrity: {surf.get('problems')}"
    if bad:
        return f"validity false: {bad}"
    return None


def members(slug, em):
    from rdkit import Chem
    d = OUT / slug
    sel = json.loads((d / "selection.json").read_text())
    log = {}
    if (d / "run_log.jsonl").exists():
        for line in (d / "run_log.jsonl").read_text().splitlines():
            r = json.loads(line)
            log[r["conformer"]] = r          # the last attempt wins
    rows = []
    for s in sel["members"]:
        c = s["conformer"]
        base = d / "conformers" / c
        mol = Chem.MolFromMolFile(str(base.with_suffix(".sdf")), removeHs=False)
        contacts = [[int(i), int(j), round(x, 3)] for i, j, x, _ in em.intramolecular_contacts(mol)]
        row = dict(conformer=c, embed_conf_id=s["embed_conf_id"], is_lowest_mmff=s["is_lowest_mmff"],
                   mmff_dE=s["mmff_dE"], contacts=contacts)
        js, npz = base.with_suffix(".json"), base.with_suffix(".npz")
        if not (js.exists() and npz.exists()):
            r = log.get(c)
            if r is None or r["rc"] == 0:
                row["status"] = "pending"
            else:
                row.update(status="excluded", reason=f"run failed rc {r['rc']}: {r['tail'][-200:]}",
                           rg_angstrom=s["rg_heavy"], genus=None, folded=bool(contacts))
            rows.append(row)
            continue
        rec = json.loads(js.read_text())
        genus = rec["results"]["surface"].get("genus")
        why = exclusion(rec)
        row.update(status="excluded" if why else "ok", reason=why, record_sha256=sha256(js),
                   npz_sha256=sha256(npz), geometry_sha1=rec["geometry"]["sha1"], rg_angstrom=heavy_rg(rec),
                   genus=genus, folded=bool(contacts) or bool(genus and genus > 0))
        rows.append(row)
    return rows


def build(slug, partial, em):
    from rdkit import Chem
    d = OUT / slug
    rows = members(slug, em)
    (d / "members.json").write_text(json.dumps(rows, indent=1))
    ok = [r for r in rows if r["status"] == "ok"]
    pend = [r["conformer"] for r in rows if r["status"] == "pending"]
    exc = [r for r in rows if r["status"] == "excluded"]
    print(f"{slug:15s} ok {len(ok)}, excluded {len(exc)}, pending {len(pend)}; "
          f"folded {sum(r['folded'] for r in ok)}/{len(ok)}")
    for r in exc:
        print(f"   EXCLUDED {r['conformer']}: {r['reason']} (Rg {r['rg_angstrom']:.2f}, folded {r['folded']})")
    if pend and not partial:
        raise SystemExit(f"{slug}: {len(pend)} members not computed yet; --partial to build anyway")
    if not ok:
        return
    recs = {r["conformer"]: json.loads((d / "conformers" / f"{r['conformer']}.json").read_text()) for r in ok}
    first = recs[ok[0]["conformer"]]
    for c, rec in recs.items():          # one protocol, one molecule, one version
        assert rec["analysis_key"] == first["analysis_key"], (slug, c)
        assert rec["key_fields"]["analysis"] == first["key_fields"]["analysis"], (slug, c)
        assert rec["input"]["computed_smiles"] == first["input"]["computed_smiles"], (slug, c)
        assert rec["provenance"]["espmap_version"] == "0.2.1" and rec["provenance"]["code"] == "v0.2.1", (slug, c)
    smiles = Chem.MolToSmiles(Chem.MolFromSmiles(first["input"]["computed_smiles"]))
    commit = subprocess.run(["git", "-C", str(Path.home() / "espmap-v021"), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=True).stdout.strip()
    sel = json.loads((d / "selection.json").read_text())
    notes = FOLDED_NOTE
    if exc:
        notes += " Excluded (plan section 3): " + "; ".join(
            f"{r['conformer']} ({r['reason']}; Rg {r['rg_angstrom']:.2f} A, folded {r['folded']})" for r in exc) + "."
    if pend:
        notes += f" PARTIAL: {len(pend)} of {K} members not yet computed."
    aid = ATLAS.get(slug) or CONTROL[slug]
    ens = {
        "schema": "spa.espmap_ensemble/0",
        "atlas_id": aid,
        "smiles": smiles,
        "inchikey": Chem.MolToInchiKey(Chem.MolFromSmiles(smiles)),
        "protocol": PROTOCOL,
        "analysis_key": first["analysis_key"],
        "analysis": first["key_fields"]["analysis"],
        "espmap": {"version": "0.2.1", "commit": commit},
        "selection": {"method": f"lowest MMFF94s + {K - 1} spread over Rg of {sel['n_embedded']} ETKDGv3 + "
                                f"MMFF94s embeddings, seed {sel['seed']} (espmap v0.2.1 from_smiles; "
                                "bench/conformers.select); folded members kept",
                      "notes": notes},
        "members": [{"conformer": r["conformer"], "record": f"conformers/{r['conformer']}.json",
                     "record_sha256": r["record_sha256"], "geometry_sha1": r["geometry_sha1"],
                     "npz": f"{r['conformer']}.npz", "npz_sha256": r["npz_sha256"],
                     "rg_angstrom": round(r["rg_angstrom"], 4), "folded": r["folded"]} for r in ok],
        "notes": "espmap-sesiidae-001 (Atlas analyses/espmap-sesiidae-001, frozen at 7e34658)."
                 + (" Teaching control: not an Atlas compound." if slug in CONTROL else ""),
    }
    root = OUT / ("control" if slug in CONTROL else "atlas") / "computed" / "espmap" / slug / PROTOCOL
    (root / "conformers").mkdir(parents=True, exist_ok=True)
    for old in (root / "conformers").glob("*.json"):
        old.unlink()
    for r in ok:
        (root / "conformers" / f"{r['conformer']}.json").write_bytes(
            (d / "conformers" / f"{r['conformer']}.json").read_bytes())
    (root / "ensemble.json").write_text(json.dumps(ens, indent=1, allow_nan=False) + "\n", encoding="utf-8")
    names = ["ensemble.json"] + [f"conformers/{r['conformer']}.json" for r in ok]
    (root / "SHA256SUMS").write_text("".join(f"{sha256(root / n)}  {n}\n" for n in names), encoding="utf-8")


if __name__ == "__main__":
    args = sys.argv[1:]
    partial = "--partial" in args
    slugs = [a for a in args if not a.startswith("--")] or list(ATLAS) + list(CONTROL)
    em = master_module()
    for s in slugs:
        build(s, partial, em)

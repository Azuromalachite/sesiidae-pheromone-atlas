"""espmap-sesiidae-001: compute the frozen ensembles (Atlas analyses/espmap-sesiidae-001,
frozen at 7e34658). Protocol from the plan's section 3, fixed:
  espmap v0.2.1 (clean clone at the tag), B3LYP/def2-SVP + RI, gas, 0.26 bohr;
  100 ETKDGv3 + MMFF94s embeddings with seed 20261024 (espmap's own embedder);
  K = 20: the lowest-MMFF conformer plus 19 spread over Rg (the pilot's selection,
  bench/conformers.select); folded members kept.
Each member is an ordinary espmap.record/1, computed by v0.2.1's own CLI from a
3D SDF of the chosen conformer (declared origin etkdg_mmff94s), one process per
member. Resumable: a member whose JSON exists is skipped.

  python s001_run.py select      # choose and write the conformers, check identity
  python s001_run.py run [MOL]   # compute what is missing
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ESPMAP = Path.home() / "espmap-v021"
OUT = Path.home() / "s001"
sys.path.insert(0, str(ESPMAP))
sys.path.insert(0, str(ESPMAP / "bench"))
import esp_map as em  # noqa: E402
from conformers import select  # noqa: E402

SEED, N_EMBED, K = 20261024, 100, 20
PY = sys.executable
CH2 = lambda a, b: "".join(f"[CH2:{n}]" for n in range(a, b + 1))  # noqa: E731
TAIL = f"/[CH:13]=[CH:14]\\{CH2(15, 17)}[CH3:18]"                 # Z13 everywhere
ACE = "[CH3:21][C:22](=[O:32])[O:31]"
# slug -> (mapped SMILES, expected canonical isomeric SMILES, head-group sites)
MOLS = {
    "z3_z13_18_oac": (f"{ACE}[CH2:1][CH2:2]/[CH:3]=[CH:4]\\{CH2(5, 12)}{TAIL}",
                      "CCCC/C=C\\CCCCCCCC/C=C\\CCOC(C)=O", "acetate"),
    "e3_z13_18_oac": (f"{ACE}[CH2:1][CH2:2]/[CH:3]=[CH:4]/{CH2(5, 12)}{TAIL}",
                      "CCCC/C=C\\CCCCCCCC/C=C/CCOC(C)=O", "acetate"),
    "e2_z13_18_oac": (f"{ACE}[CH2:1]/[CH:2]=[CH:3]/{CH2(4, 12)}{TAIL}",
                      "CCCC/C=C\\CCCCCCCCC/C=C/COC(C)=O", "acetate"),
    "z3_z13_18_oh": (f"[OH:31][CH2:1][CH2:2]/[CH:3]=[CH:4]\\{CH2(5, 12)}{TAIL}",
                     "CCCC/C=C\\CCCCCCCC/C=C\\CCO", "alcohol"),
    # the teaching control: not an Atlas compound
    "z3_z13_18_al": (f"[O:32]=[CH:1][CH2:2]/[CH:3]=[CH:4]\\{CH2(5, 12)}{TAIL}",
                     "CCCC/C=C\\CCCCCCCC/C=C\\CC=O", "aldehyde"),
}
HEAD = {  # Arrowfield's one-definition head O: the O on C1, the atom alone
    "alcohol": [{"label": "head O", "atoms": [31]}, {"label": "hydroxyl", "atoms": ["31+H"]}],
    "aldehyde": [{"label": "head O", "atoms": [32]}],
    "acetate": [{"label": "head O", "atoms": [31]}, {"label": "carbonyl O", "atoms": [32]},
                {"label": "acetyl", "atoms": ["21+H", 22, 32]}],
}


def sites(head):
    return {"by": "map",
            "groups": [{"label": f"C{n}-H", "atoms": [f"{n}+H"]} for n in range(1, 19)] + HEAD[head]}


def heavy_rg(mol, cid):
    c = mol.GetConformer(cid)
    X = np.array([list(c.GetAtomPosition(a.GetIdx())) for a in mol.GetAtoms() if a.GetAtomicNum() > 1])
    return float(np.sqrt(((X - X.mean(0)) ** 2).sum(1).mean()))


def do_select(slug):
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors3D
    smiles, expect, head = MOLS[slug]
    d = OUT / slug
    (d / "conformers").mkdir(parents=True, exist_ok=True)
    _, info = em.from_smiles(smiles, n_confs=N_EMBED, seed=SEED)
    mol = info["mol"]
    props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant="MMFF94s")
    cids = [c.GetId() for c in mol.GetConformers()]
    energy = np.array([AllChem.MMFFGetMoleculeForceField(mol, props, confId=c).CalcEnergy()
                       for c in cids])
    rg = np.array([Descriptors3D.RadiusOfGyration(mol, confId=c) for c in cids])
    picks = select(rg, energy, K)
    approved = Chem.MolFromSmiles(smiles)
    want = Chem.MolToSmiles(Chem.MolFromSmiles(expect))
    rows = []
    for k, i in enumerate(picks):
        cid = cids[i]
        spec = em._mol_to_spec(mol, cid)
        ok, computed, why = em.verify_computed(spec, approved)
        assert ok and Chem.MolToSmiles(Chem.MolFromSmiles(computed)) == want, (slug, cid, computed, why)
        assert em.verify_mapping(spec, approved)[0], (slug, cid)
        name = f"conf_{k:02d}"
        m1 = Chem.Mol(mol, confId=cid)
        m1.SetProp("_Name", f"{slug} {name}")
        m1.SetProp("espmap_geometry_origin", "etkdg_mmff94s")
        m1.SetProp("s001_note", f"espmap v0.2.1 from_smiles seed {SEED}, conformer {cid} of "
                                f"{len(cids)}; selected {k} by bench/conformers.select K={K}")
        w = Chem.SDWriter(str(d / "conformers" / f"{name}.sdf"))
        w.write(m1, confId=cid)
        w.close()
        rows.append(dict(conformer=name, embed_conf_id=int(cid), is_lowest_mmff=bool(i == int(np.argmin(energy))),
                         mmff_dE=float(energy[i] - energy.min()), rg_selection=float(rg[i]),
                         rg_heavy=heavy_rg(mol, cid)))
    (d / "sites.json").write_text(json.dumps(sites(head), indent=1))
    (d / "selection.json").write_text(json.dumps(dict(
        slug=slug, smiles=smiles, expected=expect, seed=SEED, n_embedded=len(cids), k=K,
        method="espmap v0.2.1 from_smiles (ETKDGv3 + MMFF94s), seed 20261024, 100 embeddings; "
               "bench/conformers.select: lowest MMFF94s + spread over Rg (RDKit RadiusOfGyration)",
        members=rows), indent=1))
    print(f"{slug:15s} {len(cids)} embedded, {len(rows)} selected, identity and maps verified")


def do_run(slug):
    d = OUT / slug
    sel = json.loads((d / "selection.json").read_text())
    log = d / "run_log.jsonl"
    for r in sel["members"]:
        base = d / "conformers" / r["conformer"]
        if base.with_suffix(".json").exists() and base.with_suffix(".npz").exists():
            continue
        cmd = [PY, str(ESPMAP / "esp_map.py"), "--file", str(base.with_suffix(".sdf")),
               "--sites", str(d / "sites.json"), "--basis", "def2-svp", "--density-fit",
               "--spacing", "0.26", "--json", str(base.with_suffix(".json")),
               "--npz", str(base.with_suffix(".npz")), "--out", str(base.with_suffix(".png"))]
        t = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True)
        row = dict(slug=slug, conformer=r["conformer"], rc=p.returncode, t_wall=round(time.time() - t, 1),
                   tail=p.stderr[-600:] if p.returncode else "")
        with log.open("a") as f:
            f.write(json.dumps(row) + "\n")
        print(f"{slug:15s} {r['conformer']} rc {p.returncode} {row['t_wall']:.0f}s", flush=True)


if __name__ == "__main__":
    what = sys.argv[1]
    slugs = sys.argv[2:] or list(MOLS)
    for s in slugs:
        do_select(s) if what == "select" else do_run(s)

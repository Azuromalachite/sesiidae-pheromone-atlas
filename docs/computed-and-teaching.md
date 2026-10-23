# Computed results and teaching bundles

Agreed on 2026-10-23 for the three projects:
- **espmap** computes;
- **the Atlas** owns the Sesiidae science, including the canonical espmap
  results for its compounds;
- **Arrowfield** only shows and teaches, reading a bundle the Atlas exports.

This file is the contract on the Atlas side.

## `computed/espmap/`: what was computed for an Atlas compound

```
computed/espmap/<slug>/<protocol>/
  ensemble.json            spa.espmap_ensemble/0 (schemas/espmap-ensemble.schema.json)
  SHA256SUMS               every other file in the directory, "<sha256>  <name>"
  conformers/conf_NN.json  one espmap.record/1 per conformer
```

- **`<slug>`** is the last segment of an Atlas compound or model ID: for
  example, `z3_z13_18_oac` for `spa.cmpd.z3_z13_18_oac`, or `z13_18_sme` for
  `spa.model.z13_18_sme`.
- **`<protocol>`** is a name in `[a-z0-9_.-]`, for example
  `b3lyp_def2-svp_gas_espmap-v0.2.1`.

Nothing else may sit under `computed/`. This directory is not `derived/`.
`derived/` is a function of the committed sources: CI regenerates it and
refuses any file it did not write. Computed results are inputs that the
Atlas checks, not outputs it builds.

**What `atlas_validate.py` checks.** It runs these whenever `computed/`
exists beside `data/`; failing fixtures are in `tests/fixtures/bad/computed_*`.

| code | what it refuses |
|---|---|
| `COMPUTED_LAYOUT` | any file outside the layout above |
| `COMPUTED_NPZ_IN_GIT` | an NPZ surface; these ship as release assets |
| `COMPUTED_SCHEMA` | an `ensemble.json` that is missing, not JSON, or fails its schema |
| `COMPUTED_ID` | an `atlas_id` with no record, one that does not match the slug, or a slug that names two records |
| `COMPUTED_STRUCTURE` | `smiles` that, re-canonicalised with the validator's RDKit, is not the record's structure |
| `COMPUTED_INCHIKEY` | an InChIKey that differs from the record's generated one (the second identity check) |
| `COMPUTED_PROTOCOL` | a `protocol` that is not the directory name |
| `COMPUTED_CHECKSUM` | `SHA256SUMS` missing, a file unlisted, absent or changed, or a `record_sha256` that does not match |
| `COMPUTED_MEMBER` | a member listed twice, a record or NPZ name that is not `<conformer>.json` / `<conformer>.npz`, a missing record, or a conformer file no member lists |
| `COMPUTED_RECORD` | a member file that is not an `espmap.record/1`, or whose `analysis_key` is not the member's |

**Why identity rests on SMILES first.** A standard InChIKey merges some
tautomers (2-hydroxypyridine and 2-pyridone share one), so it is only the
second check.

**What the Atlas does not check.** The gate checks these files as an index:
present, unchanged, the right molecule. It does not re-validate espmap's own
record schema or recompute anything. Atlas CI never needs espmap installed.

**NPZ surfaces.** They are not in git (`.gitignore` excludes them, and the
gate refuses one if it appears). `ensemble.json` records each surface's
`npz_sha256`. A release bundle ships them from
`--npz-dir <dir>/<slug>/<protocol>/conf_NN.npz`. `build_release.py --bundle`
refuses to build if `computed/` lists any NPZ and one is missing or its
sha256 differs.

**When espmap's own ensemble record ships** (v0.3), it replaces this index as
a new schema version. The `/0` file is never edited in place.

## `teaching/cases/`: what a teaching bundle may assert

A case (`schemas/teaching-case.schema.json`) names:
- compounds;
- observations;
- comparisons, each between two of its own observations.

It names records only. `scripts/export_teaching_bundle.py` builds the
bundle (`schemas/teaching-bundle.schema.json`, `spa.teaching/0`). Every
observation's `statement`, and both sides of every comparison's
`observed_contrast`, are assembled from record fields: taxon, place, lure
and comparator, effect, significance, response values and qualifier,
detections and negatives, antennal readings. The bundle draws no conclusion.
A comparison label names the pair; it does not interpret it.

**Validator codes** (fixtures in `tests/fixtures/bad/teaching_*`):

| code | what it refuses |
|---|---|
| `TEACH_LAYOUT` | anything in `teaching/` other than `cases/<case_id>.yaml` |
| `TEACH_SCHEMA` | a case that fails its schema |
| `TEACH_CASE_ID` | a `case_id` that is not the file name |
| `TEACH_REF` | an observation or compound with no record |
| `TEACH_COMPOUND_UNOBSERVED` | a compound that occurs in none of the case's observations (blends and comparator blends included) |
| `TEACH_COMPARISON` | a comparison of an observation with itself, or with one outside the case |

**Where bundles live:**
- `build_release.py` writes `derived/teaching/<case_id>.json`, with no
  `atlas_version` (derived/ holds no release metadata), and CI checks that it
  is current.
- A consumer pins an Atlas commit or tag and reads that file, or runs
  `python scripts/export_teaching_bundle.py <case_id> --out bundle.json`.
  That writes a copy naming the commit or tag.

**What the consumer adds.** Arrowfield adds teaching metadata only: acts,
prompts and site labels. A compound it uses as a teaching control, such as
Z3,Z13-18:Al, is not an Atlas compound and stays outside the bundle.

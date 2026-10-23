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
exists beside `data/`. Layout, checksums and record shapes are checked even
when the data records fail; the links to records are checked only once the
records are sound. Failing fixtures are in `tests/fixtures/bad/computed_*`.

| code | what it refuses |
|---|---|
| `COMPUTED_LAYOUT` | any file outside the layout above, any symlink (the `computed` root included), or a `computed` that is not a directory |
| `COMPUTED_NPZ_IN_GIT` | an NPZ surface (any case of `.npz`); these ship as release assets |
| `COMPUTED_SCHEMA` | an `ensemble.json` that is missing, not UTF-8, not strict JSON (a repeated key, NaN or Infinity), or fails its schema |
| `COMPUTED_ID` | an `atlas_id` with no record, one that does not match the slug, or a slug that names two records |
| `COMPUTED_STRUCTURE` | `smiles`, or a member record's `input.computed_smiles`, that is not the record's structure once re-canonicalised with the validator's RDKit |
| `COMPUTED_INCHIKEY` | an InChIKey that differs from the record's generated one (the second identity check) |
| `COMPUTED_PROTOCOL` | a `protocol` that is not the directory name; a member whose `analysis_key` or `key_fields.analysis` is not the ensemble's (espmap's normalised protocol: xc, basis, solvent with vacuum as null, grid, density fitting, geometry method, surface); or one computed with another espmap version |
| `COMPUTED_CHECKSUM` | `SHA256SUMS` missing or not UTF-8; a line not exactly `<64 lowercase hex>  <name>`; a name listed twice; a file unlisted, absent or changed; or a `record_sha256` that does not match |
| `COMPUTED_MEMBER` | a member listed twice; a record or NPZ name that is not `<conformer>.json` / `<conformer>.npz`; a missing record; a conformer file no member lists; two members with one `npz_sha256` or one `geometry_sha1`; or a record whose `geometry.sha1` is not its member's |
| `COMPUTED_RECORD` | a member file larger than 1 MB (a C18 record with its site table is about 175 kB), not UTF-8 or strict JSON, not an `espmap.record/1`, not verified by espmap (`input.structure_verified` and `validity.input` true), or not neutral and closed-shell |

YAML records and cases holding NaN or infinity are refused too
(`NUMBER_NOT_FINITE`): YAML reads `.nan` as a number, and JSON Schema's
bounds never reject it. The good fixtures use espmap's own records
(`espmap/fixtures/records/Z3Z13-18OAc_{extended,folded}.json`).

**Why identity rests on SMILES first.** A standard InChIKey merges some
tautomers (2-hydroxypyridine and 2-pyridone share one), so it is only the
second check. Each member record is checked too, so an ensemble cannot index
a conformer computed from another molecule.

**What the Atlas does not check.** The gate checks these files as an index:
present, unchanged, the right molecule, espmap's own verification, the stated
settings. It does not re-validate espmap's full record schema or recompute
anything. Atlas CI never needs espmap installed.

**NPZ surfaces.** They are not in git (`.gitignore` excludes them, and the
gate refuses one if it appears). `ensemble.json` records each surface's
`npz_sha256`. A release bundle ships them from
`--npz-dir <dir>/<slug>/<protocol>/conf_NN.npz`. Each file is read once,
hashed, and those same bytes are written to the bundle.
`build_release.py --bundle` refuses to build if `computed/` lists any NPZ and
one is missing or its sha256 differs. The exporter and the bundle builder
read only the ensembles the gate read (`atlas_validate.ensemble_paths`).

`computed/**` and `teaching/**` are marked `-text` in `.gitattributes`, so a
checkout on any platform keeps the bytes the checksums were taken of.

**When espmap's own ensemble record ships** (v0.3), it replaces this index as
a new schema version. The `/0` file is never edited in place.

## `teaching/cases/`: what a teaching bundle may assert

A case (`schemas/teaching-case.schema.json`) names:
- compounds;
- observations;
- comparisons, each between two of its own observations.

It names records only. `scripts/export_teaching_bundle.py` builds the
bundle (`schemas/teaching-bundle.schema.json`, `spa.teaching/0`).

**What a statement contains.** Every observation's `statement`, and both
sides of every comparison's `observed_contrast`, are one-line summaries
assembled from record fields, with numbers exactly as recorded:
- taxon, population and locality;
- lure, and comparator with its description;
- dose, and whether the comparator's trap or dispenser differs;
- effect, significance, both response values (or "not given") and the
  qualifier;
- detections with identification, abundance and measurements (with their
  qualifiers), negatives with their detection limits, and untested
  compounds;
- antennal readings with their preparation.

A statement is a summary, not the record. Each observation also carries:
- the full `context`;
- the structured lure, setup and outcome fields;
- `evidence`: the authors' statement, `unresolved` (what the record says its
  source does not give) and `atlas_notes` (the curator's notes, labelled as
  such).

A consumer that shows a statement should be able to show these too. The
bundle draws no conclusion.

**Roles.** Each compound lists its occurrences with their roles (`treatment`,
`comparator`, `detected`, `not_detected`, `not_tested`, `antennal_<response>`),
so a compound that was looked for and absent is never shown as produced.

**Evidence classes.** Each compound also carries `evidence_classes`: its rows
of `derived/tables/evidence_classes.tsv` (`docs/evidence-classes.md`) in every
taxon that the case's observations cover. The rows come from all Atlas records,
not only the case's, so a class can cite an observation the case leaves out.
The values are typed: counts are integers, a count that does not apply is
`null`, and populations and observation IDs are lists. `population_match`
(`yes` / `no` / `unknown`) is set only on `female_pheromone_component`. A
consumer reads these values and does not assert a class itself.
Contradictions keep both rows. A test checks that the bundle's rows equal the
table's, with none added and none dropped.

**The case author's words.** Only two pieces of text are not built from
records, and the bundle names them `case_title` and `case_label`. The case
schema refuses control and bidirectional-override characters in them.

**Validator codes** (fixtures in `tests/fixtures/bad/teaching_*`):

| code | what it refuses |
|---|---|
| `TEACH_LAYOUT` | anything in `teaching/` other than `cases/<case_id>.yaml`, any symlink, or a `teaching` that is not a directory |
| `TEACH_SCHEMA` | a case that fails its schema, including control or bidirectional characters in its own text |
| `TEACH_CASE_ID` | a `case_id` that is not the file name |
| `TEACH_REF` | an observation or compound with no record |
| `TEACH_COMPOUND_UNOBSERVED` | a compound that occurs in none of the case's observations, in any role |
| `TEACH_COMPARISON` | a comparison of an observation with itself, with one outside the case, or of a pair already compared |

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

# How records are validated

`atlas_validate.py` is the only gate. Atlas CI does not install espmap.

```bash
pip install -r requirements.txt
pytest -q                                   # good fixtures pass, every bad fixture fails for its reason
python atlas_validate.py data               # validate the curated records
python atlas_validate.py data --write-generated   # fill or refresh generated blocks
```

## What a compound must satisfy

A curator writes two fields, `names.shorthand` and `mapped_smiles`. The
validator then checks, by map number:

| check | error code |
|---|---|
| RDKit can parse the SMILES | `SMILES` |
| every heavy atom mapped, maps unique, no map on a hydrogen (espmap's gate rule) | `PARTIAL_ATOM_MAP`, `DUPLICATE_ATOM_MAP`, `MAPPED_HYDROGEN` |
| the shorthand parses (`E2,Z13-18:OAc`) and its head group is in `data/headgroups.yaml` | `SHORTHAND_SYNTAX`, `HEADGROUP_UNKNOWN` |
| chain maps are exactly 1..n, all carbon, one unbranched path | `CHAIN_MAPS` |
| head-group atoms and bonds exactly as in the table, attached only at C1 | `HEADGROUP_MISMATCH` |
| chain bonds single or double; every double bond has E/Z in the structure | `BOND_ORDER`, `STEREO_UNSPECIFIED` |
| double-bond positions and geometries in the structure equal the shorthand's | `DOUBLE_BOND_MISMATCH` |
| neutral, closed shell | `CHARGE` |
| generated block present, same generator versions, values equal a fresh regeneration | `GENERATED_MISSING`, `GENERATOR_VERSION`, `GENERATED_STALE` |

E/Z is read as the CIP label of each chain double bond. In an unbranched
chain each sp² carbon carries one chain neighbour and one hydrogen, so the
CIP label is the chain geometry that lipid shorthand names.

## Observations, genomes and references

JSON Schema (`schemas/`) enforces the shapes, including: `method` on every
component whose `detected` is true or false; `identification` only on a
detected component; a lure `purity` that names its `kind` (chemical,
isomeric, both or unspecified) and `basis` (measured or stated); a trap
and a dispenser `design` from fixed lists; a `chemical_measurement` names
its `sample` materials from a fixed list and, when it lists more than one,
says the result is `combined`; a compound has an `entity_type` (chemical or
computational model) and no class or role; three observation types and no
`role` field. The validator adds the checks below.

Two conventions the schema states but cannot check:
- **`effect` with `significance: not_tested`** is the direction of the raw
  numbers, so equal numbers always get the same label. The authors' reading
  goes in `author_statement`.
- **`identification`** follows the authors' own wording. The notes say what
  it rests on.

| check | error code |
|---|---|
| every taxon, compound, reference and `represents` id resolves | `REF_MISSING` |
| an observation ID is `spa.obs.<taxon slug>.<reference slug>.<what>`, from its own taxon and reference | `OBS_ID` |
| observations are of real compounds, never computational models | `OBS_MODEL_COMPOUND` |
| amounts only on detections; a detection limit only on a negative; a comparator differs from the treatment in blend, trap or dispenser | `OBS_FIELD_CONFLICT` |
| `genome_id` ends with the assembly accession.version | `GENOME_ID` |
| an annotation ID starts with its genome's taxon slug and is unique; the old `provider.method.geneset` form named no gene set (`2023_05` was shared by three species) | `ANNOT_ID` |
| a search ID is built from its scope, layer and date; a searched taxon exists | `SEARCH_ID`, `REF_MISSING` |
| ids unique | `DUPLICATE_ID` |
| no two taxa share an accepted name; a synonym spelling another accepted name carries both authorities | `TAXON_NAME_DUPLICATE`, `NAME_AMBIGUOUS` |

## Structural rules, not just checks

Some rules hold because the schema has no place to break them, and a bad
fixture keeps each one that way:

- **No species-level pheromone list.** A taxon has no `pheromone` field;
  what a species uses is read from its observations (`taxon_pheromone_list`).
- **No role on a compound.** Pheromone, synergist and antagonist are
  conclusions from behavioural records, per population (`compound_role_field`).
- **A field attractant is not a gland component.** Synthetic-lure results are
  `behavioural_response` records; only `chemical_measurement` records say a
  female produces or releases a compound. The two types share no fields that could carry
  one into the other.
- **A catch without a control says so** (`effect: caught_without_control`,
  and then no comparator; `control_less_with_comparator`, `missing_comparator`).

**Planned for v0.2, when reaction records arrive:** observation records
cannot be cited as evidence for a reaction. Co-occurrence of an alcohol and
its acetate in one gland is not evidence that one is made from the other.
Reaction evidence will be limited to types that test a conversion
(isotope labelling, enzyme assay, heterologous expression).

## The gate is seen to fail

`tests/fixtures/bad/` holds 28 cases, each a one-change edit of a good
fixture with the error code it must produce in `EXPECT`. On top of these,
the mutation tests flip every double bond's E/Z, once in the shorthand and
once in the structure, for every good compound, and require
`DOUBLE_BOND_MISMATCH` each time.

## Independent check of the structures

The InChIKeys generated for the six real fixture compounds were looked up
in PubChem on 2026-10-23. Each resolved to the expected name: for example
`NWRSOYAGXTXEMK-NHRIVICHSA-N` is [(2E,13Z)-octadeca-2,13-dienyl] acetate,
and `QBNCGBJHGBGHLS-NCCHCWSYSA-N` is (3Z,13Z)-octadeca-3,13-dien-1-ol. So
the E/Z reading is right, not merely self-consistent. The S-methyl model has
no PubChem entry, as expected.

## A YAML trap the schema catches

YAML 1.1 reads an unquoted `2023_05` as the integer 202305. Gene-set labels
must be quoted (`geneset: "2023_05"`); the genome schema requires a string,
and the `geneset_unquoted` fixture keeps that check honest.

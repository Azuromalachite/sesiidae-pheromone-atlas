# Sesiidae Pheromone Atlas

**Working repository:** `Azuromalachite/sesiidae-pheromone-atlas`  
**Working subtitle:** *A curated, machine-readable resource linking Sesiidae pheromone chemistry, genomes, biosynthetic hypotheses, and candidate enzyme families.*  
**Revision 2, 2026-10-23.** Addresses findings F1–F9 of adversarial review 1 (`atlas-concept-review-1.md`). F10–F12 are still open; see §0.

---

## 0. Changes in revision 2

| finding | what changed | sections |
|---|---|---|
| F1 taxa without genomes | taxa are chosen from a taxon × layer matrix built first; the expansion set is replaced by NCBI-assembled species; *S. myopaeformis* added | §4, §33, §36 |
| F2 no RefSeq proteins | protein identity = assembly + annotation source + release + stable ID; gene-level absence needs a genome-level search | §15, §15a, §20, §29 |
| F3 espmap on the wrong molecule | the espmap subject is a curated precursor model (truncated thioester), not the pheromone; site contrasts are reported against the per-site budget | §25, §26 |
| F4 partial atom maps | head-group heavy atoms get maps from 101; CI runs `espmap --check` on every compound | §11, §12 |
| F5 E2/E3 origin | Route C (enoyl intermediates of elongation or β-oxidation, and isomerisation); ACOX, elongation-cycle enzymes and enoyl-CoA isomerase added; isotope labelling is an evidence type | §16, §18, §19, §37 |
| F6 observation model | typed observations; method per measurement; `detected: true/false/not_tested` with detection limit; `role` split into abundance class and behavioural effect | §13, §35 |
| F7 redundant encodings | only `shorthand` and `mapped_smiles` are hand-entered; everything else is generated and diffed in CI | §10, §12 |
| F8 precursors without structure | acyl-CoA, free acid, alcohol, aldehyde and acetate are separate compounds with full structures; computational models link to them | §10a, §16 |
| F9 gate after data | validator and CI precede the first curated record | §36 |

Still open: F10 (separate data licence; Pherobase reuse terms not yet found), F11 (out-of-family reference taxa such as *Zeuzera pyrina*), F12 (cite espmap schema IDs, not a package version — partly done in §25).

The natural-history motivation (the *Amegilla* → Sesiidae origin, lipid-derived signalling, the C18 pheromone cases) lives in the companion document `sesiidae_context_lipid_signaling_amegilla_motivation.md`. Species chemistry quoted from it in §4.3 is a summary, not a curated record, until the primary papers are read.

---

## 1. Core idea

The **Sesiidae Pheromone Atlas** is an independently useful scientific resource connecting five domains that are usually scattered across separate papers and databases:

1. Sesiidae species and taxonomy
2. Pheromone chemistry and experimentally observed blends
3. Genome and proteome resources
4. Candidate biosynthetic reactions and pathways
5. Candidate enzyme families and ranked genomic candidates

The intended project relationship is:

```text
espmap
    molecular electronic analysis
    geometry → ESP → reaction-site descriptors → uncertainty/provenance

Sesiidae Pheromone Atlas
    biological and chemical knowledge resource
    species ↔ pheromones ↔ genomes ↔ pathways ↔ candidate enzymes

Arrowfield
    educational / mechanistic-reasoning environment
    presents and connects evidence layers for learners
```

A concise philosophy:

> **The Atlas records what is known, what is inferred, and what is hypothesized. espmap measures one layer of molecular evidence. Arrowfield teaches how to reason across those layers.**

---

## 2. Why this deserves its own repository

The target is no longer merely an Arrowfield case. The goal is:

> **a curated, machine-readable resource connecting Sesiidae species, pheromone chemistry, genomes, candidate pathways, and enzyme families.**

That requires its own:

- data model;
- curation rules;
- provenance model;
- versioned releases;
- validation tests;
- computational workflows;
- evidence vocabulary;
- independent scientific identity.

Arrowfield should consume the Atlas rather than own it.

---

## 3. Scientific motivation

Sesiidae are unusually attractive because they combine:

- distinctive long-chain pheromone chemistry;
- repeated use of unusual C18 diene systems;
- strong biological discrimination among closely related structural isomers;
- sparse biosynthetic-genetic characterization;
- a growing number of usable genome assemblies;
- an opportunity to connect organic chemistry, chemical ecology, genomics, enzyme evolution, and molecular modelling.

For an enigmatic insect family, a **matched nuclear genome + experimentally characterized pheromone profile** is already enough to support serious candidate-pathway reconstruction.

Pheromone-gland RNA-seq, direct biochemical assays, knockouts, or expression data should be treated as valuable future evidence, not prerequisites for inclusion.

---

## 4. Initial biological focus

Taxa are chosen from data, not from interest. The first artefact of the
project is a **taxon × layer matrix** (§4.3); a taxon enters v0.1 with a
genome layer only if the matrix shows both an assembly and a characterised
pheromone.

### 4.1 *Synanthedon tipuliformis*

Strong first flagship because:

- a chromosome-level nuclear genome exists: ilSynTipu2.1, GCA_947623395.1, 295.8 Mb, DToL (Boyes & Holland, Wellcome Open Res 8:300). Gene models come from Ensembl (11,878 protein-coding genes), not NCBI;
- gland chemistry is characterised: E2,Z13-18:OAc, E3,Z13-18:OAc, Z13-18:OAc and E2,Z13-18:OH (reported 100 : 0.7 : 2.7 : 3.2), with Z13-18:OH and 18:OH in traces;
- the Δ2 versus Δ3 distinction creates a natural regioselectivity problem;
- the gland alcohols are candidate pathway intermediates;
- the behavioural effect of E3 differs between populations (synergist in Hungary and New Zealand, reduces catches in Tasmania), so the record has to keep populations apart (§13).

The genome specimen is a single male from Wytham Woods, UK. "Matched genome
and pheromone" means matched at species level; no pheromone record so far
comes from the sequenced population.

### 4.2 *Sesia apiformis*

Strong complementary case because:

- a chromosome-level nuclear genome exists: ilSesApif2.1, GCA_914767545.1, 546.8 Mb (Ensembl: 16,358 protein-coding genes);
- the gland blend is Z3,Z13-18:OH and E2,Z13-18:Al, with E2,Z13-18:OH as a minor component (Francke et al. 2004);
- it **shares the E2,Z13 backbone** with *S. tipuliformis* (as the aldehyde rather than the acetate), and carries the Δ3 bond as **Z** where *S. tipuliformis* has **E**;
- so the pair is a controlled comparison: same Δ2/Δ13 skeleton, different terminal group, opposite Δ3 geometry.

The two flagship annotations differ by 38 % in gene count. Any comparison
of family sizes between them is conditional on the two annotation runs (§15a).

### 4.3 The taxon × layer matrix and the expansion set

NCBI Datasets listed 21 Sesiidae assemblies from 11 species on 2026-10-23,
none of them with an NCBI annotation:

| species | assembly (primary) | pheromone identified? |
|---|---|---|
| *Synanthedon tipuliformis* | GCA_947623395.1 | yes (flagship) |
| *Sesia apiformis* | GCA_914767545.1 | yes (flagship) |
| *Synanthedon myopaeformis* | GCA_944738685.1 | yes: Z3,Z13-18:OAc, GC-EAD (Judd et al. 2011) |
| *Synanthedon formicaeformis* | GCA_945859745.1 | to check |
| *Synanthedon vespiformis* | GCA_918317495.1 | to check |
| *Synanthedon andrenaeformis* | GCA_936446665.2 | to check |
| *Synanthedon spheciformis* | GCA_964332195.1 | to check |
| *Sesia bembeciformis* | GCA_943735995.1 | to check |
| *Bembecia ichneumoniformis* | GCA_910589475.2 | to check |
| *Pyropteron chrysidiforme* | GCA_982500485.1 / GCA_982500805.1 (haplotypes) | to check |
| *Sphecodoptera sheni* | GCA_062004741.1 | to check |

"To check" means a primary-literature search has not been done, not that no
pheromone is known. The matrix is regenerated from the NCBI API and committed
as `releases/taxon_layers.tsv`; the table above is a snapshot.

Expansion set for v0.1: *S. myopaeformis* (Z3,Z13 acetate, the Δ3 geometry of
*S. apiformis* on the terminal group of *S. tipuliformis*), plus any "to
check" species whose pheromone turns out to be characterised.

*Synanthedon bicingulata*, *S. tenuis* and *Nokona pernix* stay as
chemistry-only rows: none has a nuclear assembly (*S. bicingulata* has a
mitogenome). They are valuable for compound and observation records, because
together they cover the 3,13-diene space the flagships leave open (as
summarised in the companion context document §12, primary papers still to be
read for curation):

| species | reported components | why it matters here |
|---|---|---|
| *S. bicingulata* | E3,Z13-18:OAc + Z3,Z13-18:OAc, ~4 : 6 | both Δ3 geometries in one gland |
| *S. tenuis* | Z3,Z13-18:OH; the acetate **not detected** and inhibitory when added | a tested negative (§13) |
| *N. pernix* | E3,Z13-18:OH + Z3,Z13-18:OH, ~9 : 1 | both Δ3 geometries as alcohols |
| *S. scoliaeformis* | E2,Z13-18:OAc, specificity vs *S. tipuliformis* by minor components, antagonism and timing | same major compound, different channel |

Their chemistry enters the compound and observation layers; their genomes
stay "—" until an assembly exists.

Not every taxon needs every layer. Missing data should be explicit:

```text
pheromone data ✓
genome data   —
pathway       hypothesis only
enzyme candidates —
```

---

## 5. Central epistemic principle

The Atlas should rigorously separate:

```text
OBSERVATION
    ↓
what was actually measured or reported

INFERENCE
    ↓
what follows from sequence comparison, computation, phylogeny, etc.

HYPOTHESIS
    ↓
a proposed biological explanation or pathway
```

Example:

- **Observation:** female *S. tipuliformis* glands contain `E2,Z13-18:OAc`.
- **Inference:** a protein clusters near characterized lepidopteran pheromone desaturases.
- **Hypothesis:** that protein contributes to biosynthesis of the E2 pheromone component.

These should never collapse into one another through documentation drift.

---

## 6. Database-as-code architecture

Do not start with a web database or SQL-first application.

Preferred architecture:

```text
human-curated YAML
        ↓
JSON Schema validation
        ↓
generated machine-readable releases
        ↓
JSON / TSV / Parquet / SQLite or DuckDB
```

Advantages:

- readable Git diffs;
- human-reviewable curation;
- transparent provenance;
- reproducible releases;
- low infrastructure burden;
- straightforward CI validation.

A website or API can be generated later from the same source.

---

## 7. Proposed repository structure

```text
sesiidae-pheromone-atlas/
├── README.md
├── LICENSE
├── CITATION.cff
│
├── data/
│   ├── taxa/
│   ├── compounds/
│   ├── pheromone_observations/
│   ├── genomes/
│   ├── proteins/
│   ├── reactions/
│   ├── pathways/
│   ├── enzyme_candidates/
│   ├── references/
│   └── headgroups.yaml        # head-group atom maps from 101 (§11)
│
├── schemas/
│   ├── taxon.schema.json
│   ├── compound.schema.json
│   ├── observation.schema.json
│   ├── genome.schema.json
│   ├── protein.schema.json
│   ├── reaction.schema.json
│   ├── pathway.schema.json
│   ├── candidate.schema.json
│   └── assertion.schema.json
│
├── derived/
│   ├── homology/
│   ├── hmmer/
│   ├── interpro/
│   ├── phylogeny/
│   ├── structures/
│   └── espmap/
│
├── workflows/
│   ├── compound_validation/
│   ├── genome_mining/
│   ├── phylogeny/
│   └── releases/
│
├── tests/
├── docs/
└── releases/
```

---

## 8. Core entity model

Initial entity types:

1. Taxon
2. Compound
3. Pheromone observation
4. Genome assembly
5. Characterized protein/enzyme
6. Reaction
7. Pathway hypothesis
8. Candidate enzyme assertion

A ninth generic **assertion** entity can later unify evidence-bearing claims.

---

## 9. Taxon record

```yaml
taxon_id: sesiidae.synanthedon_tipuliformis
scientific_name: Synanthedon tipuliformis

taxonomy:
  family: Sesiidae
  genus: Synanthedon
  species: tipuliformis

identifiers:
  ncbi_taxid: null
  gbif: null
```

Preferred external identifiers:

- NCBI TaxID for sequence/genome interoperability;
- optional GBIF identifier for biodiversity interoperability.

Never guess identifiers.

---

## 10. Compound record

Compound records provide the **chemical identity spine**.

Two fields are written by a curator: `shorthand` and `mapped_smiles`.
Everything else in the structure and annotation blocks is **generated** from
them by the release workflow and committed so diffs stay readable; CI
regenerates it and fails on any difference. One fact, one hand-entered
copy — the same rule espmap learned for its file reader.

```yaml
compound_id: pheromone.e2_z13_18_oac
compound_class: pheromone_component   # or precursor, computational_model (§10a)

# --- curated ---
names:
  shorthand: E2,Z13-18:OAc
  systematic: null                     # optional, checked against the structure if given
mapped_smiles: "..."                   # every heavy atom mapped (§11)

external_ids:
  chebi: null                          # only when a correct entry exists

# --- generated (do not edit) ---
generated:
  canonical_isomeric_smiles: "..."
  inchi: "..."
  inchikey: "..."
  lipid_annotation:                    # parsed from the shorthand
    chain_length: 18
    unsaturation_count: 2
    double_bonds:
      - position: 2
        geometry: E
      - position: 13
        geometry: Z
    terminal_group: acetate
```

Why multiple identifiers:

- `compound_id`: stable Atlas-internal ID;
- mapped SMILES: structure, computation and persistent atom identity;
- canonical isomeric SMILES, InChI/InChIKey: generated, for external matching;
- ChEBI: only when a correct entry exists.

Never force a misleading external identifier merely to fill a field.

### 10a. Precursors and computational models are compounds too

The biosynthetic intermediates are separate compound records with full
structures, never fragments such as "Z13-18 acyl":

| `compound_class` | example | represented as |
|---|---|---|
| `precursor` | Z13-18:CoA | full acyl-CoA SMILES, CoA stereocentres explicit |
| `precursor` | Z13-18:acid | free fatty acid |
| `pheromone_component` / `precursor` | Z13-18:OH, Z13-18:Al | alcohol, aldehyde |
| `pheromone_component` | Z13-18:OAc | acetate |
| `computational_model` | Z13-18:SMe | S-methyl thioester standing in for the acyl-CoA |

A `computational_model` record must say what it stands for and what was cut:

```yaml
compound_id: model.z13_18_sme
compound_class: computational_model
represents: precursor.z13_18_coa
truncation: "CoA replaced by S-methyl at the thioester sulfur"
```

Chain maps (§11) are identical across the whole series, so C2 of the
acyl-CoA, the alcohol, the acetate and the model is the same map number.
That is a statement about identity, not chemistry: C2 is α to a carbonyl in
the thioester and β to an ether oxygen in the acetate.

---

## 11. Atom mapping convention

The mapped SMILES should bridge all analytical layers.

For linear C18 pheromone scaffolds:

```text
map 1  = biochemical carbon C1
map 2  = C2
map 3  = C3
...
map 18 = C18
```

C1 is the carbon that carries the oxygen function: the carbonyl carbon of
an acid, acyl-CoA or aldehyde, and the CH₂–O carbon of an alcohol or acetate.
Reduction and acetylation do not move it, so the chain maps are the same
along the whole pathway.

**Every heavy atom is mapped.** espmap refuses partial heavy-atom maps
(`PARTIAL_ATOM_MAP`, a gate BLOCK), and a site table with holes is worse
than none. Head-group atoms take maps from **101**, by a fixed table kept in
`data/headgroups.yaml`:

| head group | 101 | 102 | 103 | 104 |
|---|---|---|---|---|
| alcohol (–OH) | O | | | |
| aldehyde (–CHO) | O | | | |
| acid (–COOH) | O (=O) | O (–OH) | | |
| acetate (–O–C(=O)–CH₃) | O (ester, on C1) | C (carbonyl) | O (carbonyl) | C (methyl) |
| S-methyl thioester (–C(=O)–S–CH₃) | O (carbonyl) | S | C (methyl) | |

Larger head groups (full CoA, N-acetylcysteamine) continue the numbering in
the same file. Hydrogens are never mapped; sites reach them with `"N+H"`.

espmap's existing C18 fixture (`bench/fixtures/Z3Z13-18OAc_*.sdf`) is
unmapped and written acetate-first, so its RDKit index 4 is C1. Atlas
records never join to espmap by index; the espmap P3 fixture should adopt
these maps.

Then:

```yaml
double_bonds:
  - position: 3
    geometry: Z
  - position: 13
    geometry: Z
```

and an espmap site:

```json
{
  "by": "map",
  "groups": [
    {"label": "C3-H", "atoms": ["3+H"]}
  ]
}
```

refer to the same carbon identity.

Identity chain:

```text
pheromone literature
        ↓
biochemical carbon numbering
        ↓
mapped SMILES
        ↓
espmap reaction sites
        ↓
enzyme-complex geometry
        ↓
Arrowfield lesson
```

---

## 12. Automatic compound validation

Use RDKit to verify that the **shorthand** and the **mapped structure**
agree — the two hand-entered fields, so that nothing generated can hide a
disagreement between them.

The validator:

1. parses the shorthand (`Z3,Z13-18:OH`) into chain length, double-bond
   positions and geometries, and terminal group;
2. checks the mapped SMILES: chain maps are exactly 1…n along one unbranched
   path from C1; every heavy atom has a map; head-group maps follow
   `data/headgroups.yaml`;
3. reads double bonds and their E/Z from the structure **by map number**
   and compares them with step 1;
4. regenerates canonical SMILES, InChI, InChIKey and the lipid annotation and
   fails if the committed copies differ;
5. runs `espmap --check` (the admissibility gate only, no SCF) on every
   compound, so a record that espmap would refuse fails here first.

The check must catch mistakes such as:

```text
display name: Z3,Z13-18:OH
structure:    E3,Z13-18:OH
```

and CI proves it does: a test flips one E/Z in each fixture shorthand, and
then in each fixture structure, and requires the validator to fail every time.

---

## 13. Pheromone observations

Do **not** flatten evidence into `species → pheromone`.

The observation itself should be a first-class record, and it is **typed**:
what a gland contains and what males respond to are different measurements
and get different shapes.

| `observation_type` | what was measured | carries |
|---|---|---|
| `gland_composition` | compounds present in gland extract or effluvia | per-component detection and abundance, each with its method |
| `behavioural_response` | male response to a synthetic blend in a field or wind-tunnel test | blend, comparator, locality, effect |
| `electrophysiology` | antennal response (EAG, GC-EAD) | compound, response |

Two existing records show why: the *S. apiformis* aldehyde : alcohol ratio is
about 2 : 3 in pooled gland extract and about 1 : 7 by SPME of single calling
females, a 4.7-fold difference from the method alone; and *S. tipuliformis*'s
E3 component is a synergist in Hungary and New Zealand and reduces catches in
Tasmania. A per-observation `methods` list and a `role: minor` field can hold
neither.

```yaml
observation_id: obs.tipuliformis.<ref>.001
observation_type: gland_composition
taxon: sesiidae.synanthedon_tipuliformis

context:
  sex: female
  tissue: pheromone_gland
  life_stage: adult
  population: null
  locality: null

components:
  - compound: pheromone.e2_z13_18_oac
    detected: true
    abundance_class: major              # major | minor | trace, as the paper states it
    measurements:
      - value: <from primary paper>
        unit: relative_to_major         # or percent, ng_per_female
        method: gland_extract_gc_ms
        qualifier: as_reported

  - compound: pheromone.e3_z13_18_oac
    detected: true
    abundance_class: minor
    measurements: []

  - compound: pheromone.z3_z13_18_oac
    detected: false                     # looked for and not found
    detection_limit: null               # give it when the paper does
    method: gland_extract_gc_ms

evidence:
  reference: ref.<id>
```

```yaml
observation_id: obs.tipuliformis.<ref>.trap.003
observation_type: behavioural_response
taxon: sesiidae.synanthedon_tipuliformis
context:
  locality: <as reported>
  population: <as reported>
blend:
  - compound: pheromone.e2_z13_18_oac
    amount: <as reported>
  - compound: pheromone.e3_z13_18_oac
    amount: <as reported>
comparator: E2,Z13-18:OAc alone
effect: decreased                       # increased | decreased | no_effect
evidence:
  reference: ref.<id>
```

`detected` has three values. `not_tested` (the default) is unknown;
`false` is a real negative that says how it was looked for. The *S. tenuis*
gland acetate, not detected and inhibitory when added, needs both a
`gland_composition` record with `detected: false` and a
`behavioural_response` record with `effect: decreased`.

"Synergist" and "antagonist" are never fields of a compound or of a gland
record. They are conclusions from `behavioural_response` records, and they
can differ between populations.

Placeholders in examples are written `<…>` so they cannot be mistaken for
data.

This allows different studies to coexist even when they differ in:

- blend ratio;
- locality;
- season;
- population;
- analytical method;
- gland chemistry versus behavioral lure response.

Do not manufacture false consensus.

---

## 14. Literature provenance

Pherobase can be used for:

```text
discovery
cross-checking
finding primary papers
```

but important records should be traced to primary literature where possible.

For each observation preserve:

- publication;
- biological material measured;
- analytical method;
- whether compound identification was direct;
- whether blend proportion was measured;
- whether behavioral activity was tested;
- uncertainty/qualification.

The Atlas contribution is **normalization, provenance, and linkage**, not appropriation of another database's curation.

---

## 15. Genome record

```yaml
genome_id: genome.synanthedon_tipuliformis.GCA_947623395.1

taxon: sesiidae.synanthedon_tipuliformis

assembly:
  accession: GCA_947623395
  version: 1
  name: ilSynTipu2.1
  level: chromosome
  source: NCBI
  specimen: <sex, locality as in the genome note>

bioproject: <PRJ…>
biosample: <SAM…>

annotations:                            # an assembly can have several
  - annotation_id: annot.ensembl_rapid.<release>
    source: Ensembl Rapid Release       # none of the NCBI Sesiidae assemblies is annotated
    release: <release>
    protein_coding_genes: 11878
    files:
      protein_fasta: <url + sha256>
      gff3: <url + sha256>
```

Stable assembly accession/version should be the identity, not a filename.
Annotation is a separate, versioned layer on top of it.

Useful identifiers:

- GCA/GCF;
- BioProject;
- BioSample;
- annotation source and release;
- gene/transcript/protein stable IDs within that release.

### 15a. Protein identity is an annotation, not a sequence database entry

On 2026-10-23 none of the 21 NCBI Sesiidae assemblies carried an NCBI
annotation, so there are no RefSeq `XP_` proteins to curate. The gene models
that exist are Ensembl's. A protein in the Atlas is therefore identified by:

```text
(assembly accession.version, annotation source, annotation release, stable ID)
```

with `refseq_protein` and `uniprot` as optional cross-references when they
appear. Stable IDs can change between releases; the release is part of the
identity, and a release change is a migration with its own diff.

Two consequences:

- **Gene counts compare annotations as much as genomes.** *S. apiformis* has
  38 % more annotated protein-coding genes than *S. tipuliformis* (16,358 vs
  11,878) on a 1.85× larger assembly. "Family X has n members here and m
  there" is stated per annotation release.
- **A missing gene model is not a missing gene.** Before a family is recorded
  as absent or small in a species, the family's reference proteins are
  searched against the assembly itself (tblastn or a spliced aligner such as
  miniprot), and the record says how many hits came from the annotation and
  how many only from the genome search.

---

## 16. Reaction records

Distinguish established reactions from local hypotheses.

### Established reaction

```yaml
reaction_id: rhea.12345
rhea_id: RHEA:12345

substrates:
  - compound: ...

products:
  - compound: ...

status: established
```

### Atlas-local hypothetical reaction

```yaml
reaction_id: spa.rxn.0007

name: proposed E2 desaturation of Z13-18:CoA

substrates:
  - compound: precursor.z13_18_coa

products:
  - compound: precursor.e2_z13_18_coa

enzyme_family:
  - membrane_fatty_acyl_desaturase

status: hypothetical

evidence:
  - type: analogy_to_characterized_lepidopteran_pathway
    reference: ref....
```

and, for the same product, a competing reaction from a different enzyme class:

```yaml
reaction_id: spa.rxn.0008

name: E2,Z13-18:CoA as a released elongation-cycle intermediate

substrates:
  - compound: precursor.z11_16_coa      # + malonyl-CoA, via 3-keto and 3-hydroxy intermediates
products:
  - compound: precursor.e2_z13_18_coa

enzyme_family:
  - fatty_acyl_elongase_cycle           # ELO condensation, KAR, HACD; TER would reduce the E2 bond

status: hypothetical
```

Substrates and products are full compound records (§10a), never fragments.
Every reaction's mapped SMILES must conserve the chain maps 1…n from
substrate to product; cofactors are listed but not atom-balanced in v0.2.

Absence from Rhea must not be treated as evidence against a specialized Sesiidae reaction.

---

## 17. Pathway reconstruction philosophy

Reconstruct **chemistry first, genes second**.

```text
observed pheromone blend
        ↓
enumerate plausible precursors
        ↓
construct alternative reaction graphs
        ↓
assign plausible enzyme families to each arrow
        ↓
search the Sesiidae genome
        ↓
rank candidate proteins
        ↓
test mechanistic/structural plausibility
```

Generic metabolic pathway tools should serve as references, not as the main authority.

---

## 18. Competing pathway hypotheses

The Atlas should not store a single inferred route as established fact.

Example:

```yaml
pathway_id: pathway.tipuliformis.z13.direct_delta13.v1
status: hypothesis
steps:
  - reaction: spa.rxn.direct_delta13
  - reaction: spa.rxn.reduction
  - reaction: spa.rxn.acetylation
```

and alongside it:

```yaml
pathway_id: pathway.tipuliformis.z13.delta11_elongation.v1
status: hypothesis
steps:
  - reaction: spa.rxn.delta11_C16
  - reaction: spa.rxn.elongation_C16_C18
  - reaction: spa.rxn.reduction
  - reaction: spa.rxn.acetylation
```

A Z13-C18 system should explicitly consider at least:

```text
Route A
18:0
  ↓ direct Δ13 desaturation
Z13-18

Route B
16:0
  ↓ Δ11 desaturation
Z11-16
  ↓ +C2 elongation
Z13-18
```

before assuming a direct Δ13 enzyme. Δ11-C16 followed by elongation to a
Z13-C18 product has precedent in another moth (Z13-18 aldehyde
bioproduction work), so Route B is not merely formal.

The Δ2 and Δ3 bonds need the same treatment. Desaturation is one origin, and
the chemistry of fatty-acyl-CoA metabolism offers others:

```text
Route C1  elongation-cycle intermediate
Z11-16:CoA
  ↓ condensation, 3-keto reduction, dehydration
E2,Z13-18:CoA        ← normally reduced by trans-2-enoyl-CoA reductase (TER)
  ↓ released or diverted before TER
E2,Z13 product

Route C2  β-oxidation intermediate
Z13-18:CoA (or a longer chain)
  ↓ acyl-CoA oxidase (ACOX)
E2,Z13-18:CoA

Route C3  isomerisation
E2,Z13-18:CoA
  ⇄ Δ3,Δ2-enoyl-CoA isomerase
E3,Z13-18:CoA
```

These are hypotheses from general fatty-acid biochemistry, not findings:
no Sesiidae study testing them was found (review 1, F5). They make
distinct predictions. C1 ties the E2 bond to the elongation step of Route B;
C3 predicts that E3 tracks E2 and stays a minor partner of it, as in
*S. tipuliformis* (100 : 0.7); none of them explains Z3 without a further
step, which *S. apiformis*, *S. bicingulata* and *N. pernix* require.

Every pathway hypothesis lists, per step, the experiment that would
distinguish it from its competitors (§37).

---

## 19. Characterized reference enzymes

Known functionally characterized enzymes must be separate from Sesiidae candidates.

```yaml
protein_id: uniprot.QXXXX

taxon: some_lepidopteran_species

sequence:
  accession: QXXXX
  source: UniProt

function:
  enzyme_family: fatty_acyl_desaturase
  activity: delta11_desaturase
  reaction: spa.rxn.delta11_C16

evidence:
  status: functionally_characterized
  assay:
    - heterologous_expression
  reference: ref....
```

Priority reference families:

```text
fatty-acyl desaturases
├── Δ9
├── Δ10
├── Δ11
├── Δ12/Δ13-like
├── unusual regio-/stereoselective FADs
└── multifunctional FADs

elongation cycle
├── elongases (ELO, condensing step)
├── 3-ketoacyl-CoA reductase (KAR)
├── 3-hydroxyacyl-CoA dehydratase (HACD)
└── trans-2-enoyl-CoA reductase (TER)

β-oxidation / chain shortening
├── acyl-CoA oxidases (ACOX)
└── Δ3,Δ2-enoyl-CoA isomerases (ECI)

fatty-acyl reductases
acetyltransferase candidates
alcohol/aldehyde oxidoreductases
```

TER, ACOX and ECI are on the list because each can make or move a Δ2/Δ3
bond (Route C, §18), not because any has been implicated in Sesiidae.

---

## 20. Candidate enzyme records

A genomic candidate should never receive a demonstrated function solely because it is the closest BLAST hit.

```yaml
candidate_id: candidate.tipuliformis.DES07.delta11

protein:
  genome: genome.synanthedon_tipuliformis.GCA_947623395.1
  annotation: annot.ensembl_rapid.<release>
  stable_id: <Ensembl gene / transcript ID>
  model_source: annotation            # or genome_search (§15a)
  refseq_protein: null
  uniprot: null

candidate_for:
  reaction: spa.rxn.delta11_C16

evidence:
  - type: sequence_similarity
    source: derived/homology/...

  - type: profile_hmm
    source: derived/hmmer/...

  - type: domain_architecture
    source: derived/interpro/...

  - type: phylogenetic_placement
    source: derived/phylogeny/...

  - type: structural_plausibility
    source: derived/structures/...

missing_evidence:
  - pheromone_gland_expression
  - biochemical_assay
  - isotope_labelling_of_the_route

status: candidate
```

Missing RNA-seq or biochemical data are **missing evidence**, not negative evidence.

---

## 21. Genome-mining workflow

Recommended first-pass stack:

| Task | Tool |
|---|---|
| Pheromone discovery | Pherobase + primary literature |
| Chemical representation | RDKit |
| Reaction vocabulary | Rhea |
| Enzyme specificity/literature | BRENDA + UniProt |
| Genome retrieval | NCBI Datasets |
| Gene models | Ensembl Rapid Release (versioned, §15a) |
| Genome-level family search | tblastn / miniprot against the assembly |
| Insect cross-reference | InsectBase |
| Similarity search | DIAMOND / BLASTP |
| Sensitive family search | HMMER |
| Domain/motif/topology | InterProScan |
| Alignment | MAFFT |
| Trimming if needed | ClipKIT / trimAl |
| Phylogeny | IQ-TREE |
| Tree visualization | iTOL |
| Cross-species orthology | OrthoFinder, later |
| Substrate electronics | espmap |
| Protein structures | AlphaFold / AF3, later |
| Structural similarity | Foldseek |
| Data manipulation | Python / Pandas / NetworkX |

First-pass candidate ranking should rely on:

```text
similarity
+
family membership
+
motif/domain sanity
+
phylogenetic placement
```

not structure prediction alone.

---

## 22. Phylogeny as a major evidence layer

For each enzyme family:

```text
Sesiidae candidates
+
functionally characterized moth enzymes
+
representative housekeeping homologs
```

should be analyzed together:

```text
MAFFT
  ↓
optional ClipKIT / trimAl
  ↓
IQ-TREE
  ↓
iTOL
```

Phylogeny can help identify:

- housekeeping enzymes;
- pheromone-biosynthetic clades;
- lineage-specific duplications;
- unusual orphan clades;
- possible Sesiidae-specific expansions.

It remains inference, not direct proof of function.

---

## 23. OrthoFinder as a later comparative layer

Once multiple good Sesiidae genomes are available:

```text
S. tipuliformis
S. apiformis
other Sesiidae
related Lepidoptera
```

OrthoFinder can test:

- orthogroups;
- one-to-one orthologs;
- gene duplications;
- lineage-specific expansions;
- candidate family turnover.

---

## 24. Structural modelling comes after candidate narrowing

Preferred order:

```text
all family members
        ↓
homology / HMM
        ↓
motif and domain sanity
        ↓
phylogenetic ranking
        ↓
small candidate set
        ↓
AlphaFold / AF3
```

Protein structures can then ask:

- is the fold plausible?
- are catalytic motifs positioned correctly?
- is a C16/C18 substrate tunnel plausible?
- can candidate substrate geometry be accommodated?

Structure prediction alone should not be used to assign exact regioselectivity.

---

## 25. espmap integration

`espmap` remains a separate scientific instrument.

**What espmap is run on.** A site question about an enzyme is a question
about that enzyme's substrate. The desaturases, oxidases and isomerases of
§19 act on fatty acyl-CoA, where C1 is a thioester carbonyl; in the acetate
pheromone, C1 is a CH₂–O carbon. Chain maps make C2 the same atom in both
(§10a), but its electronic environment is different: α to a carbonyl in one,
β to an ether oxygen in the other. And on E2,Z13-18:OAc the C2–C3 bond is
already double, so the product cannot answer where that bond was made.

So the espmap subject is a **curated `computational_model` compound** that
stands for the substrate of the step in question, e.g. `model.z13_18_sme`
(the S-methyl thioester for Z13-18:CoA, §10a). Its record states the
truncation, because C2's electronics depend on it. Pheromone components may
also be computed, for questions about the signal itself (receptor-facing
electronics), never as proxies for a biosynthetic substrate.

The Atlas stores derived output keyed by the computed compound:

```text
derived/espmap/
└── model.z13_18_sme/
    ├── conformer_001/
    │   ├── record.json
    │   └── surface.npz
    └── conformer_002/
```

The primary compound record should not copy derived ESP values into itself.

Instead:

```yaml
analysis:
  tool: espmap
  record_schema: espmap.record/1
  sites_schema: espmap.sites/1
  analysis_key: <from the record>
  record: derived/espmap/...
```

Comparability follows espmap's own rule: two records are compared only when
their record schema, site schema and `analysis_key` match. A package version
is not an identity.

This preserves the distinction between curated identity and replaceable computation.

---

## 26. Reaction-site integration

For a mapped C18 substrate model (§25), not the pheromone:

```json
{
  "by": "map",
  "groups": [
    {"label": "C2-H",  "atoms": ["2+H"]},
    {"label": "C3-H",  "atoms": ["3+H"]},
    {"label": "C4-H",  "atoms": ["4+H"]},
    {"label": "C13-H", "atoms": ["13+H"]}
  ]
}
```

can ask:

> Does intrinsic substrate electrostatics robustly distinguish candidate reaction sites?

Important limitation:

> **espmap does not predict which site an enzyme will react at.**

It provides one evidence layer:

```text
intrinsic substrate electronics
```

which later joins:

```text
enzyme geometry
phylogenetic evidence
reaction chemistry
experimental evidence
```

**Whether the question can be answered at all is measured first.** On the
closest molecule espmap has computed, the Z3,Z13-18:OAc fixture over 10 MMFF
conformers (`bench/site_partition.jsonl`), per-carbon site means separate
sp² from sp³ carbons (C3/C4 and C13/C14 at −0.9 to 2.4 kcal/mol, chain CH₂
at 3–9), but the conformer range at a single site reaches 6.5 kcal/mol (C5:
2.2 to 8.7), more than most differences between neighbouring CH₂ sites.
espmap's per-site budget says the same: the median C18 site moves 5.1
kcal/mol across conformers and up to 3.95 with the partition rule.

So a C2-vs-C3-vs-C4 comparison is reported as a difference **with its
conformer and partition-rule spreads**, and the Atlas says "not resolved by
substrate electrostatics" when the difference is inside them. That outcome
is a result, not a failure: it is the point at which the question passes to
enzyme geometry (Arrowfield's "what does the protein contribute?").

The calibration comes before any site claim: one run of the thioester model
over a conformer set that includes folded shapes, with the C2–C3 and C3–C4
mean differences and their spreads written into the Atlas docs.

---

## 27. Derived analyses are replaceable

Core invariant:

```text
source biological record
            ↓
        curated provenance

replaceable derived computation
            ↓
    reproducibly regenerable
```

Therefore:

```text
derived/
├── diamond/
├── hmmer/
├── interpro/
├── mafft/
├── iqtree/
├── structures/
└── espmap/
```

must never be treated as manually curated fact.

---

## 28. Generic assertion model

A later version should introduce explicit evidence-bearing assertions:

```yaml
assertion_id: assertion.000123

subject: candidate.tipuliformis.DES07
predicate: candidate_for
object: spa.rxn.delta11_C16

evidence:
  - evidence_type: phylogenetic_inference
    eco_id: null
    source: derived/phylogeny/fad_tree/
    reference: null

curation:
  curator: null
  date: 2026-...
```

The schema should reserve space for **ECO — Evidence & Conclusion Ontology** identifiers from the beginning, without requiring full ontology integration in v0.1.

---

## 29. External identifier strategy

| Entity | External handles |
|---|---|
| Taxon | NCBI TaxID; optional GBIF |
| Compound | InChI, InChIKey, ChEBI |
| Genome | GCA/GCF, BioProject, BioSample |
| Protein | assembly + annotation release + stable ID (§15a); NCBI protein / UniProt when they exist |
| Reaction | RHEA, EC |
| Functional annotation | GO, InterPro, Pfam |
| Publication | DOI, PMID |
| Evidence | ECO |

External identifiers supplement Atlas IDs; they do not replace them.

---

## 30. Intellectual provenance and curation policy

Apply the same provenance discipline used in espmap.

For each assertion ask:

1. What was directly observed?
2. What paper/database supports it?
3. Is the Atlas reproducing a fact or making an inference?
4. What normalization did the Atlas add?
5. What remains unknown?

For secondary sources:

```text
secondary resource
      ↓
discovery / cross-check
      ↓
primary paper where possible
      ↓
Atlas observation record
```

The project should credit upstream databases clearly and never present their curation as original Atlas work.

---

## 31. Relationship to Arrowfield

Arrowfield should consume Atlas records such as:

```text
species
pheromone observations
compound structures
pathway hypotheses
candidate enzymes
evidence states
espmap records
structure models
```

The Atlas contains biological knowledge.

Arrowfield decides:

- what to show;
- what to hide;
- what question to ask;
- how uncertainty is visualized;
- how evidence is sequenced for learners.

```text
Sesiidae Pheromone Atlas
        │
        ├── observed chemistry
        ├── genomes
        ├── pathway hypotheses
        ├── enzyme candidates
        └── derived computation
                  │
                  ▼
              Arrowfield
                  │
                  ▼
                learner
```

---

## 32. Relationship to the educational Sesiidae homework

A flagship homework could use *S. tipuliformis*:

```text
observed pheromone chemistry
        ↓
possible biosynthetic reaction graph
        ↓
candidate enzyme families
        ↓
ranked genome candidates
        ↓
espmap analysis of substrate sites
        ↓
eventually enzyme structural geometry
        ↓
what evidence is still missing?
```

The exercise can succeed even if no enzyme is definitively identified.

Pedagogical lesson:

> **Computation narrows hypotheses; it does not manufacture experimental evidence.**

---

## 33. Release roadmap

### v0.1 — Identity spine

Scope:

```text
taxa
compounds
pheromone observations
references
genome assemblies
```

Initial taxa, from the matrix (§4.3):

```text
genome + pheromone   Synanthedon tipuliformis
                     Sesia apiformis
                     Synanthedon myopaeformis
                     + any "to check" species that qualifies

pheromone only       Synanthedon bicingulata
                     Synanthedon tenuis
                     Nokona pernix
                     Synanthedon scoliaeformis
```

Goals:

- schema stability;
- compound normalization;
- literature provenance;
- RDKit validation;
- genome accessions;
- machine-readable release.

### v0.2 — Biosynthetic chemistry

Add:

```text
reaction records
reaction vocabulary
competing pathway hypotheses
explicit evidence state
```

Classify steps as:

```text
established
analogical
hypothetical
```

### v0.3 — Chemogenomics

Add:

```text
proteomes
characterized reference enzymes
DIAMOND / BLAST
HMMER
InterPro
MAFFT / IQ-TREE
ranked Sesiidae candidates
```

### v0.4 — Molecular reasoning

Add:

```text
espmap records
protein structure models
substrate-site mappings
enzyme-pocket hypotheses
Arrowfield-compatible bundles
```

---

## 34. Longer-term possibilities

Possible later additions:

- searchable web interface;
- species × compound matrices;
- chemical similarity networks;
- pathway graph explorer;
- genome-browser links;
- protein-family dashboards;
- interactive phylogenies;
- public API;
- JSON-LD export;
- RO-Crate archival releases;
- DOI-backed dataset releases;
- comparative expansion to related moth families.

Do **not** begin with RDF/SPARQL unless a concrete interoperability need appears.

---

## 35. Suggested invariants

1. Every compound, precursors and computational models included, has an explicit stereochemical structure; no fragment is a compound.
2. Every heavy atom is mapped: chain carbons 1…n from C1, head-group atoms from 101 (§11). The numbering is machine-checked.
3. Shorthand and mapped SMILES are the only hand-entered structure fields and must agree; everything else is generated.
4. Every pheromone claim belongs to a typed observation record.
5. Every observation cites evidence, and every measurement names its method.
6. Genome identity uses stable assembly accession/version; protein identity adds annotation source, release and stable ID.
7. Characterized enzymes and genomic candidates are separate entity classes.
8. Candidate status never implies demonstrated function.
9. Every pathway step declares its evidence status and the experiment that would distinguish it.
10. Competing pathway hypotheses may coexist.
11. Derived analyses never overwrite curated observations.
12. Not tested is unknown. Tested and not detected is a negative, recorded with its method and detection limit. A missing gene model is neither.
13. Every release is reproducible from curated source files.
14. External identifiers are never guessed.
15. Arrowfield-specific presentation data stays outside biological source records.
16. espmap runs on the molecule the question is about: a substrate model for biosynthetic questions, never the pheromone as a proxy.
17. Synergist and antagonist are conclusions from behavioural records, per population, never properties of a compound.

---

## 36. Immediate first implementation

A practical first sprint:

```text
1. build the taxon × layer matrix from NCBI Datasets and the primary
   pheromone literature; commit it as releases/taxon_layers.tsv
2. create repository
3. define YAML conventions and data/headgroups.yaml (§11)
4. define JSON Schemas for:
   - taxon
   - compound (incl. precursor and computational_model classes)
   - typed observations (gland_composition, behavioural_response,
     electrophysiology)
   - genome + annotation
   - reference
5. write the RDKit validator (§12) and wire CI: schema validation,
   shorthand ↔ structure check, regeneration diff, espmap --check
6. prove the gate fails: synthetic fixtures with a flipped E/Z, a partial
   map and a wrong chain length must each fail CI
7. only now curate: S. tipuliformis, S. apiformis, S. myopaeformis
8. standardize their compounds, precursors included
9. encode the hard cases as observations: S. apiformis's two ratios,
   S. tipuliformis's population-dependent E3 effect, S. tenuis's
   undetected acetate
10. generate first JSON/TSV release
11. only then begin pathway reconstruction
```

The gate exists before the first record, so no record is grandfathered in
unvalidated: the same order espmap learned (parse → check → compute). This
deliberately postpones genome mining until the identity/provenance spine is
trustworthy.

---

## 37. First major scientific analysis

Once v0.1 exists, the first substantive analysis should probably be:

# *Synanthedon tipuliformis* pheromone biosynthetic pathway reconstruction

Questions:

1. What is the most plausible origin of the Z13-C18 backbone?
2. Direct Δ13 desaturation or Δ11-C16 + elongation?
3. How might the E2 and E3 double bonds arise: desaturation, an elongation
   or β-oxidation intermediate, or isomerisation (Route C, §18)?
4. Are observed alcohol/acetate gland compounds pathway intermediates?
5. What enzyme families are required under each pathway?
6. Which members of those families occur in the genome (annotation and
   genome-level search, §15a)?
7. Which candidates group with functionally characterized moth enzymes?
8. Which predictions are distinguishable by experiment?

Question 8 is a table, one row per competing step:

| step in question | competing routes | discriminating experiment |
|---|---|---|
| origin of Z13 | A (Δ13 on 18:0) vs B (Δ11 on 16:0, elongate) | topical deuterium-labelled 16:0 vs 18:0 and Z11-16 acid; which label reaches the pheromone |
| origin of E2 | desaturation vs C1 vs C2 | labelled Z13-18 vs Z11-16 precursor: under C1 the Z11-16 label reaches E2 and the Z13-18 label does not; under desaturation or C2 the Z13-18 label reaches E2 |
| E3 from E2 | C3 vs separate Δ3 enzyme | labelled E2 precursor appearing as E3; E2 : E3 ratio constant across individuals |
| terminal group | alcohol intermediate or not | label in E2,Z13-18:OH before E2,Z13-18:OAc |

`isotope_labelling` is an evidence type alongside sequence and phylogenetic
evidence. It is the standard way moth pheromone routes have been settled
(e.g. *Lobesia botrana*, where labelling established Δ11 desaturation and
chain shortening while the Δ7 desaturase stayed unidentified), and it can
answer questions 1–4 without any genome data.

This should yield the first:

```text
reaction graph
candidate enzyme-family set
homology search
phylogeny
ranked candidate list
```

---

## 38. Project identity

Recommended name:

# **Sesiidae Pheromone Atlas**

Repository:

```text
Azuromalachite/sesiidae-pheromone-atlas
```

Suggested one-line description:

> **A curated, machine-readable resource linking Sesiidae pheromone chemistry, genomes, biosynthetic hypotheses, and candidate enzyme families.**

A descriptive name is preferable to forcing an acronym before the project scope stabilizes.

---

## 39. Final conceptual model

```text
                         PRIMARY LITERATURE
                                │
                                ▼
                    ┌──────────────────────┐
                    │    OBSERVATIONS      │
                    │ pheromone chemistry  │
                    │ genomes / assemblies │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ NORMALIZED IDENTITIES│
                    │ taxa                 │
                    │ mapped compounds     │
                    │ proteins             │
                    │ reactions            │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │ PATHWAY         │        │ GENOME MINING   │
        │ HYPOTHESES      │        │ / PHYLOGENY     │
        └────────┬────────┘        └────────┬────────┘
                 │                          │
                 └────────────┬─────────────┘
                              ▼
                    ┌──────────────────────┐
                    │ ENZYME CANDIDATES    │
                    │ evidence-weighted    │
                    │ explicitly uncertain │
                    └──────────┬───────────┘
                               │
              ┌────────────────┴─────────────────┐
              ▼                                  ▼
      ┌───────────────────┐             ┌──────────────────┐
      │ espmap            │             │ protein models   │
      │ substrate         │             │ AF/AF3 / later   │
      │ electronics       │             │ geometry         │
      └─────────┬─────────┘             └────────┬─────────┘
                │                                │
                └──────────────┬─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │   ARROWFIELD         │
                    │ reasoning / teaching │
                    └──────────────────────┘
```

---

## 40. Guiding principle

The Sesiidae Pheromone Atlas should not try to make sparse evidence look complete.

Its value should come from making sparse evidence **structured, traceable, comparable, and computationally usable**.

The project succeeds if a researcher or learner can ask:

> What is actually known about this species' pheromone chemistry?  
> What genome is available?  
> What biosynthetic routes are plausible?  
> Which enzymes are candidates, and why?  
> Which claims are measured, inferred, or hypothetical?  
> What evidence would change the ranking?

That is the core scientific identity of the Atlas.

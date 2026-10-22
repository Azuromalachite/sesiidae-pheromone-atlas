# Sesiidae Pheromone Atlas

**Working repository:** `Azuromalachite/sesiidae-pheromone-atlas`  
**Working subtitle:** *A curated, machine-readable resource linking Sesiidae pheromone chemistry, genomes, biosynthetic hypotheses, and candidate enzyme families.*

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

### 4.1 *Synanthedon tipuliformis*

Strong first flagship because:

- a good nuclear genome is available;
- pheromone chemistry is well characterized;
- the blend includes closely related `E2,Z13-18:OAc` and `E3,Z13-18:OAc` components;
- the Δ2 versus Δ3 distinction creates a natural regioselectivity problem;
- minor gland compounds can provide possible pathway clues.

### 4.2 *Sesia apiformis*

Strong complementary case because:

- a good nuclear genome is available;
- its pheromone chemistry differs in both double-bond pattern and terminal functional group;
- useful for separating positional, stereochemical, and terminal-group effects.

### 4.3 Additional high-value taxa

Candidate expansion set:

- *Synanthedon bicingulata*
- *Synanthedon tenuis*
- *Nokona pernix*

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
│   └── references/
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

```yaml
compound_id: pheromone.e2_z13_18_oac

names:
  shorthand: E2,Z13-18:OAc
  systematic: null

structure:
  canonical_isomeric_smiles: "..."
  mapped_smiles: "..."
  inchi: "..."
  inchikey: "..."

lipid_annotation:
  chain_length: 18
  unsaturation_count: 2
  double_bonds:
    - position: 2
      geometry: E
    - position: 13
      geometry: Z
  terminal_group: acetate

external_ids:
  chebi: null
```

Why multiple identifiers:

- `compound_id`: stable Atlas-internal ID;
- canonical isomeric SMILES: structure/computation;
- mapped SMILES: persistent atom identity;
- InChI/InChIKey: external chemical identity;
- ChEBI: only when a correct entry exists.

Never force a misleading external identifier merely to fill a field.

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

Use RDKit to verify that annotation and structure agree.

Given:

```yaml
chain_length: 18

double_bonds:
  - position: 3
    geometry: Z
  - position: 13
    geometry: Z

terminal_group: alcohol
```

validate that the mapped structure actually contains:

```text
C1—C2—C3=C4 ... C13=C14 ... C18
```

with the stated stereochemistry and terminal functionality.

This should catch mistakes such as:

```text
display name: Z3,Z13-18:OH
structure:    E3,Z13-18:OH
```

before downstream computation.

---

## 13. Pheromone observations

Do **not** flatten evidence into `species → pheromone`.

The observation itself should be a first-class record:

```yaml
observation_id: obs.tipuliformis.paper_year.001

taxon: sesiidae.synanthedon_tipuliformis

context:
  sex: female
  tissue: pheromone_gland
  life_stage: adult
  population: null
  locality: null

components:
  - compound: pheromone.e2_z13_18_oac
    role: major
    abundance:
      value: 98
      unit: percent
      qualifier: approximate

  - compound: pheromone.e3_z13_18_oac
    role: minor
    abundance: null

evidence:
  reference: ref.paper_id
  methods:
    - gland_extract
    - gc_ms
```

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
genome_id: genome.synanthedon_tipuliformis.GCA_xxxxx

taxon: sesiidae.synanthedon_tipuliformis

assembly:
  accession: GCA_...
  version: 1
  level: chromosome
  source: NCBI

bioproject: PRJ...
biosample: SAM...

files:
  genome_fasta: null
  protein_fasta: null
  cds_fasta: null
  gff3: null

annotation:
  source: null
  version: null
```

Stable assembly accession/version should be the identity, not a filename.

Useful identifiers:

- GCA/GCF;
- BioProject;
- BioSample;
- protein accession;
- annotation release/version.

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

name: proposed E2 desaturation of Z13-C18 precursor

substrates:
  - compound: precursor.z13_18_acyl

products:
  - compound: precursor.e2_z13_18_acyl

enzyme_family:
  - membrane_fatty_acyl_desaturase

status: hypothetical

evidence:
  - type: analogy_to_characterized_lepidopteran_pathway
    reference: ref....
```

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

before assuming a direct Δ13 enzyme.

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

elongases
fatty-acyl reductases
acetyltransferase candidates
alcohol/aldehyde oxidoreductases
```

---

## 20. Candidate enzyme records

A genomic candidate should never receive a demonstrated function solely because it is the closest BLAST hit.

```yaml
candidate_id: candidate.tipuliformis.DES07.delta11

protein:
  accession: XP_...
  genome: genome.synanthedon_tipuliformis.GCA_xxxxx

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

The Atlas can store derived output as:

```text
derived/espmap/
└── e2_z13_18_oac/
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
  version: 0.2.0
  record: derived/espmap/...
```

This preserves the distinction between curated identity and replaceable computation.

---

## 26. Reaction-site integration

For a mapped C18 substrate:

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
| Protein | NCBI protein accession, UniProt |
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

Suggested initial taxa:

```text
Synanthedon tipuliformis
Sesia apiformis
Synanthedon bicingulata
Synanthedon tenuis
Nokona pernix
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

1. Every compound has explicit stereochemical structure.
2. Every C18 carbon-numbering convention is machine-checkable.
3. Mapped SMILES and lipid annotations must agree.
4. Every pheromone claim belongs to an observation record.
5. Every observation cites evidence.
6. Genome identity uses stable assembly accession/version.
7. Characterized enzymes and genomic candidates are separate entity classes.
8. Candidate status never implies demonstrated function.
9. Every pathway step declares its evidence status.
10. Competing pathway hypotheses may coexist.
11. Derived analyses never overwrite curated observations.
12. Missing evidence is unknown, not negative.
13. Every release is reproducible from curated source files.
14. External identifiers are never guessed.
15. Arrowfield-specific presentation data stays outside biological source records.

---

## 36. Immediate first implementation

A practical first sprint:

```text
1. create repository
2. define YAML conventions
3. define JSON Schemas for:
   - taxon
   - compound
   - pheromone observation
   - genome
   - reference
4. curate Synanthedon tipuliformis
5. curate Sesia apiformis
6. standardize the major/minor pheromone compounds
7. create RDKit compound validator
8. add CI schema + chemistry validation
9. generate first JSON/TSV release
10. only then begin pathway reconstruction
```

This deliberately postpones genome mining until the identity/provenance spine is trustworthy.

---

## 37. First major scientific analysis

Once v0.1 exists, the first substantive analysis should probably be:

# *Synanthedon tipuliformis* pheromone biosynthetic pathway reconstruction

Questions:

1. What is the most plausible origin of the Z13-C18 backbone?
2. Direct Δ13 desaturation or Δ11-C16 + elongation?
3. How might the E2 and E3 double bonds arise?
4. Are observed alcohol/acetate gland compounds pathway intermediates?
5. What enzyme families are required under each pathway?
6. Which members of those families occur in the genome?
7. Which candidates group with functionally characterized moth enzymes?
8. Which predictions are distinguishable by experiment?

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

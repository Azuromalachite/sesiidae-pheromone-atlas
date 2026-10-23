# Releases, citation and the occurrence layer

Design decisions of 2026-10-23. Nothing here is built yet except the
identifier scheme (`docs/identifiers.md`).

## Citable releases

- **The repository is the living project; a release is an immutable snapshot.**
  A release is a tagged version whose files are archived with a DOI (planned:
  GitHub–Zenodo integration, which needs the maintainer's Zenodo account).
- **Cite the release, not the repository.** For example: "analyses used Sesiidae
  Pheromone Atlas v0.1.0 (DOI …), observations `spa.obs.…`".
- **Three citation levels:**
  - the whole Atlas release;
  - the original paper behind any inherited claim — the Atlas never replaces it;
  - derived computational products, each with its own generator, version,
    commit and input release.
- **A DOI makes the dataset citable; it does not make every claim
  authoritative.** Every observation keeps its own reference, source location,
  author statement and unresolved items.

### What the release builder must produce (not built yet)

```text
sesiidae-atlas-vX.Y.Z/
├── taxa/ compounds/ references/ observations/ genomes/   records, deterministically serialised
├── schemas/
├── derived/                  each product with generated_by + input_release
├── CITATION.cff
├── CHANGELOG.md
├── datapackage.json
└── MANIFEST.sha256           SHA-256 of every file, plus the exact git commit
```

Deterministic means: the same commit always produces byte-identical files, so
the manifest can be re-checked by anyone without GitHub.

Derived products record their provenance:

```yaml
generated_by: {software: <name>, version: <x.y.z>, git_commit: <sha>}
input_dataset: {atlas_version: <x.y.z>}
```

### Timing

The first DOI should accompany a result, not a handful of records: a
dataset paper on observation-resolved records, with the *S. tenuis*, *S.
apiformis* and *S. tipuliformis* cases as the demonstration.

## The occurrence layer (v0.3 or later)

Occurrences from GBIF and iNaturalist are a separate namespace (`occurrences/`,
`spa.occ.…`). They never become `observations`, which keep their meaning:
experimental and chemical records.

### Licensing: a recipe, not a copy

The Atlas is CC BY 4.0. GBIF occurrence data may be CC0, CC BY or CC BY-NC,
and CC BY-NC cannot be relicensed. So **an Atlas release never redistributes
an occurrence table.** It stores the recipe and the identifiers:

```yaml
occurrence_analysis:
  source: GBIF
  download_doi: 10.15468/dl.<…>      # the authoritative snapshot
  retrieved: <date>
  filters: {taxon_keys: [...], basis_of_record: [...]}
  code_version: <commit>
```

It commits only derived outputs — monthly phenology summaries, range-overlap
matrices, sampling-density summaries, knowledge-gap metrics — plus GBIF
occurrence keys where a result must be traceable. Photo and sound licences are
separate from occurrence licences. Media are referenced, never redistributed.

### Sources

- **GBIF** is the analytical backbone, through DOI-bearing downloads.
- **iNaturalist** is enrichment only: identification history, annotations,
  media links. Research-grade iNaturalist records with open licences already
  reach GBIF, so a record seen in both is one occurrence, cross-referenced
  (`gbif_occurrence_key` + `inaturalist_observation_id`), never two.
- **Taxon mapping** goes to Atlas concepts by full name and authority
  (`docs/identifiers.md`, rule 4). The source's verbatim name is kept.

### Quality: profiles in code, not grades on records

No occurrence carries a stored quality grade. Analyses select through named
profiles, computed from fields the records keep:

| profile | includes |
|---|---|
| strict | preserved specimens or institutionally determined records, with acceptable coordinate and date quality |
| moderate | strict, plus verifiable photographic records with supported identification |
| exploratory | the broader accepted set |

A result is reported with the profile it used, and checked under the others.

### What occurrences are for, and not for

- **For:** ranges, phenology, sympatry and phenological overlap, sampling gaps,
  and the knowledge-gap matrix.
- **Not for:** absence, absolute abundance or direct population comparison
  without explicit bias correction. Presence-only records follow observers.
- **Phenology does not explain a zero that had a concurrent positive control.**
  The *S. tenuis* acetate caught nothing in the same replicated trial in which
  the alcohol caught males (`spa.obs.tenuis.2012.yang.trap_acetate_alone`).
  Phenology matters for comparisons between studies and for uncontrolled
  failures.

### First occurrence analysis: the knowledge-gap matrix

```text
taxon × occurrence evidence × natural chemistry × behavioural evidence
      × genome × transcriptome × receptor evidence
```

It asks which Sesiidae are observable enough to study but chemically or
molecularly under-characterised enough for new work to matter. It turns
`docs/knowledge-gaps.md` into numbers.

## Roadmap order

```text
v0.1    observation spine: taxa, compounds, references, observations,
        stable IDs, provenance
v0.2    biosynthetic chemistry: reaction grammar, pathway compiler,
        reference enzyme systems
v0.3+   ecological context: GBIF recipes, phenology, sympatry,
        knowledge-gap matrix
later   perception: odorant receptors, receptor assays, sensory graph,
        semiochemical design
```

Not yet placed in this order: genome mining and orthology (concept §21–23), and
espmap records (concept §25–26). They supersede nothing in the concept until
a decision is made.

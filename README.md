# Sesiidae Pheromone Atlas

*A curated, machine-readable resource linking Sesiidae pheromone chemistry,
genomes, biosynthetic hypotheses, and candidate enzyme families.*

**Status: building v0.1.** This repository holds the design documents, the
record schemas and the validator with its failing fixtures, and 624 curated
records:
- 28 taxa, 31 references, 24 compounds, 11 genomes and 524 observations,
  the observations all from full texts
  ([`docs/curation-log.md`](docs/curation-log.md));
- 6 dated searches, the only basis for "not found".

**No record has yet been checked by a person against its paper.** Every
record was extracted by Claude and re-read against the PDFs by other Claude
reviewers. A human spot-check, 24 random records and 14 hard cases, is
drawn and waiting in [`review/`](review/README.md).

The taxon × layer matrix is generated from these records. There are no reaction or
pathway records yet: this corpus records what was observed, not how it is made.

```bash
pip install -r requirements.lock.txt   # exact versions; constraints are in requirements.in
pytest -q                              # the validator accepts good fixtures and refuses every bad one
python atlas_validate.py data          # validate curated records
python scripts/build_release.py        # regenerate derived/ (CI runs it with --check)
```

`derived/` holds machine-readable exports: tidy relational tables in
`derived/tables/` (the analytical form), one JSONL file per record kind,
the taxon × layer matrix, one teaching bundle per `teaching/cases/` file,
and checksums. They are generated from the records,
never edited by hand. No release has been tagged and no DOI minted yet; to
cite the Atlas meanwhile, see [`CITATION.cff`](CITATION.cff) and
[`CHANGELOG.md`](CHANGELOG.md).

See [`docs/validation.md`](docs/validation.md) for what is checked.

The Atlas records what is known, what is inferred, and what is hypothesised
about clearwing-moth (Sesiidae) pheromones, and keeps those three apart. It
is planned as human-curated YAML, validated by JSON Schema and RDKit, with
generated machine-readable releases.

## Documents

| file | what it is |
|---|---|
| [`docs/concept.md`](docs/concept.md) | design history and direction (revision 3), **non-normative**: the schemas, `docs/validation.md` and `docs/identifiers.md` are the specification |
| [`docs/context.md`](docs/context.md) | the natural-history and scientific motivation, from *Amegilla* to Sesiidae to lipid-derived signalling |
| [`docs/literature-narrative.md`](docs/literature-narrative.md) | the literature as a story, from synthetic lures to blend, context and evidence layers, each claim tied to its record |
| [`docs/identifiers.md`](docs/identifiers.md) | the permanent `spa.` ID scheme and its rules |
| [`docs/releases-and-occurrences.md`](docs/releases-and-occurrences.md) | decisions on citable releases, the GBIF occurrence layer and roadmap order |
| [`docs/scope-v0.1.md`](docs/scope-v0.1.md) | what v0.1 is complete for: the scope statement, curated and target species, and how the list was built |
| [`docs/evidence-classes.md`](docs/evidence-classes.md) | the evidence-class vocabulary (gland constituent, emitted, antennally active, attractant, addition effects, female pheromone component) and the rules that derive it from records into `derived/tables/evidence_classes.tsv` |
| [`docs/computed-and-teaching.md`](docs/computed-and-teaching.md) | the contract for espmap results (`computed/espmap/`) and teaching bundles (`teaching/cases/` → `derived/teaching/`): layout, checks, what a bundle may assert |
| [`docs/direction-type1-grammar.md`](docs/direction-type1-grammar.md) | v0.2 direction: a Type-I moth reaction grammar from primary experiments, applied to Sesiidae (not built) |
| [`docs/reviews/`](docs/reviews/) | the two adversarial reviews the concept was revised against |
| [`docs/knowledge-gaps.md`](docs/knowledge-gaps.md) | gaps that set direction: the tropical and Southeast Asian frontier, *Melittia*, the trapping blind spot |
| [`derived/taxon_layers.tsv`](derived/taxon_layers.tsv) | the taxon × layer matrix, generated from the records by `scripts/build_taxon_layers.py`: genomes, gene sets, curated chemistry and dated searches ([column guide](derived/README.md)) |

## Related projects

- [espmap](https://github.com/Azuromalachite/espmap) — electrostatic potential on molecular surfaces, with per-site statistics. espmap computes; the Atlas keeps the checked index of results for its compounds in `computed/espmap/` (none yet).
- [Arrowfield](https://github.com/Azuromalachite/arrowfield) — an educational environment for mechanistic reasoning. It reads the teaching bundles in `derived/teaching/` and adds only teaching metadata.

## Licence

Code: MIT ([`LICENSE`](LICENSE)). Data, schemas and documentation: CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)).

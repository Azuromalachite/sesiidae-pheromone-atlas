# Sesiidae Pheromone Atlas

*A curated, machine-readable resource linking Sesiidae pheromone chemistry,
genomes, biosynthetic hypotheses, and candidate enzyme families.*

**Status: building v0.1.** This repository holds the design documents, the
first discovery table (the taxon × layer matrix), the record schemas and the
validator with its failing fixtures, and the first 73 curated records
(9 taxa, 10 references, 10 compounds, 4 genomes, 40 observations), all from full texts
([`docs/curation-log.md`](docs/curation-log.md)). There are no reaction or
pathway records yet: this corpus records what was observed, not how it is made.

```bash
pip install -r requirements.txt
pytest -q                          # the validator accepts good fixtures and refuses every bad one
python atlas_validate.py data      # validate curated records
```

See [`docs/validation.md`](docs/validation.md) for what is checked.

The Atlas records what is known, what is inferred, and what is hypothesised
about clearwing-moth (Sesiidae) pheromones, and keeps those three apart. It
is planned as human-curated YAML, validated by JSON Schema and RDKit, with
generated machine-readable releases.

## Documents

| file | what it is |
|---|---|
| [`docs/concept.md`](docs/concept.md) | the technical concept: data model, curation rules, invariants, roadmap. Revision 3; earlier revisions are in this file's git history |
| [`docs/context.md`](docs/context.md) | the natural-history and scientific motivation, from *Amegilla* to Sesiidae to lipid-derived signalling |
| [`docs/literature-narrative.md`](docs/literature-narrative.md) | the literature as a story, from synthetic lures to blend, context and evidence layers, each claim tied to its record |
| [`docs/identifiers.md`](docs/identifiers.md) | the permanent `spa.` ID scheme and its rules |
| [`docs/releases-and-occurrences.md`](docs/releases-and-occurrences.md) | decisions on citable releases, the GBIF occurrence layer and roadmap order |
| [`docs/reviews/`](docs/reviews/) | the two adversarial reviews the concept was revised against |
| [`docs/knowledge-gaps.md`](docs/knowledge-gaps.md) | gaps that set direction: the tropical and Southeast Asian frontier, *Melittia*, the trapping blind spot |
| [`releases/taxon_layers.tsv`](releases/taxon_layers.tsv) | the taxon × layer matrix: which species have genomes, gene sets and identified pheromones ([column guide](releases/README.md)) |

## Related projects

- [espmap](https://github.com/Azuromalachite/espmap) — electrostatic potential on molecular surfaces, with per-site statistics. The Atlas will store espmap records as derived, replaceable computation.
- Arrowfield (planned) — an educational environment for mechanistic reasoning, which will consume Atlas records.

## Licence

Code: MIT ([`LICENSE`](LICENSE)). Data, schemas and documentation: CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)).

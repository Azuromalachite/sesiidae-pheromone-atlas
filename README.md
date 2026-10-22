# Sesiidae Pheromone Atlas

*A curated, machine-readable resource linking Sesiidae pheromone chemistry,
genomes, biosynthetic hypotheses, and candidate enzyme families.*

**Status: concept stage.** This repository holds the design documents and
the first discovery table (the taxon × layer matrix). There are no schemas,
curated records or code yet.

The Atlas records what is known, what is inferred, and what is hypothesised
about clearwing-moth (Sesiidae) pheromones, and keeps those three apart. It
is planned as human-curated YAML, validated by JSON Schema and RDKit, with
generated machine-readable releases.

## Documents

| file | what it is |
|---|---|
| [`docs/concept.md`](docs/concept.md) | the technical concept: data model, curation rules, invariants, roadmap. Revision 3; earlier revisions are in this file's git history |
| [`docs/context.md`](docs/context.md) | the natural-history and scientific motivation, from *Amegilla* to Sesiidae to lipid-derived signalling |
| [`docs/reviews/`](docs/reviews/) | the two adversarial reviews the concept was revised against |
| [`docs/knowledge-gaps.md`](docs/knowledge-gaps.md) | gaps that set direction: the tropical and Southeast Asian frontier, *Melittia*, the trapping blind spot |
| [`releases/taxon_layers.tsv`](releases/taxon_layers.tsv) | the taxon × layer matrix: which species have genomes, gene sets and identified pheromones ([column guide](releases/README.md)) |

## Related projects

- [espmap](https://github.com/Azuromalachite/espmap) — electrostatic potential on molecular surfaces, with per-site statistics. The Atlas will store espmap records as derived, replaceable computation.
- Arrowfield (planned) — an educational environment for mechanistic reasoning, which will consume Atlas records.

## Licence

Code: MIT ([`LICENSE`](LICENSE)). Data, schemas and documentation: CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)).

# Sesiidae Pheromone Atlas

*A curated, machine-readable resource linking Sesiidae pheromone chemistry,
genomes, biosynthetic hypotheses, and candidate enzyme families.*

**Status: concept stage.** This repository currently holds the design
documents only. There are no schemas, records or code yet.

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

## Related projects

- [espmap](https://github.com/Azuromalachite/espmap) — electrostatic potential on molecular surfaces, with per-site statistics. The Atlas will store espmap records as derived, replaceable computation.
- Arrowfield (planned) — an educational environment for mechanistic reasoning, which will consume Atlas records.

## Licence

Code: MIT ([`LICENSE`](LICENSE)). Data, schemas and documentation: CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)).

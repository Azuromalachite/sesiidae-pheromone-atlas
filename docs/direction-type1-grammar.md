# Direction: a Type-I moth reaction grammar, applied to Sesiidae

Decided 2026-10-23, from the maintainer's notes. This is direction for v0.2
and later. **Nothing here is built.** Where a number or paper below comes from
those notes and has not been checked against its source, it is marked
*(unverified)*. It enters the Atlas only as a curated record from the primary
paper.

## The split

| layer | holds | scope |
|---|---|---|
| **Sesiidae Atlas** (today) | focal biological observations: species × compounds × populations × assays × genomes | Sesiidae |
| **Type-I reference corpus** (v0.2) | experimentally established transformations: reaction observations, enzymes, substrates, isotope evidence | any moth whose experiment establishes a Type-I step |
| **Pathway compiler** (later) | the grammar, applied to explain Sesiidae chemistry | Sesiidae as the hard test case |

The Atlas stays focal on Sesiidae. It does not become a general moth pheromone
database, and a field-lure paper from another family is out of scope. A paper
enters the reference corpus because of **what transformation it establishes**,
not because its species has a pheromone.

## The claim, phrased to be falsifiable

Sesiidae appear to occupy one region of the broadly conserved **Type-I** moth
pheromone biosynthetic grammar. That grammar runs:
- fatty-acid synthesis to C16/C18 acyl-CoA;
- desaturation, and chain editing by +2 elongation or −2 β-oxidative
  shortening, in either order and repeated;
- fatty-acyl reduction to the alcohol;
- oxidation to the aldehyde, or acetylation.

This is not a claim that all moths share one pathway. Type II
(polyunsaturated hydrocarbons and epoxides), Type III (methyl-branched) and
Type 0 (short secondary alcohols and ketones) are outgroups and boundary
cases, not part of the same grammar.

Chain editing acts as a coordinate transformation. For example:
- DES(Δ11, C16) then +2 gives Δ13-C18;
- DES(Δ10, C16) then −2, −2 gives Δ6-C12.

A small operator set can therefore produce a larger visible vocabulary. For
Sesiidae the leading Z13 hypothesis (Δ11 desaturation + elongation) is
exactly such a rule.

## Evidence ladder (already the Atlas's epistemology)

```text
experiment ──> reaction observation ──> generalised rule ──> Sesiidae pathway hypothesis
```

- A rule is derived from one or more species-specific reaction observations,
  never hand-written from a review when primary experiments exist.
- **A demonstrated reaction is not an identified enzyme.** A record says
  which it has.
- Admissible evidence for a conversion: isotope-labelled precursors,
  heterologous expression, enzyme assays, knockdown or knockout, and
  substrate-selectivity experiments. Co-occurrence in a gland is not
  admissible (`docs/validation.md`).
- External reaction databases (Rhea, EnzymeMap, RetroRules) become
  normalisation infrastructure, not the biological authority.

## Candidate reference systems (to be read from primary papers)

- *Cnaphalocrocis medinalis*: a Z11-C16 → Z13-C18 elongation route with isotope
  labelling and functional DES, ELO and FAR *(unverified; a 2026 paper per the
  notes)*. It is the closest model of the Sesiidae Z13 question.
- *Lobesia botrana*: Δ11 desaturation, β-oxidative shortening, a second
  desaturation, reduction and acetylation, resolved by isotope labelling with
  one desaturase still unidentified *(unverified)*.
- *Helicoverpa* / *Chloridea*: Δ11-C16 to alcohol to aldehyde, and storage of
  intermediates.
- *Spodoptera*: dienes by desaturation, shortening and desaturation;
  multifunctional desaturases.
- *Ostrinia*: desaturase and reductase evolution linked to receptor
  evolution.
- *Bombyx mori*: regulation and terminal steps.

The paper list goes to the maintainer as a table with verified DOIs when this
stage starts.

## The question this opens

Three spaces of very different size:
1. **Syntactic space:** every straight-chain C10–C18 OH/Ald/OAc with 0–4 C=C.
   The notes estimate about 10⁵ structures *(the maintainer's own
   calculation; to be enumerated, not quoted)*.
2. **Grammar-reachable space:** what experimentally demonstrated moth
   reactions can reach from fatty-acyl precursors. **Size unknown, to be
   enumerated.**
3. **Observed vocabulary:** structures reported from females or as
   attractants. Hundreds, per the notes *(unverified: about 700 components
   across more than 1,600 species via Pherobase; Ando & Yamamoto report
   16 new Type-I structures among 119 species studied after 2003)*.

The scientific question is **why evolution occupies so little of the
reachable space**. Candidate filters:
- enzyme specificity;
- metabolic cost;
- volatility and stability;
- receptor evolvability;
- interference with sympatric species;
- historical contingency.

Signal space (blends × ratios × release × perception) is much larger again,
and the Sesiidae records already show the pattern: few molecules, many
messages.

## What the compiler would be tested on

1. known rules on known species;
2. a held-out rule;
3. a held-out species;
4. a held-out family;
5. Sesiidae, where the route is genuinely unknown.

## Consequences for the Atlas now

- **Reaction records** (`spa.rxnobs.<taxon>.<reference>.<what>`) and a rule layer
  derived from them are the v0.2 data model. The v0.2 chemistry gate in
  `docs/validation.md` (head-group table, charge convention, CoA
  stereochemistry) must land first.
- **Reference taxa outside Sesiidae** will need taxon records. They do not
  enter the Sesiidae matrix (`derived/taxon_layers.tsv` will filter by
  family).
- Nothing in v0.1 changes.

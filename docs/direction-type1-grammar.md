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

---

# Amendment, 2026-10-26: the record model for the reference corpus

Decided in conversation with the maintainer, and written down here as design
before any implementation. **Nothing here is built.** No schema, no record and
no `derived/` output changes with this amendment, and nothing in v0.1 changes.
The *(unverified)* convention of the sections above holds for everything
below: a paper, a number or a claim marked that way has not been checked
against its source in the conversation that produced this text, and enters
the Atlas only as a curated record read from the primary paper.

## The primary object is a reaction observation, not an enzyme

`spa.rxnobs.*` records **one experiment that establishes a transformation**.
It is not an enzyme record with reactions attached. The corpus is a corpus of
experiments; enzymes are one of the things an experiment may have identified.

A reaction observation may reference:

| it may reference | may it be absent |
|---|---|
| an identified enzyme or protein | yes — a demonstrated reaction with no enzyme is still a reaction observation |
| substrate(s) | no |
| product(s) | no, except in a scoped negative (below), where there is none |
| isotope evidence | yes |
| the assay system (yeast, Sf9, insect gland, *in vitro*) | no |
| method, sample and population, as every Atlas observation already carries | no |
| `source_location` in the paper, as every Atlas observation already carries | no |

### Enzyme identity and reaction evidence stay separable

This is the v0.2 form of the rule the evidence ladder above already states.

- A **demonstrated reaction with no identified enzyme** is a valid reaction
  observation. Isotope labelling that shows Z11-16 acid becoming Z13-18 acid
  in a gland establishes the transformation whether or not the elongase was
  ever cloned.
- An **enzyme or transcript candidate with no demonstrated reaction** — a
  gland-biased desaturase-family transcript, a genome annotation, a
  phylogenetic placement — is valid molecular or context evidence. It is
  **not reaction proof**, and no derivation may promote it to one.

The two never merge into a single "characterised" flag. A record says which
it has, and a record may have both.

## One experiment, one observation

A paper that expresses a candidate in yeast, repeats it in Sf9, knocks it
down by RNAi and mutates the active site has run **four experiments**. That
is four reaction observations, not one record carrying a curator-written
evidence score of 4/4 or "strong". There is no such score anywhere in the
Atlas, and v0.2 does not introduce one.

This is the existing rule of `docs/evidence-classes.md`, applied to a new
record kind: evidence classes and coverage are **derived from record fields
by a script**, never entered by hand. No class is an author's claim or the
curator's opinion, and none is netted out. Four experiments on one
transformation produce four rows and a count, and a reader who wants a
verdict reads the rows.

## Negative results are scoped negatives

The Atlas already refuses to read "not detected" as "not made"
(`female_not_detected`). Reaction records inherit the same discipline, with
one extra distinction that matters more here than in the chemistry layer:

| the experiment did | the record says |
|---|---|
| offered the substrate, detected no product | a **negative for that assay, that method and that detection limit** |
| never offered the substrate | **absent / not tested** — no negative at all |

These are different facts and must not share a field. **Do not infer zero.**
A substrate that was never put in front of the enzyme says nothing about the
enzyme; a substrate that was offered in yeast and gave no product says
something about yeast, that construct and that detection limit, and may be
contradicted by Sf9.

## Contradictory experiments coexist

Two experiments that disagree are two records. Neither is deleted, demoted or
averaged against the other. **No netting.** This is already how a compound
that raised catches in one study and lowered them in another is held; a
desaturase active in one heterologous system and inactive in another is held
the same way.

## What stays outside the record layer

- **Non-Sesiidae reference taxa are allowed** in the corpus — that is the
  point of it — and they need taxon records. They stay out of the
  Sesiidae-derived layers through the existing family filter on
  `derived/taxon_layers.tsv`. The Sesiidae matrix does not grow a *Bombyx*
  row.
- **FASTA, MSA, trees and SSNs are regenerable `analyses/` products.** They
  are computed from accessions, never record-layer truth, and never the thing
  a reaction observation points at in place of an experiment.
- **Structure and tunnel modelling stays outside Atlas records entirely.**
  Not a field, not a record kind, not a derived column.
- **Arrowfield consumes the corpus only through the teaching bundle.** It does
  not get a second protein database to keep in step with this one.

## The minimum v0.2 record boundary

The smallest thing worth building, and the boundary of what v0.2 attempts:

**In.** Reaction observations; the taxa, references and compounds they need;
the acyl-CoA and related head groups the chemistry gate admits; derived
evidence classes and transformation coverage computed from those records;
search records saying where a transformation was looked for and not found.

**Out, explicitly deferred:**

| deferred | why it is not a v0.2 record |
|---|---|
| reaction graph | a derivation over records, and only once there are records |
| pathway inference | the compiler; a conclusion, never a stored edge |
| candidate-gene ranking | an analysis, and one that would quietly become an opinion field |
| phylogenetic function prediction | a prediction, not an experiment; the corpus holds experiments |
| structural mechanism | outside the record layer, as above |
| any "activity cliff" notion | see below |

**On activity cliffs.** A cliff needs a defined sequence distance *and* a
defined function distance. Function here is a multivariate product spectrum,
and the distance over such spectra is not obvious — it is a modelling choice,
and a contestable one. So a cliff is a **later analysis over immutable assay
records**, never a stored property of a record or a column of a derived
table. If such a distance is ever defined, it is defined in `analyses/`,
where it can be argued with and recomputed.

## Ordering

1. **Finish the Atlas v0.1.0 gate**, in the four parts `docs/scope-v0.1.md`
   states. `computed/` and the census are done — the census is generated from
   the records, with no curated status field. What is outstanding is **human
   primary-source verification**: `review/spot-check-001` and
   `review/case-check-sesiidae-homework-1`, neither of which has a verdict
   filled in yet, and then the corrections they turn up, each in its own
   traceable commit. The tag is not cut.
2. **Land the v0.2 chemistry validation and schema gate** in
   `docs/validation.md` — head-group table validation, charge and protonation
   convention, CoA stereochemistry. The first acyl-CoA must not discover it.
3. **Only then curate the corpus.**
4. **Later** compile pathways, and expose them through Arrowfield's teaching
   bundle.

No step starts before the one above it is done. In particular, no reaction
record is written against a schema that cannot yet represent acyl-CoA.

### A prerequisite of stage (3): "no route found" must be sayable

`schemas/search.schema.json` is already the mechanism that makes absence
assertable. It is **the only admissible basis for "not found"; the absence of
records never is.** A corpus whose stop condition is coverage (below) depends
on it entirely.

The obvious gap is the vocabulary: its `layer` enum and its `search_id`
pattern both admit only `pheromone` and `genome`, and a biosynthesis or
reaction layer needs **both** widened — the enum, and the pattern, which
repeats the same two values. That much is backward-compatible: the
schema-freeze mechanism permits widening of this kind (`docs/validation.md`
counts new enumeration values as additive, and `scripts/schema_shape.py`
records enum values and property names, not patterns), so it needs no
breaking change and no v0.1 migration. This is not blanket permission for
anything else the corpus might want.

**Widening the vocabulary alone is insufficient.** The stop condition below
promises something stronger than a human reading search notes: that every
required transformation has either a reaction observation or a dated
`not_found` search, **derived by a script**. Two gaps block that, and both
are stage-3 prerequisites:

- **A search record has no structured field naming what was searched for.**
  There is `scope`, there is `sources`, and there is free text in `found` and
  `notes` — nothing a script can join to a transformation. Coverage cannot be
  derived from free text.
- **Scope has no corpus-wide shape.** For every non-`census` outcome the
  `allOf` block forces `scope` to a single taxon; `census` requires a
  `family` and means "every item found in scope has an Atlas record". A
  Type-I search ranges *across* moths for evidence of one transformation,
  which fits neither, and reusing `census` for it would abuse the one word in
  this schema that currently has a precise meaning.

So the prerequisite is **structured biosynthesis-search targeting**: a way to
say which transformation or reaction query a search was for, and a way to
express a corpus-wide scope without overloading `census`. **Do not design
those fields now, and do not change the schema now.** The requirement is
named here and stops here; it is work for stage (3), not for stage (1) or
(2).

## The route, route-first

The corpus is organised around **the transformations the Sesiidae chemistry
requires**, not around whichever enzyme families are best studied. A paper on
a well-sampled desaturase clade that bears on none of these steps is not more
useful here for being well sampled.

Sesiidae pheromones are largely C18 3,13- and 2,13-dienyl acetates, alcohols
and aldehydes. Of the bonds that implies:

- **Δ13 has a plausible analogue elsewhere**: Δ11 desaturation on C16, then
  +2 elongation. This is the leading hypothesis above, and the one with a
  candidate model system.
- **Δ3 appears unresolved.**
- **Δ2 appears unresolved**, and is recorded here beside Δ3 as a second
  Sesiidae-specific problem rather than a detail of the first. Some
  clearwings carry **both** the 2,13- and the 3,13-dienes. *Synanthedon
  haitangvora* females carry Z3,Z13-18:OAc and E2,Z13-18:OAc as the two major
  components, with E3,Z13-18:OAc and both the 2,13- and 3,13-alcohols minor
  (`spa.obs.synanthedon_haitangvora.yang_2009.gland`). That record is curated
  from the primary paper, so it is not marked *(unverified)*; what is
  *(unverified)* is any inference that the co-occurrence implies a shared
  route.

### Candidate evidence, to be read from primary papers

Every item here is *(unverified)*: none has been checked against a primary
paper. Each enters the corpus as a reaction observation curated from the
paper itself, or not at all.

- ***Cnaphalocrocis medinalis* elongases** converting Z11-16 to Z13-18, said
  to be the first molecularly characterised Lepidopteran pheromone elongases
  *(unverified; 2026, per the maintainer's notes)*.
- **An independent isotope-labelling plus heterologous reconstruction** of the
  same DES → ELO → FAR route *(unverified; 2026)*. If both hold they are two
  reaction observations of one transformation, not one stronger record.
- ***Lobesia botrana* acyl-CoA oxidases** (Lbo_31670, Lbo_49602) converting
  Z11-14 acid to Z9-12 acid, said to be the first functionally identified moth
  pheromone ACO genes *(unverified)*. This is the chain-shortening step, and
  the only named candidate for it.
- **Acetyltransferase: no gene characterised.** The claim is that no
  acetyltransferase gene has been characterised in moth sex-pheromone
  biosynthesis, and that 2026 work shows **esterases modulate acetate levels
  by hydrolysis** *(both unverified)*. The consequence, if it holds, is sharp:
  **acetate abundance is not a readout of acetyltransferase activity**, and no
  derivation may treat an acetate-rich gland as evidence of one.

## Two open questions, stored as questions

Both are **unverified reasoning from the maintainer's conversation**, and may
already exist in the literature under other names. They are written down as
open questions so that they can be tested, and so that nobody later mistakes
them for curated route knowledge. **Neither is a pathway fact. Neither becomes
a record, an edge, or a derived row.**

**Q1. Does one β-oxidation cycle reach Δ3,Δ13-C18 from Δ5,Δ15-C20?**
β-oxidation removes two carbons from the carboxyl end, so it lowers every
double-bond position by two. One cycle therefore maps Δ5,Δ15-C20 onto
Δ3,Δ13-C18. What the arithmetic strictly predicts is **a Δ5,Δ15-C20
precursor**. **A Δ5 desaturase acting on a C20 substrate** is one mechanism
that would produce it, and the discriminating sub-hypothesis to look for in
assays and in gland transcriptomes — but the precursor could be reached
another way, and finding it would not by itself establish the desaturase.

**Q2. Do Δ2 and Δ3 sit across one enzyme's equilibrium rather than across two
desaturations?** trans-2-enoyl-CoA is the first intermediate of every
β-oxidation cycle, and enoyl-CoA isomerase interconverts cis-3-enoyl-CoA and
trans-2-enoyl-CoA. The Sesiidae Δ2 and Δ3 bonds may therefore sit on either
side of one standard enzyme's equilibrium. If so, the Δ2/Δ3 question is a
**chain-shortening** question rather than a desaturation question, and it
could provide a common biochemical route consistent with the co-occurrence of
2,13- and 3,13-dienes in one gland. Co-occurrence does not discriminate it:
two independent routes would produce the same observation.

*(Unverified, from the maintainer's search and not checked against a primary
paper.)* Candidate Δ3,Δ2-*trans*-enoyl-CoA isomerases have reportedly been
found among β-oxidation genes in moth pheromone-gland transcriptome work, but
no functional evidence was found that Sesiidae divert those intermediates into
their 2,13- and 3,13-dienes; the Sesiidae literature remains chemistry and
identification evidence. That is the gap Q2 exists to make the corpus
adjudicate, and it is exactly the case-3 situation of the hostile table below:
a transcript present, a reaction not demonstrated.

Q1 and Q2 are not alternatives; both could hold, or neither. What each buys is
a testable prediction, which is what an open question in this repository is
for.

## Stop condition: transformation coverage, not a paper count

The corpus is **done for v0.2** when every transformation the Sesiidae
homework chemistry requires has either its strongest primary experiment
curated as a reaction observation, or a recorded search (`spa.search.*`, once
the layer and its structured targeting exist) saying none was found:

| transformation | required by |
|---|---|
| desaturation | every Sesiidae diene |
| elongation | the Δ13 route from C16 |
| β-oxidative shortening, limited | the Δ3 and Δ2 questions above |
| fatty-acyl reduction | every Sesiidae alcohol, and every acetate through it |
| alcohol ↔ acetate | the acetate majority |
| alcohol → aldehyde | only where a curated Sesiidae observation requires it |

A count of papers is not a stop condition: a hundred desaturase papers and no
chain-shortening experiment is not coverage. A row with a dated `not_found`
search is as complete as a row with a curated experiment, and far better than
an empty one.

## Four hostile cases the schema must represent without ambiguity

For whenever implementation starts. Each must be unmistakable from the
record, and no two may collapse into each other:

| # | case | must stay distinct from |
|---|---|---|
| 1 | **reaction demonstrated, enzyme unknown** — isotope labelling shows the conversion; no protein identified | 3: this *is* reaction evidence |
| 2 | **enzyme identified and reaction demonstrated** — the protein was expressed and made the product | 1 and 3: it has both, and says so |
| 3 | **enzyme or transcript present, reaction not demonstrated** — a gland-biased candidate, a genome annotation, a clade placement | 1 and 2: this is **not** reaction proof |
| 4a | **substrate tested, result negative** — offered, no product, at a stated method and detection limit | 4b: this is a scoped negative |
| 4b | **substrate never tested** — not offered | 4a: this asserts nothing |

A schema that cannot tell 1 from 3, or 4a from 4b, is not ready to hold a
reaction record. These are the cases to write bad fixtures for first, in the
style `tests/fixtures/bad/` already uses: the gate must be **seen to refuse**
the confusion, not merely to permit the correct form.

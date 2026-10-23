# Identifiers

Decided 2026-10-23, before any citable release, so that no released ID ever
has to change.

## Form

Every primary record has a permanent ID in the `spa.` namespace:

| record | form | example |
|---|---|---|
| taxon | `spa.tax.<genus>_<species>` | `spa.tax.synanthedon_tipuliformis` |
| compound | `spa.cmpd.<name>` | `spa.cmpd.e2_z13_18_oac` |
| computational model | `spa.model.<name>` | `spa.model.z13_18_sme` |
| reference | `spa.ref.<first author>_<year>` | `spa.ref.mozuraitis_2006` |
| observation | `spa.obs.<taxon slug>.<reference slug>.<what was measured>` | `spa.obs.synanthedon_tipuliformis.mozuraitis_2006.gland` |
| genome | `spa.genome.<taxon>.<accession.version>` | `spa.genome.synanthedon_tipuliformis.GCA_947623395.1` |
| annotation | `spa.annot.<taxon slug>.<provider>.<method>.<geneset>` | `spa.annot.synanthedon_tipuliformis.ensembl_rr.ensembl.2023_05` |
| search | `spa.search.<taxon slug or family>.<layer>.<yyyy_mm_dd>` | `spa.search.sesiidae.genome.2026_10_23` |
| experiment | `spa.exp.<reference slug>.<experiment>` (not a record: a label that joins observations from one trial) | `spa.exp.naka_2013.gifu_2003_tests2_3` |

The schemas enforce each form. A compound's prefix follows its
`entity_type` (`spa.model.` only for computational models). A fatty acid that
is both a gland product and a biosynthetic precursor needs no role in its ID
or its record: occurrence and role come from observations and reactions.

An observation ID is built mechanically. The taxon slug is the record's
`taxon_id` without `spa.tax.`, the full binomial, never the epithet alone. The
reference slug is the `reference_id` without `spa.ref.`. The validator refuses
any drift (`OBS_ID`). The file is named `<ID without spa.obs.>.yaml`. Like
every ID, the binomial-looking slug is a permanent historical identifier: it
is not renamed when the genus changes.

## Rules

1. **An ID is permanent.** It is never reused and never edited after a release.
2. **Names live in fields, not IDs.** When a taxon's accepted name changes,
   `accepted_name` and `synonyms` change; `taxon_id` does not. The ID records
   which concept was meant, not what it is called today.
3. **A split mints new IDs.** If one Atlas concept turns out to be two
   biological species, each gets a new ID, with `derived_from` pointing at the
   old one. The old ID stays, so records that cited it remain readable.
4. **A name string is not identity.** Two concepts may not share an accepted
   name (`TAXON_NAME_DUPLICATE`). A synonym that spells another concept's
   accepted name must carry both authorities (`NAME_AMBIGUOUS`). External
   records — GBIF, iNaturalist, literature names — are mapped *to* Atlas
   concepts, never used as them.
5. **Contradictory observations are separate records.** A later study never
   overwrites an earlier one; both keep their IDs.

## The test case: "bicingulata"

- *Synanthedon bicingulata* (Staudinger, 1887) is the East Asian species in
  the Atlas (`spa.tax.synanthedon_bicingulata`).
- *Sesia bicingulata* Rebel, 1910 is listed by GBIF as a synonym within
  *S. myopaeformis*, the basionym of a form (`spa.tax.synanthedon_myopaeformis`,
  `synonyms`).

Matching on the epithet would merge two unrelated concepts. Any future
ingestion from GBIF or iNaturalist must map by full name and authority to an
Atlas concept, and report unmapped or ambiguous names rather than guess.

## Within a release

A release (`docs/releases-and-occurrences.md`) freezes every record under its
ID. A manuscript can cite the release DOI and the individual
`spa.obs.…` IDs it used, and both stay valid as the live repository moves on.

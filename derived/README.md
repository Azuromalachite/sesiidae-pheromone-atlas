# derived/

Tables computed from the records in `data/`. **Never edit them by hand.**
Regenerate with `python scripts/build_taxon_layers.py`; CI runs it with
`--check` and fails if a committed table is stale. The outputs depend on the
records alone, with no dates, commits or versions, so the check is stable
across commits. Release metadata (tag, commit, DOI) belongs only in a tagged
release bundle (`docs/releases-and-occurrences.md`).

`derived/` is not a release. Releases will be tagged bundles built from it.

## `taxon_layers.tsv`: the taxon × layer matrix

One row per Atlas taxon, sorted by name.

| column | from |
|---|---|
| `taxon_id`, `species` | the taxon record |
| `genome_status` | see the vocabulary below |
| `assembly_accession`, `assembly_name`, `assembly_level` | the taxon's genome record (`data/genomes/`) |
| `annotation_id`, `pep_fasta_md5` | its first gene set: the archived Ensembl Rapid Release set and the MD5 of its `-pep.fa.gz` from `md5sum.txt`, so a download can be checked |
| `pheromone_status` | see the vocabulary below |
| `compounds_detected_in_females` | every compound with `detected: true` in the taxon's `chemical_measurement` records |
| `compounds_tested_negative` | every compound with `detected: false` in those records. A compound in both columns was found in one study or population and not in another; the records say which |
| `n_chemical_measurement`, `n_behavioural_response`, `n_electrophysiology` | record counts |
| `references` | the references behind the taxon's observations |
| `search_basis` | the search records a status rests on, when it rests on a search |

`genome_status`:

| value | means |
|---|---|
| `assembly` | a genome record exists |
| `no_assembly_in_census` | a dated census of the family (`search_basis`) found no nuclear assembly. **Not evidence that none exists now** |
| `not_searched` | no census covers this taxon |

`pheromone_status`, in order of precedence:

| value | means |
|---|---|
| `female_chemistry_curated` | at least one curated `chemical_measurement` detects a compound in females |
| `attraction_curated` | curated behavioural records only: males attracted to synthetics, no female chemistry curated |
| `found_not_curated` | a dated search (`search_basis`) found literature that no Atlas record holds yet |
| `searched_not_found` | a dated search found nothing. **Not evidence that none exists** |
| `not_searched` | no record and no search |

A status of `searched_not_found` or `no_assembly_in_census` always names its
search; that "not found" is never inferred from missing records is a test
(`test_taxon_layers_never_infers_not_found`).

## Where the searches came from

The searches of 2026-10-23 (`data/searches/`):
- **Assemblies:** the NCBI Datasets genome report for Sesiidae (21 assemblies, 11 species; alternate haplotypes not recorded as genomes).
- **Gene sets:** Ensembl Rapid Release FTP listings and `md5sum.txt`. Rapid Release is archived, and IDs on the new Ensembl platform were not checked.
- **Pheromones:** web and PubMed searches, then primary abstracts. **The Pherobase could not be read** (it sits behind a bot check), so `searched_not_found` rows were not checked against it.

Only Palaearctic and East Asian taxa appear. That reflects where genomes and
pheromone work exist, not the family's diversity: Sesiidae have more than
1,500 species, many tropical (`docs/knowledge-gaps.md`).

## v0.1 taxa

Genome and pheromone: *S. tipuliformis*, *S. apiformis*, *S. myopaeformis*, *S. vespiformis*.
Pheromone only: *S. scoliaeformis*, *S. bicingulata*, *S. tenuis*, *N. pernix*, *S. hector*.
Attraction only, with genome: *S. formicaeformis*, *S. andrenaeformis*.

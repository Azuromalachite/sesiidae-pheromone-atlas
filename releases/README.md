# releases/

## `taxon_layers.tsv` — the taxon × layer matrix

Snapshot of 2026-10-23. One row per species: every Sesiidae species with a
nuclear assembly in NCBI Datasets (11), plus species with a characterised
pheromone and no assembly (5; *S. hector* added from Naka et al. 2008). It decides which taxa enter v0.1 with a
genome layer (concept §4.3). It is a **discovery table, not curated
records**: every pheromone entry was read from an abstract, and curation
reads the full paper.

| column | meaning |
|---|---|
| `assembly_accession`, `assembly_name`, `assembly_level` | primary assembly in NCBI Datasets; empty = no nuclear assembly |
| `annotation_provider`, `annotation_method`, `geneset` | where the gene models come from. All existing ones are archived Ensembl Rapid Release gene sets: `method` is the FTP directory name (`ensembl` = Ensembl's pipeline, `braker` = BRAKER), `geneset` the dated directory |
| `pep_fasta_md5` | MD5 of the gene set's `-pep.fa.gz`, from its `md5sum.txt`, so a later download can be checked against this snapshot |
| `pheromone_evidence` | see vocabulary below |
| `components_as_reported` | compounds and ratios as the source states them |
| `identification_method`, `primary_reference`, `source_read` | how the pheromone was identified, the primary paper (DOI), and what was actually read |
| `population_note` | genome specimen or pheromone population, where it matters |

`pheromone_evidence` vocabulary:

| value | means |
|---|---|
| `gland_identified` | compounds identified from female glands or effluvia, with field activity |
| `female_identified` | identified from females, sampling method not yet confirmed from the full text |
| `field_attractant_only` | males attracted by synthetic compounds in screening; no female-produced pheromone identified |
| `lure_reported_composition_unknown` | males reported at a commercial lure whose composition was not found |
| `not_found` | **no identification found by the search on the stated date.** This is not evidence that none exists |

## How it was built, and its limits

- Assemblies: NCBI Datasets genome report for taxon Sesiidae (21 assemblies, 11 species; alternate haplotypes omitted here).
- Gene sets: directory listings and `md5sum.txt` under `ftp.ensembl.org/pub/rapid-release/species/`. Rapid Release is archived; IDs on the new Ensembl platform were not checked.
- Pheromones: web and PubMed searches for each species, then the primary abstracts. **The Pherobase database could not be read** (it sits behind a bot check), so `not_found` rows have not been checked against it. Expect some of them to change.
- Only Palaearctic and East Asian taxa appear. That reflects where genomes and pheromone work exist, not the family's diversity: Sesiidae have more than 1,500 species, many of them tropical. The tropical, Southeast Asian and *Melittia* gaps are recorded as knowledge gaps, not as scope limits (`docs/knowledge-gaps.md`).

## v0.1 taxa from this table

Genome and pheromone: *S. tipuliformis*, *S. apiformis*, *S. myopaeformis*, *S. vespiformis*.
Pheromone only: *S. scoliaeformis*, *S. bicingulata*, *S. tenuis*, *N. pernix*.

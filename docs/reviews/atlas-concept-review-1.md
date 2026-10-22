# Adversarial review 1 — *Sesiidae Pheromone Atlas* concept

Artifact: `sesiidae_pheromone_atlas_concept.md` (1,356 lines, 40 sections). Reviewed 2026-10-23.
Labels: `[V]` verbatim in the concept or the espmap repo · `[M]` measured by me · `[L]` checked against a retrieved source · `[I]` inferred · `[U]` not verified.

The concept is sound in its epistemics and weak in its contact with the actual data: the taxa, the protein identifiers, the precursor molecules and the espmap hand-off are each specified in a form that does not survive checking against NCBI, Ensembl, the literature or espmap's own gate. Every one of those failures is cheap to fix now and expensive after v0.1 freezes a schema.

---

## F1 — HIGH. The expansion taxa were chosen without the genome check, and the taxa that pass it are not on the list

§4.3 and §33 propose *S. bicingulata*, *S. tenuis* and *Nokona pernix* as the v0.1 expansion set, and v0.1 includes "genome assemblies" [V].

- NCBI Datasets lists **21 Sesiidae assemblies across 11 species**, all of them DToL-style chromosome assemblies or their alternate haplotypes [M, L]. None of the three proposed expansion species is among them. *S. bicingulata* has a mitogenome (2024) and nothing nuclear; I found no sequencing at all for *S. tenuis* or *N. pernix* [L].
- At least one species that **is** in NCBI has an identified pheromone and is missing from the concept: *Synanthedon myopaeformis* (assembly GCA_944738685.1; pheromone Z3,Z13-18:OAc by GC-EAD, Judd et al. 2011) [L]. The other nine (*S. formicaeformis*, *vespiformis*, *andrenaeformis*, *spheciformis*, *Sesia bembeciformis*, *Bembecia ichneumoniformis*, *Pyropteron chrysidiforme*, *Sphecodoptera sheni*) need a Pherobase/primary-literature check [U].
- So the stated selection criterion, "a matched nuclear genome + experimentally characterized pheromone profile" (§3) [V], is applied to the flagships and then inverted for the expansion set.

**Correction.** Before writing any schema, build the taxon × layer matrix: 11 NCBI species × {pheromone identified, primary reference, genome accession, Ensembl annotation}. Pick the v0.1 taxa from rows with both layers. Keep the East Asian species as explicitly "pheromone ✓ / genome —" rows if they matter for the chemistry.
**Validation.** The matrix exists as `data/taxa/*.yaml` plus a generated table; every v0.1 taxon with `genome` filled resolves to a live GCA accession by API.

## F2 — HIGH. There are no NCBI protein accessions to curate; protein identity is an Ensembl annotation release

§20's candidate template keys the protein as `accession: XP_...` [V], and §15 makes "protein accession" an identifier [V].

- None of the 21 NCBI Sesiidae assemblies carries an `annotation_info` block: no RefSeq annotation, so no `XP_` proteins [M, L].
- The gene models that exist are Ensembl's: 11,878 protein-coding genes for *S. tipuliformis*, 16,358 for *S. apiformis* (Ensembl Rapid Release, assembly ilSesApif2.1 / GCA_914767545.1) [L]. "Ensembl" occurs 0 times in the concept [M].
- The two flagships differ by **38 % in gene count** (16,358 / 11,878 = 1.38) for a 1.85× genome-size difference (546.8 / 295.8 Mb) [M]. Whether that is biology or annotation depth is unknown [U], but it means "family X has n members in species A and m in B" is partly a statement about two annotation runs.
- Note also the assembly name: the concept's examples will need `ilSynTipu2.1` (GCA_947623395.1) and `ilSesApif2.1`, not a `…1` version [L].

**Correction.** The protein record's identity is `(assembly accession.version, annotation source, annotation release, stable gene/transcript ID)`. Reserve `refseq_protein` and `uniprot` as optional. Treat any gene-count or "family absent from genome" statement as conditional on the annotation release, and plan a targeted re-search (tblastn/miniprot against the assembly) for the families that matter, since a missing model is not a missing gene.
**Validation.** A test refuses a candidate whose protein identity lacks an annotation release; the v0.3 desaturase search reports, per species, how many hits came from Ensembl models vs from genome-level search.

## F3 — HIGH. The espmap layer is pointed at the pheromone, but the question is about the enzyme's substrate

§25 stores espmap records per **pheromone** (`derived/espmap/e2_z13_18_oac/`), and §26 asks whether "intrinsic substrate electrostatics" distinguishes C2/C3/C4/C13 [V].

- The desaturase, oxidase or isomerase that sets a Δ2 or Δ3 bond acts on a **fatty acyl-CoA**, where C1 is a thioester carbonyl. In the acetate pheromone, C1 is an ether-side CH₂–O. Biochemical numbering is preserved (good — see "What it got right"), but **the same map number sits in a different electronic environment**: C2 of the acetate is β to an ether oxygen; C2 of the acyl-CoA is α to a carbonyl. A map number carries identity across the pathway, not electronics [I].
- The product is also the wrong oxidation state for the question: on E2,Z13-18:OAc, C2–C3 is already a double bond.
- What the existing espmap data say. On the closest computed molecule, the Z3,Z13-18:OAc fixture (10 MMFF conformers, `bench/site_partition.jsonl`), per-carbon site means separate **sp² from sp³ carbons**, not neighbouring sp³ carbons from each other: C3/C4 and C13/C14 sit at −0.9 to 2.4 kcal/mol, chain CH₂ at 3–9 [M]. The conformer range at a single site reaches 6.5 kcal/mol (C5, nearest-nucleus, 2.21 to 8.73) [M]. That is larger than most neighbour-to-neighbour differences in the same table [M], and it matches espmap's own per-site budget (median C18 site moves 5.1 across conformers; rule ≤ 3.95) [V, CLAUDE.md].

**Correction.** Make the espmap subject a **curated precursor compound**, e.g. the Z13-18 acyl thioester with a stated truncation (S-methyl or N-acetylcysteamine thioester for CoA). Record the truncation in the compound record, since the electronics of C2 depend on it. Ask the site question only where the per-site budget allows an answer: report site differences against the conformer and rule spreads, and do not frame §26 as a Δ2 vs Δ3 test until a calibration shows adjacent-CH₂ contrasts exceed them.
**Validation.** One espmap run on the truncated thioester over the conformer set; the C2–C3 mean difference and its conformer spread go in the record. If |ΔV| < conformer spread, §26 says so in the Atlas docs.

## F4 — HIGH. The §11 atom-map convention is a gate BLOCK in espmap

§11 maps chain carbons 1–18 and says nothing about headgroup atoms [V]; "headgroup", "map 0" and similar occur 0 times [M]. espmap's spec makes heavy-atom maps all-or-nothing: partial maps give `PARTIAL_ATOM_MAP`, a BLOCK (`docs/per-site-spec.md` §1) [V]. An acetate has four further heavy atoms (ester O, carbonyl C, carbonyl O, methyl C); an aldehyde has one; a thioester model has more. Every Atlas mapped SMILES written to §11 as stated would be refused by espmap [I from V+V].

Also: the existing espmap C18 fixture is **unmapped and acetate-first** (`CC(=O)OCC/C=C\…`), so its RDKit index 4 is biochemical C1 [V, `bench/fixtures/Z3Z13-18OAc_conf4.sdf`]. Anyone joining Atlas compounds to that fixture by index is off by four.

**Correction.** Reserve a map range for non-chain heavy atoms (e.g. 101+ by a fixed per-headgroup table: acetate 101 O-ester, 102 C=O, 103 O, 104 CH₃), and write it into the compound schema. Coordinate with the espmap P3 fixture so the C18 fixture uses the same maps.
**Validation.** The RDKit validator asserts every heavy atom has a map and chain maps are exactly 1…n along the C1→Cn path; a CI job runs `espmap --check` (gate only, no SCF) on every compound.

## F5 — HIGH. The pathway space omits the chemistry most likely to make E2 and E3 bonds

§16's worked hypothesis is "proposed E2 **desaturation**" with `membrane_fatty_acyl_desaturase` [V]; §19's reference families are desaturases, elongases, reductases, acetyltransferases and oxidoreductases [V]. "CoA", "isomerase" and "oxidase" each occur 0 times; "chain-shortening"/"β-oxidation" 0 times [M].

- A **trans-2-enoyl-CoA** is the obligate intermediate of every fatty-acid elongation cycle (it is reduced by trans-2-enoyl-CoA reductase), and the first product of acyl-CoA oxidase in β-oxidation. **Δ3,Δ2-enoyl-CoA isomerase** interconverts E2 and E3 enoyl-CoAs [I, standard biochemistry]. So an E2 bond and a trace E3 bond (100 : 0.7 in *S. tipuliformis* glands [L]) are both what you would expect from an elongation or oxidation cycle that releases its intermediate, with no exotic desaturase. That is a hypothesis, not a finding; I found no Sesiidae study that tests it [L, negative search].
- It also links your own Route B: Δ11-C16 followed by elongation passes **through E2,Z13-18 enoyl-CoA** on its way to Z13-18 [I]. Route B and the E2 question may be one question. Δ11-C16 + elongation to Z13-C18 is precedented in another moth (2025/26 plant-bioproduction paper) [L, abstract only].
- The evidence vocabulary has no isotope labelling ("isotop|deuter": 0) [M]. Topical application of deuterium-labelled precursors is the standard route-discriminating experiment in moth pheromone biosynthesis (e.g. *Lobesia botrana*, where it established Δ11 desaturation plus chain shortening while the Δ7 desaturase stayed "elusive") [L]. It settles Route A vs B far more directly than genome mining.

**Correction.** Add enzyme families ACOX, TER/ECR and enoyl-CoA isomerase to §19. Add a Route C, "E2/E3 from an elongation or β-oxidation intermediate," next to "E2 by desaturation". Add `isotope_labelling` to the evidence types. List, per route, the labelled precursor that would distinguish it (§37 Q8 asks this; give it a column).
**Validation.** The §37 reaction graph enumerates ≥ 3 origins for the E2 bond, each with a discriminating experiment.

## F6 — MEDIUM. The observation record cannot hold the evidence that already exists

§13 has one observation shape, with `role: major|minor` and `abundance` per component and `methods` per observation [V]. The real records break it:

- *S. apiformis*: E2,Z13-18:Al and Z3,Z13-18:OH at about **2 : 3 in pooled gland extract and about 1 : 7 by SPME of single calling females** (Francke et al. 2004) [L]. The ratio depends on the method by 4.7× (0.67 / 0.14) [M]. Methods must attach to each **measurement**, not the observation.
- *S. tipuliformis*: E3,Z13-18:OAc is 0.7 % of E2 in glands, raised trap catch more than seven-fold at 100 : 0.7, was synergistic at 100 : 3 in Hungary and New Zealand, and **reduced** catches in Tasmania (Szöcs et al. 1990) [L]. "Minor" is an abundance; "synergist/antagonist" is a population-specific behavioural result; `role` conflates them. "Antagon" occurs 0 times [M].
- Invariant 12 ("missing evidence is unknown, not negative") [V] has no state for **tested and not detected**. A gland analysis that looked for a compound and failed to find it, at a stated detection limit, is a real negative, and the schema can only store it as `null`.
- The §13 example says `value: 98, unit: percent` for E2 [V]. The measured gland ratio 100 : 0.7 : 2.7 : 3.2 gives **93.8 %** [M]. Placeholder numbers that look like data end up in data; use real records or values that are obviously placeholders.

**Correction.** Split the observation into types: `gland_composition` (abundances, each with its method), `behavioural_response` (blend, locality, response, comparator), `electrophysiology`. Add `detected: true | false | not_tested` with `detection_limit`.
**Validation.** Encode the Francke 2004 and Szöcs 1990 results as fixtures; the schema must hold both ratios and the Tasmania reversal without free text.

## F7 — MEDIUM. Five hand-entered encodings of one structure, and the §12 check does not cover the error it cites

The compound record holds shorthand, lipid annotation, canonical SMILES, mapped SMILES, InChI and InChIKey [V]. §12 validates **annotation ↔ structure** [V], but its own example of the error it catches is **display name ↔ structure** (`Z3,Z13-18:OH` vs E3) [V]. Unless the annotation is derived from the shorthand, a correct annotation can sit beside a wrong name.

This is espmap's invariant 1 ("one reader") in another form: two copies of the same fact drift.

**Correction.** Hand-enter two fields: `shorthand` and `mapped_smiles`. Generate the lipid annotation by parsing the shorthand, and canonical SMILES, InChI and InChIKey from the mapped SMILES. CI regenerates them and fails on a diff.
**Validation.** A test that perturbs one E/Z in the shorthand of each fixture compound must fail.

## F8 — MEDIUM. Precursors are named, not structured

`precursor.z13_18_acyl` and `precursor.e2_z13_18_acyl` [V] are fragments: acyl attached to what? Invariant 1 requires every compound to have an explicit stereochemical structure [V]; these cannot. Reactions referencing them cannot be balanced or validated.

**Correction.** Decide in v0.1 how acyl-CoA, acyl-ACP and free acids are represented: full CoA SMILES, or a declared truncation with a `represents:` link. This decision also fixes F3's espmap subject.
**Validation.** Every reaction in v0.2 passes an RDKit atom-balance check on its mapped SMILES.

## F9 — MEDIUM. The sprint puts the gate after the data

§36 curates the flagships in steps 4–6 and adds CI validation at step 8 [V]. That is the order espmap learned to reverse ("gate before compute"; CLAUDE.md invariant 2) [V]. Records curated before the validator exists get grandfathered.

**Correction.** Order: conventions → schemas → RDKit validator + CI on 2–3 synthetic fixtures → curation.
**Validation.** The first commit with a real record also contains a CI run that passed on it.

## F10 — LOW. Licensing and upstream terms

The proposed tree has one `LICENSE` [V]. A data resource needs a data licence (CC-BY 4.0 or CC0) separate from the code licence. I could not find Pherobase's reuse terms [U]; its rights holder is listed as A. M. El-Sayed [L]. §14's "discovery and cross-checking only" is the right posture; write it into `CONTRIBUTING.md` as a rule, not a hope.

## F11 — LOW. A family boundary on a chemistry question

The same E2,Z13 / E3,Z13-18:OAc pair is a pheromone of the leopard moth *Zeuzera pyrina* (Cossidae) [L, synthesis-paper title]. A Sesiidae-only scope is fine for v0.1. The schema should still allow out-of-family reference taxa, since convergent use of the same blend in another family is direct evidence about how constrained its biosynthesis is.

## F12 — LOW. Version pinning to an untagged release

§25 pins `version: 0.2.0` [V]; espmap v0.2.0 is not tagged (open PRs #39 and #42 precede review 5 and P3) [M, `gh pr list`]. espmap's own comparability rule is by schema (`espmap.record/1`, `espmap.sites/1`, `analysis_key`), not package version [V, per-site spec §5–6]. Cite those.

## Pricing the plan

Four releases cover roughly seven technical domains: curation, cheminformatics, genome annotation, homology/HMM, phylogenetics, structure prediction and DFT. They depend on one curator who is also shipping espmap v0.2 and Arrowfield [I]. v0.1 is light (RDKit + YAML) and does not depend on espmap's frozen schema: unlike Arrowfield, it can start now without building on a guessed contract [I]. v0.3 is not light: InterProScan and an all-family DIAMOND/HMMER pass compete for the same 7 GB WSL as espmap's heavy jobs [I]. Commit to v0.1 and leave v0.2–v0.4 as direction.

---

## Summary

| # | severity | finding | correction in one line |
|---|---|---|---|
| F1 | HIGH | expansion taxa have no nuclear genomes; 11 Sesiidae species do | build taxon × layer matrix first; add *S. myopaeformis* |
| F2 | HIGH | no RefSeq annotation; `XP_` IDs don't exist | protein identity = assembly + Ensembl release + stable ID |
| F3 | HIGH | espmap on pheromone product, question is about acyl-CoA substrate | curate a truncated thioester; budget site contrasts |
| F4 | HIGH | C1–C18-only maps → espmap `PARTIAL_ATOM_MAP` BLOCK | reserve 101+ for headgroup atoms; gate-check in CI |
| F5 | HIGH | E2/E3 origin limited to desaturation; no ACOX/TER/isomerase, no labelling | add Route C + `isotope_labelling` evidence |
| F6 | MEDIUM | one observation shape; ratio is method-dependent 4.7×; no "not detected" | typed observations, per-measurement method, `detected` |
| F7 | MEDIUM | five hand-entered encodings; §12 misses its own example | enter shorthand + mapped SMILES; derive the rest |
| F8 | MEDIUM | `acyl` precursors have no structure | decide CoA representation in v0.1 |
| F9 | MEDIUM | CI after curation | validator before first record |
| F10 | LOW | one licence; Pherobase terms unknown | separate data licence; written reuse rule |
| F11 | LOW | family boundary hides convergent blend | allow out-of-family reference taxa |
| F12 | LOW | pins untagged espmap 0.2.0 | cite record/site schema IDs |

## What it got right

- **The observation is the record, not the species.** §13's refusal to flatten `species → pheromone` is the hardest decision in the document and the correct one. F6 is about making it strong enough for the data, not about reversing it.
- **Biochemical numbering carried by atom maps.** Because fatty-acyl reductase and acetyltransferase leave the chain numbering in place, a map number really does follow one carbon from acyl-CoA to alcohol to acetate. That makes the identity chain in §11 sound (F3 and F4 are about electronics and the headgroup, not the chain).
- **Route B is named before a Δ13 enzyme is assumed** (§18). Literature supports it: Δ11-C16 + elongation to Z13-C18 has been shown in another moth [L].
- **The espmap limit is stated in espmap's own terms**: it "does not predict which site an enzyme will react at" [V]. That matches espmap's per-site spec.
- **The flagships check out.** *S. tipuliformis* has a chromosome-level genome (GCA_947623395.1, 295.8 Mb) and gland data with exactly the E2/E3 pair described, plus E2,Z13-18:OH, which is a candidate intermediate [L]. *S. apiformis* has a genome and an alcohol + aldehyde blend, so it does separate terminal groups as claimed [L]. It is stronger than the concept says: it **shares the E2,Z13 backbone** with *S. tipuliformis* (as the aldehyde) and has Δ3 as **Z** where *S. tipuliformis* has **E**. That makes the pair a controlled comparison of the Δ2/Δ3 and E/Z questions, not just "different chemistry".
- **Derived ≠ curated** (§27) and **missing ≠ negative** (§20) are the right invariants, provided F6 adds the "tested, not detected" state.

## The one thing to do first

Build the taxon × layer matrix (F1) from NCBI Datasets and the primary pheromone literature before writing a single schema. It decides which taxa are in v0.1, it shows that protein identity has to be an Ensembl release (F2), and it costs an afternoon.

## Sources

- Szöcs et al. 1990 and the gland-composition record for *S. tipuliformis*, via Pherobase: <https://pherobase.com/literature/data/details/E/20748>, <https://pherobase.com/literature/data/details/C/28766>
- Francke et al. 2004, *S. apiformis* pheromone: <https://pherobase.com/literature/data/details/M/8921>
- Judd et al. 2011, *S. myopaeformis*, Can. Entomol. 143:236: <https://bioone.org/journals/the-canadian-entomologist/volume-143/issue-3/n11-002/3Z-13Z-Octadecadienyl-Acetate--Sex-Pheromone-of-the-Apple/10.4039/n11-002.full>
- *S. tipuliformis* genome, Wellcome Open Res 8:300 (v2): <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11499843/>
- *S. apiformis* genome, Wellcome Open Res (2023): <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10879760/>; Ensembl Rapid Release: <https://rapid.ensembl.org/Sesia_apiformis_GCA_914767545.1/Info/Index>
- NCBI Datasets, Sesiidae assemblies (21 records, none annotated): <https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/Sesiidae/dataset_report?page_size=50>
- *S. bicingulata* mitogenome: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11562021/>
- *Lobesia botrana* biosynthesis (labelling; Δ11 + chain shortening; elusive Δ7): <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8019676/>
- Z13-18 via Δ11 + elongation (plant bioproduction): <https://pmc.ncbi.nlm.nih.gov/articles/PMC13411944/>
- *Zeuzera pyrina* E2/E3,Z13-18:OAc synthesis: <https://pubs.acs.org/orlef7/article-abstract/1/6/845/11210/>
- Pherobase rights listing: <https://archives.internetscout.org/r22907/the_pherobase>
- espmap: `docs/per-site-spec.md` §1, §5–6; `bench/site_partition.jsonl` (c18 rows); `bench/fixtures/Z3Z13-18OAc_conf4.sdf`; `CLAUDE.md`

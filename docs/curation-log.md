# Curation log

## 2026-10-23 (15) — the six target papers, with independent review

| paper | taxon | records |
|---|---|---|
| Tumlinson et al. 1974 | *S. pictipes*, *S. exitiosa* (as *Sanninoidea exitiosa*) | 17 |
| Snow, Schwarz & Klun 1987 | *Vitacea polistiformis* (attraction only) | 17 |
| Klun, Schwarz, Leonhardt & Cantelo 1990 | *Eichlinia cucurbitae* (as *Melittia cucurbitae*) | 20 |
| Naka et al. 2010 | *Glossosphecia romanovi* | 29 |
| Yang, Kim, Kang & Jeon 2009 | *S. haitangvora* | 22 |
| Zhang, Leskey, Bergh & Walgenbach 2005 | *S. scitula* | 57 |

- **New records:** 7 taxa, 6 references and 162 observations.
- **New compounds (7):** 16:OAc, Z9-16:OAc, Z11-16:OAc, Z9-16:OH,
  Z9-18:OAc, Z3-18:OAc and Z2,E13-18:OAc. All InChIKeys resolve in PubChem
  to the expected isomers.
- **Totals now:** 23 taxa, 26 references, 24 compounds and 440 observations.

**Taxonomy.** GBIF accepts *Eichlinia cucurbitae* for the squash vine borer,
so that is the accepted name. *Melittia cucurbitae* (NCBI 655047; Klun's
name) and *M. satyriniformis* are recorded as synonyms. *Sanninoidea
exitiosa* is a synonym of *S. exitiosa*: GBIF lists only the genus
*Sanninoidea* as a synonym of *Synanthedon*. *G. romanovi* and *S.
haitangvora* have no NCBI Taxonomy entry.

**Schema (additive).** Response unit `mean_catch_per_trap_per_day`, for Klun
1990's Table 3. The frozen-shape test accepts the change.

**Review.** Three reviewers re-read every record against the PDFs and page
images. Bar readings were checked against the printed totals. No mean,
letter or significance label derived from letters was wrong. They found:
- **Double counting (Klun 1990).** Peaks 2,12 and 11,13 are each one peak,
  yet both candidates were recorded as detected. Now 2,12 is recorded once,
  as the authors' assignment (Z,Z-3,13-18:OAc, "by inference only"), and
  11,13 is left unassigned.
- **Quotes on the wrong contrast.** These were moved, or new records were
  added to carry them:
  - Snow's "did not differ significantly from the 2 %" now sits on a 99:1
    vs 98:2 record;
  - Snow's "almost as good" now sits on a 0.5:0.5 vs 1 % record;
  - Yang's "unattractive alone" now sits on an E2-vs-control record;
  - Zhang's "most of the ternary blends" was removed from its three
    non-significant contrasts;
  - Naka's "alcohol alone could attract" was removed from Test B, where the
    alcohol alone caught nothing.
- **Setup details carried over without warrant.** Naka 2010's 2006 trap
  model, septum and trap height were on the 2009 records; they are now
  stated only for 2006. Tumlinson's Fig. 2 locality and lure purity are
  dropped, because the paper states neither for that test.
- **Inconsistent significance.** Tumlinson's Fig. 2 records had mixed
  labels. All 1–50 % (Z,Z) contrasts for *S. pictipes* are now `significant`
  as the authors state, with the missing test listed under `unresolved`.
- **Missing contrasts added (14):**
  - Klun Test 1, A vs D and B vs C;
  - Klun Test 2, E vs I and G vs I;
  - Zhang Fig. 2, binary vs the Z,Z/Z,E lure at three sites;
  - Yang 9:1 vs control;
  - Naka 2010, the alcohol alone vs control in Tests A and C;
  - three Snow contrasts against the best lure.
- **Overclaims softened:**
  - Tumlinson's abundance class is removed;
  - the ozonolysis product seen only in the synthetic is now labelled so;
  - Zhang's effluvium identifications are marked as resting on retention
    matches to the gland peaks;
  - Zhang's synthetic GC-EAD column is "not stated";
  - Naka's `n_individuals` is null, because the paper does not say how many
    of its three extracts were analysed.

### Internal inconsistencies found in these papers

- **Tumlinson 1974:**
  - The natural *S. pictipes* pheromone is "120 µg" in the text and 120 ng
    in the Fig. 2 legend. The internal evidence favours ng.
  - The IR band absent in *S. exitiosa* is called 960 cm⁻¹, after the trans
    band was given as 970.
- **Klun 1990:**
  - The abstract's binary is 99.7:0.3; the lures were about 99.85:0.15.
  - Compound 9 is named as an acetate with an alcohol acronym.
  - The abstract hedges every minor compound as "probably"; the Results
    call five of them confirmed.
- **Naka 2010:**
  - Table 2's totals do not follow from its means (132 vs 144 printed).
  - The five-component lure holds the 3Z,13E isomers and Z3-18:OAc, where
    the gland had E3,Z13 compounds and Z13-18:OH. Its amounts match the
    gland ratio position by position, and the table title names
    3-octadecenyl compounds, so this is not one typo. Recorded as printed.
- **Yang 2009:** by the Fig. 2 letters, Z3,Z13-18:OAc alone did not differ
  from the control, although the text calls it attractive.
- **Zhang 2005:**
  - The Discussion cites Fig. 3 for an 88:6:6 lure that Fig. 3 did not
    test.
  - The abstract gives the binary as 1–3 % E,Z-2,13; every binary lure had
    6 parts.
  - The Methods give log transformation; the Fig. 2 legend gives arcsine
    square root.
  - The lure-longevity dates and state in Table 2 conflict with the text.

### Not recorded, by design

- **Results stated without numbers:**
  - Tumlinson's isomer purity tests and cross-species claims;
  - Snow's 1983–1984 isomer screens;
  - Yang's "other geometrical isomers" (data not shown).
- **Non-target catches:** Klun's *S. acerrubri* totals; the non-target
  species in Zhang's and Yang's traps.
- **Zhang's lure longevity** and species-specificity percentages.
- **Zhang's 0.03–0.05 mV synthetic 2,13-isomer readings.** The paper does
  not call them responses.

**Analysis.** The single-addition analysis now finds 156 contrasts in 15
species: 98 additions and 58 replacements.
- **E2,Z13-18:OAc** no longer looks inert; entry 14's "never changed
  catches of the 3,13-diene users" does not survive *S. scitula*, a
  Z3,Z13-18:OAc user. It raised catches in 13
  contrasts, all in the two species whose glands contain it (12 in *S.
  scitula*, 1 in *S. haitangvora*). It never lowered catches.
- **E3,Z13-18:OAc** is now mostly an antagonist: 28 of 46 contrasts went
  down: 12 in *S. scitula*, 6 in Japanese *S. tenuis*, 5 in *S. exitiosa*,
  2 each in *V. polistiformis* and *S. tipuliformis*, 1 in *S.
  scoliaeformis*.

## 2026-10-23 (14) — scope statement and the first analysis

**`docs/scope-v0.1.md`** states what v0.1 is complete for: species with a
female pheromone identified from glands or emissions. 9 are curated and 7
are listed to curate, with verified DOIs. No complete census was reachable:
Ando's list returned 404, the Wayback Machine refused the request (rate
limit), and the Pherobase sits behind a bot check. So the target list comes
from the identifications that the curated papers cite. The gap to the
papers' count of about 20 is stated, and the v0.1.0 tag waits for it.

**`analyses/added_compound_effects.py`** is the first analysis. It reads only
`derived/tables/`. It found 66 contrasts in which the treatment lure holds one
compound more than its comparator, across 8 species, and separates 50 true
additions from 16 replacements at constant dose. That distinction was not
in the first version of the analysis; it is derivable from the tables.
Results:
- E3,Z13-18:OAc is the most-tested modifier, with population-dependent
  effects in *S. tipuliformis* and suppression from 9 % up in Japanese
  *S. tenuis*.
- E2,Z13-18:OAc never changed catches of the 3,13-diene users.
- Z3,Z13-18:OH is required, antagonistic or neutral depending on the
  species.

The tables answered without the YAML. The one gap is in the data: Yang
2011's minor compounds have no amounts ("3 %"), so no share can be
computed. This meets the "one real analysis" condition for a DOI in
`docs/releases-and-occurrences.md`; the scope condition is not met yet.

## 2026-10-23 (13) — tidy tables as the analytical form

`taxon_layers.tsv` is not tidy. It puts several compounds in one cell, and
that is fine for a human-facing summary, which is all it is. The records
stay the normalised source. They are not flattened into a spreadsheet, which
would lose their structure.

The analytical form is now 17 tidy relational tables in `derived/tables/`,
generated by `scripts/build_tables.py` and checked with the rest of
`derived/`. Each table holds one entity or one kind of measurement, one row
per thing, keyed by Atlas IDs. Prose stays in the JSONL. A test checks that
every table is rectangular and that every key joins. Nothing in the record
shape changed.

## 2026-10-23 (12) — R5 and R6 backfilled; the v0.1 shape is frozen

- **`taxon_name_as_reported` is on all 278 observations,** each checked
  against its source's full text. Every source uses the accepted combination
  except Kovalev et al. 1988, which writes *Aegeria apiformis*. GBIF lists it
  as a synonym of *Sesia apiformis* (10560630 → 5141493), and it is now in the
  taxon's `synonyms`. The regex scan missed Priesner 1986's *S.
  andrenaeformis* (hyphenated across a line) and could not read Tamaki 1977
  (Japanese); both were confirmed by eye.
- **`experiment_id` is on all 252 behavioural records.** It was proposed from
  the existing ID suffixes and source locations, reviewed group by group, and
  corrected where the mechanical rule merged or split wrongly:
  - Szöcs 1990's Hungary records are three experiments;
  - one Table I trap series at Kairėnai caught both species in Mozūraitis
    2006;
  - Priesner 1986's Table 1 is one series of four species;
  - Naka 2013 tests II and III share traps;
  - Yang 2012's acetate-alone record pools two trials, so it lists both.
- **New checks:** `NAME_AS_REPORTED` and `EXP_ID`. Four failing fixtures.
- **The record shape is frozen as v0.1** (`schemas/frozen-v0.1.json`). The
  tests refuse any non-additive schema change.

## 2026-10-23 (11) — stage D: schema acceptance test, Naka et al. 2013 (*S. tenuis*)

**What the paper adds.** It is the Japanese *S. tenuis* gland identification,
the first gland data from Japan. 26 records: gland, GC-EAD, 22 *S. tenuis*
trap contrasts, and 3 *S. hector* records from the cross-attraction test.
Japanese females make Z3,Z13-18:OAc (about 2 ng) and no Z3,Z13-18:OH, and
10 % of the alcohol cuts catches by about 75 %. Korean females (Yang 2012)
show the exact reverse. The narrative's *S. tenuis* passage was rewritten
around this reciprocal reversal; it still decides between neither one
species with two pheromone races nor two taxa under one name.

**Acceptance questions, answered:**

| question | answer |
|---|---|
| Does `chemical_measurement` hold the gland data without awkward free text? | Yes: one sample material, one detection, eight tested negatives with methods, and the source wording in `material_as_reported` |
| Does `entity_type` stay neutral? | Yes: no compound record changed, and the unnatural isomers needed no class |
| Can every behavioural conclusion be read from the records? | Yes, with one exception: tests II and III print the same Z3,Z13-18:OAc-alone row from the same orchards and dates, so they probably share traps, and the records cannot link them. **This is the case for R5 (`experiment_id`)**, now no longer hypothetical |
| Are trap, dispenser and purity enough? | Yes; the alcohols carry no purity because the paper states none |
| Any new ambiguity? | Table 5 prints one significance mark per test in an ambiguous column, and for V-2 the "n.s." conflicts with the means under either reading. The `unresolved` field and `significance: not_reported` hold this without a schema change |

All 18 first-draft records validated on the first run. The schema took the
paper without change, so the v0.1 shape can be frozen once R5 and R6 land.

**The independent check against the PDF** found no wrong value. It found
one wrong note (on which zero-catch treatments the paper excludes) and
several overstated or mis-anchored items. All are fixed:
- the Z2,Z13 and E2,E13 negatives are dropped, because their standards
  co-elute with the Z3,Z13 peak;
- the GC-EAD males' origin is unstated in the paper, so it is not recorded;
- quotes are moved to the contrast they describe;
- the five unrecorded blanks are added, and so is *S. hector*'s own
  attraction to its 50:50 blend;
- the Tamaki 5 % conflict is noted;
- the printed coordinate swap and the caption-versus-text ion mismatch are
  in the reference notes.

The reference is `naka_2013`, matching the printed citation (online
2012-11-07).

## 2026-10-23 (10) — the database gate catches up with the structure gate

An outside adversarial review (against `origin/main`, then checked against
the local state) found the structure checks far stronger than the database
checks. Fixed now:

| finding | fix |
|---|---|
| R1 a repeated YAML key kept its last value silently, before any check ran | strict loader, `YAML_DUPLICATE_KEY`; fixtures at the root and inside an inline mapping |
| R2 one real thing could hold two IDs | `IDENTITY_DUPLICATE` on molecular graph and InChIKey, DOI (case-folded) and PMID, assembly, NCBI taxid and GBIF key; three fixtures |
| R3 an observation could contradict itself | `OBS_DUPLICATE_ENTRY` for components, each blend, and antennal readings by compound × method × preparation; `abundance_class` only on a detection |
| R4 a record in a subdirectory was never read | records are read recursively; any other YAML or `.yml` under `data/` is `DATA_OUTSIDE_GATE` |
| R7 a summary label could hide which evidence exists | the matrix's `chemical_materials` separates gland content from emission; the label is documented as a summary |
| R8 `concept.md` read as a second specification and promised an `espmap --check` CI job that does not exist | it is marked non-normative, the missing job and the failed Tasmanian strain are stated, and the README index says so |
| R9 `author_statement` mixed quotation and translation | `author_statement_form` (verbatim when absent); Tamaki's two are `curator_translation`; `LICENSE-DATA.md` carves quotations out of CC BY |
| R10 quantities allowed nulls and free unit strings | value required and non-negative; unit from `picogram` … `gram`, `ratio_part`; the one null detection limit (Francke 2004 SPME) removed |
| R12 a fixture only had to contain its code | `EXPECT` is the exact set. It exposed `missing_reference` also failing `OBS_ID`, now fixed |

The narrative's "attracts one species and repels another" (Mozūraitis 2006)
is corrected: E3 enhances attraction to a blend for one species and
suppresses it for another, and was not tested alone.

**Not done yet:**
- R5 (`experiment_id`) and R6 (`taxon_name_as_reported`) are deferred: they
  are additive and due before a public release.
- R11 (head-group table validation, charge convention, CoA stereochemistry)
  is written into `docs/validation.md` as the v0.2 chemistry gate.

None of the 252 observations broke the new rules.

## 2026-10-23 (9) — stage C: release machinery, no release

- **`scripts/build_release.py` writes `derived/`:**
  - one JSONL file per record kind;
  - the taxon × layer matrix;
  - `summary.json` (counts, generator versions, schema hashes);
  - `SHA256SUMS`.

  It refuses records that do not validate. `--check` runs in CI and in the
  tests, and flags stale files and files the script did not write.
  `.gitattributes` keeps line-ending conversion off `derived/`, so the
  byte-exact check holds on Windows checkouts too.
- **`--bundle VERSION` builds `dist/sesiidae-atlas-v<VERSION>/`** from a clean
  tree at the matching tag. Only its `manifest.json` carries the version, tag,
  commit and commit date, with `doi: null`. `dist/` is ignored by git.
- **Environment:** `requirements.txt` became `requirements.in` (constraints)
  plus `requirements.lock.txt`, resolved in a fresh Python 3.12 venv by
  `scripts/lock_requirements.sh`. CI installs the lock and runs on
  `ubuntu-24.04` rather than `ubuntu-latest`. A test checks that the lock
  satisfies every constraint.
- **`CITATION.cff`** has no DOI, and a test keeps it that way until one
  exists. **`CHANGELOG.md`** starts with the unreleased breaking changes.
- **No tag, no release, no DOI**, as decided
  (`docs/releases-and-occurrences.md`).

## 2026-10-23 (8) — stage B: the matrix is generated, and "not found" is a record

`releases/taxon_layers.tsv` was a hand-made second source of truth. It is now
`derived/taxon_layers.tsv`, built by `scripts/build_taxon_layers.py`.
`releases/` became `derived/`, because a derived table is not a release.

- **What the table needed to become records:**
  - 5 taxa: *S. spheciformis*, *Sesia bembeciformis*, *Bembecia
    ichneumoniformis*, *Pyropteron chrysidiforme* and *Sphecodoptera sheni*,
    with NCBI and GBIF IDs and authorities from GBIF;
  - 7 genome records, from the NCBI Datasets reports and the Ensembl
    `md5sum.txt` files. All four gene-set MD5s match the old table;
  - 6 searches, a new record kind (`data/searches/`, `schemas/search.schema.json`):
    - one genome census of Sesiidae;
    - five pheromone searches: three not found; *S. bembeciformis* and *B.
      ichneumoniformis* found but not curated.
- **"Not found" now comes only from a search record.** The generator
  distinguishes curated evidence, a dated search that found nothing, and no
  search at all. A test asserts that every not-found status names its search.
  GBIF IDs were also filled in for *S. formicaeformis* and *S. andrenaeformis*.
- **An ID defect found on the way.** Annotation IDs were
  `spa.annot.<provider>.<method>.<geneset>`, and
  `spa.annot.ensembl_rr.ensembl.2023_05` would have named the gene sets of
  three species. They now carry the taxon slug. `ANNOT_ID` checks the prefix
  and uniqueness.
- **The generated table drops the old prose columns.** The facts in them
  (populations, purity, ratios) are in the records, and the curatorial labels
  ("flagship", "expansion taxon") are in `derived/README.md` as the v0.1 taxon
  list. Genome-specific notes (haplotypes, frozen Rapid Release) are in the
  genome records.
- **Checks:** CI runs `build_taxon_layers.py --check`, and the test suite runs
  it too.
- **Fixtures:** `annot_id_wrong_taxon`, `search_id_mismatch`,
  `search_not_found_with_find`, `search_census_of_taxon`.

## 2026-10-23 (7) — stage A migration: identities separate from observations

One breaking commit, before anything is citable. The principle is that IDs
and chemical entities identify things, while observations describe what was
measured or done.

1. **Observation IDs carry the full binomial and the reference slug:**
   `spa.obs.<taxon slug>.<reference slug>.<what>`. For example,
   `spa.obs.tipuliformis.2006.mozuraitis.gland` became
   `spa.obs.synanthedon_tipuliformis.mozuraitis_2006.gland`.
   - The epithet alone was already ambiguous here: `bicingulata` names both
     *S. bicingulata* and Rebel's *Sesia bicingulata*, which is under *S.
     myopaeformis*.
   - All 252 IDs were derived mechanically from each record's `taxon` and
     `evidence.reference`. The script asserted that every old year and author
     matched the reference.
   - Files are renamed to match. ID references in data notes and docs were
     rewritten.
   - New check `OBS_ID`, with fixture `obs_id_taxon_mismatch`.
2. **`compound_class` is gone; `entity_type` is `chemical` or
   `computational_model`.**
   - `natural_product`, `synthetic_analogue` and the never-used `precursor`
     all described occurrence or role, which belong to `chemical_measurement`,
     behavioural and (later) reaction records, not to the molecule.
   - All 17 compounds became `chemical`.
   - Fixture `compound_class_legacy` keeps the old field out.
3. **`gland_composition` is `chemical_measurement`, with a required `sample`:**
   - `materials` comes from a fixed list: `gland_extract`,
     `ovipositor_extract`, `effluvium` and `other`.
   - `material_as_reported` keeps the source wording.
   - `result_scope` must be `combined` exactly when more than one material is
     listed, so a combined result cannot be read as shown in each matrix.
   - `context.tissue` is removed. The 12 tissue strings mapped onto
     15 × gland extract, 2 × effluvium (Judd 2011 effluvia; Francke 2004 SPME
     near the calling gland), 1 × ovipositor extract (Szöcs 1985), and
     1 × combined ovipositor extract + effluvium (James 2001).
   - Fixtures: `sample_scope_mismatch`, `sample_material_unknown`.

`docs/concept.md` revision 3 keeps its old examples and now opens with a note
on what the implementation changed. The scratchpad generators used for
earlier batches emit the old format and must not be re-run; the records are
the source.

## 2026-10-23 (6) — six more full texts, with independent review

| paper | taxon | records |
|---|---|---|
| Voerman, Persoons & Priesner 1984 | *S. tipuliformis* (Netherlands; SSR from Bavaria and Austria) | 16 |
| Mozūraitis & Būda 2013 | *S. scoliaeformis* (Lithuania) | 21 |
| Judd, Gries, Aurelian & Gries 2011 | *S. myopaeformis* (introduced, British Columbia) | 14 |
| Judd & Eby 2014 | *S. myopaeformis*, trap colour and design | 41 |
| Levi-Zada et al. 2011 | *S. vespiformis* (Israel) | 28 |
| Naka et al. 2008 | *S. hector* (Japan), new taxon | 26 |

New: 1 taxon (*S. hector*, NCBI 2912888, GBIF 1940506), 6 references,
5 compounds (Z2,Z13-18:OAc, Z2,Z13-18:OH, 18:OAc, E3,E13-18:OAc,
Z3,E13-18:OAc; all InChIKeys resolve in PubChem to the expected isomers),
146 observations. The file supplied as Naka 2012 (*S. tenuis*) was Naka et al.
2008 (*S. hector*); the *S. tenuis* paper is still wanted. Szöcs et al. 1998
is deferred (no access).

Judd & Eby 2014 was curated by a separate agent from the PDF. All six papers
were then re-read against the PDFs by three reviewers working without the
curator's notes. No number or significance letter was wrong; the defects were
in conventions, quotes, notes and missing contrasts, and all are fixed.

### Schema changes

| change | forced by |
|---|---|
| `dispenser` (design, description) on treatment and comparator; the identical-comparator check compares it | Voerman: the same lure in a polyethylene vial caught 23 per trap, on a sleeve stopper 9 |
| trap design `funnel` (Unitrap) and `bottle` | Voerman, Levi-Zada, Judd & Eby |
| antennal response `inconsistent` | Judd 2011: E3,Z13-18:OAc on DB-23 only |
| purity kind `chemical_and_isomeric` | Mozūraitis 2013 |
| unit `mean_catch_per_trap_per_week` | Levi-Zada 2011 |
| **with `significance: not_tested`, `effect` is the direction of the raw numbers**; the authors' reading goes in `author_statement` | review: Voerman's 32 and 34 vs 46 were `no_effect` on the authors' "small amounts" sentence while 35 vs 46 was `decreased` |
| **`identification` follows the authors' own wording**; the notes say what it rests on (e.g. geometry from retention on one polar column) | review: Levi-Zada and Naka identify by MS plus DB-23 retention, Judd by retention only, and none call it tentative |
| `synthetic_analogue` defined as "no Atlas gland record yet" | Naka 2008 and Voerman test isomers no gland record holds |

### What the review changed

- **Missing contrasts added:**
  - Judd 2011: ternary vs the alcohol binary, and each binary vs the control;
  - Levi-Zada: the gland-ratio 4:1 lure as comparator;
  - Naka 2008 Test I: 70:30 and 30:70 vs blank;
  - Mozūraitis: blend vs control at the second site;
  - Voerman: the headline result, E2,Z13-18:OAc vs blank;
  - Judd & Eby: four more colour contrasts;
  - gland negatives the figures show but the records lacked.
- **Quotes moved** to the sentence about each record's contrast (Judd ternary, Naka 70:30 and Test IV, Levi-Zada dose).
- **Overstated negatives softened.** Voerman's Z2,Z13-18:OAc is `not_tested`, not `inactive`: no specialist cell is not no response. Judd's effluvia E2,Z13-18:OAc negative is noted as weak: on DB-5 it drew no response even in gland extracts.
- **Purity removed where the paper gives none** (Voerman's alcohols, synthesis intermediates).
- **Inferences labelled:** the trap for Voerman's vial test, the Starnberg setup, the Mozūraitis habitat, Levi-Zada's dose-trial habitat.

### Internal inconsistencies found in these papers

- **Mozūraitis 2013:** Methods say six females; the Fig. 1 caption says three. Mozūraitis 2006 had the same kind of discrepancy, 12 vs 6.
- **Naka 2008:**
  - The abstract labels Z3 as I and E3 as II (60:36:4); the Results reverse the labels (36:60:4).
  - Test I: "92 males by four traps" against 24.5 per trap with n = 2.
- **Levi-Zada 2011:**
  - The Discussion says single components "did not attract any males"; Table 2 shows 0.2–0.4.
  - Table 3 prints 1.9 ± 2.1, which cannot be an SE of five non-negative counts.
- **Judd 2011:** the text says retention matched on four columns; Table 1 marks antennal responses on three columns (Z3,Z13-18:OH) and two (E2,Z13-18:OAc).
- **Judd & Eby 2014:** eight, listed in `data/references/judd_2014.yaml`. Among them: the wrong experiment and figure cited in the Discussion, and 82 % vs 83 %.

### Not recorded, by design

- Diel activity (Mozūraitis 2013): there is no observation type for it.
- Lure ageing (Levi-Zada 2011): the schema has no lure age.
- Mating disruption (Levi-Zada 2011).
- Feeding-attractant traps (Judd & Eby 2014, experiments 2, 3 and 15).
- Results stated without numbers (Voerman: blank traps, the Unitrap, the Starnberg confirmation).

## 2026-10-23 (5) — adversarial review of entries (3) and (4)

Every record from Yang 2011, Naka 2006 and Kwon 2021 was re-read against the
PDFs by a reviewer working without the curator's notes. **No number or
significance letter was wrong.** The defects were in what was left out, in
what was attributed, and in inferences not marked as such.

| defect | fix |
|---|---|
| **Kwon's purity labelled "chemical".** The paper says only "purity". Fig. 4 shows minor peaks 0.07–0.37 min after each main peak, and E3 and Z3 eluted 0.035 min apart (separate runs), so the impurities could be isomers | `kind: unspecified`; the notes give the peak times; narrative §3 rewritten |
| **Significant contrasts missing.** Kwon Exp. 4 was recorded only as yellow vs green and yellow vs white. At Gongju neither is significant; the only significant contrast there is yellow vs blue (6.0 vs 0) | yellow against all five other colours at each site (15 records) |
| **Yang Fig. 2 and Naka Table 4 rows missing**, including Yang's 2:8, which Kwon contrast with their own result | Yang 2:8, 5:5, 6:4, 8:2, 9:1; Naka Z3 alone, 1:9 (Test I), 5:5 and 9:1 vs E3 alone (Test II) |
| **Verbatim quotes on the wrong contrast**: Kwon 1:9, 3:7 and 5:5 (2018) and Naka 9:1 vs E3 alone | replaced with the sentence about that contrast, or left out where the paper has none |
| **Unmarked inferences**: "second flight" (Naka 2005), "spring" and "autumn" (Kwon), one female per injection (Naka gland), calling females (Yang gland), "Japanese vine clearwing" and the authority (*N. pernix*) | labelled as Atlas inferences, set to null, or credited to GBIF |
| **"Not reported" for a test that was not run.** Yang excluded zero-catch lures from the ANOVA | new `significance: not_tested` |
| **Kwon's headline 4.3:5.7 recorded nowhere** | kept out of the observations on purpose (it is a correction, not a lure anyone tested) and explained in the reference's notes |
| **The identical-comparator check depended on list order** (found in the validator audit) | blends compared as sets; new fixture `comparator_reordered` |

The narrative also overclaimed twice. Naka's major-component swaps do not show
that "geometry matters more": those lures had no natural major at all. And
the Kwon 1:9 reversal kept the site fixed at Gongju, so only season and trap
colour changed. Both are rewritten.

Kwon's Discussion says Yang 2011's lures were isomer mixtures; Yang's
Methods state isomeric purity above 99 %. Both statements are kept, each in
its own paper's records.

## 2026-10-23 (4) — Kwon et al. 2021

Full text of Kwon, Huh, Lee, Seo & Park 2021 (*S. bicingulata*, Korea,
2017–2019): 1 reference (no PubMed record), 25 observations (34 after the review in (5)). These are:
- 16 ratio contrasts against 4:6 (Gongju 2017; Jinju, Gongju and Gapyeong 2018);
- bucket vs delta trap;
- yellow vs green bucket (two spring sites);
- yellow vs green and yellow vs white bucket (three autumn sites).

Values are read from bar charts except the bucket/delta means (abstract).

### What this paper corrected, including the entry above

- **Entry (3) said the less pure lures were Kwon's. That mixes two kinds
  of purity.** Kwon's 94.18 % and 82.8 % are *chemical* purity from a GC-MS
  trace, and they state their lures held no isomers. Yang's > 99 % is
  *isomeric* purity, stated without data. Kwon's claim that Yang gave no
  isomeric information is still wrong. Neither paper shows a separation of
  the 3,13 geometric isomers on the column used for the lure check: Kwon's
  is a non-polar HP-5MS. That last point is an Atlas inference and is
  marked as one in the records. *Corrected in (5): Kwon do not say the
  purity is chemical, and the impurity peaks could be isomers.*
- **4.3:5.7 is not a tested lure.** It is the nominal 4:6 lure corrected for
  the two purities: 0.4 × 94.18 : 0.6 × 82.8 ≈ 43 : 57.
- **Text and figure disagree on where 4:6 beat 3:7.** The text says Gongju
  2018; in Fig. 5, Gongju 3:7 shares a letter with 4:6 (ab), and Jinju 3:7
  does not (bc). The records follow the figure.
- **Bucket vs delta confounds design with colour** (green bucket, white
  delta).
- **1:9 reverses between seasons:** 8.5 per trap in spring 2017 (green
  traps), close to zero in autumn 2018 (yellow traps) at all three sites.

### Schema changes forced by this paper

| change | forced by |
|---|---|
| blend `purity`: value, `kind` (chemical / isomeric / unspecified), `basis` (measured / stated) | Kwon measures chemical purity; Yang states isomeric purity |
| `trap` on the treatment and, when it differs, on the comparator: design, colour, CIE L*a*b*, supplier | trap-type and trap-colour experiments compare traps, not blends |
| validator: a comparator must differ from the treatment in blend or trap (`OBS_FIELD_CONFLICT`) | the trap experiments are the first records whose blends are identical |

Yang 2011 and Naka 2006 records were backfilled with their traps (delta;
sticky board), and Yang's with the stated isomeric purity. Older records
are not backfilled yet. Four failing fixtures: `purity_over_100`,
`purity_without_kind`, `trap_design_unknown`, `comparator_identical`.

## 2026-10-23 (3) — Yang et al. 2011 and Naka et al. 2006

Two more full texts: Yang, Kim & Lee 2011 (*S. bicingulata*, Korea) and
Naka et al. 2006 (*Nokona pernix*, Japan). New: 1 taxon (*N. pernix*,
GBIF 1940056, no NCBI entry), 2 references, 2 compounds, 23 observations.
The two new compounds, E3,E13- and Z3,E13-18:OH, are unnatural isomers
that Naka tested as lure components; their InChIKeys resolve in PubChem
to CID 5364515 and 5364516. Both PMIDs were checked against their titles.

| paper | records |
|---|---|
| Yang 2011 | gland (six compounds, 2:58:100:6:3:4, N = 10); five ratio contrasts from Fig. 2; five minor-compound additions from Fig. 3 |
| Naka 2006 | GC-EAD; gland (12.3 and 1.4 ng per female, n = 8, acetates not detected); six ratio contrasts from Table 4; four isomer substitutions from Table 5 |

**Yang 2011 values are read from bar charts** (`qualifier: approximate`).
Naka 2006 gives tables (`as_reported`), with mean ± SD in the notes.

### What these papers corrected

- **The narrative had Kwon et al. 2021's purity claim the wrong way round.**
  Kwon says Yang 2011 gave no purity and suggests impure synthetics
  flattened Yang's ratio response. Yang's Methods give isomeric purity
  above 99 % (Pherobank). Kwon measured their own lures at 94 % and 83 %.
  `docs/literature-narrative.md` §3 and the matrix row now say so.
- **Naka's "slightly attractive" is not significant.** E3,Z13-18:OH alone
  caught 0.5 per trap in Test I, which shares letter c with the blank, and
  0.0 in Test II. The record is `no_effect` and quotes the authors' wording.
- **Zero-catch treatments were left out of Yang's statistics.** Yang
  excluded them from the ANOVA, so the binary blend against either single
  acetate (10.3 vs 0) is `significance: not_reported`, not significant.

### Schema changes forced by these papers

| change | forced by |
|---|---|
| component `identification: confirmed / tentative`; only on a detected compound | Yang 2011 identifies three of six compounds by retention index only |
| `compound_class: synthetic_analogue` | Naka 2006 tests E3,E13- and Z3,E13-18:OH, which are not reported from any sesiid |

Two new failing fixtures, `identification_unknown` and
`identification_on_negative`, keep the new field honest.

## 2026-10-23 (2) — full texts

All records are now curated from full texts (`read: full_text`), ten papers:
Szöcs et al. 1985, 1990; Priesner et al. 1986; Kovalev et al. 1988;
Tamaki et al. 1977; James et al. 2001; Francke et al. 2004; Suckling et
al. 2005; Mozūraitis et al. 2006; Yang et al. 2012.

Records: 6 taxa, 10 references, 10 compounds, 40 observations
(gland composition, behavioural response, electrophysiology). All ten
compounds' InChIKeys resolve in PubChem to the expected names.

Szöcs, Henderson & McNeil 1998 (Canada) is **not** curated: the file
supplied as that paper is a different article in the same issue (Trudel et
al., white pine weevil, *Can. Entomol.* 130:201–214).

### These papers are observations, not reactions

They establish that a compound is present in a gland, emitted, antennally
active, attractive, synergistic, antagonistic, or not detected, and that
ratios depend on assay and population. They do not establish any
precursor → product conversion. Two compounds in the same gland (for
example E2,Z13-18:OH and E2,Z13-18:OAc) are not evidence that one is made
from the other; where authors suggest it (Mozūraitis et al. 2006: "could be
intermediates"), that is an author hypothesis. No reaction records were
made from this corpus. The reaction grammar needs a different corpus:
isotope-labelled precursors, enzyme assays, heterologous expression,
characterised desaturases, elongases, FARs, ACOX/ECI.

### Disagreements the records hold rather than resolve

| question | one side | other side |
|---|---|---|
| Does E3,Z13-18:OAc synergise in New Zealand? | 4.6× and significant, 1985–86 (Szöcs 1990) | 481 vs 490, equivalent, 2003–04 (Suckling 2005) |
| Does it inhibit in Tasmania? | decreased, significant, 1986 (Szöcs 1990) | not significant 1987 (Szöcs 1990); no blend effect, P = 0.83, 2003–04 (Suckling 2005) |
| Does Z13-18:OAc add anything for *S. tipuliformis*? | significant increase at 5:1, 1984 (Szöcs 1985) | no significant effect 1984–87 (Szöcs 1990); no receptor cell for it (Priesner 1986) |
| Is Z3,Z13-18:OAc attractive to *S. tenuis*? | 51 males, Japan 1976, no control (Tamaki 1977) | 0 alone and absent from glands, Korea 2011 (Yang 2012) |
| Is Z3,Z13-18:OH alone the *S. apiformis* pheromone? | "identified as a sex pheromone" (Kovalev 1988) | not attractive alone; needs E2,Z13-18:Al (Francke 2004) |
| Does 200 µg E2,Z13-18:OH reduce *S. apiformis* catch? | "significantly reduced" (Francke 2004, text) | shares a letter with the binary blend (Francke 2004, Table 3) |

The *S. tenuis* contrast differs in population and in dose, dispenser and
trap, so it does not by itself show a population difference.

### Internal inconsistencies and citation drift found in the sources

- Mozūraitis 2006: 12 calling females in Methods, 6 in Results and Fig. 1.
- Szöcs 1985 reports E2,Z13-18:OAc : Z13-18:OAc = **93:7**, with no E3. It is cited as 97:3 (Mozūraitis 2006) and as a 100:3 E2:E3 blend (James 2001). Records cite the primary paper only.
- James 2001: the abstract's 100:3 is the lure ratio; the measured blend is 98.2 : 1.8 (n = 3).
- Szöcs 1990: dose range 10–1000 µg in the paper, 10–100 in an AGRIS abstract copy.
- Szöcs 1990 counted repeated checks of a trap as repetitions, so its significance letters are weaker evidence than they look; recorded in the notes.

### Schema changes forced by the full texts

| change | forced by |
|---|---|
| `effect: caught_without_control`; `comparator` optional only then | Tamaki 1977 has no unbaited control |
| electrophysiology method `SSR`; per-response `notes` | Priesner 1986 receptor-cell recordings; Kovalev 1988 EAG on GC fractions |
| measurement `spread` (sd or se) | Francke 2004 SPME 13 ± 3 %; James 2001 98.2 ± 0.4 % |
| response units `mean_catch_per_trap`, `total_catch` | trap tables throughout |
| context `rearing: field_collected_reared` | most insects were collected as larvae or pupae and emerged in the laboratory |

New CI fixtures keep two rules from regressing: a taxon cannot carry a
species-level `pheromone` list, and a compound cannot carry a `role`.

### Taxon × layer matrix

Priesner 1986 gives field attractants for *S. formicaeformis* (E2:E3 100:100)
and *S. andrenaeformis* (10:100), both previously `not_found`; their rows
are now `field_attractant_only`, with one behavioural record each.

## 2026-10-23 (1) — first records, from abstracts

Superseded by the entry above; kept for history. Abstract-based records
drove the first schema changes (sampling context, effect size, author
statement vs Atlas notes, `unresolved`, compound ids without roles).

# Curation log

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

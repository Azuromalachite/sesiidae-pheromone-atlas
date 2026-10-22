# Adversarial review 2 — *Sesiidae Pheromone Atlas* concept, revision 2

Artifact: `sesiidae_pheromone_atlas_concept_r2.md` (1,710 lines; +485 / −132 against revision 1). Prior review: `atlas-concept-review-1.md`. Reviewed 2026-10-23.
Labels: `[V]` verbatim in the artifact or the espmap repo · `[M]` measured · `[L]` checked against a retrieved source · `[I]` inferred · `[U]` not verified.

**Independence warning.** The same model wrote review 1, revision 2 and this review. Errors that came from review 1 into the revision are the least likely to be caught here. Three were (R1–R3 below), and there may be more. A fresh reviewer that has not read either review would be a real check; this one is not.

Revision 2 is a real improvement. All nine findings were acted on, and every one is measurable in the text. Three of them were acted on with a prescription that was wrong in review 1. One fix introduced a rule that rejects the revision's own central example.

---

## Retractions (review 1 was wrong)

### R1 — F3's statistic was the wrong test, and the revision copied it into §26

Review 1 argued that espmap could not resolve neighbouring sites on a C18 chain because "the conformer range at a single site reaches 6.5 kcal/mol … larger than most neighbour-to-neighbour differences" [V, review 1 F3]. Revision 2 put that argument in §26 and told the Atlas to report site differences "with their conformer and partition-rule spreads" [V].

That compares an unpaired range with a mean difference. Conformational effects are shared by neighbouring sites, so the test that matters is the **per-conformer paired difference**. Recomputed from the same 10 conformers in `bench/site_partition.jsonl` [M]:

| pair (biochemical numbering, Z3,Z13-18:OAc) | mean diff, nearest-nucleus | paired SD | same sign | mean diff, radius-scaled | same sign |
|---|---|---|---|---|---|
| C2–C3 (sp³–sp²) | 7.05 | 2.85 | 10/10 | 7.92 | 10/10 |
| C4–C5 (sp²–allylic sp³) | −4.45 | 1.87 | 10/10 | −5.66 | 10/10 |
| C12–C13 (allylic–sp²) | 4.76 | 0.89 | 10/10 | 5.92 | 10/10 |
| C14–C15 | −4.94 | 1.02 | 10/10 | −6.21 | 10/10 |
| C5–C6 (allylic–next CH₂) | 1.62 | 1.54 | 8/10 | 1.64 | 8/10 |
| C15–C16 | 1.82 | 1.59 | 9/10 | 1.53 | 10/10 |
| C1–C2 | −1.07 | 2.64 | 6/10 | −0.06 | 6/10 |
| C10–C11 | −0.68 | 2.53 | 6/10 | −0.52 | 6/10 |
| C16–C17 | −0.61 | 1.68 | 6/10 | −0.18 | 6/10 |

At n = 10, a two-sided sign test needs 9/10 for p < 0.05 (9/10: p = 0.021; 8/10: p = 0.109) [M]. The conformers are MMFF-selected rather than random, so these are descriptive [I].

What survives: plain CH₂ neighbours are **not** resolved (5–6/10). What falls: sp²/sp³ contrasts are resolved in every conformer under both rules, and allylic-vs-next-CH₂ mostly is. Review 1 understated espmap by quoting the wrong spread. On the thioester model, where C2 is α to a carbonyl, the Δ2-vs-Δ3 contrast may well be resolvable [I]. That is what the calibration run should find out rather than assume.

**Correction to §26.** Report each site contrast as the per-conformer paired difference: mean, paired SD and sign consistency, under both partition rules. "Not resolved" means sign-inconsistent under the stated test, not "inside the single-site range". Replace the sentence quoting 6.5 kcal/mol.
**Validation.** The thioester calibration run reports this table for C2–C3, C3–C4 and C2–C4.

### R2 — F2 sent the protein layer to an archived platform

Review 1 cited `rapid.ensembl.org`, and revision 2 made "Ensembl Rapid Release (versioned, §15a)" the gene-model source in §15, §15a and the §21 tool table [V]. Ensembl froze Rapid Release in November 2024 and announced its archiving in September 2025. New genome data goes only to the new Ensembl platform (beta.ensembl.org), which becomes the main site from summer 2026. Ensembl 116 is the final release on the old platforms [L].

The diagnosis (no NCBI annotation, so protein identity must include an annotation release) still holds. The named source and its identifier scheme do not. I could not establish how the new platform identifies an annotation release or whether Sesiidae stable IDs carry over [U].

**Correction.** In §15 replace `source: Ensembl Rapid Release` with the platform and annotation identifier actually served today, and record the archived Rapid Release IDs as a cross-reference if they persist. Add this as a column in the §4.3 matrix.
**Validation.** For *S. tipuliformis*, fetch one desaturase gene by ID from the current platform and confirm the ID, annotation version and protein sequence are stable across two retrievals.

### R3 — F5's isomerase was described in the wrong shape, and the predictions drawn from it are underived

Revision 2 §18 Route C3 says Δ3,Δ2-enoyl-CoA isomerase interconverts E2 and E3. It then concludes that "C3 predicts that E3 tracks E2 and stays a minor partner of it" and that "none of them explains Z3 without a further step" [V].

The enzyme's catalogued reactions are (3Z)-enoyl-CoA → (2E)-enoyl-CoA **and** (3E)-enoyl-CoA → (2E)-enoyl-CoA, with the 3Z isomers turned over about ten times faster (EC 5.3.3.8; Rhea 23716/23717) [L]. So:

- the enzyme handles **both** Δ3 geometries, and Z3 is its preferred substrate. "None explains Z3" is wrong as stated;
- its written direction **consumes** Δ3 to make E2. An ECI in the gland is as plausibly a sink for Δ3 products as a source of them [I];
- I found no equilibrium constant [U], so "E3 stays a minor partner" has no basis.

**Correction.** Rewrite C3 as a reversible isomerisation between E2 and either E3 or Z3, direction and equilibrium unknown, citing Rhea 23716/23717. Keep it as `status: hypothetical` for Sesiidae, with the reaction established elsewhere. Delete the two predictions.
**Validation.** §18 states no prediction that needs the equilibrium position until a source for it is cited.

### R4 — review 1 credited the atom-map identity chain too broadly

Review 1's "What it got right" said a map number "really does follow one carbon from acyl-CoA to alcohol to acetate". That is true for reduction, oxidation and acetylation. It is false for elongation and chain shortening, which are the core of Routes B, C1 and C2. Revision 2 repeated the overstatement and wrote a rule on it (N1).

---

## Disposition audit, F1–F9

| finding | r1 → r2 term counts [M] | verdict |
|---|---|---|
| F1 taxa | `myopaeformis` 0 → 5; `GCA_9` 0 → 15 | **implemented.** Matrix with 11 species and the snapshot date; East Asian species moved to pheromone-only. 8 of 11 matrix rows are still "to check", which is correct for a step-1 artefact |
| F2 proteins | `Ensembl` 0 → 6; `annot.` 1 → 5; `XP_` 1 → 1 (explanatory only) | **implemented in shape, wrong source** (R2) |
| F3 espmap subject | `computational_model` 0 → 9 | **implemented**, but the statistic is wrong (R1) |
| F4 maps | `101` 0 → 5; `headgroups.yaml` 0 → 4; `espmap --check` 0 → 3 | **implemented.** `--check` exits 1 on BLOCK and returns before the basis-size guard, so it works as a CI step [V, `esp_map.py` L2415–2433]. The map rule is the gate's own (`atom_map_findings`, L405) [V] |
| F5 routes | `CoA` 0 → 27; `ACOX` 0 → 4; `labelling` 0 → 7 | **implemented**; isomerase shape wrong (R3); one discriminating test does not discriminate (N6) |
| F6 observations | `observation_type` 0 → 3; `detected:` 0 → 5; `role: ` 2 → 1 (in prose) | **implemented**; detection carries no method (N5) |
| F7 encodings | `generated` 2 → 10; `shorthand` 1 → 8 | **implemented**; the regeneration gate is fragile to RDKit versions (N7) |
| F8 precursors | `precursor.z13_18_coa` 0 → 2; leftover `_acyl` 3, all enzyme-family names, not compounds [M] | **implemented**, and its new reaction rule is wrong (N1) |
| F9 order | sprint reordered; gate-fails step added | **implemented**, but the CI ties v0.1 to espmap (N4) |

The companion-document chemistry used in §4.3 checks out against the primary abstracts [L]. *S. bicingulata* E3 : Z3 is about 4 : 6 (Yang, Kim & Lee 2011), and its gland also holds E2,Z13-18:OAc as a minor component, which the r2 table omits. *S. tenuis* has Z3,Z13-18:OH alone, the acetate was "not detected" and adding it "strongly inhibited attraction" (Yang, Lee & Park 2012). *N. pernix* has the E3 and Z3 alcohols at 9 : 1 (Naka et al. 2006). The tested-negative example the revision leans on is real.

---

## New findings

### N1 — HIGH. The chain-map conservation rule rejects the revision's own elongation reaction

§16 adds: "Every reaction's mapped SMILES must conserve the chain maps 1…n from substrate to product" [V]. Two paragraphs earlier it introduces `spa.rxn.0008`, Z11-16:CoA → E2,Z13-18:CoA [V]. In elongation the old C1 becomes C3 and Δ11 becomes Δ13 [I]. So the product's maps 1–18 correspond to the substrate's maps −1…16, and no labelling of the two can satisfy the rule. The same holds for every chain-shortening step (C2) [I]. §10a ("Chain maps are identical across the whole series") and §11 ("the chain maps are the same along the whole pathway") state the same thing as fact [V]. The rule can only decline on exactly the reactions Routes B, C1 and C2 depend on, so it is not a validator.

The underlying problem: a map number here is a **position** (biochemical numbering), and position is not identity across chain-length changes.

**Correction.** Keep chain maps positional within a compound (espmap and the shorthand need that). Give each reaction an explicit `atom_correspondence` (e.g. `{substrate: 1, product: 3}` … or an offset rule `product = substrate + 2` for one elongation cycle, with the two new carbons named). The validator checks that this correspondence maps the conserved carbons and that bond changes occur only where the reaction class allows. Fix the §10a and §11 sentences to say "across reduction, oxidation and acetylation".
**Validation.** `spa.rxn.0008` and one chain-shortening reaction pass the validator; a reaction whose correspondence moves Δ11 to Δ12 fails.

### N2 — HIGH. §26 prescribes the wrong uncertainty for every future site claim

This is R1 in the artifact: §26's comparison rule, its 6.5 kcal/mol sentence and the §0 F3 row ("site contrasts are reported against the per-site budget") all encode the unpaired test [V]. Left in, it would have the Atlas label resolved contrasts "not resolved", including the sp²/sp³ contrasts that resolve 10/10 [M].

**Correction and validation.** As R1.

### N3 — HIGH. The protein layer names an archived source

This is R2 in the artifact: §15 (`source: Ensembl Rapid Release`), §15a and the §21 tool row [V]. Because the matrix in sprint step 1 needs an annotation column, it affects tomorrow's work.

**Correction and validation.** As R2.

### N4 — MEDIUM. The F9 fix ties Atlas v0.1 to espmap before espmap's contract is frozen

Sprint step 5 makes `espmap --check` part of CI for every compound [V]. espmap's runtime dependencies include PySCF, scikit-image, matplotlib and cmcrameri [V, `pyproject.toml`]. Its own CLAUDE.md says API stability does not matter [V], and the gate is under active change before P3 [I, open PRs #39, #42]. Review 1's case for starting the Atlas now rested on v0.1 *not* depending on espmap [V, review 1 "Pricing the plan"]. The fix undid that.

**Correction.** Implement the heavy-atom map rule (all-or-none, unique, no mapped H) in the Atlas validator itself; it is 20 lines in espmap [V, `atom_map_findings`]. Run `espmap --check` as a separate job, pinned to an espmap commit, and keep it non-blocking until `espmap.sites/1` is frozen at P3.
**Validation.** Atlas CI passes with espmap not installed. The pinned espmap job agrees with the Atlas rule on the three synthetic bad-map fixtures.

### N5 — MEDIUM. A detection has no method unless it also has a number

In §13, a `detected: false` component carries `method:` at component level, a `detected: true` component carries methods only inside `measurements`, and the E3 example has `detected: true` with `measurements: []`, so no method at all [V]. Invariant 5 ("every measurement names its method") is satisfied vacuously, because detection is not modelled as a measurement. `detection_limit` appears once, with no unit [M].

**Correction.** Put `method` on the component for every `detected` value, and let `measurements` override it. Give `detection_limit` a value and a unit.
**Validation.** The schema rejects `detected: true` without a method.

### N6 — MEDIUM. One "discriminating experiment" cannot discriminate

§37's row "E3 from E2" offers "E2 : E3 ratio constant across individuals" as evidence for C3 [V]. A single bifunctional desaturase making both products would give the same constant ratio [I]. The pass condition is also the competitor's signature. The labelled-precursor half of the row is a real test; with R3 it must run both ways (labelled E2 → E3 or Z3, and labelled Δ3 → E2).

**Correction.** Delete the ratio clause, or move it to a "consistent with, not discriminating" column.
**Validation.** Each §37 row names an outcome that at least one competing route forbids.

### N7 — LOW. The regeneration gate will fail on a toolkit upgrade

§10/§12 commit generated canonical SMILES, InChI and InChIKey, and CI fails on any difference [V]. RDKit canonical SMILES can change between releases [I]; standard InChI is more stable [I].

**Correction.** Record the generator name and version in the `generated` block. On a version change, regenerate in one dedicated commit; between versions, the diff gate applies only at the same version.

### N8 — LOW. Integrity of §0 and loose ends

- §0 says F12 is "partly done" [V]. No `0.2.0` remains anywhere in r2 [M], so it is done.
- §0's F3 row describes the wrong statistic (N2).
- `electrophysiology` is declared as a type, with "compound, response" as its fields, and has no example or schema detail [V].
- The species-level caveat ("no pheromone record comes from the sequenced population") is stated for *S. tipuliformis* only [V]. *S. myopaeformis*'s pheromone was identified in an introduced British Columbia population [L]; the same caveat applies.

---

## Summary

| # | severity | finding | correction |
|---|---|---|---|
| R1/N2 | HIGH | unpaired spread used for site contrasts; paired data resolve sp²/sp³ 10/10 | report paired differences + sign consistency |
| N1 | HIGH | chain-map conservation rule rejects elongation and shortening | per-reaction `atom_correspondence` |
| R2/N3 | HIGH | gene models sourced from archived Ensembl Rapid Release | re-specify source and ID scheme against the current platform |
| R3 | MEDIUM | ECI acts on 3Z and 3E, toward 2E; two predictions underived | rewrite C3 as reversible, unknown equilibrium; cite Rhea |
| N4 | MEDIUM | CI depends on espmap pre-P3 | own map rule; pinned, non-blocking espmap job |
| N5 | MEDIUM | detection carries no method | method per component; unit on detection limit |
| N6 | MEDIUM | constant ratio is not discriminating | drop or reclassify |
| N7 | LOW | regeneration diff breaks on RDKit upgrade | record generator version |
| N8 | LOW | §0 integrity; empty electrophysiology type; caveat on one species only | small edits |
| R4 | — | review 1's identity-chain credit was too broad | absorbed into N1 |

## What it got right

- **The head-group map table is consistent through the terminal-group chemistry.** Walking it [M]: the acid's carbonyl O (101) is the thioester's carbonyl O (101), which FAR turns into the aldehyde or alcohol O (101), which acetylation keeps as the ester O (101). One fixed table, numbered so that the reactions that do *not* change chain length conserve every map. That is why N1 is about elongation only.
- **The tested negative is modelled as data.** `detected: false` with a method, separated from `not_tested`, and illustrated with a case that checks out against the primary abstract (*S. tenuis*) [L]. This is the change most likely to matter for genome-mining claims later.
- **Route C1 links the E2 bond to Route B's elongation step.** The elongation cycle does pass through E2,Z13-18:CoA when it extends Z11-16 [I], and the revision makes that a testable reaction record rather than a remark. N1 is about the validator rule, not about this hypothesis.
- **The companion chemistry was flagged "not curated" before it was checked.** It turned out correct for all three species [L], but the revision did not assume that.
- **`espmap --check` is the right CI hook technically**: exit 1 on BLOCK, before any basis-size or SCF work [V]. N4 is about when to make it blocking, not whether to use it.

## The one thing to do first

Find out what the current Ensembl platform serves for *S. tipuliformis* and *S. apiformis*: the annotation identifier, version and gene IDs (R2/N3). The matrix in sprint step 1 needs that column, and the protein schema in §15a cannot be written without it. N1 is the most severe finding, but it bites in v0.2, when reaction records arrive. Fix its two prose sentences now and the rule then.

## Sources

- Ensembl Rapid Release freeze (Nov 2024): <https://lists.ensembl.org/pipermail/dev_ensembl.org/2024-November/009157.html>
- Ensembl Rapid Release archiving notice (Sep 2025): <https://lists.ensembl.org/pipermail/dev_ensembl.org/2025-September/009206.html>
- Ensembl 116, final release on current platforms: <https://www.ebi.ac.uk/about/news/updates-from-data-resources/ensembl-116-release/>
- EC 5.3.3.8, Δ3,Δ2-enoyl-CoA isomerase: <https://www.enzyme-database.org/query.php?ec=5.3.3.8>; Rhea: <https://www.rhea-db.org/rhea/23716>, <https://www.rhea-db.org/rhea/23717>
- *S. tenuis* (Yang, Lee & Park 2012), *S. bicingulata* (Yang, Kim & Lee 2011), *N. pernix* (Naka et al. 2006), abstracts via NCBI E-utilities: <https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=22976589,21399964,16495670&rettype=abstract&retmode=text>
- *S. myopaeformis* (Judd et al. 2011): <https://bioone.org/journals/the-canadian-entomologist/volume-143/issue-3/n11-002/3Z-13Z-Octadecadienyl-Acetate--Sex-Pheromone-of-the-Apple/10.4039/n11-002.full>
- espmap: `esp_map.py` (`atom_map_findings` L405–439; `--check` path L2415–2433), `pyproject.toml`, `bench/site_partition.jsonl` (c18 rows), `CLAUDE.md`
- Paired-difference script: `c18paired.py` in the same scratchpad folder

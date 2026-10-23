# espmap-sesiidae-001: prospective analysis plan

**Status: frozen 2026-10-23.** This file and
`case-bundle.yaml` are committed, and that commit's SHA and timestamp are
recorded here **before** any conformer of this study is computed. That makes
it a prospective analysis plan. It is not a preregistration, because it is
not registered with an external registry (e.g. OSF). Changes after the
freeze go in "Deviations" below, with the date and the reason. They never
edit the frozen text.

Its home is the Sesiidae Pheromone Atlas (`analyses/espmap-sesiidae-001/`).
Arrowfield links to it.

## Disclosure: what we have already seen

This plan is written **after** a pilot on four of the five molecules.
The pilot used B3LYP/def2-SVP + RI, gas phase, 0.26 bohr, 100 ETKDG
conformers with seed 0xC0FFEE, and K chosen by radius-of-gyration spread
(Arrowfield `sesiidae-pilot.md`, `pilot/`). At K = 10 it found:

| contrast | pilot result |
| --- | --- |
| B, E/Z at C3 | no site resolved; C3-H +1.3, C4-H +1.0, inside ranges of 2.5–6.2 |
| C, C=C position | resolved at **C4-H only**: +4.20 against ranges of 4.07 and 2.03, partition sensitivity 1.43; C2-H and C3-H inside their ranges |
| A, head group (OH vs OAc) | no site mean resolved; global V_max −27.5 (the alcohol's O–H) |

At K = 5 there were also chance separations at C11-H, which disappeared at
K = 10. The homework's expected answers came from this pilot. **This study is
therefore a confirmatory replication of hypotheses the pilot generated,** on a
new conformer draw, under a decision rule fixed here before the new data
exist.

## 1. The biological question (context only)

Several Sesiidae taxa treat these closely related compounds differently: the
same compound increases, decreases or does not change catches depending on
species, population and blend. The Atlas records this as observations, with
assay context and significance. The question this study can address is
narrow:

> Does the **free molecule's** electrostatic potential distinguish the
> molecules of each contrast at the sites where they differ chemically, by
> more than the molecule's own conformational variation?

It does not address how a receptor, an enzyme or a population distinguishes
them.

## 2. Contrasts and sites (frozen in `case-bundle.yaml`)

| contrast | molecules | primary sites | secondary |
| --- | --- | --- | --- |
| B, stereo | Z3,Z13-18:OAc vs E3,Z13-18:OAc | C3-H, C4-H | head O; global V_min, V_max |
| C, position | E3,Z13-18:OAc vs E2,Z13-18:OAc | C2-H, C3-H, C4-H | head O; global V_min, V_max |
| A, head group | Z3,Z13-18:OH vs :OAc (plus the :Al teaching control) | global V_max, global V_min | head O (the O atom alone, the same atoms in each molecule) |

- A site is a carbon with its hydrogens (`Cn-H`), by atom map; the C18
  chain is mapped C1–C18 in every molecule.
- **Only primary sites are tested.** All other chain sites, C1-H to C18-H,
  are reported as exploratory and never interpreted. That is the pilot's
  C11 lesson: a lone hit at a site nobody predicted is at chance level.
- In A, a site mean of the head-group O is not compared across OH and OAc,
  because the site's atoms differ (O+H vs ester O). A's head-group statements
  rest on the global extrema and on the O atom alone.

## 3. Protocol (fixed)

- **espmap:** the tag current at the freeze (v0.2.1 unless a later release
  exists then), recorded with each record's `code`. If espmap v0.3's
  `--ensemble` is released before the run, it is used with the parameters
  below. Otherwise the pilot's selection code is used, with the same
  parameters.
- **Method:** B3LYP/def2-SVP + RI, gas phase, grid spacing 0.26 bohr, one
  `analysis_key` throughout. This is the pilot's setting, so the replication
  is like for like.
- **Conformers:** 100 ETKDGv3 + MMFF94s embeddings per molecule with
  **seed 20261024**, a new draw, not the pilot's 0xC0FFEE. Then K = **20**:
  the lowest-MMFF conformer plus 19 spread across the radius-of-gyration
  range. Folded members (an intramolecular contact or surface genus > 0)
  are **kept**. Low-energy minima the pilot also found will recur; they are
  not excluded, because excluding them would bias the sample. "New" means a
  new random draw, not disjoint shapes.
- **Exclusions:** a member is excluded only if its surface fails espmap's
  integrity checks or its record's validity is false. Every exclusion is
  listed with its Rg and folded flag. If more than 2 of 20 are excluded for
  a molecule, or any excluded member is folded, that contrast is reported as
  **not evaluable**, not as resolved or unresolved.
- **Partition:** nearest-nucleus is the primary rule; radius-scaled is
  computed alongside.

## 4. Decision rule (fixed)

For each primary site of a contrast, with ensembles X and Y (20 members
each, minus exclusions) and Δ = mean(Y) − mean(X) under the primary rule:

**Resolved** if and only if all three hold:
1. **Beyond conformational variation:** the two ensembles' site-mean ranges
   (min–max over members) do not overlap. For 20 vs 20 values from one
   distribution, chance non-overlap is 2/C(40,20) ≈ 1.5 × 10⁻¹¹ per site.
2. **Beyond the partition:** |Δ| exceeds the partition sensitivity. That is
   the larger, over the two molecules, of |mean(nearest) − mean(radius-scaled)|
   at that site.
3. **Same sign under both rules:** Δ has the same sign under the
   radius-scaled rule.

Also reported for every primary site, as a secondary result:
- Δ with a bootstrap 95 % interval (10,000 resamples of members within each
  ensemble, seed 20261024).
- **Different on average** if that interval excludes 0 and conditions 2–3
  hold, while condition 1 fails.

That is a weaker statement than "resolved", and is never reported as one.

For global extrema (A, and the secondary rows), the same rule applies to
the members' V_min and V_max.

## 5. What each outcome permits us to say

| outcome at a site | we may say | we may not say |
| --- | --- | --- |
| resolved | under this protocol, the free molecule's ESP at this site distinguishes the two compounds by more than their conformational variation | that this difference explains any biological difference |
| different on average | the ensemble means differ, but some single conformations of the two molecules are electrostatically indistinguishable at this site | that the site is resolved |
| unresolved | under this protocol, free-molecule ESP does not resolve the two compounds at this site | that the compounds are electrostatically identical, or that electrostatics plays no biological role |
| not evaluable | nothing about this contrast | anything |

**No outcome of this study means any of these:**
- that receptor or enzyme discrimination is explained;
- that biological activity is predicted;
- that a site is where a desaturase or other enzyme acts;
- anything about solvated, bound or membrane-embedded states;
- anything about taxa or compounds outside the case bundle.

**Expected, from the pilot, and stated so that a failure is visible:**
- **B:** unresolved at C3-H and C4-H.
- **C:** resolved at C4-H; unresolved at C2-H and C3-H. The pilot's margin
  at C4-H was small (+4.20 against a range of 4.07), and ranges grew with K,
  so C4-H may fail condition 1 at K = 20. If it does, the result is: **the
  pilot's C4-H call did not replicate under the stricter test.** It is
  reported as such, with "different on average" if that holds.
- **A:** global V_max resolved (OH above OAc).

## 6. Sensitivity analyses (pre-specified, reported whatever they show)

- **Population:** the decision rule applied to extended members only.
  Reported beside the all-member result, never instead of it.
- **Basis:** def2-TZVP single points on 5 members per molecule (the
  lowest-MMFF member and 4 Rg-spread ones) for contrast C's primary sites.
  This runs only if WSL time allows. If it is not run, that is stated.
  Basis moves C18 V_max by +1.5 to +2.8 kcal/mol (espmap README), the same
  order as these differences.
- **Solvent:** not studied. Gas phase is the stated baseline.

## 7. Reporting

- All primary sites and all contrasts are reported, whatever the outcome.
- Records go to the Atlas's `computed/espmap/<slug>/<protocol>/` and NPZ
  files to its release assets, each with its sha256.
- The report cites this file's frozen commit SHA, and the espmap tag, Atlas
  commit and Arrowfield commit used.

## Freeze

- Approved by: the user, 2026-10-23, as drafted: K = 20, seed 20261024,
  def2-SVP gas, and the range non-overlap + partition + sign rule. Freeze
  once the Atlas has filled the motivating observations.
- Commit SHA: 7e3465859bc2b8950078238f0bffb0ea6b4dd512 (Atlas)
- Date: 2026-10-23

## Deviations

_(none yet)_

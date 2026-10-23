# espmap-sesiidae-001: results

Prospective analysis plan: [Atlas analyses/espmap-sesiidae-001 at 7e34658](https://github.com/Azuromalachite/sesiidae-pheromone-atlas/blob/7e3465859bc2b8950078238f0bffb0ea6b4dd512/analyses/espmap-sesiidae-001/analysis-plan.md), frozen 2026-10-23 before any member was computed. A confirmatory replication of the pilot, on a new conformer draw (seed 20261024, K = 20), under the plan's section 4 rule. Not a preregistration.

Potential in kcal/mol, B3LYP/def2-SVP + RI, gas phase, 0.26 bohr, nearest-nucleus partition primary. Every verdict below is under espmap-sesiidae-001/range_partition_sign_v1, the frozen plan's rule, never espmap.compare/1's generic resolved_under. Δ = mean(Y) − mean(X). Conditions: 1 ranges disjoint, 2 |Δ| beyond the partition sensitivity (section 4 definition; the pilot-style number in brackets, never used), 3 same sign under the radius-scaled rule. Global extrema involve no partition, so 2 and 3 hold trivially.

**How to read the statistics.** The 20 members per molecule are a designed coverage set (the lowest-MMFF conformer plus 19 spread over Rg, of 100 embeddings), not independent random draws from an equilibrium population. Range non-overlap is therefore used as a deterministic robustness criterion over this prespecified, shape-diverse ensemble. The combinatorial probability the frozen plan quotes (2/C(40,20)) assumes exchangeable random observations, and is not read here as a p-value or a false-positive probability. The bootstrap interval resamples the selected conformer set: it describes that set, it is not a population-level confidence interval, and 'different on average' stays descriptive.

## Members and exclusions

| molecule | members | folded | excluded | evaluable |
| --- | --- | --- | --- | --- |
| Z3,Z13-18:OAc | 20 | 9 | none | yes |
| E3,Z13-18:OAc | 20 | 3 | none | yes |
| E2,Z13-18:OAc | 20 | 6 | none | yes |
| Z3,Z13-18:OH | 20 | 4 | none | yes |
| Z3,Z13-18:Al (teaching control) | 20 | 3 | none | yes |

## B_stereo: X = Z3,Z13-18:OAc, Y = E3,Z13-18:OAc (n = 20 / 20)

### Primary

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| C3-H | **different on average** | +2.31 | -2.78…5.02 / 1.04…6.60 | 0.93 (2.01) | +1.20…+3.42 | ✗✓✓ |
| C4-H | **unresolved** | -0.04 | 0.27…5.08 / 0.22…5.54 | 0.69 (1.11) | -0.84…+0.74 | ✗✗✓ |

- **C3-H: different on average.** We may say: the ensemble means differ, but some single conformations of the two molecules are electrostatically indistinguishable at this site. We may not say: that the site is resolved. The plan expected **unresolved**: not as expected in category: observed 'different on average', which is also not resolved. The pilot predicted no resolution and none occurred; the means do differ (descriptive).
- **C4-H: unresolved.** We may say: under this protocol, free-molecule ESP does not resolve the two compounds at this site. We may not say: that the compounds are electrostatically identical, or that electrostatics plays no biological role. The plan expected **unresolved**: as expected.

### Secondary

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| head O | **different on average** | -0.81 | -13.80…-8.02 / -12.98…-9.81 | 0.18 (0.73) | -1.50…-0.12 | ✗✓✓ |
| global V_min | **different on average** | -0.39 | -41.02…-38.61 / -41.20…-38.88 | 0.00 (0.00) | -0.76…-0.02 | ✗✓✓ |
| global V_max | **unresolved** | -0.31 | 19.57…20.98 / 19.34…22.09 | 0.00 (0.00) | -0.62…+0.04 | ✗✓✓ |

### Sensitivity: extended members only (n = 11 / 17), beside, never instead of, the result above

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| C3-H | **different on average** | +1.90 | -0.60…4.16 / 1.04…6.60 | 0.86 (2.01) | +0.64…+3.15 | ✗✓✓ |
| C4-H | **unresolved** | -0.60 | 1.45…5.08 / 0.22…5.54 | 0.68 (1.11) | -1.57…+0.33 | ✗✗✓ |

Exploratory, never interpreted (plan section 2): other chain sites meeting the rule: none.

## C_position: X = E3,Z13-18:OAc, Y = E2,Z13-18:OAc (n = 20 / 20)

### Primary

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| C2-H | **different on average** | -2.50 | 3.30…10.06 / -0.67…6.89 | 0.94 (1.21) | -3.89…-1.17 | ✗✓✓ |
| C3-H | **unresolved** | -0.35 | 1.04…6.60 / -1.79…8.80 | 0.93 (2.01) | -1.95…+1.27 | ✗✗✗ |
| C4-H | **resolved** | +5.22 | 0.22…5.54 / 6.66…9.53 | 0.69 (1.11) | +4.57…+5.88 | ✓✓✓ |

- **C2-H: different on average.** We may say: the ensemble means differ, but some single conformations of the two molecules are electrostatically indistinguishable at this site. We may not say: that the site is resolved. The plan expected **unresolved**: not as expected in category: observed 'different on average', which is also not resolved. The pilot predicted no resolution and none occurred; the means do differ (descriptive).
- **C3-H: unresolved.** We may say: under this protocol, free-molecule ESP does not resolve the two compounds at this site. We may not say: that the compounds are electrostatically identical, or that electrostatics plays no biological role. The plan expected **unresolved**: as expected.
- **C4-H: resolved.** We may say: under this protocol, the free molecule's ESP at this site distinguishes the two compounds by more than their conformational variation. We may not say: that this difference explains any biological difference. The plan expected **resolved**: as expected.

### Secondary

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| head O | **unresolved** | +0.77 | -12.98…-9.81 / -11.95…-6.66 | 0.80 (1.40) | -0.09…+1.69 | ✗✗✓ |
| global V_min | **unresolved** | -0.20 | -41.20…-38.88 / -41.36…-39.82 | 0.00 (0.00) | -0.51…+0.10 | ✗✓✓ |
| global V_max | **unresolved** | -0.29 | 19.34…22.09 / 18.60…21.57 | 0.00 (0.00) | -0.78…+0.21 | ✗✓✓ |

### Sensitivity: extended members only (n = 17 / 14), beside, never instead of, the result above

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| C2-H | **different on average** | -2.57 | 3.30…9.27 / -0.67…6.89 | 0.93 (1.21) | -4.10…-1.09 | ✗✓✓ |
| C3-H | **unresolved** | -0.02 | 1.04…6.60 / -1.79…7.74 | 0.86 (2.01) | -1.85…+1.86 | ✗✗✗ |
| C4-H | **resolved** | +5.21 | 0.22…5.54 / 6.66…9.53 | 0.67 (1.11) | +4.46…+5.97 | ✓✓✓ |

Exploratory, never interpreted (plan section 2): other chain sites meeting the rule: none.

## A_headgroup: X = Z3,Z13-18:OAc, Y = Z3,Z13-18:OH (n = 20 / 20)

### Primary

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| global V_max | **resolved** | +26.50 | 19.57…20.98 / 34.00…51.68 | 0.00 (0.00) | +24.02…+28.80 | ✓✓✓ |
| global V_min | **different on average** | -1.22 | -41.02…-38.61 / -42.62…-38.78 | 0.00 (0.00) | -1.74…-0.67 | ✗✓✓ |

- **global V_max: resolved.** We may say: under this protocol, the free molecule's ESP at this site distinguishes the two compounds by more than their conformational variation. We may not say: that this difference explains any biological difference. The plan expected **resolved**: as expected.
- **global V_min: different on average.** We may say: the ensemble means differ, but some single conformations of the two molecules are electrostatically indistinguishable at this site. We may not say: that the site is resolved.

### Secondary

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| head O | **resolved** | -20.74 | -13.80…-8.02 / -31.95…-29.03 | 5.97 (6.73) | -21.41…-20.03 | ✓✓✓ |

### Sensitivity: extended members only (n = 11 / 16), beside, never instead of, the result above

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| global V_max | **resolved** | +25.96 | 19.57…20.95 / 34.00…51.68 | 0.00 (0.00) | +22.99…+28.66 | ✓✓✓ |
| global V_min | **different on average** | -1.15 | -40.93…-39.79 / -42.62…-39.09 | 0.00 (0.00) | -1.67…-0.61 | ✗✓✓ |

Exploratory, never interpreted (plan section 2): other chain sites meeting the rule: none.

## The teaching control (descriptive chemistry, no biological claim)

| site | outcome | Δ (Y − X) | range X / Y | partition (pilot-style) | bootstrap interval (selected set) | 1 2 3 |
| --- | --- | --- | --- | --- | --- | --- |
| Al vs OAc global V_max | **resolved** | +5.76 | 19.57…20.98 / 24.89…26.85 | 0.00 (0.00) | +5.47…+6.05 | ✓✓✓ |
| Al vs OAc global V_min | **different on average** | +0.83 | -41.02…-38.61 / -40.02…-38.38 | 0.00 (0.00) | +0.48…+1.17 | ✗✓✓ |
| Al vs OAc head O | **resolved** | -16.50 | -13.80…-8.02 / -26.79…-25.81 | 1.56 (1.87) | -17.06…-15.90 | ✓✓✓ |
| Al vs OH global V_max | **resolved** | -20.74 | 34.00…51.68 / 24.89…26.85 | 0.00 (0.00) | -23.01…-18.24 | ✓✓✓ |
| Al vs OH global V_min | **different on average** | +2.05 | -42.62…-38.78 / -40.02…-38.38 | 0.00 (0.00) | +1.52…+2.55 | ✗✓✓ |
| Al vs OH head O | **unresolved** | +4.24 | -31.95…-29.03 / -26.79…-25.81 | 5.97 (6.73) | +3.81…+4.65 | ✓✗✗ |

## Sensitivity analyses not run

- Basis (def2-TZVP single points, plan section 6): **not run**.
- Solvent: not studied; gas phase is the stated baseline.

## Deviations from the plan

No deviation from the decision rule, its thresholds, the protocol, the sites or the molecules.

One dated clarification is recorded under the plan's "Deviations" (Atlas 30c4a11, approved by the user on 2026-10-24): the 20 members are a designed coverage set, range non-overlap is a deterministic robustness criterion, the plan's 2/C(40,20) is not a p-value, and the bootstrap interval describes the selected set. This report reads its numbers that way (see "How to read the statistics" above).

Implementation choices the plan left open are recorded, before the analysis ran, in `execution-manifest.json`: espmap v0.2.1 (v0.3 `--ensemble` was not released), the pilot's selection code, and the folded rule (contact by espmap master 5175515's provisional parameters, 5 bonds and Bondi + 0.5 A, OR genus > 0). espmap has since measured its contact threshold at 6 bonds (§8.2). The flags here keep the recorded rule; they were not recomputed after the results were seen.

The analysis and report scripts were tested during the run on partial data (from 1 to about 30 of 100 members, printed "PARTIAL: a test of the script, not a result"), and on the pilot's K = 10 data, which they reproduce. Nothing in the protocol, the rule or the folded definition changed after those tests; the partition-definition choice was made by the user before any member of this study was analysed.

## No outcome of this study means

- that receptor or enzyme discrimination is explained;
- that biological activity is predicted;
- that a site is where a desaturase or other enzyme acts;
- anything about solvated, bound or membrane-embedded states;
- anything about taxa or compounds outside the case bundle;

## Provenance

- espmap v0.2.1 (41a989d), each member an espmap.record/1 with its sha256 in the Atlas index.
- Atlas commit (records): base 30c4a11; records added by the PR that adds this file; plan frozen at 7e34658.
- Arrowfield commit: 63f10c1 (main); control records in Arrowfield PR #6.
- Folded: an intramolecular contact (espmap master 5175515's provisional rule) or surface genus > 0.
- Partition sensitivity: section 4's definition decides; on 2026-10-23, before any analysis, the user chose to keep it and to report the pilot's max-member number beside it. The plan's pilot table quotes that pilot-style number (1.43 at C4-H); section 4's gives 0.77 on the same data.

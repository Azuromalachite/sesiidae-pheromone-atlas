# Curation log

## 2026-10-23 — first real records, from abstracts

Records: 4 taxa, 4 references, 9 compounds, 17 observations, for the three
cases chosen to stress the schema (*S. apiformis* method-dependent ratios,
*S. tipuliformis* population-dependent E3 effect, the *S. tenuis*
tested-negative acetate), plus one *S. scoliaeformis* record from the same
paper.

**Every record was curated from an abstract, and says so** (`read: abstract`
on the reference, `source_location` on each observation). None of the four
full texts could be reached: the three Springer papers are not open access
(Unpaywall), and the De Gruyter page for Mozūraitis et al. 2006 sits behind a
human-verification check. Each observation lists what the full text must
supply in `evidence.unresolved`.

All nine compounds' generated InChIKeys resolve in PubChem to the expected
names.

### Schema changes the real records forced

| change | forced by |
|---|---|
| `context.mating_status`, `behavioural_state`, `sampling_unit`, `n_individuals`, `habitat` | "virgin females" (Mozūraitis 2006); "pooled gland extracts" vs "single calling females" (Francke 2004); "black currant field" |
| `behavioural_response.response` (measure, unit, treatment and comparator values, qualifier), `significance`, `dose` | "over seven times" (Mozūraitis 2006); close-range approaches 20 % → 65 % (Szöcs 1990); "did not differ significantly" |
| `evidence.source_location`, `author_statement`, `unresolved` | keeping the authors' words apart from the Atlas's reading, and stating what is missing |
| compound ids `cmpd.*`, class `natural_product` (was `pheromone.*`, `pheromone_component`) | 18:OH occurs in *S. tipuliformis* glands with no known role; a "pheromone" id or class would have assigned it one (invariant 17) |

Changes the records did **not** force, so not made: no `role` field, no
aggregate score, no new observation type.

### What each full text must supply

| reference | needed |
|---|---|
| Mozūraitis et al. 2006 | number of females, pooled or individual extracts, insect origin; ratio spread; which isomers were looked for and not found (notably Z3,Z13-18:OAc); trap doses, replicates, statistics; the comparator in the *S. scoliaeformis* test |
| Szöcs et al. 1990 | doses (two abstract copies disagree: 10–100 vs 10–1000 µg), sites and years, catches and statistics; the base lure in the Z13-18:OAc tests; the dose-dependent Z3,Z13-18:OAc inhibition and the five-component landing blend, both left uncurated |
| Francke et al. 2004 | **which compound is 2 and which 3 in the pooled ratio, and 1 and 7 in the SPME ratio** (curated in the abstract's listing order, alcohol then aldehyde); numbers of females; trap doses and comparators |
| Yang et al. 2012 | analytical method and detection limit for the undetected acetate; ratios, doses, catches; confirmation that the trials were in Korea; the earlier study that reported attraction to the acetate |

### Interpretations the Atlas made, and marked

- *S. tenuis*: "competitive with live virgin females" read as `effect: no_effect` against that comparator.
- *S. scoliaeformis*: "attraction antagonist" read as `decreased` against E2,Z13-18:OAc without E3,Z13-18:OAc.
- *S. apiformis*: ratio order taken from the abstract's listing order.

Each is stated in the record's `notes` or `unresolved`.

# Evidence classes

What the records show about a taxon and a compound, in a fixed vocabulary.
`scripts/build_evidence.py` derives the classes from record fields into
`derived/tables/evidence_classes.tsv`, one row per taxon, compound and
class, with the observations behind each row. **No class is an author's
claim or the curator's opinion, and none is netted out.** A compound that
raised catches in one study and lowered them in another gets both rows.

The classes keep apart what the literature keeps confusing:
- a field attractant is not a female pheromone;
- a gland constituent is not an emitted compound;
- "not detected" is not "not made" (it holds only for the method used);
- an antennal response is not attraction.

## The classes

| class | rule over the records |
|---|---|
| `female_detected_gland` | a `chemical_measurement` of females with material `gland_extract` or `ovipositor_extract` (one material) has the compound `detected: true` |
| `female_detected_emission` | the same with material `effluvium` |
| `female_detected_combined` | the same, where the source reports several materials only together (`result_scope: combined`) |
| `female_not_detected` | `detected: false` in a female `chemical_measurement`, which always carries its method. It is a negative for that method, sample and population only |
| `antennal_active` | an `electrophysiology` response `active` (EAG, GC-EAD or single-sensillum) |
| `antennal_inconsistent` | a response the authors saw in some recordings and not others |
| `antennal_inactive` | a response recorded as `inactive` |
| `attractant_alone` | a field-trapping record: a one-compound lure, a blank comparator (unbaited, solvent, empty or no-dispenser), effect `increased` |
| `attractive_lure_component` | the same with a lure of any size; every compound in that lure gets the row |
| `addition_increased` | a true addition: the treatment lure is the comparator plus this one compound, every shared compound at the same amount, same trap and dispenser; effect `increased` |
| `addition_decreased` | the same, effect `decreased` |
| `addition_no_effect` | the same, effect `no_effect` |
| `female_pheromone_component` | **derived**: in the same taxon, the compound is female-detected (gland, emission or combined) **and** an attractive lure component or an `addition_increased` |

## Columns

| column | meaning |
|---|---|
| `n_observations` | supporting observations |
| `n_significant` | behavioural classes and the derived class: how many supporting behavioural records the source reports as significant. The rest are `not_significant`, `not_tested` or `not_reported`; see the records |
| `n_tentative` | chemistry classes and the derived class: detections whose `identification` is `tentative` |
| `populations` | the populations, or localities, of the supporting records; `not given` when a record names neither |
| `population_match` | derived class only. `yes`: the chemistry and the behaviour share a named population or locality. `no`: both are named, and no name is shared. `unknown`: one side names no place |

## What a row does not say

- **`female_pheromone_component` is the Atlas's join of two lines of
  evidence**, not an identification. Check `population_match`:
  - `no` often means one population named two ways. For *P. tabaniformis*,
    "Kandagash, … European Kazakhstan" and "Kazakh population" are the same
    district.
  - `no` can also mean a real join across populations. That is why the
    column exists; read the records.
- **Replacements and removals are not classed.**
  - A replacement keeps the total dose and lowers the base. It answers a
    different question from an addition (`analyses/added_compound_effects.md`
    separates them).
  - A removal is the same contrast read backwards.
- **Places are free text.** The match is exact on the recorded population,
  or on the locality when no population is given. It is never fuzzy.
- **Absence of a row is not evidence of absence.** Only
  `female_not_detected` rows, and dated search records, assert anything
  about absence.

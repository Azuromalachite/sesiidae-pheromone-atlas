# The v0.2 chemistry gate, specified

`docs/validation.md` names three things that must land before any acyl-CoA
enters the Atlas: validate the head-group table itself, decide a charge and
protonation convention, and enforce tetrahedral stereochemistry where a head
group has stereocentres. This document specifies them.

**This is a specification, not an implementation.** Nothing here is built. No
schema, no record, no `derived/` output and no validator behaviour changes
with this document, and nothing in v0.1 changes.

**It is written ahead of its turn.** `docs/direction-type1-grammar.md` orders
the v0.1.0 gate before this one, and that ordering is unchanged: the human
primary-source verification (`review/spot-check-001`,
`review/case-check-sesiidae-homework-1`) comes first. This document exists so
that the work is specified when its turn comes, and so that the decisions in
it can be argued with before any code depends on them.

## What the gate protects

Every compound today is a neutral straight-chain C10–C18 molecule with a
four-atom head group at most. Acyl-CoA is none of those things: about 48
heavy atoms, several stereocentres, three phosphate groups, and a charge
state that depends on a convention nobody has yet written down. The existing
checks do not fail on it loudly — some of them do not fail on it at all.

| today's behaviour on an acyl-CoA | why it is wrong |
|---|---|
| `CHARGE` refuses any formal charge | correct for pheromones; for acyl-CoA it forces a silent choice of protonation state that no record states |
| tetrahedral centres are never examined | CoA's stereocentres could be unspecified, or wrong, and every check would pass |
| `data/headgroups.yaml` is read with `int()`, `float()` and bare key access (`atlas_validate.py:140`) | a malformed 48-atom entry raises an exception or loads nonsense; neither is a `Finding` |

The third is the one that bites first. A hand-written CoA entry is the
largest piece of untested data anyone will add to this repository, and today
it is the only data file with no gate of its own.

## 1. Validate the head-group table itself

New error code: **`HEADGROUP_TABLE`**, raised against
`data/headgroups.yaml`, checked once at load and before any compound is read.
A table that fails produces findings and no compound checks, because every
compound check reads the table.

`load_headgroups` must stop using bare `int()`, `float()` and `g["..."]` on
curated input. Duplicate YAML keys are already caught upstream
(`YAML_DUPLICATE_KEY`, `strict_load`); everything below is new.

| check | rule |
|---|---|
| token | matches `^[A-Za-z][A-Za-z0-9]*$`, so the shorthand parser can read it back |
| `name` | present, a non-empty string |
| `name` uniqueness | no two tokens share a `name` |
| `atoms` | present, a non-empty mapping |
| atom maps | each key parses as an integer and is `>= 101` (`HEAD_MAP_MIN`); never 1–100, which are chain carbons |
| atom elements | each value is a symbol RDKit's periodic table accepts |
| map 101 | present, and bonded to map 1 — the convention the file's own header states ("the same oxygen keeps map 101 from acid to alcohol to acetate") |
| `bonds` | present, a list of `[a, b, order]` triples |
| bond endpoints | each endpoint is either `1` (chain C1) or a map declared in `atoms`; `a != b` |
| bond orders | in `{1, 2, 3}`. Aromatic and 1.5 are refused: no head group in scope is aromatic, and an unintended 1.5 would otherwise compare equal to nothing |
| duplicate bonds | no unordered pair appears twice |
| chain attachment | every bond with a chain endpoint has that endpoint equal to `1` |
| attachment exists | at least one bond touches map 1 |
| connectivity | the graph over `atoms ∪ {1}` is connected, so the head group is one fragment and not two |

**Attachment is not single-valued.** `COOH` and `SMe` each bond two
head-group atoms to C1, so a rule of "exactly one bond to map 1" would refuse
two entries that are already correct. The rule is that no head-group atom
bonds to a chain carbon *other than* C1 — which is what
`structure_findings` already enforces per compound, now enforced on the
table as well.

## 2. Charge and protonation

**The decision: the table declares the charge, and the gate checks the
structure against the declaration.** Protonation is never inferred and never
silently coerced.

Two new keys per head-group entry:

| key | meaning |
|---|---|
| `net_charge` | integer; the net formal charge of the head group as the table's atoms encode it |
| `protonation` | a short string stating the protonation state the entry represents, and that it is a storage convention rather than a claim about the species in solution |

The `CHARGE` check becomes: the molecule's net formal charge equals the head
group's declared `net_charge` (an unbranched hydrocarbon chain contributes
zero), and no atom carries radical electrons. The per-atom refusal of any
formal charge is replaced by a net-charge comparison, so a zwitterion that
nets to the declared value is admitted — which is the only way a CoA entry
can ever be written honestly.

For all five existing entries `net_charge` is `0`, so **behaviour on every
current record is unchanged**: no compound record is edited, no InChIKey
moves, no `generated` block goes stale. The implementation commit fills the
two keys in for the five existing entries, and that data edit must be shown
to change nothing, by `python atlas_validate.py data` passing before and
after with no `--write-generated`.

**What the Atlas should store for acyl-CoA, and why it is a decision and not
a fact.** The neutral, fully protonated form keeps identity clean: the
InChIKey is stable, the molecule is comparable to the neutral pheromones, and
`computed/` — which computes free-molecule electrostatic potentials — would
otherwise be handed a molecule whose ESP is dominated by its net charge and
not comparable to anything else in the Atlas. The physiological species at
pH 7 is not that molecule. Storing the neutral form and *saying so* in
`protonation` is therefore the recommendation here; storing the charged form
is equally admissible under this gate as long as `net_charge` says so. What
the gate forbids is the third option: picking one silently.

**A reaction substrate is not an espmap target.** Nothing in this gate
implies that an acyl-CoA record gets a computed ensemble. `computed/` holds
the four Atlas compounds it already holds.

## 3. Tetrahedral stereochemistry

Today `STEREO_UNSPECIFIED` fires only for a chain double bond with no E/Z
(`atlas_validate.py:413`). Tetrahedral centres are never examined, because no
v0.1 compound has one: an unbranched saturated chain with a ≤4-atom head
group cannot carry a stereocentre. CoA carries several.

One new key per entry:

| key | meaning |
|---|---|
| `stereocentres` | list of head-group maps that must carry an assigned tetrahedral configuration; `[]` for all five existing entries |

The check, run after the existing head-group match:

- enumerate potential tetrahedral centres, assigned and unassigned alike.
  On the pinned RDKit (2026.9.1) `Chem.FindPotentialStereo` is the current
  API and reports each element's atom and whether it is specified;
  `Chem.FindMolChiralCenters(..., includeUnassigned=True)` is the older
  spelling. The implementation picks one against the pin and a fixture —
  this document does not pretend to have run either;
- the set of **assigned** centres among head-group maps must equal the
  declared `stereocentres`;
- an unassigned centre anywhere raises `STEREO_UNSPECIFIED`, naming the map;
- an assigned centre that is not declared raises `HEADGROUP_MISMATCH`: the
  structure has a stereocentre the table does not know about.

Declaring the set, rather than only requiring assignment, catches the case
that silent coercion would otherwise hide — a CoA drawn with one centre
missing still has every other check pass, and `[]` versus a 3-element list is
the difference between "no stereochemistry here" and "three centres, all
specified".

The chain is covered by the same rule at no cost: a chain stereocentre would
be undeclared and therefore refused.

## What does not change

- **The shorthand grammar.** `SHORTHAND` already accepts `[A-Za-z]+` as the
  head token (`atlas_validate.py:55`), so `Z11-16:CoA` parses today. No
  regex change, no schema change.
- **`schemas/compound.schema.json`.** A curator still writes
  `names.shorthand` and `mapped_smiles`, and nothing else.
- **The frozen v0.1 shape.** Nothing here touches `schemas/`;
  `data/headgroups.yaml` is data, and `scripts/schema_shape.py` does not read
  it. The three new keys are additive to a file with no schema — which is
  precisely the hole check 1 closes.
- **espmap's gate rule.** Every heavy atom mapped, maps unique, no map on a
  hydrogen, unchanged. For CoA that means roughly 48 head-group maps from
  101, all written by hand, which is the strongest argument for check 1
  existing before the entry does.

## The gate must be seen to fail

`tests/fixtures/bad/` holds one directory per case with an `EXPECT` listing
exactly the codes it must produce. These are the cases this gate adds. The
table cases need a fixture head-group file, since the real
`data/headgroups.yaml` must stay valid.

| case | expects |
|---|---|
| head-group map below 101 | `HEADGROUP_TABLE` |
| head-group map that is not an integer | `HEADGROUP_TABLE` |
| element symbol that is not an element | `HEADGROUP_TABLE` |
| bond endpoint not declared in `atoms` | `HEADGROUP_TABLE` |
| bond order 1.5 | `HEADGROUP_TABLE` |
| the same bond pair twice | `HEADGROUP_TABLE` |
| head-group atom bonded to a chain carbon other than C1 | `HEADGROUP_TABLE` |
| head group in two disconnected pieces | `HEADGROUP_TABLE` |
| map 101 absent, or present and not bonded to C1 | `HEADGROUP_TABLE` |
| two tokens sharing a `name` | `HEADGROUP_TABLE` |
| `net_charge` absent | `HEADGROUP_TABLE` |
| structure net charge differs from the declared `net_charge` | `CHARGE` |
| radical electrons present | `CHARGE` |
| declared stereocentre left unassigned in the structure | `STEREO_UNSPECIFIED` |
| assigned stereocentre not declared in the table | `HEADGROUP_MISMATCH` |

A fixture that starts failing for a second reason no longer proves the first,
so each `EXPECT` is the exact set — the existing rule, unchanged.

## Order of work, when its turn comes

1. Check 1 alone, with its fixtures, against the five existing entries. No
   new head group yet. This is where a bug is cheap.
2. Checks 2 and 3, with the three new keys filled in for the five existing
   entries at values that preserve today's behaviour. Prove it by validating
   before and after without `--write-generated`.
3. Only then write the CoA entry, with its own fixture, and only then the
   first acyl-CoA compound record.

Step 3 is the one `docs/validation.md` means by "the first acyl-CoA must not
discover it".

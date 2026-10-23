# espmap-sesiidae-001

A prospective analysis of whether the free molecule's electrostatic
potential distinguishes the molecules of three Sesiidae contrasts. Frozen
at 7e34658 before any conformer was computed.

| file | what it is |
| --- | --- |
| `case-bundle.yaml` | the molecules and contrasts (frozen) |
| `analysis-plan.md` | question, protocol, decision rule, interpretation (frozen; changes only under "Deviations") |
| `motivating.py` | selects the motivating observations (rule `direct_contrast_v1`) |
| `execution-manifest.json` | which implementation the plan allowed was used: espmap v0.2.1 (41a989d), library versions, seed, selection rule, folded definition |
| `results.md` | the report: every primary site, its outcome under `espmap-sesiidae-001/range_partition_sign_v1`, what each outcome permits saying, the expectations, sensitivity, provenance |
| `results.json` | the same numbers, per contrast, site and population (all members; extended only) |
| `selection/<slug>/` | per molecule: the 20 chosen conformers (`selection.json`), site definitions (`sites.json`), per-member facts with the folded call (`members.json`), and the run log (`run_log.jsonl`, every exit code) |
| `scripts/` | the code that ran: `s001_run.py` (select, compute), `s001_build.py` (Atlas index), `s001_analyse.py` (decision rule), `s001_report.py` (report) |

The member records are under `computed/espmap/<slug>/b3lyp_def2-svp_gas_espmap-v0.2.1/`
for the four Atlas compounds. Their NPZ surfaces are release assets, each
with its sha256 in `ensemble.json`. The teaching control
(Z3,Z13-18:Al) is not an Atlas compound: its records live in Arrowfield,
and its selection and run log are here with the rest of the study.

**Seed fields in the member records.** Each record's `settings.seed`
(12648430, which is 0xC0FFEE) and `settings.nconfs` (20) are espmap's
defaults, unused here. Every member's geometry was read from its SDF
(`--file`), so espmap generated no conformer. They are neither the pilot's
seed nor this study's. The study's seed is 20261024, used at selection
(`execution-manifest.json`, `selection/<slug>/selection.json`).

`s001_build.py` imports espmap master's `intramolecular_contacts` from a
copy of `esp_map.py` at commit 5175515, for the folded call (contact OR
surface genus > 0, as the plan defines it). That rule is provisional in
espmap. The members themselves were computed by v0.2.1 alone.

# analyses/

Analyses of the Atlas that read **only** `derived/tables/`, the tidy
relational tables, never the YAML records. Each one is a test of whether the
tables are enough for a real question. Each script writes a committed Markdown
report; `--check` (run by the tests) fails if the report is stale.

| script | question |
|---|---|
| `added_compound_effects.py` | What does adding one compound to a lure do, across species, populations and trials? Separates true additions from replacements at constant dose, and sets the *S. tenuis* gland chemistry from Japan and Korea beside the lure results |

Reports interpret nothing beyond the records: significance is as the source
reported it, and `not_tested` contrasts carry only the direction of the raw
means.

## Frozen studies

A study directory holds a prospective plan, frozen by commit before any of
its computation runs. Its frozen files are never edited after the freeze;
changes go in the plan's "Deviations" section, with a date and a reason.

| directory | what it is |
|---|---|
| `espmap-sesiidae-001/` | Free-molecule ESP contrasts of four Atlas acetates and an alcohol, with a teaching control: `case-bundle.yaml` (molecules, contrasts, the motivating observations) and `analysis-plan.md` (protocol and decision rule), both frozen 2026-10-23. The observations were selected at Atlas e8ca212 by `motivating.py` (rule `direct_contrast_v1`). Run with Arrowfield; computed results go to `computed/espmap/` |

Unlike the scripts above, `motivating.py` reads the records through the
validator's loader, not `derived/tables/`. The selection rule was frozen in
those terms, so it must stay reproducible at the pin.

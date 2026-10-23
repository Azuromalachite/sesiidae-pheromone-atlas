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

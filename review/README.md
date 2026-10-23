# Human spot-checks

Every Atlas record was extracted from its paper by Claude and re-read
against the PDF by other Claude reviewers. Those reviews found many defects,
but they are model output checking model output. **Until a spot-check here is
complete, no record has been checked by a person against its source.** That
is the state of the Atlas, and the README says so.

A spot-check is a person reading the papers for a sample of records. The
practice follows PAZy (Feuerriegel et al. 2026, *Nucleic Acids Res*,
[doi:10.1093/nar/gkag1026](https://doi.org/10.1093/nar/gkag1026)): it
verifies LLM-assisted extraction "through both random sampling and
hand-picked selections of publications deemed possibly difficult".

| directory | drawn | sample | status |
|---|---|---|---|
| `spot-check-001/` | 2026-10-23, seed 20261023 | 24 random observations of 524 plus 14 hard cases | not started |

## How to do one

1. **Open the sheet.** Open `spot-check-NNN/sheet.md`, and the papers it
   names. Each entry gives:
   - the citation with a DOI link;
   - *where in the paper* the record was read (a table, figure or section;
     the records do not hold page numbers);
   - the record's values, one row per field.
2. **Check each row against the paper.**
3. **Record a verdict.** In `results.yaml`, give every record a `verdict`:
   - `ok`: every row matches;
   - `error`: list the wrong rows in `wrong_rows`, with what the paper says,
     in `notes`;
   - `unclear`: the paper does not settle it; say why in `notes`.

   Fill in `checker` (your name) and `date` too.
4. **Check what you see.** Record what the paper shows, not what you think
   the curator meant. A record whose notes explain a judgement call is still
   checked against the paper.
5. **Summarise.** Run `python scripts/spot_check.py summarise
   review/spot-check-NNN`. The tests check that `results.yaml` stays
   well-formed.

## What the result licenses

- **The random part** gives an error rate over all observations, with a
  Wilson 95 % interval. With 24 records it is coarse: no errors at all still
  allows a true rate up to about 14 %.
- **The hard part** is reported on its own. It says whether the judgement
  calls hold, and it is never pooled into the rate.
- **Errors found** are fixed in the records, and each fix is noted in
  `docs/curation-log.md`. The spot-check files themselves are never edited
  after they are filled. A later spot-check is a new directory with a new
  seed.

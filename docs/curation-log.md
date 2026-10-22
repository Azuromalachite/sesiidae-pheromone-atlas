# Curation log

## 2026-10-23 (2) — full texts

All records are now curated from full texts (`read: full_text`), ten papers:
Szöcs et al. 1985, 1990; Priesner et al. 1986; Kovalev et al. 1988;
Tamaki et al. 1977; James et al. 2001; Francke et al. 2004; Suckling et
al. 2005; Mozūraitis et al. 2006; Yang et al. 2012.

Records: 6 taxa, 10 references, 10 compounds, 40 observations
(gland composition, behavioural response, electrophysiology). All ten
compounds' InChIKeys resolve in PubChem to the expected names.

Szöcs, Henderson & McNeil 1998 (Canada) is **not** curated: the file
supplied as that paper is a different article in the same issue (Trudel et
al., white pine weevil, *Can. Entomol.* 130:201–214).

### These papers are observations, not reactions

They establish that a compound is present in a gland, emitted, antennally
active, attractive, synergistic, antagonistic, or not detected, and that
ratios depend on assay and population. They do not establish any
precursor → product conversion. Two compounds in the same gland (for
example E2,Z13-18:OH and E2,Z13-18:OAc) are not evidence that one is made
from the other; where authors suggest it (Mozūraitis et al. 2006: "could be
intermediates"), that is an author hypothesis. No reaction records were
made from this corpus. The reaction grammar needs a different corpus:
isotope-labelled precursors, enzyme assays, heterologous expression,
characterised desaturases, elongases, FARs, ACOX/ECI.

### Disagreements the records hold rather than resolve

| question | one side | other side |
|---|---|---|
| Does E3,Z13-18:OAc synergise in New Zealand? | 4.6× and significant, 1985–86 (Szöcs 1990) | 481 vs 490, equivalent, 2003–04 (Suckling 2005) |
| Does it inhibit in Tasmania? | decreased, significant, 1986 (Szöcs 1990) | not significant 1987 (Szöcs 1990); no blend effect, P = 0.83, 2003–04 (Suckling 2005) |
| Does Z13-18:OAc add anything for *S. tipuliformis*? | significant increase at 5:1, 1984 (Szöcs 1985) | no significant effect 1984–87 (Szöcs 1990); no receptor cell for it (Priesner 1986) |
| Is Z3,Z13-18:OAc attractive to *S. tenuis*? | 51 males, Japan 1976, no control (Tamaki 1977) | 0 alone and absent from glands, Korea 2011 (Yang 2012) |
| Is Z3,Z13-18:OH alone the *S. apiformis* pheromone? | "identified as a sex pheromone" (Kovalev 1988) | not attractive alone; needs E2,Z13-18:Al (Francke 2004) |
| Does 200 µg E2,Z13-18:OH reduce *S. apiformis* catch? | "significantly reduced" (Francke 2004, text) | shares a letter with the binary blend (Francke 2004, Table 3) |

The *S. tenuis* contrast differs in population and in dose, dispenser and
trap, so it does not by itself show a population difference.

### Internal inconsistencies and citation drift found in the sources

- Mozūraitis 2006: 12 calling females in Methods, 6 in Results and Fig. 1.
- Szöcs 1985 reports E2,Z13-18:OAc : Z13-18:OAc = **93:7**, with no E3. It is cited as 97:3 (Mozūraitis 2006) and as a 100:3 E2:E3 blend (James 2001). Records cite the primary paper only.
- James 2001: the abstract's 100:3 is the lure ratio; the measured blend is 98.2 : 1.8 (n = 3).
- Szöcs 1990: dose range 10–1000 µg in the paper, 10–100 in an AGRIS abstract copy.
- Szöcs 1990 counted repeated checks of a trap as repetitions, so its significance letters are weaker evidence than they look; recorded in the notes.

### Schema changes forced by the full texts

| change | forced by |
|---|---|
| `effect: caught_without_control`; `comparator` optional only then | Tamaki 1977 has no unbaited control |
| electrophysiology method `SSR`; per-response `notes` | Priesner 1986 receptor-cell recordings; Kovalev 1988 EAG on GC fractions |
| measurement `spread` (sd or se) | Francke 2004 SPME 13 ± 3 %; James 2001 98.2 ± 0.4 % |
| response units `mean_catch_per_trap`, `total_catch` | trap tables throughout |
| context `rearing: field_collected_reared` | most insects were collected as larvae or pupae and emerged in the laboratory |

New CI fixtures keep two rules from regressing: a taxon cannot carry a
species-level `pheromone` list, and a compound cannot carry a `role`.

### Taxon × layer matrix

Priesner 1986 gives field attractants for *S. formicaeformis* (E2:E3 100:100)
and *S. andrenaeformis* (10:100), both previously `not_found`; their rows
are now `field_attractant_only`, with one behavioural record each.

## 2026-10-23 (1) — first records, from abstracts

Superseded by the entry above; kept for history. Abstract-based records
drove the first schema changes (sampling context, effect size, author
statement vs Atlas notes, `unresolved`, compound ids without roles).

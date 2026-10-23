# What v0.1 is complete for

Written 2026-10-23. This is the scope statement that a v0.1.0 tag, and later a
DOI, will claim (`docs/releases-and-occurrences.md`). The tag is cut when every
target row below is curated or recorded as unobtainable.

## The statement

> Sesiidae Pheromone Atlas v0.1 is a validated, observation-level corpus of
> the clearwing moths (Sesiidae) whose female sex pheromone has been
> identified from glands or emissions in primary literature. It covers what
> females produce or release, how male antennae respond, and how males
> respond to synthetic lures, each kept as a separate record. Every record
> keeps its experimental context (sample material, lure purity, trap,
> dispenser, trial) and the name its source used. The corpus is linked to
> atom-mapped compound structures and to every Sesiidae genome assembly
> available on 2026-10-23.

**v0.1 is not:**
- a census of all Sesiidae attractants;
- a record of biosynthesis (no reaction records; v0.2);
- a record of receptors;
- a record of occurrences.

## Coverage

**Target.** Species with a female-produced pheromone identified in primary
literature.

**Where the list comes from.** No complete census was reachable. Ando's
online list of moth pheromones, cited by Naka et al. 2013, returned 404 on
2026-10-23; the Wayback Machine refused the request (rate limit); the
Pherobase sits behind a bot check. So the target list is built from the
identifications that the curated papers themselves cite:
- Naka 2013, Discussion;
- Yang 2011, Introduction and Discussion;
- Naka 2008.

Those papers count about 20 identified sesiid pheromones. The list below has
16. **The gap is stated, not hidden.** A dated census search record is added
when a complete list is read, and only then can the scope say "all".

### Curated (9)

| species | female chemistry from |
|---|---|
| *S. tipuliformis* | Szöcs 1985; James 2001; Mozūraitis 2006 |
| *Sesia apiformis* | Kovalev 1988; Francke 2004 |
| *S. myopaeformis* | Judd 2011 |
| *S. vespiformis* | Levi-Zada 2011 |
| *S. scoliaeformis* | Mozūraitis & Būda 2013 |
| *S. bicingulata* | Yang 2011 |
| *S. tenuis* | Yang 2012 (Korea); Naka 2013 (Japan) |
| *Nokona pernix* | Naka 2006 |
| *S. hector* | Naka 2008 |

### To curate (7)

| species | reference | DOI |
|---|---|---|
| *Synanthedon exitiosa* and *S. pictipes* | Tumlinson JH, Yonce CE, Doolittle RE, Heath RR, Gentry CR, Mitchell ER (1974) Sex pheromones and reproductive isolation of the lesser peachtree borer and the peachtree borer. *Science* 185:614–616 | [10.1126/science.185.4151.614](https://doi.org/10.1126/science.185.4151.614) |
| *Synanthedon scitula* | Zhang A, Leskey TC, Bergh JC, Walgenbach JF (2005) Sex pheromone of the dogwood borer, *Synanthedon scitula*. *J Chem Ecol* 31:2463–2479 | [10.1007/s10886-005-7113-0](https://doi.org/10.1007/s10886-005-7113-0) |
| *Melittia cucurbitae* | Klun JA, Schwarz M, Leonhardt BA, Cantelo WW (1990) Sex pheromone of the female squash vine borer. *J Entomol Sci* 25:64–72 | [10.18474/0749-8004-25.1.64](https://doi.org/10.18474/0749-8004-25.1.64) |
| *Glossosphecia romanovi* | Naka H, Mochizuki M, Nakada K, Do ND, Yamauchi T, Arita Y, Ando T (2010) Female sex pheromone of *Glossosphecia romanovi*: identification and field attraction. *Biosci Biotechnol Biochem* 74:1943–1946 | [10.1271/bbb.100232](https://doi.org/10.1271/bbb.100232) |
| *Synanthedon haitangvora* | Yang CY, Kim J, Kang TJ, Jeon HY (2009) Identification and field bioassays of the sex pheromone of *Synanthedon haitangvora*. *J Chem Ecol* 35:1197–1201 | [10.1007/s10886-009-9694-5](https://doi.org/10.1007/s10886-009-9694-5) |
| *Vitacea polistiformis* | Snow WJ, Schwarz M, Klun JA (1987) The attraction of the grape root borer to (E,Z)-2,13-octadecadienyl acetate and the effects of related isomers on attraction. *J Entomol Sci* 22:371–374. **Attraction only**; the female identification it rests on (Schwarz et al. 1983, *Tetrahedron Lett*) is still to be found | [10.18474/0749-8004-22.4.371](https://doi.org/10.18474/0749-8004-22.4.371) |

The Tumlinson paper covers two species, which is why the 7 target rows add
up to 16 species with the 9 curated.

### Also wanted, outside the target definition

- **Szöcs, Henderson & McNeil 1998**, *S. tipuliformis* in Canada
  ([10.4039/ent130231-2](https://doi.org/10.4039/ent130231-2)). An attractant
  study that completes the geographic contrast. Deferred: no access.

### Genome layer: complete

All 11 Sesiidae species with a nuclear assembly in NCBI on 2026-10-23 have a
genome record (`spa.search.sesiidae.genome.2026_10_23`).

## What "complete for" licenses

A user of v0.1 may ask, across the target species:
- what females make;
- what antennae detect;
- what lure contrasts were tested, under which conditions;
- where two studies disagree;
- which species have genomes.

A user may not read a missing species as "no pheromone", or a missing
compound as "not produced". Absence is asserted only by `detected: false`
with a method, or by a dated search.

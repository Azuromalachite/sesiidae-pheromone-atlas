# From lure to language

*How clearwing-moth pheromone research found a shared chemical vocabulary,
then learned that its meaning depends on blend, context and the kind of
evidence used to read it.*

This is the opening chapter of the Atlas: what the curated literature says,
in order, with each claim tied to its source. `obs.` identifiers are curated
records in `data/observations/`. Papers marked **(not yet curated)** have
been read in full, but no records are made from them yet.

## 1. A small vocabulary, found with synthetic lures (1970s)

Early sesiid work screened synthetic C18 dienyl acetates in the field.
Tamaki et al. 1977 caught 51 Japanese *Synanthedon tenuis* males on
Z3,Z13-18:OAc alone, and almost none once 5 % E3,Z13-18:OAc was added
(`spa.obs.tenuis.1977.tamaki.*`). The trial ran no unbaited control, with two
traps per lure and no statistics.

That is one kind of observation: **males come to a synthetic compound.** It
says nothing about what females make.

## 2. Reading the female (1980s)

Gland analyses started to say what females produce:

- *S. tipuliformis*: Szöcs et al. 1985 found E2,Z13-18:OAc and Z13-18:OAc at
  93:7 in pooled extracts of 19 Hungarian females, and no E3 isomer
  (`spa.obs.tipuliformis.1985.szocs.gland`). Z13-18:OAc gave a significant
  increase in one trial (`…trap_z13oac`), not in later ones.
- *Sesia apiformis*: Kovalev et al. 1988 isolated Z3,Z13-18:OH, EAG-active,
  from 370 abdominal tips and called it the sex pheromone
  (`spa.obs.apiformis.1988.kovalev.*`). They followed only the alcohol fraction,
  so the aldehyde found in 2004 was never looked for.

**Production** and **attraction** are now two separate observations. They do
not always agree.

## 3. Small amounts, and ratios, change the message (1986–1990)

- Priesner et al. 1986: a few percent of E3,Z13-18:OAc raised *S.
  tipuliformis* catches, while equal amounts caught none. The same two
  compounds attracted *S. formicaeformis* best at 100:100 and *S.
  andrenaeformis* at 10:100 (`spa.obs.*.1986.priesner.*`). Receptor cells for E2
  and E3, and none for Z13-18:OAc, were reported without data
  (`spa.obs.tipuliformis.1986.priesner.ssr`).
- Szöcs et al. 1990: in Hungary, E2,Z13-18:OAc alone brought 20.6 % of
  arriving males to within 2 cm of the bait, and with E3 65.6 %
  (`spa.obs.tipuliformis.1990.szocs.approach.hungary`). The minor component
  works at close range, not only on trap catch.
- Mozūraitis et al. 2006: E3,Z13-18:OAc, which synergises for *S.
  tipuliformis*, suppressed *S. scoliaeformis* males entirely at their own
  site (`spa.obs.scoliaeformis.2006.mozuraitis.trap_e3.forest_edge`). One minor
  compound attracts one species and repels another.
- *S. bicingulata*: the female gland holds E3:Z3,Z13-18:OAc at 58:100, about
  4:6 (`spa.obs.bicingulata.2011.yang.gland`). Males came most to a 4:6
  lure, but 3:7 and 2:8 were not significantly worse
  (`…yang.trap_ratio_3_7`), while 7:3 and 1:9 were (`…trap_ratio_7_3`,
  `…trap_ratio_1_9`). Kwon et al. 2021 also found 4:6 best, in four
  site-years at three sites (`spa.obs.bicingulata.2021.kwon.trap_ratio_*`),
  with a sharper response than Yang's: 2:8 was significantly worse at all
  three 2018 sites. They attribute Yang's flatter response to
  isomer-contaminated lures and say Yang gave no isomeric information.
  Yang's Methods do give it: isomeric purity above 99 %, stated, not shown.
  Kwon's own lures were 94 % (E3) and 83 % (Z3) pure by GC-MS peak area,
  without saying what the impurities are, and they state the lures held no
  isomers. Their trace shows minor peaks 0.07–0.37 min after each main peak,
  on a column where E3 and Z3 themselves eluted only 0.035 min apart, so
  isomers among them are not excluded (Atlas reading of their Fig. 4).
  Their headline optimum, 4.3:5.7, is not a tested lure: it is the nominal
  4:6 lure corrected for those two purities. Neither paper shows that its
  lures are free of geometric isomers. **Lure purity is a hidden variable
  in any attraction record, a purity must say which kind it is, and a claim
  about another paper's lures has to be checked against that paper.**
  Records carry `purity` with its `kind` and `basis`.
- Kwon et al. 2021 also show a ratio's effect is not fixed: at Gongju, 1:9
  caught 8.5 males per trap in spring 2017 (green traps) and none in autumn
  2018 (yellow traps), and almost none at the other two 2018 sites. Season
  and trap colour changed together, so the records hold the contrast
  without explaining it.
- *Nokona pernix*: Naka et al. 2006 found two EAG-active alcohols, E3- and
  Z3,Z13-18:OH, at about 9:1 (12.3 and 1.4 ng per female), and no acetate
  (`spa.obs.pernix.2006.naka.gland`, `…gcead`). The 9:1 lure caught 49.7 males
  per trap against 0.5 for E3 alone; 5:5 and 99:1 caught almost nothing
  (`…trap_z3_added`, `…trap_ratio_5_5`, `…trap_ratio_99_1`). Unnatural 13E
  isomers were then swapped in. In place of the minor component, a 13E
  isomer still caught some males (not significantly fewer). In place of the
  major component, it caught none; but those lures had no E3,Z13-18:OH at
  all, so they show the natural major is required, not how much its
  geometry matters
  (`…trap_e3e13_for_e3`, `…trap_z3e13_for_e3`).

Specificity is not one species, one molecule. It is encoded in which isomer,
how much of it, and what else is present.

## 4. Geography: a finding that did not hold

Szöcs et al. 1990 found E3 synergistic in Hungary and New Zealand and
inhibitory in Tasmania (`spa.obs.tipuliformis.1990.szocs.trap_e3.*`). It was
read as a Tasmanian pheromone strain.

It did not hold up:

- the same group's 1987 Tasmanian repeat was not significant
  (`…tasmania_1987`);
- Suckling et al. 2005 found equivalent catches with and without E3 in **both**
  Tasmania (P = 0.83) and New Zealand (481 vs 490), and rejected the strain
  (`spa.obs.tipuliformis.2005.suckling.trap_e3.*`);
- in 2025, Anderbrant et al. **(not yet curated)** summarised the minor E3
  component as one that increased catches "in some studies, but not in
  others".

*S. tenuis* gives a second geographic contrast. The acetate attracted
Japanese males in 1976, but in 2011 it was absent from Korean glands (below
about 100 pg), caught nothing on its own, and blocked attraction to the real
pheromone, Z3,Z13-18:OH (`spa.obs.tenuis.2012.yang.*`). The two studies also
differ in dose, dispenser and trap, so this is a contrast between records,
not yet evidence of a population difference.

The Atlas keeps all of these and decides none of them.

## 5. Evidence layers come apart (2000s)

- James et al. 2001 joined female volatiles, SPME, ovipositor extracts,
  GC-MS and GC-EAD in one Washington population: E2 : E3 about 98.2 : 1.8
  (n = 3), with both compounds antennally active
  (`spa.obs.tipuliformis.2001.james.*`). **Production, emission and perception**
  appear in a single study. The abstract's "100:3" is the lure ratio, not the
  measurement.
- Francke et al. 2004 solved *S. apiformis*: Z3,Z13-18:OH plus
  E2,Z13-18:Al, the first aldehyde in a sesiid pheromone. Neither attracts
  alone; the blend does. Pooled extracts give 2:3, single calling females by
  SPME 13:87 (`spa.obs.apiformis.2004.francke.*`). **The ratio is a property of
  the measurement, not only of the moth.** In this case it did not matter
  behaviourally: lures from 30:300 to 300:300 µg all worked.
- Mozūraitis et al. 2006 found six compounds in *S. tipuliformis* glands, but
  the full six-component lure was no better than the E2/E3 pair. **The gland
  holds more than the behaviourally sufficient blend.** Yang et al. 2011 found
  the same for *S. bicingulata*: four minor compounds, three of them
  identified only tentatively, and none of them changed catches on the 4:6
  pair, alone or all together (`spa.obs.bicingulata.2011.yang.trap_{z13oac,e2z13oac,e3oh,z3oh}_added`,
  `…trap_complete`). Whether the extra compounds are biosynthetic
  intermediates is the authors' hypothesis, not an observation.

## 6. The signal is more than chemistry

- **Colour.** Yellow or green traps out-caught other colours for *S.
  tipuliformis* (Suckling et al. 2005). For *S. bicingulata*, yellow buckets
  beat green ones in spring at two sites and in autumn at two of three, and
  beat white ones at one site of three
  (`spa.obs.bicingulata.2021.kwon.trap_yellow_vs_*`). Across sites, catch
  rose with the trap's b* (yellowness) value (Kwon et al. 2021). They cite
  the same result for *S. myopaeformis*.
- **Lure and trap.** Catch rose with lure loading (Suckling et al. 2005).
  Green buckets out-caught white deltas, 13.2 vs 7.6 per trap
  (`…kwon.trap_bucket_vs_delta.exp2_2017.chuncheon`), but design and colour
  changed together, so that record cannot separate them.

Behaviour is chemistry × release × trap × light × population. An attraction
record without its trap, dose and lure purity is incomplete.

## 7. From signal to management, and what trap shutdown does not show

Mating disruption shuts traps down:

- *S. tipuliformis* in New Zealand, over 99 % (Suckling et al. 2005);
- *S. tenuis* in Korea with Z3,Z13-18:OH alone, 98.8 % (Chiluwal et al.
  2020, **not yet curated**);
- *S. tipuliformis* in Fennoscandia, up to 100 % (Anderbrant et al. 2025).

Anderbrant et al. 2025 then found no effect on damage or on the next year's
catches after one season. Chiluwal et al. note that female mating success was
not measured, and Suckling et al. tie New Zealand control failures to high
population density. **A trap catch is a measurement of male behaviour at a
trap, not of mating or population size.** That is one more layer the records
must keep separate.

## 8. Traps as instruments

Once a lure works, it becomes a tool for other questions. In Korea, *S.
bicingulata* trap series now show flight starting about a month earlier and
lasting about a month longer than in older reports. Mitochondrial haplotypes
differ among nearby sites, suggesting limited dispersal (W.J. Kim et al.
2025, **not yet curated**). A degree-day model predicts still earlier flight
under climate change (H.-J. Yang et al. 2025, **not yet curated**). Both
depend on the lure being specific, which section 3 shows is itself a
measurement with conditions attached.

## 9. Perception, first data (2025)

Cattaneo & Walker 2025 **(not yet curated)** made the first deorphanisation
of sesiid odorant receptors. They took eight *S. myopaeformis* paralogues
from two pheromone-receptor subgroups, chosen by orthology to the codling
moth, out of a male antennal transcriptome, and expressed them in Drosophila
neurons:

- SmyoOR3.4 responds to pear ester and to (Z)-6-undecenal at about 1 ng;
- SmyoOR22.4 is broadly tuned to apple volatiles and also responds to the
  species' pheromone, Z3,Z13-18:OAc, along with codling-moth pheromones;
- no behavioural tests were done, and no receptor specific to the species'
  own pheromone was found among those tested.

So the receptor layer now exists for one sesiid. It already shows that
"pheromone-clade" receptors can be tuned to host-plant odours, and that the
pheromone is not necessarily read by a dedicated receptor among those
chosen.

## 10. What these papers do not say

None of these papers tests a biosynthetic step. Two compounds in one gland,
an alcohol beside its acetate, are not evidence that one is made from the
other. No study here uses isotope-labelled precursors, enzyme assays or
characterised desaturases, elongases or reductases for a sesiid. The
literature defines **what must be explained**. The next corpus has to say
**how biology makes it**.

## What the Atlas takes from this

| distinction | why the literature forces it |
|---|---|
| attraction ≠ production | *S. tenuis*: an attractant in Japan, absent and antagonistic in Korea |
| one compound ≠ the pheromone | *S. apiformis*: the 1988 alcohol is inactive without the 2004 aldehyde |
| gland content ≠ emitted blend ≠ sufficient blend | Francke 2004 extract vs SPME; Mozūraitis 2006 and Yang 2011, six vs two |
| a ratio belongs to its method and population | 2:3 vs 1:7; 93:7 (1985) vs 100:0.7:2.7:3.2 (2006) |
| a finding is a record, not a consensus | the Tasmanian strain, reported in 1990 and rejected in 2005 |
| an attraction record needs its conditions | lure purity (Kwon 2021 vs Yang 2011), dose, trap type and colour |
| trap shutdown ≠ population control | Anderbrant 2025 |
| receptor response ≠ behaviour | Cattaneo & Walker 2025 tested no behaviour |
| co-occurrence ≠ conversion | no paper here tests a biosynthetic step |

*How can a small lipid-biochemistry grammar generate this communication
space?* That question is the subject of the Atlas's later layers. This
literature defines the space; it does not explain how it is made.

## Sources not yet curated

- Chiluwal K, Kim J, Park CG, Roh GH (2020) Disruption of chemical communication of *Synanthedon tenuis* by sex pheromone dispensers in sweet persimmon orchards. *Korean J Appl Entomol* 59:333–339. https://doi.org/10.5656/KSAE.2020.10.0.057
- Anderbrant O, Huynh H, Isaksson A-K, et al. (2025) Development of pheromone-based mating disruption for three lepidopteran pests of currant in northern Europe. *J Appl Entomol* 149:1227–1236. https://doi.org/10.1111/jen.13446
- Kim WJ, Lee SH, Pyo J-Y, Park JS, Kim I (2025) Occurrence patterns and population genetic analysis of the clearwing moth, *Synanthedon bicingulata*, in Jeollanam-do, South Korea. *Int J Indust Entomol Biomater* 49:84–100. https://doi.org/10.7852/ijie.2025.49.3.84
- Yang H-J, Nah S, Kim H, Baek S (2025) Prediction model of adult flight activities of *Synanthedon bicingulata*. *Heliyon* 11:e41856.
- Cattaneo AM, Walker WB III (2025) Candidate pheromone receptors of the red-belted clearwing moth *Synanthedon myopaeformis* bind pear ester and other semiochemicals. *Agriculture* 15:1112. https://doi.org/10.3390/agriculture15101112

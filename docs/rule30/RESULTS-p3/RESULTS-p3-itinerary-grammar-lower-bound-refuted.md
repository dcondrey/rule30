# P3: LZ77 finds no more repetition in the digit words of B^n(0) than in a random word through n = 1024; no grammar lower bound follows

Date: 2026-09-18, corrected 2026-09-21. Bears on the question the Scope of
[the two-time density](RESULTS-p3-two-time-density-refuted.md) result leaves
open, after it and [Cartier homogeneous propagation](RESULTS-p3-cartier-homogeneous-propagation-refuted.md):
whether the intermediate field A itself (not just its rise mask), via
the Phi conjugacy / K-automaton of
[section 4](RESULTS-p3-implicit-boundary-investigation.md#4-the-actual-coupled-query-rather-than-a-generic-finite-core),
admits a sublinear representation. It stays open; this removes one hope only.

## Result

On the five words measured, the LZ77 factor count of the first n base-four
digits of B^n(0) is indistinguishable from that of an i.i.d. uniform
quaternary word of the same length, n = 64 to 1024, so LZ77 finds no
repetition there for a grammar to exploit. Nothing here shows that no
grammar-based representation is sublinear.

For a length-n string, its LZ77 factor count z is a lower bound on the size
g of any straight-line grammar producing it (z <= g; standard in the SLP-
compression literature, e.g. Rytter 2003, Charikar et al. 2005). The script
counts the self-referential factorization, in which a factor may overlap
its own source; that count is at most the non-overlapping one, so the bound
holds for it too. The bound is for plain straight-line grammars producing
the string; whether it carries to grammars with Repeat(W,m) nodes, which
[the repeat-transduction report](RESULTS-p3-itinerary-repeat-transduction.md)
uses, is not checked here.

Measured: for each n in {64, 128, 256, 512, 1024}, z of the first n
base-four digits of B^n(0), generated via `p3_itinerary_conjugacy.k_prefix`,
state `'B'`, applied h = n times from x=0 (the reproduction path of the
two-time density result), against a period-4 control and one i.i.d.
uniform quaternary draw per length from `random.seed(0)`. This is the full
digit word, not the binary low field A = low(B^h(0)) that the
implicit-boundary document calls A.

| n | z(real) | z(periodic) | z(random) | z(real)/n | z(random)/n |
|---:|---:|---:|---:|---:|---:|
| 64 | 29 | 5 | 30 | 0.453 | 0.469 |
| 128 | 52 | 5 | 50 | 0.406 | 0.391 |
| 256 | 85 | 5 | 90 | 0.332 | 0.352 |
| 512 | 145 | 5 | 145 | 0.283 | 0.283 |
| 1024 | 253 | 5 | 256 | 0.247 | 0.250 |

z(periodic) stays at 5, so the count does detect repetition when there is
some. z(real) is within 6% of the random draw at each length (3.3, 4.0, 5.6,
0.0 and 1.2 percent), and both ratios z/n fall at every step, from about
0.45 to 0.25. Four things limit what the table can say.

1. The ratio falls, and a Theta(n) factor count was the premise of the
   lower bound. The script's pre-registered kill was a disjunction: z/n not
   shrinking, or z tracking the random control. The saved output records
   `flat_or_growing_ratio: false` and `tracks_random_control: true`, so the
   verdict fired on the second arm alone, a 15% test on the n = 1024 row.
2. Tracking a random word does not make a grammar linear. Every length-n
   word over a fixed alphabet has a straight-line grammar of O(n / log n)
   rules: its LZ78 parse has that many phrases, each an earlier phrase plus
   one letter, and one rule per phrase plus a start rule is such a grammar.
   That is o(n) rules, and a typical random word needs that order and no
   less. A word that looks random to LZ77 therefore has a smallest grammar
   of order n / log n rules, which is sublinear in the literal sense. What
   a persistent match to the random control could exclude is a grammar of
   n^(1-eps) or polylog(n) rules, and five lengths up to 1024 do not
   establish persistence. The document fixes no bit-cost measure, so
   nothing about charged work follows either way.
3. The five rows are five different words. The script sets h = n, and the
   first n digits of B^n(0) are not a prefix of the first 2n digits of
   B^(2n)(0): recomputed 2026-09-21, consecutive rows first disagree at
   digit 6, 7, 11 and 11. The table is not the growth curve of one word.
   Each word lies inside the aperiodic head of B^n(0): the periodic tail
   of section 6 of
   [the session-limits supplement](RESULTS-p3-session-limits-supplement.md)
   begins at 1.5n to 1.65n, beyond the n digits taken.
4. The random column is one draw per length, and the 2026-09-18 text's
   "within 5% at every scale" failed on it at n = 256, where 85 against 90
   is 5.6%. Recomputed 2026-09-21 over seeds 0 to 19 with the script's own
   counter, the random control has mean 31.4, 51.9, 86.5, 147.9, 257.8 and
   standard deviation 1.6, 1.9, 2.6, 2.5, 2.8 at the five lengths, with
   ranges 29-35, 49-55, 80-90, 143-152 and 252-262. z(real) lies inside
   the range at every length, below the mean at four of the five and never
   by more than two standard deviations. All five z(real) values reproduce
   exactly. The spread and the prefix comparison are an in-session run of
   the existing module and script functions with no saved artifact.

**Verdict: refuted**, for one hope only: that LZ77 finds in these digit
words the repetition it finds in a periodic word. At the five measured
lengths it finds no more than in a random word of the same length, so a
plain straight-line grammar producing the n = 1024 word has at least 253
rules, and that is the whole bound. The 2026-09-18 text of this section
said a Theta(n) factor count had been measured and that no SLP/grammar-based
evaluator, including the Phi/K-automaton quaternary evaluator and its
repeat-transduction extension, can be sublinear on A, "independent of which
specific grammar construction is tried". The first contradicts the table
and the second fails on item 2; both are withdrawn. The quaternary
evaluator of section 4 is in any case not bounded by this count: its
grammar is over the chronological A/B/C generator word, not over the digit
word measured here, and it need not produce the digit word to answer one
query.

## Scope

A finite measurement on five words with n <= 1024 and one random draw per
length. It is not a lower bound on any grammar, evaluator or algorithm, and
it does not close the Phi conjugacy / K-automaton route. It does not
address: the binary low field A alone; grammars with repetition nodes; a
representation that answers the singleton query without producing the
digit word, which includes the quaternary evaluator of section 4; a
derived quantity such as the rise mask, for which the two-time density
result is likewise a finite measurement and no lower bound; or the
unrestricted question of whether any algorithm at all can answer a P3
query sublinearly, which remains open.

Reproduced independently: `experiments/rule30/p3_itinerary_grammar_lower_bound.py`,
`run()`, output saved to
`experiments/rule30/p3-itinerary-grammar-lower-bound.json`.

# Refutation: Das 2022, "Rule 30: Solving the Chaos"

**Verdict: REFUTED for P1. P2 not independently established (cites Wolfram's
own billion-cell empirics, proves nothing new). P3 not addressed at all.**

Assessed 2026-09-13. Mayukhmali Das (Jadavpur University, Kolkata),
"Rule 30: Solving the Chaos", arXiv:2207.13237, submitted 2022-07-27, single
author, 3 pages, 9 figures, 2 references, not peer reviewed (no venue given on
the arXiv listing). Retrieved and read in full from `arxiv.org/pdf/2207.13237`.
Zero citations found in any citation-graph search; absent from every prior
sweep in this project's records.

## What the paper actually contains

There is no theorem, no lemma, and no proof by contradiction anywhere in the
document. The entire argument for P1 is: (1) an informal causal story about
why Rule 30 looks chaotic, (2) one empirical statistic computed by simulation
out to 16,384 iterations, (3) an assertion that "correlation equals causation"
bridging that statistic to a second, unrelated empirical quantity, and (4) a
conclusion asserted from those two pieces with no derivation connecting them
to the actual object P1 asks about, which is the periodicity of the single
sequence at column 0.

### The "decisive branching" story (Sections 2-3)

The paper observes that Rule 30's Boolean rule `left ^ center | right` (Eq. i)
agrees with the symmetric, non-chaotic Rule 150 rule `left ^ center ^ right`
(Eq. ii) except when `center & right = 1` (Eq. iii), and calls this
divergence "decisive branching." It defines

```
Randomness Count = (# cells in the whole triangle, up to iteration N,
                     where right_cell = center_cell = 1)
                    / (total # Boolean calculations, up to iteration N)
```

and reports (Table 2) that this ratio, computed for N = 1024 through 16384,
sits near 0.14 and looks to be converging.

**This statistic is a density over the entire 2-D spacetime pattern.** It has
no stated relationship to any single column, let alone column 0. Nothing in
Section 2 or 3 connects "how often does the pattern `11` occur anywhere in the
triangle" to "is the bit sequence at a fixed horizontal position periodic."
These are a global areal density and a single infinite 1-D sequence; a
non-vanishing density of a local 2-cell pattern across a growing 2-D field is
neither necessary nor sufficient for any column extracted from that field to
be non-periodic. See the explicit counterexample below.

### The inferential jump (Section 5, "Conclusion to Problem 1")

The load-bearing paragraph, quoted in full because the whole verdict rests on
parsing it correctly:

> "Now that we have seen correlation between the two plots, we can say that
> the ratio of zeroes/ones and randomness count are mildly correlated. **In
> this particular case, correlation equals causation, simply because the
> degree of randomness will affect the number of zero and one.** Now the
> ratio of zeroes and ones approaches one which is shown in first one billion
> iteration in the Wolfram dataset. We can make this statement that the ratio
> of zeroes and ones can never approach zero in the steady state. Now as the
> Randomness Count is correlated with that of the ratio of zero/one. We can
> state that the Randomness count can never be zero in steady state. ...
> **Now since the randomness count can never be zero, the central value of
> the Rule 30 structure will always remain random as there will always be
> some decisive branching taking place. Thus, as the central column continues
> to remain purely random it will always be aperiodic.**"

Every step in this paragraph fails on its own terms:

1. **"Correlation equals causation, simply because..."** is asserted, not
   argued. The clause that follows it ("the degree of randomness will affect
   the number of zero and one") restates the conclusion being sought; it does
   not justify promoting a measured Pearson coefficient of **0.45** ("moderate
   correlation," the paper's own word in Section 4) into a causal law.
2. Even granting the causal claim, "ratio of zeroes/ones -> 1" is not the
   paper's own result: it is imported from "the Wolfram dataset" (uncited,
   unnamed, unlinked) and from P2, which the paper elsewhere admits is a
   *different*, unproven prize problem. A P1 proof cannot rest on an unproven
   P2 as a premise.
3. "Randomness count can never be zero" is extrapolated from five simulated
   points (N = 1024, 2048, 4096, 8192, 16384; a factor-of-16 range) trending
   toward ~0.14 with no error bound, no convergence rate, and no argument that
   the trend continues past N = 16384. This is curve-watching, not a limit
   proof.
4. **The final step is the actual gap.** "Randomness count nonzero" is a
   statement about a density over the whole 2-D array. "The central column
   ... will always be aperiodic" is a statement about one 1-D sequence. No
   equation, inequality, or even informal argument bridges these two objects
   anywhere in the paper. The word "random" is used interchangeably with
   "aperiodic" with no definition of either and no argument that one implies
   the other (a periodic sequence can still look locally unpredictable within
   one period; an aperiodic sequence need not be "random" in any sense).

There is no fixable core here in the way Topal's paper had one valid step
(Christol's theorem correctly stated) undone by one wrong lemma. This paper
never reaches the level of a formal claim about column 0 at all; the
statistic in Eq. (vi) is simply never about the object P1 asks about.

## The inference schema is falsifiable by direct construction

The paper's Section 5 argument reduces to the general claim: *if a 2-D binary
field has row-wise density of the pattern "adjacent cells both 1" bounded
away from zero as the field grows, then any fixed-position column extracted
from that field is aperiodic.* This is false, and falsifiable without
appealing to any unproven fact about a specific cellular automaton:

Tile every row with the repeating block `1100`. Every row has exactly density
1/4 of adjacent `11` occurrences, forever (bounded away from zero at every N,
matching the paper's own "steady state" premise with a stronger, *exact*
constant instead of an empirically-eyeballed one). Fix the column at any
offset that is always the same phase within the `1100` block (e.g. column 0
mod 4): that column is constant, hence periodic with period 1. The premise
holds and the conclusion fails. The inference schema used in Section 5 is
invalid in general, independent of whether Rule 30 itself is periodic.

## Computational verification against this repo's generator

Reproduced the paper's own numerator exactly, using
`experiments/rule30/center_column.py`'s bit-parallel row update as ground
truth and counting `right_cell & center_cell` over the full evolving triangle
(area = N^2, standard light-cone width `2t+1` at generation t):

```
RULE30 N=1024  ones=261648   total=1048576   randomness_count=0.2495269775
RULE30 N=2048  ones=1049720  total=4194304   randomness_count=0.2502727509
RULE30 N=4096  ones=4200252  total=16777216  randomness_count=0.2503545284
RULE30 N=8192  ones=16786312 total=67108864  randomness_count=0.2501355410
RULE30 N=16384 ones=67096383 total=268435456 randomness_count=0.2499535047
```

The **numerators match the paper's reported counts exactly at every tested N**
(the paper states "261648" in prose for N=1024 and this reproduces bit-exact,
and the same holds at 2048/4096/8192/16384 against Table 2's implied
numerators). This confirms the underlying simulation is correct and I am
measuring the same event the paper measures.

The **denominators do not match** (paper: 1,836,528 at N=1024, implying
randomness count 0.14245; measured here against the standard triangle area
`N^2` = 1,048,576, giving 0.2495). The ratio 1,836,528 / 1,048,576 ~= 1.751 is
not a clean multiple (not 1, 2, 3, or any obvious cell-counting convention),
and is not disclosed anywhere in the paper: "total number of Boolean
calculations" is never defined precisely enough to reconstruct. Whatever
convention the paper used, it does not change the conclusion above: the
statistic converges to *some* nonzero constant either way (~0.25 here,
~0.14 there), and a nonzero limit of this areal density was never in dispute.
What is in dispute is whether that has any bearing on column periodicity, and
the answer, per the explicit counterexample above, is no.

## Rule 90 control

Ran the identical statistic (density of `right_cell & center_cell` across the
whole evolving triangle) on Rule 90 (`new = left XOR right`), single black-cell
seed, using the same bit-parallel harness:

```
RULE90 N=1024  ones=0 total=1048576   same_statistic=0.0000000000  center_col_tail_constant=True value=0
RULE90 N=2048  ones=0 total=4194304   same_statistic=0.0000000000  center_col_tail_constant=True value=0
RULE90 N=4096  ones=0 total=16777216  same_statistic=0.0000000000  center_col_tail_constant=True value=0
RULE90 N=8192  ones=0 total=67108864  same_statistic=0.0000000000  center_col_tail_constant=True value=0
RULE90 N=16384 ones=0 total=268435456 same_statistic=0.0000000000  center_col_tail_constant=True value=0
```

The statistic is **exactly zero at every generation**, not just small. This is
a genuine structural fact about additive/XOR automata, not noise: Rule 90's
active cells at generation `t` occupy only positions of one fixed parity class
(`position + t` even), so two horizontally adjacent cells in the same row can
never both be nonzero, and `right_cell & center_cell` vanishes identically.
Rule 90's center column for this seed is independently confirmed here
eventually constant at 0 (matching `REFUTATION-topal-transcendence.md`'s
established finding, cell 0 at time `2m` is `C(2m,m) mod 2 = 0` for all
`m >= 1` by Kummer), i.e. it is periodic (period 1).

Consistent with this repo's standing note from the Topal assessment: **Rule
90 is a vacuous control for arguments built on this "decisive branching"
mechanism**, because Rule 90 has no `center & right` term in its own update
rule at all (`left XOR right` does not reference the center cell), so the
paper's causal story never fires on Rule 90 in the first place. The paper
itself notices this in passing (Section 2, "we can subside the decisive
branching in Rule 30 ... ANDing Rule 30 with its symmetric counter-part ...
the net output ... is Rule 90") without drawing the conclusion that its own
mechanism is Rule-30-specific and therefore cannot be tested for false
positives on Rule 90 the way a general periodicity criterion should be. The
synthetic `1100`-tiling counterexample above is what closes that gap: it
shows the inference schema fails even where the paper's mechanism nominally
"fires" (nonzero density), which Rule 90 alone cannot show since it never
fires there at all.

## P2 and P3

**P2 is not attempted as an independent result.** Section 4 measures a
Pearson correlation (0.45, "moderate") between the paper's own randomness
count and the zero/one ratio, and otherwise defers to "the Wolfram dataset"
("shown in first one billion iteration") for the actual P2 claim. No new
bound, no rate of convergence, no proof.

**P3 is not mentioned anywhere in the paper.** The abstract, introduction,
and all five sections address only P1 (with P2 invoked as a supporting,
unproven premise). There is no discussion of computing the n-th center cell
faster than the naive quadratic simulation.

## Literature engagement

Two references, both Wolfram: *Cellular Automata and Complexity* (2018) and
"Random sequence generation by cellular automata" (1986). No citation of the
2019 prize announcement that defines the three problems being addressed, no
Christol, Cobham, Allouche-Shallit, or any automatic-sequence/periodicity
literature, and no citation of any prior computational or theoretical work on
Rule 30 specifically (Wolfram's NKS 2002, Martin-Odlyzko-Wolfram 1984, or any
of the post-2019 prize-adjacent literature this repo has already surveyed).

## What this repo should take from it

1. The paper's central statistic (a global 2-D pattern density) is a category
   mismatch for a 1-D column-periodicity question; this is provable directly
   (the `1100`-tiling counterexample) without needing to touch Rule 30 itself,
   and is a reusable check against any future "empirical density never hits
   zero, therefore periodic/aperiodic" argument reaching this project.
2. Rule 90 remains a vacuous control for the "decisive branching" family of
   arguments specifically (the mechanism has no analogue in Rule 90's own
   update rule), consistent with the standing note in
   `REFUTATION-topal-transcendence.md`. A future assessment needing a live
   (non-vacuous) control for this family should build one where the paper's
   own statistic is nonzero and the column is independently known periodic,
   e.g. the explicit synthetic tiling used here, rather than reaching for
   Rule 90 by default.
3. The paper's own numerator reproduces bit-exact against this repo's
   verified generator; only its undocumented denominator convention does not.
   That is worth recording as the second, independent case (after Topal) where
   this project's ground-truth generator confirmed a claimed paper's raw
   simulation numbers while the paper's stated logical conclusion did not
   follow from them.

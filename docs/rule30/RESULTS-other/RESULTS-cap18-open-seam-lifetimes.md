# Capacity-18 open seams: direct lifetimes exceed every closed bound

Date: 2026-09-18. **Exact witnesses and a pre-registered census. Uniform
mortality of the four open seams, the capacity-18 rung, period-two exclusion
and P1 all remain open.**

The four unresolved capacity-18 seams, indices 8, 15, 23 and 34 of
[the joint-mortality report](RESULTS-capacity18-joint-mortality.md), have so far
been attacked by closing joint column sets at one common further depth. This
report evaluates explicit members directly instead. Every open seam has members
that live far longer than any closed capacity-18 pattern. The deepest found are
N = 35 for index 8 and N = 33 for indices 15 and 23, against N = 25 for every
closed capacity-18 pattern and N = 24 at
[capacity 17](RESULTS-capacity17-mortality.md). Each cited witness has
two-step capacity exactly 18 by a direct fiber count. A closed common-depth
certificate for these seams, if one exists, needs further depth at least 29 to
34. The existing engines closed depths 8 to 15 and hit their caps at the next
attempted depth.

## 1. The question

The route targets **uniform** mortality: one further depth by which every pair
`(a,b)` has failed a guard, certified by a closed joint set with zero survivors
at that depth. That is the form of the capacity-17 theorem, which bounds `N`
and `D` independently of the original length. It is stronger than individual
mortality, where every fixed pair dies but lifetimes may grow with the
parameters. P1 needs at most the second
([counting-route audit](../AUDIT/AUDIT-counting-route-scope.md): unbounded
lifetimes need not refute a uniform repeat bound). Until now the only evidence
on the open seams was their exact survivor counts, which cannot say how long
the longest members live.

## 2. Method and controls

For an explicit full second endpoint `w`, the further lifetime `ell(w)` is the
number of successful updates of the frozen `panel/cert33.py` map: survive if
and only if `u = v` at the end of the scan, append `3-v`, repeat. For the
initial tapes `00` and `01`, `N = ell + 2`, and `D` counts adjacent equal
scalars in the whole tape.

The evaluator is the one-star sweep of `capacity18_simple_family_independent.py`.
A shared row `prefix body^K` evolves once per step, and each member's suffix is
scanned from its own end position, so all `K` members of a one-parameter slice
are exact. A two-parameter family is swept as one slice per value of `a`.
Nothing is closed or quotiented, so no state cap applies; the only cap is 96
further steps, which no member reached.

Every control passed before any open-seam number was read.

| Control | Required | Measured |
|---|---|---|
| Index 12, `a,b < 64` | every `ell = 0` | all 0 |
| Index 27, `a < 2^11`, `b < 2^4` | max `ell = 15` | 15, first at `(2008, 15)` |
| Index 5, `b = 0`, `a < 2^20` | max `ell = 22` | 22, first at `a = 816930` |
| Index 5, `a,b < 64` | `ell(a,b) = ell(a+b,0)` | holds on all 4096 pairs |
| 26 joint-certificate witnesses (indices 5, 15, 27) | same tape | identical |
| 242 index-15 pairs through `direct_step` itself | same `ell` | identical |

The three required maxima are one less than the proved first failed further
guards of indices 12, 27 and 5, which are 1, 16 and 23.

## 3. Pre-registered census of index 15

[Pre-registration](../../../experiments/rule30/PREREGISTRATION-cap18-lifetime-growth.md),
written before the script existed. Family `213(13)^a1213(13)^b03` over
`a < 2^11`, `b < 2^16`, which is 2^27 pairs. The maximum on each dyadic
rectangle `a < 2^i`, `b < 2^j`, taking the best split of `i+j`:

| `i+j` | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| max `ell` | 20 | 22 | 22 | 22 | 24 | 24 | 25 | 26 | 27 |

Pre-registered outcome **(G)** fired: the maximum rose by one at each of the
last three doublings and exceeds 22. The record is

```text
(a,b) = (1534, 42986),   ell = 27,   N = 29,   D = 14,
tape = 00 100111100000111101011010010.
```

The number of pairs with `ell >= n` roughly halves with each step through the
whole observed range: exactly `2^26, 2^25, 2^24` pairs reach
`ell >= 1, 2, 3`, and for `n = 10, ..., 27` the counts are 155648, 81408, 40704, 21312, 10560, 5224,
2513, 1266, 637, 345, 170, 85, 40, 20, 10, 7, 3, 1.

## 4. Exploratory: the other seams and fixed-a lineages

Not pre-registered; the same protocol, rectangle and controls. Every record
below was replayed through `direct_step` on the explicit word.

| Index | Full second endpoint | Rectangle record | `ell` | `N` | `D` |
|---:|---|---|---:|---:|---:|
| 8 | `21213(13)^a1213(13)^b03` | `(753, 12291)` | 33 | 35 | 22 |
| 15 | `213(13)^a1213(13)^b03` | `(1534, 42986)` | 27 | 29 | 14 |
| 23 | `3031(31)^a213(13)^b03` | `(533, 25052)` | 28 | 30 | 13 |
| 34 | `30322(2)^a100(0)^b32` | `(20, 1144)` | 26 | 28 | 12 |

The index-8 record has tape `00 001110001001010001111111100111000`. The
next-deepest index-8 pair in the rectangle reaches only 27; in the other seams
the top two differ by at most one. Index 34 reaches 26 already on `a < 2^5`,
`b < 2^11` and never exceeds it on the full rectangle, where 5 pairs reach 26 and none 27. The
halving law would predict about two or three at 27, so this is weak evidence
of a ceiling, not a demonstration. Within the rectangle, other replayed pairs
raise the largest observed `D` to 16 for indices 15 and 23 (at `(374, 36890)` and `(619, 1277)`,
both with `N` of 25 or 26).

Fixed-a slices over `b < 2^24`, 256 times the rectangle's range of `b`. The
deepest pair of every slice was replayed through `direct_step` on its explicit
word, up to 30,497,753 symbols long:

| Index | `a` | max `ell` | first attaining `b` | `N` | `D` | pairs with `ell >= 28` |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 0 | 30 | 11630084 | 32 | 20 | 2 |
| 15 | 30 | 25 | 479146 | 27 | 14 | 0 |
| 15 | 1534 | 31 | 15247338 | 33 | 15 | 8 |
| 8 | 753 | 33 | 12291 | 35 | 22 | 3 |
| 23 | 533 | 31 | 2533308 | 33 | 16 | 3 |
| 34 | 20 | 28 | 8964344 | 30 | 15 | 1 |

Index 23 rises from 28 to 31 and index 34 from 26 to 28. Index 8 does not:
in its whole slice only `b = 12291`, the rectangle record, gets past 28.
The deepest index-15 member has tape `00 1001111000001111010110101011011`.
It extends the census record 2-adically: `15247338 = 42986 (mod 2^16)`,
and the two tapes agree on their first 24 further scalars. The slice at
`a = 30` dies at 25: its 32 deepest pairs are two residue classes modulo
`2^20` (`479146` and `762790`), all 32 fail the 26th guard, and so the next
four bits of `b` never rescue them. Some lineages end and others continue.

**Capacity of the witnesses.** The pattern labels come from the all-length
language audit, which proves every member of each pattern has two-step fiber
exactly 18. [A separate count](../../../experiments/rule30/cap18_witness_fibers.py)
checks this directly on each cited witness. It runs a 32-state product
automaton over both scans (original high bit, both scan states) and handles
the long bodies by exact integer matrix powers. It agrees with brute-force
enumeration of every legal original of length 1 to 7 (68 endpoint and scalar
pairs) and gives 18 for the capacity-18 fiber `30322(2)^k121032` at every
`k <= 7`. Every pair in the two tables above has `Q_2 = 18` exactly, as do
all members with `a, b < 8` of every capacity-18 two-parameter seam, open or
closed.

## 5. What the survivor counts say, and what they do not

The exact guarded-lift layers
([statistics](../../../experiments/rule30/capacity18-guarded-15.statistics.json))
give the offspring of each old index-15 survivor:

| New depth | Old survivors | 0 children | 1 child | 2 children | Mean |
|---:|---:|---:|---:|---:|---:|
| 13 | 125 | 3 | 28 | 94 | 1.73 |
| 14 | 216 | 18 | 45 | 153 | 1.63 |
| 15 | 351 | 30 | 97 | 224 | 1.55 |

The tree still grows at depth 15 but its mean offspring falls by about 0.08
per depth, and the share of old survivors with all four sheets reachable falls
from 58 to 47 percent. A tree whose mean keeps falling can die, so these counts
do not show that index 15 is non-mortal. Neither does the halving law of
section 3. The closed seam 5 obeys it over its full first-orbit period
`2^20`: the counts with `ell >= n` fall from 1048576 at `n = 0`, roughly
halving with two short plateaus, to 4, 2, 1 at `n = 20, 21, 22`, and reach
zero at 23, exactly its proved ceiling. The census does not
decide uniform mortality. What it fixes are the lower bounds below.

## 6. Consequences

1. **Certificate depth.** A closed joint set with zero survivors at depth `d`
   needs `d > ell` for every member. So any common-depth certificate needs
   `d >= 34` for index 8, `32` for indices 15 and 23, and `29` for index 34.
   The joint closures hit their two-million-state cap at depths 12
   (indices 8, 34) and 16 (indices 15, 23), and the guarded lift for index 15
   hit its route cap at 16. Its transport records grew 107008, 340480,
   1003008 at depths 13 to 15, about threefold per depth. Extrapolated at that
   rate, depth 32 needs on the order of `10^14` records. That extrapolation is
   not a proof, but the certificate shape the route asks for is not reachable
   by enlarging these engines.
2. **Uniform bounds at capacity 18.** A capacity-18 theorem in the capacity-17
   form (`Q_2 <= 18` implies `N <= N_18`, `D <= D_18`) needs `N_18 >= 35` and
   `D_18 >= 22`, from the index-8 witness, whose two-step fiber is exactly 18
   by the direct count of section 4. Capacity 17 has `N <= 24`, `D <= 14`; the
   closed capacity-18 patterns stay within `N <= 25`, `D <= 14`. Whether a
   finite `N_18` exists at all is the open question of section 5.
3. **Lifetime and repeats are separate questions.** Unbounded lifetimes would
   not make the repeat count unbounded. The repeat inequality
   `r + N + 1 <= 2^(D+1)(r+2)` of
   [the repeat lower bound](RESULTS-repeat-budget-lower-bound.md) bounds `N`
   for each original length `r` once `D` is bounded. So a uniform bound on `D`
   alone at capacity 18 would still give individual mortality even if `N` grows
   with `r`, and would survive a refutation of uniform `N`; the
   [counting-route audit](../AUDIT/AUDIT-counting-route-scope.md) draws the same
   distinction. These data do not separate the two. `D` reaches 22 on the
   index-8 witness and 20 on the index-15 pair `(0, 11630084)`. On all 24
   distinct replayed pairs with `N >= 25` it lies between `0.40N` and
   `0.64N`, near the half a fair coin would give. So the long records show no sign of `D`
   staying bounded while `N` grows, but nothing here measures whether `D` is
   bounded.
4. **What would settle it.** A proof that some survivor lineage of an open seam
   never ends would refute uniform mortality at capacity 18. The simplest
   candidate, that an old survivor with all four sheets reachable always has a
   child with the same property, fails on the saved index-15 layers, and
   order4 reproduction provably never repeats at consecutive depths
   ([guarded-lift report, section 7](RESULTS-guarded-two-block-lift.md#7-four-sheet-propagation-and-the-lift-of-a-four-cycle)),
   so that mechanism alone cannot sustain such a lineage. The capacity rung
   would then have to be stated through `D` as in item 3, as individual
   mortality, or as a bound on
   `N` growing with the original length. The observed record lifetimes grow
   roughly like the logarithm of the parameter range, which is compatible with
   the last. A proof that the lineages end
   would have to explain why the offspring mean keeps falling. The window,
   monodromy-mask, free-group and small-nucleus quotients already refuted in
   the joint-mortality report do not supply either proof.

## 7. Scope

Every lifetime above is an exact finite computation on an explicit word. No
statement is made about pairs outside the tested ranges except the elementary
certificate-depth bounds of section 6. Nothing here bears on individual
mortality of a fixed pair, on seams outside capacity 18, on the reduction from
capacity mortality to period two, or on P1.

## 8. Reproduction

```sh
cd experiments/rule30
uv run --no-project --with numpy python cap18_lifetime_census.py      # about 35 s
uv run --no-project --with numpy python cap18_lifetime_lineages.py    # about 60 s
uv run --no-project --with numpy python cap18_lifetime_lineages.py --replay-deepest   # about 4 min
uv run --no-project --with numpy python cap18_witness_fibers.py       # seconds
```

Artifacts: [cap18-lifetime-census.json](../../../experiments/rule30/cap18-lifetime-census.json)
(pre-registered, with all controls),
[cap18-lifetime-lineages.json](../../../experiments/rule30/cap18-lifetime-lineages.json)
(exploratory, with the independent replays of every slice's deepest word) and
[cap18-witness-fibers.json](../../../experiments/rule30/cap18-witness-fibers.json)
(direct `Q_2` of every cited witness). Each records the sha256 of its scripts
and of `panel/cert33.py`.

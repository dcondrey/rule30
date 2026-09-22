# The doubling-latch exclusion of finite recurrent rows

Date: 2026-09-09. Evidence: **U** (uniform proofs), **C** (complete finite
checks), **M** (diagnostic tables). The symbolic argument was independently
audited. This result closes the specified Rule 150 finite-factor construction
class; it does not prove R1 or exhibit an R1 counterexample.

## 1. Result and mechanism

Let

\[
 K(a)_i=a_{i-2}\oplus(a_{i-1}\lor a_i)
\]

be Rule 30 followed by a spatial shift toward increasing coordinates.
A row is *recurrent* here if arbitrarily late iterates return to each of
its finite coordinate windows. This is recurrence under `K`, not recurrence
under spatial translation.

**Theorem (U).** No nonzero finite-support row is recurrent under `K`.

**Corollary (U).** For every nonempty finite initial Rule 30 row `D`,

\[
 \bigl|\operatorname{supp}(F_{30}^{\,t}(D))\bigr|
       \longrightarrow\infty\quad(t\longrightarrow\infty).
\]

This holds over all times, and in particular along dyadic times. Section
5 also gives an explicit, weak lower bound of order
`log_2 log_2 t - log_2 log_2 log_2 t - O(1)`.

The mechanism is an OR latch immediately after every period doubling in
the triangular prefix dynamics. A doubling forces a permanent 1 at the
next spatial coordinate. Finitely supported recurrence would permit
only finitely many doublings; all prefix periods would then stabilize,
forcing a finite nonzero row to be globally periodic. Its expanding
rightmost front makes that impossible. The proof permits identity branches
at arbitrarily many coordinates and does not assume that the measured
single-cycle pattern continues.

## 2. Exact prefix-cycle extension (U)

Translate a nonzero finite row so that its leftmost 1 is at coordinate 0.
Under `K`, all negative coordinates stay zero and coordinate 0 stays 1.
Every prefix `[0,N-1]` evolves autonomously.

Suppose a parent prefix is on a cycle of minimal period `P`. Appending
coordinate `i=N` gives the periodically driven bit recurrence

\[
 b(t+1)=a_{i-2}(t)\oplus\bigl(a_{i-1}(t)\lor b(t)\bigr).
 \tag{1}
\]

The map taking `b(0)` to `b(P)` is one of the four maps of a two-element
set: a constant map, the identity, or negation. Its recurrent extensions
are therefore exactly:

| `P`-step map | Complete recurrent extensions |
|---|---|
| Constant | One cycle of minimal period `P` |
| Identity | Two cycles, each of minimal period `P` |
| Negation | One cycle of minimal period `2P` |

The parent minimal period must divide an extension's period, which rules
out a smaller period in this table. Starting with the one-state prefix
`a_0=1` and applying this construction therefore enumerates every
recurrent prefix cycle, with no missing initial phases or cycles.

For an arbitrary initial prefix, the same argument inductively shows
that its eventual period is a power of 2. Once the parent has entered
its cycle, (1) is driven periodically; a constant `P`-step map enters its
fixed bit state, while identity and negation are already permutations.
The transient is finite. No bound uniform in prefix width is assumed.

## 3. Every doubling forces the next coordinate to be 1 (U)

Suppose coordinate `i` doubles its parent's minimal period from `P` to
`2P`. Its `P`-step bit map is negation. If `a_(i-1)(t)=1` at even one
phase of the parent cycle, the one-step map at that phase is constant,
independent of `b(t)`. A composition containing a constant map is
constant. Consequently a doubling requires

\[
 a_{i-1}(t)=0\quad\hbox{at every time on the parent cycle}.
\]

Write `X(t)=a_i(t)`. Negation gives

\[
 X(t+P)=1-X(t),
\]

so `X` has at least one 1. The next coordinate `Y(t)=a_(i+1)(t)` obeys

\[
 Y(t+1)=X(t)\lor Y(t).
 \tag{2}
\]

This bit is monotone in time and eventually becomes 1. On any recurrent
prefix containing it, its trace is periodic from the initial time;
hence it must be identically 1, including at the initial time. No
assumption that its period equals `P` or `2P` is needed.

This is the **doubling-latch lemma**: a period doubling at coordinate
`i` forces initial coordinate `i+1` to be 1 on every recurrent extension.

## 4. Finite-support recurrence is impossible (U)

Suppose a nonzero finite row `Q` were recurrent, translated so that its
leftmost 1 is at 0, and let `b` be its rightmost 1. Every finite prefix
of `Q` is on a finite cycle from the initial time: a return of a state
in a finite deterministic system places that state on a cycle.

Let `P_N` be the minimal period of the prefix of width `N`. Section 2
gives `P_1=1` and `P_(N+1)` equal to `P_N` or `2P_N`. By section 3, a
doubling at coordinate `i>=b` would force `Q_(i+1)=1`, contradicting
the definition of `b`. Only finitely many doublings are possible.
Therefore all sufficiently long prefix periods equal a single finite
power of 2, say `P` (the coarse bound `P<=2^b` suffices).

Every coordinate of `K^P(Q)` equals that of `Q`, since it belongs to a
prefix fixed by `K^P`. Thus `K^P(Q)=Q` as full rows.

But the rightmost 1 of a nonempty finite row advances exactly two
positions under one `K` update: at position `b+2`, the input at `b`
is 1 and the two other inputs are zero, while every farther output is
zero. Its rightmost 1 after `P` steps is at `b+2P`, contradicting
`K^P(Q)=Q`. This proves the theorem.

## 5. Limit points and population divergence (U)

### 5.1. The explicit dyadic limit

Let `D` be any nonempty finite initial row, with leftmost 1 translated
to 0. By section 2, each finite `K` prefix eventually has a power-of-two
period. For a fixed prefix, all sufficiently large times `2^m` lie
beyond its transient and are congruent to 0 modulo that period. The
prefix of `K^(2^m)(D)` therefore stabilizes. These stable prefixes are
compatible and define a row `Q` in the product topology:

\[
 K^{2^m}(D)\longrightarrow Q.
\]

Each stable prefix is a state on the eventual prefix cycle. Therefore
every prefix of `Q` is itself on a cycle from time 0. Given any finite
window, arbitrarily large multiples of its cycle period return that
window, so `Q` is recurrent. Its coordinate 0 is 1, because that
coordinate remains 1 throughout the original orbit.

The theorem implies that `Q` has infinitely many ones. For any integer
`M`, choose `M` of these ones in a finite prefix. Coordinatewise
convergence places all `M` ones in every sufficiently late dyadic
iterate. Thus the population of `K^(2^m)(D)` tends to infinity. A
spatial shift does not change population, so the same statement holds
for `F_30^(2^m)(D)`.

This argument neither assumes that the number of doublings is unbounded
nor requires a formula for the depths at which they occur.

### 5.2. Population tends to infinity over all times

Suppose instead that an unbounded sequence of times `t_n` had population
at most a fixed integer `M`. Compactness of the one-sided binary product
space supplies a subsequence along which `K^(t_n)(D)` converges to a row
`Q`. Every fixed prefix of the original orbit eventually lies on its
finite cycle. Its limiting state therefore lies on that cycle, so every
prefix of `Q` is cyclic and `Q` is recurrent, exactly as above. Its
coordinate 0 remains 1.

The set of rows with at most `M` ones is closed in the product topology:
a limit with `M+1` ones would specify those ones in a finite window, and
all sufficiently late members of the convergent sequence would contain
them too. Hence `Q` has at most `M` ones. This contradicts the theorem
excluding nonzero finite-support recurrent rows. Therefore no bounded-
population subsequence exists, which proves population divergence over
all times. Again, shifting from `K` back to `F_30` preserves population.

### 5.3. An explicit lower bound

Consider any recurrent prefix of width `N`, with `M` ones in a specified
cycle phase and minimal period `P`. A doubling at any coordinate except
the last forces a distinct visible 1 at the next coordinate. At most
one doubling, at the last coordinate, can have its forced 1 outside
the prefix. Consequently the conservative bound

\[
 P\le2^{M+1}
 \tag{3}
\]

holds. This count uses the permanent ones from section 3, so it applies
to every phase of the cycle.

Such a `K^P`-fixed prefix cannot contain `2P` consecutive zeros. Suppose
a zero block starts at `a` and ends at `a+2P-1`. The latter output under
`K^P` depends on inputs from `a-1` through `a+2P-1`. Its dependence on
the leftmost input is permutive, and when the other `2P` inputs are
zero the output equals that leftmost input: the rightmost front of a
single 1 advances exactly `2P`. Since the output here is zero, the
preceding bit at `a-1` is zero. Repeating this argument extends the
zero block leftward until it contradicts the fixed bit at coordinate 0.

There are at most `M+1` zero gaps around `M` ones. The absence of a
length-`2P` zero block and (3) give

\[
 N\le2P(M+1)\le2^{M+2}(M+1).
 \tag{4}
\]

The width-`N` autonomous system has at most `2^N` states, so by time
`t>=2^N` its orbit is cyclic. For `t>=2`, take
`N=floor(log_2 t)>=1`, and let `W(t)` be the full row population.
Applying (4) to that prefix, and then using its population at most
`W(t)`, proves the explicit inequality

\[
 \lfloor\log_2 t\rfloor\le2^{W(t)+2}\bigl(W(t)+1\bigr).
 \tag{5}
\]

In particular, writing `N=floor(log_2 t)`,

\[
 W(t)\ge\log_2 N-\log_2\bigl(\log_2 N+1\bigr)-2.
 \tag{6}
\]

To see (6), if `W(t)>=log_2 N` it is immediate; otherwise bound
`log_2(W(t)+1)` above by `log_2(log_2 N+1)` in the logarithm of (5).
The inequality is merely trivial at small times. Its asymptotic form
is the weak lower bound stated in section 1. All constants here are
deliberately conservative; no measured period-growth law is used.

## 6. Consequence for the Rule 150 construction (U)

[RESULTS-r1-r150-factor-zero-background.md](RESULTS-r1-r150-factor-zero-background.md)
proves that every nontrivial finite-radius, clock-4, space-14 local
factor of the lone-seed Rule 150 orbit into Rule 30 has zero background.
Its initial output is therefore a nonempty finite Rule 30 row.

At each sufficiently large dyadic time `2^m`, the source row consists
of precisely three ones, at `-2^m,0,2^m`. A radius-`R` local factor
with zero background can have output ones only within distance `R`
of those three source ones, giving the uniform population bound

\[
 \bigl|\operatorname{supp}(s(2^m,\cdot))\bigr|\le3(2R+1).
\]

This contradicts section 5, already using only its dyadic corollary.
Hence **there is no nontrivial finite-radius
factor in that clock-4, space-14 Rule 150 class, at any radius**. This is
a uniform construction-class exclusion; it does not follow from the
finite synthesis UNSAT results, and it does not exclude other R1
counterexample constructions.

## 7. Complete prefix-cycle diagnostic (C/M)

The diagnostic was registered with maximum width 200 and a cap of
1,000,000 recurrent cycle vertices. It uses the exact extension in
section 2, rather than enumerating all `2^N` prefix states.

Rule 30 reaches width 200 well below the cap. There is exactly one
recurrent cycle at every checked width. Period doublings occur at
coordinates 3, 8, and 29; no identity branch occurs through coordinate
199. The permanent-one coordinates at width 200 are `0,1,4,9,30`,
and the permanent-zero coordinates are `2,7,28`. These lists and the
absence of identity branches are finite measurements only.

| Prefix width | Cycles | Recurrent vertices | Minimum bit length | Minimum number of ones |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 | 2 |
| 3 | 1 | 1 | 2 | 2 |
| 4 | 1 | 2 | 2 | 2 |
| 5 | 1 | 2 | 5 | 3 |
| 8 | 1 | 2 | 5 | 3 |
| 9 | 1 | 4 | 5 | 3 |
| 10 | 1 | 4 | 10 | 4 |
| 29 | 1 | 4 | 26 | 14 |
| 30 | 1 | 8 | 26 | 14 |
| 31 | 1 | 8 | 31 | 15 |
| 100 | 1 | 8 | 98 | 44 |
| 200 | 1 | 8 | 198 | 94 |

Bit length is one plus the rightmost set-bit coordinate. Minimum bit
length and minimum population need not be attained by the same phase.
One exact minimum-bit-length width-200 phase, encoded with coordinate 0
as the least significant bit, is

```text
0x2d100a1caedaaeaaaefaae937c2054391705126f7442f1e713
```

It is a state on the eight-state width-200 cycle, not a recurrent
infinite row. All eight actual cycle states are retained.

Complete counts at **every** completed width, including branch counts,
period histograms, permanent coordinates, and a minimum-bit-length
witness, are in
[recurrent-prefix-rule30.json](../../experiments/rule30/r1-r150-factor/recurrent-prefix-rule30.json)
and the compact
[CSV table](../../experiments/rule30/r1-r150-factor/recurrent-prefix-rule30.csv).
The final cycle archive is
[recurrent-prefix-rule30-final-cycles.json.gz](../../experiments/rule30/r1-r150-factor/recurrent-prefix-rule30-final-cycles.json.gz).

## 8. Rule 90 control and independent checks (U/C)

For the analogous Rule 90 moving map,

\[
 K_{90}(a)_i=a_{i-2}\oplus a_i,
\]

period doublings do not produce the OR latch. If column `i-1` is
identically zero, the next bit obeys `Y(t+1)=Y(t)` and may stay zero.
Indeed the single finite seed is recurrent:

\[
 K_{90}^{2^m}(\delta_0)
   =\delta_0\oplus\delta_{2^{m+1}}
   \longrightarrow\delta_0.
\]

This explicit counterexample shows exactly where the finished Rule 30
proof fails for the control rule.

The Rule 90 enumeration completes width 20, with 32,768 cycles,
524,288 recurrent vertices, all of period 16, and minimum bit length
1. Width 21 would have 65,536 cycles and 1,048,576 vertices; the exact
extension counts are recorded, and the run stops before materializing
that width because it exceeds the cap. Every completed width has all
`2^(N-1)` allowed prefix states recurrent, as expected. Its full table
and retained final cycles are recorded beside the Rule 30 files.

The independent verifier constructs the complete scalar-truth-table
functional graph at widths 1 through 12 for both rules, using indegree
pruning rather than the extension algorithm. Its recurrent-state sets
agree exactly with the projected retained cycles. It also replays
every retained cycle update: 8 updates for Rule 30 at width 200 and
524,288 for Rule 90 at width 20, with no repeated state across distinct
cycles. The unchanged `controls.rule90_control(6)` is run and passes
all its `T=2,4,6` checks.

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/r1-r150-factor/recurrent_prefix_cycles.py --max-width 200 --vertex-cap 1000000
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/r1-r150-factor/verify_recurrent_prefix_cycles.py
```

The independent verification output is
[recurrent-prefix-independent-check.json](../../experiments/rule30/r1-r150-factor/recurrent-prefix-independent-check.json).
No frozen engine is modified.

## 9. Honest scope

The uniform theorem concerns finite-support recurrence in the moving
frame, and the population corollary concerns complete rows at all times. Neither
establishes eventual aperiodicity of a fixed Rule 30 column. No bounded
centre-history predictor is constructed. No averaged statistic is
used. The proof handles arbitrarily long prefixes symbolically and
allows their periods and settling times to grow; the finite diagnostic
does not replace either uniform argument.

The classical eventual periodicity of the left light-cone diagonals is
recorded in [RESULTS-ordered-wedge-glide.md](RESULTS-ordered-wedge-glide.md).
The present use of the next-coordinate OR latch does not assume a
quantitative growth law for those diagonal periods or extend their
periodicity to the centre.

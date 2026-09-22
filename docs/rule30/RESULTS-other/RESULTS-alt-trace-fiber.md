# Rule 30 alternating-trace fiber: bounded-depth and bounded-support certificates

## Status

**OPEN, with verified bounded certificates in two independent resource
parameters.**  This cycle does not prove the period-two exclusion; it reduces it
to one uniformity gap and certifies every instance of bounded left **depth** up
to 24, and separately every instance of bounded left **support** up to 26 ones in
both phases.  The support family is strictly stronger and covers sparse rows the
depth family cannot reach.  Both reduce to the same open statement: no reachable
frontier follows the zero-cost map forever.  The same construction runs for every
nonconstant word of period 2 to 5, so the route is not period-two-specific.
Nothing here bears on the center-column prize problem beyond the nonconstant
periodic subcase of the finite-configuration question.

Context: after the zero-tail note was endorsed, J. Kari suggested excluding
nonconstant periodic traces next, eventually all of them.  Both constant
traces are settled (zero: the note; one: the checkerboard fiber in
`RESULTS-eventual-period.md`).  This arm attacks the first nonconstant case,
the alternating trace, at the same fiber level as the note.

## PROVED: zero-set reduction

For any prescribed trace `c` and right half, the compatible configuration is
unique (Lemma 1 of the note).  Rotating the rule at the origin,

```text
l_t = c_(t+1) XOR (c_t OR r_t),
```

so `l_t` depends on `r_t` only at times with `c_t = 0`.  Column `-2` is
`x(t,-2) = l_(t+1) XOR (l_t OR c_t)`, a function of `(c, l)`, and inductively
every deeper column is a function of the two columns to its right.  Hence:

> The forced left half-plane is a function of the trace and of column 1
> restricted to the zero set `{t : c_t = 0}`.

For the alternating trace the zero set is one parity class.  Write
`rho_k = r_(2k)` (phase `01`, i.e. `c_0 = 0`) or `rho_k = r_(2k+1)` (phase
`10`).  The pinned parity contributes `l_t = 1` outright.  The entire forced
left half `L_j = x(0,-j)` is then a triangular function of `rho` alone:
`L_j` needs roughly `rho_0..rho_(j/2)`.  This is the general form of the
reduction in `PATH.md` section 2, specialized to the exact fiber: the
one-phase is discharged by the pin, and all remaining freedom is `rho`.

Explicitly, phase `01`: `L_1 = NOT rho_0`, `L_2 = rho_0`, `L_3 = NOT rho_1`,
`L_4 = rho_0 AND rho_1`, `L_5 = rho_2 XOR (rho_0 OR NOT rho_1)`, consistent
with the recorded stencil (`L_3 = R_1 OR R_2 OR R_3` since
`rho_1 = NOT(R_1 OR R_2 OR R_3)`).

## VERIFIED: bounded-depth exclusion certificates

Say a configuration has *left depth `d`* if its initial row vanishes at every
position left of `-d`.  Claim(d): no configuration of left depth `d` has
central trace exactly `(01)^inf` (resp. `(10)^inf`), regardless of its right
half, finite or not.

Certificate for Claim(d): a level `k(d)` such that **every** `rho`-prefix of
length `k(d)` already forces some `L_j = 1` with `j > d`.  Violation is
monotone under prefix extension (the triangle only grows), so a pruned BFS is
sound; for `d <= 12` the certificate was additionally re-verified by unpruned
exhaustive enumeration of all `2^k(d)` prefixes.

Measured certificate levels (probe defaults print `d <= 16`; the run below
went to 24; exhaustive through 12, BFS beyond):

```text
phase 01: d:  0  1-4  5-7  8-11  12-14  15-17  18-19  20-21  22  23-24
          k:  1   4    5     9     15     16     17     19    21    22
phase 10: d:  0  1  2-4  5  6  7-8  9-10  11-13  14-18  19-21  22-23  24
          k:  1  1   3   4  5   6    9     15     16     19     20     21
```

Every `d` through 24, both phases, is certified.  (An earlier draft of this
section claimed "survivor counts peak at 64" and "~15 distinct wavefront
values per level"; both described only the late post-knee levels.  Measured
with exact state instrumentation: survivors are the full `2^k` prefixes up
to the knee `k = d/2`, peaking at 4096 prefixes / 1009 distinct frontier
states at the `d = 24` knee, then halving per level.  The halving is now
explained exactly; see the parity section below.)  Consequences, stated
exactly:

* No configuration with left depth `<= 24` has central trace exactly
  `(01)^inf` or `(10)^inf`.  In particular no finite configuration of left
  support depth `<= 24` does, with **no bound on its right support**.
* This does not yet exclude the alternating trace for all finite
  configurations: a finite configuration of larger left depth, and the
  eventually-alternating case (whose translate `F^T(x)` has left depth up to
  `w + T`), need Claim(d) for unbounded `d`.

The uniformity gap is the whole remaining obligation:

> **Open target.**  Claim(d) for every `d`.  Equivalently: no `rho` sequence
> keeps `L(rho)` eventually zero.  With it, no finite configuration has an
> eventually 2-periodic nonconstant center column (translate to the onset of
> periodicity; the translate is finite, nonzero, with exact alternating
> trace).

Two facts constrain the proof search.  The certificate level grows roughly
linearly (`k(d) ~ d`), so the trace-side and cone-side collide within one
cone-return time; and the post-knee survivor dynamics is now known exactly
(next section): deterministic with one parity check per level.

*(Correction 2026-09-08: this paragraph previously contrasted `k(d) ~ d` with
"the `O(log t)` wall of trace-anchored propagation".  That wall was the run-reach
lemma, whose "exactly when" is false; centre-only reach is not the run length and
no `O(log t)` bound is proved.  See `NEXT-DIRECTIONS-post-rung2.md` 1.  The
`k(d) ~ d` measurement is unaffected.)*

## VERIFIED: the support-count certificate family, and its extension to any period

A second resource parameter, strictly stronger than left depth.  Count the
**number of ones** in the initial left row rather than the position of the
leftmost one.  Write `H(K)` for the deepest left prefix any admissible `rho`
can reconstruct using at most `K` ones, so a finite `H(K)` excludes every
configuration with at most `K` left ones.

This covers configurations the depth family cannot reach.  Left depth `<= d`
implies at most `d` ones, but not conversely: a row with five ones spread out to
position `-10^6` has support 5 and depth `10^6`, so `Claim(d <= 24)` says nothing
about it while `H(5)` does.

Measured under **no `11` in consecutive samples of `rho`**, the separately
proved necessary condition for an alternating centre (the two-row identity,
`RESULTS-BILATERAL.md`).  That is a superset of the realizable right columns, so
a finite `H(K)` is a sound exclusion:

```text
K            0    1    2    4    8   10   16   20   24   26
H, phase 01  1    7   17   28   56   79  112  140  168  191
H, phase 10  0    2    6    8   24   31   66   85  112  119
```

Both phases terminate at every budget, with no depth-cap hit.  Hence, for every
Rule 30 diagram and any start time `T`:

```text
c_T..c_(T+192) = (01)^96 0   =>   sum_(j=1..192) s(T,-j) >= 27
c_T..c_(T+120) = (10)^60 1   =>   sum_(j=1..120) s(T,-j) >= 27
```

Together these exclude an infinite alternating centre, either phase, for every
initial row with at most 26 ones at negative positions, with no bound on their
spacing and no restriction on the positive half.

**The route is not period-two-specific**, under a weaker model.  The same
construction runs for an arbitrary periodic centre word: `col_-1(t)` is pinned to
`1 - c(t+1)` wherever `c(t) = 1` and free wherever `c(t) = 0`.  But the no-`11`
condition above is derived for the alternating centre and is **not** known to be
necessary for a general word, so the sweep uses only the general one-step
condition `u(t)=1 => u(t+1) = 1-c(t)`.

### RESOLVED: the `no-11` analogue for every periodic word

`alt-trace-frontier/sample_filter.py`, validated by `test_sample_filter.py`.
This removes the gap named in the paragraph above.

The whole derivation is the column-1 update with `col_2` existentially free:

```text
s(t+1,1) = c_t XOR (s(t,1) OR s(t,2))
s(t,1) = 1  =>  s(t+1,1) = 1 XOR c_t      deterministic, the OR saturates
s(t,1) = 0  =>  s(t+1,1) free
```

So a one in `col_1` propagates deterministically, surviving each centre-zero
time and dying the step after the first centre-one time.  For the alternating
word this yields `rho_k = 1 => rho_(k+1) = 0`, recovering `no-11` from
`p1-period2-invariant/RESULTS-BILATERAL.md` as a special case.  The realizable
sample language is therefore regular for **every** periodic word, recognised by
an automaton with exactly `2 * (zeros per period)` states.

**But it is not of finite type, and that is why `no-11` never generalised.**  For
`001` the minimal forbidden words are `111, 1011, 10010, 100011, 1000010,
10000011, ...`, a family growing without bound.  Period two is the exceptional
case where the forbidden set happens to be finite.  A search does not need a
finite forbidden set, only a decidable filter, so `support_H` now takes the
automaton directly via `samples_ok`.

*Soundness.*  Quantifying `col_2` away is a relaxation, so the language is a
superset of the realizable samples and a terminating search stays a sound
exclusion.  Checked against real evolutions, which know nothing of the
automaton: the `col_1` lemma holds on over 5,000 observed instances, and no
sample word observed in an actual Rule 30 spacetime is ever rejected, over seven
words and more than 1,000 spans.

*Regression.*  On the alternating word the automaton reproduces the hand-derived
`no-11` figures exactly, `H = 1, 7, 17, 21, 28, 35, 43, 49, 56, 63, 79` for
`K = 0..10`.

*What it buys.*  Period 3 was previously stuck in the weak one-step model.  Under
the correct filter the bounds are strictly stronger wherever a period has more
than one sample:

```text
word   K=2      K=4       K=6        (weak -> strong)
001    8 -> 8   23 -> 18  41 -> 29
010   15 -> 15  28 -> 25  46 -> 38
100    8 -> 7   24 -> 15  30 -> 27
011, 101, 110: no change, one sample per period
```

### The period-two target is now a sandwich

The torus gives `H_01(K) >= 7K`.  Measured `H_01(K) - 7K` for `K = 0..23` is

```text
1, 0, 3, 0, 0, 0, 1, 0, 0, 0, 9, 4, 2, 0, 1, 0, 0, 0, 3, 2, 0, 0, 1, 0
```

every search terminating, no depth cap hit.  So the open obligation has a sharp
quantitative form:

> **Conjecture (A4).**  `H_01(K) <= 7K + c` for an absolute constant `c`, with
> `c = 9` sufficing for every `K <= 23`.

With it, period-two nonconstant is closed: finite support bounds `K`, hence
bounds the depth.  `H(10) = 79` forces `c >= 9`, so 9 is exactly the smallest
constant the data allows.  `K = 0..23` are reproduced here independently
(`H(21) = 147`, `H(22) = 155`, `H(23) = 161`); the recorded `K = 24, 26` values
remain from the external continuation.

*One mechanism is ruled out for proving it.*  A charging argument whose sink is
"annihilation at the left-permutive edge" cannot work: by the unconditional-front
lemma above, the leading difference never annihilates.  Cancellation happens in
the interior, behind the front, and is conditional on the `OR` term, so the
ledger has to charge interior events.

### MEASURED: the extremal row is a torus prefix plus a bounded coast

Recovered with `support_H(..., collect_rows=...)`.  **The depth-maximising left
row is unique at every `K <= 16`**, and the earlier description "the torus is
very nearly extremal" was too weak in one direction and too strong in another.

At `K = 1..10, 13..16` the extremal row is exactly the torus progression
`1 + 7j`.  At `K = 11, 12` it is not:

```text
K=10  ones 1,8,...,64          gaps 7^9            tail 15   H=79
K=11  ones 1,8,...,64, 80      gaps 7^9, 16        tail  1   H=81
K=12  ones 1,8,...,64, 79, 80  gaps 7^9, 15, 1     tail  6   H=86
K=13  ones 1,8,...,85          gaps 7^12           tail  6   H=91
```

The mechanism is visible: at `K = 11`, continuing the progression puts the 11th
one at 71 and the *12th* at 78, which halts the count at depth 77.  Placing it at
80 instead reaches 81.  So the optimum is a **torus prefix followed by a coast**,
and coasting wins exactly when the next progression one would arrive too early.

Consequently `H(K) - 7K` is precisely the coasting surplus, which is why it is 9
at `K = 10` (tail 15 against a 7-spacing) and 0 at `K = 13` (pure progression).
This splits A4 into two separable lemmas, a better shape than one bound:

> **Spacing lemma.**  Every extremal row is a torus-progression prefix followed
> by a coast.
>
> **Coast lemma.**  The coasting surplus is bounded by an absolute constant.

Together they give A4.  Neither is proved here, and the uniqueness and spacing
are measured to `K <= 16` only, which is exactly the evidential shape that has
collapsed before in this project; the `K = 11, 12` exceptions were found by
trying to break the pattern rather than by extending it.

### PROVED: a decisive refutation criterion for A4, and a finite search against it

The criterion is due to panel 5 (`transcript5.md`, astra-pro round 1); the
derivation is checked here rather than taken on trust.

**Criterion.**  Let a space-periodic Rule 30 spacetime have an exactly
alternating centre column, spatial period `S`, and `w` ones per period in its
row.  Taking `n` periods gives a configuration with `K = nw` left ones
reconstructing depth `nS`, so `H(nw) >= nS` and the defect is `n(S - 7w)`.
Hence

```text
any alternating-centre torus with S > 7w  =>  H(K) <= 7K + c is FALSE.
```

The space-7/time-4 torus has `S = 7`, `w = 1`, ratio exactly 7, so it sits on the
boundary and is consistent with the bound rather than a counterexample.

**Independent search**, `ether-interface/torus_search.py`, by a different method
from the panel's: build the full functional graph on the `S`-cell ring, peel to
the cycle states, and inspect every column of every cycle.  Through `S = 20`:

```text
S = 7   row 0000001         w = 1  P = 4  ratio 7.000
S = 14  row 00000010000001  w = 2  P = 4  ratio 7.000
every other S <= 20: NO alternating column on any cycle
```

`S = 14` is two copies of the `S = 7` torus, so there is exactly one primitive
alternating-centre torus at these sizes, and **no torus beats ratio 7**.  Both
the panel's search over temporal periods and this one over spatial periods come
back negative.

Alternating centres are extremely rare on rings and appear only at `S = 0 mod 7`,
which is itself a structural constraint worth proving: it would say the torus
ratio is not merely unbeaten but forced.  A negative search remains a finite
search, not a theorem.

**CORRECTION: these searches cannot establish A4, and an earlier reading of them
here was too strong.**  Panel 5 (`panel/transcript5.md`, astra-pro round 3) makes
the logical point.  A torus with `S > 7w` refutes A4, so the searches rule out
one refutation mechanism; but *unbounded surplus does not require a density below
`1/7`*.  The law `H(K) = 7K + floor(sqrt K)` has asymptotic slope exactly 7 and
unbounded surplus, so it violates `H(K) <= 7K + c` while admitting no torus of
ratio above 7.  Searching only for `S > 7w` therefore cannot confirm A4 and could
miss a refutation entirely.  The torus evidence bounds the *slope*, not the
*surplus*, and the surplus is the whole content of the conjecture.

Two further results from the same panel, both checked against the transcript:

* The refutation criterion applies to spatially periodic rows with a **temporal
  transient**, not only to rows lying on a cycle.  `torus_search.py` peels to the
  cycle states and so does not cover that case; its negative result is therefore
  narrower than stated above.
* Every bi-infinite predecessor of an `S`-periodic row has period dividing `qS`
  for some `q <= 4`, which makes the backward basin of a given torus a finite
  search.  The panel exhausted it for the space-7 torus with no refuter.
* `H(10) = 79` already forces `c >= 9`, so the constant in A4 cannot be smaller.

Panel verdict after three rounds and six executed programs:
`TARGET_NEITHER_PROVED_NOR_REFUTED`.

*These are two different relaxations and their numbers are not comparable.*  The
one-step condition couples adjacent times, so for a word whose centre-zero times
are non-adjacent — the alternating word included — it constrains nothing between
consecutive samples.  On `01` it gives `H = 1, 7, 17, 23, 33` for `K = 0..4`
against the no-`11` table's `1, 7, 17, 21, 28`.  Strictly weaker, hence strictly
larger `H`, hence a terminating search there is a *stronger* statement.

Swept over **all 52 nonconstant words of period 2 through 5, every phase**, every
search terminates at `K <= 5` under the weak model.  Weak-model depth gained per
additional one, by period:

```text
period 2:  3.6 .. 7.6     period 4:  1.8 .. 8.4
period 3:  3.0 .. 7.8     period 5:  1.8 .. 7.0
```

The minimum rate does not collapse as the period grows (3.6, 3.0, 1.8, 1.8), and
the extreme is the proved case: the all-one word gives rate exactly 2, which is
the checkerboard left tail at density 1/2.  Phase matters as much as period.
Four periods is not a trend, and these rates are weak-model rates: the
corresponding no-`11` rates for period 2 are lower.

**Sharp benchmark.**  The space-7/time-4 torus (rows `0000001`, `1000011`,
`0100110`, `1111101`, cyclic; all 28 updates close) is a genuine infinite Rule 30
spacetime with exactly alternating centre whose left row has ones at depths
`1, 8, 15, 22, ...`.  So `H(K) >= 7K` holds even over actual-right
configurations, and no universal support density above `1/7` is provable.
Measured `H_01(K)` equals `7K` exactly at `K = 1,3,4,5,7,8,9` and exceeds it only
at `K = 2,6,10`, so the torus is very nearly extremal.

**The branch cost has a closed form, and it generalises.**  Reparameterise the
free choice by the next initial-row output `p = L_(T+1)`; the required source bit
is `rho(p) = 1 XOR parity(o) XOR p`.  Feeding the next value, flipping `p` flips
every entry of the intermediate diagonal (the `C` recurrence is an XOR scan), and
since `(a OR b) XOR ((1 XOR a) OR b) = 1 XOR b`, the induced change in the
following output is

```text
delta = ((T+1) mod 2)  XOR  c_T  XOR  parity(A_1..A_T)
```

so the two branches emit `(0, q_0)` and `(1, q_0 XOR delta)` at costs
`kappa_0 = q_0` and `kappa_1 = 1 + (q_0 XOR delta)`.  Verified with 0 violations
over 2,520 reachable states across seven words of period 2 to 5.  The centre word
enters through the single bit `c_T`; dropping that term — correct only where the
phase pins `c_T = 0` — fails on 2,560 of those states.  This does **not** make
`(q_0, delta)` a closed state: the ordered `A` and `B` are still required.

**What this leaves open is one statement, and it is the same one as above.**
Every state has at most one zero-cost successor (it needs `p = 0`, `q_0 = 0`, and
a legal source bit; every `p = 1` branch spends at least one).  Writing `Z` for
that partial deterministic map: *every finite support budget is eventually
exceeded* if and only if *no frontier reachable from a finite legal prefix has an
infinite legal `Z`-orbit*.  An infinite path of bounded integer cost has finitely
many positive-cost edges and follows `Z` after the last one; conversely finite
branching turns arbitrarily deep budget-respecting paths into an infinite one.
Support count prices branching but does not rank zero-cost motion, so the
remaining obligation is a well-founded quantity on zero-cost states.  The known
ten-macro adversary (source `010101001010101010101000100010`, 17 ones by depth
60) holds the cost fixed while the frontier keeps changing; its source contains
the forbidden actual-right factor `101001`
(`RESULTS-RIGHT-FILTERED-MORTALITY.md`), so it is not an actual-right
counterexample, but it does rule out any fixed-constant bound on zero-cost runs.

## PROVED: zero-cost motion is exactly iterated suffix parity, with one OR overlap

Under **zero support cost** the frontier scan collapses to a closed form, and the
next macro's OR parity has an exact affine expression.  Write `S` for suffix
parity, `S(X)_j = XOR_(i>=j) X_i`, and `H_1(X)` for the XOR of the odd-indexed
entries `X_1, X_3, ...`.

**Lemma (suffix parity).** `parity(S(X)) = H_1(X)`.
*Proof.* `XOR_j XOR_(i>=j) X_i = XOR_i i*X_i mod 2`. ∎

**Lemma (zero-cost normal form).** Zero output at a free feed forces
`v = parity(O)`, hence

```text
C = S(O)  with  C_(T+1) = 0,     and, if the pin survives (parity(P) = 1),
D = S(P)  with  D_(T+2) = 0.
```

*Proof.* `C_j = v XOR (O_1 XOR .. XOR O_(j-1))`; substituting `v = parity(O)`
leaves the suffix. Same for `D` with `w = 1`. ∎

So an immortal zero-cost orbit iterates, with no freedom left at all,

```text
O = A OR (1.B),   C = S(O),   P = C OR (0.A),   D = S(P)
```

subject only to the pin condition `parity(P) = 1` and right-realizability.

**Lemma (next OR parity).** With `Omega(D,C) = XOR_j D_j C_(j-1)`,

```text
pi_next = c_(T+1) XOR H_1(O) XOR H_1(P) XOR Omega(D,C)
```

*Proof.* The next OR word is `O'_j = D_j OR C_(j-1)`, `j = 1..T+2`, `C_0 =
c_(T+1)`.  Over `F_2`, `a OR b = a XOR b XOR ab`, so `pi_next = parity(D) XOR
c_(T+1) XOR parity(C) XOR Omega`.  By the suffix-parity lemma
`parity(D) = H_1(P)` and `parity(C) = H_1(O)`. ∎

Checked with 0 violations over 349,440 arbitrary frontiers at `T = 3..8`
(174,552 surviving the pin).  **The leading constant is the centre bit
`c_(T+1)`, not `1`**: fixing it to `1` — correct only at the phase-01 macro
boundary — fails on exactly half the surviving states.  As with the branch
`delta` above, the centre word enters through a single bit, so this carries to
any period with a period-`p` clock.

*Consequence for the mortality target.* The first three terms are exactly the
higher-moment terms produced by iterating suffix parity.  The whole obstruction
is the single nonlinear term `Omega(D,C)`, and it is now resolved:

**Lemma (Omega closed form).** With `C_0 = c_(T+1)`,

```text
Omega = D_1 c_(T+1)  XOR  XOR_(i=1..T+1, m=1..T) [min(i-1,m) mod 2] P_i O_m
```

*Proof.* Drop the vanishing `j = T+2` term, split off `j = 1`, and substitute
`D_(k+1) = XOR_(i>k) P_i`, `C_k = XOR_(m>=k) O_m`.  For a fixed pair `(i,m)` the
number of `k` in `[1,T]` with `k < i` and `k <= m` is `min(i-1,m)`, so over `F_2`
that pair survives exactly when `min(i-1,m)` is odd. ∎

Verified with 0 violations over 87,376 assignments, `T = 1..7`.  So the entire
nonlinear obstruction is **one bilinear form** with coefficient matrix
`M[i][m] = min(i-1,m) mod 2`.

**Lemma (full rank).** `rank_(F_2) M = T` for every `T`.
*Proof.* `row_i XOR row_(i+1)` is the suffix indicator `0^(i-1) 1^(T-i+1)`, for
`i = 1..T`.  These `T` vectors are triangular, hence independent, so
`rank >= T`; `M` has `T` columns, so `rank = T`. ∎
Confirmed by computation at every `T` from 2 to 64.

**`Omega` does not telescope into any bounded moment family, and provably not.**
Full rank means it needs `T` independent `(linear in P) x (linear in O)`
products, growing one-for-one with the frontier.  No fixed collection of Hasse
or mixed moments can capture it at any size.

This is the outcome the increasing-order ladder needs, not a kill.  The archive's
existing negative result rules out *fixed* moment summaries; full rank shows the
obstruction is genuinely unbounded-order, so a bounded invariant was never
available and the ladder is the only shape that can work.  Stated in the natural
basis the result is simply that **the whole nonlinear term is the shifted inner
product of the two frontier diagonals**, `Omega = <D, shift(C)>` over `F_2`.

**What full rank does NOT give, stated so it is not misread.**  Rank is a fact
about the *ambient* variables.  The reachable zero-cost orbit is not the whole
vector space; it is a growing algebraic subset cut out by the recurrence, and a
finite seed generates unboundedly many frontier bits along it.  So "the ambient
form needs `T` parameters" does not yield "the constraints on the seed become
overdetermined".  Measured: over every frontier surviving the pin, `Omega` is
**exactly 50/50** at each `T` from 3 to 10 (at `T = 10`, 1,048,576 each way).
`Omega` is not driven anywhere, and any argument whose engine is "`Omega` is
eventually forced" is refuted rather than merely unproved.  An external note
claiming a period-two proof on that basis was rejected for this reason.

**The correctly stated remaining target (pullback independence).**  Let `X` be a
finite `rho`-prefix and `E_m(X)` the `m`-th pin condition pulled back through the
actual recurrence.  Needed:

> `E_0(X) = E_1(X) = ... = E_m(X) = 1` has no solution once `m` exceeds a finite
> function of `|X|`.

Equivalently: each successive pin condition contributes a term — moment, interval
product, or frontier incidence — absent from its predecessors.  That converts
full rank from "large ambient object" into "a new independent obligation per
step", which is what mortality needs.  Note the argument must hold for *every*
finite support bound, not one tied to the original single-cell seed: at an
eventual period-two onset the translated configuration is finite but its support
is unbounded in the onset time.

Use the interval-overlap reading of `Omega`, not its algebra.  After the knee the
orbit is deterministic — the free feed is forced to `v = parity(O)` — so the whole
question is how many consecutive parity checks a finite prefix can pass.

**Mortality needs finiteness per state, not a uniform bound.**  `survival(state)
< infinity` for every state *is* the theorem.  A uniform bound was never
required, so no uniform-bound conjecture is worth defending.  Correspondingly,
search can only lower-bound the max: it cannot separate "dies at macro `10^6`"
from immortal, and every measured survival number is evidence, never convergence.

**KILLED: twelve candidate well-founded charges.**  Tracked along 932 orbits of
survival `>= 8` (3,638 macro transitions).  None is a depleting resource:

```text
popcount(O), popcount(P), runs(O), runs(P), |O|-|O|_1, first1(P), Omega
        all increase on a substantial fraction of macros
last1(O), last1(P), T-last1(O), T-last1(P)
        increase by exactly +1 on EVERY macro -- clocks, not resources
first1(O)
        non-increasing but vacuous: the pin gives D_1 = parity(P) = 1, so
        O+_1 = D_1 OR c = 1 and first1(O+) = 1 unconditionally after one macro
```

*Proved en route (0 violations over 4,038 macros).*  `last1(D) = last1(P)`,
`last1(C) = last1(O)`, and `last1(P+) = last1(P) + 1` exactly.  The deepest 1
advances one position per macro while the frontier grows by two, which is why
every depth-derived quantity here is a clock.  Any future charge proposal must
first be checked against this list; a charge built on the deepest 1, on either
weight, or on run counts is already dead.

## PROVED: the reversed triangular form, and constant terminal scalars are bounded

A strictly better coordinate system for the zero-cost dynamics, due to an
external panel (`experiments/rule30/panel/`), **verified here to be exactly
equivalent** to the macro above.

Let `r = last1(A)` and reverse both words about it: `a_k = A_(r-k)`,
`b_k = B_(r-k)`, `0 <= k < r`, so `a_0 = 1`.  Then with
`u_(-1) = v_(-1) = a_(-1) = 0`,

```text
v_k = v_(k-1) XOR (a_(k-1) OR b_k)
u_k = u_(k-1) XOR (v_k OR a_k)

survival  <=>  u_(r-1) = v_(r-1)
on survival:  a' = (u_0..u_(r-1), 1),  b' = (v_0..v_(r-1), 1 XOR v_(r-1))
```

*Verified equivalent:* over every `(A,B)` with `T = 2..8`, at the alternating
phase `c_(T-1) = 1, c_T = 0`, this agrees with `zero_cost_macro` on **36,402
frontiers with 0 survival disagreements and 0 next-state mismatches**.  `c_next`
is correctly irrelevant, since it enters only `Omega` and not the survival test.

Why this is better than the `(A,B)` frontier.  The update is **triangular** —
site `k` never depends on any larger index — so a fixed prefix is autonomous.
The state grows by exactly one site per macro.  Survival is a single equality at
the moving boundary rather than a global parity.  And `b_0` is invariant, giving
two sectors `beta = b_0 in {0,1}`.

**Consequences established by the panel** (proofs in `panel/transcript.md`; the
first is verified here, the rest are recorded as its claims):

* *Constant terminal-scalar runs are bounded.*  With `s_n = v_(r-1)` the scalar
  appended at macro `n`, a run of surviving macros all sharing one scalar, begun
  at active length `r`, has length `L <= 2r - 1`.  The argument turns a constant
  moving-boundary signal into a temporally alternating diagonal pair at the fixed
  site `K = r-1`, propagates it backward one site at a time, and contradicts the
  invariant `a_0 = 1`.  **Checked here: 0 violations** over all 698,538 starts
  with `r <= 10` and 300,000 sampled starts to `r = 20`.
* Hence an immortal zero-cost survivor **must switch its terminal scalar
  infinitely often**.
* Every autonomous fixed prefix through site `K` is eventually periodic with
  period dividing `2^K`, and through site 4 each sector has a unique attracting
  four-cycle.  So mortality is not a fixed-window aperiodicity question; it is
  entirely about the moving terminal test.
* Claimed but NOT verified here: alternating terminal-scalar tails are also
  excluded, leaving immortality to require a tail that is neither eventually
  constant nor eventually alternating.

*Exhaustive survival in these coordinates*, max over ALL starts at active length
`r` (this is complete, not sampled, for `r <= 10`):

```text
r  1  2  3  4  5  6  7  8  9 10 | 12 14 16 18 20  (sampled)
L  2  1  3  3  7  7 10  9 13 12 | 11 13 14 13 13
```

Note `L <= 2r-1` is loose in practice: the longest constant run observed at
`r = 10` is 5 against a bound of 19.

### The well-founded quantity is the REACHABLE SET's cardinality, not a charge

This reframes the killed charge searches below.  Every one of them looked for a
function of a *state*.  `|S_R|`, the number of distinct reachable states at layer
`R`, is a non-negative integer that decreases, and no per-state charge could see
it because it is a property of the ensemble.

**PROVED, trivially.**  `S_(R+1)` is the image of `S_R` under a partial function,
so `|S_(R+1)| <= |S_R|` always.  Confirmed at every layer measured.

**Measured, seeded from a single length so there is no contamination:**

```text
r0 = 12:  8,388,608 -> 9,800 -> 1,768 -> 485 -> 190 -> 83 -> 43
                    -> 25 -> 13 -> 8 -> 4 -> 2 -> 0      extinct at R = 24
r0 = 10:    524,288 -> 1,681 -> 371 -> 118 -> 46 -> 24 -> 7
                    -> 5 -> 2 -> 2 -> 1 -> 1 -> 0        extinct at R = 23
```

**This is mortality for every state of length `r0`, computed directly.**  At
`r0 = 12` that settles all `2^23` states while never holding more than 9,800 at
once.  The macro is violently non-injective: 8.4M states collapse to 9,800 in one
step, a factor of 850.  Compare `cert33.py`, which needed `2^17` lanes for
`q <= 17`; forward-image is far cheaper for the same kind of result, and the
binding cost is enumerating the *domain*, not handling the image.

**The sharpened target.**  A non-increasing sequence of non-negative integers is
eventually constant, so immortality requires an infinite tail with
`|S_(R+1)| = |S_R|` and `S_R` nonempty.  That equality holds exactly when **no
state dies and the macro is injective on `S_R`**, simultaneously, forever.  Both
conditions are observed to fail: deaths occur at every measured layer, and
injectivity is intermittent (false at `R = 13..17` and `19`, true at `18`, `20`,
`21`, `22`, `23`).  Excluding an infinite death-free injective tail is the
remaining obligation, and unlike a Lyapunov charge the decreasing quantity here
provably exists and is provably bounded below.

**The endgame is explicit.**  At `r0 = 12` the reachable set is 8 states at
`R = 21`, 4 at `R = 22`, and 2 at `R = 23`:

```text
a=10101010100101001100101   a=10101010101001010101011
b=10110101010010101010101   b=10110101011101010101010
```

A finite endgame on two named states is a different problem from a search over
`2^33`.

### RESOLVED: the one-step image, with no domain enumeration

`experiments/rule30/image-dfa/image_dfa.py`, cross-checked by
`test_image_dfa.py` (9 checks, including the macro against `cert33.direct_step`
over all `2^(2n-1)` states for `n <= 8`).

**The macro is a letter-to-letter sequential transducer with three bits of
memory.**  Reading `(a_k, b_k)` it emits `(u_k, v_k)` and carries
`h = (u, v, alpha)`; it survives iff `u = v` at the end, then appends one
symbol.  Hence *the image of any regular set of states is regular*, by subset
construction on `Q x 8` — the domain is never enumerated.

**The whole one-step image is an 11-state DFA.**  That is the direct description
the previous draft of this paragraph asked for.  Its per-length counts are exact
and have a closed form: writing `a(q)` for the image of all `2^(2q-1)` states of
length `q`,

```text
a(q) = 2a(q-1) + a(q-2) + (-1)^(q+1),        a(1) = a(2) = 1
a(4m)   = 2 * Pell(2m)^2      a(4m+2) = NSW(m)^2
```

verified to `q = 58`.  So `1,681 = 41^2` and `9,800 = 2 * 70^2`, and the growth
rate is `(1 + sqrt 2)^q` against the domain's `4^q`.  **The "850x collapse at
`r0 = 12`" is not a feature of that length**; it is the generic thinning ratio
`(4 / (1 + sqrt 2))^q`, which keeps growing.  Nothing distinguishes `r0 = 12`.

Iterating reproduces every measured row exactly, from the DFA alone:

```text
R          0        1      2     3    4   5   6   7
minimal states     3       11    25   68  207 776 3354 18258
seed 10:   524,288  1,681  371  118   46  24   7    5
seed 12: 8,388,608  9,800 1,768 485  190  83  43    -
```

**But the conclusion drawn in the previous draft is refuted.**  It read: "if the
image admits a direct description, `q` goes far past 17, since enumeration of the
domain is the only wall."  The domain was *not* the only wall.  The image DFAs
grow by a factor of roughly 5.4 per layer and blow the 400k-subset cap at
`R = 8`; certifying seed length `q` needs `R ~ 2q`, so this reaches no further
than `cert33.py` did.  The wall moved from the domain to the image, and the
gain is qualitative, not quantitative: for any `R` reached, the DFA settles
**every** seed length at once, including lengths no enumeration could touch.

Independent corroboration: the minimal seed length surviving `R` macros is
`1, 1, 3, 5, 5, 5, 5` for `R = 1..7`, agreeing with the survivor-language DFAs
built by a different construction in `panel/transcript4.md` (astra, round 4).

### PROVED: no interface can absorb a left perturbation; and the "ether" exists

`experiments/rule30/ether-interface/truncated_torus.py`.  This closes off a
whole class of proposed constructions, in both directions.

**Lemma (unconditional front).**  If `x` and `y` agree at every site `> i` and
differ at `i`, then `F(x)` and `F(y)` agree at every site `> i+1` and differ at
`i+1`.
*Proof.*  `x(t+1, j) = x(t, j-1) XOR (x(t, j) OR x(t, j+1))`.  For `j > i+1` all
three inputs agree.  At `j = i+1` the `OR` term reads sites `i+1, i+2`, which
agree, while the `XOR` term reads site `i`, which differs; `XOR` is a bijection
in that argument. ∎

**Corollary.**  Two configurations whose leftmost difference is at `-d` have
*different* centre columns at exactly time `d`, and **nothing to the right of
`-d` can change this**.

So an interface that "absorbs or cancels the incoming wave at `x = 0`" cannot
exist, for any algebra.  Cancellation would require the arrival to depend on the
medium, and left-permutivity makes it unconditional.  The lethal wave is also
*right*-moving, not left-moving: a right-hand ether is attacking the wrong side.
Measured, tiling the space-7/time-4 torus to `L` periods left and `R` periods
right of the centre, the centre stays alternating until exactly `t = 7L + 1`,
independent of `R` over `R = 2..128`.

**The positive half of the same fact.**  The torus itself *is* the requested
ether, and it works: it is a genuine infinite Rule 30 spacetime with an exactly
alternating centre column, forever.  No local or interface property forbids a
periodic centre.  Finiteness of the support is the entire hypothesis, and it
enters only through the support count `H(K)`.

**Consequence for the proof search, and it is a hard constraint.**  The torus
truncated to `L` periods and the true torus agree on every window of radius
`< 7L` about the centre.  Therefore *no invariant computed from a fixed-radius
window can separate an immortal configuration from a mortal one*: any working
certificate must be non-local at a scale that grows with time.  This is an
independent structural reason the fixed-order moment families and the per-state
Lyapunov charges failed, and it does not rely on the `Omega` 50/50 measurement.
It also says the support-count route is the right shape, since `H(K)` is
precisely a quantity with no bounded-radius description.

### PROVED AND EXECUTED: zero-cost mortality for every initial length q <= 17

The first executed closure in this line.  `experiments/rule30/panel/cert33.py`,
constructed by panel 3 (`transcript3.md`, astra-pro round 5) and run here.

**Sector-assisted reconstruction.**  For `h >= 1`, a surviving state at length
`R = 2h+1` that has emitted at least `h` scalars is determined by its latest `h`
scalars **together with its invariant sector `beta`**.  The conservative
actual-history bounds `h_F(d) = 1+floor(d/2)`, `h_G(d) = 1+ceil(d/2)` make `F_d`
valid for `d <= 2h-1` and `G_d` for `d <= 2h-2`, which fixes `a_k` for `k >= 1`
and `b_k` for `k >= 2`.  The three missing coordinates are supplied by the
sector: `a_0 = 1`, `b_0 = beta`, and `b_1 = 1 XOR beta` (since `v_0 = beta` and
`v_1 = v_0 XOR (a_0 OR b_1)`).  So `2^(h+1)` lanes cover layer `2h+1`.

This repairs the P5 problem recorded below.  P5 as literally stated is false by
counting; supplying `beta` separately rather than reconstructing it from the
scalar history is what makes the covering construction sound.

**Executed result.**  `h = 16`, layer 33, all `2^17 = 131,072` covering lanes
carried bit-parallel through the direct triangular macro:

```text
COVER SELF-TEST PASS: 125
STEP  0  LENGTH 33  LIVE 131072
STEP  4  LENGTH 37  LIVE   8449
STEP  8  LENGTH 41  LIVE    568
STEP 12  LENGTH 45  LIVE     30
STEP 13..15         LIVE     26   (plateau)
STEP 16  LENGTH 49  LIVE      0
CERTIFIED 33 16
```

Hence **every initial state of length `q <= 17` satisfies `L < 49 - q`**.  A
state surviving `33-q` macros reaches length 33 having emitted at least 16
scalars, so sector-assisted reconstruction places it in one of the lanes;
emptying the live mask means none survives 16 further macros.  States dying
before length 33 already satisfy the bound.

*Independently checked here.*  The certificate's `direct_step` was compared
against the verified macro in `experiments/rule30/alt-trace-frontier/frontier.py`
over **699,050 states with 0 disagreements**, and the bound holds against
exhaustive truth (`q = 10`: observed max `L = 12` against bound 39, loose as
expected).  The program's own cover self-test validates the reconstruction
identity against direct evolution from every initial state of lengths 1..6.

**Scope, stated exactly.**  This is mortality for a bounded family, not the
period-two exclusion.  It settles all `2^33` states of length `<= 17` by a
computation over 131,072 lanes, but says nothing about arbitrarily large initial
lengths, and an eventual period-two onset has unbounded support.  Both panellists
state this explicitly and neither claimed otherwise.

Also proved by panel 3, unverified here: every eventually periodic terminal
scalar tail is excluded, for every period.  With that, an immortal survivor's
scalar tail must be aperiodic.

### Panel round 2: a proposed finite extinction certificate (UNVERIFIED)

`experiments/rule30/panel/transcript2.md`.  Recorded as claims; only the last
item was tested here, and the test was near-vacuous.  Do not build on these
without checking them.

Claimed, in the triangular coordinates above, with `s_n` the terminal scalar and
`M(R) = 1 + floor(R/2)`:

* A period-`p` scalar run from active length `r` has `L <= r + 2p - 1`; at
  `p = 2` this gives `L <= r + 27` via an exact period-28 boundary-depth cycle.
  Hence an immortal survivor's terminal scalar is **not eventually periodic of
  any period**.
* *Suffix reconstruction:* at length `R`, the last `M(R)` emitted scalars
  determine the entire state, including `beta`.
* Hence survival is a unique scalar extension preserving the reconstructed
  site-zero pair `(1, beta)`, and mortality is equivalent to the absence of
  infinite paths in a layered "anchored word" graph whose layer `R` has at most
  `2^M(R)` vertices, each of outdegree `<= 1`.
* **Extinction of anchored layer `2r+1` certifies mortality for every initial
  length `<= r`.**  A state surviving `r+1` macros reaches length `2r+1` having
  emitted `r+1 = M(2r+1)` scalars, so suffix reconstruction represents it as an
  anchored vertex there.

If sound, this converts mortality-for-all-states-of-length-`<= 16` from `2^31`
frontier states into **`2^17 = 131,072` words at layer 33** — a finite,
runnable certificate rather than a search.  That is the first proposal in this
document that could settle a nontrivial range of `r` outright.

*Tested here, and the test proves almost nothing.*  Suffix reconstruction had
**0 collisions**, but over only **15 distinct `(R, scalar-suffix)` keys**:
states die too fast (max survival 13) to accumulate `M(R)` scalars, so almost
nothing reaches the regime the lemma is about.  The lemma is not supported by
this check; it is merely not yet contradicted.

*Also recorded:* the panel refuted two claims made inside it — a flat assertion
that period two is proved impossible for finite configurations, and a shift
error giving `G_5`, whose correct value is `w_0 XOR w_1 XOR w_2`.  Cycle
detection on the layered graph is vacuous, since every edge increases `R` so no
directed cycle can exist.

**KILLED: the whole local-count Lyapunov class.**  An external LP screen over all
700 unique zero-cost transitions generated by no-`11` prefixes of length `<= 16`
(6,762 seeds) sought a nonnegative linear potential strictly decreasing on every
transition, over counts of all blocks of length `<= r` in `O`, in `P`, and in the
aligned pairs `(O_j,P_j)`, plus boundary/length/trailing-zero features, words both
full and trimmed past their final 1.  **Infeasible at every `r <= 4`, both
trimmed and untrimmed.**

*Checked here, because that screen had a bias.*  The words grow by exactly 2 per
macro, and raw `popcount(O)` drifts up `+0.859` per macro on average, so a
nonnegative-weight LP over raw counts is pushed toward infeasibility mechanically.
Normalising removes the bias and the class still dies: `wtO/n`, `wtP/n`,
`runs(O)/n`, `runs(P)/n`, `zeros(O)/n` and `(wtO-wtP)/n` each increase on ~45% of
transitions, symmetrically, over 2,284 transitions from 252 orbits of survival
`>= 9`.  So the kill is not a scaling artefact and it covers the density class the
LP did not.

*Still open within charges.*  A well-founded charge need not decrease at every
step.  Decrease over a bounded window, a lexicographic pair, and ordinal-valued
charges are all untested and none lie in the screened class.

*Measured survival landscape (not a bound).*  Max zero-cost survival over random
frontiers: 13, 13, 14, 15 at `T_0 = 10, 16, 24, 32`.  An independent
implementation dropping some of these conditions reports 14, 15, 17, 18 at
`T_0 = 10, 16, 24, 40`, which is correctly at or above these.  Slow,
non-monotone growth; no plateau; nothing near immortal found by random or
evolutionary search.

*Do not pursue a constant zero-gap bound.*  Measured over every finite right half
of width 8..13 with an alternating centre, the longest **interior** zero run of
the reconstructed left row is 12 at reconstruction depth 34 and 14 at depth 60,
**at every width**.  The statistic is a function of the observation depth, not of
the right width, so reports of a gap bound "breaking" at some larger width are
reading the same depth artifact that makes the trailing zero block grow.  There
is no constant to find.  The correct resource remains total support.

*Provenance:* the frontier state, scan law and parity output are this document's
own (next section).  The support-count budget and the `K <= 26` tables are from
an external continuation, independently reproduced here at `K <= 10` in both
phases.  That continuation also supplied the zero-cost normal form and the shape
of the next-OR-parity identity as a finite check at lengths 4, 6, 8.  The period
2-5 sweep, the generalised `delta`, the near-extremality of the torus, the proofs
above, the `c_(T+1)` correction, and the interior-gap measurement were done here.

## PROVED: the survivor automaton is a parity-checked deterministic map

This resolves the A1 instrumentation question ("build the exact transducer
on reconstruction wavefronts") in closed form.

**Setup.**  Reconstruct incrementally.  After consuming `T` column `-1`
values `l_0..l_(T-1)`, the forced triangle's frontier is the pair of
anti-diagonals

```text
A_j = x(T-j, -j)     (t + j = T,   j = 1..T)
B_j = x(T-1-j, -j)   (t + j = T-1, j = 1..T-1)
```

Consuming `l_T = v` computes the next anti-diagonal `C` shallow-to-deep by
the rotated rule `x(t, -(j+1)) = x(t+1, -j) XOR (x(t, -j) OR x(t, -(j-1)))`:

```text
C_1 = v,   C_(j+1) = C_j XOR o_j,   o_j = A_j OR B_(j-1),   B_0 := c_(T-1),
```

and its deepest entry is the one new forced output
`L_(T+1) = x(0, -(T+1)) = C_(T+1)`.

**Closed form.**  The XOR chain never absorbs, so it telescopes:

```text
L_(T+1) = v XOR parity(o_1 .. o_T).
```

The new output is the fed column `-1` value XOR the parity of the OR-word
of the two stored diagonals.  That is the whole transducer.

**Consequences.**  A configuration of left depth `<= d` has `L_j = 0` for
all `j > d`.  Once `T >= d` (the knee, level `k = d/2`), every step is
constrained:

* zero-set steps feed `v = NOT rho_k`, so the surviving rho bit is
  **forced**: `rho_k = 1 XOR parity(o)`.  Branching factor exactly 1.
* pinned steps feed `v = 1` with no freedom, so survival requires
  **`parity(o) = 1`**, one pure parity check on the state per level.

So past the knee the fiber BFS is a set of non-branching orbits of a
parameter-free deterministic map (`A' = C`, `B' = A`, `v` forced), each
killed at its first pin-parity failure.  This explains the observed
halving per level (the checks empirically pass ~1/2 the time: 2082/4096 at
the `d = 24` knee), and gives

```text
k(d) = d/2 + (longest forced-orbit survival from a depth-d seed) + 1.
```

**Verification** (all machine-checked, `--parity D`):

* Controls C6 (incremental frontier equals `left_from_rho`, 64 random rho,
  both phases) and C7 (incremental BFS equals the `violates()` BFS,
  survivor-set equality per level, `d = 6, 10`, both phases).
* The closed form reproduces the alive/dead status of **every** BFS
  transition at `d = 16, 24, 32`, both phases (203/133, 2008/1322,
  19108/12981 post-knee states respectively), and the forced-rho /
  branching-1 / pin-parity claims hold on all of them.
* Certificate levels reproduced: 16/16 (`d=16`), 22/21 (`d=24`).
  **Prediction confirmed:** from the `kseed = 16` orbit maximum (16, below)
  the formula predicts `k(32) = 33`; the direct `d = 32` run then certified
  at level 33, both phases.

**Forced-orbit measurements** (`--orbit K`): iterate the forced map from
every rho-seed of length `kseed`, requiring all post-seed outputs zero.
Survival to first pin failure is geometric-ish with mean ~1; the maxima
grow roughly linearly:

```text
kseed:          8   12   16      (exhaustive, both phases)
max survival:   7    9   16
```

matching, for phase `01`, `k(16) = 8+7+1`, `k(24) = 12+9+1`,
`k(32) = 16+16+1` exactly.  (Phase `10`'s leading pin shifts its seed
correspondence to odd effective `d`, so its levels can differ by one:
`k(24) = 21` there.)  No seed survived past its cap (kill condition did
not fire).  Linear growth of the
maxima means per-`d` certificates can never reach uniformity by themselves;
the theorem must come from the map.

**The open target, restated exactly.**

> No finite seed (frontier pair of a finite rho-prefix triangle) follows
> the forced map with every pin parity equal to 1 forever.

A1's "zero-emitting cycle" is now concrete: an orbit of this parameter-free
map passing every pin check.  One reachable from a finite seed is a
left-finite counterexample.  The wallpaper member `{1,4}` shows
infinite-left seeds CAN pass forever-adjacent structure (its outputs
contain ones at unbounded depth, so it violates every finite `d`; no
contradiction), so any proof must again use left-finiteness of the seed.
The raw state (the diagonal pair) grows by one cell per step, so
finiteness is not available in raw form; the remaining hunt is a finite
invariant of the forced map sufficient to force a pin failure — e.g. the
dynamics of the OR-word `o` itself, or a weight/potential argument on ones
density in `A` under the forced update.

## VERIFIED: the fiber over the alternating trace has left-periodic members

Right half `{1,4}` (i.e. `R_1 = R_4 = 1`), phase `01`: the forced left half
is spatially 7-periodic, word `0110010` repeating from depth 1, verified to
depth 1024; the left half-plane is a 7 (space) x 4 (time) wallpaper.  Its
`rho` is the alternating sequence, verified to `t = 20000` by driven
simulation.  At `W = 10`, 20 of 1024 right halves force 7-periodic tails in
the same rotation class.  Driven-column periods for `{1,4}`: columns 1..6
have period 4, columns 7..14 period 8, columns 15+ none `<= 64` in the
sampled window; the period-doubling profile matches the known nested edge
structure (Rowland 2006), which is the natural route to proving the lock.

Status: the infinite wallpaper member is **not proved**; the `rho` lock is
empirical.  What it already establishes is sharpness: the fiber contains
left-periodic members, so any exclusion must use left-finiteness itself.
The C_m analogue for period two is "forced ones at unbounded depth", not a
single forced tail; forced tails here vary with `rho` (most look chaotic).
No finite candidates among all right halves at `W=10, D=192` or `W=12,
D=288`, either phase.  Max forced-zero gap 15 (phase `01`) and 16 (phase
`10`), identical at `W=10` and `W=12`: the gap did not grow with the right
radius, consistent with a uniformly bounded forced-one density.

## Controls

All embedded in the probe and asserted before any measurement:

* C1 zero-trace fiber reproduces the prefix-OR classification (Theorem 2 of
  the note) over all `2^8` right halves.
* C2 all-one-trace fiber reproduces the checkerboard.
* C3 alternating stencil `L_1..L_4` matches the recorded stencil.
* C4 forward brute force reproduces the SMT `p=2` horizon row `6,6,6,6,8,9`
  for `w = 1..6` (independent encoding: row-as-integer evolution).
* C5 the `rho` reduction matches direct fiber reconstruction on random right
  halves, both phases.
* Rule 90 note: the same enumeration under rule 90 (`W=8, D=128`) also finds
  no finite member of its alternating fiber, so this exclusion is not
  automatically Rule-30-specific.  That is acceptable for a per-trace partial
  result; the `PATH.md` filter lesson applies per trace (rule 90's actual
  eventually periodic column is the zero trace, whose exclusion is exactly
  what fails for rule 90).

## Falsified along the way

The 7-periodic tail word was first read off a window as `1001100` and
transcribed to depth 1 in the wrong rotation; the depth-1 word is `0110010`.
The probe pins the correct alignment.

## Next targets, with kill conditions

* **A1, survivor automaton — instrumentation DONE, reduced to the parity
  question.**  The exact transducer is the parity-checked deterministic map
  above.  Remaining: prove no finite seed passes every pin-parity check
  forever.  Candidate angles: dynamics of the OR-word `o` under the forced
  update; a potential/weight argument on ones density; eventual periodicity
  classification of forced tails (the wallpaper is the eventually-periodic
  infinite-seed example).  Kill: a seed whose forced orbit survives an
  unbounded run (that is a left-finite counterexample and settles period
  two the other way); exhaustive seeds to `kseed = 16` all die within 16
  steps.
* **A2, wallpaper theorem.**  Prove the `{1,4}` lock by finite column-band
  certificates in the driven half-plane (Rowland-style nesting).  Kill: a
  lock break at some larger `t`; then the 7-periodic family claim is
  withdrawn as a transient.
* Strong outcome for the arm: "no left-finite configuration has exactly
  alternating central trace", which yields: no finite configuration has an
  eventually 2-periodic nonconstant center column.  That is the first
  nonconstant entry in Kari's requested sequence.

## Reproduction and spending

From `experiments/rule30`:

```bash
uv run python alt_trace_fiber_probe.py                 # controls + d<=16 + W=10 + wallpaper
uv run python alt_trace_fiber_probe.py --certify 24
uv run python alt_trace_fiber_probe.py --enumerate 12 288
uv run python alt_trace_fiber_probe.py --automaton 24 --dump ../../runs/alt-trace-automaton/d24-outputs.json
uv run python alt_trace_fiber_probe.py --parity 32     # closed form vs BFS, k(32)=33
uv run python alt_trace_fiber_probe.py --orbit 16      # forced-orbit survival, exhaustive seeds
```

Per-level survivor state dumps for `d = 8, 16, 20, 24` are in
`runs/alt-trace-automaton/`.

Modal: $0.  Paid model-provider calls: $0.  Everything above ran locally;
the largest single run (`--parity 32`) took about four minutes.

## Episode-composition follow-up, 2026-09-09

The constant-scalar bound `2r-1` above remains valid and now sharpens to
`r-1` for a scalar-zero episode and `r` for a scalar-one episode begun at
active length r. The proof applies at every episode onset, including
frontiers carrying earlier history.

An exact composition law now factors each update at any spatial cut into
an autonomous forward prefix and a terminal-driven backward suffix, with
a two-bit matching condition at every intermediate step. The accumulated
suffix crosses each variable-length episode boundary unchanged by any
reset. A concrete reset produces a false continuation.

See [RESULTS-variable-length-episode-composition.md](RESULTS-variable-length-episode-composition.md)
for the uniform proofs and verification. This proves an episode interface
and bounds individual episodes; it does not prove that an infinite
sequence of episodes is impossible or close the uniformity gap.

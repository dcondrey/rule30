# Rule 30 zero-tail theorem and exact inverse constraint search

## Status

**PROVED.** No nonzero finitely supported Rule 30 configuration has an
identically zero future center trace.

This is a new partial theorem for the center-column problem, subject to the
literature audit below.  It rules out an eventually constant-zero center for
the lone-seed orbit.  Together with the earlier constant-one argument in
`RESULTS-inverse-trace.md`, it rules out every eventually constant lone-seed
center.  It does **not** rule out a nonconstant eventual period.

The proof is exact and finite-coordinate at every step.  Computation was used
only to discover the recurrence and to check independent implementations; no
finite measurement is used as evidence for the theorem.

## The theorem

Let `F` be Rule 30,

```text
F(a)(x) = a(x-1) XOR (a(x) OR a(x+1)).
```

For an initial configuration with `a(0)=0`, write

```text
R_j = a(j),   j >= 1,
L_k = a(-k),  k >= 1,
R_0 = L_0 = 0.
```

The all-zero center trace has a complete inverse classification:

1. If every `R_j` is zero, every `L_k` is zero.
2. Otherwise let `m` be the least positive index with `R_m=1`.  Then the
   unique compatible left half is

```text
L_k = 0          for k < m,
L_m = 1,
L_k = k mod 2    for k > m.
```

In particular, the second case has an infinite alternating left tail and is
not finitely supported.  The first case is the all-zero configuration.  These
two cases prove the theorem.

Equivalently, the inverse map is the one-state prefix-OR transducer

```text
L_(2k+1) = OR(R_1, ..., R_(2k+1)),
L_(2k)   = R_(2k) AND NOT OR(R_1, ..., R_(2k-1)).
```

This closed update is the proof-relevant recurrence that the earlier inverse-
trace arm lacked.

## Proof

### 1. Triangular uniqueness

Fix a complete right half `a(x)` for `x >= 0` and a desired center trace.  At
most one left half realizes them.

Suppose two left halves differ and let `n` be their least differing depth.
Initial cells farther left than `-n` cannot reach the center by time `n`.
The discrepancy at `-n` follows the extreme path

```text
(-n,0), (-n+1,1), ..., (0,n).
```

At every update on this path, the center and right inputs agree and only the
left input differs.  Rule 30 is left permutive, so the output differs.  The
two center traces therefore differ at time `n`, a contradiction.  This proves
coordinatewise uniqueness without compactness or an infinite-prefix
assumption.

### 2. Closed invariant classes

For `m >= 1`, define `C_m` to contain the configurations whose right half has

```text
R_1 = ... = R_(m-1) = 0,   R_m = 1,
```

with all `R_j` for `j>m` arbitrary, and whose left half is

```text
L_k = 0 for k<m,   L_m=1,   L_k=k mod 2 for k>m.
```

One Rule 30 step gives

```text
a'(0) = L_1 XOR R_1,
R'_j  = R_(j-1) XOR (R_j OR R_(j+1)),
L'_k  = L_(k+1) XOR (L_k OR L_(k-1)).
```

For `m>1`, the center remains zero and the nearest right-hand one moves from
`m` to `m-1`.  On the left:

- `k<m-1` gives `L'_k=0`;
- `k=m-1` gives `L'_(m-1)=L_m=1`;
- `k=m` gives `L'_m=((m+1) mod 2) XOR 1 = m mod 2`;
- `k>m` has `L_k OR L_(k-1)=1`, including the boundary case `k=m+1`
  because `L_m=1`, and hence `L'_k=(1-(k mod 2)) XOR 1=k mod 2`.

Thus

```text
F(C_m) is a subset of C_(m-1),   m>1.
```

For `m=1`, `L_k=k mod 2` for every `k`.  This checkerboard left half is fixed,
the center is `1 XOR 1=0`, and the Rule-30-specific OR latch gives

```text
R'_1 = 0 XOR (1 OR R_2) = 1
```

independently of the omitted right tail.  Therefore `F(C_1)` is a subset of
`C_1`.  Every configuration in every `C_m` has center zero forever.

### 3. Classification and finite-support contradiction

Given any nonzero positive right half, choose its least one `m`.  The
corresponding member of `C_m`, with the entire farther-right half left
arbitrary and unchanged, realizes the all-zero center trace.  Triangular
uniqueness forces every other realization with that right half to have the
same infinite alternating left tail.

If the positive right half is zero, the all-zero configuration is a
realization; uniqueness forces its left half as well.  Hence the only finitely
supported realization is the zero configuration.

## Exact bounded constraint certificate

For support radius `w>=1`, consider all nonzero rows supported in `[-w,w]`
with time-zero center zero.  This is an exact space of

```text
2^(2w) - 1
```

rows.  Let

```text
q = the least odd integer strictly greater than w
  = w+1 when w is even,
  = w+2 when w is odd.
```

After constraints through depth `w`, triangular inversion leaves exactly one
left prefix for each of the `2^w` right words.  The zero right word gives the
zero row.  Each of the other `2^w-1` right words forces `L_q=1` by the odd
prefix-OR recurrence, while finite support requires `L_q=0`.  Therefore:

```text
maximum H with c(t)=0 for every 0<=t<=H = q-1 = 2 ceil(w/2),
number of nonzero extremal rows             = 2^w-1.
```

Every nonzero right word is extremal when its forced left prefix through
depth `w` is installed and the row is zero outside `[-w,w]`.  A canonical
witness has ones at `+1` and at the negative odd positions inside the support.
The compact conflict core is:

```text
right half nonzero  => prefix_OR=1,
q odd               => L_q=prefix_OR=1,
support radius w<q  => L_q=0.
```

This is an exhaustive symbolic certificate, not a fitted finite pattern.  Its
one-bit state is `prefix_OR`, and its state/update is closed.

| `w` | rows covered | exact `H_max` | extremal rows | first forced conflict |
|---:|---:|---:|---:|---:|
| 1 | 3 | 2 | 1 | 3 |
| 2 | 15 | 2 | 3 | 3 |
| 3 | 63 | 4 | 7 | 5 |
| 4 | 255 | 4 | 15 | 5 |
| 5 | 1,023 | 6 | 31 | 7 |
| 6 | 4,095 | 6 | 63 | 7 |
| 7 | 16,383 | 8 | 127 | 9 |
| 8 | 65,535 | 8 | 255 | 9 |
| 12 | 16,777,215 | 12 | 4,095 | 13 |
| 22 | 17,592,186,044,415 | 22 | 4,194,303 | 23 |

The formula covers every radius.  Independent direct forward enumeration,
which deliberately does not call the transducer, checks every center-zero
row through radius 7 in the test suite and through radius 8 in the recorded
local run.  These checks are **EXACT COMPUTATION** and are validation only; the
invariant proof carries the universal claim.

## Consequence for the lone seed

**PROVED.** The lone-seed Rule 30 center is not eventually zero.  If an
all-zero tail began at time `T`, row `F^T(delta_0)` would be a finitely
supported zero-trace configuration.  It is nonzero: if a finite nonzero row
has support interval `[A,B]`, its successor has ones at both `A-1` and `B+1`.
The zero-tail theorem gives a contradiction.

An all-one trace also has a direct inverse classification.  For every chosen
right half with center one, triangular uniqueness forces

```text
L_k = 1 exactly when k is positive and even.
```

This checkerboard negative half is invariant, while the center update is
`0 XOR (1 OR R_1)=1`, independently of the positive right tail.  It is
infinite, so no finite row has all-one trace.  Thus every eventual constant
center is excluded without appealing to the width-two theorem.  Nonconstant
periods remain open because a center-one phase breaks the `R_1=1` OR latch used
by `C_1`; the recurrence again depends on farther columns.  See
`RESULTS-eventual-period.md` for the sharp all-one horizon and the exact
same-orbit collision reduction.

## Phase-labelled generalization attempt

The exact left-column reconstruction is

```text
A_(j+1)(t) = A_j(t+1) XOR (A_j(t) OR A_(j-1)(t)),
A_j(t) = s(t,-j),   A_0(t)=c(t).
```

For the zero word, the center equation first gives
`A_1(t)=s(t,1)`, and the `C_m` descent closes.  For a general periodic word,

```text
A_1(t) = c(t+1) XOR (c(t) OR s(t,1)),
```

so a center-one phase removes rather than preserves the right-neighbor latch.
The state no longer closes on the nearest-one distance or one prefix-OR bit.

**FALSIFIED.** The claim that any period word containing a zero has the same
next-odd support conflict as the zero word already fails for radius one.  From
the finite row `{-1}`, the exact Rule 30 center trace at times `0..7` is

```text
0 1 0 1 0 1 0 0.
```

It agrees with the period-two word `01` through time 6, whereas the zero-word
radius-one conflict occurs at time 3.  This is a falsifier of the proposed
phasewise reuse, not evidence for eventual period two.

One sufficient strengthening that would settle every start phase and every
finite row, and hence the lone-seed problem, is:

> For each nonconstant word `c` of length `p`, each chosen start phase, and
> every eventually-zero spatial right half with `R_0=c(0)`, prove that the left
> half forced by the repeated trace `c^infinity` is not eventually zero.

This is stronger than the logically exact remaining lone-seed obligation,
which concerns only right halves actually reachable at a proposed tail time.
The stronger statement is proposed because it has a clean falsification
contract; it is not assumed to be true.

A useful next mechanism would be a phase-labelled finite transducer
`S_(k+1)=Phi_p(S_k,R_(k+1))` for the forced spatial tail, with an explicit
state bound depending on `p`, followed by exclusion of every reachable
zero-output cycle after the right input becomes zero.  No such closed state is
currently known.  The generic rotated recurrence still carries a growing time
prefix; naming that prefix as a state would only restate the original problem.

## Rule 90 adversarial control

**FALSIFIED for the generic-rule analogue.**  Rule 90 has a nonzero finite
zero-trace row: ones at `{-1,+1}`.  Reflection symmetry is preserved, and the
center remains the XOR of two equal neighbors.  The executable control checks
this through time 128.

The load-bearing Rule-30 fact is

```text
center=0 and R_1=1  =>  R'_1=1 regardless of R_2.
```

For Rule 90, `R'_1=R_2`; the latch and invariant `C_1` fail.  The proof is
therefore Rule-30-specific and does not smuggle in a false permutivity-only
claim.

## Literature and novelty audit, 2026-08-28

No primary source located in the audit states or proves the finite-support
zero-trace fiber theorem

```text
Tr_0^(-1)(0^infinity) intersect {finite configurations} = {0}
```

for Rule 30.

- Jen, *Aperiodicity in One-Dimensional Cellular Automata* (1990), Proposition
  3, proves that the relevant rules have at most one periodic temporal
  sequence from a nonzero finite seed.  The load-bearing propagation begins
  with two periodic columns and explicitly permits one exceptional periodic
  column.  An all-zero center could have been that exception.
  [DOI](https://doi.org/10.1016/0167-2789(90)90169-P),
  [open report](https://www.osti.gov/servlets/purl/7230855).
- Kopra, *A Natural Class of Cellular Automata Containing Fractional
  Multiplication Automata, Rule 30, and Others* (2023), proves width-two
  nonperiodicity for Rule 30 and explicitly leaves the width-one lone-seed
  question open.  Its reconstruction lemma requires a periodic observation
  window of width two; one zero column does not meet that hypothesis.
  [DOI](https://doi.org/10.1016/j.tcs.2022.12.018),
  [arXiv](https://arxiv.org/abs/2202.13809).
- Kopra's 2019 dissertation, *Cellular Automata with Complicated Dynamics*,
  Theorem 3.1.12 records Jen's width-two result and immediately states that it
  remains open whether a nonzero finite Rule 30 configuration can have an
  eventually periodic width-one trace.  The theorem here settles its
  constant-zero subcase.
  [Repository record](https://urn.fi/URN:ISBN:978-952-12-3891-8).
- Rowland, *Local Nested Structure in Rule 30* (2006), Proposition 1 and
  Lemma 1 supply closely related one-sided uniqueness and
  leading-discrepancy mechanisms.  They support treating triangular
  uniqueness as prior technique, but do not give the zero-trace fiber,
  prefix-OR transducer, or sharp support-radius law.
  [DOI](https://doi.org/10.25088/ComplexSystems.16.3.239).
- Pre-expansivity and trace-subshift results do not settle the fiber.  Standard
  pre-expansivity compares all asymptotic pairs and generally uses a finite
  observation window; trace-subshift membership records that `0^infinity` is
  realizable, not whether the zero row is its unique finite realization.
- The 2025--2026 audit included
  [Spin Models from Nonlinear Cellular Automata](https://arxiv.org/abs/2503.19572)
  and
  [Symmetric Nonlinear Cellular Automata as Algebraic References for Rule 30](https://arxiv.org/abs/2604.00165).
  Neither states a finite-support zero-trace theorem; the latter continues to
  treat center nonperiodicity as open.
- Online claimed proofs based on finite randomness, unbounded Boolean degree,
  spectral novelty, or unproved support-descriptor complexity do not supply
  the required fixed-input implication.  Their load-bearing gap is the same:
  complexity of a family of Boolean functions does not show that those
  functions are nonzero on the lone-seed input, and finite prefix behavior
  does not imply an infinite trace theorem.

This supports a novelty label of **new partial theorem**, not a claim of
absolute bibliographic exhaustiveness.  The official prize page still lists
the complete center-column problem as open: <https://rule30prize.org/>.

## Reproduction

From `experiments/rule30`:

```bash
uv run python -m unittest test_zero_tail_probe.py
uv run python zero_tail_probe.py \
  --max-radius 22 --exhaustive-through 8 --json
```

The primary method is the symbolic recurrence.  Increasing
`--exhaustive-through` only repeats the independent exponential validator and
is not a path to a stronger theorem.

## Spending

- Modal: **$0**.
- Paid model-provider calls: **$0**.
- Crosstalk: not invoked; the exact bottleneck was resolved locally before a
  new model run became justified.

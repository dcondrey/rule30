# Rule 30 nonconstant eventual periods: exact reduction and bounded certificates

## Status

**OPEN.**  This cycle does not prove center-column nonperiodicity and must not
be used to remove the qualification that nonconstant eventual periods remain
open.

It does produce three rigorous advances:

1. **PROVED:** eventual periodicity is exactly a same-forward-orbit collision
   of the one-cell trace map on a nonzero finite row;
2. **PROVED:** the all-one trace fiber has an infinite checkerboard left tail,
   giving a direct Rule-30 proof that no finite row has constant-one trace;
3. **EXACT COMPUTATION:** an incremental SMT encoding exhausts all nonzero rows
   through support radius 8 and all nonconstant proposed periods through 6,
   returning explicit extremal rows and inclusion-minimal temporal UNSAT cores.

The computation identifies no period-independent recurrence.  Its finite
exclusions are falsifiers and lemma generators, not evidence for the open
unbounded statement.

## Exact remaining obligation

Let `F` be Rule 30 and `Tr_0(x)_t=F^t(x)_0`.

**PROVED.**  A finite configuration `x` has an eventually `p`-periodic center
trace if and only if there is a nonzero finite row `y` on its forward orbit
such that

```text
Tr_0(y) = Tr_0(F^p(y)).
```

Indeed, if the tail starts at time `T`, take `y=F^T(x)`; then the displayed
identity is exactly `F^(t+p)(y)_0=F^t(y)_0` for every `t>=0`.  The converse is
the same identity read backwards.  The row stays finite and nonzero.  More
strongly, if its support interval is `[A,B]`, then the support of `F^p(y)` is
`[A-p,B+p]`, because the two extreme Rule 30 neighborhoods are `001` and
`100`.  Hence `y != F^p(y)`.

Thus the minimal theorem still needed is

> For every nonzero finite row `y` and every `p>=1`,
> `Tr_0(y) != Tr_0(F^p(y))`.

Full pre-injectivity of the one-cell trace on all asymptotic pairs would be
sufficient but is strictly stronger.  The known collision between `{0}` and
`{0,1}` shows why generic one-cell trace injectivity is false; the same-orbit
condition is essential.

Jen's Proposition 3 and Kopra's width-two theorem give a second exact target:
derive an eventually periodic adjacent column from the periodic center.  That
would supply a forbidden second periodic column.  No such derivation survived
the tests below.

## Exact phase and defect identities

Write

```text
c_t = s(t,0),  r_t = s(t,1),  l_t = s(t,-1).
```

Rotating the Rule 30 equation gives

```text
l_t = c_(t+1) XOR (c_t OR r_t).
```

Consequently a center-one phase pins `l_t=NOT c_(t+1)`, whereas a center-zero
phase passes the right neighbor as `l_t=c_(t+1) XOR r_t`.  This alternating
pin/pass behavior is the obstruction to a zero-trace-style one-bit latch.

For a proposed period `p`, put

```text
d_t(x) = s(t+p,x) XOR s(t,x).
```

Over `GF(2)` its exact Rule 30 recurrence is

```text
d_(t+1)(x) = d_t(x-1) XOR d_t(x) XOR d_t(x+1)
             XOR s(t,x)d_t(x+1) XOR s(t,x+1)d_t(x)
             XOR d_t(x)d_t(x+1).
```

Under a periodic center, `d_t(0)=d_(t+1)(0)=0`, so this reduces to

```text
d_t(-1) = (1 XOR c_t) AND d_t(1).
```

**PROVED run-of-ones wedge.**  If
`c_t=...=c_(t+r-1)=1`, then `d_t(-j)=0` for `1<=j<=r`.  The base case is the
last display.  For the induction, overlapping one-runs give zero defects at
`-(j-1)` at times `t` and `t+1`, and the recurrence there collapses to
`d_t(-j)=0`.  A nonconstant periodic word has bounded one-runs, so this gives
only a bounded wedge, not a descent to contradiction.

## Direct all-one fiber

**PROVED.**  Fix any complete right half with center value one.  The all-one
trace forces, and is realized by,

```text
L_k = s(0,-k) = 1  iff  k is positive and even.
```

The checkerboard negative half is fixed by Rule 30.  Its first negative cell
is zero, so the center update is `0 XOR (1 OR R_1)=1`, independently of the
farther right half.  Triangular uniqueness makes this the only compatible
left half.  It contains infinitely many ones, so no finite configuration has
an all-one center trace.

For support radius `w`, let `q` be the least even integer greater than `w`.
The sharp inclusive all-one horizon is `q-1`: it is `w+1` for even `w` and `w`
for odd `w`, with exactly `2^w` extremizers.  Combining this with the zero-tail
theorem, the largest horizon for either constant trace is `w+1`; the extremal
count is `2^w` for even `w` and `2^w-1` for odd `w`.

This removes the earlier dependence on the width-two theorem for the
constant-one case.  It does not address nonconstant periods.

## Incremental exact search

`experiments/rule30/eventual_period_probe.py` creates Boolean variables for
every cell in the finite causal cone and constrains them with the exact Rule 30
local equation.  For support radius `w` and proposed period `p`, it imposes:

```text
the initial row is nonzero and zero outside [-w,w],
the first p center bits contain both symbols,
c_t = c_(t-p), added incrementally for t=p,p+1,... .
```

At the first UNSAT time it deletes assumptions greedily and returns an
inclusion-minimal set of period-equality times.  At every preceding SAT time it
returns an explicit row, checked by an independent finite-set Rule 30
evaluator.  The search covers all `2^(2w+1)-1` nonzero rows, not a selected
right-half family.

The exact maximum absolute periodic-prefix horizon `H` is:

| `p` \ `w` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 6 | 6 | 6 | 6 | 8 | 9 | 9 | 14 |
| 3 | 4 | 5 | 9 | 9 | 9 | 13 | 13 | 16 |
| 4 | 6 | 6 | 7 | 10 | 12 | 13 | 13 | 16 |
| 5 | 10 | 10 | 10 | 10 | 12 | 12 | 13 | 15 |
| 6 | 7 | 9 | 13 | 13 | 13 | 15 | 15 | 17 |

Each entry is SAT through `H` and UNSAT at `H+1`.  For example:

- `p=2,w=1`: `{-1}` has trace `0101010` through time 6; equality times
  `{2,7}`, together with finite support and a nonconstant first block, form an
  inclusion-minimal UNSAT core at time 7.
- `p=2,w=8`: `{-8,-1,6}` has trace `0101010101010100` through time 15, so it
  agrees with `(01)^infinity` through time 14 and fails at time 15.
- `p=3,w=8`: a period-three prefix survives through time 16 and every such
  prefix conflicts at time 17.

There is no stable one-bit conflict pattern in the cores: both their times and
their sizes change with `w` and `p`.  In particular, the radius-one
zero-trace conflict time does not generalize phasewise.

## Adversarial controls and falsified shortcuts

**PROVED finite-prefix lemma.**  For any finite desired trace
`tau_0,...,tau_N` and any compatible right prefix `R_0,...,R_N`, left
permutivity supplies a unique `L_1,...,L_N`; zero padding then gives a finite
row matching the desired trace through time `N`.  Therefore no contradiction
can depend only on `p` or on a bounded number of center symbols independent of
support size.

**FALSIFIED:** a zero phase does not propagate the zero-trace prefix-OR latch.
The row `{-1}` matches `(01)^infinity` through time 6, and `{-8,-1,6}` matches
it through time 14.

**FALSIFIED:** even a block of two zero phases forces no radius-two mirror
symmetry.  With prescribed trace `(001)^infinity` and initial positive right
half `R_1=R_2=1`, the exact inverse begins
`L=(1,1,0,1,0,0,0,1,...)`; for the three-step defect,
`d(-1)=d(1)=1` but `d(-2)=0 != d(2)=1`.

**Rule 90 control:** the nonzero row `{-1,1}` has zero center forever.  The SMT
encoding retains it through every requested horizon instead of manufacturing
an UNSAT result.  Rule 90's defect recurrence lacks Rule 30's one-phase pin.

## Decision

The nonconstant-period claim is not ready for submission as a theorem.  The
highest-value next target is the same-orbit collision statement, starting with
period two.  For an alternating center, the exact inverse stencil through five
symbols is

```text
L_1=1 XOR R_1,  L_2=R_1,
L_3=R_1 OR R_2 OR R_3,  L_4=0.
```

Thus period two reduces to a zero-stroboscopic obstruction for `F^2`, a
radius-two CA.  The missing step is a closed finite-state descent for that
stroboscopic map; merely enlarging the SAT grid cannot prove it.

One exact local constraint for this reduced problem is available.  If a row
`a` satisfies `a(0)=F^2(a)(0)=0`, then

```text
a(-2) OR a(-1) = a(-1) OR a(1) OR a(2).
```

Therefore a one in `{−1,1,2}` forces a one in `{−2,−1}`.  This is not a
descent: `a(-1)=1` already satisfies both sides, so the identity does not
exclude a finite row or close the period-two case.

Two one-sided cases do admit an exact exclusion.  Let `G=F^2` and suppose a
nonzero finite row has `G^n(a)(0)=0` for every `n`.

* If its support is entirely to the right (`A>0`), the left edge reaches
  coordinate `1` or `2` at the least even time at least `A`, while coordinates
  `-2,-1,0` are still zero.  The displayed local identity then forces the next
  stroboscopic center to one, a contradiction.
* If its support is entirely to the left and its right endpoint `B<0` is even,
  then at time `-B-2` the right edge is at `-2` and the window
  `(-2,-1,0,1,2)` is `10000`.  The next stroboscopic center is therefore one.

Thus a period-two counterexample, if one exists, must have mixed support or a
one-sided left support with odd right boundary.  These exclusions are proved
for the stated cases; they do not close the general period-two problem.

## Reproduction and spending

From `experiments/rule30`:

```bash
python3 -m unittest test_eventual_period_probe.py
python3 eventual_period_probe.py \
  --max-radius 8 --max-period 6 --search-horizon 32 --json
uv run python -m unittest test_zero_tail_probe.py \
  test_inverse_trace_probe.py test_periodicity_bridge_probe.py
```

- Modal: **$0**.
- Paid model-provider calls: **$0**.
- Crosstalk: not invoked; no closed candidate passed the local gate.

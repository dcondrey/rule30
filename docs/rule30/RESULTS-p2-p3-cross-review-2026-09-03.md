# P2/P3 cross-review after the period-two work

Date: 2026-09-03

Status: **NEITHER PRIZE PROBLEM IS SOLVED.**  This note separates two new
exact reductions from the finite evidence that motivated them.  Here `P2`
means center density `1/2`, and `P3` means the fixed-sequence computation
question.  The nonconstant period-two trace problem is a rung toward `P1`, not
`P2`.

## 1. What transfers from the period-two investigation

The useful transfer is methodological.  The period-two work succeeded when it
retained all three of

```text
binary scale + absolute phase + the ordered seam state.
```

It repeatedly failed when a local count, a phase-free defect word, or a
bounded window replaced that state.  Its exact `D8` and 13-element monoids act
on a special inverse-cone/constant-tail system.  They do not act on the
single-seed center sequence and therefore provide no P2 or P3 theorem by
themselves.

This gives a strict acceptance test for a proposed P2/P3 renormalization: it
must define the state at a genuine single-seed time seam and an exact scale
composition.  Similar-looking dyadic periods are not a bridge.

## 2. An exact P2 reduction to canonical dyadic shells

Let `c_t` be the single-seed center bit and put

```text
x_t = 2 c_t - 1,
S(N) = sum_{0 <= t < N} x_t.
```

For `k >= 0`, define the maximum partial discrepancy in the canonical dyadic
time shell

```text
M_k = max_{0 <= u <= 2^k}
      |sum_{2^k <= t < 2^k + u} x_t|.
```

**Dyadic-shell lemma.**  P2 is equivalent to

```text
M_k / 2^k -> 0.
```

Proof.  If `S(N)/N -> 0`, then uniformly for
`2^k <= N <= 2^(k+1)`,

```text
|S(N) - S(2^k)| / 2^k -> 0,
```

which is the shell condition.  Conversely, for
`2^k <= N < 2^(k+1)`,

```text
|S(N)| <= |S(2^k)| + M_k
       <= |S(1)| + sum_{j < k} M_j + M_k.
```

If `M_j=o(2^j)`, split the sum at a fixed scale.  Its finite head is
`o(2^k)` and its geometric tail is at most an arbitrarily small constant
times `2^k`.  Hence `S(N)=o(N)`.  This proves the equivalence.

This lemma is stronger and more useful than testing only `S(2^k)`.  Dyadic
endpoint convergence alone does not control excursions inside a shell.  It
also avoids the overstrong orbit-closure target: no statement about every
invariant measure or every shifted time block is needed.

### 2.1 Equivalent integrated-energy criterion

There is an exact average-square version that removes the maximum.  Write the
signed running discrepancy inside shell `k` as

```text
S_k(u) = sum_(0 <= r < u) x_(2^k+r),
I_k    = sum_(u=1)^(2^k) S_k(u)^2.
```

**Integrated-energy lemma.**  P2 is equivalent to

```text
I_k / 2^(3k) -> 0.
```

Proof.  Put `N=2^k` and `M=M_k`.  The easy direction is

```text
I_k <= N M^2.
```

For the other direction, choose the first prefix at which `|S_k|=M`.
Because every increment is `+1` or `-1`, the preceding
`floor(M/2)+1` prefixes all have absolute value at least `M/2`.  Hence, for
integer `M>=1`,

```text
I_k >= M^3/8.
```

Thus `I_k=o(N^3)` if and only if `M_k=o(N)`, and the dyadic-shell lemma
finishes both directions.  QED.

This is the weakest exact scalar target found in the review.  It permits rare
large excursions and arbitrary individual correlations; any fixed power
bound `I_k=O(N^(3-delta))`, however small `delta>0`, proves P2.  Expanding
the squares also gives a boundary-weighted ordinary-correlation form:

```text
I_k = sum_(r,s=0)^(N-1) (N-max(r,s)) z_k(r)z_k(s),
```

where changing from `x` to `z=-x` does not change the energy.  This points to
a possible boundary-flux proof: cancellation is needed only after averaging
over all prefix endpoints, not uniformly at every endpoint.

The required scalar summary also composes exactly under concatenation.  For a
signed word `w` define

```text
D(w) = its total signed sum,
A(w) = sum_u S_w(u),
I(w) = sum_u S_w(u)^2.
```

If `u` and `v` have summary `(n_u,D_u,A_u,I_u)` and
`(n_v,D_v,A_v,I_v)`, then

```text
n(uv) = n_u+n_v,
D(uv) = D_u+D_v,
A(uv) = A_u+n_v D_u+A_v,
I(uv) = I_u+n_v D_u^2+2 D_u A_v+I_v.
```

This associative four-coordinate law is exact and regression-tested.  It
means that a future dyadic spacetime grammar need not retain every center
prefix merely to evaluate the P2 observable: it need only attach these three
integer moments to each temporal piece.  The unresolved difficulty remains
constructing the actual seed-specific pieces across the nonlinear spacetime
seam; the moment law does not supply that grammar.

On the exact `2^25`-row band cache, `I_k/N^2` remains random-walk scale rather
than approaching the cubic worst case:

| `k` | `I_k` | `I_k/N^2` | `I_k/N^3` |
|---:|---:|---:|---:|
| 12 | 1,679,956 | 0.1001 | 2.445e-5 |
| 14 | 334,979,508 | 1.2479 | 7.617e-5 |
| 16 | 1,877,755,364 | 0.4372 | 6.671e-6 |
| 18 | 5,794,553,236 | 0.0843 | 3.217e-7 |
| 20 | 356,961,632,476 | 0.3247 | 3.096e-7 |
| 22 | 12,573,129,265,932 | 0.7147 | 1.704e-7 |
| 24 | 156,527,072,865,292 | 0.5561 | 3.315e-8 |

These measurements are finite evidence only.  The probe records the integer
energy directly and regression tests exhaust all signed words of length eight
against both deterministic inequalities.

### 2.2 Probabilistic restatement without random initial conditions

One may choose the *time index* `N` uniformly in
`[2^k,2^(k+1))`; this is a genuine finite probability space on the fixed
seed orbit.  Revealing the binary digits of `N` gives a Doob martingale, but
the martingale formalism supplies no concentration by itself.  A valid proof
must bound the effects of those reveals using an exact Rule 30 coupling or
seam map.  Importing Bernoulli initial-condition independence would reintroduce
the known ensemble-to-seed gap.

### 2.3 Finite maximum diagnostic

The existing bit-exact cache through `2^25` times gives the following shell
maxima (the center is cache bit 15):

| `k` | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `M_k` | 65 | 183 | 249 | 180 | 367 | 889 | 330 | 1006 | 1198 | 940 | 3049 | 6654 | 5288 |

A log-linear fit over `k=12,...,24` has exponent about `0.490`.  This is
consistent with square-root fluctuations and is not an asymptotic result.
Its purpose is to reject proposed bounds that already fail on the recorded
orbit and to identify the exact observable a proof must control.

### 2.4 Quantitative same-orbit defects imply P2

The temporal-period investigation supplies an exact two-orbit defect system,
and van der Corput gives a rigorous way to reuse it.  Put

```text
z_t = (-1)^c_t,
C_N(h) = sum_(t=0)^(N-1-h) z_t z_(t+h).
```

For integers `N,H>=1`, zero-extend the length-`N` word and sum its `H`
translations.  Cauchy--Schwarz gives the exact finite inequality

```text
H^2 |sum_(t<N) z_t|^2
 <= (N+H-1) [HN + 2 sum_(h=1)^(H-1) (H-h) C_N(h)].
```

The bracket is a sum of squares and is nonnegative.  Replacing each
correlation by its absolute value gives the following sufficient theorem.

**Same-orbit defect theorem.**  If, for every fixed `h>=1`,

```text
C_N(h)/N -> 0,
```

then P2 holds.

Indeed, first let `N` tend to infinity with `H` fixed.  The normalized
inequality has limsup at most `1/H`; then let `H` tend to infinity.  Finally,

```text
z_t z_(t+h) = (-1)^(c_t XOR c_(t+h)),
```

so the hypothesis says exactly that the center defect between the two
same-orbit configurations `F^t(delta_0)` and `F^(t+h)(delta_0)` has limiting
density `1/2`.

This precisely calibrates what transfers from temporal period exclusion.  To
exclude eventual period `h`, it is enough to show that this defect is nonzero
infinitely often.  For P2, the reusable defect recurrence must be strengthened
to asymptotic half-density, for every fixed shift (or to the standard weaker
Cesaro-in-`h` correlation condition).  The finite inequality and all signed
words of length eight are regression-tested in the shell probe.

## 3. The live P2 composition target

Write the signed word in shell `k` as

```text
X_k = (x_(2^k), ..., x_(2^(k+1)-1)).
```

A useful scale state `Q_k` must satisfy all of:

1. `Q_k` is constructed from the actual lone-seed orbit, not an arbitrary
   input row or an invariant ensemble.
2. There is an exact operation producing `Q_(k+1)` from smaller-scale states
   and an explicit seam state.
3. `Q_k` determines or bounds the maximum prefix norm `M_k`.
4. The bound on its discrepancy component is `o(2^k)` for every `k`.
5. Its seam contains scale and absolute phase unless an identity proves they
   cancel.

The weakest immediate mathematical target is a subcubic bound for the
integrated shell energy `I_k`; a contraction or cancellation law for the
stronger maximum remains sufficient.  A candidate law must be tested on Rule
90, on the all-zero and checkerboard Rule 30 fixed points, and on the cached
single-seed shells.  The fixed points are not counterexamples to a
seed-specific law, but they refute any proof whose only hypothesis is Rule 30
invariance.

## 4. Why the previous P2 orbit-closure target is probably too strong

It would suffice to prove that every vertical-shift-invariant measure on the
single-seed orbit closure has center marginal `1/2`.  The archive now records
steadily growing all-zero and checkerboard patches.  If either fixed
configuration belongs to that closure, its Dirac measure has center marginal
`0` or `1`, refuting the sufficient target while leaving P2 untouched.

Finite patch growth does not prove orbit-closure membership, but it changes
the work order: first establish that the closure excludes these fixed points,
or abandon unique-measure rigidity in favor of the dyadic-shell discrepancy
lemma.  The latter asks exactly for the designated orbit and survives either
answer to the patch question.

## 5. P3: what the archive rules out and what remains coherent

P3 fixes the initial row and receives only `n` in binary.  Arbitrary-input
ANF degree, sensitivity, decision-tree depth, ROBDD size, and circuit size do
not lower-bound the cost of this fixed sequence.  Resolution and polynomial
calculus probes likewise give no model-independent prediction lower bound.
The finite-state 2-kernel and five fixed ROBDD orders are measured failures of
particular shortcuts, not P3 lower bounds.

The cleanest falsification program for P3 remains an exact sublinear query
algorithm.  It needs:

```text
canonical state of poly(log n) or o(n) size
        + exact dyadic composition with the nonlinear seam
        + exact extraction of c_n
        + total charged work o(n) in the registered model.
```

ARM7 found exact quadtree reuse but a state growing roughly as `n^1.48` and
perimeters of `Theta(n)` bits.  ARM8 found exponential arbitrary-input ROBDDs.
Their common defect is now precise: neither quotients only the *reachable
single-seed seams needed by one center query* while providing an exact
doubling operation.  Searching another representation is useful only if it
supplies that operation.

Conversely, a proof of P3 must name a machine model and lower-bound the fixed
index-to-bit function in that model.  Formula expansion, nonperiodicity,
nonautomaticity, and arbitrary-input dependence are not substitutes for that
bridge.  No such bridge is present in the archive.

## 6. Ranked work order and kill conditions

1. **P2 shell seam.**  Express `X_(k+1)` through actual scale-`k` spacetime
   pieces, retaining the full seam at first.  Quotient states only after an
   exact observational equivalence is proved.
2. **P2 digit coupling.**  Pair or couple indices differing in one high binary
   digit and derive the exact residual region between their center queries.
   The target is a sublinear total uncancelled residual over the shell.
3. **P2 seed-specific coboundary.**  Seek a telescoping identity with boundary
   terms supported on the two expanding seed-cone edges.  A universal local
   coboundary is excluded by Rule 30 fixed points.
4. **P3 reachable query quotient.**  Apply the ARM8 observational idea only to
   seams reachable in the lone-seed dyadic construction.  Kill it if the
   canonical seam needs `Omega(n)` bits or composition touches `Omega(n)`
   entries.

Reject a proposed advance immediately if it uses Bernoulli initial-condition
probability, infers an infinite statement from a fitted exponent, discards the
nonlinear seam, silently switches to arbitrary-input complexity, or treats a
compressed file as a sublinear construction.

The strongest new conclusion is the pair of exact shell equivalences in
section 2.  They convert P2 into either a scale-local maximum-discrepancy
theorem or the weaker subcubic integrated-energy theorem on the lone seed and
identify the only seam whose renormalization would be decisive.  The
renormalization itself remains open.

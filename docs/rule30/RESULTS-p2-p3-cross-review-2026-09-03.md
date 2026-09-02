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

### 2.1 Probabilistic restatement without random initial conditions

One may choose the *time index* `N` uniformly in
`[2^k,2^(k+1))`; this is a genuine finite probability space on the fixed
seed orbit.  Revealing the binary digits of `N` gives a Doob martingale, but
the martingale formalism supplies no concentration by itself.  A valid proof
must bound the effects of those reveals using an exact Rule 30 coupling or
seam map.  Importing Bernoulli initial-condition independence would reintroduce
the known ensemble-to-seed gap.

### 2.2 Finite diagnostic

The existing bit-exact cache through `2^25` times gives the following shell
maxima (the center is cache bit 15):

| `k` | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `M_k` | 65 | 183 | 249 | 180 | 367 | 889 | 330 | 1006 | 1198 | 940 | 3049 | 6654 | 5288 |

A log-linear fit over `k=12,...,24` has exponent about `0.490`.  This is
consistent with square-root fluctuations and is not an asymptotic result.
Its purpose is to reject proposed bounds that already fail on the recorded
orbit and to identify the exact observable a proof must control.

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

The immediate mathematical target is therefore a contraction or cancellation
law for shell-prefix sums, not another measurement of total prefix bias.  A
candidate law must be tested on Rule 90, on the all-zero and checkerboard Rule
30 fixed points, and on the cached single-seed shells.  The fixed points are
not counterexamples to a seed-specific law, but they refute any proof whose
only hypothesis is Rule 30 invariance.

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

The strongest new conclusion is the exact shell equivalence in section 2.
It converts P2 into a scale-local maximum-discrepancy theorem on the lone seed
and identifies the only seam whose renormalization would be decisive.  The
renormalization itself remains open.

# R1 mismatch follow-up: exact error budget and the remaining right history

Date: 2026-09-15. **P1 remains open. No sublogarithmic right-mismatch
bound has been established.**

The previous [finite-origin mismatch result](RESULTS-r1-periodic-realization-scope.md)
suggested a smaller sufficient conclusion than eventual periodicity of the
right neighbour. This follow-up checks its sharpness, proves an error budget
for independently driven halves, and isolates one exact right-boundary
observer. It also repairs a sampling defect in an older experiment.

## 1. An exact budget distinguishes a driven boundary from a real trace

Prescribe a binary boundary `c`, with `c_0=1`, and evolve both half-planes
from zero initial data on their respective sides. Denote their adjacent
columns by `l_t` and `r_t`. They are uniquely determined by the drive,
but the centre equation need not hold. Its error bit is

```
e_t = c_(t+1) XOR l_t XOR (c_t OR r_t).
```

The two halves form the actual singleton orbit exactly when every `e_t`
vanishes. Suppose the drive is `P`-periodic after `T0`. For `t>=T0`,
subtracting the centre equations at times `t` and `t+P` gives

```
l_(t+P) XOR l_t
  = (e_(t+P) XOR e_t) XOR ((1-c_t) * (r_(t+P) XOR r_t)).       (1)
```

This identity does not assume either the one-time pin or the zero-time
coupling. It records failures of both explicitly.

For any `T>=T0`, the finite-origin theorem guarantees a left mismatch
inside `I_T=[T,2T+P-1]`. Equation (1) therefore proves

```
sum_(t in I_T) (1-c_t) * (r_(t+P) XOR r_t)
  + sum_(t in I_T) (e_t + e_(t+P)) >= 1.                       (2)
```

Let

```
M_P(N) = #{T0<=t<N : c_t=0 and r_(t+P)!=r_t},
G(U)   = #{T0<=t<U : e_t=1}.
```

Taking the disjoint intervals with endpoints
`T_k=2^k(T0+P)-P` yields, for every integer `N>=T0`,

```
M_P(N) + 2 G(N+P) >= floor(log2((N+P)/(T0+P))).               (3)
```

Each unshifted error time and each shifted error time is counted at most
once in the respective sums. That explains the factor two; no independence
or statistical assumption enters the proof.

Consequences:

- On a genuinely glued orbit, `G=0`, recovering the logarithmic mismatch
  lower bound. An independently proved `M_P(N)=o(log N)` for one period
  multiple would contradict it.
- If a driven right neighbour is eventually `P`-periodic (choosing `P`
  to be a common multiple of the two periods when needed), then
  `M_P(N)=O(1)` and `G(N+P)>=(1/2)log2 N-O(1)`. Such a driven construction
  fails the centre equation infinitely often, even if long finite windows
  look consistent.
- More generally, both terms on the left of (3) cannot be `o(log N)`.
  Proving a right-side estimate while silently dropping the glue condition
  does not establish a seed theorem.

The [verifier](../../experiments/rule30/r1_mismatch_budget_audit.py) checks
all 2,048 length-twelve drives beginning in one, comparing both packed
half-planes against independent scalar truth-table evolution. Among
30,720 candidate intervals, 1,824 satisfy its finite periodicity condition;
all 4,512 pointwise identities and 1,824 interval budgets pass. It also
checks 24 true singleton updates with zero glue error. The symbolic proof,
not these finite controls, establishes (3) for unbounded time.

## 2. The logarithmic scale cannot be improved by generic arguments

The [sharpness report](RESULTS-r1-mismatch-sharpness.md) proves that the
actual Rule 90 singleton has adjacent ones exactly at `2^a-1`, `a>=1`.
For every fixed shift `P`, the disagreement count is
`2 log2 N + O_P(1)`. Long gaps between successive disagreement pairs have
multiplicative ratio tending to two.

Thus the order `log N` and factor-two interval expansion are sharp for
arguments using only a finite origin and left reconstruction. This does
not establish the best possible leading constant. It also does not refute
a Rule-30-specific upper bound. Rule 30's pin supplies a further exact
defect identity, but no contraction or such upper bound follows from it.

## 3. A finite right-boundary certificate leaves one residual sequence

For the separate driven problem `c=(0001)^infinity` with a zero initial
right half, an exact three-state invariant proves, for `k>=2`,

```
(r_(4k), r_(4k+1), r_(4k+2), r_(4k+3)) = (0,b_k,1,1),
b_k b_(k+1) = 0.
```

Here `b_k` is the residual observer, separate from the centre-error bit
`e_t` in section 1. The [boundary certificate](RESULTS-r1-0001-boundary-certificate.md)
calls this observer `e_k` and gives all three transitions.
Consequently period-`4q` right mismatches at centre-zero times reduce to
the ordinary shift-`q` disagreements of that observer.

The invariant is valid for every continuation beyond its four-cell
prefix. It does not determine the residual observer from that prefix:
transitions still read farther-right cells. No eventual periodicity or
sublogarithmic disagreement bound for the observer has been proved.
The prescribed drive is not asserted to be the actual centre; it starts
at zero, and no left-half compatibility is assumed. This is a precise
subproblem and a small exact certificate, not a period-four exclusion.

## 4. The old random-prefix coverage was only two words

The zero-initial branch of
[`lock_search.py`](../../experiments/rule30/p1-period2-invariant/uc/r1-r1zero-screen-pin-pi-no-periodic/lock_search.py)
formerly sampled a prefix using

```
[random.Random(7919*s+p).getrandbits(1) for _ in range(24)].
```

This restarts the same generator for each bit. Every purported random
prefix was therefore `0^24` or `1^24`. Forcing `c_0=1` changes the first
to `10^23`; it does not recover the claimed sample diversity.

The sampler now creates one generator per word. Historical `ywidth=0`
logs at `T=2048,p<=7`, `T=8192,p<=4`, and `T=32768,p<=8` must be read
with their original two-word random coverage, plus the separately tested
true prefix. Their files are preserved; no larger rerun was undertaken.
The `ywidth>0` branch already advanced one generator across its prefix,
and the exhaustive `pin_tree.py` enumeration is unaffected.

The [sampling audit](../../experiments/rule30/pin_lock_sampling_audit.py)
recovers exactly two old words versus 64 distinct corrected mixed words
for each `p=1,...,8`, and independently checks all six reported pin-count
fields on 66 drives. A separate reviewer confirmed distinctness after
forcing the initial one and checked all 512 length-ten such drives.

The output label is repaired too: a late survivor only has no violations
in `[4T,8T)`. It is a finite candidate, not a “confirmed lock,” not a
guarantee of consistency throughout `[T,8T)`, and not a counterexample to
an infinite-time conjecture.

## 5. What remains worth proving

The useful distinction is between a right boundary that looks regular
and a pair of halves that obey the centre equation from the singleton
origin. Equation (3) preserves that distinction quantitatively. An actual
advance toward P1 still needs an upper bound on its right-mismatch term
under the appropriate origin and compatibility hypotheses. The finite
observer in section 3 does not supply that bound, and the corrected
sampler supplies no asymptotic conclusion.

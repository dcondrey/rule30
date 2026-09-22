# Exact applicability of the alternating guard on actual singleton queries

Date: 2026-09-14. **The full-observation alternating guard fails for every
large actual query.** Among cases with positive guard width, it holds
exactly for N=3,4 in the even readout, and for no odd readout. This is an
all-length consequence of two explicitly closed one-hot H orbits, not
an extrapolation from sampled singleton rows.

This classifies the particular guard in
[guarded norm pruning](RESULTS-p3-actual-norm-block-pruning.md). It does
not exclude partial-block guards, different patterns, corrections that
are retained, or other P3 algorithms. No period-exclusion result follows.

## 1. Translate the actual guard to a fixed edge window

Let A be the original binary Rule30 map, B=tau0 A, and
H(x)=(x>>2) XOR((x>>1) ORx). The
[actual-query identity](RESULTS-p3-actual-b-query.md) uses

```
x_N=B^N(0)=(A^N(1))>>2,
w=N-2-e,          e in{0,1},
c_(2N-2-e)=bit_e H^w(x_N).
```

The guard under investigation requires w>=1 and

```
bit_j(x_N)=1+((j-w) mod2),       w<=j<=2w-1.            (1)
```

Here and below sums of bits are XOR. Put k=2N-2-j. Since A commutes
with left shifts and H^N=D^(2N) A^N for D(x)=x>>1,

```
bit_j(x_N)=bit_0 H^N(2^k).                             (2)
```

The finite query range becomes

```
3+2e<=k<=N+e,
bit_0 H^N(2^k)=1+((N+e-k) mod2).                      (3)
```

All indices in (2) are nonnegative in the positive-width query domain
N>=3+e. H commutes with right shifts, so fixed small k evaluate a fixed
number of bits at the moving edge for every N. Computing those finite
cores does not generate the growing singleton row.

## 2. Two exact cycles contradict the guard

The complete integer orbits needed here are

```
32 -> 56 -> 50 -> 55 -> 50,
64 ->112 ->100 ->111 ->100.
```

Each has transient length two and a two-cycle. Checking the four
edges of each orbit proves, by iteration around the cycle, that for every
N>=2,

```
bit_0 H^N(32)=N mod2,
bit_0 H^N(64)=N mod2.                                 (4)
```

For the even readout e=0, k=6 belongs to the guard range whenever N>=6.
Equation (3) would require its bit to equal1+(N mod2), contradicting
(4). Thus the guard is impossible for every N>=6.

For the odd readout e=1, k=5 belongs to the guard range whenever N>=4.
It again requires1+(N mod2), contradicting (4). Since N>=4 is precisely
the positive-width odd domain, **no positive-width odd query has this
guard**.

Only two finite cycles certify these statements for all N. Their periods
and phases are proved by the actual cycle edges, including the transient;
no eventual phase is extrapolated backward.

## 3. Complete classification of the remaining small cases

The width-seven core already gives the other needed edge bits, without
another orbit construction. For k<=6,

```
H^N(2^k)=(H^N(64))>>(6-k).
```

Reading100 at even N and111 at odd N yields, for all N>=2,

```
bit_0 H^N(8)=N mod2,
bit_0 H^N(16)=1.                                     (5)
```

At N=3,e=0 the range in (3) contains only k=3, and its guard holds.
At N=4,e=0 it contains k=3,4, and both guard bits hold.
At N=5,e=0 the k=4 bit is1, whereas (3) requires0, so the guard fails.
The N=2 even case and N=3 odd case have w=0 and fall outside the
positive-width theorem. The N=2 odd case is outside this actual-readout
parameterization as well.

Consequently, for all N,e with w>=1,

```
the full alternating1 guard holds
    if and only if e=0 and N in{3,4}.                 (6)
```

These two instances are center times4 and6. In particular, the guard
fails at every even center time at least8 and every odd center time
at least5. Formula (6) restricts application of this sufficient pruning
certificate; it does not invalidate the certificate on other supplied
inputs or prove that other guarded decompositions fail.

## 4. Exact verifier and computation scope

The [verifier](../../experiments/rule30/p3_actual_alternating_guard.py)
checks the eight decisive cycle edges with independent bitwise and
scalar H implementations. It checks both parity classes of each universal
contradiction, and handles N=2,...,5 using the same saved width-seven
cycle. The
[artifact](../../experiments/rule30/p3-actual-alternating-guard.json)
retains both complete cycles, the parity witnesses, the small-case guard
bits, and source hashes.

A bounded exploratory test had fixed k=3,...,10 in advance, with maximum
core width eleven. Its conclusion reduced to the two cycles above. The
maintained verifier runs only these decisive certificates; it does not
preserve or extend a larger orbit census. No singleton prefix, growing
query sequence, GPU job, or paid computation is generated. The repository
compute charter and prior finite-core reports were read before this test.

```
uv run --offline --no-project python experiments/rule30/p3_actual_alternating_guard.py
```

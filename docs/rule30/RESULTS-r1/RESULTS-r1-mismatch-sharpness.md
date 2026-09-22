# Exact Rule 90 control for the R1 mismatch bound

Date: 2026-09-15. **P1 remains open.** The logarithmic lower bound in
[the R1 scope audit](RESULTS-r1-periodic-realization-scope.md) has the
correct order in an actual finite-seed control. Its factor-two interval
dilation also cannot be reduced by a rule-generic argument. This does not
establish an optimal leading constant for that lower bound, or exclude a
Rule-30-specific strengthening using the seed and pin together.

## 1. Exact lone-seed Rule 90 formulas

For Rule 90 started with its only one at the origin,

```text
c_0=1,   c_t=0 for t>=1;
l_t=r_t=1  iff  t=2^a-1 for some integer a>=1.
```

These are known archive controls; see the
[inverse-trace report](RESULTS-inverse-trace.md) and
[zero-set inventory](../../experiments/rule30/p1-period2-invariant/RESULTS-R1-ZERO-SET-INVENTORY.md).
The new calculation here is their exact mismatch count for every fixed
shift, rather than a new Rule 90 orbit formula.

For completeness, the cell at `x` is the parity of
`binom(t,(t+x)/2)` when the lower index is integral. The factorization of
`(1+z)^t` over `GF(2)` shows that `binom(a+b,a)` is odd exactly when
`a & b=0`. The centre at `t=2k>0` would require `k & k=0`, which is
impossible. At `x=1,t=2k+1`, the condition is `k & (k+1)=0`, equivalent
to `k=2^m-1`, including `m=0`.

Fix an integer `P>=1` and put

```text
A = {2^a-1 : a>=1},
D_P = {t>=0 : r_(t+P) != r_t} = A symmetric_difference ((A-P) intersect N).
```

For every integer `N>=1`, the number of mismatches in `[0,N)` is exactly

```text
C_P(N) = floor(log2 N) + floor(log2(N+P)) - floor(log2 P)
         - 2 * 1{an overlap t_P exists and t_P<N}.             (1)
```

The overlap exists precisely when

```text
P=2^a(2^d-1) for integers a,d>=1; then t_P=2^a-1.             (2)
```

It is unique: `P=2^b-2^a` determines `a` as the two-adic valuation of
`P`, and then determines `b`. Formula (1) counts the powers of two in
`[2,N]` and `(P,N+P]`, subtracting the common point twice.

The centre is periodic from time one. To count only its zero phases in
`[1,N)`, subtract `1{P+1 is a power of two}` from (1); this is just the
possible mismatch at time zero. Consequently, for every fixed `P`,

```text
#{1<=t<N : c_t=0 and r_(t+P)!=r_t} = 2 log2 N + O_P(1).
```

Thus an `omega(log N)` universal lower bound is false. The earlier lower
bound has coefficient one; this control has coefficient two. **It does
not prove that either coefficient is optimal.**

## 2. The multiplicative gap factor is sharp

For all sufficiently large `a`, the mismatches occur consecutively in
pairs

```text
u_a=2^a-1-P,  v_a=2^a-1,
```

followed by `u_(a+1)`. The within-pair distance is `P`; the between-pair
distance is `2^a-P`. In particular,

```text
u_(a+1)/v_a -> 2.
```

Taking `T=2^a=v_a+1`, the next mismatch is at `2T-P-1`, so there are
no mismatches in `[T,2T-P-2]`. For any fixed `lambda<2` and any fixed
additive constant, this supplies arbitrarily late empty intervals
`[T,floor(lambda*T+constant)]`.

Therefore the factor two in the existing interval guarantee
`[T,2T+P-1]` cannot be reduced using only assumptions that also hold for
Rule 90. This says nothing about optimal additive endpoints or a
strengthening that uses Rule 30's nonlinear rule.

## 3. What the Rule 30 pin adds, and what remains missing

For a Rule 30 driven left half-plane, suppose `c` is `P`-periodic after
an onset and the pin `c_t=1 => l_t=1 XOR c_(t+1)` holds there. Write
`D_j(t)=s(t+P,-j) XOR s(t,-j)`. Then

```text
D_1(t)=0 when c_t=1,
D_2(t)=D_1(t+1) XOR (1-c_t)D_1(t)
      =D_1(t+1) XOR D_1(t).                                  (3)
```

This is an elementary specialization of the already recorded
[defect recurrence](RESULTS-eventual-period.md), not a new mechanism.
It follows by applying the inverse rule at column minus one and using
periodicity of `c`. A single discrepancy is copied to its earlier
neighbouring time in (3), rather than automatically removed.

The [periodic-mask counterexample](RESULTS-inverse-trace.md) already
shows that, after a discrepancy crosses a zero phase, its earliest
time moves one step earlier per reconstructed column. Nonconstant
periodic masks do not supply automatic contraction. That construction
does not keep the lone seed's initial left half, so it does not refute a
theorem retaining the zero-initial LHP and the pin jointly.

No stronger lower bound or sublogarithmic upper bound for that joint
Rule 30 domain is proved here. The remaining useful target is still a
bound using the seed-compatible histories, not periodic-mask erasure.

## 4. Bounded independent checks

```sh
uv run --no-project python experiments/rule30/r1_mismatch_sharpness_audit.py
```

The [checker](../../experiments/rule30/r1_mismatch_sharpness_audit.py)
compares the power-of-two formula with direct bit-packed Rule 90
evolution and binomial parity, checks (1) at all 65,536 pairs
`P=1..64,N=1..1024`, and checks the paired-gap endpoints at 512 scales.
It also exhausts the finite local bit assignments for (3). The
[JSON artifact](../../experiments/rule30/r1-mismatch-sharpness-audit.json)
records the exact bounded scopes. The proofs above, rather than these
finite checks, supply the all-length conclusions.

# P2: removing the scale factor, and the OR pairing gap

Date: 2026-09-09. **No rung of the user's P2 ladder is proved here.**
There is a strict improvement to the analytic reductions, followed by an
exact Rule 30 calculation whose remaining estimate is unproved:

```
W_k / 2^k -> 0                        is sufficient for P2;
H_k / 2^(2k) -> 0                     is equivalent to P2.
```

The factors `k` and `k+1` in the previous sufficient conditions can be
removed. An explicit sequence below satisfies the new conditions and fails
both old conditions. This sequence is a proof of strictness of the
reductions, not a Rule 30 example.

No uniform decay estimate for the actual Rule 30 sequence is established.
In particular, an implication from an unproved hypothesis does **not**
count as reaching rung 2. The previous report's ladder statement has been
corrected.

## 1. Objects and evidence domains

Let `c_t=s(t,0)` be the bit, and let `A(T)=sum_(t<T)c_t` be the count of
ones. P2 asks for `A(T)/T -> 1/2`; a single bit divided by T is not that
quantity. Use the existing shell signs

```
N=2^k,   z(r)=1-2*c_(N+r),   0<=r<N.
M=max_(0<=u<=N) |sum_(r<u)z(r)|,
W=max_a |sum_r z(r)(-1)^(a dot r)|,
E_j=sum_(aligned blocks B of length 2^j) (sum_B z)^2,
H=sum_(j=0)^k E_j,   E*=max_j E_j.
```

| Result | Evidence | Domain |
|---|---|---|
| Coarse-prefix bounds, sections 2–3 | U | Universal deterministic inequalities; apply to the designated seed shell without any measure hypothesis |
| P2 equivalences using those bounds | U/R | Seed-specific after substitution; uses the existing exact dyadic-shell equivalence |
| Strictness example | U/C | Explicit artificial deterministic sequence, **not** the Rule 30 seed |
| OR truth identities | U/C | Universal Rule 30 identities; measured specialization is seed-specific |
| Pair-frequency estimate required in section 5 | **Unproved** | Must hold on the fixed lone-seed orbit; no a.e. substitute is used |
| Finite numbers and implementation checks | C/M | Exact counts at the stated lengths only |

The prior reduction `M_k=o(2^k) iff P2` is used as proved in
`RESULTS-p2-p3-cross-review-2026-09-03.md`, section 2. The Walsh subcube
identity and energy definitions are those in `RESULTS-p2-time-index-walsh.md`.
No literature review was repeated and no external analytic theorem is
invoked without proof here.

## 2. A coarse-prefix bound removes the extra k (U)

For every integer `1<=J<=k`,

```
M <= J W + 2^(k-J)-1,
M <= sqrt(J H) + 2^(k-J)-1.                    (1)
```

**Proof.** For a proper prefix of length u, discard its final
`u mod 2^(k-J)` entries. The discarded signed sum has magnitude at most
`2^(k-J)-1`, because each entry has magnitude one. The remaining prefix
decomposes, by its first J binary digits, into at most J aligned dyadic
blocks. Each block sum has magnitude at most W by the already proved
Walsh subcube identity. Also, the squared sums of these distinct blocks
are among the nonnegative terms defining H, so Cauchy–Schwarz gives
`sqrt(J H)`. The complete prefix u=N is a single root block and satisfies
both bounds as well. This proves (1).

Put `w=W/N`. Taking `J=ceil(log2(1/w))` when this is positive (and using
`M<=N` when w=1) gives

```
M/N <= w * (2+log2(1/w)).                      (2)
```

Consequently `W_k/2^k -> 0` is sufficient for P2. Equivalently, one may
hold J fixed in (1), take the limsup as k grows, and then let J grow.
This order of limits is legitimate and requires no uniform convergence
rate in k.

The existing identity `W_k^2 <= sum_h |C_k(h)|` now yields the weaker
sufficient correlation target

```
sum_h |C_k(h)| = o(2^(2k)),                    (3)
```

without the previous division by `k^2`. This remains only a target:
no bound (3) for the Rule 30 seed is supplied.

The Walsh condition is still only sufficient. For example, an alternating
bit sequence has density one-half but W=N on every shell.

## 3. Tree energy is an exact criterion, without a logarithmic factor (U)

For every nonempty dyadic sign word,

```
M^3 <= 16 N E*,
E* <= 2 N M,
E* <= H <= 8 N M.                             (4)
```

**Lower bound.** For M>=2, choose a power of two L with
`M/4 < L <= M/2`, and a prefix u attaining magnitude M. Rounding u down
to a multiple of L discards fewer than L signs, leaving magnitude at
least `M-L >= M/2`. This rounded prefix consists of at most N/L aligned
L-blocks. Cauchy–Schwarz therefore gives

```
E_log2(L) >= (M/2)^2 / (N/L) >= M^3/(16N).
```

For M=1 the same stated bound follows from `E_0=N`.

**Upper bounds.** Each aligned block sum b is the difference of two
prefix sums, so `|b|<=2M`; also `|b|<=L` for a block of length L.
Thus `sum b^2 <= 2M sum |b| <= 2MN` at every level. More precisely,

```
E_log2(L) <= min(N L, 4 N M^2/L).
```

Sum the first bound over dyadic L<=2M and the second over L>2M.
The two geometric sums are each at most 4NM. This proves (4).

Applying (4) to each actual seed shell proves

```
P2  iff  M_k/2^k -> 0
    iff  H_k/2^(2k) -> 0
    iff  max_j E_(k,j)/2^(2k) -> 0.            (5)
```

These are seed-specific equivalences after substitution, derived from
universal deterministic inequalities. In particular, the signed
correlation target becomes the exact criterion

```
sum_(j=0)^k sum_(0<=h<2^j) C_k(h) = o(2^(2k)), (6)
```

using the existing identity `E_(k,j)=sum_(h<2^j)C_k(h)`. Negative individual
correlations are retained; neither independence nor absolute values are
introduced in (6).

There is a second direct check on section 2. Walsh orthogonality applied
to the vector of aligned L-block sums gives

```
E_log2(L) <= W^2,
H <= sum_(j=0)^k min(N 2^j, W^2)
  <= W^2 * (3+2 log2(N/W)).                    (7)
```

For completeness, if there are Q=N/L blocks, the Walsh coefficients
supported on the fixed high bits are exactly the Q-point transform of
those block sums. Parseval gives `Q E_j` as their squared sum, proving
the first inequality. Splitting the geometric sum at
`j=floor(log2(W^2/N))` proves the last; `W^2>=N` follows from ordinary
Parseval. Equation (7) and (5) again show that `W=o(N)` suffices.

## 4. Strictness is witnessed by an explicit sequence (U/C)

This example is **not Rule 30**. It establishes that the removed factors
are real restrictions, not merely alternate notation.

On each shell of length `N=2^k`, k>=4, put

```
b_k(r)=(-1)^(r_0 r_1 + r_2 r_3 + ...),
m=floor(log_4 k),   L=2^(k-m),
z_k(r)=1 if r<L, and b_k(r) otherwise.
```

Unused high bits do not enter the sum in `b_k`. The two-bit factor
`(1,1,1,-1)` has Walsh magnitudes 2. Tensoring the factors shows that
the maximal Walsh magnitude and DC of b_k both equal
`B=2^ceil(k/2)`. Its sum on the aligned prefix of length L is
`P=2^ceil((k-m)/2)`.

Replacing that prefix by ones adds an everywhere nonnegative difference
of total mass L-P. Therefore the triangle inequality bounds every new
Walsh coefficient by B+L-P, and DC attains that bound:

```
W_k = DC_k = B+L-P,
L <= W_k <= B+L.
```

Since `4^m<=k<4^(m+1)`, `W_k/N -> 0`, but
`k W_k/N >= k/2^m >= sqrt(k) -> infinity`. Moreover,

```
(k+1) H_k/N^2 >= (k+1) DC_k^2/N^2
                 >= (k+1)/4^m >= 1.
```

Assembling these shells into one infinite sequence, with any finite
initial prefix, gives density one-half by section 2. It satisfies both
new conditions and neither old one. The explicit formulas were checked
for k=4,...,16; those checks supplement the all-k tensor-product proof.

## 5. Exact OR pairing and the unclosed seed estimate (U/R)

The next attempt was to use OR saturation to bound a single derivative
and thereby reach rung 3. The mechanism was the following exact identity;
its kill condition was that the rule identities alone leave either
pair type at zero frequency, without a seed-specific exclusion.

At even times `t=N+2s`, write the actual neighbourhood as `(l,c,r)`.
The next centre bit is `d=l XOR (c OR r)`. Define

```
A_s=(z(t)+z(t+1))/2,
B_s=(z(t)-z(t+1))/2.
```

Rule 30 gives the following complete table:

| l c r | d | A | B |
|---|---:|---:|---:|
| 000 | 0 | 1 | 0 |
| 001 | 1 | 0 | 1 |
| 010 | 1 | -1 | 0 |
| 011 | 1 | -1 | 0 |
| 100 | 1 | 0 | 1 |
| 101 | 0 | 1 | 0 |
| 110 | 0 | 0 | -1 |
| 111 | 0 | 0 | -1 |

Thus

```
A = 1_{c=0,l=r} - 1_{c=1,l=0},
B = 1_{c=0,l!=r} - 1_{c=1,l=1}.
```

For a Walsh mask whose low bit is a and whose other bits form b,

```
hat z(2b)   = 2 hat A(b),
hat z(2b+1) = 2 hat B(b).                      (8)
```

This retains every overlapping neighbourhood exactly. Let D count the
pairs with a centre-bit change, and S count the pairs with a stay.
Then `D+S=N/2`, `sum |B|=D`, `sum |A|=S`, and

```
W <= 2 max(D,S) = (N+|C_k(1)|)/2,
C_k(1)=N-4D.                                 (9)
```

Therefore a seed-specific estimate

```
min(D_k,S_k) >= epsilon N/2 eventually         (10)
```

for any fixed epsilon>0 would prove
`W_k<=(1-epsilon)N`, reaching rung 3. **Estimate (10) is unproved.**
It is not a recognized external hypothesis and is not offered as rung 5.
The OR truth table supplies the exact counts being requested, not their
frequency in the designated orbit.

The existing Rule 30 all-zero fixed diagram has D=0. The existing 7-by-4
torus, with rows

```
0000001
1000011
0100110
1111101
```

has centre `0101` at the leftmost displayed position and S=0 at the
chosen even-time pairing. All 28 cyclic gates were rechecked with the
frozen ladder. Thus **a rule-only proof of (10) is false**, on exact
diagrams. These are not counterexamples to the seed-specific estimate;
they identify the seed hypothesis that the calculation has not used.
This repeats no claim that general invariant measures can settle P2.

Call the unresolved step the **OR pair-frequency gap**: exact saturation
identities do not control the proportions of the two temporal pair types
on the fixed seed. It is a fundamental obstruction to deriving the
estimate from local rule identities alone; whether the seed forces it
remains unresolved.

### The density energy keeps only one of the two channels

For density itself there is an exact refinement. Extend H's definition to
arbitrary real words using the same block-square sum. Every dyadic block
of z of length at least two has sum twice the sum of its corresponding
A-block. Hence

```
H(z) = N + 4 H(A).                            (11)
```

The B channel, although necessary for controlling every Walsh coefficient,
drops out of the density energy beyond the singleton term. On the
alternating-centre torus above, A=0, so H(z)=N while W=N. Thus a failure
to prove a positive stay frequency must not be interpreted as a failure
of P2's energy criterion.

Trying to iterate the physical OR identity does not close an estimate:
A is a ternary time-pair field, not another Rule 30 centre trace. Already
the actual k=3 shell is `11000101`, with
`A=(-1,1,0,0)`, its first shell containing all three values. An induction
would need a proved evolution or bound for these coarse fields, retaining
the overlapping physical neighbourhoods. Equation (11) by itself is just
an exact identity. **No such contraction has been proved here.**

**Follow-up:**
[`RESULTS-p2-temporal-mean-nonclosure.md`](RESULTS-p2-temporal-mean-nonclosure.md)
supplies an exact local evolution for the entire spatial two-step mean
field: it has a local inverse to the original binary row. However, two
explicit period-14 configurations have identical four-step mean fields
and different eight-step fields. Thus a mean-only scale iteration fails
at the next stage; no seed-specific energy decay follows.

The finite seed records are diagnostic input to this failed contraction
attempt, not evidence of a limit:

| k | N | D (changes) | S (stays) | bound from (9) | actual W |
|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 1 | 0 | 2 | 2 |
| 2 | 4 | 0 | 2 | 4 | 4 |
| 3 | 8 | 2 | 2 | 4 | 4 |
| 4 | 16 | 5 | 3 | 10 | 6 |
| 5 | 32 | 13 | 3 | 26 | 14 |
| 8 | 256 | 61 | 67 | 134 | 46 |
| 10 | 1,024 | 242 | 270 | 540 | 104 |
| 12 | 4,096 | 1,068 | 980 | 2,136 | 240 |

## 6. Controls, reproduction, and scope (C/M)

Run:

```sh
uv run python experiments/rule30/p2_coarse_energy_audit.py
cd experiments/rule30
uv run python -m unittest test_p2_time_index_walsh_probe.py test_p2_dyadic_shell_probe.py
```

The first command writes or exactly reproduces
`experiments/rule30/p2-coarse-energy-audit.json`. Checks comprise:

- all 65,814 sign words at lengths 1,2,4,8,16;
- 262,948 coarse-depth checks and 328,762 level-energy checks;
- 13 strictness-example shells, k=4,...,16;
- all eight OR truth rows, using the unchanged ladder rule;
- 256 rows of scalar, frozen-rule evolution against the packed seed
  generator, plus the existing centre generator through 8,192 bits;
- every coefficient of (8) on the 12 seed shells k=1,...,12;
- equation (11) on every tested sign word of length at least two, and
  on the 12 actual seed shells;
- the 28 gates of the displayed Rule 30 torus;
- the actual Rule 90 seed control through 256 times;
- five calls' records from unchanged `controls.rule90_control`, T=2,4,6,8,10.

For the Rule 90 seed, every shell k>=1 is all-zero in bits, hence
`M=N`, `W=N`, and `H=2N^2-N`. None of the vanishing hypotheses holds.
The new inequalities therefore do not falsely prove its density is
one-half. The Rule 30 OR table itself fails for Rule 90, as it must.

The all-time control is elementary, not a finite extrapolation: the
Rule 90 centre is zero at odd times by spatial parity; at time 2m>0 its
bit is `binom(2m,m) mod 2`, zero because
`binom(2m,m)=2 binom(2m-1,m-1)`. The finite simulation calibrates this
symbolic control. The two existing unit-test modules also pass all 18
tests.

All universal inequalities are fully symbolic above; their finite tests
are calibration, not extrapolation. No ensemble of initial rows is
averaged. No finite computation establishes an asymptotic claim. No claim
of non-automaticity, P1, or any of P2 rungs 1–5 is made. The remaining
target is an actual seed-specific bound in (3), (6), (10), or another
sufficient estimate. The new result is a strictly weaker analytic
requirement, together with the exact point where the tested nonlinear
contraction stops.

# Seed-specific dyadic-energy and time-index Walsh routes to P2

## Status

**OPEN, with exact sufficient theorems and finite diagnostics.**  The measured
dyadic energies and spectra are random-scale through the recorded horizons,
but no all-scale energy, Walsh, or autocorrelation bound is proved.

This route is not the archived arbitrary-input Walsh arm.  Its variables are
the binary digits of a time on the actual lone-seed orbit.

Code: `experiments/rule30/p2_time_index_walsh_probe.py` and
`test_p2_time_index_walsh_probe.py`.

**2026-09-09 analytic refinement:**
[`RESULTS-p2-coarse-energy-and-or-pairing.md`](RESULTS-p2-coarse-energy-and-or-pairing.md)
proves that `W_k=o(2^k)` already suffices, and that `H_k=o(2^(2k))` is
equivalent to P2. The sufficient conditions below remain correct, but
their extra scale factors are unnecessary. No such estimate for the
actual Rule 30 seed has been proved.

## 1. The correct Boolean functions

Let `c_t` be the lone-seed center bit.  For each `k>=1`, define a Boolean
function on `k` time-index bits by

```text
f_k(r) = c_(2^k+r),        0 <= r < 2^k,
z_k(r) = (-1)^f_k(r).
```

Its unnormalized Walsh transform is

```text
hat(z_k)(a) = sum_r z_k(r) (-1)^(a dot r),
W_k = max_a |hat(z_k)(a)|.
```

The coefficient at `a=0` is the signed discrepancy of the complete canonical
dyadic shell.  More importantly, `W_k` controls partial shells as well.

## 2. A weaker contiguous-block energy theorem

Full Walsh control is not necessary.  At dyadic level `j`, partition the
length-`N=2^k` shell into aligned blocks of length `2^j` and define

```text
E_(k,j) = sum_(blocks B at level j) (sum_(r in B) z_k(r))^2,
H_k = sum_(j=0)^k E_(k,j).
```

**Theorem.**  Every partial-shell discrepancy obeys

```text
M_k^2 <= (k+1) H_k.
```

Consequently

```text
(k+1) H_k / 2^(2k) -> 0
```

is sufficient for P2.

**Proof.**  The binary expansion of a prefix partitions it into at most one
aligned block at each of the `k+1` levels.  If their signed sums are `b_j`,
Cauchy--Schwarz gives

```text
M_k^2 <= (sum_j |b_j|)^2
      <= (k+1) sum_j b_j^2
      <= (k+1) H_k.
```

The dyadic-shell lemma then proves the conclusion.  QED.

This target retains only contiguous time blocks, so it is closer to P2 than
flatness against every XOR character.  It also has an exact tree composition:
if a signed word has halves `u,v`, then

```text
H(uv) = H(u) + H(v) + (sum u + sum v)^2.
```

The missing Rule 30 ingredient is a uniform bound on the parent block sums,
not a missing algebraic identity.  For example, any
`H_k=O(2^((2-delta)k))` with fixed `delta>0` proves P2.

### Exact signed-correlation form of the energy

The tree energy is itself an exact XOR-correlation statistic, but one with no
absolute values.  Write

```text
C_k(h) = sum_r z_k(r) z_k(r XOR h).
```

At level `j`, the ordered pair `(r,s)` lies in one aligned block of length
`2^j` exactly when `r XOR s < 2^j`.  Expanding all block squares therefore
gives

```text
E_(k,j) = sum_(0 <= h < 2^j) C_k(h),
H_k     = sum_(j=0)^k sum_(0 <= h < 2^j) C_k(h).
```

Equivalently, since `C_k(0)=N`,

```text
H_k = (k+1)N
      + sum_(h=1)^(N-1) (k-floor(log2 h)) C_k(h).
```

This identity is stronger guidance than the earlier `l1` sufficient
condition: P2 does **not** require small individual XOR correlations or small
`sum_h |C_k(h)|`.  It is enough to prove the signed, bit-scale cumulative
energy bound

```text
(k+1) sum_(j=0)^k sum_(h<2^j) C_k(h) = o(N^2).
```

Every inner prefix is nonnegative because it equals a sum of squared block
sums.  The remaining problem is thus to keep their total subquadratic, while
allowing cancellation among the individual nonzero-shift correlations.  This
is currently the weakest exact correlation target found for P2.

## 3. Walsh-to-P2 theorem

**Theorem.**  If

```text
k W_k / 2^k -> 0,
```

then the Rule 30 center column has limiting density `1/2`.

**Proof.**  Consider an aligned dyadic interval inside the shell.  In binary
coordinates it is a subcube obtained by fixing some `q` high bits and leaving
the remaining `k-q` low bits free.  The indicator of a fixed high-bit
assignment `b` has the character expansion

```text
1_(r_high=b) = 2^(-q) sum_(a supported on the high bits)
                         (-1)^(a dot (r_high XOR b)).
```

After multiplying by `z_k` and summing over `r`, the signed sum on that
subcube is an average of `2^q` Walsh coefficients.  Its absolute value is
therefore at most `W_k`.

Every integer prefix `[0,u)` of the shell is a disjoint union of at most `k`
such aligned dyadic intervals, by the binary expansion of `u`.  Consequently
the maximum partial-shell discrepancy from the dyadic-shell lemma satisfies

```text
M_k <= k W_k.
```

The hypothesis gives `M_k=o(2^k)`, and the dyadic-shell lemma gives P2.  QED.

This is a sufficient condition, not a reformulation: P2 may hold even when a
nonzero Walsh character has large correlation.

## 4. Exact derivative bridge

Define the XOR autocorrelation

```text
C_k(h) = sum_r z_k(r) z_k(r XOR h).
```

Walsh orthogonality gives the exact identity

```text
hat(z_k)(a)^2 = sum_h C_k(h) (-1)^(a dot h).
```

Thus

```text
W_k^2 <= sum_h |C_k(h)|.
```

Consequently the averaged condition

```text
sum_h |C_k(h)| = o(2^(2k) / k^2)
```

already implies `k W_k/2^k -> 0` and proves P2.  This is weaker than
controlling every nonzero shift separately.

For example, a uniform bound

```text
|C_k(h)| <= 2^(k(1-delta))       for every h != 0
```

with any fixed `delta>0` would imply
`W_k <= O(2^(k(1-delta/2)))` and hence P2.

This is the precise point of contact with the period-two investigation.  For
`h=2^j`, the pairing `r -> r XOR 2^j` compares center traces whose ordinary
times differ by `2^j` inside alternating dyadic blocks.  Those are traces of
the two same-orbit configurations

```text
F^t(delta_0) and F^(t+2^j)(delta_0).
```

The exact two-orbit Rule 30 defect recurrence already in the temporal
period-two work
applies without assuming equality:

```text
d' = d_left XOR d_center XOR d_right
     XOR center*d_right XOR right*d_center XOR d_center*d_right.
```

The old period-two target asks a qualitative question for shift two: the
center defect cannot vanish forever.  The P2 spectral target is much stronger:
prove quantitative cancellation, on average over XOR shifts or uniformly in
them.  The recurrence is reusable, while the alternating-fiber `D8` and Peel
monoids are not—they arise only after imposing a special trace.

## 5. Finite measurements

Using the independently generated band cache, the following values are exact
for the recorded prefix:

| `k` | shell length | DC | `W_k` | `W_k/sqrt(k 2^k)` | max shell prefix |
|---:|---:|---:|---:|---:|---:|
| 8 | 256 | 6 | 46 | 1.016 | 12 |
| 9 | 512 | 52 | 68 | 1.002 | 52 |
| 10 | 1,024 | 0 | 104 | 1.028 | 36 |
| 11 | 2,048 | -4 | 156 | 1.039 | 25 |
| 12 | 4,096 | -56 | 240 | 1.083 | 65 |
| 13 | 8,192 | -154 | 362 | 1.109 | 183 |
| 14 | 16,384 | -112 | 616 | 1.286 | 249 |
| 15 | 32,768 | 64 | 756 | 1.078 | 180 |
| 16 | 65,536 | 356 | 1,352 | 1.320 | 367 |
| 17 | 131,072 | -772 | 1,664 | 1.115 | 889 |
| 18 | 262,144 | -104 | 2,664 | 1.226 | 330 |

The maximum scale ratio stays between `1.00` and `1.33`, consistent with the
random-function scale `sqrt(k 2^k)`.  At `k=18` the largest absolute
correlation for a single-bit XOR derivative is `1,184`, or about `0.00452` of
the shell.  Neither observation proves decay.

The weaker dyadic-tree energy behaves much closer to its random-sign scale
`(k+1)N` than to the quadratic worst case.  Here every value includes all
tree levels from singletons through the complete shell:

| `k` | `N` | `H_k` | `H_k/N` | `sqrt((k+1)H_k)/N` |
|---:|---:|---:|---:|---:|
| 8 | 256 | 1,768 | 6.91 | 0.493 |
| 10 | 1,024 | 10,256 | 10.02 | 0.328 |
| 12 | 4,096 | 54,856 | 13.39 | 0.206 |
| 14 | 16,384 | 291,952 | 17.82 | 0.128 |
| 16 | 65,536 | 1,230,080 | 18.77 | 0.070 |
| 18 | 262,144 | 3,907,312 | 14.91 | 0.033 |
| 20 | 1,048,576 | 23,676,184 | 22.58 | 0.021 |

The last column is the theorem's upper bound divided by `N`, not the observed
prefix discrepancy.  Its decrease is finite evidence only.

The complete autocorrelation transform gives a second, unusually stable
finite diagnostic:

| `k` | max nonzero `|C_k(h)|` | `sum_h |C_k(h)|` | `log_N` of the sum |
|---:|---:|---:|---:|
| 8 | 60 | 4,596 | 1.521 |
| 10 | 144 | 35,360 | 1.511 |
| 12 | 368 | 300,416 | 1.516 |
| 14 | 720 | 2,367,136 | 1.512 |
| 16 | 1,568 | 19,151,408 | 1.512 |
| 18 | 3,176 | 152,232,080 | 1.510 |
| 20 | 6,792 | 1,213,086,912 | 1.509 |

Thus the measured `l1` norm is consistent with `N^(3/2)` rather than the
worst-case `N^2`.  Proving any fixed power saving from `N^2` would be more
than enough for the theorem.  This finite exponent is still not a proof.

The time-index ANFs close a cheaper algebraic shortcut.  From `k=4` through
`20`, their degree is always `k` or `k-1`; their term density approaches
one half (for example `32,893/65,536` at `k=16` and
`523,423/1,048,576` at `k=20`).  The full-degree cases through this range are
`k=4,5,8,13,19`; elsewhere the degree is `k-1`.  Thus these functions are not
bounded-degree quadratic phases to which a standard quadratic exponential-sum
formula applies.  High degree or dense ANF is not itself evidence of Walsh
decay, so this is a route disposition rather than positive evidence.

The transform is exact integer arithmetic.  Tests pin two known transforms,
Parseval's identity, aligned-block sums, XOR derivatives, and a direct Rule 30
shell.

## 6. Work order and failure modes

The weakest current proof target is a subquadratic dyadic-tree energy bound.
It uses only ordinary contiguous blocks and should be attempted before full
Walsh decay.  A second target is a bound on `W_k`, preferably through the
derivative identity and the exact same-orbit defect field.  Either must be
seed-specific and all-scale.  The following do not suffice:

- the arbitrary-initial-row Walsh spectrum of the `t`-step local function;
- high ANF degree, which can coexist with a huge DC coefficient;
- one or finitely many small XOR correlations;
- a fit of the displayed finite values; or
- qualitative nonidentity of two shifted traces.

A useful next lemma would bound `H_k` by `O(2^((2-delta)k))`, equivalently
bound the sum of the nonnegative cumulative correlations above, or give a
recursive spectral norm for the complete same-orbit defect state.  The
absolute-correlation route is sufficient but needlessly strong.  Any recursion
must retain the actual dyadic seam and absolute phase identified by the
temporal-period-two negative results.

## Reproduction

From `experiments/rule30`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  test_p2_time_index_walsh_probe.py
PYTHONDONTWRITEBYTECODE=1 python3 p2_time_index_walsh_probe.py \
  --min-k 8 --max-k 18 \
  --band-cache \
  ../overnight-arms/frontier_attack/a25_checkerboard_growth_extended/cache/band30_T33554432.bin
```

No finite spectrum in this report is an asymptotic claim.

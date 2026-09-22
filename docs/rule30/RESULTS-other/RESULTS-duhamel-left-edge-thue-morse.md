# The mandatory left-edge defect has an exact Thue-Morse response

Date: 2026-09-10. **Exact seed-specific identities; no P1, P2, or P3 solution.**

Rule 30 equals Rule 150 plus the quadratic source N_i=x_i*x_(i+1) over
GF(2). Its Duhamel representation is already recorded in
[Arm 5](ARM5-superposition.md) and the
[bilinear-defect audit](RESULTS-followup-bilinear-rank.md).
Here we isolate a forced part of this source and evaluate its entire
contribution to the center in closed form. This consequence was not found
in those reports; no claim of literature priority is made.

For the lone-seed center c_t and the Thue-Morse bit theta(t), the result is

```
c_t = theta(t) XOR R_t,    t>=1,
```

where R_t is the Rule-150 projection of all nonlinear defects except the
mandatory left-edge defect. The latter is active at every positive time,
contrary to the proposed explanation that nonlinearity is silent on the left.

## 1. Exact Duhamel identity and conventions

Let x^0=e be the lone seed, and use positions increasing to the right. Put

```
F(x)_i = x_(i-1) + x_i + x_(i+1) + x_i*x_(i+1),
(Lx)_i = x_(i-1) + x_i + x_(i+1),
N_i^s = x_i^s*x_(i+1)^s,
A(z) = z^-1 + 1 + z,
G(t,j) = coefficient of z^j in A(z)^t.
```

All sums in these identities are in GF(2). Induction on t gives

```
x^t = L^t e + sum_(s=0)^(t-1) L^(t-1-s) N^s.
```

In coordinates this is precisely

```
x_i^t = G(t,i) + sum_(s<t) sum_j G(t-1-s,i-j) N_j^s.
```

The source enters the next row, explaining the exponent t-1-s. This is
linear propagation with nonlinear feedback; N remains a function of the
unknown Rule 30 row. No independence or mixing follows from the rewriting.

## 2. The left-edge source never switches off

Finite propagation gives zero outside [-t,t]. The two extreme neighborhoods
001 and 100 both output one, so x_-t^t=x_t^t=1 for every t>=0.

The second cell from the left at the next time is

```
x_-t^(t+1) = 0 XOR (1 OR x_(-t+1)^t) = 1.
```

Consequently

```
x_-t^t = x_(-t+1)^t = 1, and N_-t^t=1, for every t>=1.
N_t^t = x_t^t*x_(t+1)^t = 0, for every t>=0.
```

Thus the nonlinear source is active at the leftmost occupied cell at every
positive time and vanishes at the rightmost occupied cell. It is not confined
to the right half. Already x^1 has ones at -1,0,1, giving N_-1^1=N_0^1=1.

The regular left edge is partly maintained by this nonlinear term. If a_t
denotes the second leftmost cell, Rule 150 obeys a_(t+1)=1+a_t, whereas
Rule 30 obeys a_(t+1)=1+a_t+a_t=1. The quadratic cancellation stabilizes
this edge value instead of generating randomness there.

## 3. Half of a Rule-150 row has Thue-Morse parity

Symmetry gives G(t,j)=G(t,-j). Also A(1)^t=1, so the total parity of a row
is one; symmetric pairs cancel, leaving

```
G(t,0)=1 for every t>=0.
```

Define h_t=sum_(j>0)G(t,j). Frobenius gives

```
A(z)^(2n)=A(z^2)^n,
h_(2n)=h_n.
```

Multiplying the even row by z^-1+1+z shows that the three contributions
to positive-position parity are h_n, h_n, and h_n+1. Therefore

```
h_0=0,    h_(2n)=h_n,    h_(2n+1)=h_n+1.
```

These are exactly the recurrences for theta(t)=popcount(t) modulo two.
Thus h_t=theta(t) for all t.

## 4. Closed form for the accumulated left-edge contribution

Let

```
E_t = sum_(s=1)^(t-1) G(t-1-s,s),    t>=1.
```

This is the center response to the mandatory source at position -s and
injection time s+1. Consider the finite Laurent polynomial

```
Q_t(z) = sum_(s=0)^(t-1) z^-s A(z)^(t-1-s).
```

The finite geometric-sum identity gives

```
(1+z) Q_t(z) = A(z)^t + z^-t.
```

Writing q_j for its coefficients and summing the coefficient equations over
all j<=0, the left side telescopes to q_0. The right side is

```
sum_(j<=0)G(t,j) + 1 = (1+h_t)+1 = h_t.
```

Removing the s=0 term from Q_t removes A^(t-1), whose center coefficient is
one. Hence the all-length identity is

```
E_t = 1 + theta(t),    t>=1.
```

## 5. Rule 30 as Thue-Morse plus the remaining projected defects

The initial source N^0 is zero. At positive time s its only possible nonzero
positions are -s,...,s-1, and the first of these is the mandatory one. Define

```
R_t = sum_(s=1)^(t-1) sum_(j=-s+1)^(s-1)
          G(t-1-s,-j) x_j^s*x_(j+1)^s,    t>=1.
```

The empty sum is zero. Since the unforced center is G(t,0)=1, Duhamel gives

```
c_t = 1 + E_t + R_t = theta(t) + R_t,    t>=1.
```

The time-zero exception is c_0=1; it has no effect on density or eventual
periodicity. R is still an endogenous, nonlocal projected parity, not a
prescribed stochastic source. This identity does not bound its complexity.

## 6. What would be needed for P2

Interpreting signs and averages over the real numbers, P2 is now exactly
the residual-correlation target

```
(1/T) sum_(t=1)^T (-1)^theta(t) (-1)^R_t -> 0.
```

Balance of R by itself would not suffice: R=theta would cancel the background
completely. Nonzero source density also does not control this weighted parity.

One sufficient condition would be R_(2n)=R_(2n+1) outside o(T) pairs, since
theta(2n) and theta(2n+1) are opposite. The finite measurements below offer
no support for this sparsity condition. A weaker exact requirement is signed
cancellation across the exceptional pairs. For n>=1,

```
(-1)^c_(2n) + (-1)^c_(2n+1)
 = 2 (-1)^(theta(n)+R_(2n)) [R_(2n) != R_(2n+1)].
```

Obtaining a sublinear sum of these signed contributions remains unproved.
The identity identifies the unknown correlation; it does not estimate it.
Likewise, P1 needs to exclude cancellation leaving an eventually periodic
center. P3 needs an algorithmic argument beyond evaluating this expansion.

## 7. Exact finite verification

Run:

```sh
uv run python experiments/rule30/duhamel_edge_audit.py
```

All checks passed:

* the full-row decomposition into the unforced Rule-150 row, mandatory edge
  response, and remaining response, through time 8192;
* the half-row parity and E_t=1+theta(t) identities through time 8192;
* explicit Duhamel sums over injection times and positions for every center
  time through 512;
* independent scalar truth-table replay of Rules 30 and 150 through time 128.

Measured, not asymptotic conclusions: R_t=1 at 4,147 of the times 1,...,8192.
Among n=1,...,4095, the pair R_(2n),R_(2n+1) disagrees 2,007 times.
Neither statistic indicates a small correction in this sample; neither proves
an asymptotic density or refutes a possible later sparsity statement.

## 8. Correction to the existing kernel description

The product over binary digits of t has 3^popcount(t) terms before collection,
not necessarily that many surviving monomials. For example

```
A(z)^3 = z^-3 + z^-2 + 1 + z^2 + z^3
```

has five terms, whereas 3^popcount(3)=9. Cross-factor contributions cancel
in GF(2). Arm 5's two descriptions of this as an exact support count have
been corrected to an upper bound. Its carry-DP and directly enumerated counts
are separate from this prose error; this audit does not rerun its large census
or infer an asymptotic growth exponent from finite measurements.

## 9. Spectral interpretation: sufficient conditions and false necessities

The measured 4,147 residual ones out of 8,192 times establish a marginal
count, not independence from theta. On the same interval t=1,...,8192,
theta has 4,097 ones. A hypothetical residual obtained by changing just 50
of theta's zero bits to ones therefore has exactly the measured residual
one-count, while theta XOR that residual has only 50 ones. This is a
counterexample to the statistical inference, not a proposed Rule 30 orbit.

Nor does the orthogonality target require an absolutely continuous spectrum
or positive entropy. Take the hypothetical periodic residual R_t=t modulo 2.
The defining Thue-Morse recurrences give

```
theta(t) XOR (t modulo 2) = theta(floor(t/2)).
```

Thus the output repeats each Thue-Morse bit twice. Every aligned block of
four signs sums to zero, and every sign prefix beginning at zero has absolute
sum at most two. P2's correlation target holds. Yet the residual sign
sequence is (-1)^t, with pure-point spectrum at frequency 1/2 and zero entropy.
This proves that an absolutely continuous residual spectrum is not necessary
for the correlation target. It does not identify the actual Rule 30 spectrum.

A precise sufficient spectral route is available. Work with signs
a_t=(-1)^theta(t) and b_t=(-1)^R_t. If their empirical autocorrelations exist
at every integer lag, they define spectral probability measures mu_a, mu_b.
If mu_a and mu_b are mutually singular, then the average a_t*b_t tends to zero.
To see this, use normalized finite Fourier polynomials: their squared
moduli converge weakly to these measures, while their inner product is the
time-average cross product. Split this inner product using a continuous
partition separating the two measures, then apply Cauchy-Schwarz to both
parts. Each bound can be made arbitrarily small by mutual singularity.

The signed Thue-Morse autocorrelation measure is singular continuous, so an
absolutely continuous mu_b would be sufficient under those existence
hypotheses. It is one possible sufficient theorem, not a necessary one.
This statement concerns the observable's autocorrelation measure, not the
entire dynamical spectrum. The raw 0/1 observable also has a nonzero-mean
component. See [Baake and Grimm on signed Thue-Morse diffraction](https://arxiv.org/abs/0809.0580).

Even absolutely continuous diffraction does not imply independent noise or
positive entropy: deterministic Rudin-Shapiro and fair Bernoulli sequences
provide the standard zero-versus-positive entropy comparison with the same
diffraction. See [Baake and Grimm's construction](https://arxiv.org/abs/0810.5750).

## 10. Exact relation to the existing time-index Walsh route

There is also an exact finite spectral statement that needs no invariant
measure or autocorrelation limit. On the canonical shell t=2^k+j, define

```
a_k(j)=(-1)^c_(2^k+j),
b_k(j)=(-1)^R_(2^k+j),         0<=j<2^k,
m=2^k-1.
```

Since theta(2^k+j)=1+theta(j),

```
b_k(j) = -a_k(j) (-1)^popcount(j),
Walsh(b_k)(u) = -Walsh(a_k)(u XOR m).
```

The second equation follows immediately by multiplying Walsh characters.
The complete multiset of absolute Walsh coefficients is unchanged, as are
its maximum and every absolute spectral moment. The residual's zero-frequency
coefficient is the negative of the center's all-ones-mask coefficient; the
center discrepancy is the negative of the residual's all-ones-mask coefficient.

Therefore near balance of the residual measures a different coefficient
from the one needed for P2. Masking with theta does not itself flatten the
Walsh spectrum or improve the uniform Walsh bound from the
[existing time-index analysis](RESULTS-p2-time-index-walsh.md).
These are Walsh transforms in binary time digits, not ordinary Fourier
spectral measures; the two uses of spectrum should not be conflated.

The verifier now checks all 8,190 coefficients on shells k=1,...,12,
the periodic-residual identity and prefix bound through time 8192, and the
matching-marginal counterexample above. All pass. No correlation-decay estimate
for the actual Rule 30 residual is established.

The [calibrated spectral follow-up](RESULTS-duhamel-spectral-probe.md) supplies
an exact same-spectrum/zero-correlation counterexample using a five-step
Thue-Morse shift, audits the formal GF(2) transfer function, and records
normalized FFT diagnostics through 131,072 samples with controls.

The [defect-frequency audit](RESULTS-defect-frequency-polytope.md) proves
the exact stationary maximum P(11)=2/5, derives a cumulative defect-count
bound for the finite seed, and explains why these count bounds do not
control the residual's mask-intersection parities.

## A measurement of the residual that establishes nothing, and the reason

Pre-registered in `experiments/rule30/PREREGISTRATION-p1-thue-morse-residual.md`.
**Its headline is withdrawn.** The section is kept because the reason it failed
is a reusable no-go, and because two of its three defects were already
anticipated in this document.

**What was measured.** `R_t = c_t XOR theta(t)` over `t` in `[1, 2^23)`, with
every lag to `n/2` swept. Residual density `0.5002161` (+1.25 null sd) against
the column's `0.5002196` (+1.27 sd); residual `max abs z = 5.2244` against the
column's `5.5220`, a gap of `0.2976` against a registered kill at `1.0`. No
kill fired.

**Why that null is empty.** XOR-ing a mask `m` into `c` multiplies the sign
sequence by `(-1)^(m_t)`, so the signed uncentered lag correlation becomes
`A'(l) = sum_t x_t x_(t+l) (-1)^(m_t XOR m_(t+l))`. The multiplier factors out
of the sum exactly when `m_t XOR m_(t+l)` is constant in `t`. For the period-2
mask `m_t = t mod 2`,

```text
x'_t x'_(t+l) = x_t x_(t+l) (-1)^t (-1)^(t+l) = x_t x_(t+l) (-1)^l,
```

so `corr'(l) = (-1)^l corr(l)` and **`abs z(l)` is preserved exactly at every
lag.** Checked over all `4194303` lags, not just the maximum: the two `abs z`
arrays differ by `0.0e+00` and share the argmax lag `1656153`.

**Which comparison that kills, and which it does not.** Imposing
`m_t XOR m_(t+l)` constant in `t` at `l = 1` forces `m` constant or
alternating, so the exactly invariant family is `{0, 1, t mod 2, 1 + t mod 2}`
and nothing else. Theta is not in it: `theta(0) XOR theta(1) = 1` while
`theta(1) XOR theta(2) = 0`, and the multiplier was measured to vary with `t`
at every lag tried. The invariance therefore forces

```text
abs z(c)  =  abs z(c XOR (t mod 2)),
abs z(R)  =  abs z(R XOR (t mod 2)),
```

and **not** `abs z(c) = abs z(R)`, which is the pair this run compared.
Section 9's worked example `theta XOR (t mod 2) = theta(floor(t/2))` is the
second line, not the third, and it is visible in the ensemble: masking `c` by
`theta(floor(t/2))` reproduces theta's own gap `-0.29763259112134577` and its
pointwise figure `4.976789967164454` to every digit. So the run was not blind
by mathematical invariance. It was blind empirically, which is weaker and is
the next paragraph.

**Calibration over 53 masks rather than seven.** For 48 i.i.d. balanced masks
the signed gap `max abs z(c XOR m) - max abs z(c)` has mean `-0.327`, sd
`0.219`, range `-0.655` to `+0.443`; none reached `1.0`. Five structured
deterministic masks (Rudin-Shapiro, period 3, period 4, `theta(floor(t/2))`,
`theta(t+5)`) fall inside that range. A Gumbel fitted to the ensemble has
scale `0.171` against the asserted `1/sqrt(2 ln 2N) = 0.177`, so the noise
model holds, but `0.18` is that SCALE and the sd is `0.219`: the registered
kill at `1.0` is `4.6` sd of the statistic's own noise, not `5.6`, with fitted
upper-tail probability `2.3e-4`. Theta's `-0.2976` sits at the 63rd percentile
of the random draws.

**The bar is unreachable for this mask family, not unreachable.** A mask
carrying real structure moves the statistic enormously: the Rule 90 residual
`R_t = theta(t)` reaches `max abs z = 485.72`, a gap of `480`, and an
unrestricted choice such as `m_t = c_t` drives the masked trace constant. The
defensible statement is about power, not possibility. Against a mask that
leaves the sequence noise-like a `1.0` gap is a `4.6` sd event, so the kill had
almost no power against the alternative it was aimed at; it was not incapable
of firing.

One exact case does survive as blindness rather than weakness. A mask that is
`l`-periodic at the argmax lag leaves that lag's correlation untouched: the
column's argmax `1656153` is divisible by `3`, so the period-3 mask moves
`max abs z` by `8.9e-16` while moving individual lags by up to `4.34`.

**The correct scope of the run** is a statement about the instrument: at
`T = 2^23`, `max abs z` does not separate the centre column from its
Thue-Morse mask, and the separation it failed to find is smaller than its own
sampling noise. That supports no claim about whether the Thue-Morse
decomposition simplifies anything.

**Two of the three defects were already in this document.** Section 7 above
already measures the residual (`R` ones `4147/8192`, pair-disagreements
`2007`), so the registration's claim that the catalog held no measurement of
`R_t` is false against its own source. Section 9 already pre-registers the
counter-argument, that a marginal count "establishes a marginal count, not
independence from theta", and gives `theta XOR (t mod 2) = theta(floor(t/2))`
as the worked counterexample: the same period-2 mask that is shown above to
leave the statistic exactly invariant. A catalog grep for "mutual information",
"row weight" and "column entropy" returned zero and was taken as novelty; the
document that the identity record points at contained both the measurement and
its refutation.

The Walsh relation `4cdee047bcdb8c0d` is also already proved and already gives
the absolute Walsh multiset, its maximum and every absolute spectral moment as
unchanged under theta-masking. "No simplification" was in the catalog in exact
proved form before this run.

**The Rule 90 control was vacuous.** For Rule 90 the centre column is `0` for
every `t >= 1`, so `(0 XOR theta)[1:] == theta[1:]` is the XOR identity and
passes for any array whatsoever; substituting a deliberately wrong `theta`
still passes it. It establishes only that the Rule 90 column is all-zero after
`t = 0`, not that the residual is formed correctly, which is what the
registration gated INCONCLUSIVE on. The registration's Q4 also required the
control's autocorrelation to exceed the threshold and that half never ran; it
would have passed, at `max abs z = 485.72`.

```sh
uv run python experiments/rule30/p1_thue_morse_residual.py
uv run python experiments/rule30/p1_thue_morse_mask_calibration.py
```

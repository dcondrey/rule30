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

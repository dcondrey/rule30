# Bilateral frequency extraction: bounded potential, unresolved nonlinear current

Date: 2026-09-16. **Exact reformulation at every nonreal unit frequency;
no spectral cancellation, density theorem, or prize result.**

The [one-sided classification](RESULTS-fundamental-frequency-search.md)
leaves bilateral weights explicitly open. They do remove the endpoint
difficulty at a fixed nonreal unit frequency. The resulting current is
still nonlinear and depends on the actual orbit. This is the elementary
Green function of the existing linear operator, applied to the archive's
exact integer current identity; no literature-priority claim is made.

## 1. The exponentially decaying Green function

Let `(Lx)_j=x_(j-1)+x_j+x_(j+1)` on the full integer line. For
`lambda` outside the real interval `[-1,3]`, the equation

```text
r + r^(-1) = lambda-1
```

has exactly one root `r` with `rho=|r|<1`. The roots have product one,
and a unit root would make `lambda` real in `[-1,3]`. Define

```text
C = 1/(r-r^(-1)),       w_j = C*r^|j|.                    (1)
```

Then

```text
(L-lambda I)w = delta_0,
W := ||w||_1 = |C|*(1+rho)/(1-rho) < infinity.             (2)
```

These are algebraic equations, with no complex conjugation in the
pairing. Away from zero the characteristic equation proves (2); at zero
the left side is `C*(2r+1-lambda)=C*(r-r^(-1))=1`.
The solution is unique among bounded bilateral solutions. The difference
of two such solutions is homogeneous; boundedness toward each end
eliminates one of its two characteristic roots, leaving zero.

In particular (1) applies to every `lambda=exp(2*pi*i*alpha)` with
`alpha` neither an integer nor a half-integer. For any nonreal lambda,
a useful additional bound is

```text
W <= 2/|Im(lambda)|.                                     (3)
```

Indeed, write `r=rho*exp(i*phi)`. The imaginary parts of `r+r^(-1)`
and `r-r^(-1)` give
`W*|Im(lambda)| <= (1+rho)^2/(1+rho^2) <= 2`.

## 2. Exact current and finite-radius approximation

For a binary row, use the archive's local nonlinear defect

```text
D_j(x) = x_j*x_(j+1) + 2*x_(j-1)*x_j
         + 2*x_(j-1)*(1-x_j)*x_(j+1),
(Fx)_j = (Lx)_j - D_j(x),       0 <= D_j <= 3.
```

Define

```text
P_lambda(x) = sum_j w_j*x_j,
K_lambda(x) = sum_j w_j*D_j(x).
```

Both sums converge absolutely for **every binary row**, including rows
with infinite support. Their uniform bounds and exact identity are

```text
|P_lambda(x)| <= W,       |K_lambda(x)| <= 3W,
x_0 = P_lambda(Fx) - lambda*P_lambda(x) + K_lambda(x).     (4)
```

Absolute convergence justifies shifting indices in the linear term.
This is the same defect as in the
[quarter-wave current report](RESULTS-quarter-wave-current-target.md):
if `q_i=2*x_i*(x_(i+1) OR x_(i+2))+x_(i+1)*x_(i+2)`, then
`D_j=q_(j-1)` and `K_lambda=sum_i w_(i+1)*q_i`.

For an integer `R>=0`, truncate the P and K sums to `|j|<=R`. Put

```text
E_R = 2*|C|*rho^(R+1)/(1-rho).
```

Uniformly over all binary rows,

```text
|P_lambda-P_(lambda,R)| <= E_R,
|K_lambda-K_(lambda,R)| <= 3E_R.                          (5)
```

The truncated current reads only sites `-R-1,...,R+1`. The full current
is an exponentially weighted sum of local three-cell charges; it is not
a fixed finite-window observable.

## 3. Fourier coefficients reduce to the current with a bounded endpoint

Now fix a nonreal **unit** lambda, and let `x^t` be any actual Rule 30
orbit. Write `c_t=x^t_0`, `P_t=P_lambda(x^t)`, and `K_t=K_lambda(x^t)`.
For every `N>=1`, (4) telescopes exactly to

```text
sum_(t=0)^(N-1) lambda^(-t)*(c_t-K_t)
    = lambda^(1-N)*P_N - lambda*P_0.                    (6)
```

After division by N, the error is at most `2W/N`. For the singleton
initial row, `P_0=C`, so it is at most `(W+|C|)/N`.
Consequently the centre and current Fourier averages have the same
limit whenever either limit exists, and their finite averages differ
by `O_lambda(1/N)`. No existence or vanishing of those limits is proved.

For signs `chi_t=2c_t-1`, use the signed current `J_t=2K_t-1`.
The endpoint in (6) doubles. Combining it with (5), with
`J_(R,t)=2K_(lambda,R)(x^t)-1`, gives the explicit unnormalized estimate

```text
|sum_(t<N) lambda^(-t)*(chi_t-J_(R,t))|
    <= 4W + 6N*E_R
     = 4W + 12N*|C|*rho^(R+1)/(1-rho).                  (7)
```

This removes a growing endpoint at fixed frequency. It does not make
the nonlinear current independent of the centre or of the seed history,
and does not supply a cancellation estimate for that current.

## 4. The two real unit-frequency endpoints

At `lambda=1`, the characteristic roots are `i` and `-i`. There are
bounded Green functions, for example

```text
w_j = (1/2)*sin(pi*|j|/2),
```

but none decays to zero at both ends, and none is summable. Every
solution differs from this one by a combination of the global sine and
cosine modes. The existing one-sided quarter-wave weight is another
bounded, nonsummable solution. Thus the uniform all-row potential bound
used in (6) is unavailable at this frequency.

At `lambda=-1`, the repeated characteristic root is `-1`. A particular
Green function is

```text
w_j = -(1/2)*|j|*(-1)^j.
```

Every other solution adds `(-1)^j*(A+B*j)`. No choice removes linear
growth at both ends, so there is no bounded bilateral Green function.
Neither endpoint is covered by (1)--(7).

## 5. Approaching zero frequency does not recover P2 from these bounds alone

As real `alpha->0` through nonzero values, the decaying root satisfies

```text
rho = 1-pi*|alpha|+O(alpha^2),
|C| -> 1/2,
W ~ 1/(pi*|alpha|).                                     (8)
```

For positive alpha the root approaches `-i`; for negative alpha it
approaches `i`. Expanding the characteristic equation at those roots
gives (8). Hence the universal normalized endpoint estimate has order
`1/(N*|alpha|)` and tends to zero when `N*|alpha|->infinity`.

On the other hand, for the signed centre average

```text
S_N(alpha) = (1/N)*sum_(t<N) chi_t*exp(-2*pi*i*t*alpha),
|S_N(alpha)-S_N(0)| <= pi*(N-1)*|alpha|.                 (9)
```

This follows from `|exp(i*u)-1|<=|u|` and `|chi_t|=1`. The right
side tends to zero in the opposite regime, `N*|alpha|->0`.
These two sufficient uniform estimates cannot simultaneously vanish.
This is a limitation of combining (8) and (9), **not a no-go theorem
for the singleton**, improved endpoint estimates, cancellations, or a
different approach to zero frequency. The zero-frequency current estimate
in the quarter-wave route remains unresolved.

## 6. Logarithmic radius preserves a chosen sublinear Fourier scale

At a fixed nonreal unit frequency set `kappa=-log(rho)>0`. For
`0<beta<1`, (7) is `o(N^beta)` if

```text
R_N >= ((1-beta)/kappa)*log(N) + omega(1).                (10)
```

For example, taking any fixed positive extra multiple of `log(N)`
suffices. Thus a logarithmically growing spatial window approximates the
signed Fourier sum to this accuracy. It still contains an increasing
number of cells and supplies no closed dynamics for their current.

At `alpha=1/3`, numerical calibration of the analytic formula gives
`rho=0.58069183199...`, `W=1.985308713...`. A radius-30 current has
uniform signed-current tail bound below `10^(-6)` and reads radius 31.
For `N=4^k` and `beta=log(3)/log(4)`, the coefficient of k in (10) is
`log(4/3)/kappa=0.5292796...`; a coefficient such as `0.530` suffices.
These approximations are not spectral-growth or cancellation theorems.
The [third-frequency scale target](RESULTS-third-frequency-scale-target.md)
states the corresponding conditional P1 criterion. Neither this spatial
approximation nor that scale identity supplies its missing growth bound.

## 7. An optimal localization frequency, not an identified centre tone

There is an exact best exponential decay rate within this family of
unit-frequency Green functions. Write `r=a+i*b` and `t=|r|^2<1`.
The constraint `|1+r+r^(-1)|=1` simplifies to

```text
4a^2 + 2(t+1)*a + (t-1)^2 = 0.
```

Its discriminant requires `-3t^2+10t-3>=0`, hence `t>=1/3`.
Equality occurs precisely at the conjugate pair

```text
r_* = (-1-i*sqrt(2))/3,
lambda_* = (-1+2i*sqrt(2))/3,
C_* = (1+2i*sqrt(2))/6,
rho_* = 1/sqrt(3),
alpha_* = acos(-1/3)/(2*pi) = 0.3040867...,
```

and their conjugates. Thus this frequency optimizes the spatial decay
rate of the extraction kernel. No optimization of a measured centre
amplitude, or of all finite-radius prefactors, is asserted.

Moreover `alpha_*` is irrational. Otherwise `lambda_*` would be a root
of unity, so `lambda_*+lambda_*^(-1)=-2/3` would be a rational algebraic
integer, which is impossible. A nonzero limiting centre coefficient at
this frequency would therefore rule out eventual periodicity: every
eventually periodic sequence has zero Fourier average at an irrational
frequency, by a finite geometric-series calculation. Equation (6)
transfers that conditional target to the current.
**No nonzero coefficient or limiting centre tone is established here.**

A [fixed-frequency follow-up probe](../../experiments/rule30/optimal_frequency_probe.py)
tests this derived candidate on the same previously inspected first
1,048,576 cached center bits. No frequency fitting or larger scan is used.
Its signed normalized coefficient has magnitude `0.0008118453` at the
largest horizon, compared with `1/sqrt(N)=0.0009765625` as a reference
scale. A binary oscillator at the same frequency gives `0.6366197141`.
Four disjoint blocks of 262,144 bits, retaining the global phase, have
amplitudes `0.00178027, 0.00028355, 0.00270912, 0.00192988`.
These finite values identify no convincing coherent line; they prove
neither convergence nor absence of a line.

The [probe record](../../experiments/rule30/optimal-frequency-probe.json)
stores the complex coefficients at every dyadic prefix from 4,096 through
1,048,576, source and helper hashes, and the disjoint blocks. It reuses
the validated frequency helper, independently checks 8,192 cached bits
by packed evolution and 257 by scalar evolution, and checks that the
four globally phased block coefficients average to the full coefficient.
It does not independently regenerate the full cached prefix.

```sh
uv run --offline --no-project python experiments/rule30/optimal_frequency_probe.py
```

## 8. Verification and prior scope

```sh
uv run --no-project python experiments/rule30/bilateral_frequency_current_audit.py
```

The [checker](../../experiments/rule30/bilateral_frequency_current_audit.py)
uses exact rational complex arithmetic for eight decaying rational roots,
including `(1-i)/2`. Their derived lambdas need not have unit modulus:
they test the general Green/current identities, not the unit-frequency
endpoint bound. It checks the local defect, source equations, all
seven-bit finite rows, finite telescopes, and both endpoint Green formulas.
Floating-point unit-frequency calculations only calibrate (8) and (10);
the proofs above establish their scope. The optimal-frequency algebra is
also checked exactly in the quadratic field generated by `i*sqrt(2)`. The
[JSON artifact](../../experiments/rule30/bilateral-frequency-current-audit.json)
separates these checks.

A targeted repository search found the linear spectrum, one-sided
classification, and nonlinear defect identity, but no prior bilateral
summable-current formula. This records that extension and its limitations,
not an independent estimate of the nonlinear current.

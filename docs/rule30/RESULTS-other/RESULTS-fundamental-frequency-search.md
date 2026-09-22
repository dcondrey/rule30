# Fundamental frequency: exact spatial resonance and a finite temporal search

Date: 2026-09-15. **No fundamental temporal frequency identified.**
There is a proved spatial weight of wavelength four, a narrow exact classification
explaining its role, and a finite search of the actual singleton center.
None proves P1, P2, or P3.

## 1. Which frequency could matter?

Write `c_t=(F^t(delta_0))_0`, including `c_0=1`, and define

```
C_N(alpha) = (1/N) sum_(0<=t<N) (2*c_t-1) exp(-2*pi*i*alpha*t).
```

Here alpha is in cycles per update. A persistent nonzero coefficient
would identify a coherent component, not a formula generating the entire
binary sequence. The [existing oscillator exclusion](RESULTS-constant-frequency-audit.md)
rules out an exact single thresholded sinusoid from time zero at every
frequency; it does not exclude a coherent component.

Every eventually P-periodic bounded sequence has `C_N(alpha)->0` unless
`P*alpha` is an integer. To prove this, discard the finite transient and
sum the geometric progression separately in each residue class modulo P.
Consequently, a proved `limsup |C_N(alpha)|>0` at a fixed irrational alpha
would prove P1. This sufficient condition need not hold for an aperiodic
sequence. At alpha=0, convergence to zero is exactly P2.

Finite peaks do not establish these limiting statements. In particular,
an irrational frequency can be arbitrarily close to a rational periodic
line over any prescribed finite observation interval.

## 2. An exact classification of the linear spatial weights

The [quarter-wave identity](RESULTS-quarter-wave-current-target.md) already
uses the ordinary integer linear part

```
(Lx)_j = x_(j-1)+x_j+x_(j+1),
lambda(k) = 1+2*cos(k).
```

Its spatial frequency `k=pi/2` has multiplier **1**, hence zero temporal
frequency in this linear part. It does not have temporal frequency 1/4.
The actual nonlinear correction is retained throughout the identity.

The following classification makes the selection of this spatial weight
precise. Seek complex weights `w_j=0` for `j<=0` satisfying

```
(L-lambda I)w = delta_0.
```

This is an explicit algebraic equation, without complex conjugation.
It is exactly the condition that the linear contribution to
`P_w(Fx)-lambda*P_w(x)` isolate `x_0`, where
`P_w(x)=sum_(j>=1) w_j*x_j`. It forces

```
w_0=0, w_1=1,
w_(j+1)=(lambda-1)*w_j-w_(j-1),     j>=1.                 (1)
```

**The weights are bounded iff lambda is real and -1<lambda<3.**
Within this interval write `lambda=1+2*cos(theta)`, `0<theta<pi`.
The unique solution is `w_j=sin(j*theta)/sin(theta)`, which is bounded.
At the endpoints the solutions are `j` and `(-1)^(j-1)*j`.
Otherwise the two characteristic roots have product one; a unit-modulus
root would force `lambda-1=r+r^(-1)` to be real in [-2,2]. Hence outside
the interval and its endpoints one root grows in modulus. The solution
`(r_+^j-r_-^j)/(r_+-r_-)` has a nonzero growing term.

It follows that, **if |lambda|=1, the only bounded solution is lambda=1**:

```
w_j = sin(pi*j/2) = 0,1,0,-1,0,1,...
```

For completeness, let
`D_j=x_j*x_(j+1)+2*x_(j-1)*x_j+2*x_(j-1)*x_(j+1)
-2*x_(j-1)*x_j*x_(j+1)`.
The full identity for finite rows is

```
x_0 = P_w(Fx)-lambda*P_w(x)+sum_(j>=1) w_j*D_j.         (2)
```

Thus this bounded, one-sided, linear extraction cannot select a nonzero
pure temporal frequency. This is a restriction on the stated construction,
not on nonlinear factors, bilateral weights, or the center's spectrum.
The nonlinear current in (2) remains the unresolved term. The classification
is an elementary extension of the archive's quarter-wave identity, with no
claim of literature novelty.

## 3. A real peak need not be a fundamental line

The [exact seed decomposition](RESULTS-duhamel-left-edge-thue-morse.md)
has a Thue-Morse contribution and an unknown nonlinear residual. For the
standard Thue-Morse signs `a_t=(-1)^popcount(t)`, the doubling recurrence
gives the exact finite Fourier polynomial

```
sum_(t<2^m) a_t*z^t = product_(j<m) (1-z^(2^j)).
```

At `z=exp(-2*pi*i/3)`, every factor has magnitude sqrt(3), so

```
|C_(2^m)(1/3)| = (sqrt(3)/2)^m -> 0.
```

This is an exact enhanced peak with a vanishing normalized amplitude.
It is a useful intermediate control between square-root cancellation and
a persistent line. The residual in Rule 30 can change that contribution;
the identity does not transfer this scaling to the center.

## 4. Fixed candidates and held-out blocks

The [probe](../../experiments/rule30/fundamental_frequency_audit.py) fixes
eight candidates before inspecting its numerical results: 1/4, 1/3, 1/2,
and the fractional parts of pi, e, the golden ratio, sqrt(2), and the
fine-structure constant. Constants are interpreted as cycles per update,
without fitting rescalings, reciprocals, or phases. This convention is a
limited test of named candidates, not a physical or mathematical derivation.

The dimensionless fine-structure value is `0.0072973525643`, with standard
uncertainty `1.1e-12`, from [2022 CODATA at NIST](https://physics.nist.gov/cuu/pdf/all.pdf).
For a frequency perturbation delta,
`|C_N(alpha+delta)-C_N(alpha)| <= pi*(N-1)*|delta|`.
At the largest sample, a perturbation of one stated standard uncertainty
therefore changes the coefficient by at most about `3.63e-6`.

Dimensionful constants such as the speed of light do not fix cycles per
update: bare Rule 30 supplies no seconds per update or meters per cell.
An additional physical model would have to specify that mapping.

For prefixes `N=2^12,...,2^20`, the probe retains complex coefficients
without empirical demeaning. At `N=1,048,576`:

| Candidate alpha, modulo 1 | Normalized amplitude |
|---|---:|
| 1/4 | 0.00082750 |
| 1/3 | 0.00160046 |
| 1/2 | 0.00012207 |
| pi | 0.00109603 |
| e | 0.00016126 |
| golden ratio | 0.00038035 |
| sqrt(2) | 0.00164040 |
| fine-structure constant | 0.00161154 |

The reference scale `1/sqrt(N)` is 0.00097656. A seeded fair-sign control
has amplitudes of comparable magnitude. This comparison is a calibration,
not an assumption that Rule 30 is random or a statistical rejection rule.
A binary oscillator at the golden-ratio frequency gives amplitude
0.63662004, demonstrating detection of a coherent signal. The Thue-Morse
1/3 control agrees with the exact product above.

The largest nonzero N-point FFT-bin amplitude is 0.00351153, versus
0.00381594 for the random control. The five strongest separated bins
selected on the first 262,144 bits are then frozen and evaluated on three
subsequent disjoint blocks, retaining the global time phase. All five
weaken in the first held-out block. For example, the strongest discovery
frequency, `0.16405487060546875`, gives block amplitudes

```
0.00713129, 0.00052982, 0.00271065, 0.00082366.
```

These measurements identify no convincing persistent candidate. They do
not exclude weaker lines, frequencies between sampled bins, later behavior,
or a spectrum without coherent lines.

![Finite coherent amplitudes and held-out peaks](../../experiments/rule30/fundamental-frequency-audit.png)

## 5. Reproduction and limits

The [JSON artifact](../../experiments/rule30/fundamental-frequency-audit.json)
records every horizon, complex coefficient, discovery frequency, disjoint
block, cache offset, used-payload hash, script hash, and numerical controls.
The existing WDR cache supplies the first 1,048,576 bits; the probe independently
recomputes the first 8,192 by packed evolution and 257 by the scalar truth
table. It does not independently regenerate the full cache. Parseval
normalization and oscillator controls pass. A further 2,048 exact finite-row
checks retain the nonlinear term in (2) at lambda=1,-1,i,-i.

```sh
uv run --offline --no-project python experiments/rule30/fundamental_frequency_audit.py
# Optional figure, with plotting dependencies:
uv run --no-project --with numpy --with matplotlib python experiments/rule30/fundamental_frequency_audit.py --plot
```

The useful exact object remains the spatial quarter-wave current. No
constant-based temporal frequency has been derived, and no estimate on its
nonlinear current has been proved here.

## 6. Continuation: derived frequency and a different nonperiodicity target

The [bilateral-current report](RESULTS-bilateral-frequency-current.md)
removes the growing endpoint at each fixed nonreal unit frequency using
exponentially decaying two-sided spatial weights. Their fastest decay
occurs at the irrational frequency
`acos(-1/3)/(2*pi)=0.3040867...`, with decay modulus `1/sqrt(3)`.
This optimizes the extraction kernel; it does not identify an actual
center oscillation. A separate fixed-frequency probe on the same cached
prefix finds no convincing coherent line there. The nonlinear current
remains uncontrolled, and the near-zero-frequency endpoint bound cannot
be combined with the elementary continuity bound to obtain P2.

The [third-frequency scale report](RESULTS-third-frequency-scale-target.md)
proves a different sufficient P1 criterion: at a rational frequency,
unbounded but sublinear Fourier sums contradict eventual periodicity.
At frequency 1/3 the exact residual recurrence is `F_(k+1)=3F_k+D_k`
for lengths `4^k`. A nonzero limit of `F_k/3^k` would suffice, but neither
that limit nor the weaker intermediate-growth criterion is proved for
the seed. The simplest absolute perturbation margin already fails in
the first two scales; later signed control remains open.

An [actual-seed current collision](RESULTS-quarter-wave-current-collision.md)
also excludes absorbing the original quarter-wave current into an
arbitrary function of the centered radius-five transition. The same
11-cell transition occurs at times 20 and 31 with currents -1 and +1.
This leaves larger, growing, history-dependent, and later-onset
corrections open.

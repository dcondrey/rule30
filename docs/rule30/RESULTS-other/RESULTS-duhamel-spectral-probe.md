# Calibrated finite spectra of the Rule 30 residual

Date: 2026-09-10. **Finite numerical diagnostics; no spectral-type theorem or
solution of P1, P2, or P3.**

The exact decomposition is c_t=theta(t) XOR R_t for t>=1, as proved in
[the left-edge report](RESULTS-duhamel-left-edge-thue-morse.md).
This follow-up audits the proposed FFT experiment, compares it with controls,
and distinguishes spectral overlap from the cross-correlation needed for P2.

## 1. The submitted simulation is correct; the cross-spectrum title is not

The submitted NumPy update evaluates its right-hand side before assigning
the new row, so it is a synchronous Rule 30 update. Its fixed endpoints
cannot affect the observed center before the requested horizon. An independent
packed implementation matched every one of its 16,384 center samples.

The submitted code takes times 1,...,T-1 after dropping zero, giving 16,383
samples at T=16,384. Its exact center one-count on that interval is 8,276,
and its signed cross-mean is -0.010315571018738937.

The corrected probe instead uses exactly T observations at times 1,...,T.
This keeps power-of-two sample lengths and avoids the exceptional t=0.
Its residual is calculated from the exact seed trace, never sampled as noise.

The key correction concerns

```
abs(FFT(A) * conj(FFT(B))).
```

This equals sqrt(power_A*power_B); it retains spectral magnitudes and discards
relative phase. It need not be near zero when the average A_t*B_t is near
zero. The latter is obtained by summing the complex cross-spectrum with
the correct normalization. For an M-point FFT of zero-padded length-T signs,

```
sum_j FFT(A)_j*conj(FFT(B)_j)/(M*T) = sum_t A_t*B_t/T.
```

The probe checks this Parseval identity to absolute error below 1e-12 for
every sample length and every control. The plotted cross-spectrum is its
signed real part; a one-sided rFFT calculation would additionally need the
usual interior-frequency weights for summation.

## 2. Exact counterexample: complete singular-continuous overlap and zero mean

Let a_t=(-1)^theta(t) and b_t=a_(t+5). A fixed shift preserves all limiting
autocorrelations, so the two sequences have exactly the same signed
autocorrelation spectral measure. Nevertheless their average cross product
is zero.

Indeed, the Thue-Morse autocorrelation coefficients satisfy

```
eta(0)=1,
eta(2m)=eta(m),
eta(2m+1)=-(eta(m)+eta(m+1))/2.
```

These give eta(1)=eta(2)=-1/3, eta(3)=1/3, and eta(5)=0.
Existence and these recurrences are established in
[Baake and Grimm](https://arxiv.org/abs/0809.0580).

Thus the hypothetical residual R_t=theta(t+5) satisfies the P2 correlation
target despite sharing the entire singular-continuous spectral measure
with theta. In contrast b=a has the same individual spectra and cross-mean
one. Individual power spectra alone do not determine the cross-mean.

Mutual singularity remains a sufficient route, conditional on existence of
the actual residual's empirical spectral measure. It is not necessary.
Shared singular-continuous components therefore do not, by themselves,
invalidate a P2 strategy. Topological support overlap is also different from
failure of measure-theoretic mutual singularity.

## 3. The exact transfer identity is not a complex Fourier filter

Define the bivariate generating series over GF(2) by

```
X(u,z)=sum_(t,j) x_j^t u^t z^j,
N(u,z)=sum_(t,j) x_j^t*x_(j+1)^t u^t z^j,
A(z)=z^-1+1+z.
```

Then, as formal series in u with finite Laurent polynomial coefficients,

```
(1+u*A(z))*X(u,z)=1+u*N(u,z).
```

The first source layers, independently computed from the truth table, are

```
N^0=0,
N^1=z^-1+1,
N^2=z^-2,
N^3=z^-3+1+z+z^2,
N^4=z^-4.
```

N is a timewise coefficientwise adjacent product, not an ordinary square
of X. Formal GF(2) zeros cannot be interpreted directly as complex spectral
zeros. At a primitive complex cube root omega, A(omega)=0. But the actual
Rule-150 third row is

```
A(z)^3 modulo 2 = z^-3+z^-2+1+z^2+z^3,
```

whose 0/1 coefficient lift evaluates to 2 at omega. Reduction modulo two and
complex Fourier evaluation do not commute. The proposed ordinary filtering
argument therefore requires a new justification; the formal denominator
does not supply one.

Nor is there one unqualified "Sierpinski spectrum": G(t,0)=1 is a constant
temporal observable, while the positive-half parity of G is Thue-Morse.
The observable and averaging procedure must be specified before attaching
a spectral type. First source layers alone do not determine an asymptotic
temporal spectral measure.

## 4. Numerical design and calibration

The probe uses signed sequences A_t=(-1)^theta(t), B_t=(-1)^R_t at times
1,...,T, for T=2^12,...,2^17. Comparators are identical Thue-Morse, a
five-step shift of Thue-Morse, the periodic signs (-1)^t, and fair random
signs from a reproducible generator with seed 30. The random sequence is
only a control; no randomization is inserted into Rule 30.

At each T, an M=4T zero-padded full FFT gives normalized frequency masses

```
p_j=abs(FFT_j)^2/(M*T),    sum_j p_j=1.
```

These are finite discrete periodogram measures, not inferred limiting
spectral measures. Bin them into nested partitions with K=16,64,256,1024,4096,
using a common offset sqrt(2)-1. The offset avoids placing the known periodic
control atom at a partition boundary. An asymptotic bin-mass argument would
still require continuity boundaries for the actual limiting measures.

For each pair of histograms define the finite affinity

```
H_(T,K)=sum_bins sqrt(mass_A(bin)*mass_B(bin)).
```

Exact diagnostic checks, allowing floating-point error, are

```
abs(mean(A*B)) <= H_(T,K) <= 1,
H decreases when the partition is refined,
H=1 for identical inputs.
```

All pass. The decrease on refinement is automatic by Cauchy-Schwarz, so its
presence alone is not evidence for mutual singularity. Comparison with
controls and behavior as T increases at fixed K are the informative parts.
For true limiting measures, refinement of generating partitions detects
mutual singularity through vanishing affinity. Transferring that statement
to these samples would require taking the long-time limit first at fixed
partition and then refining it, with all needed existence and error bounds.

## 5. Measurements

At T=131,072:

| Compared signs | Mean cross product with Thue-Morse | H at 256 bins | H at 4096 bins |
|---|---:|---:|---:|
| Actual residual | 0.001068115 | 0.644024 | 0.485224 |
| Identical Thue-Morse | 1 | 1 | 1 |
| Thue-Morse shifted by 5 | -0.000015259 | 0.999999 | 0.999997 |
| Periodic signs | -0.000015259 | 0.003143 | 0.002260 |
| Fair random control | -0.000915527 | 0.645422 | 0.485557 |

The actual residual closely matches the random control in this finite
diagnostic. The shifted-Thue-Morse control exhibits nearly complete spectral
overlap and nearly zero cross-mean, as the exact theorem predicts.

For the actual residual, the 256-bin affinity across the six increasing
sample lengths is 0.648117, 0.642881, 0.644922, 0.641186, 0.639824, 0.644024.
This is finite-resolution stability, not convergence to a proved spectral
measure. At the largest horizon, the center has 65,466 ones among 131,072
samples. At T=16,384 it has 8,276 ones and cross-mean -0.01025390625.

No limiting autocorrelation theorem, absence of a singular-continuous
component, mutual singularity result, or density theorem is established.
Neither Mahler-measure nor Riesz-product bounds for the actual residual have
been derived from these data.

## 6. Reproduction and artifacts

```sh
uv run --with numpy --with matplotlib experiments/rule30/duhamel_spectral_probe.py --max-power 17
```

The exact packed simulation is independently checked against scalar
truth-table evolution through 128; the submitted vectorized implementation
was also checked against it through 16,383. Every numerical series passes
Parseval, normalization, and affinity checks. The plots were inspected.

Artifacts under `experiments/rule30/duhamel-spectral-probe/`:

* `spectral-report.json`: all sample lengths, controls, lag autocorrelations,
  cross-means, and affinities;
* `periodograms-16384.png`: normalized power and signed cross-periodograms;
* `spectral-affinity.png`: partition refinement and fixed-partition sample growth.

The numerical route is the most direct of the proposed experiments for
testing a mutual-singularity hypothesis. The algebraic audit is necessary
to avoid applying complex Fourier-filter arguments to a GF(2) recurrence.
Neither substitutes for the missing all-length bound on the actual seed.

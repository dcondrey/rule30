# A18 cryptanalysis arm: pre-registration

**Frozen 2026-08-30, before any data was generated.**  Nothing in this file was
edited after the first statistic ran; deviations are recorded as an explicit
`DEVIATIONS` section appended at the bottom, never by rewriting the text above.

## Object

`c = (c_t)_{t>=0}`, the lone-seed Rule 30 centre column (OEIS A051023),
`c_t = s(t,0)` with `s(0,x) = [x=0]` and
`s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))`.

**Gate.**  Every generated column is checked bit-for-bit against the repo
ground-truth generator `experiments/rule30/center_column.py` (read-only import)
over the first `2^16` bits, and against
`experiments/overnight-arms/common/rule30.py::center_column_bits` over the same
prefix.  A statistic may not run until both gates pass.

**Target depth.**  `T = 2^20 = 1,048,576` bits for tests 2, 3, 4.
Berlekamp-Massey (test 1) is `Theta(n^2)` and is registered separately at
`n <= 2^18 = 262,144`; if that does not complete in budget the arm reports the
depth actually reached under success criterion (b), it does not silently cap.

## What this arm is NOT

This is **not** the Meier-Staffelbach attack.  That attack is a state-recovery
attack: secret initial configuration, observed output, recover the key.  A
sequence can be perfectly invertible-given-enough-output and still be
statistically indistinguishable from random by every test below.  This arm tests
only the second, weaker property: **is there a distinguisher**.  Section 1 of the
report states the distinction precisely.

## Sequences under test

| id | sequence | role |
|---|---|---|
| `rule30` | lone-seed Rule 30 centre column | the object |
| `rule90` | lone-seed Rule 90 centre column (`1,0,0,0,...`) | rule-filter control; **degenerate** |
| `lfsr32` | keystream of a maximal-length degree-32 LFSR | power control for test 1 (BM) |
| `bern51` | i.i.d. Bernoulli(0.51) | power control for test 3 (monobit, cusum) |
| `lag1000` | `r_t XOR r_{t-1000}`, `r` i.i.d. Bernoulli(1/2) | power control for tests 2, 4 |
| `iid_k` | i.i.d. Bernoulli(1/2), seeds 0..19 | null band (operative threshold) |

The Rule 90 column is `1` followed by zeros forever.  It has zero variance, so
autocorrelation, approximate entropy, the serial test and the spectral test are
mathematically **undefined or degenerate** on it, and the NIST runs test fails
its own frequency prerequisite.  A test that crashes or refuses on Rule 90 has
**not** demonstrated detection power.  This is why the three non-degenerate power
controls above are registered: each one names in advance the test it must break.

**Registered power requirements (a test that fails these is reported as having
unknown power, not as a passing null):**

* `lfsr32` must show BM linear complexity plateauing at `L = 32` (test 1).
* `bern51` must be rejected at `p < 10^-3` by monobit and by cumulative sums at
  `T = 2^20` (test 3).
* `lag1000` must be rejected by the autocorrelation test at lag 1000 (test 4)
  and by the correlation-attack statistic at `Delta = 1000` (test 2).

## The four tests, with the full hypothesis ledger

Bonferroni is applied against the **global** count `N` over all four tests, not
per test.  `N` is fixed here, before data.

### Test 1 — Berlekamp-Massey linear complexity *profile*

Row 14 (`ARM4-frequency-domain.md`) already measured `L(n)/(n/2) ~= 1.0` for
`n <= 16384`.  Re-running that ceiling check is a duplicate and is **not** the
registered statistic.  The registered statistics are profile statistics, which
have known distributions for a random sequence (Rueppel) and which a maximal
ceiling does **not** determine:

1. `J(n)` = number of jumps of the profile in `[1,n]`;
2. `Hbar(n)` = mean jump height;
3. `D(n) = (1/n) * sum_{m<=n} (L(m) - m/2)`, the mean signed deviation from the
   `m/2` line (Rueppel: `E[L_m - m/2] -> 2/9` for even `m`, `-> 5/18`... i.e.
   `O(1)`, so `D` concentrates at a small positive constant).

Prefix lengths `n in {2^10, 2^12, 2^14, 2^16, 2^17, 2^18}` (6 lengths).
Hypotheses: 3 statistics x 6 lengths = **18**.

Null: 20 i.i.d. Bernoulli(1/2) seeds, same pipeline, to `n = 2^17`; the seed
`[min,max]` band is the operative threshold, and a z-score against the seed
mean/s.d. is reported alongside.

### Test 2 — correlation-attack statistic (output-only)

For window length `k` and lag `Delta`, let `w = (c_t, ..., c_{t+k-1})` and target
`y = c_{t+Delta}`.  The maximum over **all** Boolean functions
`g: {0,1}^k -> {0,1}` of the correlation `Pr[g(w) = y] - 1/2` is attained by the
maximum-likelihood `g` and equals

```
eps(k, Delta) = (1/2) * sum_{w in {0,1}^k} | Pr[w, y=1] - Pr[w, y=0] |
```

computed in one pass.  This is the standard correlation-attack quantity for a
nonlinear combiner, evaluated **along the actual orbit**, which distinguishes it
from row 43 (ANF/Walsh spectrum of the function `f_t` over all inputs).

**Framing-artifact guard, registered in advance.**  `c_{t+Delta}` is *determined*
by the row-`t` cells in `[-Delta, Delta]`, and the output window
`c_t..c_{t+k-1}` overlaps the target whenever `Delta < k`.  Only
`Delta >= k` is admissible.  Any `Delta < k` would return `eps = 1/2` by
construction and would be measuring the dynamics, not a bias.

`k in {1,2,3,4,6,8}`; for each `k`, `Delta in ({k,...,128} union
{256,512,1024,2048,4096})`.  Ledger size
`sum_k (129-k+5)` = `134-1 + 134-2 + 134-3 + 134-4 + 134-6 + 134-8` = **780**.

Null: because `eps` is a maximum over `2^k` terms its null distribution is not
`sqrt`-normal and is **not** derived analytically.  It is calibrated by Monte
Carlo on the 20 i.i.d. seeds at the same `T`, per `(k, Delta)` scale, and a
p-value is obtained from the Monte Carlo mean and s.d. of `eps` under the null
(normal approximation on the standardized statistic, with the empirical seed max
also reported as the operative threshold, as in row 8).

### Test 3 — NIST SP 800-22 subtests, block protocol

One p-value on one long string is not what the suite is for.  Registered
protocol: partition `c[0:10^6]` into `K = 100` disjoint blocks of `10^4` bits;
run each subtest on each block; then report

* the **pass proportion** at `alpha = 0.01` against NIST's confidence interval
  `1 - alpha +/- 3 sqrt(alpha(1-alpha)/K)` = `[0.9602, 1.0198]` (upper clipped
  to 1), and
* the **uniformity of the 100 p-values**, by chi-square on 10 equal bins
  (NIST's own meta-test, threshold `P_T >= 0.0001`) and by a
  Kolmogorov-Smirnov test against `U(0,1)`.

Subtests implemented: monobit frequency, frequency-within-block, runs,
longest-run-of-ones, cumulative sums (forward), cumulative sums (reverse),
approximate entropy (`m=3`), serial (`m=3`, both `p1` and `p2`), discrete
Fourier transform / spectral.  That is **10** p-value streams.  The DFT test
uses the corrected variance constant (`sqrt(T * 0.95 * 0.05 / 4)`), not the
constant in the original 2001 document, which is known to be wrong.

Hypotheses: 10 streams x (1 pass-proportion + 1 chi-square + 1 KS) = 30, plus
10 whole-sequence p-values at `T = 2^20` = **40**.

### Test 4 — autocorrelation at every lag

`A(l) = (1/(T-l)) * sum_t (-1)^(c_t XOR c_{t+l})`, i.e. the balance of the
XOR-shifted sequence, for `l = 1 .. 100,000`.  Under i.i.d. Bernoulli(1/2),
`A(l)` is asymptotically `N(0, 1/(T-l))`, so `z(l) = A(l) * sqrt(T-l)`.
Computed by FFT.  Hypotheses: **100,000**.

Reported: `max_l |z(l)|`, the lag attaining it, the count of `|z| > 5.03`
(the Bonferroni threshold, below), the fraction with `|z| > 1.96` and `> 2.58`
against the expected `0.05` / `0.0099`, and a KS test of the `z` values against
`N(0,1)`.

## Global multiple-comparison correction

```
N = 18 (test 1) + 780 (test 2) + 40 (test 3) + 100,000 (test 4) = 100,838
```

* **Bonferroni**, family-wise `alpha = 0.05`: per-hypothesis threshold
  `alpha/N = 4.959e-7`, i.e. `|z| >= 5.032` for a two-sided normal statistic.
  This is the **headline** threshold.
* **Benjamini-Hochberg FDR at `q = 0.05`** is reported alongside, because
  Bonferroni over 10^5 lags is very conservative.
* Raw uncorrected p-values are reported in full for every hypothesis so the
  correction can be redone by a reader.

## Decision rule

* **NO BIAS FOUND** — no hypothesis survives Bonferroni at `alpha = 0.05`, BH-FDR
  at `q = 0.05` rejects nothing, and all three non-degenerate power controls fire
  as registered above.
* **BIAS FOUND: <what>** — at least one hypothesis survives Bonferroni **and**
  survives the artifact audit: re-derivation at a different `T`, an off-by-one
  re-framing check, and confirmation that the same statistic on the 20 i.i.d.
  null seeds does not produce a comparable extreme.
* **INCONCLUSIVE** — anything else, including a power control that fails to fire,
  or a registered test that could not be run to its registered depth.

## Scope limits stated in advance

**Obstruction H.**  Every result here is a statement about a finite prefix.  A
finite prefix, however deep, bounds a test's power at that depth and can never
establish randomness, absence of structure, or nonperiodicity as an infinite
statement.  This sentence is repeated next to every headline number in the
report, by design.

**Single-column gate (PATH.md 0.1).**  Section 0.1 retires quantities that move
by `O(1/W)` when column 0 is overwritten by a periodic word.  Every statistic in
this arm is a functional of column 0 *alone*: overwriting column 0 replaces the
input entirely, so each statistic moves by 100%, not `O(1/W)`.  This arm passes
the gate trivially because it **is** the column, not a functional insensitive to
it.  Demonstrated numerically once in `single_column_gate.py` rather than merely
asserted.

**What a null result does and does not buy.**  A clean null says: four
independent standard cryptanalytic techniques, at this depth, with these
thresholds, found no distinguisher.  It does not say the column is random, does
not bear on P1 or P2, and is consistent with row 8's block-frequency finding
rather than independent of it.

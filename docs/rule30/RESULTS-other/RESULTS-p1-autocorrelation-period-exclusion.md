# No autocorrelation distinguisher at any lag of the 2^23 trace, and a period band that is already excluded

Status: **a distinguisher-absence measurement at a new width and depth. Its
period-exclusion corollary is true and STRICTLY DOMINATED by an existing
record; it is stated here only so the next reader does not rediscover it and
believe it is new, which has now happened twice.**

## 1. The measurement, which is what is new

Every lag `1 <= l <= 2^22` on the stored `2^23`-bit trace
`experiments/rule30-subword-extended/rule30_center_8388608.bin`, bit order
validated against a centre column recomputed in the script (little-endian).
`z(l) = A(l) sqrt(T-l)` with `A(l)` the balance of `c_t XOR c_(t+l)`, by FFT
zero-padded to `2^24 >= 2T` so the circular correlation is exactly linear.

```text
max z   = 5.5216 at lag 1,656,153
min z   = -5.2703 at lag 661,856
lags with z >= 5.701 : 0 of 4,194,304
```

A registered gate requires the FFT to reproduce a direct mismatch count at 24
spread lags; observed maximum discrepancy `1.221e-15` in `z`.

**The number that makes this a null rather than a finding.** Two-sided
Bonferroni over `N = 4,194,304` gives `thr = 5.701`; the one-sided expected
maximum for that many i.i.d. normals is `sqrt(2 ln L) = 5.5225`. The observed
maximum is `5.5216`, **within 0.0009 of the value the sample size predicts.**
Twenty i.i.d. Bernoulli(1/2) seeds at the same `T` and lag range give empirical
`max z = 5.7157` and `max |z| = 6.0485`, both above Rule 30's maximum. The
column is less extreme than a typical random sweep of the same width.

This extends the prior sweep, which ran 100,000 lags at `T = 2^21`, by a factor
of 42 in lags and 4 in length. That extension is the contribution.

## 2. The period corollary, and why it buys nothing

If the column is eventually periodic with period `p` and preperiod `q` then
`c_t = c_(t+p)` for `t >= q`, so over `0 <= t < T-p` at most `q` positions
disagree and `z(p) >= (T-p-2q)/sqrt(T-p)`. Contrapositively `z(p) < thr`
forces `q > (T - p - thr sqrt(T-p))/2`. With no lag reaching `thr`:

| period `p` at most | preperiod `q` excluded at or below | `p + q` |
|---|---|---|
| 100,000 | 4,136,097 | 4.236e6 |
| 1,048,576 | 3,662,293 | 4.711e6 |
| 2,097,152 | 3,138,578 | 5.236e6 |
| 4,194,304 | 2,091,314 | 6.286e6 |

**Every pair in that table is already excluded.** Record
`70faaffe0b04ef36` forces `r + q >= N - L` from subword complexity, where `L`
is the longest repeated factor, **with no cap on the period at all**, and at
this same `N = 8,388,608` it gives `r + q >= 8,388,565`. Verified directly on
this trace: at window length 44 all `8,388,565` windows are distinct (at 43,
two coincide), so `L = 43`.

The boundary sum here is `p + q(p) = (T+p)/2 - thr sqrt(T-p)/2`, increasing in
`p`, with range `[4,186,048, 6,285,618]`. Since `6,285,618 < 8,388,565`, the
band is **strictly dominated with 2,102,947 of margin and no surviving
region.**

**This correction is inherited and is recorded as such.** The predecessor
record `r30-a18-autocorrelation-excludes-period-band` claims its band runs
"roughly 5.5x further" than the catalogued exclusion. That comparison was made
against `7e73f8c439ee894e`, the 200,000-bit erratum, while the 8,388,608-bit
application of the identical method sat in the same database. The claim is
false there and was repeated here before this section was written. Anyone
extending the autocorrelation sweep for period exclusion should stop: the
subword route already dominates it at every depth where both have been run,
and it dominates by construction, since `p(n) <= r+q` uses every window while
the autocorrelation uses one lag at a time.

## 3. Controls, and three disclosed registration defects

```text
period_1048573   z = 2709.2499   (= sqrt(T-P) exactly; D = 0 by construction)
rule90_lag1      z = 2896.3085   (saturation sqrt(T-1) = 2896.3092)
sturmian         max z = 1022.07 at lag 1597, a Fibonacci number
```

**Defect 1: the Rule 90 bar was unreachable, and the repair was the wrong
one.** The registration says Rule 90 "MUST fire at lag 1 with `z(1) > 1000`"
and specifies **no length**. `z(1) = (T-3)/sqrt(T-1)` saturates near
`sqrt(n)`, so at the `n = 2^18` the first run used, the ceiling is `512` and
the bar could not be met at any signal strength; that run reported INCONCLUSIVE
and the exclusion was withheld, as the registration requires. The repair raised
`n` until the fixed bar cleared. **That is the wrong direction:** the diagnosis
was a bad threshold and the fix should have been to the threshold, not to `n`,
and there is no "registered depth" for controls to appeal to. Raising a length
until a saturating statistic clears an arbitrary bar is the same defect class
as the `lag1000` control this registration names as the error it was avoiding.

**Defect 2: the control has no diagnostic power at any length.** Rule 90's
column is built as a hand-constructed delta array and `z(1)` is then pure
arithmetic; nothing in the analysis path can make it fail. The same is true of
`period_1048573`, whose `D = 0` exactly. Both "controls" are constants
independent of the Rule 30 data, so the registered kill clause is dead code.
Neither is run anywhere near the `z ~ 5.7` decision boundary; they sit at 475x
and 508x it.

**Defect 3: the Sturmian word was cast as a NEGATIVE control** required not to
exceed `thr` at any lag. It exceeds it at **260,436 of 524,288 lags**, correctly,
because a Sturmian word is highly structured. It is a positive control for
structure detection. The genuine negative control is the twenty i.i.d. seeds.

The first, INCONCLUSIVE run left no artifact: the JSON is overwritten in place
and neither file was tracked at the time, so that run is not recoverable from
the repository and this narrative is the only account of it.

## 4. What none of this can do

The measurement is a finite-prefix statistic and cannot imply aperiodicity in
either direction. It does not touch P2. The period corollary is dominated and
should not be cited. What remains citable is the null itself: no autocorrelation
distinguisher at any of 4.19M lags at `T = 2^23`, at a maximum indistinguishable
from the sample-size expectation.

```sh
uv run python experiments/rule30/p1_full_lag_period_exclusion.py
```

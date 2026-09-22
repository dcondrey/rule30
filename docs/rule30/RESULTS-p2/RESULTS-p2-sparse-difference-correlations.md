# P2: a sparse sufficient family of ordinary temporal correlations

Status: **a standard correlation argument specialized to dyadic differences,
with an exact control; no Rule 30 cancellation estimate is proved.**

The [existing same-orbit theorem](RESULTS-p2-p3-cross-review-2026-09-03.md#24-quantitative-same-orbit-defects-imply-p2)
proves P2 when every fixed ordinary time-shift correlation tends to zero.
Its finite inequality uses consecutive translations. Using dyadic translations
instead gives a sufficient condition on a zero-density set of lags, and a
one-sided bound suffices. This is a specialization of the same elementary
Cauchy--Schwarz / van der Corput argument, not a new general analytic method.

## 1. Exact finite inequality

For any signs z_0,...,z_(N-1), N>=1, write

\[
S_N=\sum_{t=0}^{N-1}z_t,\qquad
C_N(h)=\sum_{t=0}^{N-1-h}z_tz_{t+h}\quad(h\ge1),
\]

where the sum is zero when h>=N. For m>=1 put

\[
a_j=2^j-1\ (0\le j<m),\qquad H_m=2^{m-1}-1.
\]

Then the exact inequality is

\[
\boxed{m^2 S_N^2\le (N+H_m)
 \left[mN+2\sum_{0\le i<j<m}C_N(2^j-2^i)\right].}
\tag{1}
\]

**Proof.** Extend z by zero to all integer indices and set
Y_t=sum_(j<m) z_(t+a_j). Its support is contained in [-H_m,N-1], an
interval of N+H_m integer positions, and sum_t Y_t=m S_N. Expanding squares,

\[
\sum_tY_t^2=mN+2\sum_{i<j}C_N(a_j-a_i).
\]

Cauchy--Schwarz proves (1). In particular the bracket is nonnegative even
when individual correlations are negative. There is no independence assumption,
and (1) holds when N<=H_m as well.

## 2. Sufficient seed theorem and order of limits

Let c_t be the singleton Rule 30 center and z_t=1-2c_t. Define

\[
D=\{2^a-2^b:a>b\ge0\}.
\]

The following **unproved seed-specific hypothesis** suffices for P2:

\[
\boxed{\forall h\in D,\qquad
\limsup_{N\to\infty}\frac{C_N(h)}N\le0.}
\tag{2}
\]

Indeed, divide (1) by m^2 N^2 and hold m fixed. The finitely many cross
terms have nonpositive limsup by (2), while H_m/N tends to zero. Thus

\[
\limsup_{N\to\infty}(S_N/N)^2\le 1/m.
\]

Only after this limit is taken do we let m tend to infinity. This proves
S_N/N -> 0, hence center density 1/2. No uniform rate in h or m is required.
Letting m grow with N without additional bounds would not be justified.

For the defect count

\[
D_N(h)=\#\{0\le t<N-h:c_t\ne c_{t+h}\},
\qquad C_N(h)=(N-h)-2D_N(h)\quad(N>h),
\]

(2) is exactly liminf_(N->infinity) D_N(h)/(N-h)>=1/2 for each h in D.
Neither existence of a defect-density limit nor equality to 1/2 is necessary.
These are ordinary time shifts, not XOR shifts of binary time indices.

There is a weaker aggregate alternative: it is enough that, for an unbounded
set of positive integers m,

\[
\limsup_{N\to\infty}\frac1N
  \sum_{0\le i<j<m}C_N(2^j-2^i)\le0.
\tag{3}
\]

Equation (1) then gives the same 1/m bound along that unbounded set. This
retains cancellation between positive and negative correlations. Neither
(2) nor (3) is established for Rule 30.

## 3. How sparse the lag set is, and an additional implication

The integers in D have one contiguous run of ones in binary:
h=2^b(2^(a-b)-1). If 1<=h<=X, then 2^(a-1)<=X. With
L=floor(log_2 X)+1 this gives

\[
|D\cap[1,X]|\le\sum_{a=1}^{L}a=L(L+1)/2.
\]

Thus only O((log X)^2) lags up to X are requested, compared with every
positive lag in the earlier sufficient theorem. This weakens the hypothesis;
it does not prove that the remaining estimates are easier on the seed.

Hypothesis (2) also excludes every eventual period, so it would prove P1 as
well as P2. For any period p, two powers of two have the same residue modulo
p by the pigeonhole principle. Their positive difference h lies in D and
is divisible by p. An eventually p-periodic trace has C_N(h)/N -> 1, contrary
to (2). This is a conditional implication, not a new period exclusion for
the actual seed. Neither (2) nor (3) is claimed necessary for P2.

## 4. Powers-of-two lags alone are insufficient

The artificial periodic bit word

```text
(110100010000)^infinity
```

has density 1/3. Let A={0,1,3,7} be its one positions modulo 12. For
h=1,2,4,8, exactly one element t of A satisfies t+h in A. Its signed
cyclic correlation numerator is therefore

\[
\sum_{t=0}^{11}z_tz_{t+h}
 =12-4|A|+4|\{t\in A:t+h\in A\}|=0.
\]

All higher powers of two alternate between 4 and 8 modulo 12, because
2*4=8 and 2*8=4 modulo 12. Hence C_N(2^j)/N -> 0 for every j>=0, despite
the biased bit density. The correlations at the omitted dyadic differences
do not all vanish: h=6=8-2 gives numerator 4, and h=12=16-4 gives 12.

This is an exact counterexample to a generic powers-of-two-only implication.
It is not asserted to be a Rule 30 center trace. The distinction matters
when borrowing the dyadic structure in the
[time-index Walsh route](RESULTS-p2-time-index-walsh.md#4-exact-derivative-bridge):
its XOR correlations and the ordinary correlations used here are different
statistics. The counterexample does not refute that report's Walsh theorem.

For the actual Rule 90 singleton control, c_0=1 and c_t=0 for t>=1. Thus,
for each fixed h>=1 and N>h, C_N(h)=N-h-2 and C_N(h)/N -> 1. The new
hypotheses fail, as required. Their universal analytic implication does not
mistakenly establish Rule 90 balance.

## 5. Verification and next obligation

The independent, standard-library-only
[verifier](../../experiments/rule30/p2_sparse_difference_correlations_audit.py)
enumerates every nonempty sign word through length ten, for m=1,...,5.
It independently sums the translated-word square, checks its identity with
the correlation bracket, and checks (1) in integer arithmetic. It also
checks the twelve-bit control, the modular residue cycle, and the stated
finite Rule 90 formula. The [JSON record](../../experiments/rule30/p2-sparse-difference-correlations-audit.json)
contains counts and explicit control values.

```sh
uv run --no-project python experiments/rule30/p2_sparse_difference_correlations_audit.py \
  --output experiments/rule30/p2-sparse-difference-correlations-audit.json
```

The finite checks calibrate the formulas; the proofs above establish the
all-length implications. No Rule 30 data horizon is extended. The missing
step remains an origin-specific argument establishing (2), (3), or another
sufficient cancellation bound. A promising representation would compare
dyadic-time snapshots while retaining the exact singleton ancestry; the
analytic reformulation itself supplies no such dynamical mechanism.

## 6. A seed estimate at the dyadic lags, and what it cannot decide

Section 5 closes on a missing step: an origin-specific argument for (2) or
(3). This section reports a measurement of both on the actual trace. It is
not the first such measurement, it confirms nothing, and the two facts are
connected.

**Prior work, and a correction to this section's own registration.** The
pre-registration for this run asserted that the statistic had never been
evaluated on the actual trace. **That assertion is false.** The arm at
`experiments/overnight-arms/frontier_attack/a18_cryptanalysis/` computes the
same statistic on the same trace: its `test4_autocorrelation.py` returns
`z(l) = A(l) sqrt(T-l)` with `A(l) = 1 - 2 D_T(l)/(T-l)`, so its `z` is the
exact negative of the one used here. Verified rather than inferred: the two
agree to the last bit at every lag checked, and its `seq/rule30.npy` is
byte-identical to the little-endian decode of this trace's first `2^20` bits.
That arm swept **every** lag from 1 to 100,000, not a sparse set, at
`T = 2^20` and again at `T = 2^21`, with Bonferroni control over an explicit
100,838 tests and a twenty-seed empirical null band on `max|z|`. Its
calibration is stronger than this run's. The registration's novelty claim was
not checked against the repository before it was written.

**A catalog gap, which is the mechanism.** No record in the catalog cites that
arm. A tracked cryptanalytic sweep with real calibration machinery is
invisible to the record graph, which is why this document's own status field
could say that no Rule 30 seed estimate existed while one sat on disk. The
defect is in the index, not in either computation.

**What is actually new here**, once the above is subtracted: the 115 dyadic
lags above 100,000, which the prior sweep's cap excludes; all lags at
`N = 2^22` and `N = 2^23`, beyond that sweep's `2^21`; and the evaluation of
the aggregate alternative (3), which the prior arm never formed, since it
reports per-lag statistics only.

**The measurement.** `D_N(h)/(N-h)` at every lag of `D` inside `[1, 2^22]`
over prefixes `N = 2^20, 2^21, 2^22, 2^23`, on
`experiments/rule30-subword-extended/rule30_center_8388608.bin`. Every ratio
at `N = 2^23` lies in `[0.499544, 0.500591]`. The stored trace's bit order
was validated against a centre column recomputed here over its first 4096
bits, and it is **little**-endian; assuming the other convention would have
measured a different sequence in silence.

**The lag set has 254 elements, not 253.** An exclusive range bound dropped
`h = 2^22 = 2^23 - 2^22`, the largest lag in range. Its ratio is `0.499790`,
inside the band above, so the headline is unchanged, but the count was wrong
as first written. Section 3 supplies no exact count and must not be cited for
one: it proves only `|D cap [1,X]| <= L(L+1)/2`, which at `X = 2^22` is 276.

**Why the band is not evidence for (2).** `D_N(h)` is `Binomial(N-h, 1/2)`
under a fair-coin null. The overlap between the pairs `(t, t+h)` neither
inflates nor deflates this: partition `[0,N)` into residue classes modulo
`h`, and within a class the mismatch indicators are an independent uniform
family, giving variance exactly `(N-h)/4`. So the ratio has standard
deviation exactly `1/(2 sqrt(N-h))`, which is `2.44e-4` at the largest lag,
and the observed band spans `-2.56` to `+2.72` in those units. That is this
measurement's resolution floor. A true `liminf` at `1/2 - 10^-5` produces the
same table, and no finite `N` constrains a `liminf` at all.

**The pre-registered kill was uncalibrated, and is recorded as a design error
rather than rescoped.** It named a direction and no magnitude, so it fires on
the sign of a mean-zero statistic. It fired at 29 lags. The denominator is
232, not 254: the kill compares the two largest prefixes at which a lag is
reported, and lags above `2^21` appear at `N = 2^23` only. Summing the null
firing probability over those 232 gives an expectation of 28.0 against 29
observed. Per-lag `z` lies in `[-2.56, 2.72]` against the `sqrt(2 ln 508) =
3.53` that 254 two-sided null samples are expected to reach, and 127 of 254
ratios are below `1/2` against 127 expected. Nothing fired above chance.

**Three controls, and the third exists because the first two could not catch
the defect above.** The twelve-bit periodic word of section 4 gives
`D(6) = 1/3` exactly. Rule 90's centre column gives maximum ratio `1/131072`.
But Rule 90's column is 1 at `t=0` and 0 after, so `D_n(h) = 1` at **every**
lag: across 154 lags it takes exactly one distinct value, and its answer
therefore cannot depend on which lags are tested. A control blind to the lag
set cannot detect a wrong lag set, which is how `h = 2^22` went missing. The
repair is a third control with the opposite property, the Fibonacci
(Sturmian) word: aperiodic, uniquely ergodic, with exact frequencies to
infinity, its density of ones being `1/phi^2 = 0.381966` and
`D(1)/(N-1) = 2/phi^2 = 0.763932` exactly, since the word contains no `11`
factor. Its ratios run from `0.004133` to `0.763932` across 191 lags, a
spread of 0.76, collapsing at Fibonacci-number lags (`h = 8` gives `0.111`)
where its self-similarity aligns. It fails the hypothesis at 95 of 191 lags.
It is also the only control here that is aperiodic while having uniform
averages, which is the regime P2 itself occupies.

A registered control was not met and is disclosed here rather than amended in
the registration. Section 4 control 1 required reproducing `{6: 1/3, 12: 1}`;
this run reports `{6: 1/3, 12: 0}`. The two are consistent, not contradictory:
the prior audit records C-densities and this run reports D-ratios, linked by
`C = (N-h) - 2D`. The agreement at `h = 6` is a coincidence, because `1/3` is
the fixed point of `x -> 1 - 2x`, so that entry was never the cross-check the
registration intended and the `h = 12` entry is what exposes it.

**Aggregate alternative (3) is the more sensitive test against a common-mode
bias and the less sensitive one against a single lag.** Evaluated from the
same `D_N(h)` through `C_N(h) = (N-h) - 2 D_N(h)`, for every `m` from 2 to 24,
the partial sums reach `+4.3e-3` at `m = 14` and fall to `+4.8e-4` at
`m = 24`, every `z` within `[-0.44, +1.40]` of a null standard deviation
`sqrt(sum_pairs (N-h))/N`. That null is exact and not an independence
approximation: for `h != h'` the cross-covariance
`E[z_t z_(t+h) z_s z_(s+h')]` vanishes identically, since pairing requires
either `h = h'` or `h + h' = 0`.

The aggregate's lag set is not the per-lag table's. A lag enters the per-lag
test only at `h <= N/2`, so that two prefixes report it, but (3) needs only
`h < N`, section 1 making `C_N(h)` identically zero beyond that. Reusing the
table's filtered set dropped 22 of the 276 pairs at `m = 24`, and those 22
carried 55 percent of the sum; the corrected row is the one quoted above.
Past `m = 24` the pair set does not grow at this `N`, every further pair
having `h >= N`, so the statistic is frozen and further rows would suggest a
growth that is not there.

The power comparison runs in both directions and the directions are opposite.
Against a bias `D_N(h)/(N-h) = 1/2 - eps` present at **every** lag at once,
the aggregate accumulates signal linearly and noise in quadrature, so its `z`
is `2 eps sqrt(sum_pairs (N-h))` against a single lag's
`2 eps sqrt(N-h)`. The ratio is `sqrt(sum_pairs (N-h)/(N-h0))` and therefore
depends on which lag `h0` it is referenced against; it is **not** `sqrt(k)`,
which would require every `N-h` to be equal, and they are not. Against the
best-sampled lag the factor is `15.30`: the aggregate resolves `eps` to
`3.39e-5` where that lag needs `5.18e-4`. Against a bias confined to **one**
lag the same pooling is a loss of exactly the same factor, that lag's signal
being diluted by the others' noise.

Hypothesis (2) fails as soon as a single `h` fails, so the per-lag test is
the correct instrument for (2) and this aggregate for (3); the converse does
not hold, since one lag with `C_N(h)/N -> delta > 0` does not refute (3),
other lags being free to cancel it. A clean aggregate therefore does not
certify (2) **uniformly over alternatives** - though against the common-mode
class specifically it is the sharper of the two tests, and that qualification
is the whole content of this paragraph. A sign-agnostic triangle bound
`k max|C_N|/N` is available but is the wrong tool for a one-sided statement,
discarding the signs (3) is about; at fixed `m` it tends to zero in any case,
`k` being constant in `N`. Neither statistic constrains a `limsup` at finite
`N`.

`p2_sparse_difference_correlations_audit.py` is not edited and its artifact's
recorded `source_sha256` does not move; the estimate is a thin companion,
[p2_dyadic_lag_seed_estimate.py](../../experiments/rule30/p2_dyadic_lag_seed_estimate.py),
writing
[p2-dyadic-lag-seed-estimate.json](../../experiments/rule30/p2-dyadic-lag-seed-estimate.json).
Every threshold in that artifact carries the sampling floor it is read
against. The missing step of section 5 is unchanged.

```sh
uv run python experiments/rule30/p2_dyadic_lag_seed_estimate.py
```

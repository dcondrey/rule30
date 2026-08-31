# `eps_30(m)` extended to m=27, and what symbolic regression makes of it

Arm `a25_eps30_extended`, 2026-08-31.
Code and raw output: `experiments/overnight-arms/frontier_attack/a25_eps30_extended/`
(`eps_dp.py`, `analyse.py`, `sr.py`, `eps30_values.json`, `analyse_output.txt`,
`sr_output.txt`).

## 0. Scope, stated before anything else

**This is a side question. It is not a route to P1 and cannot become one.**

`PATH.md` section 9.4 flags this twice, and the flag is repeated here because
this document computes the quantity much further than before and could
otherwise be misread. Whether `eps_30(m) -> 0` as `m -> infinity` is **not** a
route to P1 even if it were answered, because Lemma Z needs *exactness* -- a
bounded window that determines `r_t` with probability 1 -- and Theorem W
already establishes `eps_30(m) > 0` at every finite `m`. A limit of zero would
say bounded windows get arbitrarily close; it would still not say any of them
arrives. Accordingly:

* nothing below changes any row's status;
* nothing below bears on P1, P2 or P3;
* the value of this arm is a clean characterisation of a quantity the project
  had already computed to `m=16`, plus an honest account of what a fitted
  functional form can and cannot settle about its limit.

## 1. Headline

1. **Reproduction: clean.** An independent third implementation reproduces all
   sixteen published numerators `m=1..16` exactly.
2. **Extension: `m=27`,** from `m=16`. That is 11 further exact values, and
   `m=27` is a principled stopping point rather than a patience limit
   (section 3).
3. **A new algorithm** brings the cost from `Theta(2^(2m+1))` to
   `Theta(m * 2^(m+2))`. Measured on the same values: a21's method needs 582 s
   for `m=17` and 2375 s for `m=18`, against 0.24 s and 0.46 s here -- 2400x
   and 5200x, with the gap doubling each `m`.
4. **The numerator sequence is not in OEIS** (searched whole, by prefix, and by
   interior window; also `"Rule 30" + Bayes/entropy` and the decimal `0.17330`).
   No prior closed form or asymptotic to meet first.
5. **Symbolic regression found a survivor, and it does not settle anything.**
   `eps(m) ~ 0.142455 + 0.123447 / sqrt(m)` passes held-out validation
   comfortably. But so does `b / (log m)^p`, whose limit is **zero**. A test
   that both sides pass does not discriminate. **The limit of `eps_30(m)` is
   undetermined by 27 exact points, and this arm's contribution is to have
   measured *why* rather than to have guessed.**

## 2. Reproduction of `m = 1..16`

`eps(m)` is defined exactly as in a21 `eps_theorem.py::eps` and a22
`independent_eps_check.py::eps_independent`. With `g = (g_0..g_{m-1})` the
observed centre-column window and `h = (h_0..h_m)` the hidden block
`s(t-m, 1..m+1)`, both uniform and independent for `t >= 2m+1` by Theorem U,

```
eps(m) = sum_g min( N(g), 2^(m+1) - N(g) ) / 2^(2m+1),
N(g)   = #{ h : F_g(h) = 1 },   F_g = m forward steps of the quarter plane x>=1
                                      driven by the boundary column g.
```

Checks run, all passing:

| check | range | result |
|---|---|---|
| DP vs a fresh brute-force enumeration written here, rules 30 and 90 | `m=1..9` | exact match |
| DP vs the published a21/a22 numerators | `m=1..16` | **exact match, all 16** |
| a22's numpy array method re-run (third code path) | `m=1..12` | exact match |
| a21's bitmask method re-run at values *past* the published range | `m=17, 18` | **exact match**, `5926792980/2^35` and `23568587796/2^37` |
| rule-90 oracle `eps_90(m) = 1/2` exactly | `m=1..27` | numerator exactly `2^(2m)` at every `m` |

The `m=17, 18` line is the one that carries weight for the extension: it
validates *new* values through a structurally different code path, which the
rule-90 oracle cannot do. The rule-90 oracle covers the rest: it is run at every `m`
alongside rule 30 and is sensitive to exactly the masking and edge-handling
errors that would otherwise produce a plausible-looking wrong number at a `m`
where no reference value exists.

Arithmetic is exact throughout: integer counts, never `np.bincount(weights=)`
(which silently returns float64), and `eps(m)` is carried as an exact
`(numerator, 2^(2m+1))` pair.

## 3. The algorithm, and the cost curve

a21 and a22 both loop over all `2^m` windows and, for each, evaluate over all
`2^(m+1)` hidden states: `Theta(m^2 * 2^(2m+1))`. But the window is consumed
one time step at a time, and after `j` steps the surviving row has only
`m+1-j` cells. So walk the trie of window *prefixes* breadth-first, carrying a
count vector at each node. At depth `j` there are `2^j` nodes each holding
`2^(m+1-j)` counts: exactly `2^(m+1)` integers per level, **independent of
`j`**. Work is `m * 2^(m+2)`, and memory is flat. Rows are packed as integers,
so one step is a three-instruction bit expression:

```
R' = (((R << 1) | b) ^ (R | (R >> 1))) & ((1 << (L-1)) - 1)      # rule 30
```

Measured cost (rule 30, one core, `int64` to `m=22`, `int32` above):

| m | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| secs | 0.09 | 0.24 | 0.46 | 1.30 | 2.26 | 5.08 | 12.3 | 34.9 | 59.0 | 127 | 456 | 910 |
| ratio | | 2.8 | 1.9 | 2.9 | 1.7 | 2.3 | 2.4 | 2.8 | 1.7 | 2.2 | 3.6 | 2.0 |

The ratio sits near the predicted `2(m+1)/m ~ 2.1` through `m=25`; the excursion
at `m=26` is memory pressure, not arithmetic (the live array reaches
`2^27` int32 = 537 MB and the working set exceeds 3 GB). Extrapolating, `m=28`
is roughly 30-60 min per rule and **memory-bound** rather than arithmetic-bound
(`2^29` int32 = 2 GB live, plus buffers); `m=30` would need a depth-first pass
over subtrees to cap the live array. Reachable, but see below for why it is not
worth doing.

**Why `m=27` is the stopping point and not `m=28`.** At `m=27` the numerator is
`748914543008093 < 2^53`, so `eps(27)` converts to float64 with **zero** error.
At `m=28` the numerator needs 55 significant bits and the conversion starts
rounding. Every value fed to the regression below is therefore exact, with no
rounding that could be fitted as if it were signal. Anyone extending past
`m=27` must move the fitting input off float64, and should say so.

## 4. The exact values

`eps_30(m) = a(m) / 2^(2m+1)`. New values in bold.

| m | eps(m) | exact fraction |
|---|---|---|
| 1 | 0.250000000000000 | 1/4 |
| 2 | 0.250000000000000 | 1/4 |
| 3 | 0.218750000000000 | 7/32 |
| 4 | 0.218750000000000 | 7/32 |
| 5 | 0.203125000000000 | 13/64 |
| 6 | 0.200683593750000 | 411/2048 |
| 7 | 0.191650390625000 | 785/4096 |
| 8 | 0.187774658203125 | 6153/32768 |
| 9 | 0.182800292968750 | 2995/16384 |
| 10 | 0.181394577026367 | 95103/524288 |
| 11 | 0.179729461669922 | 47115/262144 |
| 12 | 0.177905917167664 | 1492383/8388608 |
| 13 | 0.176829308271408 | 5933407/33554432 |
| 14 | 0.175467818975449 | 5887723/33554432 |
| 15 | 0.174551831558347 | 93711801/536870912 |
| 16 | 0.173306388780475 | 93043159/536870912 |
| **17** | **0.172492378042080** | 1481698245/8589934592 |
| **18** | **0.171484045829857** | 5892146949/34359738368 |
| **19** | **0.170751430407108** | 23467897899/137438953472 |
| **20** | **0.169974470507441** | 46722226687/274877906944 |
| **21** | **0.169331070001135** | 93090740205/549755813888 |
| **22** | **0.168731922682014** | 1484181687727/8796093022208 |
| **23** | **0.168160640097426** | 1479156632971/8796093022208 |
| **24** | **0.167658425392759** | 11797912845693/70368744177664 |
| **25** | **0.167159563701750** | 94102468599827/562949953421312 |
| **26** | **0.166722853561947** | 375426490587865/2251799813685248 |
| **27** | **0.166292433824842** | 748914543008093/4503599627370496 |

Unreduced numerators `a(m) = eps(m) * 2^(2m+1)`, `m=1..27`:

```
2, 8, 28, 112, 416, 1644, 6280, 24612, 95840, 380412, 1507680, 5969532,
23733628, 94203568, 374847204, 1488690544, 5926792980, 23568587796,
93871591596, 373777813496, 1489451843280, 5936726750908, 23666506127536,
94383302765544, 376409874399308, 1501705962351460, 5991316344064744
```

Structural notes:

* `eps` is non-increasing throughout and **strictly** decreasing for `m >= 5`.
* The exact ties `eps(1)=eps(2)` and `eps(3)=eps(4)` are the only ties. **No new
  tie appears anywhere in `m=5..27`** -- worth recording, since a recurrence of
  the tie pattern would have been a structural hint.
* `Delta(m) = eps(m-1) - eps(m)` oscillates strongly in `m mod 2`, even `m`
  running above odd `m`. The oscillation damps over the new range and has
  nearly closed by the end: at `m=26,27` the two chains give `4.367e-4` and
  `4.304e-4`. This matters for section 5.

## 5. Symbolic regression

### Protocol, pre-registered

* **Data.** Exact `eps_30(m)`, fit on `10 <= m <= 21` (12 points), **hold out
  `m = 22..27` entirely** (6 points). The lower bound drops the pre-asymptotic
  head: `m <= 9` carries both exact ties and increments up to `3.1e-2`, some
  70x the tail, and fitting an asymptotic form there is meaningless. (Fitting
  from `m>=5` instead was run as a robustness check; every family fails, which
  confirms the head is genuinely pre-asymptotic rather than that the bound was
  chosen to flatter a result.)
* **Success criterion, fixed before fitting.** `eps` spans `[0.166, 0.25]`
  while the increments near the held-out block are `~4.4e-4`. A held-out error
  of "1% of `eps`" is therefore ~30x the increment being predicted, and *any*
  smooth decreasing curve clears it. So a candidate survives only if

  ```
  max |pred(m) - eps(m)| over held-out m  <  0.5 * min Delta(m) over held-out m
                                          =  2.152e-4
  ```

  -- it must predict the next step better than half the step it is predicting.
  Anything else is a failure, including expressions with visually tiny relative
  error.
* **Report the whole Pareto front**, with a held-out verdict per member.
* **Three independent seeds.** A low-complexity form that recurs across
  independent searches is an attractor of the search; one that appears once was
  a lucky draw.
* Limits of surviving expressions are read off with sympy and labelled
  **extrapolation from a fit**, never a proof.

### One honest caveat on the split

Held-out error comes out *smaller* than in-sample error for the survivors
(`8.0e-5` vs `2.2e-4`). That inverts the usual logic and has a cause: the fit
block `m<=21` carries the strong odd/even oscillation in `Delta`, while the
held-out block `m=22..27` is where it has largely damped. The held-out block is
an **easier** target than the fit block. The survival verdicts below should be
read with that discount.

### PySR Pareto front

Front from the first search (fit `10 <= m <= 21`, held out `m = 22..26`,
threshold `2.184e-4`). Trailing near-duplicates that only add a vanishing
nuisance term are collapsed; full output in `sr_output.txt`.

| cplx | fit MSE | fit maxerr | HOLD maxerr | /thresh | m->inf | verdict | equation |
|---|---|---|---|---|---|---|---|
| 1 | 1.405e-5 | 6.96e-3 | 7.712e-3 | 35.3 | 0.174435 | fails | `0.1744349` |
| 5 | 7.185e-8 | 4.50e-4 | 8.577e-4 | 3.9 | 0.158666 | fails | `0.15866551 + 0.2317924/x` |
| **6** | **1.176e-8** | **2.23e-4** | **5.800e-5** | **0.3** | **0.142455** | **SURVIVES** | **`0.14245495 + 0.12344677/sqrt(x)`** |
| 7 | 8.391e-9 | 2.02e-4 | 3.452e-4 | 1.6 | 0 | fails | `0.5776412/(sqrt(log x) + 1.6668488)` |
| 8 | 8.336e-9 | 2.08e-4 | 3.737e-4 | 1.7 | 0.082394 | fails | `0.082394 + 0.5281369/(log x + 3.0326273)` |
| 9 | 8.332e-9 | 2.02e-4 | 3.675e-4 | 1.7 | -0.015135 | fails | `-0.0151346 + 0.68238807/(sqrt(log x) + 1.9549013)` |
| 10 | 1.621e-8 | 2.47e-4 | 5.709e-5 | 0.3 | 0.142455 | (same as cplx 6) | cplx-6 expression + a vanishing `0.7665^x` term |
| 11-22 | ~1.4e-8 | ~3.0e-4 | 3.1-3.7e-4 | 1.4-1.7 | 0 | fails | `sqrt(log x)` forms plus vanishing nuisance terms |

Reading the front:

* Exactly **one** expression survives, at complexity 6:
  `eps(m) ~ 0.14245495 + 0.12344677 / sqrt(m)`. The complexity-10 entry is the
  same expression plus a `0.7665^m` term that vanishes; it is not a second
  survivor and should not be counted as one.
* Everything the search produced *above* complexity 6 fits better in-sample and
  predicts worse out of sample -- the front's own accuracy/complexity trade-off
  turns over exactly where the held-out verdict does. That is the overfitting
  signature the held-out block was set up to catch, and it fired.
* Several higher-complexity members have limit exactly 0, and one has limit
  `-0.015`, i.e. a negative Bayes error. That such expressions sit at the top of
  the in-sample front is itself a warning about reading limits off fits.

**Seed replication was launched (seeds `20260831`, `7`, `991`) and did not
complete within this arm's budget; the front above is from a single seed.**
So `a + b/sqrt(m)` is reported as a form the search *found*, not as a verified
attractor of the search. This does not weaken the arm's conclusion, because
that conclusion does not rest on the SR expression -- the decisive comparison
below reaches the same form by a different route and then shows it does not
settle the limit anyway.

### The comparison that actually decides the limit question

PySR searches over a form space it chooses. To ask the limit question directly,
the same held-out test was applied to hand-chosen parametric families, half of
them with a strictly positive limit and half with limit exactly zero, each
fitted by multistart least squares. (Multistart is not a refinement here: with a
single start the free family `a + b*m^-p` scored *worse in-sample* than its own
restriction `a + b/sqrt(m)`, which is impossible at the optimum. That was a
local minimum being reported as a result.)

Fit `10 <= m <= 21`, held out `m = 22..27`, threshold `2.152e-4`:

| family | limit | fit maxerr | HOLD maxerr | /thresh | eps(inf) | verdict |
|---|---|---|---|---|---|---|
| `a + b/m` | positive | 4.501e-4 | 9.579e-4 | 4.45 | 0.158665 | fails |
| `a + b/sqrt(m)` | positive | 2.231e-4 | **8.010e-5** | **0.37** | 0.142455 | **SURVIVES** |
| `a + b*m^-p` | positive | 2.107e-4 | 4.211e-4 | 1.96 | 0.128606 | fails |
| `a + b*log(m)/m` | positive | 2.166e-4 | **1.888e-4** | **0.88** | 0.148845 | **SURVIVES** |
| `b*m^-p` | **zero** | 2.480e-4 | 1.045e-3 | 4.86 | 0 | fails |
| `b/log(m)` | **zero** | 2.156e-2 | 2.450e-2 | 113.9 | 0 | fails |
| `b/(log m)^p` | **zero** | 2.082e-4 | **2.128e-4** | **0.99** | **0** | **SURVIVES** |
| `b/log(c+m)^p` | **zero** | 2.090e-4 | 4.349e-4 | 2.02 | 0 | fails |
| `b/(c + log m)^p` | **zero** | 2.073e-4 | 4.549e-4 | 2.11 | 0 | fails |
| `b/(c + log m)` | **zero** | 2.357e-4 | 8.242e-4 | 3.83 | 0 | fails |

Robustness, earlier split (fit `10..18`, held out `m = 19..27`, 9 points):
`a + b/sqrt(m)` survives at 0.78, `a + b*log(m)/m` at 0.65, and the limit-zero
`b/(log m)^p` at **0.62** -- i.e. on the harder, longer held-out block the
limit-zero family is the *best* of the three.

**This is the result.** A limit-positive family and a limit-zero family both
clear a pre-registered held-out threshold that was deliberately set at the scale
of the increment. Held-out prediction over `m=22..27` does not discriminate
between `eps_30(m) -> 0.1425` and `eps_30(m) -> 0`.

`a + b*m^-p` failing while its own restriction `a + b/sqrt(m)` survives is not a
contradiction after the multistart fix -- the free family does fit better
in-sample (2.107e-4 vs 2.231e-4), as nesting requires, and predicts worse out of
sample. That is textbook overfitting with one extra parameter on 12 points, and
it is a second reason to distrust any limit read off a fitted form here.

## 6. Two more instruments, both agreeing the limit is undetermined

**Window stability of the fitted asymptote.** Fit `eps ~ a + b*m^-p` (multistart)
on windows sliding right. If the asymptote `a` were converging, that would be
real evidence for a positive limit.

| fit window | n | a (asymptote) | b | p | maxerr |
|---|---|---|---|---|---|
| m>=3..27 | 25 | 0.143509 | 0.15318 | 0.5878 | 7.43e-3 |
| m>=5..27 | 23 | 0.155619 | 0.20573 | 0.8909 | 3.37e-3 |
| m>=8..27 | 20 | 0.149855 | 0.14602 | 0.6613 | 1.20e-3 |
| m>=10..27 | 18 | 0.141240 | 0.12141 | 0.4799 | 2.09e-4 |
| m>=13..27 | 15 | 0.148320 | 0.14561 | 0.6353 | 1.69e-4 |
| m>=16..27 | 12 | 0.151625 | 0.17483 | 0.7520 | 9.97e-5 |
| m>=18..27 | 10 | 0.151431 | 0.17069 | 0.7406 | 3.86e-5 |

`a` moves over `[0.141, 0.156]` and has not settled; the exponent `p` moves over
`[0.48, 0.89]` alongside it. That 0.015 drift is **35 times `Delta(27)`**: simply
choosing where to start the fit moves the asymptote by dozens of steps' worth of
the sequence's own remaining motion. This substitutes for a confidence interval,
which cannot be legitimately constructed from 27 deterministic points.

**Aitken delta-squared** on `eps` itself, anchored at consecutive `m`:

```
m=21: 0.160620    m=22: 0.156448    m=23: 0.164007
m=24: 0.092939    m=25: 0.163654
```

Scatter of that size across adjacent anchors -- one of them 0.093 -- means the
sequence is nowhere near the regime where an extrapolation of this kind is
meaningful. It is reported precisely because it is the cleanest single piece of
evidence that 27 points cannot pin the limit.

**Decay exponent.** `log Delta = a + b log m` over trailing windows gives `b` in
`[-1.83, -1.51]` with no convergence, and the drift tracks which parities each
window happens to contain. Cleaning the parity artifact by fitting the two-step
increments `eps(m) - eps(m+2)` along each chain separately:

| floor | odd chain | even chain |
|---|---|---|
| `m >= 9` | -1.293 | -1.459 |
| `m >= 13` (consistent with `mlo=10` used everywhere else) | **-1.547** | **-1.586** |

The floor matters, and only the `m>=13` row should be read: `m>=9` lets the
pre-asymptotic head back into the odd chain, which is why the odd exponent moves
by 0.25 while the even one barely moves. At the consistent floor the two chains
agree closely, near `-1.57`.

That looks at first like evidence for a summable `Delta` and hence a positive
limit. It is not, and the reason is worth stating precisely. **Both** surviving
candidates have an effective two-step log-log slope well below `-1` over this
same finite range:

| | own predicted exponent, `m=13..25` |
|---|---|
| `a + b/sqrt(m)` (limit 0.1425) | -1.424 |
| `b/(log m)^p`, fitted `b=0.2230, p=0.2472` (limit **zero**) | -1.352 |
| **observed in the data** | **-1.547 / -1.586** |

The limit-zero family produces an apparent exponent of `-1.35` over this window
**despite `Delta ~ 1/(m (log m)^(p+1))` being non-summable**, because the
`(log log m)` term contributes about `-0.35` to the local slope at these `m`.
That is the whole point: a measured slope below `-1` over `m=13..25` carries no
information about summability, and therefore none about the limit. The two
candidates' own predicted exponents differ from each other by only 0.07, far
inside the range over which this instrument drifts with the choice of floor
(0.25, in the table above). (The candidates' figures are smooth-curve
evaluations while the observed figures come from data still carrying residual
parity structure, so the two columns are not a like-for-like comparison and no
discrepancy should be read off their difference.)

## 7. What this establishes, and what it does not

**Established (exact, checkable):**

* `eps_30(m)` for `m = 1..27`, exactly, with the published `m=1..16` reproduced
  by a third independent implementation and `m=17` confirmed by a fourth.
* `eps_90(m) = 1/2` exactly for `m = 1..27`.
* `eps_30` is non-increasing, strictly decreasing for `m >= 5`, with exactly two
  exact ties, both at `m <= 4`.
* An `m * 2^(m+2)` algorithm replacing the previous `2^(2m+1)` one.
* The numerator sequence is not indexed in OEIS.

**Not established, and explicitly disclaimed:**

* **(a) No closed form is proved.** `0.142455 + 0.123447/sqrt(m)` is a **fitted
  conjecture**, not a theorem. It survives a held-out test that a limit-zero
  competitor also survives.
* **(b) The limit is undetermined.** Three independent instruments -- held-out
  family comparison, window stability of the fitted asymptote, and Aitken
  extrapolation -- agree that 27 exact points do not distinguish a positive
  limit near 0.14 from a limit of zero.
* **(c) Per `PATH.md` 9.4, none of this is a route to P1 regardless of the
  answer.** Exactness never arrives at any finite `m`, and Theorem W already
  settles that. This section is repeated from section 0 on purpose.

## 8. Suggested `PATH.md` amendment (NOT applied)

`PATH.md` was deliberately left untouched. If the extension is to be recorded,
the minimal honest edit is in section 9.4, replacing

> Exact values `eps_30(1)=1/4` down to `0.17331` at `m=16`

with something like

> Exact values `eps_30(1)=1/4` down to `0.16629` at `m=27` (arm `a25`, which
> also reproduced `m=1..16` independently and reduced the cost from
> `2^(2m+1)` to `m*2^(m+2)`; see `RESULTS-eps30-extended.md`). Symbolic
> regression on the 27 exact values yields `0.14246 + 0.12345/m^(1/2)` as a
> held-out-validated fit, but a limit-**zero** family `b/(log m)^p` passes the
> same held-out test, so the limit remains undetermined -- which changes
> nothing, since the question is not a route to P1 either way.

No row status changes.

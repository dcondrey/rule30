# Binary-wedge horizon: a simpler sufficient target

Date: 2026-09-02, exhaustive census extended to `n=29` on 2026-09-17

Status: **THE SHARP PREREGISTERED BOUND IS FALSIFIED AT `n=15`.  THE
ONE-CELL-WEAKER BOUND THAT STILL IMPLIES DLP HAS ZERO EXACT FAILURES THROUGH
`n=29`, BUT IS UNPROVED.  PERIOD TWO AND P1 REMAIN OPEN.**

The 2026-09-17 extension changes the reading of the `n=15` saturation.  Over
`7 <= n <= 29` the slack `max_c M_c(n) - n` declines at roughly `-0.13` per
unit `n`.  It is not monotone and the three highest lengths run against the
trend: `-5, -5, -3, -2` at `n = 26, 27, 28, 29`.  `(BWH+)` is therefore **not asymptotically
tight**; it is tight only at small `n`, and the `n=15` saturator is a small-`n`
artifact rather than a near-miss of a sharp bound.  See section 4a, which
argues this makes the theorem easier to prove, not harder.

## 1. Definition

For `W in {1,2}^n` and constant inverse-cut symbol `c in {2,3}`, triangular
right-permutivity uniquely forces endpoint symbols `Q_0,Q_1,...` so that
each newly exposed inverse-terminal cut cell equals `c`.

Let `b_c(W)` be the length of the initial block of `Q` contained in
`{1,2}`, with no hard-core/no-`11` requirement, and define

```text
M_c(n) = max { b_c(W) : W in {1,2}^n }.
```

The preregistered candidate was

```text
M_c(n) <= n.                                      (BWH)
```

The exact held-out search falsified it.  The repaired live target is

```text
M_c(n) <= n+1 for every n>=7 and c in {2,3}.      (BWH+)
```

No post-hoc claim is made that the repaired threshold was preregistered.
It is retained because `n+1`, not `n`, is the exact threshold sufficient
for the existing reduction.

## 2. Why `(BWH+)` closes period two

If a DLP witness exists at length `n`, tail `c`, and residue
`r in {0,1,2}`, its forced continuation has length

```text
n+r+2 >= n+2
```

and every continuation symbol belongs to `{1,2}`.  It would therefore give
`b_c(W)>=n+2`, contradicting `(BWH+)`.  The no-`11` condition and the
terminal-pull condition are not needed for this implication.

Equivalently, using the proved rotated-Peel identity, `(BWH+)` says there is
no binary word `f` of length `2n+2` with

```text
P^n(I(f)) = c^(n+2).                               (1)
```

Thus an all-length proof of `(BWH+)` implies DLP, both constant-tail
separators, the rank-zero separator, and exclusion of the nonconstant
period-two center trace.  It would not by itself solve full P1.

## 3. Exact census and the falsifier

Exhaustive enumeration gives:

| `n` | `M_2(n)` | `M_3(n)` |
|---:|---:|---:|
| 1 | 1 | 2 |
| 2 | 2 | 1 |
| 3 | 1 | 4 |
| 4 | 2 | 3 |
| 5 | 2 | 8 |
| 6 | 9 | 6 |
| 7 | 7 | 6 |
| 8 | 6 | 7 |
| 9 | 5 | 8 |
| 10 | 9 | 9 |
| 11 | 9 | 8 |
| 12 | 9 | 11 |
| 13 | 10 | 10 |
| 14 | 11 | 11 |
| 15 | 11 | **16** |
| 16 | 14 | 14 |
| 17 | 13 | 13 |
| 18 | 17 | 18 |
| 19 | 18 | 16 |
| 20 | 16 | 17 |
| 21 | 16 | 21 |
| 22 | 18 | 19 |
| 23 | 19 | 17 |
| 24 | 21 | 23 |
| 25 | 20 | 21 |
| 26 | 21 | 21 |
| 27 | 22 | 22 |
| 28 | 22 | 25 |
| 29 | 27 | 24 |

Rows `21` to `29` are the 2026-09-17 extension, by
`binary_wedge_census_exhaustive.py`; rows `1` to `20` are the original
`binary_wedge_horizon.py` census.  The two implementations share the bit-sliced
kernel but not the enumeration path, and the newer one reproduces every
published row from `7` to `20` exactly before extending.  `(BWH+)` has zero
failures throughout, over `2^29` sources at the top length.

**Control provenance, stated because it is not uniform across the rows.**  The
`n=21..27` leg ran the `n=7..20` replay first and it passed on all 14 lengths.
The `n=28` and `n=29` rows came from one leg run with `--skip-control`.  The
control was then re-run on its own the same day, from the same working tree, and
passed on all 14 published lengths; the same invocation recomputed `n=21` as
`(16, 21)`, matching the table.  So every row above is attested by a replay that
aborts on mismatch, but the two top rows' attestation comes from a sibling run
rather than from their own invocation.

The bold entry falsifies `(BWH)`.  One exact witness is

```text
n = 15
c = 3
W = 111122211212112
Q = 1221111112211121 0 332...
                            ^ first nonbinary symbol
```

It survives exactly `16=n+1` appended symbols, so it saturates rather than
falsifies `(BWH+)`.

The bit-sliced implementation was cross-checked against the literal
inverse-cone constructor on 6,152 generated cells through source length
seven.

## 4. Long falsification pressure

A deterministic random search of 20,000 words at each length found:

| `n` | observed tail-2 maximum | observed tail-3 maximum |
|---:|---:|---:|
| 24 | 15 | 15 |
| 32 | 13 | 14 |
| 48 | 13 | 13 |
| 64 | 14 | 13 |
| 96 | 14 | 14 |
| 128 | 18 | 15 |

The separate evolutionary falsifier finds the exact `n=15`, tail-3
saturator under a small deterministic control run.  Neither random nor
evolutionary searches are evidence of an all-length bound beyond their
role as adversarial falsifiers.

## 4a. The bound is not tight, which changes the proof target

Write `g(n) = max(M_2(n), M_3(n))`.  Over the full exhaustive range
`7 <= n <= 29`:

```text
g(n) = 0.871 n + 0.24      (least squares over 7<=n<=29, residual sd 1.40)
g(n) - n  declines at -0.129 per unit n
```

Restricting to `18 <= n <= 29` gives a shallower `0.724 n + 3.91`, so the slope
is still below one on the top half of the range.  The observed slack runs `+1`
at `n=15`, `0` at `n=18` and `n=21`, then `-1, -4, -5, -5, -3, -2` at
`n = 24..29`.

**The estimate is moving, and it is moving the wrong way.**  Successive fits:
`0.842 n + 0.65` over `7..27`, `0.851 n + 0.52` over `7..28`, `0.871 n + 0.24`
over `7..29`; the restricted fit moves much more, `0.503` to `0.609` to `0.724`.
Each new length has raised the slope, the last three slacks rise rather than
fall, and `M_2(29) = 27` is the largest absolute horizon in the census.  The
conclusion of this section still holds at `0.871 < 0.95`, but the margin is
`0.079` per unit `n` and shrinking, not a comfortable `0.16`.  Two more lengths
moving the same way would put the slope where a lossy bound no longer has room,
and that, not a falsifier, is what the next census row should be read for.
Residual sd is the population sd throughout.

Two consequences.

**The `n=15` saturation is a small-`n` artifact, not a near miss.**  Modelling
the horizon tail as `P(b >= k) ~ p^k` and matching the fitted slope gives
`p = 2^(-1/0.871) = 0.451`, not the `0.5` a fair coin would give.  The expected
number of sources with `b >= n+2` is then `(2p)^n p^2 = 0.902^n * 0.203`, which
is `4.3e-2` at `n=15` and `1.0e-2` at `n=29` and keeps falling, though more
slowly than the `p = 0.439` of the `n<=27` fit implied.  The risk of
falsification was concentrated at small `n`, and small `n` is now exhausted to
`29`.  A falsifier is not where the remaining doubt should be spent.

**The theorem has roughly 16 percent slack asymptotically, so it does not need
a sharp argument.**  Section 5 concludes from the assumption cores and the ANF
expansion that a proof "should expect a branched ancestry or a nonlinear
clause".  That remains true of any argument aiming at the exact threshold.  It
is not required for `(BWH+)`.  Any counting, entropy or compression argument
establishing `g(n) <= n+1` with slack for all `n >= N_0`, combined with the
exhaustive census below `N_0`, closes the rung.  The census now supplies
`N_0 <= 30` for free.  A bound as weak as `g(n) <= 0.95 n` for large `n` would
suffice, and is `0.11 n` above the measured growth.

This is the one place the extended census changes what should be attempted
next: the target is a lossy asymptotic bound plus a finite check, not a tight
combinatorial identity.

**Maximizer degeneracy is extreme and grows more so.**  Counting sources that
attain the maximum, from the horizon histograms:

| `n` | sources at the `c=2` max | sources at the `c=3` max |
|---:|---:|---:|
| 22 | 16 | 6 |
| 23 | 26 | 40 |
| 24 | 12 | 10 |
| 25 | 60 | 64 |
| 26 | 4 | 24 |
| 27 | 12 | 50 |
| 28 | 29 | 48 |
| 29 | 4 | 48 |

Between four and sixty-four sources out of as many as `2^29` reach the
maximum.  This is section 5's `n=15` observation holding at every length
tested: the effective number of independent trials is vastly smaller than
`2^n`, which is why the naive fair-coin model overpredicts saturation.  It also
says the natural search object is the forced continuation `Q`, not the source
`W`.

**The maximum is attained by essentially one continuation.**  Counting distinct
`Q` among all maximizers, exhaustively, for `18 <= n <= 24` and both tails: 11
of the 14 `(n,c)` pairs have exactly **one** distinct `Q`, and the other three
(`n=19,c=3`; `n=23,c=2`; `n=23,c=3`) have exactly two.  (**Correction,
2026-09-17:** this sentence previously read "12 ... and the other two", which is
inconsistent with the 17 words the next paragraph counts; `11 + 3*2 = 17` and
`12 + 2*2 = 16`.  The recount is section 4b, and the source words are listed
there.)  The control is the `n=15`, `c=3` case of section 5, which
this recomputes independently as 18 maximizers sharing the single continuation
`1221111112211121`, matching the value recorded there.  So up to 40 distinct
sources, drawn from as many as `2^24` words, converge on one forced
continuation.

That collapses the problem's apparent dimension.  `(BWH+)` quantifies over
`2^n` sources, but the extremal object is a single word, so the equivalent
rotated-Peel form of section 2, "no binary `f` of length `2n+2` has
`P^n(I(f)) = c^(n+2)`", is the honest statement of the search space.  It also
explains section 5's finding that the source-assumption cores are neither
singleton nor canonical: the binding constraint does not live on the source.

**The extremal continuations are nested across lengths.**  Among the 17
continuations collected, four suffix relations hold between consecutive lengths
at the same tail, including a chain

```text
n=21, c=3   211111121221222212222     M=21
n=22, c=3     1111121221222212222     M=19
n=23, c=3       11121221222212222     M=17
```

and two more, `Q(19,c3)` a suffix of `Q(18,c3)` and `Q(20,c2)` a suffix of
`Q(19,c2)`.  In every case `n` rises by one, `M` falls by two, and the shorter
word is the longer one with its first two symbols deleted.  (**Correction,
2026-09-17:** the count was previously five.  The fifth was `Q(23,c3)` as a
suffix of `Q(21,c3)`, which is the composite of the two chain steps above and
not an independent relation.)  Four relations out of 17 words is a lead, not a
law, and the relation plainly does not hold for every consecutive pair.  But a
self-similar family of extremal continuations is the first structure found here
that could carry the induction section 5 reports as missing, and testing it is
cheap: extend the distinct-`Q` census past `n=24` and check whether each new
maximal `Q` is the previous one minus two leading symbols.  Section 4b does
that.

## 4b. The nested-continuation conjecture is falsified as a law, and what survives

Section 4a leaves one concrete experiment: extend the distinct-`Q` census past
`n=24` and check whether each new maximal `Q` is the previous length's minus two
leading symbols.  Run exhaustively for `18 <= n <= 27` and both tails.  The
`18 <= n <= 24` part is a control: it recomputes the words section 4a collected,
independently of the run that produced them.

| `n` | `c` | `M` | maximizing sources | distinct `Q` | maximal `Q` |
|---:|---:|---:|---:|---:|:---|
| 18 | 2 | 17 | 16 | 1 | `11112212122112122` |
| 18 | 3 | 18 | 3 | 1 | `221112222221212211` |
| 19 | 2 | 18 | 6 | 1 | `212111112212222121` |
| 19 | 3 | 16 | 10 | 2 | `1112222221212211`, `2221221221221111` |
| 20 | 2 | 16 | 8 | 1 | `2111112212222121` |
| 20 | 3 | 17 | 12 | 1 | `11111112212121122` |
| 21 | 2 | 16 | 2 | 1 | `2112112112221111` |
| 21 | 3 | 21 | 4 | 1 | `211111121221222212222` |
| 22 | 2 | 18 | 16 | 1 | `222221222112112221` |
| 22 | 3 | 19 | 6 | 1 | `1111121221222212222` |
| 23 | 2 | 19 | 26 | 2 | `1212122212222121122`, `2222112211221111122` |
| 23 | 3 | 17 | 40 | 2 | `11121221222212222`, `21221111111121222` |
| 24 | 2 | 21 | 12 | 1 | `121112121212222222111` |
| 24 | 3 | 23 | 10 | 1 | `11122212212222111122111` |
| 25 | 2 | 20 | 60 | 1 | `12112212212212221211` |
| 25 | 3 | 21 | 64 | 2 | `122212212222111122111`, `122221112111121112111` |
| 26 | 2 | 21 | 4 | 1 | `222212122211221211122` |
| 26 | 3 | 21 | 24 | 1 | `122212222122112121221` |
| 27 | 2 | 22 | 12 | 1 | `2212112122211211122212` |
| 27 | 3 | 22 | 50 | 1 | `1211121212112211112112` |

**Controls, and why the counts are trustworthy rather than merely plausible.**
The `--continuations` mode composes its maximum and its survivor set over the
same chunk partition the census uses, but by a different accumulation, and it
sweeps one tail per pass where the census sweeps both together.  That is an
independent path to the same numbers, so agreement is a test rather than a
restatement, and it was checked mechanically, not by eye:

* all **20** of the `M` values above equal the section 3 census entry at the
  same `(n,c)`, zero mismatches;
* all **12** maximizing-source counts in `22 <= n <= 27` equal the section 4a
  degeneracy table, zero mismatches.

Note that `width_exponent = min(width_exponent, length)` makes the chunk count
one for `n <= 18`, so `n=18` ran unchunked and only `19 <= n <= 27` exercises the
chunk-composition path.  The 18 agreeing rows over that range are the evidence
that the composition is correct.

The distinct-`Q` tally over `18 <= n <= 27` is 16 pairs with one and 4 with two;
restricted to the `18 <= n <= 24` range section 4a reported, it is 11 with one
and 3 with two, for 17 words, which is the recount behind that section's
correction.

**The conjecture is false as a law.**  Over the 18 consecutive same-tail steps
in the table, the relation `Q(n+1,c) = Q(n,c)[2:]` holds 5 times:

```text
n=18 -> 19  c=3   M 18 -> 16
n=19 -> 20  c=2   M 18 -> 16
n=21 -> 22  c=3   M 21 -> 19
n=22 -> 23  c=3   M 19 -> 17
n=24 -> 25  c=3   M 23 -> 21      <- the new one, first tested here
```

The `n=24 -> 25` step is the only new instance, and the chain
`21 -> 22 -> 23` does **not** continue to `24`: `M_3` jumps from 17 to 23 there.
No new chain of length three appears.  Every other listed relation among all 24
words is the composite `Q(23,c3)` inside `Q(21,c3)`, which is the two chain
steps applied twice and carries nothing new.

**What survives is weaker than it looks, and one half of it is definitional.**
The relation `Q(n+1) = Q(n)[2:]` *forces* `M(n+1) = M(n) - 2`, because `M` is
the word's length.  That direction is a tautology and should not be counted as
evidence.  The converse is the measurable statement, and over the range tested:

> Every step with `M(n+1,c) = M(n,c) - 2` also has `Q(n+1,c) = Q(n,c)[2:]`.
> Five steps out of five, `18 <= n <= 26`, both tails.

The trial count for that statement is 5, not 18: only the steps where `M` drops
by exactly two can test it, and there are five in the range.  Five for five with
no counterexample is a regularity worth naming and nowhere near a law, and it is
a much smaller claim than the unconditional relation, which fails 13 of the 18
steps.  It says the extremal continuation is
inherited only while the horizon is *falling at the maximal rate*, and that a
rise in `M` always installs a fresh word.  Since section 4a shows `M` is falling
relative to `n` on average but rises absolutely at most lengths, the inherited
steps are the exception, not the backbone, and a self-similar family cannot
carry the induction section 5 wants.

**Kill condition for any successor.**  A single step with `M(n+1,c) = M(n,c)-2`
and `Q(n+1,c) != Q(n,c)[2:]` refutes the surviving statement.

Only a step where `M` falls by exactly two can test it, and the census decides
which steps those are before any continuation run is worth starting.  Neither of
the two new steps qualifies.  At `27 -> 28`, `M_2` is flat at `22` and `M_3`
rises `22 -> 25`.  At `28 -> 29`, `M_2` rises `22 -> 27` and `M_3` falls by one,
`25 -> 24`.  So `n=28` and `n=29` supply **no new trial** between them, and the
statement can go several lengths without one.  Check the census row first; run
`--continuations` at `n` and `n+1` only for a tail that actually dropped by two.
The cost is a full sweep per tail, about 600 s at `n=27` and doubling per unit
`n`, so this is not a test to run speculatively.

Absent a qualifying step, the honest status is: the self-similar route is
closed, and section 5's warning that a proof "should expect a branched ancestry
or a nonlinear clause" is unrelieved.

## 5. Structural observations

At several exact maxima, many distinct source words share one forced
continuation and die on the same next cell.  At the exceptional `n=15`,
tail-3 maximum, 18 sources reach the 16-cell plateau, all with the displayed
`Q`, and all next force state `0`.  This suggests a synchronized phase
catastrophe rather than a source-by-source local obstruction.

In the exact coordinates `q=(H,L)` and `E=1+H+L`, binary legality is `E=0`.
The local Peel rule is

```text
H(phi) = H_R + 1 + E_L + E_L H_L,
E(phi) = E_R + H_R(H_L + E_L).
```

Forcing a constant newest cut determines the appended high bit by the
activity parity on its complete dependency diagonal.  `(BWH+)` is therefore
the concrete missing statement:

> A length-`n` zero-defect source cannot satisfy both output-coordinate
> legality equations through diagonal `n+1`.

The source-assumption cores are not generally singleton and their positions
are irregular.  A proof should expect a branched ancestry or a nonlinear
clause, not one propagating defect and not a fixed linear parity separator.

The exact inclusion-minimal cores found by one deterministic solver run are:

| `n` | tail 2 source positions | tail 3 source positions |
|---:|:---|:---|
| 7 | `(3)` | `(2,3,4)` |
| 8 | `(2,4,5)` | `(1,2,3,5,7)` |
| 9 | `(1,2,3,4)` | `(1,2,3,4,5)` |
| 10 | `(6,8)` | `(3,4,5)` |
| 11 | `(4,5,8)` | `(5,6,7,9)` |
| 12 | `(5,6,7,8,11)` | `(3,4,6,7)` |
| 13 | `(2,3,4,5,7,8,9)` | `(4,5,6,7,8,9)` |

Every formula is SAT when all source positions are four-state, and every
one-assumption deletion from a displayed core is SAT.  The cores are not
canonical; their growth and movement are the relevant negative result.

Direct ANF expansion gives the same warning.  By source lengths 8--12 each
binary-legality residual depends on every source variable, has hundreds to
thousands of monomials, and usually has degree `n` or `n-1`.  The apparent
counting surplus of `n+2` equations over `n` bits is therefore not a
triangular linear-rank proof in the raw source coordinates.

## 6. Reproduction

The extended census, which first replays `n=7..20` against the published table
above and aborts on any mismatch, then runs the new lengths:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python \
  experiments/rule30/p1-period2-invariant/binary_wedge_census_exhaustive.py \
  --first-n 21 --last-n 29 --chunk-exponent 18 --histogram
```

Exit status is 1 if `M_c(n) >= n+2` for any `n >= 7`.  Cost on one core:
about 5 s at `n=21`, 60 s at `n=24`, 609 s at `n=27`, 1154 s at `n=28`, 2277 s
at `n=29`, so almost exactly doubling per unit `n`; `n=31` is about 2.5 hours
and `n=33` about 10.

The distinct-`Q` census of section 4b is a separate mode, one full sweep per
tail rather than one for both, at comparable cost per length.  Section 4b's
table is the concatenation of two runs:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python \
  experiments/rule30/p1-period2-invariant/binary_wedge_census_exhaustive.py \
  --continuations --first-n 18 --last-n 23 --chunk-exponent 18 \
  | tee experiments/rule30/p1-period2-invariant/binary-wedge-continuations-n18-n23.log

PYTHONDONTWRITEBYTECODE=1 uv run --no-project python \
  experiments/rule30/p1-period2-invariant/binary_wedge_census_exhaustive.py \
  --continuations --first-n 24 --last-n 27 --chunk-exponent 18 \
  | tee experiments/rule30/p1-period2-invariant/binary-wedge-continuations-n24-n27.log
```

It prints `M` alongside each length, which cross-checks against the census
table above; that check passed on every length run here.  The suffix analysis
that section 4b reports is not done by eye:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python \
  experiments/rule30/p1-period2-invariant/binary_wedge_continuation_chains.py \
  experiments/rule30/p1-period2-invariant/binary-wedge-continuations-n18-n23.log \
  experiments/rule30/p1-period2-invariant/binary-wedge-continuations-n24-n27.log
```

It re-derives the distinct-`Q` tally, lists every suffix relation among the
collected words, marks which are composites of consecutive-step relations, and
reports the converse test separately from the definitional direction.

The `.log` files are matched by a global gitignore rule and are **not** assumed
to persist.  Section 4b's table is the artifact of record; the script's input is
whatever the two commands above produce on a fresh run, and rerunning them is
the way to re-validate the table.  If the logs are wanted in the tree they need
`git add -f`.

The original census and the adversarial and SAT arms:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/binary_wedge_horizon.py \
  --exact-first 11 --exact-last 20 --random-per-length 20000

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/binary_wedge_adversary.py \
  --lengths 15 24 32 --population 128 --generations 80

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/binary_wedge_sat.py \
  --first-n 7 --last-n 30

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/binary_wedge_source_core.py
```

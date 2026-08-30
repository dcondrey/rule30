# Geometric attacks on P1/P2: triage

**Verdict: all three proposals are closed by one lemma, measured.  No
`GEOMETRIC_PROOF_DRAFT.md` was written; the exit condition cannot fire, for
the reason below.**

Date 2026-08-30.  Code `discriminator.py`, log `discriminator.log`.
Modal: $0.  Paid model-provider calls: $0.

## 1. The lemma that covers all three

Problems 1 and 2 are statements about **one column** of the space-time
diagram.  Every quantity the three proposals compute -- hyperbolic lightcone
distance, curvature of a continuous relaxation, spectral dimension of a shift
algebra -- is a functional of the 2D field that is continuous under changes on
a density-zero subset.  A single column is density zero.  So:

> **Single-column blindness.**  A functional of the space-time diagram that is
> continuous under modification of a density-zero subset cannot distinguish a
> diagram whose centre column is periodic from one whose centre column is not.
> No such functional can decide P1, and none can pin the centre density in P2.

This is `PATH.md` R6 obstruction (i) -- "an i.i.d. plane with column 0
overwritten periodic keeps `(w-1)/w`-maximal local entropy in every window" --
stated for the general case rather than for entropy alone.  It was already
sufficient to close the complexity/entropy family; it closes the geometric
family for the same reason.

## 2. Per-proposal, before the measurement

**Agent 1, hyperbolic geodesic embedding.**  Measures the wrong object.  The
full configuration `S(t)` never repeats for *any* ECA with a growing
lightcone, Rule 90 included, whose centre column *is* eventually periodic.
`d_H(t)` built from lightcone geometry is a function of `t` alone.  The
embedding is also not canonical: a monotone-distance embedding can be
constructed for any sequence, so monotonicity of a chosen embedding is a
property of the choice, not of Rule 30.

**Agent 2, Riemannian relaxation.**  Carries a category error -- tropical /
max-plus semirings have no Riemannian metric, so "Ricci curvature under
Max-Plus relaxation" is not a defined object.  Read charitably as the
multilinear relaxation (which is what was measured below), it still sits on
the Arm 2 obstruction: `PREREGISTRATION.md` lines 42-52 record that
Rule 30 is surjective and ergodic for uniform Bernoulli, so almost every
orbit already has centre density 1/2, and P2 survives *only* because the lone
seed is a measure-zero point.  The Boolean orbit is a measure-zero vertex set
of the relaxed manifold; ambient curvature says nothing about it.

**Agent 3, spectral triple.**  Spectral dimension is a property of the
algebra, not of one orbit.  Rule 90 induces the same shift algebra on
`{0,1}^Z`.  Any invariant of that algebra is identical for the two rules and
so cannot separate their centre columns, which have opposite P1 answers.

## 3. The measurement

Three fields, identical except as stated, same seed, same `T = 400`:

* **A** true Rule 30 lone-seed diagram;
* **B** A with column 0 overwritten by `0101...`.  196 of 324,409 cells
  change, a fraction 6.0e-4.  P1's answer flips; nothing else about the field
  does.  Asserted in code that A and B differ on column 0 and nowhere else.
* **C** true Rule 90 lone-seed diagram (the section-0 filter).

Statistics, one faithful proxy per proposal, plus a positive control:

* **S0 (control)** agreement of column 0 with `0101...`.  Reads only column 0.
* **S1** hyperbolic lightcone embedding: cell `(x,t)` to the Poincare disk at
  hyperbolic radius `0.5 t`, angle `pi x/(t+1)`; mean geodesic distance to the
  row centroid.
* **S2** multilinear relaxation of Rule 30 over `[0,1]` (`XOR -> a+b-2ab`,
  `OR -> a+b-ab`); mean log singular value of the row Jacobian, the
  expansion / "negative curvature" proxy.
* **S3** spectral dimension of `D = S + S* + diag(2s-1)` from the heat trace
  `Tr exp(-tau D^2)/W`.

**Prediction was recorded in the script docstring before the run:**
`|S(A) - S(B)| = O(1/W)` for S1-S3, and a stated kill condition -- any
statistic separating A from B by more than `O(1/W)` refutes the lemma for that
statistic and puts that attack back in play.

### Result: relative `|A - B|`, by window width

| statistic | W=32 | W=64 | W=128 | W=256 | A vs C |
|---|---:|---:|---:|---:|---:|
| **S0 control** | **0.956** | **0.956** | **0.956** | **0.956** | 0.024 |
| S1 hyperbolic | 8.6e-4 | 2.3e-4 | 1.8e-4 | 7.5e-7 | 0.26-0.47 |
| S2 relaxation | 1.0e-2 | 4.8e-4 | 1.4e-16 | 0 | 0.92-0.98 |
| S3 spectral dim | 8.3e-3 | 4.1e-3 | 2.0e-3 | 1.0e-3 | 0.26-0.29 |

**The control fires.**  S0 separates A from B by 96% (0.511 vs 1.000) at every
width, so the harness does read column 0 and the nulls below are not an
artifact of never looking at it.

**S3 is the clean demonstration**: 8.31e-3, 4.11e-3, 2.02e-3, 1.01e-3, ratios
2.02, 2.03, 2.00 across successive doublings.  That is `O(1/W)` to three
digits.  S1 decays the same way with more noise.  S2 falls to machine epsilon
by `W = 128`; with 0/1 inputs the relaxation Jacobian is an integer matrix and
its mean log singular value is `(1/n) log|det|`, which plausibly explains exact
insensitivity, but that mechanism was not verified and is not needed for the
conclusion.

**The kill condition did not fire.**  No statistic separates A from B by more
than `O(1/W)`.

### The diagnostic point

All three statistics separate Rule 30 from Rule 90 *strongly* -- 26% to 98%.
They are highly rule-sensitive and completely column-blind.  That combination
is the trap: a geometric invariant can look powerfully discriminating on the
diagrams as a whole while carrying zero information about the one column the
prize problems ask about.  Rule-sensitivity is not evidence of P1-relevance.

## 4. Consequence for the route map

The section-0 filter in `PATH.md` asks one question of every route: *does this
argument fail for Rule 90?*  This run supplies a second, independent question
that is cheaper to answer and retires a larger family in advance:

> *Is the quantity sensitive to overwriting column 0?*  If overwriting column 0
> with a periodic word changes it by `O(1/W)` or less, it cannot decide P1 or
> P2, whatever else it does.

Both filters are now recorded in `PATH.md` section 0.  Any future geometric,
spectral, topological, or information-theoretic proposal should be run through
the second one first; `discriminator.py` takes a new statistic as a one-
function drop-in.

## 5. Scope

Nothing here is a result about Rule 30.  It is a negative triage: three
proposed attacks measured column-blind, with a positive control proving the
measurement could have seen the difference.  P1 and P2 are untouched.

## Reproduction

```sh
cd experiments/rule30/p_geometric_attack
uv run --with numpy python discriminator.py 400
```

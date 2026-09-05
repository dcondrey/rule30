# Disposition of the dyadic hard-core lock route

Date: 2026-09-01

Status: **THE DYADIC LOCK IS SUBSUMED AS A STANDALONE PROOF PROGRAM.  FINITE
CORE REACHABILITY HAS THE STRICTER FINITE-PEEL-RANK PROPERTY, AND THE EXACT
RANK DESCENT REDUCES ITS ENTIRE ACCEPTED INTERSECTION TO THE RANK-ZERO
SEPARATOR.**  That separator remains open, so the period-two theorem is not
proved.

## 1. Period is a quotient of the actual reachability invariant

For a finite core prefix `u` of length `m`, let

```text
x = A_u(0^omega)
```

be its infinite zero-ray carry cut.  Two all-length results are already
proved:

```text
P^m(x) is eventually zero,                              (1)
x is ultimately periodic with power-of-two period.      (2)
```

Equation (1) is the output Peel identity from
`RESULTS-DYADIC-EXCEPTION-SEPARATOR.md`.  Equation (2) is the fiber-monoid
induction from `RESULTS-DYADIC-PERIODICITY.md`.

The implication is actually structural: starting with the eventual period
one tail in (1), each inverse Peel lift multiplies the period by at most two
because every cyclic component in the 13-element lift monoid has size one or
two.  Thus (2) is a quotient of the more informative finite-rank statement
(1).  It discards the number of available Peel descents and the eventual
zero boundary.

## 2. Exact rank descent on the accepting language

Suppose `x=I(e)` for a hard-core endpoint `e` and `x` has positive finite
Peel rank `r`.  The rotated identity gives

```text
P(I(sigma f)) = sigma^2 I(f).
```

Prepending endpoint state `2` preserves the hard-core language and lowers
positive rank by exactly one.  Hence

```text
nu(I(2^r e)) = 0.                                     (3)
```

This is the uniform reduction proved in
`RESULTS-RANK-ZERO-REDUCTION.md`.  Rank zero says precisely that the inverse
cut is a nonzero finite-support word followed by `0^omega`.

Combining (1) and (3) yields the sufficient implication

```text
finite reachable accepted cut
    => nonzero finite-support cut with hard-core terminal endpoint.       (4)
```

Therefore the single statement

> The terminal cone of no nonzero finite-support cut is hard-core

excludes every finite-core collision.  It is stronger than necessary, but it
is exact and has no hidden horizon.

## 3. Why the generic dyadic lock is retired

The proposed dyadic lock asked for a classification of every ultimately
dyadic cut with a hard-core endpoint.  That class includes cuts of infinite
Peel rank which no finite core can reach.  Controlling all of them is not
needed for (4).

The standalone spectral argument also has two exact obstructions:

1. the complete eventually-`2` hard-core family has eventually alternating
   inverse cuts, so accepted and reachable period spectra overlap at period
   two; and
2. strict period doublings are isolated but can occur at arbitrarily
   separated endpoint shifts.  The no-consecutive-doubling theorem gives no
   uniform bound on their total number, and the lasso entry state is not
   determined by the cyclic return word.

The 13-element lift monoid and its two parity-pure doubling languages remain
useful descriptions of possible failure modes.  They are not a missing
spectral contradiction.

## 4. Route disposition and surviving obligation

As an independent route, “classify all ultimately dyadic accepted cuts” is
now exhausted by scope reduction: its needed reachable subcase is already
contained in finite Peel rank and descends to rank zero.  The irreducible
remaining lemma is

```text
T(y 0^omega) is not hard-core for every nonzero finite word y.             (R0)
```

The projected-diagonal, deterministic-halving, and queue-distance programs
are three different attempts to prove `(R0)`.  Progress on those routes
should be charged to `(R0)`, not advertised as evidence that separated
dyadic doublings eventually stop.

This disposition does not assert that the generic dyadic lock is true or
false.  It proves that settling it is unnecessary for the finite-core
period-two target.

## 5. Reproduction

The all-length ingredients and their independent controls are:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/dyadic_periodicity_analyzer.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/dyadic_exception_separator.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/peel_lift_monoid.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/rank_zero_separator.py
```

The final command includes a finite cutoff census only as evidence for
`(R0)`; the reduction to `(R0)` is symbolic.

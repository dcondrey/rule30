# Preregistration: nonlinear pin-parity certificate

Date: 2026-08-31

## Exact target

Prove that, for Rule 30 and every nonzero finitely supported configuration
`y`,

```text
Tr_0(y) != Tr_0(F^2(y)).
```

The constant traces are already proved and are controls only.  It is enough
to exclude the alternating phase `0101...`; applying `F` handles `1010...`.
In the exact reverse macro recurrence recorded in `RESULTS.md`, the remaining
statement is that every finite rho-seed eventually fails the nonlinear pin
condition `D_1=1`.

## Candidate certificate class

This attempt tests a **fixed-order parity-moment certificate** for the two
reverse cumulative-OR/XOR sweeps.  For a finite Boolean word

```text
X(z) = sum_(j>=1) X_j z^(j-1),
```

write `H_k(X)` for its `k`th Hasse derivative at `z=1`, equivalently

```text
H_k(X) = sum_(j>=1) binom(j-1,k) X_j mod 2.
```

The search may use all moments through one fixed order `K<=8`, the pin phase,
the exact endpoint bits needed by the two ORs, and fixed-order mixed moments
of coefficientwise products among `A`, shifted `B`, and their cumulative-XOR
images.  A candidate must close under one complete macrostep without retaining
the raw word.  A successful certificate is either:

1. a finite transition table with at most 65,536 states whose accepting part
   has no cycle reachable from a finite rho-seed; or
2. a well-founded integer/lexicographic rank computed from the fixed moment
   tuple and proved to fall on every surviving macrostep.

All identities used for closure will be proved algebraically and checked by
exhaustive enumeration of every Boolean word up to length 16.  Reachability
enumeration is a falsifier only; it cannot establish the theorem.

## Strong outcome

A strong outcome is a fixed `K`, independent of seed length and survival
time, for which the moment/mixed-moment state closes exactly and its finite
accepting graph proves eventual pin failure.  The human proof must explain
why every finite rho-seed enters that graph and why the graph certificate
applies to arbitrarily long words.  This would give the alternating theorem,
then the requested period-two same-orbit theorem after invoking the existing
constant-fiber results.

## Kill conditions

Stop this certificate class and record an exact negative if:

- updating order `K` provably requires order `K+1`, with no fixed collection
  of mixed moments eliminating that dependency;
- two exact finite frontiers have the same registered state but different
  next pin outcomes or successor states;
- the required moment order, mixed-product degree, state count, or endpoint
  window grows with frontier length, seed length, or time;
- a proposed rank fails on an exact reachable transition;
- the method becomes a fixed-depth ladder, finite-prefix test, bounded-window
  predictor, support-width descent, or raw-frontier encoding.

The smallest collision is to be reported.  A structural family of collisions
is stronger than merely observing state growth and ends this route.

## Controls

- Rule 90: the finite row `{-1,1}` must remain a period-two collision.  Any
  claimed exclusion must use Rule 30's coefficientwise OR term.
- Rule 30 adversarial prefix: `{-8,-1,6}` must alternate through time 14 and
  fail at time 15; no moment state may reject it earlier.
- Re-run the exact Rule 30 `F^2` truth table, defect truth table, and the known
  constant-zero/constant-one bounded validations.
- Exhaustively check every proposed word identity for all words through
  length 16 and every local Boolean identity on its full truth table.
- Before promoting any surviving global invariant, test it on all 131,071
  nonzero rows supported in `[-8,8]` through 64 steps, as already registered.

## Resource limits

- local CPU only; no agents, paid calls, GPU, Modal, or SAT spacetime grids;
- `K<=8`, mixed-product degree at most 3, at most 65,536 quotient states;
- at most 16 seed bits and 128 forced macrosteps for collision discovery;
- at most 15 minutes and 2 GiB per command, at most 45 minutes total search;
- do not raise a limit after a kill condition fires.

## Why success would be uniform

Hasse moments are defined for words of arbitrary finite length, and a closed
fixed-order update/table would have the same state set for every spatial
depth.  Acyclicity or rank descent in that fixed graph would quantify over
all finite supports and arbitrarily many macrosteps.  Neither a tested seed
bound nor a time horizon would appear in the proof.

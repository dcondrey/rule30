# Episode program: what is proved, what is ruled out, and what remains

Date: 2026-09-10. Consolidated record through commit `7bac13d`.

This document is an index of the episode-composition work. It records the
mathematical results and the negative results that now define the boundary of
the approach. All statements concern the legal finite frontier map Z unless a
different domain is stated. None claims that an arbitrary legal frontier is
reachable from Rule 30's lone seed.

## What is proved

The exact variable-length composition law factors a frontier at any spatial
cut into a forward prefix and a terminal-driven backward suffix. A two-bit
seam condition is necessary and sufficient at each update. For scalar tape
`alpha gamma`,

```
R_(alpha gamma) = R_gamma o R_alpha,
K_(alpha gamma) = K_alpha AND K_gamma(after alpha).
```

Every intermediate guard is retained; a later successful guard cannot repair
an earlier failure. Resetting the carried suffix gives an explicit false
continuation. See [the composition report](RESULTS-variable-length-episode-composition.md).

The history reconstruction gives uniform individual-episode bounds. For an
episode beginning at active length r, the original bounds are `L0<=r-1` and
`L1<=r`. They sharpen as follows:

* An arbitrary legal frontier of length r>=2 admits at most `r-2` consecutive
  scalar ones; the one-symbol frontier `3` is the r=1 exception.
* An image frontier of length R>=3, carrying the terminal pair created by a
  successful update, admits at most `R-3` consecutive scalar zeros. The
  length-two image exception is explicit.

The second statement gives `b<=r+a-3` for a `1^a0^b` tape once the state at
the switch has length at least three. These are all-length bounds, not finite
census extrapolations.

## The exact phase rank and why it does not close mortality

For a frontier with terminal scalar q, let H be the depth to which its inward
bits agree with the q-alternating birth pattern, using virtual zero cells past
the physical origin. Set `rho=R-1-H`.

* A repeated scalar increases H by at least two, so rho drops by at least one.
* A `0->1` switch resets H exactly to 1.
* A `1->0` switch resets H exactly to 2.
* A return to the same phase increases rho by the elapsed number of updates.

The accounting identity is

```
rho_N = rho_1 - D - E + sum(J_switch),
```

where D counts repeated neighboring scalars, E is the additional height gain
on repeats, and J is the switch refill. The refill is unbounded: the legal
family `3 2^(4k-1)` has scalar tape `01` and switch refill `4k` for every
k>=1. Thus the phase rank proves local progress but leaves the cumulative
switch term uncontrolled. See [the phase-reset report](RESULTS-repeat-budget-phase-reset.md).

## History loss and failed resource proposals

The suffix transport is exact but not injective. Two legal frontiers with
different scalar histories, `20000013` and `20000111`, both reach
`212103210303` after four accepted updates. The exact inverse fiber is a
product of local factors; for an image word it simplifies to

```
number of legal predecessors = 2^(1+q+N_up) * 3^N_down.
```

The inverse multiplicity is not monotone on repeated scalars: verified
examples increase from 2 to 12 and decrease from 648 to 216. An all-length
pumping family keeps `(N_up,N_down,q,beta,R)` fixed except for R increasing,
while taking a repeat edge at every R beyond a threshold. Therefore no
nonnegative unit-drop rank based only on those features can prove termination.

The total repeat budget

```
D = number of emissions - number of constant runs <= r-1
```

survived an exhaustive census of 11,184,810 legal starts through length 12,
and additional SAT, cover-history, inverse-predecessor, and mutation searches.
It remains a conjecture. The local phase laws alone do not imply it.

## Exact rank obstruction and language method

An eight-memory additive scan rank was tested on exact second-image languages,
separately in both invariant sectors, without an initial upper bound. Both
systems are infeasible. The certificates are rational, solver-free checked,
and contain 152 and 104 terms. This rules out that rank family, not all
possible nonlinear ranks.

Prescribed scalar tapes can instead be handled exactly as regular languages by
repeated preimage construction. Forty-four constant and two-run languages
were completed; minimized state counts for tape lengths 1 through 7 were
`10,34,130,514,2050,8194,32770`, with no observed compression. Length-eight
and 4+4 cases reached the explicit 100,000-state cap. This is an exact tool,
but it currently grows exponentially and gives no arbitrary-tape theorem.

## Verification record

The implementation and certificates are under
`experiments/rule30/episode-composition/` and
`experiments/rule30/repeat-budget-rank/`. The principal checks include:

* 481,394 temporal composition checks and 133,546 episode-bound checks;
* 85,927 phase transitions, including 39,932 repeats and 45,995 switches;
* 173,478 successful updates across the complete length-1–9 census;
* 22 pumped-family replays through insertion length 1000 and 491 inverse-image
  formula checks;
* exact solver-free verification of both additive-rank impossibility
  certificates.

The relevant commits are `d5c9e2a` (composition), `3b2b34c` (memory,
inverse fibers, and repeat-budget tests), and `7bac13d` (phase rank, reset
law, and rank obstructions). The unrelated P2 working files remain
uncommitted.

## The open theorem

The missing result is a uniform bound on cumulative switch refill, or another
argument that excludes an infinite aperiodic scalar history while retaining
the full carried frontier history. The current work establishes exact local
dynamics and identifies several insufficient summaries. It does not prove
mortality, P1, or P2.

# Preregistration: signed contact/toggle divergence certificate

Date: 2026-08-31

## Exact target

Prove finite-seed Gray-OR mortality for the alternating Rule 30 frontier, and
hence the period-two same-orbit theorem for every nonzero finite configuration.

## Candidate certificate class

Treat every color contact/switch in the exact four-state carry transducer as a
local operator.  Scanning a frontier word produces one of 16 tiles

```text
(incoming carry, input color-pair, outgoing carry, emitted color-pair).
```

Assign signed integer charges to tile occurrences, input/output contacts, and
the two terminal boundaries.  Search for an exact discrete-divergence identity
or inequality whose internal charges telescope over an arbitrarily wide
macro pyramid.  The remaining boundary flux must be bounded below on every
finite rho-seed and fall strictly on every accepting macrostep.

This implements the proposed left-minus-right count, touching-color count,
and “each pyramid occurrence is an operator” in one fixed formalism.  It does
not reuse causal connected-component counts (already killed in
`RESULTS-followup3-ball-fission-topology.md`) or the memoryless `{f,s}` labels
(already identified with the ladder pin in `RESULTS-followup2-faro-monoid.md`).

The registered feature set is:

- counts of all 16 `(carry,input)` transition tiles;
- counts of the four input colors and four emitted colors;
- counts of equal-color and switched-color contacts in each component;
- signed `A-minus-aligned-B`, black-minus-white, and left-boundary-minus-
  deep-boundary incidences;
- free bounded endpoint charges on the four initial and terminal carries.

Use integer coefficients in `[-16,16]`.  A bounded-below weighted transducer
may be normalized so every directed cycle has nonnegative weight; endpoint
potentials account for the normalization.

## Strong outcome

A strong outcome is a complete 16-tile table and endpoint inequality that can
be checked entry-by-entry, followed by a telescoping proof for every word
length.  Strict loss on every accepting macrostep, with no normalized density
or tested horizon in the proof, would establish mortality uniformly.

## Kill conditions

Stop and record a negative if:

- an exact reachable transition increases the proposed signed/ranked charge;
- a finite Farkas multiset of reachable transitions cancels all endpoint and
  signed incidences while making every bounded-below tile count nonnegative;
- the only feasible charge is a coboundary/endpoint term or is unbounded below
  as the frontier grows;
- carry/action permutations create a zero-charge accepting cycle in the local
  operator graph;
- closure requires pyramid size, support width, or a growing time prefix;
- the argument reduces to the previously killed connected-component,
  column-overwrite, periodic-mask defect, or ladder constructions.

Report the smallest exact transition/multiset and which of signed imbalance,
touching colors, and pyramid-tile charge it kills.

## Controls

- Rule 90 `{-1,1}` must remain a period-two collision; replacing OR by XOR in
  the complete tile table must not yield the claimed Rule 30 descent.
- Rule 30 `{-8,-1,6}` alternates through time 14 and fails at 15.
- Re-run all 16 carry tiles, 32 `F^2` neighborhoods, 64 defect assignments,
  and the 131,071-row radius-eight control.
- Candidate local identities are checked on every tile; reachable transitions
  through seed length 16 and follow 128 are falsifiers only.

## Resource limits

- local CPU only; no agents, SAT spacetime grids, GPU, Modal, or paid calls;
- 16 tile weights, the registered contact/incidence features, coefficients
  `[-16,16]`, at most 64 endpoint charges;
- at most 15 minutes and 2 GiB per command, 30 minutes total synthesis;
- stop rather than add wider windows or more pyramid layers after a kill.

## Why success would be uniform

The tile alphabet and carry set are fixed.  Summing a proved local divergence
over any finite word cancels every internal edge regardless of width, leaving
only fixed endpoint flux.  Therefore a strict accepting-step loss would apply
to arbitrarily large finite supports and arbitrarily many macrosteps.

# Preregistration: run-length / boundary-gap certificate

Date: 2026-08-31

## Exact target

Prove that every finite rho-seed under the alternating Rule 30 macro map
eventually fails `D_1=1`, hence exclude the nonconstant period-two same-orbit
collision for every nonzero finite configuration.

## Candidate certificate class

Encode each finite Boolean word by its starting color and the lengths of its
maximal monochromatic runs.  Equivalently, encode it by the ordered gaps
between its Gray-boundary positions.  For

```text
g(X) = X XOR (X >> 1),
```

the exact macro equations are

```text
g(C) = A OR (1 + zB),
g(D) = C OR zA.
```

Thus the run boundaries of `C` and `D` are the unions on the right, and the
run lengths are the gaps between consecutive union positions.  The pin passes
exactly when the second union has odd cardinality.

The candidate is a fixed symbolic transducer or well-founded ranking on these
colored run-length compositions.  It may use a constant number of current run
lengths, comparisons, and a signed residual between the two merged boundary
streams, but it may not retain the complete composition or a residual whose
range/state grows with word length.  Candidate ranks include exact run count,
first/last run, minimum gap, and lexicographic gap compositions from the deep
boundary.  Every claimed monotonicity or forbidden merge pattern must be
checked exactly.

## Strong outcome

A strong outcome is a finite-state merge rule or a well-founded composition
order, independent of the number and sizes of runs, that proves an accepting
orbit must contain run boundaries at unbounded initial spatial depth.  The
proof must retain the finite rho-seed language and Rule 30's two support
unions.  Tested word length cannot occur in the proof.

## Kill conditions

Stop and record a negative if:

- merging the two boundary streams requires an unbounded cumulative-position
  residual, so the proposed state is merely the raw word in run-length form;
- an exact reachable transition increases or cycles the proposed run/gap
  ranking;
- two exact finite-seed states have the same registered bounded run summary
  but incompatible next pin or successor summary;
- the argument assumes the rejected claim that a periodic OR mask contracts
  every defect;
- the number of retained runs grows with support width or survival time.

Report the smallest exact counterexample and distinguish failure of a bounded
run summary from failure of full run-length encoding, which is lossless.

## Controls

- Rule 90 `{-1,1}` remains a period-two collision; replacing both unions by
  symmetric differences must not yield a false contraction proof.
- Rule 30 `{-8,-1,6}` alternates through time 14 and fails at 15.
- Re-run the complete local Rule 30 tables and radius-eight global control
  before promoting any theorem.
- Exhaustively cross-check bit-word and run-boundary reconstruction for all
  words through length 16, and the two macro sweeps for all legal frontiers
  through `T=8`.
- Use finite rho seeds through length 16 and 128 forced steps only to falsify
  candidate summaries.

## Resource limits

- standard-library local CPU only; no agents, SAT grids, GPU, Modal, or paid
  calls;
- bounded summary: at most four runs at either endpoint, residual magnitude
  at most 32, at most 65,536 states;
- at most 15 minutes and 2 GiB per command; stop rather than enlarge a bound.

## Why success would be uniform

Run lengths are symbolic positive integers.  A fixed merge transducer or
well-founded order proved for arbitrary positive lengths would scan any finite
composition with the same rule, regardless of support width.  Exhaustive
enumeration would validate only the finite local obligations, not the theorem.

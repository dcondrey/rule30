# Preregistration: bilateral hard-core rho constraint

Date: 2026-08-31

## Exact theorem target

Prove that no nonzero finite Rule 30 configuration has center trace
`0101...`; the `1010...` phase then reduces to it by applying `F` once.
Equivalently, prove `Tr_0(y) != Tr_0(F^2(y))` for every nonzero finite `y`,
using the already-proved constant-trace exclusions for the other two phases.

## New retained hypothesis

The earlier alternating-fiber frontier allowed an arbitrary sequence

```text
rho_k = s(2k,1).
```

An actual right half-plane obeys Rule 30 at column 1.  With
`c_(2k)=0`, `c_(2k+1)=1`, and `q_t=s(t,2)`, the candidate exact identity is

```text
rho_(k+1) = (NOT rho_k) AND (NOT q_(2k)) AND (NOT q_(2k+1)).
```

In particular, an actually realizable `rho` has no adjacent ones.  This
uses Rule 30's OR and the second spatial column, so it is not an arbitrary
half-plane witness or a generic left-permutive argument.

## Candidate certificate class

Intersect the exact finite-rho-seed language of the reverse Gray-OR macro
with the fixed two-state hard-core language `no 11`.  Treat every such rho
word as a concatenation of blocks `0` and `10` (with an optional terminal
`1`).  Search for a fixed-state induction under those block generators:

- a universal constant bound on post-seed accepting macrosteps; or
- a finite set of symbolic frontier cones closed under appending `0` and
  `10`, each with an exact well-founded exit rank; or
- an exact forbidden carry/boundary-gap suffix forced by every sufficiently
  long hard-core seed.

Any proposed state must have fixed cardinality independent of rho length,
left depth, right support, and time.  Full frontier words may be used only to
discover or falsify such a state.

## Strong outcome

A strong outcome is a local proof of the displayed right-column identity and
a finite transition table/induction proving that every hard-core finite rho
seed eventually fails a pin.  The proof must explain why every finite right
half produces a hard-core rho and why every finite left half is represented
by the seed frontier.  This would be a uniform period-two theorem, not a
finite-prefix exclusion.

## Kill conditions

Stop and record a negative if any of the following occurs:

- the displayed identity fails one of its complete Boolean assignments;
- the adversarial Rule 30 row violates the hard-core condition before its
  actual alternating-trace failure;
- post-seed survival among hard-core seeds grows with seed length rather than
  having a universal bound;
- two hard-core seeds collide in a proposed fixed summary but have opposite
  next pins;
- closure requires adding a longer rho suffix, frontier window, support
  width, or time lookahead;
- the argument reduces to the existing arbitrary-rho frontier, fixed-depth
  ladder, or false periodic-OR-mask contraction.

If killed, report the smallest exact hard-core seed and structural reason.

## Controls

- Exhaustively check the right-column identity on all relevant Boolean
  values and show exactly which OR implication fails when OR is replaced by
  Rule 90's XOR.
- Rule 90 `{-1,1}` must retain its constant-zero center trace.  This
  hard-core lemma concerns the nonconstant phase and must not be used to
  reproduce the Rule 30 constant-zero exclusion generically.
- Rule 30 `{-8,-1,6}` must satisfy the derived constraint through the last
  complete alternating macro and must not be rejected before time 15.
- Re-run the 16 carry tiles, 32 `F^2` neighborhoods, 64 defect assignments,
  and all 131,071 nonzero radius-eight rows through the registered horizon.
- Test every proposed local transition on its complete Boolean table and
  test every global summary on all hard-core rho seeds through length 16
  before attempting an induction.

## Fixed limits

- seed length at most 16 and at most 128 forced continuations, used only for
  falsification/discovery;
- at most 256 candidate summary states and coefficient magnitudes at most 16;
- at most 10 minutes and 2 GiB per command, 30 minutes total;
- local CPU only; no SAT spacetime grids, agents, GPU, Modal, paid calls, or
  enlarged finite-horizon searches.

## Why success would be uniform

The hard-core language has the fixed generators `0` and `10`.  A proved
finite induction closed under both generators covers rho words of every
length.  Coupling it to the exact length-free Gray-OR carry transducer would
leave no tested support or time parameter in the conclusion.

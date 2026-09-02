# Preregistration: all-length phase-gap cover proof

Date: 2026-09-01

## Discovery boundary

The registered held-out phase-gap matching passed through length 16.  A
post-hoc reduction then showed that retreat times are nonconsecutive and that
the only possible matching obstruction is a retreat whose current and
preceding queues are both zero-free.  Exploratory automata identified the
candidate zero-free predecessor language and found an empty second
preimage.  The proof checks below are frozen before writing the permanent
checker.

## Claims to prove

1. A successful retreat is exactly a queue ending in `1` whose raw scan ends
   in state `0`.  Therefore the successor ends in `02`, and two retreats
   cannot be consecutive.

2. If `p -> q` is a successful queue step, both `p` and `q` are zero-free,
   and `q` retreats on its next step, then the tail is `2` and

   ```text
   p in P = 211 ([12]1[12]1)*,
   q in (2121)+.
   ```

   Because the displayed exponent in `P` is a four-symbol block, the image
   actually has length divisible by four.

3. Construct a literal DFA for the suffix language of `P`.  Apply the exact
   sequential queue-preimage construction twice, intersecting with the
   invariant queue language at each step.  The expected minimized sizes are

   ```text
   P:          6 states, nonempty,
   Q^-1(P):   20 states, nonempty,
   Q^-2(P):    1 dead state, empty.
   ```

4. Cross-check the first preimage and the empty second preimage by an
   independently constructed synchronous product, rather than relying only
   on the generic DFA minimizer.

5. Conclude that a retreat with no zero block in its current or preceding
   row must be the first retreat of the orbit.  Since distinct retreat times
   have disjoint event windows `{t-1,t}`, one boundary credit plus one
   arbitrary zero block from every other window gives an injective matching.

## Scope

This proves the phase-gap cover only.  It does not prove that a fixed initial
queue generates finitely many phase gaps.  That event-creation/ancestry bound
remains necessary for `d(r) -> infinity`.

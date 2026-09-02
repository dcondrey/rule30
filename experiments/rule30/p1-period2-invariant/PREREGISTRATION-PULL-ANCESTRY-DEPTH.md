# Preregistration: pull ancestry depth

Date: 2026-09-01

## Discovery boundary

The all-length suffix theorem and pull-ray stabilization imply a natural
parent forest.  Give every initial coordinate its own root.  In each queue
update, make the newly appended coordinate a child of the rightmost colex
pivot; inherited coordinates retain their nodes.  Label a parent edge by
`C` exactly when its update is a pull, and let a node's pull depth be the
number of `C` edges on its root path.

The construction and the two claims below were formulated after the frozen
pull-ray corpus had already been analyzed, but before this new annotation
was run on exact length 19 or on a new random/sparse corpus.  The older
pull-ray result therefore counts only as discovery data for this claim.

## Frozen claims

Let the pulls be indexed chronologically from zero, with times `t_i` and
newly appended nodes of depths `h_i`.

1. The depths obey

   ```text
   h_i = h_(i-1)+1                 if t_i-t_(i-1) >= 3,
   h_i = h_(i-2)+1                 if t_i-t_(i-1) = 2,
   ```

   with missing earlier depth interpreted as zero.  In particular,

   ```text
   h_i >= floor(i/2)+1,
   number of pulls <= 2 max_i h_i.                         (AD1)
   ```

2. If a pull node has initial root coordinate `r` and pull depth `h`, then

   ```text
   h <= number of initial feature starts at coordinates <= r.             (AD2)
   ```

   A feature start is a nonleading symbol `1` or the first coordinate of a
   maximal zero run, exactly as in the earlier mixed-budget registrations.

Together `(AD1)` and `(AD2)` imply

```text
number of pulls <= 2 (#1 + #zero-runs) <= 2 |R|.
```

This weaker constant-two bound is already sufficient: every finite queue
has finitely many pulls and hence finitely many retreats.

## Held-out gates

1. Exhaust every invariant normalized queue of length 19.
2. Run 50,000 newly seeded random queues per tail at lengths
   `24,32,48,64,96`.
3. Run 50,000 newly seeded sparse queues per tail at lengths through 128.
4. Reject the claim on the first depth-recurrence or feature-prefix failure.

Passing is finite evidence only.  `(AD1)` should then be proved directly
from the three suffix rewrites and coordinate arithmetic.  The sole live
proof obligation would be `(AD2)`, a one-chain feature-depth inequality
rather than a Hall matching across all pull branches.

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

## Strengthened invariant registration

After the preceding held-out run passed, the exact raw-state annotation
suggested the following stronger inductive form.  It was checked on every
invariant queue through length 16, but has not been checked at length 17 or
above, nor on a new random corpus:

> For every current coordinate whose ancestry root is a positive initial
> coordinate `r`, if its pull depth is `h` and its current unnormalized raw
> state is `s`, then
>
> ```text
> h + [s=3] <= number of initial feature starts at coordinates <= r.       (AD3)
> ```

The leading one-symbol tail-2 orbit is excluded by `r>0`; it has no bottom
feature and creates a harmless nonproductive state-1 child.

Claim `(AD3)` directly implies `(AD2)`.  An initial time-zero pull pivots at
an initial symbol `1`, which is itself a feature.  Every later pull pivots at
raw state `3` by the proved retreat/pull suffix theorem, so `(AD3)` supplies
the strict unit of slack consumed by the new `C` edge.

The strengthened held-out gate is every invariant queue of length 17,
followed by 100,000 newly seeded random and 100,000 newly seeded sparse
queues per tail across lengths through 128.  Passing remains finite evidence;
the proof target is preservation of `(AD3)` by the exact marked raw scan.

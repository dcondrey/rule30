# Preregistration: stabilized pull ray and bottom-feature crossings

Date: 2026-09-01

## Discovery boundary

The exact suffix rewrite theorem reduces every nonfirst retreat to a
productive pull

```text
1 0^m 2 -> 0^(m+1) 2 1.
```

For a pull at update time `t`, let `p` be its rightmost colex-pivot
coordinate and put `d=p-t`.  On every invariant queue through initial length
18, the following stronger geometric statement held.  It has not been
tested at length 19 or on a new random corpus.

## Frozen claim

Let the pull events be `(t_i,p_i)`, in time order.

1. If there are at least two pulls, then

   ```text
   p_i-t_i = p_2-t_2                 for every i>=2.       (PR1)
   ```

   Thus only the first pull can change the characteristic ray.

2. Put `d*=p_2-t_2` when a second pull exists and `d*=p_1-t_1` when there is
   exactly one pull.  Then

   ```text
   number of pulls
     <= number of initial feature starts at coordinates <= d*.             (PR2)
   ```

Here an initial feature start is a nonleading `1` coordinate or the first
coordinate of a maximal zero run, exactly as in the mixed-budget and
origin-Hall registrations.

Since `d*` is an initial-coordinate intercept, `(PR2)` implies the mixed
budget without requiring the stronger per-origin Hall statement.

## Held-out gates

1. Exhaust every invariant normalized queue of length 19.
2. Run 50,000 newly seeded random queues per tail at lengths
   `24,32,48,64,96`.
3. Run 50,000 newly seeded sparse queues per tail at lengths through 128.
4. Replay the length-34 raw-`#1` counterexample and the length-18
   six-retreat witness.

Any change of characteristic after the second pull or any feature deficit
kills the corresponding claim.  Passing remains finite evidence.

## Proof target if it passes

Use the three all-length suffix rewrites to expose the space-time ray
`i-t=d*`.  Prove first that the wedge to its right is forced after the
second pull, giving `(PR1)`.  Then scan the bottom prefix through `d*` into
maximal zero blocks and individual `1` cells, and construct a noncrossing
backward path from each pull on the ray to a distinct such bottom feature.
This planar ray statement is strictly weaker than origin-prefix Hall but is
already sufficient: pulls bound retreats, so every finite queue has only
finitely many retreats.

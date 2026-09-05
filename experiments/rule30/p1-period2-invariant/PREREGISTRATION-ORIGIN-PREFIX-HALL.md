# Preregistration: colex-origin prefix Hall inequality

Date: 2026-09-01

## Discovery boundary

The mixed retreat budget

```text
ret(R) <= number of nonleading 1 cells + number of maximal zero runs
```

passed its registered held-out length-19 and random/sparse gates.  In trying
to expose an ancestry map, the following stronger ordered statement was
discovered and checked on every invariant normalized queue through length 18
and on the two stored retreat controls.  It has not been tested at length 19
or on a new random corpus.

## Frozen origin labelling

Give initial queue coordinate `i` origin `i`.  On every successful update,
strict colex descent supplies the rightmost inherited coordinate `p` at which
the normalized scan differs from its input.  The input at `p` is necessarily
`1`.  Give the newly appended boundary coordinate the same origin as `p`.
All inherited coordinates retain their origins.

For the exceptional one-symbol tail-2 update, there is no inherited
difference; give its appended nonretreating boundary origin zero.  It cannot
affect the claim.

An initial **feature start** is either

1. a nonleading coordinate containing symbol `1`; or
2. the first coordinate of a maximal zero run.

For each retreat, record the origin of its colex pivot.

## Frozen claim

If the retreat origins in nondecreasing order are

```text
o_1 <= o_2 <= ... <= o_r,
```

then for every `1 <= k <= r`,

```text
number of initial feature starts at coordinates <= o_k  >= k.       (OH)
```

Equivalently, for every initial coordinate cutoff `j`, the number of retreats
whose pivot ancestry has origin at most `j` is at most the number of initial
feature starts at most `j`.  Taking `j` at the end of the initial word gives
the mixed retreat budget immediately.

## Held-out gates

1. Exhaust every invariant normalized queue of length 19.
2. Run 50,000 deterministic random queues per tail at lengths
   `24,32,48,64,96`.
3. Run 50,000 deterministic sparse queues per tail at lengths through 128.
4. Replay the length-34 raw-`#1` counterexample and the length-18 six-retreat
   witness.

Any failed prefix inequality kills `(OH)`.  Passing remains finite evidence.

## Proof target if it passes

Construct the greedy noncrossing matching that assigns each retreat, in
nondecreasing origin order, to the rightmost unused initial feature start no
larger than its origin.  The finite-state colex theorem already proves that
every pivot is an input `1`; the missing symbolic step is to show that a
boundary lineage cannot request its `(k+1)`-st retreat before the prefix that
feeds it has exposed a `(k+1)`-st initial feature.

A proof of `(OH)` proves the mixed budget, hence `d(r) >= r`.  Together with
the proved eventually-`2` exceptional separator, this closes the
constant-tail separator, rank-zero separator, and nonconstant period-two
exclusion.

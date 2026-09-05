# Preregistration: bit-sliced scale derivative validation

## Purpose

Validate the fixed pivot selector obtained from the length-1..16 derivative
audit on a new exhaustive horizon, using an independent bit-sliced
implementation of all one-source interventions.

The selector is frozen as

```text
tail 2, forced 1: alpha
tail 2, forced 2: beta
tail 3, forced 1 or 2: alpha.
```

For every hard-core word and every prefix of its hard-core forced scale
continuation, the validation target is

```text
rank(selected derivative rows) >= prefix length - K,
K_2=indicator(22 occurs), K_3=3.
```

## Independent bit-sliced implementation

Scenario bit zero is the original source word.  One further scenario bit is
allocated for each source coordinate containing state 2; in that scenario
only that state is changed to 1.  State high and low bits are propagated as
integer bitsets using the exact identities

```text
activity(l) = high(l) OR low(l),
high(phi(l,r)) = high(r) XOR activity(l),
low(phi(l,r)) = low(r) XOR ((1 XOR low(l)) AND high(r))
                XOR activity(l).
```

The newest affine map is composed in bit slices.  Its forced preimage of cut
tail `c` is

```text
high(q)=1 XOR alpha,
low(q)=low(c) XOR (beta AND high(q)) XOR gamma.
```

This implementation may not call the slow per-intervention trace constructor
inside its primary census.

## Frozen controls and horizons

- exhaustive slow/bit-sliced equality for every hard-core word through
  length 7 and both tails, including every affine derivative row and every
  forced scenario trajectory;
- exhaustive validation on lengths 17 through 22;
- recheck the length-17 repair witness explicitly;
- deterministic random validation: 1,000 hard-core words at each length
  24, 32, 48, and 64 from seed `30030`;
- both tail modes;
- direct and incremental `F_2` ranks must agree on the controls.

The previously used lengths 1 through 16 are not counted as held-out
validation, though the cross-check necessarily touches lengths through 7.

## Outcomes

One negative prefix slack kills the fixed selector.  A bit-sliced mismatch
kills the fast implementation and invalidates all results above the control
horizon.

Passing is still finite evidence, not a proof.  It promotes the fixed
selector to the next all-length lemma only if the implementation controls
pass exactly.  The remaining proof obligation would be a recurrence showing
that the selected-row nullity is bounded by one in tail 2 and by three in tail
3.

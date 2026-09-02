# Preregistration: pull ancestry coordinate depth

Date: 2026-09-02

## Discovery boundary

The previously registered feature-prefix bound is false.  The invariant
tail-3 queue

```text
30000000000000000000000000000001000000000000000000000000000000000000000000002
```

has event word `CBACACBACBA`, and its pull at time 8 has initial root 31,
feature-prefix budget 2, and new pull depth 3.  This is a literal
counterexample to `(AD2)` and therefore also to the stronger raw-reserve
claim `(AD3)`.  It was found by exhaustively targeting queues with few
features and long zero runs, after the earlier held-out corpus had passed.

The failure identifies an exact mismatch between two surviving approaches.
The ancestry attempt discarded most zero coordinates, whereas the
zero-prefix greedy/scale attempt assigns one token to every source
coordinate.  This motivates the following coarser geometric claim.

Before this registration, the claim passed every invariant queue through
length 18, the displayed feature counterexample, and newly seeded random and
sparse discovery samples at lengths 24 and 32.  Those runs are discovery
data only.

## Frozen claim

Give initial coordinate `r` capacity

```text
K(r) = ceil(r/2) = (r+1)//2,   r>0.
```

Use the existing parent forest: an `A` or `B` child inherits its parent's
pull depth, while a `C` child has depth one larger.

> **Coordinate-depth claim `(CD)`.** Every successful pull whose appended
> node has initial root `r>0` and pull depth `h` satisfies
>
> ```text
> h <= K(r), equivalently r >= 2h-1.
> ```

Together with the proved temporal recurrence
`#pulls <= 2 max pull-depth`, `(CD)` implies at most `N` pulls for an
initial queue of length `N`.  The proved retreat--pull pairing then makes
retreats finite, and the existing eventual-2 separator proves mortality.
Thus `(CD)` is sufficient to exclude the nonconstant period-two center
trace.

The intended proof object is a nested interval of `2h-1` initial coordinate
tokens ending at `r`.  The first pull consumes one token; every later pull
edge on the same ancestry chain must extend the interval by two tokens.  This
is the parent-forest counterpart of the zero-prefix greedy sweep, whose
surviving coarse scale bound also counts all source coordinates.

## Frozen held-out gates

1. Exhaust every invariant normalized queue of length 19.
2. Exhaust every invariant queue having at most five feature starts through
   length 128; these include adversarial arbitrarily long zero runs at the
   tested lengths.
3. Run newly seeded random and sparse queues at lengths
   `24,32,48,64,96,128,192,256`.
4. Retain the feature-prefix counterexample as a positive control: it must
   fail `(AD2)` at time 8 but pass `(CD)`.

Passing is finite evidence only.  A proof must construct the nested
coordinate interval or identify it with the strictly increasing tokens in
the zero-prefix greedy formulation.  No bounded census may be reported as an
all-length proof.

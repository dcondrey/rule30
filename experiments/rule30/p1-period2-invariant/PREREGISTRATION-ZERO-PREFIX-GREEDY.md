# Preregistration: greedy zero-prefix matching

## Frozen algorithm and claim

Use the zero-prefix change graph from
`PREREGISTRATION-ZERO-PREFIX-SCALE-MATCHING.md`.  Process survival steps in
time order.  Match the current step to the least token larger than the
previously matched token that is adjacent to it.  If no such token exists,
leave the step unmatched.  No backtracking or lookahead is allowed.

The target is

```text
tail 2: zero unmatched steps,
tail 3: at most one unmatched step.
```

This is stronger than existence of an ordered matching and directly implies
`s_2(W)<=|W|` and `s_3(W)<=|W|+1`.

## Frozen validation

- slow audit of all hard-core words through length 16;
- independent bit-sliced audit of lengths 17 through 22;
- slow/bit-sliced graph equality through length 7;
- the tail-3 sharp word, tail-2 repair word, and length-21 derivative
  adversary;
- every selected token must be a graph edge and token indices must be strictly
  increasing.

This strengthening was proposed after the optimal zero-prefix matching had
already passed through length 22, but before greedy outcomes above length 12
were computed.

## Interpretation

A single excess miss kills the greedy theorem while leaving optimal matching
and the coarse numerical bounds open.  Passing is finite evidence.  A proof
would need to show that after taking the earliest change token, the suffix
problem embeds in the next zero-prefix scenario; the unique tail-3 miss is a
boundary initial condition.

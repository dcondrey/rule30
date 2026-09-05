# Preregistration: greedy cumulative matching

## Target

Use the proved-by-audit left-to-right cumulative intervention graph.  Process
survival steps from earliest to latest.  At each step, match it to the least
chain token strictly larger than the previously matched token that is adjacent
to the step.  If none exists, leave the step unmatched.  No backtracking or
lookahead is allowed.

The frozen claim is

```text
number of unmatched survival steps <= K,
K_2=indicator(22 occurs in W), K_3=3.
```

Equivalently, greedy matches at least `s-K` steps.  This is stronger than the
previous existence of an order-preserving matching.

## Frozen validation

- both tails and all hard-core words through length 22;
- bit-sliced/slow cumulative-graph equality through length 7;
- the length-17 repair witness and length-21 derivative adversary;
- the greedy token sequence is asserted strictly increasing and every chosen
  edge is replayed from the graph.

The lengths are no longer a held-out set; this is a post-result strengthening
test, preregistered before computing greedy outcomes.

## Interpretation

One word with more than `K` greedy misses kills the greedy strengthening but
does not kill the already observed optimal ordered matching.  Passing remains
finite evidence.  Its proof value would be a deterministic candidate
induction: show that the earliest available token cannot advance past all
remaining source-2 tokens more than `K` times.

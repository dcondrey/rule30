# Preregistration: tail-3 final-miss placement

## Strengthening

For the deterministic zero-prefix greedy algorithm, the audit through length
12 found that every tail-3 miss, when present, is the final row of the
hard-core survival prefix.  Freeze the stronger claim:

> In tail 3, every nonfinal surviving row is greedily matched.  The final
> surviving row may be the unique miss.

Tail 2 retains the zero-miss claim.

## Validation

- every hard-core word through length 22, both tails;
- independent bit-sliced graph with slow equality through length 7;
- the three registered sharp/adversarial words;
- record the first nonfinal miss, not only the total miss count.

This is a post-result strengthening preregistered before outcomes above
length 12 were computed.

## Interpretation

A nonfinal tail-3 miss kills only this placement claim.  Passing remains
finite evidence.  Its proof value is the local formulation it permits: as
long as the next forced endpoint symbol is also hard-core legal, the current
row must have a change token strictly to the right of the preceding greedy
token.

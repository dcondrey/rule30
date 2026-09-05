# Preregistration: ordered scale matching

## Question

Can the two surviving scale-charge conjectures be strengthened from a
numerical count into a checkable ancestry certificate?

For a nonempty hard-core word `W`, let `R_c(W)` be the exact forced scale
block from `constant_tail_scale.py`, and let `s_c(W)` be the length of its
initial hard-core continuation.  The conjectured bounds are

```text
s_2(W) <= #2(W) + indicator(22 occurs in W),
s_3(W) <= #2(W) + 3.
```

The experiment will ask whether every surviving output position can be
matched injectively either to a state-2 source coordinate or to one of the
stated correction credits.

## Frozen ancestry relation

For each state-2 coordinate `r` of `W`, replace only that symbol by state 1,
recompute the exact constant-tail forced trajectory, and record the affine
`D8` boundary state before every forced endpoint symbol.  Source coordinate
`r` is adjacent to surviving output position `j` exactly when this one-symbol
intervention changes either

1. the affine boundary triple `(alpha,beta,gamma)` at step `j`, or
2. the endpoint symbol forced at step `j`.

The intervention is algebraic and is still defined when the changed source
word is no longer hard-core.  No post-hoc choice of influence relation is
allowed in the registered run.

Correction vertices are adjacent to every surviving output position:

- tail 2: one vertex iff `W` contains `22`;
- tail 3: three vertices.

The certificate is an ordinary maximum bipartite matching covering all
positions `0,...,s_c(W)-1`.  In addition, the audit will report whether an
order-preserving matching exists when source coordinates retain their
spatial order.  Failure of the order-preserving version does not falsify the
ordinary matching target.

## Frozen bounds and controls

- exhaustive hard-core words through length 16;
- both tail modes 2 and 3;
- the known tail-2 repair witness `12212121212121212` is checked separately;
- the sharp tail-3 word `121` is checked separately;
- literal inverse-cone/fast-diagonal agreement through source length 5;
- every recorded affine triple must reproduce its literal four-state newest
  cut permutation;
- every matched non-credit edge must satisfy the registered intervention
  definition when replayed independently.

## Outcomes

Positive evidence requires a covering ordinary matching for every registered
word and both named witnesses.  A compact repeated matching pattern or a
bounded local exchange rule is the desired proof lead.

The proposed intervention matching is killed by a single word whose
registered graph has no covering matching, even if the numerical scale
inequality remains true.  The ordered variant is killed separately by its
first counterexample.

Neither bounded outcome proves the scale inequalities.  A successful run is
useful only if the matching edges admit a uniform local characterization and
an all-length Hall or greedy argument.  A failed run is also informative: it
shows that Boolean one-coordinate sensitivity is not the missing conserved
ancestry and prevents this graph from being mistaken for a proof.

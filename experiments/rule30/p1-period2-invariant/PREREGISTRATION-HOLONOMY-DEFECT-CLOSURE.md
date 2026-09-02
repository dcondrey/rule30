# Preregistration: zero-prefix holonomy-defect closure

## Question

The live projected diagonal-support lemma uses the ordered zero-prefix chain

```text
W^(k)=0^k W[k:n].
```

At forced row `j`, let `A_(j,k)` be the exact newest endpoint-to-cut affine
permutation and define the adjacent `D8` defect

```text
delta_(j,k)=A_(j,k)^(-1) o A_(j,k+1).
```

Before attempting an ordinal rank on these words, determine which proposed
state descriptions actually define a transition from row `j` to row `j+1`.
The audit is solver-free and uses the literal dependency diagonal.

## Frozen state layers

For the active suffix `k>=j`, compare four increasingly informative keys:

1. `defects`: the ordered word of `delta_(j,k)`;
2. `anchored`: `defects` plus the rightmost phase `A_(j,n)`, which exactly
   reconstructs every current affine phase;
3. `boundary`: `anchored` plus the previous endpoint symbol in every active
   zero-prefix scenario;
4. `queues`: the complete reversed dependency diagonal in every active
   scenario.

The successor value is the exact ordered defect word at row `j+1`, after
removing scenario `k=j`.  A layer is not transition-closed if one key has
two distinct successor values.  Record the first replayable collision at
each failed layer.  The complete queue layer is expected to be closed by the
literal local recurrence; failure there kills the implementation.

## Scope and interpretation

Enumerate every hard-core source word through a requested length and retain
only rows required by the mortality reduction: every tail-2 survival row and
every nonfinal tail-3 survival row for which `j<n`.

This audit cannot prove diagonal support or mortality.  It decides whether
the proposed bare `D8` defect word, an anchored word, or a boundary-enriched
word is even a well-defined dynamical state.  A collision rules out an
ordinal descent based only on that layer; it does not rule out an ancestry
rank on the full growing queues.

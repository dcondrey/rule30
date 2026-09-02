# Preregistration: scale derivative rank

## Target

Let `W` be a nonempty hard-core word, let `s=s_c(W)` be its constant-tail
scale survival, and enumerate the coordinates at which `W` has state 2.  For
each such coordinate, intervene by changing that state 2 to state 1 and
recompute the exact forced trajectory.

At every surviving output step, subtract (XOR) the original and intervened
affine boundary coordinates.  For a coordinate set `C` contained in
`{alpha,beta,gamma}`, stack the selected differences into a binary matrix

```text
D_C(W,c): rows (survival step, affine coordinate), columns source-2 positions.
```

The primary registered claim is

```text
rank_F2 D_{alpha,beta,gamma}(W,c) >= s_c(W) - K_c(W),
```

where

```text
K_2(W)=indicator(22 occurs in W),
K_3(W)=3.
```

Because the matrix has exactly `#2(W)` columns, this rank inequality implies
the two desired scale-charge bounds immediately.

The three coordinate pairs and three single coordinates are frozen as
ablations.  A smaller coordinate set may be retained as a proof lead only if
it passes every registered case; the full triple is not replaced after a
failure.

## Frozen computation

- exact Gaussian elimination over `F_2`, using integer bit rows;
- exhaustive hard-core words through length 16;
- both constant cut tails 2 and 3;
- separate checks of the length-17 tail-2 repair witness
  `12212121212121212` and the tail-3 sharp witness `121`;
- trajectories and interventions are those independently controlled in
  `constant_tail_ordered_matching.py`;
- direct rank is cross-checked against a second column-basis implementation
  through length 6.

The report records the first deficiency, minimum slack
`rank-(s-K)`, and maximum nullity for each coordinate set.

## Interpretation

A single negative slack kills that coordinate set.  Passing the finite audit
does not prove the inequality.  A proof still requires an exact recurrence
for the derivative columns and either a uniform triangular minor or a rank
induction under hard-core extension.

The experiment is valuable if the full triple, or a fixed smaller set,
retains the required rank with a visible pivot law.  It is not permissible to
infer the rank bound merely from the previously observed matching graph:
structural rank can be destroyed by cancellations over `F_2`.

# Exact disjoint-cone reduction of a guarded-history MPS

Status: **proved exact representation change**, with a bounded positive
compression result. This does not prove the requested cumulative counting
inequality, finite-frontier mortality, or period-two exclusion.

The [shared-prefix construction](RESULTS-shared-prefix-mps.md) produced a
weighted deterministic representation of a fully guarded temporal message.
The reduction here can replace one such state by a positive combination of
several other states. Consequently, the resulting MPS can have multiple
next states for the same physical symbol. It is no longer restricted to a
weighted deterministic automaton.

## 1. An exact nonnegative row factorization

At one temporal site, flatten a nonnegative integer tensor row over the
coordinates `(physical symbol, child state)`. Divide each nonzero row by
the gcd of its coefficients, and merge identical normalized rows.

Process the distinct normalized rows in increasing support size. For a
row `v`, seek a partition of its support into two nonempty disjoint sets
`L,R` such that the normalized restrictions

\[
 v_L/c(v_L),\qquad v_R/c(v_R)
\]

already occur among the original normalized rows. Both restrictions have
strictly smaller support. If found, use

\[
 v=c(v_L)\,\nu(v_L)+c(v_R)\,\nu(v_R).             \tag{1}
\]

Recursively substitute the previously found expressions for those smaller
rows. If no split is found, keep `v` as a basis row. Zero rows have the
zero expression. Returning the original gcd scales gives

\[
 E_j(x)=C B_j(x)\quad\text{for every physical symbol }x,
 \qquad C\ge0,\ B_j(x)\ge0,                     \tag{2}
\]

with integer entries. The recursion terminates because support size
strictly decreases. Equation (1) is an exact identity on disjoint
coordinates, so it cannot remove a positive coefficient or introduce a
new nonzero coordinate.

Replace the tensor by `B_j` and multiply the preceding tensor by `C` on
the right. At the first site, multiply both left boundary rows by `C`.
The entire MPS function is unchanged, since each product segment satisfies

\[
 E_{j-1}(x)E_j(y)
   =\bigl(E_{j-1}(x)C\bigr)B_j(y).
\]

For a right-to-left sweep, first absorb the final nonnegative boundary
column into the last tensor. This permits one terminal state. Every
subsequent step has the same exact factorization (2). These identities
hold at arbitrary finite temporal depth and preserve both `A0` boundary
values, every guard encoded by the terminal signature, and the original
count.

Searching only some support partitions affects the amount of compression,
not correctness. An unrecognized row is retained exactly. The construction
does not assert that the retained rows form a minimal nonnegative cone or
that all possible positive decompositions have been found.

## 2. Why the experiment needs a shared branching seed

Starting from the terminal guard indicator, the four-bond MPO and a
right-only row quotient preserve point-mass suffix rows. For a fixed MPO
bond, the map from old to new physical symbol is a permutation. A row
accepting one physical symbol therefore continues to accept only one,
and a support-one row has no nontrivial disjoint partition.

The experiment accordingly reconstructs the exact shared-prefix message
after 13 spatial transfers for `alpha=0^22`, then applies **one** conic
sweep. This seed already has states accepting several physical symbols.
No new assertion about the requested length-41 count is needed to test
this representation change.

## 3. Exact bounded result

Verifier: [disjoint_cone_mps.py](../../experiments/rule30/disjoint_cone_mps.py).
Artifact: [disjoint-cone-mps.json](../../experiments/rule30/disjoint-cone-mps.json).

The saved run used 0.099411 seconds. Its limits were 20 seconds, 4,096
states per bond, support at most eight for a split candidate, and 200,000
subset tests. It used 15,789 subset tests including the controls. Rows
outside the tested support class were retained.

The seed and reduced bond dimensions are

\[
\begin{aligned}
\text{before: }&2,6,24,96,384,1082,305,9,2,1,\ldots,1,\\
\text{after: }&2,6,24,96,381,594,9,3,2,1,\ldots,1.
\end{aligned}
\]

Thus the largest bond decreases from **1,082 to 594**. The sweep accepts
793 disjoint row decompositions. In particular, the sixth tensor's input
bond decreases from 1,082 to 594, and the seventh decreases from 305 to
9. The total number of nonzero tensor entries decreases from 5,470 to
4,564.

After the sweep, **497 rows have multiple children for the same physical
symbol**; the seed had none. This verifies that the procedure actually
produces a general nonnegative MPS representation, beyond merging
proportional deterministic suffix states.

The verifier checks all 1,923 flattened-row factor identities and the
terminal boundary identity. It also checks 129 selected column evaluations
before and after reduction. The row identities, rather than the selected
evaluations, establish equality on all columns.

Separate controls include a recursive weighted split, a sparse MPS already
having multiple children for one symbol, and 126 small original-frontier
and tape membership checks against the frozen independent `cert33` engine.
Those oracle controls preserve each chronological guard and cover nine
original-count comparisons at lengths one through three. No large
original-start census or dense temporal graph is constructed.

The length-14 origin count remains zero, as required by exactness. The
experiment does **not** compute `|C_41(0^22)|`, provide an upper bound
meeting its threshold, or establish a uniform bond bound under repeated
spatial transfers. Its positive result is narrower: a certified
nonnegative conic reduction gives a smaller exact representation of a
specific fully guarded message and introduces shared latent branching.

A separate [guarded UNSAT certificate](RESULTS-constant-zero-history-certificate.md)
subsequently establishes `C_41(0^22)=empty`. That count comes from the
checked clause proof, not from this conic sweep.

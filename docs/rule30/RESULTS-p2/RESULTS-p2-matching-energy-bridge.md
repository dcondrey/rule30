# P2: exact matching deficiencies and their relation to coarse energy

Date: 2026-09-11. This addresses the matching omission in the
[audit](AUDIT-p2-overlooked-implications.md). The results below are universal
theorems about sign words. They repair the formulation of the proof target;
they do not establish decay for the singleton Rule 30 seed.

## 1. The exact target involves collections of intervals

Let `z_0,...,z_(N-1)` be a sign word. Fix an integer radius `R>=0`. Let
`U_R` be the minimum number of unmatched positions in an opposite-sign
matching with pair separation at most R. Write P and Q for the sets of
positive and negative positions. For an integer half-open interval
`I=[a,b)` contained in `[0,N)`, define

\[
I^{+R}=[\max(0,a-R),\min(N,b+R)),\qquad
d_+(I)=|P\cap I|-|Q\cap I^{+R}|.
\]

Define `d_-(I)` with P and Q interchanged. Let `F_R` consist of all finite
families of nonempty intervals whose expanded intervals `I^(+R)` are
pairwise disjoint, including the empty family. Then the exact formula is

\[
\boxed{\Delta_\pm(R)=\max_{\mathcal I\in F_R}
       \sum_{I\in\mathcal I}d_\pm(I),\qquad
       U_R=\Delta_+(R)+\Delta_-(R).}
\tag{1}
\]

Here `Delta_+` and `Delta_-` are the unmatched counts on the respective
sides of any maximum matching. In particular
`Delta_+-Delta_-=sum z`.

**Proof.** For the distance graph, the usual deficiency identity is
`Delta_+=max_(X subset P)(|X|-|Gamma(X)|)`. To see the upper bound without
assuming the identity, take alternating reachability from all unmatched
positive vertices of a maximum matching. No reached negative vertex is
unmatched, since that would give an augmenting path. Every reached
negative is paired to a reached positive. The reached set therefore has
deficiency exactly the number of unmatched positives. Conversely, every
matching must leave at least `|X|-|Gamma(X)|` positives unmatched for every
X.

For any interval family in (1), take all positive positions in its
intervals. Their actual neighbors are contained in the disjoint expanded
intervals, so its deficiency is at least the sum in (1).

For the opposite inequality, take a maximizing positive subset X. Cluster
its positions according to intersecting clipped radius-R neighborhoods.
Each cluster's neighborhood union is an integer interval. Its endpoints
are the expanded endpoints of the hull I of its positive positions.
Adding any omitted positive position inside this hull introduces no new
neighbors, and could only increase deficiency. Thus a maximizing X can
be filled inside every hull. Distinct clusters have disjoint expanded
hulls, and their deficiencies add. This gives a family attaining Delta_+.
The argument for negatives is identical. This proves (1).

One may merge adjacent expanded intervals as well; no conclusion depends
on that convention. The empty family accounts for zero deficiency.

## 2. A largest single deficit needs a packing factor

Put `D_+(R)=max(0,max_I d_+(I))`, and similarly for negatives. Disjoint
expanded intervals have centers separated by at least `2R+1`. More
precisely, if one interval ends at position b and the next starts at c
using inclusive endpoints, then `c-b>=2R+1`. Consequently every family
has at most

\[
K_{N,R}=1+\left\lfloor\frac{N-1}{2R+1}\right\rfloor
\]

members. Equation (1) gives the valid single-interval substitute

\[
\boxed{U_R\le K_{N,R}\bigl(D_+(R)+D_-(R)\bigr).}
\tag{2}
\]

For a radius schedule `R_k>=1`, `R_k=o(N_k)`, an actual seed theorem

\[
D_+(R_k)+D_-(R_k)=o(R_k)
\tag{3, unproved for the seed}
\]

would therefore suffice for P2. The radius must be specified or obtained
from an independently proved seed property; choosing it from the unknown
discrepancy bound does not prove (3). Equation (3) is a stronger, usable
sufficient target, not a newly proved estimate or an asserted necessary
condition for a prescribed radius.

By contrast, proving only `D_++D_-=o(N)` is insufficient. The word
`++++----++++----++++----`, with R=1, has `D_+=D_-=3` but
`Delta_+=Delta_-=7`, hence U=14. The maximizing positive family can use
the three positive runs, with deficits 3, 2, and 2. Repeating this example
keeps each largest single deficit bounded while the total deficiency
grows linearly with N. This is why a single favorable neighborhood bound
cannot silently replace the collection quantifier.

## 3. Matching and coarse energy convert into one another

Partition the word into K equal blocks of length L, where `L|N`. Set

\[
b_a=\sum_{t=aL}^{(a+1)L-1}z_t,\qquad
E_L=\sum_{a=0}^{K-1}b_a^2,\qquad V_L=\frac{E_L}{NL}.
\]

Then, for every R,

\[
\boxed{\frac{U_{L-1}}N\le
       \frac1N\sum_a|b_a|\le\sqrt{V_L},}
\tag{4}
\]

\[
\boxed{V_L\le\frac{U_R}{N}
          +\frac{2R(N-L)}{NL}
       \le\frac{U_R}{N}+\frac{2R}{L}.}
\tag{5}
\]

**Proof of (4).** Pair opposite signs inside each block. Every pair has
distance at most L-1; exactly `|b_a|` positions remain in block a.
Cauchy--Schwarz proves `sum|b_a|<=sqrt(K E_L)=N sqrt(V_L)`.

**Proof of (5).** Fix an optimal radius-R matching. The imbalance in a
block is contributed only by unmatched positions and endpoints of pairs
that cross a block boundary. At a particular boundary there are at most
R crossing pairs: their left endpoints lie among its preceding R integer
positions. Counting crossing edges at all K-1 boundaries, possibly more
than once, gives

\[
\sum_a|b_a|\le U_R+2R(K-1).
\]

Since `|b_a|<=L`, `E_L<=L sum|b_a|`. Division by NL proves (5).

Another useful version is

\[
\sqrt{V_L}\le\sqrt{U_R/N}+2R/L.
\tag{6}
\]

Indeed, let u_a count unmatched positions in block a, and c_a count
matched endpoints whose partners lie outside it. Then
`|b_a|<=u_a+c_a`, `sum u_a=U_R`, `sum u_a^2<=L U_R`, and
`c_a<=2R`. The last bound follows because such an endpoint lies within
R of a block boundary. The triangle inequality for the Euclidean norm
gives (6). Neither (5) nor (6) is uniformly sharper than the other.

These bounds establish the relationship without inserting the maximum
prefix discrepancy M into the conversion:

* If `V_(L_k)->0` with `L_k=o(N_k)`, (4) gives sublinear matching loss at
  `R_k=L_k-1`.
* If `U_(R_k)/N_k->0` with `R_k=o(N_k)`, choose a dyadic length L_k
  within a factor of two of `sqrt(N_k max(R_k,1))`. Then `L_k/N_k->0`
  and `R_k/L_k->0`, so (5) gives `V_(L_k)->0`.

The dyadic shell permits these lengths to divide N. For finitely many
small shells the choice is immaterial.

**Consequence:** with flexible sublinear scales, matching and the existing
coarse-energy criterion are equivalent certificate families. They should
not be counted as independently established seed mechanisms. Matching
can still be a useful representation for a dynamical argument if that
argument controls deficiencies more directly than it controls energy.

## 4. No universal preset sublinear radius can capture every balanced word

The audit's square-root counterexample generalizes. Fix *any* integer
radius schedule `R_k=o(N_k)`, `N_k=2^k`. Choose a dyadic run length H_k
within a factor of two of `sqrt(N_k max(R_k,1))`. For all sufficiently
large k, `H_k=o(N_k)`, `R_k/H_k->0`, `H_k>=2R_k`, and `2H_k` divides
N_k. Fill shell k with alternating positive and negative runs of length
H_k. Each shell has zero total sum and maximum prefix H_k. The assembled
infinite sequence therefore has limiting sign mean zero.

Every opposite pair of distance at most R_k must cross a run boundary.
There are `N_k/H_k-1` such boundaries, and at most R_k disjoint pairs
can cross any one. Matching the R_k adjacent positions on each side
at distance R_k attains that bound simultaneously at all boundaries,
since `H_k>=2R_k`. Thus

\[
\boxed{U_{R_k}=N_k-2R_k(N_k/H_k-1)=(1-o(1))N_k.}
\tag{7}
\]

This example is not Rule 30. It does not disprove any radius schedule for
the singleton seed. It proves that a fixed schedule adds substantive
seed content and cannot be justified from P2 alone. The same construction
shows why a predetermined sublinear coarse block scale may miss all the
cancellation even though the density conclusion holds.

## 5. Repaired proof obligation and verification

The noncircular use of matching is now explicit: derive from Rule 30's
singleton initial condition a radius schedule and a bound on the *total*
Hall deficiency in (1), or the stronger packed estimate (3), with radius
and loss both sublinear in the shell. The universal identities prove the
implication. They do not supply that dynamical estimate. Equations (4)--(6)
also explain when a proposed matching theorem is merely a coarse-energy
bound expressed differently.

[Verification code](../../experiments/rule30/p2_matching_energy_bridge.py)
uses exhaustive graph matching independent of the queue algorithm, and
weighted interval scheduling over every integer interval to check the
collection formula. It checks every nonempty sign word through length
10, all radii from 0 through N, and all block lengths dividing N. The
[output](../../experiments/rule30/p2-matching-energy-bridge.json) also
records the collection counterexample and delayed-cancellation controls.
Run:

```sh
uv run python experiments/rule30/p2_matching_energy_bridge.py
```

These are controls for the universal statements. No Rule 30 payload is
used and no new seed measurement or asymptotic decay is claimed.

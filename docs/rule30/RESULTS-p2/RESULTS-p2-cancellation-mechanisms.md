# P2: weighted sign diversity and exact matching obstructions

Date: 2026-09-10. **P2 remains open.** This continuation tests proof mechanisms
suggested by the [five-science exploration](RESULTS-p2-five-science-explorations.md).
It supplies an elementary sufficient certificate for delayed contrast,
proves that the distance-limited queue already finds an optimal matching,
and extracts a directly countable obstruction in the actual seed data.
There is still no all-scale seed estimate.

Audit update, 2026-09-11: [omitted implications and scope corrections](AUDIT-p2-overlooked-implications.md)
prove that freely optimized matching is equivalent to discrepancy and show
why cancellation may require blocks much larger than sqrt(N). The fixed
cutoffs below are sufficient targets, not necessary features of P2.
The [subsequent repairs](RESULTS-p2-gap-repairs.md) now implement all scales,
show actual strong cancellation missed by the sign test, and prove the
exact collection-deficiency formula for matching.

**A concrete sufficient certificate for delayed contrast.**

For one dyadic shell of length N, let the four consecutive length-L block
sums in a group be `u=(u_0,u_1,u_2,u_3)`. Put

\[
e(u)=\sum_{a=0}^3u_a^2,\qquad
\lambda(u)=e(u)-\frac14\left(\sum_a u_a\right)^2.
\]

Summing e gives E_j; summing lambda gives the loss over two merges,
`E_j-E_(j+2)/4`. Call a group sign-diverse if at most two entries are
strictly positive and at most two are strictly negative. Zeros count
toward neither side.

**Lemma.** Every sign-diverse group satisfies `lambda(u)>=e(u)/2`.

Proof: let P be the sum of its positive entries and Q the absolute sum of
its negative entries. If P>=Q, then
`(P-Q)^2<=P^2<=2 sum_(u_a>0)u_a^2<=2e(u)` by Cauchy–Schwarz, because there
are at most two positive entries. The other case uses the at most two
negative entries. Substitute into lambda. This proves the lemma without
a probabilistic hypothesis or a bound on the block magnitudes.

Define the energy weight carried by these groups as

\[
G_{k,j}=\sum_{u\ \mathrm{sign\text{-}diverse}}e(u),\qquad
\Theta_{k,j}=G_{k,j}/E_{k,j}\quad(E_{k,j}>0).
\]

Then the deterministic consequence is

\[
\boxed{V_{k,j+2}\leq(1-\Theta_{k,j}/2)V_{k,j}.}
\tag{1}
\]

All other groups have nonnegative loss. If E_j=0, every later energy
vanishes and no ratio is needed.

An explicit sufficient seed theorem would therefore be:

\[
\exists\theta>0,\ k_0\quad\forall k\geq k_0,\quad
G_{k,j}\geq\theta E_{k,j}
\quad\text{for every even }j\text{ with }j+2\leq\lfloor k/2\rfloor.
\tag{SD, unproved}
\]

Iterating (1) from j=0 to `J=2 floor(k/4)` gives

\[
\frac{M_k}{N}\leq
(1-\theta/2)^{\lfloor k/4\rfloor/2}+2^{J-k}\longrightarrow0.
\]

This would prove P2 by the existing shell-prefix equivalence. A fixed lower
bound at every such merge is unnecessary: divergence of the sum of the
Theta values along these merges also suffices, by `1-x<=exp(-x)`.

This is an alternative certificate format, not a claim that SD is weaker
than every previous contraction hypothesis. It misses some strong
cancellation: the group `(2,2,2,-6)` has G=0 and lambda=e. Neither small G
nor failure of SD disproves P2.

**What was tested, and what must still be proved.**

All 169 admissible pairs `(k,j)` with k=4,...,28 and
`j+2<=floor(k/2)` satisfy `Theta>=1/4` in the stored seed data. This tests
odd as well as even j. The minimum 1/4 occurs at (6,0); the threshold was
read from the completed measurements, not proved in advance.

| Shell k | Smallest measured Theta across admissible j |
|---:|---:|
| 8 | 21/64 |
| 12 | 395/1036 |
| 16 | 1523/4096 |
| 20 | 49063/131072 |
| 24 | 393257/1048576 |
| 28 | 3145543/8388608 |

The missing seed statement is now specific: a nonvanishing fraction of
the **squared block-sum mass** must reach groups with this sign diversity
often enough. The local Rule 30 equation has not been shown to enforce it.
This moves the candidate certificate from a quadratic cross-term inequality
to a weighted sign condition; it does not establish new asymptotic decay.

Counting groups without energy weights is insufficient. For dyadic even L,
construct 4L groups of four realizable length-L block sums. Use one group
`(L,L,L,L)` and 4L-1 groups `(2,-2,2,-2)`. There are N=16L^2 signs, so the
chosen j lies in the proposed scale domain. The unweighted fraction of
sign-diverse groups tends to one, while their energy fraction is

\[
\frac{16(4L-1)}{4L^2+16(4L-1)}\longrightarrow0.
\]

Every block is realizable because its sum has the same parity as L and
magnitude at most L. This artificial example is not Rule 30. It shows why
a count of frequently occurring good patterns would not close SD by itself.

**A local proof of the contrast bound fails on an actual seed window.**

The four aligned length-four blocks starting at time 4640 have sums

\[
(-4,-2,-4,-4).
\]

Consequently e=52 and lambda=3. A pointwise version of the two-merge
inequality with eta=1/2 and C=1 would demand
`lambda>=e/2-C(4L)=26-16=10`, which is false.

For a group define `h=(sum u)^2-2e`. Allocating a remainder proportional
to its length would require `h<=16CL`. The displayed group forces
`C>=23/16`. The largest measured requirement in this scan is 111/32,
at time 101410336 with L=8 and sums `(-8,-8,-6,-8)`.
These are finite obstructions to those specified local constants, not an
all-C impossibility theorem.

The shell itself can still contract strongly. In shell k=12 at j=2,
the positive h contributions sum to 548 and the absolute negative
contributions to 4484. The summed inequality with C=0 holds because these
groups compensate one another. A viable proof must account for that
aggregate compensation; asserting the estimate for every causal block
would discard behavior the actual seed exhibits.

**The pairing queue is already optimal.**

Fix a finite sign word and an integer distance limit R. A matching consists
of disjoint opposite-sign pairs with separation at most R. The FIFO queue
from the previous report achieves the maximum possible number of pairs.

Here is a direct proof. List positive indices and negative indices in
increasing order. Consider the first unused p and m. If `p<m-R`, p can
never pair with any remaining negative index; discard it. The symmetric
case discards m. Otherwise there is a maximum matching containing p-m:

- If either endpoint is unmatched, insert p-m and remove its partner edge
  if needed, without reducing size. If both are unmatched, the old matching
  was not maximum.
- If p is paired to m' and m to p', then `m'>=m` and `p'>=p`. Replace those
  two pairs by p-m and p'-m'. The latter is allowed because
  `p'-m'<=p'-m<=R` and `m'-p'<=m'-p<=R`.

Induct on the remaining indices. The streaming queue makes these same
earliest-index decisions as signs arrive. Expiring a token before a new
arrival cannot discard a future eligible partner, since all future indices
are even farther away. Therefore its unmatched count U_R is minimal over
all allowed pairings.

This proof is universal. Exhaustive independent maximum-matching searches
and queue checks cover all sign words of lengths 1 through 10 at selected
radii, totaling 8168 cases.

**A direct seed obstruction explains the unavoidable unmatched signs.**

Take the k=20 shell, `[1048576,2097152)`, and R=1024. The queue leaves
1476 unmatched signs. This is not just an output of the algorithm; one
interval proves that every allowed matching must leave that many.

Use these absolute time intervals:

\[
I=[1696264,2097151),\qquad
I^{+R}=[1695240,2097152),
\]

where the expansion is clipped at the shell endpoint. Direct counts give

\[
\#\{z=+1\text{ in }I\}=201119,\qquad
\#\{z=-1\text{ in }I^{+R}\}=200305.
\]

Every negative partner of a positive in I must lie in the expanded
interval. There are therefore at least 814 unmatched positives. The shell
has total signed sum 152, which is unchanged by removing opposite pairs.
Thus there must also be at least `814-152=662` unmatched negatives:

\[
\boxed{U_R\geq814+662=1476.}
\]

The queue attains equality. In its output, 468 positive and 662 negative
tokens expire, and 346 positive tokens remain at the end. The direct
interval count independently certifies its optimum.

This is the useful dynamical target suggested by matching: limit persistent
excess of one sign in an interval relative to available opposite signs in
its R-neighborhood. It concerns the actual observed word and boundary
capacity, not an imagined random input. The finite witness does not imply
that these unavoidable losses remain a positive fraction of future shells.

More generally, any set X of positive positions with fewer than |X|
negative positions in its R-neighborhood forces that difference to remain
unmatched. Disjoint expanded intervals allow such deficits to be summed.
Alternating reachability from unmatched positives constructs a set that
attains the optimum deficiency; that construction is used only to discover
the displayed interval. Its verification needs just the two counts above.

**Why the signed expiration current is not automatically easier.**

Let Q_t be signed queue content, and e_t the signed sum of expirations at
step t. Starting with an empty queue, the exact identity is

\[
S(u)=Q_u+\sum_{t<u}e_t,\qquad |Q_u|\leq R+1.
\]

If `J_R=max_(u<=N)|sum_(t<u)e_t|`, then

\[
\boxed{|M-J_R|\leq R+1.}
\]

For any chosen `R_k=o(N)`, vanishing normalized signed-expiration maximum
is therefore equivalent to the existing P2 shell criterion. The queue is
an exact bounded filter of the discrepancy. A proof of symmetry or
cancellation for the expiration process could still solve P2, but its
centering cannot be assumed as an independent noise hypothesis.

Selected exact k=20 records illustrate the distinction between absolute
and signed expirations:

| R | U_R | Positive expirations | Negative expirations | J_R | M |
|---:|---:|---:|---:|---:|---:|
| 8 | 90522 | 45337 | 45180 | 1193 | 1198 |
| 32 | 26920 | 13536 | 13384 | 1180 | 1198 |
| 128 | 8126 | 4089 | 3987 | 1127 | 1198 |
| 512 | 2230 | 1100 | 1039 | 931 | 1198 |
| 1024 | 1476 | 468 | 662 | 662 | 1198 |

An absolute expiration bound might be stronger than necessary. A small
signed *total* is insufficient because J_R must retain prefix excursions.

**What this continuation establishes, and the next proof obligation.**

The matching algorithm needs no improvement at fixed R: it already attains
the exact optimum. Its remaining problem is controlling the interval
deficiencies that force unmatched signs. The contrast route has the
explicit sufficient condition SD, including the necessary energy weights.
Both now have concrete seed quantities to attack.

Neither uniform weighted sign diversity nor a sublinear bound on the
matching deficiencies has been proved. In particular, none of the finite
numbers above is evidence that an all-scale induction has been found.
The next useful proof must use the singleton initial condition to bound
one of these quantities; another universal identity alone will not do it.

**Reproduction and verification.**

```sh
uv run python experiments/rule30/p2_cancellation_mechanism.py
uv run python experiments/rule30/verify_p2_cancellation_mechanism.py
```

- [Exploration code](../../experiments/rule30/p2_cancellation_mechanism.py)
  and [integer records](../../experiments/rule30/p2-cancellation-mechanism.json).
- [Independent verifier](../../experiments/rule30/verify_p2_cancellation_mechanism.py)
  and [verification records](../../experiments/rule30/p2-cancellation-mechanism-independent.json).
- The seed-data provenance and SHA-256 are unchanged from the preceding
  report. The large payload was not independently regenerated as a CA.
  Witnesses before time 8192, including time 4640, were checked against
  freshly generated seed bits.
- All 169 local maximum witnesses were independently recomputed. Six
  complete weighted profiles were independently summed from direct byte
  population counts, including k=28. Their energies and total defects
  agree with the preceding shell calculations.
- The sign-diversity inequality was checked on all 1375 qualifying vectors
  in `{-3,...,3}^4`, supplementing its symbolic proof. Six realizable-word
  controls verify the distinction between weighted and unweighted counts.
- The neighborhood deficit certificate was independently verified by
  direct interval counts. All checks passed.

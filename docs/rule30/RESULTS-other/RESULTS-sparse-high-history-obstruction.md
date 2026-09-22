# A counterexample to the conditional one-eighth information bound

Date: 2026-09-11. **The proposed fixed-high-row bound (H) is false, already
with two visible original low bits.** The unrestricted original-ancestor
inequality `|C_r(alpha)| 2^D <= 2^(2r-1)` remains unproved and unrefuted.

This report also proves an exact first-guard rank theorem for every original
high row. In the two-visible-bit case, a prescribed first successful scalar
already fixes the entire future trajectory within that row. Subsequent repeats
can require no further information from its original low bits.

These are legal auxiliary Z frontiers. There is no assertion of singleton-seed
reachability, unrestricted mortality, arbitrary-period exclusion, or a P2 result.
All counts keep the original length fixed and retain every chronological guard.

## 1. Exact counterexample

Fix original length and original high row

\[
 r=46735,\qquad a_i=1\ (i\ne17197),\qquad a_{17197}=0.
\]

Indices start at zero. Only the original low bits at positions 0 and 17198
are visible to the first update. The original legal word

\[
 \boxed{w=2^{17197}\,0\,2^{29537}}                     \tag{1}
\]

uses word-repetition notation and sets **all** low bits to zero. Its complete
successful scalar tape is

```text
1100000000000111110000
```

Equivalently this is `1^2 0^11 1^5 0^4`: N=22 and D=18. The next update fails.
There are exactly

\[
 |F_a(\alpha)|=2^{46733}=2^{r-2}                     \tag{2}
\]

original low rows with this fixed high row and this tape: they have
`b_0=b_17198=0`, and every other original low bit is arbitrary.

Thus the conditional probability is exactly 1/4. The former proposal

\[
 |F_a(\alpha)|\,2^{D(\alpha)/8}\le2^r                \tag{H}
\]

would require `(1/4) 2^(18/8) <= 1`, but the left side is `2^(1/4)>1`.
An integer-only certificate is

\[
 \left(\frac{|F_a(\alpha)|\,2^{D/8}}{2^r}\right)^8
   =\frac{2^{18}}{4^8}=4>1.                          \tag{3}
\]

The earlier all-length k=1 theorem, including its sharp exponent 1/8, remains
valid. Its extension to k=2 does not.

## 2. Proved: the first guarded scalar has affine rank two

Fix any legal original high row a. As in the
[erasure lemma](RESULTS-constant-high-history-family.md#2-an-exact-erasure-lemma-for-any-fixed-original-high-row), put

\[
 V(a)=\{0\}\cup\{j:1\le j<r,\ a_{j-1}=0\},
 \qquad k=|V(a)|.
\]

For j in V write z_j=b_j. Every other original low bit is erased at the first
scan. All sums and products in this section are in GF(2). Define

\[
 c_i=\sum_{h=0}^{i-1}a_h,\qquad
 Z_j=\sum_{i=j}^{r-1}(1+a_i),
\]

with c_0=0. If u,v are the terminal running bits of the first scan, then

\[
 \boxed{v=c_{r-1}+\sum_{j\in V}z_j,\qquad
 u=\sum_{i=0}^{r-1}a_i+\sum_{i:a_i=0}c_i
       +\sum_{j\in V} Z_jz_j.}                       \tag{4}
\]

**Proof of (4).** Immediately after input i, the running low bit is

\[
 v_i=c_i+\sum_{j\in V,\ j\le i}z_j.
\]

Indeed each preceding high one makes the corresponding OR equal one; the
remaining contributions are precisely the visible low bits. Also
`v_i OR a_i = a_i + (1+a_i)v_i`, so

\[
 u=\sum_i a_i+\sum_{i:a_i=0}v_i.
\]

Substitution and interchange of the finite sums give (4). This is an affine
identity, not an assumption of independent history constraints.

**Rank theorem.** If k>=2, the map from the k visible low bits to the first
terminal pair (u,v) has rank two. Consequently, for each prescribed first
successful scalar s,

\[
 E_a(s)=2^{k-2},\qquad |F_a(s)|=2^{r-2}.              \tag{5}
\]

**Proof.** Let p be the first nonterminal high-zero position. Both 0 and p+1
belong to V. Since p is the first high zero, `Z_0 + Z_(p+1)=1`. The coefficients
of these two visible bits in v are both one, whereas their coefficients in u
differ. The two coefficient rows are therefore linearly independent. Every
terminal pair has exactly `2^(k-2)` visible assignments. Requiring success
and scalar s specifies `(u,v)=(s,s)`. Multiplying by the `2^(r-k)` choices of
erased original low bits proves (5).

This includes adjacent high zeros and a high zero at the original terminal
site. It does not require the zeros to be far apart.

## 3. Proved: no later low-row filtering when k=2

If k=2, (5) leaves **one** visible assignment for either prescribed successful
first scalar. The erasure lemma then fixes the entire first image, hence its
whole actual future. Therefore, for every fixed original high row with k=2
and every nonempty chronological tape alpha,

\[
 \boxed{|F_a(\alpha)|\in\{0,2^{r-2}\}.}              \tag{6}
\]

More precisely, a nonempty successful history class equals its one-symbol
class `F_a(alpha_1)` as a set of original low rows. Any prescribed continuation
either retains that whole set or kills it. This is an all-length theorem;
it does not depend on the numerical witness.

For (1), formula (4) specializes to

\[
 u=1+b_0,\qquad v=1+b_0+b_{17198}.
\]

Success forces `b_17198=0`, and the first scalar 1 forces `b_0=0`.
The four effective originals have the following complete trajectories:

| b_0 | b_17198 | Complete successful tape | N | D |
|---:|---:|:---|---:|---:|
| 0 | 0 | `1100000000000111110000` | 22 | 18 |
| 1 | 0 | `00` | 2 | 1 |
| 0 | 1 | empty; first guard fails | 0 | 0 |
| 1 | 1 | empty; first guard fails | 0 | 0 |

Each row represents exactly `2^(r-2)` original low rows. For the first row,
all 18 repeats occur with no change in this complete conditional ancestor
set. No fresh current predecessor or unguarded completion is introduced.

## 4. What this does and does not exclude

Any uniform **high-row-conditioned** estimate

\[
 |F_a(\alpha)|\le c\,2^{r-\epsilon D(\alpha)}
\]

must now satisfy `c >= 2^(18 epsilon-2)`. In particular, c=1 requires
`epsilon <= 1/9`. This is a necessary restriction, not a proposed proof at
epsilon=1/9. The witness does not exclude every positive epsilon with an
arbitrary fixed prefactor.

More structurally, (6) says that a uniform conditional positive-rate estimate
on k=2 rows is equivalent to a uniform repeat bound on that entire family.
For example it would force `D <= (2+log_2 c)/epsilon` for every realized
nonempty history in that family. No such uniform bound is established here.
The distances between the original visible positions cannot be ignored merely
because there are only two visible bits.

The original candidate counts all legal high rows together. The **contribution
of the verified slice** to its normalized weighted count is only

\[
 \frac{2^{r-2}\,2^{18}}{2^{2r-1}}=2^{-46718}.
\]

We have not computed the other original high-row contributions for this tape.
Thus (3) refutes the conditional strengthening, not the unrestricted `2^D`
inequality. Information in the original high row can still pay for repeats
in that inequality. Finite-frontier mortality and the intended period-two
exclusion remain open.

## 5. Exact verifier and scope of computation

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/sparse_high_history_obstruction.py
```

The [verifier](../../experiments/rule30/sparse_high_history_obstruction.py)
and [artifact](../../experiments/rule30/sparse-high-history-obstruction.json)
record all four effective originals, every guard through failure, every bulk
output hash, the exact conditional count, and the integer violation (3).

An ordinary symbol implementation is compared with the unchanged frozen
`panel/cert33.py` using four bit-plane lanes. Every live original is checked
at every attempted update, including its failed guard: 28 original update
attempts in total. Two additional dense changes to the erased low bits verify
equality of the entire first image. Formula (4) has separate first-scan controls
on 127 high rows and 1,458 visible assignments at lengths 1 through 7; those
controls verify the implementation, while the proof establishes all lengths.

Discovery used bounded exact column-cycle queries for one-zero originals,
followed by actual continuations. Pruning in that search supplies no lifetime
or repeat upper bound. The maintained verifier needs no search, spatial-period
extrapolation, or enumeration of `2^r` low rows. It has a 60-second deadline
and an 80-update lifetime cap; reaching either cap raises an error. It ran
locally in under one second. No paid compute, GPU work, seed regeneration,
nor extension of the original length-1-through-12 census was used.

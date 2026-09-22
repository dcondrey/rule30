# Average forced history: the depth-ten test and an all-depth factorization

Date: 2026-09-12.

**The preregistered depth-ten test passed. The uniform average-forcing
hypothesis, the original cumulative counting bound, finite-frontier
mortality, and period-two exclusion remain open.** No greater temporal depth
was tested. The subsequent uniform proof attempt establishes the factorization
and spatial-limit theorem below, but does not establish the required lower
bound in temporal depth.

There is also a verified failure of a possible induction step: the mean
forced-bit count can **decrease at a repeat**, even though each retained
original gains or retains its own forced bits. This is a statement about
complete chronological ancestor classes, not arbitrary current predecessors.

All frontiers here are the legal auxiliary reconstruction words. None is
asserted to come from the singleton seed. There is no arbitrary-period or
P2 conclusion.

## 1. The executed test

The hypothesis in [the proposal](HYPOTHESIS-average-forced-history.md) is

\[
2Q_r(\alpha)\ge D(\alpha)G_r(\alpha),\qquad
G_r=|C_r(\alpha)|,\quad Q_r=\sum_{w\in C_r(\alpha)}f(w).
\]

The decoder reads the original free bits from right to left, low before
high, omitting a bit precisely when the complete remaining ancestor class
forces it. The original length and every chronological guard remain fixed
in this definition.

The [contract](../../experiments/rule30/average-forced-depth10-contract.json)
was written before its worker started: temporal depth exactly 10, at most
64 spatial transfers, 60 seconds externally enforced, and 1 GiB resident
memory. The [result](../../experiments/rule30/average-forced-depth10.json)
certifies:

* all 1,024 tapes at original lengths 1 through 28: 28,672 exact comparisons;
* at length 28, positive counts at every one of the 2,097,152 reverse states,
  and `2Q-9G>=14,234,187,024` at every state;
* consequently the hypothesis at **every larger original length**, by the
  previously proved positive-transfer argument.

The minimum surplus has `G=396,035,568`, `Q=8,899,253,568`. The smallest
mean-per-repeat ratio in the finite prefix is `140051/98244`, at r=14,
alpha=`0000111101`, D=6, G=196,488, Q=1,680,612. This is a finite-prefix
minimum, not a claimed minimum over all original lengths.

The run took 1.926 seconds and used a worker peak of 625,983,488 bytes.
It completed after 27 transfers. Independent BDD calculations reproduce
both G and Q for the selected classes at r=14, 20 and 28. Together with the
previous certificate, the mean-forcing hypothesis is now proved for all r
at tape lengths **at most ten**.

### Reusing the certificates proves the original normalization through ten

There is a stronger bounded-depth consequence of the saved numbers:

\[
\boxed{|C_r(\alpha)|2^{D(\alpha)}\le2^{2r-1}
       \quad\text{for every r and every }|\alpha|\le10.} \tag{C10}
\]

Only depth ten is new; the earlier depths already had this bound. For
r<=21, the saved depth-ten minima give `Q/(DG)>=140051/98244>1` whenever
G,D>0. The coding lemma therefore proves (C10) there. Empty classes and D=0
are immediate.

For r>=22, reuse the previously proved six-symbol spatial tail certificate:

```
p_r(beta) <= 891465369/1099511627776    for every |beta|=6.
```

A ten-symbol class is contained in its six-symbol prefix class, with the
same original r and every prefix guard retained. Since D<=9,

```
p_r(alpha)*2^D <= 891465369/2147483648 < 1.
```

This proves the remaining lengths. The
[deduction verifier](../../experiments/rule30/average_forced_depth10_original_bound.py)
checks the source hashes, the saved finite-range minima, and the exact
rational tail inequality; its
[artifact](../../experiments/rule30/average-forced-depth10-original-bound.json)
records the result. It performs no new transfer calculation or frontier
enumeration. Equation (C10) is still bounded in tape length and supplies no
uniform cumulative repeat bound.

## 2. An all-depth factorization of the reverse graph

Fix n>=1. Let T be the forward temporal-column adjacency matrix, with row
index the source and column index the destination, counting labeled edges.
Let A be the reverse-pair adjacency matrix in the proposal. Both have
S=2*4^n states, but a physical column and a pair state are different objects.

For an even physical column q and tau in {0,1}, write

```
P(q,tau) = {q, q XOR 1 XOR (2*tau)}.
```

Define two nonnegative integer matrices:

* H has rows indexed by pairs and columns by physical columns. It has one
  edge to each of the two members of P(q,tau).
* K has rows indexed by physical columns y and columns by pairs. For each
  choice of an original low bit b, invert the column scan from y with old
  A_0=0 and new A_0 equal to y's A_0. If the resulting even column is q',
  the K edge goes to P(q',1-b).

**Factorization theorem, for every n:**

\[
\boxed{A=HK,\qquad T^{\mathsf T}=KH.}                 \tag{1}
\]

Every row and every column of H and K has degree two, with multiplicities.

**Proof.** An HK path first selects the physical A_0=a from the incoming
pair, then selects b and applies the exact inverse. These are exactly the
four reverse edges labeled by the original symbol 2a+b.

A KH path first selects b and the inverse pair. Its two members are exactly
the two true predecessor columns with old A_0=0 or 1: changing old A_0
changes old B_1 by 1-b and changes no higher coordinate. These are the four
incoming edges of T. This proves both matrix identities, including edge
multiplicities.

The degree assertion for H follows directly from the pair formula. For a
given K destination P(q',tau'), b=1-tau' is fixed. For each new high bit a,
the fixed-symbol column bijection supplies exactly one physical y. These
are exactly the two incoming K edges. The row degree is two by construction.

This gives, for every j>=0,

\[
A^{j+1}=H(T^{\mathsf T})^jK.                           \tag{2}
\]

The [proved forward connectivity theorem](RESULTS-history-transfer-mixing.md)
supplies a strictly positive T^L at

```
L = 2(S-1) = 4^(n+1)-2.
```

Since H has no zero row and K no zero column, (2) makes A^(L+1) strictly
positive. Thus the reverse graph is strongly connected and aperiodic at
**every** depth; this does not rely on the measured cutoffs through ten.
Its four incoming and four outgoing edges make A/4 doubly stochastic.

Let v_0 indicate the two physical origin columns. Then G_0=H v_0 and

\[
G_k=A^kG_0=H(T^{\mathsf T})^kv_0.                     \tag{3}
\]

In particular G_L>0 at every pair state. Hence, at each n, the reverse
decoder eventually has full support, and its subsequent forcing charges
are identically zero. This proves existence of a finite support cutoff
uniformly in n, though L is much larger than the observed cutoffs.

## 3. An exact spatial-limit theorem for the new statistic

Here k=r-1. Write the exact forcing recurrence as

```
G_(k+1) = A G_k,
Q_(k+1) = A Q_k + c_k,
```

where c_k(s) is the nonnegative sum of child counts multiplied by the
number of forced bits at that branch. Initially Q_0=G_0. The terminal
set has four states, so degree balance gives

```
SUM_s G_k(s) = 4^(k+1).
```

If G_K has full support, c_k=0 for every k>=K. Define the exact dyadic
rational

\[
\boxed{\mu_n=
 \frac{\sum_sQ_K(s)}{4^{K+1}}
 =1+\sum_{k=0}^{K-1}\frac{\sum_s c_k(s)}{4^{k+2}}.}     \tag{4}
\]

It is independent of the choice of a full-support K; one may always use
K=L from §2.

**Spatial-limit theorem.** For every n and every pair state s,

\[
\lim_{r\to\infty}\frac{Q_{r-1}(s)}{G_{r-1}(s)}=\mu_n. \tag{5}
\]

In particular, every length-n successful tape has the same limiting mean
forced-bit count as its original length grows.

**Proof.** After K, both arrays obey the same matrix A. Equation (2) and
the positive power above give convergence of (A/4)^j to the uniform
averaging matrix. The ratio therefore tends to the ratio of the two array
sums, which is (4). Alternatively, the positive-power decomposition used
in the forward mixing proof applies directly to A/4. Formula (4) follows
by summing the forcing recurrence and dividing by 4^(k+2).

The sums over all pair states in (4) are an auxiliary ensemble. At finite
r they are **not** sums over successful scalar tapes: arbitrary pairs also
include rejected terminal patterns. The original history classes enter
(5) at their exact accepting signatures, where all earlier guards are
retained.

This identifies one necessary condition for the proposed uniform hypothesis:

```
mu_n >= (n-1)/2   for every n.                           (6)
```

Apply the hypothesis to either constant length-n tape and take the limit.
If the strict inequality holds at a fixed n, (5) implies that the full-state
positive-cone test `2Q>(n-1)G` eventually succeeds there. Equality alone does
not imply a finite cutoff. Neither (6) at all n nor the earlier valid-signature
inequalities follows from the factorization.

## 4. Exactly what a new temporal layer does

For n>=2, fix a lower pair state s at depth n-1. It has four lifts at depth
n, indexed by the new top pair z=(a,b). In a reverse step, let d be the
target high bit at level n-1 and let

```
c = (reconstructed old high bit at level n-1)
      OR (target low bit at level n-1).
```

The action on z is

\[
\pi_{c,d}(a,b)=(a\mathbin\oplus(b\lor d),\ b\mathbin\oplus c). \tag{7}
\]

The lower state and the original input symbol determine c,d. For each c,d,
(7) is a permutation: recover b first, then a. Thus every fixed original
word accepted at the lower depth belongs to **exactly one** lifted class:
the composition of these permutations must end at the unique origin top
pair (1,b_0).

Consequently, at the same k and original bit order,

\[
\sum_{z=0}^3G_k^{(n)}(s,z)=G_k^{(n-1)}(s),\qquad
\sum_{z=0}^3Q_k^{(n)}(s,z)\ge Q_k^{(n-1)}(s).           \tag{8}
\]

The second assertion holds because restricting a class cannot remove a
forced position on a retained original's decoding path. Summing (8) over
s and taking k beyond both support cutoffs proves

\[
\boxed{\mu_{n+1}\ge\mu_n,\qquad 29/16\le\mu_n\le2n.} \tag{9}
\]

For the lower starting value, the eight-state n=1 calculation has full
support at k=2, with total G=64 and total Q=116. For the upper bound, the
proved coding lemma gives `mean f <= -log_2 p_r(alpha)`, and the proved
forward mixing limit is p_r(alpha)->4^(-n).

Nondecreasing mu_n does **not** establish the positive linear rate in (6).
Nor does the four-class inequality in (8) give an inequality for a selected
successful continuation. At a valid lower signature exactly two lifts pass
the next terminal guard; the other two must be rejected.

## 5. An actual repeat lowers the conditional mean

These complete original classes occur at r=29:

| Tape | D | G | Q | Mean f |
|:---|---:|---:|---:|---:|
| `000111111` | 7 | 792,254,285,262 | 10,513,985,951,412 | 13.270973912... |
| `0001111111` | 8 | 438,162,285,492 | 5,485,341,989,826 | 12.518973383... |

The exact change in the mean is

```
-89522090718185006437 / 119045249767225257894 < 0.
```

Both classes satisfy the proposed half-rate hypothesis. The example refutes
monotonicity of the conditional mean, and therefore any induction demanding
a fixed nonnegative mean increment at every repeat. It does not refute
the cumulative hypothesis.

The four top lifts of the parent make the selection issue explicit:

| Top pair | Tenth update | G | Q |
|---:|:---|---:|---:|
| 0 | successful 1 | 438,162,285,492 | 5,485,341,989,826 |
| 1 | failed guard | 146,866,032,090 | 2,465,713,323,468 |
| 2 | failed guard | 120,222,708,894 | 2,046,200,858,298 |
| 3 | successful 0 | 87,003,258,786 | 1,520,458,805,970 |

Their counts sum to the exact parent count. Their Q totals exceed the
parent Q by 1,003,729,026,150, as required by (8). The repeated child still
has a lower mean. Treating the two failed lifts as successful ancestors,
or replacing the selected-child mean by the four-lift average, would be
invalid.

## 6. Verification and the remaining proof obligation

The [verifier](../../experiments/rule30/average_forced_lift_certificate.py)
and [artifact](../../experiments/rule30/average-forced-lift-certificate.json)
check the local permutation identity, both matrix factorizations with
edge multiplicities through n=5, and the four-lift inequalities at eight
original lengths. The general proofs are the algebra above, not these
finite controls.

The new spatial-limit statistics through n=8 are exact:

```
29/16, 7251/2048, 21571/4096, 1847425/262144,
284495409/33554432, 21719518411/2147483648,
1614526243715/137438953472, 29243268727479/2199023255552.
```

No linear-growth extrapolation is made. The repeat witness is independently
checked by the reverse recurrence against the maintained original-variable
BDD, including both valid next scalars. The same verifier saves the three
independent depth-ten BDD controls. Its completed run took 3.589 seconds;
the witness worker had an external 60-second/1-GiB cap, and every native
BDD invocation had an external timeout. There was no original-frontier
census, seed regeneration, GPU use, or paid computation.

```sh
uv run --no-project python experiments/rule30/average_forced_lift_certificate.py
uv run --no-project python experiments/rule30/average_forced_depth10_original_bound.py
```

The uniform attempt therefore establishes the reverse mixing mechanism and
the exact temporal partition law. It does **not** control the cumulative
selection of successful children as repeats accrue. A proof still needs
that control, or another argument proving a sufficient cumulative counting
bound. The depth-ten pass and the spatial limit do not settle this fixed-r,
unbounded-tape obligation.

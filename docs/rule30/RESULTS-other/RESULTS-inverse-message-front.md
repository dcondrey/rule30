# Exact inverse uncertainty and factorization of message tails

Date: 2026-09-13. **An all-length message identity is proved. No cumulative
repeat bound, finite-frontier mortality theorem, or period-two exclusion
follows.** The result factors exact backward messages, and the previously
tested contiguous-window minimum messages, into a shorter correlated part
and a deterministically pinned temporal tail.

All counts retain the original length and complete guarded scalar tape.
Physical columns below are states of the exact spatial counting graph;
they are not newly chosen predecessors of an auxiliary frontier. The legal
original boundary is imposed when the message is evaluated at the origin.
No singleton-seed ancestry is asserted.

## 1. The inverse uncertainty front

Use the physical-column state

```
x = (A_0,A_1,B_1,...,A_n,B_n)
```

and the integer spatial adjacency T_n=4P_n from the
[exact transfer construction](RESULTS-cumulative-history-transfer.md).
Let g_alpha indicate the two accepting columns for a length-n chronological
tape alpha. Its signature includes every guard and every transported birth.

Write a target column with primes. Its four incoming labeled edges select
the old A_0 and the newly read original low bit. The source coordinates are

```
A_j = A'_j XOR (B'_j OR A'_(j-1)),
B_j = B'_j XOR (A_(j-1) OR B'_(j-1)).
```

For j=1, B'_0 denotes the selected new original low bit. For j>=2 it is an
actual target-column coordinate. Recursively reconstructed **source low
bits** do not occur in the formula for a source high.

**Inverse-front theorem.** After b inverse spatial steps from the exact
accepting pair, all reachable source columns agree on every A_j with j>b
and every B_j with j>b+1.

**Proof.** Suppose a set of target columns agrees on all A'_j with j>h and
all B'_j with j>h+1. For j>h+1 the three target bits determining A_j are
fixed. For j>h+2, the two target lows determining B_j are fixed, and its
source high A_(j-1) is fixed by the preceding assertion. Thus all incoming
sources agree on A_j for j>h+1 and B_j for j>h+2, regardless of inverse
labels. The accepting pair differs only at A_0, so induction proves the
claim.

This bounds uncertainty; it does not say that evaluating one inverse column
requires reading only a bounded prefix. A representative of the common
tail can be computed by starting at the accepting column with A_0=0 and
choosing inverse label (0,0) at every step. Every such edge exists in the
exact graph. Let theta_(n,b) denote its pairs above level b+1.

## 2. Exact backward-message factorization

Let pi_k truncate a column after its kth temporal pair, and let M_k sum a
function over all coordinates above k. Then

```
M_k T_n = T_k M_k.
```

**Proof.** Fix a source prefix and one original input symbol. The column
transition maps the source's remaining temporal tail bijectively onto the
target tail. At each higher level the target pair determines the source
pair uniquely from the already known lower-level source and target data.
Consequently the sum over source tails can be replaced by the sum over
target tails, separately for each of the four input symbols. Summing these
four equalities proves the identity, with edge multiplicities retained.

Signature truncation gives M_k g_alpha=g_(alpha[:k]). Taking k=b+1<=n,
the inverse-front theorem and the aggregation identity therefore give

```
(T_n^b g_alpha)(q)
  = (T_k^b g_(alpha[:k]))(pi_k q)
    * 1[q_(k+1..n)=theta_(n,b)].
```

This is a pointwise identity on **every** physical column. Path
multiplicities are unchanged. It is not an independence approximation.
The normalized P version follows by dividing both sides by 4^b.

The statement permits k=n, in which case the tail is empty. When n< b+1
there is no claimed dimension reduction.

## 3. The same factorization holds for the tested minimum messages

For width w<=n, each bag contains A_0 and w consecutive temporal pairs.
Let C_(n,w) F be the minimum, over all such bags, of the maximum of F over
the unretained coordinates. These are exactly the bags used in the
[certified-message verifier](../../experiments/rule30/guarded_message_certificate.py).
Define the nonnegative greedy messages

```
H_(n,0)^w = g_alpha,
H_(n,b+1)^w = C_(n,w)(T_n H_(n,b)^w).
```

**Window-message theorem.** For k=b+1<=n,

```
H_(n,b)^w(q)
  = H_(k,b)^min(w,k)(pi_k q)
    * 1[q_(k+1..n)=theta_(n,b)].
```

The pinned tail is the same as in the exact backward message. The theorem
does not assert that the active minimum message equals the exact message.

**Proof: unary pins survive projection.** If a coordinate is fixed on the
support of a nonnegative F, any bag containing it has maximum zero when
that coordinate has the wrong value. Every coordinate is covered, so C
preserves that pin. The inverse-front induction therefore applies to H.
In particular, at intermediate step j, the active core itself still has
fixed A_i for i>j and B_i for i>j+1. Those pins are retained even when they
lie below the final cut k=b+1; the proof does not treat the entire core as
freely assignable.

**Proof: projection respects a fixed tail.** Suppose

```
F(q)=f(pi_k q)*1[q_(k+1..n)=theta].
```

Off the pins, one covering bag makes the envelope zero. On the pins, a full
bag becomes its intersection with the first k pairs, with A_0 still
retained. If w<=k, these intersections contain the ordinary width-w
windows on the prefix. Every additional intersection is a subset of one
of those windows, so its larger maximum is redundant in the minimum.
If w>k, the first full bag retains the entire prefix, and its maximum
equals f. Thus

```
C_(n,w) F(q)
  = (C_(k,min(w,k)) f)(pi_k q)
    * 1[q_(k+1..n)=theta].
```

Fix final b and k=b+1. At every intermediate step j<=b, the preserved
unary pins place the uncertainty front at or below this cut. The inverse
step consequently has a unique tail above k. Aggregation identifies its
remaining core with the lower-depth inverse step; the projection identity
identifies the next core with the lower-depth greedy update. Signature
truncation starts the induction. Canonical inverse paths remain in the
support throughout, since each upper projection dominates its argument,
so the common tail is precisely theta_(n,j). This proves the theorem.

The specified window family and retained A_0 are assumptions of this
statement. Arbitrary altered bags require checking their induced-prefix
projection rule separately.

## 4. Arbitrary temporal depth at fixed original length

Set b=r-1 and k=r. For n>=r the exact complete original count is

```
|C_r(alpha)| = SUM_(beta=0,1)
    (T_r^(r-1) g_(alpha[:r]))(o_(r,beta))
    * 1[theta_(n,r-1) matches the high temporal tail of o_(n,beta)],
```

where the legal origin o_(n,beta) has A_0=1 and every temporal pair
(A_j,B_j)=(1,beta). The analogous formula with H holds for the greedy
window root upper bound. The core is unchanged when a prescribed tape is
extended beyond r; only deterministic tail compatibility changes.

At n>=r+1, a compatible first tail pair fixes beta. Every further surviving
extension therefore retains that one core weight or rejects it. The greedy
majorant can retain a false-positive core weight in the same way. Its
factorization does not establish that the original class is nonempty.

Computationally, no array of 2*4^n physical columns is required merely to
extend temporal constraints above r. One can retain the depth-r core and
compute the deterministic tail. Constructing the signature and inverse
tail still takes work growing with n, and the core complexity still grows
with r.

This is an operator-level refinement of the previously proved
[synchronization theorem](RESULTS-weighted-history-endpoints.md): it applies
to all physical columns and also to a specified approximate-message
algorithm. It gives no additional information charge after synchronization.
Controlling arbitrarily long compatible tails remains the mortality issue.
No fixed finite temporal state space, repeat bound, or uniform vanishing is
deduced from the factorization.

## 5. Exact verifier

```
uv run --no-project python experiments/rule30/inverse_message_front.py
```

The [verifier](../../experiments/rule30/inverse_message_front.py) and
[artifact](../../experiments/rule30/inverse-message-front.json) check:

- 2,720 labeled inverse edges through temporal depth four;
- 162 exact message factorizations;
- 666 greedy window-message factorizations;
- 12,634 nonzero-support pin comparisons.

The bounded controls use all tapes through depth four and selected tapes
at depths five and six, with at most three backward spatial steps. The
all-length result is the algebra and induction above, not an extrapolation
from these cases. Arrays count finite column paths for this structural
check; original frontiers are not enumerated. The verifier has a ten-second
cap, saves source hashes and scope flags, and completed in under a second.
No old census, paid/GPU computation, or frozen-oracle modification was used.

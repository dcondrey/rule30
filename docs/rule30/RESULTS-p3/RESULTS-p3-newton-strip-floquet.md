# Exact distant-time queries on fixed strips of the actual Newton iterates

Date: 2026-09-14. **Proved:** for each fixed positive Newton round, a finite
spatial strip of the actual initialized approximation is purely periodic in
time, with a period polynomial in strip width. Its distant-time value can
be obtained by constructing and powering a finite matrix. Construction is
included in the algorithm and cost. **This does not solve P3:** the center
query has spatial index equal to its time, and the proved sufficient number
of Newton rounds grows with that index.

Verifier: [p3_newton_strip_floquet.py](../../experiments/rule30/p3_newton_strip_floquet.py).
Artifact: [p3-newton-strip-floquet.json](../../experiments/rule30/p3-newton-strip-floquet.json).

## 1. Actual initialization and a triangular matrix

Use the moving index j and initialized Newton sequence of the
[error-wedge theorem](RESULTS-p3-newton-error-wedge.md). Write a^(k)_t for
round k at time t; every round starts from the singleton polynomial 1.
Round zero is zero at positive times. Consequently

\[
a^{(1)}_t=(1+X+X^2)^t.
\]

For a positive-round reference a and its next Newton row v, the update is

\[
v'_i=v_i+(1+a_{i-2})v_{i-1}+(1+a_{i-1})v_{i-2}
                 +a_{i-1}a_{i-2}.                 \tag{1}
\]

Negative indices are zero. Every positive round has coefficient v_0=1
at every time. On the vector (v_0,...,v_j), replace the last term in (1)
by a_(i-1)a_(i-2) v_0. This defines a matrix M_j(a) over F2 which agrees
with the update on the invariant set v_0=1. It is lower triangular with
all diagonal entries 1. The only reference coefficients it needs are
a_0,...,a_(j-1); the reference coefficient at j is unnecessary.

For example, when i=2 the coefficient of v_0 is the XOR of both applicable
contributions, not two separate matrix columns. Since a_0=1, equation (1)
then reduces to v'_2=v_2+1. The verifier checks such overlaps explicitly.
At j=0 the entire answer is the constant 1.

## 2. An all-round period theorem

Define

\[
Q(j)=2^{\lceil\log_2(j+1)\rceil},\qquad P_k(0)=1,
\]
\[
P_1(j)=Q(j),\qquad
P_k(j)=Q(j)P_{k-1}(j-1)\quad(k\ge2,\ j\ge1).       \tag{2}
\]

For every k>=1 and j>=0, the prefix a^(k)_t modulo X^(j+1) is purely
periodic from time zero, with period dividing P_k(j). These are sufficient
periods, not claimed minimal periods. For j>=1,

\[
P_k(j)=\prod_{h=\max(1,j-k+1)}^j Q(h)
       \le [2(j+1)]^{\min(k,j)}.                   \tag{3}
\]

**Proof.** For k=1, Frobenius gives

\[
(1+X+X^2)^{Q(j)}=1+X^{Q(j)}+X^{2Q(j)}
                         \equiv1\pmod {X^{j+1}}.
\]

For k>=2, the needed reference strip has period
P=P_(k-1)(j-1) by induction. Thus the sequence of matrices in (1) has
period P. Its chronological product over one period is

\[
U=M_{P-1}\cdots M_1M_0.
\]

This product is lower unitriangular. Set K=U-I. A product of j+1 strictly
lower triangular steps has no possible matrix entry, so K^(j+1)=0.
Since Q(j) is a power of two and Q(j)>=j+1,

\[
U^{Q(j)}=(I+K)^{Q(j)}=I+K^{Q(j)}=I.
\]

After PQ(j) updates both the reference phase and the new row have returned
to their initial values. Determinism therefore gives pure periodicity of
the new strip, proving (2). Expanding the recurrence gives (3).
The argument is over arbitrary width and round count; the finite tests
below are checks of its implementation, not its induction hypothesis.

## 3. A query algorithm that constructs its reference

For k>=2, write t=qP+r with 0<=r<P. During a single pass of P steps, start
all k-1 lower Newton layers at the singleton and evolve them together,
always using the preceding layer's **old** row. This constructs every
needed M_s, the monodromy U and the prefix product V_r=M_(r-1)...M_0.
No later reference row or supplied period table is assumed. Then

\[
a^{(k)}_t\bmod X^{j+1}=V_r U^{q\bmod Q(j)}(1,0,\ldots,0)^T. \tag{4}
\]

The order matters: first apply complete periods, then the remainder phase.
The executable uses repeated squaring on U. Round one is evaluated
directly by Frobenius multiplication at the set bits of t modulo Q(j).

Using explicit binary matrices, building U takes O(P j^2) bit additions:
each local matrix row has at most four entries, while each accumulated row
has j+1 bits. Constructing the reference simultaneously takes O(k P j)
local bit operations. Powering costs O(j^3 log(j+1)) bit operations with
ordinary matrix multiplication. Counters, allocation and binary input
arithmetic add polynomial logarithmic overhead; storage is
O(j^2+kj+log(t+1)) bits, with ordinary indices charged as well.

For each **fixed k**, this is polynomial total bit work in j and in
log(t+1). In particular, arbitrarily distant time does not require a
trajectory of that length. Unlike a supplied-period shortcut, the bound
includes producing the complete reference period P. The implemented
routine has no width, time or round cap; only the verifier uses small
specified controls.

This is useful fixed-strip evaluation, not a sublinear center algorithm.
At the desired center j=t=n, polynomial dependence on j is already too
expensive. The sufficient exact-center schedule k=floor(n/2)+1 from the
error wedge also makes the construction bound in (3) much larger. No
argument here substitutes a fixed k for that growing schedule, and no
minimal-period or necessary-round lower bound follows.

## 4. Relation to algebraic prediction results

Each fixed Newton stack is a triangular system: a layer is affine over F2,
with coefficients determined by the previous layer. This meets the
quasidirect construction of Moore and Pnin, Theorem 1 and Lemma 1, which
provides efficient parallel prediction for fixed stacks. Their proof
constructs coefficients throughout the cone; parallel depth does not give
sublinear total work. The finite-strip argument above instead exploits
the one-sided triangular spatial matrix and explicitly periodic reference.
[Primary paper](https://arxiv.org/pdf/patt-sol/9701008).

Neither polynomial strip periods nor efficient fixed-width evaluation
implies a finite digit automaton for the full two-dimensional array. A
uniform algebraic-series certificate for the second actual Newton round
remains open in this investigation. The separate
[prescribed-reference counterexample](RESULTS-p3-automatic-reference-newton.md)
does not refute such a certificate for the particular reference (1+X+X^2)^t.

## 5. Independent exact controls

The verifier checks all 64 local reference/current triples against literal
Rule 30 truth-table derivatives. It checks every matrix action for the
specified small widths and legal constant coordinates, including the
overlapping source column. A separate list-of-bits Newton implementation
evolves three fixed strips, at indices 1, 3 and 5, for three rounds. It
checks their certified returns and queries at phase boundaries, plus
timestamps shifted by an 81-digit multiple of the certified period.

The proof of the general period is the triangular nilpotence argument,
not finite returns. No true singleton center census, old frontier audit,
GPU computation or paid compute is run. The previous reports and artifacts
are preserved. Run:

```
uv run --offline --no-project python experiments/rule30/p3_newton_strip_floquet.py
```

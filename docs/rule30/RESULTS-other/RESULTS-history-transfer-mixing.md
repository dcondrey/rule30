# All-depth spatial mixing and the cumulative bound through six repeats

Date: 2026-09-11. **The unrestricted cumulative counting inequality remains
open.** This continuation proves connectivity and mixing of the history-transfer
graph at every temporal depth, supplies an explicit spatial cutoff valid at
every depth, and proves the proposed inequality for arbitrary tape lengths
with at most six repeats. None of these statements bounds the number of repeats
along every trajectory of fixed original length. Unrestricted mortality and
the period-two exclusion remain open; arbitrary center periods and P2 are
outside this investigation.

All frontiers are legal auxiliary Z states. The probability notation below
means exact counting under the uniform distribution on the `2^(2r-1)` original
legal length-r words. It makes no assertion about singleton-seed reachability
or randomness of the Rule 30 seed orbit. All chronological guards are retained.

## 1. Results and their quantifiers

Let `p_r(alpha)=|C_r(alpha)|/2^(2r-1)`. For a tape of length n>=1 set

\[
 S_n=2\cdot4^n,\qquad L_n=2(S_n-1)=4^{n+1}-2,
 \qquad R_n=1+L_n4^{L_n}.
\]

**All-depth theorem.** For every fixed n, every length-n tape alpha satisfies

\[
 \lim_{r\to\infty}p_r(\alpha)=4^{-n}.                    \tag{1}
\]

The limit is uniform over the tapes at that depth. More explicitly, for every
n>=1, every such tape, and every r>=R_n,

\[
 \boxed{\frac{2}{2\cdot4^n+1}\le p_r(\alpha)
              \le\frac{3}{2\cdot4^n+1}.}                \tag{2}
\]

Consequently, in this range,

\[
 p_r(\alpha)4^{D(\alpha)}<\frac38.                       \tag{3}
\]

Thus the spatial cutoff method in the
[preceding report](RESULTS-cumulative-history-transfer.md) always terminates
in principle at any fixed depth. The cutoff R_n is deliberately crude and
enormous. No inference that a cutoff grows linearly is made from the previously
computed table.

**Unbounded-tape, bounded-repeat theorem.** For every r>=1 and every finite tape
alpha with D(alpha)<=6,

\[
 \boxed{|C_r(\alpha)|2^{D(\alpha)}\le2^{2r-1}.}           \tag{4}
\]

There is no tape-length restriction in (4). Its proof uses a new exact bound
on nine-symbol prefixes and the already proved bounded-tape result. It still
leaves D>=7 untreated in general.

**Necessary rate restriction.** If constants c>0 and epsilon>0 satisfy the
proposed positive-rate estimate for every r and every tape, then epsilon<=2.
This restriction allows an arbitrary fixed prefactor c, unlike the sharper
restriction for c=1 from the previous finite counterexample. No positive rate
in the remaining range is disproved by this argument.

## 2. The exact graph and its four incoming edges

Use the common graph T_n from the preceding report. Its vertices are

\[
 x=(A_0,A_1,B_1,\ldots,A_n,B_n).
\]

They record the last original column of n total bulk scans, with A_0 the
initial high bit at that column. Reading one more original symbol supplies
`A'_0=a, B'_0=b` and gives

\[
 B'_j=B_j\oplus(A_{j-1}\lor B'_{j-1}),\qquad
 A'_j=A_j\oplus(B'_j\lor A'_{j-1}).                      \tag{5}
\]

Every vertex has four outgoing and four incoming labeled edges, including
multiplicity. Given a target vertex, the four incoming edges correspond to
the choices of old A_0 and new B'_0; the old coordinates are

\[
 A_j=A'_j\oplus(B'_j\lor A'_{j-1}),\qquad
 B_j=B'_j\oplus(A_{j-1}\lor B'_{j-1}).                   \tag{6}
\]

The two legal first-symbol vertices are
`o_beta=(1,1,beta,...,1,beta)`. Every tape alpha determines exactly two accepting
vertices, differing only in A_0. Different tapes at depth n have disjoint
accepting pairs. The suffix transported from the original terminal cut
determines all these pairs, including every intervening guard. These are the
proved signature and path-count identities from the preceding report.

## 3. Connectivity at arbitrary temporal depth

**Theorem.** T_n is strongly connected for every n>=1. It is aperiodic because
the all-zero vertex has a self-loop on input symbol zero.

We prove that every real-valued function f with

\[
 f(x)=f(y)\quad\hbox{on every directed edge }x\to y       \tag{7}
\]

is constant. This will imply weak connectivity; the degree balance then
supplies strong connectivity.

**The first two coordinates.** States differing only in A_0 have a common
successor when the new input low bit is one: the first OR in (5) saturates,
and all subsequent emitted coordinates agree. Thus f ignores A_0.

When A_0=0, flipping both old B_1 and the new input low bit leaves B'_1, A'_1,
and every later emitted coordinate unchanged. These two states also have a
common successor. Since f already ignores A_0, it ignores B_1 everywhere.

**Inductive coordinate elimination.** Suppose f ignores

\[
 A_0,\ldots,A_{j-1},\quad B_1,\ldots,B_j.                \tag{8}
\]

For j<n, the first retained coordinates are `(A_j,B_(j+1))`. In the inverse
equations (6), abbreviate the four target bits

```text
h=A'_(j-1),  ell=B'_j,  a=A'_j,  b=B'_(j+1).
```

The retained old pair is

\[
 x=a\oplus(\ell\lor h),\qquad y=b\oplus(x\lor\ell).     \tag{9}
\]

Two exact moves follow:

* With ell=0, flip h. The old pair changes `(x,y)` to `(1-x,1-y)`.
* With h=a=1, flip ell. The old high bit stays zero and the old low bit flips.

In both moves the changed target coordinate belongs to the ignored set (8),
so its two target values have the same f. Each has an incoming edge supplied
by (6), hence the corresponding old values also have the same f. Apart from
ignored coordinates, only the displayed old pair changes: `A_(j+1)` in (6)
depends on target `A'_j,B'_(j+1)`, which stayed fixed, and all higher retained
coordinates are unchanged.

The moves apply to every assignment of the retained old tail. To see why,
fix the lower target bits and order the remaining target coordinates as

```text
A'_j, B'_(j+1), A'_(j+1), B'_(j+2), ..., A'_n.
```

Equation (6) is triangular and bijective in this order: each old coordinate
is its corresponding target coordinate XOR a function of preceding coordinates.
For the second move, fixing a=1 simply fixes the old high bit to zero; the
remaining tail is still arbitrary. Thus no independence of ancestry
constraints, or unproved realizability of a tail, is being assumed here.

Simultaneous complementation and a low-bit flip at high zero connect all four
pairs: `00` connects to `01` and `11`, and `01` connects to `10`. Therefore f
ignores both A_j and B_(j+1), proving the induction step.

After j=n-1, only A_n remains. Set B'_n=0 and flip A'_(n-1), an already ignored
coordinate. Equation (6) flips old A_n. Hence f ignores this last bit as well
and is constant. The n=1 case uses the first two-coordinate argument and this
last-bit step directly.

**From this to strong connectivity.** A function labeling weak components
satisfies (7), so the graph is weakly connected. For any vertex, its reachable
set has no outgoing edge to its complement. Summing indegree minus outdegree
over that set shows that it has no incoming edge either, because each vertex
has equal incoming and outgoing degree. A proper such set would disconnect
the underlying undirected graph. Every vertex therefore reaches every other.
This proves strong connectivity for arbitrary n, without a finite-depth
extrapolation.

## 4. Quantitative mixing and a universal spatial cutoff

Let P_n be the transition matrix whose four labeled edges each have probability
1/4. Degree balance makes it doubly stochastic, so the uniform distribution
on its S=S_n vertices is stationary. A uniform legal original word gives the
initial distribution `(delta_(o_0)+delta_(o_1))/2` after its first symbol and
then r-1 transitions of P_n.

By strong connectivity, every vertex reaches zero in at most S-1 edges, and
zero reaches every vertex in at most S-1 edges. The self-loop at zero pads
these paths to a common exact length L=2(S-1). Consequently every entry of
P_n^L is at least `delta=4^(-L)`. Put `theta=S*delta`, and let U have every
entry 1/S. Then

\[
 P_n^L=\theta U+(1-\theta)Q                              \tag{10}
\]

for a nonnegative doubly stochastic matrix Q. This is an exact decomposition;
0<theta<1. Since UQ=QU=U, after k blocks and any remaining transitions the
distribution has a uniform component of mass `1-(1-theta)^k`.

Each tape accepts two vertices, so, with
`k=floor((r-1)/L)` and `e=(1-theta)^k`,

\[
 (1-e)\frac2S\le p_r(\alpha)
       \le\frac2S+\left(1-\frac2S\right)e.              \tag{11}
\]

This proves (1) and gives an explicit error bound at every r,n. It concerns
extension of the **original spatial word**, with the temporal depth held fixed.
It is not a conditional contraction when a new scalar is appended.

For an elementary explicit cutoff, use

\[
 (1-\theta)^k\le\frac1{1+k\theta}.
\]

This follows by applying the binomial inequality to
`(1-theta)^(-k) >= (1+theta)^k >= 1+k*theta`.
At k=4^L the product k*theta equals S. Thus r>=1+L4^L implies e<=1/(S+1).
Substitution in (11) gives exactly

\[
 \frac2{S+1}\le p_r(\alpha)\le\frac3{S+1},
\]

proving (2). Since `4^D<=4^(n-1)=S/8`, (3) follows.

There is also a smaller purely qualitative realizability bound. Every finite
tape of length n has some legal ancestor of length at most S_n: take a simple
path from o_0 to one of its accepting vertices. Every length
`r>=L_n+1=4^(n+1)-1` admits an ancestor of that tape by the padded path through
zero. These ancestors may differ at every length. This supplies no infinite
trajectory from one fixed finite frontier.

## 5. Exact limiting history statistics and a rate restriction

Because the `2^n` accepting pairs are disjoint, (1) also gives

\[
 \lim_{r\to\infty}\Pr(\text{survive }n\text{ updates})=2^{-n}.
\]

Conditional on surviving n updates, the scalar tape tends to the uniform
distribution on the `2^n` tapes. For the previously considered weighted mass,

\[
 \lim_{r\to\infty}\frac{M_r(n)}{2^{2r-1}}
   =4^{-n}\sum_{|\alpha|=n}2^{D(\alpha)}
   =\frac12\left(\frac34\right)^{n-1}.                 \tag{12}
\]

The sum is `2*3^(n-1)`: choose the first scalar in two ways, and each later
position contributes weight one for switching and weight two for repeating.
Equation (12) is a spatial limit at fixed n. It does not assert stepwise
monotonicity of M_r(n); the known `M_4(1)<M_4(2)` example remains valid.

Suppose the unrestricted information bound held with c and epsilon. Apply
it to the constant tape `0^n`, which has D=n-1, and take r to infinity in (1):

\[
 2^{-2n}\le c\,2^{-\epsilon(n-1)},\qquad
 2^{(\epsilon-2)n-\epsilon}\le c.
\]

If epsilon>2 this is impossible for arbitrarily large n. Thus epsilon<=2 is
necessary even when c is arbitrary. This argument does not rule out epsilon=2
with a sufficiently large c, or any smaller positive rate. The prior c=1
restriction `epsilon<=1.569319719...` remains stronger in its narrower setting.

## 6. The candidate for all tapes with at most six repeats

The new finite coefficient calculation proves the sharp prefix estimate

\[
 \sup_{r\ge1,\ |\alpha|=9}p_r(\alpha)=\frac{27}{2048}.  \tag{13}
\]

For n=9 it checks all 512 signatures at original lengths 1 through 12. The
maximum occurs at r=8, tape `001101011`, with 432 ancestors out of 32,768.
At original length 12 the largest column count is 41,556, giving the ceiling

\[
 \frac{m_{12}}{4^{11}}=\frac{10389}{1048576}
      <\frac{27}{2048}.
\]

The previously proved spatial maximum principle
`m_(r+1)<=4*m_r` therefore extends (13) to every larger original length.
These 6,144 comparisons test a new unweighted envelope, rather than rerunning
the earlier weighted theorem or original-frontier census.

For every longer tape, complete chronological ancestry gives
`C_r(alpha) subseteq C_r(alpha[:9])`, with the same original r. Thus (13)
holds for every tape of length at least nine. If D<=6,

\[
 p_r(\alpha)2^D\le\frac{27}{2048}\,64=\frac{27}{32}<1.
\]

For shorter tapes the preceding report already proves the candidate at every
r. This establishes (4), including the empty tape. It does not assume that
any individual repeat removes ancestors.

## 7. Verification and the unresolved regime

Code: [history_transfer_mixing.py](../../experiments/rule30/history_transfer_mixing.py).
Certificate: [history-transfer-mixing.json](../../experiments/rule30/history-transfer-mixing.json).

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/history_transfer_mixing.py
```

The program checks the constant-size Boolean identities used in the connectivity
induction, including the four-pair orbit. As independent implementation controls,
it traverses every graph through depth eight in both directions from zero,
covering 174,760 vertices and checking the self-loop. The measured maximum
distances are:

| Depth | From zero | To zero |
|---:|---:|---:|
| 1 | 2 | 3 |
| 2 | 4 | 5 |
| 3 | 7 | 7 |
| 4 | 10 | 11 |
| 5 | 12 | 13 |
| 6 | 17 | 16 |
| 7 | 18 | 20 |
| 8 | 21 | 23 |

These are finite controls. The all-depth connectivity result follows from §3,
not this table, and no asymptotic distance formula is inferred.

The verifier also checks (13) and its exact rational tail ceiling. It checks
source hashes for the previously proved bounded-tape input, without rerunning
that certificate. All counting and proof comparisons use integers or exact
rationals. A cap raises an inconclusive error before any completed artifact is
written. The local run took about three seconds. There was no paid compute,
GPU use, or seed regeneration; the frozen oracle and previous artifacts were
preserved.

The main remaining issue is the order of quantifiers. Fixing n and taking
r large gives (1)-(3), whereas mortality fixes r and lets the successful tape
grow. Neither these limits nor (4) supplies an upper bound on D in that latter
regime. This is also why eventual periodicity of fixed autonomous prefixes
has not been used as a substitute for control of the moving boundary.

Combining the proved restrictions, any counterexample to the `2^D` candidate
must have original length at least 13, tape length at least 10, and at least
seven repeats. It must also lie below the explicit spatial cutoff R_n.
No such counterexample was obtained. The unrestricted positive-rate counting
bound, cumulative repeat budget, finite-frontier mortality, and period-two
exclusion remain open.

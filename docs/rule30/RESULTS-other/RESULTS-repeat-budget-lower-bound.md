# Long frontier survival requires logarithmically many scalar repeats

Date: 2026-09-10. **An unconditional lower bound on repeats, and a conditional
mortality horizon. The conjectured upper bound remains open.**

Let a legal Z-frontier of initial length r emit a successful nonempty scalar
tape of length N. Let D count equal adjacent scalars in that tape. Then

\[
\boxed{r+N+1\le 2^{D+1}(r+2).}                         \tag{1}
\]

If the initial frontier already has terminal high bit one, then

\[
\boxed{r+N+1\le 2^{D+1}(r+1).}                         \tag{2}
\]

Every successful image has that terminal high bit. In particular, (1) gives

\[
D\ge \max\left(0,
\left\lceil\log_2\frac{r+N+1}{r+2}\right\rceil-1\right).
\]

This is obtained by combining the existing alternating-run bounds across
the full scalar history. It is a quantitative corollary of those bounds;
the alternating-run theorem is not new. No literature-priority claim is made.

## Proof from the alternating-run bounds

The existing bounds are:

- an alternating scalar run beginning at length a has length at most a+3;
- if the onset has terminal high bit one, its length is at most a+1.

Their period-28 reconstruction proof appears in the panel's
[third transcript](../../experiments/rule30/panel/transcript3.json). A direct
verification and the reconstruction thresholds are supplied below to make
the input to the present corollary explicit.

Partition the successful tape immediately before each repeated scalar.
The resulting D+1 nonempty blocks are alternating. No scalar is duplicated
or discarded. If r_j is the length at a block's onset and L_j is that
block's length, then exactly

\[
r_{j+1}=r_j+L_j.
\]

The first block gives r_1+1<=2(r+2). All later block onsets are successful
images, so their bounds give

\[
r_{j+1}+1\le 2(r_j+1).
\]

Applying the latter inequality to the remaining D blocks yields (1).
When the initial terminal high bit is one, the sharper doubling inequality
also applies to the first block, yielding (2). This proof applies to an
unfinished final alternating block as well as to a complete trajectory.

## A weaker sufficient target: any finite repeat bound

The sharp conjecture D<=r-1 is not needed for this mortality implication.
Suppose there is any finite function B(r) such that every successful tape
from every legal initial frontier of length r has D<=B(r). Then (1) gives

\[
\boxed{N\le 2^{B(r)+1}(r+2)-r-1.}
\]

Thus even a much larger proved repeat budget would suffice to establish
finite-frontier mortality. The bound must hold for all successful prefixes,
with B depending only on the initial length, not the current length or the
elapsed time. This is a conditional corollary, not a new repeat upper bound.
It concerns the auxiliary frontier problem; by itself it does not exclude
every eventual period of the lone-seed center column.

The exact composition and inverse-fiber laws can be used to test quantities
that retain initial length and chronological guards. However, the simplest
such quantity, the number of compatible original ancestors, need not decrease
at a repeated scalar, or even over two consecutive repeats; see the
[fixed-origin history-count counterexamples](RESULTS-fixed-origin-history-count.md).
Any counting argument along this route therefore needs an additional
quantity or a proved bound on the repeats occurring while its count is
unchanged.

## Explicit consequence if the sharp repeat-budget conjecture is proved

The conjecture in the
[episode report](RESULTS-episode-memory-and-repeat-budget.md) is D<=r-1.
Combining it with (1) would give the explicit bound

\[
\boxed{N\le 2^r(r+2)-r-1.}                            \tag{3}
\]

For initial terminal high bit one, (2) would improve this to

\[
N\le 2^r(r+1)-r-1.
\]

These statements are conditional. Formula (1) does not supply the missing
upper bound on D. It says that an arbitrarily long surviving history must
keep introducing repeats, at least logarithmically often. Establishing that
only finitely many repeats are possible would then force mortality.

## Check of the alternating-run input

For a formally alternating scalar signal, encode each temporal two-cycle
by its two bits as an integer in {0,1,2,3}. Let sigma exchange the two bits.
The depth reconstruction starts from

```
(f_0,g_0)=(3,1),    (f_1,g_1)=(2,2),
f_(d+1)=f_d XOR (g_d OR sigma(f_(d-1))),
g_(d+1)=g_d XOR (sigma(f_d) OR sigma(g_(d-1))).
```

Direct evaluation returns the initial two consecutive depth pairs at
depths 28 and 29. Determinism then proves period 28 for all depths.
For temporal phase d+epsilon, define H_epsilon(d) as the corresponding
g-bit when the f-bit is one, and `-` when the f-bit is zero. Over one
complete period the two sequences are

```
H_0 = 111--001000---0---0-0-----1-
H_1 = 0---0-0-----1-111--001000---
```

Neither cyclic sequence contains four equal non-dash symbols. Neither
contains three equal non-dash symbols beginning at an odd depth. The
recurrence, cycle return, and both assertions were independently checked
with exact two-bit arithmetic in this investigation.

For an arbitrary onset, the existing history reconstruction determines
the whole state after n emissions when

\[
n\ge 1+\lfloor(r+n)/2\rfloor,
\]

which holds for n>=r+1. The origin then samples successive depths
d=r+n-1. Its invariant pair is (1,beta), so survival through the four
times r+1,...,r+4 would require four equal anchor symbols. Hence the
alternating run has length at most r+3.

For terminal high bit one at onset, the sharper depth thresholds are:

| Field | Sufficient number of emissions |
|---|---:|
| A_(2k) | k |
| A_(2k+1) | k+1 |
| B_(2k) | k+1 |
| B_(2k+1) | k+1 |

The base A_0(0)=1 is the extra onset information; B_0 is known after one
emission, and both depth-one fields are known after one emission. Substituting
these four thresholds in the exact backward recurrences proves them by
induction on depth. In particular, after n=r emissions the entire length-2r
state is reconstructed. The initial sampled origin depth is now 2r-1,
which is odd. The parity-sensitive three-symbol exclusion therefore rules
out survival through r,r+1,r+2 and gives the sharper r+1 bound.

The opposite initial scalar phase merely exchanges the two temporal bits
and is covered by the two values of epsilon. All arguments concern legal
finite Z-frontiers; they do not establish a new claim about a designated
Rule 30 seed orbit. P1, P2, and the upper repeat-budget conjecture remain open.

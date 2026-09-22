# Cumulative history counts: a spatial certificate and a stronger counterexample

Date: 2026-09-11. **The proposed `2^D` inequality remains open for arbitrary
tapes.** This investigation proves an exact counting theorem for every original
length when the tape has at most nine symbols, and refutes the stronger `3^D`
normalization. Neither result proves unrestricted frontier mortality or the
period-two exclusion. P2 and arbitrary center periods are outside this work.

Every frontier here belongs to the auxiliary legal Z universe. None is asserted
to arise from the singleton Rule 30 seed. Throughout, `C_r(alpha)` counts all
original legal words of exactly length r that pass **every** chronological guard
and emit alpha. D counts equal adjacent scalars.

## 1. Results

**Computer-assisted theorem, unbounded original length and bounded tape length.**
Put

\[
 b_* = \left(\frac{2^{24}}{24561}\right)^{1/6}
      = 2.967647463\ldots.
\]

For every r>=1 and every tape alpha with at most nine symbols,

\[
 \boxed{|C_r(\alpha)|\,b_*^{D(\alpha)}\le 2^{2r-1}.}       \tag{1}
\]

The factor is **sharp for this class**: equality occurs at r=14 and
alpha=`00001111`. In particular (1) proves the requested `2^D` estimate, and
the stronger estimate

\[
 |C_r(\alpha)|^2\,8^{D(\alpha)}\le 2^{4r-2},               \tag{2}
\]

on this class. The latter has c=1 and epsilon=3/2, but only for these bounded
tape lengths. It does not supply the constants for unrestricted tapes required
by the mortality argument.

This is an infinite collection of length cases certified by a finite calculation,
not an extrapolation from the original-frontier census. The all-length extension
uses the maximum principle proved below. The graph construction and maximum
principle themselves hold at every tape length; the executed certificate covers
lengths one through nine.

**Exact counterexample to the `3^D` estimate.**

\[
 |C_{14}(00001111)|=196488,\qquad D=6,
\]

so

\[
 196488\cdot3^6=143239752 > 134217728=2^{27}.              \tag{3}
\]

This strengthens the previously known refutation of the `4^D` estimate.
The `2^D` weighted ratio for this family is only
`24561/262144`, so (3) does not refute the active candidate.

## 2. One common spatial graph for every tape of a given length

Let B be the total bulk scan: emit the input-length prefix and omit the guard
and append. A fixed prefix evolves autonomously under B. Fix a temporal depth
n>=1. At one spatial column k, record

\[
 x=(A_0,A_1,B_1,\ldots,A_n,B_n),
 \qquad A_j=a_k^{(j)},\quad B_j=b_k^{(j)}.
\]

Here j is the number of bulk iterations. `A_0` is the initial high bit **at this
column**, not necessarily at the spatial origin. The initial low bit need not
be carried to the next column. There are exactly `2*4^n` possible records.

Reading the next original input symbol supplies `A'_0=a`, `B'_0=b`. The exact
cascade of scans is

\[
 \begin{aligned}
 B'_j&=B_j\mathbin\oplus(A_{j-1}\mathbin\lor B'_{j-1}),\\
 A'_j&=A_j\mathbin\oplus(B'_j\mathbin\lor A'_{j-1}),
 \qquad 1\le j\le n.
 \end{aligned}                                           \tag{4}
\]

Thus (4) defines a directed graph T_n with four labeled outgoing edges per
state, one per original input symbol. **The transition graph does not depend
on the scalar tape.** No guard has been discarded from the accepted language:
the tape will specify a complete terminal column test in §3.

**Four-incoming-edge theorem.** Every state has exactly four incoming edges,
counting labels and multiplicity.

**Proof.** Fix the target column x'. Choose the two bits `A_0` and `B'_0`
arbitrarily. The input high bit is already fixed by the target `A'_0`.
Recover the old column in increasing j by

\[
 \begin{aligned}
 A_j&=A'_j\mathbin\oplus(B'_j\mathbin\lor A'_{j-1}),\\
 B_j&=B'_j\mathbin\oplus(A_{j-1}\mathbin\lor B'_{j-1}).
 \end{aligned}                                           \tag{5}
\]

These formulas give a unique predecessor for each of the four choices, and
substitution verifies (4). Conversely an incoming labeled edge specifies both
chosen bits and must satisfy (5). Distinct choices may have the same predecessor
state, but then have different edge labels; their multiplicities must be kept.
This proves the theorem for every n. No mixing or independence assumption is
used.

After the first legal symbol `2+beta`, the state is

\[
 o_\beta=(1,1,\beta,1,\beta,\ldots,1,\beta),
 \qquad \beta\in\{0,1\}.                                \tag{6}
\]

This follows from the invariant origin pair `(1,beta)` under the bulk scan.
Consequently path counts from these two states count original legal words,
including their multiplicities, rather than distinct current frontiers.

## 3. A tape specifies exactly two accepting column states

Fix a chronological tape `s_0,...,s_(n-1)`. Cut at the end of the original
length-r word. Initially the suffix at this cut is empty. Keep every appended
cell on its right throughout the construction.

Suppose the suffix S after j-1 updates and the required preceding bulk high
bit `A_(j-1)` have been determined. Choose the two entering bits `(A_j,B_j)`
so that scanning S ends at `(s_(j-1),s_(j-1))`. Such a pair exists uniquely:
for fixed input symbols and preceding input high bit, each scan step is a
bijection of the two running bits `(u,v)`. Its inverse is the same backward
scan used in the existing
[episode factorization](RESULTS-variable-length-episode-composition.md).
The emitted suffix, with `3-s_(j-1)` appended, is the next S.

For j=1 the suffix is empty, so `A_1=B_1=s_0`, independently of the original
last high bit `A_0`. Thereafter the preceding high bit is one of the already
determined `A_j`. Induction therefore determines all n required pairs without
fixing `A_0`. Denote this column signature by sigma(alpha).

**Signature theorem.** An original legal length-r frontier belongs to
`C_r(alpha)` if and only if its bulk column at spatial index r-1 has these n
pairs. The accepting states are the two choices of `A_0` with signature
sigma(alpha).

**Proof.** At each update, the bulk prefix is the actual prefix by triangularity.
Its last emitted pair must be the unique pair just constructed for the suffix
to pass that update's prescribed terminal guard. When it matches, the emitted
suffix is exactly the transported suffix used at the next update. Induction
proves both necessity and sufficiency, including every intermediate guard.
A later matching guard cannot restore a failed earlier one. This is the
existing history-preserving seam law specialized to the original terminal cut;
the suffix carries the entire chronological history across switches.

Signatures of different tapes of the same length are different. At their first
different scalar the prior suffix and prior high bit agree, and the bijective
suffix scan requires different entering pairs. Thus the `2^n` signatures have
disjoint two-state accepting sets.

Together with a separate initial state and illegal-first-symbol sink, this
also gives a uniform DFA construction with at most `2*4^n+2` states for any
prescribed tape. This explains the size pattern previously observed for
[preimage languages](RESULTS-episode-memory-and-repeat-budget.md). It is an
upper bound and common representation, not a claim that every such DFA is
minimal.

## 4. A maximum principle in the original spatial length

Let `v_r(x)` count legal original words of length r whose depth-n bulk column
record is x. These are unconditioned counts; the accepting signature imposes
the complete history afterward. In particular

\[
 v_1=\mathbf1_{o_0}+\mathbf1_{o_1},\qquad
 \sum_xv_r(x)=2\cdot4^{r-1},\qquad
 |C_r(\alpha)|=\sum_{x\in\operatorname{Accept}(\alpha)}v_r(x). \tag{7}
\]

Write `m_r=max_x v_r(x)` and `mu_r=m_r/4^(r-1)`. The four incoming edges give

\[
 m_{r+1}\le4m_r,\qquad \mu_{r+1}\le\mu_r.                \tag{8}
\]

Since each tape has two accepting states, for any nonnegative repeat factor b,

\[
 \frac{|C_r(\alpha)|b^D}{2^{2r-1}}\le \mu_r b^D.          \tag{9}
\]

For fixed n, suppose an exact computation at length R finds

\[
 \mu_R\,4^{n-1}\le1.                                    \tag{10}
\]

Then (8)-(9) prove `|C_r(alpha)|*4^D<=2^(2r-1)` for **every r>=R** and
every length-n tape, since `D<=n-1`. Every smaller factor, including b_* and
2, is covered as well. The remaining cases `1<=r<R` form a finite exact
matrix calculation.

This maximum principle concerns extension of original spatial words at fixed
temporal depth. It asserts no contraction when a scalar is repeated, no
monotonicity in temporal depth, and no monotonicity of the aggregate weighted
history count `M_r(n)`. The known chronological plateaus and increases of M
are compatible with (8). Each quantity in (7) still counts originals of its
stated fixed length r.

## 5. The finite certificate proves the unbounded-length statement

The verifier constructs (4) and (5), checks their inverse identities on every
labeled edge, computes every signature, and propagates exact integer path
counts. The following cutoffs satisfy (10):

| Tape length n | Column states | Tail cutoff R |
|---:|---:|---:|
| 1 | 8 | 1 |
| 2 | 32 | 4 |
| 3 | 128 | 8 |
| 4 | 512 | 11 |
| 5 | 2,048 | 17 |
| 6 | 8,192 | 22 |
| 7 | 32,768 | 27 |
| 8 | 131,072 | 32 |
| 9 | 524,288 | 37 |

The artifact records `m_R` and the rational `mu_R` exactly. No fitted cutoff
formula is used or asserted beyond this table.

At every smaller length, and at the cutoff, the checker verifies (1) by the
integer comparison

\[
 |C_r(\alpha)|^6(2^{24})^D
       \le (2^{2r-1})^6\,24561^D.                        \tag{11}
\]

All 32,802 length/tape comparisons pass. Equations (8)-(10) prove the entire
remaining spatial tail. The empty tape satisfies equality separately.
This establishes (1). Because
`8^3*24561 < 2^24 < 3^6*24561`, one has `sqrt(8)<b_*<3`, giving (2).
The exact count in (3) satisfies `196488*2^24=2^27*24561`, which proves equality
in (1) there and hence optimality of b_* for tapes of at most nine symbols.

The same certificate gives the complete list of failures of the `3^D`
normalization for tapes of at most nine symbols, across **all** original lengths:

| Original length | Tape | Original ancestors | D |
|---:|:---|---:|---:|
| 14 | `00001111` | 196,488 | 6 |
| 15 | `11110000` | 751,824 | 6 |
| 14 | `000011110` | 196,488 | 6 |

For every other case in this class the `3^D` bound holds. This classification
uses the tail proof as well as the finite coefficient checks.

## 6. Independent verification of the counterexample family

The verifier counts `C_14(00001111)` by a second, backward dynamic program on
the common graph: from the two accepting states, count all completions of each
remaining original length. It then enumerates just the 196,488 accepted original
words in lexicographic order, checking strict order so none is duplicated.
Each word is replayed through the unchanged `panel/cert33.py`, using its bit-plane
interface to carry all the original words in one exact batch.

Every one passes the eight prescribed guards and reaches the same endpoint,

```text
2132030322103030303032.
```

All then emit `01` and fail the following update. Consequently

```text
C_14(00001111) = C_14(000011110) = C_14(0000111101),
```

and all have cardinality 196,488. Those two extra scalars are switches and add
no repeats. This particular family cannot develop into a violation of `2^D`.

One original word is `20100011110201`; the artifact includes additional examples
and the SHA-256 of all accepted original words, sorted and separated by newlines:

```text
bc943be8087ba68c4bb94b503ee31ac0ac1506621f2d0a042c2ccecced31c02d
```

The deterministic enumerator retains the entire finite witness family in
reproducible form. Independent replay certifies a sufficiently large family
even without relying on completeness of the count; (7) and the completion
recurrence supply completeness as well.

## 7. Reproduction, costs, and remaining scope

Run from the project directory with Python and NumPy:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/cumulative_history_transfer.py
```

Code: [cumulative_history_transfer.py](../../experiments/rule30/cumulative_history_transfer.py).
Saved certificate: [cumulative-history-transfer.json](../../experiments/rule30/cumulative-history-transfer.json).

The default certificate checks 2,796,192 inverse edges, 1,530 small membership
controls against the independent oracle, and the 32,802 coefficient inequalities.
The separate witness check replays all 196,488 accepted originals, including
their common continuation and death, in eleven oracle calls. NumPy is used for
array indexing and integer sums; unbounded counts use Python integer object
arrays. No floating-point value is used in a proof comparison. State sizes,
spatial cutoffs, and wall time are bounded; a cap raises an inconclusive error,
and the result is written only after all checks succeed.

The work ran locally in seconds, with no paid compute, GPU, or seed regeneration.
It did not rerun the existing length-1-through-12 original-frontier census.
The small oracle controls validate the new representation, and the large oracle
batch validates only the new explicit witness family. Existing research files
and the frozen oracle were preserved.

For an unrestricted bound with **c=1**, the witness forces
`epsilon <= log2(2^24/24561)/6 = 1.569319719...`. It gives no such ceiling when
an arbitrary prefactor c is allowed: a single finite witness can be absorbed by
c. In particular, no positive-rate bound with arbitrary c has been refuted.

The remaining gap is temporal uniformity. The graph has exponentially many
states in n, and this certificate supplies no relation between arbitrary
signatures' repeat counts and their probabilities before a suitable spatial
cutoff. It supplies neither a finite repeat budget for fixed r nor a bound on
arbitrarily long plateau histories. Any counterexample to `2^D` must now have
at least ten scalar symbols; the existing complete census independently requires
its original length to exceed twelve. The unrestricted inequality, finite-frontier
mortality, and the consequent period-two exclusion remain open.

**Follow-up, 2026-09-11.** The
[history-transfer mixing theorem](RESULTS-history-transfer-mixing.md) now proves
strong connectivity and spatial mixing at every temporal depth, with an
explicit all-depth spatial cutoff. It also proves the `2^D` candidate for
arbitrarily long tapes with D<=6, using a sharp nine-symbol probability
envelope. The unresolved regime still fixes the original length and permits
arbitrarily many subsequent repeats.

**Longer-history follow-up, 2026-09-11.** The
[weighted endpoint report](RESULTS-weighted-history-endpoints.md) refutes the
unrestricted extension with c=1 and epsilon=3/2. Its length-24 witness has
55,885,140 ancestors, D=15, and eight repeats with an unchanged entire ancestor
set. It lowers the necessary unrestricted c=1 exponent ceiling to
`(47-log2(55885140))/15 = 1.4176025745...`. The bounded-tape sharp theorem above
is unchanged. An exact weighted endpoint identity retains every original and
guard; a reconstruction corollary shows that after r successful updates all
further nonempty prescribed extensions keep the entire original class.

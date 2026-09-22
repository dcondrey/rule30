# A sharp all-length base case for information in the original low bits

Date: 2026-09-11. **The unrestricted cumulative counting inequality remains
open.** This continuation proves mortality and an exact information estimate
for an infinite family of original frontiers. It also refutes a proposed
row-by-row one-bit encoding and identifies a weaker row-conditioned estimate
whose base case is now proved.

**Follow-up:** the proposed extension (H) to arbitrary high rows is now
[refuted already at k=2](RESULTS-sparse-high-history-obstruction.md).
The all-length k=1 theorem and all finite observations below remain valid.

All states are auxiliary legal Z frontiers. No singleton-seed reachability,
arbitrary-period exclusion, or P2 result is asserted. All counts below retain
the original length and every actual chronological guard.

## 1. Proved: a uniform bound at every original length

**Theorem.** Let r>=1. If every nonterminal original high bit is one,

\[
 a_0=\cdots=a_{r-2}=1,
\]

with the usual legal-origin requirement a_0=1, then every trajectory has

\[
 \boxed{N\le16,\qquad D\le8.}                           \tag{1}
\]

The final original high bit and **all r original low bits are unrestricted**.
At r=1 the legal high bit is one. Thus the theorem covers 2^(r+1) originals
at each r>=2, without an upper bound on r. It is an all-length restricted-family
theorem, not a larger initial-frontier census.

Both constants are sharp. If all high bits are one, b_0=1, and

\[
 r\equiv4056\pmod{4096},
\]

the complete successful tape is `0100111100000101`: N=16 and D=8, followed by
a failed update. The other r-1 original low bits can be chosen freely.
For example, the explicit original word `3` repeated 4056 times realizes it.
At r=984 the same all-high-ones construction emits `0100111100000`, also
with eight repeats, and then fails.

The proof uses a complete guarded spatial-period certificate. It does not
infer a periodic moving boundary from periodic fixed prefixes.

## 2. An exact erasure lemma for any fixed original high row

For a fixed legal original high row a, define

\[
 V(a)=\{0\}\cup\{i:1\le i<r,\ a_{i-1}=0\},\qquad
 k(a)=|V(a)|.
\]

Call these the visible low-bit positions. Define F_a(alpha) to be the set of
original low rows whose actual trajectory with high row a emits alpha. Let
E_a(alpha) count the assignments to the k(a) visible low bits that do so,
setting the other original low bits to zero for this evaluation.

**Erasure lemma.** For every r, a, and finite chronological tape alpha,

\[
 \boxed{|F_a(\alpha)|=2^{r-k(a)}E_a(\alpha).}             \tag{2}
\]

**Proof.** At input site i>=1, if a_(i-1)=1 then
`previous_a OR b_i=1`, independently of b_i. Thus this b_i affects neither
running bit, any emitted symbol, nor the terminal guard. At site zero, b_0
can matter. Fixing a and the low bits in V(a) therefore fixes the entire
first update, including whether it fails and its emitted scalar. All later
states and guards are then identical. Each assignment to V(a) represents
exactly 2^(r-k(a)) original low rows. This proves (2), including the empty tape.

In particular the original count has the exact decomposition

\[
 |C_r(\alpha)|
   =\sum_{a:\,a_0=1}2^{r-k(a)}E_a(\alpha).              \tag{3}
\]

This uses original input bits, not arbitrary current predecessors. No later
episode or completion is substituted for the actual first update.

The family in section 1 is exactly the k(a)=1 case: zeros are allowed only
at the last high-bit position, where they have no following low bit to expose.

## 3. The finite certificate proves the all-length statement

First suppose every high bit is one. By (2), only b_0 matters. If b_0=0, the
first bulk output alternates `21`; its two terminal bits differ at every
length, so the first guard fails. If b_0=1, the whole first update is identical
to that of the explicit original `3^r`. Its first bulk output alternates `30`.

For the latter family, use the common depth-n column record from the
[history-transfer theorem](RESULTS-cumulative-history-transfer.md):

\[
 q=(A_0,A_1,B_1,\ldots,A_n,B_n).
\]

Reading each further original symbol 3 defines a deterministic spatial map
F_n on records with A_0=1. Its orbit starts at
`o_1=(1,1,1,...,1,1)`. The terminal record for original length r is the
(r-1)-st iterate of this orbit. The complete signature sigma(alpha) is the
previously proved necessary and sufficient test for every guard in alpha.

The orbit can be constructed one temporal level at a time. If its lower
levels have period p, the new pair, written (A,B), has a known periodic drive
and updates as

\[
 B'=B\oplus\kappa_i,\qquad
 A'=A\oplus(B'\lor\eta_i),
\]

where kappa_i and eta_i are fixed by the lower levels. Over one lower period
this is an affine triangular permutation

\[
 (A,B)\longmapsto(A\oplus\lambda B\oplus\mu,\ B\oplus\nu).
\]

Its fourth power is the identity. Therefore the lifted orbit closes within
four lower periods. The checker finds the first return and verifies every
edge separately using the full column recurrence. This is an exact finite
orbit, not an extrapolated period.

The accepted length residues are as follows. Residue zero means positive
multiples of the displayed period, not the illegal length-zero word.

| Successful steps n | Spatial period | Residue of r: successful tape |
|---:|---:|:---|
| 1 | 2 | `1:1`, `0:0` |
| 2 | 4 | `1:10`, `0:01` |
| 3 | 8 | `0:010` |
| 4 | 32 | `16:0101`, `24:0100` |
| 5 | 64 | `16:01011`, `24:01001` |
| 6 | 64 | `16:010111`, `24:010011` |
| 7 | 64 | `16:0101110`, `24:0100111` |
| 8 | 128 | `80:01011101`, `88:01001111` |
| 9 | 256 | `208:010111010`, `216:010011110` |
| 10 | 256 | `208:0101110100`, `216:0100111100` |
| 11 | 256 | `216:01001111000` |
| 12 | 256 | `216:010011110000` |
| 13 | 1024 | `216:0100111100001`, `984:0100111100000` |
| 14 | 2048 | `1240:01001111000010`, `2008:01001111000001` |
| 15 | 4096 | `3288:010011110000100`, `4056:010011110000010` |
| 16 | 4096 | `4056:0100111100000101` |
| 17 | 4096 | none |

The empty seventeenth row proves N<=16 at **every positive original length**.
Checking D on the retained tapes gives D<=8 and the sharp examples above.

Now allow the last original high bit to be zero, with r>=2. Directly in the
first scan, its last low bit is still erased. If r is even, the first guard
fails. If r is odd, the first scalar is b_0. For b_0=1 the first image equals
the all-high-ones first image, so it is already covered. For b_0=0 a second
certificate follows the periodic column orbit from `o_0`, then reads one final
original symbol 0. It retains the full chronological signature, now with
original terminal high A_0=0. Its periods through depth 10 are

```text
2, 8, 16, 32, 64, 64, 64, 256, 256, 256.
```

At depth 9 its only accepted length residue is r=145 modulo 256, with tape
`010010011`. At depth 10 none remains. This sector has N<=9 and D<=3 at all
lengths; the artifact gives every accepted intermediate residue. These cases
exhaust k(a)=1 and prove (1).

## 4. Independent verification, including the period seams

The maintained [certificate](../../experiments/rule30/constant_high_history_certificate.py)
and [artifact](../../experiments/rule30/constant-high-history-certificate.json)
contain two different checks of the all-length result.

The first is the column-orbit and signature calculation above. The independent
engine uses the unchanged frozen `panel/cert33.py` for bulk scans and actual
finite-frontier trajectories; it does not call the column transition, orbit
lift, origin constructor, or signature constructor.

For `3^r`, the independent engine scans a block of length 4096 through 17 bulk
iterations. At each iteration the input starts in symbol 3 and the output
ends in symbol 0. This closes the period seam: the last output resets both
running bits, and the next input's low bit one masks the preceding input high.
Thus the next copy of the block scans identically, including the initial seam.
Induction proves that 4096 is a common spatial period of all 17 bulk rows.

For the sector-zero prefix, blocks have length 256 and start in symbol 2.
The corresponding checked seam condition is that the output ends in
`(u,v)=(0,last_input_high)`. Reading the next first symbol 2 then gives `(1,0)`,
exactly as at the origin. This independently closes all ten period seams.

The engine also directly replays one complete original for every length
residue: `3^r` for r=1,...,4096, and the terminal-zero sector-zero originals
for r=2,...,257. It compares every successful prefix and every failed guard
with the tables. Joint bulk-column periodicity and the complete signature
theorem extend these exact finite checks to all original lengths. This last
guard step is essential; periodic bulk prefixes alone would not suffice.

## 5. A proved sharp base case for a weaker information bound

Condition on a fixed original high row in the k(a)=1 family, and choose its
original low row uniformly. Every nonempty successful tape has probability
exactly 1/2: only b_0 is visible, and the first successful scalar distinguishes
its two values whenever both can survive. All other tapes have probability zero.

Together with D<=8 this proves, for **every r and every high row with k(a)=1**,

\[
 \boxed{|F_a(\alpha)|\,2^{D(\alpha)/8}\le2^r.}           \tag{4}
\]

The exponent 1/8 is sharp when the prefactor is one, attained by the eight-repeat
examples. In particular, a proposed high-row-conditioned one-bit estimate is
false: at r=984 the conditional probability is 1/2 and D=8, giving weighted
probability 128. No c=1 conditional exponent greater than 1/8 can hold for all
high rows. A finite example does not rule out larger prefactors.

**Former candidate, now refuted at k=2.** Require (4) for every legal
original high row a, equivalently

\[
 \boxed{E_a(\alpha)\,2^{D(\alpha)/8}\le2^{k(a)}.}        \tag{H}
\]

If (H) were proved, summing (4) over the 2^(r-1) high rows would give

\[
 |C_r(\alpha)|\le2^{2r-1-D(\alpha)/8},
\]

a sufficient unrestricted information bound with c=1 and epsilon=1/8.
Also, E_a>=1 on a realized history would give D<=8k(a). These are explicitly
**conditional implications**. The proof above supplies the k(a)=1 base case.
The [subsequent counterexample](RESULTS-sparse-high-history-obstruction.md)
has k=2, conditional probability 1/4, and D=18, so (H) fails. In fact the
first guarded scalar already fixes every visible low bit when k=2; later
repeats impose no further low-row filtering in a surviving class.

The original unconditioned one-bit candidate remains the active stronger
target. The sufficient route through (H) cannot be completed as stated; its
failure does not change the ancestor domain or refute the original target.

## 6. The opposite row-by-row one-bit encoding also fails

Fix instead the original low row

```text
110110101010111001111101
```

at r=24. There are 2^23 legal choices of the original high row. At least 1664
of them emit the complete tape `00011100001111111100`, with D=15. Therefore

\[
 \frac{1664\,2^{15}}{2^{23}}=\frac{13}{2}>1.             \tag{5}
\]

Thus it is also false that fixing all original low bits always leaves enough
high-bit information to charge one bit per repeat. This does not refute the
unconditioned one-bit bound. The failure of (H) is a separate result in the
[sparse-high report](RESULTS-sparse-high-history-obstruction.md).

The [verifier](../../experiments/rule30/fixed_low_history_obstruction.py)
constructs 1664 distinct original words with that exact low row, then
**individually replays all of them through all 20 guards and the subsequent
failure** using the frozen oracle. Their complete list and hashes are in the
[artifact](../../experiments/rule30/fixed-low-history-obstruction.json).
For (5), this directly verified subset suffices; no assumption that arbitrary
current predecessors share the required history enters the argument.

## 7. Bounded test of the next visible-bit case

The [one-high-zero probe](../../experiments/rule30/one_high_zero_information_probe.py)
tests (H) at every location of a single original high zero, for 48 selected
lengths near the explicit long-history witnesses. It covers 402,528 effective
low-parameter cases, representing all original low rows for each of those
fixed high rows by (2). The frozen oracle propagates the cases in bit planes;
576 separate scalar trajectories check the encoding.

No tested case violates (H). The largest eighth power of its weighted
conditional probability is 1/16, at r=943 with a high zero at index 212,
tape `01111111111111`, D=12, and conditional probability 1/4. The
[artifact](../../experiments/rule30/one-high-zero-information-probe.json)
records all selected lengths and maxima. This is finite evidence only.
The later k=2 counterexample at r=46735 lies outside these selected lengths
and refutes the all-length version of (H).

Run the maintained checks from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/constant_high_history_certificate.py
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/fixed_low_history_obstruction.py
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/one_high_zero_information_probe.py
```

They ran locally in seconds. Time and lifetime limits raise errors, never
mortality verdicts. No paid compute, GPU work, singleton-seed regeneration,
or rerun of the earlier length-1-through-12 census was used. The unrestricted
one-bit inequality, any unrestricted positive-rate bound, and finite-frontier
mortality remain unproved and unrefuted.

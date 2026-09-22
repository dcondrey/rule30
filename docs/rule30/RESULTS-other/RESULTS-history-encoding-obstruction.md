# Cumulative history information exceeds coordinate deletion and affine rank

Date: 2026-09-11. **Two proposed proof mechanisms are refuted; the counting
inequality remains open.** The same chronological ancestor class obstructs
both deleting D original coordinates and obtaining D independent affine
constraints on the original bits. The obstruction uses 59 explicit legal
original words, each independently replayed through every guard.

These statements concern auxiliary Z reconstruction states. They make no
singleton-seed reachability claim and do not settle mortality, the period-two
exclusion, arbitrary periods, or P2.

## 1. The original class and the two questions

Use the already established class

\[
 C=C_{24}(\alpha),\qquad
 \alpha=00011100001111111100=0^3 1^3 0^4 1^8 0^2,
 \qquad D(\alpha)=15.
\]

The free original coordinate vector has m=47 bits, ordered as

\[
 x=(b_0,a_1,b_1,\ldots,a_{23},b_{23}).                 \tag{1}
\]

The legal origin high bit a_0=1 is not a free coordinate. Every member of C
starts at this same length and survives all twenty prescribed updates.

Two sufficient ways to prove the proposed counting estimate would be:

1. Find a coordinate set J, depending on r and alpha, such that projection
   onto J is injective on C and |J|<=m-D=32.
2. Exhibit D=15 independent affine equations over GF(2) satisfied by every
   original in C. Their common solution space would contain at most 2^(m-D)
   original assignments.

Neither mechanism exists for this C. This rules out their universal use for
the one-bit inequality. It does not refute arbitrary encodings, parity
readouts, adaptive coordinate queries, nonlinear constraints, or the inequality.

## 2. At least 39 coordinates must be retained

**Projection obstruction.** If the restriction of a coordinate projection
`pi_J` to C is injective, then |J|>=39. In particular, no choice of fifteen
original coordinates can simply be deleted while retaining a unique original.
The retained set may depend on the whole tape; the conclusion still applies.

**Proof.** For each bit index in the set

\[
 S=\{2,5\}\ \cup\ \{8,9,\ldots,40\}\ \cup\ \{42,43,44,46\},
 \qquad |S|=39,                                      \tag{2}
\]

the certificate supplies two legal original words x_i,y_i in C with

\[
 x_i\oplus y_i=e_i.                                  \tag{3}
\]

Here e_i is the unit vector for the indexing (1). If i is omitted from J,
these two distinct originals have the same projection. Hence every i in S
must belong to J, proving the claim.

The block of 33 consecutive indices 8 through 40 alone is already enough
to rule out a 32-bit coordinate projection. The complete list gives the
stronger lower bound 39. For example, the pair at bit 2 is

```text
300322220010000202222220
310322220010000202222220
```

Both emit the full tape alpha. They differ only at b_1. The witness file
gives all 39 pairs, including the less immediate changes farther right.

This argument is about one fixed projection identifying **every** original.
The pairs need not share a common center. It therefore does not establish
a lower bound of 39 on adaptive bit queries along a single original's path.
No such adaptive lower bound is claimed.

## 3. At most six independent affine equations can hold

**Affine-rank obstruction.** The affine hull of C in GF(2)^47 has dimension
at least 41. Consequently the coefficient vectors of affine equations valid
on every original in C span a space of dimension at most six. Fifteen
independent affine history constraints are impossible.

**Proof.** The certificate contains 42 originals x_0,...,x_41 in C. Exact
Gaussian elimination gives

\[
 \operatorname{rank}\{x_j\oplus x_0:1\le j\le41\}=41. \tag{4}
\]

If an affine equation `ell(x)=c` holds throughout C, subtracting its value at
x_0 shows that ell annihilates every vector in (4). The annihilator of this
41-dimensional direction space has dimension 47-41=6. All coefficient
vectors of universally valid affine equations lie in that annihilator.
This proves the bound without enumerating C or assuming any constraint
independence.

The maintained verifier proves the dimension **lower bound** needed here.
The obstruction does not rely on an upper bound for the full affine hull.
Including the fixed legal coordinate a_0 would add a known equation and an
ambient coordinate simultaneously; it would not provide another bit of
history information relative to the legal-original universe.

This does not prohibit a linear map with nonlinear inverse from being
injective on C. Affine equations defining a containing affine space and linear
readouts distinguishing a nonlinear subset are different requirements.

## 4. The information is present, but these representations miss it

The [weighted endpoint report](RESULTS-weighted-history-endpoints.md) already
proved the complete count

\[
 |C|=55\,885\,140,\qquad 2^{25}<|C|<2^{26}.
\]

Thus membership in C carries strictly more than 47-26=21 bits of counting
information under the uniform legal-original measure. The candidate asks
for only fifteen bits, and this class satisfies it:

\[
 \frac{|C|2^{15}}{2^{47}}=\frac{13971285}{1073741824}<1.
\]

Nevertheless a fixed coordinate projection requires at least 39 retained
bits, and affine equations can supply at most six independent restrictions.
The distinction is substantial: an unrestricted binary label for this finite
class requires only 26 bits, while a coordinate projection requires at least
thirteen more. Counting cannot in general be replaced by deleting an equal
number of original bits, even when the deletion positions are chosen using
the complete chronological history.

The previous exact count is reused here; it is not recomputed by this
verifier. Neither obstruction theorem needs that count. They follow already
from membership and linear algebra on the explicit originals. If an encoding
argument is pursued further, it must allow more than the two mechanisms
excluded above.

## 5. Exact certificate and independent verification

- [history-encoding-obstruction-witnesses.json](../../experiments/rule30/history-encoding-obstruction-witnesses.json)
- [history_encoding_obstruction.py](../../experiments/rule30/history_encoding_obstruction.py)
- [history-encoding-obstruction.json](../../experiments/rule30/history-encoding-obstruction.json)

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/history_encoding_obstruction.py
```

The 39 coordinate pairs and 42 affine-independent originals overlap; there
are only 59 distinct initial words. A direct implementation of the stated Z
scan replays each word. The unchanged `panel/cert33.py` independently replays
all 59 in bit planes. The verifier compares every entire bulk output, terminal
pair, emitted scalar, and guard. All twenty target updates succeed; the next
update fails for every witness. There are 1,239 original-update comparisons
across 21 frozen bit-plane calls. The deaths are an additional control, not
an assumption needed by either obstruction proof.

It then verifies every unit difference in (3), the 41 pivots in (4), and the
numerical gap between 39 required projection bits and the proposed 32. It
records source hashes for the witness list, verifier, frozen oracle, and
the earlier count artifact. The saved run takes under a tenth of a second
locally and has a 30-second replay cap.

The existing exact original-variable BDD counter was used to discover the
witnesses. The maintained proof checker does not import that engine or rely
on its proposed membership sets. It needs no SAT solver, BDD package, NumPy,
original-frontier census, GPU, or paid computation. Successful continuation
of an arbitrary current endpoint is never substituted for original ancestry.

## 6. Status of the main target

The unrestricted inequality `|C_r(alpha)|*2^D <= 2^(2r-1)` remains unproved
and unrefuted, as does the existence of a suitable uniform positive-rate
substitute. The two-run length bound explored in this continuation also
remains unproved; reconstructed origin and short-prefix consistency alone
did not provide its missing original ancestry.

This result eliminates two precise compression arguments on the actual
chronological domain. It supplies neither a uniform cumulative repeat bound
nor a new mortality theorem.

**Follow-up, 2026-09-11.** The
[history-locality report](RESULTS-history-locality-obstruction.md) constructs
a nonlinear 32-bit code for this entire length-24 class, using the allowed
values on six disjoint original-bit blocks. Their product is
3,857,168,160<2^32. This is compatible with both obstructions above. The same
report proves that bounded-arity support predicates cannot give a uniform
positive-rate count bound: for each fixed tape, sufficiently long originals
have full projections onto every bounded set of original bits.

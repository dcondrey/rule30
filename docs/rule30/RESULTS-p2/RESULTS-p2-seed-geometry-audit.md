# P2: an exact origin criterion and the limits of boundary/history data

Date: 2026-09-11. **An exact all-length origin criterion and an obstruction
to a specific certificate class; no singleton cancellation estimate.**

The outstanding question is what information from the singleton origin can
actually force cancellation. I tested a concrete proposed repair to the
earlier universal discrepancy arguments: keep the exact seed boundary
geometry, a growing central history, and the entire current right half.
This still does not force cancellation. There are alternative finite rows
with all those data, obeying Rule 30 autonomously, whose next prescribed
block is any binary word.

The result strengthens the scope of the existing
[boundary-transfer obstruction](RESULTS-boundary-ensemble-transfer-obstruction.md).
Its construction does not require infinite initial tails or external driving.
Both moving edge strips agree with the seed **forever**, including the
mandatory left-edge nonlinear defect. The competing rows have the same
exact expanding support endpoints as the seed, indexed from the construction's late
starting time. They are not generated from the singleton at time zero.
That last distinction is exactly the origin information this certificate
class has discarded.

There is a positive way to express the discarded condition precisely:
a row with support endpoints [-n,n] is the actual seed row x^n **if and
only if it has n successive finite-support predecessors**. The resulting
origin deficit is invariant under Rule 30 and excludes every altered
competitor below. This characterizes the seed orbit; it does not yet
connect that characterization to a discrepancy estimate.

## 1. Precise theorem

Write x^t=F^t(delta_0) for the actual seed evolution, and fix integers

\[
d\ge2,\quad h\ge0,\quad T\ge1,\quad a\ge h+T+d.
\]

For every prescribed binary word w_1,...,w_T, there exists a finite row y,
with evolution y^r=F^r(y), satisfying all of the following:

1. At the construction's initial time, y agrees with x^a on [-h,infinity).
   It can differ only at the T positions
   \(-h-1,-h-2,\ldots,-h-T\).
2. For every r>=0, its extreme occupied positions are exactly
   \(-a-r\) and \(a+r\). For j=0,...,d-1, both inward edge strips agree:
   \[
   y^r_{-a-r+j}=x^{a+r}_{-a-r+j},\qquad
   y^r_{a+r-j}=x^{a+r}_{a+r-j}.
   \]
3. Its central history agrees with the actual seed through relative time h:
   \(y^r_0=x^{a+r}_0\) for 0<=r<=h. More strongly,
   \[
   y^r_i=x^{a+r}_i\quad\text{whenever }i\ge r-h.
   \]
   In particular, at the observation cut r=h its **entire nonnegative
   half-row** agrees with the seed row x^(a+h).
4. Its next T center bits are precisely the prescribed ones:
   \[
   y^{h+j}_0=w_j,\qquad 1\le j\le T.
   \]

In particular, choosing w identically zero or identically one gives signed
discrepancy +T or -T on the future block. This is an exact finite-block
statement for alternative autonomous rows. It neither gives a constant
infinite tail nor contradicts the established exclusion of such tails for
finite Rule 30 rows.

## 2. Why both moving edge strips remain exact forever

For a row with extreme support [-b,b], use inward depths

\[
A_j(r)=y^r_{-b-r+j},\qquad E_j(r)=y^r_{b+r-j},
\]

and set negative-depth entries to zero. Direct substitution in Rule 30
gives

\[
A_j(r+1)=A_{j-2}(r)\oplus\big(A_{j-1}(r)\lor A_j(r)\big),
\]
\[
E_j(r+1)=E_j(r)\oplus\big(E_{j-1}(r)\lor E_{j-2}(r)\big).
\]

Each prefix of d depths is a closed subsystem: no deeper cell enters its
update. Therefore equality of these prefixes at one time propagates for
every later time, independently of the bulk. This is a closure fact, not
an assertion that the two edge dynamics are the same or linear.

Both extreme cells stay one, and zeros remain outside their radius-one
cones. The support endpoints are consequently exact. Since d>=2, the
leftmost adjacent pair is also the actual seed's pair 11 at every time.
Thus the forced defect used in the
[Thue-Morse response identity](RESULTS-duhamel-left-edge-thue-morse.md)
is preserved by this construction; knowing that defect does not distinguish
the competing future blocks.

## 3. Constructive proof of the arbitrary future

Start with y=x^a and keep every nonnegative site fixed. For each n>=1,
the initial bit y_-n cannot affect the center before relative time n.
At time n its only fastest path uses the left parent at every update.
Rule 30 is XOR-permutive in that parent, so

\[
(F^n y)_0=y_{-n}\oplus G_n(y_{-n+1},\ldots,y_n).
\]

The function G_n does not involve any more negative initial position.
This is the same triangular coding principle as the earlier boundary
analysis, applied at the actual late seed row x^a.

Leave sites -1,...,-h unchanged. Successively for n=h+1,...,h+T,
choose y_-n to give the requested center bit w_(n-h). Each choice affects
none of the already specified center bits. Leave every remaining initial
position equal to x^a. This constructs y explicitly and proves items 1
and 4.

The altered positions lie strictly inside the two preserved edge strips:
the innermost position of the left strip is -a+d-1, whereas
\(-h-T\ge-a+d\). Hence both strips agree initially, and Section 2 proves
item 2 for all time. Finite propagation gives item 3 because the backwards
cone of a cell (r,i) uses initial positions i-r,...,i+r; all these positions
lie in [-h,infinity) when i>=r-h.

The argument retains actual seed values wherever it promises agreement.
It does not replace those values with independent or random boundary bits.
Its only freedoms are the explicitly listed T interior positions.

## 4. What this rules out, with growing scales allowed

Let the observation cut have nominal seed age n=a+h. The size requirement
becomes

\[
n\ge2h+T+d.
\]

Suppose a proposed proof at that cut remembers:

- that the preceding h steps are a legal Rule 30 evolution with exact
  seed support endpoints;
- the actual seed's central h+1-bit history;
- the entire actual right half at the cut;
- both exact moving d-deep edge tapes, including their entire future.

A bound based only on these requirements must allow the constructed rows.
For h=h(n)=o(n) and d=d(n)=o(n), choose T=floor(n/2). The inequality above
holds for all sufficiently large n, while the possible signed discrepancy
is exactly T. Thus those requirements cannot establish even a uniform
sublinear bound on macroscopic future intervals.

This already allows arbitrary growing sublinear memory and edge depth;
the obstruction is not an artifact of a square-root cutoff. It is also
stronger than merely observing a periodic nonseed configuration: the
competitors share the specified actual seed data and have no driven cells.

The conclusion is narrowly scoped. A certificate that propagates an
additional global invariant from **all the initial singleton zeros** need
not admit these rows. Nor have we constructed one fixed competing row
with biased blocks at arbitrarily late times. A different y is allowed
for each prescribed block, exactly as needed to refute an estimate
uniform over the stated data class. This is not a disproof of the
singleton's P2 statement or of every possible induction from its origin.

## 5. A positive criterion: maximal finite ancestry identifies the seed

Let y be a nonzero finite-support row with support endpoints [-n,n].
Define d_fin(y) to be the greatest number of successive Rule 30
predecessors that all have finite support. Then

\[
\boxed{0\le d_{\rm fin}(y)\le n,\qquad
d_{\rm fin}(y)=n\iff y=x^n.}
\tag{8}

**Proof.** Every nonzero finite-support row expands each support endpoint
outward by exactly one under Rule 30. Thus a finite predecessor of y
must have endpoints [-n+1,n-1]. After n such steps the only possible
nonzero ancestor is the singleton at zero. Conversely, x^n has its n
actual seed predecessors.

Moreover, Rule 30 is injective on finite-support rows. If u and v differ,
let b be their rightmost differing position. Their next rows differ at
b+1, because that output is the XOR-permutive left parent and the two
right parents agree. Hence Fu != Fv. There can therefore be at most one
finite predecessor at each stage, and

\[
d_{\rm fin}(Fy)=d_{\rm fin}(y)+1.
\]

Consequently the nonnegative integer

\[
\boxed{\mathcal A(y)=n-d_{\rm fin}(y),\qquad
\mathcal A(Fy)=\mathcal A(y)}
\tag{9}

is an invariant on centered finite rows of odd support width. It is zero
exactly on the singleton orbit. Reversing until no finite predecessor
remains gives a unique ancestral core, with support width
2 A(y)+1. This is a global origin constraint, not one deduced from
the edge tapes or from the center's imbalance.

The constraint is restrictive at every finite depth. For n>=1 and
0<=h<n, exactly

\[
2^{2(n-h)-1}
\]

of the 2^(2n-1) rows with endpoints [-n,n] admit h finite predecessors.
Indeed, each ancestor has fixed endpoint ones at ±(n-h), with 2(n-h)-1
arbitrary interior bits; finite injectivity bijects these ancestors to
their h-step outputs. The fraction is 4^(-h). At h=n the sole output is
x^n. This counting fact does not give a probability law for the seed or
establish that low-discrepancy rows occupy the admitted set.

The inverse checker computes the four witnesses' exact depths:

| Starting age a | Cut age n=a+h | Prescribed future | Actual finite ancestry at cut | Origin deficit |
|---:|---:|---|---:|---:|
| 64 | 72 | 32 zeros | 12 | 60 |
| 64 | 72 | 32 ones | 10 | 62 |
| 128 | 144 | 64 zeros | 22 | 122 |
| 128 | 144 | 64 ones | 24 | 120 |

Their edge tapes and remembered histories agree as stated, but they fail
the exact origin invariant by large margins. This explains constructively
why they are excluded from the actual singleton orbit.

Equation (8) is equivalent to full seed-origin membership, and its direct
implementation reconstructs that origin. It is not a cheaper cancellation
criterion or a new asymptotic bound. A useful next theorem would have to
exploit A=0 to control imbalance or energy, rather than merely rewriting
the orbit condition in terms of ancestry. No such estimate is proved here.

## 6. Consequence for the remaining proof work

The missing link is more precise than “use the seed boundary.” Exact
boundaries can coexist with arbitrary finite center futures once the
interior's connection to time zero has been forgotten. A useful proposed
invariant must distinguish x^(a+h) from these explicit alternatives using
some further constraint inherited from the singleton origin.

In particular, edge-driven mixing, the mandatory Duhamel source, or a
sublinear verified predecessor depth cannot silently supply this distinction. Such
methods may still be useful if their state includes a proven global
origin constraint. Section 5 provides an exact such constraint, but no
quantitative cancellation consequence. The results here characterize
which omitted condition excludes the witnesses; they do not advance an
asymptotic bound toward the prize conclusion.

## 7. Exact verification and witnesses

Run from the repository root:

```sh
uv run --no-project python experiments/rule30/p2_seed_geometry_audit.py
```

The [dependency-free checker](../../experiments/rule30/p2_seed_geometry_audit.py)
constructs all 1,134 prescribed-tail cases with h=0,1,2, d=2,3,4 and
T=1,...,6 at the minimum permitted age a=h+T+d. It checks every binary
tail in these ranges, not sampled tails. A separately implemented scalar
truth-table evolution replays both the actual seed and each alternative
row and verifies 139,752 edge comparisons, the full rows, the support,
the mandatory left defect, the exact past, and the prescribed future.
Every case passes. Closed edge formulas are also checked on every binary
prefix through width eight.

The inverse checker solves from right to left using the permutive parent
and then verifies the complete forward image. An independent scalar
truth-table image census checks all 1,024 endpoint-fixed finite rows
through width 11, including rows with no finite predecessor. It also
checks d_fin(x^n)=n for every n=0,...,128 and verifies the exact origin
deficit invariance along every constructed witness's remembered history.

Four larger explicit witnesses, including their complete initial rows in
hexadecimal and the locations of every changed bit, are stored in the
[JSON certificate](../../experiments/rule30/p2_seed_geometry_audit.json):

| Starting seed age a | Seed history h | Edge depth d | Prescribed future T | Signed sums |
|---:|---:|---:|---:|---:|
| 64 | 8 | 8 | 32 | +32 and -32 |
| 128 | 16 | 16 | 64 | +64 and -64 |

The all-length claims follow from the algebraic proofs, not from extending
these finite checks beyond their tested ranges. No existing source or
artifact was edited by this audit.

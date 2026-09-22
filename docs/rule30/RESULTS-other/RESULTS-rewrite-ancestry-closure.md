# Original-ancestor rewrites across a two-update merger

**Status: two local rewrite identities and a disjoint-choice counting theorem
are proved for every original length. No positive-rate relation to cumulative
repeats is proved. Both proposed uniform ancestor inequalities remain open,
and period two is not excluded.**

This extends the [lower multiplicity proof attempt](RESULTS-lower-multiplicity-proof-attempt.md).
The new three-symbol identity connects original ancestors whose first images
have different high rows. The previous two-symbol identity cannot do that.
The enlarged rules connect three specified complete history classes, including
the 60-member class that the previous rule split into three components.
Connectivity of every two-update fiber is a separate conjecture, tested here
only through original length seven.

**Subsequent resolution:** the
[canonical-ancestor certificate](RESULTS-canonical-merger-capacity.md) now
proves that connectivity at every length. It also refutes the unit-rate
counting claim inside a single two-step component: one complete component
has 108 originals while its full tape has nine repeats. A four-update
identity repairs that infinite family. The unrestricted positive-rate
bound and mortality remain open; the finite observations below are retained.

All words are legal finite **auxiliary** frontiers, with first high bit one.
Their original length remains fixed. No word is claimed to be a frontier from
the singleton seed. The statements concern P1; they give no P2 conclusion.

## 1. Scan notation and the two-symbol identity

Let B be the bulk scan in the question, with no terminal guard or append.
Write its memory as `(u,v,p)`, where p is the preceding input high bit. B(P)
and B(B(P)) start with memory `(0,0,0)`. Their terminal memories determine
the incoming memories when a block is placed after the original prefix P.

**Theorem T.** Suppose a nonempty legal prefix P has first scan memory
`(1,c,0)`, where c is either bit. For any bit a and any suffix S, the three
originals

```text
P (1-c) (2a)   S
P (2+c) (2a)   S
P (2+c) (2a+1) S
```

have identical complete successful scalar histories, with the same failure
time if finite. If their first two updates succeed, their second Z-images
coincide. In particular, membership in every chronological `C_r(alpha)` is
equivalent for these three originals.

**Proof.** The first scan gives the following table.

| Input block | First bulk output | First exit memory |
|---|---|---|
| `(1-c) (2a)` | `13` | `(1,1,a)` |
| `(2+c) (2a)` | `03` | `(1,1,a)` |
| `(2+c) (2a+1)` | `03` | `(1,1,a)` |

The suffix therefore scans identically. The first terminal guard and scalar
coincide, including when S is empty; on success the appended symbol coincides.

B(P) ends in symbol `2+c`, so the second incoming memory has the form
`(U,V,1)`. For either displayed first output, the second block output is

```text
2(U XOR V XOR 1) + (V XOR 1),  2(U XOR V) + V,
```

with exit memory `(U XOR V,V,1)`. This holds for both U and both V. Thus
the full second scans, guards, scalars and appends coincide. Determinism
then gives every later update. Failure on either earlier step is also
simultaneous. This proves the theorem.

The earlier theorem covered only c=0. The c=1 instance is needed, for example,
to connect `2000001` with `2003001` and `2003101`: the prefix `200` has
first memory `(1,1,0)`.

**A limitation of all these two-symbol moves.** The output blocks `13` and
`03` have the same high row. Consequently T preserves the entire high row
of the first image. Moving within a one-step original fiber also preserves
that row. Any composition of these operations retains this invariant.
They cannot connect two originals whose first-image high rows differ.

There is also an exact finite classification of the following specified
class of two-symbol rules: unchanged first exit memory, and identical second
output and exit memory for **every** second running-bit pair `(U,V)`, with
the second preceding high fixed by the first incoming u. Among all eight
first incoming memories and sixteen input blocks, the only equivalence
classes containing distinct first outputs are the four T classes
`(c,a) in {0,1}^2`. The verifier checks all 512 second block scans. This
classifies that rule class; it does not classify longer rewrites or rules
conditioned on the second running bits.

## 2. A three-symbol identity that changes first-image high bits

**Theorem B.** Suppose a nonempty legal prefix P has first scan memory
`(1,c,0)` and second scan memory `(U,0,1)`. For any symbol x in `{0,1,2,3}`
and any suffix S, the following originals have identical complete successful
histories and the same second Z-image whenever two updates succeed:

```text
P (1-c) 0 x         S
P c     0 (x XOR 1) S
```

Here `x XOR 1` toggles the low bit of x. The condition on the second running
low bit is essential to this identity. Both prefix conditions are obtained
from the actual original prefix; no predecessor or completion is substituted.

**Proof.** Write `x=2a+b`, and set

```text
H = b AND (1 XOR a),  L = 1 XOR b,  y = 2H+L.
```

Scanning the two alternative blocks from `(1,c,0)` gives

| Input block | First bulk output | First exit memory |
|---|---|---|
| `(1-c) 0 x` | `1 3 y` | `(H,L,a)` |
| `c 0 (x XOR 1)` | `2 2 y` | `(H,L,a)` |

From second incoming memory `(U,0,1)`, both first outputs give

```text
2(U XOR 1)+1,  2U,  2(U XOR 1)+1,
```

with second exit memory `(U XOR 1,1,H)`. As in theorem T, equality of
both exit memories preserves the remaining suffix scans, both terminal
guards, their scalars, and the appended symbols. The second images agree;
all subsequent updates therefore agree. This proves the theorem.

For a concrete application, `P=200` has the two required memories
`(1,1,0)` and `(1,0,1)`. Taking x=0 and suffix `1` gives

```text
2000001  <-->  2001011.
```

These are both original ancestors of the full tape `0001101011`. Their
first images have different high rows, so theorem T and one-step fiber
changes alone could never connect them. This identity removes that specific
obstruction.

## 3. A rigorous way to count simultaneous choices

**Disjoint-choice theorem.** Let w belong to `C_r(alpha)`. Suppose w contains
p applicable B blocks and q applicable T blocks whose original symbol
intervals are pairwise disjoint. Then

```text
|C_r(alpha)| >= 2^p * 3^q.
```

**Proof.** Both rules preserve both outgoing scan memories. Applying an
earlier block choice leaves the prefix conditions at every later disjoint
block unchanged. Thus all choices can be made independently, and each
preserves the complete chronological history. Two different choice vectors
differ on at least one selected interval, where their input blocks differ.
The map from choice vectors to legal originals of length r is injective.

The theorem requires disjoint symbol intervals. Some larger families, such
as the exact `2*3^4` parametrization in the earlier length-ten result, can
also be counted injectively using disjoint **bit coordinates** and a separate
proof of applicability. The existence of overlapping rewrite opportunities
alone does not justify multiplying their sizes.

For unrestricted compositions, the safe finite object is a graph on original
words. Its vertices are the words themselves, so cycles and overlapping
rewrite paths never produce duplicate ancestors in the count.

## 4. Exact graphs and their scope

For two successful scalars gamma and a second image z, define

```text
E_2(r,gamma,z) = { w legal of original length r :
                  the first two guarded updates emit gamma and Z^2(w)=z }.
```

On this set put edges between originals in the same complete one-step
fiber, and edges for T and B wherever their actual prefix conditions hold.
All edges preserve `E_2`. Any later prescribed continuation from z either
retains every member of `E_2` or rejects every member. This is a graph of
original ancestors with the first two guards retained, rather than a graph
of arbitrary current predecessors.

The following are exact finite results on previously certified complete
chronological classes. Every original was replayed through its full tape.

| r | Full tape | Original class size | One-step fibers plus old T (c=0) | Plus T (c=1) | Plus B |
|---:|---|---:|---|---|---|
| 6 | `1011100` | 36 | 36 | 36 | 36 |
| 7 | `0001101011` | 60 | 6, 18, 36 | 18, 42 | 60 |
| 10 | `000101111100` | 162 | 162 | 162 | 162 |

The last three columns list connected-component sizes, not numbers of
paths. In the length-seven row, the generalized T connects the 6- and
36-member components; B then joins the remaining 18 ancestors.

**Finite connectivity observation.** Every `E_2` through original r=7 is
connected under the full catalog.

| r | Originals surviving two steps | Nonempty two-step fibers |
|---:|---:|---:|
| 1 | 1 | 1 |
| 2 | 0 | 0 |
| 3 | 8 | 2 |
| 4 | 36 | 3 |
| 5 | 130 | 8 |
| 6 | 528 | 17 |
| 7 | 1,844 | 37 |

This tests 10,922 legal originals for **two updates only**, finding 68
nonempty fibers and no disconnected one. It tests the newly specified
rewrite catalog; it does not extend the mortality census. Connectivity
for arbitrary r is unproved. Even uniform connectivity would not by itself
give a lower bound on fiber size or a relation to later repeats.

## 5. What would turn this construction into a mortality proof

For a nonempty complete history class, a sufficient target is an injectively
encoded family of originals of size `2^p*3^q`, together with universal
constants epsilon>0 and K such that

```text
p + (log_2 3) q >= epsilon D(alpha) - K.
```

This would imply `|C_r(alpha)| >= 2^(epsilon D-K)`. Since there are only
`2^(2r-1)` legal originals, it would bound D, and the already proved repeat
lower bound would bound the tape length. This is a **conditional implication**,
not a new bound. The displayed target need not use disjoint local blocks if
another injective encoding is proved.

The missing statement is a cumulative charging theorem: enough distinct
original choices must be available to pay for repeats, with bounded reuse
across scalar switches. It cannot require a new choice to appear at every
repeat. The unchanged 36-member class in the earlier audit accrues three
repeats without changing any original ancestor, so choices available earlier
must be allowed to pay for later repeats.

There are two precise obligations for this particular route:

1. Establish an original-word construction with a decoder, or an exact
   component-count formula, that continues to work when applicable blocks
   overlap. Uniform connectivity of the defined `E_2` graph is one concrete
   subproblem, with a counterexample consisting of one disconnected fiber.
   It would explain the coverage of these moves, but would not establish
   their number.
2. Prove a positive lower rate for that construction in D, allowing choices
   acquired before a run of repeats to pay for it. No such rate is currently
   proved for this catalog, for all second-image fibers, or for the complete
   chronological class. If the catalog cannot supply it, deeper mergers must
   be handled on original ancestors with every earlier guard retained.

The proved contribution is a larger family of valid original-word moves and
an injective counting theorem under an explicit disjointness condition. The
rate in item 2 remains the central mathematical obstacle; neither more local
identities nor finite connectivity observations alone remove it.

## 6. Exact verifier

Maintained files:

- [rewrite_ancestry_certificate.py](../../experiments/rule30/rewrite_ancestry_certificate.py)
- [rewrite-ancestry-certificate.json](../../experiments/rule30/rewrite-ancestry-certificate.json)

```text
uv run --no-project python experiments/rule30/rewrite_ancestry_certificate.py
```

The verifier checks all 48 cases in T's local table and all 32 cases in B's
table, the complete specified two-symbol catalog, the three stored complete
history classes, and the two-step connectivity observation. For the latter,
both updates are compared against the unchanged frozen `panel/cert33.py`
oracle. Every generated graph neighbor must be an original vertex with the
same two guarded scalars and second image. Union-find counts distinct
vertices. A disconnected fiber would be saved as a witness.

The new default has original-length cap seven, temporal depth two, and a
30-second wall cap. The saved run completed without hitting a cap. Source
hashes, finite component counts, and local tables are retained in the JSON.
The old census and symbolic history trees were not rerun. No GPU, seed
regeneration, paid compute, or BlindMind rerun was used.

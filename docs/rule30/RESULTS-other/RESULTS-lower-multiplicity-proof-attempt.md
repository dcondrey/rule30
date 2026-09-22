# Attempt to prove the lower original-ancestor bound

**Status: the unrestricted inequality `|C_r(alpha)| >= 2^D(alpha)` remains
unproved and unrefuted. Period two is not excluded.** The result below is an
explicit, all-length rewrite of original words that preserves their entire
successful scalar history, including every guard. It supplies a real way
to move between different first-image fibers. It does not yet give enough
independent choices in terms of cumulative repeats.

The exact length-ten class that led to this rewrite also refutes three
stronger proposed constructions: obtaining D independently erased original
low bits, obtaining a D-dimensional coordinate cube of original bits, and
obtaining `2^D` ancestors in one optimally selected first-image fiber.
These are failures of proof mechanisms, not counterexamples to the counting
inequality itself.

All words here are legal finite **auxiliary** Z states. No word is asserted
to occur at the singleton seed's frontier. Original length is fixed in
every history class. P2 and arbitrary periods are outside this result.

## 1. An all-length rewrite preserving complete original ancestry

Let B be the total bulk scan, omitting the final guard and appended symbol.
Let P be a nonempty legal original prefix such that its first bulk scan
finishes in memory

```
(u,v,previous_a) = (1,0,0).
```

Equivalently, the last input high bit of P is zero and B(P) ends in symbol
2. This condition is checked by scanning P; it refers to no future lifetime.
For example P=`30` and P=`301111` both qualify.

**Rewrite theorem.** Fix any bit a and any finite suffix S, possibly empty.
The three legal originals of the same length

```
w0 = P 1 (2a)   S
w1 = P 2 (2a)   S
w2 = P 2 (2a+1) S
```

have identical successful scalar tapes, including the same failure time
if one occurs. More precisely, their first guards and emitted scalars
agree; if the first two updates succeed, their second Z-images coincide.
Consequently, for **every** finite chronological tape alpha and their
common original length r,

```
w0 in C_r(alpha)  <=>  w1 in C_r(alpha)  <=>  w2 in C_r(alpha).
```

Their first images need not coincide. Thus this is an actual operation
between original ancestors across a later merger, rather than a choice
of arbitrary predecessors at a later frontier.

**Proof.** Scan just the two displayed input symbols from memory `(1,0,0)`.

| Input block | First bulk output | Exit memory |
|---|---|---|
| `1 (2a)` | `13` | `(1,1,a)` |
| `2 (2a)` | `03` | `(1,1,a)` |
| `2 (2a+1)` | `03` | `(1,1,a)` |

The suffix S therefore scans identically in every case. The last bulk
output is the same, even for empty S, so the first terminal guard and
scalar are the same. On success the same birth symbol is appended.

The first images differ only in the low bit of the first displayed output
cell: symbol `1` versus `0`. The preceding output cell is the terminal
symbol `2` of B(P), whose high bit is one. At the next scan that differing
low bit is erased by `previous_a OR b=1`. The differing cell's high bit
is zero in both cases. All later scan memories and output cells therefore
coincide. The second guard, scalar, and appended symbol coincide as well.
Determinism gives all subsequent guards and scalars. A failure on either
of the first two steps also occurs simultaneously. This proves the claim.

For a separate local check, let `(U,V,1)` be the second scan's incoming
memory at the block. Its third component is one because B(P) ends in 2;
U and V are unrestricted. All three blocks produce the same second bulk
output

```
2(U XOR V XOR 1) + (V XOR 1),   2(U XOR V) + V,
```

and exit memory `(U XOR V,V,1)`. The verifier checks all 24 cases: two a
values, four `(U,V)` values, and three input blocks.

**Independent disjoint rewrites.** If one original has k nonoverlapping
applicable two-symbol blocks, independently choosing any of the three
forms at each block gives `3^k` distinct originals with exactly the same
history. An earlier rewrite leaves its exit memory unchanged, so it does
not invalidate the first-scan condition at any later disjoint block.
Distinct choices change disjoint input positions, giving injectivity.

This is a proved lower bound in an explicitly checkable block count.
There is **no proved lower bound on k in terms of D**, nor a proof that
combining these moves with the known one-step fibers always yields `2^D`
distinct originals. That is the remaining difficulty for this mechanism.

## 2. A complete class needing more than independent bit flips

**Exact finite proposition.** For

```
r = 10,
alpha = 000101111100,
D = 7,
```

the complete original class has

```
|C_10(alpha)| = 162 = 2 * 3^4.
```

Every member has at most five nonterminal original high bits equal to
one. The largest coordinate cube contained in this class has dimension
five, hence 32 words. Its two first-image fibers have sizes 54 and 108.
Both fibers merge at the second update. Thus

```
largest coordinate cube = 32 < 128,
largest first-image fiber = 108 < 128,
complete original class = 162 >= 128 = 2^D.
```

The global lower bound survives this example. It is false that it can
always be witnessed by D independently variable original bit positions,
even allowing both high and low bits, or by a single first-image fiber.
A general injection of `2^D` choices need not be a coordinate cube.

### Exact binary/ternary parametrization

Set

```
T = {(0,1), (1,0), (1,1)},
U = {(0,1,0), (1,0,0), (1,0,1)}.
```

Choose independently

```
z in {0,1},
(p,p'), (q,q'), (s,s') in T,
(t,t',t'') in U.
```

Then the complete class consists exactly of the words `w_i=2a_i+b_i` with

```
a = (1,0,p,0,q,0,t,s,0,1),
b = (1,z,1,p',1,q',t',t'',s',0).
```

The parameters occupy disjoint original bit coordinates, so this is a
bijection, with `2*3^4=162` members. The `(t,t',t'')` choice changes the
original symbols at positions 6 and 7 by the theorem in section 1, with
the second symbol's high bit s fixed. The preceding six-symbol prefix
has the required scan memory for all choices of z,p,q. The other three
ternary factors and z supply one-step ambiguities.

The nonterminal high count is `1+p+q+t+s<=5`, with equality attainable.
For any coordinate cube in this product, the projection onto each
three-element factor has dimension at most one: a two-dimensional cube
would require four points. The z factor contributes at most one further
dimension, giving the upper bound five. Choosing `p=q=t=s=1` leaves the
five original low bits at positions 1,3,5,7,8 independently free, attaining
that bound. An independent exhaustive cube recursion verifies the same
maximum from the complete set of 162 originals.

### First images and merger

| Parameter case | First image | Original ancestors |
|---|---|---:|
| t=0 | `32103213203` | 54 |
| t=1 | `32103203203` | 108 |

Every one of these originals has second image

```
303121030303.
```

For example, original `3011111012` has t=0, while the local replacements
`3011112012` and `3011112112` have t=1. All emit exactly alpha and then
fail on their next update.

The first-image counts also follow from the established exact inverse
product formula: the respective `(N_up,N_down,q)` values give
`2*3^3=54` and `2^2*3^3=108`. The verifier independently generates every
legal one-step predecessor of each displayed first image and checks that
the two fibers partition the full original class.

## 3. Verification and bounded observations

Maintained files:

- [lower_multiplicity_certificate.py](../../experiments/rule30/lower_multiplicity_certificate.py)
- [lower-multiplicity-certificate.json](../../experiments/rule30/lower-multiplicity-certificate.json)
- [lower_multiplicity_probe.cpp](../../experiments/rule30/lower_multiplicity_probe.cpp)
- [lower-multiplicity-search.json](../../experiments/rule30/lower-multiplicity-search.json)

Default exact verification:

```
uv run --no-project python experiments/rule30/lower_multiplicity_certificate.py
```

For the complete-class proposition, the unchanged frozen
`panel/cert33.py` runs in bit planes with one lane for every one of the
`2^19` original legal length-ten words. At every chronological step the
live mask retains both the guard and prescribed scalar. This proves
completeness of the 162-member class without trusting the BDD that found
it. All 162 words are then replayed individually through all twelve
successful updates and the subsequent failed guard, with a second local
scan comparison on every successful update. The artifact stores every
word, every prefix count, the local rewrite table, and source hashes.

The exploratory max-high program weights **original** high-bit variables
on the existing guarded BDD; it never substitutes a current predecessor.
It found the false max-high lemma above. Bounded symbolic history trees
then looked directly for a counterexample to the lower count. All saved
complete trees passed. Combined with the previous small test, the bound
has finite support through original length 18. These newer tree results
are observations from the existing symbolic counter, not a uniform
theorem or an independent whole-range oracle census. The earlier targeted
subtrees are included in later complete trees and are not additional
independent evidence.

The search used the existing 5,000-node visit and 60-step limits, with
3–6-second local query caps. No query hit a cap. No seed data, GPU work,
paid compute, or rerun of the old original-by-original census was needed.
The saved JSON also records an unsuccessful 64-word single-insertion
probe; it generated no qualifying long-history class and supplied no
evidence for a theorem.

To reproduce the saved symbolic trees, without increasing their scope:

```
uv run --no-project python experiments/rule30/lower_multiplicity_certificate.py --replay-symbolic
```

The all-length result of this attempt is the explicit ancestry-preserving
rewrite. The count-to-repeat relation is still missing. Neither the new
lower-bound conjecture nor the original upper-bound conjecture is proved,
and no new Rule 30 period exclusion follows.

The subsequent [original-ancestor rewrite extension](RESULTS-rewrite-ancestry-closure.md)
generalizes the two-symbol rule to both low-memory phases and proves a
three-symbol rule that changes first-image high bits. It also states the
mixed disjoint-choice counting theorem and tests a precisely defined
two-update fiber graph. The cumulative rate in D remains unproved.

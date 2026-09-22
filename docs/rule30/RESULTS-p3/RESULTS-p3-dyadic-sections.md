# Exact dyadic sections of the singleton right-edge map

Date: 2026-09-13. Status: exact section evaluator and two precise obstructions
proved. **No sublinear center-query algorithm is established.**

This investigation constructs the powers of

```text
G(x) = x XOR ((x<<1) OR (x<<2)),       c_n = bit_n(G^n(1)),
```

through a shared expression for their ordered binary sections. The expression
is built from n, without a supplied row or orbit table. Its current evaluation
still makes n section advances, so it fails the repository's conservative
[P3 target](P3-SCOPE-AUDIT.md). Two exact results identify shortcuts that do
not repair it: an isometric affine conjugacy is impossible, and successive
full sections along the actual seed cannot repeat before the center query.

This concerns computation of dyadic iterates. It does not revive the
[retired ergodicity argument](overnight/RESULTS-anashin.md), whose stationary
distribution statements do not control the diagonal center bit.

## 1. Three exact binary sections

Process the binary input from low bits to high bits. The raw memory consists
of the two previous input bits. Memories10 and11 have identical behavior,
giving exactly three states A,B,C, where A=G:

| State | Root output | Section at input0 | Section at input1 |
|---|---|---|---|
| A | input bit | A | C |
| B | complemented input bit | A | C |
| C | complemented input bit | B | C |

In conventional recursion notation,

```text
A=(A,C),       B=(A,C) swap,       C=(B,C) swap.
```

The recursion is exact at every input length, including infinite 2-adic
inputs. At a raw memory `(a,b)`, the next input bit z emits
`z XOR(a OR b)` and changes memory to `(z,a)`. The table is the exact
quotient of those eight local transitions. A differs from B,C on input0;
B and C differ on the two-bit input00. Thus the three reachable states are
distinct as complete binary transducers.

Their integer actions are also explicit:

```text
A(x)=G(x),
B(x)=G(x) XOR1,
C(x)=G(x) XOR(3-2*(x AND1)).
```

The last two expressions change only the first two output bits. They follow
directly by comparing initial raw memories with00.

## 2. Ordered word sections and a constructive shared expression

Here a word UV lists generators in chronological application order: U acts
first, then V. Let p(U) be its root-bit toggle, the parity of its B and C
letters. For either input bit b, its exact section satisfies

```text
section(UV,b)
  = section(U,b) section(V,b XOR p(U)),
p(UV)=p(U) XOR p(V).
```

Proof: U passes the bit `b XOR p(U)` to V, and their actions on the remaining
tail compose in that same order. This argument proves the identity for every
word, not merely the seed controls.

Equivalently, scan an explicit generator word with one running bit b. At A
or B append A if b=0, otherwise C. At C append B if b=0, otherwise C. After
each letter, toggle b exactly when that letter is B or C. The ordering is
essential.

There are some cheap seed-specific substitutions:

```text
A^n --input1--> C^n,
C^n --input0--> (BC)^(n/2)                   when 2 divides n,
(BC)^(n/2) --input0--> (AC)^(n/2),
(AC)^(n/2) --input0--> (ABCC)^(n/4)          when 4 divides n.
```

The implementation retains these repetitions as a straight-line program:
leaves are A,B,C and each internal node concatenates two previously defined
words. Exact tuple interning shares identical children; memoization stores
`(node,input bit) -> section node`. The displayed section law transforms a
node recursively without first expanding its word.

**Exact query algorithm.** Construct A^n by binary powering of concatenation,
which needs O(log n) initial grammar nodes. Feed input1, followed by n zeros.
At each position read the root toggle to obtain its output bit; retain only
the section needed for the next position. Output the bit at position n.
Induction using the section law proves that this is `bit_n(G^n(1))` for
every n. All intermediate grammar construction is part of the algorithm.

**Cost.** The current algorithm performs exactly n section advances and
consumes n+1 seed bits, including the known zeros. Sharing can reduce the
work within an advance, but it does not remove those n advances. Expanding
an n-letter word gives an upper bound of O(n) binary-tree operations per
advance, hence O(n^2) grammar operations and storage overall. Deterministic
comparison-tree dictionaries give O(n^2 log n) operations on
Theta(log n)-bit words. No improved Turing-machine bound follows.

The tiny control n=32 constructs 9 initial nodes and 205 total nodes, with 246
distinct section subqueries and 32 advances. These are fully charged
construction counts, not a scaling fit or evidence for an asymptotic shortcut.

## 3. An exact obstruction to affine conjugacy

The first changed bit in a dyadic seed return is

```text
d_k = v_2(G^(2^k)(1)-1).
```

The exact small values include

```text
G^4(1)=401=0x191,           d_2=4,
G^8(1)=102849=0x191c1,      d_3=6.
```

**Theorem.** There is no binary-prefix-compatible bijection H:Z_2->Z_2
satisfying `H(G^t(1))=F^t(H(1))` for every t>=0, where
`F(z)=a*z+b` is an odd affine map on Z_2.
This excludes finite-state synchronous bit-serial conjugacies in particular;
it does not assume H has finitely many states.

Proof: a compatible bijection induces a permutation at each finite binary
precision. It therefore preserves the first differing bit of every pair:
`v_2(H(x)-H(y))=v_2(x-y)`.

For an affine map and m=2^k, direct composition gives

```text
F^(2m)(z)-z = (1+a^m)*(F^m(z)-z).
```

For odd a and k>=1, `a^(2^k)=1 mod8`, so `v_2(1+a^(2^k))=1`.
Every finite return depth must therefore increase by exactly one on the
next doubling. A zero return remains zero; it cannot match the displayed
finite returns. The actual change4→6 contradicts the required4→5. QED.

This is a seed-return obstruction, distinct from nonergodicity. It leaves
nonisometric codings, nonaffine arithmetic maps, and other powering methods
untreated.

The stronger tentative seed identity `d_k>=2^k` already fails at k=3.
A bounded 64-bit probe also records d_10=27 at time 1024. Those later values
are finite observations, not a growth law for d_k.

## 4. Why full-section cycle skipping cannot reach the center

For every positive integer x whose highest one is at position d, G(x) has
its highest one at d+2. The term x<<2 supplies that bit, while neither x nor
x<<1 can cancel it. In particular,

```text
highest_one(G^n(1)) = 2n.
```

For n>=1 let S_(n,j) be the section of G^n after reading the actual seed
prefix `1 0^(j-1)`, with j>=1. Its value on the remaining zero tail is

```text
S_(n,j)(0) = floor(G^n(1)/2^j).
```

For 1<=j<=2n, this value is nonzero and has highest one at 2n-j. Therefore
all these sections are pairwise different, even under the weaker equivalence
that only compares their complete output on the zero tail. A repeated full
section cannot occur early enough to skip to position n.

This rules out cycle detection on full seed-ray sections as the missing
sublinear step. It does not rule out manipulating unequal sections in bulk,
or a smaller equivalence that retains only the particular finite output
observable needed by the query. The highest bit used to distinguish the
sections is generally beyond the requested center bit; it is exactly the
extra information retained by the stronger section representation.

There is a related limitation on positive-word normalization. Each A,B,C
raises the highest one of an arbitrary positive input by two. Thus positive
generator words of different lengths cannot define the same complete map,
and no all-input identity shortens an n-letter section to fewer positive
letters. This test uses full actions on positive inputs, not only the
singleton query at precision n+1. It does not exclude an SLP, a circuit,
inverses, or a precision-dependent quotient.

## 5. Verification, scope, and the remaining obligation

The saved verifier checks the eight raw memory transitions, all three
state-distinguishing inputs, 96 controls for the boundary formulas, the
displayed ordered substitutions, seven standalone SLP center queries
against independent whole-row evolution, the affine factorization, and
the 16 distinct seed-ray sections for n=8. The 64-bit dyadic-return probe
stops at time 1024 and does not generate a long center-column prefix.
The full run takes under a millisecond in the saved artifact.

An independent read-only audit checked the state quotient, chronological
composition and seed substitutions, affine obstruction, full-section
distinction, and the ordered prefix passed to the second child. No
mathematical gap was found; the stated limitations remain essential.

Files:

- [Exact SLP query evaluator and verifier](../../experiments/rule30/p3_dyadic_sections.py)
- [Certificate, paid query counts, and retained falsifier](../../experiments/rule30/p3-dyadic-sections.json)

```sh
uv run --no-project python experiments/rule30/p3_dyadic_sections.py --output /tmp/p3-dyadic-sections.json
uv run --no-project python experiments/rule30/p3_dyadic_sections.py --query 32
```

The precise missing query operation is

```text
jump0(node,m) = root_toggle(section_(0^m)(node)).
```

The input node is the already constructed finite SLP, and m is binary encoded.
For n>=1 the desired query is exactly

```text
c_n = jump0(section(A^n,1), n-1).
```

The current implementation computes this by m sequential section advances.
An accelerator would need to compute only the displayed toggle without those
m advances, with all additional construction included in its cost. The
full-section no-cycle theorem does not refute such an operation.

The obstruction to immediately closing it on two child toggles is explicit.
For a chronological concatenation UV,

```text
section_(0^m)(UV)
  = section_(0^m)(U) section_(prefix_m(U(0^infinity)))(V).
```

The second child receives the ordered m-bit output prefix of the first, not
another zero input. Constructing that prefix explicitly takes linear work;
the exact single-bit section law alone supplies no way to consume it
implicitly in sublinear time. An exact operation retaining this dependency,
while computing only the required toggle, remains open. No such operation
is presented as implemented here, and neither P3 nor any period exclusion
is proved.

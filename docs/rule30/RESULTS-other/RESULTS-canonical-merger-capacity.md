# Canonical ancestors, a counting obstruction, and a four-update repair

**The general mortality route is unfinished.** This investigation proves
all-length connectivity of the proposed two-update rewrite graph, but refutes
the unit-rate counting bound inside one such component. A new four-update
identity repairs the exhibited infinite family. There is still no universal
positive-rate bound in cumulative repeats, and period two is not excluded.

Neither unrestricted conjecture

```text
|C_r(alpha)| * 2^D(alpha) <= 2^(2r-1),
|C_r(alpha)| >= 2^D(alpha)  when C_r(alpha) is nonempty
```

is proved or refuted here. C always counts all **original** legal length-r
words satisfying every chronological guard. All states are auxiliary
frontiers; none is asserted to arise from the singleton seed. P2 and arbitrary
periods are outside this result.

The follow-up [scope audit](AUDIT-counting-route-scope.md) distinguishes
survival information from survivor multiplicity and proves that canonical
forms still contain arbitrary binary block sequences. It also explains why
the family repair below did not resolve the missing general repeat bound.

## 1. The overlap problem has an all-length solution

Recall the two-step original fiber

```text
E_2(r,gamma,z) = { w legal of original length r :
                  the first two guarded scalars are gamma and Z^2(w)=z }.
```

The [previous report](RESULTS-rewrite-ancestry-closure.md) put edges within
complete one-step original fibers and for its local T and B identities.
Only bounded connectivity had been checked.

**Canonical-ancestor theorem.** Every nonempty E_2 is connected under these
edges, at every original length. The decreasing local rules below have one
irreducible in E_2, which is its lexicographically least original word.

This proves coverage of the graph even when moves overlap. It does not
relate the number of its vertices to subsequent repeats.

### Decreasing rules

Use symbol order `0<1<2<3`. Every changed position is strictly after the
legal origin. In addition to T and B, use two elementary operations within
a first-image fiber:

* **E:** if the preceding original high bit is one, lower the current low
  bit from one to zero. The OR masks this bit, so the entire first image
  is unchanged.
* **F:** if the current original high bit is one and its first emitted low
  bit is one, lower that original high bit to zero. If a following input
  cell exists, set its low bit to one. The current high is masked by the
  emitted low; the next OR remains one. After the next cell the first-scan
  memory is unchanged. At the terminal cell the high can be lowered directly,
  since its effect is masked and no later original cell needs compensation.

Both operations preserve the first guard, scalar, and full first image.
They therefore preserve every later guard and state. F changes a possible
later low bit, but its first changed symbol decreases by two, so the whole
word decreases lexicographically.

Orient T toward its smallest block:

```text
(2+c) (2a+b)  ->  (1-c) (2a),
```

where the first incoming memory is `(1,c,0)`. Orient B toward its smaller
first symbol:

```text
1 0 x  ->  0 0 (x XOR 1),
```

where the first incoming memory is `(1,c,0)` and the second incoming running
low is zero. These are the already proved identities, for either c. They
preserve the first two guarded scalars and second image, and hence the entire
successful history. Every reduction preserves original length and decreases
the original word. Thus reduction terminates on the finite set of length-r
words.

### A finite certificate for uniqueness at every length

After a prefix, store the five-bit column

```text
q = (p,u,v,U,V),
```

where p is its last original high bit, `(u,v)` its first bulk terminal pair,
and `(U,V)` its second bulk terminal pair. Reading `x=2a+b` gives

```text
v' = v XOR (p OR b),       u' = u XOR (v' OR a),
V' = V XOR (u OR v'),      U' = U XOR (V' OR u'),
q' = (a,u',v',U',V').
```

The emitted second bulk symbol is `2U'+V'`. The omitted second preceding
high is u, so there is no missing memory coordinate.

Irreducibility is recognized by this column plus four possible pending
flags. After the legal origin:

1. Reject a symbol if E or F applies immediately.
2. A possible T at this symbol becomes a rejection if any next symbol is read.
3. A possible B at this symbol becomes a rejection if a zero and then any
   further symbol are read.

The pending flags are `none`, `T awaiting a next symbol`, `B awaiting zero`,
and `B awaiting a third symbol`. Every flag is allowed at the end of a word:
a required but absent following symbol cannot complete a rewrite. The checker
spells out all transitions. This is a finite automaton with at most 128
column/flag states, not an extrapolation from short words.

The final two guards have a particularly simple form. The first succeeds
with scalar s_0 exactly when `u=v=s_0`. Its appended symbol has high one
and low `1-s_0`. Scanning this symbol in the second row changes `(U,V)` to
`(U XOR 1,V XOR 1)`. Thus the second guard succeeds exactly when `U=V`, with
`s_1=1-U`. On success the two symbols beyond the second bulk prefix are
`3s_1, 3-s_1`.

Run two copies of the irreducible automaton with equal second bulk output
at every position, and record whether their original inputs have ever
differed. Their legal first symbols must agree, since the first second-row
symbol is the original symbol `2+beta`. A compatible final pair requires

```text
u = v = u_other = v_other,   U = V.
```

Equal output already makes the two upper pairs identical. This final test
therefore retains both guarded scalars as well as the second image.

**Exact closure certificate:** the reachable product has 74 vertices and
123 labeled edges. None of its compatible terminal vertices has the
different-input flag set. The artifact stores the entire closed graph.
Induction on word length shows that every pair of irreducibles with equal
second output occurs in this graph. The terminal check therefore excludes
two distinct irreducibles in the same E_2 at **any** length.

Every original reduces inside its E_2 to an irreducible, and the irreducible
is unique. This proves the theorem. The global lexicographic minimum must
itself be irreducible, identifying the canonical representative.

### Exact counting and decoding

Given gamma and z, the irreducible automaton has one accepted original path
when E_2 is nonempty. Finite-state dynamic programming therefore decodes its
canonical representative. To count every ancestor, use the unrestricted
32-column automaton instead, with integer path weights. Keep only edges
whose second output equals the corresponding symbol of z, restrict the first
input to 2 or 3, and at the end sum weights satisfying

```text
u=v=s_0,   U=V=1-s_1.
```

Together with the required two final symbols of z, this counts exactly E_2.
It keeps original length and both guards. Overlapping rewrite paths never
enter the count.

There can still be later mergers: the distinct irreducibles `3000002` and
`3000110` emit `001` and have the same third image `3210321032`, but their
second images are `303030303` and `303031303`. The theorem does not say that
all mergers happen within two updates.

## 2. Complete two-step capacity does not pay one bit per repeat

Use word-repetition notation and define, for **every** integer k>=0,

```text
w_k = 30111111 0^k 01,       r=k+10.
```

**Constant-fiber theorem.** The first two scalars are `10`, and

```text
Z(w_k)   = 32103210 0^k 032,
Z^2(w_k) = 30312100 0^k 0303,
|E_2(r,10,Z^2(w_k))| = 108.
```

All 108 members even have the same first image. Arbitrarily composing the
old and enlarged two-update rewrite catalog therefore produces exactly
these 108 originals, by the canonical-ancestor theorem.

### Complete original parametrization

Let `T={(0,1),(1,0),(1,1)}`. Choose independently a bit z and three pairs
`(p,p'),(q,q'),(t,t')` in T. Form the eight-symbol prefix with rows

```text
a = (1,0,p,0,q,0,t,0),
b = (1,z,1,p',1,q',1,t').
```

There are `2*3^3=54` such prefixes. Append k zeros and either `01` or `03`.
These are exactly the 108 original ancestors in the indicated two-step
fiber, with no length change between members of that fiber.

**Proof of completeness.** The first eight second-output symbols are
`30312100`. Exact inverse paths in the 32-column machine give precisely
the 54 displayed prefixes, each ending at column zero. This finite prefix
calculation is exhaustively verified.

There is a useful uniform reset identity: any two consecutive second bulk
output zeros end at column zero, whatever the incoming column. For the
second of these zeros, the old upper pair is zero; the new upper low zero
forces the old first high and new first low to be zero, and the new upper
high zero forces the new first high to be zero. These first pairs then
force the new original high to be zero. All five exit bits are zero.
From column zero, the only input producing another second output zero is
symbol zero. The entire inserted gap is consequently forced on every
original ancestor, not just on the displayed representative.

From column zero the remaining two second bulk symbols `03`, together
with first scalar one, have exactly the original suffixes `01` and `03`.
This proves completeness and the count `54*2=108` for every k.

### Exact counterexample to the two-step unit-rate claim

At k=1536 the actual complete successful tape is

```text
r = 1546,
w = 30111111 0^1536 01,
alpha = 100101111100000,
N = 15,   D = 9,
```

followed by a failed guard. Consequently

```text
|E_2(r,10,Z^2(w))| = 108 < 512 = 2^D(alpha).
```

Every member of this E_2 has the same full tape, since it has the same
second image and earlier scalars. Thus even complete, overlapping closure
of the two-update moves cannot supply 512 original choices from this
component. This is an obstruction to the proposed unit-rate construction,
not an assumed failure of independence.

A smaller explicit instance is k=256, original length 266, with complete
tape `1001011111110`, D=7, and `108<128`. Both full guarded trajectories
are checked against the frozen independent oracle. The stronger witness's
entire 108-member fiber is also checked in parallel oracle lanes.

## 3. The family does not refute all weaker rates

**Sharp all-gap theorem.** For every k>=0, w_k has

```text
N <= 17,   D <= 9.
```

The repeat maximum is attained at k=1536; the lifetime maximum is attained
at k=5704, with tape `10010011001011011`. These are all-gap bounds, not
observations through a selected maximum k.

For clarity, here is the exact spatial-period certificate. At temporal
depth n, start at the column produced by prefix `30111111` and iterate the
fixed input symbol zero. The table lists every residue of k that survives
all n guarded updates after the final `01` is read.

| n | Exact spatial period | Accepted gap residues: chronological tape |
|---:|---:|---|
| 1 | 1 | `0:1` |
| 2 | 1 | `0:10` |
| 3 | 2 | `0:100` |
| 4 | 4 | `0:1001` |
| 5 | 8 | `0:10010` |
| 6 | 32 | `0:100101`, `8:100100` |
| 7 | 64 | `0:1001011`, `8:1001001` |
| 8 | 64 | `0:10010111`, `8:10010011` |
| 9 | 128 | `0:100101111`, `72:100100110` |
| 10 | 256 | `0:1001011111`, `72:1001001100`, `200:1001001101` |
| 11 | 512 | `0:10010111110`, `72:10010011001`, `256:10010111111`, `328:10010011000` |
| 12 | 512 | `0:100101111100`, `72:100100110010`, `256:100101111111` |
| 13 | 1024 | `256:1001011111110`, `512:1001011111000`, `584:1001001100101` |
| 14 | 2048 | `1280:10010111111100`, `1536:10010111110000`, `1608:10010011001011` |
| 15 | 4096 | `1536:100101111100000`, `1608:100100110010110`, `3328:100101111111001` |
| 16 | 4096 | `1608:1001001100101101`, `3328:1001011111110010` |
| 17 | 8192 | `5704:10010011001011011` |
| 18 | 8192 | none |

**Why the finite certificate proves all k.** At a new temporal level the
top pair is driven by the already periodic lower column. Over one lower
period it undergoes an affine triangular permutation

```text
(A,B) -> (A XOR lambda*B XOR mu, B XOR nu).
```

Its fourth power is the identity. The checker lifts the actual orbit,
finds its first return, and verifies every edge including that return.
Induction proves each complete spatial cycle. Every nonnegative k is
therefore represented by its residue.

For each residue the fixed suffix `01` is read in the same full column.
The established complete signature of a tape tests every guard, including
the growing birth suffix. Only extensions of an already surviving residue
are retained. The empty eighteenth row excludes every k. The frozen oracle
independently checks all 18 bulk rows across two whole copies of the common
8192-column period, as well as actual guarded trajectories covering every
surviving residue listed above.

In particular, this family cannot justify an assertion of unbounded D at
constant two-step capacity. A bound of the form

```text
|E_2| >= 2^(epsilon*D-K)
```

would have to satisfy `K >= 9*epsilon-log_2(108)` on this family. For K=0,
it requires `epsilon <= log_2(108)/9`. It does **not** rule out every positive
epsilon with an arbitrary fixed K. Such a universal weaker bound remains
unproved.

## 4. A four-update identity supplies the missing choices for this family

The previous obstruction concerns two-step components. There are explicit
valid original moves across a later merger.

Use the column convention

```text
q_4 = A_0 + SUM_(j=1..4) (2A_j+B_j) 2^(2j-1).
```

The prefix `30111111` has q_4=32. This specifies original preceding high
zero and the four incoming scan memories

```text
(0,0,0), (0,0,0), (0,1,0), (0,0,0).
```

**Four-update block theorem.** From these memories, exactly 64 eight-symbol
input blocks have fourth bulk output `32103210` and return all four scan
memories to the same incoming values. One is `00000000`; another is
`01011010`. The verifier lists all 64 and checks every block in four separate
bulk scans.

Thus, after any legal original prefix with q_4=32, replacing eight zeros
by any of these 64 blocks preserves the first four guards and scalars, and
the full fourth image if those updates succeed. To see this, each row's
unchanged exit memory preserves its remaining suffix scan and its guard.
The birth symbols then agree. At the fourth row the block output agrees
too, so the whole fourth image agrees. All later updates are identical;
an earlier failure is also simultaneous. This argument preserves the actual
chronological ancestry.

The condition is unchanged after a chosen block, so different eight-symbol
blocks can be chosen independently. The 54 prefixes in section 2 share
their entire first bulk output and last original high zero, hence share
q_4=32 as well. The final original suffix choice `01` or `03` preserves the
whole first image.

It follows that, for every k and every successful prefix alpha of w_k's
actual tape,

```text
|C_(k+10)(alpha)| >= 108 * 64^floor(k/8).
```

Distinct choices occupy disjoint original blocks, prefixes, or the terminal
high bit, giving an injective encoding. This is a constructed subfamily of
the complete original class; it does not replace that class by unrestricted
later predecessors.

For k>=8 this count exceeds `2^9`, while section 3 proves D<=9. For k<8,
the exact short controls give D<=6 and the two-step count 108 already exceeds
`2^6`. Therefore the unrestricted **lower** ancestor conjecture is proved
for every successful tape prefix realized by this particular infinite family.
Its general form and the original upper conjecture remain open.

## 5. What is finished, and what is missing

* **Proved for all original lengths:** the two-update rewrite graph is
  connected within every guarded E_2; each fiber has a unique irreducible
  original, with exact finite-state counting and decoding.
* **Refuted:** a unit-rate count of original choices within that component
  always pays for the whole future repeat count. The complete component
  can have 108 vertices while the future accumulates nine repeats.
* **Proved for one infinite family:** its two-step fiber is always 108,
  its sharp bounds are N<=17 and D<=9, and a four-update identity supplies
  enough original ancestors for the lower conjecture on every one of its
  successful tape prefixes.
* **Still open:** a uniform positive-rate count for every chronological
  original class, or for another sufficiently large original construction.
  The weaker two-step rate is also still open. There is no bound paying for
  arbitrary repetitions and switches from these results alone.

Consequently the connectivity obligation is complete and the displayed
family is handled, but the requested finite-frontier mortality proof is
not complete. No new unrestricted Rule 30 period exclusion follows.

## 6. Exact verifiers and compute scope

```text
uv run --no-project python experiments/rule30/canonical_ancestry_certificate.py
uv run --no-project python experiments/rule30/merger_capacity_obstruction.py
```

Maintained files:

- [canonical_ancestry_certificate.py](../../experiments/rule30/canonical_ancestry_certificate.py)
- [canonical-ancestry-certificate.json](../../experiments/rule30/canonical-ancestry-certificate.json)
- [merger_capacity_obstruction.py](../../experiments/rule30/merger_capacity_obstruction.py)
- [merger-capacity-obstruction.json](../../experiments/rule30/merger-capacity-obstruction.json)

The first checker validates the local column and E/F identities, closes the
entire 74-state product graph, and reduces the previously certified complete
36-, 60-, and 162-member classes with independent guard/image checks on
each selected reduction. It also retains the actual third-merger witness.

The second checker proves the constant-fiber parametrization, closes all
spatial orbits through the empty eighteenth row, checks them independently
against the unchanged frozen `panel/cert33.py`, replays the two counting
counterexamples through failure, and verifies the 64 four-update block
choices. The artifacts contain source hashes, the complete product graph,
accepted residues, original prefix parameters, block choices and guarded
witness records.

Both defaults have a 30-second wall cap. The family certificate additionally
caps temporal depth at 18 and spatial period at 8192; reaching a cap before
closure is an error, not a theorem. Both completed in under one second in
the saved run. The previous original-start census was not rerun. No GPU,
paid compute, seed regeneration, BlindMind rerun, or frozen-oracle change
was used.

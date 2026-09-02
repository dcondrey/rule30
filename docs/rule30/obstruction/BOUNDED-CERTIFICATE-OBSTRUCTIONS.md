# Ordered-ancestry obstructions in the Rule 30 period-two program

Date: 2026-09-02

Status: **THEOREM-GRADE NEGATIVE RESULTS FOR THE SPECIFIED CERTIFICATE
CLASSES. THE NONCONSTANT PERIOD-TWO TRACE AND P1 REMAIN OPEN.**

## Abstract

The current period-two reduction for Rule 30 is governed by a growing family
of inverse-cone dependency queues.  Several natural attempts tried to replace
those queues by bounded data: ordered `D8` holonomy defects, endpoint values,
two queue ends, local additive potentials, endpoint telescopes, fixed-radius
alpha support, a constant cut suffix, a finite endpoint-morph state, or a
local additive conserved density.

This note gives exact obstructions to those particular replacements.  Some
are finite counterexamples to universal statements; one is an all-word
weighted-automaton impossibility at each factor width `1<=w<=5`; two are
exhaustive lower bounds through explicitly stated finite parameters.  The
common failure is loss of ordered interior ancestry.  Complete dependency
queues are closed, while every bounded projection tested here either collides,
cancels, or grows with the horizon.

The conclusion is deliberately conditional: **within the certificate
architectures tested here**, a successful proof must retain unbounded ordered
ancestry, an equivalent lossless nonlocal state, or use a genuinely different
mechanism.  These results do not rule out a proof of period-two exclusion and
do not prove that every conceivable proof must use ancestry.

## 1. Evidence convention and setup

We use three labels.

- **`[U_w]`** is an all-word theorem at the displayed fixed width `w`.  Its
  finite automaton contains words of every length.
- **`[W]`** is an exact finite witness refuting a universally quantified
  certificate claim.  Exhaustive minimality is stated only when checked.
- **`[E_b]`** is exhaustive computation only through the displayed bound
  `b`.  It is not an all-parameter theorem.

States `0,1,2,3` are the two-bit inverse-cone states.  A hard-core endpoint
word lies in `{1,2}^*` and avoids `11`.  For a hard-core word
`W=W_0...W_(n-1)`, its zero-prefix scenarios are

```text
W^(k) = 0^k W_k...W_(n-1),        0 <= k <= n.
```

At forced row `j`, let `A_(j,k)` be the newest endpoint-to-cut permutation in
scenario `k`.  The eight permutations have affine coordinates

```text
A=(alpha,beta,gamma):
(h,l) |-> (h+alpha, l+beta*h+gamma)       over F_2.
```

Their ordered holonomy defects are

```text
delta_(j,k) = A_(j,k)^(-1) A_(j,k+1).
```

For tail `2` the sufficient support projection is `(alpha,beta)`; for tail
`3` it is `(alpha,gamma)=A(0)`.  A pull row is a nonfinal hard-core endpoint
transition `1 -> 2`.

## 2. Composite obstruction theorem

### Theorem 1 (bounded-certificate obstruction theorem)

In the constant-tail queue reduction of the nonconstant period-two problem,
the following statements hold.

1. The ordered `D8` defect word is not a closed dynamical state, even after
   adding an absolute affine anchor, every scenario's current endpoint, or
   the first and last symbol of every scenario queue.
2. For each `1<=w<=5`, no rational width-`w` padded additive factor potential
   is simultaneously bounded below on the complete invariant queue language,
   nonincreasing on every successful update, and strictly decreasing on every
   pull.
3. Equality of the two endpoint projections does not imply absence of
   internal projected support.
4. The diagonal alpha token `k=j` is not sufficient.  More generally, the
   exact certificate below excludes every proposed alpha-search radius at
   most `26`; no arbitrary-radius theorem is claimed.
5. Six terminal constant-cut symbols, even together with hard-core source and
   continuation constraints, do not exclude a late pull.
6. The binary endpoint-morph observable has at least `133` distinguishable
   finite-horizon residuals by prefix depth `10`.  This is a state lower bound,
   not a proof that the morph has infinitely many residuals.
7. For every density window `1<=m<=12`, Rule 30 has no nontrivial rational
   local additive conserved density satisfying the standard continuity
   equation.  Rule 184 has one extra density dimension at every such window.

Consequently, no certificate in the union of these precisely defined classes
can close the period-two argument.  The complete ordered dependency queues
remain a closed state for every length.  Any proof continuing within this
queue/scale architecture must therefore retain their growing ordered content,
prove a lossless nonlocal quotient of it, or introduce a mechanism outside
the excluded classes.

#### Proof

Items 1--7 are Propositions 2--8 below.  The concluding disjunction says only
that a state in an excluded class cannot be used as the required closed
certificate.  It makes no assertion about certificate classes not defined in
this note.  QED.

## 3. Holonomy profiles are observables, not states

### Proposition 2 (`[W]`; exhaustive first collisions)

The following three state projections are not closed under one required
forced-row update.

1. **Defects plus affine anchor.**  At source length eight, tail `2`, row `1`,

   ```text
   U=12122222,    V=12222222
   ```

   have the same ordered defect word and the same rightmost anchor, hence the
   same complete current affine profile, but different successor defect
   words.  Their first successor entries differ:

   ```text
   U: (0,0,1), ...
   V: (0,0,0), ... .
   ```

2. **Add every scenario endpoint.**  At source length nine, tail `2`, row
   `0`,

   ```text
   U=121212222,    V=122212222
   ```

   retain the same anchored profile and the same previous endpoint in every
   zero-prefix scenario, but again have different successor defect words.

3. **Add both queue ends.**  The depth-one two-ended annotation has no
   collision in the complete source lengths 11 and 12, but at source length
   13, tail `3`, row `0`,

   ```text
   U=1212221222122,
   V=1221221222122
   ```

   have survival length three and the same anchored defects and first/last
   symbol of every active scenario queue.  Their successors first differ as

   ```text
   U: ..., (1,0,0), (0,0,1), ...
   V: ..., (1,1,1), (0,0,0), ... .
   ```

These collisions exclude deterministic rank updates that factor through the
respective projected state.  Complete reversed dependency queues are closed
for every length by their coordinatewise recurrence; the counterexamples do
not show that every fixed-depth queue annotation fails.

#### Proof

The inverse identity

```text
(alpha,beta,gamma)^(-1)
  =(alpha,beta,gamma+alpha*beta)
```

and right-to-left reconstruction from the anchor are checked over all eight
affine maps.  Exact scenario replay then compares equal keys with their
successor defect words.  The length-13 pair differs only in the interiors of
the relevant queues, localizing the omitted information.  Complete
enumeration of every smaller audited length establishes the stated first
collisions and the length-11--12 pass.  QED.

One-command replay:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/p1-period2-invariant/constant_tail_holonomy_defect_closure.py --max-length 13
```

Source: [holonomy-defect closure](../../../experiments/rule30/p1-period2-invariant/RESULTS-HOLONOMY-DEFECT-CLOSURE.md).

## 4. No width-at-most-five additive pull potential

### Proposition 3 (`[U_w]` for each `1<=w<=5`)

Fix `w`.  Pad a normalized invariant queue `R` with distinct left and right
markers and let

```text
V(R) = sum of v(q_i...q_(i+w-1))
```

over its width-`w` factors, with rational factor weights `v`.  There is no
such `V` for `1<=w<=5` satisfying all three conditions:

```text
V is bounded below on every word in the invariant SFT;
V(R) >= V(Q(R)) for every successful queue update;
V(R) >= V(Q(R))+1 for every pull update.
```

The exact product systems are:

| `w` | factor variables | bound states/edges | update states/edges | terminals | result |
|---:|---:|---:|---:|---:|:---|
| 1 | 3 | 4 / 9 | 34 / 76 | 10 | UNSAT |
| 2 | 12 | 5 / 12 | 34 / 76 | 10 | UNSAT |
| 3 | 35 | 12 / 27 | 61 / 139 | 17 | UNSAT |
| 4 | 88 | 29 / 66 | 141 / 318 | 36 | UNSAT |
| 5 | 210 | 68 / 154 | 320 / 721 | 86 | UNSAT |

This excludes precisely translation-summed rational local factor potentials
with the displayed padding and inequalities.  Width six and arbitrary-width
potentials are not classified.  Because the factor weights are existential
variables, the exact witness for this class is the finite inconsistent linear
system in the table, not one queue word chosen independently of the weights.

#### Proof

The boundedness product is the invariant suffix automaton crossed with the
width-`w` factor memory.  Bellman variables certify that no accepted interior
cycle has negative weight, which is equivalent to a global lower bound up to
the fixed end padding.  The update products cross the same language automaton
with the exact raw scan for both tail modes.  Every accepted path of every
length therefore contributes its update inequality.  The resulting finite
rational linear systems are exactly UNSAT in the five rows above.  This is an
all-word computation at fixed width, not sampling by queue length.  QED.

The earlier frozen width-two candidate has useful human-readable witnesses:

```text
V(2110101010101)=-1,
V(3010101010101)=-1,

R_2(k)=211(01)^k,       V(R_2(k))=49-10k,
R_3(k)=30(10)^k1,       V(R_3(k))=59-10(k+1),  k>=5.
```

Thus its alternating cycle is unbounded below.  Exact arrows also refute its
`B`-monotonicity and required `AC` macro-drop; these are witnesses to that
particular candidate, while the product theorem excludes the whole stated
width-at-most-five class.

One-command replay:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python experiments/rule30/p1-period2-invariant/constant_tail_pull_potential.py --last-width 5
```

Sources: [macro-edge rank](../../../experiments/rule30/p1-period2-invariant/RESULTS-MACRO-EDGE-RANK.md) and [exact product generator](../../../experiments/rule30/p1-period2-invariant/constant_tail_pull_potential.py).

## 5. Endpoint telescoping loses internal support

### Proposition 4 (`[W]`; smallest retained witness)

Endpoint equality is insufficient to certify that all adjacent projected
differences vanish.  For

```text
W=121,    tail=3,    row=0,    survival=4,
```

the tail-3 projections along scenarios `k=0,1,2,3` are

```text
(alpha,gamma): (0,1), (1,0), (1,0), (0,1).
```

The first and last projections agree, but the ordered interior support is
nonempty.  Hence a proof using only the two endpoint scenarios cannot infer
the rowwise projected-support statement.

#### Proof

The four exact affine maps give the displayed sequence.  Its endpoints are
equal and it contains two values, which is the required counterexample.  QED.

One-command replay:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/p1-period2-invariant/constant_tail_projected_support_algebra.py
```

Source: [projected-support disposition](../../../experiments/rule30/p1-period2-invariant/RESULTS-PROJECTED-SUPPORT-DISPOSITION.md).

## 6. Alpha support is not confined to the diagonal or a tested radius

### Proposition 5 (`[W]`)

The strengthening “the diagonal token `k=j` supplies the alpha witness” is
false.  Its smallest retained counterexample is

```text
W=122221,    tail=3,    row j=0,    survival=2,
projected support={2,4,5},    alpha support={2,4}.
```

In addition, the following fixed length-96 hard-core word has tail `2`, a
nonfinal pull at row `j=0`, survival two, and first alpha-support token `27`:

```text
122122122212222212221222121222212222122222122212
222122222122222122212221212212122212122212221221
```

Its complete alpha support is

```text
{27,28,29,31,34,35,36,37,38,39,42,43,44,45,46,48,
 53,54,56,57,58,59,61,62,65,67,68,69,70,74,75,76,
 77,79,82,83,84,86,88,92}.
```

Therefore every rule which searches only `k-j<=26` fails on this witness.
The witness improves the archived lower bound 12 and in particular certifies
the requested “at least 25” displacement.  It does **not** prove an unbounded
displacement family, so the statement “no fixed radius works for any radius”
remains unproved.

#### Proof

The checker constructs all zero-prefix scenarios simultaneously, evaluates
the exact newest affine maps, verifies the pull and nonfinal hard-core row,
and compares adjacent alpha bits.  The displayed supports follow.  QED.

One-command replay:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 docs/rule30/obstruction/replay_bounded_witnesses.py alpha
```

Background: [pull-row alpha support](../../../experiments/rule30/p1-period2-invariant/RESULTS-PULL-ROW-ALPHA-SUPPORT.md).

## 7. Three event rows do not make a local patch theorem

### Proposition 6 (`[W]` at `n=12`)

The last six constant-cut symbols do not locally exclude the late pull, even
when the source and continuation are hard-core.  An exact satisfying
certificate for tail `2`, residue `0`, and `n=12` is

```text
W:          121212222121
extension:  22122122122122
cut:        01202332222222
                         ^ final six are constant 2
target:                 1 2 2
```

The target contains the required `1 -> 2` pull at extension row 12.  Imposing
the full constant-cut history makes the formula UNSAT.  At `n=12`, the exact
minimum terminal suffix lengths which make the six tail/residue formulas
UNSAT are

```text
tail 2, residues 0/1/2: 8,6,9;
tail 3, residues 0/1/2: 6,6,5.
```

Thus the three-row late-pull reduction names three candidate **event times**.
It is not a `3 x 3` local spacetime-patch theorem.  The counterexample excludes
certificates using at most the final six cut symbols and no summary of the
earlier triangle; it does not exclude a larger or history-carrying state.

#### Proof

The CNF model is decoded to the three displayed words and replayed by the
literal inverse-cone rule.  The checker verifies source and continuation
hard-core legality, the target pull, and the six constant terminal symbols.
It then solves the full-history and increasing-suffix instances exactly.  QED.

One-command replay:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python experiments/rule30/p1-period2-invariant/late_pull_diagonal_sat.py --max-n 1 --max-validate 0 --proof-through 0 --window-audit-n 12
```

Source: [late-pull diagonal](../../../experiments/rule30/p1-period2-invariant/RESULTS-LATE-PULL-DIAGONAL.md).

## 8. Endpoint-morph residuals give a finite state lower bound

Let `I` be the inverse terminal-cone map, `P` adjacent Peel, and `T=I^(-1)`.
For a binary endpoint word `e` of length at least two, put

```text
F(e)=T(P(I(e))),
lambda(e)=1  iff the final symbol of F(e) lies in {1,2}.
```

For terminal horizon `N`, assign every length-`N` word one terminal class.
Recursively assign a shorter prefix `p` the signature

```text
((lambda(p1), class(p1)), (lambda(p2), class(p2))).
```

Two prefixes have the same class exactly when their binary output trees agree
through the remaining finite horizon.

### Proposition 7 (`[E_14]`)

At horizon `N=14`, the numbers of exact residual classes over all binary
prefixes of lengths `1,...,10` are

```text
2, 3, 4, 6, 10, 16, 27, 46, 77, 133.
```

Consequently every deterministic finite-state machine which computes this
observable correctly on all finite binary inputs needs at least 133 states.

This table does not prove that the residual count is unbounded.  Accordingly,
the stronger phrase “the endpoint morph is not finite-state” is a conjectural
extrapolation and is not used in Theorem 1.

#### Proof

Backward partition refinement enumerates all `2^14` terminal words and both
children of every shorter prefix.  Equality of the recursively constructed
signatures is exact finite-horizon right congruence.  The depth-10 partition
has 133 blocks, so its members are pairwise distinguished by continuations of
length at most four.  QED.

One-command replay:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 docs/rule30/obstruction/replay_bounded_witnesses.py residual
```

The replay prints the canonical partition digest
`ce8c3eca08d15c0786bec7e18003f3f0ca6c833411f83fb078c1ac2ea2618a15`.

## 9. No local additive conserved density through window 12

For a density `rho` on `m` cells and current `J` on `m+1` cells, the standard
local continuity equation on every word `x_0...x_(m+1)` is

```text
rho(y_0...y_(m-1)) - rho(x_1...x_m)
  = J(x_0...x_m) - J(x_1...x_(m+1)),

y_i = Rule30(x_i,x_(i+1),x_(i+2)).
```

Constants and spatial coboundaries are trivial densities and span dimension
`2^(m-1)`.

### Proposition 8 (`[E_12]`)

For every `1<=m<=12`, the rational solution space for Rule 30 has density
dimension exactly `2^(m-1)`.  It therefore consists only of the trivial
constant/coboundary space.  At `m=12`, the exact mod-two matrix rank is
`10239`, its maximum possible value given the trivial solutions, and the
density dimension is `2048`.

For Rule 184, the same calculation gives dimension `2^(m-1)+1` at every
tested window, detecting the conserved particle number as a positive
control.

This excludes rational/real local additive conservation laws only through
window 12.  It says nothing about larger windows, nonadditive invariants,
growing windows, or identities specialized to the lone-seed boundary.

#### Proof

The continuity equations form an integer matrix `[A B]`.  The current block
`B` is the incidence matrix of the binary de Bruijn graph and has rank
`2^(m+1)-1`.  Trivial densities give the rational upper bound

```text
rank_Q[A B] <= 2^m + 2^(m+1) - 2^(m-1) - 1.
```

Reduction modulo two cannot increase rank.  For Rule 30, exact bit-matrix
elimination reaches this upper bound for every `m<=12`, squeezing the rational
rank to equality and leaving exactly the trivial density dimension.  Rule
184 falls short by one rank in every row, as expected.  QED.

One-command replay:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/additive_conservation_probe.py --rules 184 30 --max-window 12
```

Source: [additive conservation-law search](../RESULTS-additive-conservation-probe.md).

## 10. What the obstructions jointly say

The seven propositions fail in complementary ways.

| Compression | Information discarded | Exact symptom |
|---|---|---|
| anchored `D8` defects | queue interiors | same state, different successor |
| local factor sum | order beyond width `w` | all-word systems UNSAT for `w<=5` |
| endpoint telescope | order of internal changes | cancellation on `121` |
| diagonal/bounded alpha search | remote source position | first witness at distance 27 |
| six-symbol cut suffix | earlier triangle | hard-core late-pull model |
| finite endpoint state | growing continuation behavior | at least 133 residuals |
| local additive density | nonlocal/ordered transport | only coboundaries through `m=12` |

No single row establishes an unbounded-memory theorem for all certificate
languages.  Together they do establish a sharp design constraint for the
current program: further work should not collapse the complete queues to a
fixed list of local statistics and then search for a scalar descent.  The
surviving proof objects are ordered ancestry trees, gap vectors retaining
dyadic scale, indexed nonlocal clauses, or a new argument outside the queue
architecture.

The nonconstant period-two exclusion, P1, P2, and P3 remain open.

## Appendix A. Scope corrections for two external claims

The two corrections below concern the scope of proposed consequences, not the
validity of every construction in the cited works.  Full details and replay
commands are in [SCOPE-CORRECTIONS.md](SCOPE-CORRECTIONS.md).

1. **Nersissian.**  The subset-zeta basis change exactly reproduces the
   original rotated Rule 30 triangle.  It moves the difficult sequential
   dependence from OR-convolution to exclusive prefix XOR.  The supplied
   `compute_Sm(n+1)` loop performs all `n-1` support advances before the
   conditional `O(k log n)` row evaluator applies.  This does not give a
   logarithmic center-bit algorithm from input `n` alone.
2. **Deva.**  Decision-tree complexity of the time-`t` center function on
   `2t+1` arbitrary initial cells does not transfer to the fixed lone-seed
   index function `n |-> c_n`.  The quantifiers and inputs differ.  The
   all-zero Rule 30 orbit is an internal control: it has the same
   arbitrary-input function family before substitution but a constant center
   sequence after substitution.

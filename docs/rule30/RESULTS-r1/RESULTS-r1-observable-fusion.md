# Observable fusion and the finite-state necessity gap

Date: 2026-09-09. Evidence: **U** (construction and compactness lemmas),
**R** (explicit remaining realization conditions), **C** (Rule 90
calibration). This is an intermediate route analysis. It neither proves
nor kills R1 for Rule 30.

## 1. What the Markov certificate proves

The framework in
`experiments/rule30/r1-isolated-column/markov_extension_sat.py` was
independently audited. Its exact subset construction checks the whole
infinite-path language of its selected finite graph, not just a fixed
length of paths. Nonblocking source edges are essential: they make an
unliftable finite path a prefix of a genuine infinite source path.

If every graph path describing columns `(A,B)` has a legal right lift
`(B,C)` in the same graph, repeated lifting constructs all columns to
the right. The coordinates already constructed never change. Rule 30's
left inverse

```text
A_t = B_(t+1) XOR (B_t OR C_t)
```

then constructs all remaining columns to the left. This produces a full
diagram for nonnegative time and an actual two-sided initial row.

The SAT framework also asks for two equal-length return paths with the
same periodic first column, the same initial pair, and unequal second
columns at a zero phase of the first. Arbitrary concatenations of those
paths are legal. At an aligned distinguishing coordinate the second
column recovers the binary code selecting the paths. Consequently an
explicit non-eventually-periodic code gives a non-eventually-periodic
masked neighbour. This is a valid sufficient construction theorem.

The online witness variables impose an additional sufficient strategy
condition. The offline subset check and its conditional refinements do
not impose that condition. No error was found in the phase increments,
the current/next right-bit convention, or the repeated-column lifting
argument. A graph refutation is still a refutation of its specified
finite-state class.

## 2. A counterdiagram gives a compact subsystem, not automatically a finite graph

**U.** Suppose a full diagram has columns `C_x`, and its centre has
period `p` from time zero. Eventual periodicity can be put in this form
by discarding a finite initial time interval. Form the compact set

```text
X = closure { (C_x(t+kp), C_(x+1)(t+kp))_(t>=0) : x>=0, k>=0 }.
```

It contains the original centre-neighbour pair. Every `(A,B)` in `X`
has a legal right lift `(B,D)` in `X`: take a sequence of the displayed
pairs converging to `(A,B)`, extract a convergent subsequence of their
third columns, and pass the local Rule 30 identities to the limit.
Thus a compact right-surjective temporal-pair subsystem is necessary.

Nothing in this proof bounds the memory needed to describe `X`. Replacing
`X` by all paths permitted by its length-`m` factors can splice together
pieces with incompatible longer continuations. The resulting finite
overapproximation need not remain right-surjective. No finite cutoff
follows from compactness.

The logical distinction is real in symbolic dynamics. Fix an irrational
`alpha` in `(0,1)`, let

```text
u_n = floor((n+1) alpha) - floor(n alpha),
```

and close its time shifts in the product topology. Every point of this
nonempty compact shift has, in every length-`L` interval, a number of
ones differing from `alpha L` by at most 1. This follows directly by
telescoping the floors and passes to limits because interval counts
depend on finitely many coordinates. Every point therefore has
irrational density `alpha` and is not eventually periodic.

A nonempty sofic shift has a periodic point: an infinite path in a
finite presenting graph reaches a directed cycle, and repeating that
cycle gives one. The compact shift just constructed consequently has
no nonempty sofic subshift. This example is **not** a Rule 30
counterdiagram and does not disprove a possible special theorem for
Rule 30. It shows why the required finite-state necessity theorem
cannot be replaced by a generic compactness argument.

## 3. Prescribed-limit realization

Fix a periodic centre word `w` of length `p`. Let its zero phases be
`Z`. Write the observable sequence in blocks as

```text
Y_j = (r_(pj+z))_(z in Z).
```

Eventual periodicity on the zero set is equivalent to eventual
periodicity of `Y`; a period in microtime can be replaced by a multiple
of `p`. If `Z` is empty there is no zero-set obligation.

**U (prescribed-limit lemma).** Suppose an explicitly specified
non-eventually-periodic sequence `Y` has this property: for every `n`
there is a full Rule 30 diagram with centre `w` and observable prefix
`Y_0,...,Y_(n-1)`. Then a full Rule 30 diagram realizes all of `Y`.

Proof: take their initial right rows and a product-convergent
subsequence. With the prescribed left boundary `w`, any finite
right-half-plane space-time cone depends on finitely many initial
right cells. The limiting right row therefore has every required
observable prefix. Reconstruct the left half-plane with the exact
inverse above. The limiting diagram has the already specified
aperiodic observable `Y`.

Spatially and temporally periodic tori are sufficient witnesses for
these finite prefixes, but are not required. Their initial rows need
not be nested. It is the prescribed limiting observable, with its
independently proved aperiodicity, that makes this compactness use
valid. A substitution that uniformly produces such tori would give a
nonsofic construction route without a finite right-extension graph.

## 4. Adaptive torus fusion with permanent inequalities

If the target observable is not known in advance, enumerate all pairs
`(T,q)` with `T>=0`, `q>=1`. A concrete alternative is a recursion
producing actual tori and increasing initial-right-row prefixes `u_n`:

1. The centre of every torus is `w`, with the same phase.
2. The new prefix extends the previous prefix.
3. At stage `n`, choose a finite `j_n>=T_n` for which the current torus
   has `Y_(j_n) != Y_(j_n+q_n)`.
4. Retain enough initial right cells to determine this inequality and
   every earlier one. For example, retaining sites `1,...,L_n` with
   `L_n >= p(j_n+q_n)+p` suffices for the new witness. Also require
   `L_n -> infinity`.

**U.** If this recursion can be continued at every stage, its limiting
right row gives a full counterdiagram. Each witness is a constraint on
a fixed finite cone and survives all later stages. Every proposed
eventual period `(T,q)` is contradicted by its retained witness.

**R: the exact missing construction condition** is the existence of a
torus extension at every stage, inside a specified nonempty reservoir
of prefixes. Neither the presence of many tori nor an increasing list
of their minimal periods proves this condition. Periodic invariant
cylinders already found in this repository rule out a claim that every
right-row cylinder supplies every escape.

The smallest model of the limit problem is the sequence of periodic
words `(10^n)^infinity`. Their least periods tend to infinity, whereas
their limit is `1000...`, which is eventually periodic. The positions
of their late return violations escape to infinity. The fusion
conditions above expressly prevent that loss.

## 5. A uniform discrepancy condition that would suffice

There is another concrete way to control the limit without nesting
initial rows. Choose a zero phase `z` of `w`. Suppose actual tori with
centre `w` have sampled neighbour words

```text
v^(n)_j = r^(n)_(pj+z)
```

and rational densities `alpha_n -> alpha`, where `alpha` is irrational.
Suppose a single constant `C`, independent of the torus and interval
length, satisfies

```text
abs(sum_(j=s)^(s+L-1) v^(n)_j - alpha_n L) <= C
```

for every `n,s,L`. **U:** any product-limit diagram has the analogous
bound with `alpha`. Taking `s=0` and `L -> infinity` gives density
`alpha` for this zero-phase trace. An eventually periodic binary word
has rational density, so the limiting diagram is an R1 counterdiagram.

Rational mechanical words satisfy this discrepancy condition with
`C=1`, by the same floor telescoping used in Section 2. Thus a uniform
realization theorem for suitable balanced/Christoffel periodic words
approaching an irrational slope would suffice. **R:** no such Rule 30
realization family is established here. This condition concerns the
actual observed neighbour column, not a spatial average whose
sensitivity to overwriting one column vanishes.

## 6. Rule 90 control: an explicit successful torus limit

For every odd ring length `N>=3`, put ones at sites `-1,+1`, zeros
elsewhere, and evolve by Rule 90. Reflection symmetry preserves a
zero centre forever. The ring update is a bijection on the subspace
of even-parity rows: its full kernel consists of constant rows, and
the nonzero constant row has odd parity when `N` is odd. It preserves
even parity. These finite rows therefore lie on genuine temporal
cycles, giving actual tori, not merely long transient simulations.

As odd `N -> infinity`, their initial rows converge to the two-one
row on the line, which is the Rule 90 lone-seed row after one step.
Its neighbour is

```text
r_t = 1 iff t+2 is a power of 2.
```

It is aperiodic because it has infinitely many ones and unbounded
gaps. Here compactness works because the limiting trace is known
exactly and its aperiodicity is proved independently. The accompanying
finite calibration checks the tori and the required early trace
agreement, and reruns unchanged `controls.rule90_control`.

The fusion and prescribed-limit lemmas are rule-generic construction
tools and correctly permit Rule 90 counterdiagrams. A successful
Rule 30 application would still have to establish its missing
all-length realization step using the actual OR rule. No generic
argument here is asserted to prove R1.

## 7. Reproduction and scope

```sh
uv run python experiments/rule30/r1-isolated-column/verify_observable_fusion.py
```

This rechecks the saved calibration and the frozen engine/control
hashes. `--write` creates the saved calibration on its first run.
All asymptotic statements above have symbolic proofs; the finite
calibration is not their proof. The current finite-state refutations
do not eliminate nonsofic temporal languages, substitution limits,
or the explicit fusion conditions above. No Rule 30 realization
recursion meeting those conditions has yet been supplied. R1 and
P1 remain open at this intermediate step.

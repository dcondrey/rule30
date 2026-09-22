# C3 degree audit: a definition correction and two algebraic obstructions

Date: 2026-09-08.

**The code-defined C3 remains open. No C3 counterexample or all-length proof
was obtained.** Individual boundary edges have large measured algebraic
degree. The existential support predicate is much simpler at small lengths,
but its proposed affine form fails at length 52. Neither measurement proves
unbounded degree as length tends to infinity.

## 1. Authoritative definition

`constant_tail_zero_prefix_bitsliced.zero_prefix_bitsliced_graph` compares
**all three** newest-cut affine coordinates, and also the forced symbol.
It does not compare alpha alone. Its token indices are `0,...,n-1`;
scenario indices are `0,...,n`.

For a fixed tail, the forced symbol is determined by the affine triple:

```
high = 1 XOR alpha
low  = (tail & 1) XOR (beta & high) XOR gamma.
```

These are precisely `forced_value_bits`. Consequently the forced-symbol
comparison adds no edges to the full-affine comparison. The new audit checks
that redundancy at every computed scenario/row.

The alpha-only restatement in the task fails at the shortest failing length:

```
W = 21212122, tail = 2, row = 2, survival = 3
alpha across scenarios 0,...,8: 1 1 1 1 1 1 1 1 1
full support: {1,2,3,5,6,7}
```

`c3_degree_witness_controls.py` finds this witness by an independent scalar
search through increasing lengths, using `forced_trace`, then verifies its
full support with `zero_prefix_bitsliced_graph`. This is a definition
correction, **not a counterexample to C3**. The existing
`RESULTS-C3-LOCALIZATION-NO-GO.md` already records failure of the individual
alpha and beta projections; the distinction is not a new mechanism.

## 2. The measured Boolean functions and their domains

Write `z_i=[W_i=1]`, so the zero Boolean assignment means `W=2^n`.
Zero-prefix scenarios still replace source symbols by the actual four-state
symbol **0**, not by Boolean value zero.

For every computed row define the raw full-affine support, before survival
filtering. The audit measures, for `0<=j<n`,

```
E_j(W) = [j belongs to raw S_j]
H_j(W) = [some k >= j belongs to raw S_j].
```

`H_j` is C3's conclusion; `E_j` is an individual boundary edge. Measuring
`E_j` is not an attempt to revive the already-false claim that it is always
one. For legal rows these definitions use exactly the existing graph.
Raw values on illegal rows are explicitly included in the degree calculation.
The JSON also records alpha-edge degrees, the legality predicate `L_j`, and
`L_j E_j`, with value zero outside legal hard-core rows.

There are two different degrees:

* **Cube degree:** the ordinary ANF on all of `{1,2}^n`, including words
  containing `11`, using the unmodified forcing kernel.
* **Hard-core degree:** the minimum degree of a polynomial representing the
  raw predicate on hard-core words. This degree does not depend on an
  arbitrary assignment of values to non-hard-core words.

For completeness, the latter is computable canonically. Impose
`z_i^2=z_i` and `z_i z_(i+1)=0`. Every surviving monomial is indexed by an
independent set of positions. Its coefficient is

```
a_T = XOR over U subset T of f(1_U).
```

All these evaluations are hard-core because every subset of an independent
set is independent. The evaluation matrix is the inclusion matrix of
independent sets, triangular with diagonal one, so this representation is
unique. Reducing a polynomial by these relations never increases degree;
therefore the canonical degree is also the minimum possible extension
degree. Its upper bound is `ceil(n/2)`, rather than `n`.

Degree of the zero polynomial is encoded as `-1`. A degree on the raw
hard-core domain is **not** a lower bound for a representation required only
on legal rows. Similarly, high degree of `L_j E_j` can come from legality.

## 3. Exact degree results at each length

The following entries are maxima over `0<=j<n`, calculated by
`c3_boundary_degree.py` using the imported, unmodified
`bitsliced_trace_states`. Both tails have the listed cube degree. The final
column takes the maximum over both tails; individual rows and both tails
are in `c3_boundary_degree_results.json`.

| n | max degree E, cube, either tail | max degree E, HC, tail 2 | max degree E, HC, tail 3 | max degree H, HC, both tails |
|---|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 0 |
| 4 | 4 | 2 | 2 | 0 |
| 5 | 4 | 2 | 2 | 0 |
| 6 | 5 | 2 | 2 | 1 |
| 7 | 7 | 3 | 3 | 1 |
| 8 | 7 | 4 | 4 | 0 |
| 9 | 8 | 4 | 4 | 1 |
| 10 | 10 | 5 | 4 | 0 |
| 11 | 10 | 5 | 5 | 1 |
| 12 | 11 | 6 | 6 | 1 |
| 13 | 12 | 6 | 6 | 0 |
| 14 | 13 | 6 | 6 | 0 |
| 15 | 15 | 7 | 7 | 0 |
| 16 | 15 | 8 | 8 | 0 |
| 17 | 17 | 8 | 8 | 1 |
| 18 | 18 | 9 | 9 | 0 |

The degree-9 coefficient at `n=18`, `j=0`, for each tail is
`z_1 z_3 z_5 z_7 z_9 z_11 z_13 z_15 z_17`. Its coefficient was additionally
verified as one by XORing **512 independent scalar evaluations per tail**,
using `forced_trace` for scenarios 0 and 1, without the packed ANF transform.

Thus bounded degree at most eight cannot represent all of these raw
hard-core edge functions. The finite sequence is consistent with unbounded
growth, but does not establish it. In particular, it is not the sibling
Psi result repeated as an all-length theorem.

## 4. Smallest-length quadratic edge obstruction

The preregistered quadratic edge representation is killed first at length 7.
For `n=7`, tail 2, row 0, the coefficient of `z_1 z_3 z_5` is one:

| W | E_0(W) |
|---|---:|
| 2222222 | 0 |
| 2122222 | 0 |
| 2221222 | 0 |
| 2121222 | 1 |
| 2222212 | 0 |
| 2122212 | 1 |
| 2221212 | 0 |
| 2121212 | 1 |

All eight words are hard-core. Their XOR is one, which is impossible for
any quadratic polynomial on this Boolean subcube. These values were
independently replayed using scalar `forced_trace`.

For a single named disagreement with the canonical degree-at-most-two
truncation: `W=2122121`, tail 2, row 0 is legal and has actual `E_0=1`,
whereas the truncation predicts zero. This is the first such witness in the
audit's Boolean-mask order. No hard-core edge degree exceeds two through
length 6. The coefficient certificate, which also uses illegal rows, rules
out a quadratic formula on the **whole hard-core domain**; it does not rule
out a different quadratic formula fitted only on legal rows.

## 5. The simpler existential predicate also ceases to be affine

The edge degrees cannot be transferred to the OR over edges: `H_j` has
degree at most one throughout the complete length-18 degree audit.
The second experiment preregistered the hypothesis that this affine behavior
continues, with kill condition a hard-core coefficient of degree at least two.

`c3_suffix_degree_probe.py` varies the last `m<=6` source symbols and takes
`j=n-m`, for increasing `n` starting at 19. The original prefix is fixed to
`2^j`. Every relevant zero-prefix scenario erases that prefix, so this
computes the entire dependence of `H_j` for these rows, not a random sample
of its suffix dependence. It is **not** an exhaustive C3 census beyond 20.

The first hit in this specified family is the 405th `(n,tail,m)` case:

```
n=52, tail=3, m=3, j=49
H_49(W) = 1 XOR (z_49 AND z_51), on all hard-core W of length 52.
```

The prefix independence makes the displayed identity independent of the
choice `2^49` used for replay. The five hard-core suffixes were verified
using scalar traces at scenarios 49, 50, 51, and 52:

| suffix | affine triples at scenarios 49,50,51,52 | H_49 | survival for prefix 2^49 |
|---|---|---:|---:|
| 121 | 011, 011, 011, 011 | 0 | 0 |
| 122 | 000, 110, 010, 011 | 1 | 3 |
| 212 | 110, 000, 010, 011 | 1 | 0 |
| 221 | 111, 011, 011, 011 | 1 | 0 |
| 222 | 110, 110, 010, 011 | 1 | 0 |

Each triple lists `(alpha,beta,gamma)`. In particular the four assignments
to positions 49 and 51, keeping position 50 equal to symbol 2, give XOR one.
This rules out an affine representation of `H_49` on the hard-core domain.

The explicit frozen word is `W=2^49 121`. Its row 49 is illegal, so it is
**not a C3 counterexample**. Nor is length 52 claimed globally minimal for
non-affinity: it is the first hit within the specified `m<=6` family, after
the complete degree measurements through 18.

This locates the break in the attempted low-degree mechanism: an existential
support function that appears affine at small lengths develops a quadratic
cancellation. It still supplies no bound relating that cancellation to the
survival of a prefix attached before the suffix. That last gap is the
reachability obstruction already identified in
`RESULTS-C3-LOCALIZATION-NO-GO.md`, not a newly proved impossibility theorem.

## 6. Rule 90 and scope of the obstruction

The algebraic comparison uses `rule90_control_on_c3.Rule` and its
`rule90_carry`, checking the Rule-30 permutation implementation against the
existing graph through length 4 before comparing kernels. For Rule 90 all
16 local table entries satisfy `cone_local(left,right)=left XOR right`,
and the boundary is XOR 3.

This yields a direct all-length algebraic distinction. In this linear
construction each state is a vector XOR of endpoint symbols and a constant.
The newest-cut map is a translation. Its adjacent-scenario difference is
either zero or the single nonzero symbol `W_k`, with a coefficient independent
of the source word. Thus each raw edge predicate, and its suffix OR, is
source-independent. Their degrees are zero or the zero-polynomial sentinel
`-1`. The scalar control verifies this on every binary word through length
6, both tails, for **1,284 word/tail/row cases**.

The Rule-30 cubic and degree-9 edge coefficients cannot arise by this
Rule-90 computation. This is a kernel-level negative control, **not** a
derivation of Rule 90's own endpoint language, a completed period-two
filter, or a proof of C3. The report makes no exclusion claim that could
pass improperly through the transplanted hard-core language.

Also, even an all-length unbounded-degree theorem would only rule out
uniformly bounded-degree polynomial representations of the measured
functions. It would not rule out bounded-arity recursion or bounded-state
sequential computation: `p_(i+1)=p_i AND z_i` already has degree growing
with the number of inputs. The stronger inference in `psi_degree.py`'s
introductory comment is not used here. No fixed-radius proof is proposed.

## 7. Verification and reproduction

The full degree run performed the following checks:

* 5,616 scalar scenario-row comparisons through length 5, including
  non-hard-core binary sources and their zero-prefix scenarios.
* 62 hard-core word/tail graph comparisons through length 5.
* 150 packed-transform comparisons against an independent scalar Mobius
  transform, plus hard-core reconstruction checks on every measured column.
* 16,507 legal rows through length 18, with no C3 disagreement. Rows at or
  beyond `n` are also checked when legal; they are not silently omitted.

Existing corpus scripts were run unmodified:

* `constant_tail_zero_prefix_bitsliced.py`: 608 slow/fast control edges;
  5,165 word/tail/special cases through length 14 plus the three registered
  special cases. Zero ordinary, ordered, greedy, or nonfinal-miss failures.
* `constant_tail_pull_row_projected_support.py`: 6,652 alpha-parity control
  row states; 5,162 word/tail cases through length 14, yielding 384 pull
  rows. Zero projected or alpha failures. Its 267 diagonal failures are
  the expected failure of the already-killed diagonal assertion.

The new scripts pass `ruff check`. All new numeric results come from the
commands below. The degree JSON includes the imported kernel source hashes.
These finite checks validate the computation, not C3 for all lengths.

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/p1-period2-invariant/c3_boundary_degree.py --max-length 18 --control-length 5 --output experiments/rule30/p1-period2-invariant/c3_boundary_degree_results.json
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/p1-period2-invariant/c3_suffix_degree_probe.py --output experiments/rule30/p1-period2-invariant/c3_suffix_degree_results.json
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/p1-period2-invariant/c3_degree_witness_controls.py
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/p1-period2-invariant/constant_tail_zero_prefix_bitsliced.py --control-length 7 --first-length 1 --last-length 14
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/p1-period2-invariant/constant_tail_pull_row_projected_support.py --parity-control-length 6 --first-length 1 --last-length 14
```

# Collapsed run-length pyramid attempt

Date: 2026-08-31

Status: **OPEN.  No period-two theorem was proved.**  Collapsing rows into
colored run-length digits gives an exact and useful boundary-gap formulation.
Full run-length encoding is lossless and remains viable as a coordinate
system.  The registered bounded-digit summaries and natural run/gap rankings
were falsified by exact reachable transitions.

## 1. Exact collapsed encoding

For a finite Boolean row, record its left spatial offset, its first color, and
the positive lengths of its maximal monochromatic blocks.  Colors alternate,
so after the first color the row is represented only by integers.  For
example,

```text
black black | white white white | black
```

is `B[2,3,1]`.

For the frontier words it is cleaner to use boundary gaps.  Let

```text
g(X) = X XOR (X >> 1).
```

If the one-positions of `g(X)` are

```text
p_1 < p_2 < ... < p_m,
```

define

```text
R(X) = (p_1+1, p_2-p_1, ..., p_m-p_(m-1)).
```

These are exactly the colored run lengths of the active word, read shallow to
deep.  Its shallow color is `m mod 2`, because the word is reconstructed from
the deep zero boundary.  Thus no separate color bit is needed once the deep
boundary convention is fixed.  The maps `X -> R(X)` and

```text
R -> boundary positions -> inverse Gray code
```

are inverse on every finite word.  The implementation checks all 65,536 words
of length at most 16.

The exact alternating macro becomes a pair of union-and-gap operations:

```text
g(C) = A OR (1 + zB),
g(D) = C OR zA.
```

Consequently:

```text
R(C) = successive gaps between positions in supp(A) union supp(1+zB),
R(D) = successive gaps between positions in supp(C) union supp(zA),
pin passes iff length(R(D)) is odd.
```

This answers the representation question positively: the pyramid can be
stored row-by-row as offsets and alternating run digits, and the pin becomes
the parity of a digit-list length.  `runlength_search.py` reconstructs both
macro outputs from those gaps and matches the independent Gray map on all
34,952 legal even-boundary frontiers through `T=8`.

The known adversarial row begins in the collapsed display as

```text
t=0  offset=-8   B[1,6,1,6,1]
t=1  offset=-9   B[3,4,3,4,3]
t=2  offset=-10  B[2,2,1,2,2,2,1,2,2,2,1]
t=3  offset=-11  B[2,1,6,1,6,1,4]
...
t=14 offset=-22  B[2,2,1,3,3,2,4,1,1,2,1,1,1,2,2,3,1,2,1,1,1,2,1,2,1]
t=15 offset=-23  B[2,1,4,1,2,2,3,4,4,1,4,1,1,1,5,1,8].
```

The independent row updater verifies that its center alternates through
`t=14` and fails at `t=15`.  The spatial offset is essential: discarding it
would lose which digit contains the center.

## 2. Why the collapse is not yet a finite certificate

The run digits are not a fixed finite alphabet.  The theorem quantifies over
arbitrary finite initial rows, which may already contain a run of any positive
length.  More sharply, inverse Gray code can expand one digit into arbitrarily
many digits.  For every `m>=1`, take

```text
U = 2^m-1,
```

a single solid run of `m` ones.  Then

```text
R(I(U)) = (1,1,...,1)  [m entries].
```

Indeed `g(I(U))=U`, so every one-position of `U` is a boundary of `I(U)`.
The script verifies `m=1..64`; the identity proves the family for all `m`.
Thus a bounded-output digit substitution cannot implement even one cumulative
XOR sweep.  A symbolic run-merger can implement it, but must retain arbitrary
integer residuals and an unbounded list of output digits.

Six natural nonnegative statistics were tested on every exact surviving
transition among 32,043 distinct registered finite-seed states:

```text
total boundary count, total excess sum(gap-1), number of nonunit gaps,
maximum gap, sum of squared gaps, active height.
```

Every statistic except height has both an increasing and a decreasing exact
reachable transition.  Height only increases, reproducing the already-proved
front-growth obstruction rather than giving a descent.  Shallow-first,
deep-first, and sorted lexicographic gap lists also move in both directions;
the first increase is already at origin `(1,0,0)` and the first decrease at
`(1,0,1)`.  Hence none of these is the requested well-founded rank.

The registered bounded summary retained, for each of `A`, aligned `B`, `C`,
and `D`, the first and last four gap digits (values above 32 collapsed to one
overflow symbol), plus the number of gaps, total span, and nonunit count modulo
four.  It does not close even on the finite rho-seed language.

The first opposite-next-pin collision found is between origins `(8,198,0)`
and `(10,792,0)`.  A stronger equal-frontier-length collision is

```text
origin (rho length, seed integer, follow) = (13,358,1)
(T,A,B) = (28,88421171,44411562)

origin = (13,1766,1)
(T,A,B) = (28,88499507,44389802).
```

Their complete registered bounded summaries agree and both pass the current
pin, but their next pins are respectively `1` and `0`.  The exact `A`/aligned
`B` gap lists are printed by the verifier.  This fires the bounded-summary
kill condition without claiming that full, lossless run-length encoding is
invalid.

## 3. Controls and interpretation

After the run-length test, the complete control script again passed:

- `F^2`: 32/32 neighborhoods;
- defect recurrence: 64/64 assignments;
- alternating strobe local pattern: complete truth table;
- Rule 30 `{-8,-1,6}`: alternating through 14, failure at 15;
- Rule 90 `{-1,1}`: zero center through 128;
- every 131,071 nonzero row in `[-8,8]` through 64 steps, with maximum
  alternating horizon 14;
- constant-zero/one bounded validations: horizons 8 and 9.

For Rule 90, the two support unions become symmetric differences.  The
run-length representation still exists, but no contraction theorem was found,
so its known finite period-two collision is retained.

## 4. Reproduction and conclusion

From `/Volumes/A/researchpapers/13-rule30`:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/runlength_search.py

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/derive_and_controls.py
```

The period-two theorem and Prize Problem 1 remain open.  The digit pyramid is
a genuinely cleaner exact representation, especially because pin acceptance
is just boundary-list parity.  It does not by itself reduce the state: digit
values and digit-list length are unbounded, and the tested bounded projections
lose the next pin.

The single best next theorem target in these coordinates is:

> **Finite-seed boundary-gap tail theorem.**  If every iterate of the two
> displayed union-and-gap operations has an odd second boundary list, then the
> initial rho boundary composition has infinitely many digits.

That statement uses the same-orbit relation and left-finiteness exactly.  A
proof would need a seed-specific invariant of the *full cumulative offsets*,
not a fixed number of endpoint digits or the false claim that an OR mask
contracts every alternating defect.  It is explicitly period-two-specific and
would not settle the other periods of Prize Problem 1.

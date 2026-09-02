# Three-row late-pull diagonal

Date: 2026-09-02

Status: **THE PERIOD-TWO RUNG IS REDUCED TO EXCLUDING PULLS IN THREE ROWS
AROUND ONE SCALE DIAGONAL.  THE REDUCTION IS UNIFORM.  THE EXCLUSION HAS
STRONG FINITE SUPPORT BUT IS NOT PROVED, SO PERIOD TWO AND P1 REMAIN OPEN.**

## 1. A strict weakening of pull-row alpha support

Let `W` be a binary hard-core scale word of length `n`, let the forced cut
tail be `c in {2,3}`, and call forced row `j` a pull when its endpoint
transition is `1 -> 2`.  Pull-row alpha support says that every nonfinal pull
has a zero-prefix alpha witness `k` with `j<=k<n`.  Its empty-interval
consequence is the much weaker statement

```text
no nonfinal pull occurs at j>=n.                     (LPH)
```

No alpha coordinate, spatial derivative, matching, or ancestry depth appears
in LPH.  Even LPH is stronger than the period-two application needs.  It is
enough to exclude the three rows

```text
j in {n,n+1,n+2}.                                   (DLP)
```

Thus DLP is the smallest current sufficient finite-word conjecture.

## 2. Exact scale-placement proof

Suppose an infinite hard-core endpoint whose inverse cut is eventually the
constant `c` has a pull at absolute endpoint position `m`.  For `m`
sufficiently large, put

```text
n=floor(m/3),   m=3n+r,   0<=r<=2.
```

The scale block `W=e[n:2n]` is followed by the forced block beginning at
absolute coordinate `2n`.  The pull at `m` therefore appears at relative row

```text
j=m-2n=n+r in {n,n+1,n+2}.                          (1)
```

The infinite endpoint makes it nonfinal.  DLP contradicts every sufficiently
late pull.  By the proved endpoint/event identity, a surviving endpoint with
only finitely many pulls is eventually `2^omega`; the proved dyadic
exceptional-family separator already excludes that case.  Hence DLP implies
the two constant-tail separators, the rank-zero separator, and the
nonconstant period-two exclusion through the existing reductions.

This corrects the earlier shorthand “fix `W`, then choose an arbitrarily late
row in its extension.”  A fixed finite scale block has only a finite forced
window.  Equation (1) instead chooses the scale from the absolute pull.

## 3. Solver-free finite audit

`constant_tail_late_pull_horizon.py` packs independent source words into
Python bit planes and replays the exact dependency triangle.  It was checked
against literal scale extension on 1,936 forced rows through source length
seven.

The frozen audit found no surviving pull at `j>=n`, which is stronger than
DLP, in:

```text
hard-core word/tail cases through n=23:        392,830
surviving pulls in that corpus:                 62,903
nonfinal pulls in that corpus:                  31,595
late pulls:                                          0

aligned stored GA word/tail cases:                   8
surviving pulls:                                    19
late pulls:                                          0

random word/tail cases, n=24,...,128:          240,000
surviving pulls:                                36,433
late pulls:                                          0.
```

After registration, the source-language restriction was relaxed from
hard-core words to every word over `{1,2}`.  All 4,194,300 word/tail cases
through length 20 again have zero late pulls.  A four-state source relaxation
is false: an arbitrary-source SAT control exists already at length two.
This identifies the binary state alphabet, not the internal no-`11` grammar,
as the essential source restriction for the observed diagonal bound.

These are finite results only.

## 4. Exact diagonal CNF and negative proof-complexity result

For each `(n,c,r)`, `late_pull_diagonal_sat.py` constructs the right-edge
triangle from `0^n W`, constrains every symbol of `W` to state `1` or `2`,
forces cut symbol `c` through row `n+r+1`, keeps the appended endpoint
hard-core, and asserts transition `1 -> 2` at row `n+r`.  It is SAT exactly
when DLP fails at that triple.

The encoding agrees with literal enumeration on all 42 formulas through
`n=7`.  Both negative controls are SAT and replay exactly:

```text
arbitrary four-state source: n=2, tail=3, r=0, W=33;
dropped continuation no-11: n=5, tail=3, r=1, W=12121.
```

All six tail/residue formulas are UNSAT for every `1<=n<=20`.  This does not
prove the family.  Generic resolution also fails the preregistered proof-form
test: among Glucose proofs, maximum added-clause width grows from at most six
at `n=2` to 81 at `n=10`; CaDiCaL conflicts grow from thousands at `n=10` to
roughly 93,000--129,000 at `n=20`.  No stable local clause or recurrence was
visible, so the intended sweep to 40 was stopped under the growth kill
condition.  The UNSAT table is evidence for DLP, not an induction.

There is also an exact negative for a literal bounded patch around the pull.
At `n=12`, retaining only the last six constant-cut constraints makes the
tail-2, residue-zero formula SAT even when both the source and continuation
are hard-core:

```text
W:          121212222121
extension:  22122122122122
cut:        01202332222222
                         ^ last six are constant 2
target:                 1 2 2
```

The target pull is the `1 -> 2` at extension row 12.  With the entire cut
history imposed, the formula is UNSAT.  At `n=12`, the minimum number of
terminal constant-cut constraints needed for UNSAT is respectively

```text
tail 2, residues 0/1/2:  8,6,9
tail 3, residues 0/1/2:  6,6,5.
```

Thus the three-row reduction identifies only three *event positions*; it
does not turn the theorem into a literal `3 x 3` patch check.  The displayed
certificate kills every proof using at most the final six cut symbols and no
summary of the earlier triangle.  It does not rule out a larger or
history-carrying finite state.

## 5. Relation to the other live routes

DLP is the exact intersection of three earlier ideas:

- **scale blocking:** an absolute endpoint position is placed in a
  length-`n` forced block;
- **endpoint/event bridge:** only `1 -> 2` pull events need to be excluded;
- **three-row spacetime alignment:** the residue `m mod 3` leaves exactly the
  three candidate event rows in (DLP), although the six-row counterexample
  above proves that the needed cut history is not a literal local patch.

The alpha-support route remains a possible way to prove DLP, but all its
early-row obligations are dispensable.  The deterministic halving and full
diagonal-support conjectures remain stronger fallbacks.  The next proof
attempt should therefore target a three-row triangular boundary identity,
or a finite interpolant specific to `j=n+r`, rather than a matching across
all survival rows.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_late_pull_horizon.py

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/late_pull_diagonal_sat.py \
  --max-n 20 --proof-through 10
```

The preregistrations are `PREREGISTRATION-LATE-PULL-HORIZON.md` and
`PREREGISTRATION-LATE-PULL-DIAGONAL-CNF.md`.

# Pre-registration: mu(n), the SMALLEST sufficient cell set

Frozen 2026-08-30, before `min_gmus.py` was run for the first time.

**Object.** `mu(n)` = size of the minimum-cardinality set `G` of rule-bearing
cells of the diamond `D_n` such that enforcing the rule exactly on `G` (all
other cells free) is unsatisfiable together with the wrong-value unit at
`(n,0)`.  Computed exactly by implicit hitting-set SMUS.

**Why.** `mu(n) - 2` is a valid lower bound on the length of any resolution
derivation of `c_n` from the light-cone CNF (leaf-counting bound, derived in
`min_gmus.py`'s docstring).  It is the only sound bridge from the stored GMUS
probe to a derivation-length bound.  The stored probe measured a
DELETION-MINIMAL set, which is an upper bound on nothing and a lower bound on
nothing.

**Hypothesis under test.** `mu(n)` is a constant fraction of `|D_n|` (i.e.
`Theta(n^2)`), matching the deletion-minimal numbers 33/41 at `n=8`.

**Strong outcome.** `mu(n)` tracks the deletion-minimal size closely at every
computable `n`. Then the leaf-counting bound would give, at those `n`, an
explicit derivation-length lower bound quadratic in `n` — but see the kill
conditions, which apply regardless.

**Inverted outcome (kill condition K1), flagged loudly if it fires.** `mu(n)`
is substantially below the deletion-minimal size and/or scales visibly
sublinearly in `|D_n|`.  Then the deletion-minimal 76-82% fill is an artifact
of the deletion order and carries no lower-bound content at all, and the
bridge from the probe to R9 is dead as measured.

**Kill condition K2 (Rule 90 filter), decided independently of the numbers.**
If the same argument applied to rule 90 also yields a quadratic-in-`n` bound,
the technique does not discriminate the nonlinear rule from the additive one
and fails `PATH.md` section 0's standing filter.  Rule 90 is run as the
control at the same `n`.

**Kill condition K3 (obstruction H).** Any `mu(n)` measured on finitely many
`n` establishes nothing asymptotic.  Recorded in advance: even the strong
outcome yields a bound only at the `n` actually computed, never a theorem.

**Budget.** 900 s per band.  Bands `n = 4, 6, 8, 10, 12`, extended only if
cheap.  A band that times out is reported as a wall, not as a number.

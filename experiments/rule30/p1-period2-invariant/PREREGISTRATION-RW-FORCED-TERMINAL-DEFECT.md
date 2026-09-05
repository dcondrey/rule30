# Preregistration: forced terminal exclusion on the three RW rows

Date: 2026-09-04 (revised same day after an advisor pass caught a trivial
kill condition, a drifted reading of "rows n,n+1,n+2", and an unverified
range claim in the first draft)

Status: design frozen here (unchanged below). The section 4 measurement
has now been run: see `RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md` —
`|H_r(n)| = 0` exactly for `n = 1..16`, every `r`, both `c`, stronger than
the decay question this document poses. Not yet extended past `n=16`.

## 0. Why this route, and why not the alternatives already killed

`PROOF-STATE-CAPSULE.md` section 7 and `RESULTS-PSI-ANCESTRY-LAW.md` section
10 jointly fire the capsule's own pre-registered fallback: the full-generality
`(BWH+)` defect `Delta_j(W) = Psi_n(W)_j + Psi_n(W)_{j+1}` has algebraic degree
exactly `n` in the source bits at every measured `n` (4 through 15), so no
bounded-arity seam law can compute it. Separately, `PREREG-psi-constraint-counting.md`
found the empirical near-miss rate for `(BWH+)` does not shrink with `n`, so
its empty census to `n=20` is thin evidence, not a proof surrogate. Both facts
point the same way: stop trying to prove `Delta_j != 0` for *some* `j` over
*all* `W in {1,2}^n` (full BWH+). The capsule's own fallback sentence is:
"weaken to DLP/RW ... and target the forced adjacent `E` change at rows
`n, n+1, n+2` rather than for every arbitrary binary source."

This is genuinely new: `grep -rl "forced adjacent" .` hits only the capsule
and the ancestry-law report, no script or prereg formalizes it yet.

## 1. Reading "rows n, n+1, n+2" — corrected

The first draft of this document read the phrase as a 3-coordinate tail
window inside a single RW instance. That reading was not grounded in any
cited document and was dropped after review. The reading adopted here
instead follows `PREREGISTRATION-BINARY-WEDGE-HORIZON.md`'s own gloss of the
same object: `(BWH)` "is strictly stronger than the three-row late-pull
diagonal, which only needs to exclude a particular terminal pull after
`n+2`, `n+3`, or `n+4` binary continuation symbols." Three continuation
lengths — `n+2`, `n+3`, `n+4`, one per `r in {0,1,2}` — each contributing one
terminal row. So "rows n, n+1, n+2" denotes the three separate RW instances
themselves (indexed by `r`), each asking for exactly one thing: is the
*last* forced step of that instance's continuation excluded. This is weaker
than the tail-window reading, which is the direction section 7 explicitly
asks to move ("weaken immediately"), and it matches RW's own definition
directly rather than requiring a new multi-coordinate object.

Concretely, per `r`: RW at `(n,r,c)` already IS the single terminal claim —
its defining condition `P^n(I(f))=c^{n+r+2}` combined with the terminal pull
`f[-3:-1]=12` says the *whole* continuation is constant and the *last*
appended step is preceded by the specific pull pattern. So under this
reading there is no new object to define past what `RESULTS-DLP-ROTATED-WEDGE.md`
already states; this document's contribution is narrowing *which* `W` can
possibly matter (Setup, below) and asking whether nonexistence of a witness
at the last step can be argued locally for that narrowed population, rather
than needing the global degree-`n` polynomial the capsule's section 10
measurement rules out.

## 2. The collapse lemma (resolved by reading code, not by running it)

**Claim.** For fixed `(n,r,c)`, an RW witness exists iff the single word
`Q = late_pull_diagonal_sat.literal_extension(W, c, n+r+2)` is simultaneously
hard-core (incl. the `W`-`Q` junction) and terminal-pull `12a`; there is no
remaining existential over `Q`.

**Why this holds, read directly from `literal_extension`
(`late_pull_diagonal_sat.py:254-273`).** At each of the `n+r+2` appended
rows it tries all 4 states and keeps the *unique* one whose
`append_dependency_edge` output has last cell `== tail` (`tail` is `c`,
confirmed load-bearing here, not vestigial — each row is forced to the
*full* two-bit state `c`, not merely to `H=1`). By the triangularity already
proved in `psi_kernel.py`'s docstring (appending a symbol fixes exactly one
new final-output cell and never revisits earlier ones), forcing row `k`'s
last cell to equal `c` is forcing that row's *permanent* final-output value,
not a transient intermediate one. So `literal_extension` is exactly the
row-by-row incremental construction of the *only* word that can make every
one of the `n+r+2` final cells equal `c` — which is what `P^n(I(f))=c^{n+r+2}`
requires. `psi_kernel.psi`'s `Q_n(W)` forces only the high bit at each row
(`H=1`), which is weaker: it is the *same* word as `literal_extension` only
on the event that the low bit *also* comes out matching `c` at every row,
i.e. only on the event that `Psi_n(W)` is already exactly constant. That is
not circularity, it is the correct statement: **both constructions agree
everywhere `Psi_n(W)` happens to be constant, and disagree (or rather,
`literal_extension` is simply the object worth asking about, `Q_n(W)` is a
distinct word) everywhere it does not.** So the census question "is
`Psi_n(W)` constant" and the RW question "does `literal_extension(W,c,...)`
survive hard-core + `12a`" are asking about the same event for the same `W`,
just computed two different ways, and the existing `(BWH+)` exact-constant
counts (`RESULTS-PSI-ANCESTRY-LAW.md` section 6) already are, for `r=0`, an
exhaustive enumeration of every `W` for which an RW-style full-constancy
witness could possibly exist — no independent check of `literal_extension`
against `psi_kernel.psi` is needed; it follows from what each function is
defined to do. This closes the former Setup step S1 without a run.

**What is NOT already covered.** The `(BWH+)` table in
`RESULTS-PSI-ANCESTRY-LAW.md` section 6 is for continuation length exactly
`n+2`, i.e. `r=0` only. `r=1` (length `n+3`) and `r=2` (length `n+4`) pair a
fixed source length `n` with a continuation *not* equal to `n+2`, so they do
not correspond to any `BWH+(m)` instance at any `m` (`BWH+(m)` always pairs
source length `m` with continuation `m+2`; there is no `m` with source
length `n` and continuation `n+3` or `n+4` in that family, since that would
require `m = n` and `m+2 = n+3` or `n+4` simultaneously, which is
inconsistent). So **only `r=0` is already covered by existing exact data
through `n=18`**. `r=1` and `r=2` are new computation: extend the same
forced recursion (`literal_extension` already parameterizes on the target
length directly, so this is calling it with `n+3` / `n+4` rather than any
new derivation) and get exact constant-`Psi_{n,r}` counts for those two
families for the first time. This is cheap (same machinery, one more
argument value) and is Setup step S1' below, not a research gap.

## 3. Setup (before the pre-registered test)

- **S1 (closed above by reading code).** No run needed. Recorded here so a
  later reader does not re-open it as pending.
- **S1'.** Compute exact constant-`Psi_{n,r}` counts for `r=1` and `r=2` at
  the same exhaustive horizon `RESULTS-PSI-ANCESTRY-LAW.md` section 6 used
  for `r=0` (`n` up to the largest exhaustive-feasible value, expect
  `n<=17` or so given the one/two extra forced rows raise cost slightly).
  If any `W` gives constant `Psi_{n,1}` or `Psi_{n,2}` at `n>=7`, this is
  potentially a live RW/BWH+ counterexample family at `r=1,2` even where
  `r=0` has none — check it against hard-core + `12a` immediately, do not
  defer.
- **S2.** For every `W` found constant in S1' or in the existing `r=0`
  table, check hard-core + `12a`-terminal directly (cheap, a handful of
  cases expected, likely zero). This is the actual RW existence check for
  the exhaustive range; it needs no new theory, only filtering already- or
  now-computed constant-`Psi` words.

## 4. What remains open after S1'/S2, and the actual pre-registered target

If S1'/S2 come back empty (expected, consistent with `r=0`'s existing zero
count), RW is empirically excluded over the exhaustive range for all three
`r`, same caveat as always: an empty census is not a proof, and
`PREREG-psi-constraint-counting.md`'s near-miss statistics say the
unrestricted (`r=0`, arbitrary `W`) empty count should not be trusted to
extrapolate. That caveat is about the *unrestricted* population, though —
it says nothing directly about the size or shape of the much smaller
hard-core + `12a`-terminal subpopulation, which is a different question:

**Pre-registered question.** Let `H_r(n) = {W in {1,2}^n :
literal_extension(W,c,n+r+2)` survives the hard-core and `12a`-terminal
checks in `rotated_wedge_witness}`, i.e. the population for which an RW
witness is even a live possibility before asking about constancy. Measure
`|H_r(n)| / 2^n` for each `r`. If this ratio decays with `n` (rather than
holding near a constant, e.g. `1/8` from the two local constraints alone),
that decay — not an appeal to the `(BWH+)` near-miss statistic, which does
not apply to this restricted population — is the actual argument for why
RW might be provable where `BWH+` is not: a shrinking candidate population
combined with the existing near-`1.0` constant-rate-per-candidate would
still shrink the expected witness count toward zero, which is the shape of
argument the capsule is asking for, not a claim that no such argument
exists yet.

**Kill condition (corrected).** This document does NOT propose "no `W` has
a constant tail" as a kill condition — a single `W` with an unrelated
coincidental agreement is not evidence against anything, since nothing here
yet claims a *forced* law linking hard-core/`12a`-terminal membership to
nonconstancy. The kill condition for the actual next step is narrower and
honest: if `|H_r(n)|/2^n` does *not* decay (stays within a constant factor
of its small-`n` value across the measured range), the "shrinking
population" argument sketched above has no force and this route contributes
nothing beyond S1'/S2's already-cheap exhaustive check. That outcome does
not refute RW; it says this document's proposed argument shape is not the
one that will prove it, and the next step reverts to the capsule's other
listed open item (the endpoint-restart-cocycle extension) rather than a
retry of this shape under a new name.

## 5. Controls

1. `H_r(n)` computed two independent ways: forward via `literal_extension`
   plus a direct hard-core/`12a` filter, and via `rotated_wedge_witness`'s
   own `surviving`/`terminal_pull` booleans, must agree exactly on every `W`.
2. S1'/S2's `r=1,2` constant-`Psi` counts must reduce to the existing `r=0`
   table's counts when the extra one or two forced rows are dropped from
   the check (i.e. re-deriving the `r=0` numbers from the same code path
   used for `r=1,2` is a regression check on the new code, not new physics).
3. `|H_r(n)|` must equal exactly the count of `W` for which `S2`'s filter
   returns true; report both the exact count and the ratio, not the ratio
   alone, so a later reader can recompute the denominator check.

## 6. What this does not claim

This does not claim RW, DLP, or period-two exclusion is true or false. It
does not claim a bounded-arity law for the restricted population exists —
section 4 states a measurement (population decay) that would motivate
looking for one, not a proof that one exists. Horizon extension past the
already-established hard-core census range is explicitly out of scope, per
`PROOF-STATE-CAPSULE.md` section 5 and 7.

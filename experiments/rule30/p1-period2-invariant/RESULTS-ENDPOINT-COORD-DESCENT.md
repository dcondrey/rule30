# Result: endpoint-coordinate descent (fusion #2) killed at the same wall as source-word descent

Date: 2026-09-04. Scope: David's proposed fusion #2, "endpoint-coordinate
descent + counting-line" -- fix `MEMO-RW-DESCENT-EXPLORATION.md`'s
padding-misalignment obstruction by defining the `n -> n-1` reduction on the
endpoint/cut coordinate `e` directly, holding distance-to-cut fixed, instead
of on the source word `W`.

## Verdict up front

**No exact reduction exists here either, and the failure is quantitatively
the same failure already on record.** Dropping any single coordinate from a
length-`n` endpoint sequence and comparing the resulting length-`(n-1)`
endpoint's diagonal against the original's *deepest* cut coordinate (the one
DLP/RW/`H_r(n)` actually reads) gives, at best, a constant ~40.6% exact-match
rate that neither grows to 1 (no identity) nor decays to 0 (not simply
irrelevant) as `n` grows through 2..8. That constant is the same order as
the independently-measured 0.4-per-level flip-pairing coverage rate already
recorded in `BACKLOG.md` section 17 ("only `e_0, e_1, e_2` preserve earlier
levels... a flip at depth `delta <= n-4` is alive at level `j` with
probability `0.4^j`"). Three independently-coded checks (flip-pairing on
structured hard-core sources, block-halving's per-level ratio, and this
check on raw unconstrained 4-state endpoint sequences) now converge on the
same ~0.4 constant. That convergence is itself evidence the 0.4 is a real
structural correlation of the underlying Rule 30 recursion, not an artifact
of any one encoding -- but a stable non-1, non-0 correlation is exactly what
an exact reduction lemma cannot be built from.

## 1. What "holding distance-to-cut fixed" concretely means and how it was tested

Read directly against `psi_kernel.Endpoint` (not a reimplementation): for a
length-`n` sequence of raw endpoint symbols `seq in {0,1,2,3}^n`,
`Endpoint.diagonal` after `n` appends is the array of cut coordinates
`I(e)_0 .. I(e)_{n-1}`, and `diagonal[-1]` is the deepest one -- the exact
quantity `H_r(n)`/DLP-RW forces at the terminal row. "Holding distance to
cut fixed while dropping a coordinate" was tested as: for every drop
position `p in 0..n-1`, build `short = seq` with position `p` removed
(length `n-1`), and ask whether `short.diagonal[m] == full.diagonal[-1]` for
some FIXED index `m` (depending only on `n, p`, not on the sequence's
values) -- i.e. whether removing coordinate `p` and reading out at a fixed
offset reproduces the deep cut exactly, for every sequence.

An earlier version of this check used a weaker "any-shift, any-overlap"
criterion and returned 100% agreement at every `n` for drop-first -- that
was an artifact: the shift that satisfied it left almost no positions in
range to check (an early, shallow window only), never touching the deep
coordinate that matters. Restated and rerun against the actual deepest
entry (`scratch_endpoint_coord_check.py`), the numbers are:

```
n=2 total=16    best_drop_pos=0  best_target_index=0  match=    4/16    = 0.2500
n=3 total=64    best_drop_pos=0  best_target_index=1  match=   26/64    = 0.4062
n=4 total=256   best_drop_pos=0  best_target_index=2  match=  104/256   = 0.4062
n=5 total=1024  best_drop_pos=0  best_target_index=3  match=  416/1024  = 0.4062
n=6 total=4096  best_drop_pos=0  best_target_index=4  match= 1664/4096  = 0.4062
n=7 total=16384 best_drop_pos=0  best_target_index=5  match= 6656/16384 = 0.4062
n=8 total=65536 best_drop_pos=0  best_target_index=6  match=26624/65536 = 0.4062
```

Every drop position other than `p=0` (first symbol) scores strictly lower
at every `n` tested (full per-`(n,p)` table is in the script's output).
`p=0` plateaus exactly at `13/32 = 0.40625` from `n=3` through `n=8`, five
consecutive doublings of the sample space with no drift -- this is a stable
constant, not a slowly-decaying transient, and a background rerun at
`n=9,10` (killed once the plateau was already unambiguous at 5 points) was
not needed to make that call.

## 2. Why this is the same obstruction as the source-word case, not a new one

`MEMO-RW-DESCENT-EXPLORATION.md` part 1 already identifies the mechanism:
`I(e)_t` depends on the *entire* window `e[floor(t/2)..t]`, a width growing
linearly with `t`, with no fixed-radius truncation available. Dropping any
one coordinate from that window and re-reading at a fixed offset changes
which values feed the recursion for every subsequent step; the only way the
deep entry could still come out equal is if the recursion happened not to
depend on the dropped coordinate at all near the boundary, which is exactly
the coincidence rate ~0.4 measures for the raw, unconstrained alphabet. The
source-word memo found the analogous thing from the other direction (fixed
padding convention, hard-core-restricted words): a plateauing absolute
count of accidental matches (7 at `n=10..12`) against an exponentially
growing candidate population, i.e. fraction -> 0. Here, on the raw
unconstrained recursion, the fraction does not decay to 0 (there is no
Fibonacci-growth restriction to a sparse subpopulation forcing it down) --
it instead sits at a nontrivial constant. Both are still "not an identity";
0.4062 exact-match is not usable as a reduction lemma any more than a
0-limit fraction is. The specific value ~0.4 recurring across three
unrelated codings (flip-pairing's empirical `0.4^j`, block-halving's
measured per-level ratio, and this raw-endpoint check) is worth recording
as a possibly-real invariant of the construction, but it is evidence *for*
a probabilistic/measure-theoretic framing (per-level survival is governed
by a fixed non-degenerate correlation, not a deterministic law) and
evidence *against* any exact combinatorial descent of the kind fusion #2
proposed.

## 3. Bottom line for fusion #2

The premise -- that moving the reduction from the source word `W` onto the
endpoint/cut coordinate `e` would sidestep the padding-coupling obstruction
-- does not hold. The obstruction was never really about the specific
`0^n`-padding convention; it is that the cut coordinate's dependency window
width grows with depth and has no compressible summary (this is the same
fact underlying every killed finite-automaton/bounded-quotient route in
`BACKLOG.md`). Reformulating the reduction on `e` instead of `W` moves where
the growing window shows up but does not shrink it. No further variant of
"drop one coordinate, read out at a fixed offset" is worth trying without a
new idea for what makes an offset choice non-coincidental; none was found
here, and this document is registering that absence, not proposing a next
attempt under a different name.

## 4. Reproduction

`scratch_endpoint_coord_check.py` (this directory, throwaway, not wired
into the pipeline), against `psi_kernel.Endpoint` unmodified. Run with no
arguments; prints the table above (`n=2..8`) plus the full per-drop-position
breakdown.

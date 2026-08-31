# Rule 30 alternating-trace fiber: bounded-depth exclusion certificates

## Status

**OPEN, with verified bounded-depth certificates.**  This cycle does not prove
the period-two exclusion; it reduces it to one uniformity gap and certifies
every instance of bounded left depth up to 24.  Nothing here bears on the
center-column prize problem beyond the period-two subcase of the
finite-configuration question.

Context: after the zero-tail note was endorsed, J. Kari suggested excluding
nonconstant periodic traces next, eventually all of them.  Both constant
traces are settled (zero: the note; one: the checkerboard fiber in
`RESULTS-eventual-period.md`).  This arm attacks the first nonconstant case,
the alternating trace, at the same fiber level as the note.

## PROVED: zero-set reduction

For any prescribed trace `c` and right half, the compatible configuration is
unique (Lemma 1 of the note).  Rotating the rule at the origin,

```text
l_t = c_(t+1) XOR (c_t OR r_t),
```

so `l_t` depends on `r_t` only at times with `c_t = 0`.  Column `-2` is
`x(t,-2) = l_(t+1) XOR (l_t OR c_t)`, a function of `(c, l)`, and inductively
every deeper column is a function of the two columns to its right.  Hence:

> The forced left half-plane is a function of the trace and of column 1
> restricted to the zero set `{t : c_t = 0}`.

For the alternating trace the zero set is one parity class.  Write
`rho_k = r_(2k)` (phase `01`, i.e. `c_0 = 0`) or `rho_k = r_(2k+1)` (phase
`10`).  The pinned parity contributes `l_t = 1` outright.  The entire forced
left half `L_j = x(0,-j)` is then a triangular function of `rho` alone:
`L_j` needs roughly `rho_0..rho_(j/2)`.  This is the general form of the
reduction in `PATH.md` section 2, specialized to the exact fiber: the
one-phase is discharged by the pin, and all remaining freedom is `rho`.

Explicitly, phase `01`: `L_1 = NOT rho_0`, `L_2 = rho_0`, `L_3 = NOT rho_1`,
`L_4 = rho_0 AND rho_1`, `L_5 = rho_2 XOR (rho_0 OR NOT rho_1)`, consistent
with the recorded stencil (`L_3 = R_1 OR R_2 OR R_3` since
`rho_1 = NOT(R_1 OR R_2 OR R_3)`).

## VERIFIED: bounded-depth exclusion certificates

Say a configuration has *left depth `d`* if its initial row vanishes at every
position left of `-d`.  Claim(d): no configuration of left depth `d` has
central trace exactly `(01)^inf` (resp. `(10)^inf`), regardless of its right
half, finite or not.

Certificate for Claim(d): a level `k(d)` such that **every** `rho`-prefix of
length `k(d)` already forces some `L_j = 1` with `j > d`.  Violation is
monotone under prefix extension (the triangle only grows), so a pruned BFS is
sound; for `d <= 12` the certificate was additionally re-verified by unpruned
exhaustive enumeration of all `2^k(d)` prefixes.

Measured certificate levels (probe defaults print `d <= 16`; the run below
went to 24; exhaustive through 12, BFS beyond):

```text
phase 01: d:  0  1-4  5-7  8-11  12-14  15-17  18-19  20-21  22  23-24
          k:  1   4    5     9     15     16     17     19    21    22
phase 10: d:  0  1  2-4  5  6  7-8  9-10  11-13  14-18  19-21  22-23  24
          k:  1  1   3   4  5   6    9     15     16     19     20     21
```

Every `d` through 24, both phases, is certified.  (An earlier draft of this
section claimed "survivor counts peak at 64" and "~15 distinct wavefront
values per level"; both described only the late post-knee levels.  Measured
with exact state instrumentation: survivors are the full `2^k` prefixes up
to the knee `k = d/2`, peaking at 4096 prefixes / 1009 distinct frontier
states at the `d = 24` knee, then halving per level.  The halving is now
explained exactly; see the parity section below.)  Consequences, stated
exactly:

* No configuration with left depth `<= 24` has central trace exactly
  `(01)^inf` or `(10)^inf`.  In particular no finite configuration of left
  support depth `<= 24` does, with **no bound on its right support**.
* This does not yet exclude the alternating trace for all finite
  configurations: a finite configuration of larger left depth, and the
  eventually-alternating case (whose translate `F^T(x)` has left depth up to
  `w + T`), need Claim(d) for unbounded `d`.

The uniformity gap is the whole remaining obligation:

> **Open target.**  Claim(d) for every `d`.  Equivalently: no `rho` sequence
> keeps `L(rho)` eventually zero.  With it, no finite configuration has an
> eventually 2-periodic nonconstant center column (translate to the onset of
> periodicity; the translate is finite, nonzero, with exact alternating
> trace).

Two facts constrain the proof search.  The certificate level grows roughly
linearly (`k(d) ~ d`), so the trace-side and cone-side collide within one
cone-return time, not at the `O(log t)` wall of trace-anchored propagation
(`PATH.md` 3.1); and the post-knee survivor dynamics is now known exactly
(next section): deterministic with one parity check per level.

## PROVED: the survivor automaton is a parity-checked deterministic map

This resolves the A1 instrumentation question ("build the exact transducer
on reconstruction wavefronts") in closed form.

**Setup.**  Reconstruct incrementally.  After consuming `T` column `-1`
values `l_0..l_(T-1)`, the forced triangle's frontier is the pair of
anti-diagonals

```text
A_j = x(T-j, -j)     (t + j = T,   j = 1..T)
B_j = x(T-1-j, -j)   (t + j = T-1, j = 1..T-1)
```

Consuming `l_T = v` computes the next anti-diagonal `C` shallow-to-deep by
the rotated rule `x(t, -(j+1)) = x(t+1, -j) XOR (x(t, -j) OR x(t, -(j-1)))`:

```text
C_1 = v,   C_(j+1) = C_j XOR o_j,   o_j = A_j OR B_(j-1),   B_0 := c_(T-1),
```

and its deepest entry is the one new forced output
`L_(T+1) = x(0, -(T+1)) = C_(T+1)`.

**Closed form.**  The XOR chain never absorbs, so it telescopes:

```text
L_(T+1) = v XOR parity(o_1 .. o_T).
```

The new output is the fed column `-1` value XOR the parity of the OR-word
of the two stored diagonals.  That is the whole transducer.

**Consequences.**  A configuration of left depth `<= d` has `L_j = 0` for
all `j > d`.  Once `T >= d` (the knee, level `k = d/2`), every step is
constrained:

* zero-set steps feed `v = NOT rho_k`, so the surviving rho bit is
  **forced**: `rho_k = 1 XOR parity(o)`.  Branching factor exactly 1.
* pinned steps feed `v = 1` with no freedom, so survival requires
  **`parity(o) = 1`**, one pure parity check on the state per level.

So past the knee the fiber BFS is a set of non-branching orbits of a
parameter-free deterministic map (`A' = C`, `B' = A`, `v` forced), each
killed at its first pin-parity failure.  This explains the observed
halving per level (the checks empirically pass ~1/2 the time: 2082/4096 at
the `d = 24` knee), and gives

```text
k(d) = d/2 + (longest forced-orbit survival from a depth-d seed) + 1.
```

**Verification** (all machine-checked, `--parity D`):

* Controls C6 (incremental frontier equals `left_from_rho`, 64 random rho,
  both phases) and C7 (incremental BFS equals the `violates()` BFS,
  survivor-set equality per level, `d = 6, 10`, both phases).
* The closed form reproduces the alive/dead status of **every** BFS
  transition at `d = 16, 24, 32`, both phases (203/133, 2008/1322,
  19108/12981 post-knee states respectively), and the forced-rho /
  branching-1 / pin-parity claims hold on all of them.
* Certificate levels reproduced: 16/16 (`d=16`), 22/21 (`d=24`).
  **Prediction confirmed:** from the `kseed = 16` orbit maximum (16, below)
  the formula predicts `k(32) = 33`; the direct `d = 32` run then certified
  at level 33, both phases.

**Forced-orbit measurements** (`--orbit K`): iterate the forced map from
every rho-seed of length `kseed`, requiring all post-seed outputs zero.
Survival to first pin failure is geometric-ish with mean ~1; the maxima
grow roughly linearly:

```text
kseed:          8   12   16      (exhaustive, both phases)
max survival:   7    9   16
```

matching, for phase `01`, `k(16) = 8+7+1`, `k(24) = 12+9+1`,
`k(32) = 16+16+1` exactly.  (Phase `10`'s leading pin shifts its seed
correspondence to odd effective `d`, so its levels can differ by one:
`k(24) = 21` there.)  No seed survived past its cap (kill condition did
not fire).  Linear growth of the
maxima means per-`d` certificates can never reach uniformity by themselves;
the theorem must come from the map.

**The open target, restated exactly.**

> No finite seed (frontier pair of a finite rho-prefix triangle) follows
> the forced map with every pin parity equal to 1 forever.

A1's "zero-emitting cycle" is now concrete: an orbit of this parameter-free
map passing every pin check.  One reachable from a finite seed is a
left-finite counterexample.  The wallpaper member `{1,4}` shows
infinite-left seeds CAN pass forever-adjacent structure (its outputs
contain ones at unbounded depth, so it violates every finite `d`; no
contradiction), so any proof must again use left-finiteness of the seed.
The raw state (the diagonal pair) grows by one cell per step, so
finiteness is not available in raw form; the remaining hunt is a finite
invariant of the forced map sufficient to force a pin failure — e.g. the
dynamics of the OR-word `o` itself, or a weight/potential argument on ones
density in `A` under the forced update.

## VERIFIED: the fiber over the alternating trace has left-periodic members

Right half `{1,4}` (i.e. `R_1 = R_4 = 1`), phase `01`: the forced left half
is spatially 7-periodic, word `0110010` repeating from depth 1, verified to
depth 1024; the left half-plane is a 7 (space) x 4 (time) wallpaper.  Its
`rho` is the alternating sequence, verified to `t = 20000` by driven
simulation.  At `W = 10`, 20 of 1024 right halves force 7-periodic tails in
the same rotation class.  Driven-column periods for `{1,4}`: columns 1..6
have period 4, columns 7..14 period 8, columns 15+ none `<= 64` in the
sampled window; the period-doubling profile matches the known nested edge
structure (Rowland 2006), which is the natural route to proving the lock.

Status: the infinite wallpaper member is **not proved**; the `rho` lock is
empirical.  What it already establishes is sharpness: the fiber contains
left-periodic members, so any exclusion must use left-finiteness itself.
The C_m analogue for period two is "forced ones at unbounded depth", not a
single forced tail; forced tails here vary with `rho` (most look chaotic).
No finite candidates among all right halves at `W=10, D=192` or `W=12,
D=288`, either phase.  Max forced-zero gap 15 (phase `01`) and 16 (phase
`10`), identical at `W=10` and `W=12`: the gap did not grow with the right
radius, consistent with a uniformly bounded forced-one density.

## Controls

All embedded in the probe and asserted before any measurement:

* C1 zero-trace fiber reproduces the prefix-OR classification (Theorem 2 of
  the note) over all `2^8` right halves.
* C2 all-one-trace fiber reproduces the checkerboard.
* C3 alternating stencil `L_1..L_4` matches the recorded stencil.
* C4 forward brute force reproduces the SMT `p=2` horizon row `6,6,6,6,8,9`
  for `w = 1..6` (independent encoding: row-as-integer evolution).
* C5 the `rho` reduction matches direct fiber reconstruction on random right
  halves, both phases.
* Rule 90 note: the same enumeration under rule 90 (`W=8, D=128`) also finds
  no finite member of its alternating fiber, so this exclusion is not
  automatically Rule-30-specific.  That is acceptable for a per-trace partial
  result; the `PATH.md` filter lesson applies per trace (rule 90's actual
  eventually periodic column is the zero trace, whose exclusion is exactly
  what fails for rule 90).

## Falsified along the way

The 7-periodic tail word was first read off a window as `1001100` and
transcribed to depth 1 in the wrong rotation; the depth-1 word is `0110010`.
The probe pins the correct alignment.

## Next targets, with kill conditions

* **A1, survivor automaton — instrumentation DONE, reduced to the parity
  question.**  The exact transducer is the parity-checked deterministic map
  above.  Remaining: prove no finite seed passes every pin-parity check
  forever.  Candidate angles: dynamics of the OR-word `o` under the forced
  update; a potential/weight argument on ones density; eventual periodicity
  classification of forced tails (the wallpaper is the eventually-periodic
  infinite-seed example).  Kill: a seed whose forced orbit survives an
  unbounded run (that is a left-finite counterexample and settles period
  two the other way); exhaustive seeds to `kseed = 16` all die within 16
  steps.
* **A2, wallpaper theorem.**  Prove the `{1,4}` lock by finite column-band
  certificates in the driven half-plane (Rowland-style nesting).  Kill: a
  lock break at some larger `t`; then the 7-periodic family claim is
  withdrawn as a transient.
* Strong outcome for the arm: "no left-finite configuration has exactly
  alternating central trace", which yields: no finite configuration has an
  eventually 2-periodic nonconstant center column.  That is the first
  nonconstant entry in Kari's requested sequence.

## Reproduction and spending

From `experiments/rule30`:

```bash
uv run python alt_trace_fiber_probe.py                 # controls + d<=16 + W=10 + wallpaper
uv run python alt_trace_fiber_probe.py --certify 24
uv run python alt_trace_fiber_probe.py --enumerate 12 288
uv run python alt_trace_fiber_probe.py --automaton 24 --dump ../../runs/alt-trace-automaton/d24-outputs.json
uv run python alt_trace_fiber_probe.py --parity 32     # closed form vs BFS, k(32)=33
uv run python alt_trace_fiber_probe.py --orbit 16      # forced-orbit survival, exhaustive seeds
```

Per-level survivor state dumps for `d = 8, 16, 20, 24` are in
`runs/alt-trace-automaton/`.

Modal: $0.  Paid model-provider calls: $0.  Everything above ran locally;
the largest single run (`--parity 32`) took about four minutes.

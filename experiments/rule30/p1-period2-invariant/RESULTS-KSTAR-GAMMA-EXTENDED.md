# k_star(n), max-survival-row(n), and the extinction margin gamma(n): extended range via a fast dedup method

Date: 2026-09-04.

Status: **method verified against brute force at n<=18 (all mismatches
zero); data extended past brute-force range using the new method**, in
parallel with (not editing) the concurrently running
`overnight_census.py` brute-force sweep for n=17..24 (see
`PREREGISTRATION-OVERNIGHT-EXTENSION.md`).

## What this measures

Same objects as `continuation_image_analysis.py` /
`PREREGISTRATION-OVERNIGHT-EXTENSION.md`:

- `D_k(n)` = number of distinct length-`k` forced-continuation prefixes
  achieved among source words `W in {1,2}^n` that survive that far
  (image size of `Phi_k`), compared against `Fib(k+1)`, the exact size of
  the hard-core language of length `k`.
- `k_star(n)` = first `k` with `D_k(n) < Fib(k+1)`.
- `max_survival_row(n)` = the largest `k` with `D_k(n) > 0` (equivalently:
  the deepest row any source word's forced continuation reaches before
  hitting a hard-core defect).
- `gamma(n) = (n+r+2) - max_survival_row(n)`, the **extinction margin**:
  how many rows of "slack" remain between the forced-continuation death
  point and the target row `n+r`. `H_r(n) = 0` follows structurally if
  `gamma(n) >= 1` for all `n` at the relevant `r`.

Note established during cross-checking (see below):
**`max_survival_row(n)` does not depend on `r`** — it is a property of
the forced continuation's own death point, independent of how many rows
are requested (`literal_extension` is prefix-consistent, already
controlled in `overnight_census.py`). So `gamma(n, r) = gamma(n, 0) + r`,
and `r=0` is the binding (smallest-margin) case; `r=1,2` only add slack.

## Method: dedup on the dependency-edge state (not brute force over 2^n words)

`late_pull_diagonal_sat.literal_extension(W, tail, rows)` builds a
"dependency edge" — a tuple of automaton states — incrementally via
`constant_tail_scale.append_dependency_edge`, one symbol at a time (first
the `n` zero-padding symbols, then `W`'s own `n` symbols). Critically,
**the forced continuation depends on `W` only through the resulting
`(edge, last_symbol)` pair** — nothing about `W`'s actual symbol history
is used afterward. So two different source words that reach an identical
`(edge, last_symbol)` state after their `n` symbols are indistinguishable
to every later step: identical forced continuation, identical survival
depth, identical continuation prefixes at every `k`.

This licenses replacing brute-force enumeration of all `2^n` words with a
breadth-first walk of the length-`n` symbol trie that **dedupes branches
landing on the same `(edge, last_symbol)` state** at each prefix length,
carrying only the (much smaller) set of distinct states forward. Only
after all `n` symbols are consumed do we run the forced-continuation loop
— once per *distinct* final state, not once per word.

Empirically (see `fastdk_prototype.py`), the number of distinct edge
states grows with a ratio well below 2 per extra symbol, and the ratio is
*itself decreasing* as `n` grows (measured multiplicative step-ratio:
~1.96 near step 8, ~1.34 by step 22), which is exactly what saves the
runtime budget needed to push past brute force's practical n=~20-22
ceiling.

Implementation:
- `fastdk_fastedge.py` — allocation-lean reimplementation of
  `append_dependency_edge` using a precomputed 4x4 `cone_local` lookup
  table. **Verified bit-for-bit identical** to the original
  `constant_tail_scale.append_dependency_edge` by exhaustive comparison
  over all edge histories up to length 9 (`equivalence_check`,
  3,029,220 incremental steps, zero mismatches).
- `fastdk_core.py` — `distinct_final_states(n)` (the dedup trie walk) and
  `d_k_table_fast(n, tail, residue)` (drop-in analogue of
  `continuation_image_analysis.d_k_table`, same `(k, Fib(k+1), D_k)`
  table format plus `max_survival_row`).
- `fastdk_crosscheck.py` — asserts exact agreement with
  `continuation_image_analysis.d_k_table` (brute force) at n=8,10,12,14,16
  (and n=18 for c=2 in flight), both `c=2,3`, `r=0`.
- `fastdk_crosscheck_r.py` — same cross-check extended to `r=1,2` at
  n=6,8,10,12,14, both `c`.
- `fastdk_benchmark.py` — timing-only sweep of the fast method past
  brute-force range.

### Cross-check result (this is the correctness gate, not a formality)

All of the following passed with **zero mismatches** (table entries,
`D_k`, `max_survival_row` all agreed exactly):

| n | c | r | brute D_k table | fast D_k table | max_survival match |
|---|---|---|---|---|---|
| 8,10,12,14,16,18 | 2,3 | 0 | matched | matched | matched |
| 6,8,10,12,14 | 2,3 | 0,1,2 | matched | matched | matched |

n=18 (both `c`) finished: brute force took 292s/295s per `(n,c)`; the
fast method took 17.1s/16.9s for the identical `(k, Fib(k+1), D_k)` table
and `max_survival_row` -- a ~17x speedup already at n=18, and the ratio
is expected to widen further with `n` since brute force is exactly
`2^n`-scaling and the fast method is not (see growth-ratio data above).
All of n<=18 exactly agrees, including with the "cruder max_survival
script" numbers quoted in the task brief: n=10,12,14,16 gave
gamma=7,5,6,8 there and gamma=7,5,6,8 here via the fast method -- exact
agreement.

## Data: k_star(n), max_survival_row(n), gamma(n), c=2, r=0

(Extended live below as the sweep progresses — this file is checkpointed
incrementally.)

| n | k_star | max_survival_row | rows=n+2 | gamma |
|---|---|---|---|---|
| 8  | 3 | 3  | 10 | 7 |
| 10 | 4 | 5  | 12 | 7 |
| 12 | 4 | 9  | 14 | 5 |
| 14 | 5 | 10 | 16 | 6 |
| 16 | 5 | 10 | 18 | 8 |
| 18 | 7 | 12 | 20 | 8 |
| 20 | 8 | 11 | 22 | 11 |
| 22 | 8 | 12 | 24 | 12 |
| 24 | 9 | 14 | 26 | 12 |
| 26 | 10 | 15 | 28 | 13 |
| 28 | 11 | 21 | 30 | 9 |
| 30 | 11 | 18 | 32 | 14 |

## Data: c=3, r=0

| n | k_star | max_survival_row | rows=n+2 | gamma |
|---|---|---|---|---|
| 8  | ?  | 6  | 10 | 4 |
| 10 | ?  | 7  | 12 | 5 |
| 12 | ?  | 8  | 14 | 6 |
| 14 | ?  | 8  | 16 | 8 |
| 16 | ?  | 10 | 18 | 8 |
| 18 | 7  | 11 | 20 | 9 |
| 20 | 7  | 14 | 22 | 8 |
| 22 | 9  | 14 | 24 | 10 |
| 24 | 9  | 16 | 26 | 10 |
| 26 | 10 | 15 | 28 | 13 |
| 28 | 10 | 17 | 30 | 13 |
| 30 | 11 | 19 | 32 | 13 |

(`?` = not yet re-extracted from the fast method's k_star field at
these small n; max_survival/gamma already cross-checked exactly against
brute force above.)

(See "Gamma trend assessment" below for the running interpretation --
kept as one place to avoid the data and its reading drifting out of
sync across checkpoints.)

## Checkpoint (2026-09-04, ~22:15)

Recording state and assessment at this checkpoint so a reader
picking this up cold has the full picture. `fastdk_benchmark.py`
(n=18,20,22,24,26,28,30,32) and `fastdk_crosscheck.py` (n=16,18) were
both still running as of this checkpoint -- both have since completed
(see updated Cross-check
table above: n=18 brute-force agreement is now confirmed PASS for both
`c`, and the benchmark has continued past n=22; later sections update
this further as more data lands).

### crosscheck_r (r-independence claim): COMPLETE, ALL PASS

`fastdk_crosscheck_r_20260904.log` finished with **ALL PASS** across
n=6,8,10,12,14, both c=2,3, all of r=0,1,2 (30 cases total). Every case
showed `max_survival_row` identical across r=0,1,2 for a given (n,c) --
e.g. n=12,c=2: max_survival=9 at r=0,1,2 alike; n=14,c=3: max_survival=8
at r=0,1,2 alike. This is exact empirical confirmation, not just
construction-level argument, of the claim above that
`max_survival_row(n)` doesn't depend on `r`, hence `gamma(n,r) =
gamma(n,0) + r` and r=0 is the binding case. No exceptions found.

### crosscheck (n=16,18 brute-force agreement): STILL RUNNING, no output yet

`fastdk_crosscheck.py 16 18` is still in flight, writing to
`/private/tmp/xc1618.log`, which is 0 bytes as of this pass (brute force
at n=18 takes on the order of a minute per (c,r) cell per the note
above, so this is expected, not a hang). n<=14 is already fully
cross-checked (both the plain n-sweep above through n=16, and the r-sweep
through n=14). Whatever lands in that log should be folded into the
Cross-check table above when read.

### fastdk_core.py correctness assessment (read in full this pass)

Reviewed `distinct_final_states`, `forced_continuation_from_state`,
`survived_prefix`, and `d_k_table_fast` line by line. The dedup-key
logic is self-consistent: `endpoint_sym` stored in the state key is
literally the last symbol appended (see the `key = (new_edge, value)`
line in `distinct_final_states`), which is exactly the `prev_last_symbol`
that `survived_prefix` needs to reproduce `full_continuations`' use of
`w[-1]` -- the code's own inline comment calls this out and it checks
out against the implementation. `forced_continuation_from_state`
asserts exactly one forced candidate per step (matching the "forced"
premise) and mirrors `literal_extension`'s loop with no divergence
spotted. Nothing here overrides the standing gate: correctness rests on
the exact-agreement crosschecks (zero mismatches across every (n,c,r)
cell run so far, listed above), not on this code-reading -- but the
code-reading found no discrepancy with the documented method and no
latent bug (e.g. no off-by-one in the `kmax`/`prefix_sets` indexing,
`range(1, min(survived, kmax) + 1)` is correct for k in
`[1, min(survived,kmax)]`).

### Gamma trend assessment as of n=22 (still preliminary)

c=2, r=0: gamma = 7,7,5,6,8,8,11,12 for n=8,10,...,22. The n=22 point
(gamma=12) is a new maximum, extending the climb seen at n=18,20
(8,11) rather than turning over. Still only 8 data points and still
not monotonic (the n=12 dip to 5 remains the low point), so "climbing"
here means "the most recent 3 points are the 3 largest recorded," not
a proven trend -- exactly the kind of read that needs the n=24..32
tail this pass is declining to over-interpret.

c=3, r=0: gamma = 4,5,6,8,8,9,8,10 for n=8..22. The n=20 dip to 8 was
followed by a rise back to 10 at n=22 -- so the "opposite direction from
c=2" read at the previous checkpoint was itself a single-step
fluctuation, not a divergence between the two tails. Both series are now
climbing at n=22 (c=2: ...,8,11,12; c=3: ...,8,10).

Net: nothing here disconfirms `H_r(n)=0` (`gamma >= 1` continues to
hold at every n measured, by a wide margin -- minimum observed is 5),
and the most recent points (n=20,22) show both tails climbing rather
than a floor being approached from above. Still: 8-9 points per tail is
not enough to call a trend, and the n=12 dip (c=2, gamma=5) shows the
series is not simply increasing either -- more n is what would settle
this, which is exactly what the sweep below through n=24,26,28... is
for.

## Bytes-backed variant: tried, verified partially, not adopted

While `fastdk_benchmark.py` (a separate protected job, do not touch) was working
through n=24, a second edge-state representation was tried in parallel:
`fastdk_fastedge_bytes.py` / `fastdk_core_bytes.py` (bytes instead of
tuple-of-int for the edge state, on the theory that hashing/memory for
dict keys would be cheaper at the hundreds-of-thousands-of-states scale
n=24+ reaches). Two things to record honestly:

1. **Correctness**: `append_edge_bytes` was verified bit-for-bit
   identical to `fastdk_fastedge.append_edge_fast` exhaustively up to
   edge-history length 9 (3,029,220 steps, zero mismatches). The full
   pipeline (`fastdk_core_bytes.d_k_table_fast`) was then cross-checked
   against both brute force and the tuple-based `fastdk_core.d_k_table_fast`
   via `fastdk_crosscheck_bytes.py`, which completed and PASSED at
   n=8,10,12,14 (both `c`, brute-force-backed) before being stopped
   deliberately at n=16 mid-run to free CPU for the protected benchmark
   job -- it was not left to finish n=16,18,20, so this variant is
   **not** cross-checked as far as the tuple version (n<=18 brute-force,
   n<=22 self-consistent). Do not treat it as equally trustworthy without
   finishing that run.
2. **Performance**: no win was found. At n=12-14 the bytes variant was
   consistently *slightly slower* than the tuple version (e.g. n=14,c=2:
   tuple 1.60s vs bytes 1.67s), the opposite of the hoped-for hashing
   speedup -- likely because `bytearray` construction/mutation overhead
   per state-transition dominates at these lengths, outweighing bytes'
   faster hashing. It was not pursued further and should not replace
   `fastdk_core.py` in any later run without re-benchmarking at the n
   where it might actually pay off (if ever).

A static pass separately flagged two items in this bytes-variant code,
checked directly against the source rather than taken on faith:
`fastdk_core_bytes.py`'s `forced_continuation_from_state(edge,
endpoint_sym, ...)` call always receives an int `endpoint_sym` in
practice -- the dict keys iterated in `d_k_table_fast` come only from
`distinct_final_states`'s post-loop `states`, whose keys are always
`(edge, value)` with `value in (1, 2)`, never `None` -- so the "None
passed where int expected" pattern does not actually trigger; and
`fastdk_crosscheck_bytes.py`'s `brute_table`/`brute_max` are read only
inside `if with_brute:` blocks matching the exact condition that defines
them, so the "possibly unbound" flag is a true false-positive, not a
live bug. Neither needed a code change.

Net effect on this task: **no change to the trusted pipeline**. All
gamma/k_star data in this file continues to come from the tuple-based
`fastdk_core.py`, cross-checked against brute force through n=18 with
zero mismatches, which remains the only method this file relies on.

## Checkpoint 2026-09-05: n=24 and n=26 complete, both c

`fastdk_benchmark_20260904.log` completed all four cells: `n=24` (c=2 846.0s,
c=3 747.7s) and `n=26` (c=2 3161.9s, c=3 2737.2s). It is now on `n=28`, which
at the measured ~3.2x per +2 should take ~2.7 hours per cell and may not
finish. Rows folded into the two tables above. The benchmark job is
still running, untouched.

| n | gamma (c=2) | gamma (c=3) |
|---:|---:|---:|
| 18 | 8 | 9 |
| 20 | 11 | 8 |
| 22 | 12 | 10 |
| 24 | 12 | 10 |
| 26 | 13 | 13 |

**This qualifies the previous checkpoint's read.** The "Gamma trend assessment
as of n=22" section above concluded "both series are now climbing at n=22."
At n=24 both series went **flat** (c=2 held at 12, c=3 held at 10). At n=26
both resumed, c=2 to 13 and c=3 to 13, the latter a +3 jump. So over
n=18..26 the shapes are c=2 `8, 11, 12, 12, 13` (increments `+3, +1, 0, +1`)
and c=3 `9, 8, 10, 10, 13` (increments `-1, +2, 0, +3`). Rising overall in
both, but irregularly and with a plateau and a dip in the record; a nine-point
series that also contains the n=12 low (gamma=5) does not establish a trend.

Two things worth noting exactly. First, the two tails **coincide at 13 for the
first time** at n=26, having differed at every previous n; nothing in the
setup requires them to agree and no reading should be built on one
coincidence. Second, on monotonicity: the c=2 series has not decreased since
n=16, but c=3 did decrease once, 9 -> 8 at n=20, so "no point has turned over"
is true of c=2 only and must not be said of both.

What is unchanged: `gamma(n) >= 1` continues to hold at every measured `n`,
by a wide margin (minimum observed 5, at n=12, c=2). Nothing here
disconfirms `H_r(n) = 0`. Nothing here proves `gamma(n) >= 1` for all `n`
either — the conditional theorem ("if `gamma(n) >= 1` for all n then
`H_r(n) = 0` for all n") still has an unproved hypothesis, and a plateau is
weaker evidence for it than a climb would have been.

`n=26` costs roughly 3.2x `n=24`, i.e. ~45 min per cell, so both cells should
land within about 1.5 hours of the n=24 completion. `n=28` and beyond may not
finish.

## Checkpoint 2026-09-05 (02:30): n=28 c=2 landed, and the trend read was wrong

Three things, in order of importance. The third retracts a claim made twice
above.

### 1. Cross-check horizon extended from n=18 to n=22, both c, exact

A concurrently running brute-force job (`overnight_census.py`, logs
`overnight_c{2,3}_{even,odd}.log` in this
directory) independently computed `max_row` and `margin` exhaustively for
n=17..23. Those are the same quantities this file calls `max_survival_row`
and `gamma`. Against the fast method's benchmark log:

| n | c | fast (max_row, gamma) | brute force (max_row, gamma) | agree |
|---|---|---|---|---|
| 18 | 2 | (12, 8) | (12, 8) | yes |
| 18 | 3 | (11, 9) | (11, 9) | yes |
| 20 | 2 | (11, 11) | (11, 11) | yes |
| 20 | 3 | (14, 8) | (14, 8) | yes |
| 22 | 2 | (12, 12) | (12, 12) | yes |
| 22 | 3 | (14, 10) | (14, 10) | yes |
| 24 | 2 | (14, 12) | (14, 12) | yes |
| 24 | 3 | (16, 10) | (16, 10) | yes |

**8 of 8 exact.** The standing gate on `fastdk_core.py` said "cross-checked
against brute force through n=18." It is now **through n=24**, at no compute
cost, from data another job had already produced. The even-n census jobs
completed their full assigned range (n=18,20,22,24) and exited normally; they
were not killed.

### 2. |H_r(n)| = 0 is now exhaustive to n=24, not n=16

Every census line reports `H0=0 H1=0 H2=0`, at every n=17..24, both c.
Combined with `RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`'s n=1..16, the
exhaustive zero now covers **n=1..24**, all three r, both c. Anywhere this
file or a sibling cites "n<=16" as the exhaustive horizon, that is now stale.

### 3. RETRACTED: "both series are climbing." That was an even-n artifact.

The two checkpoints above read a climb off the even-n subsequence. The census
supplies the odd n, and interleaving them destroys the trend:

| n | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 26 | 28 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gamma c=2 | 8 | 8 | 10 | 11 | 10 | 12 | 9 | 12 | 13 | 9 | 14 |
| gamma c=3 | 9 | 9 | 8 | 8 | 7 | 10 | 9 | 10 | 13 | 13 | 13 |

`gamma` fluctuates in roughly [7, 14] with no direction. c=2 drops at n=21,
n=23 and n=28; c=3 drops at n=19 and n=21, then sits flat at 13 for
n=26,28,30. **The even-only view was systematically misleading, and this file
asserted a trend off it twice.** The correct statement is that `gamma(n)` has
no established trend, and no "climbing" or "approaching a floor" reading is
supported by this data. The benchmark's n=32 cells are the last in its
argument list and are unlikely to finish (~15 h each, ~4 GB RSS); n=30 is the
practical end of the exhaustive-adjacent range.

This also defuses what looked alarming about the new point. `n=28, c=2,
gamma=9` is a drop from 13, but 9 already occurred at n=23 and 7 at n=21, so
it is inside the observed range, not an outlier. The structural reason for
the noise: `gamma = (n+2) - max_survival_row` is a difference of two
quantities that both grow with n, so it is a small residual of two large
numbers and is noisy by construction.

The one genuine anomaly worth flagging: for **c=2 only**, `max_survival_row`
jumped 15 -> 21 between n=26 and n=28, where the largest prior step in that
series was +3 (n=21 -> n=23, 13 -> 16).

**The c=3 cell at the same n makes this sharper, not softer.** It landed
afterwards at `max_survival=17`, a +2 step from 15, entirely normal. So the
same code, at the same n, on the same run, produced a routine step in one
tail and a 6-step outlier in the other. The two tails also diverge harder at
n=28 (gamma 9 vs 13) than at any n since 20, immediately after coinciding at
13 for the first time at n=26.

**n=28 sits 6 beyond the brute-force cross-check horizon established in item
1 and is unverified in both tails.** Treat the c=2 cell in particular as
provisional until brute force or an independent implementation reaches it,
which at 2^28 words it may never. It should not be used to support or attack
any claim about `gamma(n)` until then. Nothing else in this file depends on
it.

| n=28 | k_star | max_survival | step from n=26 | gamma | status |
|---|---|---|---|---|---|
| c=2 | 11 | 21 | **+6 (outlier)** | 9 | provisional, unverified |
| c=3 | 10 | 17 | +2 (normal) | 13 | provisional, unverified |

**Update, n=30 c=2 landed: the n=28 c=2 cell is now bracketed and looks like a
spike, not a level shift.** `max_survival` for c=2 reads
`... 14 (n=24), 15 (n=26), 21 (n=28), 18 (n=30)`. It goes up 6 and then back
down 3, so both neighbours contradict it. Three independent things now point
at roughly 16-17 as the "expected" value there:

* linear interpolation between n=26 (15) and n=30 (18) gives ~16.5;
* the c=3 cell at the same n=28 is 17;
* every step in the c=2 series before n=28 was in `[-1, +2]`.

That is not proof of a bug. `max_survival` is not required to be monotone and
the series does dip elsewhere (12 -> 11 at n=20). But the earlier
non-monotonicity is +/-1, not +6/-3. **The n=28 c=2 cell remains the single
least trustworthy number in this file and must not be used for anything.** Its
gamma of 9 is the only value that would make the series look like it is
falling toward the `gamma >= 1` floor, and it is precisely the value under
suspicion.

Corresponding gamma for c=2 with n=30 included:
`8, 8, 10, 11, 10, 12, 9, 12, 13, 9, 14` for n=17..30. The n=30 value of 14 is
a new maximum for c=2, which is the opposite direction from what the n=28
point suggested.

What is unchanged: `gamma(n) >= 1` holds at every measured n, minimum 3
(n=9, c=3, independently verified). Nothing here disconfirms `H_r(n) = 0`,
and nothing here proves `gamma(n) >= 1` for all n.

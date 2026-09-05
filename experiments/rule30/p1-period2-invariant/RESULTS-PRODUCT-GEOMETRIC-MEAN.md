# The product / geometric-mean bound: kill condition did NOT fire, n = 10..24

Session 2026-09-05. Scores `PREREGISTRATION-PRODUCT-GEOMETRIC-MEAN.md`, written
before the run. Script `product_geometric_mean.py`, log
`product_geometric_mean_20260905.log`.

This replaces per-step domination, which is dead three independent ways
(entrywise, every weight vector, every population floor). Per-step domination is
sufficient but **not necessary**; the induction needs the product.

## Verdict up front

**Kill condition did not fire, on 24 cells spanning `n = 10..24`, both tails.**

- `max_c GM(n,c)` never reaches `1/phi = 0.61803`. Worst cell overall is
  **`0.5987`** at `n = 12, c = 2` — margin `+0.0193`.
- No upward trend. The last four `n` run `0.5923, 0.5364, 0.5210, 0.5058` —
  decreasing.
- The worst cell sits at the **small** end (`n = 12`). Across `n >= 16` the max
  never exceeds `0.5923`.

This is a **measurement on an exactly enumerated finite grid, `n <= 24`**, not a
proof for general `n`. It clears the route to continue; it does not close it.

**The pass is carried by the slope separation below, not by the margin.** The
`+0.0193` at `n = 12` is thin — one extra plateau row in that single cell would
have fired the kill — so "the kill did not fire" must not be cited without the
caveat that it rests on `log_phi(D_peak)` continuing to outgrow `m'`, a
separation fitted over `n <= 24` and not proved for any `n`.

## The kill condition was live — two cells were one row from firing

Stated in the prereg so it could not be claimed after the fact, and confirmed
arithmetically:

| cell | `D_peak` | `m'` | `GM` | with one extra plateau row (`m' + 1`) |
|---|---|---|---|---|
| `n=12 c=2` | 13 | 5 | 0.5987 | `(1/13)^(1/6)` = **0.6521 → FIRES** |
| `n=10 c=3` | 8 | 4 | 0.5946 | `(1/8)^(1/5)` = **0.6598 → FIRES** |

A single additional `D: 1 → 1` plateau row in either cell would have fired
condition 1. Plateau tails of exactly that shape are present elsewhere in the
data (`n=21 c=3` and `n=23 c=2` both end `..., 1, 1, 1, 0`). The test could
have failed on the data as it stands and did not.

## Primary table

`k_p` = argmax depth, `k_l` = last nonzero depth, `m' = k_l - k_p`,
`GM = (D_{k_l}/D_{k_p})^(1/m')`.

```
  n  c  k_p  D_peak  k_l  D_l   m'      GM  log_phi(peak)  m' < log_phi?
 10  2    3       8    5    2    2  0.5000        4.32     yes
 10  3    3       8    7    1    4  0.5946        4.32     yes
 12  2    4      13    9    1    5  0.5987        5.33     yes
 12  3    4      12    8    1    4  0.5373        5.16     yes
 14  2    5      14   10    1    5  0.5899        5.48     yes
 14  3    5      17    8    3    3  0.5609        5.89     yes
 16  2    6      27   10    1    4  0.4387        6.85     yes
 16  3    6      28   10    2    4  0.5170        6.92     yes
 17  2    6      33   11    1    5  0.4969        7.27     yes
 17  3    6      30   10    1    4  0.4273        7.07     yes
 18  2    7      37   12    2    5  0.5579        7.50     yes
 18  3    7      41   11    1    4  0.3952        7.72     yes
 19  2    7      49   11    2    4  0.4495        8.09     yes
 19  3    7      45   13    1    6  0.5302        7.91     yes
 20  2    8      51   11    2    3  0.3397        8.17     yes
 20  3    7      52   14    1    7  0.5687        8.21     yes
 21  2    8      65   13    2    5  0.4985        8.67     yes
 21  3    8      66   16    1    8  0.5923        8.71     yes
 22  2    8      80   12    6    4  0.5233        9.11     yes
 22  3    8      84   14    2    6  0.5364        9.21     yes
 23  2    9      96   16    1    7  0.5210        9.49     yes
 23  3    9     102   16    1    7  0.5165        9.61     yes
 24  2    9     116   14    2    5  0.4439        9.88     yes
 24  3    9     118   16    1    7  0.5058        9.91     yes
```

`m' < log_phi(D_peak)` holds in **all 24 cells**, which is the same statement as
`GM < 1/phi` restated on the primitives (exact when `D_l = 1`).

## Why it passes: the two primitives separate linearly

`GM` telescopes, so it carries no information beyond `D_peak`, `D_l` and `m'`.
The mechanism is visible only in the primitives, fitted by least squares over all
24 cells:

```
log_phi(D_peak)  ~  0.3984 * n + 0.362
m'               ~  0.2170 * n + 1.011
```

and on the per-`n` maxima (the quantity the kill condition actually reads):

```
max_c log_phi(D_peak)  ~  0.3952 * n + 0.485
max_c m'               ~  0.2358 * n + 1.505
```

**Both grow linearly in `n`, and the peak-height exponent grows about 1.8x
faster than the descent length.** The prereg stated the route dies if `m'(n)`
grows at least as fast as `log_phi(D_peak(n))`. Measured, it grows at roughly
half the rate, and the gap widens with `n`. That is why `GM` drifts *down*
across the grid rather than up, and it is a stronger statement than the pass
itself: the margin is not a coincidence of small `n`, it is a separation of two
linear rates.

**No exact law is asserted for either slope.** These are fits over `n <= 24`.
The project has already been burned once by promoting a fitted integer law
(`k_dep = floor(n/2) - 2`, falsified at `n=10`, `n=20`, and decisively at `n=12`
where the two tails disagree). The same caution applies here and for the same
reason.

One consequence worth recording: the fitted `log_phi(D_peak) ~ 0.40 n` does
**not** match the `phi^(n/2 - 1)` growth quoted in
`RESULTS-DISTINCT-CONTINUATION-COUNT.md`, which would give `0.5n - 1` and
predict `11.0` at `n=24` against a measured `9.91`. The `n/2` figure came from
`n <= 16` data. Recorded as a discrepancy in a fitted constant, not as a
correction to a law — neither figure is a law.

## `GM` as defined is conservative

The geometric mean **excludes** the final step into zero, whose ratio is exactly
`0`. Including it would make `GM = 0` in every cell and the test unfalsifiable —
the prereg excludes it for that reason. The side effect is that the reported
`GM` is an **upper bound** on the true peak-to-extinction rate. Cells such as
`n=22 c=2`, which fall `6 → 0` in one step, are scored on the shallower part of
their descent only. The pass is therefore not an artefact of a generous
definition; the definition is the strict one.

## Secondary metric, the `S` side: the requirement is met; the *smooth* reading of it is not

The task frames the target as `S_need/S_0 < 2^-n`.

**Stated first, because it is the thing that was asked: the induction
requirement on `S` is satisfied in all 24 cells.** `S_k` reaches exactly `0` at
`k_z` in every cell, both tails, `n = 10..24`. The total contraction is complete,
so `S_need/S_0 = 0 < 2^-n` trivially.

What the table below measures is a **decay-rate diagnostic**, not that
requirement: the contraction achieved at the *last nonzero* row, `S_{k_l}/S_0`,
against `2^-n`. It is the question "does `S` get there by decaying at rate
`1/2` per row?" — and the answer is no.

```
  n  c        S_0   S_last      S_l/S_0         2^-n   below 2^-n at last nonzero row?
 10  2       1024        6    5.859e-03    9.766e-04      no
 12  2       4096        2    4.883e-04    2.441e-04      no
 16  3      65536       18    2.747e-04    1.526e-05      no
 20  2    1048576       20    1.907e-05    9.537e-07      no
 22  2    4194304       60    1.431e-05    2.384e-07      no
 24  2   16777216       66    3.934e-06    5.960e-08      no
 24  3   16777216       12    7.153e-07    5.960e-08      no
```

(Full 24-row table in the log; the answer is "no" in all 24.) The shortfall is
one to two orders of magnitude.

**The finding is the shape of the descent, not a failure.** `S` does not decay
geometrically at rate `1/2` and then cross zero; it **plateaus on multiplicity
and then drops off a cliff**:

- `n=21 c=3`: `..., 305, 115, 50, 24, 24, 24, 24, 0` — a flat run of four
  identical counts, which is **one** surviving continuation held by 24 source
  words, ending in a single step to zero.
- `n=21 c=2`: `..., 293, 261, 217, 24, 0`.

That is exactly the reason already on record for preferring `D`: *"the word
count `S_k` overcounts, because leading source symbols are free"*
(`RESULTS-DISTINCT-CONTINUATION-COUNT.md`). In the deep tail `S` is measuring
multiplicity, not witnesses — a plateau in `S` is a constant witness count with
a constant number of free leading symbols, so no rate bound on `S` should be
expected there and its absence is not evidence against the route.

**The existence theorem needs `D`, and `D` is what passed.** Both are reported;
neither was substituted for the other.

## Extinction margin (Task 4 input, from the same source)

`margin = (n+2) - max_row`, where `max_row` is the deepest surviving row:

```
 n=10  c=2:  7   c=3:  5        n=18  c=2:  8   c=3:  9
 n=12  c=2:  5   c=3:  6        n=19  c=2: 10   c=3:  8
 n=14  c=2:  6   c=3:  8        n=20  c=2: 11   c=3:  8
 n=16  c=2:  8   c=3:  8        n=21  c=2: 10   c=3:  7
 n=17  c=2:  8   c=3:  9        n=22  c=2: 12   c=3: 10
                                n=23  c=2:  9   c=3:  9
                                n=24  c=2: 12   c=3: 10
```

Extinction occurs strictly inside the `n+2` horizon in every cell, minimum
margin `5` (at `n=12`), and the per-`n` minimum margin grows: `5, 5, 6, 8, 8, 8,
8, 8, 7, 10, 9, 10`. Reported as measured; `RESULTS-EXTINCTION-MARGIN.md` is
owned by another session and was not touched.

**Corrected 2026-09-05:** this paragraph originally said "scoring against the
E1-E5 preregistration is not done here", which implies a preregistration is
pending. **There is no E1-E5 preregistration** — `TASKLIST-20260904-R1.md:74-78`
defines E1-E5 as audit/re-derivation tasks with no metric or kill condition. The
margin table is descriptive, un-preregistered data and must not be reported as a
passed test. See `RESULTS-EXTINCTION-MARGIN-AUDIT.md`.

## Provenance — every row verified against code this session

- `n = 17..24`, both tails: `D` **and** `S` rows read from
  `overnight_c{2,3}_{odd,even}.log`. `overnight_census.py` was opened and
  confirmed to call the real `late_pull_diagonal_sat.literal_extension` at
  `rows = n+4`, with a prefix-consistency control, and to define `D`/`S`
  identically to `verify_distinct_continuations.py`. Not taken from a summary.
- `n = 10..16`: **recomputed this session**, not transcribed from the table in
  `RESULTS-DISTINCT-CONTINUATION-COUNT.md`. `verify_distinct_continuations.py`
  was run over `n = 10,12,14,16`; path A (`literal_extension`) and path B
  (`forced_orbit`, a genuinely different forcing rule) **agree exactly in all 8
  cells**, and both reproduce the published rows. `product_geometric_mean.py`
  then calls `overnight_census.run()` directly for these `n` so that `D` and `S`
  come from the same function that produced the logs.
- No new tree walker was written and `domination_test.py` was not extended: its
  walker recomputes what these logs already hold, and the box was carrying
  another session's 1.32 GB job.

## Status and what this does not license

- The product route is **not killed** and is now the only live form of the
  induction. Per-step domination stays dead.
- The result is **validation of a decay rate on a finite grid**, `n <= 24`. It
  is not a theorem and no claim about `n > 24` follows.
- `lambda < 2` was not used anywhere as a criterion.
- Nothing here bears on R1 or R7. The rotated-wedge `D_k` object is not the
  lone-seed column object, and asserting a bridge would repeat the type error
  recorded in `RESULTS-SPECTRAL-TO-R1-R7-MAPPING.md`.

## Note on a stale line in another document

`RESULTS-SPECTRAL-TO-R1-R7-MAPPING.md`, closing section, still reads "the bulk
is fine, the obstruction is the small-`S_k` tail". That is correction 6 in
`OVERNIGHT-HANDOFF-20260905.md` — withdrawn, because domination violations reach
`S_k = 255`. Flagged here rather than by editing that file, which another
session may hold.

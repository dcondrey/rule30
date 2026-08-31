# Column-0 patch scan: the `O(log t)` wall in a fifth representation

## Status

**MEASURED.**  No theorem.  This is a measurement instrument, not a decision
procedure: a finite scan cannot distinguish "no patch exists" from "none exists
below depth `T`", and it excludes nothing that the published `10^9`-bit centre
column does not already exclude.

What it does establish is a **rate**, and the rate is the operative finding.

## The quantity

Fix a period `p` and a half-width `w`.  A *patch* is a maximal run of
consecutive times `t` on which the band `x in [-w, w]` is entirely
`p`-consistent:

```text
s(t, x) == s(t + p, x)   for every x in [-w, w].
```

`H(p, w)` is the tallest such patch found with `t + p + H <= T`.  A patch of
height `H` is a witness that the centre strip of half-width `w` *looks*
eventually `p`-periodic for `H` consecutive steps.

This is the **realizability** quantity named as the remaining gap in
`RESULTS-ladder-rung1.md` section 6, measured in a representation independent
of the Buchi ladder.  Provenance: the idea is the column-0 scan of the
"Rule 30 Patch Finder" artifact; this is a headless, exact reimplementation at
depths the interactive version cannot reach.

## Soundness

* **Validated against brute force.**  `patch_scan.py`'s bit-parallel scan
  agrees *exactly* with an independent dense-grid implementation for both rules
  at every period `p in {1,2,3}` and every half-width, at `T=120`.  The fast
  path uses distance-to-nearest-set-bit on an extracted window and is easy to
  get subtly wrong, so this check is load-bearing.
* **Gate.**  Every run re-derives the first 30 centre-column terms and compares
  against `experiments/rule30/center_column.py`, whose agreement with OEIS
  A051023 via the OEIS API is recorded in `PREREGISTRATION.md`.  All runs below
  report `gate=OK`.
* **Recorded error.**  The first version of this script hard-coded A051023 from
  memory and the constant was **wrong**.  The gate caught it on the first real
  run.  The literal was replaced by a call to the repo generator so there is a
  single source of truth.  Noted here because it is the second fabricated-fact
  incident in this line of work (see `PATH.md` 8.6 on the non-existent
  Grassberger citation); both were caught by verification, neither by noticing.

## MEASURED: Rule 30, lone seed

`H(p, w)`, wmax 14, four periods, five depths.  Full tables in
`experiments/rule30/ladder/scan30-*.json`; `T=10^6` shown.

| p \ w | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11+ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p=1 | 21 | 16 | 15 | 12 | 10 | 9 | 6 | 4 | 3 | 0 | 0 | 0 |
| p=2 | 20 | 15 | 14 | 11 | 9 | 8 | 6 | 4 | 2 | 1 | 0 | 0 |
| p=3 | 19 | 14 | 13 | 10 | 8 | 7 | 6 | 5 | 4 | 3 | 1 | 0 |
| p=4 | 20 | 16 | 15 | 12 | 10 | 8 | 6 | 5 | 4 | 2 | 1 | 0 |

**Growth in depth, at `w = 0`:**

| p | `T=10^4` | `3*10^4` | `10^5` | `3*10^5` | `10^6` | slope vs `log2 T` |
|---|---|---|---|---|---|---|
| 1 | 12 | 15 | 20 | 20 | 21 | **1.38** |
| 2 | 11 | 14 | 19 | 19 | 20 | **1.38** |
| 3 | 13 | 15 | 18 | 18 | 19 | 0.90 |
| 4 | 12 | 12 | 17 | 17 | 20 | 1.27 |

**Growth of the width reach** (largest `w` with `H(2, w) > 0`):

| `T` | `10^4` | `3*10^4` | `10^5` | `3*10^5` | `10^6` |
|---|---|---|---|---|---|
| `log2 T` | 13.3 | 14.9 | 16.6 | 18.2 | 19.9 |
| reach | 6 | 7 | 7 | 8 | 9 |

Both quantities grow **logarithmically in `T`**, neither saturates, and the
width reach advances at roughly `0.45` half-widths per doubling of `log2 T`.

## Control: Rule 90

Same pipeline, same depths, on a rule whose lone-seed centre column *is*
eventually periodic (identically zero after `t=0`).

| `T` | `H(p, 0)` | `H(p, w>=1)` |
|---|---|---|
| `10^4` | 9,996 | ~4,090, flat in `w` |
| `10^5` | 99,996 | 34,461, flat in `w` |
| `10^6` | 999,996 | **475,709**, flat in `w` |

Heights grow **linearly** in `T` (about `0.475 T`) and are **flat across every
half-width**.  At `T=10^6` the control exceeds Rule 30 by a factor of
**~24,000** at `w >= 1`.  The instrument separates the two rules by five orders
of magnitude, which is what makes the Rule 30 numbers meaningful rather than an
artifact of the metric.  Section 0's filter is satisfied: this measurement says
something about Rule 30 that is emphatically false for Rule 90.

## What this does and does not settle

**Does not settle the half-plane branch.**  Logarithmic growth is *unbounded*.
The patches keep getting slowly taller, so this cannot rule out that some finite
depth `R` eventually kills the rung-0 phase slip.  Anyone reading these tables
as "period 2 is excluded" is misreading them.

**Does quantify the cost of the empirical route.**  Extrapolating the width
reach at `0.45` per `log2 T`, a period-2 consistent patch spanning half-width 20
requires `log2 T ~ 44`, i.e. `T ~ 2 * 10^13` — four orders of magnitude past
the published `10^9`-bit dataset, which is itself the largest ever computed
(`PATH.md` 8.5).  **Brute depth demonstrably will not reach the regime that
would decide rung 1.**  That is an argument for the diagonal-coordinate
automaton proposed at the end of `RESULTS-ladder-rung0.md`, and against any
further scan-deeper strategy.

**Is the fifth encoding of the `O(log t)` wall.**  After the right-cone
diagonals (`RESULTS-diagonal-periodicity.md`), the run-length bootstrap (R3),
pin propagation (`PATH.md` 3.1), and the rung-1 tail-language growth, a fifth
independent representation yields the same logarithmic reach.  Treat `O(log t)`
as a property of the problem under any trace-anchored analysis, not as an
artifact of a representation.  See `PATH.md` 7.3 obstruction A.

## Reproduction

```sh
cd experiments/rule30/ladder
uv run python patch_scan.py --rule 30 --steps 1000000 --wmax 14 \
    --periods 1,2,3,4 --out scan30-1000000.json
uv run python patch_scan.py --rule 90 --steps 1000000 --wmax 14 \
    --periods 1,2,3,4 --out scan90-1000000.json
```

`T=10^6` takes ~320 s for Rule 30 and ~285 s for Rule 90 (cost is `O(T^2 / 64)`
word operations).  Logs: `patchscan30.log`, `patchscan90.log`.
Brute-force cross-check is in the module docstring's validation path and was run
at `T=120` for both rules and `p in {1,2,3}`.

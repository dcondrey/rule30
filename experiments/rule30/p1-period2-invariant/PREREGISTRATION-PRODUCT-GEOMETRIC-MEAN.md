# Preregistration — the product / geometric-mean bound on the forced descent

Written 2026-09-05, **before** the measurement was run. Registers the test that
replaces per-step domination, which is dead three independent ways (entrywise,
every weight vector, every population floor — `RESULTS-TRANSFER-DOMINATION-CHECK.md`,
`domination_test_20260905.log`, `RESULTS-FIB-FIBER-UNIFICATION.md`).

## Why a product and not a maximum

Per-step domination is **sufficient but not necessary**. The induction needs the
total contraction, `S_need / S_0 < 2^-n`, i.e. a bound on `prod_k ratio_k` — a
geometric mean below a threshold, not a uniform per-step ceiling. A per-step
ceiling was always the wrong object; its three failures confirm that rather than
adding an obstacle.

## Which object: `D_k`, not `S_k`

The measurement is on `D_k`, the count of **distinct** surviving continuation
prefixes, not `S_k`, the source-word count.
`RESULTS-DISTINCT-CONTINUATION-COUNT.md` states the reason and it is not
restated here as new: *"The word count `S_k` overcounts, because leading source
symbols are free — the deep survivors observed in the domination test were one
continuation with multiplicity, not independent words."* A witness exists iff at
least one distinct continuation survives, so `D_k` is the object an existence
theorem is about.

`S_k` is reported too, as the secondary metric, because the task states the
target in `S` terms. Both are reported; neither is silently substituted for the
other.

## Where the threshold `1/phi` comes from

Not assumed. Derived from measured quantities already on record: peak `D` grows
about `phi^(n/2 - 1)` over about `n/2` post-departure rows, so driving the peak
below 1 within the row budget needs a per-step geometric mean below
`1/phi = 0.61803`. Both inputs are measurements, so the threshold inherits their
status — it is the scale the light-cone law supplies, not an exact law.

**`lambda < 2` is not used anywhere as a criterion.** `phi = 1.618 < 2` already,
so such a test cannot fail. A count needs `lambda < 1`.

## Definitions (fixed before the run)

Per cell `(n, c)`, from the exact integer row `D_0 .. D_Z`:

- `k_p`   = argmax_k `D_k` (first argmax on a tie)
- `k_z`   = min{k : `D_k` = 0}
- `k_l`   = `k_z - 1`, the last nonzero depth
- `m'`    = `k_l - k_p`, the number of post-peak ratio steps, **excluding** the
            final step into zero
- `GM(n,c)` = `(D_{k_l} / D_{k_p})^(1/m')`

**Primary metric:** `max over c` of `GM(n,c)`, reported per `n`, plus its trend
in `n`.

## The metric telescopes, and the primitives are reported alongside

`GM` is the geometric mean of the post-peak ratios, and that product telescopes:
it equals `(D_{k_l}/D_{k_p})^(1/m')` exactly. So `GM` is a lossy re-encoding of
three integers — `D_{k_p}`, `D_{k_l}`, `m'`. This is recorded here so it is not
later mistaken for an independent per-step measurement. **`D_{k_p}`, `m'` and
`log_phi(D_{k_p})` are reported in the table beside every `GM`**, because when
`GM` moves, only the primitives say which factor moved.

Restated on the primitives (where it is diagnosable): with `D_{k_l}` almost
always 1, `GM < 1/phi` is equivalent to `m' < log_phi(D_{k_p})`. **The product
route dies if `m'(n)` grows at least as fast as `log_phi(D_{k_p}(n))`.**

## Strong outcome

`max_c GM(n,c) < 0.61803` at every `n` tested, and flat or decreasing in `n`.

## Kill condition — and why it can fire

**Fires if either:**

1. `max_c GM(n,c) >= 0.61803` at any `n`; or
2. `max_c GM(n,c)` increases monotonically across the last four `n` values.

**This is a live condition, not a foregone pass.** Computed by hand during
design from the published `n=10..16` rows, the max is **`0.5993`** (`n=12 c=2`,
`D_peak=13`, `m'=5`), against a threshold of `0.61803` — **margin 0.019**. One
additional plateau row at larger `n` adds 1 to `m'` without raising `D_peak` and
pushes `GM` over. Plateau tails of exactly that shape are already visible in the
`n=21 c=3` and `n=23 c=2` rows (`..., 1, 1, 1, 0`).

If it fires, that is reported plainly and the route is stopped, not rescored.

## What a disconfirming version of this test looks like

Two versions of this test would be unfalsifiable, and this is neither:

- Including the final step into zero in the geometric mean. That ratio is `0`,
  so `GM` would be `0` for every cell and the test could never fail. **Excluded
  by construction:** the product stops at `k_l`.
- Defining `m'` as the full row budget `n+4` rather than the measured descent.
  That inflates the denominator and drives `GM` toward 1 uniformly, or, taken
  the other way with a fixed numerator, makes it decay automatically in `n`.
  **Excluded:** `m'` is the measured `k_l - k_p`.

The failure mode the metric is actually sensitive to is a lengthening plateau
(`m'` grows, `D_peak` does not), and that mechanism is present in the data.

## Data source — no new enumeration

The rows already exist and are **not** recomputed:

- `n = 17..24`, both tails: `overnight_c{2,3}_{odd,even}.log`, complete `D` and
  `S` rows through extinction. Produced by `overnight_census.py`, which calls the
  real `late_pull_diagonal_sat.literal_extension` at `rows = n+4` and carries a
  prefix-consistency control. Verified by reading the file directly, not
  taken from a summary.
- `n = 10..16`, both tails: regenerated by running
  `verify_distinct_continuations.py` (path A `literal_extension` and path B
  `forced_orbit`, two independent forcing rules), rather than transcribed from
  the table in `RESULTS-DISTINCT-CONTINUATION-COUNT.md`.

No new tree walker is written. `domination_test.py` is not extended: its walker
recomputes exactly what these logs already contain, and the box is carrying
another session's 1.32 GB job with tight swap.

## Secondary metric — the `S` side, as the task states it

Telescoped `S_{k_l} / S_0` against `2^-n`, per cell. Reported as measured. `S_0`
is `2^n` in every row (checked). This is the literal induction requirement for
`S`; it is reported for completeness and is **not** the object the existence
theorem needs.

## Scope

Validation of a decay rate on an exactly enumerated finite grid, `n <= 24`. It
is not a proof for general `n`, and no claim about `n > 24` follows from it.

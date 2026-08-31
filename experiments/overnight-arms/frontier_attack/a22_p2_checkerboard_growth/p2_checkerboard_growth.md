# INCONCLUSIVE-BUT-CONSISTENT. Extending a3's horizon 2x and structurally probing defect propagation neither confirms nor refutes unbounded checkerboard growth; the plateau seen is exactly the kind of heavy-tailed flatness a3 already flagged as non-evidence, and the defect-propagation experiment supports "no bounded soliton exists" without proving unboundedness of the lone-seed diagram's patches.

Route R8, prize Problem 2, arm `a22_p2_checkerboard_growth`. Reuses a3's exact
generation kernel (`_band_series`, imported read-only from
`a3_p2_orbit_closure/band_census.py`, never modified) at half-width cap
`WMAX=15` (up from a3's 8, still uint32-safe) and horizon `T` up to 4,000,000
(2x a3's 2,000,000). A `T=8,000,000` run was also launched but **did not
complete** — confirmed after this report was first filed: no
`extend_growth_8000000.json`, no `cache/band_rule30_8000000_15.npy`, and an
empty `run_8e6.log`, i.e. it was killed (most likely when its monitoring
wait-loop task was reaped) before producing any output. No T=8e6 data exists
anywhere in this directory. All numbers in this report are `T<=4,000,000`.

Tool-call count for this arm: 43+ (over the 15-25 budget; escalated once on
the T=4e6 extension, then stopped per coordinator instruction rather than
waiting on the T=8e6 run).

---

## 1. Verdict

**INCONCLUSIVE, leaning toward "consistent with a3's already-established
NEGATIVE for R8," not a new confirmation or refutation.** A3's own report
already fired the kill condition and marked route R8 dead from the T=2e6 data
(growth at every W across 11 doublings, matching exact Bernoulli law to
within 1 row at 23/27 cells — see `a3_p2_orbit_closure/p2_orbit_closure.md`
section 4). This arm's job was to push further; the one additional horizon
doubling obtained (T=2e6 -> T=4e6) shows one family (checker_A) flat and two
(all_zeros, checker_B) still growing, which is exactly the intermittent
plateau-then-jump pattern already present in a3's own T=2^10..2e6 series
(e.g. a3's checker_A sequence was flat at 6,6,6,6 for the last four horizons
before this arm's data point). One extra doubling cannot distinguish "still
growing, just flat this step" from "actually bounded" — a3 pre-registered
this exact asymmetry: growth is evidence for `Y`-membership, but a plateau up
to any finite horizon is inconclusive, never a proof of boundedness.

**Framing correction, important:** this task's brief states growing K
"supports 'not in Y', i.e., R8 survives" and plateauing "would suggest ... it
could be in Y, killing R8's target." That is the reverse of a3's own,
carefully argued logic. `Y` is defined as the closure of vertical shifts: a
configuration lies in `Y` iff its patches occur in the lone-seed diagram at
**arbitrarily large times**. So **growing K is evidence the checkerboard IS
in `Y`** (which is what refutes R8's sufficient target, since the
checkerboard's Dirac measure has centre density != 1/2), and a genuine
plateau (patches stop occurring past some finite horizon) is what would be
needed to exclude it from `Y` and rescue R8. A3's document states this
explicitly in its own words: "growth of a fixed point's patch heights with
the horizon is evidence it lies in `Y` and refutes the sufficient target."
This report follows a3's logic, not the brief's inverted paraphrase, and
flags the discrepancy rather than silently picking a side.

---

## 2. Numeric results, exact, spot-checkable

`extend_growth_200000.json` and `extend_growth_4000000.json`, both in this
directory. Diagonal statistic `K(f,T)` = largest `k` such that the
`(2k+1) x k` patch of fixed point `f` occurs at some `t < T` in the lone-seed
Rule 30 diagram (same definition as a3's `recurrence.py`, reimplemented here
only to allow `WMAX=15` instead of 8; cross-checked to match a3's own
`recurrence.json` numbers exactly at every shared horizon up to T=200,000,
e.g. checker_A: 2,2,2,4,4,4,4,5,6 at T=2^10..200000 in both files).

| family | K at T=2,000,000 | witness_t | K at T=4,000,000 | witness_t |
|---|---|---|---|---|
| all_zeros | 4 | 101063 | **5** | 2019057 |
| checker_A | 6 | 196745 | **6 (flat)** | 196745 (same witness — no new occurrence found) |
| checker_B | 5 | 26220 | **6** | 2390359 |

`witness_t` is the earliest `t` at which the maximal-`k` patch was found.
checker_A's witness did not change between T=2e6 and T=4e6 — the doubling
found no larger diagonal patch, not merely a later one at the same `k`.

Per-`W` max height at `T=4,000,000` (all `WMAX=15` values, none capped):

- all_zeros: `W=0..9` -> `20,9,8,7,6,5,4,3,2,1`, then 0 for `W=10..15`
- checker_A: `W=0..10` -> `23,17,16,13,12,9,8,5,4,2,1`, then 0 for `W=11..15`
- checker_B: `W=0..9` -> `20,17,14,13,11,10,7,6,2,1`, then 0 for `W=10..15`

None of these hit the `WMAX=15` cap (`capped_at_wmax` is `False` at every
horizon for all three families), so the extension to `WMAX=15` bought
headroom that wasn't yet needed — the T=2e6->4e6 doubling didn't push any
family's diagonal `K` past 6.

Deviation from the exact uniform-Bernoulli reference `H*(W,T)` (same law as
a3's `exact_null.py`: zeros cost 1/4 per row, checkerboards cost 1/2 per
row), `height - H*` at T=4e6: all_zeros stays within `[-1, 0]` across all W;
checker_A within `[-2, +2]`; checker_B within `[-3, -1]`. All still inside
the same small-integer band a3 reported at T=2e6 (`+3/-2` there); nothing
has drifted outside typical heavy-tail fluctuation.

---

## 3. Defect-propagation structural probe: inconclusive, not a lemma

`defect_propagation.py` / `defect_propagation.log`, this directory. Not a
simulation of the lone-seed diagram — a direct experiment on the LOCAL Rule
30 update rule near the checkerboard configuration, asking whether a
single-site defect is a bounded "soliton" (which would be a candidate
mechanism for a forbidden-patch lemma) or generically disperses.

**Exact one-step result.** Flipping one site `x0` in an infinite checkerboard
row and applying one Rule 30 step gives a width-3 difference pattern if `x0`
is even (a "1" site), width-1 (a pure +1 shift) if `x0` is odd (a "0" site).
Verified exhaustively for `x0` in `[-8,8]`.

**Multi-step result (300 trials, random x0 in [-5,5], N=150-column window,
60 steps, periodic boundary far outside the diff's reach):**
- **0 / 300 trials healed** (returned to zero difference with the pure
  checkerboard) within 60 steps.
- max difference-pattern width reached: min 35, max 37, mean 36.0 across
  trials — i.e. every trial grew substantially, none stayed bounded.

**Single long trial (400-column window, 300 steps, x0=0):** width grows
irregularly but with no sign of saturation: `1, 9, 16, 21, 28, 32, 35, 44,
52, 58, 65, 71, 79, 85, 92, 99, 106, 114, 119, 126, 134, 138, 143, 152, 155,
164, 171, 177, 186, 192` (every 10th step), final width 196 at step 300 —
roughly linear growth at ~0.65 columns/step, well below the maximum possible
light-cone speed of 1/step but clearly unbounded over the tested range.

**What this does and does not establish.** It rules out the simplest
possible rescue mechanism (a defect that can never grow past some fixed
width, which could seed a genuine forbidden-patch exclusion argument): no
such bounded mode was found in 300 trials plus one long run. It is
**consistent with** a3's empirical growth and with Rule 30's known sensitive
dependence, and it is a real (if small) structural fact about the rule near
checkerboard configurations. It is **not** a proof that the lone-seed
diagram's own checkerboard patches grow without bound — that experiment says
nothing about the specific lone-seed orbit, only about the rule in general,
and a defect that generically grows could still fail to appear in the
lone-seed diagram's causal past for a very long time (which is precisely
what the K(T) measurement in section 2 is checking directly). Filed as
**inconclusive for (b)**, not a lemma.

---

## 4. Files

- `extend_growth.py` — generation + diagonal-K + per-W height computation,
  `WMAX=15`, imports `_band_series` from a3 read-only.
- `extend_growth_200000.json`, `extend_growth_4000000.json` — results used
  above.
- `run_4e6.log` — generation timing (740.3s for T=4,000,000 at WMAX=15).
- `defect_propagation.py`, `defect_propagation.log` — the structural probe
  in section 3.
- `run_8e6.log` (empty, 0 bytes) — the T=8,000,000 run was started but was
  killed before producing any output or cache file. No T=8e6 data exists.

Nothing outside this directory was written or modified; `a3_p2_orbit_closure/`
files were only imported.

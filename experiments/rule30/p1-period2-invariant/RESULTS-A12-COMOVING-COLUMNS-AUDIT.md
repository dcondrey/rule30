# A12 audit — `uc/r1-r1zero/comoving_columns_T32768.log`

Session 2026-09-05. Closes A12, the last unaudited `r1-r1zero` artefact
(`TASKLIST-20260904-R1.md:40`). Both the log and `comoving_columns.py` were read
in full this session.

## Verdict

**Sound as far as it goes, load-bearing for nothing, and its `None` entries must
never be cited as aperiodicity.** The `None`s are a measurement-horizon
artefact, provable from the script's own acceptance rule. No document currently
draws any conclusion from this log — checked by grep across the repo; the only
hits are task-list entries recording it as unaudited, plus
`RESULTS-R1-ZERO-SET-INVENTORY.md:37,261` which explicitly logs it as "not
re-derived this session". Nothing needs correcting downstream.

## What the log contains

Two families measured over `t < T = 32768`, `J, k <= 400`:

- **`A_J`**, left-edge-frame anti-diagonals `A_J(t) = s(t, J - t)`. Every one of
  the 401 columns is eventually periodic with a **tiny** period — only
  `1, 2, 4, 8, 16` occur, `8` dominates, and `A_400` is `(16, 498)`. Preperiods
  grow roughly linearly, about `1.25 J`.
- **`D_{-k}`**, right-edge-frame diagonals `D_{-k}(t) = s(t, t - k)`. Periods
  double with `k` and preperiod is `0` throughout:
  `1, 2, 2, 4, 8, 8, 16, 32, 32, 64, ... , 4096` at `k = 29..33`, then
  **`None` for every `k >= 34`**.

This is **validation of the known left-regular / right-chaotic asymmetry** of the
Rule 30 light cone, not a discovery. Labelled as validation so it is not
later mis-cited.

## The `None`s are a detection ceiling, and the ceiling is exactly 4096

`comoving_columns.py`'s `exact_period` accepts a candidate period `q` only if

```python
if n - onset >= max(8 * q, 128):
```

with `n = T = 32768`. So for any `q >= 4097`, `8q >= 32776 > 32768 >= n - onset`,
and the condition **cannot be satisfied for any onset whatsoever**. The largest
period this run is capable of reporting is therefore exactly

```
q_max = T / 8 = 4096
```

irrespective of the `max_q = T // 4 = 8192` search bound, which is never the
binding constraint.

**`D_-33` reports exactly `4096`, with preperiod `0` — it sits precisely at the
ceiling**, passing by equality (`n - onset = 32768 >= 8 * 4096 = 32768`). Given
the observed doubling, `D_-34` would carry a period of `8192`, requiring
`T >= 65536`. It is unmeasurable at this horizon **by construction**.

So the transition from `4096` to `None` at `k = 34` is the instrument running
out, not the sequence becoming aperiodic. The 367 `None` entries carry **zero**
information about periodicity. Reading them as an aperiodicity result would be
the same class of error as citing `lhp_lock_search`'s "0 lock candidates" as an
exclusion (`OVERNIGHT-HANDOFF-20260905.md`).

## Disconfirming check

A version of this audit that could not fail would be one that merely observed
"`None` appears late, so it is probably a horizon effect". This is not that: the
ceiling is derived from the acceptance inequality in the source, is exact, and
independently predicts the *observed* crossover point — the last successful `k`
must be the last one whose period is `<= 4096`, and `k = 33` is exactly that
cell. The prediction and the data agree on the specific index, not just the
qualitative shape.

The disconfirming outcome would have been a `None` at some `k` whose period was
well under 4096, or a reported period above 4096. Neither occurs: every reported
period is a power of two `<= 4096`, and the `None`s begin exactly where the
ceiling says they must.

## Consequences

- **A12 is closed.** The artefact is internally consistent and correctly
  computed; it simply has a horizon.
- **Do not cite `D_{-k} = None` as evidence of anything.** If a period for
  `k >= 34` is ever actually wanted, it needs `T >= 65536` for `k = 34` and
  doubles per `k` after that — which puts `k = 40` at `T >= 4194304`. That is a
  memory-bound run on a box that has been swap-tight all week, and no result on
  record depends on it.
- The left-frame result (`A_J` eventually periodic with period `<= 16` out to
  `J = 400`) is the substantive content, and it is validation of known Rule 30
  structure, not new.
- Nothing here touches R1's zero-set obligation. The comoving frames move with
  the light cone; R1 is about the fixed centre column.

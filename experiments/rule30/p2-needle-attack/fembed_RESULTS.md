# RESULTS — the 2-row forcing embedding of live states

Pre-registration: `fembed_PREREG.md`. Script: `fembed_lemma.py`. Data:
`fembed_lemma.json`. Deterministic; no seeds, so every number below is
regenerated exactly by `uv run python fembed_lemma.py` (it skips cells already
present in the JSON; delete it to force a full rerun).

`*.log` is globally gitignored, so `fembed_lemma.log` and the `krow_run.log`
cited in §E.1 are local-only. Every figure taken from a log is also derivable
from a committed JSON: the separations in §E.1 come from `krow_run.log` but
the `m(n)` values behind them are in `krow_hc_extend.json`.

Scope run: `c in (2,3)`; arm `all` for `n=10..17`, arm `hardcore` for
`n=10..26`. **50 cells.** Every survival recomputed from the live state;
nothing read from `estate_census.json` or `krow_hc_extend.json`.

## Provenance, stated plainly

`krow_RESULTS.md` §4 already asserted parts A and B (100%, hard-core arm,
`n=10..20`, both tails). Those numbers came from an interactive session with no
script behind them. This run is a **re-derivation of an inherited claim**, plus
the four sub-questions that interactive check never asked. The claim survived.

## A — the embedding: CONFIRMED, 50,146 checks, 0 failures

For every live state `L` at level `n` with survival `s >= 2`, the state after
two forced rows is a **realizable** live state at level `n+1` with survival
exactly `s-2`.

* 50,146 `(n, c, arm, L)` instances with `s >= 2`.
* `A_unrealizable = 0` and `A_survival_mismatch = 0` in all 50 cells.
* Newly covered: the **`all` arm**, which the prior assertion did not test, and
  hard-core `n=21..26`. It holds in both.

`survival(image) == s-2` is a theorem, not data: `append_live` sets
`out[0] = BOUNDARY[v]` and `BOUNDARY` is an involution, so
`prev == BOUNDARY[live[0]]` is a forcing invariant and `hc_run` restarted at
the image reads the parent's continuation shifted by two with the right `prev`.
`selftest_invariant()` checks this directly (state-by-state, all 114 states of
`n=12` hard-core, every row `t`, not just `t=2`) and passes. **Realizability is
the content of A**, and it is not a theorem.

Consequence: `m(n+1, c) >= m(n, c) - 2`, hence `gamma(n+1,c) <= gamma(n,c)+3`.

## B — four rows into level n+2: CONFIRMED, 8,136 checks, 0 failures

Same statement with `s >= 4`, image at level `n+2`, survival `s-4`. No
exceptions in any cell.

## A' — independent reproduction of `krow_hc_extend.json`

Unplanned, and free: this script recomputes `max_survival(n,c)` from a
different code path (`enumerate_leaves` + per-state `force_live`, no two-pass
histogram, no `TOPK` threshold). Across the **34 overlapping hard-core cells**
(`n=10..26`, `c in (2,3)`) there are **zero mismatches** against
`krow_hc_extend.json`. That column of the extended census is now independently
reproduced.

## C — the map is NOT injective

Only 2 of 50 cells (`n11_c2_hardcore`, `n13_c2_hardcore`, both tiny) are
injective. Typical collision histogram (`n17_c2_all`, 3,772 sources onto 3,062
images): 2,480 images with one preimage, 487 with two, 69 with three, 21 with
four, 4 with five, 1 with seven.

So the embedding transports **existence, not counts**. Fiber sizes at level `n`
say nothing about fiber sizes at level `n+1` through this map, and any argument
that tries to push a counting bound forward along it is invalid.

## D — coverage is a stable ~7-10%, with no trend

Image size over `|leaves(n+1, arm)|`, `c=2`:

| arm | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|
| all | .077 | .064 | .079 | .071 | .073 | .069 | .072 | .073 |
| hardcore | .065 | .123 | .104 | .078 | .106 | .082 | .097 | .096 |

| hardcore, cont. | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|---|
| | .104 | .089 | .097 | .098 | .097 | .092 | .096 | .095 | .094 |

Flat in `n` in both arms, and the hard-core arm settles to `.094-.098` across
the whole of `n=20..26` rather than drifting. The level-`(n+1)` state set is
roughly 10-13x the image of level `n` at every size checked, so the hierarchy
is nowhere near collapsing into a single forward orbit, and the embedding sees
a fixed small slice of each new level.

## E — the bound is usually SLACK, and it is the wrong direction anyway

`slack = m(n+1) - (m(n) - 2)`, over all 50 cells:

| slack | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| cells | 7 | 6 | 14 | 12 | 4 | 5 | 2 |

Tight (`slack = 0`) at exactly `n12_c2_all`, `n10_c3_hardcore`,
`n18_c2_hardcore`, `n21_c2_hardcore`, `n23_c2_hardcore`, `n23_c3_hardcore`,
`n26_c3_hardcore`.

### E.1 — tightness predicts the killing-row spikes, and the match is exact

`krow_RESULTS.md` §4 claims the spikes occur at the `n` where this bound is
tight, because tightness forces the level-`(n+1)` extremal state to BE the
2-row image of the level-`n` extremal state, hence exact state equality. That
claim was stated only for `n=23,26,28`. The tight `n` are now computed directly
for `n<=26` here, and read off `krow_hc_extend.json`'s `m(n)` for `n=27..29`;
the separations are in `krow_run.log:28,36` (hard-core `K0`, 20 pairs, index
`i` = pair `n=10+i -> 11+i`).

Hard-core arm, every tight `n` in `n=10..29`, against the `K0 prefix`
separation at that pair:

| c | tight n | source | K0-prefix separation |
|---|---|---|---|
| 2 | 18 | this run | +31 |
| 2 | 21 | this run | +35 |
| 2 | 23 | this run | +47 |
| 3 | 10 | this run | +9 (suffix +20) |
| 3 | 23 | this run | +45 |
| 3 | 26 | this run | +53 |
| 3 | 28 | `krow_hc_extend.json` | +52 |

All 7 tight `n` show a positive separation. Conversely, **no non-tight pair in
either tail reaches +20**: in `c=2` the only separations `>= +20` are at
indices 8, 11, 13 (`n=18,21,23`) and in `c=3` only at 13, 16, 18
(`n=23,26,28`). The correspondence is exact in both directions over
`n=10..29`, and it holds at `n=18` and `n=21`, two pairs `krow_RESULTS.md` did
not name because §4 only looked at the extended range.

Caveat on the one weak entry: `c=3, n=10` is tight but separates by only +9.
That is a length effect, not a miss. The killing-row state is ~21 cells long
there versus ~58 at `n=23`, so +20 (suffix) is near-total agreement in relative
terms. It is reported rather than smoothed over.

### E.2 — usefulness verdict: none for `gamma >= 1`

`m(n+1) >= m(n)-2` is a lower bound on max survival; `gamma = (n+2) - m` and
`gamma >= 1` needs an UPPER bound on `m`. The lemma pushes in the direction
that cannot prove the target, and it is slack in 43 of 50 cells besides. It is
an explanation of a measured artifact (the spikes), not a step toward the
theorem. Recorded so no later session re-derives it and mistakes it for
progress.

## F — WORDS vs STATES: settled, in evidence

`RESULTS-GAMMA-PROOF-ATTEMPT.md` §2 rules out an `n -> n+2` induction because
the zero-padding prefix has length `n` tied to the same `n`, so a level-`(n+1)`
problem starts at a different absolute offset and the level-`n` best **word**
cannot be continued.

The two statements are compatible, and this is now measured rather than argued.
For one extremal source state per cell, the script records the level-`n`
representative word, the level-`(n+1)` representative word of its image, and
whether the second extends the first. **In 0 of 50 cells does the image word
extend the source word.** Example, `n17_c2_all`, source survival 11:

```
source (level 17):  1 1 1 1 2 1 2 1 1 1 1 1 1 1 2 1 2
image  (level 18):  1 1 1 1 2 2 1 1 1 1 1 1 1 2 1 2 2 2
```

They diverge at position 6. The image state is realized at level `n+1` by a
**different** word, reached from a longer zero-padding prefix. §2's obstruction
is about word continuation and stands; the lemma is about state coincidence and
also stands. Neither doc needed a correction, only a cross-reference, which has
been added to both.

## Net

The inherited claim is now reproducible and true on a wider range than it was
asserted for (50 cells, both arms, hard-core to `n=26`). It is also, per E.2,
useless for the target, and per C it cannot carry counts. The two things it
does deliver: it explains the killing-row state equalities in `krow_RESULTS.md`
§4 as generic forcing behaviour rather than family structure, which is what it
was invoked for and which E.1 now verifies exactly in both directions over
`n=10..29`; and per A' it independently reproduces the `max_survival` column of
`krow_hc_extend.json`.

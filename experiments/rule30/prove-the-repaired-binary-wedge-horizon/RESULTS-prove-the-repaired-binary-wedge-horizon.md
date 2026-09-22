# The maximal-drop inheritance converse, three trials the census already held

Status: **partial. `(BWH+)` is still conjectured and no ladder statement
changed.** Three previously untested trials of the §4b converse are settled
from the published census at no new compute cost, all inherited. The decisive
experiment for this target is not reachable here and the blocker is named in §2.

## 1. Three qualifying steps nobody had run (C)

`RESULTS-BINARY-WEDGE-HORIZON.md:347` states the surviving §4b claim: every
step with `M(n+1,c) = M(n,c) - 2` also has `Q(n+1,c) = Q(n,c)[2:]`. Its kill
condition at `:361-362` is unrestricted in `n`, but §4b only ever tested
`18 <= n <= 26`, and the frozen-inequality extension added `29 -> 30`. The
published census below `n = 18` contains three qualifying steps that were never
examined, because §4b never looked there.

| step | `M(n,c) -> M(n+1,c)` | `Q(n,c)[2:]` | `Q(n+1,c)` | verdict |
|---|---|---|---|---|
| `n=15 -> 16`, `c=3` | 16 -> 14 | `21111112211121` | `21111112211121` | inherited |
| `n=5 -> 6`, `c=3` | 8 -> 6 | `112121` | `112121` | inherited |
| `n=6 -> 7`, `c=2` | 9 -> 7 | `1111122` | `1111122` | inherited |

Reproduced in this session from
`p1-period2-invariant/binary_wedge_census_exhaustive.py`, cwd that directory:

```sh
uv run --offline --no-project python binary_wedge_census_exhaustive.py --continuations --first-n 15 --last-n 16
uv run --offline --no-project python binary_wedge_census_exhaustive.py --continuations --first-n 5 --last-n 8
```

Both under a second, single-process, and neither writes any tracked artifact.
All three steps carry a **single** distinct `Q` on each side, so the strong form
of the claim (every maximal `Q(n+1)` is inherited) also holds here, where it had
failed at `18->19` `c=3`, `22->23` `c=3` and `29->30` `c=2`.

**Control.** Every `M` printed matches the published census at its `(n,c)`:
`n=15` gives 11 and 16, `n=16` gives 14 and 14, `n=5` gives 2 and 8, `n=6`
gives 9 and 6, `n=7` gives 7 and 6, `n=8` gives 6 and 7. That is the same
cross-check §4b's published rows passed, and it fires against the census rather
than against the continuation pass that produced the `Q` values.

**Scope, both readings.** Unrestricted, as the kill condition is written: 9 of
9. Inside the `(BWH+)` regime `n >= 7`, where `n=5->6` and `n=6->7` straddle the
region in which `(BWH+)` is itself false (`M_3(5)=8`, `M_2(6)=9`): 7 of 7, with
`n=15->16` the one clean new trial. **Computed, not proved.** Nine trials are no
more a law than six, exactly as `RESULTS-BINARY-WEDGE-HORIZON.md:348-359` says
of the original six.

## 2. What the next trial costs, and one sweep that must not be run

`29 -> 30` at `c=3` is **not** a trial and re-running it proves nothing: the
published values are `M_3(29) = 24` and `M_3(30) = 24`
(`RESULTS-BINARY-WEDGE-HORIZON.md:104`,
`frozen-inequality-survives-an-exhaustive/RESULTS-frozen-inequality-survives-an-exhaustive.md:110`),
a drop of zero, so it never satisfied the hypothesis. That is roughly 3000 s of
continuation sweep not worth spending. The `c=2` half of the same step does
qualify, `27 -> 25`, and the frozen doc already tested it.

The next genuinely new trial therefore needs `M_c(31)`, which is the `n=31`
census at about 6500 s single-core by the doubling in
`frozen-inequality…md:188-202`, followed by a `--continuations` pass per
qualifying tail. **Blocker: over the one-hour bar for a single serial
experiment, and the machine is at 6 of 10 cores under a running census.**

## 3. The atlas prompt for this target is the older reading (flag, not a result)

The target prompt states that `(BWH+)` is the wrong thing to prove and that the
live edge moved elsewhere. `RESULTS-BINARY-WEDGE-HORIZON.md:195-206` concludes
the opposite and is the later document: any argument giving `g(n) <= n+1` with
slack for `n >= N_0`, plus the exhaustive census below `N_0`, closes the rung;
"A bound as weak as `g(n) <= 0.95 n` for large `n` would suffice, and is
`0.11 n` above the measured growth"; and the census supplies `N_0 <= 30` for
free, `31` once the held-out `n=30` row is counted. The doc's own framing is
that the target is "a lossy asymptotic bound plus a finite check, not a tight
combinatorial identity".

Both readings are in the archive. This section records the divergence; it does
not adjudicate which a later session should follow, and nothing in §1 depends
on the answer.

## 4. Files

No new scripts. Everything here is `binary_wedge_census_exhaustive.py` with
`--continuations` at ranges the published runs did not cover, plus the census
rows already in `RESULTS-BINARY-WEDGE-HORIZON.md` and the frozen extension.

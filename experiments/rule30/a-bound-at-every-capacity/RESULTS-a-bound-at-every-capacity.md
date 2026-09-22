# The capacity language's dimension grows as log_3(K/2), located exactly through K=500

Status: **computed at every cap `K = 1..500`, with two pre-stated predictions
confirmed. No ladder statement changed; "a bound at every capacity" stays
open.** This rescopes one precondition of an existing kill; it proves no bound.

## 1. What was open

The capacity route is killed partly on the claim that the dimension of the
guarded capacity language expands with the cap. The tracked evidence for that
was two points: `capacity-17-language.json` carries one independent repetition
parameter and `capacity-32-language.json` carries two. Two points locate
neither where the growth happens nor how fast.

`capacity_dimension_sweep.py` runs the same `decompose()` and
`verify_language()` at every cap and records the first cap at which each
parameter count appears. It calls them directly rather than through the CLI,
which would write `capacity-{K}-language.json` into the shared directory for
every `K`, two of them tracked.

**Control.** At caps 17 and 32 the decomposition reproduces the tracked JSON
exactly in every result field. `verification.all_lengths` is true at every one
of the 500 caps.

## 2. Result

| parameters `d` | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| first cap `K` with `d` | 1 | 6 | 18 | 54 | 162 | 486 |

The first appearances are `2 * 3^d`. Checked at **every** cap, not only the
first appearances: the parameter count equals `max{n : 2 * 3^n <= K}` at all
500 caps with zero exceptions, so it is a step function in `log_3(K/2)` with no
dips. At `K = 500` the language has 1784 patterns over 535 states and 1194
edges.

**Pre-registration.** After the sweep to `K = 64` showed 6, 18, 54, I wrote
`first_cap(4) = 162` and `first_cap(5) = 486` into `PREDICTION.txt`, with the
kill "`first_cap(4) != 162`", before running further. The file's timestamp
field did not render, a formatting slip; its modification time, 19:28:51,
precedes `sweep200.json` at 19:28:55, and both files are kept as that evidence.
Both predictions held.

## 3. What it changes

The kill's precondition is **confirmed and quantified**. Dimension does grow
without bound on this evidence, so any argument that needs a bounded number of
independent repetition parameters across all capacities is dead through
`K = 500` rather than on one step from 17 to 18. But it grows only
logarithmically: a capacity-`K` argument has `floor(log_3(K/2))` independent
parameters to control, not a number comparable to `K`. That is a different
obstacle from the one the kill's wording suggests, and a narrower one.

What it does not do: it bounds nothing. The node needs a finite `B(K)` for every
`K`, and a dimension count is a statement about the language's shape, not about
mortality within it.

## 4. Scope

Exact at every cap `1 <= K <= 500` and nothing past it. The law
`d(K) = max{n : 2 * 3^n <= K}` is measured over that range with two
out-of-sample confirmations; it is not proved for all `K`, and a third step at
`K = 1458` was then predicted and confirmed, §6. The four cap-18 seams are being
worked in another session and are not touched here.

## 5. Files

`capacity_dimension_sweep.py` (`capacity_dimension_sweep.log`),
`PREDICTION.txt`, `sweep200.json`. The sweep writes no tracked artifact. Logs
are hidden by the global ignore; `git add -f` to commit them.

## 6. Third prediction, to `K = 1460`

§4 left the law's next step, `first_cap(6) = 1458`, predicted and not run.
`PREDICTION-2.txt` states it with its kill, "`first_cap(6) != 1458`, or any
`K` in `501..1460` where `d(K)` differs from the law", timestamped
2026-09-20 21:41:33, eight minutes before the run's log was written at
21:49:33. This time the timestamp rendered.

It held. Six parameters first appear at exactly `K = 1458`, and the parameter
count equals `max{n : 2 * 3^n <= K}` at **every** cap `1..1460` with zero
deviations. Both tracked controls reproduce and `all_lengths` holds at every
cap. 475 s single-process.

That is three out-of-sample confirmations of one law, at 162, 486 and 1458,
each predicted from data that stopped short of it. It is still measured, not
proved, and its next step at `K = 4374` is predicted and not run.

`capacity_dimension_sweep_1460.log`, `PREDICTION-2.txt`.

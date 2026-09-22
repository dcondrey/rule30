# Four of the five pure period-5 seeds are robust shields at buffer 44 to 48

Status: **four exhaustive closure certificates, one seed still open. No ladder
statement changed; "Infinite-support xhat(y)" stays conjectured.**

## 1. What was open

`strengthen/strengthen_4.json` stores all five pure period-5 seeds of width 16
(99cb, 20dc, 60dc, 9b6a, a0dc) as `violation at J=32`: the shield certificate
found a counterexample state at every buffer it tried, through 32. The stored
ladder stopped there, so whether any of them closes at a larger buffer was
unmeasured. Nothing past `J = 32` exists for them in the tree.

`period5_shield_ladder.py` imports `spacetime`, `certify` and
`near_wall_pattern_from` from the existing code and runs the same ladder to
`J = 64`. It builds the spacetime 72 columns wide instead of 40 so `certify` can
read that far; `near_wall_pattern_from` stops at the first non-periodic column,
well inside 40 for these seeds, so `j*` is unchanged and that is asserted
against each stored row. The existing drivers rewrite tracked JSON, so this
writes only its own log.

**Control.** At `J = 32` every seed reproduces its stored verdict and its stored
state count exactly: 124, 96, 89, 96 and 344 states, all `violation`. The same
code that later closes a seed first fails it at the smaller buffer, so the
checker demonstrably says no.

## 2. Result

| seed | `j*` | `L` | `t0` | at `J = 32` | verdict |
|---|---|---|---|---|---|
| 20dc | 18 | 10 | 2 | violation, 96 | **closed at `J = 44`** |
| 9b6a | 18 | 10 | 0 | violation, 96 | **closed at `J = 44`** |
| a0dc | 16 | 10 | 1 | violation, 344 | **closed at `J = 44`** |
| 60dc | 16 | 10 | 1 | violation, 89 | **closed at `J = 48`** |
| 99cb | 9 | 10 | 2 | violation, 124 | violation at every buffer through `J = 60`, §6 |

`closed` is `certify`'s exhaustive outcome: the reachable state set closes with
no violation, below the cap. It is a machine-checked certificate for that seed
at that buffer, which the existing ladder reports as `PROVED`. 28 s in all,
single-process.

## 3. What it changes, and what it does not

The stored `violation at J=32` for these four seeds was **buffer-limited**: they
are robust shields, at buffers between 44 and 48, and nothing before this run
went past 32.

It does **not** contradict `RESULTS-RIGHT-SEED-MARGIN.md:321-325`, and an
earlier reading of mine that it did was wrong. That sentence says no period-5
block with `j* <= 12` is a robust shield **at buffer 16**, which stays true: the
four seeds that closed have `j* = 16` or `18`, outside that class, and at
buffer 32 or more, above it. The one seed inside the class, 99cb with `j* = 9`,
fails at every buffer through 60 (§6). What the sentence's gloss, "consistent with the
period-5 regime being broken by defects", no longer covers is these four: they
hold period 5 robustly once the buffer is large enough. The same paragraph
already records period-7 shields that close only at buffers 23 to 28, so this
is the same buffer effect one regime over.

It proves nothing about the ladder statement: four seeds of one width decided
is not an infinite-support statement for `xhat(y)`. The 4,170 late period-5
settlers have no periodic near-wall column at all, so this method cannot start
on them.

## 4. Scope

Five seeds of width 16, buffers `J = 34..64` in steps of 2, state cap
6,000,000; 99cb was re-run past that cap in §6 and violates through 60. Nothing
is claimed for any other seed, width or buffer.

## 5. Files

`period5_shield_ladder.py` (`period5_shield_ladder.log`). Writes no tracked
artifact. Logs are hidden by the global ignore; `git add -f` to commit them.

## 6. 99cb fails at every buffer through 60

§2 left 99cb undecided at `J = 58..64` because the ladder hit its 6,000,000
state cap there. It is the only seed of the five inside the class the margin
document scopes, `j* <= 12`, so it is the one whose outcome bears on that
document's claim. `seed99cb_high_cap.py` re-runs those buffers with a larger
cap, after reproducing the stored `J = 56` violation and its state count,
3,718,373, exactly.

| `J` | cap | verdict | states to verdict | peak RSS |
|---|---|---|---|---|
| 58 | 12,000,000 | **violation** | 11,470,281 | 2.2 GB |
| 60 | 24,000,000 | **violation** | 23,109,794 | 4.2 GB |

So 99cb fails with an outright violation at all fourteen buffers
`J = 34..60`. It is not buffer-limited the way the other four were. The states
needed to find the violation roughly double per two buffers at the top of the
range, so `J = 62` would need about 46 million states and about 9 GB, which is
where this stops, with the census holding six cores and the memory beside them.

This strengthens the margin document's scoped claim rather than weakening it:
"no period-5 block with `j* <= 12` is a robust shield" was measured at buffer
16, and its only member in this family now fails through buffer 60. The four
seeds that closed lie outside that class. So the section-3 reading holds with
more force: robust period-5 shielding appears here only for `j* = 16` or `18`.

Scope: one seed, buffers 58 and 60, caps 12M and 24M. `J >= 62` is
undecided, and a violation at every buffer measured is still finite.

`seed99cb_high_cap.py` (`seed99cb_high_cap.log`, `probe99cb.log`).

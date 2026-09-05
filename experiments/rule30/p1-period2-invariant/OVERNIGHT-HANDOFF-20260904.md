# Overnight run handoff — 2026-09-04 ~21:50

## How to read the results in one command

```bash
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
grep -h "^RESULT\|^   D=" overnight_c2_odd.log overnight_c2_even.log \
                          overnight_c3_odd.log overnight_c3_even.log
```

Also check the four `n=30` SAT jobs (separate, started earlier):

```bash
for f in uc/r1-skeptic/gap_30_*.log; do printf "%-22s " "$(basename $f)"; \
  [ -s "$f" ] && cat "$f" || echo "(still running)"; done
```

## What is running

Four detached streams of `overnight_census.py` (PIDs 62820, 62822, 62825,
62827), one pass per `(n, tail)` computing `|H_r(n)|` (r=0,1,2), `D_k`,
`S_k`, max survival row, and the extinction margin together:

| stream | tail | n values | log |
|---|---|---|---|
| A | 2 | 17, 19, 21, 23 | `overnight_c2_odd.log` |
| B | 2 | 18, 20, 22, 24 | `overnight_c2_even.log` |
| C | 3 | 17, 19, 21, 23 | `overnight_c3_odd.log` |
| D | 3 | 18, 20, 22, 24 | `overnight_c3_even.log` |

Output is flushed per `n`, so a killed or unfinished stream still leaves
every smaller `n` usable. Rough cost scaling measured at ~5x per `+2` in
`n` (`n=12` took 1.5 s): expect `n=22` ~80 min and `n=24` ~7 h, so the
`n=23/24` entries may not land. Everything through `n=22` should.

Controls that already passed at launch (in `overnight_c2_odd.log`):
prefix-consistency of `literal_extension`, and an `n=16, c=2` regression
reproducing the committed `D=[2,3,5,8,13,21,27,20,6,3,1,0]` exactly.
`n=10`/`n=12` margins reproduced the concurrent session's `7` and `5`.

## The predictions being tested (frozen before the run)

Full text in `PREREGISTRATION-OVERNIGHT-EXTENSION.md`. Scoring guide:

- **P1, the real test.** `D_k`'s Fibonacci/surjectivity phase should depart
  at `k_dep ~ floor(n/2) - 2`, i.e. predicted `6,7,7,8,8,9` for
  `n = 17..22`. Read `k_dep` off the printed `D=` array as the first index
  where `D_k` falls below the hard-core count `2,3,5,8,13,21,34,55,89,...`.
  Correct if within 1 everywhere; **falsified** if any `n` is off by 2+, or
  if the deviation grows with `n`. This tests the light-cone explanation of
  the `D_k` phase, which was written before any `n>16` data existed.
- **P2, census.** Expect `H0=H1=H2=0` everywhere. **A single nonzero value
  is an RW counterexample** and by far the most valuable outcome — it would
  refute the conjecture on the tested range. Do not gloss over it.
- **P3, extinction margin.** `margin = (n+2) - max_row` should stay `>= 1`,
  probably near 8 (measured `7,5,6,8,8,8` at `n = 10..18`). **Kill:** a
  monotone decline toward 0 across `n=17..22` means the concurrent
  session's "bounded below" hope is dying — report that, don't smooth it.
- **P4, product margin.** Geometric mean of post-departure `D_{k+1}/D_k`
  should stay under `1/phi = 0.618`. Any `n` at or above that breaks the
  only surviving form of the `D_k` contraction argument (the per-step form
  is already dead: true max is 1.0 at `n=12,14`).

## Standing caveat

Six more zeros in the census is evidence, not a proof surrogate — the
project's own `PREREG-psi-constraint-counting` near-miss statistic warns
against extrapolating an empty census. The value of this run is in P1, P3
and P4, which are falsifiable structural predictions, not in P2.

## State of play when this was launched

Verified and standing:
- SAT grid **complete through `n=29` with no gaps** (the last cell,
  `n=29,r=2,c=3`, returned UNSAT at 9440.7 s: 29473 vars, 91524 clauses).
  Four `n=30` instances still running.
- `|H_r(n)| = 0` for `n <= 16` (concurrent session, `rw_population_h.py`).
- `D_k` computation verified by two independent forcing rules.
- `phi/4` null model's core assumption verified (forced symbol uniform over
  the 4 states to within 0.005 at `n=16`).
- `13/32` is exact and now **explained**: the deepest diagonal value is
  exactly uniform on the 4 states at every `n`, because every four-symbol
  action is a permutation generating D8 and permutations preserve uniform
  measure. Demoted from "invariant" to "consequence of bijectivity", and it
  is **not** `phi/4` (0.40625 vs 0.404508).

Retracted or demoted during the session (all committed with corrections):
- The `Psi_n` vs `H_r(n)` "naming collision" — **false**, withdrawn. The
  two constructions define the same survivor population (0 death-level
  mismatches over 7168 words). Caused by comparing different-typed outputs.
- "Three independent codings converge on 0.4" — dropped; they are three
  codings of one process.
- "`D_k` is Fibonacci `2,3,5,8,13,21`, surjective for ~5 rows" — true only
  at `n=16`; the phase length grows as `~n/2-2`.

Strongest open lead is **not** mine: the concurrent session's
extinction-margin idea (`BACKLOG.md` L11, `RESULTS-EXTINCTION-MARGIN.md`).
P3 above is a direct test of it, which is why it is in this run.

## Do not

- Do not send the Kari email (`DRAFT-EMAIL-KARI.md`); it is parked
  deliberately pending the domination/extinction question.
- Do not claim `n=30` until the four `gap_30_*.log` files are non-empty.
- A concurrent session is active in this directory. Check `git status` and
  `ps` before staging; it owns `rw_population_h.py`,
  `RESULTS-EXTINCTION-MARGIN.md`, `RESULTS-TRANSFER-DOMINATION-CHECK.md`
  and the `fib_absent_*` files.

# Handoff — 2026-09-04 late session (R1-weighted, no compute launched)

Working directory:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant`

Read this before `NEXT-SESSION-PROMPT.md`. Two of that prompt's instructions
are now stale and are corrected below.

## DONE

1. **`uc/r1-r1zero/` fully inventoried** (`RESULTS-R1-ZERO-SET-INVENTORY.md`).
   Every log resolved to what it actually ran and what it showed.
2. **Two identities re-verified exactly** against real Rule 30, `T=400`:
   pin (`c_t=1 -> l_t = NOT c_(t+1)`) 207 tests / 0 failures; pass
   (`c_t=0 -> l_t = c_(t+1) XOR r_t`) 193 tests / 0 failures.
3. **New verified structural fact:** the entire left half-plane `x <= -1` is a
   function of the centre column `c` and the LHP's own `t=0` data. 0 mismatches
   against the true lone-seed LHP over `x in [-400,-1]`. The pin is therefore a
   self-consistency condition on `c` that never mentions `r`.
4. **`lhp_lock_search`'s "0 lock candidates" is NOT an exclusion.** It fixes LHP
   init to zero and is blocked by the PROVED finite-prefix lemma in
   `docs/rule30/RESULTS-eventual-period.md`. Its violation-free tails (9, 14,
   65) are pin-only and measured over `[T/2, T)`, so they are **not**
   comparable to the `H(p,w)` horizons; the argument does not rest on them.
   **Do not cite it as evidence against eventual periodicity.**
5. **Seed task 34 retired as stated.** The lone-seed form of the zero-set probe
   is trivial: direct computation of `c` excludes every period `p <= 64` at
   every onset `<= 10000` in **0.1 s**. Replaced by task A7 (below).
6. **R1's forcing hypothesis is answered NO in the driven-RHP model** by prior
   logs, re-read this session: a periodic `c` does not force `r|Z` periodic in the driven RHP
   (word `01`: no period `q <= 4096` at `T = 524288`; `011` and `00101`:
   0/11 prefixes). It is word-dependent. R1 cannot run through local forcing.
7. **Rule 90 filter applied explicitly** and recorded per argument. Pin
   arguments pass, and pass for the right reason: with `c ≡ 0` the pin has zero
   tests, so it is vacuous exactly where the statement is false.
8. **Seed task 36 answered: no.** `phi/4` and the zero-set density are
   different types. True lone-seed centre-column density measured
   **0.500362** at `T = 200000`; `phi/4 = 0.404508` is a rotated-wedge
   per-row survival eigenvalue. `drive01_long`'s `|Z| = T/2` is `T/2` by
   construction and is not evidence about the real column.
9. **`k_dep` re-derived, not inherited, at every `n` in the corrected table.**
   `n=17..21` computed here from the logged `D` rows against the hard-core
   counts `2,3,5,8,13,21,34,55,89`: `n=17` -> 6/6, `n=18` -> 7/7, `n=19` -> 7/7,
   `n=20` -> 7/7, `n=21` -> 8/8 (`c=2`/`c=3`). All six confirm
   `NEXT-SESSION-PROMPT.md`'s table; none was copied from it.
10. **P1 correction landed** in `RESULTS-DISTINCT-CONTINUATION-COUNT.md`: full
   `n=10..21` table, the three ways `floor(n/2)-2` fails, the light-cone story
   demoted from formula to scale, and the no-tolerance-on-integers rule.
   Corroborated independently against tonight's census logs (`n=20` `k_dep=7`,
   `n=21` `k_dep=8`).
11. **Task list written** (`TASKLIST-20260904-R1.md`), R1-first, with every
    compute item marked blocked and the reason.
12. **`H(2,w) >= w` — VALIDATION, not a finding.** This started the session as
    the top open item ("does the horizon table plateau? a plateau IS the
    theorem"). It was already settled: the finite-prefix lemma proved in
    `docs/rule30/RESULTS-eventual-period.md` gives `H(2,N) >= N` outright, so a
    plateau cannot occur and the question should never have been queued as a
    measurement. The run adds an implementation check and a Rule 90 control,
    and measures the bound to `w = 300` in **0.04 s**
    with `H - w` in `{1,2,3,5}`, reproducing the published `H(2,1) = 6` exactly
    and sitting under every other published cell. **Do not spend SMT compute on
    `w = 9,10,11`.** Rule 90 control shows the same behaviour, so this is a
    left-permutivity fact and a negative about the *method*; it says nothing
    about Rule 30 specifically and must not be cited as if it did, nor cited as
    a new result.
    (`uc/r1-r1zero/h_horizon_lower_bound.py` + `.log`.)

## OPEN

- **A8** general-finite-row form of the zero-set obligation (the real R1
  question): does diagram-global consistency restore the forcing that the
  driven RHP lacks?
- **A12** `comoving_columns_T32768.log` is the last unaudited `r1-r1zero`
  artefact.
- **D1-D3** direct measurement of the source-coordinate dependency window. After
  the P1 falsification this is the only thing that can rehabilitate the
  light-cone story.
- **E1-E5** extinction margin (the concurrent session's lead) — verify, do not
  assume. E4 is the one that could become a theorem fragment.
- **B1-B4, C4, C5, I1** blocked on load or on data that does not exist yet.
- Everything else in `TASKLIST-20260904-R1.md` sections F-I.

## Corrections to `NEXT-SESSION-PROMPT.md` — read these before following it

1. **"Launch the long jobs FIRST" is VOID at current load.** That instruction
   was written at load average 26. At this session's start it was **43.70 on 10
   cores** (12 CPU-bound python processes, ~1.38 GB free RAM), and at session
   end **32.34**. **No jobs were launched this session, deliberately.** Do not
   launch any until the four `n=30` SAT processes retire. This repo has a
   documented jetsam history.
2. **`TaskCreate`/`TaskUpdate`/`TaskList` did not resolve** via `ToolSearch`
   this session (the tool reported no match). If they still do not, write the
   task list to a file as done here; do not burn calls retrying.

## n=30 SAT GRID COMPLETE — all six cells UNSAT (2026-09-05 02:42); n=31 RUNNING

**The RW SAT exclusion grid now runs clean through `n=30`**, extending the
`n<=29` range recorded in `NEXT-SESSION-PROMPT.md`. No SAT job is running.

The grid is `r in {0,1,2}` x `c in {2,3}`. `r=1,2` come from
`rw_sat_r_grid.py`/`rw_sat_gap_fill_one.py`; **`r=0` is a separate earlier
scan** (`rw_sat_n30_20260903.log`) and is easy to miss — the four `gap_30_*`
logs are only four of the six cells, so "all four gap logs returned" is NOT the
same as "the `n=30` row is complete". Both `r=0` cells were already done.

| cell | vars | clauses | result | seconds | log |
|---|---|---|---|---|---|
| `n=30 r=0 c=2` | 29761 | 92417 | UNSAT | 10403.09 | `rw_sat_n30_20260903.log` |
| `n=30 r=0 c=3` | 29761 | 92417 | UNSAT | 13242.53 | `rw_sat_n30_20260903.log` |
| `n=30 r=1 c=2` | 30592 | 95001 | UNSAT | 27975.38 | `gap_30_1_2.log` |
| `n=30 r=1 c=3` | 30592 | 95001 | UNSAT | 26581.05 | `gap_30_1_3.log` |
| `n=30 r=2 c=2` | 31432 | 97613 | UNSAT | 24330.31 | `gap_30_2_2.log` |
| `n=30 r=2 c=3` | 31432 | 97613 | UNSAT | 20477.98 | `gap_30_2_3.log` |

34.2 CPU-hours for the row. `n=29` is likewise complete; its `r=0 c=3` cell is
in `rw_sat_n29_c3.log` in a **different output format** (`n=29 r=0 c=3 ...`
rather than columns), so a `grep '^29 0 '` misses it. Verify the row with:

```sh
cd uc/r1-skeptic && grep -hE "^30 [012] " *.log | tr -s ' ' | sort -k2,2n -k3,3n
```

### CORRECTION: my "~2.2x per n" scaling claim was wrong

Two turns ago I wrote that cost scales ~2.2x per `n` and that `n=31` is
therefore ~12 h. **That was drawn from a single cell (`r=2 c=3`) and does not
generalise.** Per-cell `n=29 -> n=30` ratios:

```
r=0 c=2   11796.39 ->  10403.09    0.88x   (FASTER at larger n)
r=0 c=3    6419.65 ->  13242.53    2.06x
r=1 c=2    2228.47 ->  27975.38   12.55x
r=1 c=3    2547.48 ->  26581.05   10.43x
r=2 c=2   12747.06 ->  24330.31    1.91x
r=2 c=3    9440.73 ->  20477.98    2.17x
```

The ratio ranges 0.88x to 12.55x — one cell got *faster* — so no single growth
factor describes this grid and **no `n=31` runtime estimate is currently
supportable.** What is visible instead is the spread collapsing: `n=29` spans
2228-12747 s, `n=30` spans 10403-27975 s. That is the same
generalise-from-one-case failure the prompt lists four retractions for, and it
is also a datum for **B4**: solve time does not track instance size either (the
`r=1` encoding is *smaller* than `r=2` — 30592/95001 vs 31432/97613 — yet slower
at `n=30`). Any core-scaling study must record `r` and `c`, not just `n`.

### n=31 LAUNCHED at 2026-09-05 08:34, on David's explicit instruction

All six cells, detached, from the project directory. PIDs 23957-23962, all
confirmed alive at 97-99% CPU. Logs `uc/r1-skeptic/gap_31_{r}_{c}.log`, all
0 bytes until their cell returns.

```sh
for r in 0 1 2; do for c in 2 3; do
  nohup env PYTHONPATH=. /Volumes/A/researchpapers/.venv/bin/python3 \
    uc/r1-skeptic/rw_sat_gap_fill_one.py 31 $r $c \
    > uc/r1-skeptic/gap_31_${r}_${c}.log 2>&1 &
done; done
```

**No runtime estimate is supportable** — see the retraction above; the
`n=29 -> n=30` per-cell ratios ranged 0.88x to 12.55x. `n=30` cells spanned
10403-27975 s, so treat "longer than a day" as possible and do not infer a
failure from a long-empty log. Check with:

```sh
cd uc/r1-skeptic && for f in gap_31_*.log; do printf '%-20s %5s bytes  ' "$f" "$(wc -c < "$f")"; tr -s ' ' < "$f" | tr -d '\n'; echo; done
ps -eo pid,etime,%cpu,rss,command | grep '[r]w_sat_gap_fill_one'
```

Remember the `n=30` trap: **six cells, not four.** For `n=31` all six are in
`gap_31_*` logs, so that particular split does not recur here, but do not
declare the row complete off a subset.

### MEMORY RISK on this machine, not caused by the n=31 launch

At launch time `fastdk_benchmark.py` (PID 87926, another session's job, 10h30m
elapsed) was at **8.8 GB RSS**, up from 408 MB when this session started at
23:05 — it is growing without bound. Swap was **7.87 GB used of 9.22 GB**, and
free pages were 73 MB; the launch was judged safe only because ~8 GB of
inactive pages are reclaimable and the six solvers were ~100 MB each at start
(`n=30` peaked ~570 MB, so expect ~4 GB for the row).

This repo has a documented jetsam history. **If something gets killed, suspect
`fastdk_benchmark.py` first, not the SAT jobs.** Whoever owns it should decide
whether it still needs to run; it was not touched here because it is not this
session's process.

**Withdrawn earlier:** an annotation in `TASKLIST-20260904-R1.md` said A7
devalued the SAT-core-scaling task. That conflated two grids —
`rw_sat_gap_fill_one.py` grids the rotated-wedge census over word length `n`,
while `H(p,w)` grids the eventual-period SMT probe over support radius `w`.
`H(2,w) >= w` says nothing about the `n`-grid. Corrected in place.

## Post-midnight update (2026-09-05 00:27), single read

The concurrent session (`88e37218`) had three background tasks killed. What went
with them was its own work only: both `scratch_finalist_via_dedup.py` processes
and the `dlp_rotated_wedge` heredoc. **Every shared long job survived**: the four
`rw_sat_gap_fill_one.py 30 *` (now 5h34m, logs still 0 bytes), the four
`overnight_census.py` streams (3 `RESULT` lines each, now working `n=23,24`), and
`fastdk_benchmark.py`.

Load average was **33.94** at 00:27, and **10.72** at 00:33 once
`gap_30_2_3` finished — back to roughly one job per core. The embargo is
therefore no longer absolute, but three SAT jobs are still running at ~98% CPU
each; **re-check `uptime` yourself before launching anything**, and prefer the
R1 and D1-D3 work, which needs no CPU at all.

## Job state at session end (single read, no polling)

```
uc/r1-skeptic/gap_30_1_2.log   0 bytes   \
uc/r1-skeptic/gap_30_1_3.log   0 bytes    |  4h13m elapsed, still running
uc/r1-skeptic/gap_30_2_2.log   0 bytes    |  NON-EMPTY = the n=30 cell returned
uc/r1-skeptic/gap_30_2_3.log   0 bytes   /   Do not claim n=30 until then.
```

Census: `n=21` complete on both tails, all zero.

```
RESULT n=20 c=2  H0=H1=H2=0  max_row=11  margin=11  1503.6s -> k_dep=7
RESULT n=20 c=3  H0=H1=H2=0  max_row=14  margin=8   1493.9s -> k_dep=7
RESULT n=21 c=2  H0=H1=H2=0  max_row=13  margin=10  2922.9s -> k_dep=8
RESULT n=21 c=3  H0=H1=H2=0  max_row=16  margin=7   2928.0s -> k_dep=8
```
`k_dep` re-derived here from the logged `D` rows against the hard-core counts
`2,3,5,8,13,21,34,55,89`, not copied from the prompt's table:
`n=20 c=2` `D_7 = 50` and `n=20 c=3` `D_7 = 52`, both short of 55, so **both**
`n=20` tails depart at `k=7` against a registered `floor(n/2)-2 = 8`;
`n=21` has `D_7 = 55` on both tails and departs at `k=8`. This independently
reproduces the prompt's `n=20,21` row, and the `n=20` miss is a clean
off-by-one on both tails, not a tail split.

`n=23, 24` streams are still running in the same four processes.

## One command to read every log

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
for f in uc/r1-skeptic/gap_30_*.log overnight_c{2,3}_{odd,even}.log; do
  printf '===== %s (%s bytes)\n' "$f" "$(wc -c < "$f")"; tail -6 "$f"; done
uptime
ps -eo pid,etime,%cpu,command | grep '[p]ython3 ' | grep -v uv
```

## Frozen predictions and their current scores

Registered predictions only. `H(p,w)` growth is deliberately **not** listed: it
was raised and answered inside this one session and was never pre-registered,
and this table exists to keep "a registered kill condition fired" distinct from
"we asked something and answered it". See DONE item 12 instead.

| id | prediction | score |
|---|---|---|
| P1 | `k_dep = floor(n/2) - 2` | **FALSIFIED** exactly (`a0f539b`). Fails at `n=10` (one high) and `n=20` (one low, on both tails), and decisively at `n=12`, where the two tails disagree (`4` at `c=3`, `5` at `c=2`) so no formula in `n` alone can hold at any tolerance |
| P3 | extinction margin bounded below by a positive constant | **SURVIVING.** Running minimum still 5 (at `n=12`). New: `n=20` gives 11/8, `n=21` gives 10/7 (`c=2`/`c=3`). Report the running minimum, never the mean |
| P4 | post-departure geometric mean `< 1/phi = 0.618` | **UNSCORED** at `n>=20`; the `c=3` series was creeping (0.427, 0.395, 0.530, 0.569). Watch for a crossing |

## Rules earned this session

- **Do not attach a tolerance to an exact integer-valued structural
  prediction.** It makes the prediction unfalsifiable. This is what turned the
  `n=20` P1 disagreement into a logged "OK".
- **A search that fixes one initial-data family is a calibration, not an
  exclusion.** Check what the search varied before reading a null result as a
  kill. `lhp_lock_search` varied the prefix and the word, never the left half.
- **Before building a probe, check whether direct computation is cheaper.** The
  lone-seed zero-set probe was going to be real work; the statement it targets
  falls to a 0.1 s loop.
- **Read the load average before following a "launch these first" instruction.**
  It is a fact about the machine now, not about the plan when it was written.
- **Before queueing a measurement, ask whether an already-proved lemma decides
  it.** The `H(p,w)` plateau question was queued as this session's top compute
  item and cost 0.04 s once the finite-prefix lemma already in
  `RESULTS-eventual-period.md` was pointed at `H` itself instead of only at
  `lhp_lock_search`.
- **A kill condition has to be checked against the data already in hand.** The
  drafted `H(2,w) > w + 8` would not have fired on the existing `w <= 8` row,
  so it could not have detected the growth it was written to detect.

## Do not

- Do not send the Kari email or touch arXiv.
- Do not claim `n=30` SAT until those four logs are non-empty.
- Do not `git add` a directory or use `-A`; a concurrent session owns
  `rw_population_h.py`, `RESULTS-EXTINCTION-MARGIN.md`,
  `RESULTS-TRANSFER-DOMINATION-CHECK.md`,
  `RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md` and the `fib_absent_*` files.
- Do not cite `lhp_lock_search`'s zero-lock result as an exclusion.
- Do not extend the `H(p,w)` table to `w = 9,10,11`; `H(2,w) >= w` settles it.
- Do not cite `H(2,w) >= w` as a fact about Rule 30. Rule 90 does the same
  thing; it is a left-permutivity fact about the method.
- Do not spend compute on R7 mode (i); it is closed by a proved limitation
  theorem and the blocker is a state-count wall.

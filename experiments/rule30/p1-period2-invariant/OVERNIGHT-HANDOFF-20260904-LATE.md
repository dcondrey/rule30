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
12. **`H(2,w) >= w` — the SAT/SMT exhaustion route cannot close R1 or the
    `p=2` exclusion.** This started the session as the top open item ("does the
    horizon table plateau? a plateau IS the theorem") and turned out to be
    answerable for free. A plateau cannot occur: the finite-prefix lemma gives
    `H(2,w) >= w`, and the construction measures it to `w = 300` in **0.04 s**
    with `H - w` in `{1,2,3,5}`, reproducing the published `H(2,1) = 6` exactly
    and sitting under every other published cell. **Do not spend SMT compute on
    `w = 9,10,11`.** Rule 90 control shows the same behaviour, so this is a
    left-permutivity fact and a negative about the *method*; it says nothing
    about Rule 30 specifically and must not be cited as if it did.
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

| id | prediction | score |
|---|---|---|
| P1 | `k_dep = floor(n/2) - 2` | **FALSIFIED** exactly (`a0f539b`). Fails at `n=10` (one high) and `n=20` (one low, on both tails), and decisively at `n=12`, where the two tails disagree (`4` at `c=3`, `5` at `c=2`) so no formula in `n` alone can hold at any tolerance |
| P3 | extinction margin bounded below by a positive constant | **SURVIVING.** Running minimum still 5 (at `n=12`). New: `n=20` gives 11/8, `n=21` gives 10/7 (`c=2`/`c=3`). Report the running minimum, never the mean |
| P4 | post-departure geometric mean `< 1/phi = 0.618` | **UNSCORED** at `n>=20`; the `c=3` series was creeping (0.427, 0.395, 0.530, 0.569). Watch for a crossing |
| — | `H(p,w)` growth in `w` | **RESOLVED: `H(2,w) >= w`, measured to `w=300`.** Unbounded, so R1 is **not** reachable by extending the SAT/SMT grid. Rule 90 behaves identically, so this constrains the method, not the rule |

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

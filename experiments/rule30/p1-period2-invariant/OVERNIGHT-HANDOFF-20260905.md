# Handoff — 2026-09-05

Supersedes `OVERNIGHT-HANDOFF-20260904-LATE.md` (still accurate for the R1
inventory and the load history; read this one first).

## DONE this session

**SAT grid.**
- **`n=30` complete, all six cells UNSAT** (`r in {0,1,2}` x `c in {2,3}`),
  34.2 CPU-hours. The exclusion range now runs clean through `n=30`.
- **Trap:** the grid is six cells but only four are in `gap_30_*` logs; the
  `r=0` pair is in `rw_sat_n30_20260903.log`. `n=29 r=0 c=3` is in
  `rw_sat_n29_c3.log` in a different format, so `grep '^29 0 '` misses it.
- **`n=31` has never been solved.** Launched 08:34, stopped 08:36 on
  instruction, every log 0 bytes, empty logs deleted.
- **No runtime estimate for `n=31` is supportable.** Per-cell `n=29 -> n=30`
  ratios range **0.88x to 12.55x** (one cell got faster). An earlier "~2.2x per
  n, so ~12 h" claim was drawn from one cell and is retracted.

**R1 / R7.**
- `uc/r1-r1zero/` fully inventoried (`RESULTS-R1-ZERO-SET-INVENTORY.md`).
- **LHP closure verified:** the whole half-plane `x <= -1` is a function of `c`
  and its own `t=0` data. 0 mismatches, `T=400`. The pin never mentions `r`.
- **`lhp_lock_search`'s "0 lock candidates" is NOT an exclusion** — it fixes LHP
  init to zero and is blocked by the proved finite-prefix lemma. Do not cite it.
- **Seed task 34 retired:** the lone-seed zero-set probe is trivial (direct
  computation excludes all `p <= 64`, onset `<= 10000`, in 0.1 s).
- **`H(2,w) >= w`** — validation of the finite-prefix lemma, confirmed
  constructively to `w = 300`. The SAT/SMT grid cannot close R1 by exhaustion.
  **Do not extend the `H(p,w)` table to `w = 9,10,11`.**
- **The spectral work maps to R7, not R1** (`RESULTS-SPECTRAL-TO-R1-R7-MAPPING.md`).
  A de Bruijn/window automaton *is* the R7 ladder automaton (`PATH.md:1418`),
  and R7's blocker is "state-count wall plus the **free-boundary escape**"
  (`PATH.md:587`) — which is exactly what was proved vacuous here.
- **Ladder ratio -> 4 is saturation, not a trigger or oscillation.**
  `log4(states) - R -> 3.213` constant; absolute deficit `s_R - 4 s_(R-1)`
  bounded at ~-210. No `R` at which it starts compressing.

**Spectral / domination — three kills.**
- Width-`w` window relaxation: `lambda_max = phi` identically, **provably
  vacuous at every width** (the free `(h,F)` cell is always steerable onto the
  target, since `h' = h XOR a XOR 1` with `a` depending only on the left parent).
- **`domination_test.py` scored for the first time** (`domination_test_20260905.log`):
  raw, weighted `w=(1,phi)`, and LP-optimal all give max ratio `1.0000` against
  a needed `< 0.5`. **Dead for every weight vector**, because a same-last-symbol
  `1 -> 1` step has weighted ratio exactly 1 for any positive `w`.
- With a population floor of 30: violations persist at `S_k` = 42, 87, 99, 157,
  **255**; LP optimum `0.5611`. **Raising the floor does not rescue it.**

**Unification and controls.**
- `|S_k| <= Fib(k+1) * max_fiber`: the width-`w` matrix **is** the `phi/4`
  matrix with the fiber factor set to 1. Charging the free cell `1/4` gives
  `phi/4 = 0.404508` exactly; ratio exactly 4.0000 at every `w`.
  **Everything failed at the fiber factor; the Fibonacci factor is rule-blind.**
- **Rule 90 filter: `phi/4` PASSES**, for the right reason. Rule 30's four
  `(c,r)` pairs split **1:3** across the two `l`-behaviours (`q = 1/4`);
  Rule 90's split **2:2** (`q = 1/2`). Same machinery: Rule 30 `2 lambda = 0.809`
  (extinction), Rule 90 `1.618` (correctly, none).
- **Rule 30 is the UNIQUE quiescent left-permutive ECA with `q < 1/(2 phi)`.**
  16 of 256 are left-permutive; 8 also quiescent; only rule 30 passes. Rules
  15, 45, 75, 135 pass `q` but are **not quiescent** (`f(0,0,0)=1`), so they
  admit no finite-seed framing. Rule 240 (`f = l`) is the opposite extreme
  (`q = 1`) and has a *total* pin, showing **the pin alone is not sufficient**.
  Rule 10 is not left-permutive; the framework does not apply to it.

**Paper.** `docs/rule30/paper/zero-tail-note.tex` Scope section extended: the
paper's constant-trace theorem is the `p=1` rung, `H(1,w) = w+2` sharp, while
`H(2,w) >= w` is unbounded — so `p=1` is not the first case of a uniform family.

## Corrections made against myself this session

1. "~2.2x per `n`" scaling — from one cell, retracted.
2. Compared `lhp_lock_search`'s pin-only tails to `H(p,w)` horizons — different
   objects, withdrawn.
3. Called `H(2,w) >= w` a NEW RESULT — it is **validation** of a proved lemma.
4. Said A7's plateau branch was open — it is closed by that same lemma.
5. Said the criterion "isolates Rule 30's equivalence class" — wrong; with
   quiescence imposed it isolates **Rule 30 alone**.
6. Said domination failed only in a small-`S_k` tail — **wrong**, violations
   reach `S_k = 255`. Read off a ratio-sorted top-8 list.
7. Annotated B4 as devalued by A7 — conflated the RW `n`-grid with the `H(p,w)`
   `w`-grid; withdrawn.

## OPEN — where to go next

**The live target is the PRODUCT, not the per-step maximum.** Per-step
domination is sufficient but not necessary, and is now dead three ways. The
induction needs `S_need / S_0 < 2^-n`, i.e. `prod_k ratio_k` bounded —
a geometric mean below `1/phi = 0.618`. The aggregate rate converges to
`phi/4 = 0.4045` with real margin even though individual depth ratios exceed
0.5. `RESULTS-DISTINCT-CONTINUATION-COUNT.md` already records the product form
as the surviving one.

Also open: **R1-A8** (general-finite-row zero-set obligation),
**A12** (`comoving_columns_T32768.log`, the last unaudited r1-r1zero artefact),
**D1-D3** (direct dependency-window measurement), **E1-E5** (extinction margin).

## Do NOT

- Do not build another De Bruijn / window / transfer-matrix automaton. It is
  R7's encoding, its verdict is recorded, and `PATH.md:298-299` says not to
  re-run at larger `R`, `k` or `Q`. Two independent refutations exist
  (`MEMO-SPECTRAL-BOUND-CANNOT-CLOSE.md`, concurrent session, same day).
- Do not use `lambda < 2` as a criterion — `phi = 1.618 < 2` already, so it
  cannot fail. A count needs `lambda < 1`, i.e. `rho < 1/2`.
- Do not extend `H(p,w)` to `w = 9,10,11`.
- Do not spend compute on R7 mode (i).
- Do not claim `n=31`. Do not send the Kari email or touch arXiv.
- Do not `git add` a directory or use `-A`.

## Machine and concurrency

`fastdk_benchmark.py` (PID 87926, **not this session's**) has run 12+ hours and
reached multi-GB RSS; swap has been tight all session and kept climbing after
every other job was killed. It is the jetsam risk on this box. `kill 87926` if
unwanted. At least two other sessions are active in this directory and own
`BACKLOG.md`, `rw_population_h.py`, `RESULTS-EXTINCTION-MARGIN.md`,
`RESULTS-TRANSFER-DOMINATION-CHECK.md`, `MEMO-SPECTRAL-BOUND-CANNOT-CLOSE.md`,
the `fastdk_*`/`fiber_*`/`scratch_*` files, and the new `r1-zero-set-attack/`
and `p1-seam-cegis/` directories. **Stage by name only.**

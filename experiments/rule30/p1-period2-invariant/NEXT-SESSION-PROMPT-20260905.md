# Prompt for the next session (copy everything below the line)

---

You are resuming the Rule 30 period-2 exclusion project. Working directory:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant`

Read `OVERNIGHT-HANDOFF-20260905.md` FIRST, then
`RESULTS-FIB-FIBER-UNIFICATION.md` and `RESULTS-SPECTRAL-TO-R1-R7-MAPPING.md`.
Do not re-derive anything marked DONE there. Note that handoff's "Corrections
made against myself" list — those are claims that were committed and then
withdrawn, and re-asserting any of them is the main way to waste this session.

## Before anything else

Run `uptime` and `ps -eo pid,etime,%cpu,rss,command | grep '[.]venv/bin/python3'`.
`fastdk_benchmark.py` (PID 87926) is another session's job, has run 12+ hours,
and is the memory risk on this box; swap has been tight. Launch nothing heavy
until you have looked. Several sessions are active in this directory — run
`git status` before staging and **stage files by name, never `-A` or a
directory**.

## Verified state — do not redo

- SAT exclusion grid **complete and all-UNSAT through `n=30`** (six cells:
  `r in {0,1,2}` x `c in {2,3}`; the `r=0` pair is in
  `rw_sat_n30_20260903.log`, NOT the four `gap_30_*` logs). `n=31` has never
  been solved. No runtime estimate for `n=31` is supportable: per-cell
  `n=29 -> n=30` ratios ranged 0.88x to 12.55x.
- P1 (`k_dep = floor(n/2) - 2`) is **falsified exactly**; the light-cone story
  is a scale, not a formula.
- `H(2,w) >= w`, so exhaustive-in-`w` SAT/SMT cannot close this.
- Per-step domination is **dead three ways**: entrywise, weighted for *every*
  weight vector, and at every population floor tested (violations at `S_k` up
  to 255; LP optimum 0.5611 even with a floor of 30).
- The spectral/De Bruijn route is R7's own machinery and is closed
  (`PATH.md:587` "state-count wall plus the free-boundary escape";
  `MEMO-SPECTRAL-BOUND-CANNOT-CLOSE.md`).
- Rule 30 is the unique **quiescent left-permutive** ECA with `q < 1/(2 phi)`;
  the `phi/4` route passes the Rule 90 filter via the OR's 1:3 split.

## Your task, in priority order

**1. The product/geometric-mean bound — the main event.**
Per-step domination is *sufficient but not necessary* and is dead. The
induction actually needs `S_need / S_0 < 2^-n`, i.e. a bound on
`prod_k ratio_k`, equivalently a geometric mean below `1/phi = 0.618`. The
aggregate rate converges to `phi/4 = 0.4045` with real margin even though
individual depth ratios exceed 0.5.

Preregister before running, with a kill condition that can fire on a plausible
negative. Concretely:
  - Measure the geometric mean of `ratio_k` over `k = 0..deepest`, per `(n,c)`,
    for every `n` you can compute exhaustively. Report the **max over `(n,c)`**,
    not the mean, and the trend in `n`.
  - Kill condition: if the max geometric mean over `(n,c)` exceeds `1/phi` at
    any `n`, or trends upward in `n`, the product form is dead too — say so
    plainly and stop.
  - `domination_test.py` already builds the exact survivor tree from the real
    `literal_extension`; extend it rather than writing a new tree walker.
    It takes `--min-n/--max-n/--min-count`. `n=10..16` takes ~90 s.

**2. R1-A8** — the general-finite-row form of the zero-set obligation. The
driven-RHP evidence shows a periodic `c` does NOT force `r|Z` periodic, so local
forcing is dead; the open question is whether diagram-global consistency
restores it. **Check `r1-zero-set-attack/` and `p1-seam-cegis/` first** — another
session created them and may already be on this.

**3. A12** — audit `uc/r1-r1zero/comoving_columns_T32768.log`, the last
unaudited artefact in that directory.

**4. E1-E5** — the extinction margin, the concurrent session's lead. Verify from
`literal_extension` directly, do not relay. E4 (excluding the max-survival
family by an exact argument) is the one that could become a theorem fragment.

## Working discipline (non-negotiable)

- No claim before the curve. Preregister each comparative experiment with a kill
  condition that can actually fire.
- **Re-verify any fact you are about to repeat from a document, handoff, or
  subagent, against the code, and say that you did.** Seven claims were
  committed and withdrawn on 2026-09-05 alone; every one was caught by opening
  the file.
- Before reporting a number, state what a disconfirming version of the test
  looks like and confirm this isn't it. The small-`S_k`-tail error came from
  reading a ratio-sorted top-8 list and never asking what it excluded.
- Label validation as validation. Confirming a proved lemma numerically is
  worth doing and is not a discovery.
- Use the REAL functions (`literal_extension`, `psi_kernel.Endpoint`,
  `rw_sat.encode`), never a reimplementation.
- Check `Grep`/`Glob` and the existing scripts before writing a new one. A
  finite-window spectral automaton already existed in
  `verify_survivor_decay_markov.py` and was rebuilt from scratch this session.

## Do NOT

- Do not build another De Bruijn / window / transfer-matrix automaton.
- Do not use `lambda < 2` as a criterion (`phi = 1.618 < 2`, it cannot fail);
  a count needs `lambda < 1`, i.e. `rho < 1/2`.
- Do not extend the `H(p,w)` table to `w = 9,10,11`.
- Do not spend compute on R7 mode (i).
- Do not launch `n=31` unless explicitly asked; it buys one more `p=2` zero on
  a rung that does not close Problem 1.
- Do not send the Kari email or touch arXiv.
- Do not cite `lhp_lock_search`'s zero-lock result as an exclusion.

Python: `env PYTHONPATH=. /Volumes/A/researchpapers/.venv/bin/python3`, run from
the project directory.

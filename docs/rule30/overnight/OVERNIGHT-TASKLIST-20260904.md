# Overnight task list, 2026-09-04/05

Coordinator-tracked (no TaskCreate available this session). Status as of
launch; update as tracks report back.

## Running
1. **[running]** Push `gamma(n)` computation to largest feasible n —
   background `fastdk_benchmark.py` in `experiments/rule30/p1-period2-invariant/`,
   watched via a persistent Monitor on `fastdk_benchmark_20260904.log`.
2. **[running]** Attempt an inductive proof that `gamma(n) >= 1` for all n,
   or find a counterexample — subagent, writes
   `RESULTS-GAMMA-PROOF-ATTEMPT.md` in the same directory.
3. **[running]** Survey literature/state-of-the-art on Rule 30 P1
   specifically (rule30prize.org, Wolfram Physics Project, arXiv,
   symbolic-dynamics/automatic-sequence aperiodicity techniques) —
   researcher subagent, report only (no file write in repo).
4. **[running]** Orient on the existing P1/P2/P3 attack history in
   `docs/rule30/` and `experiments/rule30/` (START-HERE.md,
   OVERNIGHT-PROMPT.md, FACT-INDEX.md, PATH.md) before launching more
   tracks — fork, report only.

## (4) returned — superseded the blind P2/P3/general-P1 expansion plan

Orientation fork confirmed: period-2 (tonight's whole thread) IS the
recognized live internal edge of the P1 reduction chain per `PATH.md`, not
a bespoke detour — no need for a separate "is this legitimate" track.

Literature survey (independent, real citations) found something more
valuable than a generic P2/P3 fan-out: **Kopra (PhD thesis 2019 + TCS 946
(2023) 113668, arXiv:2202.13809) proved Rule 30's WIDTH-2 column is never
eventually periodic** via a Morse-Hedlund word-complexity argument, and
explicitly left WIDTH-1 (the actual center column) open as his own
Problem 3.10/4.8 — stating his technique is *provably* blocked from
reaching width 1 (a Rule-90 counterexample kills the general lemma).
Zero citations of this paper since 2023. This is the sharpest, most
specific unexploited gap surfaced all night.

5. **[done]** Deep-dive: got the EXACT mechanism of the Rule-90
   obstruction to Kopra's width-1 extension (structural, not
   quantitative — Rule 90 is also "rapidly left expansive," genuinely
   has an eventually-periodic width-1 column, so no strengthening of
   Kopra's general lemma to width 1 can be true). Confirmed: PT2/DLP
   (period-2 machinery) is genuinely orthogonal to Kopra's technique —
   no forced connection is real, don't manufacture one. BUT surfaced a
   real, higher-leverage target: `PATH.md`'s own **R1 route** — does
   "center column eventually periodic" force "right-neighbor column
   restricted to `{c_t=0}` eventually periodic"? If yes, contradicts
   Kopra's real published width-2 theorem directly, closing P1 outright.
   General in period, not period-2-specific, already pre-registered with
   a kill condition, existing tooling (`inverse_trace_probe.py`, the pin
   identity) already built toward it.
5b. **[running]** Attack the R1 kill condition directly — subagent,
   working in a new isolated directory
   `experiments/rule30/r1-zero-set-attack/` (created fresh to avoid any
   conflict with the period-2/gamma(n) work still running elsewhere).
   This supersedes the generic P2/P3/general-P1 expansion below (kept for
   the record, not being launched):
   - ~~5b. Fresh P2 (density 1/2) track~~ — deprioritized, not launched.
   - ~~5c. Fresh P3 (Omega(n) lower bound) track~~ — deprioritized, not
     launched. Published state of the art (per the literature survey):
     only upper bounds exist (O(n^2), O(n^2/log n)); no nontrivial lower
     bound published anywhere. Worth a track eventually, not tonight.
   - ~~5d. General (all-period) P1 track~~ — deprioritized: the literature
     survey's read is that period-specific work (what tonight's thread
     does) isn't obviously a stepping stone to general P1 unless it
     generalizes past period 2, which is itself now an open question
     worth asking once the Kopra-gap deep-dive returns.
6. `OVERNIGHT-PROMPT.md` is a ready-made, ALREADY-EXECUTED protocol from
   a prior session — not a template to blindly rerun. It hard-fences work
   to `experiments/overnight-arms/`, `docs/rule30/overnight/`,
   `runs/overnight/` and explicitly forbids touching `experiments/rule30/`,
   `docs/rule30/*.md`, `runs/alt-trace-automaton/` (another session marked
   those active). Its fencing CONVENTION (disjoint directories per
   session, explicit "active elsewhere" markers) is worth reusing for any
   new track, even though its specific content is already spent.
7. Named killed approaches (do not relaunch): P1 — larger finite-period
   SAT grids, fixed-depth ladders, generic left-permutive arguments,
   bounded adjacent-column prediction, support-width descent, periodic-
   mask contraction, local additive rankings, plus 9 named obstructions
   A-I in `PATH.md`/`FACT-INDEX.md`. P2 — uniform Bernoulli/a.e. density
   1/2 (misses the lone-seed case), literal local additive conservation
   (killed through width 12), orbit-closure route (flagged as likely
   *stronger* than P2, not a shortcut to it). P3 — literal Hashlife
   shortcut (proven superlinear, not actually a shortcut), inferring a
   lower bound from ANF degree/proof size/derivation-system size/fitted
   runtime exponent (all explicitly invalid inference patterns here).

## Standing / ongoing (not track-specific)
9. Reconcile tonight's `p1-period2-invariant` period-2 work with the
   wider `PROOF-STATE-CAPSULE.md`/`PATH.md` narrative once orientation
   data is in — without clobbering concurrent sessions' edits.
10. Watch `fastdk_benchmark_20260904.log`; fold new n values into
    `RESULTS-KSTAR-GAMMA-EXTENDED.md` as they land.
11. Check `ps aux` periodically for other concurrent sessions touching
    the same files before any shared-doc edit (known risk this project
    has hit before — see project memory on concurrent sessions).
12. When (2) reports, re-verify any claimed induction step against the
    actual code before trusting it — do not relay a subagent's proof
    claim as fact without independent spot-checking.
13. When (3) reports, use it to recalibrate/redirect tracks 5-7 — may
    kill some before they're launched if the literature already rules
    a specific angle out.
14. If (3) surfaces a specific promising external technique (automatic
    sequences, substitution systems, transducer theory), spawn a
    dedicated track applying it directly to Rule 30's center column.
15. Do NOT draft or send anything toward arXiv/email without explicit
    user approval — earlier session guidance flagged this explicitly.
16. Before any BACKLOG.md/PATH.md edit, re-read the file (multiple
    concurrent sessions are editing it) rather than editing blind.
17. Prepare a single consolidated morning summary (proven / falsified /
    open, per problem) written for someone with zero overnight context.
18. If any track finds a genuine counterexample or contradiction to an
    already-recorded result, stop, flag as highest priority, verify
    extremely carefully before reporting (this would be huge either way).
19. Manage subagent lifecycle actively: stop any subagent caught polling
    uselessly (happened twice already tonight with the k_star agent),
    resume/redirect the ones that need fresh data instead of new spawns.
20. Sanity-check every subagent's claimed file writes (stat the file)
    before repeating its claim, per this session's own standing practice.
21. Keep rough track of aggregate CPU/background-job load across all
    parallel overnight processes so one runaway computation doesn't
    starve the others on shared cores.
22. At wake-up, produce one clear "what changed overnight" diff against
    this list — done/still-open/killed — not a raw transcript dump.

## Explicit non-goals for tonight
- Not attempting to fully solve P1, P2, or P3 in the prize sense — these
  are open problems; the realistic goal is credible partial progress,
  correctly calibrated, not a claimed solution.
- Not publishing/emailing/timestamping anything without the user's
  explicit go-ahead.

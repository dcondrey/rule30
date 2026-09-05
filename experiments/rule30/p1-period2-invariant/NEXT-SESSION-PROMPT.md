# Prompt for the next session (copy everything below the line)

---

You are resuming the Rule 30 period-2-exclusion research project. Working
directory:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant`

Read `OVERNIGHT-HANDOFF-20260904.md` and
`PREREGISTRATION-OVERNIGHT-EXTENSION.md` first. Do not re-derive anything
below; it is all verified and committed.

## Hard reality about "run overnight"

You cannot stay alive for 10 hours. Your session ends when you stop
producing output. The ONLY work that survives is:

- detached processes (`nohup env PYTHONPATH=. /Volumes/A/researchpapers/.venv/bin/python3 SCRIPT ... > LOG 2>&1 &`)
- files and commits you write before stopping

So your job is: **build the task list, write the scripts, LAUNCH the long
jobs detached, commit, and write a handoff.** Do not attempt to babysit
jobs by polling. Do not use `sleep` loops to stay awake. Front-load the
launching; put the analysis instructions in the handoff for whoever reads
the logs next.

## Machine limits (respect these)

10 cores. As of the last check there were already ~8 CPU-bound processes
(4 SAT `rw_sat_gap_fill_one.py 30 *` jobs, 4 `overnight_census.py`
streams). Load average was 26. **Do not launch more than ~4 additional
concurrent jobs**, and prefer long sequential streams over wide fan-out.
~1.7 GB free RAM; this machine has a documented history of jetsam kills
from runaway python, so stream counts, never store per-word data.

Python is `uv run python` or `/Volumes/A/researchpapers/.venv/bin/python3`,
always with `PYTHONPATH=.` from the project directory.

## State of play — verified, do not redo

**SAT.** Complete UNSAT grid through `n=29`, no gaps (last cell
`n=29,r=2,c=3` returned UNSAT: 29473 vars, 91524 clauses, 9440.7 s). Four
`n=30` instances still running; logs `uc/r1-skeptic/gap_30_*.log` are empty
until they finish. **Do not claim n=30 until those files are non-empty.**

**Census.** `|H_r(n)| = 0` exactly for all `n <= 21`, every `r in {0,1,2}`,
both `c in {2,3}`. (Through 16 by the concurrent session; 17-21 by the
overnight run.)

**D_k** = distinct surviving continuation prefixes. Verified by two
independent forcing rules (`literal_extension` edge-forcing vs
`forced_orbit` H-bit forcing) — identical at every `n` tested.

**The light-cone departure "law" (P1) is FALSIFIED as an exact formula.**
`D_k` tracks the hard-core counts `2,3,5,8,13,21,34,55,89,...` exactly,
then departs at `k_dep`. The registered prediction was
`k_dep = floor(n/2) - 2`. Full data:

```
n         10  12   14  16  17  18  19  20  21
k_dep      4  4/5   5   6   6   7   7   7   8
floor(n/2)-2  3   4    5   6   6   7   7   8   8
```

It fails at `n=10` (off by one high), at `n=20` (off by one low), and at
`n=12` it is not even a function of `n`: the two tails disagree (`k_dep=4`
at `c=3`, `5` at `c=2`), so no formula in `n` alone can be correct there.
The increments land at `n=18` and `n=21` — runs of length 2, then 3, then
1 — which is not `floor(n/2)` behaviour.

**Methodological note, and the reason this is stated so bluntly:** the
original preregistration scored P1 as passing if `|k_dep - predicted| <= 1`.
That tolerance was a design error — it made the prediction effectively
unfalsifiable, and it caused a genuine disagreement at `n=20` to be logged
as "OK". Mathematics here is exact: `D_k` is an exact integer computed by
exhaustive enumeration, with no sampling and no noise. **Do not carry
tolerances on integer-valued structural predictions.** Either find an exact
law that reproduces every value above including the `n=12` tail split, or
state plainly that no exact law is known and that the light-cone argument
supplies only a heuristic scale (~`n/2`), not a formula.

Task: with `n=22,23,24` data, either (a) produce an exact law and verify it
against every `n` in the table above, or (b) record P1 as falsified and
demote the light-cone story to a heuristic in
`RESULTS-DISTINCT-CONTINUATION-COUNT.md`, which currently overstates it.

**Extinction margin** = `(n+2) - max_survival_row`. This is the strongest
open lead and it is the CONCURRENT SESSION's idea, not ours. Measured:
`7,5,6,8,8,8` (`n=10..18`, theirs) and `8/9, 8/9, 10/8, 11/8, 10/7` for
`n=17..21` (`c=2`/`c=3`, ours). No decline toward zero; minimum so far is
5 at `n=12`. If bounded below by any positive constant for all `n`, then
`H_r(n)=0` follows directly with no statistics.

**phi/4 null model.** Per-row survival matches "forced symbol uniform over
4 states, subject only to hard-core no-11"; that transfer matrix
`[[0,1/4],[1/4,1/4]]` has leading eigenvalue exactly `phi/4 = 0.404508`.
Uniformity of the forced symbol verified: max deviation from 0.25 is 0.017
(n=12), 0.006 (n=14), 0.005 (n=16).

**13/32** is exact at every `n>=3` and is EXPLAINED: the deepest diagonal
value is exactly uniform on the 4 states at every `n`, because every
four-symbol action is a permutation generating D8 and permutations preserve
uniform measure. It is a consequence of bijectivity, NOT a new invariant,
and it is NOT `phi/4` (0.40625 vs 0.404508).

## Retracted today — do not resurrect

1. **"Psi_n vs H_r(n) naming collision" — FALSE, withdrawn.** The two
   constructions define the same survivor population (0 death-level
   mismatches over 7168 words). The error was comparing
   `literal_extension`'s 4-valued *edge* output against `forced_orbit`'s
   binary *source symbol* output elementwise — different types. `BACKLOG.md`
   section 17 carries the retraction.
2. **"Three independent codings converge on 0.4"** — dropped. They are
   three codings of ONE process.
3. **"D_k is Fibonacci 2,3,5,8,13,21, surjective for ~5 rows"** — true only
   at `n=16`; the phase length grows as `~n/2-2`.
4. **"32/32 complete branching"** — appears in no file; unverified
   inheritance from a chat summary. Do not cite without recomputing.

The common failure mode in all four: generalizing from the first case
examined, then "verifying" with a method that could not separate the
hypotheses. **Before asserting any pattern, check it at 3+ values of the
parameter and state what a disconfirming result would look like.**

## Working discipline (non-negotiable)

- Research mode: no claim before the curve. Preregister each experiment
  with a kill condition that can fire on a plausible negative, BEFORE
  running it.
- Verify, never relay. If a subagent reports a number, re-derive it
  yourself against the real code before repeating it. If a prior document
  states a fact, re-check it — several were wrong today.
- Use the REAL functions (`literal_extension`, `psi_kernel.Endpoint`),
  never a reimplementation.
- Report negative results as plainly as positive ones. An honest kill is
  worth more than a survived hypothesis.
- Commit each logical unit with the correction history intact; never
  silently edit away a wrong claim.

## A concurrent session is active in this directory

It owns `rw_population_h.py`, `RESULTS-EXTINCTION-MARGIN.md`,
`RESULTS-TRANSFER-DOMINATION-CHECK.md`,
`RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`, and the `fib_absent_*` files.
**Run `git status` and `ps` before staging anything**; stage files by name,
never `git add -A` or a directory sweep. Do not edit its files. If you need
to correct something in them, write your finding in your own file and note
the disagreement.

## READ THIS BEFORE PRIORITISING: what this project is actually for

Everything in this directory — PT2, RW, `H_r(n)`, `D_k`, the SAT grid — is
the **`p=2` rung** of the R1..R7 register of direct routes to Problem 1
(`docs/rule30/PATH.md`). Their status:

| route | status |
|---|---|
| **R1** zero-set obligation | **OPEN — the only open route** |
| R2 cascade descent | KILLED (determination density decays, `O(log t)` reach) |
| R3 bounded-depth pin bootstrap | KILLED (run-of-ones wedge) |
| R4 right-boundary anchoring | KILLED (`O(log t)` reach) |
| R5 left permutivity/expansivity alone | KILLED (Rule 90 filter) |
| R6 Kolmogorov/entropy framings | KILLED (three independent ways) |
| R7 omega-automata periodicity ladder | STALLED; **mode (i) provably dead**, mode (ii) untouched |

**The uncomfortable fact:** PATH.md line 933 records that no per-period
exclusion theorem for the Rule 30 centre column exists "not even for
`p=2`", and that this is exactly R7. So our whole `p=2` programme is one
rung of a ladder that needs one theorem per period `p` — infinitely many.
Completing it does **not** close Problem 1. R7's mode (i) is closed by a
*proved* limitation theorem (the phase slip extends to a full half-plane;
`plain_{R,k}(w)` nonempty for every `R,k,w`, so mode (i) can never return
EMPTY at any depth), and the blocker is a state-count wall, not compute —
do not throw CPU at it.

**Why R1 is different, and verified here.** R1 assumes, for contradiction,
that the centre column `c` is eventually periodic, and needs only ONE more
column (`-1`) to be eventually periodic too — which hands the contradiction
to Jen 1990 Prop. 3 / Kopra Thm 3.5 (width-two column pairs of Rule 30 from
a finite seed are never eventually periodic). One theorem, not a ladder.

The pin does half of it for free. From `c_{t+1} = l_t XOR (c_t OR r_t)`:

```
c_t = 1  ->  OR saturates  ->  l_t = NOT c_{t+1}        (determined by c alone)
c_t = 0  ->  OR collapses  ->  l_t = c_{t+1} XOR r_t    (needs r)
```

**Verified in this session: 0 violations of both identities over 299 steps
of real Rule 30.** So the entire remaining obligation localises to: *is `r`
eventually periodic on the zero-set `{c_t = 0}`* — one column, half the
timeline.

**Hard constraint on any R1 attempt:** it cannot be rule-generic. Rule 90's
centre column is eventually periodic (identically 0 after `t=0`) while its
neighbour on that zero-set has `r_t = 1` iff `t = 2^j - 1` — aperiodic. So
the implication is outright FALSE for Rule 90, and any valid proof must use
Rule 30's OR-nonlinearity specifically. Arguments built on the pin pass this
filter by construction; arguments built on permutivity/expansivity alone do
not (that is exactly how R5 died). **Apply the Rule 90 filter to any
candidate R1 argument before spending compute on it.**

Given this, weight R1-relevant tasks above accumulating more `p=2` census
zeros. Extending the census from `n=21` to `n=26` is six more zeros on a
rung that does not close the problem.

## Your task now

Build a task list of **at least 30 concrete tasks** using
TaskCreate/TaskUpdate (load them first with
`ToolSearch({query: "select:TaskCreate,TaskUpdate,TaskList"})` — called
blind they fail on the old shape). Then work through as many as possible,
prioritizing (a) launching long detached computations early so they run
while you do cheap work, and (b) tasks whose result would change what we
believe, over tasks that just accumulate more zeros.

Seed list — extend, reorder, and add your own; do not treat it as complete:

**Long compute — launch these FIRST, detached**
1. Extend the census to `n=25,26` (streams for `n=23,24` may still be running; check first).
2. Extend the `D_k`/margin census on the `r=1` and `r=2` continuations specifically at high `n`.
3. Launch `n=31` SAT once any `n=30` cell returns, one instance at a time.
4. Measure UNSAT core size vs `n` on the SAT instances (`L10-SAT-CORE-SCALING`, currently deferred in BACKLOG).

**Score the frozen predictions**
5. Score P1 (`k_dep` vs `floor(n/2)-2`) at `n=22,23,24`; declare it falsified if any deviates by 2+.
6. Fit `k_dep(n)` across ALL data `n=10..24` — is it really `n/2-2`, or `n/3+c`, or something else? Report the best fit and its residuals.
7. Score P4 (post-departure geometric mean vs `1/phi=0.618`); the `c=3` series was creeping up (0.427, 0.395, 0.530, 0.569) — is it crossing?
8. Score P3 (extinction margin) at every new `n`; report the running minimum, not the mean.

**Test the light-cone explanation directly (not via D_k)**
9. Measure directly how many source coordinates determine the continuation prefix of length `k` (vary one source symbol at a time, record which prefixes change). Compare against the proved memory law `k_seed(L)=ceil((L+1)/2)`.
10. Test whether the departure point coincides with where that dependency window saturates `n`.
11. Quantify which source positions are free — the leading symbols are known free; find the exact boundary as a function of `n` and `k`.

**Extinction margin (strongest lead — verify, don't assume)**
12. Independently re-derive the concurrent session's margin numbers for `n=10..18` from `literal_extension` directly.
13. Read `RESULTS-EXTINCTION-MARGIN.md` and audit every numeric claim in it against the code.
14. Extract the actual max-survival words at each `n`. Are they a structured family (periodic, checkerboard, near-constant)?
15. If they are structured, test whether that family can be excluded by a separate exact argument — that would be a real theorem fragment.
16. Test whether the margin is tail-dependent in a systematic way (`c=2` is rising, `c=3` is flat — why?).

**The distinct-continuation object**
17. Measure the multiplicity distribution (words per distinct continuation) as a function of `n`; is the mean multiplicity growing like `2^n/D`?
18. Check whether `D_k`'s peak location and height obey a law in `n` (peak grew ~1.17x per step, slower than `phi^(n/2)`).
19. Test whether the post-departure decline is better modelled by the null transfer matrix than the Fibonacci bound.

**Null model**
20. Extend the forced-symbol uniformity measurement to `n=18,20` — does the deviation keep shrinking?
21. Test whether the null model predicts the `D_k` peak position correctly (it predicts survival rate, not distinctness — check if it transfers).
22. Compute the exact null-model prediction for `D_k` and overlay it on measured `D_k`.

**Audit and consolidation**
23. Re-verify the `13/32` uniformity claim at `n=10,11,12` with exact rational arithmetic (currently verified `n=1..9`).
24. Grep the whole directory for any other claim citing "32/32 complete branching" and annotate it.
25. Cross-check `rw_population_h.forward_filter` against a third, independently written filter.
26. Audit `PROOF-STATE-CAPSULE.md` section 5 against current findings; flag anything now known false.
27. Update `BACKLOG.md` L11 with the overnight results (coordinate — the concurrent session also edits this row).

**Write-up**
28. Update `RESULTS-DISTINCT-CONTINUATION-COUNT.md` with `n=17..24` data and re-score its four checks.
29. Update `RESULTS-CROSS-METHOD-INVARIANT-AUDIT.md` if any constant moved.
30. Refresh `DRAFT-EMAIL-KARI.md` with the verified `n<=21` census range and the P1 result — **but do not send it**; it stays parked.
31. Write a fresh handoff (`OVERNIGHT-HANDOFF-<date>.md`) with a one-command way to read every log, the frozen predictions and their scores, and what to do next.

## Do not

- Do not send the Kari email or touch arXiv.
- Do not claim `n=30` SAT until its logs are non-empty.
- Do not `git add` a directory or use `-A`; a concurrent session is writing here.
- Do not launch more than ~4 additional concurrent CPU-bound jobs.
- Do not report a subagent's number without re-deriving it.
- Do not extend a census purely to collect more zeros when a falsifiable
  structural question is available instead.

## R1 task seeds (weight these highly — add to the 30)

32. Read `docs/rule30/PATH.md` R1 (around lines 215-240, 296-320, 1268-1290)
    and `RESULTS-eventual-period.md:52-55` in full. Do not re-derive the pin;
    it is verified (0 violations, 299 steps).
33. Inventory `uc/r1-r1zero/` — it already contains `comoving_columns.py`,
    `drive01_deep.py` (T=65536), `drive01_long.py` (T=524288),
    `driven_halfplane.py` and their logs. Establish what was actually run,
    what it showed, and what was left unfinished, BEFORE writing new code.
34. State the zero-set obligation as a precise, falsifiable proposition and
    build the smallest computational probe that could refute it: assume `c`
    periodic with period `p`, and test whether `r` restricted to
    `{c_t = 0}` is forced periodic. Start at small `p`.
35. Apply the Rule 90 filter to every candidate argument produced: if the
    argument would also prove the statement for Rule 90, it is wrong, since
    Rule 90 is an explicit counterexample (`r_t = 1` iff `t = 2^j - 1` on an
    identically-zero centre column). Record this check explicitly per
    argument; do not leave it implicit.
36. Check whether the `phi/4` / maximal-entropy machinery developed today
    says anything about the DENSITY of the zero-set `{c_t = 0}` — Problem 2
    (each colour equally often) is exactly a statement about that set, and
    the zero-set is also R1's domain. This is the one place today's work may
    connect to a prize problem other than through the dead ladder.
37. Do NOT spend compute on R7 mode (i); it is closed by a proved limitation
    theorem. If R7 is touched at all, it is mode (ii) only, and the blocker
    there is a state-count wall, not CPU.

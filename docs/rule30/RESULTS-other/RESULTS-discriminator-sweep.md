# Discriminator sweep on untested proposals: nothing new to retire

Date: 2026-09-09.

**Deliverable: a negative sweep result, reported precisely.** A systematic
search of the repo's backlogs, memos, and "next steps" sections for
proposed-but-untested *quantities* found no candidate that fits
`discriminator.py`'s drop-in signature (`fn(grid, B, W) -> float`, a
real-valued statistic of a window of the actual 2D space-time diagram) other
than the three already tested and killed in
[GEOMETRIC-TRIAGE.md](../../experiments/rule30/p_geometric_attack/GEOMETRIC-TRIAGE.md).
Every other "proposed, not started" item found operates on a *different
representation* -- forced-symbol sequences over abstract source words,
automaton/DFA states, frontier "anchored word" graphs -- not on windows of
the raw diagram, so per the task's own escape clause these are a different
category, not a discriminator failure. This is recorded so nobody re-derives
"but has anyone run the filter on X" for these specific items.

| Candidate | Proposed where | Ever tested? | Discriminator-applicable? | Verdict |
|---|---|---|---|---|
| S1 hyperbolic lightcone embedding | `p_geometric_attack` (Agent 1) | Yes | Yes | Already killed: `relAB` -> 0 as `1/W` (0.0021 at W=32 down to 0.0 at W=256, T=60 rerun below), `relAC` stays 1-3% |
| S2 multilinear-relaxation Jacobian | `p_geometric_attack` (Agent 2) | Yes | Yes | Already killed: `relAB` -> 0.0 by W=64, `relAC` stays 70-90% |
| S3 spectral dimension of Dirac operator | `p_geometric_attack` (Agent 3) | Yes | Yes | Already killed: `relAB` -> 0.0 by W=256, `relAC` stays 6-17% |
| `N_j` Myhill-Nerode quotient size (`MEMO-COUNTING-LINE-BOUNDED-QUOTIENT.md`) | `p1-period2-invariant` | Yes (own method) | **No** | Function of `psi_kernel.Endpoint` state over source words, not of a diagram window |
| `phi/4` decay-rate identification (`MEMO-PHI-OVER-4-FIRST-MOMENT.md`) | `p1-period2-invariant` | Yes (own method) | **No** | An eigenvalue of a De Bruijn transfer matrix on the hard-core language, not a diagram statistic |
| Minimal-counterexample "peel" descent (`MEMO-RW-DESCENT-EXPLORATION.md`) | `p1-period2-invariant` | Yes (own method, killed) | **No** | Operates on padded source-word coordinates, not a window of the diagram |
| Finite-width spectral/transfer-matrix bound for `H_r(n)=0` (`MEMO-SPECTRAL-BOUND-CANNOT-CLOSE.md`) | `p1-period2-invariant` | Yes (own method, killed: criterion is vacuous) | **No** | Same De Bruijn-matrix object as above |
| Pull-row alpha support / projected diagonal support / one-credit half-word recurrence (`EXPERIMENT-ATLAS.md` sec. 10, items 1-2) | `EXPERIMENT-ATLAS.md` | Partially, own methods | **No** | Proposed *lemmas* about a combinatorial support structure, not real-valued window statistics |
| Reversed-inverse-diagonal scale/gap vector for the coordinate-interval bound (`EXPERIMENT-ATLAS.md` sec. 10, item 3) | `EXPERIMENT-ATLAS.md` | No | **No** | Proof strategy, not a statistic; also not a function of a fixed-width window (explicitly scale/gap-dependent) |
| Peel-recursive interpolants vs. checked cores (`EXPERIMENT-ATLAS.md` sec. 10, item 4) | `EXPERIMENT-ATLAS.md` | No | **No** | Certificate-search proposal, not a statistic |
| Bounded-window / lexicographic-pair / ordinal-valued Lyapunov charges (`RESULTS-alt-trace-fiber.md`, "Still open within charges") | `RESULTS-alt-trace-fiber.md` | No | **No** | A charge is a potential function of the abstract `(O,P)` frontier-state pair used for a mortality descent, not a statistic of the raw diagram |
| Pushdown/context-free representation of the RW survivor language (`BACKLOG.md` sec. 18) | `p1-period2-invariant` BACKLOG | No | **No** | A language-class question about forced-symbol sequences, not a real-valued window statistic |
| ~19 other `BACKLOG.md` entries (sections 1-17, 19+) | `p1-period2-invariant` BACKLOG | Mostly yes, own methods | **No** | Sampled throughout; all concern the `psi_kernel`/`literal_extension`/`Endpoint` combinatorial formalism, none propose a function of a diagram window |
| 20 `PREREGISTRATION-*.md` files in `p1-period2-invariant/` with no name-matching `RESULTS-*.md` or `BACKLOG.md` mention found by a simple grep (listed in section 3) | `p1-period2-invariant` | Unknown by this sweep | **No** (same formalism) | Flagged as a possible follow-up audit, out of scope for the discriminator since none propose a diagram-window statistic either |

## 1. What the discriminator actually filters

`discriminator.py` takes a statistic `fn(grid, B, W)` and measures it on
three fields (`A` = true Rule 30, `B` = `A` with column 0 overwritten by a
period-2 word, `C` = true Rule 90), reporting `relAB` (should be `O(1/W)`
for anything the single-column-sensitivity filter kills) against `relAC`
(should stay large for anything that merely separates the two rules, per
`PATH.md` section 0.1). This only makes sense for a **function of a window
of the actual 2D space-time diagram**. Anything defined on a different
object -- a forced-symbol sequence over an abstract source word, a DFA
state, a De Bruijn transfer matrix, a Lyapunov charge on a frontier-state
pair -- is not a drop-in candidate, and running it through this harness
would require a from-scratch reduction to a diagram-window statistic, not a
one-function plug-in. The task explicitly anticipates this category and
asks that it be named rather than forced through the filter.

## 2. Reproduction of the already-tested three

Rerun for this report (`T=60`, matching the harness's own default range of
widths; full output in `experiments/rule30/discriminator-sweep/rerun-T60.json`):

```text
W=32:  S1 relAB=0.0021  relAC=0.033   S2 relAB=0.0016  relAC=0.90   S3 relAB=0.00070 relAC=0.17
W=64:  S1 relAB=0.00057 relAC=0.021   S2 relAB=0.0     relAC=0.79   S3 relAB=0.00032 relAC=0.12
W=128: S1 relAB=0.00011 relAC=0.018   S2 relAB=0.0     relAC=0.71   S3 relAB=0.00017 relAC=0.065
W=256: S1 relAB=0.0     relAC=0.026   S2 relAB=0.0     relAC=0.68   S3 relAB=0.0     relAC=0.069
```

Matches the qualitative pattern already on record in `GEOMETRIC-TRIAGE.md`:
all three `relAB` columns collapse toward 0 as `W` grows while `relAC` stays
large (6-90%), confirming the harness and the frozen result still agree.
No new statistic was added; this is a reproduction, not a discovery.

## 3. Grep-level orphan flag (not itself a discriminator finding)

A crude heuristic (does any `RESULTS-*.md` filename or file body in
`experiments/rule30/p1-period2-invariant/` contain the preregistration's own
name fragment) flagged 20 of the ~65 `PREREGISTRATION-*.md` files in that
directory as *possibly* never written up:

```
BITSLICED-SCALE-DERIVATIVE, BITSLICED-TWO-ROW-RANK, CUMULATIVE-GREEDY,
CUMULATIVE-SCALE-MATCHING, FOUR-ROW-TELESCOPE, MIXED-RUN-RETREAT-BUDGET,
ORDERED-SCALE-MATCHING, ORIGIN-PREFIX-HALL, PAS-SUFFIX-INTERPOLANT,
PHASE-GAP-COVER-PROOF, PHASE-GAP-RETREAT-COVER, RETREAT-BUDGET,
RIGHT-DIAGONAL-SUPPORT, RIGHT-ZERO-PREFIX-SELECTOR, SCALE-DERIVATIVE-RANK,
SCALE-HALVING-RECURRENCE, SCALE-PIVOT-SELECTOR, TWO-ENDED-DEFECT-CLOSURE,
UNRESTRICTED-DIAGONAL-SUPPORT, ZERO-PREFIX-SCALE-MATCHING
```

This is **not verified** -- the heuristic is a filename substring grep and
almost certainly has false positives (some of these are likely narrated in
`BACKLOG.md` prose under a different name, the normal pattern in that
directory). It is reported only as a pointer for a future dedicated audit
(closer to this batch's Task 6 than Task 7), and explicitly **not** run
through the discriminator, because -- like everything else in that
directory -- these preregistrations concern the `psi_kernel` combinatorial
formalism, not a real-valued function of a diagram window.

## 4. Reproduction

```bash
cd experiments/rule30/p_geometric_attack
python3 discriminator.py 60 > ../discriminator-sweep/rerun-T60.json
```

## 5. Scope and honesty notes

- **Nothing was retired that wasn't already retired.** The three geometric
  proposals were already dead per `GEOMETRIC-TRIAGE.md`; this sweep found no
  additional live candidate anywhere in the searched material.
- **The searched material was large but not exhaustive.** `BACKLOG.md`
  alone runs to 19+ sections and was sampled, not read line-by-line;
  `EXPERIMENT-ATLAS.md` section 10 and `RESULTS-alt-trace-fiber.md` were
  read in full. Other `RESULTS-*.md` "next steps" sections across the
  `docs/rule30/` tree were grepped for the keywords `propose`, `untested`,
  `not (yet) tested/run/measured`, `never tested/run` rather than read in
  full; a hit list is in the grep transcript, not reproduced verbatim here.
- **The category judgment ("not a drop-in statistic") is a claim about
  representation, checked against each item's own defining file, not an
  assumption.** Where a proposal's definition explicitly quantifies over
  scale/gap vectors or unbounded history rather than a fixed-width window
  (e.g. `EXPERIMENT-ATLAS.md` section 10 item 3), that is stated as the
  specific reason, not just asserted.
- **No claim is made about the 20 flagged orphan preregistrations beyond
  "flagged by a crude grep."** They were not read, not categorized beyond
  "same formalism as the rest of the directory," and not run through
  anything.

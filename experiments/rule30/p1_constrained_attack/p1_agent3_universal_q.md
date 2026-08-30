# Agent 3: Diff quantified over all q <= Q

**Verdict: a genuine new mode, correctly reasoned, calibrated, and measured
dead -- with a structural reason, not a compute limit.  My prior claim that
"no choice of q escapes the bounded wedge" was wrong: the conjunction is not
a choice of q.**

## Why the conjunction is strictly better than fixed q

Let `S(q)` be the ladder language with the `Diff_q` Buchi condition and
`S(1..Q)` the one requiring infinitely many diffs at **every** `q <= Q`.
Then `S(1..Q)` is a subset of `S(q)` for each `q <= Q`, so emptiness is
strictly easier to obtain.  The conclusion is correspondingly weaker but
still sufficient:

```text
S(1..Q) empty  =>  every admissible word has col_{-1} eventually periodic
                   with period <= Q for SOME q
               =>  col_{-1} and col_0 both eventually periodic
               =>  contradiction, Jen 1990 Prop. 3 / Kopra 2023 Thm 3.5
```

A disjunctive conclusion discharges Jen/Kopra exactly as a fixed-`q` one does.
That is the error in the earlier dismissal.

## Encoding

Exact `Q`-bit history of `col_{-1}` rather than the repo's guess-and-verify
gadget: cost `2^Q * Q` against `prod_{q<=Q} 2(2q+1)`, i.e. 64 against 15,120
at Q = 4, and the diff flags are computed exactly instead of guessed.
Generalized Buchi degeneralized by an accept index cycling `0..Q-1`, advancing
on the flag for `q = acc+1`, accept on wrap.  **The index advances only when
`phase is not None`**, so no run can earn acceptance on diffs observed before
the periodicity hypothesis is in force.

## Calibration (`run_calib.py`, `pin2_sound.log`)

* regression: the true lone-seed word is accepted at rule 30 and 90,
  `(R,k)` in {(1,1),(2,2),(3,2),(4,2)}, 0 mismatches;
* Q = 1 reproduces rung-0's fixed-`q=1` verdicts exactly (w=1 R=1 EMPTY,
  w=0 R=2 EMPTY, w=01 R=2 k=2 NONEMPTY);
* rule 30 `p = 1` stays EMPTY at Q = 2, 3, 4 (both tails);
* rule 90 `w = 0` stays NONEMPTY at Q = 1, 2, 3, 4 -- the section-0 control.
  **This control is pin-OFF only.**  The Q-conjunction by itself adds no
  rule-specific constraint, so Rule 90 survives it; but the headline table
  below is the pin-ON climb, and under the pin the true Rule 90 word is
  rejected and the control collapses to 3 states, EMPTY
  (`pin2_sound.log`).  See `p1_agent2_pincascade.md` for why that is by
  design and what it costs.  No result in the pin-ON table has a Rule 90
  control behind it.

## Result: NONEMPTY to Q = 14

`p = 2`, tail 01, R = 2, k = 2, full 1-pin on (`pin2_climb.log`):

| Q | 1 | 2 | 3 | 4 | 6 | 8 | 10 | 12 | 14 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| states | 199 | 211 | 361 | 718 | 2,850 | 11,392 | 45,481 | 182,589 | 735,328 |
| witness cycle length | 4 | 4 | 4 | 12 | 22 | 28 | 32 | 44 | 50 |

NONEMPTY at every Q, witness verified each time against the forward rule, the
full wedge, the pin identity, centre periodicity, and diffs at every `q <= Q`.
Without the pin the same climb runs to Q = 14 at 2,134,760 states, same
verdicts (`qclimb.log`).  All 69 primitive necklaces `p = 2..8` are NONEMPTY
at Q = 4 (`pin2_sweep.log`).

## Why it cannot close, stated as a lemma

**Lemma.** `S(1..Q)` is omega-regular, so if nonempty it contains an
ultimately periodic word `u v^omega`.  The window state of `u v^omega` is
eventually `|v|`-periodic and every column is a letter-to-letter delayed
function of it, so `col_{-1}` is eventually `|v|`-periodic.  A word in
`S(1..Q)` has infinitely many `q`-diffs for every `q <= Q`, so no `q <= Q` is
an eventual period of `col_{-1}`.  Hence `|v| > Q`.

**Corollary.** `S(1..Q)` is empty **iff** every admissible lasso has
`col_{-1}` eventual period at most `Q`.  The lasso cycle lengths available to
the search are bounded only by the state count `N(Q)`, and `N(Q)` is measured
to double per unit of `Q` (199 * 2^(Q-1) with the pin, 472 * 2^(Q-1)
without).  So the room to escape grows exponentially in `Q` while the
requirement grows linearly.

**And the corollary has a trap in it.**  `col_{-1}`'s eventual period is the
eventual cycle length of the *base* window state, which is at most the number
of reachable base window states `N_base(R,k)` -- a fixed finite number, not a
function of `Q` (472 at R=2, k=2 without the pin; at most 199 with it).  The
lemma forces every period to exceed `Q`.  So for `Q >= N_base`, `S(1..Q)` is
empty for automaton-theoretic reasons that have nothing to do with Rule 30,
and **an EMPTY verdict there proves nothing.**  Extrapolating the measured
escape (about `3.5 Q`) puts that threshold near `Q = 135` at R=2, k=2.  Any
future run climbing `Q` must check its verdict against `N_base` before
reading an EMPTY as a theorem.

The measured escape is linear and comfortable: the returned witness cycle
length tracks roughly `3.5 Q` (BFS-shortest through the accepting SCC, not
certified minimal), always above `Q`, never within orders of magnitude of
`N(Q)`.  **Raising `Q` is therefore not a route to EMPTY**, for the same
reason raising `R` and `k` was not: the constraint and the freedom grow
together.

## Scope

No `Thm(p)` for any `p >= 2`.  What is new and worth keeping: the conjunction
mode itself, its calibration, the exact-history encoding (240x cheaper than
the gadget product at Q = 4), and the lemma above, which converts "raise Q"
from an open option into a closed one.

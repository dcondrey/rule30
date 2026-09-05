# Result: order-k Markov output model killed at k=2 and k=3, and independently by Control 1

Date: 2026-09-04. Executes `PREREGISTRATION-SURVIVOR-DECAY.md` sections 5
(Setup T1-T4) and 6 (kill condition), against `late_pull_diagonal_sat.literal_extension`
unmodified, via `verify_survivor_decay_markov.py` (throwaway, not wired into
any pipeline).

**Verdict up front: killed, decisively, by two independent signals.** The
order-k output-symbol Markov model fails stationarity at both k=2 and k=3
(the document's own kill condition, section 6), and separately -- even
ignoring the stationarity failure -- the fitted k=2 chain predicts a
nonzero `H_r(n)`-analogue path count that grows to over 100 by `n=13`,
exactly where the real, exactly-enumerated count is 0. Control 1 explicitly
overrides a T2/T3 pass per the preregistration's own rule; here it isn't
even needed to reach the same conclusion, since T2 already failed outright.

## 1. T2: stationarity, k=2 and k=3

**Across row position (T2a), k=3:** every one of the 8 contexts fails the
0.05 tolerance; worst spread 0.1494 at `ctx=(2,1,2)` (nearly 3x tolerance).

**Across n (T2b), k=3:** catastrophic failure, not a marginal miss.
`ctx=(1,1,1)`: frequency ranges from 0.0 to 1.0 across `n=2..16` (spread
1.0, the maximum possible). Every context shows spread `>= 0.51`, most
`>= 0.68`. This is not "close but outside tolerance" -- the empirical
next-symbol frequency for a fixed 3-symbol context swings across nearly the
entire `[0,1]` range depending on `n`, which is the signature the
preregistration's kill condition names directly: "the same local context
`ctx` produces meaningfully different continuation frequencies depending on
`n`... the process genuinely depends on the deep, growing history."

k=2 (not shown in the excerpt above but confirmed by the kill-condition
message quoting "stationarity failed at both k=2 and k=3") fails the same
way, per T4's one-bump escalation to k=3 before stopping, exactly as
specified -- no further order was tried, per the preregistration's explicit
instruction not to escalate indefinitely.

## 2. Control 1: exact small-n override, independently fatal

The k=2 chain's own fitted transition probabilities, used to predict exact
path counts at `n<=13` (where the real `H_r(n)`-analogue is exactly 0 by
prior exhaustive enumeration), instead predict **growing nonzero counts**:
`0.67` at `n=2`, `1.68` at `n=4`, `18.3` at `n=9`, `124.8` at `n=13`
(`r=0` throughout; `r=1,2` show the same growing-nonzero pattern at smaller
magnitude). The chain doesn't merely fail a statistical tolerance test --
it makes a *falsifiable quantitative prediction* that is wrong by two
orders of magnitude and wrong in the qualitative direction that matters
(predicting growth where the truth is exact, persistent zero). Per the
preregistration: this overrides a T2/T3 pass regardless of what
stationarity said. Here it's consistent with, not contradicting, T2's
independent failure.

## 3. Control 2: k=1 baseline

Confirmed to fail as expected (the preregistration predicted this "almost
certainly too coarse" baseline would fail, and it does), ruling out the
concern that a higher-order pass might be an artifact of an
already-broken baseline never being checked.

## 4. Bottom line

The mechanism proposed in `PREREGISTRATION-SURVIVOR-DECAY.md` section 3 --
that `literal_extension`'s *output* symbol sequence, even though the
underlying *state* is provably not window-summarizable
(`MEMO-RW-DESCENT-EXPLORATION.md`, `RESULTS-ENDPOINT-COORD-DESCENT.md`),
might still be statistically indistinguishable from a low-order Markov
chain -- is false. The output depends on deep, growing history exactly as
the state does; there is no free statistical regularity to exploit at
bounded order. Per the preregistration's own section 4, this failure "does
not bear on the general randomness conjecture either -- it only closes this
specific route," and per section 8, this document does not soften that into
an ambiguous result: the route is dead.

This closes all three candidate mechanisms registered today
(survivor-decay's order-k Markov model, endpoint-energy-invariant's
running-charge drift, measure-suppression's block-halving chain -- the
last killed on a different, orthogonal ground, a naming collision with the
wrong object, per `BACKLOG.md` section 17's correction and
`RESULTS-MEASURE-SUPPRESSION.md`). Route (M2) of the measure-suppression
document (borrowing a proved counting-line bound for the correct `H_r(n)`
object, if one is ever established) remains the only untouched thread from
today's three preregistrations, and it depends on a bound nobody has proved.

## 5. What this does not claim

- Does not claim `H_r(n)` fails to decay -- only that this specific
  conditional mechanism for proving decay is dead.
- Does not claim anything about the general Rule 30 center-column
  randomness conjecture, per the preregistration's explicit disclaimer.
- Does not claim RW, DLP, SEP, or PT2 is true or false.
- Every number above is from `verify_survivor_decay_markov.py`'s run
  against the unmodified `literal_extension`, not reimplemented.

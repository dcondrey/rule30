# Charge inequality (12): the run steps can be matched injectively to source `2`s they depend on, but by no fixed positional rule

Date: 2026-09-16. Scripts and logs in `charge-injection/` (`tight_words.py`,
`injection_probe.py`, `injection_rule.py`). Kernel `psi_kernel.py` and
`seam_history_inheritance.run`. No pre-registration; a probe of the proof
shape the capsule names in section 6.4 ("a phase-decorated injection into the
`n` ordered source tokens").

**`[C]` For every hard-core source `W` of length `n = 8..16` and tail `c = 2`,
the bipartite graph joining forced step `j` (`j < run_c(W)`) to the positions
`i` with `W_i = 2` whose flip changes the cut cell at step `j` (the forced
prefix held fixed) has a matching that saturates the steps: the run steps
can be charged injectively to distinct `2`s they depend on, which is
inequality (12) of `RESULTS-EVENTUAL-CONSTANT-TAIL.md` with zero slack on
this range and a structural reason for it. For `c = 3` the matching falls
short of the run by 1, 3, 1 at `n = 8, 9, 10` and by 0 at `n = 11..16`, the
shortfall never exceeding the `+3` of (12). No fixed positional rule is the
injection: charging step `j` to the `(j+1)`-th `2` from the end of `W` hits a
dependency for 56 to 84 percent of steps, within a window of three ranks for
99 to 100 percent, and fails outright on words such as `12212122221` (step
0) and `12121222222212` (step 4). The dependency sets are large (mean about
`0.6 n`, minimum 2 to 5) and include the last source symbol in about three
quarters of the steps. The tight words of (12) at `c = 2` are one at `n = 17`,
`1 22 (12)^7` (run 10, nine `2`s); at `c = 3` within 2 of the bound only at
`n = 9` (`121222122` and three relatives, run 8). So the injection exists
combinatorially on every word checked and is not positional; a proof of (12)
would have to construct it from the dependency structure, step by step.**

## 1. Objects

`run_c(W)` is the wide-grammar constant-cut run of `seam_history_inheritance`
(`maxrows n + 4`), `Q` its forced symbols. `cut_j(W')` is
`Endpoint(W' Q[:j]).peek(Q[j]).diagonal[n]`; `D_j(W) = {i : cut_j(W with W_i
flipped) != c}`. The matching is between steps `0..run-1` and
`{i in D_j : W_i = 2}`, computed by augmenting paths. Rule `R1(k)`: some `2`
among the ranks `j+1 .. j+1+k` from the end of `W` lies in `D_j`; `R2`: the
`(j+1)`-th `2` from the start lies in `D_j`.

## 2. Results

Minimum over words of `matching - run` (`injection_probe_n8-16.log`):

| `n` | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|
| `c = 2` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `c = 3` | -1 | -3 | -1 | 0 | 0 | 0 | 0 | 0 | 0 |

The `c = 3` deficits: `12222212` (run 1, its one step depends on no `2`),
`122222122` (run 8, matching 5), `1222212212` (run 6, matching 5). Mean
`|D_j|` grows from 4.6 at `n = 8` to 9.9 at `n = 16`.

Rule hits (`injection_rule_n8-15.log`), fraction of steps: `R1(0)` 0.67 to
0.84 (`c = 2`), 0.56 to 0.84 (`c = 3`); `R1(3)` 0.988 to 1.000 (`c = 2`),
0.768 to 1.000 (`c = 3`); `R2` 0.23 to 0.45. Last source symbol in `D_j`:
0.68 to 0.83. Failures of `R1(3)` at `c = 2`: `12212122221` step 0 (`D_0 =
{2,3,4,5,10}`, the four last `2`s at 9, 8, 7, 6 all absent), `12122122121222`
step 0, `121222121222222` step 0; at `c = 3`: `121222122` step 5,
`1222212212` step 3, `12121222222212` step 4.

Tight words (`tight_words_n8-20.log`): at `c = 2` slack 0 only at `n = 17`,
`12212121212121212`, forced `2122122121`; at `c = 3` slack at most 2 only at
`n = 9`.

Greedy rules (`greedy_rules.py`, log `greedy_rules_n8-14.log`): charging
step `j` to the oldest (smallest-index) unused `2` in `D_j` saturates every
word `n = 8..14` at `c = 2` and every word `n = 11..14` at `c = 3` (deficits
1, 3, 1 at `n = 8, 9, 10`, the same as the maximum matching); charging to the
newest unused `2` fails at `n = 14` (`c = 2`, deficit 1). On the tight word
`12212121212121212` the dependency sets are broad from step 1 on (steps 3
and 4 depend on every position from 2), the early defect at positions 1, 2
enters at step 1 and stays through step 6, and step 7 is the narrowest
(`2`-positions `{8, 10}` only).

Extended to `n = 15..18` (`greedy_rules_n8-18.log`): the oldest-unused rule
fails at `c = 2` by 3 at `n = 17` and by 1 at `n = 18` (the newest-unused
rule by the same amounts), and at `c = 3` by 1 at `n = 18` (newest) and 0
(oldest). Part of the `n = 17` deficit is forced: the tight word has ten
forced steps and nine `2`s, so no injection into `2`-tokens alone exists
there, and the `+[22 in W]` term of (12) is exactly the missing token. The
statement that survives is therefore: run steps inject into `2`-tokens plus
one token per `22` factor (and plus three at `c = 3`); the pure `2`-token
matching of section 2 is saturating only below the first tight length.
Recomputed later the same day (`RESULTS-CHARGE-INJECTION-TOKENS.md`): the maximum
matching at `n = 17` on the tight word is 8, so even with the `22` credit the injection
fails by 1, and at `n = 18` every word saturates (the greedy deficit of 1 there was an
artefact of the order). The "statement that survives" above is therefore false as a
matching statement.

## 3. Reading

Inequality (12) is the sharpest sufficient condition on record for `RW` on
narrow sources (`#2 <= 0.8 n` there), and it has been treated as a falsifier
target. This probe says what a proof would look like and what it would not:
the run steps do depend, collectively, on at least as many distinct `2`s as
there are steps (Hall's condition holds on every word to `n = 16` at
`c = 2`, and fails by at most the known slack at `c = 3`), but the assignment
is not "step `j` uses the `(j+1)`-th `2` from either end", nor any window of
three ranks. The dependency of a cut on the source is broad (most of the
source, and usually the last symbol), so the binding steps are the early
ones with small `D_j`. A proof would construct the injection greedily from
the dependency structure, which means understanding why each new forced step
reaches a `2` the earlier steps did not need; on the tight word `1 22 (12)^7`
every `2` is needed and the order of consumption is the object to read off.
`RW`, `SEP`, `PT2` untouched.

## 4. Scope

Finite: hard-core words `n <= 16` (matching), `n <= 15` (rules), `n <= 20`
(tight words), wide grammar, one implementation. `D_j` is a single-flip
dependency with the forced prefix held fixed, not a full Boolean dependency.

## 5. Reproduction

```sh
uv run --no-project python charge-injection/injection_probe.py 16   # 4 min
uv run --no-project python charge-injection/injection_rule.py 15    # 3 min
uv run --no-project python charge-injection/tight_words.py          # 2 min
```

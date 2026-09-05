# Rule 90 filter applied to this session's machinery, and what the ladder's 4x ratio is

Session 2026-09-05. Two questions answered: how the Fibonacci/fiber apparatus
maps to Rule 90, and whether the ladder automaton's state ratio approaching 4 is
a trigger, an oscillation, or something else.

## Part 1 — the Rule 90 filter, ingredient by ingredient

`f_30(l,c,r) = l XOR (c OR r)`, `f_90(l,c,r) = l XOR r`. The filter: Rule 90's
centre column from `{-1,1}` is identically 0 (eventually periodic) while
`r_t = 1` iff `t = 2^j - 1` (aperiodic), so R1's implication is FALSE for
Rule 90 and any rule-blind argument is wrong. Exhaustive check over all 8
neighbourhoods (`scratchpad/rule90_filter.py`):

| ingredient | what it rests on | rule 30 | rule 90 | verdict |
|---|---|---|---|---|
| hard-core counts, Fibonacci, `phi` | the no-`11` constraint only | — | — | **RULE-BLIND** |
| the vacuity bijection (free boundary) | left-permutivity | permutive | permutive | **RULE-BLIND** |
| `H(2,w) >= w` | left-permutivity | `H-w` in {1,2,3,5} | `H-w` in {1,3} | **RULE-BLIND** (measured) |
| the pin | the OR saturating at `c=1` | `c=1`: `f` independent of `r` — **yes** | `c=1`: **no** | **RULE 30 ONLY** |

So everything on the **Fibonacci half** of `|S_k| <= Fib(k+1) * max_fiber` is
rule-blind. Rule 90 has all of it. Any argument resting only on those
ingredients fails the filter by construction, which is the same verdict R5
already earned ("left permutivity/expansivity alone — KILLED (Rule 90 filter)").

## The `1/4` is exactly where Rule 30 differs from Rule 90

The unanticipated finding. Classify the four `(c,r)` pairs by the behaviour they
induce on `l`:

```
rule 30 (OR):   distinct l-behaviours = 2 over 4 pairs, split 1 : 3
rule 90 (XOR):  distinct l-behaviours = 2 over 4 pairs, split 2 : 2
```

Rule 30's `c OR r` is `0` for exactly one of four pairs; Rule 90's `r` is `0`
for two of four. **That 1:3 asymmetry is the source of the `1/4` in `phi/4`**,
and Rule 90's balanced 2:2 replaces it by `1/2`. Feeding each into the same null
matrix `M = [[0,q],[q,q]]`, whose leading eigenvalue is `q*phi`:

| rule | `q` | `lambda = q*phi` | `2*lambda` | conclusion |
|---|---|---|---|---|
| 30 | `1/4` (`P(c OR r = 0)`) | `phi/4 = 0.404508` | `0.809017` | `< 1` -> **extinction** |
| 90 | `1/2` (`P(r = 0)`) | `phi/2 = 0.809017` | `1.618034` | `> 1` -> **no extinction** |

**The same machinery gives extinction for Rule 30 and correctly refuses it for
Rule 90.** So the `phi/4` route **passes** the Rule 90 filter, and it passes for
the right reason: the discriminating quantity is the OR-nonlinearity, exactly as
required of any valid R1-adjacent argument.

This locates the difficulty precisely. Everything rule-blind (`phi`, the
Fibonacci factor, left-permutivity, the free-boundary escape) is the part that
was easy and proved nothing. Everything rule-specific (the `1/4`, the fiber
factor, the pin) is the part where every route failed. **The hard half and the
Rule-30-specific half are the same half** — which is what one should expect, and
is mild evidence the difficulty is real rather than an artefact of the encoding.

## Part 2 — the ladder automaton's ratio -> 4: saturation, not a trigger

`RESULTS-ladder-rung1.md:118-123` state counts, with the deficit from exact `4x`:

```
 R   states   ratio    s_R - 4*s_(R-1)   log4(states) - R
 1      428     -            -                3.371
 2     1445   3.3762      -267                3.248
 3     5574   3.8574      -206                3.222
 4    22087   3.9625      -209                3.215
 5    88136   3.9904      -212                3.214
 6   352329   3.9976      -215                3.213
```

**Not an oscillation.** The ratios increase monotonically and never cross 4; no
sign change, no periodicity.

**Not a trigger point.** Nothing happens *at* 4. Four is the trivial upper bound
— the full `(h,F)` alphabet — and the sequence approaches it from below and
stays under it. A trigger would require the ratio to reach or cross the value
and the behaviour to change there; instead the value is an asymptote that is
never attained.

**It is saturation, and "step counter" is the right reading.**
`log4(states) - R` converges to a constant `3.213`, i.e. `states_R ~ A * 4^R`:
the automaton stores exactly one 4-state cell per extra level and merges
essentially nothing. It is doing nothing but counting depth.

Sharper than the ratio: the **absolute** deficit `s_R - 4*s_(R-1)` is
**bounded** — `-267, -206, -209, -212, -215`, drifting about `-3` per step, not
growing. So the merging saves a *constant* number of states forever, never a
growing fraction. (Five differences from six data points; the `-3` drift is
reported as observed, not as a law.)

That is the state-count wall stated quantitatively, and it agrees with two
independent records: exact DFA minimization achieving **zero** collapse
(`RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md`, minimized sizes
`5, 17, 65, 257, 1025, 4097, 16385, 65537 = 4^(h+1)+1`), and the proved
`k_dia(L) = L` (`RESULTS-DIAGONAL-MEMORY.md`, "the anti-diagonal remembers every
symbol").

The visible merging at small `R` (deficit `-267`, ratio `3.376` at `R=2`) is a
finite-size effect and is where the pin's `1.9x-7.5x` state pruning lives —
a constant-factor saving, consistent with `PATH.md:304-306` recording that the
pin "prunes 58% and flips no verdict".

**Consequence:** there is no `R` at which the automaton starts compressing, so
there is no threshold worth running to. This is an independent argument for
`PATH.md:298-299`'s instruction not to re-run R7 at larger `R`, `k` or `Q`.

## Files

- `scratchpad/rule90_filter.py` — the ingredient-by-ingredient filter check.

# The 10/44 vs 0/44 flag is resolved: identity I does not hold across the driven pair

Answers the discrepancy raised in
`experiments/rule30/r1-zero-set-attack/RESULTS-R1-ZERO-SET-ATTACK.md` section 6,
which explicitly flagged it "for whoever owns `p1-period2-invariant/uc/r1-r1zero/`,
not resolved here". This directory owns it.

Date 2026-09-05. Script `identity_audit.py`, log `identity_audit_T4096.log`.

## The flag

`driven_halfplane_T4096.log` line 228 reports, over 44 (word, prefix) drives:

    RHP r|Z eventually periodic in 10/44 drives; LHP l eventually periodic in 0/44

The x = 0 instance of the rule,

    c_{t+1} = l_t XOR (c_t OR r_t)                                    (identity I)

was read as forcing `l` eventually periodic whenever `c` and `r` are, making
10/44 against 0/44 look inconsistent. Two candidate explanations were named
there (a period-bound accounting mismatch; an onset-detection artifact) and
neither was tested.

## Result

**Neither candidate explanation is needed. There is no inconsistency, because
identity I is not a property of the pair of sequences being compared.**

`driven_halfplane.py` runs two *separate* simulations. `driven_rhp` builds the
right half-plane `x >= 1` from the drive; `driven_lhp` builds the left half-plane
`x <= -1` from the same drive. Each writes `c_{t+1}` into its own `x = 0` slot by
fiat (`nxt = (nxt & ~1) | ct1` in both, `r1zero_lib.py`), discarding whatever the
rule would have produced there. The rule instance at `x = 0` -- the *only* thing
that couples `l` to `r` -- is therefore enforced in neither model. `l` and `r` as
measured come from two configurations that share a boundary word and nothing else.

Measured directly, all 44 drives, `T = 4096`:

| | value |
|---|---|
| drives satisfying identity I at every `t` | **0 / 44** |
| typical I-violation rate | ~2000 / 4096, i.e. ~50%, coin-flip |
| **control**: identity I on the true lone-seed diagram (`l`, `c`, `r` from one configuration) | **0 violations / 4096** |

The control is the point: identity I is exact where the three columns come from
one configuration, and is satisfied at chance rate where they do not. The
premise of the flag fails before either candidate explanation is reached.

## The length-matched column, which also rules out explanation 2

The original run compared `r|Z` (length `|Z|`) against `l` (length `T+1`), so an
onset-detection or detector-power artifact was a live worry. `l|Z` is
length-matched to `r|Z` and uses the identical `eventual_period` call:

    r|Z periodic 10/44      l|Z periodic 0/44      l periodic 0/44

`l|Z` is 0/44, exactly as `l` is. The 10-vs-0 split survives length-matching, so
it is not a detector-window artifact. It is what a comparison of two unrelated
objects looks like.

## What this does and does not settle

- **Settles**: the flagged discrepancy. `RESULTS-R1-ZERO-SET-ATTACK.md` section 6
  can be marked resolved, with its explanations 1 and 2 both unneeded rather than
  refuted -- they were never reached.
- **Does not settle**: anything about R1. The 10/44 figure is *not* thereby
  validated as evidence that a periodic `c` sometimes forces `r|Z` periodic in a
  real diagram; it is a statement about a driven model with an arbitrary clamp,
  and this audit shows that model is even less coupled to the real diagram than
  the flag assumed.
- **Reinforces, from a third angle**: the diagnosis already reached independently
  by `RESULTS-R1-ZERO-SET-INVENTORY.md` (simulation) and
  `RESULTS-R1-ZERO-SET-ATTACK.md` section 5 (automaton/census internals) -- only
  *global* consistency couples `l`, `c` and `r`. Here that is not an inference
  from a failure to force; it is the measured 0/44 vs 0-violation control above.

## Reproduction

```sh
cd experiments/rule30/p1-period2-invariant/uc/r1-r1zero
env PYTHONPATH=. /Volumes/A/researchpapers/.venv/bin/python3 identity_audit.py 4096 512
```

~20 s. Reuses `r1zero_lib.py` (`driven_rhp`, `driven_lhp`, `eventual_period`,
`lone_seed_columns`) and reconstructs the same 44 drives as `driven_halfplane.py`.
No file outside this directory is written or modified.

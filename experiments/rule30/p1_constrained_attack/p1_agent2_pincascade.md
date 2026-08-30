# Agent 2: pin-cascade automaton safety rules

**Verdict: a genuine tightening, and my prior claim that it was "entailed by
construction" was wrong.  It prunes 39% (cascade) to 58% (full 1-pin) of the
state space.  It flips no verdict, and it destroys the Rule 90 control.**

## Why it is not entailed

`INV[30](an, a, b) = an ^ (a | b)` is the forward rule at `(t, x)` solved for
`s(t, x-1)`, so the forward rule holds at every column from `x_min + 1` up to
`R - 1`.  It does **not** hold at `x = R`: there is no `col_{R+1}` to enforce
it against.  The pin at the rightmost modelled column is therefore free
information, and that is exactly where the filter fires.

Two forms, both Rule 30 theorems (`PATH.md` section 1, zero violations at
T = 300):

```text
cascade  s(t,x+1)=1 and s(t,x)=0  =>  s(t+1,x+1)=1
full     s(t,x+1)=1               =>  s(t,x) = NOT s(t+1,x+1)
```

`full` implies `cascade` and is what should be used.

## Soundness

`regression()` drives the true lone-seed letter sequence through the filter
(`pin2_sound.log`): rule 30, `(R,k)` in {(2,2),(3,2),(4,2),(3,3)}, both modes,
**0 mismatches, accepted, 0 pin hits**.  The constraint never rejects the real
diagram.

## Pruning

Q = 2, R = 2, k = 2 (`pin.log`, `pin2_climb.log`):

| filter | states, w=10 | states, w=01 at Q=1 |
|---|---:|---:|
| none | 526 | 472 |
| cascade | 323 (-39%) | -- |
| full 1-pin | -- | 199 (-58%) |

## Verdicts: unchanged

All 6 necklaces `p = 2..4` under cascade, and all 69 primitive necklaces
`p = 2..8` under the full pin at Q = 4 (`pin2_sweep.log`, 69 rows, zero state
caps, 714-1,007 states each): **NONEMPTY, every one, witness verified.**
Witness verification was extended to re-check the pin identity on the derived
lasso independently of the automaton.

Rule 30 `p = 1` stays EMPTY under both pins, at Q = 2, 3, 4.

## The cost: the Rule 90 control is gone

The pin is rule-specific by design -- `PATH.md` section 1.1 tabulates that
Rule 90 pins on nothing, and Rule 90 violates the identity at all 7,227 of its
ones.  So the true Rule 90 lone-seed word is **rejected** by the filter
(`accepted=False, hits=1` at every `(R,k)` tested) and the Rule 90 automaton
collapses to 3 states, EMPTY.

This is the intended behaviour of a pin-based argument and is why `PATH.md`
says such arguments pass the section-0 filter by construction.  But it means
the pin-augmented ladder **has no soundness control**: there is no rule-90
analogue of the constraint to run as a negative.  What remains is the Rule 30
regression above and the `p = 1` calibration.  Any future EMPTY from this
encoding rests on those two alone, and that should be stated wherever such an
EMPTY is reported.

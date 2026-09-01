# Bilateral hard-core rho attempt

Date: 2026-08-31

Status: **OPEN.  No period-two theorem was proved.**  Actual right-side
realizability restricts the alternating-fiber boundary word `rho` to the
hard-core language with no `11`, but this is a two-step corollary of the
already-recorded rung-0 pin cascade.  It permits the relevant oscillations,
and the smallest phase-aware operator summary does not close.

## 1. Exact right-column identity

Assume the center trace has phase `c_(2k)=0`, `c_(2k+1)=1`.  Put

```text
rho_k = s(2k,1),
q_even = s(2k,2),
q_odd  = s(2k+1,2).
```

Applying Rule 30 at column 1 twice gives

```text
s(2k+1,1) = rho_k OR q_even,
rho_(k+1) = 1 XOR (s(2k+1,1) OR q_odd)
          = (NOT rho_k) AND (NOT q_even) AND (NOT q_odd).
```

Therefore

```text
rho_k = 1  =>  rho_(k+1) = 0,
```

so every actually realizable rho word avoids adjacent ones.  The eight
Boolean assignments were checked exhaustively.

This is **validation, not a new labeled result**.  Rung 0 already records the
one-step pin cascade

```text
c_t=0 and s(t,1)=1  =>  s(t+1,1)=1.
```

At the following center-one phase, that pinned one forces the next even-phase
neighbor to zero.  The displayed formula makes the resulting two-step
constraint explicit but does not add an independent mechanism.

For Rule 90, column 1 instead satisfies

```text
s(2k+1,1)=q_even,
rho_(k+1)=1 XOR q_odd,
```

so `rho_k=rho_(k+1)=1` is possible, for example with
`(rho_k,q_even,q_odd)=(1,0,0)`.  Thus the implication uses Rule 30's OR in the
intended way.  It is not applied to Rule 90's constant-zero trace, which
remains a valid finite period-dividing-two control.

## 2. Oscillation survives the restriction

For the adversarial finite row `{-8,-1,6}`, the exact even-time neighbor word
through the last valid alternating strobe is

```text
rho_0..rho_7 = 01010101.
```

All seven complete two-step identities through time 14 pass.  The center
trace then fails at time 15 as already recorded.  Hence the hard-core rule
correctly retains the deepest known finite prefix rather than rejecting it
prematurely.

The recorded infinite-left wallpaper member with finite right half `{1,4}`
also has alternating rho empirically.  Thus `0101...` is not an artificial
bounded witness: it is the maximal oscillation allowed by the hard-core
language.  Any proof still has to use initial left-finiteness to exclude it.

## 3. Registered finite-seed falsification

Every hard-core rho seed through length 16 was converted to the exact
alternating-fiber frontier.  After the seed, each rho bit is forced by the
left-zero requirement; an orbit was stopped either when its next pin failed
or when the forced rho would create `11`.  The number of seeds is Fibonacci:

| length | hard-core seeds | maximum accepted post-seed macros | first witness | death |
|---:|---:|---:|---:|---|
| 1 | 2 | 2 | `0x0` | pin |
| 2 | 3 | 1 | `0x2` | pin |
| 3 | 5 | 1 | `0x0` | hard-core |
| 4 | 8 | 4 | `0xa` | pin |
| 5 | 13 | 3 | `0xa` | pin |
| 6 | 21 | 2 | `0x2a` | pin |
| 7 | 34 | 2 | `0x40` | pin |
| 8 | 55 | 4 | `0x50` | hard-core |
| 9 | 89 | 3 | `0x0` | hard-core |
| 10 | 144 | 8 | `0x80` | hard-core |
| 11 | 233 | 7 | `0x480` | hard-core |
| 12 | 377 | 6 | `0x480` | hard-core |
| 13 | 610 | 5 | `0x480` | hard-core |
| 14 | 987 | 4 | `0x1120` | pin |
| 15 | 1597 | 5 | `0x2120` | pin |
| 16 | 2584 | 6 | `0x1028` | pin |

No seed reached the continuation cap of 128.  This is bounded falsification
data only.  In particular, the maximum of eight at length ten is not evidence
for a universal bound and is not used as one.

## 4. Smallest fixed-summary collision

The registered candidate summary was

```text
(previous rho bit, exact D8 action of the current four-carry word).
```

It has nominal capacity 16.  It fails on the lexicographically first pair:

```text
origin (rho length, seed, follow) = (1,0,0)
state (T,A,B) = (2,1,1)

origin = (3,0,0)
state  = (6,21,21).
```

Both are hard-core seeds, both have previous rho zero, and both current words
act as

```text
(1,0,2,3).
```

They also agree on the immediate forced rho and pin: `(rho,pin)=(1,1)`.
Nevertheless their successor actions are respectively

```text
(2,3,1,0)  and  (0,1,3,2).
```

On the following macro, the first path has `(rho,pin)=(0,1)` and continues
once more before a pin failure; the second has `(rho,pin)=(1,0)`, so it both
violates hard-core after the previous one and fails its pin.  Thus the
16-state phase-aware action summary does not determine its own successor.

Adding the next action to the summary would be precisely time-lookahead
growth, a preregistered kill condition.  It was not attempted.  This collision
is the structural reason the hard-core constraint does not repair the
previous dihedral-action closure failure: it restricts which input words are
admissible but does not make the emitted word action a function of the
current action.

## 5. Reproduction and controls

From `/Volumes/A/researchpapers/13-rule30`:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/bilateral_hardcore.py

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/derive_and_controls.py

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/carry_transducer.py
```

The first command checks the 8/8 local identity, the explicit Rule 90
counterassignment, all seven adversarial macro identities, every hard-core
seed through length 16, and the exact closure collision.  The latter two
commands reproduce the complete 32-neighborhood `F^2`, 64-assignment defect,
131,071-row radius-eight, adversarial, Rule 90, 16-tile, and 34,952-frontier
controls.  All passed in the final run; no SAT grid or enlarged horizon was
used.

## 6. Conclusion and next theorem

The hard-core coordinate does not advance the status of Prize Problem 1.
It is a useful exact restriction on genuine right half-planes, but it is
already implicit in the pin cascade and allows alternating rho forever.
Neither a universal post-seed survival bound nor a closed finite action
quotient was proved.

The sharper remaining period-two target is:

> **Hard-core isolated-pulse theorem.**  If rho has no adjacent ones and the
> full forced-left reconstruction `L(rho)` is eventually zero, then rho is
> eventually periodic.

Indeed `col_(-1)(2k)=NOT rho_k` and `col_(-1)(2k+1)=1`.  Eventual periodicity
of rho would therefore make the adjacent width-two trace eventually periodic,
contradicting the width-two theorem already recorded in
`RESULTS-periodicity-bridge.md`.  Proving eventual zero is a sufficient
stronger subtarget, but is not required.  The theorem must use full cumulative
boundary offsets: bounded suffixes, fixed action summaries, and bounded-depth
zero wedges have all failed.  It is period-two-specific and would not settle
the other periods of Prize Problem 1.

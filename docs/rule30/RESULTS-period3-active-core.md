# Primitive period-three active-core conjugacy

Date: 2026-09-03

Status: **EXACT REDUCTION; ALL-LENGTH MORTALITY OPEN.**  A period-three
exclusion is not proved by the finite census below.

Code: `experiments/rule30/period3_active_core.py` and
`test_period3_active_core.py`.

## 1. Exact finite-word state after the left-support knee

For the anti-diagonal frontier of `RESULTS-period3-fiber.md`, encode the two
stored diagonals as shallow-to-deep pair-symbols

```text
q_j=(A_j,B_(j-1)) in {00,01,10,11}.
```

Let

```text
p(q) = XOR_j (A_j OR B_(j-1)).
```

After the finite-left knee, the next newly exposed initial cell must be zero.
At a center-zero phase the free shallow input is therefore uniquely
`v=p(q)`.  At a center-one phase the local rule fixes `v`; survival is exactly
the check that this fixed value equals `p(q)`.  Thus **every surviving step
uses `v=p(q)`**.

With carry `x=p(q)`, read a symbol `(a,b)` and perform

```text
x' = x XOR (a OR b),
emit (x',a).
```

Prepend the boundary symbol `(p(q),c_t)`.  The final carry is zero by the
definition of `p`, so an appended deep `00` emits `00` forever.  The maximal
deep `00` suffix can consequently be stripped exactly.  This gives a
deterministic partial map on arbitrary finite words over four symbols, driven
only by temporal phase.

There is also an exact three-symbol quotient.  Reverse the word so it is read
deep-to-shallow.  Raw symbols `10` and `11` are indistinguishable: both have
first bit one, OR-value one, and therefore the same carry transition and
output.  Write

```text
00 -> 0,   01 -> 1,   {10,11} -> 2.
```

Starting with carry zero, a quotient input symbol `s` emits

```text
carry=0:  emit 1 iff s=2, otherwise 0,
carry=1:  emit 2,
toggle carry iff s!=0.
```

After the last input, append `2` when the final parity is one, and otherwise
append the center bit `c_t`.  Leading zeros are inert in this orientation and
are stripped.  This quotient is exact after every step, not an empirical
merger, and is cross-checked against the four-symbol map.

The implementation cross-checks this word map against the independent packed
integer frontier for every binary shallow-input history through length nine
in both primitive necklaces.

## 2. The two pin schedules

For trace `011`, the required parities are

```text
phase 0: free,
phase 1: p(q)=0,
phase 2: p(q)=1.
```

For trace `001`, they are

```text
phase 0: free,
phase 1: free,
phase 2: p(q)=1.
```

Mortality of every finite core under all three starting phases proves the
corresponding primitive necklace impossible for every finite-left initial
row, and hence for every finite Rule 30 configuration.

## 3. Exact finite census and structural warning

Every normalized core of length at most ten dies under both schedules within
the checked cap.  The longest cases at length ten are:

```text
011: lifetime 21,
001: lifetime 37.
```

These are bounded facts, not induction.  More importantly, normalized core
length does not contract.  If its last symbol has first bit one (`10` or
`11`), the next normalized length is `L+1` and the new last symbol is `01`.
If the last symbol is `01`, the next length is `L` and its last symbol has
first bit one.  Hence every nonempty surviving core grows by one cell every
two steps.  A proof cannot be a finite-state no-cycle argument or a monotone
length descent.

The live theorem is therefore:

> Every finite four-symbol core eventually violates the parity schedule
> `(*,0,1)` for `011`, and every core eventually violates `(*,*,1)` for
> `001`.

This all-word statement is stronger than necessary because it discards
reachability constraints at the knee.  Its survival through length ten makes
it a legitimate first proof target; a counterexample at larger length would
redirect the proof to the exact reachable language without affecting the
conjugacy.

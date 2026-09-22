# Primitive period-three fibers: exact phase-driven frontier

Date: 2026-09-02

Status: **A PERIOD-THREE EXCLUSION IS NOT YET PROVED.  THE TWO PRIMITIVE
PHASE CLASSES NOW HAVE AN EXACT FINITE-LEFT FRONTIER, LOCAL STROBOSCOPIC
FIBERS, AND BOUNDED EXCLUSION CERTIFICATES.**

## 1. Two genuinely different cases

After the same-orbit reduction and removal of the already excluded constant
traces, a period-three center has one of two primitive necklaces.  Temporal
rotation lets us choose representatives

```text
001 and 011.
```

They are not equivalent under a Rule 30 time shift: rotations stay within
one necklace.  They also have different reconstruction budgets.  In `001`,
two phases expose a free right-column bit and one phase is pinned.  In `011`,
one phase is free and two are pinned.

## 2. Exact radius-three stroboscopic fibers

Enumerating the 128 radius-three neighborhoods against three literal Rule 30
steps gives eight solutions in each case.  Suppressing the always-free cell
at position `+3`, the allowed words on positions `-3,...,+2` are

```text
001: 011010, 011011, 100001, 110000,
011: 000010, 000011, 111000, 111001.
```

The second line has the especially rigid five-cell consequence

```text
(a(-3),a(-2),a(-1),a(0),a(1)) in {00001,11100}
```

at every three-step strobe.  Equivalently, the three cells immediately left
of the center agree and the right neighbor is their complement.  This local
rigidity is new, but it is not by itself a finite-support contradiction.

## 3. Uniform frontier and parity reduction

For any prescribed center trace `c`, rotate Rule 30 at the center:

```text
l_t = c_(t+1) XOR (c_t OR r_t).
```

Thus `c_t=0` makes `l_t` freely selectable through `r_t`, while `c_t=1`
fixes `l_t=1 XOR c_(t+1)`.

Retain the two reconstruction anti-diagonals

```text
A_j=x(T-j,-j),  B_j=x(T-1-j,-j).
```

Feeding `v=l_T` constructs the next diagonal by

```text
C_1=v,
C_(j+1)=C_j XOR (A_j OR B_(j-1)),
B_0=c_(T-1).
```

The newly exposed initial-left cell therefore has the exact closed form

```text
L_(T+1)=v XOR parity(A OR shift(B) OR c_(T-1)).
```

Suppose the initial row has left depth `d`.  Once `T+1>d`:

- at a zero phase, exactly one value of `v` makes `L_(T+1)=0`;
- at a one phase, `v` is already fixed, so survival is one pure parity check.

The surviving dynamics is consequently deterministic after the knee, driven
only by the three temporal phases.  For `011` it faces two parity checks per
macro; for `001`, one.  The period-two alternating fiber is the corresponding
one-check-per-two-step member of the same construction.

## 4. Exact bounded certificates

`period3_fiber_probe.py` checks the local fibers independently, compares the
anti-diagonal frontier with direct column reconstruction on every binary
input word through length ten, and verifies the parity formula on every
input word through length nine.

It then merges identical exact frontiers and exhausts the finite-left tree.
Every tested tree dies:

```text
011: every left depth d <= 36; latest first-empty time 53,
001: every left depth d <= 24; latest first-empty time 87.
```

These are finite-depth theorems only.  Their different profiles agree with
the exact phase budgets: `011` is the more constrained candidate, while
`001` has longer plateaus and substantially larger survivor sets.

## 5. Live theorem targets

The preferred first target is the `011` class:

> No finite reconstruction frontier can pass forever under the periodically
> driven sequence “one free zero-emitting step, check `0`, check `1`.”

Here “check `0`, check `1`” are the fixed left-column values at the two one
phases.  A proof excludes the complete `011` necklace, including all temporal
rotations, for every nonzero finite Rule 30 row.

The `001` class is the analogous sequence “free, free, check `1`.”  It should
be treated separately rather than hidden inside a generic period-three
search.  A proof for `011` alone is already a genuine nonconstant temporal
period exclusion, but both necklaces are required to exclude period three.

The frontier remains unbounded.  Therefore a bounded-window quotient, a
finite-depth ladder, or the finite death table is not an admissible proof.
The next useful object must be a well-founded quantity for the full ordered
anti-diagonal or a phase-macro identity that consumes finite-left support.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/period3_fiber_probe.py
```

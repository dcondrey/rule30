# Reflected overlays, the ordered OR latch, and dual colex descent

Date: 2026-09-01

Status: **THE REFLECTED-HALF OVERLAY HAS BEEN IDENTIFIED EXACTLY WITH TWO
COMPLEMENTARY QUOTIENTS OF THE EXISTING FOUR-STATE CARRY.  EVERY PURELY
SYMMETRIC XOR/AND/OR OVERLAY IS NOT LOCALLY CLOSED.  A NEW ALL-WORD DUAL
COLEX DESCENT IS PROVED, BUT THE GROWING BOUNDARY STILL PREVENTS MORTALITY.
THE PERIOD-TWO EXCLUSION REMAINS OPEN.**

## 1. The exact folded rule and alternating boundary pins

Fold a Rule 30 row at the center and put

```text
q_i=(L_i,R_i)=(x(-i),x(i)),  i>=1.
```

For the inward, current, and outward folded cells, the bulk update is

```text
L'_i = L_(i+1) XOR (L_i OR L_(i-1)),
R'_i = R_(i-1) XOR (R_i OR R_(i+1)).                 (1)
```

This is a radius-one four-state CA.  The checker matches (1) against the two
literal Rule 30 updates on all `4^3=64` folded neighborhoods.

If the center alternates `0,1,0,1,...`, the center update gives two exact
overlay pins at distance one:

```text
c_t=0, c_(t+1)=1  => L_1 XOR R_1=1,
c_t=1, c_(t+1)=0  => L_1=1, hence L_1 OR R_1=1.     (2)
```

Thus the XOR overlay is pinned on the zero phase and the OR overlay is pinned
on the one phase.  These are boundary conditions, not density statements.

## 2. Symmetric overlays lose the decisive orientation

Write

```text
X=L XOR R,  A=L AND R,  O=L OR R.
```

Every nonempty subset of `{X,A,O}` fails to be a local factor of (1).  One
collision kills even the complete triple.  The neighborhoods

```text
(00,01,01) and (00,01,10)
```

have identical `(X,A,O)` labels cell by cell, but their folded outputs are
respectively `01` and `11`.  Hence XOR, AND, OR, or any combination of them
cannot evolve without an additional orientation bit.

The exhaustive subset audit also finds that the inclusion-minimal closed
bulk projections among `{L,R,X,A,O}` are just `L` and `R` separately.  This
is expected: away from the fold each half is its own Rule 30 evolution.  The
center boundary condition couples them and is exactly where a symmetric
overlay loses information.

## 3. The ordered overlay is the existing OR-latch quotient

For the four-state carry input `q=(a,b)`, the exact transition is

```text
c' = c XOR (a OR b),
d' = d XOR (c OR a).                                (3)
```

Consequently the carry action depends only on the ordered pair

```text
(a, a OR b).
```

It has three classes: `00`, `01`, and `{10,11}`.  In state notation this is
the forward quotient

```text
F=(0,1,2,2),                                        (4)
```

and it explains the already-proved equality of carry input actions `2~3`.
The two mismatch states `01` and `10` have the same symmetric overlays but
different carry actions.  The missing orientation is therefore not a
rendering artifact: it is precisely the `D8` phase data.

The inverse constant-tail queue uses the complementary normalization

```text
B=(0,1,2,1),                                        (5)
```

which identifies `1~3`.  The joint labels are

```text
state:       0      1      2      3
(B,F):    (0,0)  (1,1)  (2,2)  (1,2).              (6)
```

Thus the two ternary quotients together recover the full raw state, and raw
state `3` is their sole disagreement.

## 4. New uniform theorem: simultaneous colex descent

Let a legal normalized constant-tail queue be scanned as in
`RESULTS-COLEX-DESCENT.md`, and exclude the newly appended boundary cell.
The previous theorem showed strict colex descent after applying `B`.

The same finite-product proof now gives, for words of every length:

1. `B(raw scan)` strictly colex-decreases under both `0<2<1` and `2<0<1`;
2. `F(raw scan)` strictly colex-decreases under the same two orders; and
3. the unquotiented raw scan strictly colex-decreases, for example under
   `0<2<3<1` and `2<0<3<1`.

The complete synchronous products have at most 36 reachable states.  Every
legal final product state has comparison `less`; this is an all-word proof,
not a bounded queue enumeration.

This strengthens the ordered pivot theorem: the descent exists before
normalization, in both complementary OR-latch orientations, and after the
actual queue normalization.

## 5. Why it still does not prove mortality

The queue update appends a new hard-core boundary symbol after each of the
three descending inherited words.  That cell is colex-most-significant and
resets all three comparisons simultaneously.  The dual quotient therefore
does not repair the reset problem by itself.

Nor can all branching be charged to the sole disagreement state `3`.  For
every `m>=1`, the legal tail-2 queue

```text
2 1 0^m 1
```

has raw scan

```text
1^(m+1) 2.
```

This follows uniformly from the three table entries
`g_2(1)=1`, `g_1(0)=1`, and `g_1(1)=2`.  It creates arbitrarily many new
normalized `1` cells without visiting raw state `3`.  Hence the failed raw
`#1` retreat budget cannot be repaired by merely adding a count of quotient
disagreements.

The surviving target remains an ancestry theorem: repeated boundary resets
must be charged to the *ordered extent* of state-1 propagation through the
full word, not to a bounded overlay count.  The lossless boundary-gap list or
the deterministic halving recurrence retains that extent; a symmetric image
overlay does not.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/folded_overlay_audit.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_dual_colex.py
```


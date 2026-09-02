# Reverse-order and center-controlled folds

Date: 2026-09-01

Status: **THE REVERSE ORDER IS AN EXACT CHARACTERISTIC SHEAR, AND USING THE
CENTER BIT TO SELECT THE ORDER FORCES ZERO XOR AT BOTH FOLDED ENDPOINTS.
HOWEVER, EVERY SYMMETRIC ONE- OR TWO-STEP QUOTIENT IS NONCLOSED, AND ALL 64
EDGE-COMPATIBLE TWO-HALF LEXICOGRAPHIC RANKS FAIL BY LENGTH FOUR.  THIS DOES
NOT EXCLUDE PERIOD TWO.**

## 1. Reverse the already mirrored right row

Reading the left half center-to-edge and the right half edge-to-center gives

```text
Q_t(i)=(A_t(i),B_t(i))=(x_t(-i),x_t(t-i)), 0<=i<=t.       (1)
```

For an interior coordinate the exact update is

```text
A_(t+1)(i)=f(A_t(i+1),A_t(i),A_t(i-1)),
B_(t+1)(i)=f(B_t(i),B_t(i-1),B_t(i-2)),                  (2)
```

where `f(l,c,r)=l XOR (c OR r)`.  Equation (2) was checked on all
`4^4=256` pair neighborhoods and directly against 16 single-seed spacetime
steps.

The `B` recurrence is precisely the binary one-sided right-characteristic
shear.  It is analogous to, but not conjugate to, the four-state
inverse-terminal queue: the alphabets, local maps, and boundary variables
are different.

For the single-seed triangle the two word endpoints are

```text
Q_t(0)=(c_t,1),       Q_t(t)=(1,c_t).                    (3)
```

Thus reverse ordering changes the ordinary fold into a two-ended word whose
end states are transposes.

Every nonempty projection from the symmetric features

```text
X=A XOR B,  N=A AND B,  O=A OR B
```

is nonclosed under (2), including the complete joint label `(X,N,O)`.  The
inclusion-minimal closed bulk projections are just the two literal sides
`A` and `B`.  Reverse order therefore exposes the shear but does not compress
away mismatch orientation.

## 2. Let the center select the order

Encode the physical right half `u_t=(x(t,0),...,x(t,t))` by

```text
E_c(u)=u              when c=0,
       reverse(u)     when c=1.                         (4)
```

Under the hypothetical alternating center trace, (4) reverses on every
step.  The new right-edge bit appears at the beginning on `0 -> 1` and at
the end on `1 -> 0`.  This is an exact alternating-end deque representation;
1,023 finite words checked the literal update and edge placement.

There is one uniform descent.  Delete the newly added edge after a `1 -> 0`
step.  In the encoded word the old first bit is the right edge `1`, while the
new first bit is the prescribed center `0`.  Hence the inherited word is
strictly smaller in lexicographic `0<1` order for every length.  The complete
length-14 census has

```text
less/equal/greater = 8192/0/0.                          (5)
```

The complementary `0 -> 1` phase has both directions in every lex/colex bit
order.  Small witnesses are

```text
01 -> 11,       0111 -> 0011.                          (6)
```

The two-step macros also increase and decrease in every fixed order.  Thus
the descent (5) is reset on the intervening phase.

## 3. Adaptive folded boundary

Keep the left side center-to-edge, and select standard or reverse pairing on
the right using the center:

```text
Q_t(i)=(x(t,-i),x(t,i))       when c_t=0,
       (x(t,-i),x(t,t-i))     when c_t=1.               (7)
```

If the center alternates `0,1,0,1,...`, then the XOR label is zero at both
word endpoints in both phases.  This is a genuine boundary simplification:

```text
c=0: endpoints (0,0),(1,1),
c=1: endpoints (1,1),(1,1).                            (8)
```

It does not close the bulk.  For each phase, every nonempty symmetric
projection from `{X,N,O}` has an exact same-input-label/different-output-label
collision under the two-step map that returns to that phase.  In particular,
even `(X,N,O)` cannot evolve without the ordered mismatch orientation.

## 4. Can the left half pay for the bad phase?

The final registered test combined both literal halves.  The left half was
always read center-to-edge.  The right half used (4).  Word significance was
restricted so each new characteristic edge was least-significant:

- left: lex in both phases;
- right: lex in phase zero, colex in phase one;
- either half could be primary;
- each half and phase could independently use `0<1` or `1<0`.

These choices give 64 phase-dependent lexicographic products.  Exhausting
43,691 admissible left/right row pairs through length nine rejects all 64.
The last surviving choice already fails at length four:

```text
phase 0: A/B = 0001/0001 -> 1011/1101.                 (9)
```

Therefore the left half does not repair the reset within this complete
finite class of simple two-half ranks.

## 5. Consequence for the period-two attack

Center-controlled reversal contributes two exact facts worth retaining:

1. new spatial boundary cells alternate ends in the one-step representation;
2. the adaptive XOR word has fixed zero endpoints.

But neither fact descends to a closed symmetric factor, and the simplest
boundary-compatible ordinal product is decisively false.  A useful successor
would have to retain the four-state orientation as a cocycle and couple the
two phases before comparison—essentially a boundary-annotated transducer,
not an XOR/AND/OR image.

This coordinate also does not directly solve the constant-tail queue reset.
That queue evolves in the inverse-terminal macro coordinate; its appended
symbol is not the physical characteristic edge in (4).  An explicit
conjugacy would be required before transferring the alternating-end result.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/reverse_order_fold_audit.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/center_controlled_reversal_audit.py
```

The preregistrations are `PREREGISTRATION-REVERSE-ORDER-FOLD.md`,
`PREREGISTRATION-CENTER-CONTROLLED-REVERSAL.md`, and
`PREREGISTRATION-ADAPTIVE-TWO-HALF-RANK.md`.

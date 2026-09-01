# Reversed-diagonal queue cocycle for constant cut tails

Date: 2026-09-01

Status: **THE GROWING FORMULA UPDATE HAS AN EXACT ONE-WORD QUEUE FORM.  A
HARD-CORE ENDPOINT OVER AN EVENTUALLY CONSTANT CUT WOULD PRODUCE AN IMMORTAL
QUEUE.  THE STRONGER QUEUE-MORTALITY BOUND IS EXHAUSTIVELY TRUE THROUGH WORD
LENGTH 15, BUT ITS ALL-LENGTH INDUCTION IS OPEN.  PERIOD-TWO MORTALITY AND P1
REMAIN OPEN.**

The solver-free checker is `constant_tail_queue.py`.

## 1. The growing right-edge formula

After reading an endpoint word of length `m`, retain the complete right-edge
diagonal of its inverse-terminal triangle:

```text
D_m=(d_0,...,d_(m-1)).
```

Its last cell is the newly exposed inverse-cut symbol.  If the current
endpoint symbol is `p` and the next symbol is `q`, direct use of the local
triangle rule gives the exact update

```text
D'_0 = B(q),
D'_1 = phi(p,D'_0),
D'_k = phi(D_(k-2),D'_(k-1)),   2 <= k <= m.        (1)
```

This is the requested dynamic cocycle: the formula at size `m+1` is produced
from the full formula at size `m` by one local scan.  It is not a fixed-width
summary; its ordered diagonal grows with the active cone.

`constant_tail_queue.py` reconstructs the inverse-cut diagonal from the
successive last cells of (1) and matches `inverse_cone_diagonal` on all 21,844
four-symbol endpoint words through length seven.  It separately checks 5,461
constant-tail queue updates against literal appended triangles.

## 2. Reverse the diagonal

Fix one of the two tails `c in {2,3}` left by the first-infinite-tail lemma.
On a surviving step both `D_(m-1)` and `D'_m` equal `c`.  Reverse the diagonal:

```text
R=(D_(m-1),...,D_0),   so R_0=c.
```

For `P(y)_t=phi(y_t,y_(t+1))`, let `g_a(l)` be the unique right state with
`phi(l,g_a(l))=a`.  Reversing (1) and using right-permutivity gives the prefix
scan

```text
S_0 = c,
S_i = g_(S_(i-1))(R_i),             1 <= i < m.      (2)
```

The new reversed diagonal is

```text
R'=(S_0,...,S_(m-1),B(q)),                          (3)
```

where the final scan state uniquely decodes `q` from

```text
S_(m-1)=phi(p,B(q)).                                (4)
```

Equations (2)-(4) are an exact deterministic partial map on a single growing
word.  They retain precisely the ordered prefix information lost by the
rejected cycle profiles.

## 3. Hard-core decoder

For a hard-core endpoint, `p,q in {1,2}` and `11` is forbidden.  The final
queue symbol is `B(p)`, so it already records `p`.  The complete legal decoder
is

```text
R_last=2  (p=1): final scan state must be 2; append B(q)=1.
R_last=1  (p=2): final scan state may be 0 or 2;
                 append 2 after state 0 and 1 after state 2.
```

All other final states kill the orbit.  No external endpoint variable or
finite-horizon boundary choice remains.

The four-symbol middle alphabet has an exact quotient.  For every scan state
`s`,

```text
g_s(1)=g_s(3).                                      (5)
```

Consequently replacing every nonleading queue symbol `3` by `1` preserves
the complete next queue, the emitted endpoint, and mortality.  The leading
`3` in the tail-3 mode initializes the scan and is
not replaced.  Thus every queue orbit has a canonical representative over
the ternary middle alphabet `{0,1,2}`.  This is a uniform semiconjugacy, not a
finite-census pattern; 5,461 arbitrary four-symbol queues check it literally.

The normalized image is smaller still.  Subset determinization of the four
scan states gives a five-live-state DFA (plus its dead state) whose language
is exactly the ternary words avoiding

```text
20, 22, 011.                                         (6)
```

The boundary append allowed by the hard-core decoder preserves all three
forbidden factors.  Therefore every surviving queue enters this fixed
shift-of-finite-type language after one update and remains in it.  This is an
all-word graph calculation: the checker compares the complete DFA transition
table, rather than inferring the factors from a bounded word list.

## 4. Uniform reduction

Suppose a hard-core endpoint had inverse cut eventually equal to `c`.  At the
first coordinate after the constant tail starts, form its right-edge diagonal
and reverse it.  Every later endpoint symbol is hard-core and every later cut
symbol is `c`, so equations (2)-(4) iterate forever.

Therefore the following statement is sufficient for both constant-tail
fibers:

> **Queue mortality.** For `c in {2,3}`, every finite word beginning in `c`
> and ending in `{1,2}` eventually leaves the domain of (2)-(4).

This statement is stronger than required because an arbitrary middle word
need not be the diagonal of an endpoint prefix.  A convenient quantitative
version is

```text
lifetime(R) <= |R|.                                 (7)
```

By the exact image theorem (6), it is enough to prove this only after the
first update, on normalized queues avoiding `20`, `22`, and `011` (with the
fixed leading tail-3 symbol treated as the scan initializer).  This is the
smallest proved invariant language presently available for the induction.

Proving (7), or any finite bound depending on `|R|`, would prove the
constant-tail separator, the rank-zero separator, and the nonconstant
period-two exclusion.

## 5. Exact arbitrary-word census

Every normalized word with the two required boundary symbols—not merely
endpoint-derived diagonals—was tested through length 15.  By (5), this covers
all four-symbol words at those lengths.  The maximum number of successful
updates is

```text
length:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
tail 2:  1  0  2  2  5  4  3  5  4  9  8  8  9  9  9
tail 3:  -  1  2  1  5  4  3  4  5  8  7 10  9 10 11
```

All values satisfy (7), and no word survives the explicit 1,000-step
falsification cap.  This is exact finite evidence for the stronger theorem,
not a proof for arbitrary length.

The scan state is the changing formula rather than a scalar energy.  The
remaining induction must explain why each legal right-boundary emission
consumes irrecoverable ordered information from the initial queue despite the
one-symbol growth in (3).  A potential depending only on symbol counts or the
four-state final action would discard the information that the period-16
branch certificate proves necessary.

## 6. Reproduction

From `13-rule30/`:

```bash
uv run python \
  experiments/rule30/p1-period2-invariant/constant_tail_queue.py \
  --control-length 7 --max-queue-length 15 --orbit-cap 1000
```

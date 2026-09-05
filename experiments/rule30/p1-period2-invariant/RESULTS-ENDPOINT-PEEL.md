# Moving-endpoint identities and peel obstruction

Date: 2026-09-01

Status: **OPEN.  No period-two theorem was proved.**  The moving-endpoint
identities were verified, but the registered one-seed/two-follow induction is
false at the level of exact survivor semantics.

## 1. Exact aligned tableau

For a frontier `(T,A,B)`, put `V=1|(B<<1)` and read the aligned symbols

```text
q_j = (A_j,V_j)
```

from deep to shallow.  Starting with carry `(c,d)=(0,0)`, one symbol has the
exact Rule 30 update

```text
c' = c XOR (a OR b),
d' = d XOR (c OR a),
emit (d',c').
```

After the last input symbol the new shallow symbol is `(c XOR d,1)`.  Thus a
pin-passing macro appends symbol `3`.  Padding the deep end by aligned zero
symbols is inert from zero carry, so this gives a fixed-width triangular
tableau even when the stored integers omit leading zeros.

`endpoint_peel.py` independently constructed this word tableau and compared
it with `gray_macro` on all 34,952 even frontiers through width eight.  The
pin and every output symbol agreed.  This is a uniform reformulation of the
existing carry map, not a mortality proof.

## 2. Moving-endpoint block proof

Let

```text
(K_w)_(i,j) = (min(i,j)+1) mod 2.
```

For even `w`, if both indices are below `w`, the old `K_w` block is unchanged.
If exactly one index is new, its minimum is the old index, giving
`e_i=(i+1) mod 2`.  On the two new indices `(w,w+1)`, direct substitution gives

```text
[ 1 1 ]
[ 1 0 ].
```

Therefore, entry by entry over `F_2`,

```text
K_(w+2) = [ K_w   e   e ]
          [ e^T   1   1 ]
          [ e^T   1   0 ].
```

Likewise suffix XOR immediately gives

```text
P_(w+2)(x,a,b) = (P_w(x) XOR a XOR b, a XOR b, b).
```

The checker exhaustively verified the first identity on 364 entries through
`w=10` and the second on 5,460 extended words.  The preceding case split is
the width-independent proof.  These formulas correctly expose the two moving
endpoint coordinates, but do not by themselves say that a seed coordinate
can be removed.

## 3. Exact obstruction to the registered peel

The proposed induction required every legal `(n,H)` tableau to produce a
legal `(n-1,H-2)` tableau, apart from a fixed set of base cases.  Its semantic
implication is already false at the smallest spike in the exact mortality
profile:

```text
length 4, seed 0xa, state (8,243,10): survives 4 macros, then pin fails;
every length-3 hard-core seed: survives at most 1 macro.
```

A total peel applied to the displayed witness would have to produce a
length-3 seed surviving `4-2=2` macros, contradicting exhaustive enumeration
of all five length-3 hard-core seeds.  This obstruction is stronger than a
radius-four closure collision: no choice of local radius, endpoint stack, or
one of the registered 16 boundary modes can repair a rewrite whose output is
required to have those exact `(n-1,H-2)` semantics.

The full profile through the preregistered length 18 was

```text
2,1,1,4,3,2,2,4,3,8,7,6,5,4,5,6,6,8.
```

The later jump at length 10 is another obstruction, but is not needed for the
certificate.  The kill condition fired, so no local-rule fitting or increased
radius was attempted.

This negative retires only a literal one-seed/two-follow semantic peel.  It
does not rule out an amortized induction with a proved credit, a rewrite that
changes the induction parameter, a genuinely different full-tableau lemma,
or the eventual-periodicity route.

## 4. Controls

The retained checker also verified:

- the Rule 30 right-column identity on all `8/8` assignments and the required
  Rule 90 counterexample;
- the Rule 30 row `{-8,-1,6}` alternates through time 14 and first fails at
  time 15;
- Rule 90 row `{-1,1}` has zero center through time 128; and
- no continuation cap was reached during complete hard-core enumeration
  through seed length 18.

## 5. Reproduction

From the Rule 30 project root:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/endpoint_peel.py
```

The period-two theorem, the linear hard-core mortality lemma, and the general
Rule 30 prize problem all remain open.

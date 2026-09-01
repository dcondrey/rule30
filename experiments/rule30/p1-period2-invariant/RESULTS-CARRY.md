# Four-state carry-transducer attempt

Date: 2026-08-31

Status: **OPEN.  No period-two theorem was proved.**  The contraction and
finite-action quotient registered in `PREREGISTRATION-CARRY.md` were killed by
an exact order-eight permutation group and reachable closure collisions.

## Exact subsequential transducer

Let the current aligned symbol be

```text
q_j = (a,b) = (A_j,B_(j-1)).
```

Read symbols from deep to shallow.  Immediately before reading `q_j`, retain
the two carries

```text
(c,d) = (C_(j+1),D_(j+2)).
```

The two reverse Rule 30 recurrences give

```text
c' = c XOR (a OR b) = C_j,
d' = d XOR (c OR a) = D_(j+1).
```

The transition emits `(d',c')`, which is exactly the next aligned symbol
`q'_(j+1)`.  The initial deep carry is `(0,0)`.  After the last input, the
terminal shallow symbol is

```text
q'_1 = (c XOR d, 1),
```

so the pin passes iff the terminal carry has `c XOR d=1`.  This is the
two-carry observation in `RESULTS.md` made into a complete length-free
subsequential transducer; it does not change that result's provenance.

Encode carry `(c,d)` as `2c+d`, input `(a,b)` as `2a+b`, and emitted symbol
`(d',c')` as `2d'+c'`.  The complete table, with entries `next/output`, is

```text
          input 0  input 1  input 2  input 3
state 0      0/0      2/1      3/3      3/3
state 1      1/2      3/3      2/1      2/1
state 2      3/3      1/2      1/2      1/2
state 3      2/1      0/0      0/0      0/0
```

`carry_transducer.py` reconstructs `(D,C)` from the emitted symbols and
matches the independent inverse-Gray macro on all 34,952 legal even-boundary
frontiers through `T=8`.

## Exact group obstruction

Each input symbol acts on the four carry states by a permutation:

```text
input 0: (0,1,3,2)
input 1: (2,3,1,0)
input 2: (3,2,1,0)
input 3: (3,2,1,0).
```

Let `r` be input 1 and `s` input 0.  Exact composition gives

```text
r^4 = 1,  s^2 = 1,  s r s = r^(-1),
input 2 = input 3 = s r.
```

The eight distinct generated maps are

```text
(0,1,2,3)  (0,1,3,2)  (1,0,2,3)  (1,0,3,2)
(2,3,0,1)  (2,3,1,0)  (3,2,0,1)  (3,2,1,0).
```

Hence the transition monoid is the dihedral permutation group of order eight.
No word synchronizes two carries because every word acts bijectively.  A
nonempty two-sided ideal of a group is the whole group, so there is no proper
contracting/rejecting ideal.  The action is transitive on all four carries,
while terminal acceptance is `{1,2}` and rejection is `{0,3}`.  Thus no orbit
of carry states alone separates the pin parities.

The group element of the entire word does determine the *current* terminal
carry, but it does not determine the next emitted word's group element.  The
smallest reachable collision found in the registered lexicographic order is

```text
origin (rho length, seed integer, follow) = (1,0,0)
state (T,A,B) = (2,1,1)

origin = (3,0,0)
state  = (6,21,21).
```

Both words act as `(1,0,2,3)` and both pass their current pin.  Their successor
actions are respectively `(2,3,1,0)` and `(0,1,3,2)`, and their following pins
are `1` and `0`.  This collision is inside the finite rho-seed language.

There is also an equal-frontier-length collision:

```text
origin (4,10,2), state (12,755,394)
origin (5, 0,1), state (12,819,682).
```

Both act as `(2,3,1,0)`, but their following pins again differ.  Retaining one
lookahead action gives eight possible summaries and does not close.  Retaining
two gives at most 64 and also does not close: origins `(1,0,0)` and `(4,10,1)`
share the action trace

```text
((1,0,2,3),(2,3,1,0))
```

through two accepting pins, but their third actions and pins differ.  Adding a
third lookahead has nominal capacity `8^3=512`, beyond the registered 256-state
limit, and is precisely state growth with prediction horizon.  It was not run.

This fires the preregistered kill conditions.  The exact four-state transducer
remains a useful normal form, but transformation-monoid contraction and finite
action lookahead should be retired.

## Rule 90 control

Replacing both ORs by XOR gives four different input transformations but again
the same size-eight transitive permutation group.  Thus the proposed
contraction mechanism fails for Rule 90 rather than falsely excluding its
finite zero-trace row `{-1,1}`.  The Rule-30-specific equality of input maps 2
and 3 comes from `1 OR b=1`; it is absent under XOR, but does not create a
rejecting ideal.

## Reproduction

From `/Volumes/A/researchpapers/13-rule30`:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/carry_transducer.py
```

The final run checked all 16 local transitions, listed every generated group
element and its order, checked the dihedral presentation, cross-checked 34,952
frontiers, and searched 32,043 distinct reachable states under the registered
seed/follow bounds.  The group proof is uniform; the reachable searches are
exact falsifiers only.

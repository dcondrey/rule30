# Projected diagonal support and a one-credit halving route

Date: 2026-09-01

Status: **TWO SMALLER ALL-LENGTH TARGETS NOW SUFFICE FOR THE CONSTANT-TAIL
SEPARATOR.  BOTH PASS EXHAUSTIVE HELD-OUT TESTS THROUGH LENGTH 23 AND LONG
RANDOM CONTROLS, BUT NEITHER IS PROVED.  THE PERIOD-TWO EXCLUSION AND PRIZE
PROBLEM 1 REMAIN OPEN.**

## 1. Outcome

The full three-coordinate zero-prefix greedy lemma can be weakened twice.

First, use only the projected affine coordinates

```text
pi_2(alpha,beta,gamma) = (alpha,beta),
pi_3(alpha,beta,gamma) = (alpha,gamma).              (1)
```

Second, discard matching and the greedy history.  It is enough that required
row `j` has one adjacent zero-prefix change at any token `k>=j`.

The resulting **projected diagonal-support lemma** is:

> For every hard-core word `W`, every tail-2 survival row `j` has some
> `k>=j` where `pi_2(A_(j,k)) != pi_2(A_(j,k+1))`.  Every nonfinal tail-3
> survival row has some `k>=j` where
> `pi_3(A_(j,k)) != pi_3(A_(j,k+1))`.

This lemma has no actual-right hypothesis.  A temporary use of the proved
five-zero right-trace theorem helped reveal `(alpha,beta)`, but a held-out
audit of every omitted word containing `22222` showed that the restriction
is unnecessary for diagonal support.

An independent second target also survives:

```text
s_c(W) <= ceil(n/2)+1+
          max(s_2(L),s_3(L),s_2(R),s_3(R)),           (2)
```

where `L,R` are the two halves of `W`.  Equation (2) is the **one-credit
halving recurrence**.  It is weaker than diagonal support but aligns with the
proved Peel/halving geometry.

Neither statement is yet a theorem.

## 2. Why diagonal support is sufficient

There are `n` zero-prefix tokens, indexed `0,...,n-1`.

For tail 2, suppose the hard-core continuation has length `s`.  Apply
diagonal support at its final row `j=s-1`.  Then

```text
s-1 = j <= k <= n-1,
```

so `s<=n`.

For tail 3, if `s>=2`, apply diagonal support at the final nonfinal row
`j=s-2`.  It gives `s-2<=n-1`, hence `s<=n+1`; the cases `s<2` are immediate.

Thus the projected lemma implies

```text
s_2(W) <= n,
s_3(W) <= n+1.                                      (3)
```

As recorded previously, (3) makes `R_c(W)` fail before its full length `2n`
in both tail modes, with only the small length-one tail-3 case checked
directly.

No matching theorem is needed.  The earlier greedy certificate remains a
stronger source of evidence, but it is no longer the minimal proof target.

## 3. Algebraic meaning of the two projections

Every newest boundary permutation is

```text
(h,l) -> (h+alpha, l+beta*h+gamma).
```

The local affine composition law is

```text
(a,b,g) o (A,B,G) = (a+A,b+B,g+G+b*A).              (4)
```

Consequently `(alpha,beta)` is a closed additive quotient of the D8
cocycle: its update never refers to `gamma`.  For a local left state `q`, its
increment is

```text
(activity(q), 1+low(q)).                             (5)
```

This makes the tail-2 target a two-parity leading-variable statement rather
than a three-coordinate nonlinear rank claim.

The second projection has a different interpretation:

```text
(alpha,gamma) = A(0).                                (6)
```

It is literally the newest cut state produced by appending endpoint state
zero.  Thus the tail-3 target compares one concrete terminal-cone cell across
adjacent zero-prefix scenarios.

These interpretations are exact.  They do not yet prove that a projected
change must occur on or to the right of the row diagonal.

## 4. Exact audits

The first right-aware selector audit covered every hard-core word through
length 22 after applying `22222` only in the tail-2 branch.  It checked
170,740 word/tail cases and found

```text
greedy failures:          0
deadline failures:        0
minimum deadline slack:   0.
```

The registered held-out diagonal-support run then covered:

- every eligible word at length 23: 101,388 cases;
- 1,000 deterministic random words for each tail at lengths 24, 32, 48, 64:
  8,000 cases;
- zero diagonal failures.

The stronger unrestricted tail-2 claim was frozen after a post-hoc probe
through length 18.  Its held-out corpus was precisely every word containing
`22222` at lengths 19 through 23:

```text
length 19:  6,187 cases
length 20: 10,410 cases
length 21: 17,456 cases
length 22: 29,184 cases
length 23: 48,662 cases
total:    111,899 cases
```

There were zero diagonal failures.  Together, the two disjoint length-23
corpora cover every hard-core word in both tail modes.

The registered one-credit halving recurrence passed all words at lengths 21
and 22 in the original exact implementation, then length 23 and 8,000 long
random tail cases in the affine-forcing implementation.  The length-23 run
contained 150,050 word/tail cases and had maximum excess `-2`; no equality
case occurred in that held-out row.

All of these are bounded results.

## 5. Why the halving recurrence is sufficient

Let

```text
T(n)=max {s_c(W): |W|=n, W hard-core, c in {2,3}}.
```

If (2) is proved, then

```text
T(n) <= ceil(n/2)+1+
        max(T(floor(n/2)),T(ceil(n/2))).              (7)
```

Assume inductively that `T(m)<2m` at both smaller half lengths.  Since values
are integral, (7) gives

```text
T(n) <= 3*ceil(n/2).                                 (8)
```

For even `n`, the right side is `3n/2<2n`.  For odd `n>=7`, it is
`3(n+1)/2<2n`.  The exact values at `n<=6` supply the finite bases.  Therefore
(2), despite being much weaker than (3), also proves `T(n)<2n` at every
length and closes the scale separator.

## 6. Killed simplifications

The new positive results do not resurrect several simpler arguments.

1. **No local edge monotonicity.**  In each projected corpus, all sixteen
   binary `2x2` edge patterns occur.  Only a small minority of edge rows are
   intervals.  A Monge or total-monotonicity proof is unavailable.

2. **No bounded pivot jump.**  The full projected greedy jump reaches six by
   length 19 and grows with the horizon.  A fixed-radius propagation table is
   not the invariant.

3. **No endpoint-only telescope.**  Comparing projected labels only at
   scenario `k=j` and the all-zero scenario `k=n` fails frequently.  Internal
   changes can cancel and return, so the ordered word of adjacent differences
   remains essential.

4. **No one-symbol deletion induction.**  Deleting either end and allowing
   either constant-tail mode can reduce the smaller survival by much more
   than one.

5. **No literal half-block embedding.**  After the charged
   `ceil(n/2)+1` rows, the remaining endpoint continuation need not equal a
   prefix of any of the four half-word scale extensions.  A proof of (2)
   must compare a frontier potential or a boundary-mode conjugate, not raw
   endpoint symbols.

## 7. Exact remaining proof targets

The preferred sharp target is the following contrapositive.

> If all adjacent zero-prefix projections are constant for tokens `k>=j`,
> then row `j` cannot be tail-2 hard-core legal; in tail 3, row `j` cannot be
> legal together with row `j+1`.

For tail 2 this should exploit the additive quotient (5).  For tail 3 it
should use the terminal state (6).  The proof must be scale-free: bounded
edge patterns and bounded pivot jumps are already false.

The fallback target is (2).  The proved identity

```text
P^m I(sigma^m e)=sigma^(2m)I(e)
```

shows why a half-scale residual exists, but the earlier halving audit also
showed that one boundary symbol survives.  A proof of (2) must retain that
boundary annotation and show that its survival potential is dominated by
one of the four half-word/tail modes.  Literal symbol embedding is false.

Either proof would exclude the two eventually constant cut tails, close the
rank-zero separator, and prove the nonconstant period-two center trace
impossible.  It would not settle all of Prize Problem 1.

## 8. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_right_zero_prefix_selector.py \
  --first-length 23 --max-length 23 --random-per-length 1000

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_right_zero_prefix_selector.py \
  --first-length 19 --max-length 23 --only-tail2-with-22222

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_halving_recurrence.py \
  --first-length 23 --last-length 23 --random-per-length 1000
```

The selector implementation inherits the exact slow/bit-sliced controls from
the full zero-prefix audit.  The halving implementation uses the same
cross-checked affine-forcing kernel with one bit-slice.

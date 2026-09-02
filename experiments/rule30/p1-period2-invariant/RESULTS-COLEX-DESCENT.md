# Ordered colex descent in the constant-tail queue

Date: 2026-09-01

Status: **A STRICT ORDERED ONE-STEP DESCENT IS PROVED FOR WORDS OF EVERY
LENGTH.  THE GROWING BOUNDARY PREVENTS IT FROM BEING A MORTALITY PROOF BY
ITSELF.  THE CONSTANT-TAIL SEPARATOR AND PERIOD-TWO EXCLUSION REMAIN OPEN.**

## 1. Statement

Let `R=(c,r_1,...,r_(m-1))` be a normalized constant-tail queue in the
proved SFT avoiding `20`, `22`, and `011`, and suppose its hard-core boundary
decoder accepts.  Let

```text
S_0=c,
S_i=g_(S_(i-1))(r_i)
```

be the old-coordinate scan, normalized by `3 -> 1`.  Order the ternary
alphabet by either

```text
0 < 2 < 1,  or  2 < 0 < 1.
```

and compare equal-length words from right to left.  Then

```text
(q(S_1),...,q(S_(m-1))) <colex (r_1,...,r_(m-1)).   (1)
```

Equivalently, at the rightmost coordinate where the scan differs from its
input, the input is `1` and the output is `0` or `2`.

## 2. All-word proof

The checker forms the synchronous product of:

- the four exact scan states;
- the suffix automaton for `20`, `22`, and `011`;
- the final input symbol used by the hard-core decoder;
- the comparison at the most recently read differing coordinate; and
- a bit recording that a nonleading symbol has been read.

Reading left to right is sufficient because each new difference becomes the
rightmost, hence decisive, colex difference.  Every reachable legal final
state has comparison `less`.  For the first order, the complete products
contain 31 reachable states for tail 2 and 30 for tail 3; for the second they
contain 35 and 34.  Exhausting these finite products proves (1) for words of
arbitrary length; it is not a bounded queue census.  Since both possible
orders of `0,2` work while `1` is largest in each, the decisive input is
necessarily `1` and its output is `0` or `2`.

The length-one tail-2 queue is excluded from (1) because it has no scanned
suffix.  It is already an exact base case in the queue mortality census.

## 3. Why this does not yet prove mortality

A legal queue update is

```text
R'=(S_0,...,S_(m-1),B(q)).                          (2)
```

Equation (1) orders the transformed coordinates inherited from `R`, but (2)
also appends a new hard-core boundary symbol at the colex-most-significant
end.  That symbol can reset the comparison.  Therefore ordinary colex order
on the complete growing queue is not decreasing, and (1) alone does not
exclude an immortal orbit.

The reusable gain is an exact ordered pivot: every successful step consumes
the rightmost decisive `1` among its inherited coordinates.  A completion
must attach ancestry to an appended `1` and prove that this replacement
cannot continue forever.  This is compatible with the zero-prefix greedy
certificate and with the exact fact that strict Peel period doublings cannot
occur consecutively; symbol counts and endpoint products discard the pivot.

## 4. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_colex_descent.py
```

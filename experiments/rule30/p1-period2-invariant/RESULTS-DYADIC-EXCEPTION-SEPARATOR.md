# Dyadic exceptional-family separator

Date: 2026-09-01

Status: **A UNIFORM EXCLUSION LEMMA IS PROVED. IT REMOVES THE COMPLETE
EVENTUALLY-`2` ACCEPTANCE COUNTERFAMILY FROM THE REACHABLE ZERO-RAY ORBIT,
BUT THE NON-EVENTUALLY-`2` CASE REMAINS OPEN.** This is not active-core
mortality and does not prove the period-two theorem.

## 1. Why the previous spectrum argument stopped

Two exact facts were already available:

1. every cut in the orbit of `000...` under a finite positive word of carry
   generators is ultimately periodic with power-of-two eventual period; and
2. every hard-core endpoint eventually equal to `222...` has inverse-terminal
   cut eventually equal to `1212...`.

The second family made a raw period-spectrum separation false: accepted and
reachable cuts both allowed eventual period two. The missing question was
whether this overlapping accepted family was actually reachable.

It is not.

## 2. Uniform alternating-output descent

Let `T_m` be the width-`m` triangular zero-ray cascade. At time `t`, write

```text
p_t = carry output after the first m-1 symbols,
x_t = carry output after all m symbols,
q_t = last internal symbol before the final carry action.
```

The cascade update stores the bit-swap of each new carry as the corresponding
next internal symbol. Therefore

```text
q_t = swap(x_(t-1)),
x_t = tau_(q_t)(p_t).                                (1)
```

Suppose `x_t` is eventually `1212...` or `2121...`. On that tail,

```text
swap(x_(t-1)) = x_t,
```

so (1) becomes `x_t=tau_(x_t)(p_t)`. The two literal inverse-action rows are

```text
x_t=1  => p_t=tau_1^(-1)(1)=2,
x_t=2  => p_t=tau_2^(-1)(2)=1.                       (2)
```

Thus the width-`m-1` output `p_t` is itself eventually alternating, in the
opposite phase. The first `m-1` coordinates evolve autonomously as `T_(m-1)`,
so the same argument applies again. Iterating (2) reaches width zero, whose
carry output is identically `0`, contradicting eventual alternation.

This proves, for every finite word `u`,

> `A_u(000...)` is not eventually `1212...` in either phase.

The proof is independent of `m`; it is not inferred from a width census. It
also does not assume that the internal state has already entered a cycle.

There is a stronger output-only formulation. Define the one-sided local map

```text
(Peel x)_t = tau_(swap(x_(t-1)))^(-1)(x_t)
            = phi(x_(t-1),x_t),                       t >= 1.   (3)
```

Equation (1) says exactly that applying `Peel` to the width-`m` output gives
the width-`m-1` output, apart from its irrelevant first coordinate. Hence

```text
x=A_u(000...), |u|=m  =>  Peel^m(x) is eventually 0.           (4)
```

This is strictly more informative than the eventual-period statement: it is
an output-only, nearest-neighbor necessary condition for zero-ray
reachability. Notably, `phi` in (3) is the same four-state local rule used in
the exact inverse-terminal diagonal recurrence. The two previously separate
constructions therefore meet on one literal local table.

## 3. Consequence for the accepted counterfamily

The predecessor audit proved from the exact inverse-cone recurrence that
`x_t` depends only on endpoint coordinates

```text
floor(t/2), ..., t.
```

Hence an endpoint equal to `2` from coordinate `N` onward has inverse cut
equal to `1212...` from coordinate `2N` onward. Section 2 excludes every such
cut from the reachable zero-ray orbit. Therefore

```text
reachable zero-ray orbit
  intersection
inverse-terminal(eventually-2 hard-core endpoints)
= empty.                                             (5)
```

This repairs the specific uniform counterfamily that killed the first dyadic
period-mismatch proposal. Merely observing that the two languages share the
integer period `2` was too coarse; adding orbit reachability separates them.

## 4. Sharpened remaining theorem

The period-two mortality problem would now follow from the single generic
statement

> If a hard-core endpoint is not eventually `2`, then its inverse-terminal
> cut is not ultimately periodic with power-of-two eventual period.

Indeed, a hypothetical immortal finite core would give a hard-core endpoint
whose inverse cut lies in the reachable zero-ray orbit. The dyadic cascade
theorem makes that cut ultimately dyadic-periodic. Statement (5) excludes
the eventually-`2` endpoint case; the displayed generic statement would
exclude everything else.

A weaker but sufficient—and more local—remaining theorem is

> If `e` is a hard-core endpoint and `x=inverse_terminal(e)`, then no finite
> iterate `Peel^m(x)` is eventually zero.

This formulation keeps the full unbounded word but replaces the generator
history by one fixed radius-one rule. A plausible next proof mechanism is a
rotated-triangle or commuting-square identity between the `phi`-triangle that
constructs `x` from `e` and the `phi`-triangle formed by iterating `Peel`.
No such identity is asserted here.

Subsequent continuation derived that identity exactly:
`P(I(sigma e))=sigma^2 I(e)`.  See
`RESULTS-ROTATED-PEEL-IDENTITY.md`; it proves that every finite-rank collision
must have an aperiodic hard-core endpoint, but does not exclude that remaining
case.

This is a genuine reduction, not a proof of the displayed statement. The
finite census of nonconstant periodic hard-core endpoints through period ten
is consistent with it—the inverse-cut periods all contain odd factors—but
finite period data cannot establish the all-endpoint claim. In particular,
one must not assume that an ultimately periodic inverse cut forces its
hard-core endpoint to be ultimately periodic; that implication is also
unproved.

## 5. Independent checks

`dyadic_exception_separator.py` verifies:

- the two inverse-action rows in (2) directly from the carry tables;
- the output-only `Peel` identity on every state through width five and
  24 time layers;
- every complete finite cascade state through width eight has no eventual
  output block `12` or `21` (a regression check only); and
- every hard-core endpoint prefix through length eight followed by `2`s has
  inverse cut in the claimed alternating phase from coordinate `2N`.

Reproduce from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/dyadic_exception_separator.py
```

The period-two theorem and all three full Prize Problems remain open.

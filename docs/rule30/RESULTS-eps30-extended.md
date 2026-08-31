# `eps_30(m)` extended, and what symbolic regression makes of it

Arm `a25_eps30_extended`, 2026-08-31.
Code: `experiments/overnight-arms/frontier_attack/a25_eps30_extended/`.

## 0. Scope, stated before anything else

**This is a side question. It is not a route to P1 and cannot become one.**

`PATH.md` section 9.4 flags this twice, and the flag is repeated here because
this document computes the quantity in question much further than before and
could otherwise be misread. Whether `eps_30(m) -> 0` as `m -> infinity` is
**not** a route to P1 even if it were answered, because Lemma Z needs
*exactness* — a bounded window that determines `r_t` with probability 1 — and
Theorem W already establishes `eps_30(m) > 0` at every finite `m`. A limit of
zero would say bounded windows get arbitrarily close; it would still not say
any of them arrives. So:

* nothing below changes any row's status;
* nothing below bears on P1, P2 or P3;
* the value of this arm is a clean characterisation of a quantity the project
  had already computed to `m=16`, and an honest account of what a fitted
  functional form can and cannot settle about its limit.

<!-- FILL -->

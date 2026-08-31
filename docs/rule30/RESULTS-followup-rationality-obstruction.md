# RESULTS — roundtable follow-up, "rationality obstruction" (Direction 3)

STATUS: **KILLED as stated, at the mechanism level** (not merely at finite length).
Everything below is MEASURED or a checked derivation; nothing here is a proof of P1
or of anything weaker. Work lives entirely under
`experiments/overnight-arms/roundtable_followup/rationality_obstruction/` and is new
code, not a modification of any existing probe.

## 0. What was checked, and the verdict up front

The panel's proposal asks for a proof that the center-column generating function
`A(z)` cannot be rational, derived from the quadratic (OR-as-`b+c+bc`) term alone,
"not from any finite spacetime window," and claims this evades the `O(log t)` wall
because it would be an identity in the full series ring.

Two independent things kill this at the mechanism level, before any question of
whether the target statement would even help:

1. **The claimed closed equation `Q(G)=0` in `G` alone does not exist.** The
   nonlinear term forces in a second, independent unknown series (the lag-1
   pair-correlation generating function `K`), and `K` itself does not close under
   one more step — its evolution needs triple-point data. This is the standard
   Gutowitz/BBGKY-style non-closure of the correlation hierarchy for a nonlinear
   cellular automaton, and it is verified directly below (not asserted).
2. **Even granting a workable identity, "rationality obstruction from the bilinear
   term alone" is exactly the mechanism `docs/rule30/overnight/RESULTS-automaticity.md`
   already proved cannot work**, one level down from where it was stated there.
   That document's "Two proved negatives," item 1, shows algebraicity is closed
   under Hadamard product (Sharif–Woodcock 1988) — the *only* nonlinearity Rule 30
   has is exactly this Hadamard-type pair product — so nonlinearity alone can never
   force transcendence. The same argument is even more elementary one level down:
   eventually-periodic (= rational) sequences over `F_2` are trivially closed under
   any fixed-lag Hadamard product (a shift-and-AND of two eventually-periodic
   sequences is eventually periodic by inspection). So a "the bilinear term forces
   irrationality" argument is structurally impossible for the same reason a
   "nonlinear rule forces transcendence" argument was already shown impossible.
   What would have to fail instead is uniformity of some order/height parameter
   *as it grows with `t`* — and that is precisely the content of the `S(n)` ladder
   already built and run in row 46 of `PATH.md`, not a new object.

So Direction 3, as proposed, reduces to: (a) a non-closing equation that is not
actually "`Q(G)=0`" in the sense claimed, and (b) if repaired into the nearest
well-posed question ("is `A(z)` rational", i.e. `S(0)` in the existing ladder), it
is not new — `docs/rule30/overnight/RESULTS-automaticity.md` already asked exactly
this question and already has stronger certificates (order 0, height up to 800,
`N` up to ~3400) than anything computed fresh here.

## 1. Deriving `Q(G)=0` — what actually holds

Local rule, OR written as the quadratic F_2 identity (`b|c = b+c+bc`):

    u_{t+1,i} = u_{t,i-1} + u_{t,i} + u_{t,i+1} + u_{t,i}*u_{t,i+1}

Let `G_t(x) = sum_i u_{t,i} x^i` (finite-support Laurent polynomial at each `t`),
`K_t(x) = sum_i u_{t,i}*u_{t,i+1} x^i` (the lag-1 pair-correlation series), and
`G(x,z) = sum_t G_t(x) z^t`, `K(x,z) = sum_t K_t(x) z^t`. Summing the local rule
over `i` gives the exact row identity

    G_{t+1}(x) = (x + 1 + x^{-1}) * G_t(x) + K_t(x)        ... (*)

and hence, in `F_2[[x^{+-1}, z]]`,

    G(x,z) = G_0(x) + z*(x+1+x^{-1})*G(x,z) + z*K(x,z)      ... (**)

**Verified computationally** (`functional_eq_check.py`): identity (*) checked cell
by cell against direct bit-parallel simulation of the lone-seed orbit for `t=0..39`,
exact match every step (this also re-validates `b|c=b+c+bc` on all four input pairs,
used as the derivation's only nonstandard step).

**The claimed reduction to `G` alone fails.** (**) is a relation between *two*
series, `G` and `K`. The panel's `Q(G)=0` implicitly assumes `K` is obtainable from
`G` by ring operations (`+`, `x`, and the Frobenius substitutions `x -> x^{2^i}`
that Christol theory allows). It is not: `K_t(x)` is a lag-1 Hadamard-type
extraction of `G_t` with itself, not a coefficient of any one-variable polynomial
combination of `G_t(x)`. Concretely (`functional_eq_check.py`, `t=6`): the only
"natural" ring self-product of a single Laurent series over `F_2` is the Frobenius
square `G_t(x)^2 = G_t(x^2)`, whose support is forced to be entirely even indices;
`K_6` has support `{-5,-2,-1,0,3,4}`, which contains odd indices, so `K_6 != G_6(x)^2`
and in fact `K_t` is not expressible as *any* fixed polynomial map of `G_t(x)` alone
(no such map can move odd-indexed information into existence from an object with no
odd/even structure of its own). `K` is a genuinely independent unknown, not an
eliminable one.

**The pair-correlation object does not close either.** `hierarchy_check.py` computes
the full truth table (32 rows) of `K_{t+1,0} = u_{t+1,0}*u_{t+1,1}` as a Boolean
function of the window `u_{t,-1..2}` and takes its algebraic normal form (Möbius/
Zhegalkin transform). Result:

    K_{t+1,0} = a_0 + a_1 + a_{-1}a_0 + a_{-1}a_1 + a_{-1}a_2 + a_0 a_2
                + a_{-1}a_1 a_2 + a_0 a_1 a_2

ANF degree 3, with two genuine degree-3 monomials (`a_{-1}a_1a_2`, `a_0a_1a_2`).
So the pair-correlation's own one-step evolution needs *triple*-point information
about `u_t` that is not contained in `K_t` (a purely pairwise object). This is
exactly the standard obstruction in Gutowitz local structure theory (already the
cited adjacent prior art in `PATH.md` row 50, there for a P2 question): for a
nonlinear CA, the hierarchy of `n`-point spacetime correlation generating functions
does not close at any finite `n`. A "quadratic relation `Q(G)=0`" that stops at
order 2 is the truncation of an infinite hierarchy, not an identity.

## 2. Is "`A(z)` rational" the same statement as P1, or a weaker cousin?

Precise, and it decides everything: **for a formal power series over a finite
field with an honest denominator (`Q(0) != 0`, so the ratio is a well-defined power
series, not merely a formal symbol), `A(z)` rational is EXACTLY EQUIVALENT to the
coefficient sequence being eventually periodic.** Not stronger, not weaker,
not incomparable — the same statement in different language.

- If `a(t)` is eventually periodic with preperiod `q`, period `p`, then
  `A(z) = (\text{prefix polynomial}) + z^q \cdot (\text{one-period block}) / (1 - z^p)`,
  and `1 - z^p` has constant term `1` (units of `F_2`), so `A` is rational with an
  honest denominator.
- Conversely, if `A(z) = P(z)/Q(z)` with `Q(z) = 1 + q_1 z + ... + q_d z^d`, then
  `a(t)` satisfies the linear recurrence `a(t) = sum_{k=1}^d q_k a(t-k)` for `t`
  past `deg P`. The recurrence's state `(a(t),...,a(t+d-1)) in F_2^d` evolves under
  a fixed linear map on a set of size `2^d`; by pigeonhole the state sequence
  eventually cycles, hence `a(t)` is eventually periodic.

This is not a new observation of this document — it is exactly `S(0) <=> P1
exactly` from `docs/rule30/overnight/RESULTS-automaticity.md`, restated with the
proof sketch spelled out. **Consequence for Direction 3: if a proof that `A(z)` is
irrational existed, it would be a complete proof of P1, not a weaker result.**
That raises the bar, it does not lower it — the panel's target is not an easier
side-door into P1, it is P1 itself under a different name (`S(0)` in the existing
ladder), and the existing ladder already has better finite certificates for it
(order 0, height 800, `N ~ 39000`) than anything this follow-up computed.

## 3. Hankel-rank measurement (cheapest test, run as specified)

`hankel_rank.py` computes the linear-complexity profile `L(N)` via Berlekamp–Massey
over `GF(2)` for `N` up to 2000. `L(N)` is the length of the shortest LFSR
reproducing the length-`N` prefix; boundedness of `L(N)` as `N -> infinity` is
exactly boundedness of Hankel rank, exactly rationality.

| sequence | L(50) | L(100) | L(200) | L(500) | L(1000) | L(2000) | growth over back half |
|---|---|---|---|---|---|---|---|
| A051023 (Rule 30 center) | 26 | 48 | 101 | 249 | 500 | 1000 | +499 (tracks `N/2`) |
| Rule 90 center | 1 | 1 | 1 | 1 | 1 | 1 | +0 (flat) |
| synthetic eventually-periodic, period 11 | 10 | 10 | 10 | 10 | 10 | 10 | +0 (flat) |
| random control (seeded) | 26 | 50 | 99 | 250 | 501 | 1001 | +500 (tracks `N/2`) |

A051023's `L(N)` is indistinguishable from the random control's `~N/2` growth over
this range and shows no sign of saturating, while both controls (Rule 90 and a
genuine eventually-periodic sequence) saturate immediately and stay flat. This is
**MEASURED**, consistent with non-rationality at this length, exactly as
`RESULTS-automaticity.md` already found (its independent order-0 Ore-relation check
found no relation of height <= 800 through `N ~ 39000`, a strictly stronger
certificate covering 20x the prefix length and 800 vs the effective ~1000 seen here).

**What this measurement is not.** By construction (obstruction H, `PATH.md` 7.3,
and Theorem O in `RESULTS-automaticity.md`): the sequence formed by taking A051023's
first `N` terms and appending zeros forever is eventually periodic — hence rational,
hence has *some* finite Hankel rank — for every `N`. So no finite computation of
`L(N)`, however large `N` gets, can ever certify `sup_N L(N) = infinity`; every
run only produces a lower bound on the true (possibly infinite) Hankel rank, worth
exactly `N`-terms-buys-`~N/2`-of-lower-bound and nothing more, ever. This is the
same wall that already closed rows 2, 3, 4, 17, 32, 33, 41 and bounds row 46 — it
is not evaded by writing the identity in the "full series ring" rather than a
finite window, because the *test* performed on that identity (a rank computation)
is unavoidably a finite-prefix operation regardless of which ring the identity
formally lives in.

## 4. Rule-90 screen, verified directly

`hankel_rank.py` computes the Rule 90 lone-seed center column directly (bit-parallel
`new = (row<<1) XOR (row>>1)`, no OR/AND term) and confirms: first 16 bits
`1000000000000000`, and every bit after `t=0` is exactly `0`. So
`A_90(z) = sum_t a_90(t) z^t = 1` exactly (all higher coefficients are zero), the
constant series — rational with denominator `1`, as the panel's own screen states.
`hierarchy_check.py`'s ANF computation used Rule 30's rule (`b|c=b+c+bc`); redoing
it with Rule 90's linear rule (`am1 XOR a1`, dropping the `a0` and the `a0&a1` term
entirely) has ANF degree 1 by inspection — no bilinear term exists to feed a
hierarchy, `Q` collapses to the linear identity the panel already names, and it is
solved by the (rational) Sierpinski/Rule-90 generating function. The screen holds:
Rule 30's nonlinearity is exactly the source of the non-closure in section 1, and
removing it (Rule 90) removes both the non-closure and the Hankel-rank growth.

## 5. Is Hankel-rank growth new evidence?

No. It is obstruction **H** (`PATH.md` 7.3, "Finite data cannot establish an
infinite statement") wearing different notation. Concretely:

- `S(0,d)` ("no order-0 Ore relation of height `<= d`") in
  `RESULTS-automaticity.md` **is** "Hankel rank exceeds `d`" for the relevant
  prefix length — an order-0 Ore relation `P_{-1}(x) + P_0(x)F(x) = 0` of degree
  `<= d` is literally an LFSR of length `<= d` reproducing the sequence, which is
  literally a statement about Hankel-matrix rank `<= d`. The two computations
  (`ore_check.py`'s Gaussian elimination on a truncated linear system, and this
  document's Berlekamp–Massey) are two implementations of the same finite
  certificate, and the existing one is already stronger (height 800 vs. the
  effective ~1000 reached here, at 20x the prefix length: `N=39000` vs `N=2000`).
- Theorem O in the same document already states the exchange rate precisely:
  `N` terms of agreement buy a kernel/rank lower bound of about `N/8` (there,
  for the automaticity kernel; the Hankel-rank analogue here is the same
  argument at order 0) "and nothing more, ever."

So this document adds no new lower bound and no new proof technique beyond what
`RESULTS-automaticity.md` already has; its only new content is (a) the explicit,
computationally verified demonstration that the panel's proposed closed equation
`Q(G)=0` in `G` alone does not exist and why (sections 1 and the hierarchy
non-closure), and (b) the explicit equivalence proof in section 2 pinning down that
"`A` rational" is not a weaker target than P1 but an exact restatement of it.

## Verdict

- **Is this route logically capable of proving P1 even in principle?** Only in the
  trivial sense that "`A(z)` is irrational" already *is* P1 (section 2) — so success
  would prove P1, but the specific mechanism proposed (an obstruction "from the
  bilinear term alone") is one this repo already has a general proof cannot work
  (`RESULTS-automaticity.md`'s Sharif–Woodcock argument, restated a level down in
  section 0/1: Hadamard-type nonlinearity does not obstruct rationality, since
  rational/eventually-periodic sequences are trivially closed under any fixed-lag
  Hadamard product). What would have to fail is uniformity of the Ore
  order/height *as a function of `t`*, which is exactly Lemma L, the open
  obligation already sitting at the top of row 46 — not a new target.
- **Is it distinct from known-dead approaches?** No. It is the `S(0)` rung of the
  existing automaticity ladder (row 46), reached by a different, non-closing route
  (a truncated correlation hierarchy instead of the Ore-relation construction),
  and bounded by the same obstruction H that already governs row 46's reading.
- **What was measured:** the local-rule functional identity `(*)`/`(**)` (exact,
  verified by simulation); that the claimed `Q(G)=0` requires an independent
  second series `K` which itself fails to close at the next order (ANF degree 3,
  verified by brute-force truth table); Hankel rank / linear complexity of
  A051023 tracking `~N/2` like a random control out to `N=2000`, against Rule 90
  and a period-11 control both flat from the start; and the Rule 90 screen itself
  (`A_90(z)=1` exactly, confirmed by direct simulation).

## Code

All under `experiments/overnight-arms/roundtable_followup/rationality_obstruction/`:

- `functional_eq_check.py` — derives and verifies identity (*)/(**); shows `K` is
  not a ring expression in `G` alone.
- `hierarchy_check.py` — brute-force ANF of `K_{t+1}` as a function of `u_t`;
  shows degree-3 monomials, i.e. non-closure at the pair-correlation level.
- `hankel_rank.py` — Berlekamp–Massey linear-complexity profile for A051023, Rule
  90 center, a period-11 control, and a random control; also verifies
  `A_90(z) = 1` directly.

No file outside this new directory and this results document was modified.

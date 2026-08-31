# a17 — 2-adic valuation / Newton polygon attack on P1

**VERDICT: KILLED. The missing piece is the equation. The pin identity yields no
closed functional equation for the centre-column generating function — it is a
guarded relation among *three different columns* whose unconditional form
contains a coefficientwise product `c_t r_t`, which is not an operation of
`F_2[[x]]`, so the column system never closes. Newton polygons and Weierstrass
preparation are tools that consume a polynomial/functional equation and return
valuations of its roots; with no equation there is no object for them to act on.
And even if an equation were handed over for free, the tools are degenerate on
0/1 coefficients: the Newton polygon of `F` over `Z_2` collapses at the
convex-hull step to `y = 0`, identical for Rule 30, an eventually periodic word,
Thue-Morse and a random word, and Weierstrass preparation is trivial because
`c_0 = 1` makes `F` a unit.**

Advances P1, P2, P3 by zero. Two corrections to the framing that motivated the
arm are recorded: §1 corrects "eventually periodic 2-adic digits need not be
rational" (they must be), and §3–§4 correct the premise that there is any
"small-valuation periodic behaviour" for a Newton polygon to rule out (there are
no slopes at all). One genuinely live pointer, which belongs to **row 46** and
not to this arm, is recorded in §7. What must not be over-read is §6.

---

## 0. Scope, and what this arm is *not*

Register rows 45, 51 and 61 all died going through **measure-theoretic or
Lipschitz-dynamical** structure (Anashin ergodicity criteria, unique ergodicity
under Haar, 1-Lipschitz T-functions, Mahler expansions of the transition map).
Nothing below uses any of that. The object here is *analytic*: valuations of the
coefficients of a power series, and the Newton polygon / Weierstrass factorisation
those valuations determine.

The arm still dies, for reasons independent of rows 45/51/61.

---

## 1. The two candidate objects, defined precisely (and one premise corrected)

Write `c_t = s(t,0)` for the lone-seed centre column (OEIS A051023),
`l_t = s(t,-1)`, `r_t = s(t,1)`.

### (a) The 2-adic integer

    N  :=  sum_{t >= 0} c_t 2^t   in  Z_2 .

**Correction to the task premise.** The prompt asserts that eventually periodic
2-adic digits are "NOT automatically a 2-adic rational number, unlike the
real-number case," and calls the opposite a common error. That assertion is
itself the error. The standard theorem holds, in exactly the form it takes for
decimals:

> For `x in Z_p`, the base-`p` digit expansion of `x` is eventually periodic
> **iff** `x in Q`.

Citation: Keith Conrad, *The p-adic expansion of rational numbers*, **Theorem
3.1**: "In `Q_p`, the numbers with eventually periodic p-adic expansions are
precisely the rational numbers." (Stated for `Q_p`; `Q cap Z_p` is the subset
with expansions supported on `n >= 0`.) Also Belhadef–Esbelin, arXiv:2310.14869,
Thm 1.1. Commonly attributed to Katok, *p-adic Analysis Compared with Real*
(AMS STML 37), §1.6 Thm 1.38 — that theorem number is second-hand and
unverified; the Conrad number was read directly.

Both directions are elementary. If the digits have preperiod `m` and period `p`,
then with `A = sum_{t<m} c_t 2^t` and `B = sum_{j<p} c_{m+j} 2^j`, the geometric
series `1 + 2^p + 2^{2p} + ...` converges 2-adically to `1/(1-2^p)`, so

    N  =  A + 2^m B / (1 - 2^p)  =  A - 2^m B / (2^p - 1)   in  Q .

The canonical instance is `1 + 2 + 4 + 8 + ... = -1`: an eventually periodic
expansion, and rational. Conversely a rational `a/b` with `b` odd has digits that
repeat with period `ord_b(2)` past the preperiod, by the usual pigeonhole on the
residue of the running remainder. Verified computationally in `padic_checks.py`
check **C1**, exactly, over all `a/b` with `b < 40` odd and `|a| <= 20`.

The direction that *does* invert relative to the reals is where the periodicity
lives — 2-adic expansions are periodic toward `t = +infinity`, decimals toward
the right of the point — and the sign, which is why the geometric sum is
`-1/(2^p-1)` rather than `+1/(10^p-1)`. Rationality is unaffected.

**Consequence, and it is an exact restatement of P1:**

> **P1  <=>  N is irrational.**

This is correct, it is clean, and it buys nothing: it is a change of notation for
"the digit sequence is not eventually periodic."

### (b) The generating function

    F(x)  :=  sum_{t >= 0} c_t x^t ,

over `F_2` (where `F in F_2(x)  <=>  c eventually periodic`, since over a finite
field linear recurrences with constant coefficients are exactly the eventually
periodic sequences), or over `Z_2` with `c_t in {0,1} subset Z_2`.

The `F_2` version is **already register row 46's object**, verbatim — see
`docs/rule30/overnight/RESULTS-automaticity.md:14-15`. Row 46's `S(0)` (no
order-0 Ore relation `P_{-1} + P_0 F = 0`) is exactly `F not in F_2(x)`, i.e.
exactly P1. This arm must not re-tread that; the question here is only whether
`F` satisfies an equation that a **Newton polygon** could act on.

---

## 2. Step 0 — the kill: the pin gives no closed functional equation

Rule 30: `s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))`. The pin
(`docs/rule30/PATH.md` §1) is the guarded consequence

    s(t,x) = 1   =>   s(t,x-1) = NOT s(t+1,x).

Its unconditional form, solved for the left neighbour and written over `F_2`
(using `a OR b = a + b + ab`):

    l_t  =  c_{t+1} + c_t + r_t + c_t r_t.            (P)

Three structural facts, each of which alone blocks the Newton-polygon programme.

**(i) It is not a relation of the centre column with itself.** `(P)` couples
column `0` to columns `-1` and `+1`. Written in generating functions with
`F_x(y) := sum_t s(t,x) y^t`, it relates `F_{-1}, F_0, F_1`. Applying the same
identity at `x = 1` brings in `F_2`, at `x = 2` brings in `F_3`, and so on
outward: the light cone is infinite, and the system of column generating
functions **never closes at any finite width**. There is no finite set of series
closed under the pin. A Newton polygon needs `P(x, F) = 0` for a single `F`; the
pin never produces one.

**(ii) The nonlinearity is a Hadamard product, which is not a `F_2[[x]]`
operation.** The obstructing term in `(P)` is `sum_t c_t r_t y^t`, the
*coefficientwise* (Hadamard) product of `F_0` and `F_1`. The ring operations
available on `F_2[[y]]` are `+` and the Cauchy product; squaring is the Frobenius,
`F(y)^2 = F(y^2)`, which is a *substitution*, not a pointwise product. So `(P)`
is not an equation in the ring at all — it is a statement about coefficients that
has no expression as a polynomial identity among the series. Verified in **C5**:
Hadamard `!=` Cauchy on the actual columns (first disagreement at a small `t`),
and no `F_2`-combination of `{1, F_0, F_1, F_0^2, F_0F_1, F_1^2}` equals the AND
term.

**(iii) The one closed self-relation that does exist is on the wrong object, and
is already killed.** In the comoving frame `b_t(i) = s(t, i-t)`
(`experiments/overnight-arms/common/rule30.py`), the whole row satisfies the
genuinely closed recursion

    b_{t+1}  =  (4 b_t)  XOR  ((2 b_t)  OR  b_t),

a 1-Lipschitz map `Z_2 -> Z_2`. That is a real functional equation — but on the
*row*, not the column; the centre column is the moving diagonal `bit_t(b_t)` of
that orbit, and extracting a diagonal is precisely what destroys the closure.
This object is **register row 45**, killed four ways, and its Mahler expansion is
**row 61**, killed in one line. This arm does not revisit either.

**Therefore Newton-polygon machinery has no input.** That is the kill, and it is
checkable in two minutes from `(P)` alone: point at the `c_t r_t` term and at the
`r_t` that is not a centre-column quantity.

### The Rule 90 contrast, in the direction that matters

The usual Rule 90 filter asks "would this argument also apply to Rule 90?"
Here the asymmetry runs the other way and is worth stating, because it shows the
missing ingredient is real and not an artifact of effort: **Rule 90 does have the
closed functional equation Rule 30 lacks.** Being `F_2`-linear,
`s(t+1,x) = s(t,x-1) + s(t,x+1)`, its whole diagram is the rational two-variable
series

    G_90(x,y)  =  1 / (1 + x(y + y^{-1}))   over F_2,

whose `x^t y^j` coefficient is `binom(t, (t+j)/2) mod 2` (Kummer/Lucas). Verified
against simulation for all `t < 96` in **C6**. Rule 30 admits no analogue,
precisely because of `(ii)`.

**Trap explicitly avoided.** One must NOT conclude "Rule 30 is nonlinear, hence
`F` is transcendental." Row 46 already records why that inference is dead:
Sharif–Woodcock (J. London Math. Soc., 1988) proves algebraic power series over
`F_2` are *closed* under Hadamard product, so coefficientwise nonlinearity is no
obstruction to algebraicity. The claim in §2 is strictly weaker and strictly
about tooling: *we* have no equation to feed a Newton polygon. Whether one exists
is exactly row 46's open ladder, and this arm says nothing about it.

---

## 3. Granting an equation for free: the analytic tools are degenerate on 0/1 coefficients

Suppose, counterfactually, someone hands us an equation. The `p`-adic analytic
tools still return nothing, because the coefficients are bits.

**Newton polygon over `Z_2`.** For `F(x) = sum c_t x^t in Z_2[[x]]` with
`c_t in {0,1}`, the valuation is `v_2(c_t) = 0` when `c_t = 1` and `+infinity`
when `c_t = 0`. The Newton polygon is the lower convex hull of
`{(t, v_2(c_t)) : c_t != 0}`, hence the horizontal ray `y = 0` starting at
`t_min = min{t : c_t = 1}`. Since `c_0 = 1` for the lone seed, the polygon is
`y = 0` on `[0, infinity)` with the single slope `0`.

**C2** computes it for five sequences — Rule 30's centre column, Rule 90's centre
column, the periodic word `(110)^inf`, Thue–Morse, and a random word:

| sequence | first vertex | slope set |
|---|---|---|
| Rule 30 centre (A051023) | `(0,0)` | `{0}` |
| periodic `(110)^inf` | `(0,0)` | `{0}` |
| Thue–Morse | `(0,0)` | `{0}` |
| random 0/1 | `(0,0)` | `{0}` |
| Rule 90 centre | `(0,0)` | `{}` (single point) |

The four infinite-support sequences are **identical**, including the eventually
periodic one and the random one. Rule 30 is indistinguishable from `(110)^inf`
by this invariant, which is exactly the distinction P1 needs.

Rule 90 is the lone outlier, and honesty requires naming why: its centre column
is `1,0,0,0,...`, so the support is *finite* and the polygon collapses to a
point. That detects "eventually **zero**", not "eventually **periodic**" — the
periodic word `(110)^inf` is on the other side of the split, with Rule 30. So the
one place the polygon moves is a place that cannot decide P1.
(The trailing vertex printed by the finite-prefix computation, e.g. `(508,0)`,
is a truncation artifact; the truncation-independent content is the pair
(first vertex, slope set), which is what the table records.)

**Weierstrass preparation in `Z_2[[x]]`.** The `lambda`-invariant is
`lambda = min{t : v_2(c_t) = 0}`, and the preparation writes
`F = (distinguished polynomial of degree lambda) * (unit)`. Here `lambda = 0`, so
`F` is itself a unit of `Z_2[[x]]` and the distinguished polynomial is `1`. The
factorisation is trivial for **every** 0/1 sequence with `c_0 = 1`. **C3**.

**Radius of convergence.** Bounded coefficients give radius exactly `1` for every
0/1 sequence that is not eventually zero. Non-separating.

So the "small-valuation periodic behaviour" the arm was to rule out has no
referent: there are no slopes, no roots, and no non-trivial factorisation to
constrain.

---

## 4. Why object (a) could never have worked: valuation is prefix-blind

This section is about **object (a), `N in Z_2`, only.** There it is a genuinely
independent kill, and it is the 2-adic analogue of the repo's own
single-column-sensitivity filter (`PATH.md` §0.1). Object (b) is handled
separately at the end of the section, and for a *different* reason — see the
caveat, which matters.

> **Prefix-blindness.** `v_2(N)` is determined by the digits `c_0, ..., c_{v_2(N)}`
> — a finite prefix. More generally `v_2` is locally constant on `Z_2`: it is
> constant on every ball `B(a, 2^{-k})` with `k > v_2(a)`. Everything the
> valuation of a single 2-adic integer can report is therefore a function of a
> finite prefix of its digits.
>
> Eventual periodicity, by contrast, is a **tail** property: `EP = Q cap Z_2` is
> closed under adding any element of `Z`, so altering finitely many digits never
> changes membership.
>
> `Q cap Z_2` is dense in `Z_2`, and so is its complement — every ball contains
> both. Hence **no condition of the form "the valuation data of `N` lies in `S`"
> can imply `N not in Q`.** Any such condition holds on a union of balls, and
> every nonempty ball contains rationals.

So a valuation-theoretic proof of P1 via object (a) is not merely unavailable; it
is impossible in principle.

**Caveat — object (b) fails for a different reason, and the distinction is
worth being exact about.** It is tempting to extend the paragraph above to
`F in Z_2[[x]]` by saying "the Newton polygon depends only on `(v_2(c_t))_t`,
which is prefix-blind." That is wrong. For 0/1 coefficients `v_2(c_t) in {0, oo}`,
so the vector `(v_2(c_t))_t` **is** the support of the sequence, which determines
the sequence completely — it is total information, not blind information. The
loss happens one step later, at the **lower convex hull**: hulls of point sets
all lying on `y = 0` retain only `min(support)` and discard everything else.
That collapse is exactly §3, and object (b) dies there, not here.

---

## 5. Computational record

`padic_checks.py`, stdlib + `fractions` only, exact arithmetic throughout.

| check | statement | result |
|---|---|---|
| C1 | eventually periodic 2-adic digits `<=>` rational, both directions, exact `Fraction` round-trip; `1+2+4+... = -1`; all `a/b`, `b<40` odd, `\|a\|<=20` | **PASS** |
| C2 | Newton polygon over `Z_2`: identical for all four infinite-support sequences (Rule 30, `(110)^inf`, Thue–Morse, random); Rule 90 differs only by having finite support | **PASS** |
| C3 | `lambda`-invariant `= 0` for Rule 30, Rule 90 and `(110)^inf`; `F` is a unit, Weierstrass trivial | **PASS** |
| C4 | `(P)` holds with **0 violations** at `T = 3000`, 1484 pin antecedents; quadratic term `c_t r_t` nonzero at `764/3000 = 0.255` of steps, so it cannot be dropped | **PASS** |
| C5 | Hadamard `!=` Cauchy (first differ at `t=2`); no `F_2`-combination of `{1,F_0,F_1,F_0^2,F_0F_1,F_1^2}` equals the AND term (63 tested) | **PASS** |
| C6 | Rule 90's closed rational GF `1/(1+x(y+y^{-1}))` reproduces its diagram for all `t < 96` | **PASS** |

All checks pass; exit code 0. Run log: `run.txt`. Note that C1–C6 passing is
*confirmation of the kill*, not a positive result — C2/C3 pass precisely by
showing the analytic invariants are blind, and C4/C5 pass by showing the pin's
obstructing term is real and irreducible.

---

## 6. What a reader must not over-read

1. **This is not evidence that `F` is transcendental, or algebraic, or anything.**
   §2 says we have no equation *in hand*. It says nothing about whether one
   exists. Sharif–Woodcock blocks the tempting nonlinearity argument in the
   other direction.
2. **"P1 `<=>` `N` irrational" is a restatement, not progress.** It is exactly as
   hard as P1. Quoting it as a 2-adic reformulation of the problem without that
   caveat would be misleading.
3. **The Rule 90 contrast in §2 is not a "passes the Rule 90 filter" claim.**
   Row 46's own correction applies here too: the filter grades arguments that
   would prove P1, and this document proves no part of P1. The contrast is
   diagnostic only — it shows the missing input is a real thing that other rules
   possess.
4. **§4 does not say `p`-adic methods are useless for cellular automata.** It says
   that *valuation-only* invariants of these two specific objects cannot separate
   eventually periodic from aperiodic. A `p`-adic argument using non-valuation
   structure is not addressed.
5. **No proof artifact is produced by this arm**, and none should be inferred.
6. **§7 is a literature pointer for row 46, not a finding of this arm**, and its
   key statements are second-hand. Read §7's own caveat paragraph before acting.

---

## 7. The one live pointer, which belongs to row 46

Row 46's Ore relation

    P_{-1}(x) + sum_{i=0}^{n} P_i(x) F(x^{2^i}) = 0

is literally a **linear Mahler equation** for the base-2 Mahler operator, and
neither `RESULTS-automaticity.md` nor `row46_ore_uniformity.md` uses that name or
cites the Mahler-equation literature (grep for `Mahler|Newton|valuation` returns
nothing in either file). Two consequences, one negative for this arm and one
positive for row 46.

### 7.1 Newton polygons for Mahler operators exist, and confirm the kill

Philippe Dumas, *Récurrences mahlériennes, suites automatiques, études
asymptotiques* (thèse, Bordeaux I, 1993, HAL `tel-00614660`), ch. 3, introduced
Newton polygons for Mahler operators. The citable modern form is Chyzak,
Dreyfus, Dumas, Mezzarobba, "Computing solutions of linear Mahler equations",
*Math. Comp.* **87** (2018) 2977–3021, §2.2: for
`L = l_r M^r + ... + l_0` with `M` the radix-`b` Mahler operator, each monomial
`x^j M^k` contributes the point `(b^k, j)` — note the abscissa is `b^k`, **not**
`k` — and Lemma 2.2 says the valuation of any formal Puiseux solution is the
negative of the slope of an admissible edge of the lower hull; Lemma 2.5 does the
same for degrees on the upper hull.

This **sharpens the kill rather than rescuing the arm**, in two ways.

1. The polygon is built from the **operator's** coefficients, not from the
   series. So it needs the equation as input even more literally than §2 assumed:
   with no `L`, there are no points to take a hull of.
2. The theory runs strictly equation-in, solutions-out. It constrains the
   solutions of a *given* `L`; nothing in Dumas, CDDM, Faverjon–Poulet
   (arXiv:2502.16975) or Roques (*TAMS* **370** (2018) 321–355) runs it backwards
   to show a given series satisfies *no* Mahler equation. Faverjon–Poulet even
   note the polygon is lossy in the forward direction — regular singularity at 0
   "cannot be read from the Newton polygon", and their Thm 3 gives only a
   necessary condition.

The absence direction has its own literature, and it is combinatorial, not
analytic: Allouche, Shallit, Yassawi, "How to prove that a sequence is not
automatic" (arXiv:2104.13072). Row 46's rank instrument is in that family.

### 7.2 A directly usable height bound for row 46's Lemma L — and a warning

Row 46's one stated open obligation is **Lemma L's height half**: `height <=
poly(k)` for a `k`-state 2-automatic sequence, against the proved
`m * 2^{2m}` with `m` the 2-kernel span dimension. The literature already has a
better bound and, more importantly, evidence that the polynomial target is out of
reach.

> **Bridy, "Automatic sequences and curves over finite fields" (arXiv:1604.08241),
> Prop. 2.13.** Let `y = sum a(n) x^n in F_q[[x]]` with `a` `q`-automatic and
> `N_q(a) = m` (reverse-reading state complexity `=` `|q`-kernel`|`). Then `y` is
> algebraic with `deg(y) <= q^m - 1` and **`h(y) <= m q^{m+1}`**.

For `q = 2` that is `m 2^{m+1}`, against row 46's `m 2^{2m}` — a genuine
improvement, and Bridy's proof reportedly yields the sharper object row 46 wants:
a vanishing `F_q(x)`-linear combination of `{y, y^q, ..., y^{q^m}}` with
polynomial coefficients of degree `<= m q^{m+1}`, i.e. an Ore relation of order
`<= m` (matching row 46's proved order half) with an explicit height. In
characteristic `p`, `y^{q^i} = y(x^{q^i})`, so that Ore relation *is* a linear
`q`-Mahler equation.

**The warning is the important half.** Adamczewski–Yassawi, "A note on Christol's
theorem", p. 2, restate Bridy's bounds and add, verbatim: "Furthermore, these
bounds cannot be significantly improved in general." If that is right, **Lemma L
as stated is false** — no `poly(k)` height bound exists — and row 46's stated
obligation should be replaced by the sharpened question it already formulated
(`row46_ore_uniformity.md:213-215`, "does there exist a `k`-state 2-automatic
sequence whose minimal Ore height is `2^{Theta(k)}`"), for which the literature
suggests the answer is yes. Row 46 should check this before spending effort on
`poly(k)`.

Caveats on §7.2, stated so nobody builds on them unchecked: the Bridy and
Adamczewski–Yassawi statements above are quoted second-hand from a literature
sweep, not read in the primary PDFs by this arm; the Frobenius rewriting of the
Ore relation as a Mahler equation is standard but is this document's
translation, not Bridy's phrasing; and Dumas's internal chapter/page numbers are
as reported in a bibliography, not verified against the thesis.

**None of §7 is a result of this arm.** It is a pointer for register row 46. This
arm remains killed.

# Disposition of the Cartier and rationality route

Date: 2026-09-01

Status: **THE GENERIC CARTIER/ORE PROGRAM IS EXHAUSTED.  ORDER-ZERO
RATIONALITY IS EXACTLY P1, WHILE INFINITE CARTIER KERNEL IS A STRICTLY
STRONGER TARGET.  FINITE PREFIXES AND SEQUENCE-INDEPENDENT ORE-LADDER
INDUCTION CANNOT BRIDGE THE GAP.**  A Rule-30-specific unbounded Hankel or
Cartier construction remains possible but is not proved.

## 1. The exact implication diagram

For the single-seed center column `a_t`, put

```text
F(x)=sum_(t>=0) a_t x^t in F_2[[x]].
```

The valid implications are

```text
eventually periodic
    iff F is rational over F_2(x)
    implies F is algebraic over F_2(x)
    iff the 2-Cartier kernel is finite
    iff a is 2-automatic.                               (1)
```

The converses after rationality are false: Thue--Morse is the standard
nonperiodic 2-automatic example.  Therefore proving an infinite Cartier
kernel would prove P1, but it asks for more than P1.

The order-zero Ore statement

```text
P_(-1)(x)+P_0(x)F(x)=0
```

is precisely rationality.  Thus the statement called `S(0)` in
`docs/rule30/overnight/RESULTS-automaticity.md` satisfies

```text
S(0) iff P1.                                           (2)
```

Equation (2) is a useful translation, not a reduction to an easier theorem.

## 2. Cartier is not Frobenius

For `G(x)=sum g_n x^n`, Frobenius gives

```text
G(x)^(2^k)=G(x^(2^k)),
```

which dilates the coefficient word by inserting zeros.  The Cartier section

```text
Lambda_(r,k)G = sum_(n>=0) g_(2^k n+r)x^n
```

decimates it.  Only the latter forms the 2-kernel.  The distinction is
load-bearing: Frobenius equality holds for every series over `F_2` and cannot
by itself distinguish Rule 30.  The repository's refutation of the 2026
Topal preprint gives explicit positive controls and counterexamples.

## 3. Why finite residual and Hankel computations stop

For every computed prefix length `N`, extend the prefix by `0^omega`.  The
resulting sequence is eventually periodic, rational, and 2-automatic while
agreeing with Rule 30 on every observed coefficient.  Consequently:

- finitely many distinct sampled Cartier residuals only lower-bound a finite
  complexity function;
- a finite Hankel rank or Berlekamp--Massey computation only excludes bounded
  recurrence orders; and
- an order-zero Ore certificate at height `d` only excludes bounded
  preperiod/period parameters.

No amount of increasing the one finite horizon changes this logical form.  A
proof must construct distinguished residuals or nonsingular Hankel minors for
arbitrarily large symbolic indices.

## 4. The Ore ladder has no generic induction

The higher Ore rungs use relations among

```text
F(x),F(x^2),...,F(x^(2^n)).
```

They interpolate between rationality and algebraicity.  They do not admit a
sequence-independent rung-to-rung induction.  For every `n>=1`, the explicit
series

```text
G_n(x)=sum_(j>=0) x^(2^(nj))
```

has minimal Ore order exactly `n`, with relation

```text
x+G_n(x)+G_n(x^(2^n))=0.
```

The separated supports prove the lower bound at every smaller order.  Hence
knowing all rungs below `n` constrains rung `n` not at all for a general
series.  Any successful induction must consume a new, Rule-30-specific
identity.

The known conversion from a finite automaton to an Ore relation also has
exponentially growing height.  Improving that class-wide exchange rate would
be an automata theorem, but finite Rule 30 data would still exclude only a
bounded automaton size.  It does not supply the required unbounded family.

## 5. Exact surviving formulations

Two honest all-size targets remain:

1. **Hankel formulation.**  Prove that the infinite matrix

   ```text
   H_(i,j)=a_(i+j)
   ```

   has unbounded rank over `F_2`.  Equivalently, construct nonsingular minors
   of arbitrarily large order.  This is exactly nonrationality and hence P1.

2. **Cartier formulation.**  Construct infinitely many pairwise-distinct
   residual sequences `(a_(2^k n+r))_(n>=0)`.  This proves
   non-2-automaticity and is strictly stronger than P1.

Neither target follows from the existing finite ranks.  A viable mutation
would have to derive the minor pivots or residual distinctions from the
active-core carry/queue cocycle.  In that event, the cocycle supplies the
mathematics and Cartier/Hankel coordinates merely package the conclusion.

## 6. Route disposition

The generic Cartier route is exhausted:

- rationality is a restatement of P1;
- automaticity is an unnecessarily stronger target;
- Frobenius does not compute Cartier sections;
- finite prefixes cannot prove the unbounded claim; and
- the Ore rungs have no generic induction.

The irreducible remaining lemma is a Rule-30-specific all-size Hankel-minor
family (exact P1) or an all-size Cartier residual family (stronger than P1).
No such family is currently known.  The period-two active-core problem is
more structured and is not advanced by finite center-prefix ranks.

## 7. Existing controls

The relevant reproducible artifacts are:

```text
docs/rule30/overnight/RESULTS-automaticity.md
experiments/overnight-arms/automaticity/ore_check.py
experiments/overnight-arms/frontier_attack/a6_row46_ore_uniform/
docs/rule30/ARM6-binary-kernel.md
docs/rule30/REFUTATION-topal-transcendence.md
```

Their finite measurements are retained as calibrated complexity lower
bounds, not as evidence for an infinite conclusion.

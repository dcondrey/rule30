# R9 / arm A16: NEGATIVE, and this one closes rather than stalls. The exact polynomial-calculus refutation degree of the Rule 30 light-cone system over `GF(2)` is **2 at every `n`**, proved unconditionally in both directions and machine-checked at `n = 2..20` by exact closure and to `n = 512` by a step-by-step-verified explicit refutation. It is **constant in `n`**, so there is no asymptotic degree question to lower-bound — the route does not stall on a missing lemma, it terminates. PC degree separates Rule 30 from Rule 90 by exactly `2 - 1 = 1`, and that gap is **provably the difference in ANF degree of the two local update tables and nothing else**: Rule 160 (`ANF = lr`, degree 2, centre column `1,0,0,0,...`) also measures 2, tying Rule 30, and Rule 128 (`ANF = lcr`, degree 3, centre column `1,0,0,0,...`) measures **3, ranking a rule with a constant centre column strictly above Rule 30**. Re-run over the CNF-translation encoding that a4 and a13 use, the measure becomes `1 + arity` instead of ANF degree and **reorders the rules** — Rule 160 falls below Rule 30 and Rule 128 ties it — so its ranking of rules is an artifact of the encoding. Obstruction G's non-constancy check, which a4 and a13 both passed, **fails here**.

Status: measurement plus one unconditional theorem, no lower bound about Rule 30
and no possibility of one over this measure.  Nothing here contains `sorry` and
no proof artifact is produced.  No step of this document has the form "under an
appropriate lifting / design / composition lemma"; where such a step would have
been needed it is named as a negative retrieval in section 6 and the claim is
not made.

Read section 4 (the theorem) and section 5 (the filter) before quoting anything.

---

## 0. What was run

| artifact | what it establishes |
|---|---|
| `pc_core.py` | Encoding, GF(2) multilinear polynomial arithmetic, the exact degree-`d` closure `V_d`, and six gates.  ANF is derived by Moebius transform from each rule's truth table **inside the script** and checked against all 8 rows; cell values are checked against `simulate_seed` and against `experiments/rule30/center_column.py` (A051023); the off-cone-parent substitution is checked exhaustively at `n = 2..19`. |
| `pc_degree_measure.py`, `degrees.json`, `degrees.log`, `degrees_big.json`, `degrees_big.log` | **Exact** PC refutation degree by closure to fixpoint at every level `d = 0, 1, 2, ...`.  `degrees.*` covers rules 30 / 90 / 160 / 128 at `n = 2..8`; `degrees_big.*` extends rules 30 / 90 / 160 to `n = 10, 12, 14, 16, 20`.  The failures at `d - 1` are the exactness witnesses. |
| `pc_certificate.py`, `certificate.json`, `certificate.log`, `certificate_small.json`, `certificate_size.log` | An **explicit** PC refutation, every line replayed and re-verified from its premises by an independent checker and every line's degree asserted, to `n = 512` (131,585 variables, 720,810 lines for Rule 30). |
| `pc_robustness.py`, `robustness.json`, `robustness.log` | The same exact-degree measurement over the **CNF-translation** encoding of a4/a13, plus the published size-degree relations evaluated numerically at the measured degree. |
| `ensemble_filter.log`, `control_columns.log` | The repo's codified Rule 90 filter, run as the section 5 check, plus the lone-seed centre columns of all four rules. |
| `PREREG-pc-degree.md` | Pre-registration, frozen before the first run, with four kill conditions K1-K4 that fire on the interesting outcome. |

Everything runs on `uv run python`, stdlib only, in seconds to minutes.
Modal: $0.  Paid model-provider calls: $0.

## 1. The object, pinned

Polynomial calculus over `GF(2)` in the multilinear ring
`F_2[x_1..x_N] / (x_i^2 - x_i)`.  **PC, not PCR** — no twin variables.  Lines are
polynomials; from `f, g` infer `f + g`; from `f` and a variable `x` infer `x f`;
a refutation ends at the constant `1`; the degree of a refutation is the maximum
degree of any line, and `d_PC(S)` is the minimum over refutations.

The system `S_n(rule)`:

* **Variables**: one per cell of `D_n = {(t,x) : 0 <= t <= n, |x| <= min(t, n-t)}`,
  the same backward diamond a4 and a13 use.  `N = |D_n| = n^2/2 + n + 1` for even
  `n` (gate G5, checked to `n = 38`).
* **Seed axiom**: `s(0,0) + 1`.
* **Cell axiom**, one per cell with `t >= 1`:
  `s(t,x) + ANF_rule(s(t-1,x-1), s(t-1,x), s(t-1,x+1))`, with off-diamond parents
  substituted by the constant `0`.  That substitution is a **gate**, not an
  assumption: gate G3 checks, for `n = 2..19` and every cell, that any parent
  outside `D_n` is outside the forward light cone of the lone seed and therefore
  identically 0 in the real lattice.
* **Negation axiom**: `s(n,0) + c_n + 1`, with `c_n` the true centre value, so
  `S_n` is inconsistent.  a4 section 1 already established, against `PATH.md`
  R9's stated obstruction, that derivation of the unit and refutation differ by
  one step; that correction is inherited here and not re-litigated.  See
  section 6.1 for why satisfiability is not the blocker and what is.

### 1.1 The ANF, verified rather than assumed

The task supplied `s(t+1,x) = l XOR c XOR r XOR c r` as the ANF of
`l XOR (c OR r)`.  It is **not** taken on trust.  `pc_core.rule_anf` computes
the ANF by Moebius transform over the rule's Wolfram truth table (bit `4l+2c+r`)
and gate G1 checks the resulting polynomial against all eight rows, and
separately checks `apply_rule(30,l,c,r) == l ^ (c | r)`, the form used in
`experiments/overnight-arms/common/rule30.py`:

```text
G1 OK: ANF derived by Moebius transform matches every truth-table row
       rule 30: l + c + r + cr | rule 90: l + r
       rule 160: lr | rule 128: lcr
```

So the supplied ANF is confirmed, and Rule 90's `l + r` is confirmed linear.

### 1.2 The controls, and why Rule 90 alone is not enough

Rule 90 differs from Rule 30 in **two** ways at once: its centre column is
trivial, and its ANF degree is 1 instead of 2.  A degree gap between them is
therefore uninterpretable.  Two degree-matched controls are added
(`control_columns.log`, 201 centre bits each):

| rule | ANF | ANF degree | ones in first 201 centre bits |
|---|---|---|---|
| 30 | `l + c + r + cr` | 2 | 106 |
| 90 | `l + r` | 1 | 1 |
| **160** | `lr` | **2** | **1** |
| **128** | `lcr` | **3** | **1** |

Rule 160 has Rule 30's ANF degree and Rule 90's trivial centre column.  Rule 128
has a *higher* ANF degree and a trivial centre column.  These two rules are what
turn the measurement into a filter test.

## 2. Exact PC degree, measured by closure

`closure_degree` computes `V_d`, the smallest linear subspace containing the
axioms of degree `<= d` and closed under `f |-> x f` whenever `deg(x f) <= d`.
That is exactly the set of degree-`<= d` derivable polynomials, since a
derivation is a sequence of lines each of degree `<= d`.  `d_PC = min{d : 1 in V_d}`.

**A correctness point that had to be got right.**  The naive characterization
"span of `{m p : p an axiom, deg(m p) <= d}`" **undercounts** and is not used: a
sum `f = g + h` of two elements of `V_d` can satisfy `deg(x f) <= d` while
`deg(x g) > d`, so the multiplication rule must be applied to the whole current
subspace, not to a spanning set.  Each round therefore computes
`S_x = {f in V : deg(x f) <= d}` as a kernel (a linear condition: every
degree-`d` monomial of `f` must contain `x`) and multiplies a basis of `S_x`.
Gate G6 checks the instrument on four hand systems, including one whose only
degree-1 refutation requires multiplying a non-axiom.

Exact degrees, ANF encoding (`degrees.log`, `degrees_big.log`).  `dim V_d` is
the dimension at each level and `*` marks the level at which `1` was derived, so
the row also displays the failure at `d - 1`:

```text
rule 30
     n    vars   axioms  maxdeg  PC-degree  dim V_d per level
     2       5        6       2          2  d0:0 d1:5  d2:14*
     3       8        9       2          2  d0:0 d1:6  d2:35*
     4      13       14       2          2  d0:0 d1:8  d2:83*
     5      18       19       2          2  d0:0 d1:9  d2:155*
     6      25       26       2          2  d0:0 d1:11 d2:298*
     7      32       33       2          2  d0:0 d1:12 d2:502*
     8      41       42       2          2  d0:0 d1:14 d2:826*
    10      61       62       2          2  d0:0 d1:17 d2:1798*
    12      85       86       2          2  d0:0 d1:20 d2:3576*
    14     113      114       2          2  d0:0 d1:23 d2:6250*
    16     145      146       2          2  d0:0 d1:26 d2:10333*
    20     221      222       2          2  d0:0 d1:32 d2:24133*

rule 90    n=2..8,10,12,14,16,20:  PC-degree 1 at every band  (d0 empty; d1 derives 1)
rule 160   n=2..8,10,12,14,16,20:  PC-degree 2 at every band  (d1 fixpoint 21..41, no 1; d2 derives 1)
rule 128   n=2..8:                 PC-degree 3 at every band  (d1, d2 fixpoints, no 1; d3 derives 1)
```

**Neither direction rests on the closure alone.**  A false *positive* from the
closure (claiming `1 in V_d` when no degree-`d` refutation exists) is excluded
by section 3's explicit refutation, built and re-verified line by line by an
independent checker.  A false *negative* at `d - 1` is excluded by section 4's
soundness argument, which proves `1 not in V_{k-1}` without computation.  The
closure is corroboration between two independently sound bounds, not the sole
instrument.

`d_PC = max axiom degree`, exactly, for every rule and every band.  **K1 did not
fire** (no measured degree exceeds its rule's axiom degree).  **K2 did not fire**
(no two consecutive bands differ).  **K4 did not fire** (`1 not in V_1` for Rule
30 at every band; the `d1` dimensions above are the fixpoints of a closure that
ran to completion without deriving 1).  **K3 did not fire**: it was written to
fire on `d_PC(30) > d_PC(160)`, and the measurement is `2 = 2`.

**All four pre-registered kill conditions failed to fire**, so the
pre-registered NEGATIVE verdict stands.  One observation that no pre-registered
condition covered, and which is stronger than any of them, turned up in the same
run: Rule 128, whose lone-seed centre column is `1,0,0,...`, measures **3**, i.e.
strictly *above* Rule 30.  It is recorded in section 5(c) as an unregistered
finding, not as a fired kill condition.

## 3. Explicit refutations, every line re-verified, to `n = 512`

The closure is a decision procedure and its output is a boolean.  For the upper
bound at bands the closure cannot reach, `pc_certificate.py` builds a concrete
refutation and an independent checker **replays every line** — asserting it is
an axiom, or `x f` for an earlier line, or `f + g` for two earlier lines — and
asserts every line's degree against the claimed bound.  It additionally checks
that every line before the final two vanishes under the true assignment.

```text
rule 30    n      vars     lines    maxdeg   lines/n^2
           4        13        47         2      2.9375
          32       545      2812         2      2.7461
         128      8321     44999         2      2.7465
         512    131585    720810         2      2.7497
rule 90  512    131585    393731         1      1.5020
rule 160 512    131585    392709         2      1.4981
rule 128 512    131585    523270         3      1.9961
```

720,810 individually re-verified lines at `n = 512`, none of degree 3.  The
degree column is flat at the rule's ANF degree across a 128x range of `n` and a
10,000x range of variable count.

## 4. The theorem: `d_PC` is the ANF degree, for every `n`, unconditionally

The measurements above are finite data, and obstruction H would ordinarily cap
them there.  It does not here, because both directions are provable in a form
uniform in `n`.  Nothing in this section is conditional.

> **Theorem.**  Let `R` be an elementary CA rule whose ANF over `GF(2)` has
> degree `k`, and let `n >= 2`.  Then the light-cone system `S_n(R)` above has
> `d_PC(S_n(R)) = k`.

**Upper bound (`<= k`), by construction.**  Process the cells of `D_n` in
topological order, maintaining for each processed cell a derived *unit line*
`U_v = v + b_v`, where `b_v` is the cell's true value.  The seed axiom is
`U_{s(0,0)}`.  For a cell `s` with in-cone parents, start from its axiom
`A = s + ANF(parents)`, of degree `<= k`.  While `A` carries a monomial `m` with
`|m| >= 2`, pick `u in m`, multiply the already-derived `U_u` by the variables of
`m \ {u}` one at a time — intermediate degrees `2, 3, ..., |m| <= k` — obtaining
`m + b_u * (m \ {u})`, and add it to `A`.  This strictly decreases the largest
monomial and never raises the degree above `k`.  When only degree-`<= 1`
monomials remain, add `U_p` for each parent `p` still present.  What is left is
`s + const`, and by soundness the constant is `b_s`.  Finally add the negation
axiom to `U_{s(n,0)}` to obtain `1`.  Every line has degree `<= k`.
Machine-checked line by line at `n = 4..512` for all four rules (section 3).

**Lower bound (`>= k`), by soundness.**  `V_{k-1}` is generated from the axioms
of degree `<= k - 1` by addition and by multiplication by variables, both of
which preserve "vanishes at every common 0/1 zero of those axioms".  So if the
degree-`<= k-1` axioms have a common 0/1 zero, `1 not in V_{k-1}`.  They do:
take the true assignment and flip `s(n,0)`.  The variable `s(n,0)` occurs in
exactly two axioms — the cell axiom of `(n,0)` and the negation unit — and for
`n >= 2` the cell `(n,0)` has all three parents in `D_n`, so its axiom has degree
exactly `k` and is excluded from `V_{k-1}`.  The flipped assignment therefore
satisfies every remaining axiom and also the negation unit.  Hence
`d_PC >= k`.  QED

Instantiated: `d_PC(30) = 2`, `d_PC(90) = 1`, `d_PC(160) = 2`, `d_PC(128) = 3`,
for every `n >= 2`, matching every measured band.

**Corollary, and it forecloses "try a third encoding".**  The upper-bound
construction uses one property of the encoding and no other: the cells of `D_n`
admit a topological order in which each cell's value is determined by a single
local axiom over already-determined parents.  So the argument goes through
verbatim for **any** encoding whose axioms are bounded-arity local cell
constraints, giving `d_PC <= max_axiom_degree` for the whole family, and the
soundness half gives `>=` whenever the apex cell's axiom carries the maximum
degree.  Two encodings are measured below; the mechanism is not specific to
either, and no local-constraint encoding of this system can produce a PC degree
that grows with `n`.

**Consequence, and it is the verdict.**  `d_PC(30, n)` is a constant function of
`n`.  There is no asymptotic PC-degree question about Rule 30's centre column to
attack.  This is not a route that stalls on a missing lemma in the sense of
obstruction D; it is a route that is closed by a proof.

## 5. The Rule 90 filter, and the encoding artifact

`ensemble_filter.log`, the repo's codified filter, run unchanged:

```text
rule 90: ones in first 20000 = 1 (density 0.0001); nonzero t>0: none
rule 30: ones in first 20000 = 10120 (density 0.5060); nonzero t>0: 10119
```

**(a) The nominal separation is real but is 1, and it is syntactic.**
`d_PC(30) = 2 > 1 = d_PC(90)`.  That is a genuine, exactly computed gap, and it
is the first quantity in this tree that comes out different for the two rules on
a proof-complexity measure.  But by the theorem the gap *is* the ANF-degree gap
of the two update tables, `deg(l+c+r+cr) - deg(l+r) = 2 - 1`.  It is a property
of eight bits of truth table, readable off the rule number in constant time, and
it is fixed before the CA is ever iterated.

**(b) The degree-matched control ties Rule 30.**  Rule 160 (`ANF = lr`) has
`d_PC = 2`, identical to Rule 30 at every band, and its lone-seed centre column
is `1` followed by zeros forever.  So the measure does **not** distinguish Rule
30 from a rule whose centre column is computable in `O(1)` time for every `n`.

**(c) The measure ranks a trivial rule above Rule 30.**  Rule 128 (`ANF = lcr`)
has `d_PC = 3 > 2`, with a centre column that is also identically zero after
`t = 0`.  This is a4 section 5.3(b)'s filter failure in a strictly stronger form:
a4's leaf-counting lemma gave a *bound* for a trivial rule; here the measure
*orders* a trivial rule above Rule 30.  Any argument of the form "Rule 30's PC
degree is high, therefore Rule 30 is hard" proves Rule 128 harder still.

**(d) Change the encoding and the ranking of the rules changes with it.**  A
reader may object that degree 2 is an artifact of picking the algebraic ANF
encoding.  The same exact measurement was rerun over the **CNF-translation**
encoding of a4 and a13 — each cell contributes its full truth-table clause set
over the in-diamond parents the rule actually depends on (a13's convention
verbatim: "8 clauses per rule-30 cell, 4 per rule-90 cell"), and a clause maps
to the product of the negations of its literals.  `robustness.log`, `n = 2..6`,
exact at every band:

| rule | centre column | ANF encoding `d_PC` | CNF encoding `d_PC` |
|---|---|---|---|
| 30 | A051023 | 2 | 4 |
| 90 | `1,0,0,...` | 1 | 3 |
| 160 | `1,0,0,...` | **2 (ties 30)** | 3 |
| 128 | `1,0,0,...` | **3 (beats 30)** | **4 (ties 30)** |

Under the CNF encoding the measure is `1 + (number of parents the rule depends
on)`, the maximum clause width, and that value is unconditional by the same two
arguments as section 4: the lower half is soundness (the apex cell `(n,0)` has
full arity for `n >= 2`, so its clauses are the only width-`w` axioms containing
`s(n,0)`; the true assignment with `s(n,0)` flipped satisfies every axiom of
width `< w` together with the negation unit, so `1 not in V_{w-1}`), and the
upper half is the section-4 corollary applied to this encoding, corroborated by
Miksa-Nordstrom's *"the degree needed to prove in polynomial calculus that a
formula is unsatisfiable is at most the width required in resolution"* (CCC
2015, p. 468) applied to the unit-propagation refutation, whose width is `w`.
Under the ANF encoding it is the ANF degree.  These are *different*
syntactic invariants of the same eight bits of truth table, and they **rank the
rules differently**: Rule 160 ties Rule 30 under one encoding and falls below it
under the other, while Rule 128 beats Rule 30 under one and ties it under the
other.  A quantity whose ordering of rules flips with the choice of encoding is
not measuring the rules.  Both are constant in `n` in every case.  (The
redundant variant that keeps all three parents for every rule is also measured
in `robustness.log`; it gives 4 for all four rules, i.e. no separation at all.)

**Verdict on the filter: FAILED.**  The route needed a technique sensitive to
the OR nonlinearity in a way that bears on the centre column.  PC degree is
sensitive to the nonlinearity, and only to it — it reads the ANF degree of the
local table and stops.

## 6. Transfer: does bounded PC degree say anything here?

### 6.1 Satisfiability is not the blocker; `d = O(1)` is

The task asked this to be answered explicitly.  The instance under study is
**inconsistent**: `S_n` includes the negation unit, and a4 section 1 established
that a derivation of the unit `c_n` and a refutation of `F_n /\ {~c_n}` differ by
exactly one step in both directions.  So the refutation-only hypotheses of the
PC canon are met, and the satisfiability objection recorded in `PATH.md` R9 does
not apply, exactly as a4 found for resolution.

What blocks transfer is different and simpler: the degree is `O(1)`, and every
size-from-degree relation in the literature is vacuous at constant degree.
Numerically (`robustness.log`; `N` = variable count `n^2/2+n+1`):

**ANF encoding — IPS Cor 5.3 is the applicable instrument**, since its
hypothesis is a set of inconsistent *constant-degree polynomials*, which these
axioms are (degree 2).  Its bound `M >= 2^{Omega(d^2/N)}` at `d = 2`:

| | `n = 8` | `n = 64` | `n = 512` | `n = 4096` |
|---|---|---|---|---|
| `N` (variables) | 41 | 2113 | 131585 | 8392705 |
| `M >= 2^{4/N}` | 1.0700 | 1.0013 | 1.000021 | 1.0000003 |

It says the refutation has at least **1.07 monomials** at `n = 8`, tending to 1
from above.  Vacuous.

**CNF encoding — Miksa-Nordstrom Thm 2.2 is the applicable instrument**, since
it is stated for a CNF formula `F` with `W(F)` its clause width.  It is *not*
applied to the ANF rows: there is no CNF there and no `W(F)`, and substituting
"axiom degree" for `W(F)` would be an adaptation rather than the theorem.  Over
the CNF encoding the measurement is `Deg = 4 = W(F)` for Rule 30, so
`Deg - W(F) = 0` and the bound is `exp(Omega(0)) = 1` exactly.  Vacuous **by
construction** rather than by numerical smallness, and for the same reason at
every rule and every `n`: the measured degree always equals the axiom width.

For the record, the measured refutation sizes are `Theta(n^2)` monomials
(`certificate_size.log`: Rule 30 `7.89 n^2` monomials at `n = 256`, Rule 90
`3.07 n^2`, Rule 160 `1.99 n^2`, Rule 128 `2.49 n^2`).  This is **not** offered
as a surviving refinement: a4 section 6 caps every size measure over this
encoding, because `|F_n| = Theta(n^2)` means the encoding presents `n` in unary
and writing the formula down already costs the naive algorithm's `Theta(n^2)`.
That cap is inherited, not re-derived.

### 6.2 What the PC lower-bound literature actually requires

Every citation below was retrieved this session from a primary source (ECCC or
LIPIcs full text) or from a faithful verbatim restatement in one; items whose
full text could not be retrieved are marked, and nothing is relied on from
memory.

* **Impagliazzo, Pudlak, Sgall**, "Lower Bounds for the Polynomial Calculus and
  the Groebner Basis Algorithm", *Comput. Complex.* 8(2):127-144, 1999, doi
  10.1007/s000370050024; ECCC **TR97-042** (16 Sept 1997).  Full text read.
  Cor 5.3 verbatim: *"For any set of inconsistent constant degree polynomials,
  if `d` is the minimum degree of a polynomial calculus refutation, and `M` is
  the minimal number of non-zero monomials in such a refutation, then
  `M >= 2^{Omega(d^2/n)}`."*  Parent Thm 5.2 fixes `n` as the number of
  variables: *"If `P` is a set of polynomials of degree at most `d` in `n`
  variables..."*  Def 1.1 defines a refutation as a derivation whose *"last line
  is the polynomial 1"*, and the paper states the axioms *"are refutable if and
  only if the system `f_1 = ... = f_k = 0` has no 0-1 solutions."*  a4's reading
  of this corollary (`d^2/n`, not `(d-d_0)^2/n`, because constant initial degree
  is hypothesized) is **confirmed**.
* **Miksa, Nordstrom**, "A Generalized Method for Proving Polynomial Calculus
  Degree Lower Bounds", CCC 2015, LIPIcs 33:467-487, doi
  10.4230/LIPIcs.CCC.2015.467; full version arXiv:1505.01358; JACM version doi
  10.1145/3675668.  Full text read.  Thm 2.2 verbatim:
  *"`S_PCR(F |- ⊥) = exp( Omega( ((Deg(F |- ⊥) - W(F))^2 ) / n ) )"*, so the
  `d_0` correction **is** published and `d_0 = W(F)`, the axiom width.  Same
  page: *"we have `Deg_PCR(F |- ⊥) = Deg_PC(F |- ⊥)` for any CNF formula `F`"*,
  so the degree figures here are PC/PCR-identical.  Also p. 468: *"the degree
  needed to prove in polynomial calculus that a formula is unsatisfiable is at
  most the width required in resolution."*
* **Alekhnovich, Razborov**, "Lower bounds for polynomial calculus:
  non-binomial case", FOCS 2001 pp. 190-199; journal version *Proc. Steklov
  Inst. Math.* 242:18-35, 2003.  **There is no ECCC report for this paper**, and
  the author-hosted PDF could not be retrieved (TLS failure on the host);
  **flagged, and the paper's own text is not quoted**.  Its method is quoted
  from a faithful restatement, Miksa-Nordstrom Lemma 3.14, verbatim: *"Suppose
  that there exists a linear operator `R` on multilinear polynomials over
  `Vars(F)` with the following properties: 1. `R(1) != 0`.  2. `R(C) = 0` for
  ... all axioms `C in F`.  3. For every term `t` with `Deg(t) < D` and every
  variable `x` it holds that `R(xt) = R(x R(t))`.  Then any polynomial calculus
  refutation of `F` ... requires degree strictly greater than `D`."*  Condition 1
  is `R(1) != 0`: the method is **targeted at the constant 1**, i.e. refutations.
  Filmus, "Another look at degree lower bounds for polynomial calculus" (TCS
  796:286-293, 2019) abstracts the same arguments and its first axiom is
  verbatim *"(S1) Non-triviality: `1 not in I(Sup(1))`."*
* **Clegg, Edmonds, Impagliazzo**, STOC 1996 pp. 174-183, doi
  10.1145/237814.237860.  Full text **not retrieved** (ACM 403); the abstract
  calls the system the *"Groebner proof system"*, and the name "polynomial
  calculus" is attached later — Miksa-Nordstrom p. 468 verbatim: *"This proof
  system was introduced by Clegg et al. [9] in a slightly weaker form that is
  usually referred to as polynomial calculus (PC)"*.  The `n^{O(d)}`
  degree-bounded algorithm is quoted from Berkholz (STACS 2018, p. 11:4) and
  Galesi-Lauria, not from CEI itself.
* **Negative retrieval, reported as such.**  No published technique was located
  that lower-bounds the PC **degree** required to **derive** a specified
  polynomial from a **satisfiable** system.  Beyersdorff-Kullmann (SAT 2014,
  LNCS 8561:170-187; arXiv:1310.7627) extends hardness measures to satisfiable
  clause-sets, verbatim *"taking a worst-case approach over all unsatisfiable
  sub-instances"*, but its measures are depth, hardness, symmetric and
  asymmetric width, and three space measures — **all resolution**, and no
  algebraic extension exists.  Berkholz (STACS 2018, p. 11:4) does define a PC
  derivation of a general `f`, verbatim, but every degree lower bound retrieved
  instantiates `f = -1`.

**This negative retrieval costs nothing here.**  It would matter if the arm
needed a degree *lower* bound.  It does not: section 4 proves a matching
*upper* bound of 2, so no lower-bound technique, existing or hypothetical, can
push the quantity above 2.

### 6.3 Why `GF(2)` in particular deletes the Tseitin toolbox

`PATH.md` R9 names the grid-Tseitin canon as the toolbox to borrow.  The PC
degree bounds in that canon are for `mod-p` counting principles; over `GF(2)` an
`F_2`-linear system is refutable at degree 1 by Gaussian elimination — Filmus,
Lauria, Miksa, Nordstrom, Vinyals (*Theory of Computing* 21(4):1-48, 2025, doi
10.4086/toc.2025.v021a004) put it verbatim: *"the CNF encodes a linear system of
equations, which is easily shown inconsistent in PC by summing up all equations
in a tree-like fashion."*  Choosing `GF(2)` is exactly the choice that makes the
XOR structure free, which is measured here as `d_PC(90) = 1`.  It is stated as
the mechanism for Rule 90's degree 1; **it is not needed for Rule 30**, whose
constant degree is settled by section 4's theorem and does not depend on any
claim about characteristic.

## 7. Obstruction G check: FAILED

`PATH.md` 7.3 obstruction G: P3 fixes the input to the lone seed and varies only
`n`, so measures of a function of *variable* inputs collapse to 0 on the
one-point domain, which killed rows 63-66.  Row 9 is the framing built to evade
it.  a4 and a13 both executed this check and both passed, because derivation
length grows in `n`.  Executed here, honestly, whichever way it lands:

* **P3's parameterization is respected.**  The seed is a unit *axiom* of `S_n`,
  not an argument; there is no input distribution.  So the literal G collapse —
  "the function is a constant and the measure is 0" — does **not** occur:
  `d_PC` is 2, not 0.
* **The non-constancy half of the check fails.**  a13's executed form of the
  check is whether the quantity is a nontrivial, non-constant function of `n`.
  Derivation length is (`n^2/2 + n`).  `d_PC` is **2 at every `n >= 2`**, proved
  in section 4, and 4 at every `n` under the CNF encoding.  A constant carries
  no information about `n` whatsoever.
* **So the verdict is FAIL, not "evaded".**  Evading G is supposed to buy a
  nontrivial question about `n`.  Here it buys a constant.  The failure mode is
  one step removed from rows 63-66's: those measures were identically zero, this
  one is identically two.

## 8. Where this leaves R9, and what is *not* missing

a4 and a13 both end with a named missing lemma.  This arm does not, and the
difference is the point.

* There is no missing lemma for the upper bound: section 4 proves
  `d_PC(30, n) = 2` outright.
* There is no missing lemma for the lower bound either, because a lower bound
  above 2 is **impossible**, not merely unproved.
* The only statements that remain open are about a *different* object, and they
  are a4's Open Problem B restated for the algebraic setting: exhibit an
  encoding of "`c_n = 1`" of size `poly(log n)` and prove a superpolynomial PC
  size lower bound over it.  Nothing here approaches that, and over systems with
  extension such a bound implies circuit lower bounds.

### 8.1 This settles a4 section 4.5's open item

a4 recorded, of `P3_ASSESSMENT.md`'s suggestion that row 43's ANF degree
theorem `deg f_t = 2t-1` might feed a PC degree bound: *"That step is a second
missing lemma, not an available one... No implication between the two is known
to this document, and none is assumed."*  It is now settled, and in the
direction a4 suspected.  `deg f_t` is the `F_2`-degree of the centre function on
`2t+1` **arbitrary** inputs and grows linearly in `t`; the PC refutation degree
of the **fixed lone-seed** instance is `2`, for every `n`.  No implication is
possible, because the second quantity is constant while the first is not.
`PATH.md` row 43's own verdict — the degree theorem is "provably inert" for P3 —
is confirmed from the PC side, and a4's refusal to assume the lemma was correct.

**PC degree should be marked KILLED for R9**, on stronger grounds than any other
P3 arm so far: not "we could not prove it", but "the quantity is a constant and
here is the proof".

## 9. What a reader must not over-read

1. **The `2` versus `1` gap is not a separation of Rule 30 from Rule 90 on
   anything dynamical.**  It is `deg(ANF_30) - deg(ANF_90)`, readable off the
   rule number without running the CA, and section 4 proves that is all it is.
   Rule 160 ties Rule 30 at 2; Rule 128 beats it at 3; both have centre columns
   that are `1,0,0,0,...`.  Under the CNF encoding the ranking changes: 30 and
   128 are both 4, while 90 and 160 are both 3.
   **Quoting "PC degree separates Rule 30 from Rule 90" without those three
   facts inverts the finding.**
2. **`d_PC = 2` is not a hardness statement and not an easiness statement.**  It
   is a statement about the arity of the local update table.  It bears on the
   difficulty of computing `c_n` in no direction.
3. **The section 4 theorem is about this system and this ring.**  PC over
   `F_2[x]/(x^2-x)`, not PCR, and not PC over any other field.  A different
   encoding gives a different constant (4, measured), never a growing function.
4. **Nothing here is evidence about `mu(n)`, derivation length, or resolution.**
   The a4/a13 window over resolution is untouched by this arm; PC degree and
   resolution derivation length are different measures and this document
   contributes nothing to the latter.
5. **The size figures in 6.1 are not a bound.**  They are the sizes of the
   particular refutations constructed here, and a4 section 6's unary-encoding
   cap applies to any size measure over this encoding.
6. **Nothing here bears on P1 or P2.**
7. **Nothing here bears on Wolfram's Problem 3 in its Turing-machine
   formulation.**  P3 gives `n` in digit form, `Theta(log n)` bits; this encoding
   has `Theta(n^2)` variables, i.e. `n` in unary.  Proof systems with extension
   simulate fast algorithms, so no proof-complexity quantity over this encoding
   can separate anything about the prize question.  This sentence is required to
   travel with every result above.

## Reproduction

```sh
cd experiments/overnight-arms/frontier_attack/a16_pc_degree
uv run python pc_core.py                                              # 6 gates
uv run python pc_degree_measure.py --ns 2 3 4 5 6 7 8 --out degrees.json
uv run python pc_degree_measure.py --ns 10 12 14 16 20 --rules 30 90 160 \
    --dmax 3 --budget 600 --out degrees_big.json
uv run python pc_certificate.py --ns 4 8 16 32 64 128 256 512 --out certificate.json
uv run python pc_robustness.py --ns 2 3 4 5 6 --rules 30 90 160 128 --out robustness.json
uv run python ../../common/ensemble_filter.py

# certificate_size.log and control_columns.log (monomial counts; control columns)
uv run python -c "import sys,logging; sys.path.insert(0,'.');
from pc_core import System; from pc_certificate import refute;
logging.basicConfig(level=logging.INFO, format='%(message)s')
[logging.info('%s %s %s %s', r, n, len(D.lines), sum(len(l) for l in D.lines))
 for r in (30,90,160,128) for n in (8,32,128,256)
 for s in [System(n,r)] for D in [refute(s)]]"
```

Modal: $0.  Paid model-provider calls: $0.

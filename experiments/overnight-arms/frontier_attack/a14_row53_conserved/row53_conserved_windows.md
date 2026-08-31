# Row 53, conserved window functions: KILLED at step 0 by obstruction C (single-column blindness), width-independently; the exhaustive search is a byproduct that found nothing at any width reached

Register row 53, "latent-space geometry to exact non-additive conserved window
functions", `docs/rule30/PATH.md` 7.1 row 53 / `overnight/TRIAGE.md` row 4.
Arm `a14_row53_conserved`.  Date 2026-08-30.  Modal $0.  Paid
model-provider calls $0.  No `sorry`, no proof artifact, no missing lemma:
the characterisation used below is derived, not assumed.

The kill is width-independent and does not rest on the search.  Read the
search result as *confirmation that there was nothing to find*, never as the
reason the arm died; if the search were the reason, "maybe width 13 works"
would still be open, and it is not.

---

## 1. Definitions, and what is already known

**Window function.**  A map `phi: {0,1}^w -> K` for a coefficient ring
`K in {Z, Z/2, Z/3}`.

**Aggregate.**  `Phi(s) = sum_x phi(s(x), s(x+1), ..., s(x+w-1))`.

**Conserved.**  `Phi(F(s)) = Phi(s)` for every `s` in a stated class.  Two
classes are used, and both are computed below:

* *spatially periodic* configurations, all periods.  This is the standard
  class (the sum over one period is finite and well defined);
* *finite-support* configurations, which is the class the lone seed lives in.
  Here `Phi` is defined only if `phi(0^w) = 0`.

**What is already catalogued, so that nothing below is presented as
rediscovery.**  Site-sum conserved quantities of cellular automata are settled
theory with a decision procedure.  The framework is Hattori and Takesue's
additive-conserved-quantity analysis (*Physica D* 49, 1991), the
number-conserving-rule catalogues of Boccara and Fukś (*J. Phys. A* 31, 1998)
and the surrounding number-conserving-CA line, and Pivato's general
conservation-laws treatment (*Nonlinearity* 15, 2002), which is where the
current / discrete-continuity formulation used in section 3 comes from.  Note
that in that literature the whole class above is called **additive**, because
`Phi` is a site sum; the register's "non-additive" means `phi` itself is not
affine in the cells.  Both readings are answered here, because the *complete*
solution space is computed rather than a subclass of it.  These are framework
attributions by name; the specific dimension counts in sections 4 and 5 are
this arm's own computation and are not claimed to be quoted from anywhere.

Also standing, per the task framing: row 47's two proved byproducts (the
counting rate `N_1(T) >= floor(log2(T+4)) - 1` and universal depth-4 diagonal
pinning) exist already and **neither bounds the density**.

---

## 2. STEP 0, the mandatory gate: how could this constrain one column, and does it

### 2.1 The strong argument, which is the load-bearing one

The loophole to close first, because obstruction C as stated is a continuity
condition and an exact algebraic identity is not a continuous functional.  A
conserved quantity could hope to dodge C by entering the ladder of rows
7/46/54-56 as a **hard constraint** rather than as a statistic, in the same
shape as row 55's boundary pin.  Stated plainly so it is not strawmanned:
`Phi(row_t) = c` for all `t` **is** a sound, exactly valid pruning constraint,
and constancy along the orbit is what makes conservation laws useful in the
Hattori-Takesue line rather than what makes them empty.  It is not killed by
any information-theoretic argument, and row 55 is the precedent for a sound
Rule-30-specific constraint that still flips no verdict.

It is killed by the **support-growth asymmetry**, which is the exact-constraint
form of obstruction C:

> `Phi(row_t)` is a sum over a support that grows without bound -- about `2t`
> cells for the lone seed at time `t`.  Column 0 enters at most `w` of those
> terms, and `w` is **fixed** while the support grows.  Each of those `w`
> terms contributes a bounded amount.  So the single equation
> `Phi(row_t) = c` cannot force a value at column 0 unless the other
> `~2t - w` terms are themselves already pinned -- and pinning the rest of the
> row is a strictly stronger statement than the one being sought.  For every
> width `w`, every coefficient ring, and in both the statistic reading and the
> exact-constraint reading, a conserved aggregate leaves column 0 free.

This is genuinely width-independent: `w` is a constant and the support is
`Theta(t)`.  It also extends to every class section 6 lists as unsearched, for
the same structural reason -- a non-abelian row product still has column 0 in
`O(1)` of its factors, and a multi-row space-time window function still has
`O(1)` windows per row touching column 0.  The register's own arithmetic says
the same thing from the other side: row 47's counting rate
`N_1(T) >= floor(log2(T+4)) - 1` is an aggregate bound and is recorded there
as "real, unconditional, and very weak", bounding no density.

### 2.2 The obstruction-C argument, and its bound

Read as a statistic on a width-`W` window about the centre, the only reading
on which "does it move when column 0 is overwritten" is meaningful:

```
Phi_W(s) = (1/W) * sum_{x in window} phi(s(x), ..., s(x+w-1)).
```

Overwriting column 0 changes exactly one cell per row.  That cell lies in at
most `w` of the `W` window terms.  Therefore, for every `phi` in the class and
every configuration,

```
|Phi_W(A) - Phi_W(B)|  <=  w * (max phi - min phi) / W  =  O(1/W).
```

This is a theorem about the entire family, not a property of one candidate.
It is exactly the `O(1/W)` condition of `PATH.md` 0.1.

### 2.3 The measurement, `step0_gate.py`, log `step0_gate.log`

Harness: the mandated `experiments/rule30/p_geometric_attack/discriminator.py`,
imported read-only, using its `diagram`, `overwrite_centre` and `s0_control`.
Fields `A` = true Rule 30 lone seed, `B` = `A` with column 0 overwritten by
`0101...`, `C` = Rule 90 lone seed.  `T = 400`; 196 of 324,409 cells change
from `A` to `B`, a fraction `6.04e-4`, and the harness asserts the two fields
differ on column 0 and nowhere else.

Six representative `phi` spanning the class the search then enumerates.
`absAB` = `|Phi_W(A) - Phi_W(B)|`; `relAC` = relative separation of Rule 30
from Rule 90.

| statistic | W=32 | W=64 | W=128 | W=256 | ratio per doubling | relAC (rule separation) |
|---|---|---|---|---|---|---|
| **S0_control_col0** (positive control) | **0.4888** | **0.4888** | **0.4888** | **0.4888** | **1.00, flat** | 0.024 |
| `phi_w1_density` (additive, w=1) | 4.664e-4 | 2.332e-4 | 1.166e-4 | 5.83e-5 | 0.500 | 0.942-0.976 |
| `phi_w2_block11` (nonlinear, deg 2) | 1.710e-3 | 8.551e-4 | 4.275e-4 | 2.138e-4 | 0.500 | 1.000 |
| `phi_w3_monomial` v0v1v2 | 2.643e-3 | 1.322e-3 | 6.608e-4 | 3.304e-4 | 0.500 | 1.000 |
| `phi_w3_majority` | 0.0 | 0.0 | 0.0 | 0.0 | exact cancellation, see 2.4 | 0.971-0.988 |
| `phi_w5_random` (integer, [-3,3]) | 1.866e-3 | 9.328e-4 | 4.664e-4 | 2.332e-4 | 0.500 | 0.524-0.764 |
| `phi_w5_maxrun` (run-length; the shape row 53's ML half emits) | 3.887e-3 | 1.943e-3 | 9.717e-4 | 4.859e-4 | 0.500 | 0.950-0.979 |

Every `phi` halves to four significant digits per doubling of `W`, matching
the analytic bound of 2.2 exactly.  The positive control, which reads column
0, moves by **0.4888 absolute / 95.6% relative and does not decay at all** as
`W` grows.  Meanwhile the family separates Rule 30 from Rule 90 by **52% to
100%**.

**KILL CONDITION FIRED.**  Pre-registered in `step0_gate.py`'s docstring
before the run: kill if `|A-B|` decays like `1/W` against a flat 96% control.
The disconfirming outcome that would have kept the arm alive -- any `phi`
whose `|A-B|` stays flat or decays slower than `1/W` -- did not occur for any
member.  This is the fourth instance of the recorded lesson: **rule-sensitivity
is not evidence of P1-relevance** (rows 57, 58, 59).

### 2.4 The one zero row, shown to be cancellation and not a miss

`phi_w3_majority` reports `absAB` exactly `0.0` at all four widths, which read
alone looks like a statistic that is not seeing column 0 -- the precise
failure mode `s0_control` exists to catch.  `addenda.py` prints the
**unnormalised** numerator instead of the `W`-normalised statistic:

| W | numerator A | numerator B | diff |
|---|---|---|---|
| 32 | 3146 | 3146 | 0 |
| 64 | 6348 | 6348 | 0 |
| 128 | 12708 | 12708 | 0 |
| 256 | 25456 | 25456 | 0 |

The numerators differ across `W` (so the statistic is being computed on the
window, not returning a constant) and agree between `A` and `B` at each `W`.
Only the `w = 3` windows containing column 0 can change, and on this diagram
the majority of each of those three windows is unchanged by the overwrite.
This is an exact cancellation in the affected terms, stronger than the
`O(1/W)` bound, not weaker.

---

## 3. The search: exact finite characterisation, no sampling and no guessed bound

`conserved_search.py`.  Let `n = w + 2`.  For `u in {0,1}^n` read as
`s(x-1 .. x+w)`, set

```
Lambda(u) = phi( F(s)(x .. x+w-1) ) - phi( s(x .. x+w-1) ),
```

a function of `n` cells, so that `Phi(F(s)) - Phi(s) = sum_x Lambda(u_x)`.
Words of length `n` are exactly the edges of the de Bruijn graph `B(2, n-1)`
whose vertices are words of length `n-1`, and cyclic configurations are
exactly its closed walks.  An edge weighting has zero circulation on every
closed walk iff it is a potential difference.  Hence

> `Phi` is conserved on **all** spatially periodic configurations
> **iff** there exists `J: {0,1}^{n-1} -> K` with
> `Lambda(u) = J(u_0..u_{n-2}) - J(u_1..u_{n-1})` for every `u in {0,1}^n`.

`J` is the discrete current and the displayed equation is the discrete
continuity equation.  This is an exact `iff` over the whole infinite class,
established in one step; there is no period cutoff to justify and nothing is
sampled.  `B(2,n-1)` is connected, so `J` is pinned by `phi` up to one
additive constant.

Implementation: `J` is eliminated exactly by fixing `J(0)=0` and walking a
spanning tree, which makes each `J(v)` an explicit linear functional of `phi`
and satisfies the `V-1` tree edges by construction; the remaining
`E - (V-1) = 2^(w+1) + 1` edges are the complete constraint set, a
`(2^(w+1)+1) x 2^w` matrix `C` over `K` whose kernel is exactly the conserved
space `V_w`.  Cross-checked at `w <= 5` against the un-eliminated `(phi, J)`
system: **100 cross-checks, 100 agree, 0 disagree** (`control_battery.jsonl`,
field `elimination_cross_check`).

**Trivial subspace `T_w`, quotiented out before any find is claimed:**
constants (1 dimension); coboundaries `phi(v) = g(v_0..v_{w-2}) -
g(v_1..v_{w-1})`, which make `Phi` identically zero on every periodic
configuration (`2^(w-1) - 1` dimensions, the kernel of `g -> g o p_L - g o p_R`
being the constants); and lifts of conserved width-`(w-1)` functions together
with their shifted twins.  A **new** conserved quantity at width `w` exists
iff `dim V_w > dim T_w`.  The code asserts `T_w subset V_w` at every width and
the assertion never fired.

---

## 4. Controls

| rule | why it is here | result |
|---|---|---|
| **184** | proved number-conserving; the width-1 density MUST appear or the harness is broken | `new_nontrivial = 1` at `w = 1` — the density, recovered — and 0 at every `w >= 2`, at all four moduli |
| **204** (identity) | saturation control | `dim V_w = 2^w` at every width, i.e. everything is conserved |
| **170** (shift) | saturation control | `dim V_w = 2^w` at every width |
| **90** | the repo's standing section-0 filter | see section 5 |

The 184 and 204/170 controls are the ones with real discriminating power.
The `bruteforce_verified: true` field (independent re-simulation on 400 random
cyclic configurations per basis vector) has **near-zero power for Rule 30**,
because Rule 30's entire found space consists of coboundaries whose aggregate
is identically zero, so that check confirms `0 = 0`.  It is reported for
completeness, not as evidence.

---

## 5. Result: exhaustive absence, and an identical answer for Rule 90

For **Rule 30**, at every width `w = 1..12` and every coefficient ring:

```
dim V_w  =  2^(w-1)  =  1 (constants)  +  (2^(w-1) - 1) (coboundaries)
dim T_w  =  2^(w-1)
new_nontrivial  =  0
```

The exact match against `2^(w-1)` at every single width is itself an internal
consistency check on the linear algebra, and it says something sharper than
"nothing found": **Rule 30's conserved window space is precisely the space
that every ECA conserves.**  There is nothing rule-specific in it at all, and
the lifts contribute nothing because there is nothing to lift.

For **Rule 90**, the numbers are **identical at every width and every
modulus**.  That is an independent kill by the repo's section-0 filter: the
object is non-separating.  Even a hypothetical find would have had to survive
the fact that the two rules have the same conserved window space while having
opposite P1 answers.

Both rules, both classes:

| | Rule 30 | Rule 90 |
|---|---|---|
| `dim V_w`, `w = 1..12`, `K = Z` via `p = 2^31-1` (and `p = 1000003` to `w = 8`) | `2^(w-1)` | `2^(w-1)` |
| `dim V_w`, `w = 1..12`, `K = Z/2` | `2^(w-1)` | `2^(w-1)` |
| `dim V_w`, `w = 1..12`, `K = Z/3` | `2^(w-1)` | `2^(w-1)` |
| new nontrivial, any width, any ring | **0** | **0** |
| finite-support class (`phi(0^w)=0`), `w <= 10` | `2^(w-1) - 1`, exactly the coboundaries | same |

**Rigour over `Z` from the mod-`p` runs.**  Reduction mod `p` can only lose
rank, so `rank(C)_p <= rank(C)_Q`, giving `dim V_w(Q) <= dim V_w(p)`.  The
same direction on the trivial generators gives `dim T_w(p) <= dim T_w(Q)`.
Measured: `dim V_w(p) = dim T_w(p)`.  Since `dim T_w(Q) <= dim V_w(Q)` always,
chaining gives `dim V_w(Q) = dim T_w(Q)`: **the absence is a statement about
rational-valued `phi`, not merely about `phi` mod a prime.**  The `Z/2` and
`Z/3` runs are separate coefficient rings in their own right, not
approximations to `Q`, and they answer the register's "group-valued" reading
for those two groups.

**Class gap closed** (`addenda.py`, `addenda.json`).  Section 3 characterises
conservation on *periodic* configurations; the lone seed is *finite-support*.
Adding the single affine row `phi(0^w) = 0` drops the dimension by **exactly
1** at every width `w = 1..10` for rules 30 and 90 over both `Z` and `Z/2`,
leaving exactly the coboundary space and `new_nontrivial = 0`.  Asserted in
code, and the assertion never fired.  So the periodic-class result covers the
class the register actually cares about.

---

### 5.1 Verification ledger

| check | count | result |
|---|---|---|
| deep-search records (rules 30, 90 x `Z`, `Z/2`, `Z/3` x `w = 1..12`) | 72 | 72 satisfy `dim V_w = dim T_w = 2^(w-1)`, `new_nontrivial = 0`; **0 mismatches** |
| control-battery records (5 rules x 4 moduli x `w = 1..8`) | 160 | rule 184 gives `new_nontrivial = 1` at `w = 1` under all 4 moduli; rules 204 and 170 saturate at `2^w` in all records |
| `elimination_cross_check` (J-eliminated system vs full `(phi, J)` system, `w <= 5`) | 100 | 100 agree, **0 disagree** |
| class-gap assertions (`phi(0^w)=0`, rules 30/90, `Z` and `Z/2`, `w <= 10`) | 40 | drop is exactly 1 in every case; assertion never fired |
| `T_w subset V_w` assertion inside the search | every record | never fired |

## 6. The bound, stated exactly (obstruction H)

**Exhaustive absence up to width 12 is a bound, not a theorem about all
widths**, and it is also a bound on the *class*, not only on `w`.  The search
covers: abelian **site-sum aggregates** of **single-row** windows of width
`w <= 12`, with `phi` valued in `Z` (rigorously, via section 5's rank
argument), `Z/2` and `Z/3`, conserved under one step on all spatially periodic
configurations and, separately, on all finite-support configurations.

Explicitly **outside** the bound, and not claimed: non-abelian monoid- or
group-valued *products* along the row (TRIAGE row 4's "group/monoid-valued"
reading in its widest sense); multi-row space-time window functions; `Z/m` for
composite `m` and for primes other than 2 and 3; conservation only up to a
`k`-step period rather than one step; and every width `w > 12`.

One class the register names is *not* a gap: **"tilted-direction" conservation
of a site-sum aggregate is not a distinct object.**  `Phi` is a sum over all
`x` and is therefore shift-invariant by construction, so tilting the direction
in which the aggregate is read gives back the same functional and the same
equation.  A genuinely different tilted object would have to be a multi-row
window function, which is listed above as outside the bound.

None of this matters for the verdict.  Section 2.1 kills the whole family at
every width and in every coefficient ring, including all of the classes just
listed as unsearched, because a conserved quantity is by definition constant
along the orbit and so distinguishes no two rows.

---

## 7. Files, reproduction, and fence

```
step0_gate.py           the mandatory gate; imports discriminator.py read-only
step0_gate.log          its output (the section 2.3 table)
conserved_search.py     the exact de Bruijn / continuity-equation search
control_battery.jsonl   rules 184,204,170,90,30 x 4 moduli, w <= 8, with the
                        100 elimination cross-checks
deep_search.jsonl       rules 30,90 x moduli {2^31-1, 2, 3}, w <= 12
deep_search.log         stdout of the above
addenda.py, addenda.json  class-gap check and the majority-numerator check
```

```
uv run python step0_gate.py 400
uv run python conserved_search.py --wmax 8 --primes 2147483647,1000003,2,3 --rules 184,204,170,90,30 --out control_battery.jsonl
uv run python conserved_search.py --wmax 12 --primes 2147483647,2,3 --rules 30,90 --out deep_search.jsonl
uv run python addenda.py
```

**Fence disclosure**, following the precedent of row 70's
`overnight/FENCE-COMPLIANCE.md`: all writes are inside
`experiments/overnight-arms/frontier_attack/a14_row53_conserved/`, with one
exception of the same kind row 70 disclosed.  The mandated read-only
`exec_module` import of `discriminator.py` caused CPython to write
`experiments/rule30/p_geometric_attack/__pycache__/discriminator.cpython-311.pyc`
(12,150 bytes, created 2026-08-30 13:53).  It is byte-code generated by the
interpreter, no existing file was modified, and it was left in place rather
than deleted so that no write of any kind was performed on that subtree.  No
git commits were made.

---

## 8. What a reader must not over-read

1. **The arm did not die because the search came up empty.**  It died at step
   0, width-independently.  Reading it the other way leaves "maybe width 13"
   open; it is not open.
2. **"No conserved window function up to width 12" is not "no conserved
   quantity".**  Section 6 lists the classes outside the bound.
3. **Zero `new_nontrivial` is not a defect of the method.**  Rule 184 returns
   the density at `w = 1` and rules 204/170 saturate, so the method finds what
   is there when it is there.
4. **`bruteforce_verified: true` for Rule 30 proves almost nothing** (`0 = 0`
   on coboundaries); the load-bearing controls are 184 and 204/170.
5. **The 52%-100% Rule 30 versus Rule 90 separation in section 2.3 is not
   evidence of anything.**  That is the exact trap rows 57-59 recorded.  In
   the search itself the two rules give *identical* answers, which is the
   honest reading.
6. **Row 53's ML half was not run and is not evaluated here.**  It was a
   candidate generator for the class that section 2.1 kills wholesale, so no
   generator can rescue it; but nothing here is a measurement of a
   latent-space method.
7. **This document contains no proof artifact and no conditional lemma.**  The
   de Bruijn characterisation in section 3 is derived in full, so the
   negative-result clause's "under an appropriate conservation lemma" pattern
   does not appear and no lemma is owed.

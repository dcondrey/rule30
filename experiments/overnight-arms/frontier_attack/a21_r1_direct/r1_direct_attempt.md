# NEW-OBSTRUCTION-NAMED — the obstruction is **bounded-window closure failure**, stated with its hypotheses inline: *for every `m >= 1` and every `t >= 2m+1` there exist two LEFT-SUPPORTED rows (`s(0,x) = 0` for `x >= 1`; the lone seed is one) whose centre-trace prefixes `c_0..c_{t-1}` agree on their last `m` symbols and whose `r_t = s(t,1)` differ.* So `r_t` is provably not a function of any bounded suffix of the centre trace, and the route "prove Lemma Z by exhibiting a bounded centre window that determines `r`" is closed at every width. Proved for all `m` and all `t >= 2m+1` (Theorems U + S + W, explicit witness rows exhibited for `m = 2..5`), quantified exactly for `m <= 16` (`eps(m)`), and separately refuted on the true lone-seed orbit to `m <= 28`.

Arm a21, 2026-08-30.  Route R1 / register row 1 / Prize problem 1.
**Prize movement: none.  P1, P2, P3 all unmoved.**
No git commit.  No solver.  Paid model-provider calls: `$0`.  No `sorry`, no
proof artifact.

**Fence.**  Every file written by this session is in this directory.  One
disclosed exception, the same one a1 records: the read-only import of
`experiments/overnight-arms/common/rule30.py` causes CPython to write
`common/__pycache__/rule30.cpython-*.pyc`.  No source file outside this
directory was modified; `docs/rule30/PATH.md` was read, not edited.

---

## 0. Verdict in one paragraph, before any detail

Lemma Z is not proved and not refuted.  What is new is an **unconditional**
object that the three prior arms never formed: for a left-supported initial row
(the lone seed is one) there is a single explicit function `phi_t` with
`r_t = phi_t(c_0,...,c_{t-1})`, exactly, for every `t`.  The whole of R1 is
therefore a question about how far back `phi_t` reaches into the centre trace.
If `phi_t` were a function of a bounded suffix `c_{t-m}..c_{t-1}`, Lemma Z would
be a one-line corollary (bounded-window image of an eventually periodic word is
eventually periodic).  **It is not, for any `m`, and that is a theorem here, not
a measurement.**  The measurement that goes with it is the exact Bayes error
`eps(m)` of the best `m`-window predictor, computed as an exact rational for
`m <= 16`, together with a proof that `eps(m)` no longer depends on `t` once
`t >= 2m+1`.  Rule 90 is a genuine live control throughout and separates
sharply: `eps_90(m) = 1/2` exactly for every `m` (proved), against
`eps_30(16) = 1488690544/8589934592 ≈ 0.1733`.

---

## 1. The three missing lemmas, and in what sense they are one statement

They are three encodings of the eventual behaviour of **one word**: the column-1
word restricted to the zero set of the centre column, under the hypothesis that
the centre column is eventually periodic.  Write, for a Rule 30 space-time
diagram `s`, `c_t = s(t,0)`, `r_t = s(t,1)`, `l_t = s(t,-1)`,
`Z = {t : c_t = 0}`, and `D(t,x) = s(t+p,x) XOR s(t,x)`.  The shared statement,
with its quantifiers written out:

> **(★)** For every `p >= 1`: if there exists `t_0` such that for all `t >= t_0`,
> `c_t = c_{t+p}`, then there exists `t_1` such that for all `t >= t_1` with
> `c_t = 0`, `r_t = r_{t+p}`  (equivalently `D(t,1) = 0`).

* **a1's LEMMA Z** is (★) verbatim, for the diagram of a nonzero finite
  configuration, phrased through `D`.
* **a2's MISSING lemma** is the `p = 2` instance.  At `p = 2` a nonconstant
  2-periodic trace has `Z` equal to a single parity class, and "eventually
  2-periodic on one parity class" is literally "eventually constant on `Z`".
  So a2's "`s(2s,1)` is constant in `s`" **is** (★) at `p = 2`, not a variant of
  it.
* **a7's `Diff_q` gap** is the same object approached from the other polarity,
  and a7's own text says so ("aimed at the same zero set from opposite sides").
  a7 needs `col_1(t) = 1` for infinitely many `t in Z` for its half-plane
  extension `X(k,01)`; that fails exactly when `r` is eventually the constant
  `0` on `Z`, i.e. in one of the two branches (★) at `p = 2` permits.  **The
  honest statement of the relation:** a7 needs one polarity of (★)'s `p = 2`
  conclusion excluded, on a relaxed object (the half-plane extension, not a
  finite configuration).  It is the same word about the same zero set; it is not
  literally the same implication, and this document does not claim it is.

Everything below is aimed at (★).

**Scope note, stated once and load-bearing.**  a1/a2 state (★) for an arbitrary
nonzero finite row `y` on the forward orbit.  The results in sections 3-7 are
proved for **left-supported** initial rows (`s(0,x) = 0` for every `x >= 1`).
The lone seed is left-supported, so they apply directly to the lone-seed
diagram, which is P1's actual object and is the form R1 is stated in
(`PATH.md` section 2 works with the lone seed's `c_t, l_t, r_t`).  They do
**not** apply verbatim to row 31's reduction, which passes to `y = F^T(x)`; that
row is not left-supported.  Do not cite section 3-7 against the general-finite-row
form of (★).

---

## 2. Order of work, and the two assigned directions that died first

1. Verified the assigned direction **(b)** simplification.  It is real and it is
   **already in the tree, verbatim**: `PATH.md` section 2, lines 146-148, in the
   repo's own notation — `c_t = 1 => l_t = 1 XOR c_{t+1}`, `c_t = 0 =>
   l_t = c_{t+1} XOR r_t`.  Re-checked anyway (`defect_pde.py`: 1,516 zero-phase
   and 1,484 one-phase steps of the lone seed, 0 violations).  Nothing was found
   here; the brief's premise that this was un-isolated is incorrect.  Cost: 10
   minutes.  Recorded so the next session does not spend them again.
2. Killed the assigned direction **(a)** as briefed, on logic, before spending
   compute.  "ANF degree of the window map **restricted to inputs consistent
   with `c` being eventually `p`-periodic**" conditions on a set that is empty
   if P1 is true.  A restriction to an empty set has no ANF.  The only
   nonvacuous replacement is a finite-`k` agreement window, which is obstruction
   H.  See section 8.1.
3. Reformulated **(a)** into an unconditional object, which is what sections 3-7
   are.  This is the advisor-suggested pivot and it is the substance of the arm.
4. Direction **(c)**, the counting identity, was **found and proved** — it is
   Theorem U (section 4).  It is not a measured near-identity; it is exact and
   it has a two-line proof.
5. Wrote down the defect PDE and the leftward closing cascade (section 9).
   Validation, labelled as such.

---

## 3. Theorem P: `r_t` is an explicit function of the centre-trace prefix

> **THEOREM P.**  Let `s(0,.)` be any configuration with `s(0,x) = 0` for every
> `x >= 1` ("left-supported"); the lone seed is one.  Then for every `t >= 1`
> there is a single function `phi_t : {0,1}^t -> {0,1}`, the **same** function
> for every left-supported initial row, with
>
> ```text
> r_t = phi_t(c_0, c_1, ..., c_{t-1}).
> ```
>
> Moreover `phi_t(c) = c_{t-1} XOR psi_{t-1}(c_0,...,c_{t-2})`, i.e. `c_{t-1}`
> occurs in the ANF linearly and in no other monomial.

*Proof.*  Because `s(0,x) = 0` for `x >= 1`, the cell `s(t,x)` depends only on
`s(0, x-t .. 0)`, i.e. on `b_j := s(0,-j)` for `0 <= j <= t-x`.  Hence
`r_t = s(t,1)` is a function of `b_0..b_{t-1}` and `(c_0..c_{t-1})` is a
function of `b_0..b_{t-1}`.  Left permutivity (a7's Lemma P) gives
`c_j = b_j XOR H_j(b_0..b_{j-1})`, a triangular map with unit diagonal, hence a
bijection `{0,1}^t -> {0,1}^t`.  Compose the inverse with `r_t`.  The last
clause follows from `r_t = b_{t-1} XOR H'(b_0..b_{t-2})` and
`c_{t-1} = b_{t-1} XOR H_{t-1}(b_0..b_{t-2})`. ∎

*Verified* (`phi_anf.py`, `phi_epsilon.py`): the truth table of `r_t` in
`c`-coordinates is single-valued and total for every `t <= 21` and both rules
(`phi_epsilon.py` asserts it at every `t` it builds); unchanged when the initial
row carries 1, 2 or 3 extra free bits beyond `b_{t-1}` (so the arity is exactly
`t`, not `t+1`); and it predicts `r_t` with 0 errors on 2,000 random
left-supported rows of width up to `t+25`, per rule.  The `c_{t-1}`
linear-and-isolated clause holds at every `t <= 16` for both rules.

**Why this matters.**  R1 asks whether an eventually periodic `c` forces `r` to
be eventually periodic on `Z`.  Theorem P says `r` is a function of `c` **with
no hypothesis at all**.  The entire content of R1 is therefore: *how far back
into `c` does `phi_t` reach?*  That question has no periodicity hypothesis in
it, so it is not vacuous, and it is decidable at each finite `t`.

**Full ANF support, rule 30** (`phi_anf.py`, exact Möbius transform):

| `t` | 4 | 6 | 8 | 10 | 12 | 14 | 15 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `deg phi_t` | 2 | 3 | 5 | 6 | 8 | 9 | 11 | 12 |
| monomials | 6 | 18 | 60 | 188 | 712 | 2650 | 5144 | 9942 |
| variables absent from the ANF | none | none | none | none | none | none | none | none |

**Every** `c_j`, `j = 0..t-1`, occurs in the ANF of `phi_t` at every
`t <= 16` — the reach is maximal at every computed `t`.

Rule 90's `phi_t` is by contrast **linear at every `t`** (degree 1 throughout)
with a tiny support: `1,1,2,2,2,2,3,3,3,3,3,3,3,3,4,4` monomials for
`t = 1..16`, earliest variable `min_var = t - reach` with
`reach = 1,1,3,3,3,3,7,7,7,7,7,7,7,7,15,15`.  So Rule 90's reach is unbounded
too, but only along dyadic jumps — which is exactly Kummer, and exactly why a1
could prove Rule 90's version of (★) false.  Rule 90 therefore does **not**
provide a bounded-window counterexample to the method here; it fails
bounded-window closure as well, and section 6 explains in what different way.

---

## 4. Theorem U: the exact counting identity (assigned direction (c), proved)

> **THEOREM U.**  Draw the bits `b_j = s(0,-j)` of a left-supported initial row
> uniformly.  Then for every `t` and every `k <= t`, the tuple
> `(s(t,0), s(t,1), ..., s(t,k))` is **exactly uniform** on `{0,1}^{k+1}`.

*Proof.*  By left permutivity `s(t,x) = b_{t-x} XOR (a function of
b_0..b_{t-x-1})`.  So at any fixed value of `b_0..b_{t-k-1}` the map
`(b_{t-k},...,b_t) -> (s(t,k),...,s(t,0))` is triangular with unit diagonal,
hence a bijection of `{0,1}^{k+1}`.  Summing over the fixed part gives exact
uniformity. ∎

*Verified* (`eps_theorem.py`): exhaustive over all `2^{t+1}` left-supported rows
for every `t <= 11` and every `k <= t`, both rules — **maximum deviation from
exact uniformity: 0**.

This is the exact counting identity direction (c) asked for, and it is stronger
than "the counts are close": every cell count is exactly `2^{n-k-1}`.  It is
**not rule-specific** (rule 90 satisfies it too), and it is the reason the
finite-window counting design in the brief is degenerate: the counts are exactly
uniform by a two-line argument, so no information about (★) can be extracted
from them.  That closes direction (c) as a route, by proving its identity rather
than by failing to find one.

---

## 5. Theorem S: `err(m,t)` stops depending on `t`, and `eps(m)`

Define `err(m,t)` = the exact minimum error, over the uniform measure on all
`2^t` centre prefixes, of **any** predictor of `r_t` from the `m` most recent
centre values `c_{t-m},...,c_{t-1}`.  `err(m,t) = 0` for some `m < t` would say
`phi_t` collapses to a bounded window at that `t`.

> **THEOREM S.**  For `t >= 2m+1`,  `err(m,t) = eps(m)`, independent of `t`,
> where `eps(m)` is the Bayes error of predicting `r_t` from `m` boundary bits
> `gamma = (c_{t-m},...,c_{t-1})` when the `m+1` hidden bits
> `w = (s(t-m,1),...,s(t-m,m+1))` are uniform and independent of `gamma`.

*Proof.*  The quarter plane `x >= 1` is driven forward by the column `x = 0`:
`s(j+1,1) = c_j XOR (s(j,1) OR s(j,2))` and `s(j+1,x) = s(j,x-1) XOR (s(j,x) OR
s(j,x+1))` for `x >= 2`, so its dependence cone from time `t-m` to `r_t` is
exactly `s(t-m, 1..m+1)` together with `c_{t-m}..c_{t-1}`.  By Theorem U that
block is uniform; the bits `b_{t-m},...,b_{t-1}` carrying `c_{t-m}..c_{t-1}` do
not occur in `s(t-m, .>= 1)` at all (which uses only `b_0..b_{t-m-1}`), so the
two are independent.  `t >= 2m+1` is what makes `m+1 <= t-m`, i.e. Theorem U
applicable at `k = m+1`. ∎

*Verified* (`eps_theorem.py`): `eps(m)` computed by an independent
`2^{2m+1}`-cost block enumeration agrees with the direct `2^t` enumeration of
`phi_epsilon.py` at **every** `(m,t)` with `m <= 10` and `2m+1 <= t <= 21`, for
both rules.  The predicted threshold is visible in the raw table: `err(m,t)`
first becomes constant in `t` at exactly `t = 2m+1` for `m = 6, 7, 8`
(`eps_stability.txt`).

**`eps(m)`, exact rationals** (`eps_theorem_output.txt`):

| `m` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| rule 30 | 1/4 | 1/4 | 7/32 | 7/32 | 13/64 | 1644/2^13 | 6280/2^15 | 24612/2^17 |
| decimal | .250000 | .250000 | .218750 | .218750 | .203125 | .200684 | .191650 | .187775 |
| rule 90 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |

| `m` | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|
| rule 30 | .182800 | .181395 | .179729 | .177906 | .176829 | .175468 | .174552 | .173306 |
| rule 90 | .500000 | .500000 | .500000 | .500000 | .500000 | .500000 | .500000 | .500000 |

The rule-30 numerators `2, 8, 28, 112, 416, 1644, 6280, 24612, 95840, 380412,
1507680, 5969532, 23733628, 94203568, 374847204, 1488690544` are recorded in
`eps_theorem_results.json`.  No claim is made that this sequence is in OEIS or
that it has a closed form; neither was checked.

---

## 6. Theorem W: `eps(m) > 0` for **every** `m` — the obstruction, proved

> **THEOREM W.**  For every `m >= 1`, take `gamma = 0^m` and the hidden block
> `w = (0,...,0,b)` with the single free bit in the last slot,
> `w_{m+1} = s(t-m, m+1) = b`.  Then `r_t = b`.  Hence `r_t` is **not** a
> function of `(c_{t-m},...,c_{t-1})` alone, and `eps(m) >= 2^{-(2m+1)} > 0`.

*Proof.*  With the block `(0,...,0,b)` of length `m+1` and boundary value `0`,
one Rule 30 step gives at position `m` the value `0 XOR (0 OR b) = b`, and `0`
at every position `< m`; the block shortens by one from the right, reproducing
the shape `(0,...,0,b)`.  After `m` steps the single remaining cell is `b`. ∎

*Verified* (`witness.py`): the witness holds for `m = 1..64`, both `b`, both
rules, 0 failures; and the block simulator that Theorem S and Theorem W are
stated over agrees with a genuine diagram on 3,000 random `(m,t,row)` triples
per rule, 0 mismatches.

**Realisability of the witness pair, composed explicitly.**  Theorem W lives on
the block ensemble `(gamma, w)`; the headline is about centre-trace prefixes of
actual rows.  Theorem U closes that gap in general — every `(gamma, w)` is
realised by exactly `2^{n-2m-1}` left-supported rows of `n` free bits at any
`t >= 2m+1` — but because Theorem U is *verified* exhaustively only to `t <= 11`
(its proof is general), the specific pair is also exhibited directly.
`witness.py` searches all nonzero left-supported rows at `t = 2m+1` and returns,
for `m = 2,3,4,5` and both rules, two genuine rows with `gamma = 0^m`, hidden
blocks `(0,...,0,0)` and `(0,...,0,1)`, and `r_t = 0` and `r_t = 1`
respectively.  E.g. rule 30, `m = 4`, `t = 9`:
`(s(0,0),s(0,-1),...) = 0000000001` gives `r_9 = 0` and `1111010110` gives
`r_9 = 1`, with identical `c_5..c_8`.

> **THEOREM N (rule 90 only).**  `eps_90(m) = 1/2` exactly for every `m >= 1`.

*Proof.*  Rule 90's quarter-plane map is GF(2)-linear, so `r_t = L(gamma) XOR
M(w)` with `L, M` linear.  Theorem W shows `M` has coefficient 1 on `w_{m+1}`,
so `M` is a nonzero linear form; `M(w)` is then uniform under uniform `w` and
independent of `gamma`, so `r_t | gamma` is uniform and the Bayes error is
exactly `1/2`. ∎  *Verified:* affinity checked exhaustively for `m <= 6`, and
`coeff(w_{m+1}) = 1` for `m <= 12`.  The rule-30 contrast is measured in the
same script: at `gamma = 0^m`, 3/8, 7/16 and 15/32 of the hidden blocks violate
affinity at `m = 2, 3, 4`.

**The obstruction, named.**

> **BOUNDED-WINDOW CLOSURE FAILS (rule 30 and rule 90 alike).**  There is no
> `m` for which `r_t` is determined by the last `m` centre values.  The route
> "prove Lemma Z by exhibiting a bounded window of the centre trace that
> determines `r`" is therefore closed at every width, unconditionally, with an
> explicit two-line witness — not by a failed search.

**And this is where the OR nonlinearity shows up, quantified — on the ENSEMBLE
of left-supported rows, not on the lone-seed orbit.**  That scope is part of the
sentence, not a footnote to it; `eps(m)` is a Bayes error over a uniform measure
and says nothing directly about any single orbit.  With that said: both
rules fail bounded-window closure, but they fail it in opposite ways.  For
rule 90, `eps(m) = 1/2` exactly at every `m`: the recent centre window carries
**literally zero** information about `r_t`, because the linear map washes the
uniform hidden block over the answer.  For rule 30, `eps(m) ≈ 0.173` at
`m = 16`: the recent centre window carries **a great deal** of information —
83% accuracy — and still never all of it.  The OR is what converts "no
information" into "almost all of it, never all".  That contrast is the exact,
non-decorative form of the Rule 90 filter for this object.

---

## 7. The same question on the true orbit, and its ceiling

Theorem W is about the universal `phi_t`.  A single orbit is measure-zero and
could be special (`PATH.md` obstruction E has this shape), so the orbit-level
version was run separately (`orbit_window.py`, lone seed, `T = 60,000`):
for each `m`, is `(c_{t-m},...,c_{t-1}) -> r_t` single-valued over `t < T`?

```text
rule 30, |Z| = 29,907 of 60,000
 m:                 1     8    16    20    24    26    28    29    30
 conflicts, all t: 30034 14194 4966  400   20     7     3     2     0
 conflicts, t in Z:14880  7388 1401   86    5     1     1     0     0
 repeat-window
   opportunities:  59997 59736 20863 1776   98    21     6     3     0
```

Bounded-window determination is refuted on the true orbit for every
`m <= 28` (all `t`) and every `m <= 26` (restricted to `Z`).

**The `m = 29, 30` zeros are a birthday artifact and must not be read as
structure.**  The last column is why they are in the table: at `m = 30` there
are **zero** repeat-window opportunities in 60,000 steps, so "no conflict" is
vacuous.  With a pseudorandom trace the expected number of colliding pairs is
`~T^2 / 2^{m+1}`, so this test can only ever refute `m` up to about
`2 log2 T`.  **That is `PATH.md` obstruction H again, at the same exchange
rate a1 section 4 records** — doubling the horizon buys one more window bit.
The test is a refuter with a logarithmic ceiling, not a confirmer.

Rule 90's orbit-level control fires at **every** `m <= 30`, and is provable for
all `m` **given two facts that are a1's, not this arm's**: Rule 90's lone-seed
centre is `1,0,0,0,...` (a1 section 2, verified to `t < 65536`) and its
`r_t = 1` exactly at `t = 2^j - 1` (a1's Kummer argument).  Granted those, every
window of length `m` is `0^m` from `t = m+1` on while `r` still takes both
values — one window value, both answers, forever.  The `m in {2,6,14,30}` rows with ~59,980 conflicts are the
cases where the first occurrence of the all-zero window lands on a `t = 2^j-1`,
flipping which answer is recorded first.

---

## 8. Two corollaries about the register, both sharp and both small

### 8.1 Direction (a) as assigned conditions on an empty set

"The ANF degree of the map from a window to `r_t`, **restricted to inputs
consistent with `c` being eventually `p`-periodic**" has an empty conditioning
class if P1 is true.  There is no ANF of a function on the empty set, so the
question as posed is not answerable in either direction, and a positive finding
would have been a symptom of an implementation reading a finite-`k` agreement
window instead — which is obstruction H.  Sections 3-7 are the unconditional
replacement.  This is why register row 43's degree law was not re-used: its
caveat ("provably inert for P3") is not the reason it does not help here; the
reason is that the conditioned version of the question has no domain.

### 8.2 R1's stated kill condition cannot fire as written

`PATH.md` R1's kill condition is: "exhibit a Rule 30 space-time diagram, **or a
consistent formal model of one**, with `c` eventually periodic and `r` provably
aperiodic on the zero-set."  Read on the first disjunct it is unsatisfiable if
P1 is true, so it can never fire.  Read on the second disjunct it **has already
been satisfied** — a7 exhibits half-plane extensions `X(k,w)` with prescribed
eventually periodic `col_0`, nonempty at every `p = 2..8` with verified
witnesses — and R1 did not die, because a relaxed model is not a diagram.  So
R1 is a route whose stated falsifier is either vacuous or already-fired-without-
effect, depending on which disjunct is read.

This is **not** a1 section 6 note 3, which makes a different point (decidability
of `r|Z` from `c` and the truth of the implication are logically independent).
Both should stand; they are about different clauses.

**Do not over-read 8.2 into a general claim.**  It is a tautology of proof by
contradiction that any lemma sufficient for a theorem with a refutable
hypothesis is equivalent to that theorem, and that observation has no
discriminating power — it would equally "kill" a lemma that turned out easy.
The corollary above is worth recording only because it is about a specific
sentence in the register that reads as an operational test and is not one.

---

## 9. Validation, kept separate on purpose: the defect PDE and the closing step

Neither of these is new mathematics.  They are recorded because they make the
`p = 2` closing argument self-contained and uniform in `p`.

**(A) The exact defect equation.**  For any two Rule 30 diagrams with
`D = s XOR s'`:

```text
D(t+1,x) = D(t,x-1) XOR D(t,x) XOR D(t,x+1)
           XOR D(t,x)*s(t,x+1) XOR D(t,x+1)*s(t,x) XOR D(t,x)*D(t,x+1)
```

and for Rule 90, `D(t+1,x) = D(t,x-1) XOR D(t,x+1)` — **no coupling to the
underlying orbit at all**.  That difference is the OR nonlinearity in its
smallest form.  *Verified* (`defect_pde.py`): exact on all 64 local states for
both rules, and on 914,520 (rule 30) / 921,120 (rule 90) cells of genuine
stroboscopic pairs `(t, t+p)` of random finite orbits.  At `x = 0` with
`D(.,0) = 0` it reduces to the repo's `D(t,-1) = (1 XOR c_t) AND D(t,1)`
(re-checked, 5,736 checks, 0 violations).  **Label: a formulation, not a
theorem.**

**(B) The closing cascade, uniform in `p`.**  From the PDE, `D(t,x) = D(t,x+1)
= 0` implies `D(t+1,x) = D(t,x-1)` (exact, 16 states, both rules).  So if
`D(t,0) = 0` and `D(t,-1) = 0` for all `t >= t_1`, induction on depth gives
`D(t,-k) = D(t+k-1,-1) = 0` for every `k >= 1`.  The whole left quarter-plane
vanishes.  But the leftmost 1 of a nonzero finite row moves left at speed
exactly 1 (verified: 0 deviations over 300 random rows × 80 steps, both rules),
so `D(t, L_0 - t - p) = 1`, and `L_0 - t - p < 0` for large `t`.  Contradiction.

This is the content of Jen 1990 Prop. 3 / Kopra Thm 3.5 re-derived in three
lines, and it **generalises a2's Lemma B from `p = 2` to every `p`**, without
the 16-state enumeration and without a2's all-zero-cycle hole (which does not
arise, because the contradiction comes from the left edge rather than from a
cycle classification).  It is a trust-base improvement of a believed step, in
exactly the sense a2 labelled Lemma B.  **It is rule-generic** — it holds for
Rule 90 too — and that is consistent, because for Rule 90 it is (★) itself that
is false, not the closing step.

---

## 10. What is still missing, named precisely, with no "under an appropriate X"

Theorem W closes the bounded-window route.  It does not close (★).  The gap is
exactly this:

> **MISSING.**  `phi_t` reaches arbitrarily far back into `c` (Theorem W).  What
> is missing is a proof that the *residual* — the part of `phi_t` that a length-`m`
> window cannot capture — **fails to become eventually periodic in `t` when `c`
> is eventually periodic and `t` is restricted to `Z`**.  Equivalently: a proof
> that `eps(m) > 0` is realised *on the lone-seed orbit's own trace* rather than
> only across the ensemble of left-supported rows.

Theorem W's witness lives at `gamma = 0^m` with a specific hidden block.  For
(★) one needs the witness to be realised by the actual orbit at infinitely many
times of `Z`, which is a statement about a measure-zero set that Theorem U — an
ensemble statement — cannot see.  That is `PATH.md` obstruction E, reached from
a new direction and now with a named quantity attached (`eps(m)`) rather than a
general worry.

**A second question, flagged loudly because it is the one item here most likely
to be mis-read as progress: it is NOT a route to P1.**  It has a clean number
attached and looks tractable, and it is neither.  It is
recorded because nothing in the tree asks it: **does `eps_30(m) -> 0`?**  The
sequence falls from `1/4` to `0.1733` over `m = 1..16` with decrements around
`0.0013` and slowly shrinking; the data distinguishes neither a positive limit
nor a `~ c / log m` decay.  Note that even `eps(m) -> 0` would **not** prove
(★): (★) needs exactness, and Theorem W already shows exactness never arrives.
So this question is interesting for its own sake and is **not** a route to P1.
It is a bounded computation and obstruction H binds any extrapolation of it.

---

## 11. What a reader must not over-read

1. **(★) / Lemma Z is neither proved nor refuted.**  Register row 1 stays OPEN.
2. **Theorem W is rule-generic.**  It holds for Rule 90.  It is an obstruction,
   not a proof of P1, and obstructions are allowed — indeed strengthened — by
   being rule-generic.  What is *not* rule-generic is the quantitative content:
   `eps_90(m) = 1/2` exactly (proved) against `eps_30(16) ≈ 0.1733`.  Anyone
   citing Theorem W as "passing the Rule 90 filter" is misciting it.
3. **Theorems P, U, S, W are proved for LEFT-SUPPORTED initial rows only.**  The
   lone seed is one; `F^T(lone seed)` is not.  Do not apply them to row 31's
   reduction.
4. **`eps(m)` is an ensemble quantity.**  It is the Bayes error over the uniform
   measure on left-supported rows.  It says nothing directly about the single
   lone-seed orbit.  Section 7 is the orbit-level version, and it is a bounded
   computation with a `2 log2 T` ceiling.
5. **The `m = 29, 30` zeros in section 7 are vacuous** (0 and 3 repeat-window
   opportunities respectively).  The table carries that column so the zeros
   cannot be quoted as structure.
6. **Section 9 is validation.**  The defect PDE is a formulation; the closing
   cascade is Jen/Kopra re-derived.  Neither is offered as new.
7. **Section 8.2 is a remark about one sentence in the register, not a general
   theory of localisation.**  Section 8's own warning paragraph says why.
8. **Direction (b) as briefed was already in `PATH.md` section 2** and this arm
   found nothing there.
9. **The `eps` numerator sequence was not checked against OEIS** and no closed
   form is claimed.
10. **Nothing here is a Lean artifact and nothing here contains `sorry`.**

---

## 12. Reproduction

From this directory, in order.  Stdlib only; `uv run python`.

```bash
uv run python substrate.py                     # cross-validation vs common/rule30.py  (~2 s)
uv run python defect_pde.py    > defect_pde_output.txt      # section 9        (~30 s)
uv run python phi_anf.py 16    > phi_anf_output.txt         # Theorem P        (~3 s)
uv run python phi_reach.py 16  > phi_reach_output.txt       # influence/err(m,t) (~2 s)
uv run python phi_epsilon.py 21 > phi_epsilon_output.txt    # full err(m,t)    (~60 s)
uv run python eps_stability.py > eps_stability.txt          # Theorem S check  (~1 s)
uv run python eps_theorem.py 16 > eps_theorem_output.txt    # Theorems U, S    (~55 s)
uv run python witness.py       > witness_output.txt         # Theorems W, N    (~5 s)
uv run python orbit_window.py 60000 30 > orbit_window_output.txt  # section 7  (~2 s)
```

`substrate.py` validates its simulator against
`experiments/overnight-arms/common/rule30.py` (`center_column_bits` to `n = 2048`
and `simulate_seed` on 200 random finite seeds, plus an independently written
Rule 90 grid simulator on 100 more) and aborts on mismatch; every other script
imports it.  `eps_theorem.py` additionally cross-checks its own `eps(m)` against
the independent `2^t` enumeration in `phi_epsilon_results.json` at every
`(m, t >= 2m+1)` pair in range, and asserts on mismatch.

Files: `substrate.py`, `defect_pde.py` / `defect_pde_output.txt`, `phi_anf.py` /
`phi_anf_output.txt` / `phi_anf_results.json`, `phi_reach.py` /
`phi_reach_output.txt` / `phi_reach_results.json`, `phi_epsilon.py` /
`phi_epsilon_output.txt` / `phi_epsilon_results.json`, `eps_stability.py` / `eps_stability.txt`,
`eps_theorem.py` / `eps_theorem_output.txt` / `eps_theorem_results.json`,
`witness.py` / `witness_output.txt`, `orbit_window.py` /
`orbit_window_output.txt`.

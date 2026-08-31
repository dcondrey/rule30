# NEGATIVE. Kopra Problem 3.1.13 is not settled here. The missing lemma is a separating family uniform in its index: an explicit infinite family `{w_j}` in `L(Sigma_2(W30))` whose follower sets are proved pairwise distinct for ALL `j` (which would give NOT SOFIC), or a finite bound `B` with `Q_B = Q_{B+1}` in the rightward-extendability chain (which would give SOFIC). Neither exists; every candidate we produced is verified only over a finite window.

Arm a10, `experiments/overnight-arms/frontier_attack/a10_trace_soficness/`. Run 2026-08-30.
Nothing in this document is a proof of P1 or P2, and nothing in it bears on either
(section 2 says exactly why).

Two things WERE proved, and they are the reason the arm is worth reading:

* **`Sigma_1(W30)` is the full shift `{0,1}^N`** — and so is `Sigma_1(F)` for every
  one of the 16 left-permutive ECAs, Rule 90 included. So **the object named in
  this arm's own charter is trivially sofic and rule-blind**; it fails the Rule 90
  filter by construction. Section 1.
* **`Sigma_2(W90)` is the full shift `({0,1}^2)^N`, hence sofic**, by convergence of
  the fixed-point chain at round 2 to a one-state automaton, independently
  confirmed by exhaustive enumeration (`|L_n| = 4^n` for all `n <= 12`).
  Section 4. The Rule 30 / Rule 90 separation lives at width 2, not width 1.

Quantified claim carried forward: **`Sigma_2(W30)` has at least 492 distinct follower
sets** (scope in section 5). 492 is finite and therefore consistent with soficness;
it is a lower bound and nothing more.

---

## 0. Provenance flags on the citations (read first)

**One statement this document's framing depends on is proxy-retrieved, not
PDF-read**, because `utupub.fi` 403s on every direct path to the Kopra thesis PDF
and every alternative route was exhausted (three utupub URL shapes, `urn.fi`,
oldtucs TLS failure, CORE, OpenAIRE, BASE, Semantic Scholar):

* Kopra thesis, **Problem 3.1.13**: "Is `W30` regular?" — PROXY ONLY, and the
  thesis is the **unique** source for the Rule 30 instantiation: the phrase occurs
  in no published venue reachable here, including Kopra's own arXiv:2202.13809
  (checked page by page, all 12 pages) and arXiv:2211.15293. Cited by number only,
  without page numbers, and without a verbatim quotation of thesis Def 2.4.4.

The *definition* of regularity, on the other hand, is now PDF-read from two
independent sources and does not rest on the proxy:

* **Kůrka, ETDS 17(2):417-433 (1997)**, read from the author's own PostScript at
  `cts.cuni.cz/~kurka/equi.ps` (Cambridge Core 500s; `equi.pdf` 404s). Definition 4
  and: *"A cellular automaton is regular, if all its one-sided factor subshifts are
  regular (i.e. sofic systems)."* This is the origin of the notion.
* **Kopra, arXiv:2211.15293v2, Def. 5.15, p.38** (PDF-read), restating it and
  attributing it to Kůrka 1997: *"A dynamical system (X, T) with X a
  zero-dimensional compact metrizable space is called regular if all its one-sided
  subshift factors are sofic shifts,"* followed by *"to check the regularity of
  (X, F) for a CA F it is sufficient to check whether all of its trace subshifts
  are sofic shifts, i.e. whether the trace subshifts of all widths are sofic."*

**The verdict does not depend on any of this.** "Problem 3.1.13 is not settled
here" holds however regularity is defined; the citations support only section 1's
reduction from `Sigma_2` non-soficness to a negative answer.

Per-citation status:

| statement | status |
|---|---|
| Kopra, arXiv:2202.13809, Def 2.6, Ex 2.3, Thm 3.5, Problem 4.8, Rule 90 remark | PDF-read |
| Kopra thesis Thm 3.1.12 ("finite configuration" wording) | string-presence confirmed in PDF |
| Kopra thesis Problem 3.1.13 ("Is `W30` regular?") | **proxy only**, and the unique source for that instantiation |
| "regular CA = all one-sided subshift factors sofic" | PDF-read twice: Kurka ETDS 1997 `equi.ps` Def 4 (origin), and Kopra arXiv:2211.15293v2 Def 5.15 p.38 |
| arXiv:2202.13809 contains no soficness/regularity material | PDF-read, complete 12-page absence check |
| Kurka, ETDS 17 (1997) 417-433 | obtained as the author's PostScript `cts.cuni.cz/~kurka/equi.ps` and read there (Cambridge Core HTTP 500). Its Definition 4 and the three-class list L1/L2/L3 are quoted from it. Its **other** theorem numbers are still unverified, so Thm 52/53 below carry the numbering of Kurka's survey `cantor.pdf`, where the 1997 paper is ref [28]. |
| Cervelle-Formenti-Guillon, CiE 2007 (arXiv:math/0703241) and STACS 2010 (arXiv:1001.0251) | PDF-read |
| Lind & Marcus, Thm 3.2.10 (sofic iff finitely many follower sets) | number confirmed from citing literature, **not from the book** |
| `Sigma_1` = full shift for left-permutive ECAs | **no published theorem found.** Proved here; corroborated by NKS note 10-10, "all 2^t possible single columns of t cells can be generated from some initial condition" |
| "Gillman and Kopra" | **no such paper.** The Rule-30-adjacent author is **R. H. Gilman** (one L), "Classes of cellular automata", ETDS 7 (1987) 105-118, cited by Kurka for a CA whose column subshift is not sofic. David Gillman has no CA work (OpenAlex, 34 works). |

---

## 1. What `W30` is, and why the charter's object is the wrong one

Conventions, following Kurka's survey Definition 50 and Kopra arXiv:2202.13809
Definition 2.6: configurations are two-sided (`X = {0,1}^Z`), traces are one-sided
(`t in N`). For `k >= 1` the *k-th column subshift* is

        Sigma_k(F) = { ( F^t(x)_{[0,k)} )_{t >= 0}  :  x in {0,1}^Z }  in  ({0,1}^k)^N.

`Sigma_k(F)` is a continuous shift-commuting image of a compact space, and Rule 30
is surjective, so it is a genuine subshift and its language is its factor set.
Write `c_x(t) = F^t(x)_x` for the columns of one space-time diagram.

**This arm's charter named `Sigma_1(W30)`: "the column-0 factor of the full shift
under Rule 30". That object is the full shift.**

> **Theorem 1.** Let `F` be a left-permutive ECA, i.e.
> `s(t+1,x) = s(t,x-1) XOR g(s(t,x), s(t,x+1))`. Then `Sigma_1(F) = {0,1}^N`.
>
> *Proof.* Induction on `t` gives `s(t,0) = x_{-t} XOR G_t(x_{-(t-1)},...,x_t)`:
> the base case is the rule itself, and `s(t+1,0) = s(t,-1) XOR g(s(t,0),s(t,1))`
> where `s(t,-1) = x_{-(t+1)} XOR G_t(x_{-t},...,x_{t-1})` and `s(t,0), s(t,1)`
> depend only on cells `x_{>= -t}`. So the dependence is triangular. Fix
> `x_1, x_2, ...` arbitrarily; choose `x_0` to realise the trace bit at `t = 0`,
> then `x_{-1}` for `t = 1`, then `x_{-2}` for `t = 2`, and so on. Every word is
> realised. QED

Verified exhaustively: `width1_full_shift.py` enumerates all `2^17` width-17 cell
windows for each of the 16 left-permutive ECAs and finds `|L_9| = 512 = 2^9` for
all 16, with no exceptions; non-left-permutive controls are proper
(rule 110: 310/512; rule 232: 18/512; rule 4: 3/512; rule 0: 2/512).
`exact_language.py` gives the same for rules 30 and 90 at every `n <= 13`.

**Consequence — this is the Rule 90 filter firing on the charter.** Rule 30 and
Rule 90 give the identical answer at width 1, as does every other left-permutive
ECA. A soficness question about `Sigma_1` therefore cannot be a question about
Rule 30. That is why Kopra's Problem 3.1.13 does not ask it.

**What Kopra actually asks.** Problem 3.1.13 is "Is `W30` regular?", and regularity
of a CA is defined (thesis Def 2.4.4, proxy-flagged above) as *all* its subshift
factors being sofic. The reduction to a single width is the standard one: by
Kurka's survey Definition 50(3) each `phi_k` is a factor map, so **`Sigma_k(W30)` is a
subshift factor of `({0,1}^Z, W30)` for every `k`**, and therefore

> **Reduction.** `Sigma_2(W30)` NOT sofic  ==>  `W30` not regular  ==>
> Problem 3.1.13 answered negatively.

This direction is free and needs no intermediate theorem. The converse direction
does need Blanchard-Maass / Di Lena (Kurka survey Thm 52(2)): for radius `r`, if
`Sigma_{2r+1}(F)` is sofic then every factor subshift is sofic; with `r = 1` that is
`Sigma_3`. And dropping the third coordinate is a 1-block code, so
`Sigma_3` sofic `=>` `Sigma_2` sofic for free.

So the whole problem sits between widths 2 and 3. Measured, and **conjecture
only**: `|L_n(Sigma_3(W30))| = 2 * |L_n(Sigma_2(W30))|` at every `n = 2..12`
(`width_k_language.py`; 24/12, 64/32, 160/80, ..., 179688/89844), and the same
factor-2 relation holds for Rule 90. Counting agreement at `n <= 12` is not a
conjugacy and does **not** prove `Sigma_2` sofic `=> Sigma_3` sofic. Everything below
therefore works on `Sigma_2`, where the implication that matters is unconditional.

---

## 2. What a soficness answer would and would not imply for P1

Write it out, because the charter asked and because the trap is real.

1. **`Sigma_1(W30)` = full shift (Theorem 1) carries zero information about P1.** The
   full shift contains eventually periodic points and non-eventually-periodic
   points alike. P1 asks about ONE point of it. This is the precise reason P1 is
   not a subshift question at all, and it is the same shape as PATH.md
   obstruction C (single-column blindness) one level up: a subshift is blind not
   just to one column of a diagram but to any single point of itself.
2. **Soficness or non-soficness of `Sigma_2`, of `Sigma_3`, or regularity of `W30`
   implies nothing about P1 in either direction.** Sofic shifts contain aperiodic
   points; non-sofic shifts contain eventually periodic ones. There is no
   implication to be had.
3. **The one reading that touches P1 is a different object**: the orbit closure of
   the lone-seed centre column `a = A051023`. If `a` is eventually periodic its
   orbit closure is finite, hence sofic; so *non*-soficness of that orbit closure
   would prove P1. That target therefore **implies the prize problem and is
   strictly harder than it** — it is not a cheaper route, and it must not be
   confused with Problem 3.1.13, which quantifies over all configurations.
4. **The single-point ladder is separate and partly settled.** Kopra
   arXiv:2202.13809 Thm 3.5 (PDF-read): "If `F` is rapidly left expansive with
   width `w` and `x in N(Sigma)`, then `Tr_{[i,i+w-1]}(x)` is not eventually
   periodic for any `i`" — width-2 aperiodicity for number-like configurations,
   Rule 30 included. Problem 4.8 of the same paper *is* P1: "Let `x = ...0001000...`
   ... Is `Tr_{W30,0}(x)` eventually periodic?", with "The answer 'no' is expected."

Register consistency: this arm neither advances nor kills any P1 row. Row 7's
sentence "irrelevant to soundness here, since each `S_k` is regular by
construction" stands; this arm attacks the open problem that sentence sets aside,
and finds it open.

---

## 3. The exact structure of `Sigma_2`: a rightward-extendability game

Left permutivity splits the diagram. Given the pair `(c_0, c_1)`, the columns to
the left are *defined outright* by

        c_{x-1}(t) := c_x(t+1) XOR ( c_x(t) OR c_{x+1}(t) ),

and they satisfy the local rule at every `x <= 0` by construction: no constraint
comes from the left. All the constraint is on the right. The rule at `x = 1`,

        c_1(t+1) = c_0(t) XOR ( c_1(t) OR c_2(t) ),

is solvable for `c_2(t)` iff `c_1(t) = 1 => c_1(t+1) XOR c_0(t) = 1` — this is
exactly the boundary pin of register row 55 — and then `c_2(t)` is forced where
`c_1(t) = 0` and free where `c_1(t) = 1`. Hence

> **Proposition 2.** `(c_0, c_1) in Sigma_2(W30)` iff the rightward chain
> `c_2, c_3, ...` can be continued forever.

Define the monotone operator on subshifts of `({0,1}^2)^N`

        Phi(Q) = { (c_0,c_1) : exists c_2 with the rule at x=1 holding for all t
                                and (c_1,c_2) in Q }.

Then `Sigma_2(W30)` is the **greatest fixed point** of `Phi`, and equals
`intersection_k Q_k` for `Q_0 = everything`, `Q_{k+1} = Phi(Q_k)`, by compactness.
`Q_k` = pairs extendable to rightward depth `k`. Each `Q_k` is **sofic by
construction** (one existential projection of a memory-1 SFT), so the chain is a
decreasing chain of sofic shifts whose intersection is the object in question.

This yields a genuine decision procedure on one side:

> **If `Q_{B+1} = Q_B` for some `B`, the greatest fixed point IS `Q_B`, so
> `Sigma_2` is sofic — a proof, not evidence.**
> If the chain is strictly decreasing as far as computed, **that decides nothing**:
> a strictly decreasing chain of sofic shifts can have sofic intersection.

`fixpoint.py` implements `Phi` as NFA construction (state `(q, a, b, e)` carrying
the one-step lookahead obligation) plus subset construction plus partition-refinement
minimisation, with an exact product-reachability language-equality test.

---

## 4. Result of the fixed-point run (`out/fixpoint.json`, `out/fixpoint.log`)

**Rule 90 — control, and it is a theorem.** For Rule 90 the rule at `x=1` reads
`c_1(t+1) = c_0(t) XOR c_2(t)`, so `c_2` always exists and is unique: `Phi` is the
identity on the full shift. The run **converges at round 2** to a 1-state
automaton, i.e.

> `Sigma_2(W90) = ({0,1}^2)^N`, the full shift, **SOFIC**.

Independently confirmed by exhaustive enumeration: `|L_n| = 4^n` exactly for
`n = 1..12` (`width_k_language.py`), and every follower-set count is exactly 1
(section 5). The control could have failed and did not.

**Rule 30 — no fixed point, a state-count wall.**

| round `k` | `|Q_k|` states | first word length where depth `k` beats depth `k-1` |
|---|---|---|
| 1 | 3 | - |
| 2 | 8 | 3 |
| 3 | 14 | 6 |
| 4 | 42 | 7 |
| 5 | 185 | 8 |
| 6 | 1000 | 9 |
| 7 | 7020 | 10 |
| 8 | 90318 | 11 |
| 9 | killed at 3.4 GB RSS, 90+ min, determinisation incomplete | - |

`Q_1 > Q_2 > ... > Q_8` strictly, with a separating word length recorded at every
step. So no fixed point is reached, and the kill mode is the one PATH.md R7
predicted for the sibling ladder: state blowup, not compute time.

**The depth law (measured for `k = 2..7`, NOT proved).**

> `Q_{k+1}` first differs from `Q_k` at word length `k+4`. Equivalently
> **`Q_k` agrees with `Sigma_2(W30)` exactly on all words of length `<= k+3`:
> one extra column of rightward depth buys exactly one more letter of the word.**

Cross-checked against exhaustive light-cone enumeration: `Q_8` reproduces
`|L_11| = 38616` exactly and misses `|L_12| = 89844` (it gives 89876). This is a
*linear* wall, unlike PATH.md obstruction A's `O(log t)` wall, and it is the sharp
obstruction of this arm: deciding a length-`n` word needs rightward depth `n-3`,
so no `Q_k` we can build is `Sigma_2`. It still decides nothing about soficness.

---

## 5. The follower-set ladder, and the bound obstruction H forces

Criterion (Lind & Marcus Thm 3.2.10, number confirmed from citing literature only):
a shift space is sofic iff it has finitely many follower sets
`F(w) = { v : wv in B(X) }`.

The **language** here is exact, not approximated: with neighbourhood `{-1,0,1}` the
width-`k` trace letters `t = 0..n-1` depend only on cells `[-(n-1), n-2+k]`, and
every assignment of that window extends to a configuration of `Z`, so exhaustive
enumeration of the `2^(2n+k-2)` windows gives `L_n` exactly. The **follower
truncation** is the approximation:

        f(n, m) = #{ F_m(w) : w in L_n },   F_m(w) = { u in Sigma^m : wu in L }.

**OBSTRUCTION H, in the same sentence as the numbers.** Distinct `F_m` implies
distinct `F`, so `f(n,m)` is a **LOWER BOUND** on the number of follower sets and is
monotone nondecreasing in both `n` and `m`. Finitely many observed does not prove
sofic — a larger `m` can split classes. Unboundedly many observed up to `(n,m)`
does not prove non-sofic without an argument uniform in `n` and `m`.

`follower_table.py`, `k = 2`, exact `L_14` (all `2^28` width-28 cell windows):

**Rule 30** — `f(n,m)`, rows `n`, columns `m`:

```
  n\m    1     2     3     4     5     6     7     8     9    10    11    12    13
   1     3     4     4     4     4     4     4     4     4     4     4     4     4
   2     3     6     7     8    10    11    12    12    12    12    12    12
   3     3     6     8    11    16    22    29    31    32    32    32
   4     3     6    11    18    31    47    65    73    76    78
   5     3     6    14    28    54    93   137   162   179
   6     3     7    16    37    89   169   272   347
   7     3     7    18    47   126   267   492
   8     3     7    19    55   177   416
   9     3     7    19    63   224
  10     3     7    19    66
  11     3     7    19
  12     3     7
  13     3
```

**Rule 90** — the same table is **identically 1** in every cell. One follower set,
the full shift, sofic. The method separates the two rules cleanly; it is not
measuring the wrong thing.

**The claim carried forward, with its scope stated literally:**

> `Sigma_2(W30)` has **at least 492 distinct follower sets**. Scope: 492 words of
> length 7 in `L_7`, pairwise distinguished by continuations of length 7; the
> language is exact by exhaustive enumeration of all `2^28` width-28 cell windows,
> which is the exact light cone for width-2 words of length 14. **492 is finite and
> is therefore consistent with `Sigma_2(W30)` being sofic.** It is a lower bound.

Reading the columns: for fixed `m`, `f(n,m)` saturates in `n` at
`g(1)=3, g(2)=7, g(3)=19` (confirmed: `m=3` is 19 at `n = 8,9,10,11`),
and `g(4) >= 66` (still rising at `n=10`, so not yet saturated). A tempting fit
`2*3^(m-1)+1` matches 3, 7, 19, 55 and was **refuted** by extending the window from
`N=12` to `N=14`: `f(9,4) = 63` and `f(10,4) = 66` exceed 55. Recorded because it is
exactly the trap this ladder invites — the saturation of `f(n,m)` in `n` at `N=12`
was an artifact of the window, not a limit.

---

## 6. Which standard technique fails, and precisely how

The textbook route from "the table grows" to "not sofic" is a **separating family**:
words `w_1, w_2, ...` in `L` with pairwise distinct follower sets, exhibited by
explicit continuations, and made provable for all indices by pumping,
`w_j = x y^j z`. `pump_search.py` runs the finite half of that search inside exact
`L_14`.

**Search scope, stated because the finding is scope-limited:** `|y| in {1,2,3}`,
`|x| <= 2`, truncation `m in {3,4}`, `j` up to the window limit
`|x| + j|y| + m <= 14`, over the full alphabet `Sigma = {0,1}^2`.

**Pass 1, `|y| <= 2`, `m = 4`** (`out/pump_search_rule30_N14_m4.json`): 15 families
with pairwise distinct follower sets, **all 4 members long, all built on
`y = [1,3]` or `y = [3,1]`** (letter `a = c_0 + 2 c_1`, so `1 = (1,0)`, `3 = (1,1)`;
the block is `c_0 = 11`, `c_1 = 01`). Follower sizes along the best family
`y = [1,3]`, `x` empty: **48, 44, 32, 16** -- strictly shrinking -- and then
`(13)^5` **leaves the language**, which is why the family stops. At `m = 3`, 2
families, longest 4 members.

**This pass looks like a disjointness result and is not one.**
`periodic_survival.py` measures, for every block `|u| <= 4`, the largest `j` with
`u^j in L_14`: of 340 blocks, 288 die inside the window and 52 reach the window
edge undecided. But the survivors with `|u| <= 2` are exactly
`[0], [1], [2], [00], [11], [22]` -- and `[00], [11], [22]` generate the same words
as `[0], [1], [2]`, so **the survival side of pass 1's searched set is three
constant letters**, which cannot encode an index in the first place. The apparent
disjointness of separation and survival was fixed by the scope before the search
ran. It is a property of `|y| <= 2`, not of Rule 30. Rule 90 control, same script
at `N = 12`: **all 340 blocks survive**, as they must in a full shift
(`out/periodic_survival_N12.json`).

**Pass 2, `|y| = 3`, `m = 3`** (`out/pump_search_rule30_N14_m3_y3.json`), run
against exactly the non-constant survivors pass 1 had missed: **27 families with
pairwise distinct follower sets, and 10 of them sit on blocks whose powers survive
to the window edge** --

```
[0,0,3]  [0,1,3]  [0,2,3]  [0,3,0]  [1,3,0]  [2,3,0]  [2,3,1]  [3,0,0]  [3,0,1]  [3,1,2]
```

-- best family `x = [0]`, `y = [0,1,3]`, follower sizes **20, 12, 8**, strictly
shrinking, with explicit separating continuations (`j=1` vs `j=2` by `[0,2,2]`;
`j=1,2` vs `j=3` by `[0,0,0]`). Every one of them is **3 members long, and 3 is the
window ceiling**: `|x| + 3j + m <= 14` forces `j <= 3`.

> **The honest obstruction.** Exact `L_14` is **underpowered** for the pumping
> route at `|y| = 3`, not negative on it. Ten concrete candidate families for
> Lemma U (U-neg) exist on surviving blocks; each is verified separating for
> `j = 1,2,3` and cannot be pushed further inside this window. What a larger exact
> language would buy is directly quantifiable: each `+3` of window length adds one
> member to every `|y| = 3` family, so `L_20` would take them to `j = 5` and `L_26`
> to `j = 7` -- and `L_N` costs `2^{2N}` window enumerations, i.e. `2^40` at `N=20`.
> That is the compute wall on the finite half. The infinite half -- proving the
> separation for all `j` -- is the actual missing lemma and no amount of window
> buys it.

The consequence for the proof strategy is concrete and positive: the search
identified a short list of pumped candidates on blocks that persist, and the next
step for anyone continuing this arm is to take one of those ten and prove its
separation by induction on `j` using the rightward-extendability game of section 3,
rather than to search wider.

Two further standard techniques, reported honestly:

* **Deciding it.** Cervelle-Formenti-Guillon, STACS 2010 (arXiv:1001.0251), Thm 5.6
  (PDF-read) is a Rice theorem for traces: any property satisfied by some but not
  all traces of CA over `{0,1}` and stable under ultimate coincidence is undecidable
  — and the text immediately after names **soficness** as one such property. So
  there is no general algorithm; the fixed-point procedure of section 3 is a
  semi-decision procedure for the *sofic* side only, and section 4 shows it not
  halting through depth 8.
* **Getting soficness from dynamics.** Kurka survey Thm 53 (attributed to [28] =
  ETDS 1997; the 1997 paper itself was unobtainable): if every `Sigma_k(F)` is an SFT
  then `F` has shadowing, and shadowing implies every factor subshift is sofic.
  Inapplicable: `Sigma_2(W30)` is not an SFT at any order we can certify, and Rule 30
  is not equicontinuous. The known concrete non-sofic column subshift is Kurka's
  Example 6, attributed to **Gilman 1987** — `F(x)_i = x_{i+1} x_{i+2}`, with the
  explicit forbidden structure `x_[n,n+1] = 10 => x_[n,2n+1] = 10^{n+1}`. That is a
  counter encoded by a *spreading* rule; Rule 30 has no such visible counter, and
  finding one is precisely the missing family.

---

## 7. The missing lemma, named

> **LEMMA U (missing).** Either
> **(U-neg)** an explicit family `{w_j}_{j >= 1}` in `L(Sigma_2(W30))` together with
> continuations `{v_j}` such that `w_i v_j in L` iff `i = j`, with the separation
> proved for all `j` — giving infinitely many follower sets, hence `Sigma_2(W30)`
> non-sofic, hence `W30` not regular, hence Kopra Problem 3.1.13 answered NO;
> or
> **(U-pos)** a bound `B` with `Q_B = Q_{B+1}` in the chain of section 3 — giving
> `Sigma_2(W30) = Q_B` sofic.

What is proved here reaches neither. Section 6 leaves (U-neg) with ten explicit
candidate families, each verified separating for `j = 1,2,3` and each capped there
by the window, not refuted. Section 4's linear depth law is the obstruction to
(U-pos): the chain buys one letter per column, so `B`, if it exists, is not small,
and the automata are already 90318 states at `k = 8`.

No proof artifact was produced, and none contains `sorry`.

---

## 8. What a reader must not over-read

* **"Rule 30's centre-column trace subshift is the full shift" is true (Theorem 1)
  and says nothing about the open problem.** It is true for all 16 left-permutive
  ECAs. It is not Kopra's question.
* **492 follower sets is a lower bound consistent with soficness.** It is not
  evidence of non-soficness. Neither is the growth of the table: the whole content
  of obstruction H is that a finite window cannot distinguish "grows forever" from
  "grows then stops".
* **The `f(n,m)` saturation values are window-dependent.** `g(4) = 55` looked
  saturated at `N = 12` and is at least 66 at `N = 14`. Any fitted formula from
  this table is untrustworthy; one was fitted and refuted inside this run.
* **The fixed-point chain not converging through depth 8 is not evidence of
  non-soficness.** A strictly decreasing chain of sofic shifts can intersect to a
  sofic shift.
* **`|L_n(Sigma_3)| = 2 |L_n(Sigma_2)|` is a measured coincidence at `n <= 12`, not a
  conjugacy**, so the `Sigma_2 -> Sigma_3` direction of the reduction is not available.
* **Section 6 is not a negative on pumping.** The `|y| <= 2` pass looks like a
  disjointness result and is a scope artifact; the `|y| = 3` pass finds ten
  separating families on surviving blocks and is cut off at three members by the
  window. Do not cite this arm as having ruled out the pumping route.
* **Nothing here bears on P1 or P2.** See section 2, all four bullets.

---

## 9. Files

| file | what it does | output |
|---|---|---|
| `exact_language.py` | exact `L_n` of `Sigma_1` for rules 30 and 90, `n <= 13` | `out/exact_language.json` |
| `width1_full_shift.py` | Theorem 1 stated + verified for all 16 left-permutive ECAs, with non-left-permutive controls | `out/width1_full_shift.json` |
| `width_k_language.py` | exact `L_n` of `Sigma_k`, `k <= 3`, `n <= 12`, both rules | `out/width_k_language.json` |
| `fixpoint.py` | the `Phi` chain: NFA construction, determinisation, minimisation, exact language equality; the one procedure that could have PROVED soficness | `out/fixpoint.json`, `out/fixpoint.log` |
| `follower_table.py` | 2-D follower-set lower-bound table `f(n,m)`, chunked exact enumeration | `out/follower_table_k2_N12.json`, `..._N14.json`, `out/follower_table_N14.log` |
| `follower_ladder.py` | the `n+m=N` diagonal of the same, kept as the first-pass artifact | `out/follower_ladder_k2_N12.json` |
| `pump_search.py` | search for a pumped separating family `x y^j z`; `--ylens` selects block lengths | `out/pump_search_rule30_N14_m3.json`, `..._m4.json` (`|y|<=2`), `..._m3_y3.json` (`|y|=3`), `out/pump_search.log` |
| `periodic_survival.py` | max `j` with `u^j in L` for every `|u| <= 4`, both rules | `out/periodic_survival_N14.json` (rule 30), `out/periodic_survival_N12.json` (rule 90) |
| `out/L_30_k2_n14.npy` | cached exact `L_14` (476596 words) | - |

Cross-validation actually run, in both directions: the `Phi` automata reproduce the
brute-force `|L_n|` exactly for every `n <= k+3` (`Q_8` gives `|L_11| = 38616`,
matching exhaustive enumeration over `2^24` windows), and the brute-force
enumerator agrees with the repo ground-truth generator via
`experiments/overnight-arms/common/rule30.py`'s own self-test.

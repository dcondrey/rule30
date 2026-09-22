# Proof: driven-lhp-column-minus-one-aperiodic (direct)

**Correction, 2026-09-15:** the driven-LHP aperiodicity proof stands, but
the literal PIN-Pi statement in section 5(b3) is false, witnessed by
`c=110^infinity`. Only the pin tests at times zero and one are nonvacuous,
and both pass. The full zero-initial right/left glue fails at time two.
See [the scope audit](../../../../../docs/rule30/RESULTS-r1-periodic-realization-scope.md).

Date: 2026-09-03.  Style: direct.  Status: **PROVED**, with two precision
corrections to the lemma text (section 0) and no gaps.

Everything below is one of: an exhaustive check over all argument tuples
(script `driven_lhp_direct_checks.py`, log `driven_lhp_direct_checks.log`,
both in this directory); a derivation written out in full; or a finite gate
of a definition against an explicit reference.  The proof itself uses no
finite computation; the checks pin the three local identities it rests on
and the identifications it makes.

## 0. Statement, with the two corrections

**Theorem.**  Let `y : {x <= -1} -> {0,1}` have finite support, let
`c = (c_t)_{t >= 0}` be an eventually periodic binary word, and let
`s = LHP_y(c)` be the driven left half-plane of definition D2.  Assume

```text
(N)   y_x = 1 for some x <= -1,  or  c_t = 1 for some t >= 0.
```

Then `l_t := s(t,-1)` is not eventually periodic.

**Correction 1 (hypothesis).**  The lemma says "for every nonzero finite
y".  If `y` is read on `x <= 0` with `y_0 := c_0`, "nonzero" implies (N);
(N) is the weakest hypothesis under which the conclusion holds, and it is
necessary: with `y = 0` on `x <= -1` and `c = 0^omega` the half-plane is
identically zero and `l = 0^omega` is periodic (CHECK8, first line).  The
lemma's proof sketch justifies the moving edge in the `y = 0` case by "the
first time `c_t = 1`, which exists since `c` has infinitely many ones"; an
eventually periodic `c` need not have infinitely many ones (`c = 1 0^omega`),
but only one `1` is needed (Lemma A; CHECK8, second line, exercises
`c = 1 0^omega`: the edge holds and `l` has no period `q <= 64` to `T = 4096`).

**Correction 2 (consequence (b)).**  The sentence "any proof of P1 must use
the coupling at the zero-times" is not a theorem as written.  Section 5
proves the exact facts the lemma states there ((b1) the left half-plane is
consistent with every boundary word; (b2) its only self-constraint is the
pin), an exact "glue" reformulation of P1 ((b4)), and a dichotomy ((b3))
that says precisely when the sentence is true: exactly when some eventually
periodic drive is pin-consistent forever, which is the open statement
(PIN-Pi) screened in `../r1-r1zero-screen-pin-pi-no-periodic/`.

Consequence (a) is proved in full in section 4.  "R1 is equivalent to P1"
is proved as (a7).

## 1. Definitions

**D1.**  Rule 30 is `f(a,b,d) = a XOR (b OR d)`, applied as
`s(t+1,x) = f(s(t,x-1), s(t,x), s(t,x+1))`.

**D2 (driven left half-plane).**  For `y` and `c` as above, `LHP_y(c)` is
the unique `s : N x {x <= 0} -> {0,1}` with

```text
(i)   s(0,x) = y_x                                  for x <= -1
(ii)  s(t,0) = c_t                                  for t >= 0
(iii) s(t+1,x) = f(s(t,x-1), s(t,x), s(t,x+1))      for t >= 0, x <= -1
```

Existence and uniqueness: row `0` is fixed by (i) and (ii); given row `t`
on `x <= 0`, (iii) fixes row `t+1` on `x <= -1` because the three positions
`x-1, x, x+1` read are all `<= 0`, and (ii) fixes position `0`; induction on
`t`.  Rows keep finite support: `f(0,0,0) = 0`, so if row `t` vanishes for
`x < m` then row `t+1` vanishes for `x < m-1`.  In the mirrored bit
convention of `r1zero_lib.driven_lhp` (bit `i` holds `s(t,-i)`) this is
`row(t+1) = ((row >> 1) XOR (row OR (row << 1))) with bit 0 := c_(t+1)`;
CHECK4 gates that kernel against an explicit cell array on 127,592 cells
(60 random `(y,c)` pairs, Rules 30 and 90), 0 mismatches.

**D3.**  A word `u` is *eventually periodic* if there are `p >= 1`, `t0 >= 0`
with `u_{t+p} = u_t` for all `t >= t0` ("`p`-periodic from `t0`").

**D4.**  `Z = {t : c_t = 0}`, enumerated `z_0 < z_1 < ...` when infinite.
"`u` restricted to `Z` is eventually periodic" means the sequence
`i -> u_{z_i}` is eventually periodic in the sense of D3.  (This is the sense
of R1 in `PATH.md` section 2: its derivation of "column `-1` eventually
periodic implies `r|Z` eventually periodic" yields a time-index period that
is a multiple of `p`, which is an instance of D4.  The alternative reading
"`u_{t+q} = u_t` whenever `t, t+q in Z` and `t` is large" is degenerate for
arbitrary `q`: for `c = (01)^omega` beyond the transient and `q` odd it holds
vacuously for every `u`.  It coincides with D4 when `q` is a multiple of
`p`, by (a5) and (a6) below.)

## 2. The three local identities (exhaustive)

**I1 (inverse rule).**  For all `a, b, d in {0,1}`:
`a = f(a,b,d) XOR (b OR d)`.  Exhaustive over the 8 triples, also for Rule
90's `a XOR d`: CHECK2, 0 failures.  Consequently, in `LHP_y(c)`, for all
`t >= 0` and `x <= -1`,

```text
s(t, x-1) = s(t+1, x) XOR (s(t,x) OR s(t,x+1)).                       (I1)
```

**I2 (edge step).**  `f(0,0,1) = 1` and `f(0,0,0) = 0`.  CHECK3, 0 failures
(also Rule 90).

**I3 (rule at x = 0 with r free).**  For `c_t, c_{t+1}, l_t in {0,1}`: there
is `r in {0,1}` with `c_{t+1} = l_t XOR (c_t OR r)` iff
`(c_t = 0) or (l_t = 1 XOR c_{t+1})`; when `c_t = 0` the solution is unique,
`r = c_{t+1} XOR l_t`; when `c_t = 1` and `l_t = 1 XOR c_{t+1}` both values
of `r` work.  Exhaustive over the 8 triples: CHECK1, 0 failures.

## 3. Proof of the theorem

**Lemma A (moving edge).**  Assume (N).  Define `(a, t0)`: if `y_x = 1` for
some `x <= -1`, let `a = min{x <= -1 : y_x = 1}` (finite support) and
`t0 = 0`; otherwise let `a = 0` and `t0 = min{t : c_t = 1}`.  Put
`e(t) = a - (t - t0)`.  Then for every `t >= t0`:

```text
s(t, e(t)) = 1   and   s(t, x) = 0 for all x < e(t).                   (A)
```

*Proof.*  Base `t = t0`.  Case 1 (`y` has a `1` at some `x <= -1`): `t0 = 0`,
`s(0,a) = y_a = 1` by (i), and `s(0,x) = y_x = 0` for `x < a` by minimality
of `a`.  Case 2 (`y = 0` on `x <= -1`): then `c_t = 0` for `t < t0` and
`c_{t0} = 1`.  Claim: `s(t,x) = 0` for all `x <= -1` and all `t <= t0`.
Induction on `t`: `t = 0` is (i).  If row `t` vanishes on `x <= -1` and
`t < t0` (so `s(t,0) = c_t = 0`), then for every `x <= -1` the three
arguments of (iii) at `(t+1,x)` are `s(t,x-1), s(t,x), s(t,x+1)`, all at
positions `<= 0`, all zero, so `s(t+1,x) = f(0,0,0) = 0` by I2.  Hence row
`t0` vanishes on `x <= -1`, and `s(t0, 0) = c_{t0} = 1 = s(t0, a)` with
`a = 0`, `e(t0) = 0`.  So (A) holds at `t0` in both cases.

Step.  Assume (A) at some `t >= t0` and write `e = e(t)`; note `e <= a <= 0`.
Since `e - 1 <= -1`, (iii) applies at `(t+1, e-1)`:
`s(t+1, e-1) = f(s(t,e-2), s(t,e-1), s(t,e)) = f(0,0,1) = 1` by (A) and I2.
For `x < e-1` (so `x <= -1`): `s(t+1,x) = f(s(t,x-1), s(t,x), s(t,x+1))` with
`x-1 < x < x+1 < e`, all three zero by (A), so `s(t+1,x) = f(0,0,0) = 0`.
This is (A) at `t+1`, since `e(t+1) = e - 1`.  QED.

The step uses nothing about `c` after `t0`.  CHECK5 exercises (A) on 40
random drives (both cases, Rules 30 and 90) to `T = 600`: 24,040 rows, 0
violations.  The screening log
`../r1-r1zero-screen-driven-lhp-column-minus-one-aperiodic/driven_lhp_aperiodic_T131072_deep1048576.log`
reports "moving-edge violations 0" in every SUMMARY line (lines 51, 98, 147,
180, 188).

**Lemma B (two adjacent periodic columns propagate downward).**  Let
`s = LHP_y(c)` for any `y`, `c`.  Suppose `c` is `p`-periodic from `t0'` and
`l` is `q`-periodic from `t1`.  Put `P = pq >= 1` and `T = max(t0', t1)`.
Then for every `x <= 0` and every `t >= T`: `s(t+P, x) = s(t, x)`.

*Proof.*  Downward induction on `x`; let `S(x)` be "column `x` is
`P`-periodic from `T`", i.e. `s(t'+P,x) = s(t',x)` for all `t' >= T`.

`S(0)`: `s(t',0) = c_{t'}` and `P` is a multiple of `p`; iterating
`c_{t'+p} = c_{t'}` `q` times (all times involved are `>= t0'`) gives
`c_{t'+P} = c_{t'}` for `t' >= t0'`, in particular for `t' >= T`.
`S(-1)`: the same with `l`, `q`, `t1`.

Step.  Assume `S(x)` and `S(x+1)` for some `x <= -1`.  For `t >= T`, apply
(I1) at `(t+P, x)` and at `(t, x)` (both valid, `x <= -1`):

```text
s(t+P, x-1) = s(t+P+1, x) XOR (s(t+P, x) OR s(t+P, x+1))
            = s(t+1, x)   XOR (s(t, x)   OR s(t, x+1))      [S(x) at t+1 >= T and at t; S(x+1) at t]
            = s(t, x-1).
```

So `S(x-1)`.  By induction `S(x)` holds for every `x <= 0`.  QED.

**Proof of the theorem.**  Suppose, for contradiction, that `l` is
`q`-periodic from `t1`; `c` is `p`-periodic from `t0'` by hypothesis.  Lemma
B gives `P = pq` and `T` with every column `x <= 0` `P`-periodic from `T`.
Lemma A (hypothesis (N)) gives `(a, t0)` and (A).  Let `T* = max(T, t0)` and

```text
x* = e(T*) - P = a - (T* - t0) - P.
```

Then `x* <= e(T*) - 1 <= -1`, so `x*` is in the domain, and:

- `x* < e(T*)`, so `s(T*, x*) = 0` by (A) at time `T*`;
- `e(T* + P) = a - (T* + P - t0) = x*`, so `s(T* + P, x*) = 1` by (A) at
  time `T* + P`;
- `T* >= T` and `x* <= 0`, so `s(T* + P, x*) = s(T*, x*)` by Lemma B.

Hence `1 = 0`.  Contradiction; `l` is not eventually periodic.  QED.

*What the proof uses.*  Only I1 (left permutivity), I2 (the edge step), and
the domain bookkeeping of D2.  It does not use the value of `c` beyond
periodicity and (N), does not use the OR, and applies verbatim to Rule 90
(section 7).

## 4. Consequence (a)

Let `S*` be the lone-seed Rule 30 diagram: `S*(0,x) = [x = 0]` and
`S*(t+1,x) = f(S*(t,x-1), S*(t,x), S*(t,x+1))` for all `x in Z`.  Write
`c*_t = S*(t,0)`, `l*_t = S*(t,-1)`, `r*_t = S*(t,1)`, `Z = {t : c*_t = 0}`.

**(a1) The true left half-plane is the driven one.**  The restriction of
`S*` to `N x {x <= 0}` equals `LHP_0(c*)` (`y = 0` on `x <= -1`).
*Proof.*  The restriction satisfies (i) (`S*(0,x) = 0` for `x <= -1`), (ii)
(definition of `c*`), and (iii) (the rule at `(t+1,x)` with `x <= -1` reads
only positions `x-1, x, x+1 <= 0`, on which the restriction agrees with
`S*`).  By the uniqueness in D2 it is `LHP_0(c*)`.  (N) holds since
`c*_0 = 1`.  CHECK6 gates this identification cell-for-cell to `T = 3000`
(9,012,003 cells, 0 mismatches).

**(a2)**  Assume `c*` is `p`-periodic from `t0`.  By (a1) and the theorem
(`y = 0`, `c = c*`), `l*` is not eventually periodic.  This is the first
claim of (a).

**(a3) `Z` is infinite.**  If `Z` were finite, `c*_t = 1` for all
`t >= t2`; the rule at `(t+1, 0)` with I1 gives
`l*_t = c*_{t+1} XOR (c*_t OR r*_t) = c*_{t+1} XOR 1 = 0` for `t >= t2`, so
`l*` would be eventually periodic, contradicting (a2).

**(a4)**  D4 fixes the meaning of "`r*|Z` eventually periodic": there are
`q >= 1` and `i1` with `r*_{z_{i+q}} = r*_{z_i}` for all `i >= i1`.

**(a5) Z-enumeration.**  Let `k = |{j in [0,p) : c*_{t0+j} = 0}|`; `k >= 1`
by (a3) and periodicity.  Let `i0 = min{i : z_i >= t0}`.  Then
`z_{i+k} = z_i + p` for all `i >= i0`.
*Proof.*  First, `|Z cap [t0+m, t0+m+p)| = k` for every `m >= 0`, by
induction on `m`: `m = 0` is the definition of `k`; passing from `m` to
`m+1` removes `t0+m` and adds `t0+m+p`, and `t0+m in Z` iff `t0+m+p in Z`
(periodicity at `t0+m >= t0`), so the count is unchanged.  Now fix
`i >= i0`.  Since `z_i >= t0`, the window `[z_i, z_i+p)` contains exactly
`k` elements of `Z`; they are `z_i, ..., z_{i+k-1}` (consecutive in the
enumeration, starting at `z_i`).  Also `z_i + p in Z` (periodicity at
`z_i >= t0`), and it is the least element of `Z` that is `>= z_i + p`.  So
`z_{i+k} = z_i + p`.  QED.  CHECK7 (i): 312 drives, 0 failures.

**(a6) `r*|Z` eventually periodic forces `l*` eventually periodic.**
Suppose (a4) holds with `q, i1`.  Put `P = qp`.  For `i >= max(i0, i1)`:
iterating (a4) `k` times gives `r*_{z_{i+qk}} = r*_{z_i}`, and iterating
(a5) `q` times gives `z_{i+qk} = z_i + qp = z_i + P`.  So with
`T1 = z_{max(i0,i1)}`: for every `t in Z` with `t >= T1`, `t + P in Z` and
`r*_{t+P} = r*_t`.  Let `T2 = max(t0, T1)` and take `t >= T2`.  The rule at
`(t+1, 0)` and I1 give `l*_t = c*_{t+1} XOR (c*_t OR r*_t)`, and likewise
at `t + P`.  If `c*_t = 0`: `t in Z`, hence `t+P in Z` and
`l*_{t+P} = c*_{t+P+1} XOR r*_{t+P} = c*_{t+1} XOR r*_t = l*_t` (periodicity
of `c*` at `t+1 >= t0`).  If `c*_t = 1`: `c*_{t+P} = 1` and
`l*_{t+P} = c*_{t+P+1} XOR 1 = c*_{t+1} XOR 1 = l*_t`.  So `l*` is
`P`-periodic from `T2`, contradicting (a2).  Hence `r*|Z` is not eventually
periodic.  This is the second claim of (a).  CHECK7 (ii) exercises exactly
this algebra on synthetic `r` (312 drives, 0 failures).

**(a7) R1 is P1.**  R1 (`PATH.md` section 4, row 1) asserts: if `c*` is
eventually periodic then `r*|Z` is eventually periodic.  Claim:
`R1 <=> P1`.  If P1 holds, R1's hypothesis is false and R1 holds vacuously.
If R1 holds and `c*` were eventually periodic, then `r*|Z` would be
eventually periodic by R1 and not by (a6); so `c*` is not eventually
periodic, which is P1.  QED.  Under its own hypothesis R1's conclusion is
false, so R1's zero-set obligation cannot be discharged by any property of
`c*` or of the right half-plane taken alone; it can only be contradicted.

## 5. Consequence (b), exact form

**(b1)**  For every `y` and every `c in {0,1}^N`, `LHP_y(c)` exists (D2) and
satisfies (iii) at every cell `(t+1,x)`, `x <= -1`, with column `0` equal to
`c`.  So the set of configurations on `N x {x <= 0}` obeying Rule 30 at all
`x <= -1` has column `0` ranging over all of `{0,1}^N`: the left half-plane
alone constrains `c` not at all.

**(b2)**  Adjoin the rule at `x = 0` with `r` unconstrained.  By I3, the
pair `(c, l)`, `l = LHP_y(c)(.,-1)`, admits some `r in {0,1}^N` with
`c_{t+1} = l_t XOR (c_t OR r_t)` for all `t` iff the pin holds at every
one-time:

```text
c_t = 1  =>  l_t = 1 XOR c_{t+1}.                                   (PIN)
```

On `Z` the `r_t` is then unique, `r_t = c_{t+1} XOR l_t`; off `Z` it is
free.  So the only self-constraint of the left half-plane plus the `x = 0`
rule is (PIN), as the lemma says.

**(b4) Glue form of P1 (exact).**  Let `RHP_0(c)` be the mirror of D2 on
`x >= 1` with zero initial data (this is `r1zero_lib.driven_rhp`; a21's
Theorem P, `PATH.md` 9.4, says its column `1` at time `t` is a function of
`c_0..c_{t-1}`).  Then

> P1 holds iff for every eventually periodic `c` with `c_0 = 1` there is a
> `t` with `c_{t+1} != LHP_0(c)(t,-1) XOR (c_t OR RHP_0(c)(t,1))`.

*Proof.*  (=>) If some eventually periodic `c` with `c_0 = 1` satisfies the
glued rule at every `t`, the configuration obtained by gluing `LHP_0(c)` and
`RHP_0(c)` along column `0` obeys Rule 30 at every `x` (`x <= -1` by (iii),
`x >= 1` by the mirror of (iii), `x = 0` by hypothesis) and has initial row
`[x = 0]`; by uniqueness of forward evolution it is `S*`, so `c* = c` is
eventually periodic, contradicting P1.  (<=) If `c*` is eventually periodic,
(a1) and its mirror give `LHP_0(c*)(t,-1) = l*_t`, `RHP_0(c*)(t,1) = r*_t`,
and the rule at `(t+1,0)` in `S*` says the glued rule holds at every `t`,
contradicting the right side with `c = c*`.  QED.

The glued rule at a one-time is (PIN), a constraint on `LHP_0(c)` alone; at
a zero-time it is `r_t = c_{t+1} XOR l_t`, coupling the two half-planes.
This is the "shape of any P1 proof" the lemma's value field describes, now
as an exact equivalence.

**(b3) Dichotomy, and the status of the lemma's sentence.**  Let (PIN-Pi)
be: no eventually periodic `c` with `c_0 = 1` makes `LHP_0(c)` satisfy (PIN)
at every `t`.  (This is the lemma `pin-pi-no-periodic` named in the
statement; its text is not on disk, and this is the reading its screen
`../r1-r1zero-screen-pin-pi-no-periodic/lhp_lib.py` implements.)

- If (PIN-Pi) holds, P1 follows: by (a1), `LHP_0(c*)` satisfies (PIN) at
  every `t` (the rule at `x = 0` holds in `S*` with `r = r*`), so `c*` is
  not eventually periodic.  In this horn a proof of P1 need not use the
  right half-plane, and the lemma's sentence is false.
- If (PIN-Pi) fails, some eventually periodic `c` with `c_0 = 1` is
  pin-consistent forever; by (b1) and (b2) the statement "no configuration
  on `x <= 0` obeying (iii), the `x = 0` rule for some `r`, with column `0`
  eventually periodic and `c_0 = 1`" is false, so no proof of P1 can rest on
  those constraints alone and must use `r*` itself, i.e. the zero-time
  coupling of (b4).  In this horn the lemma's sentence is true.

The literal statement is now settled in the second horn by
`c=110^infinity`: `l_0=0`, `l_1=1`, and no later pin test has a true
antecedent. The old finite screen therefore did not cover this eventually
constant counterexample. A repaired target restricted to nonconstant
eventual tails remains open; existing constant-tail exclusions concern
the full Rule 30 diagram and are not pin-only results.

## 6. What the lemma implies in the BRIEF chain

Nothing.  It implies none of `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)`, P1.
It is a structural theorem about R1 (`PATH.md` row 1): (a7) shows R1 is not
a route to P1 but P1 itself, and (b4) gives the exact shape any P1 proof
must take.

## 7. Obstructions A to H

- **A** (`O(log t)` wall): not applicable.  Nothing is propagated from the
  trace; the argument consumes the global periodicity hypothesis (Lemma B
  propagates it to every column at once) and the moving edge (Lemma A).
- **B** (Rule 90 filter): passed in the only sense available to a
  limitation theorem.  The proof uses I1 and I2 only, both of which hold
  for Rule 90 (CHECK2, CHECK3), so the theorem holds for Rule 90's driven
  left half-plane too; the screen confirms it (`RULE90` lines 181 to 183 of
  the screening log: `c = 1 0^omega` gives `l_t = [t = 2^j - 1]` exactly
  through `2^14 - 1`, aperiodic).  This is why the lemma is explicitly not a
  proof route: it says what R1 is, not that P1 holds.
- **C** (single-column blindness): not applicable; the statement is about
  two named columns and uses no density-continuous functional.
- **D** (missing composition law): not applicable; every step is derived
  above.
- **E** (measure-zero orbit): not applicable; no measure.  (a1) ties the
  theorem to the single lone-seed orbit exactly.
- **F** (free boundary of a fixed-depth strip): evaded; Lemma B has
  infinite depth, and the contradiction is at depth `P` below the edge, not
  at a fixed strip boundary.
- **G** (variable-input measures): not applicable.
- **H** (finite data): not applicable to the theorem, which is a proof; it
  applies to the finite checks, which only gate definitions and identities,
  and to the pin-screen evidence cited in (b3), which is labelled as such.

## 8. Nearest killed mechanisms

`PATH.md` row 3 (run-of-ones wedge, proved dead): that argument propagates
zero defects `d_t(-j) = 0` a bounded distance from a bounded one-run.  Lemma
B instead assumes two full periodic columns and propagates the period to
infinite depth; the moving edge then supplies the contradiction.  `PATH.md`
row 7 mode (ii) (inclusion `col_{-1}` eventually periodic): the theorem
shows that inclusion is false for every eventually periodic drive, so mode
(ii) can only succeed vacuously.  Nothing in BRIEF section 6 is touched: no
energy, quotient, DFA, SAT table, or seam law appears.

## 9. Kill test and finite checks

The lemma is a proof; the kill test validates its two premises on the
kernel (a hit would contradict the proof).  Results:

- Screening (`../r1-r1zero-screen-driven-lhp-column-minus-one-aperiodic/driven_lhp_aperiodic_T131072_deep1048576.log`,
  line 189): `l` eventually periodic in 0 of 172 driven left half-planes,
  moving-edge violations 0, verdict HOLDS.  Pre-registered 44 drives
  reproduced at `T = 4096, Q = 256` (line 51, `0/44`) and pushed to
  `T = 131072, Q = 1024` (line 98, `0/44`).
- This directory, `driven_lhp_direct_checks.py` and its log
  `driven_lhp_direct_checks.log` (all lines `failures=0` or
  `mismatches=0`, final line `ALL CHECKS PASS=True`):

| check | what | size | result |
|---|---|---|---|
| CHECK1 | I3, rule at `x = 0` with `r` free | 8 tuples | 0 failures |
| CHECK2 | I1, inverse rule, Rules 30 and 90 | 8 neighbourhoods x 2 | 0 failures |
| CHECK3 | I2, edge step, Rules 30 and 90 | 2 x 2 | 0 failures |
| CHECK4 | D2 kernel vs explicit cell array | 60 pairs, 127,592 cells | 0 mismatches |
| CHECK5 | Lemma A on random drives, both cases, both rules | 40 drives, 24,040 rows | 0 violations |
| CHECK6 | (a1) true `x <= 0` half-plane vs `LHP_0(c*)` | `T = 3000`, 9,012,003 cells | 0 mismatches |
| CHECK7 | (a5) and (a6) algebra on synthetic `r` | 312 drives, `T = 3000` | 0 failures |
| CHECK8 | Correction 1: `c = 0^omega` gives `l = 0`; `c = 1 0^omega` keeps the edge, no period `q <= 64` | `T = 4096` | as stated |

Reproduce:

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
uv run python uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-direct/driven_lhp_direct_checks.py
```

## 10. Gaps

None for the theorem, for consequence (a), or for (b1), (b2), (b3), (b4).
The lemma's informal sentence in (b) ("any proof of P1 must use the
coupling") is not asserted; section 5 shows it is equivalent to the
negation of (PIN-Pi), which is open and is not a step of this proof.

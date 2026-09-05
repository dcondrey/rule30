# Verdict (LOGIC lens): driven-lhp-column-minus-one-aperiodic, direct proof

Date: 2026-09-03.  Proof audited:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-direct/PROOF.md`

**Verdict: SOUND.**  Every inference in the theorem (section 3), consequence
(a) (section 4) and the exact form of consequence (b) (section 5) follows from
the definitions D1 to D4, the three exhaustively checked identities I1 to I3,
and derivations written out in full.  No quantifier changes silently.  No
external theorem is load-bearing: Jen 1990 / Kopra 2023 are not used, and the
one external result named (a21's Theorem P) appears only as a descriptive
aside in (b4), whose proof rests on the mirror of D2 and on determinism of
forward evolution.  The proof's own two corrections to the lemma text
(hypothesis (N); the "(b) must use the coupling" sentence downgraded to a
dichotomy) are both correct and both necessary.  Six minor notes on commentary
follow in section 3; none touches a proved step.

Independent checks (mine): `verify_logic_checks.py`, log
`verify_logic_checks.log`, both in this directory; all six pass
(`ALL VERIFY-LOGIC CHECKS PASS=True`).  No counterexample was found and no
claim was contradicted, so `reproduced = false`.

## 1. Step-by-step audit

| step | claim | follows from | status |
|---|---|---|---|
| D2 existence/uniqueness | `LHP_y(c)` unique on `N x {x<=0}` | rule at `(t+1,x)`, `x<=-1`, reads only `x-1,x,x+1 <= 0`; induction on `t` | correct |
| D2 finite support | row `t+1` vanishes for `x < m-1` if row `t` vanishes for `x < m` | `f(0,0,0)=0` | correct |
| D4 | "`r|Z` eventually periodic" = enumeration-index sense | definitional; matches PATH.md section 2's derivation, whose time-index period is a multiple of `p` | correct; V6 (400 samples, 0 disagreements) confirms the two readings coincide |
| I1, I2, I3 | inverse rule; edge step; `x=0` rule with `r` free is solvable iff pin, `r` unique on `Z` | exhaustive over 8 tuples each | correct; V1 re-verified independently, 0 failures |
| Lemma A base, Case 1 | `s(0,a)=1`, `s(0,x)=0` for `x<a` | (i) and minimality of `a` (finite support gives the minimum) | correct |
| Lemma A base, Case 2 | rows `t<=t0` vanish on `x<=-1`; `s(t0,0)=1` | induction on `t` using `c_t=0` for `t<t0` and `f(0,0,0)=0`; `c_{t0}=1` | correct |
| Lemma A step | `s(t+1,e-1)=1`, `s(t+1,x)=0` for `x<e-1` | (iii) applies since `e-1<=-1`; `f(0,0,1)=1`, `f(0,0,0)=0` | correct; uses nothing about `c` after `t0` |
| Lemma B `S(0)`, `S(-1)` | columns 0 and -1 are `P=pq`-periodic from `T=max(t0',t1)` | iterate `c_{t+p}=c_t` `q` times, `l_{t+q}=l_t` `p` times | correct |
| Lemma B step | `S(x)` and `S(x+1)` give `S(x-1)` with the same onset `T` | I1 at `(t+P,x)` and `(t,x)`; `S(x)` at `t` and `t+1>=T`, `S(x+1)` at `t` | correct; strong induction on `-x` |
| Theorem | contradiction at `x* = e(T*)-P` | `x*<=-1` since `P>=1`, `a<=0`, `T*>=t0`; (A) at `T*` gives 0, (A) at `T*+P` gives 1, Lemma B gives equality | correct |
| (a1) | `S*` restricted to `x<=0` is `LHP_0(c*)` | restriction satisfies (i),(ii),(iii); D2 uniqueness; `(N)` from `c*_0=1` | correct; V3 re-gated independently to `T=400`, 161,603 cells, 0 mismatches |
| (a2) | `c*` ev. periodic implies `l*` not ev. periodic | theorem with `y=0`, `c=c*` | correct |
| (a3) | `Z` infinite (under the hypothesis) | `c*_t=1` for `t>=t2` forces `l*_t=0`, contradicting (a2) | correct |
| (a5) | `z_{i+k}=z_i+p` for `i>=i0` | window count `|Z cap [t0+m,t0+m+p)|=k` by induction on `m`; `z_i+p in Z` | correct; `k>=1` from (a3) |
| (a6) | `r*|Z` ev. periodic (D4) forces `l*` `qp`-periodic from `T2` | iterate (a4) `k` times and (a5) `q` times; case split on `c*_t` via the `x=0` rule; periodicity of `c*` at `t+1>=t0` | correct; the index bookkeeping (`t in Z`, `t>=z_{max(i0,i1)}` implies index `>= max(i0,i1)`) is right |
| (a7) | R1 iff P1 | both directions two lines; uses (a6) | correct (see note 3) |
| (b1) | LHP alone constrains `c` not at all | D2 existence for every `c` | correct |
| (b2) | with `x=0` rule and `r` free, the only constraint is (PIN) | I3 pointwise; `r_t` independent across `t` | correct |
| (b4) `=>` | a pin-and-glue consistent ev. periodic `c` with `c_0=1` yields `S*` | glued configuration obeys the rule everywhere, initial row `[x=0]`, determinism of forward evolution | correct |
| (b4) `<=` | `c*` ev. periodic satisfies the glued rule | (a1) and its mirror (same locality argument, no permutivity needed) | correct |
| (b3) horn 1 | (PIN-Pi) implies P1 | (a1) plus I3 | correct |
| (b3) horn 2 | not (PIN-Pi) implies the constraints of (b1),(b2) alone cannot prove P1 | satisfiability of the constraint set by a non-P1 object | correct as a consequence-relation statement |
| Section 6 | implies none of `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)`, P1 | | correct and honest |
| Section 7 B | proof uses only I1 and I2, both true for Rule 90 | Lemma A uses I2 and (iii); Lemma B's step works for any `f(a,b,d) = a XOR g(b,d)` | correct; the theorem is a limitation theorem, as stated |

Quantifiers checked: the theorem is universal over finite-support `y`, all
`p`, all `t0'`, all eventually periodic `c` with `(N)`; the proof by
contradiction assumes some `q`, `t1` and derives `1=0` with no dependence on
any finite horizon.  All finite checks (CHECK1 to CHECK8; the screening logs
at lines 51, 98, 147, 180, 181 to 183, 188, 189; `driven_halfplane_T4096.log`
line 228) are cited as gates or evidence only and I confirmed each cited line
exists with the quoted content.

## 2. Corrections in the proof, both verified

1. Hypothesis `(N)`: necessary (V5: `y=0`, `c=0^omega` gives `l=0^omega` to
   `T=512`) and sufficient (theorem).  Only one `1` in `c` is needed; the
   lemma's "infinitely many ones" was an error in the sketch, correctly
   repaired by Lemma A Case 2.
2. The lemma's "(b) any proof of P1 must use the coupling at the zero-times"
   is correctly not asserted; (b3) identifies it as exactly the negation of
   (PIN-Pi), which is open.

## 3. Minor notes (none load-bearing)

1. **Citation slip.**  (b4) cites "a21's Theorem P, `PATH.md` 9.4".  Theorem P
   is in `experiments/overnight-arms/frontier_attack/a21_r1_direct/r1_direct_attempt.md`
   section 3; `PATH.md` 9.4 names Theorems S and W only.  The (b4) proof does
   not use Theorem P, so nothing depends on it.
2. **Section 8, row 7 mode (ii).**  "The theorem shows that inclusion is false
   for every eventually periodic drive, so mode (ii) can only succeed
   vacuously" is loose.  The theorem constrains driven half-planes with
   finite-support `y`.  The ladder's `S_k(p)` witnesses are lassos, so their
   `col_{-1}` IS eventually periodic; by Lemma B their full leftward extension
   is periodic in every column, and by the theorem's contrapositive its row 0
   has infinite support (or `(N)` fails).  So the correct statement is: the
   inclusion can hold only if `S_k(p)` contains no element whose leftward
   extension has finite-support row 0; it says nothing about `S_k(p)` being
   empty.  This is commentary, not a step of the proof.
3. **(a7) is an instance of a general fact.**  For any hypothesis `H` and
   conclusion `C` with `H and C` refutable, `H => C` is equivalent to `not H`.
   `H and C` (c* periodic and `r*|Z` periodic) was already refutable through
   `PATH.md` section 2 (`r*|Z` periodic gives column -1 periodic) plus Jen
   1990 Prop. 3 / Kopra Thm 3.5.  What the proof adds is a self-contained
   refutation (Lemma A plus Lemma B, no external theorem) and the precise D4
   sense in which the equivalence holds.  The register note "R1 is equivalent
   to P1 rather than a route to it" is therefore a reframing of a
   proof-by-contradiction route, not a new logical fact about R1.  Logically
   correct; the value claim is for the obstruction lens.
4. **(a7) trailing sentence** ("cannot be discharged by any property of `c*`
   or of the right half-plane taken alone; it can only be contradicted") is
   commentary after the QED, not a proved claim, and should be read as such.
5. **(b3) horn 2** quotes the constraint set without "y = 0"; (PIN-Pi) is
   about `LHP_0(c)`, so `y = 0` is intended and the argument is unchanged.
6. **D4 is a choice.**  The proof argues it is R1's sense and that the
   time-index reading with period a multiple of `p` coincides with it; V6
   confirms coincidence on 400 random samples (208 enumeration-periodic, 0
   disagreements).  The arbitrary-`q` time-index reading is degenerate as the
   proof says.  Any reader of R1 who intends a different sense must re-derive
   (a6).

## 4. My checks (script `verify_logic_checks.py`, log `verify_logic_checks.log`)

| check | what | result (from the log) |
|---|---|---|
| V1 | I1, I2, I3 exhaustive, independent code | failures=0 |
| V2 | Lemma A on 24 random drives, both `(a,t0)` cases, dict cell-array kernel (no bitmask), `T=200` | rows checked=4824, violations=0 |
| V3 | (a1) gate, independent full-diagram cell-array lone seed vs `LHP_0(c*)`, `T=400` | cells=161603, mismatches=0 |
| V4 | theorem counterexample search: all 64 `y` supported in `[-6,-1]`, all 52 primitive words of period `<=5`, prefixes of length `<=2`, `(N)` enforced, `T=2048`, strict eventual period `q<=256`, onset `<=T/2` | drives=23293, `(N)`-failing skipped=3, eventually periodic `l` found=0 |
| V5 | `(N)` necessary: `y=0`, `c=0^omega` | `l` identically zero to `T=512`: True |
| V6 | D4 vs time-index (multiple of `p`) reading | 400 samples, disagreements=0 |

Reproduce:

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
uv run python uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-direct-verify-logic/verify_logic_checks.py
```

## 5. BRIEF section 7 compliance

Every step is a derivation written in full, an exhaustive check with script
and log, or a definition the proof states completely (D1 to D4 define the
two-state language; BRIEF section 2's four-state kernel is not needed).  No
"clearly" or "standard argument" appears.  The one phrase closest to an
appeal, "uniqueness of forward evolution" in (b4), is determinism of the CA
map, immediate by induction on `t` from D1.  Section 6 states the implication
into the chain is "nothing", which is correct; the deliverable is a limitation
theorem and register correction, as the lemma itself says.

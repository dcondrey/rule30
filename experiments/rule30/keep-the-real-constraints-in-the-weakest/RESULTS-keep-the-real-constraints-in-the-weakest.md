# RW/DLP: certified rewriting cannot cover the source language, and every RW-relevant state summary tried is exponential

Date: 2026-09-18. Target: `O_c ∩ I(HC_ω) = ∅` (SEP) via RW/DLP.

**STATUS: partial. RW/DLP and SEP are still conjectured. No ladder statement
changed.** This document adds one proved general rewrite lemma, three exact or
certified negative measurements that close the "finite separator retaining the
ordered suffix action" prescription, and an independent finite census. It
proves no all-length RW certificate and no reduction theorem.

Evidence labels follow the capsule: U uniform proof, C exact finite
certificate or census, K counterexample or measured obstruction.

## 0. Witness bank and controls

Query first (`scripts/research-pipeline/query_witness_bank.py`, threshold 12):
the statement "finite quotient separator ... uniform erasure of interrupted
defects" returned 0 hits. A direct scan of `data/research-metadata/witness_bank.jsonl`
(1289 records) for this route found only these relevant kills, all respected:

- `wit-1af7976d4b57bd86`, `Q=1212121`: refutes the shorter `22122 -> 22222` erasure.
- `wit-38625561d1873861` (`Q=2122122`) and `wit-33868369d16ba3b1`
  (`Q=222122122`): the four-guard seam descent lemma is refuted (not RW
  counterexamples).

Controls reproduced from the code (`reproduce_cocycle.py`, `reproduce_cocycle.log`;
direct `power(morph, ., t)` evaluation, not the repo verifiers, which rewrite
tracked JSON):

```
F^4(22122 Q)=11230303   F^4(22222 Q)=21230303   (Q=1212121)
F^5(222122 Q)=01333210  F^5(222222 Q)=20333210
```

Also reproduced by exact section-string equality: identity (1) for `k=0..40`;
equality at the sharp padding `f(k)` for `k=0..20` (the claimed formula (10));
the interrupted `1 2^k 1 ~ 2 2^k 1` absorption for `k=2..60`; `g(0)=5`, `g(1)=1`.
Minimality of `f(k)` (smaller padding fails): string inequality for all `k<=20`,
plus an explicit distinguishing input word for `k<=9`. For `10<=k<=20` that
check is string inequality only, not an exhibited distinguishing word.

## 1. Section formula and a general leading-flip lemma (U, from a local fact)

`block_section` gives `M_W = s_1 s_2 ... s_n` with `s_i` the state reached from
`start(W_i)` (`B` for 1, `C` for 2) after reading the whole word `J(W_{i+1..n})`.
Equal state strings give equal actions. Two consequences.

**(a) Full-source transfer.** If `|W|=|W'|` and `M_W=M_W'` then
`F^n(WQ)=F^n(W'Q)` for every `Q`, so a witness `(W,Q)` gives a witness `(W',Q)`
whenever the junction survives (`W'_last=2`, or `W_last=1`).

**(b) Leading-flip lemma.** If `B` and `C` reach the same state along `J(t)`, then
`M_{1t}=M_{2t}`. The section positions `i>=2` see identical tails, and
position 1 gives the same end state. The local fact `B.22 = C.22 = C` (already
in `rw_interrupted_defect_absorption.py`) makes this hold whenever `J(t)` begins
`(2,2)`. Over all binary `t` of length 2..14 this holds exactly for those
beginning `22` (8191 cases, all equal). So

```
122 r  ~  222 r     for every suffix r, every length.
```

This contains the catalogued `r30-rw-interrupted-defect-absorption` lemma
(`1 2^k 1`, `k>=2`) as the case `r = 2^(k-2) 1 ...`, and needs no second
defect. A catalog search (`rule30_research_db.jsonl`, terms: interrupted,
defect, leading symbol, M_W) found that record and no record of the
generalization or of the class counts below.

The step from `J(t)` to `t` is the bridge `J(t)_1 = morph(t)[0]`, which by the
locality of `inverse_terminal`, `peel` and `terminal` (argued in
`rw_interrupted_defect_absorption.py`) depends only on `t_0,t_1`. Checked
exhaustively: `J(t)[:2]=(2,2)` iff `t` begins `22`, for all binary `t` of
length 2..14, plus random long extensions (`reproduce_cocycle.log`). The
universal statement rests on the section formula, the local fact, and that
locality argument; the range checked is a control, not the proof.

**Front rewrite only.** `M_t=M_t'` does not imply `J(t)=J(t')` (the lemma
itself is the witness: `J(1s)_0=1`, `J(2s)_0=2`). For `W=u t`, the sections
inside `u` read `J(t)`, so substituting inside `W` is not licensed. The
docstring of `chaining_controls` in `rw_interrupted_defect_absorption.py`
says the lemma applies "wherever the pattern occurs, not just at the front";
its test checks only front substitution with an arbitrary suffix. That
sentence is an unsupported overclaim (file not edited, outside this
session's write scope).

## 2. Exact number of distinct suffix actions is exponential (C, exact)

`action_classes.py`. Distinct `M_W` over the actual period-two source language
`N = {no 11, no 22222}` and hard-core `H = {no 11}`. At every `n` the number of
distinct state strings equals the number of distinct fingerprints (actual
outputs on 200 fixed test inputs of length `2n+8`). Equal strings prove equal
actions; different fingerprints prove different actions; so both counts are
exact.

```
N  n : 4 5 6  7  8  9  10 11 12 13  14  15  16  17  18  19   20   21   22
sources 8 12 18 28 43 66 101 155 238 365 560 859 1318 2022 3102 4759 7301 11201 17184
classes 4 6 10 15 21 31 46 66 99 143 207 299 426 614 888 1276 1830 2623 3773
H  n=14..19 classes: 258 385 574 865 1300 1946   (sources 987 ... 10946)
```

Successive ratios are stable near 1.44 for `N` and 1.50 for `H`, against 1.53
and 1.62 for the language sizes. Any separator whose state retains the ordered
suffix action needs at least this many states at length `n`. This is the
prescription in the task, so that literal design cannot be a finite automaton.
Range: `n<=22` for `N`, `n<=19` for `H`; growth beyond that is extrapolation.

## 3. Proved exclusions, closed under full M-equality, cover almost nothing (K)

`closure_coverage.py`. Seeds are the sources excluded by proved theorems: `1^n`,
`2^n`, `12^(n-1)`, `212^(n-2)`, and `2^k 1 2^m` with `m>=f(k)+2`. A source is
covered if its `M`-class holds a seed with a compatible junction. This is the
finest sound rewrite closure.

```
n     : 9    10   11   12   13
all   : 12/512 12/1024 20/2048 22/4096 26/8192
H     : 7/89  7/144  11/233  11/377  11/610
N     : 0/66  0/101  0/155   0/238   0/365
```

Zero coverage of `N` is certain (different fingerprints prove different
actions). Positive coverage counts (`n>=9`) are upper bounds: exact bisimulation
confirmed every merge for `n<=8` only, and hit its state cap at `n=9`.
The proved erasure families reach nothing in the actual source language, and
the class count in section 2 says why: any rewriting to a bounded family must
bring exponentially many classes to zero.

## 4. Forced continuation and an independent census (C)

`M_W` is invertible, so for each source `W`, target `c`, residue `r` the RW
continuation is forced: `J(Q_W) = M_W^{-1}(J(T(c^m)))`, `m=n+r+2`
(`forced_continuation.py`; the inversion is checked against direct `F^n(WQ)` on
60 random pairs). Distinct forced words over `N` are 0.89 to 0.99 of the class
count (`n=8..20`), so the coarser RW-relevant invariant compresses almost
nothing (1680 of 1830 classes at `n=20`). It does not depend on `r`.

`alive_depth.py`, run for every `r in {0,1,2}` (`m=n+r+2`; the maximum alive
depth is identical across `r`): `alive(W)` is the longest prefix of `J(Q_W)` that equals the
`J`-image of some hard-core binary prefix (junction included). A witness needs
`alive >= m`. The prefix set is always the hard-core one, so for the `N` rows
the continuation is not also tested against `22222` (permissive, so the
negative result stands). Controls: 40 positive (a target built from a real `(W0,Q0)`
keeps `W0` alive to depth `m`), 40 negative (`11` planted in `Q0`), 396
prefix-locality checks (`alive_controls.log`).

```
hard-core and N sources, n=6..21, c in {2,3}: maximum alive depth over all sources
c=2, H: 2 4 3 2 4 4 5 5 7 7 10 10 9 7 10 12        (n=6..21)
c=3, H: 2 4 3 8 6 4 5 5 5 6 6  5  9 8 8 8
no source reaches m for any r; smallest shortfall m-alive is 3 (n=9, r=0), then >=6 for n>=10.
N rows, n=6..21: c=2: 2 4 3 2 4 4 5 5 7 7 10 10 8 7 7 7 ; c=3: 2 4 3 8 6 4 5 5 5 5 6 5 8 6 8 8
```

No RW witness with hard-core `W` exists for `n<=21`, `c` in {2,3}, `r` in
{0,1,2} (computed). The capsule's "hard-core corpus through length 23"
indexes whole words `f` (`n` about 10); this run reaches `|f|` up to 46 but
only for hard-core `W`. RW allows arbitrary binary `W`, and the capsule's
"all binary sources through length 20" is a different language, so this
extends one census and is not a new all-binary claim. The maximum alive depth
grows about `0.5 n`, which is the known `M_hc ~ w/2+5` behaviour, not a proved bound.

## 5. Kill tests for this approach

- Proposed state is not a congruence: fires for the prescribed state (full
  ordered suffix action, section 2) and for the forced-word summary (section 4).
  Evaded only by a summary proved closed; none found.
- Finite computation cannot certify all lengths: fires for sections 2 to 4
  (horizon `n=21..22`, no proved horizon).
- Counting injection: not used.
- Monotone potential (number of 1s): rank descent exists for 5846 of 8192
  sources at `n=13` (`words_in_class_with_fewer_ones`), yet the normal forms are
  still exponentially many and no `N` source at `n>=9` is covered by a seed.
- Restates the target: deciding a class is deciding `Q_W`, which is RW itself.

## 5b. Follow-up: the state-string route and the survival profile (C, negative)

Cascade view: `y_W = s_n^{-1}...s_1^{-1}(z)` with `z=J(T(c^m))` equal to `1 3^inf`
(c=2) or `0 3^inf` (c=3); each layer pushes a marker three cells right, so the
active region is about `3n` cells while RW reads only the first `n+2`. For fixed
depth `d` the cascade lives in a finite group, but the depth needed is `n+2`.

- The state string `s(W)` is not a self-contained generator. Whether `s(qW')`
  is determined by a leftmost window of `s(W')` fails for every window `k<=10`
  (`state_string_language.py`, `W'` up to length 14, thousands of conflicts),
  and the full string `s(W')` does not even determine the two prepend states
  (conflicts at every `n>=3`). So no sliding-block or Markov description of
  the state strings exists on this data, another instance of the
  no-closed-quotient test.
- Survival profile (`survival_profile.py`, `survival_profile.log`): the fraction
  of hard-core sources whose forced word stays admissible to depth `d+1`
  given depth `d` is about 0.41 per cell in the bulk (`n=21`: 0.412 0.408 0.438
  0.393 0.456), which matches the admissible density `phi/4 = 0.405`, so the
  bulk behaves as an independent-coin sieve, then the tail is structured
  (`n=21, c=2`: 52 sources sit at depth 10, 11 and 12 together, then all die).
  A rigorous version is the uniform counting bound already recorded as dead
  (0.70 of the 1.0 bits required).
- The 52 deepest sources at `n=21, c=2` share the suffix `222221212122`. Fixing
  it and sweeping all 89 hard-core prefixes gives alive depth 12 for 52, and 0
  to 2 for the rest (`tail_locality.log`), so the prefix matters through a
  finite-looking compatibility, but the deepest sets at `n=13,16,18,21` have
  different suffixes (`221222121212`, `212212122122122`,
  `22121221222221`, `222221212122`), so no stable extremal family emerged.

- Fixed-depth survival is not regular in `W` (`hankel_depth.py`,
  `hankel_depth_c2.log`, `c=2`). The Hankel matrix `[alive(u t) >= d]` over
  hard-core `u,t` of length up to 9 has rank growing about 1.5 per symbol even
  at `d=1` (ranks 3, 6, 11, 17, 26, 39, 60, 92 for `L=2..9`), and at `d=2..6`
  it reaches the same rank at `L=9` or trails it by the depth delay. So even
  the first forced cell is not decided by any finite automaton reading `W`.
  Reason: `y_0` is a product of `S_4` permutations chosen by the state string,
  which is finite-state in `s`, but `s(W)` carries the whole of `J(W)`, a
  bijective image of `W`. This closes "one automaton per fixed depth in source
  coordinates" as a route to an inductive family.

## 6. Still open

A closed all-length RW/DLP or SEP certificate; formal reductions RW/DLP to SEP
to nonconstant period two; three or more interrupted defects beyond the
`122 -> 222` lemma; the general hard-core source language. The one direction
these numbers leave is a summary strictly coarser than `Q_W`: it would have to
track the first violation of the hard-core/binary/`12a` grammar rather than
the whole forced word.

## Files

`action_classes.py` (`action_classes_{N,H}.log`), `closure_coverage.py`
(`closure_coverage.log`, `closure_coverage_narrow.log`), `forced_continuation.py`
(`forced_continuation_N.log`), `alive_depth.py` (`alive_{H,N}.log`,
`alive_controls.log`), `reproduce_cocycle.py` (`reproduce_cocycle.log`),
`state_string_language.py`, `survival_profile.py` (`survival_profile.log`),
`tail_locality.py` (`tail_locality.log`), `hankel_depth.py` (`hankel_depth_c2.log`). Logs
are hidden by the global ignore; `git add -f` to commit them. Nothing committed.

## 7. Sharp depth of the guarded erasures, and the `c=3` Hankel ranks

Status: **two exact results, neither moves a ladder statement.** `RW`, `DLP`,
`SEP` and `PT2` are unchanged and still conjectured.

### 7a. The guarded erasures are valid one step earlier at `k=1` and `k=3` (U)

`RESULTS-rw-defect-cocycle.md` displays each guarded erasure at the length of
its own prefix: `(1)` at `F^{4k+3}`, `(3)` at `F^7`, `(11)` at `F^8`. The depth
at which the two images actually coincide is a second parameter, and the
padding theorem `(10)` does not fix it. From `J(wv)=J(w)M_w(J(v))` and
`J(F(u))=J(u)[1:]`,

    F^d(left v) = F^d(right v) for every v   <=>   M_left ~ M_right  and  J(left)[d:] == J(right)[d:].

Both halves are exact finite checks, so the depth is all-length in `v`.

| `k` | prefix | displayed | sharp | `J(left)` | bisimulation pairs |
|---|---|---|---|---|---|
| 0 | `122` | 3 | 3 | `130` | 141 |
| 1 | `2122` | 4 | **3** | `2002` | 517 |
| 2 | `2212222` | 7 | 7 | `2210130` | 18,619 |
| 3 | `22212222` | 8 | **7** | `22202002` | 57,741 |
| 4 | `22221222222` | 11 | 11 | `22221320130` | 1,555,372 |

Controls, and they are the point: at `sharp - 1` the **empty** suffix already
separates the two words, so each depth above is sharp and not merely
sufficient. At `k=1` and `k=3` the separating images are `00` against `22`, at
`k=0,2,4` they are `0` against `2`.

The erasure identity itself is the published theorem and is not reproved here;
only its depth is computed. The `k=1` and `k=3` rules are therefore usable one
`F`-step before their displayed cutoff, which matters only where the guard must
survive to a stated depth. `k=0,2,4` are already sharp as displayed.

Scope: `k<=4`. For `k>=5` the exact bisimulation passes 2,000,000 pairs without
closing under a cap set to bound memory, so no depth is asserted there.
Granting the published all-`k` theorem the `J` comparison alone gives
`sharp = displayed` at `k=5,6,7`, but that reading inherits the theorem rather
than certifying it, and it is not a claim of this section.

### 7b. The fixed-depth automaton kill also holds at `c=3` (C, negative)

§5b measured the Hankel rank of `H_d[u,t] = [alive(ut) >= d]` over hard-core
`u,t` at `c=2` only, and `SEP` quantifies over `c in {2,3}`. At `c=3`, `d=1`,
`L=2..9`:

    4, 7, 11, 17, 26, 39, 60, 92

against `3, 6, 11, 17, 26, 39, 60, 92` at `c=2`. The two agree exactly from
`L=4` on, and the `c=3` rank grows at the same ~1.5 per symbol with no
saturation in range. `d=2..6` carry the same shape (`hankel_depth_c3.log`).

So the recorded kill of "a small automaton on the source decides survival of
the forced RW continuation to a fixed depth" is not a `c=2` artifact. Its scope
widens from one constant to both. The extrapolation in its original scope line
is unchanged and still applies: ranks are measured to `L=9`, and that the rank
never saturates remains extrapolation.

### 7c. §4's census is subsumed by the RW SAT census (defect in this document)

§4 states that no RW witness with hard-core `W` exists for `n<=21` and calls it
an extension of one census. It compares against the capsule only. Complete SAT
over **arbitrary binary** `W` already decides RW to `n=30` for `r=0,1,2` and both
`c`, UNSAT at every solved cell (`p1-period2-invariant/BACKLOG.md:229`, re-read
here). §4's census is a weaker result, in a smaller language, at a lower horizon.

Corrected 2026-09-20. The first version of this section also leaned on the
population result `|H_r(n)| = 0`, calling its filter "strictly stronger" and
giving it to `n=24`. Both need qualifying. The overnight logs do reach `n=24`
(`overnight_c{2,3}_{odd,even}.log`, e.g. `RESULT n=24 c=3 H0=0 H1=0 H2=0`), but
`RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md` records the result to `n=16`, and
`BACKLOG.md:233` warns it is a necessary-only statement, weaker than the SAT
census and over a different range. The subsumption does not need it and no
longer rests on it.

### 7d. Files

`erasure_depth.py` (`erasure_depth.log`), `hankel_depth.py 3 9 6`
(`hankel_depth_c3.log`). Logs are hidden by the global ignore; `git add -f` to
commit them.

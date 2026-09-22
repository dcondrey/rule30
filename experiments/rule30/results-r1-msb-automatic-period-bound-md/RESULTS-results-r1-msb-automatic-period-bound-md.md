# MSB period bound: kill tests, exhaustive N<=5 regression, and exact optimality of the sharp constants

Date: 2026-09-19. Source under test: `docs/rule30/RESULTS-r1/RESULTS-r1-msb-automatic-period-bound.md`
(MSB automatic sequence period theorem `6cdca41320d7d11d`, sharper corollary `9cce6b3201f30d22`).
Bears on: R1 zero-set obligation, as an observation tool only. R1 and P1 are unchanged.

Labels: **proved** = machine-checked or exhaustive certificate plus a control that fails when the claim
is false; **computed** = exhaustive or sampled over a stated range, no extrapolation; **conjectured**.

## 1. What the argument uses

1. Deterministic binary-output MSB automaton, N states, canonical (no leading zero) inputs, root
   self-loop on 0. The loop is needed only to define `u(0)` and to pad the addition product.
2. Minimisation, for the proof only (`n<=N`).
3. Eventual periodicity gives a purely periodic extension `v` with least period `p=2^a*b`.
4. Residual functions `f_r(w)=v(2^|w| r+val w)`; `Q_tail={f_r}` is transition-closed and every large
   prefix lands in it (Sec. 2 of the doc).
5. `f_r=f_s` implies `b | r-s` (minimality of `p`), so `M=|Q_tail|>=b`.
6. `E_k` (equal successor states at depth k) has `b` classes at level `a`, and each of the `a` steps
   is strict because `p/2` is not a period (Sec. 3), so `M>=a+b`.
7. A canonical prefix cannot revisit a state outside `Q_tail`, so it enters `Q_tail` within `n-M`
   digits; `x = r mod b`; `a` more digits align residues mod `p` (Sec. 4).
8. Digit arithmetic: length `>= n-M+a`, and `n-M+a <= n-b <= N-1`.
9. The decision procedure: exact MSB addition product with cap `N+1` on the digit count of `n`.

## 2. Numbers reproduced from code before use

`uv run python experiments/rule30/r1-isolated-column/msb_automatic_period_bound.py` and
`msb_period_sharp_audit.py` both exit 0 and match their saved JSON: 2 / 16 / 720 labelled machines with
2 / 12 / 292 eventually periodic; sharp product states 8 / 78 / 3780. My `census.py` re-derives the
same counts independently (canonical machines times `(N-1)!`: 360*2=720, 146*2=292, 214*2=428) and the
sharp constants for N=4..8 from `extremal_family.py` (`extremal-family.json`): (4,24), (8,240), (16,480),
(32,6720), (64,13440), identical to the doc table. Rule 90 witness N=3, H=8, P=48, n=31: values 1 and 0
at 31 and 79 (`kill-tests.json`, K1).

## 3. Kill tests

Taken from the mechanisms that killed neighbouring R1 zero-set approaches. `kill_tests.py`, `kill-tests.json`.

| Test | Origin | Result |
|---|---|---|
| K1 Rule 90 filter | R1 inventory (`d0f87a134c62e6bb`, `12196b62c8d5d083`) | The rule-generic bound classifies the Rule 90 neighbour aperiodic while an independently evolved centre is identically 0 (T=1024, lone seed and seed {-1,+1}). It certifies the true Rule 90 fact and asserts nothing about R1: passes. |
| K2 Thue-Morse handle | `r30-aut-residual-handle-false` | Thue-Morse (2 states), Rudin-Shapiro (4), and [n a power of two] (3) are aperiodic under both the MSB checker and the reversal+LSD checker, each with a scalar witness. The proof never uses "no constant residual"; it uses residuals of a periodic sequence only: passes. |
| K3 power-of-two clock/mask | `r30-dfm-observable-no-clock-factor`, `r30-dco-time-axis-guarded-observation` | `u'(n)=u(2^a n+r)` keeps N states. All canonical machines N=2,3,4 with (a,r) in {(1,0),(1,1),(2,0..3)}: 96 / 2160 / 78,336 subsequences, 0 disagreements between the exact classifier and the N-state sharp equality: passes. |
| Controls | | Halving H_sharp: 8 (N=3) and 72 (N=4) machines misclassified. Halving P_sharp: 8 and 48. The harness does fail on false constants (`censusH-N3-4.json`, `censusP-N3-4.json`). |

Observation on the record, not a change to it: for the seed {-1,+1} the right neighbour is 1 exactly when
`t+2` is a power of 2 (t=0,2,6,14,...), not when `t=2^j-1` as retracted record `d0f87a134c62e6bb` states.
That statement is retracted; the qualitative point (centre periodic, neighbour aperiodic) is confirmed.

## 4. The gap and the case attempted

The doc proves an upper bound and says "neither pair of bounds is claimed optimal", and its regression
stops at N=3, while the SAT work it serves is at N=5. Three questions follow, in order of size:
the exhaustive N=4 and N=5 regressions; whether `a+b<=N` and the sharp constants are attained; whether
an odd-modulus mask keeps the N-state bound.

## 5. Results

### 5.1 Exhaustive N<=5 regression (computed, exhaustive over the stated class)

Every reachable machine with a root loop, canonical BFS labelling, all 2^N outputs. The eventual-periodicity
classifier is the reversal + LSD checker (`automatic_period_bound.mismatch`), independent of the MSB
theorem under test; the test is the exact sharp equality `u(n+P_sharp)=u(n), n>=H_sharp` (LSD-side product
`differs`). For each eventually periodic machine the proof's intermediate claims are also recomputed from
the minimal machine: `a+b<=M<=n_min<=N`, `E_a` has exactly `b` classes, `E_k` strictly decreasing for
`k<=a`, onset `<= 2^max(0,n_min-M+a-1)`, tail states equal the residual states, `f_r=f_s` implies `b|r-s`.

| N | canonical machines | labelled (x(N-1)!) | eventually periodic (canonical) | aperiodic (canonical) | violations |
|---|---:|---:|---:|---:|---:|
| 1 | 2 | 2 | 2 | 0 | 0 |
| 2 | 16 | 16 | 12 | 4 | 0 |
| 3 | 360 | 720 | 146 | 214 | 0 |
| 4 | 13,056 | 78,336 | 2,564 | 10,492 | 0 |
| 5 | 647,200 | 15,532,800 | 61,004 | 586,196 | 0 |

Exact maximum onset: 0, 1, 2, 4, 8 for N=1..5 (`2^(N-2)` from N=2). Attained least tail periods, N=5:
1,2,3,4,5,6,8,12,16; attained (a,b) at N=5: (0,1),(1,1),(2,1),(3,1),(4,1),(0,3),(1,3),(2,3),(0,5),
exactly the nine pairs with `b` odd and `a+b<=5`. Files: `census-N1-2-3-4.json`, `census-N5.json`.
Beyond N=5 (seeded random samples, `radix_census.py 2 N sample`, same classifier, sharp equality and
period-divides-`P_sharp` and `a+b<=M<=n` checks): N=6, 100,000 machines, 4,647 eventually periodic, 0
violations, max onset 14 (bound 16); N=7, 30,000 machines, 767 eventually periodic, 0 violations, max
onset 29 (bound 32). Random machines rarely reach the extremal onset or the large periods, so the samples
are weak evidence there; the families in 5.2 cover the extremes.
Scope: the classification rests on the established LSD theorem; this is an exhaustive regression
for N<=5, not a proof for larger N.

### 5.2 The sharp constants are optimal (proved)

Definitions. `(H',P')` is *universal for N* if every eventually periodic N-state MSB machine
(root loop) satisfies `u(n+P')=u(n)` for all `n>=H'`. Optimality is componentwise: Claim A shows no
`H'<H_sharp` is universal with any `P'`; Claim B shows no `P'` that is not a multiple of `P_sharp` is
universal with any `H'`. That `(H_sharp,P_sharp)` is universal is the doc's corollary; the joint
statement "the pair is the unique minimal pair" follows from A and B together, since each component
is minimal independently of the other.

**Claim A (onset).** For every `N>=2`, `H_sharp=2^(N-2)` cannot be lowered, for any shift.
Machine: count digits up to `N-2`, then a sink; output 1 on root and the counting states, 0 on the sink.
It has N states and computes `u(n)=[n<2^(N-2)]`. For any period `P'>=1`,
`u(2^(N-2)-1)=1` and `u(2^(N-2)-1+P')=0`, so equality from any `H'<2^(N-2)` fails while `u` is
eventually periodic. Machine-checked for N=2..15 (`extremal_family.py`): formula equals machine on
`n<2^16`, equality from `H_sharp` holds exactly (product), and it fails at `H_sharp-1`.
N=1 is excluded: constants are attained only from N=2 (census max onset at N=1 is 0).

**Claim B (period).** `P_sharp=2^(N-1)*lcm(odd<=N)` is the least positive universal period. Machines:
`[2^(N-1) | n]` (N states, trailing-zero count) has least tail period `2^(N-1)`; for each odd prime
power `q^k<=N` the residue machine `[q^k | n]` (`q^k` states) has least tail period `q^k`. A universal
`P'` must be a multiple of every attained least tail period (if `u(n+P')=u(n)` for `n>=H'` and `p` is
the least tail period then `p | P'`), hence of their lcm, which is `P_sharp`. Machine-checked N=2..15:
each machine passes at `P_sharp` and fails at `P_sharp/q` for every prime `q | P_sharp` (product).
The conservative `P=2^N*lcm(1..N)` is therefore a proper multiple of the optimum for every `N>=2`.

**Claim C (the restriction `a+b<=N` is exact).** The pair `(a,b)`, `b` odd, is attained by an N-state
machine iff `a+b<=N`. Necessity is the doc's theorem. Sufficiency: `u=[2^a b | n]` has exactly `a+b`
states. Proof: the state after a word `x` is `f_{x mod p}` for `p=2^a b`. If `b` does not divide `r`,
then `f_r(w)=0` for all `|w|<a` (`|w|=k<a` forces `2^k | w`, so `w=0` and then `b | r`), and for
`|w|>=a` it depends on `r mod b` only, giving `b-1` distinct states. If `r=bj`, then for `|w|=k<a`
`f_r(w)=[w=0 and 2^(a-k) | j]`, which determines `min(v_2(j),a)`: `a+1` distinct states, all distinct
from the others because for `|w|>=a` they equal `[p | w]`. Total `(b-1)+(a+1)=a+b`; the root `f_0` loops
on 0. Machine-check: minimal DFAO size equals `a+b` for all 72 pairs `b in {1,3,...,15}`, `a in 0..8`
(`pair_family.py`, `pair-family.json`). Consistent with 5.1: every admissible pair occurs for N<=5.

**Second, independent confirmation of A and B (computed).** The exhaustive census reaches the same
constants by a different route: it never uses the families. Exact maximum onset over all eventually
periodic machines is 1, 2, 4, 8 for N=2..5, equal to `H_sharp`. The lcm of the attained least tail periods
is 2, 12, 24, 240 for N=2..5 (attained sets {1,2}, {1,2,3,4}, {1,2,3,4,6,8}, {1,2,3,4,5,6,8,12,16}),
equal to `P_sharp` at every size (recomputed from `census-N1-2-3-4.json` and `census-N5.json`).

Controls. A and B fail at `H_sharp-1` and `P_sharp/q` by construction of the checks above. C: over the same
72 pairs the predicate "minimal size equals `a+b+1`" and "equals `a+b-1`" accept 0 pairs, while
"equals `a+b`" accepts all 72. Census: the halved-constant runs fail in 8 (N=3) and 72 (N=4) cases for H,
8 and 48 for P. Every one of those is a "classification mismatch" (all 16 N=3 examples and the 10 stored for
each N=4 run say so; the other six checks do not read the mutated constants and had 0 violations in the
unmutated run, so no other reason can account for the rest).

Consequence, available and not exercised: optimality licenses the sharp pair wherever the conservative
pair is used, for example in the five-state SAT encodings (H 32 to 8 and P 1920 to 240 at N=5), which
shrinks the witness circuit. `msb_automatic_period_bound.py` retains the conservative constants to
preserve issued certificates and is untouched.

### 5.3 Odd-modulus masks (computed, conjecture beyond the range)

The doc warns that a mask needs its own state count. For `u'(n)=u(qn+r)` the composed LSD machine
reaches 48 states at (N=4, q=3) and 80 at (N=4, q=5), well above N. Yet every eventually periodic subsequence satisfies
the ORIGINAL N-state sharp equality, with no exception.
Range: q=3, N=2,3,4 exhaustive over all r (48 / 1080 / 39,168 subsequences, 0 violations, 0 aperiodic
subsequences passing); q=5 and q=7, N=2,3 exhaustive (0 violations); q=5, N=4 a seeded random sample of
20,000 of 65,280 (0 violations); q=7, N=4 a seeded sample of 20,000 of 91,392 (0 violations); q=3, N=5 a
seeded sample of 200,000 of 1,941,600 (0 violations, 20,355 eventually periodic, composed machines up to 96
states; an earlier 20,000 sample is a subset of the same seeded order); q=9 and q=15, N=2,3 exhaustive
(144 / 3,240 / 240 / 5,400 subsequences, 0 violations, composed machines up to 120 states). In every run no aperiodic subsequence passed the equality. Files: `odd-mask-*.log`,
`odd-mask-probe-*.json`. Conjectured: for odd `q` an eventually periodic `u(qn+r)` of an N-state
sequence obeys the same sharp constants. No proof, and nothing is claimed past these ranges; the three
seeded samples cover about 31%, 22% and 10% of their populations.

SAT search past the enumerable range (`sat_mask_search.py`, `sat_jobs.txt`, `sat-mask-results.log`, pysat
Cadical). Unknown N-state MSB machine with a root loop; constraint `u(3n+r)=v[n mod p]` for `n>=2^N`
inside the window `3n+r<2^L`, where `v` is free with least period `p` (every maximal proper divisor of
`p` is not a period). Periods with `a+b` equal to `N+1` or `N+2` (violations of `a+b<=N`), `p<=64`:
N=3 {5,6,8,12,16}, N=4 {5,10,12,16,24,32}, N=5 {7,10,20,24,32,48,64}, N=6 {7,14,20,40,48,64}, all `r` in
{0,1,2}, `L`=11,12,13,14. Result: UNSAT in all 72 period runs (24 periods x 3 values of `r`; with the 12 onset runs, 84 jobs, all completed). UNSAT is a rigorous exclusion: no N-state
machine agrees with any least-period-`p` sequence on that window, so no eventually periodic mask with onset
at most `2^N` violates the period bound for these `p` (it excludes more than needed, including machines
that are periodic only inside the window). Onset-violation runs (`u'` periodic with period `P_sharp` from
`2^N` but with a forced mismatch at some `n` in `[H_sharp, 2^N)`): UNSAT at N=3,4,5 for all `r`. At N=6 all
three runs were SAT, but each returned machine composes to an exactly aperiodic mask (composed LSD machine,
exact classifier, all six states reachable), so these are artifacts of a window of only about 11 periods of
length 480, not counterexamples; the N=6 onset case is inconclusive.

How far past the window each artifact sits is now measured, and it kills the registered next lever. The
measurement was pre-registered in the `onset_witness_break.py` docstring with three predictions, and that
docstring, not this paragraph, is the registered text (`onset-witness-break.json`). P1, registered as
`n_break >= top` for all three, FIRED on `r`=1 at `n_break`=5,345 against `top`=5,461; the threshold was
wrong, not the encoding, because periodicity binds only where both `n` and `n+480` carry a constraint, so
the last fully constrained `n` is `top-P-1`: 4,981 at `r`=0 and 4,980 at `r`=1,2. P1 stands as registered in
the docstring, `break_inside_constrained_pairs` is the field that discriminates, and under it all three
pass. The smallest `n>=2^N` at which each witness's own mask first breaks 480-periodicity is 168,457, 5,345
and 19,908. Excluding a witness needs `3(n+480)+r` back inside the window, so `L` would have to reach 19, 15
and 16. P2, registered as a KILL for the "rerun at `L`=15" lever on any `L_needed>15`, FIRED on `r`=0 and
`r`=2: `L`=15 excludes only the `r`=1 witness, and `L`=19 carries 32x the state variables of an `L`=14 run
that already cost 12.3 hours in period mode at this `N` (`p`=64, `r`=0). The lever is retired, not deferred,
and N=6 stays inconclusive with no replacement lever registered. P3 split 2-1 against its treadmill
reading: against `2P`=960 the gaps are 162,995, -116 and 14,447, so the three witnesses do not point the
same way. Measured past the last constrained index, `r`=1 breaks after 365 terms, under one period, which is
a solver putting the break wherever it is cheapest; `r`=2 breaks 31 periods past and `r`=0 340 periods past,
which is not. So a break can sit either just outside the constrained range or far beyond it, nothing here
bounds which, and a fresh search at `L`=15 has more freedom than this one, not less. Both `n` values at each
break were read twice, by the MSB reader and by the composed LSD machine, which also agree on every
`n<3000`.

The distribution behind those three witnesses is now measured over 152 machines rather than three, and it
retires windowed onset exclusion rather than one lever of it (`onset_cegis_probe.py`,
`onset-cegis-probe.json`, `onset-cegis-probe.jsonl`). The probe walks the family by CEGIS: solve, read the
machine, classify its mask with the same exact composed-LSD classifier, measure `n_break`, block that
machine, re-solve. What is blocked is the certified implication cube -- the selected transition literals of
the states reachable from 0 plus their signed outputs -- so one clause kills every completion of the states
nobody can reach; and all `(N-1)!`=120 relabellings fixing state 0 go with it, since a cube naming specific
`t[s][d][s']` variables is not invariant under them and without the orbit the loop enumerates names rather
than machines. Seven predictions were registered in that docstring and committed before the first run. Under
a 2,700 s cap per residue the loop returned 47 machines at `r`=0, 44 at `r`=1 and 61 at `r`=2, 18,240
blocking clauses over 8,143 solver seconds and 21.7M conflicts. Every one of the 152 is a distinct core
signature, has all six states reachable, and has an exactly aperiodic mask, so Q1 held and no in-window
witness exists in this sample; Q2 held, every break sitting above its own last fully constrained index,
including the `r`=1 minimum at 5,345, which is below `top`=5,461 but above 4,980 exactly as the amended P1
says it may be. All three runs stopped at the wall-clock cap, never at UNSAT, so Q3 held and nothing here
excludes anything -- the same standing as `r30-loc-class-search-unknown`, which reached UNKNOWN at three caps
on this architecture.

The three committed break points are reproduced as members of the family (168,457 at `r`=0, 5,345 at `r`=1,
19,908 at `r`=2), and the family around them is far wider than they suggested. `n_break` runs 11,899 to
220,886 at `r`=0 (median 24,278), 5,345 to 255,838 at `r`=1 (median 54,861) and 6,801 to 232,536 at `r`=2
(median 40,297). Q4 fired as a KILL at all three: the median `L_needed` is 17, 18 and 17 weighted by machine
and 19, 18 and 18 over the distinct break values, against a registered KILL threshold of 17. The counting is
what settles the lever. `L`=15 excludes 13 of the 152, and none at all of the 47 at `r`=0, where the cheapest
break needs `3(11,899+480)`=37,137 past `2^15`=32,768; `L`=16 reaches 58, `L`=19 reaches 138, and only `L`=20
reaches all 152, at 64x the state variables of the `L`=14 runs this table is built from. Q5 fired at all
three against its own treadmill reading: 0 of 47, 8 of 44 and 0 of 61 break within `2P`=960 of the window
top, and the smallest gap at `r`=0 is 6,437, more than thirteen periods out. So the breaks are not parked at
the window edge waiting for one more window; they are scattered, and raising `L` buys a fraction of a family
that regenerates.

What this is not, and what it does not settle. It is a capped enumeration, so it excludes nothing: a
blocking clause adds no window, and every model it returns still breaks outside `L`=14. The sample is
narrower than 152 suggests, and the narrowing was not predicted. The 47 machines at `r`=0 carry only 8
distinct break values, 44 at `r`=1 carry 15 and 61 at `r`=2 carry 13, so the effective sample for the
distribution of `n_break` is 8, 15 and 13, and the machine-weighted medians are weighted by how often Cadical
returned each cluster rather than by anything about the family; the distinct-value medians are quoted above
precisely because they do not depend on that bookkeeping, and the KILL holds under both. The narrowing is
not the machines being redundant presentations of each other, which was the first thing checked and is
refuted: run through `census.minimize`, all 152 are already minimal at six states and all 152 are distinct
as minimal machines, so the orbit blocking did enumerate 152 genuinely different behaviours and the count of
machines is not inflated by non-minimal copies. `n_break` is therefore a coarse invariant, many-to-one on
distinct minimal machines rather than a fingerprint of one; the map runs one way only, each minimal machine
having a single break and several minimal machines sharing one. No registered prediction measured break
diversity, so this is exploratory and nothing here says the 8 values at `r`=0 are all of them. They are
reproducible rather than asserted: three runs before the registered one, all at N=6 `r`=0 and all discarded,
found 49,036, 11,899 and 168,457 at seed 999 with phases over the machine, 24,278, 110,203 and 168,457 at
seed 999 with phases over the free period sequence too, and 220,886 at seed 7 -- every value inside the
seed-30 set -- while seed 999 with no phase randomization at all returned 168,457 twice and 41,754, which is
outside it. So the set is seed-robust and demonstrably not closed, at nine values and counting. The three
residues share no break value at all. Q6b, which measures core diversity rather than break diversity, held
at exactly its registered floor of 4 of 18 at `r`=0 and cleared it by nothing.

Controls (`sat-controls.log`, nineteen records). Negative, at `q=1`, N=4: `p=8` (`a+b=4`) is SAT, `p=12` and
`p=16` (`a+b=5`) are UNSAT, as the theorem requires. Positive, at the tested modulus `q=3`: because every run
in the table above is UNSAT, a vacuously unsatisfiable encoding would produce exactly the same output, so the
largest `a+b<=N` period, `p=2^(N-1)`, was run at each of the four `(N,L)` pairs the table uses -- `p=4` at N=3
`L`=11, `p=8` at N=4 `L`=12, `p=16` at N=5 `L`=13, `p=32` at N=6 `L`=14 -- and at all three `r`, twelve runs.
All twelve are SAT in at most 1.0 s, each with a reachable machine and an exactly eventually periodic mask, so
the encoding is non-vacuous at every `(N,L,r)` the table ranges over, not only at the two smallest `N`. Since
`r` enters the encoding in the window bound, the `u(qn+r)` offset and the onset selector, covering all three
is what makes an UNSAT at `r=1` or `r=2` mean what it does at `r=0`. Reproduction, on the N=6 `r=0` onset run: it
returns the same machine as the logged run and reports the mask aperiodic. Recheck (`sat_mask_search.py
recheck`): the exact classifier re-run over the three SAT records of `sat-mask-results.log`, all six states
reachable and all three masks exactly aperiodic, the `r=0` record agreeing machine-for-machine with the
reproduction. Provenance warning on the 84-record `sat-mask-results.log`: it predates that check. In that run
`machine_reachable` was emitted as a hardcoded constant rather than computed, and there was no
`mask_eventually_periodic` field at all. Both are carried by the three recheck records in `sat-controls.log`,
not by that log; do not read the logged `machine_reachable` as a computed result.

Range, and what UNSAT does not cover: `q=3` only, the `p` listed, `L` as stated, and -- the binding
restriction -- the encoding pins `u(qn+r)=v[n mod p]` only from `n0=2^N`, so it excludes a violating mask
only if that mask's onset is at most `2^N`. That floor is far below the a priori bound for the composed
machine, which reaches 96 states at N=5, where the LSD onset bound is `2^96`. The floor is not binding in
the range that can be enumerated (`mask_onset_distribution.py`, `mask-onset-*.json`): over all 1,080 `q=3`
subsequences at N=3, of which 456 are eventually periodic, the largest mask onset is 1; in a seeded 4,000 of
39,168 at N=4, of which 798 are eventually periodic, it is 2. The floors there are 8 and 16. Both runs
report `window_unresolved` 0, so each maximum is over every eventually periodic case and not over a
resolvable subset; at N=3 the count 456 independently matches `odd-mask-probe-q3-N2-3-4.json`. For N=5 and
N=6 that is extrapolation from smaller N, not evidence.

### 5.4 Radix k>=3 (sharp pair derived; optimality proved; validity exhaustively supported)

Derivation. The radix theorem `1b53bd2baa1611ab` writes the tail period as `p=e*d` (every prime of `e`
divides `k`, `gcd(d,k)=1`), `a` least with `e | k^a`, and proves `M>=a+d` and agreement once the canonical
length is at least `n-M+a<=n-d<=N-1`. Hence `a<=N-1`, `d<=N`, `e | k^(N-1)`, `d | L_k(N)` with
`L_k(N)=lcm{d<=N : gcd(d,k)=1}`, and every integer `>=k^(N-2)` has at least `N-1` digits:

```text
H_sharp(k,N) = k^max(0,N-2),     P_sharp(k,N) = k^(N-1) * L_k(N).
```

At `k=2` this is the binary pair. For `k=3`: N=4 gives (9,108), N=5 gives (27,1620); at N=5 the
conservative pair `(k^N, k^N lcm(1..N))` is (243, 14580), so the sharp period is smaller by a factor of 9.

Optimality (proved, componentwise as in 5.2, `radix_families.py`, `radix-families.json`). Machines with at
most N states and a root loop: `[n<k^(N-2)]`; `[k^(N-1) | n]` (saturating trailing-zero counter);
`[d | n]` for each prime power `q^j<=N`, `gcd(q,k)=1`. The onset machine violates equality at
`k^(N-2)-1` for every shift; the lcm of the attained least tail periods is `P_sharp(k,N)`, so any universal
period is a multiple of it. Machine-checked with the exact LSD product for bases 3,4,5,6,7 and N=2..8:
each family passes at the sharp pair and fails at `H_sharp`-1 or at `P_sharp/q` for every prime `q | P_sharp`.

Exactness of `a+d<=N` (partly proved). The proof of Claim C carries over word for word for `e=k^a`: `[k^a d | n]`
has exactly `a+d` states in every radix (`|w|=i<a` with `w<k^i` forces `k^i | w`, hence `w=0`; class `0 mod d`
splits by `min(v_k(j),a)`). Checked by minimal DFAO size for all `p<=1200` in radices 3,4,5,6,10
(`radix-pair-sizes.json`): 0 periods have fewer than `a+d` states; every prime-power radix (3,4,5) has
exactly `a+d` for all 1200; radices 6 and 10 have exactly `a+d` whenever `e=k^a` and MORE than `a+d` for
317 and 290 periods with `e` not a power of `k` (e.g. base 6, `p=8`: 5 states against `a+d=4`). For those
periods the indicator machine does not attain the bound. Exact answer for every sequence, not only
indicators (`radix_min_states.py`, `radix-min-states.json`): for a tail period `p` the minimum state count
of any eventually periodic sequence is the minimum, over all `2^p` purely periodic labelings with least
period `p`, of the number of bisimulation classes of the residue automaton `r -> (k r+d) mod p` (prefix
states only add). Exhaustive for bases 6, 10, 12 and `p<=18` (54 cases): the minimum equals `a+d` in 45
and exceeds it in 9, never falls below it. The 9: base 6 `p`=8 (5 vs 4), 9 (4 vs 3), 16 (8 vs 5); base 10
`p`=8 (5 vs 4), 12 (7 vs 5), 16 (9 vs 5); base 12 `p`=9 (4 vs 3), 16 (5 vs 3), 18 (4 vs 3). So the radix
proof's `M>=a+d` is sound but not tight for composite `k` when `e` is not a power of `k`; a sharper
bound exists there and is not derived. `P_sharp` is unaffected: it is attained by the families above.

Regression of validity (`radix_census.py`, exact LSD classifier, sharp equality by LSD product):

| base | N | machines | scope | violations |
|---:|---:|---:|---|---:|
| 3 | 2 | 96 | exhaustive canonical | 0 |
| 3 | 3 | 18,144 | exhaustive canonical | 0 |
| 3 | 4 | 300,000 | seeded sample | 0 |
| 4 | 2 | 448 | exhaustive canonical | 0 |
| 4 | 3 | 609,768 | exhaustive canonical | 0 |
| 5 | 2 | 1,920 | exhaustive canonical | 0 |
| 5 | 3 | 200,000 | seeded sample | 0 |
| 6 | 2 | 7,936 | exhaustive canonical | 0 |
| 6 | 3 | 200,000 | seeded sample | 0 |
| 7 | 2 | 32,256 | exhaustive canonical | 0 |

Exhaustive runs reproduce the constants from the data: max onset `k^(N-2)` and lcm of attained periods equal to
`P_sharp` (3,N=3: 18; 4,N=3: 48; 5,N=2: 10; 6,N=2: 6; 7,N=2: 14). The samples do not attain every period and
are not used for that. Validity of the sharp pair for `N>=4` rests on the radix proof's inequality plus these
tests; it is not independently proved here.

## 6. What is not covered

- No all-N proof of the MSB theorem itself beyond the doc's argument; the regression stops at N=5.
- `census.tail_states` takes the union of successor sets over iterations 120 to 239, a fixed horizon
  rather than a detected fixed point. Adequate for N<=5 (preperiod plus period is below 2^N) but it feeds
  `M` and is not a general implementation.
- Radix `k>=3` is now covered by 5.4. Open inside it: the exact attainable set for composite radices when `e`
  is not a power of `k` (`a+d` is not tight there, shown for `p<=18`; the true bound is not derived). Record `1b53bd2baa1611ab` still carries only the conservative pair.
- The exact classifier is the LSD checker; a bug shared by both would not be seen, though the two
  products were written for different digit orders.
- Nothing here concerns Rule 30: the constants apply to a generic automatic observable, and a Rule 30
  presentation still needs every local identity verified at every coordinate.

## 7. Reproduction

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/results-r1-msb-automatic-period-bound-md
uv run python census.py 1 2 3 4        # census-N1-2-3-4.json
uv run python census.py 5              # census-N5.json  (about 6 min on 10 cores)
CTRL=H uv run python census.py 3 4     # control: halved onset must fail
CTRL=P uv run python census.py 3 4     # control: halved period must fail
uv run python extremal_family.py 15    # extremal-family.json
uv run python pair_family.py           # pair-family.json
uv run python kill_tests.py            # kill-tests.json
uv run python odd_mask_probe.py 3 2,3,4
uv run python odd_mask_probe.py 5,7 2,3
uv run python odd_mask_probe.py 5,7 4 20000     # seeded samples
uv run python odd_mask_probe.py 3 5 20000
uv run python odd_mask_probe.py 9,15 2,3
cat sat_jobs.txt | xargs -P 9 -L 1 sh -c 'uv run python sat_mask_search.py "$@"' _   # 84 runs
uv run python sat_mask_search.py 4 1 0 period 11 8     # sat-controls.log, negative controls at q=1:
uv run python sat_mask_search.py 4 1 0 period 11 12    #   SAT, then UNSAT for 12 and 16
uv run python sat_mask_search.py 4 1 0 period 11 16
for r in 0 1 2 ; do                                    # positive controls at q=3, every (N,L,r): all SAT
  uv run python sat_mask_search.py 3 3 $r period 11 4
  uv run python sat_mask_search.py 4 3 $r period 12 8
  uv run python sat_mask_search.py 5 3 $r period 13 16
  uv run python sat_mask_search.py 6 3 $r period 14 32
done
uv run python sat_mask_search.py 6 3 0 onset 14 480    # reproduces the logged N=6 SAT machine
uv run python sat_mask_search.py recheck sat-mask-results.log   # classifies its three SAT records
uv run python onset_witness_break.py sat-mask-results.log 1048576   # onset-witness-break.json, under 1 s
uv run python mask_onset_distribution.py 3 3           # mask-onset-q3-N3.json
uv run python mask_onset_distribution.py 3 4 4000      # mask-onset-q3-N4-sample4000.json
uv run python radix_census.py 3 3 ; uv run python radix_census.py 4 3      # also (3,2) (4,2) (5,2) (6,2) (7,2)
uv run python radix_census.py 3 4 300000 ; uv run python radix_census.py 5 3 200000 ; uv run python radix_census.py 6 3 200000
uv run python radix_census.py 2 6 100000 ; uv run python radix_census.py 2 7 30000
uv run python odd_mask_probe.py 3 5 200000
uv run python radix_families.py        # radix-families.json, radix-pair-sizes.json
uv run python radix_min_states.py 6,10,12 18   # radix-min-states.json
```

The `.log` files are ignored by the global gitignore; force-add cited logs.

## 8. Report

STATUS: done

Proved (exhaustive or symbolic, each with a control that fails when false):
- For every `N>=2`, `H_sharp=2^(N-2)` cannot be lowered and `P_sharp` is the least universal period (componentwise); machine-checked N=2..15.
- `(a,b)` is attained by an N-state machine iff `a+b<=N`; `[2^a b | n]` has exactly `a+b` states, checked for 72 pairs and proved symbolically.

Computed (stated ranges only):
- Zero violations of the sharp equality or of the proof's intermediate claims over all reachable machines N<=5 (15,532,800 labelled).
- Kill tests K1 to K3 pass; odd-modulus masks q=3,5,7,9,15 keep the N-state constants in every tested case (exhaustive q=3 N<=4, q=5,7,9,15 N<=3; seeded samples beyond, up to 200,000 at q=3 N=5).
- Radix 3..7 sharp pair `(k^(N-2), k^(N-1)*L_k(N))`: optimal (proved, N<=8) and 0 violations in the regression of 5.4; binary samples at N=6,7 also 0 violations.

Refuted: nothing. One record-level observation: the retracted statement `t=2^j-1` for the seed {-1,+1} neighbour is wrong (`t+2` is a power of 2), which is consistent with its retraction.

Still open: an all-N proof of the theorem is only the doc's argument plus regression (exhaustive N<=5, samples N=6,7); odd-mask preservation is conjectured with no proof (SAT-excluded window-wise for `q=3`, N=3..6, the listed periods, and only for masks whose onset is at most `2^N`, a floor far below the a priori bound and checked non-binding only at N=3,4; N=6 onset inconclusive, and the registered next lever is retired by its own pre-registration, P2 firing on `r`=0 and `r`=2: excluding the three `L`=14 witnesses needs `L`=19, 15 and 16, so a rerun at `L`=15 clears one of three, where a fresh witness would break is not bounded, and no replacement lever is registered); radix `k>=3` validity for N>=4 rests on the radix proof plus samples, and for composite `k` and `e` not a power of `k`, `a+d<=N` is shown NOT tight (computed, `p<=18`) and the true attainable set is not derived; the sharp pair is not applied to the SAT encodings (not my files); R1 itself.

Ladder statement changed: none. R1 and P1 are unchanged.

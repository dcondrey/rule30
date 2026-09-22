# Formalizing the reduction chain

Date: 2026-09-21. **STATUS: three of the six bridges named by ladder node
`formal_reductions` are kernel-checked: the P2 energy bridge (sections 1 to 4),
capacity/budget -> mortality (8), mortality -> pt2 (9). No prize is less open.**

Artifact: [Rule30P2Bridge.lean](Rule30P2Bridge.lean), Lean 4.33.1, core only
(`import Std.Tactic`), no Mathlib, no lake project. Replay output:
[replay.txt](replay.txt).

## 1. What is proved

**PROVED (Lean kernel, every sequence `c : Nat → Bool`):** the P2 target and
its three ladder forms are one statement.

| Lean theorem | Ladder edge | Source claim |
|---|---|---|
| `densityHalf_iff_shellMaxLittleO` | `shell_max <-> p2` | P2.1, `A(T) - T/2 = o(T)` iff `M_k = o(N)` |
| `shellMaxLittleO_iff_flexibleEnergyToZero`, `densityHalf_iff_flexibleEnergyToZero` | `energy <-> p2` | `P2 <=> F_k -> 0`, RESULTS-p2-flexible-scale-audit.md section 1 |
| `shellMaxLittleO_iff_orderedEnergyLittleO`, `orderedEnergyLittleO_iff_maxBlockEnergyLittleO`, `densityHalf_iff_orderedEnergyLittleO` | `ordered_energy <-> p2` | P2.2, `P2 <=> H_k = o(N^2) <=> max_j E_(k,j) = o(N^2)` |

The theorems are quantified over every Boolean sequence, so they hold for
the Rule 30 centre column without using anything about Rule 30. The file
states them for it as `center_densityHalf_iff_shellMaxLittleO`,
`center_densityHalf_iff_flexibleEnergyToZero` and
`center_densityHalf_iff_orderedEnergyLittleO`, where `center t` is the bit at
coordinate zero after `t` steps of `l XOR (c OR r)` from the singleton.
`center_first_eight` checks `c_0..c_7 = 11011100` by kernel evaluation, with
no axiom.

Intermediate results a later bridge can reuse: Cauchy-Schwarz for finite
integer sums (`sumTo_sq_le`), the squared prefix estimate
`(M - L)^2 L <= N E_(k,j)` when `M > L` (`prefix_estimate`), and
`H_k <= 8 M_k 2^k` (`orderedEnergy_le`).

## 2. Definitions and how the little-o statements are written

Everything is over `Nat` and `Int`; no rationals or reals appear. Each
little-o is written with its denominator cleared.

| Object in the documents | Lean |
|---|---|
| `z_t = 1 - 2 c_t` | `z c t` |
| `A(T)`, ones among `c_0..c_(T-1)` | `ones c T`, with `signedSum_eq : S c T = T - 2 * ones c T` |
| `M_k = max_(0<=u<=N) abs(sum_(r<u) z_(N+r))`, `N = 2^k` | `shellMax c k`, both ends of `0 <= u <= 2^k` included |
| `b_(k,j,a)`, `E_(k,j)`, `H_k` | `blockSum`, `blockEnergy`, `orderedEnergy` |
| `A(T) - T/2 = o(T)` | `DensityHalf`: for every `m`, eventually `m * abs(2 A(T) - T) <= T`; this is `abs(A(T) - T/2) <= T/(2m)` |
| `M_k = o(N)` | `ShellMaxLittleO`: for every `m`, eventually `m * M_k <= 2^k` |
| `F_k -> 0`, `F_k = min_(j<=k) (V_(k,j) + 4^(j-k))`, `V_(k,j) = E_(k,j)/(N 2^j)` | `FlexibleEnergyToZero`: for every `m`, eventually some `j <= k` has `m * (E_(k,j) 2^k + 8^j) <= 4^k 2^j`, which is `m (V_(k,j) + 4^(j-k)) <= 1` multiplied by `4^k 2^j` |
| `H_k = o(N^2)`, `max_j E_(k,j) = o(N^2)` | `OrderedEnergyLittleO`, `MaxBlockEnergyLittleO`, against `4^k` |

A reader checking faithfulness needs only the definitions at the top of the
file, lines 34 to 129, and the theorem statements. The proofs are checked
by the kernel.

## 3. Control

**CONTROL (kernel-checked, the weakened bridge is false):**
`dyadicEndpoints_bridge_fails` and `unpenalizedEnergy_bridge_fails` refute the
two natural weakenings. The witness `halfShell` is `+1` on the first half of
every shell and `-1` on the second. Its dyadic endpoint sums are constant,
`S(2^k) = 2`, and its top-scale energy `E_(k,k)` is zero, so
`DyadicEndpointsLittleO` and `UnpenalizedEnergyToZero` both hold, while
`S(3 * 2^(k-1)) = 2 + 2^(k-1)` and `DensityHalf` fails at `m = 4`. This is the
sentence of P2.1, "checking only dyadic endpoint densities is insufficient",
and the reason `F_k` carries the penalty `4^(j-k)`, both now theorems.

Two checks on the pipeline itself. A first assembly of the file with one
helper lemma replaced by a weaker one of the same name was rejected by `lean`
with exit code 1, so a wrong proof does not pass. And the definitions in the
committed file are byte-identical to the ones the statements were written and
type-checked against before any proof existed.

## 4. What this does not prove

Nothing here bounds `M_k`, `F_k` or `H_k` on the centre column. The file
contains no estimate that uses Rule 30, and P2 stays open. What changes is the
trust in three arrows: a proof of any one of the four forms is now a proof of
P2 by a kernel-checked implication, not by a source-reviewed one.

The other two arrows into `p2` with a P2-side proof, `fixed_window -> p2` and
`matching -> p2`, are not formalized here. Neither is the merge recurrence
`E_(k,j+1) = 2 E_(k,j) - D_(k,j)` on these definitions; its list form is in
`experiments/rule30/Rule30ResearchReduction.lean` and the two files are not
connected.

Axioms: every result depends on `propext`, `Classical.choice` and
`Quot.sound` only, the three standard ones, and `center_first_eight` on none.
The two earlier Lean files in this repository stay on `propext` and
`Quot.sound`; this one also uses `Classical.choice`, which the `grind` tactic
introduces.

## 5. The capacity bridge is not the pigeonhole shape

**CORRECTION (capacity -> mortality):** `capacity_bounds_length` in
`experiments/rule30/Rule30P1Reduction.lean` bounds the length of a walk over a
finite alphabet in which each letter occurs at most `cap` times, and its
docstring matches `cap` to `K = 8` of `bounded_capacity_language.py`. That `K`
is the threshold at which inverse path counts saturate, "replace every count
n by min(n,K+1) after every update"
(docs/rule30/RESULTS-other/RESULTS-bounded-capacity-language.md:81-85). It is
not a bound on how often a state recurs. The bridge as the ledger states it,
"Every original has finite `Q_2`; a repeat bound at its capacity and the
survival inequality force finite lifetime", contains no walk and no occurrence
bound: it instantiates `B` at `K = Q_2(w)` and applies
`r + N + 1 <= 2^(D+1) (r + 2)`. So instantiating the abstract shape against
`capped_edge` would not produce the bridge. The whole weight of both
`capacity -> mortality` and `budget <-> mortality` is the survival inequality
of docs/rule30/RESULTS-other/RESULTS-repeat-budget-lower-bound.md, which
section 8 now proves.

A read-only extraction pass over the five P1 bridges, with definitions,
proof locations and size estimates, is saved beside this file as
`p1-bridge-specs.json`. Nothing in it has been verified here except the point
above, and no claim in this document rests on it.

## 6. Replay

From the repository root, where `lean-toolchain` pins 4.33.1:

```sh
lean experiments/rule30/formalize-the-reduction-chain/Rule30P2Bridge.lean; echo $?
lean experiments/rule30/formalize-the-reduction-chain/Rule30SurvivalBridge.lean; echo $?
lean experiments/rule30/formalize-the-reduction-chain/Rule30AlternatingTraceBridge.lean; echo $?
```

Each exits 0 in a few seconds, printing the axiom reports saved as
`replay.txt`, `replay-survival.txt` and `replay-alternating-trace.txt`. Exit status alone is not the check: confirm the file has no
`sorry` and that the printed axiom lists are the ones above.

## 7. Ladder statements changed

- Edges `energy <-> p2`, `shell_max <-> p2` and `ordered_energy <-> p2`:
  `logic_verified` true, basis `lean_kernel_checked`.
- Node `formal_reductions`: one of six bridges checked; its closure text no
  longer sends the reader to instantiate the pigeonhole shape.
- Node `p2`: its closure text no longer says the three equivalences are not
  formally verified.
- Edges `budget <-> mortality` and `capacity -> mortality`: `logic_verified`
  true, basis `lean_kernel_checked` (section 8).
- Edge `mortality -> pt2`: `logic_verified` true, basis `lean_kernel_checked`
  (section 9).
- No node status moves. `formal_reductions` stays open until the three remaining
  P1 bridges are checked: sep -> pt2, rw -> sep, bwh -> rw.

## 8. The survival inequality and the capacity/budget -> mortality bridge

Artifact: [Rule30SurvivalBridge.lean](Rule30SurvivalBridge.lean), same
toolchain and conventions. Replay output:
[replay-survival.txt](replay-survival.txt).

**PROVED (Lean kernel, every legal Z-frontier):** the survival inequality and
both mortality bridges, with no finite computation assumed.

| Lean theorem | Statement |
|---|---|
| `reconstruction` | After `n` successful updates, the high bit at depth `d` is the formal field `F_d` of the emitted scalars once `n >= 1 + floor(d/2)`, the low bit is `G_d` once `n >= 1 + ceil(d/2)`; from an onset with terminal high bit one the thresholds are `ceil(d/2)` and `1 + floor(d/2)` |
| `runBound` | A run with no repeated scalar from a legal frontier of length `a` has length at most `a + 3`, at most `a + 1` when the terminal high bit is one |
| `survival` | `r + N + 1 <= 2^(D+1) (r + 2)` on every successful prefix, and `(r + 1)` in place of `(r + 2)` when the terminal high bit is one |
| `budgetAt_iff_mortalAt`, `budget_iff_mortality` | Edge `budget <-> mortality`: a repeat budget at length `r` holds iff every legal frontier of length `r` dies, and so for all lengths; `horizon_of_budget` gives the explicit `N <= 2^(B+1)(r+2) - r - 1` |
| `mortality_of_capacity_budget` | Edge `capacity -> mortality`: if for every `K` one `B(K)` bounds repeats over the legal frontiers with `Q(w) <= K`, every legal frontier dies. Proved for every function `Q` at once, so it needs no definition of `Q_2` |

The frontier, the update `Z` and the chronological guards are the definitions
of RESULTS-variable-length-episode-composition.md:25-39, stated in lines 40 to
146 of the file. Before any proof was attempted the Lean `Z` and `run` were
compared with `aperiodic_mortality_audit.step` on all 682 legal frontiers of
length at most 5: counts, total lifetimes and a checksum of final frontiers and
repeat counts agree. `reconstruction`, `runBound` and `survival` were brute-force
checked as statements on every legal frontier of length at most 6, 8 and 8.

The period-28 table of RESULTS-repeat-budget-lower-bound.md:110-136 is not an
input: the file evaluates the two-bit recurrence in the kernel, proves its
return at depth 28 by `decide`, and derives the two pattern facts, no four
equal non-dash symbols and no three from an odd depth. The source's strings
`H_0` and `H_1` were reproduced exactly by `#eval` during the proof.

**CONTROL (kernel-checked, the counting step needs the run bound):**
`survival_counting_fails_without_runBound` shows `r + N + 1 <= 2^(D+1) (r + 2)`
is false for tapes in general, at `r = 1` with ten alternating scalars. Three
data controls were tried first and none fails, which is itself information:
through length 6 to 8, frontiers with `a_0 = 0` also satisfy the inequality, an
unguarded scan never alternates longer than `a + 3`, and an XOR variant of the
scan satisfies both bounds. The run bound is far from sharp at these lengths,
the longest initial alternating run found being 5 at `r = 6`.

What this does not prove: a budget at any length, a bound at any capacity, or
mortality. The correspondence between `Q_2` as computed by `capped_edge` and
its set-theoretic definition is evidence for `cap17` and `cap18` and is not
part of this bridge. The file carries five small helper lemmas twice, under a
suffixed name, because its four parts were proved independently.

## 9. The alternating-trace reconstruction and the mortality -> pt2 bridge

Artifact: [Rule30AlternatingTraceBridge.lean](Rule30AlternatingTraceBridge.lean).
Replay output: [replay-alternating-trace.txt](replay-alternating-trace.txt).
Every result depends on `propext` and `Quot.sound` only.

**PROVED (Lean kernel, every left-finite Rule 30 row):** an alternating centre
trace yields a legal finite Z-frontier that passes every chronological guard,
so mortality excludes period two.

| Lean theorem | Statement |
|---|---|
| `immortalFromAlternating` | If `y` has a leftmost one and its centre trace satisfies `c_(t+2) = c_t` for all `t` with `c_1 != c_0`, there is a legal frontier `w` with `run w n` defined for every `n` |
| `leftFinite_of_nonzero_finiteSupport` | A nonzero row of finite support has a leftmost one |
| `periodTwoExcluded_of_mortality'` | Edge `mortality -> pt2`: if every legal finite frontier eventually fails a guard, no nonzero finite row has a nonconstant centre trace of period two from time zero |

The written sources assert this bridge and never assemble it:
PRIZE-PROBLEM-DEPENDENCIES.md:63-65 and RESULTS-alt-trace-fiber.md:374-381 state
it as a sentence, and how the first frontier and its length come from the
diagram is not written anywhere. The proof here does not follow the documented
route through suffix parity, the zero-cost normal form and `last1`. It uses an
explicit dictionary: with the leftmost one at `-d`, a time `T0` with `c_T0 = 0`,
`p = floor((d + T0)/2)` and `q = T0 - p - 1`, the frontier after `n` updates is
`a_k(n) = x(q+1+n+k, -(p+n-k))`, `b_k(n) = x(q+n+k, -(p+n-k))`, `0 <= k < p+n`.
Each scan step is then Rule 30 at one cell (`scanStep_mem`, with no hypothesis),
the zero start memory and `a_0 = 1` come from the left front (`front`,
`mem_zero`, `symA_zero`), and the `n`-th guard is Rule 30 at the single cell
`(T0 + 2n + 1, -1)` given the pinned value one (`pin`, `guard`). Finiteness
enters in exactly those two places.

Before the proof was attempted the dictionary was brute-force checked here on
38,973 random left-finite rows of support within `[-9, 9]` whose centre
alternates on a finite window, 85 of them with the leftmost one at a
non-negative position: the frontiers are legal, `step` maps `w_n` to `w_(n+1)`,
and the `n`-th guard passes whenever the centre alternates through time
`T0 + 2n + 2`. A first version of that test, whose window stopped one step
short, reported guard failures on 73 percent of cases; the failures were the
test's, and they show the check can fail.

**CONTROL (kernel-checked, finiteness is load-bearing):**
`alternatingCenter_without_finiteSupport` exhibits the 7-periodic row with ones
at `j = 6 (mod 7)`. Its orbit 0000001, 1000011, 0100110, 1111101 has temporal
period 4 and its centre column reads 0, 1, 0, 1, so `PeriodTwoExcluded` is false
with `FiniteSupport` dropped. That row has no left front, which is why its
frontier is immortal without contradicting mortality.

What this does not prove: mortality, or period-two exclusion. It treats an
exact period from time zero; an eventual period is reduced to that by P1.1 and
is not formalized here. `Z` ignores the right-realizability of the scalar tape,
which only enlarges the set of frontiers mortality must kill, so no converse
holds or is claimed. The scalar the proof tracks is `x(T0 + 2n - 1, -2)`; its
identification with the column `+1` sample `x(T0 + 2n, 1)` is a two-line
consequence of the rule at the centre and is not part of the Lean file.


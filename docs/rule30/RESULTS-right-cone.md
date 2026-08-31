# Rule 30 right-cone reconstruction: branch-free inverse traces and a solver-free horizon certificate

## Status

**OPEN.**  Nothing here proves center-column nonperiodicity, and nothing here
licenses removing that qualification anywhere else in this tree.  Bounded
exhaustion is not a nonperiodicity proof.

This cycle produces:

1. **PROVED:** three boundary-pinned right-cone diagonals, valid for every
   finite row, independent of the interior.
2. **EXACT COMPUTATION:** a branch-free, bit-parallel inverse-trace
   reconstruction that solves an entire exponential family of right parts in
   `O(depth^2)` bigint operations, validated cell for cell against the SMT
   horizon table of `RESULTS-eventual-period.md`.
3. **EXACT COMPUTATION:** a solver-free bounded certificate on the minimum
   support radius of any finite row with a `p`-periodic center prefix.

**ATTRIBUTION.**  The inverse-trace reconstruction itself is left permutivity
and is not new; `RESULTS-inverse-trace.md` says so explicitly.  What is new
here is the branch-free bit-parallel form, the pinned diagonals below, and the
removal of the SMT solver from the trust base of the horizon table.

## The right-cone representation

Rule 30 is

```text
s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).
```

Fix a row `a` with `a(x)=0` for `x>W` and index space-time by the right-cone
diagonal `k` via `D_k[t] = s(t, t-k)`.  Substituting `x=t-k` turns the three
neighbours into diagonals `k`, `k-1`, `k-2`, giving exactly

```text
D_k[t] = D_k[t-1] XOR (D_{k-1}[t-1] OR D_{k-2}[t-1])       (Rule 30)
D_k[t] = D_k[t-1] XOR  D_{k-2}[t-1]                        (Rule 90)
D_k[0] = a(-k),   D_k[k] = c_k,   D_k == 0 for k <= -W-1.
```

Two consequences do the work.

* Diagonal `k` reads only diagonals `k-1` and `k-2`, so the diagonals can be
  computed in one increasing pass over `k`.
* Within that pass, `D_k[0]` enters `D_k[t]` through an XOR chain only.
  Flipping `D_k[0]` flips `D_k[t]` for every `t`.  Hence the value of `a(-k)`
  forced by a target center bit `c_k` is a single XOR:
  `a(-k) = c_k XOR (the a(-k)=0 evaluation of D_k[k])`.

The reconstruction is therefore **branch-free**: no search, no backtracking, no
case split.  Because the only data-dependent quantities are single bits, an
entire family of right parts can be carried in the bit positions of one bigint
per `(k,t)` cell, so `2^W` right parts are reconstructed simultaneously in
`O((W+depth) * depth)` bigint operations.

`experiments/rule30/right_cone_probe.py` implements this;
`test_right_cone_probe.py` checks the diagonal recursion against direct
simulation for both rules and both index conventions.

## PROVED: pinned right-cone diagonals

Let `a` be any finite row with right endpoint `B` (so `a(B)=1` and `a(x)=0` for
`x>B`).  Then for every `t>=0`

```text
s(t, B+t)   = 1
s(t, B+t-1) = a(B-1) XOR (t mod 2)
s(t, B+t-2) = a(B-2) XOR (t mod 2)
```

*Proof.*  In diagonal coordinates these are `D_{-B}`, `D_{-B+1}`, `D_{-B+2}`.
Diagonals `k <= -B-1` vanish identically, so `D_{-B}[t] = D_{-B}[t-1]`, and
`D_{-B}[0]=a(B)=1`.  With `D_{-B} == 1` the OR gate for the next two diagonals
is constantly one, so each satisfies `D[t] = D[t-1] XOR 1` from its initial
value `a(B-1)`, `a(B-2)`.  QED

The first identity is the standard right-edge invariant.  The second and third
are the ones used below: the two diagonals under the edge are pure period-two
alternations whose phase is set by the initial row and nothing else.  Rule 30's
right cone is thus rigid for three diagonals and only becomes data-dependent at
the fourth.  Test: `DiagonalAlgebra.test_pinned_diagonals`.

## EXACT COMPUTATION: reproducing the SMT horizon table with no solver

Fix a nonconstant period-`p` word and let the target be its periodic extension.
Pin `a(0)=c_0` and let `a(1..w)` range over all `2^w` values, which covers every
row with right endpoint at most `w`.  For each such right part the
reconstruction returns the unique forced left half.

A row supported in `[-w,w]` agrees with the target through time `H` and fails at
`H+1` exactly when `H+1` is the least `k>w` whose forced `a(-k)` is one: the
forced values at `k<=w` are inside the allowed support, and the first forced one
outside it is the first time the actual row (which has `a(-k)=0` there) must
disagree.  Any other left half disagrees strictly earlier.  So the maximum over
all rows in `[-w,w]` of the periodic-prefix horizon is the maximum over right
parts and words of that least-`k` minus one.

Recomputing the table of `RESULTS-eventual-period.md` this way reproduces all
40 cells:

| `p` \ `w` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 6 | 6 | 6 | 6 | 8 | 9 | 9 | 14 |
| 3 | 4 | 5 | 9 | 9 | 9 | 13 | 13 | 16 |
| 4 | 6 | 6 | 7 | 10 | 12 | 13 | 13 | 16 |
| 5 | 10 | 10 | 10 | 10 | 12 | 12 | 13 | 15 |
| 6 | 7 | 9 | 13 | 13 | 13 | 15 | 15 | 17 |

Test: `OracleTable.test_reproduces_smt_horizons`.  Two structural properties
are asserted on the transcribed table, and the measured values are asserted
equal to it, so a mask or indexing bug would have to break both together:
`H(p,w)` is nondecreasing in `w`, and `H(kp,w) >= H(p,w)` because a
`p`-periodic prefix is also `kp`-periodic.

`test_forced_row_realises_its_horizon` closes the loop the other way: it rebuilds
each forced row as an explicit cell set, simulates it forward with the naive
Rule 30 evaluator, and checks the trace matches the target through exactly
`H` and differs at `H+1`.  Nothing in the horizon claim rests on the
reconstruction being trusted.

The witness of `RESULTS-eventual-period.md` is recovered: the row `{-1}` has
trace `0101010` and breaks at `t=7`, and the reconstruction against
`(01)^infinity` forces `a(-7)=1`.

**This removes Z3 from the trust base of the table.**  It does not extend the
table's meaning: these are still bounded exclusions.

## Adversarial control: the metric can fire negative

The sweep statistic below is the per-right-part **deepest forced one**: the
largest `k <= depth` whose forced `a(-k)` is one.  A finite row realising the
target must have left endpoint at or below `-d`, so the minimum of `d` over the
family is a lower bound on the support radius of any counterexample.  The
statistic is capped by `depth` by construction, so "it saturates" is worthless
evidence unless the same statistic is shown to come back small on a problem
where finite rows genuinely exist.

Rule 90 supplies that problem.  Its diagonal recursion drops the OR, so the
`D_{k-1}` term disappears and with it the phase gate that makes Rule 30's
forced left half self-sustaining.  The row `{-1,1}` has identically zero center
forever; `Rule90Control.test_row_minus1_plus1_has_zero_center` confirms it by
direct simulation through `t=128`, not by assertion.

Running the identical sweep at `depth=256` on the all-zero target:

| `W` | Rule 90, (min, max) deepest forced one | Rule 30, (min, max) deepest forced one |
|---:|---:|---:|
| 1 | (1, 1) | (255, 255) |
| 2 | (1, 2) | (255, 255) |
| 4 | (1, 4) | (255, 255) |
| 8 | (1, 8) | (255, 255) |
| 12 | (1, 12) | (255, 255) |

Under Rule 90 every right part's forced left half goes silent within the width
itself: `W=1` returns `{-1,1}` exactly.  Under Rule 30 every nonzero right part
forces ones out to `k=255`, the deepest odd diagonal in range; the reason is
the checkerboard left tail described below.  The single unresolved
case in each column is the all-zero row, whose trace really is constantly zero.

So the statistic distinguishes "no finite row exists" from "the method always
emits ones," and it does so on a rule one gate away from the target.  A second
data point: at the alternating target `(01)^infinity`, Rule 90 also forces ones
to `k=253` for every `W<=12`, so the separation is a property of the target and
rule together, not a Rule-90-is-easy artifact.

The Rule 90 entries are the (min, max) of the deepest forced one over the
`2^W - 1` nonzero right parts; the Rule 30 entries are that same pair, which is
`(255, 255)` in every column, so every nonzero right part forces a one at
`k=255` and none forces one at `k=256`.  The reason is exact and checked, not
inferred: for `k>W` the forced left half is the checkerboard `a(-k)=1` iff `k`
is odd, identically across all nonzero right parts, so the deepest one in range
is the deepest odd `k`.  The transient below `k<=W` does depend on the right
part.  Test: `Rule90Control.test_rule30_zero_target_does_not_go_silent`.

## EXACT COMPUTATION: the bounded support certificate

Sweep: rule 30, `depth=256`, periods 2 through 6, all 114 nonconstant words,
right-part widths `W=1..16`.  That is 1824 sweeps covering 14,941,980 right
parts, each of which forces exactly one left half.

For each `(p, W)` the table gives the minimum over words of
`min_deepest_one`, the smallest over right parts of the deepest forced one:

| `p` \ `W` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 252 | 252 | 252 | 252 | 252 | 251 | 251 | 247 | 244 | 242 | 242 | 242 | 242 | 242 | 242 | 242 |
| 3 | 253 | 253 | 252 | 250 | 249 | 249 | 248 | 240 | 240 | 240 | 240 | 240 | 240 | 240 | 239 | 239 |
| 4 | 251 | 250 | 250 | 250 | 249 | 249 | 249 | 247 | 244 | 242 | 242 | 242 | 242 | 242 | 242 | 237 |
| 5 | 243 | 243 | 243 | 243 | 243 | 243 | 243 | 243 | 243 | 242 | 242 | 242 | 239 | 239 | 239 | 235 |
| 6 | 246 | 246 | 245 | 245 | 245 | 245 | 245 | 240 | 240 | 240 | 240 | 240 | 240 | 239 | 238 | 233 |

Reading a cell, with the depth qualifier attached because it is not optional:

> **EXACT COMPUTATION.**  No finite row with right endpoint at most `W` and
> left endpoint above `-min_deepest_one` has a center trace agreeing with any
> nonconstant `p`-periodic target through time 256.

Across all 1824 sweeps, **zero** right parts had no forced one at all, so no
right part in this family admits a finite row with a `p`-periodic center that
the reconstruction fails to constrain.

The global minimum is 233, at `p=6`, word `001010`, `W=16`.  Its single
extremal right part is `a(0..16) = 00000111011010001` and the forced row is
supported in `[-233, 16]` with 122 ones.  Simulating that row forward with the
naive evaluator reproduces `(001010)^infinity` exactly through `t=256`, and no
`a(-k)` is forced for `233 < k <= 256`.  So the certificate is close to tight:
the bound 233 is achieved by an actual row, not merely not contradicted.
`Certificate.test_extremal_case_is_a_real_row` pins the same construction on a
cheaper cell.

**The result is flat.**  `min_deepest_one` sits within about 20 of `depth` for
every `(p, W)` swept, drifting down slowly as `W` grows and never approaching a
bounded value.  There is no descent: nothing here shrinks the obligation to a
finite check.  What it does show is that the forced left half never goes silent
for any of the 14.9 million right parts examined, which is the behaviour a true
nonperiodicity theorem would require and which Rule 90 visibly fails.

## What this does not do

* **It is not a proof.**  Bounded UNSAT is not nonperiodicity.  This targets
  item 5 of the brief, a sharply reduced obligation with an executable exact
  certificate.  It is not items 1 through 3.
* **The search space is `2^W` right parts per (word, `W`), each forcing exactly
  one left half.**  It is not `2^(W+depth)` rows.  The completeness argument is
  that any other left half disagrees with the target strictly earlier, so the
  forced one is extremal; that is what makes `2^W` enough.  Do not inflate the
  count and do not report it as an exhaustive row search.
* **Every claim is conditional on agreement through `depth`.**  A right part
  whose forced left half went silent at `k=233` is constrained only up to
  `t=256`; `min_deepest_one` is a support bound *given* agreement through 256,
  not a support bound simpliciter.  Rows with left endpoint below `-depth` are
  outside the computation entirely.
* **On the lone-seed orbit the parameters are not independent.**  For
  `y = F^T(seed)` the support is `[-T,T]`, so `B = T` and extending left depth
  while capping `W` buys nothing there.  This is a statement about all finite
  rows of bounded right endpoint, not about the seed orbit.
* **The pinned diagonals are the only new PROVED content.**  The reconstruction
  is left permutivity, already recorded in `RESULTS-inverse-trace.md`.

## Next measurement: done, and it closes this line

The follow-on named here was the settling time and eventual period of diagonal
`j`.  It was run.  `RESULTS-diagonal-periodicity.md` records the result: every
right-cone diagonal is purely periodic with a power-of-two period (a KNOWN
result, re-derived), the periods grow like `2^(0.4 j)`, and the periodic region
reachable from the right boundary at time `t` is only `~2.4 log2(t)` diagonals
wide while the center column at time `t` sits at diagonal `t`.

The center bit is therefore always read strictly inside the first period of its
diagonal, where periodicity constrains nothing.  That is a quantitative reason
why this representation, and the sweep above with it, cannot reach the center
column.  The same document records that the forced left half does *not* forget
the right part for nonconstant periodic targets, which is why the mechanism
behind both constant-trace theorems has no analogue here.

Do not extend the sweep.  The bounded certificate above stands as an exact
computation; it is not a step toward the theorem.

## Reproduction and spending

From `experiments/rule30`:

```bash
uv run python -m unittest test_right_cone_probe.py
uv run python right_cone_probe.py --max-width 16 --depth 256 \
  --periods 2 3 4 5 6 --json > sweep30.json
uv run python right_cone_probe.py --max-width 12 --depth 256 \
  --rule 90 --zero-target
```

The full sweep runs in 99 seconds single-threaded.  Width 18 and above is
dominated by bigint memory traffic and was not run.

- Modal: **$0**.  The MODAL-COMPUTE-CHARTER gate is not satisfied and nothing
  here needs it.
- Paid model-provider calls: **$0**.
- Crosstalk: not invoked.

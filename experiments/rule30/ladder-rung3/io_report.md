# Original a7 i.o. lemma: already implied by the existing five-zero theorem

Date: 2026-09-09. Status: **the original a7 i.o. lemma follows from a theorem
already proved in this repository. This does not settle the aperiodic-witness
problem, and adds no new `q` to rung 2's existing coverage.**

The source is
[`RESULTS-RIGHT-FILTERED-MORTALITY.md`, section 1](../p1-period2-invariant/RESULTS-RIGHT-FILTERED-MORTALITY.md),
dated 2026-09-01. Its `rho_k=s(2k,1)` is exactly a7's right column sampled on
the alternating centre's zero phase. The uniform exclusion `rho != 00000`
therefore supplies the infinitely-often statement a7 still labels missing.
The five-zero theorem is prior work; the result of this audit is the explicit
connection and correction of the stronger interpretation.

| Claim | Evidence |
|---|---|
| Actual alternating-centre right traces avoid five successive zero-phase zeros | `U`, prior theorem, independently replayed |
| Original a7 i.o. lemma for every `X(k,01)` | `U`, immediate implication of that prior theorem |
| Three-cell proof below, checked against unmodified `ladder.FWD[30]` | `U/C` |
| Original a7 construction agrees with unmodified ladder on the stated short regression | `C`, finite coordinate/safety validation |
| i.o. implies all-even-`q` failure or aperiodicity | **False inference**, named `T=4` torus obstruction |
| Aperiodic witness exists, or no such witness exists | Neither established |

## 1. Exact original statement and quantifiers

The original source is
[`a7_ladder_realizability/ladder_realizability.md`, section 4](../../overnight-arms/frontier_attack/a7_ladder_realizability/ladder_realizability.md):

> `col_1(t) = 1` for infinitely many `t` with `col_0(t) = 0`, in `X(k,01)`.

Here `k>=1` and `X(k,01)` is the particular unique greedy construction in
`realize.build`: initial right half zero, central seed one, initial cells
`-2k,...,-1` zero, and freely chosen deeper-left cells forcing the centre from
`T0=2k+1` onward. Phase zero uses `col_0(T0+2n)=0`. The implementation also
supports the other phase, for which one starts at the next centre-zero time.

Define, after that onset,

```text
a_n = col_1(T0+2n),
col_-1(T0+2n)   = 1-a_n,
col_-1(T0+2n+1) = 1.
```

Both identities follow from `ladder.INV[30]`. Thus the original i.o. lemma
means `a_n=1` infinitely often. Theorem B of the original source explicitly
derives `Diff_q` infinitely often for **odd** `q`, and explicitly requires an
additional analogous statement for even `q`.

For even `q=2m`, the remaining assertion is exactly

```text
a_n != a_(n-m) infinitely often.
```

Five-zero exclusion has no such implication. For example the existing
`N=7,T=4` torus with `U=0101,V=1100` has `a=10` periodically and
`col_-1=0111` periodically. It satisfies i.o., all odd-`q` differences, and
fails `Diff_4` and `Diff_420`. This is the smallest time-period certificate
among the recorded four tori, not a claim of a new exhaustive minimum search.

## 2. Compact proof of the existing five-zero theorem

At a centre-zero time, let the first five cells to its right be `(a,b,c,d,e)`.
The centre takes the values `0,1` during the next two updates. Apply the exact
Rule 30 forward function twice. Conditional on `a=0`, the first three cells
after those two updates satisfy

| Present `(a,b,c)` | Next `(a,b,c)` |
|---|---|
| `000` | first coordinate `1` |
| `001` | `010` |
| `010` | `000` |
| `011` | `00(d OR e)` |

These are exact identities for all choices of the omitted right tail. Their
verification uses the two actual update rows on five cells, shrinking to
three cells; all 16 assignments with `a=0` were checked against the imported,
unmodified `ladder.FWD[30]` by `io_verify.py`.

While `a` remains zero, the longest possible trajectory in this table is

```text
011 -> 001 -> 010 -> 000 -> first coordinate 1.
```

Choosing the other successor of `011` reaches `000` sooner. Consequently
five consecutive zero-phase samples of column 1 cannot all be zero. Time
translation applies this statement at every centre-zero phase of every
actual alternating half-plane, with arbitrary right initial data.

This proves the original i.o. lemma for `X(k,01)` for every `k`, independently
of its particular right initial data. It also bounds the gap between
zero-phase ones by five such samples. The known `T=10,N=155` torus has
`a=10000` periodically, so this bound is sharp on actual full diagrams.

The OR is essential: the saturation identities giving the displayed table
fail for Rule 90. This proof addresses recurrence of one value under a
specified alternating drive. It does not use a finite window to decide
eventual periodicity, and the sharp periodic torus explicitly demonstrates
that limitation.

## 3. Independent cell-by-cell derivation

For a separate check, suppose `a_0,...,a_4=0`, with time origin at centre
phase zero. Write `b_i=col_1(2i+1)`, `D=col_2`, `E=col_3`, `F=col_4`.

The rule at column 1 on even times gives `D(2i)=b_i`. The rule there on odd
times gives `b_i OR D(2i+1)=1`. If `b_i=1`, the rule at column 2 on even
times also gives `D(2i+1)=1`, since its left input is zero. Hence
`D(2i+1)=1` in either case, for `i=0,...,3`. The rule at column 2 on odd
times then gives `b_(i+1)=1-b_i`, for `i=0,1,2`.

Choose `i=0` or `1` with `b_i=0`, and put `u=2i`. Then

```text
D(u),...,D(u+5) = 0,1,1,1,0,1.
```

The rule at `D` forces `E(u)=E(u+4)=1`. The rule at `E` then forces
`E(u+1)=1` and `E(u+2)=0`. To obtain `E(u+4)=1` when its left input
`D(u+3)=1`, both `E(u+3)` and `F(u+3)` must be zero. To obtain
`E(u+3)=0` from `D(u+2)=1,E(u+2)=0`, one must have `F(u+2)=1`. Finally
the rule at `F` has left input `E(u+2)=0` and central input `F(u+2)=1`, so
it forces `F(u+3)=1`, a contradiction.

## 4. Machine checks actually run

`io_verify.py` imports all pre-existing engines read-only. Its JSON output is
[`io_verify.json`](io_verify.json). The completed run checked:

* All 16 five-cell assignments with first coordinate zero against the compact
  table, using unmodified `ladder.FWD[30]`.
* All 512 nine-cell right cones for each rule, comparing a shrinking-cone
  implementation using `ladder.FWD` with the existing
  `right_trace_forbidden.numeric_rho`: zero disagreements. Rule 30 has zero
  five-zero witnesses; Rule 90 has 16, first mask `0x114`.
* The prior exact ANF certificate: the four-zero indicator is nonzero, the
  five-zero Rule 30 indicator is zero, and the Rule 90 indicator is nonzero.
* The existing `T=10` torus against `torus.verify_torus`: `N=155`,
  `U=0101010101,V=1101000100`, zero-phase right word `10000`,
  `col_-1` minimal period 10. It has every tested odd difference
  `q=1,3,5,7,9`, and no `q=420` difference.
* Existing `controls.rule90_control(Tmax=6)`: all three entries satisfy the
  original bijectivity and forward-torus checks.
* Original `realize.build` at `k=1,2,3`, both phases, horizon 128, with
  independent `realize.rowsim` through time 64. At each `R=1,...,6`, the
  unmodified ladder accepts every replayed safety step, its derived columns
  agree with the construction, and the pin holds. All 36 `(k,phase,R)`
  cases pass. This short regression verifies coordinates and safety; the
  infinite claims come from the proofs, not from the horizon.

The ladder file's SHA-256 before and after was
`589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.

Reproduce from the repository root:

```sh
uv run --with numpy python experiments/rule30/ladder-rung3/io_verify.py
```

## 5. Honest scope

This closes a stale weak obligation in the a7 documentation by connecting it
to an already-proved result. It does not prove the requested aperiodic
object exists or does not exist, does not extend rung 2's set of covered
`q`, and does not prove a claim about the lone seed's eventual periodicity.

There are two independent logical gaps in the target's convergence story.
The original i.o. lemma is weaker than even-`q` failure, and absence of useful
time-periodic tori through `T=24` does not exclude useful tori with larger
time periods. Neither gap is repaired by five-zero exclusion. The remaining
all-even-shift assertion for the particular `X(k,01)` remains open here.

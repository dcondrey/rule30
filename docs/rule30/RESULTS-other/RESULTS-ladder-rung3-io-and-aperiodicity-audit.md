# R7 rung 3: the original i.o. lemma is settled; aperiodicity is not

Date: 2026-09-09.

**The literal a7 i.o. lemma follows from an existing theorem in this repo.
Neither existence nor nonexistence of the stronger aperiodic full-diagram
object was established. These are different statements.** The useful result
is a corrected reduction, exact obstructions to the proposed witnesses, and
a uniform repair of the published pinned splice.

The five-zero theorem used below was already proved on 2026-09-01 in
[`RESULTS-RIGHT-FILTERED-MORTALITY.md` §1](../../experiments/rule30/p1-period2-invariant/RESULTS-RIGHT-FILTERED-MORTALITY.md).
It is not a newly discovered theorem. This audit connects it to a7's
subsequently stale obligation and independently checks the connection.

Evidence labels follow rung 2: `U` uniform proof, `R` reduction, `C` finite
certificate, `M` measurement, `K` counterexample to a stated mechanism.

| Finding | Level |
|---|---|
| Original a7 i.o. holds for every `X(k,01)` | `U`, consequence of prior R5 |
| i.o. is weaker than nonperiodicity and than `Diff_420` | `R/K`, existing T=4 torus |
| The two documented q=420 plain lassos cannot extend one more column | `C/K`, exact pin violations |
| Pinned R=1 replacement cannot extend to a full right half-plane | `U/K`, its rho contains `00000` |
| Fibonacci and zero-interleaved Thue–Morse prescriptions fail | `C/K`, named shortest forbidden factors |
| Published literal torus splice can fail its seam pin | `C/K`, first at T=4,R=1,k=1 |
| A one-letter bridge repairs that splice for all R,k | `U`, independently checked on the original grid |
| Aperiodic full-diagram witness, or its impossibility | **Open in this audit** |

## 1. Exact primary statement and the repaired implication

The primary source is
[`a7_ladder_realizability/ladder_realizability.md` §4](../../experiments/overnight-arms/frontier_attack/a7_ladder_realizability/ladder_realizability.md),
checked against its original `realize.build` and the unmodified `ladder.py`.
It asks:

> `col_1(t)=1` for infinitely many `t` with `col_0(t)=0`, in `X(k,01)`.

`X(k,01)` is a specified diagram, with initial right half zero and centre
alternating from `T0=2k+1`. It is not an existential variable over all
alternating-centre diagrams. The primary Theorem B explicitly concludes
odd-q acceptance and explicitly asks for another statement for even q.

Choose an onset `T0` with centre-zero phase and define

```
rho_n = col_1(T0+2n),
m(T0+2n)   = 1 XOR rho_n,
m(T0+2n+1) = 1,                  where m=col_-1.
```

These equations are exactly `ladder.INV[30]`. Prior theorem R5 says every
actual alternating-centre right trace avoids `00000`. Therefore every five
consecutive rho samples contain a one. Apply this at every time after the
onset of `X(k,01)`: the literal a7 i.o. lemma follows for every k. Its
odd-q Theorem B is consequently unconditional. No new q is added to the
existing torus coverage, which already includes all odd q.

For comparison, the remaining even-q condition is exactly

```
Diff_(2h) infinitely often  <=>  rho_n != rho_(n-h) infinitely often.
```

Thus q=420 requires failure of eventual **210-periodicity** of rho.
Failure of every eventual period of m is equivalent to failure of every
eventual period of rho. Neither follows from recurrence of ones.

The smallest supplied torus separating these claims is the already verified
`N=7,T=4` example:

```
col_0=(0101)^omega, col_1=(1100)^omega,
rho=(10)^omega,    col_-1=(0111)^omega.
```

It satisfies i.o., but fails both `Diff_4` and `Diff_420`. The repaired
fixed-word splice was independently run through actual `ladder.successors`
and the accepting-SCC test: q=1 accepts; q=4 and 420 do not. This is not
merely a finite count of difference events.

## 2. Short symbolic proof of the prior local theorem

At a centre-zero time let the first five right cells be `(a,b,c,d,e)`.
The centre inputs on the next two updates are 0 and 1. Applying
`FWD[30](l,m,r)=l XOR(m OR r)` twice gives, while `a=0`,

| First right triple | Triple two time steps later |
|---|---|
| 000 | first bit is 1 |
| 001 | 010 |
| 010 | 000 |
| 011 | 00(d OR e) |

The longest path on which the first bit remains zero is

```
011 -> 001 -> 010 -> 000 -> first bit 1.
```

Hence five successive zero-phase zeros are impossible, for arbitrary
right-tail data and arbitrary starting time. The existing T=10,N=155 torus
has `rho=(10000)^omega`, so the bound is sharp on full diagrams.

This proves a bounded gap between occurrences of one under a prescribed
drive. It is not a bounded-window decision of eventual periodicity. The
sharp periodic example shows exactly why the locality filter does not turn
this result into an aperiodicity proof.

The original exact Boolean-ANF identity and its independent 512-cone check
were rerun without modification. A second implementation using
`ladder.FWD` agrees on all 512 cones for each rule. Rule 90 has a five-zero
witness at the existing mask `0x114`; the OR-dependent transition table
does not carry over. The existing rung-2 Rule 90 control was also reused,
not rebuilt.

Details and an additional cell-by-cell proof are in
[`io_report.md`](../../experiments/rule30/ladder-rung3/io_report.md).

## 3. The q=420 near-witnesses, actually extracted

Before recomputation the registered approach was to test right extension of
the documented lassos. A failed pin kills that exact extension; a forbidden
actual-right factor kills a candidate full diagram. No larger-depth census
was substituted for a proof.

`lasso_audit.py` calls the unchanged `ladder.decide` for the original two
cases and `rung1.decide_pin` for the pinned replacement. All three lassos
pass the existing independent `ladder.verify_witness`. The new audit then
checks their cyclic columns and every boundary transition.

| R,k | pin required | engine states | cycle/minimal m period | Diff_420 events per cycle | obstruction |
|---|---|---:|---:|---:|---|
| 1,1 | no | 23,592 | 424 | 2 | pin fails at cycle time 420 |
| 2,2 | no | 376,857 | 426 | 210 | pin fails at cycle time 416 |
| 1,1 | yes | 17,692 | 424 | 2 | rho begins with five zeros |

Packed letters are `(col_(R-1)<<1)|col_R`. The first failure is `1 -> 2`;
the second is `1 -> 0`. Both prescribe `(left,centre)=(0,1)` and next
centre zero at the outer boundary. For every possible next-column bit z,
`FWD[30](0,1,z)=1`, a literal contradiction. The two plain lassos therefore
cannot extend even one further column, regardless of temporal periodicity.

The pinned R=1 replacement has cycle length 424, centre `01`, and column 1
equal to `0^420 1100` on that cycle. It passes the actual pin, but its first
five even samples are `00000`. R5 excludes any full right extension, even
one with aperiodic farther columns. This is a precise failure of the
proposed near-witness mechanism, not evidence against other full witnesses.

Full prefixes and cycles are retained in the three `lasso_*q420.json` files;
the compact audit and source hashes are in
[`lasso_audit.json`](../../experiments/rule30/ladder-rung3/lasso_audit.json).

## 4. Two substitution prescriptions fail before infinite realization

The registered construction prescribed rho directly, using Fibonacci
`0->01,1->0` or the Thue–Morse bits each followed by zero. The kill condition
was a shortest forbidden factor in an exact right light cone. Source factor
sets were obtained from substitution supertiles, rather than inferred from
one sampled prefix.

| Prescription | Shortest forbidden factor | First source index | Independent exhaustive replay |
|---|---|---:|---|
| Fibonacci | 101001 | 4 | zero matches among 2,048 width-11 initial rows |
| Zero-interleaved Thue–Morse | 00000 | 9 | zero matches among 512 width-9 initial rows |

All shorter factors of these specific sources are realizable on their
finite cones. Fibonacci's shortest infeasible prefix is `0100101`, also
checked over all 8,192 width-13 rows. These forbidden words were already
in the prior right-trace report; their use here is a precise rejection of
the proposed substitutions, not a new language theorem. No claim about
all substitutions, all Sturmian words, or all possible witnesses follows.

The named obstruction is right realization, beyond the two easy constraints
`no 11` and `no 00000`: Fibonacci obeys both but contains `101001`.
Choosing an abstract aperiodic word is not enough.

See [`construction_report.md`](../../experiments/rule30/ladder-rung3/construction_report.md)
for the complete factor tests and replayable SAT/scalar controls.

## 5. A pin defect in the published splice, with a uniform repair

The original `ladder_splice.run` checks pins only inside the torus. It
omits the transition from the last seed-prefix letter into the torus.
That transition matters to `rung1.explore_pin`.

For T=4,R=1,k=1, the true seed prefix is `[2,3,0,3]` and the torus cycle
begins with 1. The seam `3 -> 1` fails the actual `pin_ok`. Across the
original four grids, R=1..12 and k=1..4, the seam fails in 50 of 192 cases
(15,13,9,13 for T=4,6,10,14). The published assertion that this identical
splice always satisfies the pin is false. The nonemptiness theorem is
repairable.

If the last prefix letter is `(a,b)` and the first tail letter is `(a',b')`,
insert the single bridge letter

```
(1-b', b*(1-a)).
```

When b=1 its right bit is `1-a`, satisfying the first pin. If the bridge's
right bit is 1, its left bit is `1-b'`, satisfying the second. Otherwise
the relevant pin is vacuous. This covers all letters.

Insert the bridge at `saturate`, after every wedge check. It changes only
a finite prefix and delays the torus tail by one letter; guessed onset
and infinite difference events are preserved. This repairs the pinned
construction uniformly in R,k and the applicable q. All 16 bridge cases
were checked against `rung1.pin_ok`, and all 192 repaired splices have no
pin failure and an actual accepting fixed-word SCC for q=1.

The exact construction, table, and SCC checks are in
[`logic_audit.md`](../../experiments/rule30/ladder-rung3/logic_audit.md).
The original engine and splice code remain unchanged, making both the
failure and repair reproducible.

## 6. What still blocks each direction

**Direction A.** The proposed finite lassos are not full-diagram witnesses,
and the two specified substitutions are not right-realizable. A successful
construction must retain compatible extensions at every spatial depth and
prove infinitely many differences at every even shift of rho. The existing
R5 theorem provides neither condition. The exact missing assertion for the
particular a7 diagram is, for every h>=1,

```
for every N, some n>=N has rho_n != rho_(n+h).
```

For the weaker single-q task, take h=210. No proof or counterexample to
that assertion for `X(k,01)` was obtained.

**Direction B.** Ruling out aperiodic rho would not refute the original i.o.
lemma: the T=4 torus satisfies i.o. with periodic rho. A nonexistence proof
would have to classify all right-realizable traces sufficiently to show
eventual periodicity, including nonconstant periodic possibilities. The
available finite forbidden-factor information does not do that. Moreover,
even a theorem that every full diagram has some eventual period does not
by itself supply one common q or a finite-depth ladder EMPTY verdict.
Those are additional uniformity and liveness obligations, detailed in the
logical audit.

Two overstatements in rung 2 must therefore be corrected. Its exact census
through T=24 does not exclude useful periodic diagrams with T>24, nor a
diagram with a periodic neighbour but no common time period for all columns.
Also, an aperiodic witness obtained by a different construction would not
prove a statement about the specific `X(k,01)`. No variant of the killed
2-times-prime prediction was attempted.

## 7. Verification, artifacts, and scope

All findings above were rechecked by the primary agent against code and
completed outputs. The original ladder, rung1, rung2, a7, and right-trace
engines were imported without edits. Their hashes are retained in the audit
outputs; the ladder SHA-256 is
`589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.

Original a7 construction replay: k=1,2,3, both phases, R=1..6; all 36
cases match derived ladder columns and satisfy every safety/pin check
tested. The finite horizon is 128, with independent row simulation through
64. Infinite recurrence comes from R5, not this regression. The unchanged
ladder/rung1/rung2 test suite reports **25 passed**. The four new audit
scripts pass `ruff check`.

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/p1-period2-invariant/right_trace_forbidden.py --max-language 7
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/ladder-rung3/io_verify.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/ladder-rung3/lasso_audit.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/ladder-rung3/logic_audit.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver python experiments/rule30/ladder-rung3/construction_substitution_probe.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with pytest python -m pytest experiments/rule30/ladder/test_ladder.py experiments/rule30/ladder/test_rung1.py experiments/rule30/ladder-rung2/test_rung2.py -q
```

This resolves the stale original i.o. obligation and identifies why it is
not the requested aperiodicity theorem. The full aperiodic-object question,
the residual all-even-q limitation theorem, and period-two exclusion remain
open. No new assertion about P1, P2, or P3 is made.

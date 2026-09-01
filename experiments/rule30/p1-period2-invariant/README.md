# Period-two same-orbit attempt: resumption sheet

Updated: 2026-09-01

Status: **OPEN.  No period-two theorem was proved.**

Target:

```text
For every nonzero finite y, Tr_0(y) != Tr_0(F^2(y)).
```

The constant-zero and constant-one cases are already proved elsewhere.  The
remaining trace is alternating; phase `1010...` reduces to `0101...` after one
application of `F`.  Proving this target would settle only the `p=2` rung of
Prize Problem 1.

## Read only this file first

The directory is intentionally flat because the scripts import one another by
filename and every raw report contains historical reproduction commands.
Preregistrations and result reports are retained unchanged as an audit trail.
Do not load them all into context.

Use this routing table:

| Need | Read/run |
|---|---|
| Exact target, `F^2`, defect, primary certificates | `RESULTS.md`; `derive_and_controls.py`; `verify_negative_certificate.py` |
| Inverse-Gray and moment hierarchy | `RESULTS-PARITY.md`; `verify_moment_negative.py` |
| Four-state operator/carry form | `RESULTS-CARRY.md`; `carry_transducer.py` |
| Run-length/boundary-gap coordinates | `RESULTS-RUNLENGTH.md`; `runlength_search.py` |
| Signed counts, touching colors, row toggle | `RESULTS-DIVERGENCE.md`; `verify_divergence_negative.py`; `toggle_phase.py` |
| Actual-right trace restrictions (`11`, `00000`) | `RESULTS-BILATERAL.md`; `RESULTS-RIGHT-FILTERED-MORTALITY.md`; `bilateral_hardcore.py`; `right_trace_forbidden.py` |
| Joint left-finite/right-realizable mortality | `PREREGISTRATION-JOINT-MORTALITY.md`; `RESULTS-JOINT-MORTALITY.md`; `joint_mortality.py` |
| Variable-seed mortality SAT and triangular correlations | `RESULTS-MORTALITY-SAT.md`; `mortality_sat.py`; `verify_drup.py`; `quadratic_probe.py` |
| Time-ordered pivot/emission audit | `RESULTS-PIVOT-EMISSION.md`; `pivot_emission_audit.py` |
| Dynamic Boolean ideal/variety trace | `RESULTS-DYNAMIC-BOOLEAN-IDEAL.md`; `ideal-variety-n4-n12.json`; `pivot_emission_audit.py` |
| Exact `n=10` plateau cofactors | `RESULTS-PLATEAU-BEZOUT.md`; `plateau_bezout.py`; `verify_plateau_bezout.py`; `plateau-bezout-n10.json` |
| Cofactor and interval-annihilator shifts | `RESULTS-COFACTOR-AUTOMATON.md`; `RESULTS-INTERVAL-ANNIHILATOR.md`; matching generators/verifiers/JSON |
| Moving-endpoint block and literal peel obstruction | `RESULTS-ENDPOINT-PEEL.md`; `endpoint_peel.py` |
| Tail density, deep-zero/core conjugacy | `RESULTS-TAIL-DENSITY.md`; `tail_density.py` |
| Start a fresh research session without rederiving history | `CONTINUATION-PROMPT.md` |
| Audit search design before interpreting a result | Matching `PREREGISTRATION*.md` only |

## Canonical exact map

Let `I` be inverse Gray code on finite bit words:

```text
I(X) = X XOR (X >> 1) XOR (X >> 2) XOR ...
```

At an even alternating-trace frontier:

```text
C = I(A OR (1 OR (B << 1)))
D = I(C OR (A << 1))
pin passes iff D & 1 = 1
(A,B) maps to (D,C).
```

Boundary-gap form:

```text
g(C)=A OR (1+zB)
g(D)=C OR zA,
g(X)=X XOR (X>>1).
```

Carry form for aligned symbol `q=(a,b)` and carry `(c,d)`:

```text
c' = c XOR (a OR b)
d' = d XOR (c OR a)
emit (d',c').
```

The four symbol actions generate `D8`, a transitive permutation group of order
eight.  The active front grows exactly one position per macrostep.

For an actual right half-plane, not an arbitrary rho boundary:

```text
rho_k=s(2k,1)
rho_(k+1)=(NOT rho_k) AND (NOT s(2k,2)) AND (NOT s(2k+1,2)),
```

so rho contains no adjacent ones.

Actual right realizability is strictly stronger.  The exact nine-cell
light-cone identity in `right_trace_forbidden.py` proves uniformly that rho
also contains no `00000`.  The realized-prefix counts are already below the
hard-core Fibonacci counts at length five.

After reversing the complete aligned word and deleting its inert leading
deep zeroes, one forced macro is exactly the active-core map

```text
v -> Transduce(v) . 3.
```

This is an all-width conjugacy, not a bounded summary.  Pin passage is final
carry `c XOR d=1`, and the next forced rho is `1 XOR c`.

## What was tried and why it stopped

| Attempt | Positive normalization | Exact kill |
|---|---|---|
| Local additive ranking | Fixed-local de Bruijn normal form | Farkas multisets for locality 1–4 |
| Modular/local quotient | Finite summaries of counts/endpoints | Same-summary, different-future collisions |
| Hasse/mixed moments | `H_k(I(X))=H_k(X) XOR H_(k+1)(X)` | Every fixed order needs the next; reachable equal-length collision |
| Carry contraction | Complete four-state subsequential transducer | All actions are permutations; no synchronizing/rejecting ideal |
| Action lookahead | Exact D8 word action | Closure fails at depths 1 and 2; further depth is horizon growth |
| Run-length digits | Lossless full boundary-gap list | Digits/list length unbounded; bounded summary collision |
| Natural gap/run ranks | Boundary count, gap excess, max gap, squares, lex orders | Each moves both ways or merely restates front growth |
| Signed left/right/contact counts | Exact tile/contact features | Two-step six-summary oscillation; 36-transition Farkas multiset |
| Odd-row toggle | Alternating OR/AND-dual rules | Two phases compose to exactly `F^2`; odd rows become cofinite |
| Hard-core rho + action | Genuine-right-half no-`11` language | Length-1/3 zero seeds share summary but have different successors |
| Variable-seed CDCL proofs | Exact mortality CNF with no free post-knee boundary | Checked finite UNSAT; proof additions and width grow sharply |
| Triangular quadratic algebra | `<Ix,Iy>=x^T K y`, `K_ij=(min(i,j)+1) mod 2` | `rank(K)=width`; 37-bit split-correlation summary has an equal-depth closure collision |
| Time-ordered kernel pivots | Exact ANF emission recurrence through three post-knee macros | `K=P^T P` is symmetric with raw diagonal `1,0,...`; a length-`n` seed starts its tail constraints at row depth `2n`; the first `n=4` post-knee pin is `1+rho_2 rho_4`, with no linear pivot |
| Dynamic Boolean ideals | Exact ANF generators and projected SAT counts for every horizon, `n=4..12` | Unit ideal reached at horizons `5,4,3,3,5,4,9,8,7`; long nonzero plateaus occur, so finite generator absorption is not immortality |
| `n=10` plateau Bezout extraction | Exact dynamic and hard-core lift cofactors in the Boolean quotient | `epsilon_8=1` already on `V_3`, `q_8=1` already on `V_5`; dynamic cofactor degree is at most 5 but support spans almost all seed positions |
| Shift-normalized cofactor automaton | Exact recurrence `C_(i+1)=C_i(1+g_i)` | Degree five fails at `n=12`; support spans the seed; the highlighted motif has a literal self-loop and is not a closed state |
| Interval annihilator | Uniform matched-extension identity on complete survivor indicators | Matched appends are exact macro shifts; an unmatched rank-five defect appears, so restart/defect states remain unclassified |
| Literal endpoint peel | Full aligned Mealy tableau and exact `K_(w+2)` endpoint block | `(n,H)->(n-1,H-2)` is semantically false: length-4 seed `0xa` survives 4, while every length-3 seed survives at most 1 |
| Coefficient-seven tail density | Exact minimum-weight falsifier and period-seven sharp control | Survives through `n=24`; phase/rho/D8 observer has a 14-edge negative cycle of total charge `-28` |
| Two-factor right-filtered mortality | Uniform right-light-cone prohibition of `00000` | **Killed:** a length-30 seed avoiding `11`/`00000` survives 10; it contains the actual-right forbidden factor `101001` |
| Exact joint mortality | Direct coupling to a genuine Rule 30 right light cone | `J(n,8)` is UNSAT through `n=31`, but finite-factor witnesses move to lengths 24 and 25; no arbitrary-`n` proof |

Do not retry the killed fixed-summary classes merely by increasing locality,
moment order, lookahead, or endpoint window.  Their standalone certificates
are uniform negatives for the stated classes.  The variable-seed UNSAT data is
different: both the hard-core and joint sweeps are finite evidence, not a
negative or a theorem.

### Translation of geometric ideas already considered

| Informal idea | Exact version tested | Present status |
|---|---|---|
| Replace touching same-color squares by a digit | Full run-length/boundary-gap sequence | Lossless but unbounded; every tested bounded collapse has an exact collision |
| Collapse pyramids to their sizes or make each pyramid an operator | Ordered gap digits and their D8 carry actions | Basic finite operator summaries do not close; an order-sensitive unbounded offset argument remains untested |
| Subtract left-side from right-side counts | Signed mass, boundary, and contact-count features | Exact oscillating transition multiset rules out a strict additive ranking in that class |
| Count by touching colors instead of rows | Adjacent equal/unequal tiles and boundary counts | Included in the same certified negative class |
| Treat each color switch or next row as a toggle | Odd-row complement and OR/AND-dual phase rules | Exact two-phase composition returns to `F^2`; it is a change of coordinates, not a descent |
| Look for oscillation or a time-varying rule | Period-two summaries and alternating phase transducers | Useful diagnostically; a two-step summary cycle falsifies monotonicity, while the original CA rule itself remains fixed |

Thus the unspent geometric version is not another scalar count.  It would
need to retain the ordered locations of all pyramid/run boundaries and prove a
well-founded spatial statement about that unbounded sequence.

## Smallest counterexamples to remember

- Rule 90 control: finite row `{-1,1}` has zero center forever.
- Rule 30 shallow-control trap: `{-8,-1,6}` alternates through time 14 and
  fails at 15.
- Natural signed summaries oscillate on
  `(2,1,1) -> (4,3,2) -> (6,5,5)` and return to their starting summary.
- Carry action closure: `(2,1,1)` and `(6,21,21)` have the same current D8
  action but different successor actions.
- Full RLE is lossless; only bounded projections are killed.  One solid OR
  run of length `m` becomes `m` unit boundary digits under inverse Gray.

## Independently checkable controls

Latest verified results:

```text
F^2 truth table                         32/32 PASS
two-orbit defect recurrence             64/64 PASS
carry local table                       16/16 PASS
carry/Gray arbitrary frontiers          34,952 PASS
moment/Hasse standalone checks          589,824 PASS
variable-seed SAT thresholds n<=16       95/95 PASS vs direct enumeration
shortest-death DRUP certificates        independently checked through n=17
triangular-correlation word pairs       87,380 PASS through width 8
moving-endpoint K block / append words      5,824 PASS through width 10
aligned endpoint tableau frontiers          34,952 PASS through width 8
Rule 30 radius-eight rows               131,071 PASS
Rule 30 adversarial trace               fail exactly at t=15
Rule 90 {-1,1}                          zero through t=128
Rule 30 rho five-zero ANF identity      zero polynomial; 512/512 PASS
Rule 90 five-zero negative control      witness right mask 0x114 PASS
active-core conjugacy                   511 reachable macros PASS
tail-density falsifier                  all hard-core seeds through n=24 PASS
local-ranking negative certificates     PASS without solver
divergence negative certificate         PASS without solver
```

Core commands:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/derive_and_controls.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_negative_certificate.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_moment_negative.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_divergence_negative.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/bilateral_hardcore.py
uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/mortality_sat.py \
  --validate --max-validate 16
uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/quadratic_probe.py
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/endpoint_peel.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/right_trace_forbidden.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/tail_density.py
```

## Best next theorem

> **Joint sixteen-zero gap theorem.**  Along an actual alternating-center
> Rule 30 right trace, the uniquely reconstructed initial left tail cannot
> contain sixteen consecutive zeros immediately after any even endpoint.

This is `J(n,8)=UNSAT` for every seed length.  The exact coupled formula is
UNSAT only through `n=31`, which is not a proof.  Approximating the genuine
right trace by all known forbidden factors does not stabilize: the first
horizon-eight finite-type witnesses move from width 36 to width 42 when the
factor cutoff moves from 18 to 24.  A proof therefore needs a coupled
layer-peeling identity or a parameterized right-language obstruction.

Why it suffices: every finite left half has an even endpoint after at most one
phase adjustment, while its rho word comes from the actual right light cone.
Sixteen forced zeros beyond that endpoint are necessary for an infinite
alternating trace.  The joint gap theorem would forbid them.  The broader
hard-core density and linear-mortality targets remain valid fallbacks if the
constant joint bound is falsified.

What a proof must retain:

- the full cumulative boundary offsets or triangular form, not finitely many
  gap/parity digits;
- the finite-left-support hypothesis (`L` eventually zero);
- actual right-side realizability (`rho` has no `11`), not an arbitrary
  half-plane;
- Rule 30's OR, with Rule 90 failing in the intended branch.

What would kill this exact bound: one length-`n` hard-core seed surviving
`2n+2` post-seed macros.  That witness would not by itself establish an
immortal seed or refute period-two mortality.

The exact endpoint formulas do **not** support a literal induction that peels
one seed macro at the cost of two continuation macros.  The length-4/length-3
survival spike is a solver-free obstruction to that semantic implication.
Any renewed endpoint induction must use a proved amortized credit or a
different induction parameter; increasing the local peel radius cannot fix
the false implication.

## Provenance policy

Every `PREREGISTRATION*.md` predates its substantive search.  Every
`RESULTS*.md` records exact commands, qualifications, and failures.  They are
kept for audit/publication but should be read only through the table above.
No `PATH.md` or publication claim should be changed unless the next result is
uniform and its controls plus an independent verifier pass.

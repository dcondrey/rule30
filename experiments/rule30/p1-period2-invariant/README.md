<!-- repo-header:start -->
<img src="https://github.com/dcondrey.png?size=160" alt="Period-two same-orbit attempt: resumption sheet logo" width="120" align="left">

<h1>Period-two same-orbit attempt: resumption sheet</h1>

<p><strong>Documentation for Period-two same-orbit attempt: resumption sheet in Rule30.</strong></p>

<br clear="left">

[![Best Practices Evidence](https://img.shields.io/badge/best%20practices-evidence%20reviewed-6a4c93?style=flat-square&labelColor=20232a)](../../../.bestpractices.json) [![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Sponsor-EA4AAA?style=flat-square&labelColor=20232a)](https://github.com/sponsors/dcondrey)
<!-- repo-header:end -->

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
| Actual-right-half no-`11` restriction | `RESULTS-BILATERAL.md`; `bilateral_hardcore.py` |
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

Do not retry these by increasing locality, moment order, lookahead, endpoint
window, seed bound, or time horizon.  The standalone certificates are uniform
negatives for their stated classes even though finite searches discovered them.

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
Rule 30 radius-eight rows               131,071 PASS
Rule 30 adversarial trace               fail exactly at t=15
Rule 90 {-1,1}                          zero through t=128
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
```

## Best next theorem

> **Hard-core isolated-pulse theorem.** If rho has no adjacent ones and its
> full forced-left reconstruction `L(rho)` is eventually zero, then rho is
> eventually periodic.

Why it suffices: `col_(-1)(2k)=NOT rho_k` and
`col_(-1)(2k+1)=1`.  Eventual periodicity of rho makes the adjacent width-two
trace eventually periodic, contradicting the recorded width-two theorem.

What a proof must retain:

- the full cumulative boundary offsets, not finitely many gap digits;
- the finite-left-support hypothesis (`L` eventually zero);
- actual right-side realizability (`rho` has no `11`), not an arbitrary
  half-plane;
- Rule 30's OR, with Rule 90 failing in the intended branch.

What would kill this target: one infinite no-`11`, aperiodic rho whose exact
forced-left reconstruction is eventually zero.  A finite prefix or a growing
survival record is not such a counterexample.

## Provenance policy

Every `PREREGISTRATION*.md` predates its substantive search.  Every
`RESULTS*.md` records exact commands, qualifications, and failures.  They are
kept for audit/publication but should be read only through the table above.
No `PATH.md` or publication claim should be changed unless the next result is
uniform and its controls plus an independent verifier pass.

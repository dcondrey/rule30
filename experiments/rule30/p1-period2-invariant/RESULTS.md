# Period-two same-orbit invariant attempt

Date: 2026-08-31

Status: **OPEN.  No period-two theorem was proved.**  The primary
de-Bruijn-normal fixed-locality additive-ranking class was falsified by exact
finite certificates, and the natural finite quotients exposed by that class
all fail closure.  This is a useful negative, not progress sufficient to
change Prize Problem 1's status.

## 1. Exact two-step rule and defect

Write

```text
a = y(i-2), b = y(i-1), c = y(i), d = y(i+1), e = y(i+2).
```

Direct substitution into `F(y)(i)=y(i-1) XOR (y(i) OR y(i+1))` gives the
radius-two rule

```text
G(y)(i) = F^2(y)(i)
        = F(y)(i-1) XOR (F(y)(i) OR F(y)(i+1)).
```

Its algebraic normal form over `GF(2)` is

```text
G(y)(i) = a XOR d XOR b*d XOR c*d
            XOR e XOR b*e XOR c*e XOR d*e XOR b*d*e XOR c*d*e.
```

Thus the initial same-orbit defect `delta(i)=y(i) XOR G(y)(i)` is

```text
delta(i) = a XOR c XOR d XOR b*d XOR c*d
             XOR e XOR b*e XOR c*e XOR d*e XOR b*d*e XOR c*d*e.
```

Both formulas were checked on all 32 radius-two neighborhoods against a
separate packed-row two-step evaluator.

More generally put

```text
D_t(i) = F^(t+2)(y)(i) XOR F^t(y)(i),  s_t(i)=F^t(y)(i).
```

The exact two-orbit defect update, exhaustively checked on all 64 assignments,
is the already-recorded identity

```text
D_(t+1)(i) = D_t(i-1) XOR D_t(i) XOR D_t(i+1)
              XOR s_t(i)*D_t(i+1) XOR s_t(i+1)*D_t(i)
              XOR D_t(i)*D_t(i+1).
```

Trace equality is exactly `D_t(0)=0` for every `t`.  Using this at two
consecutive times reduces the center equation to

```text
D_t(-1) = (1 XOR s_t(0))*D_t(1).
```

This restates the existing defect identity and is validation, not a new
lemma.

## 2. Exact alternating-phase macro constraint

The existing constant-zero and constant-one theorems leave the traces
`0101...` and `1010...`.  Applying `F` to a hypothetical `1010...` row gives a
finite nonzero `0101...` row, so it is enough to fix the latter phase.

Let `a_n=G^n(y)`.  The three consecutive center conditions

```text
a_n(0)=0,  F(a_n)(0)=1,  G(a_n)(0)=0
```

are equivalent, on all 32 radius-two neighborhoods, to

```text
a_n(0)=0,
a_n(-2)=a_n(1),
a_n(-1)=1 XOR a_n(1).
```

Therefore every stroboscopic row has one of the two four-cell center words

```text
(a_n(-2),a_n(-1),a_n(0),a_n(1)) in {1001, 0100}.
```

The value at `a_n(2)` is free.  This is stronger than merely asking for a zero
center under `G`; it retains the intermediate odd phase and uses Rule 30's OR.

## 3. Exact reverse macro transducer

The search reused, without relabeling, the alternating-fiber anti-diagonals
`(A,B)` from `RESULTS-alt-trace-fiber.md`.  After a complete zero/pin pair the
frontier length `T` is even.  Read the words from the deep end and set
`B_0=1`, `A_0=0`.  A surviving next macrostep is exactly

```text
C_(T+1)=0,  C_j XOR C_(j+1) = A_j OR B_(j-1),
D_(T+2)=0,  D_j XOR D_(j+1) = C_j OR A_(j-1),
```

with the pin condition `D_1=1`; the next frontier is `(D,C)`.  This is a
right-to-left transducer with two Boolean carry bits.  It was checked against
the original shallow-to-deep recurrence on every surviving arbitrary state
through `T=10`: 279,279 states, zero mismatches.

One exact structural lemma follows.  Let `h(X)` be the deepest occupied index
of a nonzero frontier word.  Every finite-seed post-pin state has
`h(A)>=h(B)`.  Since OR takes the union of supports and the reverse cumulative
XOR preserves the deepest occupied index,

```text
h(C) = max(h(A),h(B)+1),
h(D) = max(h(C),h(A)+1) = h(A)+1.
```

Hence `h(D)>=h(C)`, so induction applies at the next macrostep.  The active
front advances exactly one position per macrostep, while the stored word grows
by two; its deep zero margin also grows by one.  This is the structural reason
support/degree rankings do not descend: the survivor carries two balanced,
outward-moving fronts.  The equality uses OR support union and need not hold
for Rule 90, where XOR may cancel the deepest term.

## 4. Falsified certificate class

Encode the aligned frontier by the four-symbol word

```text
q_j = (A_j,B_(j-1)),  j=1..T.
```

For locality `L`, the implemented primary class assigns a weight to every
length-`L` word in `q`, sums the resulting pattern counts, and adds separate
bounded terms for the length-`L-1` prefix and suffix.  A local energy bounded
below on all finite words can be put in this normal form with nonnegative local
weights: its weighted de Bruijn graph has no negative cycle, and vertex
reweighting moves the graph potential into the two endpoint terms.  An energy
whose lower bound relies on a special reachable sublanguage is outside this
normal form and requires the secondary finite-state invariant.

For every `L=1,2,3,4`, `verify_negative_certificate.py` contains a finite
multiset of exact reachable, surviving macrotransitions such that

```text
sum endpoint-incidence changes = 0,
sum local-pattern-count changes >= 0 componentwise.
```

If an energy strictly decreased by at least one on every transition,
multiplying those inequalities by the certificate multiplicities would give

```text
0 <= summed energy change <= - summed multiplicities < 0,
```

a contradiction.  This is a complete soundness proof for the finite
certificates; coefficient magnitude is irrelevant.  The independently
executable certificate summary is:

| locality | transition types | total multiplicity | aggregate local-count gain | endpoint incidence |
|---:|---:|---:|---:|---:|
| 1 | 3 | 3 | 6 | 0 |
| 2 | 4 | 12 | 24 | 0 |
| 3 | 8 | 13 | 26 | 0 |
| 4 | 16 | 43 | 86 | 0 |

The smallest single-orbit obstruction occurs already at locality two: the
finite rho seed `1010`, between forced-continuation steps 1 and 3, returns to
the same length-one prefix/suffix summaries while changing the length-two
pattern counts only by

```text
N(00 00) += 2,  N(00 11) += 1,  N(11 00) += 1.
```

Thus no nonnegative local energy can fall over that exact segment.

Allowing signed local weights makes the sampled inequalities feasible, but
the resulting quantities are not rankings: at locality one the solution is
simply minus the word length and tends to negative infinity.  A proof that a
signed energy is bounded below only on a special reachable sublanguage would
need a separate exact finite invariant.  The secondary search looked for the
natural candidates: local-pattern counts modulo `2,3,4`, length modulo the same
modulus, and zero-, one-, or two-symbol endpoints, for localities 1 through 4.
All 36 candidates have exact transition collisions.  The first is only three
summary states deep: seeds `0` and `11` share the `L=1,m=2,e=0` summary, while
one survives and the other fails.  Each candidate was rejected by a collision
before the 256-state ceiling needed to be considered.

Finally, because the macrostep is cumulative XOR, multiplicity of `(1+x)` in
the corresponding `GF(2)` frontier polynomials was tested as the canonical
non-additive rank.  Polynomial division was checked on all 4,096 polynomials
of degree below 12.  No valuation, degree, degree-minus-valuation, or deep-zero
rank from any of the 14 nonconstant Boolean projections of `q_j` strictly
decreases on the 1,712 exact transition types.  The zero-violation degree
statistics grow outward and are diagnostics of the two-front lemma, not
well-founded descents.

## 5. Controls and exact results

- Rule 30 `{-8,-1,6}` alternates through `t=14` and fails at `t=15`, exactly as
  recorded.  No proposed invariant rejected it earlier.
- Every one of the 131,071 nonzero rows supported in `[-8,8]` was simulated
  through 64 steps.  The largest alternating horizon was 14, with witness
  `{-8,-1,6}`.  This is a preregistered falsification control only.
- On the same exhaustive sweep, the largest all-zero and all-one inclusive
  horizons were 8 and 9, reproducing the recorded sharp radius-eight values as
  bounded validation only.
- Rule 90 `{-1,1}` had zero center at all checked times `0..128`, so the
  complete period-two pipeline retains the required negative control.  The
  existing Rule 30 constant-zero theorem is the OR-dependent branch that Rule
  90 fails.
- The `F^2` rule was checked on 32/32 neighborhoods; the two-orbit defect rule
  on 64/64; the reverse macro transducer on 279,279 exact arbitrary states.
- The final standalone negative certificate passes without SciPy or a solver.

## 6. Commands run

From `/Volumes/A/researchpapers/13-rule30` unless noted:

```bash
ps aux | grep claude
cd /Volumes/A/researchpapers && git status --short --branch

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/derive_and_controls.py

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/ranking_search.py \
  --max-seed 12 --max-follow 64

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/ranking_search.py \
  --max-seed 16 --max-follow 64

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_negative_certificate.py

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/quotient_search.py \
  --max-seed 12 --max-follow 64

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/valuation_search.py \
  --max-seed 12 --max-follow 64
```

The max-seed-12 ranking run produced 1,712 distinct surviving macrotransitions
and the exact certificates above.  The max-seed-16 falsification run produced
16,066 distinct transitions and still no locality-1-through-4 de-Bruijn-normal
additive ranking.  All commands completed without a resource-limit or timeout
event; no SAT grid, Modal job, GPU, paid model call, or writing agent was used.

## 7. What remains open and the next theorem

No theorem excludes an alternating trace, so the period-two same-orbit
statement and Prize Problem 1 both remain open.  The work contributes an exact
`F^2`/phase reduction, an exact two-carry reverse macro transducer, a
front-degree growth lemma, and a checked negative certificate retiring local
additive energies and the tested modular-count quotients.  It does **not**
justify updating `PATH.md`, the attempt register, or publication documents.

The single best next theorem target is the nonlinear pin-parity statement in
the new reverse form:

> Starting from every finite rho-seed frontier, iteration of the two reverse
> cumulative-OR/XOR equations in section 3 eventually gives `D_1=0`.

That statement is exactly the existing “finite seed eventually fails a pin
check” gap, now stripped of the growing raw diagonal representation.  A proof
must control the full OR word or an unbounded hierarchy of its parity moments;
scalar local energies, endpoint summaries, support degree, and the first
`(1+x)`-adic valuation cannot do it.

The dependence on period two is explicit: there is one free zero phase followed
by one pinned phase, giving `B_0=1`, `A_0=0`, a forced first cumulative sweep,
and the single check `D_1=1`.  For a general period, multiple zero phases add
independent free inputs and the macro transducer is phase-word dependent.  No
period-uniform generalization was obtained.

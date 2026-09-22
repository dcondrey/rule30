# Audit of the cumulative-counting route

Status: **the original upper inequality, general positive-rate bounds,
finite-frontier mortality, and the resulting period-two exclusion remain
unproved.** This audit identifies limitations of the recent route and records
a new all-length obstruction to simplifying its normal forms. All frontiers
here are auxiliary reconstruction states; no singleton-seed ancestry is
asserted.

## 1. Two different quantities were being investigated

Fix an original length r and a successful chronological tape alpha, retaining
every guard. Write

```
M = 2^(2r-1),  G = |C_r(alpha)|,  D = D(alpha),
I = log2(M/G),  H = log2(G).
```

Then I+H=2r-1 exactly. The original upper conjecture is I>=D. The newer
lower-multiplicity conjecture is H>=D. These are different inequalities:
one asks how many originals survival excludes, the other how many originals
remain indistinguishable. Neither is an algebraic reformulation of the other,
and no dynamical implication between them has been established.

If both were proved, they would imply 2D<=2r-1, hence the sharper integer
bound D<=r-1. This is an elementary conditional consequence, **not** a proof
of either conjecture or the sharper bound.

The distinction was already stated in the
[BlindMind audit](RESULTS-blindmind-p1-audit.md). The present issue is allocation
of effort: the later work on merger fibers rigorously describes ambiguity
among survivors, but has not supplied its required relation to future repeats.

### A precise limitation of history-preserving encodings

Let W_r be all legal original words of length r. The original upper conjecture
is equivalent, as a finite-set cardinality assertion, to the existence of an
injection

```
C_r(alpha) x {0,1}^D  ->  W_r.
```

If an encoder transforms each input original solely by operations that
preserve its full history alpha, its output lies in C_r(alpha). For G>0 and
D>0 this cannot be injective: its domain has G*2^D elements and its output
set has only G elements. This applies to encodings made solely from the
certified E/F/T/B or later-merger rewrites whenever those rewrites preserve
the prescribed complete history.

This is **not** an impossibility result for using rewrites indirectly to
prove a lower bound. It identifies the freedom that a direct upper-bound
encoding must use: outputs can have a different scalar tape, or can fail an
intermediate guard. Only the decoded input must belong to C_r(alpha).
A decoder still has to recover both the original and all D labels. No such
encoder is constructed here.

## 2. Synchronization fixes both quantities before a possible infinite tail

The proved [synchronization theorem](RESULTS-weighted-history-endpoints.md),
section 3, gives, for |alpha|=r,

```
C_r(alpha beta) is either empty or exactly C_r(alpha).
```

All members have the same endpoint at time r. Thus along its surviving
continuation, G, I, and H are constant. Further repeats add no information
about which original was chosen and create no new original ancestors.

Writing E=D(alpha beta)-D(alpha), the two conjectures would respectively
require

```
E <= I-D(alpha),            E <= H-D(alpha).
```

This is a restatement of their remaining obligation, not a new bound on E.
The synchronized-continuation conjecture in the BlindMind audit already
isolated a weaker sufficient version of that obligation. It remains open.

Consequently, an argument intended to exclude an infinite trajectory must
account for this regime. The recent original-length-1546, 15-emission
counterexample to a two-step capacity normalization never reaches it.
Such examples are valid tests of a uniform inequality, but they do not
themselves expose the mechanism of an unbounded future at fixed r.

## 3. The recently repaired family did not require a unit rate

For the family `30111111 0^k 01`, the
[canonical merger report](RESULTS-canonical-merger-capacity.md) proves, for
every k>=0,

```
complete guarded two-step fiber size Q2 = 108,
total successful lifetime N <= 17,
total repeat count D <= 9.
```

This already establishes mortality for the whole family. It also gives

```
Q2 >= 2^(epsilon D)  whenever 0 < epsilon <= log2(108)/9.
```

The four-update, 64-choice block construction correctly repairs the
stronger unit-rate lower bound on this family. It does not repair a failure
of every positive rate: no such failure occurred in this family. Neither
the original task nor its mortality implication requires this particular
unit normalization.

The certificates themselves survived an independent read-only audit:
the complete 74-vertex/123-edge normal-form product graph, local rewrite
identities, exact spatial orbit closure, frozen-oracle bulk comparisons,
and the guarded block checks all passed. The issue is their scope, not an
identified error in those proofs.

## 4. New theorem: canonical forms retain arbitrary binary block sequences

Use the canonical irreducibility convention of the
[merger report](RESULTS-canonical-merger-capacity.md): lexicographic order
0<1<2<3 and decreasing E/F/T/B moves away from the legal origin.

**Theorem.** For every integer m>=0 and binary word b_1...b_m, set

```
B(0) = 00000,              B(1) = 10001,
phi(0) = 00000,            phi(1) = 32100,
w = 32001 B(b_1)...B(b_m).
```

Then w is an irreducible legal original of length 5+5m, its first two
guarded scalars are `01`, and

```
Z^2(w) = 32100 phi(b_1)...phi(b_m) 32.
```

In particular, at original length 5+5m there are at least 2^m distinct
canonical two-step fibers with the same first-two scalar tape `01`.

**Proof.** The normal automaton records the two bulk scans in
q=(previous_a,u,v,U,V) and a pending-pattern flag f. The legal prefix and
both blocks follow allowed transitions and return to the exact same state
(q,f)=((0,0,0,0,0),0). Their bulk outputs are:

| Input | First bulk output | Second bulk output |
|---|---|---|
| `32001` | `30310` | `32100` |
| `00000` | `00000` | `00000` |
| `10001` | `31310` | `32100` |

Both scan memories end at (0,0,0) in each row. The legal origin is admitted
only in the prefix; neither block uses an origin exception. The full
normal state, including the pending flag, resets at each boundary. Thus
concatenation preserves irreducibility, including patterns crossing block
boundaries.

The first guard succeeds with scalar 0 and appends `3`. In the second
scan this appended `3`, read from zero memory, emits `3` and leaves terminal
pair (1,1). The second guard therefore succeeds with scalar 1 and appends
`2`. This proves the displayed complete second image, with both guards
and both birth symbols retained.

Finally phi(0) and phi(1) differ and have equal length. Splitting the second
image after its five-symbol prefix recovers each binary choice. Distinct
choices therefore give distinct second images and distinct guarded
two-step fibers. This proves the assertion for every m by concatenation,
not by extrapolation from short examples.

**Scope.** The theorem makes no assertion about a third success, lifetime,
or repeat count. It proves that the finite normal automaton still carries
an unrestricted sequence of spatial choices. More precisely, the canonical
language cannot be contained in a finite union of fixed expressions

```
u_0 v_1^* u_1 ... v_t^* u_t
```

with fixed words u_i and nonempty v_i. Each expression contributes at most
(r+1)^t words of length r, since each exponent is at most r. A finite union
therefore has only polynomially many words at each length. The theorem
provides 2^m words at r=5+5m, contradicting such a bound for large m. This
includes finitely many fixed templates with a bounded number of variable
zero gaps or other periodic blocks.

A finite automaton recognizing whole words is not a finite state space for
their iterated, length-growing dynamics.

## 5. A value-separated hypothesis suggested by the update

There is a concrete asymmetry between terminal scalar values. Holding the
incoming memory and terminal low bit fixed, changing the terminal high bit
a does not affect the terminal v. The last update of u is

```
u_out = u_in XOR a       if v_out=0,
u_out = u_in XOR 1       if v_out=1.
```

For original length r>=2, toggling the last original high preserves legality.
If the first successful scalar is 0, this toggle converts the successful
guard (0,0) into the failed guard (1,0). In fact it gives an injective
one-label encoding `(w,e) -> toggle_last_high(w,e)` into W_r: the output's
terminal u recovers e, and toggling back recovers w. A nonempty first-scalar-0
class necessarily has r>=2, so the origin exception cannot occur.

If the first scalar is 1, the same toggle leaves the entire first image
unchanged. It pairs original ancestors inside every nonempty class whose
tape begins with 1, provided r>=2. These are exact one-step facts; neither
asserts cumulative independence or a new general counting bound.

Define D_00 and D_11 as the numbers of adjacent `00` and `11` pairs in the
chronological tape. A different **unproved** pair of hypotheses is

```
I >= D_00,                  H >= D_11,
```

or, equivalently,

```
G * 2^D_00 <= M,            G >= 2^D_11.
```

Their sum would give D=D_00+D_11<=2r-1 and hence the already established
conditional mortality estimate. They are jointly weaker than requiring
both full-D conjectures from section 1. Neither proposed inequality is
proved here. The terminal calculation motivates distinguishing the two
repeat values; it does not justify applying a fresh terminal-bit choice at
later, born cells. The original-ancestry issue remains essential.

This formulation also avoids requiring a unit rate: inequalities
`I>=epsilon_0*D_00-A_0` and `H>=epsilon_1*D_11-A_1`, with fixed positive
epsilons and fixed constants, would suffice after addition.

The [bounded-capacity investigation](RESULTS-bounded-capacity-language.md)
provides a useful diagnostic. Its exact six-member two-step fiber has a
tape with twelve repeats, but ten are `00` and only two are `11`. Thus
that particular witness does not violate the restricted inequality
`Q_2>=2^D_11`. However, the restricted version is **false** for another
already certified member of the small-capacity language:

```
r = 87,       first two scalars = 00,
Z^2(w) = 303 (13)^42 03,
successful tape prefix = 001001111,
Q_2 = 6,      D_00 = 2,      D_11 = 3.
```

The complete guarded language classification proves there are exactly six
original ancestors of this second image; its stored exact spatial-cycle
certificate verifies the subsequent tape. Thus 6<2^3 refutes the restricted
version without dropping ancestry or an intermediate guard. This does not
refute the proposal for G, which counts originals in all second images that
realize the complete tape. It prevents another silent restriction to one
merger component.

Follow-up: the [split-encoder obstruction](RESULTS-split-encoder-obstruction.md)
refutes the proposed independent-original-high-bit hypercube directly at
this r=87 example and identifies the missing ancestry of toggled birth bits.
It also proves a coordinated three-update block construction giving at
least `6*4^20` global ancestors of this tape. That positive construction
does not establish a cumulative repeat rate.

## 6. A concrete small-capacity problem, with counting already solved

The bounded-capacity investigation also proves a complete all-length
classification of every guarded two-step fiber of size at most eight.
For one remaining family,

```
w_k = 20001 0^(2k),
Z^2(w_k) = 21213 (13)^k 03,
E_2 = {20001,20020,20021,21001,21020,21021} 0^(2k).
```

The count is exactly six for every k; both initial scalars are 0. The
future temporal problem remains open despite this complete description of
the original fiber. At k=30500, independent replay gives 21 successes,
twelve repeats, and then failure. An attempted all-k orbit closure stops
at its explicit period cap; no all-k conclusion is inferred for this family.

This separates two obligations sharply: ancestry construction and counting
are finished for this family, while its uniform future-repeat bound is not.
It is a concrete test for a qualitative bound `D<=B(Q_2)`, if that route is
retained. Such a bound need not have logarithmic growth. It is sufficient
for mortality but is stronger than mortality alone, since it must be uniform
over unbounded original lengths with the same Q_2.

The diagnostic must count repeats, not demand a lifetime cutoff independent
of k. If this family had D<=B for all k, the known repeat inequality would
already give

```
N <= 2^(B+1)(r+2)-r-1,       r=2k+5.
```

This sufficient bound depends on k. Thus unbounded lifetimes as k varies
would not by themselves refute a uniform repeat bound. Similarly, an
infinite path through nested dyadic residue classes need not correspond to
an ordinary finite k, and need not have unbounded repeat count.

A concrete next test is an exact recurrence for residual parameter families
`k=a+2^m*j`, retaining the actual guards and last scalar, with transition
weights equal to newly emitted repeats. If a finite set of residual types
can be proved closed at all depths, a reachable graph with no positive-weight
cycle supplies a bound on repeats. A positive-weight cycle refutes the
uniform-repeat hypothesis only when arbitrarily many traversals are proved
to lift to actual guarded residual families containing ordinary finite k.
An overapproximation or a graph fitted to the stored finite layers cannot
certify that refutation. Establishing finite closure itself is an open proof
obligation, not an available theorem.

Success on this family alone would not give B(6) for every size-six fiber;
the other classified families must also be handled. General mortality would
still require an argument for every capacity, or a bound on the complete
original history classes.

## 7. Exact verifiers

```
uv run --no-project python experiments/rule30/canonical_binary_blocks.py
```

Files:

- [Verifier](../../experiments/rule30/canonical_binary_blocks.py)
- [Certificate](../../experiments/rule30/canonical-binary-blocks.json)

The verifier stores all 15 local normal transitions, independently checks
the six bulk scans using the frozen `panel/cert33.py`, and checks seven
short guarded concatenations as controls. The all-length proof is the
local reset and concatenation argument above. It completed in under a
second with a 10-second wall cap. Source hashes and explicit scope flags
are saved. No old census, GPU work, paid compute, seed regeneration, or
BlindMind rerun was used.

The counting distinctions, synchronization consequence, and fixed-family
scope analysis above are algebraic deductions from previously proved
statements. They do not constitute a new mortality theorem.

The bounded-capacity report links its separate exact language verifier,
completed companion-family proof, six-ancestor witness, and explicitly
unfinished spatial-cycle certificate.

The value-separated audit is reproducible with

```
uv run --no-project python experiments/rule30/repeat_value_budget_audit.py
```

Its [verifier](../../experiments/rule30/repeat_value_budget_audit.py) and
[artifact](../../experiments/rule30/repeat-value-budget-audit.json) check all
32 local terminal-toggle cases and postprocess 121 previously certified
residue tapes from the two family artifacts. They retain the restricted
counterexample, repeat counts separated by value, and source hashes. They
compute no new trajectories, spatial orbits, original census, or ancestor
counts. The complete-G hypotheses remain explicitly unproved and unrefuted.

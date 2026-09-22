# R7 residual q=420: T=26 is empty; periodic neighbours through period 30 classified

Date: 2026-09-09.

**The q=420 gap remains open.** The requested unmodified T=26 census is
negative, with zero undecided candidates. T=28 and T=30 add no periods.
The stronger result is a classification that does not assume a common time
period for the diagram: **if the neighbour of an eventually alternating
centre is eventually periodic with minimal period p<=30, then
p is one of {4,6,10,14}.** All four possibilities have existing torus
witnesses, and all four divide 420.

This reads the [rung-3 audit](RESULTS-ladder-rung3-io-and-aperiodicity-audit.md)
as superseding the older rung-2 claims about aperiodicity and the splice.
There is no restored prime-pattern prediction and no enumeration beyond T=30.

| Finding | Evidence |
|---|---|
| T=26: no alternating-centre torus | `C`, unmodified resolver, no undecided candidates |
| T=28 and T=30: only repeats of existing tori | `C`, exhaustive candidates plus right-cone certificates |
| Eventual neighbour periods p<=30 are exactly {4,6,10,14}, without a common-period assumption | `C` finite classification, `R/U` transfer to arbitrary full diagrams and onsets |
| Every nonconstant eventual neighbour period is even | `U`, OR-dependent odd-phase identity |
| First pin count and redundancy of later leftward pin tests | `U`, explicit OR identities |
| Period-22 and period-26 prescriptions | `K/C`, named forbidden right-cone prefixes |
| Classification at all periods; q=420 witness or impossibility | **Open** |

## 1. Registration and exact census

[REGISTRATION-Q420.md](../../experiments/rule30/ladder-rung2/REGISTRATION-Q420.md)
records the approach and kill conditions. The initial T=26 approach was
also stated before launching the original resolver: all 2^26 right-column
words; threshold=3; K=20000; lambda cap=2000000. A useful torus must have
minimal neighbour period not dividing 420 and pass the forward rule and
the unmodified ladder. Zero useful cycles with zero undecided candidates
kill this T, not the entire route.

All counts below fix `col_0=0101...`. They count column-pair presentations,
not spatial/temporal rotation classes of tori. The other centre phase is
obtained by a time shift. The period filter removes only p<=2.

| T | all V enumerated | candidates p>=3 | pin-dead | on-cycle | off-cycle | undecided | on-cycle neighbour periods |
|---:|---:|---:|---:|---:|---:|---:|---|
| 26 | 67,108,864 | 67,092,480 | 67,006,030 | 0 | 86,450 | 0 | none |
| 28 | 268,435,456 | 268,402,688 | 268,190,586 | 9 | 212,093 | 0 | 2 at p=4; 7 at p=14 |
| 30 | 1,073,741,824 | 1,073,676,288 | 1,073,157,442 | 8 | 518,838 | 0 | 3 at p=6; 5 at p=10 |

The four outcome classes sum exactly to the eligible candidate count.
All 17 positive presentations at T=28,30 were reconstructed and checked
cell by cell against the forward rule. They are temporal repeats/time
shifts of the existing four certificates, not new witnesses.

**The last two rows were not decided by pretending a timeout is negative.**
The bounded-memory orbit adapter initially reported:

| T | on-cycle | off-cycle by closed orbit | undecided at K=20000, lambda<=2000000 |
|---:|---:|---:|---:|
| 28 | 9 | 180,901 | 31,192 |
| 30 | 8 | 103,128 | 415,710 |

Those outputs remain in `resolve30-28.json` and `resolve30-30.json`.
Section 4 explains the independent certificate resolution producing
`resolve30-{26,28,30}-certified.json`, from which the complete table is taken.
Transient lengths and eventual spatial cycle lengths of the formerly
undecided candidates were not computed.

## 2. What the OR/pin actually does

For a cyclic pair `(A,B)`, write

```
W = rot(A) XOR (A OR B),       L(A,B) = (W,A).
pin(A,B): B AND NOT(A XOR rot(B)) = 0.
```

Every leftward image satisfies its pin identically:

```
A AND NOT(W XOR rot(A)) = A AND NOT(A OR B) = 0.
```

Thus all pin deaths in this census occur at the starting pair. The later
pin checks in the frozen resolver are redundant. Passing that first pin
does not put the pair on a cycle: the obstruction is compatibility of
arbitrarily deep right extensions, not a later pin failure along L.

There is also an exact count. Let T=2h, `a_i=V(2i)`, `b_i=V(2i+1)`.
Against centre 01, the pin says `a_i=1 => b_i=1` and
`b_i=1 => a_(i+1)=0`. The numbers of choices of b for transitions of a are

```
M = [[2,1], [1,0]].
```

The number of pin-passing cyclic V is `trace(M^h)`, where
`s_0=s_1=2` and `s_h=2s_(h-1)+s_(h-2)`. Removing p<=2 leaves
`s_h-2^h` survivors. The eligible count before the pin is
`4^h-2^(h+1)`. Both formulas agree exactly with the three census rows.

The first leftward image `(W,U)` forgets the odd-time bits of V. Equal
first images have identical later orbits. Grouping them reduces the
212,102 pin survivors at T=28 to 842 distinct first images, and the
518,846 at T=30 to 1,363. The adapter retains the root-to-image map and
checks each original root's membership in its own eventual cycle; it
does not confuse a transient with a cycle member.

This explains a large part of the sparsity and permits an exact, much
cheaper implementation of the existing test. It does not, by itself,
explain the terminal set of achievable periods.

For Rule 90 there is no such OR pin: the existing `controls.rule90_control`
is reused unchanged and passes at T=2,4,6. Its leftward map is bijective.
The Rule 30 obstruction is not imposed on that control.

## 3. Removing the common-time-period assumption

Choose an onset T0 with centre-zero phase and write

```
rho_n = col_1(T0+2n),
m(T0+2n) = 1 XOR rho_n,       m(T0+2n+1) = 1.
```

If a nonconstant eventual period of m were odd, shifting by it would
carry every even position to an odd position and force m identically one.
The resulting rho identically zero is excluded by the existing five-zero
theorem. Constant rho one is excluded by the existing `11` obstruction.
Consequently the minimal eventual period of m is `2h`, where h is the
minimal eventual period of rho.

For each h<=15, enumerate primitive binary words modulo cyclic rotation.
There are 4,720 such necklaces altogether. Recompute the actual right
language through length 10 with the unchanged `right_trace_forbidden.py`;
its forbidden factors eliminate 4,692 necklaces. Four surviving necklaces
are realized by the existing forward-verified tori. The remaining 24 are
all killed by finite exact right light cones:

| primitive rho period h | necklaces | killed by frozen factors | killed by further cones | realized |
|---:|---:|---:|---:|---:|
| 1 | 2 | 2 | 0 | 0 |
| 2 | 1 | 0 | 0 | 1 |
| 3 | 2 | 1 | 0 | 1 |
| 4 | 3 | 2 | 1 | 0 |
| 5 | 6 | 5 | 0 | 1 |
| 6 | 9 | 9 | 0 | 0 |
| 7 | 18 | 17 | 0 | 1 |
| 8 | 30 | 29 | 1 | 0 |
| 9 | 56 | 55 | 1 | 0 |
| 10 | 99 | 98 | 1 | 0 |
| 11 | 186 | 183 | 3 | 0 |
| 12 | 335 | 332 | 3 | 0 |
| 13 | 630 | 627 | 3 | 0 |
| 14 | 1,161 | 1,156 | 5 | 0 |
| 15 | 2,182 | 2,176 | 6 | 0 |

The four realized rho necklaces are `01`, `001`, `00001`, `0000101`.
Their respective m-periods are 4,6,10,14.

Each cone prescribes only rho at centre-zero times. All initial right
cells are free; the centre drive is alternating; no spatial wrap, temporal
wrap, or periodic farther column is imposed. A word of length n uses exactly
2n-1 initial cells and the forward evolution through time 2n-2. Hence a
forbidden prefix excludes the periodic word in *every* full diagram. The
same prefix occurs arbitrarily late in an eventually periodic tail, so the
argument also covers eventual periodicity and arbitrary onsets.

The shortest infeasible prefixes at the canonical necklace phase include:

| m-period | rho necklace | first infeasible prefix length |
|---:|---|---:|
| 8 | `0001` | 32 |
| 16 | `00001001` | 32 |
| 22 | `00001000101` | 31 |
| 22 | `00001001001` | 30 |
| 22 | `00001010001` | 22 |
| 26 | `0000100001001` | 39 |
| 26 | `0000100010001` | 22 |
| 26 | `0000101010001` | 46 |

For example, the last obstruction is the first 46 symbols of
`(0000101010001)^omega`; its 91-cell initial light cone is UNSAT.
The preceding 45-symbol prefix is SAT and its decoded initial row is
replayed by the unchanged `numeric_rho`. These are shortest prefixes at
the stated phase, not claims of globally shortest forbidden factors.

This answers why 2x11 and 2x13 fail within the bounded classification:
every possible periodic neighbour word has an explicit right-realizability
obstruction. It is stronger than requiring avoidance of `11` and `00000`.
It is not yet a structural characterization for arbitrary h.

The phrase “incommensurate periods” needs care: integer periods of any
finite set of columns always have an lcm. The meaningful relaxation is
absence of a uniform time period for infinitely many columns. These
certificates cover that relaxation for neighbour period p<=30, even if
the farther columns themselves are aperiodic.

## 4. Resolving the capped orbit candidates without longer orbits

If `(U,V)` belongs to an L-cycle, the cycle gives a genuine full torus.
Its periodic rho must therefore survive section 3. For every other rho,
the finite cone obstruction proves the root is off-cycle.

For each of the four surviving rho necklaces, an existing torus provides
a cycle pair `(U,V*)`. All candidates with this same rho have the same
first image `(W,U)`. A finite functional graph has exactly one predecessor
*on its cycle* at each cycle vertex. Therefore V* is the only on-cycle
candidate with that first image; all other V are transient.

`resolve_by_cones.py` re-enumerates every V, checks every distinct first
image against these two alternatives, and retains the complete class
counts and certificate references:

| T | off-cycle by forbidden rho | off-cycle by wrong predecessor of a known cycle |
|---:|---:|---:|
| 26 | 86,450 | 0 |
| 28 | 211,652 | 441 |
| 30 | 516,190 | 2,648 |

There is no unclassified first image. The zero-undecided final census is
thus a certificate conclusion, not an increased orbit timeout.

## 5. Verification and artifacts

The primary cone queries import the existing rung-3 Z3 implementation.
Every additional UNSAT result is independently encoded using the scalar
Rule 30 truth table, solved by Glucose, and accompanied by a DRUP proof.
The existing `verify_drup.py` checks every proof addition by reverse unit
propagation. All 24 proofs pass, with 34,810 checked additions in total;
the persisted DIMACS/proof files are parsed and checked again when resolving
the census. CNF and proof hashes are retained.

The independent CNF encoding agrees with the unchanged exact right-language
enumerator on all 254 binary words of lengths 1..7; every SAT model is
replayed with `numeric_rho`. The batched resolver matches the frozen
resolver on 21 small cases, including deliberately insufficient caps, and
matches the saved complete T=22,24,26 censuses. The frozen ladder/rung1/rung2
suite passes **25 tests**. All four new Python scripts pass Ruff.

No original engine was edited. In particular the ladder SHA-256 remains
`589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.
The existing witnesses' engine acceptance and the uniform bridge repair
remain those verified in rung 3; no new accepting q=420 witness is claimed.

Artifacts are in [`experiments/rule30/ladder-rung2/`](../../experiments/rule30/ladder-rung2/):

- `resolve30-26.json`: original engine output.
- `resolve30-{28,30}.json`: honest capped orbit outputs, including undecided counts.
- `resolve30-{26,28,30}-certified.json`: complete classifications and first-image evidence.
- `periodic-neighbor-results.json`: all necklace counts, forbidden prefixes, feasible predecessors, controls, and hashes.
- `periodic-neighbor-certificates/`: 24 DIMACS/DRUP certificate pairs.
- `residual-verification.json`: independent encoding, resolver, count, and forward-rule checks.

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/ladder-rung2/resolve.py -T 26 -K 20000 --lam 2000000 --json experiments/rule30/ladder-rung2/resolve30-26.json
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/ladder-rung2/resolve_batched.py -T 28 --json experiments/rule30/ladder-rung2/resolve30-28.json
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/ladder-rung2/resolve_batched.py -T 30 --json experiments/rule30/ladder-rung2/resolve30-30.json
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver --with python-sat python experiments/rule30/ladder-rung2/periodic_neighbor_probe.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver --with python-sat python experiments/rule30/ladder-rung2/resolve_by_cones.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver --with python-sat python experiments/rule30/ladder-rung2/verify_residual.py
```

## 6. Honest scope

The result excludes every useful eventual neighbour period p<=30, even in
a full diagram with no common time period. Odd nonconstant neighbour
periods are excluded altogether. It does **not** exclude useful even
periods p>=32, or an aperiodic neighbour that fails eventual 420-periodicity.
No global terminal-period theorem has been proved.

A finite forbidden cone is used only to reject a specified periodic word.
There is no fixed-radius criterion for eventual periodicity, no claim that
the recorded forbidden factors present the entire right-trace language,
and no stabilization inference from the finite census. The original
aperiodic constructions already killed in rung 3 were not retried.

Every period of a T=28 or T=30 torus divides 420 anyway; those rows extend
the census and test the apparent period set, rather than offering a direct
q=420 escape. Larger-period work requires a structural theorem or torus
constraint solving, not continuation of this 2^T enumeration. R7's residual
q=420 gap, the all-period classification, and the aperiodic construction
remain open. No assertion about P1, P2, or P3 follows.

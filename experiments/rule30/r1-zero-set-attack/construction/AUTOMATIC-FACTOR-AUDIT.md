# Exact fixed-orbit automatic-factor synthesis

Date: 2026-09-09. Evidence: **U** for the finite carry construction and
the conditional implication of a factor model; **C** for the indicated
finite lookup exclusions; **R** for the remaining construction problem.
This is an intermediate R1 attack, not an R1 proof or counterexample.

## Mechanism and success condition

Let `z(t,x)` be the lone-seed Rule 90 diagram. The first candidate class is

```
s(t,x) = g(t mod 4, x mod 14, z(t,x-R),...,z(t,x+R)).
```

The lookup is unknown. Its local Rule 30 equation is imposed on every
context that actually occurs anywhere on this fixed Rule 90 orbit. The
centre is required to equal an unknown period-4 clock for every `t>=1`;
the clock at phase 3 is zero. At `x=1,t=3 mod 4`, the output is required
to copy or complement `z(t,1)`, with one common polarity. The earlier
radius-2 and radius-3 runs allowed only copy; the radius-4 run permits
both polarities in a single CNF.

A satisfying lookup would be a full diagram, because the gate context
set is complete for all times and sites. It would kill the stated
generic R1 obligation: `z(t,1)=1` exactly at `t=2^j-1`, so on phase 3
there are infinitely many ones separated by unbounded gaps. Its
complement is also not eventually periodic. A sequence periodic on all
centre-zero times would be periodic on this phase-3 subsequence, which
is impossible. This implication concerns an arbitrary explicitly
constructed Rule 30 diagram; it would not identify that diagram with
the Rule 30 lone-seed orbit.

The finite stopping condition is UNSAT for the chosen lookup class.
UNSAT at a tested radius supplies no exclusion at larger radius, another
clock, or another source automaton.

## Exact context closure (U, instantiated by C)

Write

```
P(a,b) = [a>=0 and b>=0 and (a & b)=0].
z(t,x) = P((t+x)/2,(t-x)/2)  if t+x is even; otherwise 0.
```

For a context of radius `K`, every nonzero context has an anchor offset
`j in [-K,K]` with `z(t,x+j)=1`. Put

```
u=(t+x+j)/2, v=(t-x-j)/2.
t=u+v, x=u-v-j, u>=0, v>=0, u&v=0.
```

Its bit at offset `k` is zero when `k-j` is odd, and otherwise is
`P(u+d,v-d)` with `d=(k-j)/2`. Thus all nonzero contexts can be generated
from the disjoint digit pairs `(u_i,v_i) in {00,10,01}`. All-zero
contexts occur at every clock phase and spatial class by taking the
site sufficiently far outside the light cone.

The LSD carry automaton keeps, for every `d in [-K,K]`, the two signed
carries initially `(d,-d)` and whether an overlapping pair of one bits
has already occurred. Reading `(a,b)` sends carries `(c,e)` to
`(floor((a+c)/2),floor((b+e)/2))` and records overlap of their emitted
low bits. It also retains `u mod M`, `v mod M`, and `2^i mod M`, where
`M=lcm(T,q)`. Carries range over a fixed finite interval; all other
state components are finite. The BFS runs to transition closure.

Every reached state is a possible finite input. To terminate it, pad
with `00` until carries are fixed at `0` or `-1`; a shifted predicate
is one exactly when both carries are zero and no overlap occurred.
Requiring both carries zero is essential: overlap flags alone would
incorrectly accept a negative argument such as `P(-1,0)`.

This construction is sound because every terminal state has a finite
integer representative; it is complete because every finite disjoint
pair is an input path. The code checks every resulting feature vector
against integer arithmetic and every retained context against the
Lucas formula. Closure, rather than these representative checks,
establishes the all-time quantifier.

The actual centre and neighbour pattern sets are computed separately.
At a fixed site `x`, write `t=2n+epsilon`; a parity-compatible offset
`k` has value

```
P(n+(epsilon+x+k)/2,n+(epsilon-x-k)/2).
```

The same carry mechanism now reads one digit of `n` into both
arguments. A nonzero-input flag allows exactly `t=0` to be omitted for
the centre. Only patterns occurring at the actual sites `x=0` and
`x=1` receive observation pins. Spatial classes congruent to those
sites do not receive additional observation assumptions.

Implementation: `r90_exact_contexts.py`. An independent agent audited
signed carries, terminal signs, coordinate residues, offsets, and the
fixed-column construction. Its independent direct row evolution through
time 511 found exactly the closure's context sets at radii 1 through 5,
with counts `154,238,329,434,560`; this is a diagnostic cross-check,
not the completeness proof.

## Exact ordinary-factor results (C)

| Factor radius | Polarity | Lookup variables | Total variables | Rule contexts | CNF clauses | Result |
|---:|---|---:|---:|---:|---:|---|
| 2 | Copy | 238 | 242 | 329 | 2,649 | UNSAT, DRAT verified |
| 3 | Copy | 329 | 333 | 434 | 3,491 | UNSAT, DRAT verified |
| 4 | Copy or complement | 434 | 439 | 560 | 4,507 | UNSAT, DRAT verified |

The context automata for the three rows have respectively
`3,652 / 10,956`, `6,142 / 18,426`, and `7,490 / 22,470`
states/transitions. Every state has exactly three outgoing digit
transitions. The centre pattern counts are `7,8,9`; neighbour pattern
counts across all four phases are `9,10,12`.

Radius-4 UNSAT also excludes smaller radii with free polarity: a smaller
lookup can be lifted to radius 4 by ignoring its outer input bits. This
is an inclusion of finite classes, not an extrapolation to larger radii.

For the radius-4 instance, grouping each local Rule 30 gate and each
observation constraint separately gives 574 groups. An initial SAT core
had 189 groups; deletion yielded an inclusion-minimal core of 117 groups
and 851 clauses. Every single-group deletion is SAT, and the retained
core has its own checked DRAT refutation. It contains 103 rule gates
and all 14 observation groups: all nine actual centre-pattern pins,
the zero-clock-phase pin, and all four neighbour-pattern/polarity pins.
No claim of minimum cardinality is made. This core did not expose an
immediate one-pin inconsistency or a proved radius-independent cause.

Files: `exact_orbit_factor_synthesis.py`,
`exact-orbit-factor-R*-T4-q14*.json`,
`exact_factor_pin_core.py`, `R4-T4-q14-minimal-group-core.json`, and
`exact-orbit-factor-certificates/`. JSON records include artifact hashes.

## A distinct two-scale class (U definition, C exclusion)

The second class reads the coarser diagram:

```
s(t,x) = g(t mod 4, x mod 14,
           z(floor(t/2), floor(x/2)-R),...,
           z(floor(t/2), floor(x/2)+R)).
```

This is not an ordinary larger-radius factor of the same-time row. Let
`n=floor(t/2),m=floor(x/2)`. Source contexts of coarse radius `R+1`
and clocks `(n mod 2,m mod 7)` suffice. For the spatial left gate the
coarse centre shifts to `m-1` exactly when `x` is even; for the right
gate it shifts to `m+1` exactly when `x` is odd. The next-time coarse
row is unchanged when `t` is even and evolves by Rule 90 when `t` is
odd. Thus its next window is the XOR of the two neighbouring source
windows. Each coarse context and all four microphase pairs are
enumerated exactly.

The centre is pinned from `t>=2` using the actual coarse centre patterns
at `n>=1`. At fine phase 3 and site 1, the required fine Rule 90 bit is
the XOR of the coarse central and right bits; polarity remains free.

| Coarse radius | Lookup variables | Total variables | Fine Rule contexts | CNF clauses | Result |
|---:|---:|---:|---:|---:|---|
| 1 | 252 | 257 | 448 | 3,153 | UNSAT, DRAT verified |
| 2 | 448 | 453 | 728 | 5,173 | UNSAT, DRAT verified |

These derive from respectively 112 and 182 exact coarse contexts. The
carry automata have `2,047 / 6,141` and `3,211 / 9,633`
states/transitions. The actual coarse centre has three and four patterns.

Files: `coarse_orbit_factor_synthesis.py`,
`coarse-orbit-factor-R{1,2}-T4-q14.json`, and
`coarse-orbit-factor-certificates/`.

## Rule 90 controls (C)

For every ordinary-factor instance, changing only the target rule from
30 to 90 admits the explicit identity lookup (central source bit), an
all-zero centre clock, and copy polarity. It satisfies every CNF clause
and every exact context gate. For every two-scale instance the explicit
control reconstructs the fine Rule 90 diagram using

```
z(2n,2m)=z(n,m),
z(2n+1,2m+1)=z(n,m) XOR z(n,m+1),
z(t,x)=0 when t and x have opposite parity.
```

It likewise satisfies every exact gate and observation. Each control
also passes direct forward checks on times `0..127`, sites `-256..256`.
The finished constraints therefore do not produce a Rule 90 exclusion.

The unchanged `controls.rule90_control(6)` was separately run: at
`T=2,4,6`, all `L90_bijective` and `torus_ok` checks pass. Output:
`automatic-factor-unchanged-rule90-control.json`. The unchanged source
SHA-256 is
`3e5da3ab9db71aaccc44cefda80cb5f08f780b3ae3fb11bff78f98d5efd3301a`.

## Reproduction

The programs preserve previous outputs by refusing to overwrite them.
Run in a fresh directory, copying these four source files:

```sh
task_dir=$(mktemp -d /tmp/rule30-automatic-factor.XXXXXX)
cp experiments/rule30/r1-zero-set-attack/construction/{r90_exact_contexts,exact_orbit_factor_synthesis,exact_factor_pin_core,coarse_orbit_factor_synthesis}.py "$task_dir/"
cd "$task_dir"
uv run --with python-sat python exact_orbit_factor_synthesis.py --radius 2
uv run --with python-sat python exact_orbit_factor_synthesis.py --radius 3
uv run --with python-sat python exact_orbit_factor_synthesis.py --radius 4 --free-polarity
uv run --with python-sat python exact_factor_pin_core.py
uv run --with python-sat python coarse_orbit_factor_synthesis.py --radius 1
uv run --with python-sat python coarse_orbit_factor_synthesis.py --radius 2
```

The proof checker is DRAT-trim, located by
`experiments/rule30/r1-isolated-column/drat_trim.py`: `$RULE30_DRAT_TRIM`,
then `/tmp/rule30-family-seam-drat-trim/drat-trim`, then `drat-trim` on
`PATH`; `docs/rule30/RESULTS-family-seam.md` gives the pinned build
recipe. Each UNSAT run checks its proof and records its CNF,
proof, and checker log. Routine runtimes are under one second per
listed instance on the current environment; the solver timeout is 60
seconds.

## Scope and unresolved step

Established: exact all-time source-context sets and certified exclusion
of the specified finite lookups. Not established: exclusion of all
automatic Rule 30 diagrams, all radii/scales/clocks, all diagrams with
periodic centre, R1, or P1. No SAT prefix is promoted to an infinite
construction. No predictor from bounded centre history is proposed;
the bounded lookup reads an auxiliary full Rule 90 diagram instead.

The obstruction is the **fixed-orbit factor gate incompatibility** at
the listed parameters. The exact step that fails is simultaneous
satisfaction of the Rule 30 update gates, periodic-centre pins, and
sparse aperiodic-neighbour pins. The core is an exact finite witness to
that failure. Whether it reflects a structural obstruction extending
beyond these classes remains unresolved. Further clock choices are a
separate live direction, not ruled out by this computation.

Subsequent strengthening: [DYADIC-RESET-OBSTRUCTION.md](DYADIC-RESET-OBSTRUCTION.md)
proves a uniform exclusion of the stated q14/T4 Rule 90 source
copy-or-complement mechanism at every radius, using complete preimage
sets rather than extrapolating this SAT table. It still does not exclude
other sources or all observation functions.

# Exact Rule 150 source label quotient for the R1 kill predicate

Date: 2026-09-09. Evidence: **U** for the context/label reductions;
**C** for the listed SAT exclusions; **R** for the remaining factor
construction problem. No R1 proof or counterexample is claimed.

## Mechanism

Let `z` be the lone-seed Rule 150 diagram and consider the unknown lookup

```
s(t,x)=g(t mod T,x mod q,z(t,x-R),...,z(t,x+R)).
```

This source escapes the earlier Rule 90 dyadic reset obstruction:
`z(2^n,x)` retains its central seed. The aim is an exact Rule 30 factor
with an eventually periodic centre and a neighbour aperiodic on its
zero set. Both the all-time update equation and that observation
predicate have finite exact encodings. A SAT result would give an
actual full diagram; the present listed results are all UNSAT.

## Exact context closure (U)

Rule 150 is additive, with polynomial `X^-1+1+X`. Squaring over `F_2`
gives the binary identities

```
z(2t,2x)=z(t,x),             z(2t,2x+1)=0,
z(2t+1,2x)=z(t,x),           z(2t+1,2x+1)=z(t,x) XOR z(t,x+1).
```

For every radius `W>=1`, the fine window centred at
`(2t+e_t,2x+e_x)` is determined by a coarse window of the same radius.
Start with all time-zero windows: one seed-containing pattern for
centres `x=-W,...,W`, plus the zero pattern at every spatial clock
class. Close the finite states `(t mod T,x mod q,window)` under all
four binary lifts. Every transition maps a real context to a real
context. Every real context is obtained by repeatedly halving its time
until time zero, with integer floor division also handling negative
spatial coordinates. Thus transition closure is complete for every
time and site.

At the fixed centre, close only the spatial-bit-zero transitions;
the fixed site-1 patterns are the spatial-bit-one lifts of these states.
The implementation is `additive_exact_contexts.py`. Every state retains
an actual coordinate witness. Independent direct XOR row evolution
through time 511 reproduces all global and fixed-column pattern sets
at radii 1 through 4; its global Rule 150 counts are
`217,364,560,812`. The same independent check with the Rule 90 lift
gives `154,238,329,434`, agreeing with the earlier carry construction.
These finite replays check the implementation; binary descent proves
the all-time quantifier.

## The complete observation quotient (U)

Let `u_n=z(n,1)`. The centre is always 1, and the binary identities give

```
u_(2n)=0, u_(2n+1)=1 XOR u_n,
u_n=v2(n+1) mod 2.
```

For every odd positive `d` and residue `j`, the subsequence `u_(dm+j)`
is not eventually periodic. If it had eventual period `P`, write
`a=v2(P)`. Choose `k>a` of the opposite parity to `a`. Because `d`
is odd, there are arbitrarily large `m` with
`v2(dm+j+1)=k`. At `m+P`, the valuation is exactly `a`, contradicting
that period. Both values consequently occur infinitely often.

Write `T=2^a*d` with `d` odd. Choose a power of two `H>=R+1` divisible
by `2^a`. Frobenius gives

```
z(Hn+p,x) = XOR_j z(n,j) z(p,x-Hj),  0<=p<H.
```

For centre/righthand windows, `|x|<=R+1<=H`, while the source row at
time `p` has support `[-p,p]`. Only `j=-1,0,1` contribute. Symmetry
gives `z(n,-1)=z(n,1)=u_n`, and `z(n,0)=1`. Each entire window is
therefore one of precisely two patterns:

```
A_p = window at time p,
B_p = window at time H+p,
window at Hn+p = A_p if u_n=0, otherwise B_p.
```

The patterns may coincide. On `n=dm+j`, the lookup clock is fixed at
`(Hj+p) mod T`, while the selector `u_(dm+j)` is aperiodic. Hence a
labelled output column is eventually periodic **if and only if** its
labels agree on every such A/B pair. In that case it is purely
`H*d`-periodic. No larger eventual period or onset escapes these
equalities: restricting an eventually periodic sequence to any fixed
arithmetic progression is eventually periodic.

After imposing the A/B equalities for the centre, the neighbour is
aperiodic on its zero set **if and only if** some residue has centre
label 0 and unequal neighbour A/B labels. If no such residue exists,
the zero-set neighbour is purely `H*d`-periodic. This is the complete
R1 kill predicate inside the chosen factor class, not a required copy
of one particular source bit.

The CNF uses two equality clauses per centre A/B pair and a disjunction
of selectors. Each selector implies centre label zero and XOR of the
two neighbour labels. There are no explicit clock variables, fixed
zero phases, or neighbour-copy constraints in this final encoding.
All labels refer to actual source contexts; both A/B values occur in
each odd progression unless the patterns coincide.

The source, valuation, Frobenius, and CNF arguments were independently
audited. The CNF audit checked that earlier fixed-clock and neighbour
copy clauses are discarded rather than retained accidentally.

## Exact finite results (C)

Final complete-label encoding:

| Radius R | Lookup T | Spatial q | Guaranteed centre period if periodic | Lookup variables | Total variables | Contexts | Clauses | Result |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2 | 4 | 14 | 4 | 364 | 367 | 560 | 4,494 | UNSAT, DRAT verified |
| 4 | 4 | 14 | 8 | 812 | 817 | 1,141 | 9,152 | UNSAT, DRAT verified |
| 2 | 40 | 8 | 40 | 980 | 995 | 1,205 | 9,706 | UNSAT, DRAT verified |
| 4 | 40 | 8 | 40 | 1,440 | 1,465 | 1,700 | 13,716 | UNSAT, DRAT verified |
| 8 | 40 | 8 | 80 | 2,720 | 2,765 | 3,155 | 25,456 | UNSAT, DRAT verified |

The T40 rows use `d=5`, with `H=8` at radii 2 and 4 and `H=16` at
radius 8. Their nonconstant source subsequences are odd-progressions
of `u`, rather than one phase of the sparse Rule 90 sequence. The
centre periods 8 and 80 permitted above are not restricted to the
respective lookup periods 4 and 40.

Before the general quotient, a complete special case for `R<=3,T=4`
was checked with unknown centre clock and a disjunction over all
centre-zero phases. Its results were:

| R | Total variables | Clauses | Result |
|---:|---:|---:|---|
| 1 | 223 | 2,929 | UNSAT, DRAT verified |
| 2 | 371 | 4,502 | UNSAT, DRAT verified |
| 3 | 568 | 6,523 | UNSAT, DRAT verified |

The relevant neighbour pattern pairs, in integer bit encoding, were
`R1: p2=(1,5),p3=(3,5)`;
`R2: p1=(7,23),p2=(2,10),p3=(23,26)`;
`R3: p0=(4,68),p1=(14,110),p2=(21,68),p3=(53,110)`.
These are genuine alternatives to the earlier copy-only source-bit
pin. Nonetheless all were incompatible with the local Rule 30 gates.

### Stronger source-response diagnostic at R8/T40/q8 (C)

After removing **all** centre-periodicity and zero-set-aperiodicity
conditions, the Rule 30 gates still exclude any dependence on the
source. This uses the exact condition that some actual nonzero source
window has an output different from the all-zero window at the same
time and spatial clocks. The 2,400 response selectors and 2,720 lookup
variables give 5,120 variables, 30,041 clauses, and 3,155 exact source
contexts. The resulting CNF is UNSAT, with a checked DRAT proof.

Consequently every radius-8/T40/q8 factor in this fixed-source class is
source-independent: its diagram is just its periodic clock background.
This is stronger than excluding R1 counterexamples inside this finite
class, but it is not an exclusion of all radii.

The background itself is not forced to zero. The explicit width-8
initial row encoded by integer 7 has minimal Rule 30 time period 40.
Ignoring the source and returning this background satisfies every one
of the 3,155 exact factor gates. All 40 rows are retained in
`r150-trivial-background-witness-T40-q8.json`.

Files: `r150_source_response.py`,
`r150-source-response-R8-T40-q8.json`, and its certificate files.
An equivalent response condition is a changed output at time zero
somewhere in `[-R,R]`: if the initial output equals its periodic
background everywhere, determinism forces equality at every future
time. Thus the remaining uniform question can be phrased as existence
of a finite initial defect that supports this exact source factor.

## Controls and reproduction

`r150_orbit_factor_synthesis.py` first checked the more restricted
phase-3 copy/complement class at radii 1 and 2. Its Rule 150 identity
control satisfies every source/target-150 local gate, centre pin, and
neighbour-copy pin after omitting the requested zero-centre phase:
the source centre is 1, so that omission is necessary and explicitly
recorded. It independently replays 12,352 source windows per radius
with direct Rule 150 truth-table evolution. This checks the source
encoding; it is not presented as a Rule 90 counterexample control.

The unchanged `controls.rule90_control(6)` also passes at `T=2,4,6`;
its output is retained in `automatic-factor-unchanged-rule90-control.json`.
The earlier exact Rule 90 source identity control passes every gate and
the full zero-centre/aperiodic-neighbour specification. Nothing here
purports to prove a rule-generic R1 statement.

From a fresh copy of the construction directory:

```sh
uv run --with python-sat python r150_label_quotient_synthesis.py --radius 2
uv run --with python-sat python r150_label_quotient_synthesis.py --radius 4
uv run --with python-sat python r150_label_quotient_synthesis.py --radius 2 --period 40 --spatial 8
uv run --with python-sat python r150_label_quotient_synthesis.py --radius 4 --period 40 --spatial 8
uv run --with python-sat python r150_label_quotient_synthesis.py --radius 8 --period 40 --spatial 8
uv run --with python-sat python r150_source_response.py --radius 8 --period 40 --spatial 8
```

The required source files are `additive_exact_contexts.py`,
`r150_orbit_factor_synthesis.py`, and
`r150_label_quotient_synthesis.py`. Output JSON records artifact hashes.
Proofs, CNFs and checker logs are in `r150-orbit-factor-certificates/`;
the checker is DRAT-trim, located by
`experiments/rule30/r1-isolated-column/drat_trim.py` (`$RULE30_DRAT_TRIM`,
then `/tmp/rule30-family-seam-drat-trim/drat-trim`, then `PATH`; pinned
build recipe in `docs/rule30/RESULTS-family-seam.md`).

## Scope

The exact label quotient settles periodicity of every output labelling
within each chosen finite factor class. It is not a bounded-window
prediction of the Rule 30 neighbour from its centre history. The
labelled windows belong to an auxiliary Rule 150 source.

The finite UNSAT results exclude the listed classes, including every
smaller radius obtainable by ignoring outer bits. They do not exclude
all radii, all clocks, all automatic source diagrams, or all Rule 30
configurations. No actual R1 kill, proof of R1, or proof of P1 has been
obtained. The remaining issue is the **exact factor synthesis gap**:
the observation obligation is completely encoded, but no full Rule 30
factor satisfying it has been found.

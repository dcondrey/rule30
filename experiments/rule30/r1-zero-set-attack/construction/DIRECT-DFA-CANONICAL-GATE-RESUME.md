# Canonical gate regeneration for the same binary automatic class

This continuation preserves the five-state binary MSB coordinate class
with lookup phases `t mod 4` and `x mod 14`, arbitrary eventual centre
period, and an aperiodic zero-set neighbour. The exact observation
predicate and all-coordinate Rule 30 gate checker are unchanged.
The preregistered solver cap is 300 seconds after source reconstruction;
a time-cap result is a measurement, not a class exclusion or an R1 result.

## Mechanism and success/kill conditions

The old whole-alphabet state numbering differs from the new axis-first
numbering on 19,148 of the 23,505 old models that reached a failed local
gate. That is a representation diagnostic. It does not by itself measure
the number of useful missing clauses.

**U — Conjugated cuts remain necessary.** Let `pi` be a permutation fixing
the initial state. Set `delta_new(q,a) = pi^-1(delta_old(pi(q),a))` and
`g_new(p,s,q) = g_old(p,s,pi(q))`. Induction on a coordinate's digit word
gives equal output values for every coordinate. Consequently each old
failed Rule 30 gate still fails at exactly the same `(t,x)`. Negating its
renamed transition/output implicant gives a necessary clause. This does
not assume that the old model satisfies the new observation predicate.

The implementation retains every original ordinary gate cut, regenerates
the corresponding cuts after axis-first renaming, and checks all 20
transition entries and 280 output entries of each source model. It checks
the conjugacy of every state on all four coordinate paths as well as the
forcing Rule 30 truth-table cube. All cut literals refer only to preserved
transition/output variables 1 through 381. Old centre-clock and observation
constraints are discarded. New unique canonical clauses are counted only
after the entire independently audited broader 180-second pool has been
imported, avoiding an inflated count from import order.

**U — Rule 30 eventual-zero-centre prune.** If the centre is eventually
zero, the neighbour satisfies `r(t+1) = r(t) OR s(t,2)` and is eventually
constant. Thus an R1 countermodel must have a one in its eventual centre
period. For each canonical axis, the exact endpoint relation's left
projection lists every state reached at coarse times beyond the uniform
onset bound. Folding the low time-phase suffix and using the already
defined composed centre outputs gives an exact guarded disjunction that
some actual tail state has centre label one. No new variables are needed.
The helper enforces Rule 30 and a power-of-two lookup period explicitly.
It must not be used for an odd-factor lookup period without its residue
lift. Rule 90 fails the monotonicity primitive: `F90(0,1,0)=0`.

Success still requires one model passing complete all-coordinate Rule 30
closure and the exact R1 observation predicate, followed by independent
verification. The finite-class kill condition is UNSAT with a checked
proof of the complete final CNF. No finite set of failed models substitutes
for either condition.

## Producer checks

**C.** The small canonical-import regression checks all 24 permutations
fixing the root of a five-state control, 24,576 scalar coordinate values,
480 transition and 6,720 output conjugacy entries. It includes a mixed old
pool with an actual legacy-clock literal and verifies that only ordinary
gate clauses survive. It also tests that a canonical clause already in
the later broad pool is not counted as new.

**C.** The OR-prune regression checks all 32,768 two-state/two-phase/two-
spatial-class parameter assignments, retaining 384 nonconstant eventual-
centre observations and excluding 336 eventually-zero-centre observations.
The four frozen Rule 30 gate values, Rule 90 counterexample, and prevention
of Rule 90 helper application are checked explicitly. Independent symbolic
reviews passed for both the canonical importer and the OR-tail helper.
The independent OR-tail implementation also rebuilt all 20,927 added
clauses over the 21,091-axis catalogue, checking 390,036 actual-time
prefix-state evaluations and 25,088 small tail-label assignments; the
164 axes with no possible aperiodic observable were correctly skipped.

```
uv run --with python-sat --with ijson python experiments/rule30/r1-zero-set-attack/construction/verify_general_canonical_import.py
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_or_tail_prune.py
uv run --with python-sat --with ijson python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_general_resume.py --gate-source experiments/rule30/r1-zero-set-attack/construction/direct-dfa-lean-path-R30-N5-T4-q14-shared-900.json.gz --checkpoint experiments/rule30/r1-zero-set-attack/construction/direct-dfa-general-R30-N5-T4-q14-cadical180.json.gz --nonzero-tail --seconds 300 --output direct-dfa-general-R30-N5-T4-q14-canonical-gates-cadical300.json.gz
```

Use a fresh output filename for a repeated run. The result and exact
additional-clause counts are recorded by the producer and final artifacts.
These changes do not establish R1 or P1, or exclude other automaton sizes
or output lookup phase counts.

## Exact rebuilt pool

The full producer replay passed for 23,505 old gate-failing models and
728,441 ordinary gate records, including 470,100 transition and 6,581,400
output conjugacy entries. Of those models, 19,148 change naming and
contribute 592,244 gate records. There are 711,445 distinct canonical gate
clauses: 144,297 were already in the complete earlier broad pool, and
**567,148 are new**. The sorted new-clause stream SHA-256 is
`b88830214435daa8c40437ca0b6752e9cedb3cdac69f6079d491bca34963ceba`.

The earlier pool is reconstructed exactly at 1,357,337 clauses. After the
canonical additions and 20,927 tail-prune clauses, the solver base has
1,945,412 clauses and the same 2,069 variables. Source hashes, ordered cut
hashes, the permutation hash, and the complete rebuild counts are in
`direct-dfa-general-R30-N5-T4-q14-canonical-gates-cadical300-producer.json`.

## Measured continuation

The result is **M / UNKNOWN** after 300.1602085 seconds, with 5,576 new
models and 143,765 gate records. Every model passed the complete automatic
R1 observation predicate and failed an actual Rule 30 gate. The final
pool has 2,069 variables and 2,089,019 clauses; the retained CaDiCaL195
solver used 5,583 solve chunks and 283,429 conflicts. All new deterministic
paths and forcing truth-table cubes replayed correctly. The largest saved
cut has 21 literals, including at most 17 distinct transition literals.

All 5,576 candidate centres have a nonconstant eventual period. Their
reachable axis sizes are two for 32 models, three for 487, four for 870,
and five for 4,187. These are failed parameter models, not realizations.

The final artifact is
`direct-dfa-general-R30-N5-T4-q14-canonical-gates-cadical300.json.gz`.
Its compressed SHA-256 is
`cc61bf0bf7270d66446d7bd108bc624ad161391c84ba6772a57413e56f30a3ae`;
its exact uncompressed JSON SHA-256 is
`bf61d977372ed321cb9a2ddab668552bb5ff82916fb38294dd580d048db2872e`.
The semantic provenance dependencies remain the earlier shared checkpoint
and broader 180-second artifact. Independent full replay of this new
continuation is pending separately; the previous pool and all new helper
semantics have already passed independent review. There is no UNSAT proof
to report and no explicit Rule 30 counterdiagram.

## Shared-prefix diagnostic for the next implementation

**M.** All 5,576 saved failed models were checked against the separately
audited uniform-prefix gate encoding. Depth two rejects 5,547; depth
three rejects the remaining 29. This is evidence about these models,
not an exclusion of the automatic class. Each rejection was independently
re-evaluated at its actual coordinate against the frozen Rule 30 gate.
For example, zero-based candidate 1,595 passes depth two but fails at
depth three at `(t,x)=(11,57)`: its four values are `1,0,0,0`, although
`F30(1,0,0)=1`. The full diagnostic is
`direct-dfa-canonical300-prefix-diagnostic.json`.

```
uv run --with python-sat --with ijson python experiments/rule30/r1-zero-set-attack/construction/diagnose_resume_prefix_gates.py experiments/rule30/r1-zero-set-attack/construction/direct-dfa-general-R30-N5-T4-q14-canonical-gates-cadical300.json.gz --count 5576 --output experiments/rule30/r1-zero-set-attack/construction/direct-dfa-canonical300-prefix-diagnostic.json
```

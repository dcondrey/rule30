# Pointed sofic inverse covers: exact operator and short-return obstructions

This is an intermediate construction result. **No R1 proof or Rule 30
counterdiagram is obtained.** There is an exact finite-language checker
for a sufficient return mechanism, and several proposed return maps are
uniformly excluded by specific sampled words. Rule 90 passes the same
covering mechanism.

## Uniform mechanism (`U`, independently audited)

Let `G_a(x)_i = x_(i-1) XOR (x_i OR x_(i+1))`, with prescribed `x_0=a`.
For a finite drive `d` beginning in zero, let `H` be its composed driven
map, repeated periodically. One observation is the initial right
neighbour at each complete return. The drive length need not be the
minimal centre period.

Starting from all infinite right rows, define compact sets

```
X_0 = {0,1}^N,
X_(n+1) = X_n intersect H(X_n intersect [0]) intersect H(X_n intersect [1]).
```

A nonempty fixed point supplies both inverse covers: every target in X
has a predecessor in X with observation zero and another with observation
one. For every prescribed finite future observation word, choose those
predecessors backwards from any terminal point of X. The sets of initial
rows realizing longer prefixes while returning to X are nested, compact,
and nonempty. Their intersection gives a single coherent forward orbit
with any chosen infinite observation word. Choosing a provably aperiodic
word therefore gives an R1 counterdiagram; the zero phase of the periodic
drive is sampled throughout. This argument does not reverse the order
of one preselected infinite past orbit.

Finite stabilization is sufficient, not necessary. If all X_n were proved
nonempty, compactness would give a nonempty X_infinity. For any target in
that intersection, the nested compact predecessor fibres
`H^-1({target}) intersect X_n intersect [b]` show that both inverse covers
persist. Mere finite nonemptiness is not such a proof.

An empty X_n excludes this covering mechanism for every candidate subset
of right rows, including nonsofic subsets. The mechanism is stronger than
an aperiodic trace: invertible chaotic systems can have unique predecessors
and fail the cover condition. Its exclusion does not establish R1.

## Exact finite representations (`C` and `U`)

The first implementation uses a rooted partial DFA whose productive
infinite paths label right rows. For one driven step, the image NFA state
`(q,l,c)` records the source-language state after consuming current input
bit c. Choosing the next source bit r emits `F30(l,c,r)` and advances to
`(q_next,c,r)`. The first l is the prescribed boundary. Each infinite
output path has one coherent infinite source lift by the finite-branching
path lemma. All actual intermediate Rule 30 gates are retained.

Image determinization gives an exact partial DFA. Intersections use the
ordinary product, but all states without an infinite continuation are
removed before testing nonemptiness. Minimal productive-prefix DFAs give
semantic equality of infinite row languages.

The second implementation retains NFAs through image and intersection,
with productive trimming and a sound strong-bisimulation quotient. Cover
inclusion is decided by a finite search on `(source_state,target_subset)`.
A reachable empty target subset gives an exact failed source prefix;
the productive source state guarantees an infinite source continuation.
This avoids independently determinizing each large image.

Independent checks cover 773 small NFAs, 9,276 all-word image equivalences,
51,076 inclusion pairs, and 51,076 intersection pairs; also 86 partial
DFAs and 1,032 all-word image equivalences. Six Rule 90 covers pass.
These are full finite-automaton language comparisons, not bounded-word
sampling. See `sofic-return-cover-independent-check.json`.

## Computed sets and the representation obstruction

For drive `01`, the DFA operator has X_1 of 68 states. Its branch images
at iteration two have 3,962 and zero states, so X_2 is empty. The result
matches the direct forbidden observation `11`.

For drive `0101`, the individual four-step images each have 256 NFA
states, with microstep counts `4,16,64,256`. Neither covers all right rows:
the shortest failed target prefixes are `110` for the source-first-bit
zero branch and `011` for the one branch. Their productive common target
X_1 has a 7,033-state NFA. A 100,000-state cap stops the second iteration
during its zero-branch image, after the first microstep has 26,774 states.
No fixed point or empty X_2 was inferred from that cap.

The original 5,000-state DFA trials for `0101`, `010101`, `011`, `0111`,
and `0011` stopped in first-image determinization. A 100,000-state DFA
retry for `0101` also stopped there. These are representation limits.
The short-return exclusions below make further enlargement of those
particular cases unnecessary. The automaton state count is not a
well-founded decreasing quantity, although the represented sets are nested.

## Exact failed observation words

| Centre drive | Microsteps per observation | Missing word | Evidence |
|---|---:|---|---|
| `01` | 2 | `11` | U OR identity; exact X_2 extinction |
| `01` | 4 | `10011` | U after recorded burn-in; 16 exact completions |
| `01` | 6 | `1011` | U after recorded burn-in; 64 exact completions |
| `0111` | 4 | `11` | U OR identity; 32 five-cell initial rows |
| `0011` | 4 | `010` | C checked DRUP: 9 cells, 45 variables, 259 clauses |
| `0011` | 8 | `10101` | C checked DRUP: 33 cells, 561 variables, 4,101 clauses |

For alternating centre at rho-stride two, every completion of
`1?0?0?1?1` contains `11` (14 completions), `00000` (one), or `0100101`
(one). At stride three, every completion of `1??0??1??1` contains `11`
(60), `00000` (one), `101001` (two), or `1010001001` (one). These are
the previously certified eventual factors, so the conservative shared
burn-in is 23 rho samples. This gives operator extinction upper bounds
17 and 12 respectively, without constructing the larger automata: a
nonempty X_n would realize every n-letter sampled itinerary, including
the forbidden mask placed after that burn-in. No minimal extinction
iteration is claimed for these two returns.

The 32 frozen triple checks for two-step boundary drives give, with
initial right bits `(r,u,v)`, precisely

```
00: r OR u OR v                 01: NOT(r OR u OR v)
11: r AND (u OR v)              10: NOT[r AND (u OR v)].
```

Therefore a zero boundary followed by an odd number of ones forbids
consecutive return observations one. An initial one becomes one after
the zero step, zero after the first one step, and stays zero under each
remaining pair of one steps. This uses the OR nonlinearity.

For `0011` with observation times `0,4,8`, `010` is the shortest missing
word; all one- and two-letter words occur. A proper-prefix `01` witness
starts `00100`. At stride eight all 30 binary words of lengths one through
four occur; the first missing five-letter word in lexicographic order is
`10101`. Every saved SAT initial row is replayed with the frozen rule
table. Each UNSAT result is re-solved with its observation units included
in the actual CNF and checked by `drat-trim`.
Independent replay subsequently rebuilt both exact CNFs and rechecked
both DRUPs, all 8 and 51 preceding SAT words, and the two Rule 90 witness
rows: 17,796 frozen cell updates. All 32 two-step OR truth rows and the
unchanged project Rule 90 control also pass. This is recorded in
`sampled-return-cone-independent-check.json`.

These finite cones refute fully specified sampled words with the entire
periodic boundary fixed and other neighbour times unconstrained. They
do not decide eventual periodicity of an unknown centre word from a
bounded window, so the front-lemma prohibition is not implicated.

## Control, reproduction, and scope

Rule 90 has the full right-row space as an immediate fixed point of the
same covering operator. Both initial-neighbour choices lift every target
under each driven map. The exact operator checks reproduce this, and the
unchanged `controls.rule90_control(6)` passes. Rule 90 also realizes both
new forbidden Rule 30 sampled words; its saved initial rows are replayed.

```
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/sofic_return_cover.py
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/sofic_return_cover_nfa.py --states 100000 --iterations 2 --output sofic-return-cover-nfa-b2-100k-repeat.json
uv run python experiments/rule30/r1-zero-set-attack/construction/sampled_factor_cover_masks.py
uv run --with numpy --with python-sat python experiments/rule30/r1-zero-set-attack/construction/sampled_drive_cover_gate.py
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/sampled_return_cone_sat.py
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_sofic_return_cover_independent.py
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_sampled_return_cones_independent.py
```

No invariant Cantor return or aperiodic Rule 30 diagram has been found.
The established obstructions concern the specified binary covering
mechanisms, not all periodic drives, all returns, or all aperiodic
subsystems. A proper spatial-language certificate with more suitable
observations, or a quotient that does not require two actual predecessors
of every whole target row, remains outside these exclusions.

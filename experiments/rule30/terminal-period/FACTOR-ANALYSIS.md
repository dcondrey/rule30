# Finite-factor candidates fail uniformly

Date: 2026-09-09. This supplies obstruction evidence, not a terminal-period
proof or a realizable counterexample. No necklaces beyond the existing
h<=15 regression are enumerated.

## Exact regression and original factors

`factor_graph.py` uses the seven frozen minimal forbidden factors through
length 10 and the 24 saved certified prefixes. Its prefix-suffix graph has
355 states and 495 edges. Its only recurrent SCC has 337 states, 466 edges,
and 129 states with two outgoing edges inside the component.

The candidate accepts exactly the four known necklaces in the full existing
regression: 4,720 primitive necklaces, 4,692 killed by frozen factors, 24
more killed by saved prefixes, four accepted, zero mismatches.

Nevertheless, at state suffix `0101010` the words

```
A = 0010001010101010
B = 10
```

are both closed walks. Therefore every `A B^k`, k>=0, is cyclically accepted.
Up to rotation these words are `0001 0001 (01)^(k+4)`, of minimal period
16+2k. Their cyclic zero-gap words have exactly two 3s, adjacent, and at
least four 1s. The unique cyclic occurrence of the gap pair (3,3) marks a
single rotation position, so no nontrivial cyclic shift fixes the word.
This proves primitivity uniformly in k.

The k=0 word `0001000101010101` is *not* right-realizable: its first
infeasible canonical prefix has length 24. Its 23-symbol predecessor has
the exact initial right row

```
001000111101000100011111101000001111000101000
```

and replays through the frozen `numeric_rho`. The independent Z3 encoding
agrees at both boundary lengths, and the new CNF/DRUP proof checks 152
additions. See `factor-cone-results.json` and `factor-cones/`.

## Eventual sparse masks: the stronger candidate still fails

A selected assumption core may retain observations only at sample positions
a+D, with all earlier observations unprescribed. Such a core forbids its
normalized mask at every actual trace position p>=a: use the cone beginning
at sample p-a. Its alternating boundary has the same centre-zero phase,
and its free initial right row is the actual row at that time. Thus the
normalized mask is an *eventual* forbidden factor. It need not be forbidden
at a fresh onset. Since every phase recurs arbitrarily late in a periodic
tail, this distinction permits sound cyclic mask tests on that tail.

The 24 selected cores provide 15 distinct masks, with maximum burn-in 23
rho samples. `core_factor_graph.py` adds their restrictions. It expands
wildcards only along paths avoiding factors already established. Every
discarded completion was already forbidden; consequently the resulting
exact-factor language equals the original-factor language intersected with
avoidance of all masks. Only 38 new completions are needed, despite the
largest mask having 25 wildcards. Removing redundant factors leaves 45.

The strengthened graph has 557 states and 718 edges. Its only recurrent SCC
has 287 states, 350 edges, and 63 branching states. An independent slower
prefix-suffix construction reproduces every state and edge of the efficient
Aho-Corasick construction. All 4,720 old necklaces regress unchanged:
4,716 rejected and precisely the four known necklaces accepted.

At suffix `0100100100` (state 116), these are exact return words:

```
A = 0010000100100100
B = 100
A states: 116,140,164,189,215,241,266,288,312,338,362,292,317,343,71,91,116
B states: 116,71,91,116
```

Hence `A B^k` is a closed walk for every k>=0. A deterministic
prefix-suffix graph rejects a transition exactly when a forbidden factor
ends there. Repeating a closed walk therefore avoids all 45 factors,
including those crossing the period boundary. These words consequently
avoid all 31 original factors and all 15 normalized eventual core masks.

Rotating the final two zeros of `A B^k` to the front gives

```
rho_k = 00001 00001 (001)^(k+2),   k >= 0.
h_k   = 16 + 3k.
```

Its cyclic zero-gap sequence is `(4,4,2,...,2)`, with k+2 copies of 2.
There is exactly one cyclic occurrence of adjacent gap pair (4,4).
Every rotational symmetry of rho must preserve its 1s and induce a cyclic
symmetry of the gap sequence. The unique (4,4) position must be fixed,
which fixes a particular 1-position and forces the rotation to be trivial.
Thus h_k is the minimal period for every k>=0. This is an all-k obstruction
to the strengthened *finite-language criterion*. It is not an all-k
realizability claim.

The k=0 word `0000100001001001` is also not right-realizable. Its first
infeasible canonical prefix has length 51, namely

```
000010000100100100001000010010010000100001001001000
```

The 50-symbol predecessor is realized by these 99 initial right cells:

```
011011100011100111001111101010010010001010000010011101000101110001010100101001001011111110011011100
```

The frozen `numeric_rho` verifies that predecessor, independent Z3 agrees
at lengths 50 and 51, and a scalar truth-table CNF with 5,151 variables and
40,051 clauses has a checked DRUP proof with 10,961 additions. See
`core-factor-cone-results.json` and `core-factor-cones/`.

The selected assumption core of this new 51-symbol cone has burn-in 16
and normalized mask `0?????0??1????????0???0??1??1????00` of length 35.
It rejects rho_0 but misses every rho_k with k>=1. The finite checks k=1..10
are sufficient for this last assertion: write rho_k=P(001)^(k+2), where
P=`0000100001`. For k>=10 the periodic background between consecutive
marked P blocks has length at least 36. A 35-symbol window meets at most
one P; all such windows, and the pure `001` windows, already occur at
k=10. Their set is therefore constant for k>=10. The complete phase scans
are in `h16-family-mask-results.json`, reproduced by
`h16_family_mask_check.py`. This additional selected core is solver-checked
with all single-deletion witnesses replayed; its sparse CNF has no separate
DRUP certificate, as recorded in `h16-selected-core.json`.

The specific missing implication is **finite-language completeness**:
these sound necessary constraints leave recurrent branching, and accepted
closed walks need not lift to arbitrarily deep Rule-30 right cones. The
second k=0 witness demonstrates this failure even after all selected core
masks are included. An all-h proof needs a further uniform restriction,
or a proof controlling the whole descending family of right-extension
languages. Neither an SCC in this necessary language nor a finite SAT
prefix proves a realizable periodic trace.

## Reproduction and scope

```
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/terminal-period/factor_graph.py
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/terminal-period/core_factor_graph.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver --with python-sat python experiments/rule30/terminal-period/factor_cone_check.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver --with python-sat python experiments/rule30/terminal-period/factor_cone_check.py --core
```

The original proof cores must be fully extracted before the second command;
the script requires 24 records and records the source hash. The finite
checks are `C`; the return-word implications and primitive-family arguments
are `U`; the two registered finite-factor candidates are `K`. These
arguments inherit their Rule-30 content from the OR-dependent certified
factors and masks. They supply no such restrictions for Rule 90.

Both checked h=16 words would have neighbour period 32 if realizable, and
32 does not divide 420. Both are certified impossible, so neither is a
q=420 witness. The terminal-period theorem, its periodic-branch consequence,
and the separate aperiodic q=420 branch remain open.

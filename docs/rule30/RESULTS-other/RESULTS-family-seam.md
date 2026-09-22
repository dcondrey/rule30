# The family 00001 00001 (001)^(k+2): a uniform seam exclusion

Date: 2026-09-09.

**Deliverable (a): every member of the family is right-unrealizable.** This
is a uniform, computer-assisted proof with a finite seam certificate and
seven finite exceptions, all independently proof-checked.

The mechanism is a **failed return after the seam**. The width-20 reachable
set for the gap-2 regime stabilizes at 670 states. The `4,4` excursion itself
is feasible from that set, with 794 possible endpoint states. However, none
of those endpoints can complete six further gap-2 blocks. This is the
additional finite question needed after a positive answer to the excursion
test: feasibility of the excursion does not imply a realizable periodic
member.

The uniform argument covers every `k>=7`. The finitely many exceptions
`k=0,...,6` have direct finite-cone refutations. The diagnostic table below
is not extrapolated to prove the theorem.

| Result | Evidence |
|---|---|
| Stable width-20 gap-2 set: exactly 670 states after nine blocks | `C`, two implementations |
| Excursion followed by six gap-2 blocks has empty image | `C`, two implementations |
| No family member with k>=7 is right-realizable | `U/C`, induction plus the finite strip certificate |
| No family member for any k>=0 is right-realizable | `U/C`, uniform tail plus seven certified finite exceptions |
| The same uniform seam word is UNSAT in the frozen unrestricted cone | `C`, checked DRUP and independent Z3 |
| Shortest canonical prefix lengths for k=0,...,10 | `M/C`, diagnostic boundaries and exact SAT predecessor rows |

## 1. The finite state and its soundness

At an even original time, retain right columns `1,...,20`. Represent their
bits by an integer `r=sum_(j=1)^20 a_j 2^(j-1)`. In particular, the low bit
is the current rho observation. There is no spatial wrap, no periodicity
assumption on farther columns, and no constraint on the initial right row.

For original-time phase `b in {0,1}` and an arbitrary exterior bit `e`, the
next retained row is obtained by the scalar rule

```text
a'_j = a_(j-1) XOR (a_j OR a_(j+1)),
a_0 = b,  a_21 = e.
```

Both choices of `e` are retained at every update. Two updates, at phases
zero and one, followed by filtering the low bit to a prescribed sample,
define a relation on the finite row set. Every actual right half-plane
projects to a path in this relation, by taking its actual column-21 value
as `e`. The converse is not assumed or needed.

For a word `w`, let `B_w(X)` be the set reached from `X` by prescribing the
**next** samples to be `w`. All block endpoints below have rho equal to one.
Define

```text
U = { r : 0 <= r < 2^20, r is odd },
G(X) = B_001(X),
E(X) = B_0000100001(X),
S_0 = U,   S_(m+1) = G(S_m).
```

Thus `G` crosses a gap of two zeros between ones, using six original
updates. `E` crosses the two successive four-zero gaps, using twenty.

Finite-width evolution is a **relation**, not an assumed partial function.
Nevertheless, the reachable-set argument works: `G(U) subset U`, and
relational image is inclusion-preserving. Inductively,

```text
S_(m+1) subset S_m  for every m>=0.
```

The finite descending sequence therefore stabilizes. Equality of two
successive sets proves equality at every subsequent step. This is the
justification for stabilization, rather than an observed plateau in an
unjustified state model. The stabilized set concerns arbitrarily long
gap-2 **prehistories in the relaxed strip**; it is not asserted to be the
exact projection of all full right rows that continue gap-2 forever.

## 2. The computed stable set and the failed return

The exact counts, starting at `S_0`, are

```text
m       0       1      2     3     4     5    6    7    8    9   10
|S_m| 524288   17015  3706  2436  1814  1293  944  761  709  670  670
```

Set equality `S_10=S_9`, not only cardinality equality, was checked.
Consequently `S_inf^(20)=S_9` for every subsequent iterate. All 670 integers
are explicitly listed in
[strip-w20-r30-sinf.txt](../../experiments/rule30/family-seam/strip-w20-r30-sinf.txt),
one integer per line in the encoding above. Its SHA-256 is
`867934af47c38e91d88c71c704465eeed4bc2e47d5beb9f1ada5d8445f5aa56a`.

Starting from this set, the excursion and return give

```text
j                  0    1    2    3    4   5   6
|G^j(E(S_inf))|    794  75  145  188  155  86   0
```

In particular, **`G^6(E(S_inf))` is empty**. These intermediate sets are
not claimed to be nested: `75 -> 145` explicitly shows why cardinality
monotonicity cannot be applied to an arbitrary seed under a relation.

[strip_sets.py](../../experiments/rule30/family-seam/strip_sets.py) computes
the images using whole-row bit operations. Independently,
[verify_strip.py](../../experiments/rule30/family-seam/verify_strip.py)
constructs all 4,194,304 `(row, phase, exterior-bit)` transitions directly
from the scalar Rule 30 truth table, then recomputes the sets. The two
implementations agree on the complete stable set and all displayed counts.
See [strip-verification.json](../../experiments/rule30/family-seam/strip-verification.json).

## 3. Uniform proof for k>=7

**Lemma.** Under the alternating centre, no actual rho contains

```text
W = 1 (001)^9 00001 00001 (001)^6.
```

**Proof.** The retained row at the first one lies in `U`. After the first
nine gap-2 blocks, it lies in `G^9(U)=S_inf`. After the excursion and the
next six gap-2 blocks, it would have to lie in
`G^6(E(S_inf))`, which is empty. Soundness of the strip projection gives
the contradiction. ∎

This 56-sample word is exactly

```text
10010010010010010010010010010000100001001001001001001001
```

It was also checked directly with the **unmodified unrestricted cone**:
111 initial cells, 6,216 variables, 48,456 clauses. The frozen DRUP checker
accepts all 17,947 proof additions and the empty clause. The independent
frozen Z3 cone also returns UNSAT. These are a separate certificate route
for the finite lemma, independent of the row-set implementation. See
[uniform-seam-certificate.json](../../experiments/rule30/family-seam/uniform-seam-certificate.json).

**Proposition.** No `rho_k` with `k>=7` is right-realizable.

**Proof.** Put `m=k+2`, so `m>=9`. Around any recurring `4,4` excursion in
`rho_k`, take the preceding nine of its `m` gap-2 blocks and the following
six of its `m` gap-2 blocks. Together with the initial one they form `W`.
Equivalently, in the canonical infinite word of period `h=16+3k`, `W`
starts at sample `h-28` (zero-based). The lemma excludes this occurrence.
The same argument applies after any periodic onset. ∎

This proof concerns specified periodic words. It uses no bounded-window
decision of eventual periodicity for an unknown word, so the front-lemma
restriction does not apply.

## 4. Diagnostic n(k) and the finite exceptions

Here `n(k)` is the shortest infeasible canonical prefix length. Each
predecessor of length `n(k)-1` has an explicit initial row, forward-replayed
with the unchanged `numeric_rho`. Each infeasible boundary uses the frozen
truth-table cone. Monotonicity under prefix extension makes these two
boundary checks sufficient for minimality.

| k | h_k | n(k) | Initial cells in infeasible cone |
|---:|---:|---:|---:|
| 0 | 16 | 51 | 101 |
| 1 | 19 | 114 | 227 |
| 2 | 22 | 189 | 377 |
| 3 | 25 | 63 | 125 |
| 4 | 28 | 69 | 137 |
| 5 | 31 | 65 | 129 |
| 6 | 34 | 47 | 93 |
| 7 | 37 | 50 | 99 |
| 8 | 40 | 53 | 105 |
| 9 | 43 | 56 | 111 |
| 10 | 46 | 59 | 117 |

The diagnostic is irregular: increments are
`63,75,-126,6,-4,-18,3,3,3,3`. The last four equal increments are observations,
not an asserted all-k formula. The proof of the infinite tail is section 3.
The rows `k=0,...,6` separately finish the finite exceptions to that proof.

**Theorem.** For every integer `k>=0`, the infinite periodic word
`rho_k = (00001 00001 (001)^(k+2))^infinity` is not right-realizable under
the alternating Rule 30 centre. **Proof.** Section 3 covers `k>=7`; the
seven checked finite-cone refutations cover `0<=k<=6`. ∎

Exact initial rows, query timings, and every prescribed prefix are in
[diagnostic-results.json](../../experiments/rule30/family-seam/diagnostic-results.json).
The first Glucose query for `k=2` timed out at length 196; it was correctly
recorded as UNKNOWN. Incremental CaDiCaL on the same cone found SAT at 188
and UNSAT at 189. Using a 200-sample transition cone with only its first
`n` observation units is equivalent to the `n`-sample cone: all extra
initial cells are free and all later transitions can be filled forward.
The SAT predecessor was additionally replayed from just its first 375 cells.
The persisted final boundary certificate uses the exact 189-sample cone.

The original k=0 and uniform-seam proofs pass the frozen Python DRUP checker.
The larger boundary proofs are checked and trimmed using
[DRAT-trim](https://github.com/marijnheule/drat-trim) at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; the retained trimmed proofs are
then checked again against the original, unmodified CNFs. The checker
and package provenance is recorded in
[toolchain.json](../../experiments/rule30/family-seam/toolchain.json).

An initial CaDiCaL proof export was rejected because the wrapper had not
flushed its C output buffer. This was reproduced on a small pigeonhole
formula. The producer explicitly flushes the C buffer before reading the
proof, and accepts an artifact only after both external checks. The rejected
export is recorded separately and is not evidence for any conclusion.

## 5. Controls, preservation, and scope

The positive regimes remain feasible. In the same width-20 relaxation,
pure gap-2 has the 670-state stable set and pure gap-4 stabilizes at 1,021
states. No contradiction is attributed to the interior of either regime.

The relevant nonlinear identity remains

```text
rho_(n+1) = NOT(a_1 OR a_2 OR a_3).
```

The transition relation retains OR-saturation, including the fact that
when `a_20=1` the next top retained bit is independent of the exterior
bit. For Rule 90 that independence is absent. A direct width-8 Rule 90
control has all 128 odd rows in its gap-2 stable set and still all 128
after the excursion and six returns; it does not produce extinction.
The **unchanged** `controls.rule90_control(6)` also passes at `T=2,4,6`.
As in the prior report, Rule 90 realizes every rho by recursive choice of
odd initial cells, so the exclusion is specifically nonlinear.

All 25 frozen ladder/rung1/rung2 tests pass. The original terminal-period
machinery, `right_trace_forbidden.py`, `numeric_rho`, and `ladder.py` remain
unchanged; the ladder SHA-256 is
`589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.
The final [artifact audit](../../experiments/rule30/family-seam/artifact-verification.json)
rechecks all twelve retained proofs, regenerates every CNF exactly from the
frozen encoder, replays all eleven SAT predecessors, and confirms all twelve
recorded frozen source hashes. Redundant untrimmed boundary proofs were
removed after verification; their hashes are retained in the provenance file.

This settles this family only. No member supplies a q=420 witness,
including `k=18`. The arithmetic distinction remains correct: only
`h_18=70` divides 210; every other member would have been a witness if
realizable. Excluding this family does not classify every remaining
periodic word or close the periodic or aperiodic branch of q=420.

The registered mechanism and kill conditions are in
[REGISTRATION.md](../../experiments/rule30/family-seam/REGISTRATION.md).

## 6. Reproduction

From the repository root, the finite-state proof and its independent check:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/family-seam/strip_sets.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/family-seam/verify_strip.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver --with python-sat python experiments/rule30/family-seam/seam_certificate.py
```

The diagnostic producer deliberately refuses to overwrite existing results.
To repeat the search, first preserve `diagnostic-results.json` elsewhere,
then run `diagnostic.py` and `resolve_k2.py`, using
`uv run --with numpy --with z3-solver --with python-sat python`.
The stored artifact verifier supplies a read-only reproduction path without
rerunning all searches.

Build the external checker at the pinned revision, then verify all saved
proofs, exact cone contents, initial rows, and source hashes:

```sh
DRAT_TRIM_DIR="$HOME/.cache/rule30-family-seam-drat-trim"
git clone https://github.com/marijnheule/drat-trim.git "$DRAT_TRIM_DIR"
git -C "$DRAT_TRIM_DIR" checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C "$DRAT_TRIM_DIR" drat-trim
export RULE30_DRAT_TRIM="$DRAT_TRIM_DIR/drat-trim"
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver --with python-sat python experiments/rule30/family-seam/verify_artifacts.py --checker "$RULE30_DRAT_TRIM"
```

Any build of the pinned revision serves once `RULE30_DRAT_TRIM` names its
binary: the resolver in `experiments/rule30/r1-isolated-column/drat_trim.py`
reads that variable first, then `/tmp/rule30-family-seam-drat-trim/drat-trim`,
then `drat-trim` on `PATH`. A build under `/tmp` does not survive a reboot or
a temporary-file sweep, so keep it under `$HOME`.
`certify_boundaries.py --checker "$RULE30_DRAT_TRIM"`
regenerates missing boundary certificates from the recorded `n(k)` values.

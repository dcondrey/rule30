# `sig_A` is injective for every length: the closed-form argument

Date: 2026-09-06. Script: `syntactic_monoid_injectivity_proof.py`.

Status: **PROVED FOR ALL `L`. The open gap left by
`RESULTS-SYNTACTIC-MONOID-QUOTIENT.md` ("exhaustive-computation support up to
`L~18`, not a proof for unbounded `L`") is closed. The proof is two finite
checks on a 4x4 table and does not need the re-synchronization argument that
document named as the missing ingredient.**

Evidence level: `U/K` (uniform proof, all quantifiers discharged, with both
premises machine-checked; it kills the bounded-summary mechanism class and
nothing beyond it — see section 6).

## 1. Statement

Write `delta_a := QUEUE_INPUT_ACTIONS[a]` for the action of symbol `a` on the
four scan states, `full_trace(q, w)` for the literal sequence of intermediate
states from entering state `q`, and `sig_A(w) = (full_trace(q, w))_{q in 0..3}`,
all exactly as in `syntactic_monoid_quotient.py`.

> **Theorem.** For any two distinct words `w != w'` of the same length over
> `{0,1,2}`, `sig_A(w) != sig_A(w')`.

## 2. The two premises, both finite

- **L1.** Every `delta_a` is a permutation of `{0,1,2,3}`.
- **L2.** For `a != b` in `{0,1,2}`, `delta_a != delta_b` as functions:
  `diff(a,b) := {s : delta_a(s) != delta_b(s)}` is nonempty.

Measured (`syntactic_monoid_injectivity_proof.py`, rc=0):

```text
diff(0,1) = {0,1,2,3}
diff(0,2) = {0,1,2,3}
diff(1,2) = {0,1}          <- the only tight pair
diff(1,3) = {}             <- delta_1 == delta_3 identically
```

## 3. Proof

Let `i` be the first index where `w` and `w'` differ, `a = w_i`, `b = w'_i`, and
`p = w[:i]` the shared prefix. By L1 the prefix map
`pi_p = delta_{p_{i-1}} o ... o delta_{p_0}` is a composition of permutations,
hence a bijection of `{0,1,2,3}`. So as the global entering state `q` ranges
over all four states, the state *arriving* at position `i`, namely `pi_p(q)`,
also ranges over all four states.

By L2 choose `s in diff(a,b)`, and set `q = pi_p^{-1}(s)`. Then
`full_trace(q,w)` and `full_trace(q,w')` agree at every position `< i`, because
the prefix is shared, and differ at position `i`, because
`delta_a(s) != delta_b(s)`. Hence the `q`-th components of `sig_A(w)` and
`sig_A(w')` differ. QED

The witness is constructive, not a search: `theorem_witness(w, w')` in the
script returns that `q` directly and the run verifies the traces really do
separate, at `L = 19, 50, 200, 2000` — past the exhaustive horizon — for every
first-difference symbol pair and for the difference pushed to the final
position, where no suffix can re-separate.

### Why the quotient doc's stated obstacle was not on the path

Section 5 of `RESULTS-SYNTACTIC-MONOID-QUOTIENT.md` correctly observes that a
first point of difference need not produce a different trace value at *every*
entering state — `delta_1` and `delta_2` agree at states 2 and 3 — and concludes
a proof "would need to show the four trajectories ... can never simultaneously
re-synchronize". Only one entering state has to see the difference, and L1
guarantees one of the four arrives at any state you name. Re-synchronization
after position `i` is irrelevant: the traces have already differed at `i`, and
trace equality is positionwise.

## 4. Three things the exhaustive run could not state

**Legality is unused.** The theorem holds on the full product alphabet, so the
`{20, 22, 011}`-avoiding restriction plays no role. The exhaustive run was
measuring a strictly weaker statement: the script re-checks `L=1..8` over all
`3^L` words and reproduces the quotient doc's legal-word counts
(`3, 7, 16, 36, 81, 182, 409, 919`) as a regression alongside.

**Two entering states already suffice, and which two is decidable.** Only the
pair `(1,2)` is tight, so a subset `S` of entering states fails exactly when
some realizable prefix map carries `S` into the agreement set `{2,3}`. The
realizable prefix maps are the 8-element D8 image (identity included, from the
empty prefix), and enumerating them gives 9 sufficient subsets with minimal
elements `{0,2}, {0,3}, {1,2}, {1,3}` — one entering state from `{0,1}` and one
from `{2,3}`. The 6 insufficient subsets are all singletons plus `{0,1}` and
`{2,3}`, each with an explicit colliding pair printed by the script (e.g. `(1,)`
and `(2,)` collide on `{2}` and on `{3}`).

**The symbol quotient is what makes L2 true.** `delta_1 == delta_3` identically,
so on the un-normalized alphabet `{0,1,2,3}` the theorem is false and `1 ~ 3` is
its only collision — precisely the identification `SYMBOL_QUOTIENT = (0,1,2,1)`
already performs in `constant_tail_queue.py`. The normalization is not a
convenience; it is the exact kernel of the block action.

## 5. Consequence for the no-go family

`RESULTS-SYNTACTIC-MONOID-QUOTIENT.md` section 6 states its conclusion
conditionally: "If that holds at every `L` (not proved here), it says no
finite-state summary of an interior block, of ANY shape (not just D8-based
ones), can serve as a lossless transition congruence for this queue dynamics."
It holds at every `L`. That sentence is now unconditional.

Stated in monoid terms: the right congruence induced by `queue_step`'s block
scan on `{0,1,2}*` is the identity relation, so its syntactic monoid on blocks
is the free monoid on three generators. A lossless bounded summary would be a
finite quotient of it, and there is none at any radius. This subsumes
`RESULTS-QUEUE-WINDOW-PHASE-NO-GO.md`, which ruled out fixed end-window plus
total D8 action for every finite radius via one counterexample family; the
D8 collapse it exhibits is now the `sig_B` special case of a general fact.

## 6. Scope, honestly

This is a shallow result, and it should be recorded as one. Once the object is
named correctly — a scan that re-emits its whole intermediate trace, driven by
permutations — injectivity is close to immediate, and the interest is that it
retires a family cheaply, not that it is deep. Specifically it does **not**:

- close route R1 or bear on P1 directly. It closes one family of *tools* that
  was being tried on R1, in the direction the no-go doc had already established;
- rule out **lossy** summaries. It says no bounded summary is lossless for the
  successor queue. A downstream target that does not need the literal queue —
  only, say, an eventual-periodicity predicate on it — is untouched by this;
- say anything about summarizing the **queue as a whole** across a step. The
  congruence here is on an interior block scanned in isolation, which is the
  object the no-go doc and the quotient doc both work with.

The live question the no-go family was serving remains the one in
`RESULTS-ZERO-PREFIX-LEADING-TERM-EXTEND.md` (zero-prefix greedy lemma,
verified exhaustively to length 23 and adversarially to 2000, still unproved).

## 7. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/syntactic_monoid_injectivity_proof.py
```

Runs in a few seconds; no sampling anywhere, and every printed line is an
assertion that must hold for the run to exit 0.

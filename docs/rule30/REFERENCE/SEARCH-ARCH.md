# Arm 3, iteration 2 — search architecture

Design only. Nothing here is built. Companion to `PREREGISTRATION.md` (the
target) and `RESULTS-arm3-run1.md` (the measured baseline this design reacts to).

## Three corrections to the brief, with the evidence

**The 1.95 exponent threshold fires on constant-factor wins.** Run 1 measured
the 64-bit bit-parallel candidate at alpha_hat = 1.9676. That candidate is plain
forward simulation with a 40x constant factor and no reducibility whatsoever. A
1.95 gate sits 0.017 away from rewarding it. The gate below is the
pre-registered one: alpha_hat < 1.9 sustained over at least three octaves and
held on an out-of-band n.

**The n to n+100 difference quotient is ill-conditioned.** Its denominator is
log((n+100)/n), which at n = 10^6 is about 1e-4, so any local structure in the
cost is amplified by 10^4. Cost is not smooth in n: word counts and loop trip
counts cross integer boundaries. Run 1's two-point estimate over a 2x lever arm
gave 1.9993 for the naive baseline; the same estimator over a 1.0001x lever arm
measures nothing. Exponents are fitted over octaves.

**Do not cap linear memory at o(n).** The tempting move, since forward
simulation needs a Theta(n) row, is to make the row unrepresentable. It narrows
the arm from "beat n^2" to "beat n", which is the prize this program has already
documented as out of reach: an O(n^1.5)-time candidate is a legitimate win under
the variant Wolfram names and carries no space obligation below n. If a space
cap is wanted it must be tied to the target exponent, `space <= C * n^(alpha_target/2)`,
and declared as a separate stricter arm.

One part of the brief needs no correction. Excluding forward simulation from the
grammar does **not** cost the tournament its reference point, because
`crosstalk-lab run` takes the baseline as a committed artifact outside the
search space. The real risk of a narrow grammar is vacuity, handled in 1.4.

---

## 1. Seed grammar

Two sorts only. `Poly` is a multivariate polynomial over GF(2) in the initial-row
variables; `Idx` is a machine integer position or step index. There is no sort
for a row, a generation, or a mutable buffer, so no derivation can name "the
state after step t".

### 1.1 Primitives

```
Idx  ::= n | Lit(k) | Add(Idx,Idx) | Sub(Idx,Idx) | Shl(Idx,k) | Shr(Idx,k)
       | Half(Idx) | Log2(Idx)

Poly ::= Var(Idx)                      -- initial-row cell at a position
       | Zero | One
       | Xor(Poly,Poly)                -- + over GF(2)
       | And(Poly,Poly)                -- * over GF(2)
       | Rule30(Poly,Poly,Poly)        -- p + q + r + qr, the local map
       | Compose(Poly, Shift)          -- substitute Var(i) -> Var(i+Shift)
       | Iterate(Poly, Idx)            -- functional power of a Poly-to-Poly map
       | InvertLeft(Poly, Poly)        -- left-permutive inversion, see 1.3
       | Restrict(Poly, Support)        -- fix Var(i)=0 outside Support
       | Eval(Poly, Init)              -- evaluate under a named initial condition
```

`Init` is a closed enumeration, currently `{ Delta }`, the lone-1 configuration.
`Support` is an `Idx` interval. `Shift` is an `Idx`.

### 1.2 Exclusions, and why each one is structural rather than economic

- **No sequence, array, vector, or memory sort.** There is nothing to index into
  and nothing to write, so a row cannot be materialised.
- **No general recursion and no `while`.** `Iterate` is the only repetition and
  its count is an `Idx` expression, so every program's control flow is a closed
  form in `n`.
- **No `Iterate` over a term containing `Eval`.** This is the specific rule that
  kills forward simulation: stepping a *concrete* configuration repeatedly is
  exactly `Iterate(Eval(...))`. Composition of *symbolic* maps stays legal.
- **No table, constant array, or literal wider than 64 bits.** Enforced twice:
  in the grammar, and by `max_candidate_bytes = 64 KiB` on the challenge file
  (landed in 61f0deb). The center column is published to 10^9 bits, so without
  both a candidate wins by transcription.

### 1.3 The backward-solving primitive

Rule 30 is left-permutive: it is linear in the left neighbour `p`, since
`f(p,q,r) = p + q + r + qr`. Fixing `q` and `r`, the map `p -> f` is a bijection,
so `p = f + q + r + qr`. `InvertLeft(target, known)` denotes exactly this: given
a term for the output cell and a term for the `(q,r)` pair to its lower right,
recover the cell to its left in O(1) algebra.

This is the primitive behind Meier and Staffelbach's 1991 stream-cipher attack
and it is the only demonstrated reducibility anywhere in rule 30. It is the
reason this grammar is worth building. It is also *not* by itself a route to
`a(n)`: inversion propagates a known column leftward and says nothing about a
column you do not have.

### 1.4 Non-vacuity, which is the acceptance test for the grammar

A grammar that cannot express a single correct program produces a search where
every candidate fails the accuracy gate, forever, with no gradient. That failure
looks identical to "no shortcut exists" and would be the worst outcome here.

The grammar is non-vacuous by construction:
`Eval(Iterate(Rule30-as-map, n), Delta)` is the n-step composed polynomial
evaluated at the lone-1 configuration, which is `a(n)` by definition. Naive
composition is worse than quadratic, so this term is a correctness witness, not
a competitor.

**Gate before any search runs:** hand-write that witness plus at least one
`InvertLeft`-bearing program, and confirm both pass bounded equivalence (3.3) at
n = 64. If a human cannot write a correct program in this grammar, the search
cannot find one, and the grammar is wrong rather than the problem being hard.

---

## 2. Fitness

### 2.1 The sealed 64 are a gate, never a gradient

Two independent reasons the brief's Pass 1 cannot be the training signal:

- **No gradient exists.** The output is one bit under a strict boolean match, so
  63/64 and 0/64 score identically. Nothing to climb.
- **Selection leaks the holdout.** Sixty-four cases consulted every generation,
  with survival decided on them, is a training set wearing a holdout's name.
  After enough generations the population has been fitted to the committed
  cases and the commitment certifies nothing.

The sealed set is therefore consulted exactly once, on the final population, as
pass/fail. Everything the search climbs comes from 2.2 and 3.3.

### 2.2 Pass 1, graded correctness from bounded equivalence

Grade a candidate by the largest `n` at which it is provably equivalent to rule
30 over **arbitrary initial rows**, via the SMT check in 3.3:

```
correctness(c) = log2(n_max(c))   where n_max is the largest n with UNSAT
                                  on the disequality, searched by doubling
```

This is strictly stronger than the sealed cases, which only ever exercise the
single lone-1 orbit and so cannot distinguish a general algorithm from one that
happens to be right on that orbit. It is also graded, monotone, and cheap at
small n, which is what an evolutionary loop needs. A candidate with
`n_max < 64` is dead: `fatal_flaws` gets `"bounded-inequivalence at n=<k>"`.

### 2.3 Pass 2, the scaling metric

Only candidates surviving 2.2 are metered. For each octave `n_i` in
`{2^10, 2^11, ... , 2^20}`, run one sealed-commitment tournament with its own
committed case set and record `fuel_consumed`. Fit

```
log(fuel) = alpha_hat * log(n) + c        by least squares over >= 4 octaves
```

and report `R^2` alongside. Run 1's naive baseline gives alpha_hat = 1.9980 with
R^2 = 1.00000, so the instrument is known good to three decimals on a known
exponent.

```
scaling(c) = clamp( (2.0 - alpha_hat(c)) / 0.2 , 0, 1 )        -- 0 at 2.0, 1 at 1.8
```

Continuous, so a candidate drifting from 1.99 to 1.96 is rewarded, but no cliff
at 1.95 hands a prize to a constant-factor win.

### 2.4 The gate that decides a claim

All four conditions, or the result is a speedup and is reported as one:

1. `n_max >= 1024` under bounded equivalence over arbitrary initial rows.
2. `alpha_hat < 1.9` with `R^2 >= 0.99` over at least three consecutive octaves.
3. Holds on an **out-of-band** n, from a freshly committed case set at an octave
   the candidate was never metered on. A candidate whose gains evaporate here
   was fitted to the bands.
4. Passes the sealed 64 at 64/64. Chance floor 2^-64; run 1 showed a
   `solve(n) = 1` cheater scoring 0.53125, which is why the count is 64 and not
   5.

**Kill condition**, unchanged from the pre-registration and expected to fire:
budget exhausted with no candidate meeting 1 through 3. Reported as a negative
result. Publishable, and the honest default.

---

## 3. Mutator and the SMT hook

### 3.1 What Z3 cannot be asked

"This program computes `a(n)` for all `n`" is not an SMT query. It is an
induction obligation over an unbounded family, and it needs an inductive
invariant, which is a proof rather than a decision procedure call. Any design
that routes whole-program correctness through Z3 will either hang or silently
answer a bounded question while reporting an unbounded one.

Worse, the bounded version does not scale where it matters: checking a candidate
against rule 30 unrolled to n steps means a circuit of order n^2 gates, so at
n = 10^6 the check is more expensive than the forward simulation it is trying to
beat. Equivalence checking is a small-n instrument by nature.

### 3.2 What Z3 is for: validating one rewrite

Every mutation is a **local rewrite** `A -> B` on a subterm. Emit SMT-LIB2 over
the free variables of `A` and `B` as booleans, assert the disequality, and
require UNSAT:

```smt2
(set-logic QF_UF)
(declare-fun v0 () Bool) (declare-fun v1 () Bool) (declare-fun v2 () Bool)
(assert (distinct <A-as-bool-term> <B-as-bool-term>))
(check-sat)          ; UNSAT => the rewrite is semantics-preserving
```

Subterm rewrites have few free variables, so these are milliseconds. Shell out
to `/opt/homebrew/bin/z3 -in`, matching the existing subprocess pattern in
`src/engines/formal_verification.rs` (lean, verus, coqc) rather than adding a
crate binding. Apply the same fail-closed discipline that engine already uses:
a missing binary, a timeout, or anything other than a literal `unsat` rejects
the mutation. `sat` or `unknown` are both rejections.

Rewrite rules the mutator draws from, each validated once at registration and
then again per application because the free-variable instantiation differs:

- GF(2) identities: `x+x=0`, `x*x=x`, distribution, `Xor`/`And` associativity
- The rule 30 local map both ways: `Rule30(p,q,r) <-> p + q + r + qr`
- Left inversion introduction and elimination: `InvertLeft(Rule30(p,q,r),(q,r)) <-> p`
- `Compose` fusion: `Compose(Compose(f,a),b) -> Compose(f,a+b)`
- `Iterate` splitting: `Iterate(f, a+b) -> Compose(Iterate(f,a), Iterate(f,b))`,
  the one rule with any chance of changing the exponent, since it is where a
  doubling or square-and-multiply schedule would come from
- `Restrict` propagation, which is how a light-cone bound gets exploited

### 3.3 Bounded equivalence, the graded signal from 2.2

Separate from rewrite validation, and the source of `n_max`. For a fixed n,
unroll rule 30 to n steps as a circuit over `2n+1` free boolean inputs, assert
it differs from the candidate's term, and require UNSAT. Search `n` by doubling
until the first `sat` or a wall-clock cap. Quantifying over the initial row is
what makes this stronger than the sealed cases, which only exercise `Delta`.

Cost note: the unrolled circuit is Theta(n^2) gates, so expect `n_max` in the
hundreds, not the thousands. Condition 1 of the gate asks for 1024, which is
already near the practical ceiling. If Z3 cannot reach it, that condition
weakens to the largest n reachable in the cap and the weakening is recorded in
the report, not quietly dropped.

### 3.4 The limitation this architecture must not hide

Every mutation is semantics-preserving by construction. Since all correct
programs compute the same function, that keeps the search inside the correct
set, which is the point. But it also means the mutator explores an equivalence
class, and **local peephole rewrites will not connect Theta(n^2) forward-style
composition to a sub-quadratic algorithm.** The algorithmic leap is not a
peephole.

So the realistic role of this search is to find cheaper *re-expressions* within
the class, with `Iterate` splitting (3.2) as the only rule whose repeated
application could plausibly restructure the schedule. Fresh algorithmic ideas
have to arrive as new seeds from the LLM proposal arm, which is what the
deliberation engine is for. The evolutionary loop refines and verifies; it does
not invent. Any writeup saying otherwise is overclaiming.

---

## 4. Integration with `crosstalk-evolution`

The engine owns the deterministic policy, lineage, Pareto retention, and
resumable checkpoints. None of that gets rebuilt.

**Candidate representation.** `ConceptDraft` is text-only
(`domain`/`title`/`mechanism`/`rationale`) and generation and evaluation are
caller-supplied traits, so iteration 1 serialises the AST as an S-expression
into `ConceptDraft.mechanism` and parses it back in the generator and evaluator.
The AST is text anyway. No engine change.

**Fitness mapping, and this is deferred debt.** `Fitness` has seven axes built
for idea evolution, and `dominates` runs Pareto over all of them, so a careless
mapping makes retention behave unpredictably. Stated axis by axis:

| axis | program-search meaning | risk |
|---|---|---|
| `utility` | `scaling(c)` from 2.3, the primary driver | none, this is the intended use |
| `feasibility` | `correctness(c)` from 2.2, normalised | weighted 1.5x in `blindmind_compatible_score`, so it outweighs utility |
| `evidence` | fraction of the octave ladder actually metered | fine |
| `safety` | constant 10.0 | inert axis, weakens Pareto discrimination |
| `novelty` | AST edit distance to the nearest ancestor | a proxy for novelty, not novelty |
| `semantic_jump` | constant 0.0 | semantics are invariant by 3.4, so this axis is meaningless here |
| `prior_art_overlap` | constant 0.0 | feeds a `novelty_bonus` of +2.5 to every candidate uniformly |
| `fatal_flaws` | bounded-inequivalence and grammar violations | correct use |

Three of seven axes are inert and `feasibility` outranks the metric the search
exists to optimise. That is a real distortion, not a cosmetic one. Program search
wants its own fitness type with `(correctness, alpha_hat, fuel)`; reusing
`Fitness` is a deliberate iteration-1 shortcut and is logged here as debt.

---

## 5. Build order

Each step has a kill condition, cheapest disconfirming step first.

1. Hand-write the two witness programs from 1.4 and check them with a standalone
   Z3 script. **Kill: no correct program is expressible, so the grammar is
   wrong.** Nothing below is worth building until this passes.
2. Rewrite validator, subprocess plus fail-closed parse. **Kill: registration
   validation rejects a rule believed sound, meaning the term encoding is wrong.**
3. Bounded-equivalence driver and `n_max`. **Kill: `n_max` caps below 64, so 2.2
   yields no usable gradient.**
4. Octave harness, which is `experiments/rule30/sweep.sh` and `fit.py` extended
   upward from n = 4031. Independent of 1 through 3 and can proceed in parallel.
5. Generator and evaluator over `ConceptDraft.mechanism`, wired to the engine.
6. Run, with the gate in 2.4 and the pre-registered kill condition.

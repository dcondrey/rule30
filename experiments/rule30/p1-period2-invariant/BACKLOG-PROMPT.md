# Prompt: generate a backlog of lemmas for Rule 30 Problem 1

Paste everything below the line into a fresh session. It is self-contained;
the file pointers at the end are optional and only apply inside the
`13-rule30` repository.

---

You are generating a backlog of candidate lemmas for an attack on Wolfram's
Rule 30 Problem 1: **the centre column of Rule 30 from a single black cell is
not eventually periodic.** The backlog will be screened by machine, so every
entry must be a precise, finitely testable statement. Ideas without a kill
test are not accepted.

## 1. Where the attack stands

The live attack is period-specific. Constant tails are proved impossible.
Period two has been reduced along a proved chain, each arrow one way:

```text
(PT2)  no nonzero finite configuration y has Tr_0(y) = Tr_0(F^2 y)
  <=  (SEP)  a separation of two orbits in a four-state inverse-cone system
  <=  (DLP) <=> (RW)  the rotated wedge, stated exactly in section 2
```

Proving (RW) proves period-two exclusion. It does not prove Problem 1.

## 2. The exact language

Cells are four-state, `T in {0,1,2,3}`, bits `H = T>>1`, `Lo = T&1`, defect
`E = 1 + H + Lo mod 2`. Binary symbols `{1,2}` are exactly `E = 0`.

A triangle `T[u][d]` is built from endpoint symbols `e_0 .. e_{L-1}`:

```text
    T[u][-u-1] = e_u,   T[u][-u] = e_u XOR 3,
    T[u][d] = phi(T[u-1][d-1], T[u][d-1])   for d > -u
```

`phi` is bijective in its right argument. It decouples exactly:

```text
    H(phi(l,r)) = H(r) + 1 + [l == 0]
    E(phi(l,r)) = E(r) + H(r) * [Lo(l) == 0]
```

Consequently the column map is a fixed 4-state Moore transducer with state
`(h,F) = (H,E)`, reading column `u-1` bottom-up through the 3-letter quotient
`(a,b) = ([T==0], [Lo(T)==0])`, `step(h,F,a,b) = (h+1+a, F + h*b)`, starting at
`(1 - H(e_u), 0)`. The three letters generate the affine group of order 8.
Cells `1` and `3` are indistinguishable as left arguments.

**(RW).** There are no `n >= 1`, `r in {0,1,2}`, `c in {2,3}` and binary
`f in {1,2}^(2n+r+2)` with (1) `f[n:]` hard-core (no `11`) including its
junction with `f[n-1]`; (2) `T[u][n] = c` for every `u in [n, 2n+r+1]`;
(3) `f[-3:-1] = 12`.

**Orbit form** (verified). For `u >= n` the symbol `e_u` is forced by column
`u-1` through `H(T[u][n]) = 1`, and then `E(T[u][n]) = Phi(col_{u-1})` with,
over the window `d in [-u, n-1]` of length `m = n+u`, `Z` = zero cells,
`W2` = cells equal to 2, `N` = nonzero cells:

```text
    H(e_u)     = 1 + (n+u+1) + |Z|                                        (mod 2)
    E(T[u][n]) = (|Z|+|W2|)(1 + m + |Z|) + #{(x,y): x<y, x in N, y in Z or W2}  (mod 2)
```

So (RW) says the deterministic forced map on columns, started from the `2^n`
binary prefixes, never makes `n+r+2` consecutive hits of the half-set
`{Phi = E(c)}` while the forced symbols stay hard-core.

**Diagonal form** (verified). The solution set `{g in {0..3}^L : T[u][n] = c
for all u >= n}` has exactly `4^n` elements, bijectively parametrized by the
main diagonal `T[0][0], ..., T[n-1][n-1]`.

## 3. What is measured (complete search, `n` up to 20)

- No admissible word reaches more than about `0.7n` of the `n+2` hits a
  counterexample needs; the slack has not dropped below 8 since `n = 15`.
- Surviving-prefix counts decay at `1.35 +/- 0.15` bits per column
  (predicted `1 + log2(4/3) = 1.415` under per-column independence).
- The naive bound `N_k <= 2^(n-k)` is FALSE (ratio up to 4 at small `n`);
  any counting lemma must carry a constant.
- Dropping hard-core gives exactly the retired target (BWH+), whose slack is
  1 at `n = 15`. Neither hard-core nor the E-pin alone carries the slack.
- Every early source bit is a one-in-two constraint on survival depth: there
  is no effective forgetting and no bounded-window description.
- `Delta_j = Psi_j + Psi_{j+1}` (the BWH+ defect difference) has full
  algebraic degree `n` in the source bits for every `n` in 4..15: no
  bounded-arity seam law exists for it.

A sufficient rate target: **(RW-alpha)** there are `alpha < 1` and `C` with
no admissible run longer than `alpha*n + C` for all `n`.

## 4. What has been tried. Do not resubmit any of these.

**Direct routes to Problem 1 (PATH.md register).**
R1 zero-set obligation (OPEN, no rule-generic proof possible; the whole
remaining obligation is `r` eventually periodic on `{c_t = 0}`). R2 cascade
descent (KILLED by its own kill condition, determination density decays).
R3 bounded-depth pin bootstrap (KILLED, run-of-ones wedge). R4 anything
anchored at the right boundary (KILLED, `O(log t)` reach). R5 left
permutivity or expansivity alone (KILLED, Rule 90 filter). R6 Kolmogorov or
entropy boundary framings (KILLED, three independent ways). R7 omega-automata
periodicity ladder (STALLED: `p=2` nonempty at every depth reached; depth,
the boundary pin, and the Diff bound all retired; a limitation theorem shows
the phase slip extends to a half-plane).

**Periodicity bridges.** Kopra width-two extension to a nonlinear
left-permutive subclass (KILLED); finite-delay reconstruction of an adjacent
column from the centre (KILLED); centre-trace injectivity (KILLED); doubling
separation `s(p,0) != s(2p,0)` (KILLED); period-independent contradiction
from a periodic centre (KILLED); periodic-mask contraction (KILLED);
inverse-trace continuation (STALLED); phase-labelled prefix-OR latch
(KILLED); extending the constant-trace mechanism to nonconstant periods
(KILLED); stroboscopic descent for `p=2` (OPEN, no descent found);
same-forward-orbit collision reduction (OPEN); alternating-trace fiber
certificates (OPEN, per-`d` certificates cannot reach uniformity); Ore-relation
ladder to non-2-automaticity (OPEN; induction on rungs KILLED); preimage-tree
backward descent (KILLED); trace subshift soficness (NEGATIVE).

**Ergodic, arithmetic, and complexity framings.** Invariant-measure
classification of the vertical orbit closure (OPEN, conditional on
checkerboard patch growth, measured to `2^24`); jointly invariant Markov
measures (STALLED); Anashin 2-adic comoving ergodicity (KILLED); 2-adic
Mahler expansion with Haar unique ergodicity (KILLED, not uniquely ergodic);
2-adic Newton polygon (KILLED); S-adic decomposition plus Morse-Hedlund
factor complexity (KILLED); finite 2-kernel or bounded-rank digit query
(KILLED); ANF/Walsh of the iterated centre-bit function (PROVED, exact degree
`2t-1`, inert for P1); algebraic immunity, AC0/Smolensky, straight-line
length, sensitivity along the single-seed path (all KILLED by obstruction G:
the input is one fixed point); resolution and polynomial-calculus lower
bounds for `c_n` (KILLED); conserved non-additive window functions and
nonabelian transfer invariants (KILLED); Rule 150 plus sparse error
superposition (KILLED); Rowland-Yassawi nonlinear analogue (NEGATIVE).

**Geometric and physical analogies.** Persistent homology, quantum-circuit
entanglement entropy, hydrodynamic PDE limit, non-standard analysis,
homotopy type theory, hyperbolic light-cone embedding, Riemannian curvature
of a multilinear relaxation, spectral dimension of a Dirac operator, OTOC and
random-matrix statistics, braid-group defect world lines: all KILLED, most
by single-column blindness (obstruction C) or the Rule 90 filter.

**Search and ML.** Cryptanalytic bias detection on the trace (no bias
found); ML-guided conjecture mining (refuted at depth 20000); Lean 4 or
evolutionary search for a proof (not run); LLM-driven program search for a
sub-quadratic centre-column algorithm (instrument validated, search not
run; that is P3, not P1).

**Inside the period-two program (exact counterexamples exist for each).**
Fixed-radius additive energy or potential (Farkas contradictions at
localities 1..4, radius-seven negative cycles); fixed finite quotient of the
frontier (same summary, different legal successors; the carry actions are
permutations); raw dyadic period mismatch (`2^omega` maps to accepted
`(12)^omega`); bare holonomy-defect word (identical profiles, different next
rows at length 8; two-ended repair fails at 13); static DFA rank contraction
(survivor DFA grows as `4^(h+1)+1`); literal final local patch (a length-12
control survives with six constant final cells); one backward source defect
(single-coordinate relaxations stay UNSAT; the obstruction is branched);
counting pulls by the initial endpoint `12`; counting arbitrary-queue pivots
(pull depth 3 and 4 witnesses at length ~390); pointwise scale derivative or
matching (exact failure at length 21); the sharp bound `M_c(n) <= n`
(`M_3(15) = 16`); static right-boundary penetration; larger bounded SAT or GA
tables (they falsify candidates, never supply the all-length quantifier);
bounded-arity seam law for `Delta` (full algebraic degree); the target BWH+
itself (slack 1, survivor counts at the independence null then clustering to
18x; retired for RW).

**Five defects that killed 41 of 77 entries in earlier rounds before any
computation.  An entry with any of them is discarded unread.**

1. In the diagonal form every one of the `4^n` diagonals already satisfies
   `T[u][n] = c` for all `u >= n`.  That is the constraint, not a function
   of the diagonal.  Any statement about `E(T[u][n])(x)`, its degree, rank,
   Hamming distance or Jacobian over diagonal vectors `x` is about a
   constant.  The free quantity in diagonal coordinates is the edge defect
   `E(e_u)`; in source coordinates it is the unstopped defect word
   `Psi_n(W)`.
2. `(H, E)` are coordinates on the four-state inverse-cone carry cells.
   Rule 30's forward diagram has binary cells; `H` or `E` of a forward cell,
   or of "the centre column", is undefined.  `T[t][0]` from a seed in the
   triangle is not the centre column.
3. A statement about the ANF, Walsh spectrum, or degree of the indicator of
   the RW counterexample set is a statement about the zero function wherever
   RW holds, and is false exactly when the target is true.
4. An admissible run stops at its first miss, so a hit vector is `1^j 0^*`.
   Word counts, entropies, palindromes and pairwise distances of hit vectors
   are trivial.  Use `Psi_n(W)` (forcing continued past misses) if a
   nontrivial word is wanted, and say so.
5. For `u >= n` the next symbol is forced by the `H` constraint.  "At most
   one of the two symbols continues" is vacuous, and "each hit halves the
   survivors" is false (`n = 9, c = 3`: six survivors persist through four
   consecutive levels).

**Standing obstructions, each must be addressed by name in every entry.**
A: the `O(log t)` wall. B: the Rule 90 filter. C: single-column blindness.
D: naming the missing composition law instead of deriving it. E: the
measure-zero single orbit. F: the free boundary of a fixed-depth strip.
G: complexity measures on a single fixed input are zero. H: finite data
cannot establish an infinite statement.

## 5. Entry format. Every field required.

```text
ID:            short slug
STATEMENT:     precise, in the language of section 2 or a language you
               define completely
IMPLIES:       one of RW-alpha / RW / SEP / PT2 / P1, and the argument for
               the implication (a proved arrow from section 1, or your own)
KILL TEST:     a finite computation that refutes the statement if it is
               false and can plausibly fire; the n range; what a failure
               looks like; concrete enough to implement from this text alone
NEAREST KILLED: the closest item in section 4 and exactly why this differs
OBSTRUCTIONS:  for each of A..H: "not applicable because ..." or
               "evaded because ..."
P_TRUE:        your honest probability
VALUE:         what it buys if true
COST:          rough compute and proof effort
```

## 6. What to generate

Produce 30 to 50 entries across these lenses, at least three per lens:

1. Injection or triangular structure in the diagonal parametrization.
2. Global or ordered potential along the forced orbit (not fixed-radius).
3. `Phi` as an F2 quadratic form: rank, Arf, composition with the Moore map.
4. The composite transducer as a cocycle over the order-8 group; spectral
   gap of the induced transfer operator.
5. Symbolic dynamics: entropy of the `k`-hit language, all-orbits bounds.
6. The hard-core forced-symbol language: transfer matrix, Fibonacci counting.
7. Structured counterexample families to RW or RW-alpha (periodic sources,
   suffix cylinders grown past exhaustive reach, SAT on the diagonal form).
8. Routes to Problem 1 entire that are not period-specific and clear section 4.
9. The R1 zero-set obligation in decoupled `(H,E)` coordinates on the forward
   diagram.
10. Anything else, provided it clears section 4.

Rank the final list by `P_TRUE x VALUE`. An entry that turns out to be a
relabeling of a section-4 item is worth less than nothing; say so and drop it.
Honest low probabilities are fine. Entries whose kill test cannot fire are
rejected.

## 7. Optional file pointers (inside the 13-rule30 repository)

- `experiments/rule30/p1-period2-invariant/uc/BRIEF.md` (this material with
  proofs of the identities)
- `experiments/rule30/p1-period2-invariant/PROOF-STATE-CAPSULE.md`
- `experiments/rule30/p1-period2-invariant/RESULTS-PSI-ANCESTRY-LAW.md`
- `experiments/rule30/p1-period2-invariant/RESULTS-RW-LINEAR-SLACK.md`
- `docs/rule30/PATH.md` sections 7.1, 7.3, 8 (the full register)
- Kernel: `psi_kernel.py` (`Endpoint.peek/append`, `psi`), `rw_margin.py`
  (`deepest`), `psi_column_map.py` (`forced_columns`); run with
  `uv run python` from the arm directory

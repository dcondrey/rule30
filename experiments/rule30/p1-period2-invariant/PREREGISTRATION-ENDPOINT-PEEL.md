# Preregistration: moving-endpoint peel induction

Date: 2026-09-01

## Exact target

Prove the uniform implication

```text
hard-core rho seed of length n survives H post-seed macros
    => H <= 2n+1.
```

This is the contrapositive form of `M(n,2n+2)` being UNSAT for every `n`.
Together with the already-checked bilateral reduction it would prove only the
period-two rung, not arbitrary Rule 30 nonperiodicity or unpredictability.

## Candidate certificate

Use the full ordered frontier, not a fixed summary.  Encode a frontier as the
aligned word

```text
q_j = (A_j, (1 | (B << 1))_j),
```

read deep-to-shallow.  One macro is the exact four-carry Mealy sweep from
`carry_transducer.py`; on a surviving sweep its new shallow terminal symbol is
`3`.  Iterating gives a triangular tableau of all symbols and carry edges.

The candidate is a **one-seed/two-follow endpoint peel**.  Seek an explicit
local rewrite `P` on that whole tableau such that every legal tableau with
parameters `(n,H)`, away from finitely many shallow boundary cases, maps to a
legal tableau with parameters `(n-1,H-2)`.  `P` may carry an unbounded ordered
stack of exposed endpoint symbols.  It may not replace the row by finitely
many counts, moments, `D8` actions, or a bounded endpoint window.

The algebraic checksum for a proposed rewrite is the moving block identity,
for even `w` and `e_i=(i+1) mod 2`,

```text
K_(w+2) = [ K_w   e   e ]
          [ e^T   1   1 ]
          [ e^T   1   0 ],
```

together with

```text
P_(w+2)(x,a,b) = (P_w(x) XOR a XOR b, a XOR b, b).
```

The two post-knee deep outputs are zero.  A successful peel must explain how
those zeros remove the two new endpoint coordinates and must preserve the
pin and no-`11` terminal conditions.

If such a rewrite exists, iterating it reduces a putative `(n,2n+2)` tableau
to a forbidden fixed base case.  Success requires a symbolic proof of the
local commutation rules and exhaustive checking of the finite boundary-rule
table; finite agreement alone is not success.

## Search and resource limits

1. Implement an independent tableau constructor and cross-check every row
   against both `wf_step` and `gray_macro`.
2. Verify the two displayed block identities exhaustively through width 10
   and symbolically entry-by-entry in the result report.
3. Enumerate every hard-core seed through length 18 and its complete legal
   continuation (cap 128, which must not be reached).  Record full tableaux,
   endpoint diagonals, and candidate peel correspondences only; do not extend
   the mortality horizon or run another SAT sweep.
4. Test local peel rules with radius at most 4 in the two-dimensional
   tableau and at most 16 explicit boundary modes.  Total wall-clock budget:
   10 minutes.  Increasing radius, modes, seed length, or runtime after a
   collision is forbidden in this attempt.

## Success and kill conditions

Promote the candidate only if a single rewrite is total on the exact local
tile alphabet, commutes with the macro rule, preserves hard-core/pin legality,
and yields the symbolic `(n,H)->(n-1,H-2)` induction with checked base cases.

Record a negative and stop this certificate class if any of the following
occurs:

- an exact reachable pair has the same proposed radius-4 peel boundary data
  but needs incompatible rewritten symbols;
- a locally legal cycle lets an exposed stack return to the same boundary
  mode without consuming a seed endpoint;
- the rewrite needs radius 5, a seventeenth boundary mode, or a statistic
  whose size grows only by storing the unchanged whole tableau;
- either block identity, transducer cross-check, Rule 30 adversarial control,
  or Rule 90 control fails;
- the rewrite discards the finite-left endpoint or also excludes the known
  infinite-left period-seven wallpaper.

A failure kills only this bounded-local endpoint-peel grammar.  It does not
kill mortality, a genuinely context-free/unbounded peel, or the alternative
eventual-periodicity route.

## Load-bearing controls

- Rule 30 row `{-8,-1,6}` must alternate through `t=14` and first fail at 15.
- Rule 90 row `{-1,1}` must keep zero center through at least `t=128`.
- The right-column Rule 30 identity and no-`11` consequence must pass all
  eight local assignments; its Rule 90 analogue must fail.
- Dropping the post-knee deep-zero requirements must leave surviving models.
- No finite computation will be reported as a proof over all `n`.

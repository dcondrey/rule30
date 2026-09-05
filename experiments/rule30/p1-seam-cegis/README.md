# Z3-first synthesis of the deterministic `(Q, Delta)` seam decoder

Status: **the local phase/holonomy decoder is synthesized and proved exactly;
the recursive interval `Join` law that produces its phase profile remains
open.  This does not prove the period-two rung or P1.**

This experiment acts on the new object requested in the proof-state capsule:

```text
W -> (Q_n(W), Delta(W)),   Delta_j = Psi_j XOR Psi_(j+1).
```

It does not rerun the cocycle-potential or rank-zero endpoint-generator
searches.

## Exact factorization found by CEGIS

Let the affine map exposing output coordinate `j` be

```text
A_j = (a,b,g): (h,l) -> (h XOR a, l XOR b*h XOR g).
```

High-bit elimination gives the suffix symbol directly:

```text
Q_j = 2-a.
```

Write the ordered adjacent holonomy as

```text
D_j = A_j^-1 o A_(j+1) = (x,y,z).
```

The typed grammar `{0,1,a,x,y,z,XOR,AND}` synthesizes the exact seam law

```text
Delta_j = x XOR z XOR (y AND (1 XOR a XOR x)).
```

The stored syntax may have a different but Boolean-equivalent association.
Z3 checks `candidate != exact-group-definition` and returns `UNSAT`.  The
target supplied to Z3 is built by composing the two `D8` phases and comparing
their forced output equality bits; the simplified formula above is not
inserted as an axiom.

The entering phase is load-bearing.  The experiment records a two-assignment
collision with the same `(x,y,z)` and opposite `Delta`, excluding every
phase-free function, not just the enumerated grammar.

## Falsification cascade

Candidates pass through:

1. typed-AST validation (candidate Python is never executed);
2. the current CEGIS example set;
3. a Z3 universal local-schema query;
4. the independent full inverse-cone recurrence on every binary source
   through the requested small-word bound;
5. every split placement in each produced phase profile; and
6. the archived sharp saturator and bounded-summary collision words.

Every rejected CEGIS candidate and its first literal counterexample are saved
in `cegis-result.json`.

The split check here folds the exact ordered phase profile as left-deep,
right-deep, and balanced recursive summaries, and also tests every top-level
binary split.  Every adjacent output defect is isolated at its unique seam
and the decoded output is independent of parenthesization.  It is **not** yet a source-interval
composition theorem.  The missing synthesis target is a recursive `Join`
that derives the phase profile from left/right source summaries while
retaining ordered ancestry, phase, length parity, and dyadic scale.

## Reproduction

The existing `sygus-p3` environment supplies `z3-solver`:

```bash
uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-seam-cegis/run_cegis.py --max-source 9

uv run --project experiments/sygus-p3 python -m unittest discover \
  -s experiments/rule30/p1-seam-cegis -p 'test_*.py'
```

No cvc5, egglog, AALpy, OpenEvolve, or proof assistant is required for this
stage.  OpenEvolve should only be attached after the recursive `Join` grammar
has this same independent evaluator; evolving the already-solved local
decoder would add no information.

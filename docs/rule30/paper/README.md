# Rule 30 zero-tail note

This directory contains a theorem note for the proved finite-support
constant-trace results, with two generated figures and a reproducibility
appendix.  The theorem set is:

- Theorem 2: exact zero-trace fiber for every prescribed right half;
- Theorem 3: exact all-one fiber for every prescribed right half;
- Corollaries 4 and 5: no eventually constant column in any nonzero finite
  Rule 30 orbit;
- Theorems 6 and 7: sharp zero- and one-trace horizons;
- Corollary 8: maximum last constant time `w+1`, equivalently maximum prefix
  length `w+2`, with `2^w` extremizers for even `w` and `2^w-1` for odd `w`.

The constant-one half was added on 2026-08-30:
Theorem 3 (the all-one fiber is a single checkerboard), Corollary 5 (no
eventually constant column), Theorem 7 (the all-one sharp horizon) and
Corollary 8 (the combined sharp law).  Numbering after that insertion is
Lemma 1, Theorem 2, Theorem 3, Corollary 4, Corollary 5, Theorem 6, Theorem 7,
Corollary 8.  Author metadata is set to David Lee Condrey, WritersLogic, Inc.

Both figures are TikZ fragments under `figures/`, generated rather than drawn. Regenerate them with:

```bash
uv run python ../../../experiments/rule30/figures.py
```

Every cell in them is computed by `zero_tail_probe`, and `--check` asserts the
property each figure claims to show (zero center trace on each `C_m` sample,
Rule 90 zero-forever versus Rule 30 escape on the same row, and escape time
`2*ceil(w/2)+1` for every horizon extremizer) before anything is written.

Build from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error zero-tail-note.tex
```

The direct pdfTeX output is retained. It preserves the PDF keywords and is less
than 0.5 MB; all fonts are embedded and subset, and both figures remain vector
graphics.

The executable artifact is `../../../experiments/rule30/zero_tail_probe.py`.
Its exhaustive forward mode is an independent validator; the manuscript's
universal statements rest on the invariant-class proof.

`../../../experiments/rule30/constant_trace_audit.py` audits every numbered
claim in the note against a transcription of equation (1), importing nothing
from this repository on purpose.  It checks Lemma 1's finite form, both fiber
theorems and their single-cell uniqueness, and all three horizon laws
exhaustively for radius `w <= 7`, matching Theorem 7's extremizer set exactly
rather than only its cardinality.  It exits nonzero on any mismatch.

The optional local-schema certificate can be run in an isolated environment
with its dependency supplied explicitly:

```bash
uv run --with z3-solver python \
  ../../../experiments/rule30/zero_tail_smt_certificate.py --json
```

It proves the negations of all finite Boolean proof obligations UNSAT. The
unbounded steps remain the explicit mathematical inductions in the manuscript;
the SMT result is not represented as a full proof-assistant formalization.

`../../../experiments/rule30/Rule30ZeroTail.lean` is a partial formalization.
With a compatible Lean installation, check it with:

```bash
lean ../../../experiments/rule30/Rule30ZeroTail.lean
```

It formalizes the local Rule 30 equation and left permutivity, arbitrary-depth
triangular sensitivity, the prefix-OR closed form conditional on a first
positive right-hand one, the local invariant identities, and the infinite-tail
contradiction conditional on the paper's classification disjunction. It does
not derive that classification from an all-zero trace, and it does not cover
the all-one fiber, the finite-support corollaries, or the sharp horizon/count
theorems. It is therefore not labelled a full machine-checked proof.

The exact command transcript, expected numerical table, audited code commit,
figure checks, and the same Lean coverage statement appear in Appendix A of
the paper. `CITATION-AUDIT.md` records the source-by-source novelty audit.

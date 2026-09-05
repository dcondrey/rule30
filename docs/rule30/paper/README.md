# Rule 30 zero-tail note

This directory contains a six-page theorem note for the proved
finite-support constant-trace results, in six sections with two figures.  It
was four pages before the constant-one half was added on 2026-08-30:
Theorem 3 (the all-one fiber is a single checkerboard), Corollary 5 (no
eventually constant column), Theorem 7 (the all-one sharp horizon) and
Corollary 8 (maximum horizon index `w+1`, hence combined prefix length
`w+2`).  Numbering after that insertion is
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
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress \
   -dSubsetFonts=true -dCompressFonts=true \
   -sOutputFile=compressed.pdf zero-tail-note.pdf && mv compressed.pdf zero-tail-note.pdf
```

The Ghostscript pass takes the file from about 461 KB to about 132 KB. It is
lossless for this document: all 27 fonts stay embedded and subset, the figures
stay vector, and a rendered pixel diff against the uncompressed build is at
antialiasing level (1.3-2.2% of pixels, no structural change). Skipping it
produces a valid but needlessly large PDF.

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

`../../../experiments/rule30/Rule30ZeroTail.lean` is a kernel-checked partial
formalization. With Lean 4.33.1 installed, check it with:

```bash
lean ../../../experiments/rule30/Rule30ZeroTail.lean
```

It formalizes left permutivity, arbitrary-depth triangular sensitivity, the
prefix-OR closed form, the local invariant identities, and the infinite-tail
contradiction conditional on the paper's classification disjunction. It does
not formalize the derivation of that classification from an all-zero trace,
the all-one fiber, either sharp horizon theorem, or the eventual-constant
corollaries, so it is not labelled a full machine-checked proof.

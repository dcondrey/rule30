# ARM7: exact dyadic spacetime grammar

## Status

Promising diagnostic structure, not a Rule 30 shortcut.  Exact dyadic tiles
repeat much more often than in a matched random triangle, but the measured
state vocabulary is still super-polylogarithmic and every current probe first
constructs the full spacetime area.

## Question

Can the Rule 30 center cell be obtained by composing a small exact grammar of
spacetime tiles, rather than evolving every row of its light cone?

The required deliverable is not a smaller file.  It is an exact state type and
a doubling/composition operation that can construct the state for horizon
`2n` from states of size `n`, using `poly(log n)` time and space, followed by an
exact center-cell query.

## Exact probes

`experiments/rule30/spacetime_grammar_probe.py` constructs a power-of-two
square containing the first `n` rows and full width `2n` of the single-seed
spacetime diagram.  It recursively interns equal quadrants.  Node equality is
structural, not hash-probabilistic, and every bit is reconstructed from the
resulting quadtree DAG as an exactness check.

`experiments/rule30/compression_ensemble_probe.py` applies 16 fixed reversible
encodings before zlib, bzip2, and LZMA:

- row order, all whole-square rotations/reflections, diagonal order, and
  Morton/Z-order;
- spatial and temporal XOR derivatives;
- reversible left/right, top/bottom, and transpose symmetry/residual channels;
- a reversible dyadic residual stream, equivalent to adding a scale axis.

Every transform and compressor is round-tripped in the test suite.  The
compressors are only lenses: construction remains quadratic in `n`.

## Measurements

At horizons 64, 128, 256, and 512, exact quadtree-DAG node counts were:

| source | 64 | 128 | 256 | 512 | fitted exponent |
|---|---:|---:|---:|---:|---:|
| Rule 90 control | 21 | 24 | 27 | 30 | 0.171 |
| Rule 22 control | 21 | 24 | 27 | 30 | 0.171 |
| Rule 30 | 210 | 521 | 1,237 | 3,704 | 1.367 |
| deterministic random triangle | 391 | 1,438 | 5,459 | 20,078 | 1.897 |

Extending Rule 30 through horizon 1024 gives 13,304 nodes and raises the fit
over horizons 64--1024 to about 1.48.  Rule 30 therefore has substantial exact
hierarchical reuse, but the observed exponent is increasing and is nowhere
near a demonstrated polylogarithmic state bound.

Across horizons 32--512, the best generic lossless representation was Morton
order.  Its compressed-size envelope grew as approximately `n^1.649` for Rule
30 and `n^1.880` for the random control.  At horizon 512 it used 12,769 bytes
for Rule 30 versus 33,883 bytes for random.  The reversible scale residual and
mirror channels did not win.

A second generic compression pass did not expose another Rule 30 layer.  At
horizon 512 the best Rule 30 chain was 11 bytes larger than the best single
pass; the best random chain was 25 bytes smaller.  Recompression is therefore
closed as a direct mechanism, although compressor scaling remains a diagnostic.

## Direction and symmetry

The reuse is not simple vertical periodicity.  For aligned nonblank tiles of
size 8 through 64, there were no identical adjacent tiles and no repeated
complete horizontal or vertical strips.  Quotienting tile types by left/right
reflection or all eight square symmetries merged no types at these scales.
At scale 4 only, Rule 30 fell from 320 raw types to 310 mirror types and 289
dihedral types.

Unaligned one-dimensional windows do repeat in both directions.  In the
horizon-512 diagram, length-32 nonzero windows gave:

| source | horizontal distinct / observations | vertical distinct / observations |
|---|---:|---:|
| Rule 30 | 168,886 / 277,055 | 174,157 / 291,885 |
| random | 267,546 / 276,100 | 271,088 / 290,809 |

Thus about 39% of Rule 30 horizontal observations and 40% of vertical
observations are repeat surplus, compared with about 3% and 7% in the control.
Length 64 retains a similar separation.  Canonicalizing those long words with
their reversals removes almost no Rule 30 types, so reflection is not the
source of the effect.

For every observed aligned Rule 30 tile at scales 4--64, the full four-edge
perimeter uniquely identified its interior.  This is an exact empirical fact
for the sampled tiles, but the perimeter carries `Theta(scale)` bits and is not
yet a bounded composition state.

## Candidate contract for Crosstalk

A surviving proposal must supply all of the following:

1. A canonical tile or boundary state whose bit size is bounded by
   `poly(log n)`, not a pointer into an empirically enumerated table.
2. An exact operation that composes four child states into their parent, or an
   equivalent exact doubling law.
3. A method to obtain the necessary leaf/input states and the requested center
   bit without generating `Theta(n)` rows or `Theta(n^2)` cells.
4. A proof obligation explaining why the observed Morton/dyadic reuse persists
   for every scale.
5. A deterministic comparison with the bit-parallel oracle on held-out `n`.

The proposal must explicitly differ from these measured failures:

- applying a generic compressor repeatedly;
- relying on horizontal or vertical periodic strips;
- treating mirror/rotation equivalence as the missing compression;
- treating a 3D rendering as new information without a reversible state and
  composition law;
- reporting a subquadratic empirical exponent as if it implied
  `poly(log n)` work.

## Reproduction

From `experiments/rule30`:

```bash
uv run python -m unittest \
  test_compression_ensemble_probe.py \
  test_spacetime_grammar_probe.py \
  test_support_state_probe.py

uv run python spacetime_grammar_probe.py --sizes 64 128 256 512
uv run python compression_ensemble_probe.py --sizes 32 64 128 256 512
```

# TP3-011 residual-SFT rank synthesis

Date: 2026-09-02

Status: **THE ONE PHASE-AWARE ADDITIVE RANK CLASS TESTED HERE IS EXACTLY
UNSAT.  TP3-011 REMAINS OPEN; TP3-001 IS UNTOUCHED.**

## Question tested

After stabilization of the proved eleven-component factor vector, every
hypothetical immortal TP3-011 zero-tail dual orbit lies in the language

```text
L = {w in {0,1,2}* : w avoids 01, 11, and 220}.
```

This is a positive-entropy shift of finite type, not a length bound.  Dual
words grow under the update, so entering `L` does not reduce termination to a
finite-state cycle question.

The four live deterministic states used here are: start, last symbol in
`{0,1}`, a single terminal `2`, and a terminal run of at least two `2`s.
The dead transitions are exactly those completing `01`, `11`, or `220`.

For the current zero-branch phase `d in {0,1}`, the synthesis asks for every
rank of the form

```text
R_d(w) = k_d
       + sum_i weight[d, s_i, w_i]
       + terminal[d, s_final],
```

where all constants, live-edge weights, and terminal weights are
nonnegative integers.  Separate weights for the two branch phases make this
strictly more general than a phase-blind local factor count.

The required inequality is

```text
R_d2(successor(w)) <= R_d1(w) - 1
```

for every `w` in `L` that has two consecutive zero transitions of phases
`d1,d2`.  Every post-initial word begins with `200` or `202`; the product
retains both possibilities rather than relaxing that boundary information.

## Exact decision

The synchronous product tracks:

```text
the first three-bit dual action,
the second three-bit dual action,
the input SFT state,
the successor SFT state,
the prior 200/202 prefix and both branch phases.
```

For each of the eight prefix/phase cases, removal of states that cannot reach
a valid terminal leaves 192 states.  Difference-graph potentials encode the
universal all-word inequality: each graph edge gives a linear lower bound on
the greatest accumulated rank difference, and every terminal is required to
have difference at most `-1`.  This finite integer-linear system is

```text
UNSAT.
```

This is an exact obstruction to the displayed rank class, not a finite word
census and not evidence accumulated over a horizon.  It rules out every
nonnegative additive rank recognized by this four-state SFT with one carried
branch bit and arbitrary terminal potentials.  It does not rule out a
nonadditive rank, a larger automaton state, an ordinal or positional rank, or
termination by a different argument.

The checker is `tp3_011_sft_rank.py`.  It performs the single bounded
synthesis described above; it does not enumerate dual words by length.


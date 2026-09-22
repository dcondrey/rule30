# Periodic prehistory: one transient split, no return certificate

Date: 2026-09-09. Evidence: **M** for the bounded tree shape; **C** for
the complete preimage list at each visited node; **U** for the finite
inverse-state completeness argument below. This does not prove or kill R1.

The target right row is `0` repeated, at centre phase zero. Invert the
driven halfline map

\[
G_a(x)_i=x_{i-1}\mathbin\oplus(x_i\lor x_{i+1}),\qquad x_0=a,
\]

with successive prescribed predecessor boundaries `1,0,1,0,...`.
Words in this report start at spatial cell 1. The run was limited to
depth 12, 60 seconds, and total stored period one million.

| Backward depth | Complete predecessor words | Distinct zero-phase histories |
|---:|---|---:|
| 0 | `0` | 1 |
| 1 | `1` | 1 |
| 2 | `010`, `100` | 2 |
| 3 | `011` | 1 |
| 4 | `001010` | 1 |
| 5 | `101011` | 1 |
| 6 | `101100` | 1 |
| 7 | `000111` | 1 |
| 8 | `000010` | 1 |
| 9 | `111011` | 1 |
| 10 | `010001001010` | 1 |
| 11 | `011101101011` | 1 |
| 12 | `001000101010` | 1 |

Every displayed word repeats spatially and has the displayed length as
its least period. The depth-2 branch `100` has no boundary-1 predecessor;
the branch `010` continues. The depth-12 zero-phase observations, in
chronological order from time -12 to time -2, are `000100`.

For completeness at each node, a target of period N determines a
deterministic backward map on the four pairs `(x_i,x_(i+1))`, using
`x_(i-1)=y_i XOR (x_i OR x_(i+1))`. A right-infinite predecessor supplies
an infinite inverse orbit of this N-step pair map. Every state on such
an orbit lies on a directed cycle: a state outside the cycles has
bounded inverse depth in a finite functional graph. The cycle length
is at most four, so every right-halfline predecessor is purely periodic
with period dividing dN for some d≤4. Its pair `(x_0,x_1)` determines
the whole predecessor, leaving at most two after x_0 is prescribed.
Thus the imported full-line inverse routine also enumerates all these
right-halfline predecessors. This is not a truncated-cone relaxation.

The implementation reuses `all_full_line_preimages` from
`clock40_preimage_collision.py`, rotates between the two coordinate
conventions explicitly, and checks every admitted halfline branch
against the unchanged ladder `FWD[30]` table for two source periods
(164 cells). Its existing full-ring check also runs on every enumerated
preimage. `controls.rule90_control(6)` runs unchanged and passes. The
four-state bound uses left permutivity and is therefore not itself a
Rule30 obstruction; the reported branch transitions use Rule30's OR.

Reproduce:

```sh
uv run python experiments/rule30/r1-isolated-column/periodic_prehistory_tree.py
```

Exact rows, edges, inverse maps, histories, and control results are in
`experiments/rule30/r1-isolated-column/periodic-prehistory-tree.json`.
The surviving finite chain supplies no all-length branching lower bound,
no spatial-word morphism with a proved return, and no infinite prehistory
claim. In particular these counts establish neither an aperiodic
zero-set trace nor eventual periodicity of every trace.

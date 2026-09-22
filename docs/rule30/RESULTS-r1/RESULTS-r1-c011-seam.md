# The c=011 column-2 seam reduction

Date: 2026-09-09. Evidence: **U** (symbolic necessary conditions), **C**
(complete finite Boolean checks and exact periodic witnesses), **R** (the
remaining extension problem). This is an intermediate result for R1. It
does not prove R1 or construct an R1 counterexample.

## 1. Mechanism and the missing condition

Fix the centre column to `c=(011)^inf`. Let `B`, `C`, and `D` denote
columns 1, 2, and 3. Sample column 1 on the centre's zero set:

\[
 a_n=B_{3n},\qquad q_n=1-a_n.
\]

After the first sampled 1, sampled zeros are isolated. On this tail,
column 1 is determined by the samples, and column 2 has the form

\[
 (B_{3n},B_{3n+1},B_{3n+2})=(a_n,1,0),
 \tag{1}
\]
\[
 (C_{3n},C_{3n+1},C_{3n+2})=
 \bigl(q_n\mathbin\oplus q_{n+1},
       1\mathbin\oplus q_{n+1}\mathbin\oplus e_n,
       q_{n+1}\bigr),
 \tag{2}
\]
where a possible seam bit satisfies

\[
 e_n\le (1-q_n)(1-q_{n+1})q_{n+2}.
 \tag{3}
\]

In particular, the only remaining column-2 choice occurs at the final
`11` immediately before a sampled zero. There is at most one such choice
per run of at least two sampled ones. Equations (1)--(3) are **necessary**
conditions for a genuine Rule 30 diagram. The seam bits are not asserted
to be independent, and these equations do not assert that a right
extension exists.

The proposed next mechanism is to propagate the two streams `(q,e)` to
further columns and find an invariant class of streams admitting a
provably aperiodic `q`. Its success condition is a symbolic extension
induction supplying every column, or another compactness argument whose
finite hypotheses have been proved at every depth. Its present stopping
point is exact: (2) describes column 2, but no transformation closing the
class under all further column extensions has been established. A finite
list of allowed seam patterns would not supply that missing induction.

## 2. Symbolic derivation (U)

Use Rule 30 in the form

\[
 X_j(t+1)=X_{j-1}(t)\oplus(X_j(t)\lor X_{j+1}(t)).
 \tag{4}
\]

The OR pin is

\[
 X_j(t)=1\quad\Longrightarrow\quad
 X_j(t+1)=1\oplus X_{j-1}(t).
 \tag{5}
\]

Every calculation below uses the OR rule, including its saturation at
1. The equations are independent of the initial right tail.

### 2.1. The sampled factor 100 is impossible

Translate time by a multiple of 3 and suppose `B_0=1` and `B_3=0`.
Equation (5) gives `B_1=1` and `B_2=0`. Equation (4) at column 1,
time 2, then gives `C_2=1`. Consequently

\[
 C_3=1\oplus B_2=1,
 \qquad B_4=0\oplus(0\lor C_3)=1,
 \qquad B_5=0.
\]

Two more pins give `C_4=1 xor B_3=1` and
`C_5=1 xor B_4=0`. Thus

\[
 B_6=1\oplus(B_5\lor C_5)=1.
\]

Therefore `a_n a_(n+1)=10` forces `a_(n+2)=1`. If a sampled 1 has
occurred, a later `00` would have a first such occurrence and hence be
preceded by a 1, contradicting this rule. Thus no `00` occurs after the
first sampled 1. If no sampled 1 ever occurs, the sample word is simply
`0^inf` and this tail reduction is unnecessary.

### 2.2. Column 1 has block (a,1,0)

At a block starting with `a=1`, two applications of the pin give `110`.
If `a=0`, the no-`00` condition gives the next sample `b=1`. The update
from phase 2 to this next sample forces `B_2=C_2=0`. If also `B_1=0`,
the first two updates force `C_0=0` and `C_1=1`; the pin at `C_1=1`
would then give `C_2=1 xor B_1=1`, a contradiction. Hence this block is
`010`, proving (1).

Here and below subscripts 0, 1, and 2 inside a block denote its three
time phases. They can be replaced throughout by `3n`, `3n+1`, and
`3n+2`.

### 2.3. First possible column-2 blocks

For adjacent samples `a,b`, equation (4) gives `C_2=1-b`. If `a=0`,
it also gives `C_0=1`. The pin at `C_0=1` gives `C_1=1-a`, and the
pin at `C_1=1` forces `C_2=0`. Thus the initial list is

| Samples `ab` | Possible `C` block before checking column 3 |
|---|---|
| `01` | `110` |
| `10` | `001`, `101` |
| `11` | `000`, `010`, `100` |

This table is obtained from the local equations, rather than inferred
from sampled frequencies.

### 2.4. Column 3 removes two blocks and locates the seam

For `ab=10`, suppose the `C` block were `001`. The updates where `C`
is zero force `D_0=1` and `D_1=0`. But the pin at `D_0=1` would give
`D_1=1 xor C_0=1`. Thus this block is impossible.

For `ab=11`, suppose the `C` block were `100`. Its phase-1 update
forces `D_1=1`. The pin would give `D_1=0` if `D_0=1`, so `D_0=0`.
Since the current sample is 1, the immediately preceding update at
column 1 forces both preceding phase-2 bits `B_-1=C_-1=0`. The update
from `C_-1=0` to `C_0=1` then forces `D_-1=1`. Its pin gives `D_0=1`,
a contradiction. This argument uses an earlier time, so it is applied
only to blocks starting at time at least 3.

The remaining table is therefore

| Samples `ab` | Necessary `C` block |
|---|---|
| `01` | `110` |
| `10` | `101` |
| `11` | `000`, `010` |

Finally, suppose an `11` block uses `C=000`. Its first two updates
force `D_0=D_1=1`. The pin at `D_1=1` gives `D_2=1`, while the
phase-2 update gives `D_2=C_next,0`. Thus the next `C` block starts
with 1. In the remaining table, with next first sample `b=1`, that
requires the following sample to be 0. Consequently `C=000` is possible
only over the sampled triple `110`.

If `n_0` is the first sampled 1, all these conclusions hold for every
`n >= max(n_0,1)`. Set `e_n=1` precisely when this `C` block is `000`.
The last table and the `110` restriction give (2)--(3) directly. This
establishes the stated necessary conditions uniformly on the tail.

## 3. Pulse interpretation and the extension gap (R)

Subtracting the periodic column-2 background `010` by XOR turns (2) into

\[
 \bigl(q_n\oplus q_{n+1},\ q_{n+1}\oplus e_n,\ q_{n+1}\bigr).
\]

A sampled zero at index `z`, with neighbouring sampled zeros at least
three indices away, therefore has the following local description:

| Block index | Column-2 block |
|---|---|
| `z-2` | `010` or `000` |
| `z-1` | `101` |
| `z` | `110` |

Away from these event blocks, column 2 is `010`. This identifies where
the background changes and where the sole possible column-2 choice
sits. It does not make arbitrarily separated events feasible: later
columns can constrain both the event separations and the seam choices.

A renormalization that simply returns an actual farther-right spatial
column to a periodic drive would not produce a counterexample. Together
with the fixed periodic centre, that would enclose column 1 between two
eventually periodic columns; the finite-strip argument in
[RESULTS-r1-isolated-column.md](RESULTS-r1-isolated-column.md) would make
column 1 eventually periodic. A useful construction must preserve
nonperiodic information in the farther-right columns, for example through
a closed evolution of the defect streams. No such closure is proved
here.

The named obstruction for this step is the **column-extension seam
closure gap**: a necessary description at one additional
column does not provide a compatible infinite succession of additional
columns. This is an unresolved sufficiency problem, not a refutation of
the construction route or of R1.

### 3.1. Exact nonsufficiency witness (U supported by C)

The candidate `a=(01)^inf`, with all `e_n=0`, satisfies (1)--(3). Those
equations give the period-6 column words

```text
B = 010110
C = 110101
```

Nevertheless this candidate has no Rule 30 right extension. This is the
smallest nonconstant sample period; no assertion is made here about the
shortest infeasible finite prefix. The following finite graph argument
checks arbitrary next-column traces, including nonperiodic traces.

For two known period-6 column words `L,M`, let a graph vertex be
`(t mod 6,N_t,O_t)`, where `N,O` are the next two columns. A directed
edge to `(t+1 mod 6,N_(t+1),O_(t+1))` is present exactly when

\[
 M_{t+1}=L_t\oplus(M_t\lor N_t),\qquad
 N_{t+1}=M_t\oplus(N_t\lor O_t),
\]
\[
 O_{t+1}\in\{N_t\oplus(O_t\lor b):b\in\{0,1\}\}.
\]

Every actual right extension traces an infinite path in this graph.
The last equation allows the next bit to its right independently at
every time, so this graph is an overapproximation; it cannot exclude an
actual diagram by imposing a periodic right-tail assumption.

A vertex that belongs to no directed cycle can occur at most once on
any path. Thus every infinite path eventually visits only cyclic
vertices. If all cyclic vertices at phase `t` agree on `N_t`, the next
column is forced eventually to the corresponding period-6 word.

The verifier constructs each graph from its defining equations, with
all 24 vertices, and finds the following exact results:

| Known `L` | Known `M` | Edges | Cyclic vertices | Forced eventual next column |
|---|---|---:|---:|---|
| `010110` | `110101` | 30 | 9 | `101100` |
| `110101` | `101100` | 27 | 7 | `100100` |
| `101100` | `100100` | 24 | 6 | `100001` |
| `100100` | `100001` | 24 | 0 | No infinite path |

At each stage one may discard a finite initial time interval and use
the forced periodic columns in the next graph, keeping the same time
phase. The last graph is acyclic, which is incompatible with a right
extension for all future times. This proves the candidate impossible
and explicitly demonstrates that (1)--(3) are insufficient. It does not
show that all other sample words are impossible.

The finished argument passes a further Rule 90 check. The same centre
and right trace `c=011011`, `B=010110` occur in an exact Rule 90 torus
of width 30 and time period 6. It is generated by the Rule 90 column
recursion `next(t)=current(t+1) xor previous(t)`, stopping on return to
the initial pair. The verifier records all six actual initial/time rows
in `verification.json` and checks all 180 local updates. Thus Rule 90
realizes the alternating sampled word refuted here for Rule 30.

## 4. Exact periodic backgrounds (C)

Both constant sample words occur in the following Rule 30 torus, with
rows indexed by time and columns by space:

```text
010011111000
111110000100
100001001111
```

The next time row after the third is the first. All 36 local updates
are checked directly with the Wolfram truth table.

| Centre index, starting at 0 | Centre trace | Right trace | Sample word |
|---|---|---|---|
| 0 | `011` | `110` | `1^inf` |
| 9 | `011` | `001` | `0^inf` |

Thus neither constant sample regime is contradictory. The second witness
also illustrates why the no-sampled-1 case is separate: its right trace
does not have the form (1).

## 5. Independent Boolean checks and Rule 90 control (C)

The new verifier uses direct truth-table lookup
`(rule >> (4*left + 2*centre + right)) & 1` and complete shrinking cones.
It does not import or modify the frozen ladder, `numeric_rho`, or
terminal-period engines. Its initial right bits are ordered from site 1
toward increasing spatial coordinates. The centre is driven by `011`.

For the `100` lemma it checks all 128 initial rows of width 7 through
time 6, with samples at times 0, 3, and 6:

| Sample word | Rule 30 initial rows | Rule 90 initial rows |
|---|---:|---:|
| `000` | 12 | 16 |
| `001` | 20 | 16 |
| `010` | 12 | 16 |
| `011` | 20 | 16 |
| `100` | 0 | 16 |
| `101` | 24 | 16 |
| `110` | 28 | 16 |
| `111` | 12 | 16 |

Rule 90 realizes the supposedly forbidden sample prefix `100` from
the explicit initial right prefix `1001000`. Thus already the first
Rule 30 lemma fails for the control rule, as its use of OR saturation
requires.

For the seam formula the verifier checks all 1,024 width-10 initial
rows through time 9. It retains windows whose samples at times 0, 3,
6, and 9 have no `00`, and checks the block at times 3, 4, and 5.

| Check | Rule 30 | Rule 90 |
|---|---:|---:|
| Retained initial rows | 768 | 512 |
| Failures of (1) | 0 | 384 |
| Failures of the reduced column-2 table | 0 | 320 |
| `C=000` outside sample triple `110` | 0 | 64 |
| Failures of (2)--(3) | 0 | 352 |

For Rule 30 the retained table counts are `01:110` = 192,
`10:101` = 320, `11:000` = 144, and `11:010` = 112. Counts enumerate
initial cone rows, not distinct infinite extensions. For Rule 90 the
all-zero width-10 right prefix already violates the reduced table:
its sampled word is `0110` and its checked column-2 block is `110`
above the sample pair `11`.

The unchanged `controls.rule90_control(6)` is also run. Its `T=2,4,6`
checks all report `L90_bijective=true` and `torus_ok=true`. The control
file SHA-256 recorded by this run is
`3e5da3ab9db71aaccc44cefda80cb5f08f780b3ae3fb11bff78f98d5efd3301a`.

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/r1-c011-seam/verify.py
```

The exact output is
[verification.json](../../experiments/rule30/r1-c011-seam/verification.json).
The finite checks independently calibrate the symbolic derivation. The
uniform claims in section 2 follow from the displayed local equations
with arbitrary time translation, not from extrapolating these counts.

## 6. Scope

Established: necessary tail constraints for the fully specified periodic
centre `011`, a column-2 pulse formula with localized possible seam bits,
two exact periodic backgrounds, an explicit nonsufficiency witness for
the formula, and explicit failure of the Rule 30 constraints for Rule 90.

Not established: sufficiency of (1)--(3), an all-depth extension map,
existence or nonexistence of an aperiodic sample word in this fibre, R1,
or the lone-seed P1 claim. No bounded history of the centre is asserted
to determine the neighbour. These are constraints on an entire diagram
conditioned on a specified periodic centre, so they do not decide eventual
periodicity of an unknown word from a bounded window. No geometric or
averaged statistic is proposed, and the single-column overwrite test has
no statistic to evaluate here.

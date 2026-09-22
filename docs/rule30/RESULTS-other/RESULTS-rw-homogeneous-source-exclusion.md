# Homogeneous sources and two mixed families are excluded from the rotated wedge

Date: 2026-09-13. **An all-length restricted-family exclusion is proved.**
No rotated-wedge witness has source `W=1^n` or `W=2^n`, for any `n>=1`,
either constant cut target `c in {2,3}`, or any residue `r in {0,1,2}`.
Exact prefix rewrites also exclude `W=12^(n-1)` for `n>=3` and
`W=212^(n-2)` for `n>=4`.
The proof retains the complete constant-cut equality and the hard-core
junction. It does not prove the general rotated-wedge statement, its
separator consequence, or period-two exclusion.

## 1. Exact target and notation

Use the [rotated-wedge formulation](../../experiments/rule30/p1-period2-invariant/RESULTS-DLP-ROTATED-WEDGE.md).
Let `I` be the inverse-terminal diagonal, `T=I^(-1)`, and

```text
P(x)_i = phi(x_i,x_(i+1)),       F = T o P o I.
```

A witness would consist of

```text
n>=1, r in {0,1,2}, c in {2,3},
f=WQ in {1,2}^(2n+r+2),
|W|=n,       |Q|=m=n+r+2,
Q hard-core including its junction with W,
f[-3:-1]=12,
P^n(I(f)) = c^m.                                           (RW)
```

Hard-core means avoiding `11`. The terminal condition is the nonfinal pull
`12a`, where `a in {1,2}`. No intermediate constant-cut cell is omitted.
The conjugacy makes the final equality exactly

```text
F^n(f)=T(c^m).                                               (1)
```

The restricted theorem below proves more than needed for these two source
families: constancy and the hard-core junction already contradict each other,
so the terminal pull need not be invoked in the last step. It remains part
of the stated RW domain.

The local data, in state order `0,1,2,3`, are

```text
B = (3,2,1,0),
phi = [ [0,1,3,2],
        [3,2,1,0],
        [3,2,0,1],
        [3,2,1,0] ].
```

Every row of `phi` is a permutation. Both `I` and `T` preserve finite
prefixes, and their first output is `B` of the first input.

## 2. Constant-prefix sections and exact restart maps

The [endpoint restart proof](../../experiments/rule30/p1-period2-invariant/RESULTS-ENDPOINT-RESTART-COCYCLE.md)
establishes

```text
F(2e)=r_2(e_0) . F(e),       r_2=(1,0,2,3).                 (2)
```

The same local square yields the conditional leading-one section

```text
F(11v)=1 . F(1v).                                           (3)
```

For completeness, the endpoint-prefix grammar is

```text
I(qe)=(B(q),a) . P(I(e)),       a=phi(q,B(e_0)).
```

An output `s . F(e)` is justified whenever

```text
B(s)=phi(B(q),a),       phi(s,z)=phi(a,z) for every z.
```

For (3), `q=e_0=s=a=1`; both equalities follow directly from the displayed
local table. For (2), the four choices of `e_0` give `s=r_2(e_0)` and the
same two identities. These local equalities prove the arbitrary-suffix
sections; finite-word checks are not being used as an induction.

Define the length-preserving map

```text
R_a(v)=F(av),       a in {1,2}.
```

Equations (2)--(3), with `r_2(2)=2`, imply

```text
F(a^k v)=a^(k-1) R_a(v),       k>=1,
F^t(a^n Q)=a^(n-t) R_a^t(Q),   0<=t<=n.                    (4)
```

The second identity follows by induction on `t`. It preserves the entire
unshown suffix, even when a restart map produces states `0` or `3` there.
Thus the homogeneous-source equality (1) is exactly

```text
R_a^n(Q)=T(c^m).                                             (5)
```

## 3. The source `1^n`

The first output of `R_1` is the permutation

```text
r_1=(0,1,3,2).
```

The hard-core junction from the final source symbol `1` forces `Q_0=2`.
Consequently (4) gives

```text
(F^n(1^n Q))_0 = 2 if n is even, and 3 if n is odd.           (6)
```

But `(T(c^m))_0=B(c)` is `1` for `c=2`, and `0` for `c=3`. This
contradicts (5) for every `n,r,c`, proving the exclusion of `W=1^n`.

More generally, the first-change marker has the uniform prefix law

```text
F^t(1^k 2v) begins 1^(k-t) d_t,
d_t=2 for even t and 3 for odd t,       0<=t<=k.
```

Once that marker has reached the first coordinate, further applications
depend on the following ordered symbols. This law alone supplies no general
mixed-source induction.

## 4. The source `2^n`

For a finite word `w`, the equation `R_2(v)=w` has a unique solution of the
same length. One construction fixes the first cut symbol to `B(2)`, solves
`P(x)=I(w)` from left to right using the permutation rows of `phi`, and then
sets `2v=T(x)`. This proves existence and uniqueness without enumeration.

Call the inverse map `H=R_2^(-1)`. It preserves prefixes: solving the first
`L` coordinates of the lift reads only the first `L` coordinates of `w`.
Equivalently, by (2), it is the existing autonomous restart map determined by

```text
v_0=r_2^(-1)(w_0),       F(v)=w[1:].                          (7)
```

Thus (5) with `a=2` forces the **actual** continuation

```text
Q=H^n(T(c^m)).                                               (8)
```

When `m>=5`, prefix preservation gives

```text
Q[:5]=H_5^n(T(c^5)),                                        (9)
```

where `H_5` is the exact restriction to five-symbol words. Equation (9)
retains full ancestry through the unique inverse branch; it does not replace
the continuation by a fresh completion.

The finite autonomous orbits of (9) have the following exact certificates:

| Constant target | Initial five-symbol word | Preperiod | Period | Hard-core states anywhere in the orbit |
|---|---|---:|---:|---:|
| `2` | `12003` | 0 | 32 | 0 |
| `3` | `01021` | 0 | 16 | 0 |

The full ordered cycles are saved in the artifact. Every state is distinct
before returning to the initial state; each transition is checked by the
forward identity `R_2(H_5(w))=w`. None is a word over `{1,2}` avoiding `11`.
Because `H_5` is an exact autonomous map, its return proves by induction
that the orbit repeats forever. This is a finite proof of the all-iterate
claim, not extrapolation from a bounded orbit prefix.

The period-32 tail-2 quotient was previously established for the exceptional
zero-cut restart fiber. Here it is applied directly to (8); the tail-3
period-16 quotient supplies the second constant target.

For tail `3`, the two-symbol quotient already suffices: its exact orbit is
`01 -> 11 -> 02 -> 13 -> 01`, containing no hard-core state. The five-symbol
cycle is retained as a direct control at the same width as the tail-2 proof.

The only cases with `m<5` are displayed below. They are the unique
continuations from (8), and each already fails hard-core legality.

| `n` | `r` | `c` | Forced `Q` |
|---:|---:|---:|---|
| 1 | 0 | 2 | `003` |
| 1 | 0 | 3 | `110` |
| 1 | 1 | 2 | `0032` |
| 1 | 1 | 3 | `1100` |
| 2 | 0 | 2 | `1013` |
| 2 | 0 | 3 | `0210` |

Together with (9), this proves the exclusion of `W=2^n` for all `n,r,c`.

## 5. Two mixed families by exact prefix erasure

The [endpoint section proof](../../experiments/rule30/p1-period2-invariant/RESULTS-ENDPOINT-SECTION-MACHINE.md)
establishes the arbitrary-suffix identities

```text
F^3(122v)=F^3(222v),
F^3(2122v)=F^3(2222v).                                      (10)
```

They also admit a direct local cut proof, independently checked here. The
inverse-diagonal recurrence shows by induction that `I(f)_j` depends only on
endpoint coordinates `floor(j/2),...,j`. In the first identity the changed
endpoint coordinate is zero, and in the second it is one. Computing the
affected cut prefixes therefore gives

```text
I(122v)=221z,       I(222v)=121z,
I(2122v)=1002z,     I(2222v)=1212z,                           (11)
```

with the same suffix `z` within each pair. For the first pair, two Peels
leave prefixes `3` and `1` followed by an identical suffix; the third merges
them because `phi(3,s)=phi(1,s)` for every `s`. For the second pair, the
first Peel leaves `303` and `121` before a common suffix. The second leaves
`32` and `12` before a common suffix, using that same row equality. The third
again merges the complete cuts. Conjugacy with `T` proves (10).

If a source begins with `122`, the first rewrite is entirely inside `W`
when `n>=3`. Applied to `W=12^(n-1)`, it produces `2^n`. Similarly, the
second rewrite takes `W=212^(n-2)` to `2^n` when `n>=4`. Applying the
remaining `n-3` powers of `F` preserves the complete equality (1). Each
rewrite also preserves source length, its final symbol `2`, the exact
continuation `Q`, the hard-core junction, and the terminal `12a`. Thus any
RW witness in either mixed family would give a homogeneous-source witness,
contradicting section 4.

These are **anchored prefix** rules. They do not justify substitution at an
arbitrary source position. For example, with `n=5`, `r=0`, and the same
continuation `Q=1212121`, both `22122Q` and `22222Q` satisfy the binary,
hard-core-junction and terminal-pull predicates, but their complete cut rows
are respectively

```text
P^5(I(22122Q)) = 2321330,
P^5(I(22222Q)) = 3021330.                                  (12)
```

Neither cut is constant. Equation (12) refutes only the unrestricted
context rewrite `22122 -> 22222`; it is not a counterexample to RW or to a
possible implication that additionally assumes full constant-cut equality.

## 6. Scope and exact verification

This excludes both homogeneous source families and the two mixed families
of section 5 in the full RW domain.
It does not exclude arbitrary binary sources, arbitrary hard-core sources,
or all actual endpoint-derived sources containing several runs. It supplies no
bound on their number of runs or on the length of a hypothetical separator
collision. The two constant-tail separators and period-two exclusion remain
open.

The conditional section (3) also sharpens a local obstruction: for any
nonconstant binary word whose first change is `a^k b`, its first Peel/Craig
image begins `a^(k-1)3` if `a=1`, and `a^(k-1)0` if `a=2`. Hence `F(f)` is
binary exactly when `f` is constant. A direct replacement `f'=F(f)` can
preserve the constant-cut equality while destroying binary-source legality.
This rules out that unqualified local induction, not an induction retaining
additional ordered state.

Run:

```text
uv run --offline --no-project python experiments/rule30/rw_homogeneous_source_exclusion.py
```

The [verifier](../../experiments/rule30/rw_homogeneous_source_exclusion.py)
uses the explicit local table and a literal finite inverse-cone diagonal.
It checks the proof-level section squares, both complete autonomous cycles,
and all six short cases. Small arbitrary-suffix and homogeneous-source
controls compare the identities with direct `F` iterations, including the
complete constant row. The [artifact](../../experiments/rule30/rw-homogeneous-source-exclusion.json)
records the exact cycles, check totals and source hashes. No horizon census,
SAT sweep, fresh original-frontier enumeration or paid compute is used.

The verifier independently reproduces all three initial quotient words and
all 52 cycle transitions with the older inverse-feed `terminal_cone` and
`endpoint_restart_cocycle.tail_step` implementations. Their source hashes are
included. This supplies a second implementation of the complete finite
cycles underlying the proof.

The prefix-erasure checks include complete local coalescence certificates
with an arbitrary shared cut suffix, bounded direct comparisons through both
coordinate systems, and the exact failed-context witness (12). The finite
coalescence closure, rather than the bounded word comparisons, proves the
arbitrary-suffix rewrite identities.

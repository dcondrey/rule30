# The Psi ancestry law: exact composition law for the binary wedge

Date: 2026-09-02

Status: **EXACT LAW DERIVED AND EXHAUSTIVELY VERIFIED.  `(PSI)`, `(BWH+)`,
`(PT2)` and P1 ALL REMAIN OPEN.**  Nothing here proves period-two exclusion.
This report supplies the object `PROOF-STATE-CAPSULE.md` section 7 asks for
("derive an exact composition/ancestry law for the deterministic pair
`W -> (Q_n(W), Psi_n(W))`") and measures the margin any proof must clear.

## 0. What is claimed, and at what strength

| # | Claim | Level | Artifact |
|---|---|---|---|
| 1 | `O(L)` incremental kernel for the forced continuation, replacing the `O(L^3)`-per-source reference | `U` (derivation) + `C` (gate) | `psi_kernel.py` |
| 2 | `phi` decouples into two parity accumulations in `(H, E)` | `U`, exhaustive over all 16 argument pairs | `psi_structure.py` |
| 3 | Parameter-free column integrals `(H)` and `(E)` | `U` (derivation) + `C` to `n=8` | below, `psi_column_map.py` |
| 4 | Closed form for `Psi` as a single parity count, no free constant | `U/C`, exact to `n=10` | below |
| 5 | The column map is a fixed **4-state Moore transducer** over a **3-letter** quotient alphabet, uniform in `n` and `u` | `U/C`, 17,410 columns | below |
| 6 | The margin `(PSI)` must clear is exactly one position, and it is attained | `C`, exhaustive to `n=18` | below |
| 7 | The `[0,n]` column window is **not** a sufficient state; the deficit is exactly one bit per step | `K`, exact conflicts | `psi_column_map.py` |

`U` = uniform identity, `C` = finite exact certificate, `K` = exact
counterexample, as in `PROOF-STATE-CAPSULE.md`.

## 1. One triangle, not two

The reference pipeline composes `inverse_terminal_cone` with `peel_power`,
which reads as two unrelated recurrences.  They are one.  Writing
`T[u][d]` for the cell at endpoint index `u` and depth `d`:

```text
    T[u][d] = phi(T[u-1][d-1], T[u][d-1])          d > -u
    T[u][-u-1] = e_u                                (the endpoint symbol)
    T[u][-u]   = phi(3, e_u) = BOUNDARY[e_u] = e_u XOR 3
```

Negative `d` is the `inverse_terminal_cone` triangle and non-negative `d` is
the peel triangle; the identification is `B[k][i] = T[i][-k]`.  The virtual
left parent at the wedge edge is the constant state `3`.  `psi_kernel.py`
exploits exactly this to update one column in `O(L)` instead of `O(L^2)`, and
is gated against the reference on 1,022 binary sources, 21,844 arbitrary
four-state endpoints, and the recorded `n=15` falsifier.

## 2. The rule decouples

With `E = 1 + H + Lo`, exhaustively over all 16 argument pairs:

```text
    H(phi(L, R)) = H(R) + 1 + [L == 0]
    E(phi(L, R)) = E(R) + H(R) * [Lo(L) == 0]
```

`H` sees the left parent only through the indicator `[L == 0]`.  `E` sees it
only through `[Lo(L) == 0]`, and is gated by the *right* parent's `H`.  Neither
`E` nor `Lo` of the left parent feeds `H`.  This is the decoupling that makes
everything below closed-form.

## 3. The column integrals, with both constants eliminated

Integrating down a column from the wedge edge, and using `E(e_u) = 0` for
binary `e_u` (both `1` and `2` have `E = 0`, and the virtual `3` contributes
nothing because `Lo(3) = 1`):

```text
    H_u(d) = H(e_u) + (d + u + 1) + #{d' in [-u, d) : T[u-1][d'] == 0}     (H)
    E_u(d) =                        #{d' in [-u, d) : H_u(d') & ~Lo(T[u-1][d'])}  (E)
```

`(E)` has **no free constant**.  Verified on 134,642 cells over all binary
sources to `n = 8`.

Two consequences are immediate and both are new in explicit form.

**The forced continuation symbol has a closed form.**  The high-bit forcing is
`H_u(n) = 1`, so by `(H)`

```text
    H(e_u) = 1 + (n + u + 1) + #{d in [-u, n) : T[u-1][d] == 0}
```

i.e. `Q_n(W)_j` is a parity of the number of zero-cells in one column window.
The capsule records `Q_n` as "uniquely determined"; this says what it is.

**`Psi` is a single parity count.**  Setting `d = n` and `u = n + j`:

```text
    Psi_j = #{d in [-(n+j), n) : H_{n+j}(d) = 1 and Lo(T[n+j-1][d]) = 0}  mod 2
```

Exact for all binary sources to `n = 10` (2,046 sources, zero failures).  This
is the "ordered ancestry of the `E` defect" the capsule section 3 names as the
likely proof object, now written down rather than described.

## 4. The column map is a fixed 4-state Moore transducer

Quotient a cell to `(a, b) = ([T == 0], [Lo(T) == 0])`.  This is 4-to-3:
state `0 -> (1,1)`, state `2 -> (0,1)`, states `1` and `3` both `-> (0,0)`.

Then `(H)` and `(E)` say precisely that column `u` is the output of a Moore
machine with state `(h, F) = (H_u(d), E_u(d))` reading column `u-1`'s quotient:

```text
    emit(h, F) = ( [h == 0 and F == 1] , [h != F] )
    step(h, F, a, b) = ( h XOR 1 XOR a , F XOR (h AND b) )
    initial state at d = -u:  (h, F) = (1 - H(e_u), 0)
```

Four states, three input letters, uniform in `n` and `u`, emitting
`|input| + 1` letters.  Verified on 17,410 columns over all binary sources to
`n = 9`, zero failures.

**The map factors through the quotient.**  Column `u`'s full four-state content
is recovered from column `u-1`'s *three-letter* quotient plus one initial bit.
The distinction between cells `1` and `3` is never needed.

**Correctness cross-check against known structure.**  The three input letters
induce three maps on `(h, F)`: `(1,1)` is the shear `F -> F + h`, `(0,0)` is the
translation `h -> h + 1`, and `(0,1)` is their composite.  Shear and
translation each have order 2 and their product has order 4, so the transition
monoid is the group of order 8.  That reproduces the affine `D8` recorded in
`PROOF-STATE-CAPSULE.md` section 3 from an independent derivation, which is a
check on this one, not a new finding.

## 5. What this does not do

**It does not prove `(PSI)`.**  The transducer is fixed but its input word
grows with `u`, so iterating it `n` times is not a bounded quotient, and the
capsule's section 5 row "static formula/DFA rank contraction" (survivor DFA
size expanding as `4^(h+1)+1`) still applies to the composite.

**The `[0, n]` window is not a sufficient state, and the deficit is exactly one
bit.**  `(H)` is autonomous on `[0, n]`: the whole `H` profile of column `u` is
a function of where column `u-1` is zero, with no reference to `d < 0`.  `(E)`
integrated from `d = 0` instead of `d = -u` keeps one constant, `E(T[u][0])`,
and that constant is *not* a function of column `u-1` restricted to `[0, n]`.
Exact conflicts at `n = 2`: the column `(2,1,2)` continues to both `(3,1,2)`
and `(2,0,3)`, with seed defect `1` and `0` respectively.  So the growing
negative-depth tail is load-bearing for exactly one bit per step, and no more.
This is a sharpening of the capsule's section 5 diagnosis ("a growing ordered
dependency diagonal stores phase in long gaps"), not an escape from it.

**Searching for a bounded-window description of that bit fails.**  Testing
whether `T[u][0]` is a function of the previous `m` values of the same row
together with the last `m+1` endpoint symbols: conflicts at `m = 1, 2, 3, 4`
over four-state endpoints, with state counts `24, 112, 448, 1808`, i.e.
multiplying by 4 per window step with no sign of saturation.

## 6. The margin, measured

`(PSI)` is `Delta = Psi_j + Psi_{j+1}` containing a `1`, with `Delta` of length
`n+1`, indices `0..n`.  Exhaustive over all `2^n` binary sources:

| n | max first-`1` index in `Delta` | limit | constant `Psi` |
|---|---|---|---|
| 5 | 6 | 5 | **2** |
| 6 | 7 | 6 | **3** |
| 7 | 6 | 7 | 0 |
| 8 | 6 | 8 | 0 |
| 9 | 7 | 9 | 0 |
| 10 | 8 | 10 | 0 |
| 11 | 8 | 11 | 0 |
| 12 | 10 | 12 | 0 |
| 13 | 9 | 13 | 0 |
| 14 | 10 | 14 | 0 |
| **15** | **15** | **15** | 0 |
| 16 | 13 | 16 | 0 |
| 17 | 12 | 17 | 0 |
| 18 | 17 | 18 | 0 |

`n = 5` and `n = 6` are the known finitely many exceptions below `(BWH+)`'s
`n >= 7`; they are recovered here rather than assumed.

**The margin is exactly one position and it is attained.**  At `n = 15` the
maximum first-`1` index equals `n`, so `Psi` is constant on all of
`Psi_0..Psi_n` and flips only at the final coordinate `Psi_{n+1}`.  Any
candidate lemma, potential function or recursion that cannot separate
`Delta = 0^{n+1}` from `Delta = 0^n 1` is `(PSI)` restated, not a proof of it.
`n = 18` reaches `n-1`, so the phenomenon is not a single accident at 15.

**The extremal set is a suffix cylinder.**  All 18 sources attaining index 15
at `n = 15` share the 9-symbol suffix `211212112`; the free prefix is 18 of the
64 six-symbol words, all ending in `2`.  The extremal behaviour is carried by
the source's tail, the end nearest the continuation.

Splitting by target constant (`c = 2` is `Psi = 0^{n+2}`, `c = 3` is
`1^{n+2}`), the longest constant prefix over all sources reaches `n+1` on the
all-ones side at `n = 15` and at most `n-2` on the all-zeros side through
`n = 16`.  The two cases are not equally tight, but neither is cheap.

## 7. Honest position

This is a reformulation with three exact identities behind it, not a step
across the gap.  It converts `(PSI)` from a statement about `2^n` independent
binary sources into a statement about the depth-`n` read-out of `n` iterations
of one fixed 4-state Moore machine.  Whether that is progress depends entirely
on whether the composite admits an argument the raw form did not, and this
report does not exhibit one.

The measured margin is the reason to be cautious: one position.  The census is
finite evidence and obstruction H applies to it in full; extending it further
is explicitly ruled out by the capsule and buys nothing here either.

## 8. Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python psi_kernel.py --max-source 9        # gate against the reference
uv run python psi_structure.py --max-source 14    # laws + census
uv run python psi_column_map.py --max-source 10   # integrals, non-autonomy, extremal set
```

## 9. Follow-up the same day: the target is probably wrong

`PREREG-psi-constraint-counting.md` pre-registers and runs the obvious
counting check on `(BWH+)`, and it went against the program.  `Psi` has `n+2`
coordinates against an `n`-bit source, so independence predicts `1/2` constant
sources per `n`, *constant in `n`*, hence infinitely many counterexamples to
`(BWH+)`.  Measured exhaustively for `n = 7..18`: the ratio to the
independence null sits at `1.00 +/- 0.05` over most of the range and exceeds 1
at every `n`, peaking at 18 for `n = 15`.  There is no suppression mechanism
visible in the statistics, and the near-miss population does not shrink with
`n`.

That does not refute `(PT2)` — `BWH+ => DLP => SEP` runs one way only — but it
does say `(BWH+)` is the wrong thing to try to prove, and it says the empty
census through `n = 20` is a thinner reed than it reads as.  The fallback is
the one the capsule already names: DLP/RW, which keeps the hard-core suffix
and the terminal `12a` pull and is therefore a strictly smaller solution set
this count says nothing about.

The one encouraging detail, and the concrete next target: the survivors die
*simultaneously*.  All 18 `n = 15` survivors clear `k = 15` and all 18 fail at
`k = 16`.  A shared cause kills a whole suffix cylinder at once.  Identifying
that cause is a sharper question than `(PSI)` and it is the thing the ancestry
law of sections 3 and 4 is built to express.

## 10. The fan-out test: `Delta` has full algebraic degree

`PROOF-STATE-CAPSULE.md` section 7 names the switch criterion exactly: "if the
complete-state recursion necessarily fans out, weaken immediately to RW/DLP."
Section 3's closed form makes that testable.  Encode the source
`W in {1,2}^n` as `n` bits and take the algebraic normal form of each
coordinate.

| n | `deg(Psi_j)` range over `j` | `max_j deg(Delta_j)` |
|---|---|---|
| 4 | 3..4 | 4 |
| 6 | 5..6 | 6 |
| 8 | 7..8 | 8 |
| 10 | 9..10 | 10 |
| 12 | 11..12 | 12 |
| 14 | 13..14 | 14 |
| 15 | 14..15 | 15 |

`max_j deg(Delta_j) = n` **exactly, at every `n` from 4 to 15**, and
`deg(Psi_j)` is `n` or `n-1` for essentially every coordinate.  `Delta` is a
maximum-degree Boolean function of the source.

**Consequence.**  There is no bounded-degree seam law and no local composition
identity of bounded arity for `Delta_j`.  Any recursion that computes it must
carry state of unbounded size, which is the fan-out the capsule anticipates.
The pre-authorised fallback therefore fires on its own stated criterion:
**weaken to DLP/RW**, retaining the two facts `(BWH+)` discards — the
hard-core suffix and the terminal `12a` pull — and target the forced adjacent
`E` change at rows `n, n+1, n+2` rather than for every arbitrary binary
source.

This is a limitation theorem about the `(BWH+)` formulation, not about
`(PT2)`.  `BWH+ => DLP => SEP` runs one way only, so nothing here bears on
whether period-two exclusion is true.

**Scope, stated exactly.**  Full degree rules out a *bounded-arity polynomial*
seam law.  It does not rule out a proof by other means: an ordered-ancestry or
injection argument of the kind capsule section 6.4 describes is not a
bounded-degree object and is untouched by this measurement.  The closed form
in section 3 remains the right vehicle for one.

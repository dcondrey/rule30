# Fresh-onset trace obstruction and the eventual-core gluing gap

Date: 2026-09-09. **U/C/K:** the full alternating-centre trace space is
not topologically transitive. **R:** a distinct gluing obligation on its
eventual core remains unresolved. This neither proves nor kills R1.

## 1. The actual observable factor

Let X be all initial right rows, B=G_1∘G_0, and

```text
tau(x)_n = (B^n(x))_1,
Y = tau(X).
```

The map tau is continuous, since every finite trace prefix depends on
finitely many initial cells, and `tau∘B = shift∘tau`. Thus Y is compact
and closed under the forward shift. For a finite word v, `[v]_Y` denotes
the traces in Y beginning with v. These are observable cylinders; they
are different objects from cylinders fixing an initial right row.

The periodic row cylinders in
[RESULTS-r1-periodic-cylinders.md](RESULTS-r1-periodic-cylinders.md)
alone do not show that Y is nontransitive. Their images are single
periodic traces, which need not be open in Y. There is nevertheless a
separate exact obstruction using an existing eventual forbidden core.

## 2. Exact observable witness (`U/C/K`)

Take

```text
u = 00010000100001000010000       (length 23),
w = 100010001                    (length 9).
```

Both observable cylinders are nonempty. The fresh initial right prefix

```text
10110010000000110
```

produces w under unchanged `numeric_rho`. The word u is a prefix of
`(00010)^infinity`, a phase of the known realized period-five necklace.
Its spatial-period-155, time-period-10 torus, at microphase 4, gives the
explicit initial right prefix

```text
001110101110100010011001010101001110001101100
```

which produces u under the same frozen routine.

The verified h4 core in
[RESULTS-terminal-period-core-obstruction.md](RESULTS-terminal-period-core-obstruction.md)
forbids `1?0?1?0?1` at every rho start at least 23. Its selected indices
are 23,25,27,29,31. Resetting that free-row cone before a proposed late
occurrence proves the exclusion uniformly. Since w matches that mask,
w cannot start at any n≥23 in any member of Y.

For 0≤n<23, w cannot start in a trace whose prefix is u either. At
positions of u equal to zero there is already a first-bit conflict.
Its ones occur at n=3,8,13,18; at each such n the bit at n+4 is zero,
whereas w's bit 4 is one. These coordinates all lie within u. Hence

```text
shift^n([u]_Y) intersection [w]_Y = empty, for every n>=0.
```

This is a direct failure of observable-factor transitivity. In
particular, no bridge v makes `u v w` realizable. The source length 23
is minimal for this particular certificate method: a source prefix of
length at most 22 cannot block a putative start at 22 by overlap alone.
No global shortest-pair or shortest-transient-word claim is made.

The h4 CNF and DRUP are rechecked, with hashes

```text
CNF:  f78513e25bdf5cac5ae2de3907a401c70ada0f9bbdba61fb936f9aa9b1bb336d
DRUP: 3f3c904fc12c3bdb4f0a1ba14883ff4629adb69c0f18bf36d6a7c9aeb521d781
```

The CNF has 2,016 variables and 15,381 clauses. The stored independently
verified proof has 6,490 additions. The new check covers all 23 early
overlaps, both actual finite traces, and the unchanged torus verifier.
The infinitely many later shifts are covered by the translated core,
not by a numerical horizon.

## 3. The eventual trace core is a separate object (`U`, `R`)

Put

```text
Omega = intersection_(n>=0) B^n(X),
Y_infinity = intersection_(n>=0) shift^n(Y).
```

Then **U:** `Y_infinity = tau(Omega)`. One inclusion follows by applying
tau. For the other, fix y in every `tau(B^n(X))`. The compact sets
`B^n(X) intersection tau^(-1)({y})` are nonempty and nested. Their
intersection supplies a preimage in Omega. The same compactness
argument shows that B maps Omega onto itself, so the shift maps
Y_infinity onto itself.

The word w above occurs nowhere in Y_infinity. Otherwise a trace in
the core would have a prehistory long enough to put w at a start at
least 23 in a member of Y. Thus the explicit nontransitivity witness
does not descend to this core.

Periodic row basins do not settle core trace transitivity either. An
exact abstract example shows the distinction. Take two clopen copies
of the binary full shift. On the first copy use the shift map and
observe its first bit. On the second use the identity map and observe
zero. Every point of the second clopen copy has trace `0^infinity`,
but the full trace factor is the binary full shift, which allows every
word concatenation. The whole row-state system equals its eventual
core, so passing to the core does not change the example.

To match the two existing periodic basins more closely, use one free
shift copy and twelve further clopen copies arranged in cycles of
lengths five and seven. Advance the copy label while leaving its
hidden binary sequence fixed, and observe the appropriate phase of
`10000` or `1010000`. Both incompatible locked basins exist, yet the
free component still makes the trace factor the full shift. This is
an explicit compact dynamical example, **not a Rule30 construction**.

The live sufficient obligation is therefore:

> **Eventual-core observable gluing (`R`, unproved).** For every two
> words u,v occurring in Y_infinity, there is a finite bridge b such
> that u b v occurs in Y_infinity.

This obligation concerns complete observable continuations and permits
changing the hidden right row between finite construction stages. It
does not require any arbitrary initial-row cylinder to escape its
periodic basin.

If proved, it would give a counterdiagram, not merely a heuristic.
The known period-five and period-seven tori belong to Omega. Starting
with one of their trace words, repeatedly use gluing to extend the
current observable prefix by increasingly long blocks of those two
periodic traces, alternating between them. Every prefix stays in the
actual core language. Compactness supplies a trace realizing all the
nested prefixes. It cannot be eventually periodic: a fixed periodic
tail containing arbitrarily long blocks of both distinct primitive
periodic sequences would have to equal both. Equivalently, take a
block longer than the product of its proposed period and the two
primitive periods to force equality of the corresponding periodic
words. Continuity of tau supplies an initial right row; the exact
left inverse then completes the Rule30 diagram as in
[RESULTS-r1-observable-fusion.md](RESULTS-r1-observable-fusion.md).

No step in that construction establishes the required gluing premise.
The current cumulative avoidance graph has one recurrent component
containing all known regimes, so it permits bridges in its necessary
language. It is an overapproximation: those bridges have not been
lifted uniformly to actual right half-planes. This is the precise
remaining **eventual-core gluing gap**.

## 4. Rule90, reproduction, and scope

Rule90 realizes the concatenation `u w`, with w starting at 23. The
artifact gives the exact 63-cell initial right prefix and verifies
all 32 samples using unchanged `numeric_rho(..., rule30=False)`.
The recursive construction chooses the new ancestral bit at index 2n
to set sample n, so the uniform OR-core exclusion cannot transfer to
Rule90. `controls.rule90_control(6)` passes unchanged.

```sh
uv run python experiments/rule30/r1-isolated-column/trace_factor_transitivity_obstruction.py
```

Exact witnesses, overlap positions, certificate hashes, and controls
are in `trace-factor-transitivity-obstruction.json`. Full fresh-onset
trace transitivity is refuted. Eventual-core gluing, R1, and P1 remain
open; no aperiodic Rule30 trace is constructed here.

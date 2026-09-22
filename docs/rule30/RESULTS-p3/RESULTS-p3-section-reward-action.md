# Exact section-root rewards and an ordered boundary obstruction

Status: **an exact aggregate action is proved and implemented on a shared
word expression.** At a fixed requested bit, it composes without expanding
the word. Its table has `2^m` contexts for requested bit `m`, so this
implementation does not provide the required growing-precision bulk jump.
An actual core supplies a counterexample to recovering the reward from
letter counts and even the complete action on the preceding two bits.

This concerns composition in the ordered generator word, unlike the
earlier [affine time-block summaries](RESULTS-p3-aggregate-affine-blocks.md).
It also uses an aggregate across a whole expression, rather than the
individual cell inferences covered by the
[literal lazy-evaluation barrier](RESULTS-p3-local-evaluation-barrier.md).

## 1. The exact demanded-bit action

Use the chronological generators

\[
\begin{aligned}
A(x)&=x\mathbin{\mathrm{XOR}}((x\ll1)\mathbin{\mathrm{OR}}(x\ll2)),\\
B(x)&=A(x)\mathbin{\mathrm{XOR}}1,\\
C(x)&=A(x)\mathbin{\mathrm{XOR}}(3-2(x\mathbin{\&}1)).
\end{aligned}
\]

Fix an output bit index `m>=2`. For any generator `g`,

\[
 \operatorname{bit}_m(g(x))=\operatorname{bit}_m(x)
       \mathbin{\mathrm{XOR}}r_m(x\bmod2^m),
 \qquad
 r_m(s)=\operatorname{bit}_{m-1}(s)\mathbin{\mathrm{OR}}
                     \operatorname{bit}_{m-2}(s).          \tag{1}
\]

The reward is independent of the generator label because their corrections
are confined to bits zero and one. Their actions on the lower bits remain
different and determine which input reaches the next generator.

For a word `U`, define the two tables

\[
 \pi_U(s)=U(s)\bmod2^m,
 \qquad
 \rho_U(s)=\operatorname{bit}_m(U(s)),
 \qquad 0\le s<2^m.                                     \tag{2}
\]

Equivalently, `rho_U(s)` is the root toggle of the section obtained by
feeding the `m` low-to-high bits of `s` into `U`. For an arbitrary input
whose lower bits are `s` and whose bit `m` is `z`, the output through
that bit is

\[
 (s,z)\longmapsto(\pi_U(s),\ z\mathbin{\mathrm{XOR}}\rho_U(s)).
                                                               \tag{3}
\]

Higher input bits do not affect this action. Equation (3) follows from
(1) by induction on the word; the coefficient of the entering bit `z`
remains one.

**Exact composition.** If `U` acts before `V`, then

\[
\begin{aligned}
 \pi_{UV}(s)&=\pi_V(\pi_U(s)),\\
 \rho_{UV}(s)&=\rho_U(s)\mathbin{\mathrm{XOR}}
                           \rho_V(\pi_U(s)).              \tag{4}
\end{aligned}
\]

This transports the actual intermediate lower prefix. It is an associative
action on lower-prefix states with a one-bit accumulated reward. In
particular, the desired zero-input section root is `rho_U(0)`.

At `m=2`, there are four lower-prefix contexts. Adding the requested bit
gives an **eight-state action**, exactly the complete action on three
input bits. This is not eight-bit precision. The explicit representation
stores four two-bit permutation entries and four reward bits.

## 2. Exact aggregation on a shared expression

Construct the generator tables from (1)-(2). For each concatenation node
of a straight-line program, compile its two children and compose their
tables using (4). Memoize by node identity. The construction processes an
existing shared expression without flattening its generator word or
advancing one input bit at a time.

If `S` distinct concatenation nodes are compiled, this uses
`2^m S` context-record compositions, plus construction of the three
generator tables and identity. Each record contains an `m`-bit state and
one reward bit. The explicit action storage is therefore
`Theta((m+1)2^m)` payload bits per stored node, before indexing overhead.
These are counts of indexed table operations and stored bits; treating
the indices or variable-width operations as free would require a separate
machine-model justification. The input expression's construction is
charged as well.

The fixed-precision control constructs `C^(2^40+3)` by binary powering
of concatenation and obtains its bit-two reward at zero. It uses 46
grammar nodes and processes 168 composition records at four contexts per
action, without expanding any generator letters. Its answer is one.
The exact four-step low-three-bit cycle of `C` independently checks that
answer using only `C^3`. This demonstrates compressed execution at fixed
precision, not a growing-index singleton shortcut.

For the current bulk section at `2k` input bits, direct use of this
construction requires `2^(2k)` contexts. Thus the fixed-precision success
does not make the implicit boundary evaluator uniform in `k` at low cost.

## 3. Why letter charges and boundary potentials do not telescope

A prospective simplification would assign one constant charge `chi(g)`
to each letter and a potential `Phi(s)` to each lower-prefix state, so
that every local reward satisfies

\[
 r_2(s)=\chi(g)+\Phi(s)+\Phi(\pi_g(s))\quad\text{over }\mathbb F_2.
                                                               \tag{5}
\]

Summing would then determine the reward from letter counts and entering
and departing states, without following their order.

Equation (5) is impossible. The generator `A` fixes both lower-prefix
states zero and two, but their rewards are respectively zero and one.
The two self-loops force `chi(A)=0` and `chi(A)=1`. No choice of potential
can repair that contradiction.

The failure occurs inside an **actual seed-derived core**, not just on
unrestricted generator words. One exact core update gives

```text
Q(C^9) = CACACACAC.
```

Take the length-four chunks starting at zero-based positions three and
four. Their data are

| Chunk | Actual preceding prefix | Actual entering integer | Low-two-bit endpoints | Section-root reward |
|---|---|---:|---|---:|
| `ACAC` | `CAC` | 50 | `2 -> 0` | 0 |
| `CACA` | `CACA` | 222 | `2 -> 0` | 1 |

Both chunks have the same complete letter counts `(A:2,B:0,C:2)`.
They even have the same **entire permutation on the two-bit boundary**:

\[
 \pi_{ACAC}=\pi_{CACA}=(2,3,0,1).
\]

Nevertheless their reward vectors, indexed by incoming residues
`0,1,2,3`, are

\[
 \rho_{ACAC}=(0,0,0,0),\qquad
 \rho_{CACA}=(1,0,1,0).                                  \tag{6}
\]

The actual entering residue is two in both compiler contexts, where the
rewards differ. Thus even the full two-bit boundary action and exact
letter counts lose the demanded next-bit information. The extra reward
component in (4) carries real information and cannot be inferred from
those retained data.

This witness compares section-root **toggles**. The actual entering bit
two of the two prefix integers differs; it is not claimed that their
actual departing bit-two values differ. A compiler composing sections
needs the toggle in (3), with that entering bit treated correctly.

## 4. Verification and consequence

Run the [verifier](../../experiments/rule30/p3_section_reward_action.py):

```sh
uv run --offline --no-project python experiments/rule30/p3_section_reward_action.py
```

The [artifact](../../experiments/rule30/p3-section-reward-action.json)
records 336 checks against an independent raw-memory bit-serial engine
at fixed bit indices two and three, and 84 checks against the original
one-bit section recursion. It preserves the actual one-step core, both
ordered chunk contexts, their full action tables, the self-loop
contradiction, all paid counters for the large compressed fixed-precision
control, and source hashes. No new orbit or compression census is used.

The result supplies a sound aggregate evaluator at fixed precision and
identifies exactly what the proposed telescoping summary discards.
Avoiding the growing context table while constructing the demanded
reward remains unresolved. No assumption of independent constraints,
automatic error decay, or constant-cost iteration is used, and no
sublinear P3 algorithm or general lower bound is claimed.

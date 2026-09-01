# Quotient-ring cofactor automaton audit

Date: 2026-09-01

Status: **THE PROPOSED FINITE, DEGREE-PRESERVING, ACYCLIC SHIFT AUTOMATON
FAILS ON THE EXISTING `n=10` CERTIFICATE AND THE EXACT `n=12` EXTENSION.**
The ordered-prefix cofactors do expose a useful stabilizer recurrence, but
the cofactor alone is not a closed finite state and does not yield the
uniform `2n+2` bound.

## 1. Algebraic extraction without a seed sweep

Order the dynamic generators as

```text
g_0=epsilon_0, g_1=q_0, g_2=epsilon_1, g_3=q_1, ...
```

and work in

```text
B_n = F_2[rho_1,...,rho_n]
      / <rho_i^2+rho_i, rho_i rho_(i+1)>.
```

For an exact target `t`, define

```text
P_k = product_(i<k) (1+g_i),
C_i = (1+t) P_i.                                      (1)
```

The first forcing prefix is the least `k` for which `C_k=0` in `B_n`.
Telescoping (1) then gives the exact quotient-ring Bezout identity

```text
1 = t + sum_(i<k) C_i g_i,                            (2)
```

and, crucially, the actual cofactor transition

```text
C_(i+1) = C_i (1+g_i).                                (3)
```

The frontier recurrence `R_v(T,A,B)` does not itself define a unary map on
an arbitrary seed polynomial `C_i`; it acts on the full frontier triple. Once
`R_v` has produced `epsilon_m` and `q_m`, equation (3) is the exact induced
update on the certificate cofactor. Any smaller motif transition must be a
quotient of (3), and must retain enough frontier context to be well-defined.

All calculations in this audit use exact ANF multiplication and hard-core
monomial reduction. No seed assignment is enumerated. The regenerated
`n=10` coefficients match every nonzero dynamic cofactor in
`plateau-bezout-n10.json` exactly.

## 2. Certificate profiles

The `n=12` terminal macro is offset six. Its quotient certificates are
derived directly from (1)--(3), filling the missing cofactor data behind the
existing emission trace.

| `n` | target | first forcing generator prefix | macro horizon | maximum cofactor degree | maximum support span | nonzero / unique exact cofactors |
|---:|---|---:|---:|---:|---:|---:|
| 10 | `epsilon_8` | 5 | 3 | 5 | 9 | 5 / 5 |
| 10 | `q_8` | 9 | 5 | 5 | 9 | 9 / 6 |
| 12 | `epsilon_6` | 9 | 5 | **6** | **11** | 9 / 8 |
| 12 | `q_6` | 11 | 6 | **6** | **11** | 11 / 9 |

Thus the proposed degree-five cap already fails at `n=12`. The leading
cofactors are also global on the available seed: their spans grow from
`rho_2,...,rho_10` to `rho_2,...,rho_12`.

Bounded degree would not by itself make the quotient finite-dimensional
uniformly in `n`. The number of hard-core monomials of degree at most `d` is

```text
sum_(j=0)^d binom(n-j+1,j),                            (4)
```

which grows with `n`. For `d=5`, (4) is 144 at `n=10` and 370 at `n=12`.
A uniform finite dictionary would additionally require a uniform spatial
footprint or another proved translation quotient; neither is present here.

## 3. Complete shifted-cofactor dictionary

To make "same motif up to shift" exact, each whole cofactor polynomial is
translated so that its least supported variable is `rho_1`, with the
constant monomial fixed. Whole cofactors are used because factorization into
fragments in a Boolean quotient is nonunique; this normalization is
canonical for the ordered-prefix certificates.

Across the four certificates there are:

```text
28 nonzero normalized cofactor motifs,
1 zero terminal motif,
29 dictionary states total.
```

There are **zero nonzero normalized motifs shared between `n=10` and
`n=12`**. Repetition occurs within a certificate, not as a common
translation-stable dictionary across the two lengths.

The small `n=12` stabilizers are also different from the `n=10` motif. For
`epsilon_6`, the late coefficients include

```text
q_2:
  rho_6rho_8rho_10 + rho_6rho_8rho_12 + rho_6rho_9rho_12
  + rho_4rho_6rho_8rho_10 + rho_4rho_6rho_8rho_12
  + rho_2rho_4rho_6rho_8rho_10rho_12,

epsilon_3:
  rho_6rho_8rho_10 + rho_6rho_8rho_12 + rho_6rho_9rho_12
  + rho_4rho_6rho_8rho_10 + rho_4rho_6rho_8rho_12,

q_3, epsilon_4:
  rho_6rho_9rho_12.
```

This is exact algebraic simplification, but it is neither a translate of
`rho_6rho_9(1+rho_4)` nor degree-preserving along the full transition.

## 4. The repeated `n=10` motif is a self-loop

Let

```text
M = rho_6rho_9(1+rho_4).
```

In the `q_8` certificate, `M` is the coefficient of `q_2`, `epsilon_3`,
`q_3`, and `epsilon_4`. By (3), equality of these consecutive coefficients
means

```text
M(1+q_2)       = M,
M(1+epsilon_3) = M,
M(1+q_3)       = M.                                  (5)
```

Consequently the complete macro-three transition is

```text
M --[epsilon_3,q_3]--> M.                            (6)
```

Equation (6) is an exact stationary self-loop, not a rightward shift. At the
next macro, `epsilon_4` sends the same cofactor state to zero. Therefore a
state consisting only of the normalized motif is not even deterministic:

```text
M -> M     at macro 3,
M -> 0     at macro 4.                                (7)
```

It must retain at least generator/frontier context to choose a successor.
There are 19 extracted macro transitions, four of which terminate at zero.
Of the 15 nonterminal transitions, only six preserve degree and only one is a
translate; that one is the stationary shift by zero in (6). There are no
positive right-shifts. The observed motif graph is thus not a DAG.

Calling the extracted dictionary "closed" would also be circular: its 29
states were defined as the union of the observed sources and destinations.
No calculation here proves that an arbitrary later macro or arbitrary `n`
stays in that dictionary; the absence of cross-length reuse is evidence in
the other direction.

## 5. Consequence for the uniform bound

The stabilizer identity (3) is real and potentially useful. It explains why
a cofactor can persist across absorbed generators. It does **not** currently
give a finite acyclic automaton:

1. degree five is already exceeded at `n=12`;
2. support spans the whole tested seed and grows with `n`;
3. no nonzero whole-cofactor motif is shared across `n=10` and `n=12` after
   translation normalization;
4. the highlighted `n=10` motif produces a literal self-loop; and
5. motif state alone does not determine the next transition.

Even a DAG of translation *types* would not automatically prove `2n+2`: a
chain `M_k -> M_(k+1)` can have unbounded length while visiting one motif
type. A proof must supply a well-founded quantity that counts spatial
progress and show how it couples to the moving inverse-Gray frontier.

The sharp next algebraic target is therefore not acyclicity of the present
cofactor dictionary. It is a parameterized identity of the form

```text
C_(m+s) = Shift(C_m) + terms killed by J_m,
```

together with a bounded-width normal form and a strictly monotone spatial
rank. Neither property follows from the current certificates.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/cofactor_automaton.py \
  --json \
    experiments/rule30/p1-period2-invariant/cofactor-automaton-n10-n12.json

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/verify_cofactor_automaton.py \
  experiments/rule30/p1-period2-invariant/cofactor-automaton-n10-n12.json
```

The JSON artifact records all four targets, generators, exact cofactors,
successor cofactors, normalized motif occurrences, generator and macro
edges, support spans, and graph-audit flags. The standalone verifier expands
all four identities and every transition directly from recorded monomial
masks.

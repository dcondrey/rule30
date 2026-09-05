# Claim audit: Dual-Flow decision-tree lower bound

Date: 2026-09-03

## Verdict

**The advertised algebraic-degree/decision-tree argument does not prove P3.**
It lower-bounds a Boolean function whose inputs are the cells of an arbitrary
initial light cone.  P3 fixes those cells to the lone seed and gives a Turing
machine only the binary digits of the time index `n`.  These are different
input problems, and the former lower bound does not transfer to the latter.

The same distinction also invalidates the advertised inference from unbounded
algebraic degree to P1.  This audit does not assess any independent structural
identities in the paper.

Source assessed: Dhashvin Deva, *Algebraic Obstruction and Dual-Flow
Consistency in Rule 30*, SSRN
[`10.2139/ssrn.5908722`](https://doi.org/10.2139/ssrn.5908722), posted
2026-01-09.  The abstract claims linear algebraic-degree growth, algebraic
immunity, and essential-variable saturation, followed by an `Omega(n)`
decision-tree lower bound for the `n`th center bit and nonperiodicity.  SSRN's
anti-bot layer prevented retrieval of the 20-page PDF during this audit, so
the verdict is deliberately limited to that advertised implication.  The
official prize site still lists all three questions as open.

## 1. The two functions

For a time `t`, let

```text
G_t : {0,1}^(2t+1) -> {0,1}
```

be the `t`-step center cell as a function of an arbitrary initial light cone.
Algebraic degree, algebraic immunity, essential variables, and ordinary
decision-tree complexity are properties of `G_t`.

The archive already has the exact strongest version of this result: for every
`t>=3`, `G_t` has degree `2t-1` with a unique top monomial.  This is a genuine
arbitrary-input theorem.

The prize object is instead the fixed sequence

```text
a(n) = G_n(delta_0),
```

and its algorithmic input is the `O(log n)`-bit representation of `n`.  Once
`n` is fixed and the lone-seed substitution is made, `G_n(delta_0)` is a
constant; it has no remaining light-cone variables to query.  A uniform
machine still has to determine which constant is correct for each `n`, but an
arbitrary-initial-row decision tree says nothing about that index-to-bit task.

Consequently

```text
D(G_n)=Omega(n)
```

does not imply

```text
time_TM(n -> a(n))=Omega(n).
```

This is a quantifier failure, not a missing constant in the complexity model.

## 2. Exact internal control

No different cellular automaton is needed to see the break.  Keep Rule 30 and
use the all-zero initial configuration.  The arbitrary-input function `G_t`
is unchanged, so it retains exactly the same algebraic degree and essential
variables.  Yet after substituting the all-zero seed, the center sequence is

```text
0,0,0,...,
```

which is periodic and computable in constant time.

Therefore no implication based only on the arbitrary-input algebraic
complexity of `G_t` can establish either nonperiodicity or a time lower bound
for a designated seed orbit.  A valid bridge must use a property that survives
the lone-seed substitution and relates different time indices uniformly.

## 3. Consequences for the three advertised claims

- **P3:** a decision tree querying initial cells solves a different problem
  from a Turing machine receiving `n`.  The claimed lower bound is inert for
  the prize unless an additional uniform reduction is supplied.
- **P1:** unbounded degree across the family `G_t` does not preclude a fixed
  seed from producing a finite linear recurrence; the all-zero Rule 30 orbit
  is an exact counterexample to that implication.
- **P2:** the abstract offers structural evidence against sustained bias, not
  a seed-specific limiting-density theorem.

## 4. Reusable criterion

Any future algebraic-complexity claim must identify its variables before it is
compared with P3:

| Function | Inputs | Relevant conclusion |
|---|---|---|
| `G_t` | `2t+1` arbitrary initial cells | Worst-case local prediction |
| `f_k(r)=a(2^k+r)` | `k` time-index bits on the fixed seed | P2/P3-relevant uniform index structure |
| `a(n)` | binary representation of unbounded `n` | The actual P3 function |

Only the latter two retain the prize's fixed seed.  High complexity of the
first cannot be substituted for them.

No prize problem is solved by this audit.

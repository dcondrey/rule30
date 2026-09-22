# Refutation: Fradkin, "Rule 30 Resolved"

**Verdict: REFUTED, for all three problems, by one error appearing three times.**

Assessed 2026-08-31. Yuval Fradkin, "Rule 30 Resolved: Synchronization, Uniform
Cylinder Frequencies, and Unconditional Convergence from First Principles",
Zenodo. Not on arXiv, not peer reviewed.

## Scope of this assessment, stated first

**Only version 1 was read in full**: DOI 10.5281/zenodo.17377540, deposited
2025-10-17, 126 pp. Everything below about the proof is attested against that
file.

The concept DOI is **10.5281/zenodo.17377539 with seven versions**, not the five
recorded earlier. The bodies of the five 2026 versions (12.6-15.9 MB) were
unreachable: Zenodo serves files as `application/octet-stream` so PDF conversion
never runs, and the working proxy route caps out between 10.4 and 12.6 MB.
Authorea, CORE, OpenAIRE and Zenodo IIIF all failed. So the 2026 bodies are
assessed only through their **descriptions**.

## Version drift

- `.17377540` and `.18838072` describe mathematics: "an explicit
  right-determining De Bruijn factor with a synchronizing word", uniform cylinder
  frequencies, per-time frequency 1/2, "all claims are proved within the paper".
- `.18838239`, `.18865858`, `.19148341` replace that, **under an unchanged
  title**, with a "unified energetic framework / scalar stability field / FEATAM"
  whose propositions include "logical incompleteness corresponds to spectral
  boundary effects".
- `.19187115` blends both and self-disclaims: the framework "does not increase
  proof-theoretic strength beyond classical foundations".

A framework disclaiming added proof strength cannot supply the missing step in an
open problem. Across versions the abstract got vaguer, not the mathematics
stronger.

## The false step: nearby configuration to seed

**It does not fail through the single-orbit / measure-zero gap.** That was the
anticipated failure and the anticipation was wrong. Parts 10 and 14 state
seed-specific theorems and never route through the Bernoulli results. The
transfer that fails is cruder.

**P1 (Part 4 Thm 6.1 / Part 8 Thm 5.1).** Fix period `p`, choose `M << n` and
`t` in `[n/3, 2n/3]`. Pin the initial condition to the seed on `B_M = [-M, M]`
and use the bits **outside** `B_M` to force `(x(t)_0, x(t+p)_0) = (0,1)`. Then,
verbatim:

> "for every M there exists y(0)(M) agreeing with the seed on [-M, M] and
> satisfying c_y[t + p] != c_y[t]"
>
> "As M -> infinity (and n -> infinity with t in [n/3, 2n/3]), locality implies
> the genuine seed center also violates period p."

Invalid, and the paper's own parameters make it visible. With `M << n` and
`t ~ n`, the violation sits at a time whose light cone reaches far outside the
window where `y` agrees with the seed. Locality gives the opposite: `y(0)(M)`
tends to `delta_0` in the product topology and continuity of the CA gives
`c_y[t] -> c_seed[t]` **for each fixed `t`**, while the discrepancy is placed at
`t -> infinity`. What is proved is that arbitrarily close to the seed there are
configurations violating period `p`. That is a statement about the neighbourhood,
not the seed.

**P2 (Part 10 Thm 3.1).** Same substitution: "for each `N` there exists a
boundary realization on `T_N` with exactly `floor(N/2)` ones", then Cesaro-glue.
The boundary realization is a different configuration; the pairing map
`P_T: R -> R xor v(T)` changes right-boundary bits. Existence of a balanced
nearby configuration is not balance of the seed.

**P3 (Part 6 Thm 3.1, Part 7 Thm 4.1).** Worst-case-over-inputs bounds: "every
deterministic decision tree computing `f_n` has worst-case query complexity
`2n+1`", and `Omega(n)` expected time "on all inputs". P3 asks for the effort to
compute `c(n)` on **one fixed known input**. Same quantifier error.

## Rule 90 kills it, verified locally

The argument uses exactly two ingredients: **left-permutivity** (Def 1.1 /
Lemma 1.1) and triangular solvability of boundary bits along the cone (Part 9's
Boolean-derivative calculus over `F_2`, lower-triangular unit-diagonal Jacobian).

Rule 90 is left-permutive, and being `F_2`-linear its influence matrix is
triangular **by construction**, so the backsolve is *easier* for Rule 90.
Substituting Rule 90 throughout, the argument concludes that Rule 90's lone-seed
centre column is non-periodic with density 1/2.

Both are false. Computed here directly:

```
Rule 90 centre column t=0..40 : 1000000000000000000000000000000000000000 0
  ones in t=0..64             : 1
  all-zero after t=0          : True
```

`1,0,0,0,...`: at even `t = 2s` the value is `C(2s,s) mod 2`, odd only at `s = 0`
by Kummer, and zero at odd `t` by parity. Eventually constant, hence eventually
periodic, density 0.

**Which of the paper's hypotheses genuinely fails for Rule 90: none.** The
strings "Rule 90", "additive", "bipermutive", "linear cellular automaton" and
"XOR" appear **nowhere** in 126 pages. There is no discriminator.

## Internal contradiction

Part 9 carries an explicit **Conjecture 4.1 (Uniform temporal pairing)**. Part 10
asserts the same statement for arbitrary finite `T` as **Theorem 2.1** —
conjectured in one Part, theorem-ed in the next. Part 9 also states verbatim:

> "This note does not claim a proof of seed half-frequency."

which contradicts the deposit description's "all claims are proved within the
paper".

The argument fails **even granting Conjecture 4.1 in full**: perfect control over
which centre times you flip by choosing boundary bits still only produces a
modified configuration. The load-bearing step is the locality transfer, and it is
**asserted** — an "Outline" in Part 4 defers to Part 8, and Part 8 restates the
same one-line assertion rather than discharging it.

"Synchronization", in the title, is **undefined**: two occurrences, both outside
any numbered statement, no formal definition, and irrelevant to the seed theorems
in any case.

## Literature engagement

Three references total: Hedlund 1969, Lind-Marcus 1995, Pivato 2009. **No** Jen,
Kopra, Meier-Staffelbach, Rowland, or **Wolfram**. A 126-page paper claiming all
three prize problems, omitting the originator of the problems.

## The one falsifiable number, tested

Part 6 Thm 3.1 claims `f_n` is evasive with query complexity exactly `2n+1`.
Computed the full `F_2` Mobius expansion of `f_n` for `n = 1..9`:

| n | vars `2n+1` | top-degree monomial present | ANF degree |
|---|---|---|---|
| 1 | 3 | no | 2 |
| 3 | 7 | no | 5 |
| 5 | 11 | no | 9 |
| 7 | 15 | no | 13 |
| 9 | 19 | no | 17 |

Degree is exactly `2n-1`, two below the ceiling, at every `n`. **This does not
refute evasiveness** — ANF degree is only a lower bound on decision-tree
complexity, so `D(f) = 2n+1` remains possible. What it shows is that the standard
degree argument yields `2n-1`, not `2n+1`, so if Part 6's proof runs through
full-degree monomial presence it is broken and needs inspection.

*This is a reproduction, not a discovery:* `ARM4-frequency-domain.md` already
records degree exactly `2t-1` at `t = 1,3,5,7,9,10`. The values here match it
exactly, which cross-validates both.

## What this repo should take from it

1. The anticipated failure mode was wrong. Obstruction E (measure-zero single
   orbit) is not the only ensemble-to-seed trap; **nearby-configuration-to-seed**
   is a distinct one and should be named alongside it. A proof can be entirely
   seed-specific in its statements and still smuggle in a different
   configuration.
2. Rule 90 remains the correct first control **for arguments of this shape**, in
   contrast to the Topal assessment where it passes vacuously. Left-permutivity
   plus `F_2` triangularity is exactly the hypothesis set Rule 90 satisfies.
3. Version count and content drift are worth recording for any claimant: seven
   versions whose descriptions weaken over time, ending in a self-disclaimer.

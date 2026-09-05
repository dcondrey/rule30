# The Fibonacci/fiber decomposition unifies this session's three kills into one obstruction

Session 2026-09-05. This is a **synthesis of results already on record plus one
new exact identification**; it is not a new proof, and the individual kills it
connects were each established separately (and are cited below). Labelled as
synthesis so it is not later mis-cited as a discovery.

## The bound everything reduces to

`MEMO-PHI-OVER-4-FIRST-MOMENT.md:38-41` states the Fibonacci-times-fiber bound:

```
|S_k| <= Fib(k+1) * max_fiber  ~  phi^k * 2^n/4^k  =  2^n (phi/4)^k
```

Two factors:

- **`Fib(k+1) ~ phi^k`** — the hard-core (no-`11`) word count. These are exactly
  the counts `2,3,5,8,13,21,34,55,89` that `D_k` tracks before departure.
- **`max_fiber ~ 2^n/4^k`** — the *equidistribution* factor for
  `Psi_k : {1,2}^n -> {0,1,2,3}^k`, i.e. the assumption that each forced-symbol
  prefix is hit by only `4^{-k}` of the source words.

`phi/4 < 1/2` comes entirely from the second factor. The first factor alone
gives `phi = 1.618 > 1`, which proves nothing.

## NEW, and exact: the width-`w` window matrix IS the `phi/4` matrix with the fiber factor set to 1

`RESULTS-WINDOW-SPECTRAL-RELAXATION.md` reports that the width-`w` relaxation
gives `lambda_max = phi` identically, because the free incoming `(h,F)` cell can
always be steered onto the target (a bijection: `h' = h XOR a XOR 1` with `a`
depending only on the left parent). Charge that cell its true probability
instead of letting it be chosen for free, and the matrix becomes the null model
exactly (`scratchpad/fib_fiber_map.py`):

```
w  c   surviving-unknowns/(state,symbol)   lambda(weight=1)   lambda(weight=1/4)   ratio
1  2   1.0000                              1.618034           0.404508             4.0000
1  3   1.0000                              1.618034           0.404508             4.0000
2  2   1.0000                              1.618034           0.404508             4.0000
2  3   1.0000                              1.618034           0.404508             4.0000
3  2   1.0000                              1.618034           0.404508             4.0000
3  3   1.0000                              1.618034           0.404508             4.0000
```

Exactly **one** of the four `(h,F)` values satisfies the target, always — that
is the `1.0000` column, and it is the bijection restated as a count. So:

| object | per-step rate | what the `(h,F)` cell costs |
|---|---|---|
| width-`w` window relaxation | `phi = 1.618034` | free (probability 1) |
| `phi/4` null transfer matrix | `phi/4 = 0.404508` | charged `1/4` |

**The gap between the vacuous bound and the useful one is exactly the factor
`4 = |{(h,F)}|`, the four states.** The relaxation is not "a different, weaker
model": it is the same transfer matrix with the equidistribution factor set to
1. That is why it was vacuous, and it is the same factor that
`MEMO-PHI-OVER-4-FIRST-MOMENT.md` identifies as the load-bearing one.

## The consequence: four separate kills are one obstruction

Everything that failed, failed at the *fiber* factor, never at the Fibonacci
factor:

1. **Width-`w` window relaxation** (this session): drops the fiber factor
   entirely -> `phi`. Vacuous at every `w`.
2. **`Psi_k` equidistribution** (`MEMO-PHI-OVER-4-FIRST-MOMENT.md:64-79`):
   the fiber factor is *false as stated*. Max fiber stabilises at a small
   constant — **24, 30, 74** at `n=12,14,16` — instead of decaying like
   `2^n/4^k`. Past `k ~ n/2` the bound would need max fiber `< 1`, "impossible
   for a nonempty fiber".
3. **Entrywise domination** (`RESULTS-TRANSFER-DOMINATION-CHECK.md:71-74`):
   asks whether the true weight is entrywise `<= M`. Fails; needs ~1.75x even
   at `N >= 100`, "giving effective eigenvalue ~0.71, not < 1/2".
4. **Weighted domination** (scored this session,
   `domination_test_20260905.log`): fails for *every* weight vector, because a
   same-last-symbol `1 -> 1` step has weighted ratio exactly `w_s/w_s = 1`.

So the Fibonacci half of the bound is solid and never in question. **The entire
difficulty is the fiber half**, and it is one difficulty wearing four hats.

## Where it breaks: the `n/2` scale, in four independent objects

The transition is at the same place every time — stated as a **scale**, not a
formula, per the P1 correction in `RESULTS-DISTINCT-CONTINUATION-COUNT.md`:

| object | transition | measured |
|---|---|---|
| `D_k` departs the Fibonacci counts | `k_dep` | 4,5,6,6,7,7,7,8 at `n=10,14,16,17,18,19,20,21` — i.e. `~n/2 - 2` |
| `Psi_k` stops being many-to-one | `k ~ n/2` | fibers stop shrinking; map becomes essentially injective (`MEMO-PHI-OVER-4` section 4) |
| weighted domination fails | deep `k` | every violator at `S_k` = 1,2,3,4,14,28 |
| proved light-cone memory law | `k_seed(L) = ceil((L+1)/2)` | the source runs out at `2k ~ n` |

`k_dep/n` measured is `0.40, 0.36, 0.375, 0.35, 0.38` — that is `n/2` with the
`-2` offset, not `0.5n` at these `n`, and the offset matters at the sizes we can
compute. **No exact law for `k_dep` is known** and none is claimed here; `n/2`
is the scale the light-cone argument supplies.

## What this says about the next attempt

- **Do not attack the Fibonacci factor.** It is exact, it is not where anything
  broke, and `lambda < 2` against it is automatic and meaningless.
- **Do not look for a better global weight/matrix.** Four routes have now failed
  at the same factor, and the weighted family is dead for *all* weights by the
  `1 -> 1` argument.
- **The live shape is a split argument.** The bulk regime (`k <~ n/2`, large
  `S_k`, fibers genuinely shrinking) is fine — measured ratios 0.35-0.47 against
  a 0.5 threshold. The obstruction is entirely the deep regime where `S_k` is a
  small constant and `Psi_k` is injective. A proof needs a spectral/counting
  bound for the first regime plus a **separate finite argument** for the second.
- That second regime is exactly what the **extinction margin** (the strongest
  open lead on record) measures, and exactly what
  `RESULTS-FIBER-EXTREMAL-FAMILY.md`'s shared-long-suffix structure describes.
  The rigidity fact from `MEMO-PHI-OVER-4` section 4 — "the forced continuation
  nearly determines the source word" — is a *help* there, not a hindrance: a
  near-injective map on a fixed family of `~0.2 * 2^n` images is a finite
  combinatorial object, not a statistical one.

## Files

- `scratchpad/fib_fiber_map.py` — the weighted-eigenvalue check above. Kept in
  scratchpad: it is a six-line variant of the killed builder in
  `RESULTS-WINDOW-SPECTRAL-RELAXATION.md`, and its full output is transcribed
  here.

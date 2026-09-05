# Width-w window relaxation of the RW: lambda_max = phi identically, and why that is vacuous

Session 2026-09-05. Preregistration and result in one file because the kill
condition fired on the first run.

## The proposal

Replace brute-force SAT at `n=31` with a spectral bound: model the surviving
hard-core continuations as paths on a De Bruijn-style graph for a finite window
width `w`, build the adjacency matrix `M_w` of valid Rule 30 transitions that do
not violate the constraints, and compute `lambda_max`. If `lambda_max < 2` for
some finite `w`, conclude geometric extinction for all `n`, with no `n=31`.

The logic of the direction is right and worth stating, because it is what makes
any such attempt admissible: the truncation must **over-approximate** the true
survivor set, so that `lambda_max` is an **upper** bound on the true growth
rate. A model that under-counts proves nothing.

## Construction (against the real constraint system, not a re-derivation)

`uc/r1-skeptic/rw_sat.py:encode` carries between adjacent columns the entire
depth profile of `(h, F)` pairs — `O(n)` pairs, so `4^O(n)` states. That is the
documented state-count wall. The relaxation truncates the profile to the deepest
`w` levels and lets the unknown incoming level be arbitrary, taking the union
over all four `(h, F)` values. The cell recurrence is copied verbatim from
`encode` (BRIEF section 2):

```
a  = (NOT h_L) AND F_L
b  = h_L XOR F_L
h' = h XOR a XOR 1
F' = F XOR (h AND b)
```

State = (`w`-tuple of packed `(h,F)`, `s_prev`); edges filtered by the hard-core
constraint `s_{u-1} OR s_u` and the target constraint `(h, F) = (1, c & 1)` at
the deepest level.

## Result: `lambda_max = phi` exactly, at every `w`, for both tails

```
w   c   states      edges    lambda_max   converged   lambda<2?
1   2   8           12       1.618034     True        yes
1   3   8           12       1.618034     True        yes
2   2   32          48       1.618034     True        yes
2   3   32          48       1.618034     True        yes
3   2   128         192      1.618034     True        yes
3   3   128         192      1.618034     True        yes
4   2   512         768      1.618034     True        yes
4   3   512         768      1.618034     True        yes
```

**`lambda_max < 2` is achieved — and it is worthless.** `1.618034` is exactly the
golden mean, the entropy of the hard-core (no-`11`) shift, which this project
already has on record as the Fibonacci hard-core counts `2,3,5,8,13,21`. The
value is independent of `w` and of `c`, and `edges = 1.5 * states` exactly,
i.e. two symbol choices with one quarter removed by the hard-core rule and
**nothing removed by the target constraint**.

## Why: the relaxation is provably vacuous at EVERY width

The disconfirming test, run before reporting the eigenvalue
(`scratchpad/vacuity_check.py`): for every left column and every target value,
can the free incoming cell be chosen to satisfy the target?

```
 w   left columns   reachable-target failures   verdict
 1   4              0                           VACUOUS
 2   16             0                           VACUOUS
 3   64             0                           VACUOUS
 4   256            0                           VACUOUS
 5   1024           0                           VACUOUS
 6   4096           0                           VACUOUS
```

Zero failures out of 4096 left columns at `w=6`. The structural reason, which
makes this a proof rather than a measurement:

> `h' = h XOR a XOR 1`, and `a = (NOT h_L) AND F_L` depends **only on the left
> parent**. So for a fixed left column the map (free cell's `h`) -> (target `h`)
> is `h XOR const`, a bijection; `F` follows likewise. The free incoming cell
> can therefore always be steered to hit `(1, c & 1)`.

Hence the target constraint prunes no edge at any `w`, `lambda_max = phi` for
all `w`, and **increasing `w` cannot help**. This is not a small-`w` artefact to
be scaled away.

## Verdict, and what it does and does not kill

**KILLED: the naive width-`w` window truncation, at every width.** Do not scale
`w`. The measured `lambda_max < 2` must not be cited as evidence of extinction;
it is a restatement of the hard-core golden mean and says nothing about Rule 30.

**NOT killed: spectral bounding in general.** What went wrong is specific and
diagnosable — the relaxation grants a *free* cell at the window's shallow edge,
and that freedom is exactly what the true system does not have. In the real
wedge the shallow edge is pinned at the boundary, `cells[(u,-u-1)] = (s_u, 0)`
and `cells[(u,-u)] = (NOT s_u, 0)`, which is determined by `s_u`. Anchoring the
window there removes the freedom — but then the window must span `-u` to `n`,
i.e. `n + u` levels, which is the `4^O(n)` wall again.

**So this run explains the state-count wall rather than merely hitting it:** the
wall is not an implementation inconvenience, it is the fact that any truncation
which leaves the shallow edge free is vacuous by the bijection above.

## The quantity a real bound has to reach

For the record, so a future attempt aims at the right number. The exact census
gives `N_k` = words surviving to depth `k`, with `N_0 = 2^n`, and extinction
needs `N_{n+2} = 0`. From `uc/r1-skeptic/census_n21_30.log` at `n=30, c=2` the
successive ratios `N_{k+1}/N_k` are

```
0.375, 0.4165, 0.4004, 0.4067, 0.4045, 0.4045, 0.4006, 0.4075, 0.4024, 0.4069, ...
```

converging to `phi/4 = 0.404508`. Since `N_{n+2} <= 2^n * rho^(n+2)`, extinction
for all large `n` follows from a **uniform** bound `rho < 1/2`, giving
`(2 rho)^n -> 0`. Measured `rho ~ 0.4045`, so the margin is real but it is a
measurement, not a bound.

**The theorem target is therefore: prove `rho <= const < 1/2` uniformly in `n`
and `k`.** `phi/4` is already the project's null-model eigenvalue for exactly
this ratio; what is missing is domination (that the null model upper-bounds the
truth), not the constant. That is the object worth attacking, and it is a
different object from the `M_w` above.

## Files

- `scratchpad/rw_window_spectral.py` — the `M_w` builder and power iteration.
- `scratchpad/vacuity_check.py` — the disconfirming test above.

Both are kept in the session scratchpad rather than committed: the construction
they implement is killed, and the repo should not carry a builder for a
relaxation that is provably vacuous. Their full output is transcribed above.

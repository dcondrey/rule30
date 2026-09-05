# The 0.4045 decay constant is exactly phi/4 — and why the obvious proof it suggests fails

Date: 2026-09-04 (late session, Opus review pass)

Status: **one identification confirmed, one proof route tested and REFUTED.**
Recorded so the refuted route is not re-derived and believed.

## 1. The constant is not an empirical fit

`RESULTS-TRANSFER-DOMINATION-CHECK.md` reports a measured per-row survival
rate ~0.4033 for the hard-core-surviving population of
`literal_extension`'s forced continuation, and notes it matches the leading
eigenvalue `(1+sqrt5)/8 = 0.404508` of the proposed null matrix
`M = [[0,1/4],[1/4,1/4]]`.

That eigenvalue is **exactly `phi/4`**, `phi = (1+sqrt5)/2` the golden ratio
(`(1+sqrt5)/8 = phi/4` identically). This is not a numerical coincidence to
be fitted — it is the ratio of two structural quantities:

- `phi^k` — the growth rate of the **hard-core (Fibonacci) language**, which
  is where every surviving continuation must live *by definition* (survival
  means the length-`k` continuation prefix is a hard-core word; there are
  exactly `Fib(k+1) ~ phi^k` of those).
- `4^k` — the size of `{0,1,2,3}^k`, the codomain of the forced-symbol map
  (`literal_extension` emits a symbol in `{0,1,2,3}` at every row; hard-core
  survival additionally requires it land in `{1,2}` with no `11`).

## 2. The proof route this suggests

Define `Psi_k : {1,2}^n -> {0,1,2,3}^k`, `W -> (first k forced symbols)`,
defined on ALL source words (the forced symbol always exists and is unique —
each row's candidate set is a singleton by bijectivity of the composed
`cone_local` permutations). Survivors are `S_k = Psi_k^{-1}(hard-core words)`.

If `Psi_k` were **equidistributed** — every fiber of size `~2^n/4^k` — then

```
|S_k| <= Fib(k+1) * max_fiber ~ phi^k * 2^n/4^k = 2^n (phi/4)^k
```

and since `phi/4 = 0.4045 < 1/2`, `|S_k| < 1` once
`k > n*ln2/ln(4/phi) = 0.7658*n`. Extinction by row `~0.766n`, while an
`H_r(n)` candidate needs the continuation to survive `n+r+2` rows. Since
`0.766n < n < n+r+2` for all `n`, `H_r(n) = empty` for **all** n, and
`gamma(n) >= 0.234n + 2 -> infinity`. That would prove the extinction-margin
conjecture outright, with **no** pseudorandomness/equidistribution-of-Rule-30
assumption in the deep regime — only a fiber-counting bound.

The first-moment curve even fits: against the measured `n=16, c=2` survival
curve (`alive_after` = 65536, 24540, 10598, 4332, 2017, 765, 255, 124, 35,
11, 3, 0), the bound `|S_k| <= C * 2^n (phi/4)^k` holds with `C = 1.15`.

## 3. Why it fails: `Psi_k` is NOT equidistributed

Measured directly (max fiber of `Psi_k` vs the equidistributed ideal
`2^n/4^k`), `tail=2, r=0`:

| n | k | #distinct image | 4^k | max fiber | 2^n/4^k | ratio |
|---|---|---|---|---|---|---|
| 12 | 4 | 251 | 256 | 50 | 16.0 | 3.1 |
| 12 | 6 | 947 | 4096 | 24 | 1.0 | 24 |
| 12 | 10 | 1086 | 1048576 | 24 | 0.004 | 6144 |
| 14 | 6 | 2304 | 4096 | 34 | 4.0 | 8.5 |
| 14 | 10 | 3368 | 1048576 | 30 | 0.016 | 1920 |
| 16 | 6 | 3761 | 4096 | 92 | 16.0 | 5.8 |
| 16 | 10 | 10565 | 1048576 | 74 | 0.06 | 1184 |

Two facts kill the route:

1. **The image saturates.** `#distinct` stalls (1087 at `n=12`, 3374 at
   `n=14`, 10604 at `n=16`) and never approaches `4^k`. The map's image is a
   fixed set of size `~0.16-0.27 * 2^n`, not a growing subset of `{0,1,2,3}^k`.
2. **Fibers do not shrink.** Max fiber stabilizes at a small constant
   (24, 30, 74 at `n=12,14,16`) rather than decaying like `2^n/4^k`. Past
   `k ~ n/2` the required bound is `< 1`, which is impossible for a nonempty
   fiber — the bound cannot hold at any `k > n/2` even in principle.

So the decomposition `|S_k| <= |image| * max_fiber` is far too lossy in the
deep regime, and the `phi/4` agreement of the *aggregate* rate is not
produced by the equidistribution mechanism that would make it provable.

## 4. What survives

- **The identification `0.4045 = phi/4` stands** and should be stated that
  way (Fibonacci growth over 4-ary alphabet), not as a fitted constant. Any
  future write-up should use `phi/4`, exact.
- **A rigidity fact, opposite to what was assumed:** max fiber is bounded by
  a *small constant* in `k` (24/30/74 above). The forced continuation nearly
  determines the source word. This is the reverse of the "fibers shrink like
  `4^{-k}`" hypothesis and is the genuinely new structural datum here. It is
  consistent with the shared-long-suffix structure already reported in
  `RESULTS-FIBER-EXTREMAL-FAMILY.md`.
- **The two-regime picture is real:** `k <~ n/2` the map is many-to-one and
  fiber-shrinking does most of the work; `k > n/2` the map is essentially
  injective and decay is entirely about which of a fixed family of `~0.2*2^n`
  continuations happen to remain hard-core. Only the second regime is
  pseudorandomness-flavored. Any future attempt should target regime 2
  specifically and can treat regime 1 as understood.

## 5. Do not retry

Do not re-propose "first moment via equidistribution of the forced-symbol
map." It is refuted by the table in section 3, not merely unproven. A
first-moment argument can only work if it uses a bound on the image that is
*not* `Fib(k+1)` (the image saturates well below `4^k`, so `Fib(k+1)` is not
the binding constraint in regime 2) or a fiber bound that is not `2^n/4^k`.

## Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python - <<'PY'
from itertools import product
from late_pull_diagonal_sat import literal_extension
n, tail, rows = 16, 2, 18
conts = [literal_extension(w, tail, rows) for w in product((1,2), repeat=n)]
for k in (4, 6, 10):
    b = {}
    for c in conts: b[c[:k]] = b.get(c[:k], 0) + 1
    print(k, len(b), max(b.values()), 2**n / 4**k)
PY
```

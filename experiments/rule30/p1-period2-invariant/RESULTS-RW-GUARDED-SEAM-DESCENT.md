# The missing seam in a minimal rotated-wedge descent

Date: 2026-09-13.

**Two exact counterexamples refute completion of the proposed descent from
the first four constant cut cells, even with the full endpoint grammar and
the terminal pull. Neither is an RW counterexample. RW/DLP and period-two
exclusion remain open.**

The verifier is `guarded_rw_seam_audit.py`; its artifact is
`guarded-rw-seam-audit.json`. It checks two explicit words, without a census.

## 1. The narrower language supplied by an actual counterexample

The exact right-trace identity in `RESULTS-RIGHT-FILTERED-MORTALITY.md`
excludes both `11` and `00000` from the even-time right-neighbor bit trace
under an alternating center. Endpoint symbols `1,2` encode right bits `1,0`,
so the actual endpoint avoids `11` and `22222`.

The finite-rank reduction prepends only finitely many endpoint `2`s. The
first-infinite-tail reduction subsequently takes a suffix. Consequently the
resulting endpoint retains these two forbidden-factor conditions beyond a
finite prefix, although it need not be an actual right trace at its origin.
Selecting the DLP scale beyond this prefix makes the entire word `f=WQ`
avoid both factors. This includes `W`, whereas the stronger published RW
statement allows an arbitrary binary `W`.

Thus it suffices for the period-two application to exclude RW witnesses in
this smaller language. This is a valid use of actual-right constraints
after the artificial prefix; it does not impose them on arbitrary queues.

## 2. An exact descent and its complete missing condition

Let `|W|=n`, `f=WQ`, `|f|=2n+r+2`, and suppose the complete word avoids `11`
and `22222` and ends in `12a`. Let `d` be the distance from the final
nonfinal pull to the preceding pull. Whenever that preceding pull exists,

```text
2 <= d <= 5.
```

For `n>=4` it necessarily exists: the final `1` cannot be the first `1`
after a prefix longer than four symbols. Set

```text
k = ceil((d-r)/3),       r' = r+3k-d in {0,1,2}.
```

If `k=0`, truncating the last `d` symbols preserves `n` and lowers the
residue. Otherwise `k` is either one or two. For a candidate binary prepend
`v` of length `k`, define

```text
f' = v f[:-d],           n' = n-k.
```

The earlier pull is now the terminal pull, and
`|f'|=2n'+r'+2`. Requiring `vW` to avoid both forbidden factors ensures the
complete new word has the required grammar.

Here is the exact cut identity, retaining the entire original source `W`:

```text
P^(n-k) I(v f[:-d])
  = [P^(n-k) I(vW)] . [(P^n I(f))[:-d]].                 (1)
```

Its hypotheses are `0<=k<n` and `|f|-d>=n`. The first bracket has exactly
`2k` cells. To prove (1), apply the iterated rotated-Peel identity to `vf`:

```text
sigma^(2k) P^(n-k) I(vf) = P^n I(f).
```

Prefix causality identifies its first `2k` output cells with
`P^(n-k)I(vW)`. The same causality allows deleting the last `d` endpoint
symbols and hence the last `d` cut cells. These statements prove (1) for
arbitrary finite words; the verifier's two instances are controls.

If the old cut is entirely constant `c`, all inherited cells in (1) already
equal `c`. The complete new obligation is precisely

```text
P^(n-k) I(vW) = c^(2k).                                  (SEAM)
```

There are at most two or four prepends to consider, but each seam depends
on the full ordered `W`. A counterexample minimal in `n`, then in `r`,
would have to reject every grammar-admissible prepend. Nothing proved here
forces one prepend to succeed.

## 3. Four cut guards do not supply the seam

Consider the proposed weaker lemma that the endpoint grammar, terminal pull,
and first four constant cut cells already force (SEAM). Both tail values
give exact counterexamples:

| `n,r,c` | `W` | `Q` | Full `P^n I(WQ)` | Only admissible prepend | Seam |
|---|---|---|---|---|---|
| `3,2,3` | `121` | `2122122` | `3333231` | `v=2` | `31`, required `33` |
| `7,0,2` | `1222121` | `222122122` | `222213000` | `v=2` | `33`, required `22` |

In both cases the complete endpoint has exactly the RW length, avoids `11`
and `22222` throughout, and ends in `122`. Its last two nonfinal pulls have
gap `d=3`, so the prescribed descent uses `k=1` and keeps `r'=r`. Prepend
`1` would create `11` at the new origin; prepend `2` fails the seam.

The first four cut cells equal the designated constant in each row. The
displayed later cells do not. Thus these words satisfy the deliberately
weakened guard, and **do not satisfy the full RW premise**. They refute the
four-guard seam lemma, not the separator or a descent theorem retaining all
cut constraints.

The full shortened words and their cuts are recorded in the artifact.
Their cut decompositions are exactly

```text
313333   = 31 . 3333,
33222213 = 33 . 222213.
```

## 4. Why an actual prior prefix does not finish the induction

If an actual endpoint tail `e` satisfies `I(e)_t=c` for every `t>=T`, its
true preceding symbols provide a successful seam whenever the smaller
scale still has `2(n-k)>=T`. The rotated identity then makes the entire
smaller cut constant. Its grammar also persists when the smaller scale is
beyond the finite artificial prefix.

This descent stops at an orbit-dependent threshold determined by `T` and
that prefix. Their sizes are unbounded across hypothetical counterexamples.
Descending to these unknown base cases supplies no uniform contradiction.

The remaining possible induction must either prove (SEAM) using stronger
history information or reduce the unknown initial constant-tail threshold
itself. The exact identity identifies that obligation; it does not prove
progress toward the separator by itself.

Update 2026-09-15: the first alternative is closed by
`RESULTS-SEAM-HISTORY-GUARDS.md`. Its uniform lemmas `(L1)` and `(L2)` make
every finite-history version of (SEAM) either refuted by an explicit orphan
at run `D_n(c)` or vacuous, so "stronger history information" collapses to
the full constant cut, `RW`'s own hypothesis; both witnesses of section 3
reproduce there (cuts `3333231` and `222213000`, runs `4`, seams `31` and
`33`). The second alternative, reducing the initial constant-tail threshold,
is untouched.

## 5. Verification

```sh
uv run --offline --no-project python \
  experiments/rule30/p1-period2-invariant/guarded_rw_seam_audit.py
```

The verifier reconstructs the local rule independently in Boolean `(H,E)`
coordinates and the inverse cone by its second-order diagonal recurrence.
It compares all 16 local entries and four boundary entries with the
maintained inverse-carry implementation, then compares the finite words
with the separate inverse-feed construction. It checks every admissible
prepend, the complete endpoint guards, both full cut words, and equation
(1), and records source hashes. No inference is made from extending a
finite search range.

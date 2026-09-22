# Full-history ancestor counts do not decrease at every repeat

Date: 2026-09-10.

Conditioning on the complete scalar history repairs the domain mismatch of
ambient inverse-fiber counting, but it does not provide a resource spent at
every repeated scalar. The smallest repeat already supplies a counterexample.
Two consecutive repeated scalars can also leave the candidate set unchanged.

## Exact domain and candidate set

Use the legal finite frontier map Z from
[the episode-composition report](RESULTS-variable-length-episode-composition.md).
A legal word has symbols `w_i=2a_i+b_i` and `a_0=1`. For a chronological scalar
tape alpha, define

```
C_r(alpha) = {w: |w|=r, a_0=1, and every update in alpha survives
                with exactly its prescribed scalar}.
```

This counts original ancestors of one fixed, exact length. It counts neither
distinct current endpoints nor arbitrary current inverse fibers. Every guard
is retained. The sets satisfy `C_r(alpha s) subseteq C_r(alpha)` by definition,
but strict inclusion at a repeated scalar is false. No arbitrary legal
frontier here is claimed to arise from the lone-seed orbit.

## Minimal counterexample, including the invariant sectors

**Proposition.** The following equality of entire ancestor sets holds:

```
C_3(0) = C_3(00)
       = {201, 211, 220, 221, 230, 231, 302, 312}.
```

**Exact finite proof.** Evaluate the scan on all 32 legal words of length
three. Exactly the displayed eight words survive with first scalar zero.
Their next transitions are

| Original ancestors | First update | Second update |
|---|---|---|
| `201,211,220,221,230,231` | `--0--> 2103` | `--0--> 21303` |
| `302,312` | `--0--> 3203` | `--0--> 30303` |

Thus every candidate after tape `0` also realizes the repeated scalar.
The exhaustive calculation is implemented below using a polynomial GF(2)
scan and independently checked against the frozen Boolean scan. Exhausting
the two legal length-one starts and eight length-two starts finds no repeat
at all. Therefore r=3 is minimal, and tape length two is necessarily minimal.

Conditioning further on the invariant sector `beta=b_0` does not repair
strict decrease: the first table row has sector zero and six ancestors;
the second has sector one and two ancestors. Both sector-specific sets
remain exactly unchanged. Consequently neither strict decrease nor a factor
of two contraction holds for every repeat.

## Two successive repeat edges can also be free

Exact enumeration at initial length six gives equality of entire sets:

```
C_6(101) = C_6(1011) = C_6(10111),  cardinality 36.
```

Both appended ones repeat the preceding scalar, yet neither removes an
ancestor. The JSON artifact lists all 36 starts and a complete example
replay. This also excludes charging one strict cardinality decrease to
every pair of consecutive repeats.

This is a finite counterexample, not a proof of arbitrarily long plateaus.
The existing inverse-crossing-count pumping family concerns different
projected statistics; its fixed feature values do not establish equality
of these full ancestor sets at arbitrary lengths.

## Verification and remaining scope

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/fixed_origin_history_count.py
```

The standalone verifier enumerates every legal start of exact lengths 1–7,
checks every attempted update against the unchanged `panel/cert33.py`, and
counts all accepted chronological prefixes. A lifetime cap raises an error
instead of returning a completed census. It writes
`experiments/rule30/fixed-origin-history-count.json`, including both explicit
candidate sets, the per-length results, and source hashes.

Ancestor cardinality remains a nonincreasing integer, but the proved
plateaus prevent charging repeats individually, or in every consecutive
pair, to its decrease. An amortized decrease allowing longer plateaus,
or a different history-conditioned quantity, remains possible. No bound
on all plateau lengths, repeat budget, mortality, P1, or P2 is established
or refuted by this calculation.

Follow-up, 2026-09-11: the same 36 length-six starts also satisfy
`C_6(10111)=C_6(101110)=C_6(1011100)`. Thus three repeat edges can occur
without changing the whole ancestor set. This disproves the absolute bound
`|C_r(alpha)|*4^D<=2^(2r-1)`, while the weaker one-bit bound
`|C_r(alpha)|*2^D<=2^(2r-1)` remains an unproved sufficient target. See the
[aperiodic mortality audit](RESULTS-aperiodic-mortality-audit.md) for the
conditional mortality implication, exact verifier, and finite scope.

Further follow-up, 2026-09-11: the
[weighted endpoint report](RESULTS-weighted-history-endpoints.md) gives a
55,885,140-member length-24 class with eight repeat edges and no change in its
complete original ancestor set. It also proves the uniform reconstruction
corollary `C_r(alpha beta)` is either empty or exactly `C_r(alpha)` whenever
`|alpha|>=r`. Every surviving class has synchronized by that time, so no further
successful extension can remove only part of it. This does not bound its
remaining repeats or prove the cumulative information inequality.

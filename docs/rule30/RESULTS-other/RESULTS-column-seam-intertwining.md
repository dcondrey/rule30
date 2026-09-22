# Three capacity-18 families have only one effective history parameter

Status: **exact all-temporal-depth intertwining identities are proved**.
They reduce three two-parameter endpoint families to one parameter while
preserving their entire guarded scalar history. This is a structural
identity, not an inference from equal finite orbit sizes. No new mortality
orbit or original-frontier census is run.

For temporal depth `n`, let `Phi_w` be the full column operator obtained
by reading spatial word `w` from left to right in the exact auxiliary
bulk dynamics. Its input is a previous-column record
`(p,(u_1,v_1),...,(u_n,v_n))`; `p` is its original high bit. The result
below holds for every choice of the temporal pairs.

## 1. Exact seam identities

For every `n>=0`,

\[
 \Phi_{03131}(q)=\Phi_{13031}(q)
       \quad\text{whenever }p(q)=1.                       \tag{1}
\]

Equivalently, scanning the repeat block `31` after the seam `031` is
the same as scanning `13` before that seam. The high-bit restriction
is part of the theorem. It cannot be removed.

There is also the derived identity

\[
 \Phi_{303131}(q)=\Phi_{313031}(q)
       \quad\text{whenever }p(q)=0.                       \tag{2}
\]

Indeed both words start with the same `3`, which sets the column's
original high bit to `1`; their remaining words are exactly the two
sides of (1). Thus the seam `3031` commutes with the repeat block `31`
on the stated slice.

**All-length certificate.** A spatial letter is an eight-state vertical
Mealy machine. Its memory is `(previous,a,b)`, initialized with the old
original high bit and the spatial input letter `2a+b`. On reading one
old temporal pair `(u,v)`, it computes

\[
 V=v\mathbin\oplus(previous\mathbin\lor b),\qquad
 U=u\mathbin\oplus(V\mathbin\lor a),
\]

emits `(U,V)`, and changes its memory to `(u,U,V)`. A spatial word is
the ordered cascade of these machines. The initial `previous` value
of each later machine is the preceding spatial letter's high bit.

The complete reachable product comparing the two sides of (1) has
**143 states and 572 labeled edges**. Their emitted pairs agree on
every edge. Both output original high bits are `0`. Induction on the
number of input temporal pairs proves (1) for arbitrary `n`.
An additional complete product verifies (2) directly, with **283 states
and 1,132 edges**, independently of the shared-prefix deduction above.

## 2. Three exact reductions with every chronological guard retained

Each expression below is a **full second endpoint**, including its two
birth symbols. All exponents are independent nonnegative integers.
The indices are the zero-based indices in `capacity-32-language.json`.

| Pattern | Full endpoint | Endpoint with the same complete scalar history |
| --- | --- | --- |
| 5 | `21213(13)^a031(31)^b303` | `21213(13)^(a+b)031303` |
| 12 | `213(13)^a031(31)^b303` | `213(13)^(a+b)031303` |
| 27 | `3031(31)^a3031(31)^b303` | `3031(31)^(a+b)3031303` |

The prefixes in the first two rows end in `3`, so their entering high
bit is `1`; each intervening `13` block preserves that bit. Repeated
use of (1) moves all `b` blocks across the seam and replaces them by
`13` blocks. The last row uses (2), with entering bit `0` preserved by
every `31` block. The complete final column therefore agrees at every
temporal depth, after the common suffix has also been read.

The [guarded terminal-signature theorem](RESULTS-cumulative-history-transfer.md#3-a-tape-specifies-exactly-two-accepting-column-states)
says that a full terminal column accepts a prescribed scalar tape
exactly when every chronological guard and every birth constraint is
satisfied. Equal full columns for every depth thus imply the same
successful tapes and the same first failed update. This includes all
births after the second endpoint; the suffix is never reset.

The [capacity-18 language certificate](../../experiments/rule30/capacity18-language-audit.json)
assigns exact original fiber size `18` and first two scalars `00` to
every displayed endpoint. Each pair of endpoints has the same length.
Their original ancestor sets need not coincide: the conclusion is
equality of their subsequent histories, retaining the original
two-step ancestry separately for each endpoint.

There is a useful counting corollary. Fix `k=a+b` within any one row.
The `k+1` splits yield distinct endpoints: the moving seam changes
the first `0` position in rows 5 and 12, and the second `0` position
in row 27. Their original fibers are disjoint, each of size `18`.
Consequently every finite prefix `alpha` of their common complete
original tape satisfies

\[
 |C_r(\alpha)|\ge18(k+1),                         \tag{3}
\]

where `r=2k+9` for rows 5 and 27, and `r=2k+7` for row 12.
This is a lower bound for these particular common histories, not the
unproved cumulative upper bound for arbitrary histories.

## 3. The harder seam does not satisfy the same global identity

The proposed full-slice commutation
`Phi_121313=Phi_131213` with entering high bit `1` is false already
at temporal depth one. Give it the input pair `(u,v)=(0,0)`. The
respective output pairs are `(0,1)` and `(1,1)`; the packed full
output columns are `3` and `7`.

This is a counterexample to an operator identity on the entire slice.
It does not assert that this particular input column occurs after an
admissible family prefix. Prefix-dependent relations for the harder
`1213` seam remain a separate question.

For completeness, the exact verifier also retains the depth-one
counterexamples to removing the `p=1` restriction in (1), and to the
analogous global relations `21313=31213` at `p=0` and `1000=2100` at
`p=1`. None of these local failures is a mortality counterexample.

## 4. Maintained verification

The [verifier](../../experiments/rule30/column_seam_intertwining.py) saves
the complete product vertices and edges in
[column-seam-intertwining.json](../../experiments/rule30/column-seam-intertwining.json).
It also checks all 32 local memory/input cases and 680 complete-column
controls at temporal depths one through four against the existing
`column_step` engine, which uses the opposite loop order. These finite
controls check the implementation; the closed products prove the
unbounded identities. All four failed global identities retain exact
input and output columns. Source hashes are saved.

The remaining four two-parameter capacity-18 families are not reduced
by this report. No unrestricted mortality, positive-rate cumulative
information estimate, RW separator, or period-two exclusion follows
from these three reductions alone.

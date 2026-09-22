# Exact non-compression certificates for Rule 30 blocks of sizes one through eight

Date: 2026-09-10. **Finite classification, all input configurations;
no arbitrary-size theorem and no P1/P2/P3 solution.**

For each n=1,...,8, group a configuration into consecutive blocks of n bits
and advance Rule 30 by n time steps. Every block projection that admits
exact autonomous evolution is either constant or injective. Thus no proper
nonconstant state compression works at these sizes, regardless of the number
of symbols allowed in the output alphabet.

This is an independently reproducible result within the established
coarse-graining program. It does not claim literature priority. See the
prior-work discussion in the [investigation summary](RESULTS-p2-defect-route-investigation.md).

## 1. The algebra tested

Let A_n={0,1}^n. For a,b,c in A_n, let g_n(a,b,c) be the n-bit word left
after applying the local Rule 30 update n times to the concatenation abc,
discarding the two exterior cells at each step. This is exactly the central
output block after n time steps; its causal cone is contained in abc.

A projection pi:A_n->B admits a coarse local rule if

\[
\pi(g_n(a,b,c))=h(\pi(a),\pi(b),\pi(c))
\]

for all a,b,c. Equivalently, equality of projection labels must be an
equivalence relation preserved by g_n in each of its three arguments.
Such an equivalence relation is called a congruence of this finite algebra.

It is enough to prove that every congruence identifying any two distinct
states identifies all states. Equality and the universal relation always
remain, corresponding to injective and constant projections.

## 2. Four necessary maps suffice

Write 0 for the all-zero n-bit word and 1 for the all-one n-bit word.
Any congruence of g_n must be preserved by these four unary maps:

\[
A(u)=g_n(u,0,0),\qquad B(u)=g_n(u,0,1),
\]
\[
C(u)=g_n(0,u,0),\qquad D(u)=g_n(0,u,1).
\]

The symbols 0 and 1 in these formulas mean words, not integer encodings.
The executable uses integer 2^n-1 for the all-one word.

For each specified n, the certificate has two parts:

1. Every unordered pair of distinct states has a nonnegative integer depth.
   A recorded unary map sends it to a distinct pair of strictly smaller
   depth, except for one terminal pair of depth zero. The terminal pair is
   {0,2} in integer encoding at n=2, and {0,1} for the other listed sizes.
2. Starting with the terminal pair as an equivalence, a list of 2^n-1
   successful merges connects all states. Every merge after the first is
   the image of an earlier merge under one recorded unary map.

Here the pairs in the second part are integer encodings; {0,1} there is not
the zero-word/all-one-word pair except at n=1.

If a congruence identifies any distinct input pair, preservation under the
maps and strict depth descent force identification of the terminal pair.
The second certificate then forces all its listed merges, whose graph is
connected. Hence the congruence is universal. This is a finite proof by
exact integer checks, not sampling of candidate projection functions.

| n | Block states | Distinct pairs checked | Maximum descent depth | Spanning merges |
|---:|---:|---:|---:|---:|
| 1 | 2 | 1 | 0 | 1 |
| 2 | 4 | 6 | 2 | 3 |
| 3 | 8 | 28 | 5 | 7 |
| 4 | 16 | 120 | 12 | 15 |
| 5 | 32 | 496 | 5 | 31 |
| 6 | 64 | 2,016 | 7 | 63 |
| 7 | 128 | 8,128 | 10 | 127 |
| 8 | 256 | 32,640 | 11 | 255 |

The proof covers every partition at these sizes, including those with more
than two classes. It avoids enumerating the much larger space of partitions.

## 3. What the theorem does and does not exclude

The universal conclusion also excludes an evolution inspecting more of the
projected field. If a projection's equivalence fails a unary-map constraint,
put the corresponding three blocks into two otherwise identical finite
configurations. Their complete projected fields coincide, but their next
projected central blocks differ. No function of that whole projected field
can determine both outputs.

All statements concern a fixed block alignment and exactly n original time
steps per coarse step. Other spacetime sampling schemes are outside the
tested family. The argument permits arbitrary input configurations; it does
not prove that its larger-block witnesses occur on the lone-seed orbit.
The [pair report](RESULTS-dyadic-pair-factor-obstruction.md) separately gives
actual-seed witnesses for radius-one two-cell projections.

No induction proving the result for every n was found. In particular, one
cannot replace the certificates by an assertion that B is a full cycle:
at n=3 it has two cycles of length two and one of length four. At n=4 it
has four cycles of length four. These cycle structures are also checked.

Even an arbitrary-size theorem in this representation would need a separate
argument to imply a center-column property. Non-compressibility of these
block states is neither a temporal cancellation bound nor a computational
lower bound against every algorithm.

## 4. Independent replay

Run without modifying the saved certificate:

```
uv run python experiments/rule30/supercell_congruence_certificate.py
```

The [verifier](../../experiments/rule30/supercell_congruence_certificate.py)
recomputes all four maps from Rule 30, checks every map entry with a separate
list-of-bits implementation, then checks every descending pair step and
every spanning merge in the
[certificate](../../experiments/rule30/supercell-congruence-certificates.json).
There is no floating-point arithmetic or external solver.

The producer can regenerate the bundle with `--generate`. Generation and
verification are separate: replay checks only the finite proof obligations
and does not trust the search procedure that selected the maps or merges.

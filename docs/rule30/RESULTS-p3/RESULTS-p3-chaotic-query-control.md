# A known expanding-map orbit with an exact fast digit query

Date: 2026-09-13. **Positive control only: this is neither a new theorem nor
a Rule 30 shortcut.**

Let `d_0 d_1 ...` be the concatenation of the binary representations of
`1,2,3,...`, beginning `11011100101110111`. Put

\[
x=\sum_{n\ge0}d_n2^{-n-1},\qquad D(x)=2x\pmod1.
\]

This is the binary Champernowne construction. Its digit stream has infinitely
many zeros and ones, so its binary expansion is unambiguous. The leading
binary digit of `D^n(x)` is exactly `d_n`. The map doubles distances locally,
but that fact does not require computing this specified orbit sequentially.
No normality claim is needed for this control.

There are `k*2^(k-1)` digits in the block of all positive `k`-bit integers.
Its cumulative endpoint is

\[
S(k)=\sum_{j=1}^k j2^{j-1}=(k-1)2^k+1,\quad S(0)=0.
\]

For a zero-indexed digit query `n`, locate the unique `k` satisfying
`S(k-1)<=n<S(k)`. Write

\[
n-S(k-1)=qk+r,\quad0\le r<k.
\]

Then `n` lies at position `r`, from the left, in the binary representation
of `m=2^(k-1)+q`, and

\[
d_n=\left(\left\lfloor m/2^{k-1-r}\right\rfloor\bmod2\right).
\]

This is a complete exact algorithm. Its block search uses `O(log(n+2))`
iterations on `O(log(n+2))`-bit integers. Charging each arithmetic operation
conservatively by the square of its operand length gives
`O(log^3(n+2))` bit work, including block location, division, and extraction.
No table depending on `n`, stored digit prefix, or approximation of the real
number to `n`-bit precision is used.

[The implementation](../../experiments/rule30/p3_chaotic_query_control.py)
and [saved artifact](../../experiments/rule30/p3-chaotic-query-control.json)
check all 9,217 digits obtained by literally concatenating integers through
1,023, the cumulative-sum formula at 33 block lengths, and 45 exact boundary
cases, including indices near `S(4096)`. The latter are checked from the
first and last integers of each specified block, without constructing the
enormous digit prefix. The run passed in approximately 0.011 seconds.

The relevance to P3 is limited and concrete: sensitivity of an expanding
map does not by itself forbid fast exact queries on a particular explicitly
described orbit. Rule 30 would need its own index-to-answer construction;
the block-address formula above does not supply one.

```sh
uv run --offline --no-project python experiments/rule30/p3_chaotic_query_control.py
```

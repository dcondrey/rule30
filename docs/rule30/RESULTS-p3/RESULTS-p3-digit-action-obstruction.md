# Small nilpotent digit actions cannot predict the singleton center

Status: **proved restricted index-predictor obstruction through nilpotency
class three**, plus a class-four extension supported by existing cached
singleton data. The theorem is
about the actual singleton queries `n -> c_n`, not a center function with a
variable initial row. It gives no unrestricted running-time or memory lower
bound and does not settle P3 or any unresolved periodicity case.

## 1. Exact index witnesses

With `c_0=1` at the initial singleton,

\[
c_{22}=1,\qquad c_{25}=0.
\]

The canonical binary indices are `10110` and `11001`. Both have length five,
two zeros, three ones, and four scattered occurrences of `10`. Their complete
scattered-pair counts agree:

| Pair | `00` | `01` | `10` | `11` |
|---|---:|---:|---:|---:|
| Count in either index | 1 | 2 | 4 | 3 |

Consequently no decoder of only the length, digit counts, and these ordered
pair counts computes all singleton center queries. The decoder may be an
arbitrary function: the two equal summaries already contradict correctness.

## 2. An algebraic model class excluded by the same witnesses

Let `A` and `B` be two fixed invertible state updates for digits zero and one.
Assume their commutator is central in the group they generate. The state set
and generated group may be finite or infinite. A predictor processes the
binary index by these updates and then decodes the final state. Its initial
state and decoder may depend on the binary input length.

**Theorem.** No such predictor computes `c_n` for every canonical binary index.
In particular, this excludes every fixed two-generator action of a nilpotent
group of class at most two, including every choice of digit actions in `D8`.

**Proof.** Write `K=[B,A]=B^-1 A^-1 B A`, so `BA=ABK`. Since `K` is central,
collecting a binary word moves all `A`s left and all `B`s right, with one
factor `K` per scattered `10`. Hence the two words are identical group
elements:

\[
B A B B A=B B A A B=A^2B^3K^4.
\]

Spaces are only typographical: the left word is `B A B B A`, corresponding
to `10110`, and the other is `B B A A B`, corresponding to `11001`.
Equivalently, their tails satisfy

\[
AB^2A=BA^2B=A^2B^2K^2.
\]

Thus dropping the common leading one does not evade the identity. Reading
least-significant digits first, or writing function composition in the
opposite order, also gives equal products: reversal preserves the equality
of digit counts and transforms both inversion counts in the same way.

The two inputs have the same length, so the permitted initial states and
decoders are identical. Equal actions produce equal final states, contrary
to `c_22 != c_25`. This proves the theorem.

For the `D8` application, the presentation `r^4=s^2=1`, `srs=r^-1` gives
commutator subgroup `{1,r^2}`, which is central. The verifier independently
checks every one of its 64 ordered choices of digit generators.

The tail identity also holds for any two involutions, without assuming
class two, because both sides are the identity. This is a further restricted
class excluded by the same two singleton queries.

## 3. What this says about endpoint-derived algorithms

The endpoint machinery's four-sheet transport belongs to `D8`, but its
sections depend on the complete lower state. Replacing that recursion by
one fixed pair of `D8` digit updates would fall into the excluded class.
The obstruction therefore supplies a small exact test for a proposed
binary-index transfer: it must distinguish these two indices by information
or state-dependent updates beyond this fixed group action.

The theorem permits neither an extra decoder argument containing the full
index nor index-dependent preprocessing hidden in the starting state. Either
would remove the model restriction. Arbitrary length-dependent initialization
and decoding are allowed because both witness indices have length five.
This is a state-identity obstruction, not a complexity result. Any proposed
algorithm outside this class must still charge construction, preprocessing,
operand sizes, and decoding before claiming a time bound.

## 4. Verification and official P3 scope

The [verifier](../../experiments/rule30/p3_digit_action_obstruction.py) and
[artifact](../../experiments/rule30/p3-digit-action-obstruction.json) retain
both singleton queries, their exact digit signatures, and all 64 `D8`
generator-pair controls. The center values are checked independently by a
literal finite-set evolution and the maintained bit-row engine. Rule90 and
Rule150 controls give equal center values at these indices, as required for
this obstruction to leave their simple predictors available. No large scan
or variable-frontier census is used.

Checked on 2026-09-13, the [official prize page](https://rule30prize.org/)
still phrases P3 using “at least O(n) computational effort.” Its linked
[announcement](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/)
still gives a displayed predicate excluding a correct finite machine with
finite `limsup T(n)/n`. That predicate excludes `O(n)` algorithms; it is not
equivalent to either an eventual `Omega(n)` lower bound or exclusion of
`o(n)` algorithms. The repository's [scope audit](P3-SCOPE-AUDIT.md) therefore
still applies. The present restricted-class theorem asserts none of those
unrestricted predicates.

## 5. An all-class word identity and two stronger finite witnesses

There is a precise family of candidate collisions. Define positive binary
words

\[
u_0=0,\quad v_0=1,\qquad
u_{k+1}=u_kv_k,\quad v_{k+1}=v_ku_k.
\]

For any two group elements interpreting the digits, let `gamma_1(G)=G` and
`gamma_(j+1)(G)=[gamma_j(G),G]` be the lower central series of the group they
generate. Then

\[
u_kv_k^{-1}\in\gamma_{k+1}(G)\qquad(k\ge0).
\]

**Proof.** The base case lies in `G`. If `d=u_kv_k^-1` belongs to
`gamma_(k+1)`, substitution `u_k=d v_k` gives

\[
u_{k+1}v_{k+1}^{-1}
 =u_kv_ku_k^{-1}v_k^{-1}
 =d v_k d^{-1}v_k^{-1}\in\gamma_{k+2}(G).
\]

Thus `u_k=v_k` in every nilpotent group of class at most k. Any common
binary prefix or suffix preserves this equality. This all-k word identity
is proved. Separation by the Rule30 singleton sequence is verified only at
the specific pairs below; there is no asserted all-k separation theorem.

At `k=3`, `u_3=01101001` and `v_3=10010110`. The initial trial with common
prefix `1` gives indices 361 and 406, both with center value zero. Prefix `10`
instead gives

\[
c_{617}=1,\qquad c_{662}=0.
\]

These two values are recomputed by the literal singleton set evolution and
the independent bit-row engine. **Therefore no fixed digit-action predictor
in the stated model with nilpotent generated group of class at most three
computes all singleton center queries.** This is a complete finite witness
to that restricted theorem, not a growth estimate.

At `k=4`, the common prefix `1` gives

\[
1u_4=10110100110010110=92566,\qquad
1v_4=11001011001101001=104041.
\]

The stored values are `c_92566=0` and `c_104041=1`. They support the same
exclusion through class four. Their validation status differs from the
class-three witnesses: this run reads them from two existing archives and
does not regenerate the corresponding Rule30 prefix.

| Existing archive | Payload offset | Bit order |
|---|---:|---|
| `rule30-subword-extended/rule30_center_8388608.bin` | 0 | Least significant bit first |
| Official WDR billion-bit container in `a20_deep_simulation/ref` | 239 bytes | Most significant bit first |

The verifier independently redetermines both alignments using the exact
first 64 bits, reads the two requested bits, and retains full file hashes,
byte offsets, byte values, and bit shifts. It also checks the WDR container
against its previously stored checksum. The
[prior WDR validation](../../experiments/overnight-arms/frontier_attack/a20_deep_simulation/crosscheck_wdr_final.json)
records agreement with the 100,001-term OEIS file and a 1,980,000-bit independent
simulation. That prior validation is provenance, not a new proof run here.
If either archive is unavailable, the verifier reports the cache-supported
extension unavailable; it does not silently upgrade it to a recomputed
theorem. No class-five query or long-prefix regeneration is performed.

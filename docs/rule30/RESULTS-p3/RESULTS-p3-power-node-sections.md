# Exact exponent division in ordered itinerary sections

Date: 2026-09-13. **A power node can be sectioned by dividing its exponent
along the exact root-digit orbit, without expanding that exponent.** The
implementation retains the complete ordered return word and the remainder.
This makes exponent division constructive, but does not close the family
of return words or skip the linear number of digit advances in the current
singleton query.

The [source](../../experiments/rule30/p3_power_node_sections.py) and
[artifact](../../experiments/rule30/p3-power-node-sections.json) extend the
[quaternary section evaluator](RESULTS-p3-itinerary-conjugacy.md) with explicit
power nodes. They preserve the previous implementation as a comparison
control. This concerns powers of an **action word**, distinct from the
[one-pass transduction of a repeated input word](RESULTS-p3-itinerary-repeat-transduction.md).

## 1. The universal power-section identity

Let U be any finite chronological word in A,B,C, let p be its permutation
of the first base-four digit, and let d be the actual entering digit.
Write its complete root orbit as

```
d_0=d, d_1=p(d), ..., d_(q-1)=p^(q-1)(d), p^q(d)=d.
```

The q digits are distinct, so q<=4. Define the chronological words

```
R_d(U)=U|d_0 U|d_1 ... U|d_(q-1),
S_(d,r)(U)=U|d_0 U|d_1 ... U|d_(r-1),  S_(d,0)=identity.
```

For n=qk+r with 0<=r<q,

```
(U^n)|d = R_d(U)^k S_(d,r)(U).                    (1)
```

**Proof.** In the jth copy of U, the entering digit is p^j(d).
The section law therefore concatenates U|p^j(d) in chronological order.
Each group of q copies returns the entering digit to d, and has the same
ordered section R_d(U). The remaining r copies start again at d and
produce the stated S. This argument retains every seam and applies to
every higher input tail. It is not an equality inferred from zero-output
samples.

If n<q, only the first n child sections are required. Otherwise there
are q child-section requests, at most four. Constructing their return
and remainder needs a bounded number of new concatenation and power
nodes. This bound does **not** make the recursively requested child
sections free.

For the initial C power the formula is especially simple:

```
(C^(2k))|0   = (CA)^k,
(C^(2k+1))|0 = (CA)^k C.                          (2)
```

Thus the division by two is an exact operation. Its new action is CA,
whose root orbit has length four; the next complete return is
`CBCCBCAA`. The [return-class report](RESULTS-p3-itinerary-return-classes.md)
gives exact guarded reductions and proves why CA cannot simply be
replaced by B through a prefix-compatible conjugacy.

## 2. What the smaller exponent does and does not measure

Every ABC letter has one ABC letter as each section. If U has length L,
then R_d(U) has length qL and S_(d,r)(U) has length rL. In particular,

```
|R_d(U)^k S_(d,r)(U)| = qL*k+rL = nL.             (3)
```

The exponent decreases while the return word grows. Equation (3) is a
conservation identity for **expanded positive-word length**, not a lower
bound on compressed computation. A power node or shared expression may
still be much smaller. What is missing is a useful bound on the size and
construction work of that expression under many sections, or an operation
that directly computes the requested digit after many sections.

It would therefore be incorrect to count only the number of exponent
divisions and conclude logarithmic time. Conversely, it would be
incorrect to infer a general linear lower bound from (3).

## 3. Implemented construction and finite controls

The expression language has identity/letter, binary concatenation, and
power nodes. Each node stores its actual four-digit permutation and
expanded length. Concatenation passes the first child's actual output
digit to the second child. A power uses (1). Nested powers multiply
their exponents; no exponent-sized word is allocated. Exact tuple
interning and section memoization retain shared nodes.

The current query still starts with C^(h+1), where h=floor(n/2), and
executes h zero sections for odd n, or h-1 for positive even n. Its final
root-digit readout is the proved singleton-center formula. Therefore its
correctness follows for every n from the existing reduction and (1).
Its current loop still has a linear number of advances.

| Query n | Advances | New power-node grammar | Previous concatenation grammar |
|---:|---:|---:|---:|
| 8 | 3 | 13 nodes | 17 nodes |
| 17 | 8 | 32 nodes | 38 nodes |
| 32 | 15 | 92 nodes | 90 nodes |

The construction is not a uniform improvement even in these small node
counts. Powers also carry exponents and require arithmetic. The artifact
records root-orbit steps, composed permutation entries, arithmetic operand
bit lengths, and the logical node metadata size. These counters are not
wall-time ratios or complete Turing-machine operation counts; dictionary
access, allocation, cache storage, and integer arithmetic remain charged.

As a directed large-exponent control, the verifier computes the zero
section of C^(10^30+1), retaining the result `(CA)^(5*10^29) C`. Including
a separate fixed A-power control, the construction has nine nodes and
five distinct section contexts. The exponent has 100 bits; the retained
node metadata has 791 bits. This checks one exact power section, not a
singleton query at an enormous index or a jump over many digit positions.

The verifier checks 48 specified word/exponent combinations at all four
entering digits against an independent literal arithmetic scan, plus a
nested mixed power at all four digits. The six tiny singleton queries
agree with both the earlier evaluator and independent row evolution.
The all-length identity is proved in section1; these bounded controls
check its implementation, including remainders and ordered seams.

```
uv run --offline --no-project python experiments/rule30/p3_power_node_sections.py
```

No exact sublinear singleton algorithm, unrestricted lower bound, or new
P1/P2 exclusion follows.

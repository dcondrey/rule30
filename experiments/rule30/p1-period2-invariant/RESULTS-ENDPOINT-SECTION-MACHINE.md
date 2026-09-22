# Exact endpoint sections and two safe source-prefix rewrites

Status: **all-length section identities and two source normalization rules
are proved**. The RW/DLP separator, period-two exclusion, and P1 remain
open. No horizon census is extended here.

The main usable conclusions are

\[
 F^3(122v)=F^3(222v),\qquad
 F^3(2122v)=F^3(2222v)                              \tag{1}
\]

for every finite four-state suffix `v` (with the empty-output convention
when necessary). Each rewrite removes one source symbol `1`. Used entirely
within the binary source block `W`, the first is safe for RW at `n>=3`,
and the second at `n>=4`. Both leave the hard-core suffix, its junction,
the terminal `12a` pull, and the selected tail `c=2` or `c=3` intact.

These are prefix rules. The next attempted internal extension,
`22122 -> 22222`, is false. Consequently (1) is not an unrestricted
rewrite system that reduces every source to a homogeneous word.

Subsequent [defect-cocycle analysis](../../../docs/rule30/RESULTS-rw-defect-cocycle.md)
retains that failure and computes its exact suffix-independent correction
at `F^3`. It proves a longer padded rewrite at every source depth, as well
as `2212222 -> 2222222` at `F^7`. The short failed erasure therefore does
not terminate the investigation of source rewrites.

## 1. Exact deck actions retain the complete suffix

Use `I`, `T=I^-1`, `P`, `F=T P I`, and the boundary permutation `B`
from the [rotated-wedge report](RESULTS-DLP-ROTATED-WEDGE.md).
The first endpoint symbol together with `F(e)` determines `e` uniquely:
`I(e)_0=B(e_0)` is fixed, and each row of `phi` is a permutation, so the
Peel output determines the remaining cut cells successively.

For any permutation `mu` of the four endpoint symbols, define `K_mu(e)`
to be the unique word with first symbol `mu(e_0)` and the same `F` image
as `e`. Set `K_mu(empty)=empty`; this includes the one-symbol suffix case
of (3), where `F(e)` is empty. Equivalently, on nonempty cuts, replace the first symbol `x_0` by
`B mu B(x_0)` and take the unique lift of the same Peel output. Thus

\[
 F K_\mu=F,\qquad K_\mu K_\nu=K_{\mu\nu}.        \tag{2}
\]

If `mu` fixes the first symbol of a word, `K_mu` fixes that entire word.
The definition retains the whole ordered suffix. It does not replace that
suffix by its first symbol or by a group element.

Four permutations suffice for the sections below, listed by their images
of `0,1,2,3`:

\[
 p_0=(0,1,2,3),\quad p_1=(1,0,2,3),\quad
 p_2=(2,3,1,0),\quad p_3=(2,3,0,1).
\]

For a nonempty suffix `e`, the complete section identity is

\[
 F(qe)=R_q(e_0)\;K_{p_{D_q(e_0)}}(F(e)),           \tag{3}
\]

where rows and columns of the following tables use the four-state order.

| `q` | `R_q(0),R_q(1),R_q(2),R_q(3)` | `D_q(0),D_q(1),D_q(2),D_q(3)` |
| --- | --- | --- |
| 0 | 2,3,1,0 | 0,0,0,0 |
| 1 | 0,1,3,2 | 0,0,1,1 |
| 2 | 1,0,2,3 | 0,0,0,0 |
| 3 | 3,2,0,1 | 2,1,3,0 |

**All-length proof.** Put `a=phi(q,B(e_0))`, `r=R_q(e_0)`, and
`mu=p_(D_q(e_0))`. The endpoint-prefix grammar gives

\[
 I(qe)=(B(q),a)\;P(I(e)).
\]

The complete local table verifies

\[
 B(r)=\phi(B(q),a),\qquad
 \phi(r,B\mu B(y))=\phi(a,y)\quad\text{for every }y.\tag{4}
\]

The lift defining `K_mu` has the same Peel image, so (4) and the
endpoint-prefix grammar identify every cell of the two sides of (3)
after applying `I`. Bijectivity of `I` proves (3). No bound on the suffix
length is used.

For a binary endpoint, the only active correction in (3) is a `121`
motif. In particular, `F(12v)=3 K_(01)(F(2v))`; if `v` begins with `2`,
then `F(2v)` begins with `2`, and the deck action fixes it. This observation
does not say that subsequent images remain in the binary or hard-core
language. Their `0` and `3` residues must be kept.

## 2. A seven-state machine for the full ordered action

Define the finite-word bijection

\[
 J(e)=(e_0,F(e)_0,F^2(e)_0,\ldots).
\]

Its bijectivity follows inductively from uniqueness of the pair
`(e_0,F(e))`. In these coordinates `F` deletes the first symbol, while
`K_mu` changes only that symbol by `mu`.

Prefixing an endpoint symbol `q` has the exact form

\[
 J(qe)=q\;S_{(q,0)}(J(e)).                         \tag{5}
\]

The formal machine state is `(a,m)`, and its update on input `s` is

\[
 z=p_m(s),\qquad b=R_a(z),\qquad
 \text{output }b,\quad\text{next state }(b,D_a(z)). \tag{6}
\]

To prove (6), apply (3) to `a K_(p_m)(u)` and use `F K_(p_m)=F`.
Induction over the remaining word proves (5) at all lengths. Each output
row is a permutation, so these are invertible letter-to-letter actions.

There are 16 formal states. Exact partition refinement gives 14 classes:
`(0,3)` equals `(2,0)`, and `(2,3)` equals `(0,0)`. The raw reachable set
from the four prefix starts has eight states, including both `(0,3)` and
`(2,0)`. After their exact identification, the reachable machine has
**seven** states:

| State | Representative | Output permutation | Sections on inputs `0,1,2,3` |
| --- | --- | --- | --- |
| A | (0,0) | 2,3,1,0 | C,E,B,A |
| B | (1,0) | 0,1,3,2 | A,B,F,D |
| C | (2,0) | 1,0,2,3 | B,A,C,E |
| D | (2,1) | 0,1,2,3 | A,B,C,E |
| E | (3,0) | 3,2,0,1 | G,D,C,B |
| F | (3,1) | 2,3,0,1 | D,G,C,B |
| G | (3,2) | 0,1,2,3 | C,B,D,G |

The seven states are minimal. Their root permutations distinguish every
pair except `D,G`, which the input word `00` distinguishes. This is an
all-word machine minimization, not minimization against a finite sample.

The growing object is still an **ordered composition of machine actions**.
Seven machine states do not mean seven possible reconstruction frontiers.

For both RW tails, this representation retains the exact target:

\[
 P^n I(f)=c^{n+r+2}
 \quad\Longleftrightarrow\quad
 J(f)[n:]=(3-c)3^{n+r+1},\qquad c\in\{2,3\}.       \tag{7}
\]

Indeed `P(c^m)=0^(m-1)` for either tail and `P(0^m)=0^(m-1)`.
Equation (7) does not remove the binary source, the hard-core junction,
or the terminal `12a` conditions. It is not itself a separator proof.

## 3. Source rules certified by complete action equality

For a fixed endpoint block `w`, define its suffix action `M_w` by

\[
 J(wv)=J(w)\;M_w(J(v)).                            \tag{8}
\]

Composition is written leftmost after rightmost. From (5), prefixing `q`
to a block `w` gives

\[
 M_{qw}=S_{(q,0)}|_{J(w)}\,M_w.                    \tag{9}
\]

The exact hard-core gap blocks have

| Block | `J` prefix | Suffix action |
| --- | --- | --- |
| 12 | 13 | FC |
| 122 | 130 | C^3 |
| 1222 | 1302 | C^4 |
| 12222 | 13022 | C^5 |

Here `J(2^k)=2^k`, `M_(2^k)=C^k`, and the section of `B` after input `2`
is `F`, while after two or more consecutive `2`s it is `C`. The table
therefore follows for arbitrary suffixes, including those outside the
hard-core language.

For `122` and `222`, the suffix actions are both `C^3`, so their `J`
images agree after the first three coordinates. For `2122` and `2222`,
the suffix actions are both `C^4`, and the fourth coordinate of their
`J` prefixes `2002` and `2222` also agrees. This proves both identities
in (1), with three iterations sufficient in each case.

There is an independent local proof. The cut prefixes for `122v` and
`222v` are `(2,2,1)` and `(1,2,1)`, with all later cells equal. Successive
Peel rows leave first-cell pairs `(0,1)` and then `(3,1)`; the next row
coalesces because `phi(3,s)=phi(1,s)` for every `s`. For `2122v` and
`2222v`, the cut prefixes are `(1,0,0,2)` and `(1,2,1,2)`, with all
later cells equal. One row leaves the three pairs `(3,1),(0,2),(3,1)`;
two rows leave only the first pair `(3,1)` unequal; the third coalesces.
Equality of later cut cells follows from the prefix grammar in the first
case and the inverse-cone dependency interval in the second.

For RW, an occurrence of one of these patterns at the **beginning of W**
can be replaced when the displayed pattern is contained in `W`. The
length and binary alphabet are preserved. No symbol at the junction or
in the hard-core continuation is changed, nor is the terminal pull.
The required `F^n` image is unchanged because `n>=3`. This argument works
for both target tails and all three residues. It strictly reduces the
number of `1`s for these admitted prefix rules; it does not supply a
reduction for every source word.

## 4. The first failed extension and the retained residual

The seemingly natural extension `22122 -> 22222` has respective suffix
actions `BC^4` and `C^5`. Their root permutations already differ.
With the common continuation `Q=1212121`, both words have the required
hard-core junction and terminal `121`, but

\[
 F^5(22122Q)=1333210,\qquad
 F^5(22222Q)=0333210.
\]

Neither output asserts an RW witness. They refute an unconditional
internal erasure identity while preserving its proposed input guards.

There is a precise indexed residual for a longer initial run. The action
of `C` on the three-symbol word `130` has an exact period-16 orbit. Its
return section is

\[
 R=CCCAGBAEBEEBDABC,
\]

whose root permutation is `(1,0,3,2)`. If `Q_s` is the product of the
sections encountered during the first `s` steps of that orbit, then

\[
 (C^{16m+s})|_{130}=Q_sR^m,\qquad0\le s<16.         \tag{10}
\]

Thus

\[
 M_{2^{16m+s}122}=Q_sR^m C^3.
\]

The periodic three-symbol orbit is an exact finite action, but its return
retains the unbounded ordered word `R^m`. It cannot be discarded when
normalizing the endpoint source. This is the missing information in the
failed unrestricted erasure proposal, not a finite quotient of the full
state.

There is also a neutral section `C^3|_2=C^3`, with output `2`; `C^3` is
nonidentity. Hence strict descent under every unrestricted section is
impossible for this word. This does **not** refute a guarded descent using
the terminal `12a` condition and the target in (7): the neutral input
stream need not satisfy those conditions. No conclusion about whether
the generated automaton group is finite or infinite is claimed here.

## 5. Verification and the remaining obligation

[endpoint_section_machine.py](endpoint_section_machine.py) verifies the
complete local square, the raw-state aliases, the exact machine
minimization, full finite automaton bisimulations for the source rules,
the independent local coalescences, and the full period-16 return.
[endpoint_section_machine.json](endpoint_section_machine.json) saves the
certificate statistics, distinguishing witnesses, and source hashes.
The 336 short endpoint-prefix comparisons are implementation controls;
they are not the all-length justification for the identities.

The two source rules are genuine normalizations, and the seven-state
machine retains their ordered residual actions exactly. What remains
unproved is a well-founded reduction or separator that also handles
sources such as `22122...` while preserving **both** the hard-core
junction and the terminal `12a` pull. The finite machine and these two
rules do not establish that all sources reach a ruled-out normal form.
